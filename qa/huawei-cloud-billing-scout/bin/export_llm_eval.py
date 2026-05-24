#!/usr/bin/env python3
"""Export LLM eval cases (prompt + merged assertions + rubric) as JSONL for Skill Creator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("FAIL: PyYAML is required") from exc


def main() -> int:
    qa_dir = Path(__file__).resolve().parents[1]
    evals_file = qa_dir / "evals" / "evals.json"
    rubric_file = qa_dir / "evals" / "llm-rubric.yml"
    out = sys.stdout if len(sys.argv) < 2 else Path(sys.argv[1])

    data = json.loads(evals_file.read_text(encoding="utf-8"))
    rubric = yaml.safe_load(rubric_file.read_text(encoding="utf-8")) or {}
    global_assertions = list(rubric.get("global_assertions") or [])
    dimensions = rubric.get("dimensions") or []

    lines: list[str] = []
    for item in data.get("evals") or []:
        merged = list(dict.fromkeys(global_assertions + list(item.get("assertions") or [])))
        record = {
            "id": item.get("id"),
            "name": item.get("name"),
            "skill_name": data.get("skill_name"),
            "prompt": item.get("prompt"),
            "expected_output": item.get("expected_output"),
            "covers": item.get("covers"),
            "assertions": merged,
            "rubric_dimensions": dimensions,
        }
        lines.append(json.dumps(record, ensure_ascii=False))

    payload = "\n".join(lines) + ("\n" if lines else "")
    if out is sys.stdout:
        sys.stdout.write(payload)
    else:
        out.write_text(payload, encoding="utf-8")
        print(f"Wrote {len(lines)} LLM eval cases to {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
