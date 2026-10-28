# Asset Permissibility Rules — {Country name} / {Product name}

> Synthetic document created for a portfolio project. It does not describe any real insurer, product or regulation.

| Field | Value |
|---|---|
| Document ID | RULES-{CC}-{PP} |
| Country | {CC} ({Country name}) |
| Product | {PP} ({Product name}) |
| Policy type | Dedicated portfolio |
| Version | {x.y} |
| Effective date | {YYYY-MM-DD} |
| Owner | Investment Compliance |

## 1. Scope

This document sets out which assets may be held in the dedicated portfolio linked to a {product name} issued by the insurer's {country name} entity. Every rule has a unique ID and assessments must cite the IDs they rely on. Where no rule clearly applies, or the facts needed to apply a rule are missing, {CC}-{PP}-14 applies.

## 2. General rules

### {CC}-{PP}-01 — General eligibility
- **Applies to:** all assets

### {CC}-{PP}-02 — Investor classification
- **Applies to:** all rules that depend on investor classification

## 3. Asset rules

Each asset rule follows this shape:

### {CC}-{PP}-NN — {Asset type name}
- **Asset type:** `{asset_type key from dimensions.yaml}`
- **Status:** Permitted | Conditional | Not permitted

{Rule statement. Conditional rules list every condition explicitly.}

Fixed numbering, identical in every document:

| ID suffix | Asset type |
|---|---|
| 03 | `listed_equity` |
| 04 | `ucits_fund` |
| 05 | `non_ucits_fund` |
| 06 | `corporate_bond` |
| 07 | `government_bond` |
| 08 | `structured_product` |
| 09 | `crypto_asset` |
| 10 | `real_estate` |
| 11 | `cash` |

## 4. Exclusions

### {CC}-{PP}-12 — Assets connected to the policyholder
### {CC}-{PP}-13 — Personal-use and collectible assets

## 5. Escalation

### {CC}-{PP}-14 — Referral to Investment Compliance
