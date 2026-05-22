#!/usr/bin/env python3
"""Aggregate iteration-1 layout: <eval_name>/{with_skill,without_skill}/grading.json"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WS = REPO / ".workspaces/huawei-cloud-billing-scout/iteration-1"
EVALS = json.loads(
    (REPO / "qa/huawei-cloud-billing-scout/evals/evals.json").read_text(encoding="utf-8")
)


def stats(values: list[float]) -> dict:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    n = len(values)
    mean = sum(values) / n
    stddev = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1)) if n > 1 else 0.0
    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_config(config: str) -> list[dict]:
    rows = []
    for ev in EVALS["evals"]:
        gpath = WS / ev["name"] / config / "grading.json"
        if not gpath.exists():
            print(f"WARN missing {gpath}")
            continue
        g = json.loads(gpath.read_text(encoding="utf-8"))
        s = g.get("summary", {})
        rows.append(
            {
                "eval_id": ev["id"],
                "eval_name": ev["name"],
                "pass_rate": s.get("pass_rate", 0.0),
                "passed": s.get("passed", 0),
                "failed": s.get("failed", 0),
                "total": s.get("total", 0),
            }
        )
    return rows


def main() -> None:
    with_rows = load_config("with_skill")
    without_rows = load_config("without_skill")
    with_rates = [r["pass_rate"] for r in with_rows]
    without_rates = [r["pass_rate"] for r in without_rows]
    delta = round(stats(with_rates)["mean"] - stats(without_rates)["mean"], 4)

    benchmark = {
        "metadata": {
            "skill_name": "huawei-cloud-billing-scout",
            "skill_path": str(REPO / "skills/huawei-cloud-billing-scout"),
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "layout": "named-eval/with_skill|without_skill",
            "evals_run": [e["name"] for e in EVALS["evals"]],
            "runs_per_configuration": 1,
        },
        "runs": {"with_skill": with_rows, "without_skill": without_rows},
        "run_summary": {
            "with_skill": {"pass_rate": stats(with_rates)},
            "without_skill": {"pass_rate": stats(without_rates)},
            "delta": {"pass_rate": f"{delta:+.4f}"},
        },
    }
    out = WS / "benchmark.json"
    out.write_text(json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# iteration-1 benchmark",
        "",
        f"- **with_skill** mean pass rate: {stats(with_rates)['mean']:.0%}",
        f"- **without_skill** mean pass rate: {stats(without_rates)['mean']:.0%}",
        f"- **delta**: {delta:+.0%}",
        "",
        "| eval | with_skill | without_skill |",
        "| --- | ---: | ---: |",
    ]
    wmap = {r["eval_name"]: r["pass_rate"] for r in with_rows}
    omap = {r["eval_name"]: r["pass_rate"] for r in without_rows}
    for ev in EVALS["evals"]:
        md.append(
            f"| {ev['name']} | {wmap.get(ev['name'], 0):.0%} | {omap.get(ev['name'], 0):.0%} |"
        )
    (WS / "benchmark.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"OK: {out}")
    print(f"with_skill mean={stats(with_rates)['mean']:.0%} without_skill mean={stats(without_rates)['mean']:.0%} delta={delta:+.0%}")


if __name__ == "__main__":
    main()
