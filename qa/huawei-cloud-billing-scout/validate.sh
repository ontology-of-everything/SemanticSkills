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
    "$SKILL_DIR/references/semantic/catalog.yml"
    "$SKILL_DIR/references/semantic/billing-ontology.yml"
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
  local legacy_semantic=(
    AccountBalance.yml
    AccountChangeRecord.yml
    AmortizedCost.yml
    BillingStatement.yml
    CostAnalysis.yml
    CouponChangeRecord.yml
    CouponQuota.yml
    EnterpriseAndPartnerContext.yml
    FreeResourcePackage.yml
    MonthlyBillSummary.yml
    OrderEvidence.yml
    PricingAndIdentity.yml
    ReferenceDimensions.yml
    ResourceBillDetail.yml
    ResourceBillRecord.yml
    ResourceUsage.yml
    StoredValueCard.yml
  )
  local file item

  for file in "${required[@]}"; do
    [[ -f "$file" ]] || fail "missing file: $file"
  done
  [[ ! -e "$SKILL_DIR/references/billing-playbook.md" ]] || fail "billing-playbook.md should be removed"
  [[ ! -e "$SKILL_DIR/references/billing-semantics.md" ]] || fail "stale billing-semantics.md still exists"
  for file in "${legacy_semantic[@]}"; do
    [[ ! -e "$SKILL_DIR/references/semantic/$file" ]] || fail "stale semantic shard still exists: $file"
  done
  for item in "${forbidden[@]}"; do
    [[ ! -e "$SKILL_DIR/$item" ]] || fail "forbidden runtime bundle path: $item"
  done
}

check_text_guards() {
  local hits
  hits=$(rg -n 'billing-semantics|Semantic entities \(8\)' "$DOC_FILE" "$SKILL_DIR" "$ROOT/README.md" "$ROOT/README-CN.md" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "stale documentation text"; }

  hits=$(rg -n 'billing-playbook\.md|Catalog\.yml' "$SKILL_DIR" "$DOC_FILE" "$QA_DIR/README.md" "$QA_DIR/assertions/README.md" "$QA_DIR/bin/verify_ops.py" "$QA_DIR/fixtures/ops_contracts.yml" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "stale playbook or uppercase catalog reference"; }

  hits=$(rg -n 'playbook_section|总体判断、分层事实' "$SKILL_DIR/references/semantic/catalog.yml" 2>/dev/null || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "stale catalog.yml routing text"; }

  if [[ "$(rg -c '^name: HuaweiCloudBillingSemanticCatalog$' "$SKILL_DIR/references/semantic/catalog.yml" 2>/dev/null || echo 0)" -ne 1 ]]; then
    fail "catalog.yml must contain exactly one root name block"
  fi

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
if entry.get("version") != "2.3.2":
    raise SystemExit("docs/catalog.yml version should match VERSION (2.3.2)")
if entry.get("distribution") != "direct-skill":
    raise SystemExit("docs/catalog.yml distribution should be direct-skill")
if "openclaw" not in entry.get("agents", []):
    raise SystemExit("docs/catalog.yml agents should include openclaw")
if "MIT-0" not in entry.get("clawhub_license", ""):
    raise SystemExit("docs/catalog.yml should document ClawHub MIT-0 terms")

doc = root.joinpath("docs/skills/huawei-cloud-billing-scout.md").read_text(encoding="utf-8")
for needle in [
    "ClawHub-first",
    "billing-ontology.yml",
    "catalog.yml",
    "58 unique read-only BSS query operations",
    "validate.sh",
    "clawhub skill publish",
    "clawscan-note",
    "claude-code-skill",
    "MIT-0",
    "Output Contract",
    "briefing-style",
    "conclusion-first summary",
    "chat-safe formatting",
]:
    if needle not in doc:
        raise SystemExit(f"skill docs missing: {needle}")

skill_text = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
for needle in [
    "语义本体",
    "答复格式",
    "不要把调查负担转交给接收人",
    "完整业务 ID",
    "profile/region",
    "未查不写",
    "请自行对账",
]:
    if needle not in skill_text:
        raise SystemExit(f"SKILL.md missing output contract guard: {needle}")
if "易懂的事实称呼" not in skill_text:
    raise SystemExit("SKILL.md missing output contract guard: 易懂的事实称呼")
if "业务说法" not in skill_text:
    raise SystemExit("SKILL.md missing output contract guard: 业务说法")
if not any(
    token in skill_text
    for token in ("0 元或低金额", "不得扩大成整月", "最终出账")
):
    raise SystemExit(
        "SKILL.md missing output contract guard: low-amount / scope ceiling (0 元或低金额 / 不得扩大成整月)"
    )

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
if not isinstance(evals, list) or len(evals) < 21:
    raise SystemExit("expected at least 21 eval cases")
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

contracts = yaml.safe_load(root.joinpath("qa/huawei-cloud-billing-scout/fixtures/ops_contracts.yml").read_text(encoding="utf-8"))
expected_domains = {
    str(item.get("domain"))
    for item in (contracts.get("operations") or {}).values()
    if isinstance(item, dict) and item.get("domain")
}
if domains != expected_domains:
    raise SystemExit(f"eval domain coverage mismatch: {sorted(expected_domains - domains)}")

semantic_entities = set()
for path in sorted((skill / "references/semantic").glob("*.yml")):
    if path.name == "catalog.yml":
        continue
    obj = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if obj.get("name") and obj.get("type") != "semantic_ontology":
        semantic_entities.add(obj["name"])
    for entity in obj.get("entities", []) or []:
        if isinstance(entity, dict) and entity.get("name"):
            semantic_entities.add(entity["name"])
missing_entities = semantic_entities - entities
if missing_entities:
    raise SystemExit(f"eval entity coverage missing: {sorted(missing_entities)}")

llm_eval = data.get("llm_eval") or {}
rubric_rel = llm_eval.get("rubric")
if rubric_rel != "evals/llm-rubric.yml":
    raise SystemExit("evals.json llm_eval.rubric must be evals/llm-rubric.yml")
rubric_path = root / "qa/huawei-cloud-billing-scout" / rubric_rel
if not rubric_path.is_file():
    raise SystemExit(f"missing LLM rubric: {rubric_path}")
rubric = yaml.safe_load(rubric_path.read_text(encoding="utf-8")) or {}
dims = rubric.get("dimensions") or []
if len(dims) < 4:
    raise SystemExit("llm-rubric.yml needs >=4 dimensions")
global_assertions = rubric.get("global_assertions") or []
if len(global_assertions) < 3:
    raise SystemExit("llm-rubric.yml needs >=3 global_assertions")
export_script = root / "qa/huawei-cloud-billing-scout" / (llm_eval.get("export") or "")
if not export_script.is_file():
    raise SystemExit(f"missing LLM export script: {export_script}")

print(f"yaml/docs/evals ok: {len(evals)} evals, {len(semantic_entities)} semantic entities, llm rubric ok")
PY
}

