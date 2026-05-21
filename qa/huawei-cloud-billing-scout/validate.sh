#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$TEST_DIR/../../skills/huawei-cloud-billing-scout" && pwd)"
EVALS_FILE="$TEST_DIR/evals/evals.json"

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

run_local_or_npx() {
  local bin=$1; shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else need_cmd npx; npx "$bin" "$@"; fi
}

check_rg() {
  local label=$1 pattern=$2 hits
  hits=$(rg -n "$pattern" "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references" 2>/dev/null | head -80 || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "$label"; }
}

check_skill_layout() {
  local f item
  local files=(
    SKILL.md
    references/cli-installation.md
    references/iam-policies.md
    references/related-commands.md
    references/billing-playbook.md
    references/billing-semantics.md
    references/semantic/AccountBalance.yml
    references/semantic/MonthlyBillSummary.yml
    references/semantic/ResourceBillRecord.yml
    references/semantic/ResourceBillDetail.yml
    references/semantic/FreeResourcePackage.yml
    references/semantic/AccountChangeRecord.yml
    references/semantic/CouponChangeRecord.yml
    references/semantic/CostAnalysis.yml
  )
  local forbidden=(.DS_Store .agents analysis evals qa scripts tests .workspaces huawei-cloud-billing-scout-workspace)

  for f in "${files[@]}"; do [[ -f "$SKILL_DIR/$f" ]] || fail "missing file: $f"; done
  for item in "${forbidden[@]}"; do [[ ! -e "$SKILL_DIR/$item" ]] || fail "forbidden in skill dir: $item"; done
  [[ -f "$EVALS_FILE" ]] || fail "missing evals file: $EVALS_FILE"
  [[ ! -f "$TEST_DIR/evals.json" ]] || fail "duplicate eval source: $TEST_DIR/evals.json"
  [[ -f "$TEST_DIR/assertions/README.md" ]] || fail "missing assertions guide"
}

check_eval_schema() {
  need_cmd python3
  python3 - "$EVALS_FILE" <<'PY'
import json, sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if data.get("skill_name") != "huawei-cloud-billing-scout":
    raise SystemExit("skill_name mismatch")

evals = data.get("evals")
if not isinstance(evals, list) or not evals:
    raise SystemExit("evals must be a non-empty list")

required = {"id", "name", "prompt", "expected_output", "files", "assertions"}
names = set()
for item in evals:
    missing = required - item.keys()
    if missing:
        raise SystemExit(f"eval {item.get('id', '<unknown>')} missing {', '.join(sorted(missing))}")
    name = item["name"]
    if name in names:
        raise SystemExit(f"duplicate eval name: {name}")
    names.add(name)
    if not isinstance(item["files"], list):
        raise SystemExit(f"eval {name} files must be a list")
    assertions = item["assertions"]
    if not isinstance(assertions, list) or len(assertions) < 3 or len(set(assertions)) != len(assertions):
        raise SystemExit(f"eval {name} needs >=3 unique assertions")

print(f"eval schema ok: {len(evals)} cases")
PY
}

check_semantic_consistency() {
  check_rg "ResourceBillDetail has stale resource_Type_code path" \
    'resource_Type_code'

  rg -q 'ListCustomer(Account|Coupon)ChangeRecords' \
    "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references" \
    || fail "missing readonly ChangeRecords policy"

  check_rg "readonly ChangeRecords blocked by broad Change rule" \
    '禁止.*`Change`|`Change`.*写操作|名称含.*`Change`'
}

run_scanner() {
  need_cmd skill-scanner
  local report
  report=$(mktemp)
  skill-scanner scan "$SKILL_DIR" --use-trigger --enable-meta --policy balanced \
    --format json --output-json "$report" >/dev/null 2>&1 || true
  python3 - "$report" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
bad = [f for f in data.get("findings", []) if f.get("severity", "").upper() in {"CRITICAL", "HIGH"}]
if bad:
    print(json.dumps(bad, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(1)
print(f"skill-scanner ok: max_severity={data.get('max_severity')}, findings={data.get('findings_count')}")
PY
  rm -f "$report"
}

run_npx_install_check() {
  need_cmd npx
  local tmp_home tmp_project
  tmp_home=$(mktemp -d)
  tmp_project=$(mktemp -d)
  (cd "$tmp_project" && HOME="$tmp_home" npx skills add "$SKILL_DIR" \
    --skill huawei-cloud-billing-scout --agent cursor --yes --copy)
}

run_real_smoke() {
  [[ "${HUAWEICLOUD_BILLING_SCOUT_REAL:-0}" == "1" ]] || return 0
  need_cmd hcloud
  local region=${HUAWEICLOUD_BILLING_SCOUT_REGION:-cn-north-1}
  hcloud BSS ShowCustomerAccountBalances --cli-region="$region" --cli-read-timeout=30 >/tmp/huawei_billing_balance.json
  hcloud BSS ShowCustomerMonthlySum --bill_cycle="${HUAWEICLOUD_BILLING_SCOUT_CYCLE:?set cycle}" \
    --limit=3 --cli-region="$region" --cli-read-timeout=30 >/tmp/huawei_billing_monthly.json
  python3 -c 'import json; [json.load(open(p)) for p in ("/tmp/huawei_billing_balance.json","/tmp/huawei_billing_monthly.json")]; print("real smoke json parse ok")'
}

need_cmd rg
check_skill_layout
check_eval_schema
check_semantic_consistency
check_rg "forbidden mutable KooCLI operations found" \
  'hcloud[[:space:]]+[A-Za-z0-9/-]+[[:space:]]+(Pay|Renewal|Cancel|Reclaim|Update|Create|Delete|Set|Change|Send|Claim|AutoRenewal)[A-Za-z0-9/-]*'
check_rg "ECS diagnosis residue found" \
  'SSH|VNC|安全组规则|NovaStart|NovaStop|NovaReboot|DeleteServers|CreateSecurityGroup|sshpass'
run_local_or_npx skills-ref validate "$SKILL_DIR"
run_local_or_npx markdownlint-cli2 "$SKILL_DIR/**/*.md"
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70
run_scanner
run_npx_install_check
run_real_smoke

printf 'OK: huawei-cloud-billing-scout validation passed\n'
