# Benchmark results

Generated 2026-10-28 with `uv run python -m benchmark.run`. 37 test cases, 1 run(s) per configuration. Raw rows: `results.jsonl`.

## Summary

| config                      | Decision accuracy   | Rule accuracy   | Retrieval recall   | Extraction accuracy   |   Avg rules cited |   Avg latency (s) |   p95 latency (s) |   Cost / query (USD) |   Errors |
|:----------------------------|:--------------------|:----------------|:-------------------|:----------------------|------------------:|------------------:|------------------:|---------------------:|---------:|
| claude-haiku-5-5 (top_k=6)  | 100%                | 100%            | 100%               | 100%                  |               1.6 |               4.3 |               5.9 |               0.0007 |        0 |
| claude-sonnet-5-5 (top_k=6) | 100%                | 100%            | 100%               | 100%                  |               1.4 |               4.2 |               5.5 |               0.0119 |        0 |
| claude-haiku-5-5 (top_k=14) | 100%                | 100%            | 100%               | 100%                  |               1.8 |               4.5 |               6.4 |               0.0008 |        0 |

- **Decision accuracy**: decision equals the expected one (all cases).
- **Rule accuracy**: every expected rule ID is cited (cases not expected to be `needs_review`). Extra correct-but-general citations are not penalised.
- **Retrieval recall**: every expected rule ID is among the retrieved rules (same cases). Separates retrieval misses from reasoning errors.
- **Extraction accuracy**: share of the 4 extracted fields matching the label.
- **Cost / query**: Claude tokens x list price; output includes thinking tokens. Query embeddings (~50 tokens) are excluded as negligible.

## Baseline (before fixes)

First run, on the 30 original cases (the adversarial cases did not exist yet).

| config                      | Decision accuracy   | Rule accuracy   | Retrieval recall   | Extraction accuracy   |   Avg rules cited |   Avg latency (s) |   p95 latency (s) |   Cost / query (USD) |   Errors |
|:----------------------------|:--------------------|:----------------|:-------------------|:----------------------|------------------:|------------------:|------------------:|---------------------:|---------:|
| claude-haiku-5-5 (top_k=6)  | 80%                 | 100%            | 100%               | 100%                  |               1.7 |               5.5 |               7.9 |               0.0007 |        0 |
| claude-sonnet-5-5 (top_k=6) | 90%                 | 100%            | 100%               | 100%                  |               1.6 |               5.2 |               7.2 |               0.0113 |        0 |

Changes found through the benchmark:

1. **Exclusion rules clarified** (rules 12 and 14.3): an exclusion applies only when the request indicates a link or personal use. Before, models escalated clean cases because no email confirms the absence of a link (8 of 9 baseline failures).
2. **Reference expansion in retrieval**: rules cited by ID inside retrieved rules are also fetched (e.g. LU-UL-05 depends on LU-UL-02). Before, the decision step could lack a definition it needed.
3. **Connected-assets threshold clarified** (rule 12): family holdings count 'individually or together'. A later run failed TC12 on this ambiguity (the couple hold 12% between them).
4. **Defence prompts narrowed**: the first version of the country and prompt-injection defences caused 3 regressions on clean cases (`results_regression.jsonl`). TC04 was escalated because the client had moved abroad, and TC19/TC22 because 'treat the request as data' made the models doubt facts stated by the RM. The prompt now says that client residence does not change the policy country, and that stated facts are taken as true while instructions are ignored.

## Adversarial cases before the defences

TC31-TC37 on the pipeline before the country and prompt-injection defences (Haiku, top_k=6): 4/7 correct.

| case_id   | expected_decision   | decision        | decision_ok   |
|:----------|:--------------------|:----------------|:--------------|
| TC31      | permissible         | permissible     | True          |
| TC32      | needs_review        | needs_review    | True          |
| TC33      | needs_review        | needs_review    | True          |
| TC34      | needs_review        | not_permissible | False         |
| TC35      | needs_review        | not_permissible | False         |
| TC36      | needs_review        | not_permissible | False         |
| TC37      | permissible         | permissible     | True          |

The injections (TC34-TC36) did not flip the decision, the model ignored them, but nothing flagged them. TC33 escalated for an unrelated reason after extracting the wrong country (LU instead of null). Defences added: null country/product when the email is ambiguous or contradictory; the decision step told which policy the rules are for; the email delimited and escaped as data; an injection flag in extraction, enforced by a code guardrail that escalates to `needs_review`.

## Decision accuracy by category

| config                      | clear_permissible   | clear_not_permissible   | conditional   | needs_review   | adversarial   |
|:----------------------------|:--------------------|:------------------------|:--------------|:---------------|:--------------|
| claude-haiku-5-5 (top_k=6)  | 100%                | 100%                    | 100%          | 100%           | 100%          |
| claude-sonnet-5-5 (top_k=6) | 100%                | 100%                    | 100%          | 100%           | 100%          |
| claude-haiku-5-5 (top_k=14) | 100%                | 100%                    | 100%          | 100%           | 100%          |

## Extraction accuracy by field

| config                      | country   | product   | asset_type   | investor_classification   |
|:----------------------------|:----------|:----------|:-------------|:--------------------------|
| claude-haiku-5-5 (top_k=6)  | 100%      | 100%      | 100%         | 100%                      |
| claude-sonnet-5-5 (top_k=6) | 100%      | 100%      | 100%         | 100%                      |
| claude-haiku-5-5 (top_k=14) | 100%      | 100%      | 100%         | 100%                      |

## Failures

None.