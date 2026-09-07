"""Measure concept-family payload against the saved task-start baseline.
Run: uv run --with tiktoken python qa/concept-design/measure-tokens.py
Runtime scripts are counted separately from agent-readable Markdown.
"""
import json
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parents[2]
baseline = json.loads(Path(__file__).with_name("token-baseline.json").read_text())
encoding = tiktoken.get_encoding(baseline["encoding"])
current = [p for d in (ROOT / "skills").glob("concept-*")
           for p in d.rglob("*") if p.is_file()]


def measure(scope, skill=None):
    def selected(path):
        return ((skill is None or path.startswith("skills/" + skill + "/"))
                and (scope == "all" or
                     (scope == "markdown" and path.endswith(".md")) or
                     (scope == "entrypoint" and path.endswith("/SKILL.md"))))
    before = sum(row["tokens"] for row in baseline["files"] if selected(row["path"]))
    after = sum(len(encoding.encode(p.read_text())) for p in current
                if selected(p.relative_to(ROOT).as_posix()))
    return {"before": before, "after": after,
            "reduction_percent": round(100 * (1 - after / before), 2)}


result = {"encoding": baseline["encoding"], "baseline": baseline["baseline"],
          "totals": {scope: measure(scope) for scope in ("entrypoint", "markdown", "all")},
          "markdown_by_skill": {d.name: measure("markdown", d.name)
                                for d in sorted((ROOT / "skills").glob("concept-*"))}}
print(json.dumps(result, ensure_ascii=False, indent=2))
