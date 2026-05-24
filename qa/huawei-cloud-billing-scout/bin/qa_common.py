"""Shared offline QA utilities for huawei-cloud-billing-scout."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("FAIL: PyYAML is required") from exc

BIN_DIR = Path(__file__).resolve().parent
QA_DIR = BIN_DIR.parent
ROOT = QA_DIR.parents[1]
SKILL_DIR = ROOT / "skills/huawei-cloud-billing-scout"
DOC_FILE = ROOT / "docs/skills/huawei-cloud-billing-scout.md"
CONTRACTS_FILE = QA_DIR / "fixtures/ops_contracts.yml"
EVALS_FILE = QA_DIR / "evals/evals.json"
RUBRIC_FILE = QA_DIR / "evals/llm-rubric.yml"
VERSION_FILE = ROOT / "VERSION"

SCANNER_SEVERITIES = frozenset({"CRITICAL", "HIGH", "MEDIUM", "LOW", "WARNING"})
SKILLCHECK_ALLOWED_WARNINGS = frozenset({"disclosure.metadata-budget"})


def ensure_bin_path() -> None:
    path = str(BIN_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def load_eval_bundle() -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    data = load_json(EVALS_FILE)
    rubric = load_yaml(RUBRIC_FILE)
    return data, list(data.get("evals") or []), list(rubric.get("global_assertions") or [])


def merge_assertions(eval_item: dict[str, Any], global_assertions: list[str]) -> list[str]:
    return list(dict.fromkeys(global_assertions + list(eval_item.get("assertions") or [])))


def run_rg(pattern: str, paths: list[Path], *, count: bool = False) -> str:
    if not shutil.which("rg"):
        raise SystemExit("FAIL: missing command: rg")
    cmd = ["rg", "-c" if count else "-n", pattern, *[str(p) for p in paths]]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc.stdout.strip()


def parse_skill_frontmatter() -> dict[str, Any]:
    body = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
    return yaml.safe_load(body) or {}


def run_skillcheck(skill_md: Path | None = None, config: Path | None = None) -> None:
    target = skill_md or (SKILL_DIR / "SKILL.md")
    cfg = config or (QA_DIR / "skillcheck.toml")
    args = ["skillcheck", "--format", "json"]
    if cfg.is_file():
        args.extend(["--config", str(cfg)])
    args.append(str(target))
    raw = subprocess.run(args, capture_output=True, text=True, check=False)
    if raw.returncode not in (0, 1):
        print(raw.stderr or raw.stdout, file=sys.stderr)
        raise SystemExit(1)
    data = json.loads(raw.stdout)
    if any(not result.get("valid", True) for result in data.get("results", [])):
        raise SystemExit("skillcheck reported invalid files")
    unexpected = [
        diag
        for result in data.get("results", [])
        for diag in result.get("diagnostics", [])
        if diag.get("severity") == "warning"
        and diag.get("rule") not in SKILLCHECK_ALLOWED_WARNINGS
    ]
    if unexpected:
        for item in unexpected:
            print(item, file=sys.stderr)
        raise SystemExit("skillcheck reported unexpected warnings")


def run_markdownlint() -> None:
    config = QA_DIR / ".markdownlint.json"
    cmd = ["markdownlint-cli2"]
    if config.is_file():
        cmd.extend(["--config", str(config)])
    cmd.extend([str(SKILL_DIR / "SKILL.md"), str(SKILL_DIR / "references/**/*.md")])
    subprocess.run(cmd, check=True)


def run_skill_scanner() -> None:
    policy = QA_DIR / "policy.skill-scanner.yaml"
    proc = subprocess.run(
        ["skill-scanner", "scan", str(SKILL_DIR), "--policy", str(policy), "--format", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise SystemExit(proc.stderr or "skill-scanner failed")
    bad = [
        f
        for f in json.loads(proc.stdout or "{}").get("findings", [])
        if f.get("severity") in SCANNER_SEVERITIES
    ]
    if bad:
        print("skill-scanner findings:", bad, file=sys.stderr)
        raise SystemExit(1)
