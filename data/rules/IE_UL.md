# Asset Permissibility Rules — Ireland / Unit-Linked Investment Policy

> Synthetic document created for a portfolio project. It does not describe any real insurer, product or regulation.

| Field | Value |
|---|---|
| Document ID | RULES-IE-UL |
| Country | IE (Ireland) |
| Product | UL (Unit-linked investment policy) |
| Policy type | Dedicated portfolio |
| Version | 4.0 |
| Effective date | 2026-01-01 |
| Owner | Investment Compliance |

## 1. Scope

This document sets out which assets may be held in the dedicated portfolio linked to a unit-linked investment policy issued by the insurer's Irish entity. As a general principle, assets must be listed or publicly authorised investments; private and unlisted assets are restricted. Every rule has a unique ID and assessments must cite the IDs they rely on. Where no rule clearly applies, or the facts needed to apply a rule are missing, IE-UL-14 applies.

## 2. General rules

### IE-UL-01 — General eligibility
- **Applies to:** all assets

All assets must be held in the policy's dedicated portfolio, be legally owned by the insurer, be held in custody with the insurer's approved custodian bank and be managed by an investment manager approved by the insurer. An asset that cannot be held in custody by the custodian bank is not permissible. Custody, legal ownership and the manager appointment are verified by Operations when the trade is executed; the permissibility assessment assumes they are met unless the request indicates otherwise.

### IE-UL-02 — Investor classification
- **Applies to:** all rules that depend on investor classification

The policyholder is a **professional investor** if at least one of the following applies:
1. They are classified as a professional client by their bank or investment firm and written confirmation is available.
2. They hold net financial assets of at least EUR 1,000,000.

All other policyholders are **retail investors**. If the classification cannot be established from the information available, it must not be assumed: the case is referred under IE-UL-14.

## 3. Asset rules

### IE-UL-03 — Listed equities
- **Asset type:** `listed_equity`
- **Status:** Permitted

Shares listed on a recognised stock exchange in an EEA or OECD country are permitted. Listed real estate investment trusts (REITs) are treated as listed equities under this rule. Unlisted shares are not permissible.

### IE-UL-04 — UCITS funds
- **Asset type:** `ucits_fund`
- **Status:** Permitted

Units of funds authorised under the UCITS Directive are permitted, including UCITS exchange-traded funds (ETFs) and UCITS money market funds, whatever the fund's domicile within the EEA.

### IE-UL-05 — Non-UCITS and alternative funds
- **Asset type:** `non_ucits_fund`
- **Status:** Conditional

Non-UCITS funds, including alternative investment funds (AIFs), hedge funds, private equity, private debt, ELTIFs and non-UCITS real estate funds, are permissible only if both conditions are met:
1. The policyholder is a professional investor under IE-UL-02.
2. The fund is authorised by a financial regulator in an EEA country (for example an authorised AIF or an ELTIF).

Unregulated funds, including funds domiciled outside the EEA, are not permissible for any investor. Retail investors may not hold non-UCITS funds.

### IE-UL-06 — Corporate bonds
- **Asset type:** `corporate_bond`
- **Status:** Conditional

Corporate bonds listed on a recognised stock exchange are permitted, whatever their credit rating. Unlisted corporate bonds are not permissible.

### IE-UL-07 — Government bonds
- **Asset type:** `government_bond`
- **Status:** Permitted

Bonds issued or guaranteed by the government of an EEA or OECD country, or by a supranational body such as a multilateral development bank, are permitted. Bonds issued by other governments are not permissible.

### IE-UL-08 — Structured products
- **Asset type:** `structured_product`
- **Status:** Conditional

Structured products are permissible only if they are listed on a recognised stock exchange. Unlisted structured products, including over-the-counter (OTC) instruments and private placements, are not permissible for any investor.

### IE-UL-09 — Crypto-assets
- **Asset type:** `crypto_asset`
- **Status:** Not permitted

Crypto-assets are not permissible in any form, including direct holdings, exchange-traded products (ETPs or ETNs) and funds whose main strategy is crypto-asset exposure, whatever the investor classification.

### IE-UL-10 — Real estate
- **Asset type:** `real_estate`
- **Status:** Not permitted

Direct holdings of real property (land, residential or commercial buildings) are not permissible, including through a property-holding company created for the policy. Indirect real estate exposure is assessed under the rule for the instrument used: listed REITs under IE-UL-03, UCITS real estate funds under IE-UL-04 and other real estate funds under IE-UL-05.

### IE-UL-11 — Cash and deposits
- **Asset type:** `cash`
- **Status:** Permitted

Cash and deposits in any freely convertible currency, including term deposits with a maturity of up to 12 months, are permitted, provided they are held with the custodian bank or another credit institution approved by the insurer.

## 4. Exclusions

### IE-UL-12 — Assets connected to the policyholder
- **Applies to:** all assets
- **Status:** Not permitted

The following are not permissible:
1. Shares, bonds or other securities issued by a company in which the policyholder, the insured person, a beneficiary or a member of their close family holds 10% or more of the capital or voting rights, or exercises control.
2. Loans to any of those persons or to companies they control.
3. Any asset that gives those persons personal use or benefit.

This exclusion overrides any asset rule in section 3. It applies only where the request indicates a link between the issuer or borrower and the policyholder, the insured person, a beneficiary or their close family, or a personal use of the asset. Such links are declared at onboarding; if the request gives no indication of one, this exclusion does not apply.

### IE-UL-13 — Personal-use and collectible assets
- **Applies to:** all assets
- **Status:** Not permitted

Art, antiques, jewellery, wine, classic or collector cars, yachts, aircraft, horses and other collectibles or assets intended for personal use are not permissible.

## 5. Escalation

### IE-UL-14 — Referral to Investment Compliance
- **Applies to:** all assessments

A case must be referred to Investment Compliance (outcome: **needs review**) when:
1. The asset cannot be mapped to a single asset type covered by this document (for example physical commodities, exchange-traded commodities, convertible or other hybrid instruments).
2. Information needed to apply a rule is missing or contradictory, including the investor classification, credit rating, listing status, capital protection level or portfolio exposure where a rule depends on it.
3. The request indicates a possible link or personal use, but it is unclear whether an exclusion under IE-UL-12 or IE-UL-13 applies.

Missing facts must never be assumed.
