"""Step 1: extract structured facts from a free-text request."""

from app.llm import Usage, parse
from app.schemas import Extraction

SYSTEM_PROMPT = """\
You extract facts from emails sent by relationship managers at a life insurer. Each email asks \
whether an asset can be held in a client's insurance policy. All policies hold a dedicated portfolio.

Extract only what the email states. Never guess, and never apply permissibility rules: that is a later step.

Field guidance:
- country: the country of the insurer entity that issued the policy (IE, LU or IT). Ignore where the \
client lives, their nationality, the RM's office and the fund's domicile.
- product: UL = unit-linked investment policy, CB = capitalisation bond, RP = retirement or pension policy.
- If the email mentions more than one policy and does not say which one will hold the asset, or \
contradicts itself about the policy's country or product, use null for the field in doubt. A null is \
escalated to a human; a wrong value applies the wrong rules.
- asset_type: map the asset to one type. ETFs and money market funds that are UCITS are ucits_fund. \
ELTIFs, AIFs, hedge funds and private equity funds are non_ucits_fund. Listed REITs are listed_equity. \
Crypto ETPs/ETNs are crypto_asset. Direct property is real_estate. Use null if the asset fits none of \
the types (e.g. art, commodities, gold ETCs) or the email does not say what the asset is.
- investor_classification: only if the email explicitly says retail or professional. If it only gives \
wealth figures, use null and record the figures in facts.
- facts: short statements copied or paraphrased from the email that could affect permissibility. \
Leave out small talk and irrelevant details."""


def extract(text: str, model: str | None = None) -> tuple[Extraction, Usage]:
    return parse(SYSTEM_PROMPT, text, Extraction, effort="low", model=model)
