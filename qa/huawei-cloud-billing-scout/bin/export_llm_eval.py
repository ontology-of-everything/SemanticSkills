#!/usr/bin/env python3
"""Export eval cases (prompt + merged assertions) as JSONL for Skill Creator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from qa_common import RUBRIC_FILE, ensure_bin_path, load_eval_bundle, load_yaml, merge_assertions

ensure_bin_path()


def main() -> int:
    out = sys.stdout if len(sys.argv) < 2 else Path(sys.argv[1])
    data, evals, global_assertions = load_eval_bundle()
    dimensions = load_yaml(RUBRIC_FILE).get("dimensions") or []
    lines = [
        json.dumps(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "skill_name": data.get("skill_name"),
                "prompt": item.get("prompt"),
                "expected_output": item.get("expected_output"),
                "covers": item.get("covers"),
                "assertions": merge_assertions(item, global_assertions),
                "rubric_dimensions": dimensions,
            },
            ensure_ascii=False,
        )
        for item in evals
    ]
    payload = "\n".join(lines) + ("\n" if lines else "")
    if out is sys.stdout:
        sys.stdout.write(payload)
    else:
        out.write_text(payload, encoding="utf-8")
        print(f"Wrote {len(lines)} eval cases to {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
