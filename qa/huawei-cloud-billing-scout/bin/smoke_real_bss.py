#!/usr/bin/env python3
"""Read-only BSS smoke when HUAWEICLOUD_BILLING_SCOUT_REAL=1 (maintainer / local hcloud)."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from qa_common import QA_DIR, ROOT, ensure_bin_path

ensure_bin_path()

CLI_REGION = "cn-north-1"
SENSITIVE_RE = re.compile(
    r'"(account_id|customer_id|sub_customer_id|resource_id|order_id|trade_id|'
    r'coupon_id|quota_id|card_id|access_key|secret|token|domain_id|project_id|'
    r'account_name)"\s*:\s*"[^"]+"',
    re.I,
)


def _redact_json(text: str) -> str:
    return SENSITIVE_RE.sub(lambda m: f'"{m.group(1)}": "<redacted>"', text)


def _run(op: str, extra: list[str]) -> dict:
    cmd = [
        "hcloud",
        "BSS",
        op,
        f"--cli-region={CLI_REGION}",
        "--cli-output=json",
        *extra,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    out = {
        "operation": op,
        "argv": cmd,
        "exit_code": proc.returncode,
        "ok": proc.returncode == 0,
    }
    if proc.stdout.strip():
        try:
            out["response"] = json.loads(proc.stdout)
        except json.JSONDecodeError:
            out["stdout"] = proc.stdout[:4000]
    if proc.stderr.strip():
        out["stderr"] = proc.stderr[:2000]
    return out


def _default_cycle() -> str:
    env = os.environ.get("HUAWEICLOUD_BILLING_SCOUT_CYCLE", "").strip()
    if env:
        return env
    now = datetime.now(timezone.utc)
    year, month = now.year, now.month
    if month == 1:
        return f"{year - 1}-12"
    return f"{year}-{month - 1:02d}"


def main() -> int:
    if os.environ.get("HUAWEICLOUD_BILLING_SCOUT_REAL") != "1":
        print("SKIP: set HUAWEICLOUD_BILLING_SCOUT_REAL=1 to run BSS smoke", file=sys.stderr)
        return 0

    if not shutil.which("hcloud"):
        print("FAIL: hcloud not in PATH", file=sys.stderr)
        return 1

    cycle = _default_cycle()
    cases = [
        ("ShowCustomerAccountBalances", []),
        ("ShowCustomerMonthlySum", [f"--bill_cycle={cycle}"]),
        ("ListServiceTypes", ["--limit=3", "--offset=0"]),
    ]

    results = []
    failures = 0
    for op, extra in cases:
        row = _run(op, extra)
        results.append(row)
        if not row["ok"]:
            failures += 1
            print(f"FAIL {op}: exit {row['exit_code']}", file=sys.stderr)
            if row.get("stderr"):
                print(row["stderr"][:500], file=sys.stderr)
        else:
            print(f"OK {op}")

    out_dir = ROOT / "huawei-cloud-billing-scout-workspace" / "smoke-real"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cli_region": CLI_REGION,
        "bill_cycle": cycle,
        "results": results,
    }
    raw_path = out_dir / "last-run.json"
    red_path = out_dir / "last-run.redacted.json"
    raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    red_path.write_text(_redact_json(raw_path.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"smoke log: {red_path}")

    if failures:
        return 1
    print(f"smoke ok: {len(cases)} read-only BSS calls, cycle={cycle}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
