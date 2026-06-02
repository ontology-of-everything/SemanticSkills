#!/usr/bin/env python3
"""Grade A/B eval outputs under repo-root huawei-cloud-billing-scout-workspace/.

Usage:
  python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py snapshot-old-skill
  python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py init-metadata
  python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py grade-all
  python3 qa/huawei-cloud-billing-scout/bin/run_ab_eval.py aggregate
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parents[1]
EVALS_JSON = QA / "evals" / "evals.json"
WORKSPACE = ROOT / "huawei-cloud-billing-scout-workspace" / "iteration-1"
SNAP_SKILL = WORKSPACE / "skill-snapshot" / "huawei-cloud-billing-scout"
CURRENT_SKILL = ROOT / "skills" / "huawei-cloud-billing-scout"
GRADER = QA / "bin" / "grade_response.py"
AGG = QA / "bin" / "aggregate_ab.py"
VIEWER = Path.home() / ".claude/skills/skill-creator/eval-viewer/generate_review.py"
VIEWER_PY = Path("/opt/homebrew/bin/python3.12")
if not VIEWER_PY.exists():
    VIEWER_PY = Path(sys.executable)
CONFIGS = ("with_skill", "old_skill")


def load_evals() -> list[dict]:
    data = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
    return list(data["evals"])


def snapshot_old_skill() -> None:
    prefix = "skills/huawei-cloud-billing-scout"
    if SNAP_SKILL.exists():
        import shutil

        shutil.rmtree(SNAP_SKILL)
    for rel in subprocess.check_output(
        ["git", "ls-tree", "-r", "HEAD", "--name-only", prefix],
        cwd=ROOT,
        text=True,
    ).splitlines():
        rel = rel.strip()
        if not rel:
            continue
        out = SNAP_SKILL / rel.removeprefix(prefix + "/")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(subprocess.check_output(["git", "show", f"HEAD:{rel}"], cwd=ROOT))


def init_metadata() -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    for ev in load_evals():
        name = ev["name"]
        meta_dir = WORKSPACE / name
        meta_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "eval_id": ev["id"],
            "eval_name": name,
            "prompt": ev["prompt"],
            "assertions": ev.get("assertions", []),
        }
        (meta_dir / "eval_metadata.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    print(f"metadata: {len(load_evals())} evals under {WORKSPACE}")


def grade_all() -> None:
    for ev in load_evals():
        name = ev["name"]
        meta = WORKSPACE / name / "eval_metadata.json"
        if not meta.exists():
            init_metadata()
        for cfg in CONFIGS:
            resp = WORKSPACE / name / cfg / "outputs" / "response.md"
            if not resp.exists():
                print(f"SKIP {name}/{cfg}: missing {resp}")
                continue
            out = WORKSPACE / name / cfg / "grading.json"
            subprocess.run(
                [sys.executable, str(GRADER), str(resp), str(meta), "-o", str(out)],
                check=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))["summary"]
            print(f"OK {name}/{cfg} pass_rate={summary['pass_rate']}")


def aggregate() -> None:
    subprocess.run([sys.executable, str(AGG), str(WORKSPACE)], check=True)


def viewer_static() -> None:
    out = WORKSPACE / "benchmark-review.html"
    bench = WORKSPACE / "benchmark.json"
    if not VIEWER.exists():
        print(f"SKIP viewer: missing {VIEWER}")
        return
    cmd = [
        str(VIEWER_PY),
        str(VIEWER),
        str(WORKSPACE),
        "--skill-name",
        "huawei-cloud-billing-scout",
        "--static",
        str(out),
    ]
    if bench.exists():
        cmd.extend(["--benchmark", str(bench)])
    subprocess.run(cmd, check=True)
    print(f"viewer: {out}")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "grade-all"
    if cmd == "snapshot-old-skill":
        snapshot_old_skill()
        print(f"snapshot: {SNAP_SKILL}")
    elif cmd == "init-metadata":
        init_metadata()
    elif cmd == "grade-all":
        grade_all()
    elif cmd == "aggregate":
        aggregate()
        viewer_static()
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
