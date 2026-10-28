"""Guardrails in app.pipeline, with the LLM and retrieval steps replaced by fakes."""

import pytest

from app import pipeline
from app.llm import Usage
from app.schemas import Country, Decision, DecisionOutput, Extraction, Product, Rule

RULES = [Rule(rule_id="LU-UL-05", text="..."), Rule(rule_id="LU-UL-02", text="...")]


def make_extraction(**overrides) -> Extraction:
    fields = {
        "country": Country.LU,
        "product": Product.UL,
        "asset_type": "non_ucits_fund",
        "asset_description": "hedge fund",
        "investor_classification": "professional",
        "facts": [],
    }
    return Extraction(**(fields | overrides))


@pytest.fixture
def fake_steps(monkeypatch):
    """Replace the three steps; tests set calls['extraction'] and calls['output']."""
    calls = {"extraction": make_extraction(), "output": None, "retrieve": 0}

    def fake_extract(text, model=None):
        return calls["extraction"], Usage(10, 5)

    def fake_retrieve(extraction, country, product, top_k=None):
        calls["retrieve"] += 1
        return RULES

    def fake_decide(text, extraction, rules, model=None):
        return calls["output"], Usage(100, 50)

    monkeypatch.setattr(pipeline, "extract", fake_extract)
    monkeypatch.setattr(pipeline, "retrieve", fake_retrieve)
    monkeypatch.setattr(pipeline, "decide", fake_decide)
    return calls


@pytest.mark.parametrize("missing", ["country", "product"])
def test_missing_country_or_product_escalates_without_retrieval(fake_steps, missing):
    fake_steps["extraction"] = make_extraction(**{missing: None})

    result = pipeline.assess("some email")

    assert result.assessment.decision == Decision.NEEDS_REVIEW
    assert result.assessment.rule_ids == []
    assert result.assessment.missing_info == [missing]
    assert fake_steps["retrieve"] == 0
    assert result.usage == Usage(10, 5)  # the decision step was not called either


def test_invented_rule_escalates(fake_steps):
    fake_steps["output"] = DecisionOutput(
        decision=Decision.PERMISSIBLE,
        rule_ids=["LU-UL-05", "LU-UL-99"],
        justification="Looks fine.",
        missing_info=[],
    )

    a = pipeline.assess("some email").assessment

    assert a.decision == Decision.NEEDS_REVIEW
    assert a.rule_ids == ["LU-UL-05"]  # the invented ID is removed
    assert "LU-UL-99" in a.justification


def test_valid_decision_passes_through(fake_steps):
    fake_steps["output"] = DecisionOutput(
        decision=Decision.PERMISSIBLE,
        rule_ids=["LU-UL-05", "LU-UL-02"],
        justification="Professional investor, non-UCITS at 18% is within the 30% limit.",
        missing_info=[],
    )

    result = pipeline.assess("some email")

    assert result.assessment.model_dump(exclude={"extracted"}) == fake_steps["output"].model_dump()
    assert result.assessment.extracted == fake_steps["extraction"]
    assert result.retrieved == RULES
    assert result.usage == Usage(110, 55)
