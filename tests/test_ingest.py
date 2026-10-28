from app.ingest import RULES_DIR, parse_rules

DOCS = sorted(RULES_DIR.glob("*.md"))


def test_nine_documents_with_fourteen_rules_each():
    assert len(DOCS) == 9
    for path in DOCS:
        country, product = path.stem.split("_")
        ids = [node.id_ for node in parse_rules(path)]
        assert ids == [f"{country}-{product}-{n:02d}" for n in range(1, 15)]


def test_metadata_matches_document():
    for path in DOCS:
        country, product = path.stem.split("_")
        for node in parse_rules(path):
            assert node.metadata["country"] == country
            assert node.metadata["product"] == product
            assert node.metadata["rule_id"] == node.id_
            assert node.ref_doc_id == path.stem  # what idempotent re-ingestion deletes by


def test_asset_type_only_on_asset_rules():
    # Rules 03-11 are the asset rules (03 listed_equity ... 11 cash); the others are general.
    for path in DOCS:
        for node in parse_rules(path):
            number = int(node.id_[-2:])
            assert ("asset_type" in node.metadata) == (3 <= number <= 11), node.id_


def test_each_node_holds_exactly_one_rule():
    for node in parse_rules(RULES_DIR / "LU_UL.md"):
        assert node.text.startswith(f"### {node.id_} — ")
        assert node.text.count("### ") == 1
