# Asset Permissibility Rules — Luxembourg / Unit-Linked Investment Policy

> Synthetic document created for a portfolio project. It does not describe any real insurer, product or regulation.

| Field | Value |
|---|---|
| Document ID | RULES-LU-UL |
| Country | LU (Luxembourg) |
| Product | UL (Unit-linked investment policy) |
| Policy type | Dedicated portfolio |
| Version | 3.1 |
| Effective date | 2026-01-01 |
| Owner | Investment Compliance |

## 1. Scope

This document sets out which assets may be held in the dedicated portfolio linked to a unit-linked investment policy issued by the insurer's Luxembourg entity. Every rule has a unique ID and assessments must cite the IDs they rely on. Where no rule clearly applies, or the facts needed to apply a rule are missing, LU-UL-14 applies.

## 2. General rules

### LU-UL-01 — General eligibility
- **Applies to:** all assets

All assets must be held in the policy's dedicated portfolio, be legally owned by the insurer, be held in custody with the insurer's approved custodian bank and be managed by an investment manager approved by the insurer. An asset that cannot be held in custody by the custodian bank is not permissible. Custody, legal ownership and the manager appointment are verified by Operations when the trade is executed; the permissibility assessment assumes they are met unless the request indicates otherwise.

### LU-UL-02 — Investor classification
- **Applies to:** all rules that depend on investor classification

The policyholder is a **professional investor** if at least one of the following applies:
1. They are classified as a professional client by their bank or investment firm and written confirmation is available.
2. They hold net financial assets of at least EUR 2,500,000 **and** the premium paid into the policy is at least EUR 250,000.

All other policyholders are **retail investors**. If the classification cannot be established from the information available, it must not be assumed: the case is referred under LU-UL-14.

## 3. Asset rules

### LU-UL-03 — Listed equities
- **Asset type:** `listed_equity`
- **Status:** Permitted

Shares admitted to trading on a regulated market or a multilateral trading facility (MTF) in an EEA or OECD country are permitted. Listed real estate investment trusts (REITs) are treated as listed equities under this rule. Shares not admitted to trading on such a venue are not permissible.

### LU-UL-04 — UCITS funds
- **Asset type:** `ucits_fund`
- **Status:** Permitted

Units of funds authorised under the UCITS Directive are permitted, including UCITS exchange-traded funds (ETFs) and UCITS money market funds, whatever the fund's domicile within the EEA.

### LU-UL-05 — Non-UCITS and alternative funds
- **Asset type:** `non_ucits_fund`
- **Status:** Conditional

Non-UCITS funds, including alternative investment funds (AIFs), hedge funds, private equity, private debt, ELTIFs and non-UCITS real estate funds, are permissible only if both conditions are met:
1. The policyholder is a professional investor under LU-UL-02.
2. Total exposure to non-UCITS funds does not exceed 30% of the portfolio value after the investment.

Retail investors may not hold non-UCITS funds.

### LU-UL-06 — Corporate bonds
- **Asset type:** `corporate_bond`
- **Status:** Conditional

Corporate bonds rated investment grade (BBB- or above, or equivalent, by at least one recognised credit rating agency) are permitted. Corporate bonds rated below investment grade, or unrated, are permissible only for professional investors under LU-UL-02.

### LU-UL-07 — Government bonds
- **Asset type:** `government_bond`
- **Status:** Permitted

Bonds issued or guaranteed by the government of an EEA or OECD country, or by a supranational body such as a multilateral development bank, are permitted. Bonds issued by other governments are assessed under the rating conditions of LU-UL-06.

### LU-UL-08 — Structured products
- **Asset type:** `structured_product`
- **Status:** Conditional

Structured products are permitted for professional investors under LU-UL-02. For retail investors, a structured product is permissible only if both conditions are met:
1. It offers at least 90% capital protection at maturity.
2. The issuer is rated investment grade.

### LU-UL-09 — Crypto-assets
- **Asset type:** `crypto_asset`
- **Status:** Conditional

Direct holdings of crypto-assets (coins, tokens, stablecoins) are not permissible. Exchange-traded products (ETPs or ETNs) giving exposure to crypto-assets are permissible only if all conditions are met:
1. The product is admitted to trading on a regulated market.
2. The policyholder is a professional investor under LU-UL-02.
3. Total crypto-asset exposure does not exceed 5% of the portfolio value after the investment.

### LU-UL-10 — Real estate
- **Asset type:** `real_estate`
- **Status:** Not permitted

Direct holdings of real property (land, residential or commercial buildings) are not permissible, including through a property-holding company created for the policy. Indirect real estate exposure is assessed under the rule for the instrument used: listed REITs under LU-UL-03, UCITS real estate funds under LU-UL-04 and other real estate funds under LU-UL-05.

### LU-UL-11 — Cash and deposits
- **Asset type:** `cash`
- **Status:** Permitted

Cash and deposits in any freely convertible currency, including term deposits with a maturity of up to 12 months, are permitted, provided they are held with the custodian bank or another credit institution approved by the insurer.

## 4. Exclusions

### LU-UL-12 — Assets connected to the policyholder
- **Applies to:** all assets
- **Status:** Not permitted

The following are not permissible:
1. Shares, bonds or other securities issued by a company in which the policyholder, the insured person, a beneficiary or a member of their close family hold, individually or together, 10% or more of the capital or voting rights, or exercises control.
2. Loans to any of those persons or to companies they control.
3. Any asset that gives those persons personal use or benefit.

This exclusion overrides any asset rule in section 3. It applies only where the request indicates a link between the issuer or borrower and the policyholder, the insured person, a beneficiary or their close family, or a personal use of the asset. Such links are declared at onboarding; if the request gives no indication of one, this exclusion does not apply.

### LU-UL-13 — Personal-use and collectible assets
- **Applies to:** all assets
- **Status:** Not permitted

Art, antiques, jewellery, wine, classic or collector cars, yachts, aircraft, horses and other collectibles or assets intended for personal use are not permissible.

## 5. Escalation

### LU-UL-14 — Referral to Investment Compliance
- **Applies to:** all assessments

A case must be referred to Investment Compliance (outcome: **needs review**) when:
1. The asset cannot be mapped to a single asset type covered by this document (for example physical commodities, exchange-traded commodities, convertible or other hybrid instruments).
2. Information needed to apply a rule is missing or contradictory, including the investor classification, credit rating, listing status, capital protection level or portfolio exposure where a rule depends on it.
3. The request indicates a possible link or personal use, but it is unclear whether an exclusion under LU-UL-12 or LU-UL-13 applies.

Missing facts must never be assumed.
