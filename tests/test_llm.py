from types import SimpleNamespace

import pytest

from app import llm
from app.llm import Usage
from app.schemas import Rule


def fake_client(response):
    return SimpleNamespace(messages=SimpleNamespace(parse=lambda **kwargs: response))


def response(stop_reason="end_turn", parsed_output=None):
    return SimpleNamespace(
        stop_reason=stop_reason,
        parsed_output=parsed_output,
        usage=SimpleNamespace(input_tokens=7, output_tokens=3),
    )


@pytest.mark.parametrize(
    "resp",
    [response(stop_reason="refusal"), response(stop_reason="max_tokens")],
    ids=["refusal", "no-parsed-output"],
)
def test_no_structured_output_raises(monkeypatch, resp):
    monkeypatch.setattr(llm, "get_client", lambda: fake_client(resp))
    with pytest.raises(RuntimeError):
        llm.parse("system", "user", Rule, effort="low")


def test_returns_parsed_output_and_usage(monkeypatch):
    rule = Rule(rule_id="IE-UL-09", text="Crypto prohibited.")
    monkeypatch.setattr(llm, "get_client", lambda: fake_client(response(parsed_output=rule)))
    assert llm.parse("system", "user", Rule, effort="low") == (rule, Usage(7, 3))
