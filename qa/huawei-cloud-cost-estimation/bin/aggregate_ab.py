#!/usr/bin/env python3
"""Aggregate iteration-1 A/B results (with_skill / without_skill layout)."""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ITER = ROOT / "huawei-cloud-cost-estimation-workspace" / "iteration-1"


def main() -> int:
    iter_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ITER
    configs = ("with_skill", "without_skill")
    by_config: dict[str, list[float]] = {c: [] for c in configs}
    per_eval = []

    for eval_dir in sorted(d for d in iter_dir.iterdir() if d.is_dir() and not d.name.endswith(".json")):
        row = {"eval_name": eval_dir.name}
        for cfg in configs:
            gpath = eval_dir / cfg / "grading.json"
            if not gpath.exists():
                row[cfg] = None
                continue
            pr = json.loads(gpath.read_text(encoding="utf-8"))["summary"]["pass_rate"]
            row[cfg] = pr
            by_config[cfg].append(pr)
        if row.get("with_skill") is not None and row.get("without_skill") is not None:
            row["delta"] = round(row["with_skill"] - row["without_skill"], 4)
        per_eval.append(row)

    def stats(vals: list[float]) -> dict:
        if not vals:
            return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0, "n": 0}
        return {
            "mean": round(statistics.mean(vals), 4),
            "stddev": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
            "min": round(min(vals), 4),
            "max": round(max(vals), 4),
            "n": len(vals),
        }

    ws, wo = stats(by_config["with_skill"]), stats(by_config["without_skill"])
    out = {
        "metadata": {
            "skill_name": "huawei-cloud-cost-estimation",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "layout": "named-eval/with_skill|without_skill",
        },
        "per_eval": per_eval,
        "run_summary": {
            "with_skill": ws,
            "without_skill": wo,
            "delta": {"pass_rate_mean": round(ws["mean"] - wo["mean"], 4)},
        },
    }
    (iter_dir / "benchmark.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# huawei-cloud-cost-estimation A/B (iteration-1)",
        "",
        f"| Config | mean pass_rate | stddev | n |",
        f"| --- | --- | --- | --- |",
        f"| with_skill | {ws['mean']} | {ws['stddev']} | {ws['n']} |",
        f"| without_skill | {wo['mean']} | {wo['stddev']} | {wo['n']} |",
        f"| **delta** | **{out['run_summary']['delta']['pass_rate_mean']:+.4f}** | | |",
        "",
        "## Per eval",
        "",
        "| eval | with_skill | without_skill | delta |",
        "| --- | --- | --- | --- |",
    ]
    for r in per_eval:
        lines.append(
            f"| {r['eval_name']} | {r.get('with_skill','—')} | {r.get('without_skill','—')} | {r.get('delta','—')} |"
        )
    (iter_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(out["run_summary"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
