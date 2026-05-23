#!/usr/bin/env bash
# Offline quality gate for huawei-cloud-billing-scout.
set -euo pipefail

QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$QA_DIR/../.." && pwd)"
SKILL_DIR="$ROOT/skills/huawei-cloud-billing-scout"
DOC_FILE="$ROOT/docs/skills/huawei-cloud-billing-scout.md"
CATALOG_FILE="$ROOT/docs/catalog.yml"
CURSOR_DOC="$ROOT/docs/agents/cursor.md"
CLAUDE_DOC="$ROOT/docs/agents/claude-code.md"
CODEX_DOC="$ROOT/docs/agents/codex.md"
EVALS_FILE="$QA_DIR/evals/evals.json"
CONTRACTS_FILE="$QA_DIR/fixtures/ops_contracts.yml"

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

need_cmd python3
need_cmd rg

check_layout() {
  local required=(
    "$SKILL_DIR/SKILL.md"
    "$SKILL_DIR/references/cli-installation.md"
    "$SKILL_DIR/references/iam-policies.md"
    "$SKILL_DIR/references/related-commands.md"
    "$SKILL_DIR/references/billing-playbook.md"
    "$SKILL_DIR/references/semantic/Catalog.yml"
    "$DOC_FILE"
    "$CATALOG_FILE"
    "$CURSOR_DOC"
    "$CLAUDE_DOC"
    "$CODEX_DOC"
    "$QA_DIR/README.md"
    "$QA_DIR/assertions/README.md"
    "$QA_DIR/bin/verify_ops.py"
    "$EVALS_FILE"
    "$CONTRACTS_FILE"
  )
  local forbidden=(.DS_Store .agents analysis evals qa tests .workspaces huawei-cloud-billing-scout-workspace)
  local file item

  for file in "${required[@]}"; do
    [[ -f "$file" ]] || fail "missing file: $file"
  done
  [[ ! -e "$SKILL_DIR/references/billing-semantics.md" ]] || fail "stale billing-semantics.md still exists"
  for item in "${forbidden[@]}"; do
    [[ ! -e "$SKILL_DIR/$item" ]] || fail "forbidden runtime bundle path: $item"
  done
}

check_text_guards() {
  local hits
  hits=$(rg -n 'billing-semantics|Semantic entities \(8\)' "$DOC_FILE" "$SKILL_DIR" "$ROOT/README.md" "$ROOT/README-CN.md" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "stale documentation text"; }

  hits=$(rg -n '≥2 stars|repo \*\*≥2|--agent claude($|[[:space:]])' "$DOC_FILE" "$ROOT/docs" "$ROOT/README.md" "$ROOT/README-CN.md" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "stale marketplace guidance"; }

  hits=$(rg -n -- '--dry-run' "$DOC_FILE" "$ROOT/README.md" "$ROOT/README-CN.md" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "unsupported ClawHub skill publish dry-run guidance"; }

  hits=$(rg -n 'hcloud[[:space:]]+BSS[[:space:]]+(Pay|Create|Update|Cancel|Renewal|Reclaim|Set|Send|Delete|Change|Claim|AutoRenewal)[A-Za-z0-9]+' "$SKILL_DIR" "$DOC_FILE" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "mutable BSS command example found"; }
}

