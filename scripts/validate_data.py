"""Sanity checks for the synthetic data. Run: python scripts/validate_data.py

Checks that every rules document has rules 01-14 in order, and that every test
case is well formed and only references rule IDs that exist.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
RULE_HEADING = re.compile(r"^### ([A-Z]{2}-[A-Z]{2}-\d{2}) — ", re.MULTILINE)
ASSET_TYPE_LINE = re.compile(r"^- \*\*Asset type:\*\* `(\w+)`", re.MULTILINE)
DECISIONS = {"permissible", "not_permissible", "needs_review"}
CATEGORIES = {"clear_permissible", "clear_not_permissible", "conditional", "needs_review"}

errors = []
rule_ids = set()
countries, products, asset_types = set(), set(), set()

for path in sorted((DATA / "rules").glob("*.md")):
    country, product = path.stem.split("_")
    countries.add(country)
    products.add(product)
    text = path.read_text()
    ids = RULE_HEADING.findall(text)
    expected = [f"{country}-{product}-{n:02d}" for n in range(1, 15)]
    if ids != expected:
        errors.append(f"{path.name}: rule IDs {ids} != expected 01-14")
    rule_ids.update(ids)
    asset_types.update(ASSET_TYPE_LINE.findall(text))

if len(rule_ids) != 9 * 14:
    errors.append(f"expected 126 rule IDs, found {len(rule_ids)}")

cases = [json.loads(line) for line in (DATA / "test_cases.jsonl").read_text().splitlines()]
for c in cases:
    cid = c["id"]
    if c["category"] not in CATEGORIES:
        errors.append(f"{cid}: unknown category {c['category']}")
    if c["expected_decision"] not in DECISIONS:
        errors.append(f"{cid}: unknown decision {c['expected_decision']}")
    if not c["expected_rule_ids"]:
        errors.append(f"{cid}: no expected rule IDs")
    for rid in c["expected_rule_ids"]:
        if rid not in rule_ids:
            errors.append(f"{cid}: rule {rid} does not exist")
    ex = c["expected_extracted"]
    for field, valid in [
        ("country", countries),
        ("product", products),
        ("asset_type", asset_types),
        ("investor_classification", {"retail", "professional"}),
    ]:
        if ex[field] is not None and ex[field] not in valid:
            errors.append(f"{cid}: invalid {field} {ex[field]}")
    if ex["country"] and ex["product"] and c["expected_decision"] != "needs_review":
        prefix = f"{ex['country']}-{ex['product']}-"
        if not all(r.startswith(prefix) for r in c["expected_rule_ids"]):
            errors.append(f"{cid}: rule IDs do not match {prefix}")
    if (c["expected_decision"] == "needs_review") != bool(c["expected_missing_info"]):
        errors.append(f"{cid}: missing_info must be set if and only if decision is needs_review")

if len({c["id"] for c in cases}) != len(cases):
    errors.append("duplicate test case IDs")

print(f"{len(rule_ids)} rules in {len(countries) * len(products)} documents, {len(cases)} test cases")
print("decisions:", dict(Counter(c["expected_decision"] for c in cases)))
print("categories:", dict(Counter(c["category"] for c in cases)))
if errors:
    print("\nERRORS:\n" + "\n".join(errors))
    sys.exit(1)
print("OK")
