# Benchmark results

Generated 2026-10-28 with `uv run python -m benchmark.run`. 30 test cases, 1 run(s) per configuration. Raw rows: `results.jsonl`.

## Summary

| config                      | Decision accuracy   | Rule accuracy   | Retrieval recall   | Extraction accuracy   |   Avg rules cited |   Avg latency (s) |   p95 latency (s) |   Cost / query (USD) |   Errors |
|:----------------------------|:--------------------|:----------------|:-------------------|:----------------------|------------------:|------------------:|------------------:|---------------------:|---------:|
| claude-haiku-5-5 (top_k=6)  | 100%                | 100%            | 100%               | 99%                   |               1.9 |               5   |               7.2 |               0.0007 |        0 |
| claude-sonnet-5-5 (top_k=6) | 97%                 | 100%            | 100%               | 100%                  |               1.6 |               5.2 |               7.4 |               0.012  |        0 |
| claude-haiku-5-5 (top_k=14) | 97%                 | 100%            | 100%               | 99%                   |               2.1 |               5   |               7.3 |               0.0008 |        0 |

- **Decision accuracy**: decision equals the expected one (all cases).
- **Rule accuracy**: every expected rule ID is cited (cases not expected to be `needs_review`). Extra correct-but-general citations are not penalised.
- **Retrieval recall**: every expected rule ID is among the retrieved rules (same cases). Separates retrieval misses from reasoning errors.
- **Extraction accuracy**: share of the 4 extracted fields matching the label.
- **Cost / query**: Claude tokens x list price; output includes thinking tokens. Query embeddings (~50 tokens) are excluded as negligible.

## Baseline (before fixes)

| config                      | Decision accuracy   | Rule accuracy   | Retrieval recall   | Extraction accuracy   |   Avg rules cited |   Avg latency (s) |   p95 latency (s) |   Cost / query (USD) |   Errors |
|:----------------------------|:--------------------|:----------------|:-------------------|:----------------------|------------------:|------------------:|------------------:|---------------------:|---------:|
| claude-haiku-5-5 (top_k=6)  | 80%                 | 100%            | 100%               | 100%                  |               1.7 |               5.5 |               7.9 |               0.0007 |        0 |
| claude-sonnet-5-5 (top_k=6) | 90%                 | 100%            | 100%               | 100%                  |               1.6 |               5.2 |               7.2 |               0.0113 |        0 |

Changes between the baseline and the current results:

1. **Exclusion rules clarified** (rules 12 and 14.3): an exclusion applies only when the request indicates a link or personal use. Before, models escalated clean cases because no email confirms the absence of a link (8 of 9 baseline failures).
2. **Reference expansion in retrieval**: rules cited by ID inside retrieved rules are also fetched (e.g. LU-UL-05 depends on LU-UL-02). Before, the decision step could lack a definition it needed.

## Decision accuracy by category

| config                      | clear_permissible   | clear_not_permissible   | conditional   | needs_review   |
|:----------------------------|:--------------------|:------------------------|:--------------|:---------------|
| claude-haiku-5-5 (top_k=6)  | 100%                | 100%                    | 100%          | 100%           |
| claude-sonnet-5-5 (top_k=6) | 100%                | 100%                    | 89%           | 100%           |
| claude-haiku-5-5 (top_k=14) | 100%                | 88%                     | 100%          | 100%           |

## Extraction accuracy by field

| config                      | country   | product   | asset_type   | investor_classification   |
|:----------------------------|:----------|:----------|:-------------|:--------------------------|
| claude-haiku-5-5 (top_k=6)  | 97%       | 100%      | 100%         | 100%                      |
| claude-sonnet-5-5 (top_k=6) | 100%      | 100%      | 100%         | 100%                      |
| claude-haiku-5-5 (top_k=14) | 97%       | 100%      | 100%         | 100%                      |

## Failures

### claude-sonnet-5-5 (top_k=6)

**TC20** (conditional, wrong decision)
- Expected: `permissible` ['IT-UL-05']
- Got: `needs_review` ['IT-UL-05', 'IT-UL-14']
- Retrieved: ['IT-UL-05', 'IT-UL-04', 'IT-UL-10', 'IT-UL-01', 'IT-UL-14', 'IT-UL-03', 'IT-UL-02', 'IT-UL-12', 'IT-UL-13']
- Justification: IT-UL-05 permits ELTIFs for all investors, including retail, provided total ELTIF exposure is at most 10% of portfolio value after the investment. The request says the new holding is 6% and that there are no other alternatives, but it does not explicitly confirm there are no existing ELTIF holdings or the post-investment total. IT-UL-14 requires referral when exposure information a rule depends on is missing, and missing facts must not be assumed. No exclusion appears to apply.

### claude-haiku-5-5 (top_k=14)

**TC12** (clear_not_permissible, wrong decision)
- Expected: `not_permissible` ['IE-UL-12']
- Got: `needs_review` ['IE-UL-03', 'IE-UL-12', 'IE-UL-14']
- Retrieved: ['IE-UL-03', 'IE-UL-06', 'IE-UL-12', 'IE-UL-10', 'IE-UL-02', 'IE-UL-05', 'IE-UL-01', 'IE-UL-14', 'IE-UL-04', 'IE-UL-08', 'IE-UL-11', 'IE-UL-07', 'IE-UL-09', 'IE-UL-13']
- Justification: Corrib Foods plc is listed on the Dublin exchange, which would make it a permitted listed equity under IE-UL-03. However, the client and his wife hold about 12% between them, and IE-UL-12 excludes shares in issuers that the policyholder or close family hold at 10% or more. Whether that exclusion applies depends on the split of the holding and whether the rule aggregates spouse holdings, which the request does not establish, so the case is referred under IE-UL-14.
