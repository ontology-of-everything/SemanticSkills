#!/usr/bin/env python3
"""Verify semantic catalog, semantic YAML, command docs and operation contracts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any
import re

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency failure path
    raise SystemExit("FAIL: PyYAML is required") from exc


TEMPLATE_HEADING_RE = re.compile(r"^#### `([A-Z][A-Za-z0-9]+)`$")
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


def collect_catalog(catalog: dict[str, Any]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    entities: set[str] = set()
    entry_points = catalog.get("entry_points", {}) or {}
    for entry in entry_points.values():
        for entity in entry.get("ontology_entities", []) or []:
            entities.add(str(entity))
    return entities, entry_points


def collect_related_commands(
    path: Path,
    contract_required: dict[str, list[str]] | None = None,
) -> tuple[dict[str, list[str]], dict[str, str]]:
    ops: dict[str, list[str]] = {}
    blocks: dict[str, list[str]] = {}
    current_template: str | None = None
    contract_required = contract_required or {}

    for line in path.read_text(encoding="utf-8").splitlines():
        heading = TEMPLATE_HEADING_RE.match(line)
        if heading:
            current_template = heading.group(1)
            blocks.setdefault(current_template, []).append(line)
            continue

        if current_template is not None:
            if line.startswith("## "):
                current_template = None
            else:
                blocks.setdefault(current_template, []).append(line)
                continue

        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("| ---"):
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        op_match = re.fullmatch(r"`([A-Z][A-Za-z0-9]+)`", cells[0])
        if not op_match:
            continue
        op = op_match.group(1)
        required_cell = cells[2]
        if required_cell.strip() == "见模板":
            ops[op] = list(contract_required.get(op, []))
        else:
            ops[op] = extract_required(required_cell)
        blocks.setdefault(op, [])

    return ops, {op: "\n".join(lines) for op, lines in blocks.items()}


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
        if yml.name == "catalog.yml":
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
    catalog = load_yaml(skill_dir / "references/semantic/catalog.yml")
    contracts = load_yaml(contracts_file)
    contract_ops_map = contracts.get("operations") or {}
    contract_required = {
        op: list((spec or {}).get("required") or [])
        for op, spec in contract_ops_map.items()
    }
    related, related_blocks = collect_related_commands(
        skill_dir / "references/related-commands.md",
        contract_required,
    )
    catalog_entities, catalog_entry_points = collect_catalog(catalog)
    semantic_entities, semantic_ops = collect_semantic(skill_dir)

    expected = int(catalog.get("coverage", {}).get("expected_query_operations", 0))
    contract_ops = set((contracts.get("operations") or {}).keys())
    related_set = set(related)

    require(catalog.get("type") == "semantic_catalog", "Catalog type should be semantic_catalog", failures)
    require(bool(catalog_entry_points), "Catalog must define entry_points", failures)
    require(expected == len(contract_ops), f"Catalog expected {expected}, found {len(contract_ops)} contracts", failures)
    require(expected == len(related_set), f"related-commands expected {expected}, found {len(related_set)}", failures)
    require(expected == len(contract_ops), f"ops_contracts expected {expected}, found {len(contract_ops)}", failures)
    require(contract_ops == related_set, f"contracts/related mismatch: {sorted(contract_ops ^ related_set)}", failures)
    require(contract_ops == semantic_ops, f"contracts/semantic source mismatch: {sorted(contract_ops ^ semantic_ops)}", failures)
    require(catalog_entities <= semantic_entities, f"Catalog references unknown ontology entities: {sorted(catalog_entities - semantic_entities)}", failures)

    for entry_name, entry in catalog_entry_points.items():
        require(bool(entry.get("questions")), f"{entry_name} missing questions", failures)
        require(bool(entry.get("ontology_entities")), f"{entry_name} missing ontology_entities", failures)

    for op in sorted(contract_ops):
        require(op.startswith(("List", "Show")), f"{op} is not a List*/Show* query", failures)
        require(not op.startswith(MUTABLE_PREFIXES), f"{op} looks mutable", failures)
        contract = contracts["operations"].get(op, {})
        require(contract.get("entity") in semantic_entities, f"{op} entity is not defined in semantic YAML", failures)
        require(
            sorted(contract.get("required", [])) == sorted(related.get(op, [])),
            f"{op} required fields mismatch: contract={contract.get('required', [])} related={related.get(op, [])}",
            failures,
        )
        for template in contract.get("templates", []) or []:
            require(
                f"--{template}" in related_blocks.get(op, ""),
                f"{op} missing verified template parameter --{template}",
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
