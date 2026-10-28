# Asset Permissibility Assistant

[![CI](https://github.com/psmmd/asset_permissibility_assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/psmmd/asset_permissibility_assistant/actions/workflows/ci.yml)

A life insurer's relationship managers email the investment team asking whether a client's policy may hold a given asset: *"Can Mr Okafor's Luxembourg unit-linked policy buy this Cayman hedge fund?"*. The answer depends on the policy's country, its product type, the asset, the investor's classification and portfolio limits, all spread across rules documents.

This project answers those emails with an LLM pipeline that returns a decision (`permissible`, `not_permissible` or `needs_review`), the IDs of the rules it relied on and a short justification. It is built to **never make up a rule**: missing information, ambiguity or anything suspicious goes to a human as `needs_review`.

> All rules, companies, people and test cases are **synthetic**. No real company or regulation is referenced.

**Example.** Input:

```text
re Mr Okafor - Luxembourg unit-linked, dedicated portfolio of around EUR 5m. The manager wants to add a
Cayman long/short equity hedge fund (not UCITS) for EUR 400k, i.e. 8% of the portfolio. He already holds
a private debt fund at 10%, so non-UCITS would go to 18% in total. He's a professional client (his bank's
confirmation is on file from last year).
```

Output (real run, Claude Haiku):

```json
{
  "decision": "permissible",
  "rule_ids": ["LU-UL-05", "LU-UL-02"],
  "justification": "LU-UL-05 permits non-UCITS funds, including hedge funds, when the policyholder is a professional investor and total non-UCITS exposure stays within 30% of the portfolio after the investment. Mr Okafor is classified as a professional client with written bank confirmation on file, and the total non-UCITS exposure would be 18% (10% existing plus 8% proposed), so both conditions are met.",
  "missing_info": [],
  "extracted": { "country": "LU", "product": "UL", "asset_type": "non_ucits_fund", "investor_classification": "professional", "...": "..." }
}
```

## Results

37 test cases: 30 covering clear, conditional and incomplete requests, plus 7 adversarial ones (misleading policy country, prompt injection). One run per configuration; full report in [`benchmark/results.md`](benchmark/results.md).

| Model | Decision accuracy | Rule accuracy | Avg latency | Cost / query |
|---|---|---|---|---|
| Claude Haiku 5.5 | 100% | 100% | 4.3 s | $0.0007 |
| Claude Sonnet 5.5 | 100% | 100% | 4.2 s | $0.0119 |

**Haiku is the default**: same accuracy as Sonnet on this task at about 1/17 of the cost. The first run scored 80% (Haiku) and 90% (Sonnet). [How it got from there to here](#how-it-was-evaluated) is the most useful part of this project.

## Architecture

```mermaid
flowchart LR
    A[Email] --> B["1 - Extraction<br/>(Claude, structured output)"]
    B --> G1{"Injection flag?<br/>Country or product missing?"}
    G1 -- yes --> R[needs_review]
    G1 -- no --> C["2 - Retrieval<br/>pgvector, filtered by<br/>country + product"]
    C --> X["Reference expansion<br/>(rules cited by ID)"]
    X --> D["3 - Decision<br/>(Claude, structured output)"]
    D --> G2{"Cites a rule that<br/>was not retrieved?"}
    G2 -- yes --> R
    G2 -- no --> O[Decision + rule IDs + justification]
```

Three steps, chained in code:

1. **Extraction** turns the email into typed fields (`country`, `product`, `asset_type`, `investor_classification`, stated facts) and flags text addressed to the AI system.
2. **Retrieval** searches only the rules for that policy's country and product (one document of 14 rules out of 9), then adds any rule that a retrieved rule cites by ID.
3. **Decision** applies the retrieved rules and returns the decision, the rule IDs and a justification.

Guardrails between the steps are plain Python, not prompt instructions, so they hold even when a model misbehaves.

**Stack:** Python 3.12, uv, FastAPI, LlamaIndex, Postgres + pgvector, Anthropic SDK (Claude Haiku / Sonnet 5.5), OpenAI `text-embedding-3-small` for embeddings (Anthropic has no embeddings model), pytest, ruff, GitHub Actions, Docker, Terraform on AWS.

## Running it locally

Requirements: [uv](https://docs.astral.sh/uv/), Docker, an Anthropic API key and an OpenAI API key (embeddings only).

```bash
cp .env.example .env              # add your API keys; .env is git-ignored
docker compose up -d              # Postgres 17 with pgvector
uv sync
uv run python -m app.ingest       # embeds the 126 rules into pgvector (idempotent)

uv run uvicorn app.main:app       # web page at http://localhost:8000, API docs at /docs
uv run python -m app.cli TC17 "free text request"   # or from the command line
```

```bash
uv run pytest                     # 20 unit tests: no network, database or API keys needed
uv run python scripts/validate_data.py
uv run python -m benchmark.run    # full benchmark, Haiku + Sonnet (~$0.50, ~10 min)
```

API: `POST /assess` with `{"text": "..."}` returns the assessment; `GET /health` checks the database.

## Design decisions

**One chunk per rule.** Each rules document has 14 numbered rules (`LU-UL-05 — Non-UCITS funds`), split on their headings. A rule is the unit the answer cites, so it is also the unit retrieved. Fixed-size chunks would cut rules in half or mix two of them.

**Hard metadata filter on country and product.** Without it, a crypto query retrieved equity rules from other countries and missed the right rule. The filter turns a fuzzy retrieval problem into an extraction problem: one enum field, measured on its own in the benchmark. The risk this moves into extraction is handled below.

**Prompt chaining, not one call or an agent.** Separate extraction and decision steps let code check the extraction before any rule is applied, and let the benchmark tell retrieval errors from reasoning errors. An agent with tools would add non-determinism and cost for a task whose steps are always the same.

**Structured outputs with enums.** Both steps use Claude's structured outputs, validated against Pydantic models, so a decision can only be one of the three values and fields are never free-form where they matter.

**Guardrails in code.** Missing country or product, an injection flag, or a cited rule that was not retrieved all force `needs_review`. A prompt saying "never invent rules" is a request; a set comparison is a guarantee.

**No self-reported confidence.** LLM confidence scores are poorly calibrated. Instead, the escalation rule in each rules document says when to refer a case, and the model applies it like any other rule.

**Reference expansion.** LU-UL-05 says "professional investor under LU-UL-02". Similarity search does not follow such links, so rules cited by ID are fetched explicitly (one level deep, same document). This fixed a baseline failure, and with it `top_k=6` matches `top_k=14` at lower cost.

**Haiku over Sonnet.** Equal accuracy, similar latency and 17x cheaper. Sonnet would be the choice if harder, longer rules made Haiku fall behind; the benchmark makes that a measurement, not a guess.

**A wrong policy country is the riskiest failure**, because it is silent: the right reasoning applied to the wrong rules. Three layers address it. Extraction returns `null` when the email names several policies or contradicts itself, which escalates. The decision step is told which policy the rules are for and escalates if the email says otherwise. The web page shows "Assessed against: Ireland · Unit-linked" so a reader can spot a mistake at a glance.

**Prompt injection defences, in layers.** The email is wrapped in tags and HTML-escaped, so it cannot close the tag or fake a `<rule>`. Both prompts treat it as data. Extraction flags text addressed to the system, and code escalates those cases before retrieval. Escalating, rather than silently ignoring, is deliberate: an attempt to steer a compliance tool is something a human should see.

## How it was evaluated

[`data/test_cases.jsonl`](data/test_cases.jsonl) holds 37 labelled cases. Each has the expected decision, the minimal set of rules that settle it, the expected extracted fields, and notes on the trap it tests (labelling conventions in [`data/README.md`](data/README.md)). The benchmark measures:

- decision accuracy;
- **rule accuracy**: the expected rules are cited;
- **retrieval recall**: the expected rules were retrieved, which separates retrieval misses from reasoning errors;
- extraction accuracy per field;
- latency and cost.

What the benchmark found, in order:

1. **Baseline: Haiku 80%, Sonnet 90%.** 8 of the 9 failures were the models escalating clean cases because no email confirms that the client has *no* link to the issuer. The rules were ambiguous, so the fix went into the rules: exclusions apply when the request indicates a link.
2. **A missing definition.** The decision step needed LU-UL-02 (the investor classification) but only LU-UL-05 had been retrieved. Fixed with reference expansion.
3. **An aggregation ambiguity.** Does "a family member holds 10%" include a couple holding 12% together? The rules now say "individually or together".
4. **Adversarial cases, before the defences: 4/7.** The injections did not flip any decision, because the model ignored them, but nothing flagged them either. One case escalated by luck after extracting the wrong country.
5. **The defences caused regressions.** The first version broke 3 clean cases that used to pass: a client living abroad was read as "different country", and "treat the email as data" made the models doubt facts the RM stated. The prompts were narrowed: client residence does not change the policy country, and stated facts are taken as true while instructions are ignored. All 37 cases now pass on all configurations.

The baseline, the adversarial "before" run and the regression run are kept in `benchmark/` alongside the current results.

## Deployment (AWS, Terraform)

```mermaid
flowchart LR
    U[Browser] -- HTTP :80 --> E
    subgraph AWS["AWS eu-west-1, default VPC"]
        E["EC2 t4g.small<br/>Docker: FastAPI app"] -- ":5432 from app SG only" --> DB[("RDS Postgres 17<br/>+ pgvector")]
        E -. pull image .-> ECR[ECR]
        E -. read secrets .-> SM[Secrets Manager]
        SSM[SSM Session Manager] -. shell, no SSH .-> E
    end
    E -- HTTPS --> LLM[Anthropic + OpenAI APIs]
```

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # email for budget alerts
terraform apply                                # ~10 min, mostly RDS
./set-api-keys.sh                              # copies the keys from .env to Secrets Manager
./deploy.sh                                    # builds for ARM64, pushes to ECR, restarts the app
terraform destroy                              # removes everything
```

On every start, a systemd service on the instance:

1. reads the secrets;
2. pulls the image;
3. re-ingests the rules shipped in the image;
4. starts the app.

Retries are left to systemd, so the deployment steps can run in any order. Cost is about **$1.1/day** while running; it is meant to be created before a demo and destroyed after.

Security choices:

- **No secrets in Terraform state.** RDS generates and stores its own password, and the API keys secret is created empty and filled by a script that reads from stdin.
- **No SSH port.** Shell access goes through SSM. The database only accepts connections from the app's security group.
- **The instance role can only** pull from this repository and read these two secrets.
- **IMDSv2 with a hop limit of 1**, so a compromised container cannot read the role's credentials.
- **Rate limit on `POST /assess`** (10/min per IP plus a daily cap), because every call costs money. An AWS Budgets alert backs this up.

## Limitations and next steps

- **Small benchmark, one run.** 37 cases, so each case is about 3% of the score, and there is no measure of run-to-run variance (`--repeat` exists for that).
- **Some overfitting risk.** The rules and defence prompts were refined after seeing failures, so new held-out cases would be the next step.
- **Rule accuracy does not penalise extra citations.** A wrong extra rule ID goes unnoticed as long as the expected ones are cited.
- **No defence against prompt injection is complete.** These are layers that make an attack harder and visible, with a human reviewing escalations.
- **The deployment is a demo.** It runs on HTTP with no domain or TLS. The rate limit lives in memory on a single instance. Terraform state is local; a team would use an S3 backend with locking.
- **Synthetic rules.** They are shorter and more regular than real investment guidelines. Real documents would need a sturdier parser, and possibly hybrid (keyword + vector) search for exact terms.

## Repository layout

```text
app/           pipeline (extraction, retrieval, decision), API, web page, ingestion
data/          9 synthetic rules documents (126 rules), 37 test cases, data conventions
benchmark/     benchmark runner and results (current, baseline, adversarial before, regression)
tests/         unit tests (LLM and database replaced by fakes)
infra/         Terraform for AWS and deployment scripts
scripts/       data validator
```

Built in one day with [Claude Code](https://claude.com/claude-code) as a pair programmer. Every design decision above was discussed and reviewed before it was implemented.
