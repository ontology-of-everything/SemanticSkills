#!/usr/bin/env python3
"""Orchestrate A/B eval grading after manual or agent-generated responses.

Usage:
  python3 qa/huawei-cloud-cost-estimation/bin/run_ab_eval.py grade-all
  python3 qa/huawei-cloud-cost-estimation/bin/run_ab_eval.py aggregate
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parents[1]
EVALS_JSON = QA / "evals" / "evals.json"
WORKSPACE = ROOT / "huawei-cloud-cost-estimation-workspace" / "iteration-1"
GRADER = QA / "bin" / "grade_response.py"
AGG = Path.home() / ".claude/skills/skill-creator/scripts/aggregate_benchmark.py"
VIEWER = Path.home() / ".claude/skills/skill-creator/eval-viewer/generate_review.py"


def load_evals() -> list[dict]:
    data = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
    return data["evals"]


def grade_all() -> None:
    for ev in load_evals():
        name = ev["name"]
        exp_path = WORKSPACE / name / "_expectations.json"
        exp_path.write_text(json.dumps(ev["expectations"], ensure_ascii=False), encoding="utf-8")
        for cfg in ("with_skill", "without_skill"):
            resp = WORKSPACE / name / cfg / "outputs" / "response.md"
            if not resp.exists():
                print(f"SKIP {name}/{cfg}: missing {resp}")
                continue
            out = WORKSPACE / name / cfg / "grading.json"
            subprocess.run(
                [
                    sys.executable,
                    str(GRADER),
                    str(resp),
                    str(exp_path),
                    "-o",
                    str(out),
                ],
                check=True,
            )
            meta_dir = WORKSPACE / name
            meta = {
                "eval_id": ev["id"],
                "eval_name": name,
                "prompt": ev["prompt"],
                "assertions": ev["expectations"],
            }
            (meta_dir / "eval_metadata.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"OK {name}/{cfg} pass_rate={json.loads(out.read_text())['summary']['pass_rate']}")


def aggregate() -> None:
    if not AGG.exists():
        sys.exit(f"missing {AGG}")
    subprocess.run(
        [sys.executable, str(AGG), str(WORKSPACE), "--skill-name", "huawei-cloud-cost-estimation"],
        cwd=str(AGG.parent.parent),
        check=True,
    )
    print(f"benchmark: {WORKSPACE / 'benchmark.json'}")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "grade-all"
    if cmd == "grade-all":
        grade_all()
    elif cmd == "aggregate":
        aggregate()
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
