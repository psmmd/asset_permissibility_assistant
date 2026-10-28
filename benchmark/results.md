# Benchmark results

Generated 2026-10-28 with `uv run python -m benchmark.run`. 30 test cases, 1 run(s) per configuration. Raw rows: `results.jsonl`.

## Summary

| config                      | Decision accuracy   | Rule accuracy   | Retrieval recall   | Extraction accuracy   |   Avg rules cited |   Avg latency (s) |   p95 latency (s) |   Cost / query (USD) |   Errors |
|:----------------------------|:--------------------|:----------------|:-------------------|:----------------------|------------------:|------------------:|------------------:|---------------------:|---------:|
| claude-haiku-5-5 (top_k=6)  | 80%                 | 100%            | 100%               | 100%                  |               1.7 |               5.5 |               7.9 |               0.0007 |        0 |
| claude-sonnet-5-5 (top_k=6) | 90%                 | 100%            | 100%               | 100%                  |               1.6 |               5.2 |               7.2 |               0.0113 |        0 |

- **Decision accuracy**: decision equals the expected one (all cases).
- **Rule accuracy**: every expected rule ID is cited (cases not expected to be `needs_review`). Extra correct-but-general citations are not penalised.
- **Retrieval recall**: every expected rule ID is among the retrieved rules (same cases). Separates retrieval misses from reasoning errors.
- **Extraction accuracy**: share of the 4 extracted fields matching the label.
- **Cost / query**: Claude tokens x list price; output includes thinking tokens. Query embeddings (~50 tokens) are excluded as negligible.

## Decision accuracy by category

| config                      | clear_permissible   | clear_not_permissible   | conditional   | needs_review   |
|:----------------------------|:--------------------|:------------------------|:--------------|:---------------|
| claude-haiku-5-5 (top_k=6)  | 50%                 | 100%                    | 78%           | 100%           |
| claude-sonnet-5-5 (top_k=6) | 75%                 | 100%                    | 89%           | 100%           |

## Extraction accuracy by field

| config                      | country   | product   | asset_type   | investor_classification   |
|:----------------------------|:----------|:----------|:-------------|:--------------------------|
| claude-haiku-5-5 (top_k=6)  | 100%      | 100%      | 100%         | 100%                      |
| claude-sonnet-5-5 (top_k=6) | 100%      | 100%      | 100%         | 100%                      |

## Failures

### claude-haiku-5-5 (top_k=6)

**TC03** (clear_permissible, wrong decision)
- Expected: `permissible` ['IT-RP-03']
- Got: `needs_review` ['IT-RP-03', 'IT-RP-12']
- Retrieved: ['IT-RP-03', 'IT-RP-12', 'IT-RP-05', 'IT-RP-01', 'IT-RP-10', 'IT-RP-08']
- Justification: Shares of Lunetta Meccanica SpA are admitted to trading on the Milan regulated market, an EU regulated market, so IT-RP-03 permits listed equities in principle. However, IT-RP-12 prohibits securities of any company in which the policyholder, insured person, a beneficiary or a close family member holds 10% or more of capital or voting rights or exercises control, and the request does not say whether this applies.

**TC05** (clear_permissible, wrong decision)
- Expected: `permissible` ['IE-UL-06']
- Got: `needs_review` ['IE-UL-06', 'IE-UL-12']
- Retrieved: ['IE-UL-06', 'IE-UL-07', 'IE-UL-12', 'IE-UL-11', 'IE-UL-10', 'IE-UL-05']
- Justification: IE-UL-06 permits corporate bonds listed on a recognised stock exchange regardless of credit rating, and the bond is listed on the Dublin exchange, so the rating concern does not block it. However, IE-UL-12 excludes securities of companies in which the policyholder, insured, beneficiaries or close family hold 10% or more or exercise control, and the request does not confirm ownership of Harbourline Logistics plc.

**TC06** (clear_permissible, wrong decision)
- Expected: `permissible` ['LU-CB-06']
- Got: `needs_review` ['LU-CB-06', 'LU-CB-12']
- Retrieved: ['LU-CB-06', 'LU-CB-07', 'LU-CB-03', 'LU-CB-08', 'LU-CB-12', 'LU-CB-05']
- Justification: The bond is rated BBB+ by a major agency, which meets the investment-grade condition in LU-CB-06 for corporate bonds. However, the exclusion in LU-CB-12 overrides asset rules, and the request does not state whether the Andersens, their family or beneficiaries hold 10% or more of Kestrel Energy AG or control it, so the exclusion cannot be ruled out.

