#!/usr/bin/env python3
"""Grade a billing-scout agent response against evals.json assertions (offline rules)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parent
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

from protocol_grading import grade_assertion  # noqa: E402
from qa_common import load_eval_bundle, merge_assertions  # noqa: E402


def grade_eval_item(eval_item: dict, text: str) -> dict:
    _, _, global_assertions = load_eval_bundle()
    assertions = merge_assertions(eval_item, global_assertions)
    expectations = []
    passed = 0
    for assertion in assertions:
        ok, reason = grade_assertion(assertion, text, eval_item)
        expectations.append({"text": assertion, "passed": ok, "evidence": reason})
        if ok:
            passed += 1
    total = len(expectations)
    return {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("response", type=Path, help="Agent response markdown")
    parser.add_argument("eval_spec", type=Path, help="eval_metadata.json or eval item JSON")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    spec = json.loads(args.eval_spec.read_text(encoding="utf-8"))
    if "eval_name" in spec and "assertions" in spec and "prompt" in spec:
        _, evals, _ = load_eval_bundle()
        name = spec["eval_name"]
        eval_item = next((e for e in evals if e["name"] == name), None)
        if not eval_item:
            print(f"unknown eval_name: {name}", file=sys.stderr)
            return 1
    else:
        eval_item = spec

    text = args.response.read_text(encoding="utf-8")
    out = grade_eval_item(eval_item, text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out["summary"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
