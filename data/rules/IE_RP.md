# Asset Permissibility Rules — Ireland / Retirement Policy

> Synthetic document created for a portfolio project. It does not describe any real insurer, product or regulation.

| Field | Value |
|---|---|
| Document ID | RULES-IE-RP |
| Country | IE (Ireland) |
| Product | RP (Retirement policy) |
| Policy type | Dedicated portfolio |
| Version | 1.3 |
| Effective date | 2026-01-01 |
| Owner | Investment Compliance |

## 1. Scope

This document sets out which assets may be held in the dedicated portfolio linked to a retirement policy issued by the insurer's Irish entity. Because the policy funds the policyholder's retirement income, only listed, liquid and publicly authorised investments are allowed. Every rule has a unique ID and assessments must cite the IDs they rely on. Where no rule clearly applies, or the facts needed to apply a rule are missing, IE-RP-14 applies.

## 2. General rules

### IE-RP-01 — General eligibility
- **Applies to:** all assets

All assets must be held in the policy's dedicated portfolio, be legally owned by the insurer, be held in custody with the insurer's approved custodian bank and be managed by an investment manager approved by the insurer. An asset that cannot be held in custody by the custodian bank is not permissible. Custody, legal ownership and the manager appointment are verified by Operations when the trade is executed; the permissibility assessment assumes they are met unless the request indicates otherwise.

### IE-RP-02 — Investor classification
- **Applies to:** all rules that depend on investor classification

The policyholder is a **professional investor** if at least one of the following applies:
1. They are classified as a professional client by their bank or investment firm and written confirmation is available.
2. They hold net financial assets of at least EUR 1,000,000.

All other policyholders are **retail investors**. If the classification cannot be established from the information available, it must not be assumed: the case is referred under IE-RP-14.

## 3. Asset rules

### IE-RP-03 — Listed equities
- **Asset type:** `listed_equity`
- **Status:** Permitted

Shares listed on a recognised stock exchange in an EEA or OECD country are permitted. Listed real estate investment trusts (REITs) are treated as listed equities under this rule. Unlisted shares are not permissible.

### IE-RP-04 — UCITS funds
- **Asset type:** `ucits_fund`
- **Status:** Permitted

Units of funds authorised under the UCITS Directive are permitted, including UCITS exchange-traded funds (ETFs) and UCITS money market funds, whatever the fund's domicile within the EEA.

### IE-RP-05 — Non-UCITS and alternative funds
- **Asset type:** `non_ucits_fund`
- **Status:** Not permitted

Non-UCITS funds, including alternative investment funds (AIFs), hedge funds, private equity, private debt, ELTIFs and non-UCITS real estate funds, are not permissible in a retirement policy, whatever the investor classification and whatever the fund's authorisation status.

### IE-RP-06 — Corporate bonds
- **Asset type:** `corporate_bond`
- **Status:** Conditional

Corporate bonds are permissible only if both conditions are met:
1. The bond is listed on a recognised stock exchange.
2. The bond is rated investment grade (BBB- or above, or equivalent, by at least one recognised credit rating agency).

### IE-RP-07 — Government bonds
- **Asset type:** `government_bond`
- **Status:** Permitted

Bonds issued or guaranteed by the government of an EEA or OECD country, or by a supranational body such as a multilateral development bank, are permitted. Bonds issued by other governments are not permissible.

### IE-RP-08 — Structured products
- **Asset type:** `structured_product`
- **Status:** Not permitted

Structured products are not permissible in a retirement policy, whether listed or unlisted and whatever the level of capital protection.

### IE-RP-09 — Crypto-assets
- **Asset type:** `crypto_asset`
- **Status:** Not permitted

Crypto-assets are not permissible in any form, including direct holdings, exchange-traded products (ETPs or ETNs) and funds whose main strategy is crypto-asset exposure, whatever the investor classification.

### IE-RP-10 — Real estate
- **Asset type:** `real_estate`
- **Status:** Not permitted

Direct holdings of real property (land, residential or commercial buildings) are not permissible, including through a property-holding company created for the policy. Indirect real estate exposure is assessed under the rule for the instrument used: listed REITs under IE-RP-03 and UCITS real estate funds under IE-RP-04. Non-UCITS real estate funds are not permissible under IE-RP-05.

### IE-RP-11 — Cash and deposits
- **Asset type:** `cash`
- **Status:** Permitted

Cash and deposits in any freely convertible currency, including term deposits with a maturity of up to 12 months, are permitted, provided they are held with the custodian bank or another credit institution approved by the insurer.

## 4. Exclusions

### IE-RP-12 — Assets connected to the policyholder
- **Applies to:** all assets
- **Status:** Not permitted

The following are not permissible:
1. Shares, bonds or other securities issued by a company in which the policyholder, the insured person, a beneficiary or a member of their close family holds 10% or more of the capital or voting rights, or exercises control.
2. Loans to any of those persons or to companies they control.
3. Any asset that gives those persons personal use or benefit.

This exclusion overrides any asset rule in section 3. It applies only where the request indicates a link between the issuer or borrower and the policyholder, the insured person, a beneficiary or their close family, or a personal use of the asset. Such links are declared at onboarding; if the request gives no indication of one, this exclusion does not apply.

### IE-RP-13 — Personal-use and collectible assets
- **Applies to:** all assets
- **Status:** Not permitted

Art, antiques, jewellery, wine, classic or collector cars, yachts, aircraft, horses and other collectibles or assets intended for personal use are not permissible.

## 5. Escalation

### IE-RP-14 — Referral to Investment Compliance
- **Applies to:** all assessments

A case must be referred to Investment Compliance (outcome: **needs review**) when:
1. The asset cannot be mapped to a single asset type covered by this document (for example physical commodities, exchange-traded commodities, convertible or other hybrid instruments).
2. Information needed to apply a rule is missing or contradictory, including the investor classification, credit rating, listing status, capital protection level or portfolio exposure where a rule depends on it.
3. The request indicates a possible link or personal use, but it is unclear whether an exclusion under IE-RP-12 or IE-RP-13 applies.

Missing facts must never be assumed.