**TC08** (clear_permissible, wrong decision)
- Expected: `permissible` ['IE-RP-03']
- Got: `needs_review` ['IE-RP-03', 'IE-RP-12']
- Retrieved: ['IE-RP-03', 'IE-RP-10', 'IE-RP-12', 'IE-RP-05', 'IE-RP-01', 'IE-RP-04']
- Justification: Shares in a REIT listed on the London Stock Exchange, a recognised exchange in an OECD country, are permitted as listed equities under IE-RP-03, and the proposal is an indirect route to UK warehouses, which is consistent with the IE-RP-10 prohibition on direct property. The connected-person exclusion in IE-RP-12 depends on whether the policyholder, insured person, beneficiaries or close family hold 10% or more of Bramblegate or control it, and the request does not state this, so it cannot be ruled out.

**TC17** (conditional, wrong decision)
- Expected: `permissible` ['LU-UL-05']
- Got: `needs_review` ['LU-UL-05', 'LU-UL-01']
- Retrieved: ['LU-UL-05', 'LU-UL-04', 'LU-UL-09', 'LU-UL-10', 'LU-UL-12', 'LU-UL-01']
- Justification: LU-UL-05 permits non-UCITS funds only for a professional investor under LU-UL-02 and where total non-UCITS exposure stays at or below 30%. After the investment, exposure would be 18%, which is within the limit, but the professional classification rests on a bank confirmation from last year and LU-UL-02 was not provided, so it cannot be verified against the classification criteria.

**TC23** (conditional, wrong decision)
- Expected: `permissible` ['LU-UL-08']
- Got: `needs_review` ['LU-UL-08', 'LU-UL-12']
- Retrieved: ['LU-UL-08', 'LU-UL-06', 'LU-UL-07', 'LU-UL-02', 'LU-UL-12', 'LU-UL-11']
- Justification: The note meets the retail conditions of LU-UL-08: 95% capital protection is above the 90% minimum, and an A rating is investment grade. However, LU-UL-12 prohibits securities issued by companies connected to the policyholder, insured, beneficiary or close family, and the request gives no information on whether the issuer is connected. That ownership fact must be confirmed before the exclusion can be ruled out.

### claude-sonnet-5-5 (top_k=6)

**TC03** (clear_permissible, wrong decision)
- Expected: `permissible` ['IT-RP-03']
- Got: `needs_review` ['IT-RP-03', 'IT-RP-12']
- Retrieved: ['IT-RP-03', 'IT-RP-12', 'IT-RP-10', 'IT-RP-08', 'IT-RP-01', 'IT-RP-05']
- Justification: Shares on the Milan regulated market satisfy IT-RP-03, and IT-RP-01 conditions are assumed met. However, IT-RP-12 excludes securities of a company in which the policyholder, insured, a beneficiary or close family holds 10% or more or exercises control, and the request says nothing about any such connection to Lunetta Meccanica SpA. This cannot be assumed away, so it must be confirmed before approval.

**TC05** (clear_permissible, wrong decision)
- Expected: `permissible` ['IE-UL-06']
- Got: `needs_review` ['IE-UL-06', 'IE-UL-12']
- Retrieved: ['IE-UL-06', 'IE-UL-07', 'IE-UL-12', 'IE-UL-03', 'IE-UL-10', 'IE-UL-11']
- Justification: IE-UL-06 permits listed corporate bonds whatever their rating, and the Dublin listing is stated, so the missing rating is not an obstacle. Dublin is presumably a recognised exchange but this is not confirmed in the request. The exclusion in IE-UL-12 overrides asset rules, and the request says nothing about whether the policyholder, insured person, beneficiary or close family hold 10% or more of Harbourline Logistics plc or control it, so the exclusion cannot be ruled out.

**TC17** (conditional, wrong decision)
- Expected: `permissible` ['LU-UL-05']
- Got: `needs_review` ['LU-UL-05']
- Retrieved: ['LU-UL-05', 'LU-UL-04', 'LU-UL-09', 'LU-UL-10', 'LU-UL-01', 'LU-UL-12']
- Justification: LU-UL-05 allows non-UCITS funds only for professional investors as defined in LU-UL-02, with total non-UCITS exposure at or below 30% after the purchase. The 18% exposure meets the limit, but LU-UL-02 was not provided, so it cannot be confirmed that a bank confirmation from last year satisfies the professional investor definition. It is also unclear whether the exclusion in LU-UL-12 applies, because nothing shows whether the fund is connected to the policyholder.
