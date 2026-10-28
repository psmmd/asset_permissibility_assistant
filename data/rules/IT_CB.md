# Asset Permissibility Rules — Italy / Capitalisation Bond

> Synthetic document created for a portfolio project. It does not describe any real insurer, product or regulation.

| Field | Value |
|---|---|
| Document ID | RULES-IT-CB |
| Country | IT (Italy) |
| Product | CB (Capitalisation bond) |
| Policy type | Dedicated portfolio |
| Version | 1.5 |
| Effective date | 2026-01-01 |
| Owner | Investment Compliance |

## 1. Scope

This document sets out which assets may be held in the dedicated portfolio linked to a capitalisation bond issued by the insurer's Italian entity. Capitalisation bonds carry no life cover and may be held by individuals or legal entities. Every rule has a unique ID and assessments must cite the IDs they rely on. Where no rule clearly applies, or the facts needed to apply a rule are missing, IT-CB-14 applies.

## 2. General rules

### IT-CB-01 — General eligibility
- **Applies to:** all assets

All assets must be held in the policy's dedicated portfolio, be legally owned by the insurer, be held in custody with the insurer's approved custodian bank and be managed by an investment manager approved by the insurer. An asset that cannot be held in custody by the custodian bank is not permissible. Custody, legal ownership and the manager appointment are verified by Operations when the trade is executed; the permissibility assessment assumes they are met unless the request indicates otherwise.

### IT-CB-02 — Investor classification
- **Applies to:** all rules that depend on investor classification

The policyholder is a **professional investor** only if they are classified as a professional client by their bank or investment firm and written confirmation is available. Wealth or portfolio size thresholds do not qualify a policyholder as a professional investor.

All other policyholders are **retail investors**. If the classification cannot be established from the information available, it must not be assumed: the case is referred under IT-CB-14.

## 3. Asset rules

### IT-CB-03 — Listed equities
- **Asset type:** `listed_equity`
- **Status:** Conditional

Shares admitted to trading on a regulated market in the EU/EEA, the United Kingdom, Switzerland or the United States are permitted. Listed real estate investment trusts (REITs) on those markets are treated as listed equities under this rule. Shares listed only on any other market, or not listed, are not permissible.

### IT-CB-04 — UCITS funds
- **Asset type:** `ucits_fund`
- **Status:** Permitted

Units of funds authorised under the UCITS Directive are permitted, including UCITS exchange-traded funds (ETFs) and UCITS money market funds, whatever the fund's domicile within the EEA.

### IT-CB-05 — Non-UCITS and alternative funds
- **Asset type:** `non_ucits_fund`
- **Status:** Conditional

European long-term investment funds (ELTIFs) are permitted for all investors, provided total ELTIF exposure does not exceed 10% of the portfolio value after the investment.

Other non-UCITS funds, including alternative investment funds (AIFs), hedge funds, private equity, private debt and non-UCITS real estate funds, are permissible only if both conditions are met:
1. The policyholder is a professional investor under IT-CB-02.
2. Total exposure to those funds does not exceed 10% of the portfolio value after the investment.

### IT-CB-06 — Corporate bonds
- **Asset type:** `corporate_bond`
- **Status:** Conditional

Corporate bonds rated investment grade (BBB- or above, or equivalent, by at least one recognised credit rating agency) are permitted. Corporate bonds rated below investment grade, or unrated, are permissible only if both conditions are met:
1. The policyholder is a professional investor under IT-CB-02.
2. Total exposure to such bonds does not exceed 15% of the portfolio value after the investment.

### IT-CB-07 — Government bonds
- **Asset type:** `government_bond`
- **Status:** Permitted

Bonds issued or guaranteed by the government of an EU/EEA or OECD country, or by a supranational body such as a multilateral development bank, are permitted. Bonds issued by other governments are permissible only if rated investment grade.

### IT-CB-08 — Structured products
- **Asset type:** `structured_product`
- **Status:** Conditional

Structured products are permissible only if both conditions are met:
1. They offer 100% capital protection at maturity.
2. The issuer is rated investment grade.

All other structured products are not permissible, whatever the investor classification.

### IT-CB-09 — Crypto-assets
- **Asset type:** `crypto_asset`
- **Status:** Conditional

Direct holdings of crypto-assets (coins, tokens, stablecoins) are not permissible. Exchange-traded products (ETPs or ETNs) giving exposure to crypto-assets are permissible only if all conditions are met:
1. The product is admitted to trading on a regulated market.
2. The policyholder is a professional investor under IT-CB-02.
3. Total crypto-asset exposure does not exceed 5% of the portfolio value after the investment.

### IT-CB-10 — Real estate
- **Asset type:** `real_estate`
- **Status:** Not permitted

Direct holdings of real property (land, residential or commercial buildings) are not permissible, including through a property-holding company created for the policy. Indirect real estate exposure is assessed under the rule for the instrument used: listed REITs under IT-CB-03, UCITS real estate funds under IT-CB-04 and other real estate funds under IT-CB-05.

### IT-CB-11 — Cash and deposits
- **Asset type:** `cash`
- **Status:** Permitted

Cash and deposits in any freely convertible currency, including term deposits with a maturity of up to 12 months, are permitted, provided they are held with the custodian bank or another credit institution approved by the insurer.

## 4. Exclusions

### IT-CB-12 — Assets connected to the policyholder
- **Applies to:** all assets
- **Status:** Not permitted

The following are not permissible:
1. Shares, bonds or other securities issued by a company in which the policyholder, the insured person, a beneficiary or a member of their close family holds 10% or more of the capital or voting rights, or exercises control.
2. Loans to any of those persons or to companies they control.
3. Any asset that gives those persons personal use or benefit.

This exclusion overrides any asset rule in section 3. It applies only where the request indicates a link between the issuer or borrower and the policyholder, the insured person, a beneficiary or their close family, or a personal use of the asset. Such links are declared at onboarding; if the request gives no indication of one, this exclusion does not apply.

### IT-CB-13 — Personal-use and collectible assets
- **Applies to:** all assets
- **Status:** Not permitted

Art, antiques, jewellery, wine, classic or collector cars, yachts, aircraft, horses and other collectibles or assets intended for personal use are not permissible.

## 5. Escalation

### IT-CB-14 — Referral to Investment Compliance
- **Applies to:** all assessments

A case must be referred to Investment Compliance (outcome: **needs review**) when:
1. The asset cannot be mapped to a single asset type covered by this document (for example physical commodities, exchange-traded commodities, convertible or other hybrid instruments).
2. Information needed to apply a rule is missing or contradictory, including the investor classification, credit rating, listing status, capital protection level or portfolio exposure where a rule depends on it.
3. The request indicates a possible link or personal use, but it is unclear whether an exclusion under IT-CB-12 or IT-CB-13 applies.

Missing facts must never be assumed.
