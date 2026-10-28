# Data

All data in this folder is **100% synthetic**. Rule documents, companies, people and products are invented. Real places (cities, countries) appear only as context.

## Contents

| Path | What it is |
|---|---|
| `dimensions.yaml` | Canonical values: countries, products, asset types, investor classifications, decisions |
| `rules_template.md` | Structure every rule document follows |
| `rules/{CC}_{PP}.md` | One rules document per country–product pair (9 in total, 14 rules each) |
| `test_cases.jsonl` | 30 labelled test cases for the benchmark |

## Rule documents

- Each rule is a `###` heading starting with its ID (`LU-UL-05 — Non-UCITS and alternative funds`). This makes "one chunk per rule" a simple, deterministic split.
- The numbering is the same in every document: `01` general eligibility, `02` investor classification, `03`–`11` one rule per asset type, `12`–`13` exclusions, `14` escalation to review.
- Each asset rule has a `Status` of Permitted, Conditional or Not permitted.
- The same asset can get a different answer depending on country and product, by design. For example, crypto ETPs are conditional in LU-UL and LU-CB, prohibited in every Irish product and allowed only in IT-CB in Italy. This is why retrieval must filter by country and product.

### Main differences at a glance

| Asset type | LU UL / CB | LU RP | IE UL / CB | IE RP | IT UL / CB | IT RP |
|---|---|---|---|---|---|---|
| Listed equity | Regulated market or MTF, EEA/OECD | Regulated market only | Recognised exchange, EEA/OECD | Same | Regulated market in EU/EEA, UK, CH, US | Same |
| UCITS | Permitted | Permitted | Permitted | Permitted | Permitted | Permitted |
| Non-UCITS | Professional, ≤30% (UL) / ≤50% (CB) | Professional, ≤10% | Professional + EEA-authorised | Not permitted | ELTIF ≤10% for all; others professional ≤10% | ELTIF ≤10% only |
| Corporate bonds | IG; sub-IG professional | IG only | Listed (UL); unlisted professional (CB) | Listed and IG | IG; sub-IG professional ≤15% | IG only |
| Structured | Professional; retail if ≥90% protection and IG issuer | Not permitted | Listed (UL); unlisted professional (CB) | Not permitted | 100% protection and IG issuer | Not permitted |
| Crypto | ETP professional ≤5% (UL) / ≤10% (CB) | Not permitted | Not permitted | Not permitted | Not permitted (UL); ETP professional ≤5% (CB) | Not permitted |
| Direct real estate | Not permitted | Not permitted | Not permitted | Not permitted | Not permitted | Not permitted |

## Test cases (`test_cases.jsonl`)

One JSON object per line:

| Field | Meaning |
|---|---|
| `id` | `TC01` … `TC30` |
| `category` | `clear_permissible`, `clear_not_permissible`, `conditional` or `needs_review` |
| `input` | Free-text email from a relationship manager |
| `expected_decision` | `permissible`, `not_permissible` or `needs_review` |
| `expected_rule_ids` | Minimal set of rules that determine the decision (see below) |
| `expected_extracted` | Expected extraction: `country`, `product`, `asset_type`, `investor_classification` (`null` = not stated in the text) |
| `expected_missing_info` | For `needs_review` cases: the information that is missing |
| `notes` | Why this is the right answer, and the trap the case tests |

Labelling conventions:

- `expected_rule_ids` holds the **minimal** set of rules that settle the decision, normally the asset rule (or the exclusion that overrides it). Rule `02` is added only when the investor classification has to be derived from the wealth thresholds, not when the email states it explicitly.
- `needs_review` cases list the relevant rules plus rule `14`. The benchmark scores **only the decision** for these cases.
- `investor_classification` is extracted only when the email states it. If it has to be derived from figures (for example net financial assets), extraction returns `null` and the decision step applies rule `02`.

Distribution: 8 clear permissible, 8 clear not permissible, 9 conditional (6 resolve to permissible and 3 to not permissible), 5 needs review. Final decisions: 14 permissible, 11 not permissible, 5 needs review.
