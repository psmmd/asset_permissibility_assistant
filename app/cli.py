"""Run the pipeline from the command line.

  uv run python -m app.cli TC01 TC13 TC26        # test cases from data/test_cases.jsonl
  uv run python -m app.cli "free text request"   # any text
"""

import json
import sys
import time
from pathlib import Path

from app.pipeline import assess

TEST_CASES = Path(__file__).resolve().parent.parent / "data" / "test_cases.jsonl"


def main(args: list[str]) -> None:
    cases = {c["id"]: c for c in map(json.loads, TEST_CASES.read_text().splitlines())}
    for arg in args:
        case = cases.get(arg)
        text = case["input"] if case else arg
        start = time.perf_counter()
        result = assess(text)
        elapsed = time.perf_counter() - start

        print(f"=== {arg if case else 'input'} ({elapsed:.1f}s) ===")
        print(result.assessment.model_dump_json(indent=2))
        print("retrieved:", [r.rule_id for r in result.retrieved])
        if case:
            ok = result.assessment.decision == case["expected_decision"]
            print(f"expected: {case['expected_decision']} {case['expected_rule_ids']} -> {'OK' if ok else 'MISMATCH'}")
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
