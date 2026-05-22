#!/usr/bin/env python3
"""Scaffold skill-creator iteration-1 dirs from evals.json (metadata only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EVALS = REPO / "qa/huawei-cloud-billing-scout/evals/evals.json"
WS = REPO / ".workspaces/huawei-cloud-billing-scout/iteration-1"


def main() -> None:
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    WS.mkdir(parents=True, exist_ok=True)
    for ev in data["evals"]:
        name = ev["name"]
        for cfg in ("with_skill", "without_skill"):
            base = WS / name / cfg
            (base / "outputs").mkdir(parents=True, exist_ok=True)
            meta = {
                "eval_id": ev["id"],
                "eval_name": name,
                "prompt": ev["prompt"],
                "assertions": ev["assertions"],
            }
            (base / "eval_metadata.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    print(f"OK: scaffolded {len(data['evals'])} evals x 2 configs under {WS}")


if __name__ == "__main__":
    main()