check_yaml_and_docs() {
  python3 - "$ROOT" "$EVALS_FILE" <<'PY'
import json
import sys
from pathlib import Path

import yaml

root = Path(sys.argv[1])
evals_file = Path(sys.argv[2])
skill = root / "skills/huawei-cloud-billing-scout"

for path in sorted((skill / "references/semantic").glob("*.yml")) + [root / "docs/catalog.yml"]:
    yaml.safe_load(path.read_text(encoding="utf-8"))

frontmatter = yaml.safe_load(
    skill.joinpath("SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
)
if frontmatter.get("name") != "huawei-cloud-billing-scout":
    raise SystemExit("SKILL.md name mismatch")
if "储值卡" not in frontmatter.get("description", ""):
    raise SystemExit("SKILL.md description missing stored-value card trigger")
if "license" in frontmatter:
    raise SystemExit("SKILL.md must omit license to avoid ClawHub MIT-0 conflict")

openclaw = (frontmatter.get("metadata") or {}).get("openclaw") or {}
requires = openclaw.get("requires") or {}
if "hcloud" not in requires.get("bins", []):
    raise SystemExit("metadata.openclaw.requires.bins must include hcloud")
if "SemanticSkills/tree/main/skills/huawei-cloud-billing-scout" not in openclaw.get("homepage", ""):
    raise SystemExit("metadata.openclaw.homepage should point to the skill directory")
env_vars = {item.get("name"): item for item in openclaw.get("envVars", []) if isinstance(item, dict)}
for name in ["HUAWEICLOUD_SDK_AK", "HUAWEICLOUD_SDK_SK", "HUAWEICLOUD_SDK_REGION"]:
    if name not in env_vars:
        raise SystemExit(f"metadata.openclaw.envVars missing optional {name}")
    if env_vars[name].get("required") is not False:
        raise SystemExit(f"metadata.openclaw.envVars {name} must be optional")

docs_catalog = yaml.safe_load(root.joinpath("docs/catalog.yml").read_text(encoding="utf-8"))
entry = next((item for item in docs_catalog.get("skills", []) if item.get("id") == "huawei-cloud-billing-scout"), None)
if not entry:
    raise SystemExit("docs/catalog.yml missing huawei-cloud-billing-scout")
if entry.get("path") != "skills/huawei-cloud-billing-scout" or entry.get("qa") != "qa/huawei-cloud-billing-scout":
    raise SystemExit("docs/catalog.yml path/qa mismatch")
if entry.get("version") != "2.1.0":
    raise SystemExit("docs/catalog.yml version should be 2.1.0 for the 58-operation expansion")
if entry.get("distribution") != "direct-skill":
    raise SystemExit("docs/catalog.yml distribution should be direct-skill")
if "openclaw" not in entry.get("agents", []):
    raise SystemExit("docs/catalog.yml agents should include openclaw")
if "MIT-0" not in entry.get("clawhub_license", ""):
    raise SystemExit("docs/catalog.yml should document ClawHub MIT-0 terms")

doc = root.joinpath("docs/skills/huawei-cloud-billing-scout.md").read_text(encoding="utf-8")
for needle in [
    "58 unique read-only BSS query operations",
    "StoredValueCard",
    "quote_and_identity",
    "validate.sh",
    "clawhub skill publish",
    "clawscan-note",
    "claude-code-skill",
    "MIT-0",
]:
    if needle not in doc:
        raise SystemExit(f"skill docs missing: {needle}")

repo_docs = "\n".join(
    root.joinpath(path).read_text(encoding="utf-8")
    for path in [
        "README.md",
        "README-CN.md",
        "docs/authoring.md",
        "docs/agents/cursor.md",
        "docs/agents/claude-code.md",
        "docs/agents/codex.md",
    ]
)
for needle in ["clawhub skill publish", "claude-skills", "--agent claude-code", "--agent codex"]:
    if needle not in repo_docs:
        raise SystemExit(f"repo docs missing marketplace guidance: {needle}")

data = json.loads(evals_file.read_text(encoding="utf-8"))
if data.get("skill_name") != "huawei-cloud-billing-scout":
    raise SystemExit("eval skill_name mismatch")
evals = data.get("evals")
if not isinstance(evals, list) or len(evals) < 17:
    raise SystemExit("expected at least 17 eval cases")
domains = set()
entities = set()
names = set()
for item in evals:
    required = {"id", "name", "prompt", "expected_output", "files", "assertions", "covers"}
    missing = required - item.keys()
    if missing:
        raise SystemExit(f"eval {item.get('id')} missing {sorted(missing)}")
    if item["name"] in names:
        raise SystemExit(f"duplicate eval name: {item['name']}")
    names.add(item["name"])
    if not isinstance(item["files"], list):
        raise SystemExit(f"eval {item['name']} files must be list")
    assertions = item["assertions"]
    if not isinstance(assertions, list) or len(assertions) < 4 or len(set(assertions)) != len(assertions):
        raise SystemExit(f"eval {item['name']} needs >=4 unique assertions")
    covers = item["covers"]
    domains.update(covers.get("domains", []))
    entities.update(covers.get("entities", []))

catalog = yaml.safe_load(skill.joinpath("references/semantic/Catalog.yml").read_text(encoding="utf-8"))
expected_domains = set(catalog["domains"])
if domains != expected_domains:
    raise SystemExit(f"eval domain coverage mismatch: {sorted(expected_domains - domains)}")

semantic_entities = set()
for path in sorted((skill / "references/semantic").glob("*.yml")):
    if path.name == "Catalog.yml":
        continue
    obj = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if obj.get("name"):
        semantic_entities.add(obj["name"])
    for entity in obj.get("entities", []) or []:
        if isinstance(entity, dict) and entity.get("name"):
            semantic_entities.add(entity["name"])
missing_entities = semantic_entities - entities
if missing_entities:
    raise SystemExit(f"eval entity coverage missing: {sorted(missing_entities)}")

print(f"yaml/docs/evals ok: {len(evals)} evals, {len(semantic_entities)} semantic entities")
PY
}

check_layout
check_text_guards
check_yaml_and_docs
python3 "$QA_DIR/bin/verify_ops.py" "$SKILL_DIR" "$CONTRACTS_FILE"

printf 'OK: huawei-cloud-billing-scout validation passed\n'
