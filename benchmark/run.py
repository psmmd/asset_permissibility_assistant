"""Run the 30 test cases against one or more models and write benchmark/results.md.

  uv run python -m benchmark.run                                   # Haiku and Sonnet, top_k from settings
  uv run python -m benchmark.run --models claude-haiku-5-5 --top-k 14 --append
  uv run python -m benchmark.run --report-only                     # rebuild results.md from results.jsonl

Cases run sequentially so that latency is not distorted by concurrency or rate limits.
"""

import argparse
import json
import time
from datetime import date
from pathlib import Path

import pandas as pd

from app.config import settings
from app.pipeline import assess

ROOT = Path(__file__).resolve().parent.parent
TEST_CASES = ROOT / "data" / "test_cases.jsonl"
RAW = Path(__file__).parent / "results.jsonl"
BASELINE = Path(__file__).parent / "results_baseline.jsonl"  # first run, before the fixes described below
ADVERSARIAL_BEFORE = Path(__file__).parent / "results_adversarial_before.jsonl"  # before the defences
REPORT = Path(__file__).parent / "results.md"

# USD per million tokens (input, output). Output includes thinking tokens.
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
}
EXTRACTED_FIELDS = ["country", "product", "asset_type", "investor_classification"]


def run_case(case: dict, model: str, top_k: int, run: int) -> dict:
    row = {
        "config": f"{model} (top_k={top_k})",
        "model": model,
        "top_k": top_k,
        "run": run,
        "case_id": case["id"],
        "category": case["category"],
        "expected_decision": case["expected_decision"],
        "expected_rule_ids": case["expected_rule_ids"],
        "expected_extracted": case["expected_extracted"],
        "decision": None,
        "rule_ids": [],
        "retrieved_ids": [],
        "extracted": None,
        "justification": "",
        "latency_s": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "error": None,
    }
    start = time.perf_counter()
    try:
        result = assess(case["input"], model=model, top_k=top_k)
    except Exception as exc:  # noqa: BLE001 - a failed case counts as wrong, the benchmark keeps going
        row["error"] = f"{type(exc).__name__}: {exc}"
        return row
    a = result.assessment
    row.update(
        latency_s=time.perf_counter() - start,
        decision=a.decision.value,
        rule_ids=a.rule_ids,
        justification=a.justification,
        retrieved_ids=[r.rule_id for r in result.retrieved],
        extracted=a.extracted.model_dump(mode="json"),
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens,
    )
    return row


