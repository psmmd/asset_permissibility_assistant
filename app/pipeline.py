"""Prompt chain: extraction -> filtered retrieval -> decision, plus code-level guardrails."""

from dataclasses import dataclass

from app.decision import decide
from app.extraction import extract
from app.llm import Usage
from app.retrieval import retrieve
from app.schemas import Assessment, Decision, Rule


@dataclass
class PipelineResult:
    assessment: Assessment
    retrieved: list[Rule]  # kept for debugging and for measuring retrieval recall
    usage: Usage


def assess(text: str, model: str | None = None, top_k: int | None = None) -> PipelineResult:
    extraction, usage = extract(text, model=model)

    # Guardrail 1: without country and product we cannot filter, and unfiltered rules would mix regimes.
    missing = [f for f in ("country", "product") if getattr(extraction, f) is None]
    if missing:
        assessment = Assessment(
            decision=Decision.NEEDS_REVIEW,
            rule_ids=[],
            justification=f"The policy's {' and '.join(missing)} could not be determined from the request, "
            "so the applicable rules cannot be identified.",
            missing_info=missing,
            extracted=extraction,
        )
        return PipelineResult(assessment, [], usage)

    rules = retrieve(extraction, extraction.country, extraction.product, top_k=top_k)
    output, decision_usage = decide(text, extraction, rules, model=model)
    usage += decision_usage

    # Guardrail 2: every cited rule must be one we retrieved. Never return an invented rule.
    retrieved_ids = {r.rule_id for r in rules}
    invented = [rid for rid in output.rule_ids if rid not in retrieved_ids]
    if invented:
        output = output.model_copy(
            update={
                "decision": Decision.NEEDS_REVIEW,
                "rule_ids": [rid for rid in output.rule_ids if rid in retrieved_ids],
                "justification": f"Escalated: the model cited rules that were not retrieved ({', '.join(invented)}). "
                f"Original justification: {output.justification}",
            }
        )

    return PipelineResult(Assessment(**output.model_dump(), extracted=extraction), rules, usage)