check_style_gates() {
  local ml_config="$SKILL_DIR/.markdownlint.json"
  if command -v markdownlint-cli2 >/dev/null 2>&1; then
    if [[ -f "$ml_config" ]]; then
      markdownlint-cli2 --config "$ml_config" "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references/**/*.md" \
        || fail "markdownlint-cli2 reported errors"
    else
      markdownlint-cli2 "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references/**/*.md" \
        || fail "markdownlint-cli2 reported errors"
    fi
    printf 'style: markdownlint ok\n'
  else
    printf 'style: skip markdownlint-cli2 (not installed)\n'
  fi

  if command -v skillcheck >/dev/null 2>&1; then
    local sc_config="$SKILL_DIR/skillcheck.toml"
    local sc_args=()
    [[ -f "$sc_config" ]] && sc_args=(--config "$sc_config")
    python3 - "${sc_args[@]}" "$SKILL_DIR/SKILL.md" <<'PY' || fail "skillcheck failed"
import json
import subprocess
import sys

args = sys.argv[1:]
path = args[-1]
cmd = ["skillcheck", "--format", "json", *args[:-1], path]
raw = subprocess.run(cmd, capture_output=True, text=True, check=False)
if raw.returncode not in (0, 1):
    print(raw.stderr or raw.stdout, file=sys.stderr)
    raise SystemExit(1)
data = json.loads(raw.stdout)
allowed_warnings = {"disclosure.metadata-budget"}
failed = 0
unexpected = []
for result in data.get("results", []):
    if not result.get("valid", True):
        failed += 1
    for diag in result.get("diagnostics", []):
        sev = diag.get("severity")
        rule = diag.get("rule")
        if sev == "warning" and rule not in allowed_warnings:
            unexpected.append(diag)
if failed:
    raise SystemExit("skillcheck reported invalid files")
if unexpected:
    for item in unexpected:
        print(item, file=sys.stderr)
    raise SystemExit("skillcheck reported unexpected warnings")
print("skillcheck: pass (OpenClaw metadata-budget warning allowed)")
PY
    printf 'style: skillcheck ok\n'
  else
    printf 'style: skip skillcheck (not installed)\n'
  fi
}

check_llm_eval_export() {
  local count
  count=$(python3 "$QA_DIR/bin/export_llm_eval.py" 2>/dev/null | wc -l | tr -d ' ')
  [[ "$count" -eq 21 ]] || fail "LLM eval export expected 21 lines, got ${count:-0}"
  printf 'llm: export_llm_eval ok (%s cases)\n' "$count"
}

check_protocol_eval() {
  python3 "$QA_DIR/bin/run_protocol_eval.py" || fail "protocol eval (LLM assertions) failed"
  printf 'llm: protocol eval ok\n'
}

check_layout
check_text_guards
check_yaml_and_docs
check_style_gates
check_llm_eval_export
check_protocol_eval
python3 "$QA_DIR/bin/verify_ops.py" "$SKILL_DIR" "$CONTRACTS_FILE"

printf 'OK: huawei-cloud-billing-scout validation passed\n'
