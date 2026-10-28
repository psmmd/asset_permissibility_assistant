from types import SimpleNamespace

from app import retrieval
from app.schemas import Rule


def test_build_query_uses_extracted_facts_and_skips_empty_fields():
    extraction = SimpleNamespace(asset_type=None, asset_description="gold ETC", facts=["listed in Dublin"])
    assert retrieval.build_query(extraction) == "gold ETC. listed in Dublin"


def test_referenced_rules_are_fetched_only_from_the_same_document(monkeypatch):
    requested = []

    def get_nodes(node_ids):
        requested.extend(node_ids)
        return [SimpleNamespace(id_=i, get_content=lambda i=i: f"text of {i}") for i in node_ids]

    fake_index = SimpleNamespace(vector_store=SimpleNamespace(get_nodes=get_nodes))
    monkeypatch.setattr(retrieval, "get_index", lambda: fake_index)
    rules = [
        Rule(rule_id="LU-UL-05", text="Professional investors under LU-UL-02 only. See also IE-UL-02."),
        Rule(rule_id="LU-UL-14", text="Refer to Compliance; see LU-UL-05."),  # already retrieved
    ]

    extra = retrieval.fetch_referenced_rules(rules, "LU", "UL")

    assert requested == ["LU-UL-02"]  # not IE-UL-02 (other document), not LU-UL-05 (already have it)
    assert extra == [Rule(rule_id="LU-UL-02", text="text of LU-UL-02")]


def test_no_lookup_when_nothing_is_referenced(monkeypatch):
    monkeypatch.setattr(retrieval, "get_index", lambda: (_ for _ in ()).throw(AssertionError("no lookup")))
    assert retrieval.fetch_referenced_rules([Rule(rule_id="LU-UL-11", text="Cash.")], "LU", "UL") == []
