#!/usr/bin/env python3
"""Unified quality gate: fast (deterministic) | full (+ offline protocol eval) | style."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from qa_common import (
    CONTRACTS_FILE,
    QA_DIR,
    SKILL_DIR,
    ensure_bin_path,
    run_markdownlint,
    run_skill_scanner,
    run_skillcheck,
)

ensure_bin_path()

from gate_checks import (  # noqa: E402
    check_docs_and_evals,
    check_layout,
    check_text_guards,
)
from protocol_grading import run_protocol_suite  # noqa: E402


def _run_verify_ops() -> None:
    script = QA_DIR / "bin/verify_ops.py"
    subprocess.run(
        [sys.executable, str(script), str(SKILL_DIR), str(CONTRACTS_FILE)],
        check=True,
    )


def _run_export_count() -> int:
    script = QA_DIR / "bin/export_llm_eval.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    return len(lines)


def run_style(*, require_all: bool) -> None:
    has_sc = shutil.which("skillcheck")
    has_md = shutil.which("markdownlint-cli2")
    has_scan = shutil.which("skill-scanner")

    if require_all and not (has_sc and has_md and has_scan):
        raise SystemExit("FAIL: style gate requires skillcheck, markdownlint-cli2, and skill-scanner")

    if has_sc and has_md and has_scan:
        print("== skillcheck ==")
        run_skillcheck()
        print("== markdownlint-cli2 ==")
        run_markdownlint()
        print("== skill-scanner ==")
        run_skill_scanner()
        print("style: ok")
        return

    if has_md:
        run_markdownlint()
        print("style: markdownlint ok")
    elif not require_all:
        print("style: skip markdownlint-cli2 (not installed)")
    elif require_all:
        raise SystemExit("FAIL: markdownlint-cli2 not installed")

    if has_sc:
        run_skillcheck()
        print("style: skillcheck ok")
    elif not require_all:
        print("style: skip skillcheck (not installed)")
    elif require_all:
        raise SystemExit("FAIL: skillcheck not installed")

    if has_scan:
        run_skill_scanner()
        print("style: skill-scanner ok")
    elif not require_all:
        print("style: skip skill-scanner (not installed)")
    elif require_all:
        raise SystemExit("FAIL: skill-scanner not installed")


def cmd_fast(args: argparse.Namespace) -> int:
    check_layout()
    check_text_guards()
    eval_count, entity_count = check_docs_and_evals()
    print(
        f"yaml/docs/evals ok: {eval_count} evals, "
        f"{entity_count} semantic entities, rubric ok"
    )
    _run_verify_ops()
    export_count = _run_export_count()
    if export_count != eval_count:
        raise SystemExit(
            f"FAIL: eval export expected {eval_count} lines, got {export_count}"
        )
    print(f"export: export_llm_eval ok ({export_count} cases)")
    if not args.skip_style:
        run_style(require_all=False)
    return 0


def cmd_full(args: argparse.Namespace) -> int:
    fast_args = argparse.Namespace(skip_style=True)
    cmd_fast(fast_args)
    if not args.skip_style:
        run_style(require_all=False)
    run_protocol_suite()
    print("OK: huawei-cloud-billing-scout validation passed")
    return 0


def cmd_style(_args: argparse.Namespace) -> int:
    run_style(require_all=True)
    print("OK: skill gate passed (0 errors, 0 warnings)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="huawei-cloud-billing-scout QA gate")
    sub = parser.add_subparsers(dest="command", required=True)

    fast = sub.add_parser("fast", help="Deterministic checks (layout, docs, ops, export)")
    fast.add_argument("--skip-style", action="store_true", help="Skip optional style tools")
    fast.set_defaults(func=cmd_fast)

    full = sub.add_parser("full", help="fast + protocol eval (CI / validate.sh)")
    full.add_argument("--skip-style", action="store_true", help="Skip optional style tools")
    full.set_defaults(func=cmd_full)

    style = sub.add_parser("style", help="skillcheck + markdownlint + skill-scanner")
    style.set_defaults(func=cmd_style)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