def score(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-case correctness columns."""
    df = df.copy()
    df["decision_ok"] = df["decision"] == df["expected_decision"]
    # Rules and retrieval are scored only where a definitive decision is expected.
    decided = df["expected_decision"] != "needs_review"
    df["rules_ok"] = [
        set(e) <= set(c) if d else None for e, c, d in zip(df["expected_rule_ids"], df["rule_ids"], decided)
    ]
    df["retrieval_ok"] = [
        set(e) <= set(r) if d else None
        for e, r, d in zip(df["expected_rule_ids"], df["retrieved_ids"], decided)
    ]
    for field in EXTRACTED_FIELDS:
        df[f"{field}_ok"] = [
            (x or {}).get(field) == e[field] for x, e in zip(df["extracted"], df["expected_extracted"])
        ]
    df["extraction_ok"] = df[[f"{f}_ok" for f in EXTRACTED_FIELDS]].mean(axis=1)
    price_in, price_out = zip(*(PRICES.get(m, (float("nan"),) * 2) for m in df["model"]))
    df["cost_usd"] = (
        df["input_tokens"] * pd.Series(price_in, index=df.index)
        + df["output_tokens"] * pd.Series(price_out, index=df.index)
    ) / 1e6
    df["n_cited"] = df["rule_ids"].map(len)
    return df


def pct(x: float) -> str:
    return f"{x:.0%}"


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    by = df.groupby("config", sort=False)
    return pd.DataFrame(
        {
            "Decision accuracy": by["decision_ok"].mean().map(pct),
            "Rule accuracy": by["rules_ok"].apply(lambda s: s.dropna().astype(bool).mean()).map(pct),
            "Retrieval recall": by["retrieval_ok"].apply(lambda s: s.dropna().astype(bool).mean()).map(pct),
            "Extraction accuracy": by["extraction_ok"].mean().map(pct),
            "Avg rules cited": by["n_cited"].mean().map("{:.1f}".format),
            "Avg latency (s)": by["latency_s"].mean().map("{:.1f}".format),
            "p95 latency (s)": by["latency_s"].quantile(0.95).map("{:.1f}".format),
            "Cost / query (USD)": by["cost_usd"].mean().map("{:.4f}".format),
            "Errors": by["error"].apply(lambda s: s.notna().sum()),
        }
    )


def baseline_section() -> list[str]:
    if not BASELINE.exists():
        return []
    baseline = summary_table(score(pd.read_json(BASELINE, lines=True)))
    return [
        "## Baseline (before fixes)",
        "",
        "First run, on the 30 original cases (the adversarial cases did not exist yet).",
        "",
        baseline.to_markdown(),
        "",
        "Changes found through the benchmark:",
        "",
        (
            "1. **Exclusion rules clarified** (rules 12 and 14.3): an exclusion applies only when the request "
            "indicates a link or personal use. Before, models escalated clean cases because no email confirms the "
            "absence of a link (8 of 9 baseline failures)."
        ),
        (
            "2. **Reference expansion in retrieval**: rules cited by ID inside retrieved rules are also fetched "
            "(e.g. LU-UL-05 depends on LU-UL-02). Before, the decision step could lack a definition it needed."
        ),
        (
            "3. **Connected-assets threshold clarified** (rule 12): family holdings count 'individually or "
            "together'. A later run failed TC12 on this ambiguity (the couple hold 12% between them)."
        ),
        (
            "4. **Defence prompts narrowed**: the first version of the country and prompt-injection defences "
            "caused 3 regressions on clean cases (`results_regression.jsonl`). TC04 was escalated because the "
            "client had moved abroad, and TC19/TC22 because 'treat the request as data' made the models doubt "
            "facts stated by the RM. The prompt now says that client residence does not change the policy "
            "country, and that stated facts are taken as true while instructions are ignored."
        ),
        "",
    ]


def adversarial_section() -> list[str]:
    if not ADVERSARIAL_BEFORE.exists():
        return []
    before = score(pd.read_json(ADVERSARIAL_BEFORE, lines=True))
    table = before[["case_id", "expected_decision", "decision", "decision_ok"]].set_index("case_id")
    return [
        "## Adversarial cases before the defences",
        "",
        (
            f"TC31-TC37 on the pipeline before the country and prompt-injection defences "
            f"(Haiku, top_k=6): {before['decision_ok'].sum()}/{len(before)} correct."
        ),
        "",
        table.to_markdown(),
        "",
        (
            "The injections (TC34-TC36) did not flip the decision, the model ignored them, but nothing flagged "
            "them. TC33 escalated for an unrelated reason after extracting the wrong country (LU instead of "
            "null). Defences added: null country/product when the email is ambiguous or contradictory; the "
            "decision step told which policy the rules are for; the email delimited and escaped as data; an "
            "injection flag in extraction, enforced by a code guardrail that escalates to `needs_review`."
        ),
        "",
    ]


def build_report(df: pd.DataFrame) -> str:
    df = score(df)
    by = df.groupby("config", sort=False)
    summary = summary_table(df)
    by_category = df.pivot_table(
        index="config", columns="category", values="decision_ok", aggfunc="mean", sort=False
    ).map(pct)
    by_field = by[[f"{f}_ok" for f in EXTRACTED_FIELDS]].mean().map(pct)
    by_field.columns = EXTRACTED_FIELDS

    n_runs = df.groupby("config")["run"].nunique().max()
    lines = [
        "# Benchmark results",
        "",
        (
            f"Generated {date.today()} with `uv run python -m benchmark.run`. "
            f"{df['case_id'].nunique()} test cases, {n_runs} run(s) per configuration. Raw rows: `results.jsonl`."
        ),
        "",
        "## Summary",
        "",
        summary.to_markdown(),
        "",
        "- **Decision accuracy**: decision equals the expected one (all cases).",
        (
            "- **Rule accuracy**: every expected rule ID is cited (cases not expected to be `needs_review`). "
            "Extra correct-but-general citations are not penalised."
        ),
        (
            "- **Retrieval recall**: every expected rule ID is among the retrieved rules (same cases). "
            "Separates retrieval misses from reasoning errors."
        ),
        "- **Extraction accuracy**: share of the 4 extracted fields matching the label.",
        (
            "- **Cost / query**: Claude tokens x list price; output includes thinking tokens. "
            "Query embeddings (~50 tokens) are excluded as negligible."
        ),
        "",
        *baseline_section(),
        *adversarial_section(),
        "## Decision accuracy by category",
        "",
        by_category.to_markdown(),
        "",
        "## Extraction accuracy by field",
        "",
        by_field.to_markdown(),
        "",
        "## Failures",
        "",
    ]
    rules_wrong = df["rules_ok"].map(lambda ok: ok is False)  # None means not scored
    failures = df[~df["decision_ok"] | rules_wrong]
    if failures.empty:
        lines.append("None.")
    for config, group in failures.groupby("config", sort=False):
        lines += [f"### {config}", ""]
        for _, r in group.iterrows():
            what = "decision" if not r["decision_ok"] else "rules"
            lines += [
                f"**{r['case_id']}** ({r['category']}, wrong {what}{f', run {r.run}' if n_runs > 1 else ''})",
                f"- Expected: `{r['expected_decision']}` {r['expected_rule_ids']}",
                f"- Got: `{r['decision']}` {r['rule_ids']}",
                f"- Retrieved: {r['retrieved_ids']}",
                f"- Justification: {r['error'] if pd.notna(r['error']) else r['justification']}",
                "",
            ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=list(PRICES))
    parser.add_argument("--top-k", type=int, default=settings.retrieval_top_k)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--cases", nargs="+", help="Subset of case IDs, e.g. TC01 TC13")
    parser.add_argument("--append", action="store_true", help="Add to results.jsonl instead of overwriting")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    if not args.report_only:
        cases = [json.loads(line) for line in TEST_CASES.read_text().splitlines()]
        if args.cases:
            cases = [c for c in cases if c["id"] in args.cases]
        with RAW.open("a" if args.append else "w") as f:
            for model in args.models:
                for run in range(1, args.repeat + 1):
                    for case in cases:
                        row = run_case(case, model, args.top_k, run)
                        f.write(json.dumps(row) + "\n")
                        f.flush()
                        status = "OK " if row["decision"] == case["expected_decision"] else "BAD"
                        latency = f"{row['latency_s']:.1f}s" if row["latency_s"] else "error"
                        print(f"{model} run {run} {case['id']} {status} {row['decision']} ({latency})")

    df = pd.read_json(RAW, lines=True)
    REPORT.write_text(build_report(df))
    print(f"Report written to {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
