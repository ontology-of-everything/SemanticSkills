#!/usr/bin/env python3
"""Verify Catalog, semantic YAML, command docs and operation contracts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency failure path
    raise SystemExit("FAIL: PyYAML is required") from exc


OP_HEADING_RE = re.compile(r"^### `([A-Z][A-Za-z0-9]+)`$")
MUTABLE_PREFIXES = (
    "Pay",
    "Create",
    "Update",
    "Cancel",
    "Renewal",
    "Reclaim",
    "Set",
    "Send",
    "Delete",
    "Change",
    "Claim",
    "AutoRenewal",
)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def defaults() -> tuple[Path, Path]:
    qa_dir = Path(__file__).resolve().parents[1]
    return (
        (qa_dir / "../../skills/huawei-cloud-billing-scout").resolve(),
        qa_dir / "fixtures/ops_contracts.yml",
    )


def extract_required(cell: str) -> list[str]:
    cell = cell.strip()
    if cell == "-":
        return []
    return re.findall(r"`([^`]+)`", cell)


def collect_catalog(catalog: dict[str, Any]) -> tuple[list[str], dict[str, str]]:
    ops: list[str] = []
    domains: dict[str, str] = {}
    for domain_name, domain in catalog.get("domains", {}).items():
        for op in domain.get("operations", []):
            ops.append(op)
            domains[op] = domain_name
    return ops, domains


def collect_related_commands(path: Path) -> dict[str, list[str]]:
    ops: dict[str, list[str]] = {}
    current: str | None = None
    collecting_required = False

    for line in path.read_text(encoding="utf-8").splitlines():
        heading = OP_HEADING_RE.match(line)
        if heading:
            current = heading.group(1)
            ops[current] = []
            collecting_required = False
            continue

        if current is None:
            continue

        if line.startswith("- 必填："):
            values = extract_required(line)
            ops[current].extend(values)
            collecting_required = "无" not in line
            continue

        if collecting_required:
            if line.startswith("  - "):
                ops[current].extend(extract_required(line))
                continue
            if line.strip():
                collecting_required = False

    return ops


def walk_sources(obj: Any, out: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "source_operation":
                out.append(str(value).split("/")[-1])
            elif key == "source_operations":
                out.extend(str(item).split("/")[-1] for item in value)
            else:
                walk_sources(value, out)
    elif isinstance(obj, list):
        for item in obj:
            walk_sources(item, out)


def collect_semantic(skill_dir: Path) -> tuple[set[str], set[str]]:
    entity_names: set[str] = set()
    source_ops: list[str] = []
    for yml in sorted((skill_dir / "references/semantic").glob("*.yml")):
        if yml.name == "Catalog.yml":
            continue
        data = load_yaml(yml)
        if data.get("name"):
            entity_names.add(str(data["name"]))
        for entity in data.get("entities", []) or []:
            if isinstance(entity, dict) and entity.get("name"):
                entity_names.add(str(entity["name"]))
        walk_sources(data, source_ops)
    return entity_names, set(source_ops)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def verify(skill_dir: Path, contracts_file: Path) -> list[str]:
    failures: list[str] = []
    catalog = load_yaml(skill_dir / "references/semantic/Catalog.yml")
    contracts = load_yaml(contracts_file)
    related = collect_related_commands(skill_dir / "references/related-commands.md")
    catalog_ops, catalog_domains = collect_catalog(catalog)
    semantic_entities, semantic_ops = collect_semantic(skill_dir)

    expected = int(catalog.get("coverage", {}).get("expected_query_operations", 0))
    contract_ops = set((contracts.get("operations") or {}).keys())
    catalog_set = set(catalog_ops)
    related_set = set(related)

    require(len(catalog_ops) == len(catalog_set), "Catalog has duplicate operations", failures)
    require(expected == len(catalog_set), f"Catalog expected {expected}, found {len(catalog_set)}", failures)
    require(expected == len(related_set), f"related-commands expected {expected}, found {len(related_set)}", failures)
    require(expected == len(contract_ops), f"ops_contracts expected {expected}, found {len(contract_ops)}", failures)
    require(catalog_set == related_set, f"Catalog/related mismatch: {sorted(catalog_set ^ related_set)}", failures)
    require(catalog_set == contract_ops, f"Catalog/contracts mismatch: {sorted(catalog_set ^ contract_ops)}", failures)
    require(catalog_set == semantic_ops, f"Catalog/semantic source mismatch: {sorted(catalog_set ^ semantic_ops)}", failures)

    for op in sorted(catalog_set):
        require(op.startswith(("List", "Show")), f"{op} is not a List*/Show* query", failures)
        require(not op.startswith(MUTABLE_PREFIXES), f"{op} looks mutable", failures)
        contract = contracts["operations"].get(op, {})
        require(contract.get("domain") == catalog_domains.get(op), f"{op} domain mismatch", failures)
        require(contract.get("entity") in semantic_entities, f"{op} entity is not defined in semantic YAML", failures)
        require(
            sorted(contract.get("required", [])) == sorted(related.get(op, [])),
            f"{op} required fields mismatch: contract={contract.get('required', [])} related={related.get(op, [])}",
            failures,
        )

    return failures


def main() -> int:
    default_skill, default_contracts = defaults()
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", type=Path, default=default_skill)
    parser.add_argument("contracts_file", nargs="?", type=Path, default=default_contracts)
    args = parser.parse_args()

    failures = verify(args.skill_dir, args.contracts_file)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("operation contracts ok: 58 BSS query operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
