#!/usr/bin/env bash
# huawei-cloud-billing-scout 质量门禁：布局、eval、语义路由、跨层契约、安装纯度、外部 linter。
# CI 入口：tools/validate-all.sh；可选 HUAWEICLOUD_BILLING_SCOUT_REAL=1 做真实 BSS 冒烟。
set -euo pipefail

QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/huawei-cloud-billing-scout" && pwd)"
EVALS_FILE="$QA_DIR/evals/evals.json"
CONTRACTS_FILE="$QA_DIR/fixtures/ops_contracts.yml"
VERIFY_PY="$QA_DIR/bin/verify_ops.py"
MANUAL_VERIFY="$QA_DIR/bin/manual_verify_ops.sh"

run_verify_ops() {
  python3 "$VERIFY_PY" "$SKILL_DIR" "$CONTRACTS_FILE" "$@"
}

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

run_local_or_npx() {
  local bin=$1; shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else need_cmd npx; npx "$bin" "$@"; fi
}

# rg 命中 pattern 则失败（用于禁止写操作示例、ECS 残留等）
check_rg() {
  local label=$1 pattern=$2 hits
  hits=$(rg -n "$pattern" "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references" 2>/dev/null | head -80 || true)
  [[ -z "$hits" ]] || { printf '%s\n' "$hits" >&2; fail "$label"; }
}

# skill 必需文件、禁止 eval/qa 混入安装包、QA 侧必需产物
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
  [[ ! -f "$QA_DIR/evals.json" ]] || fail "duplicate eval source: $QA_DIR/evals.json"
  [[ -f "$QA_DIR/assertions/README.md" ]] || fail "missing assertions guide"
  [[ -f "$CONTRACTS_FILE" ]] || fail "missing operation contracts"
  [[ -f "$VERIFY_PY" ]] || fail "missing verify_ops.py"
  [[ -f "$MANUAL_VERIFY" ]] || fail "missing manual operation verifier"
  [[ -f "$QA_DIR/README.md" ]] || fail "missing QA README"
}

# evals.json 字段完整性：Skill Creator 用例结构
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

# 文档口径：禁止错误字段名；ChangeRecords 只读策略必须存在且不被宽泛 Change 规则误伤
check_semantic_consistency() {
  check_rg "ResourceBillDetail has stale resource_Type_code path" \
    'resource_Type_code'

  rg -q 'ListCustomer(Account|Coupon)ChangeRecords' \
    "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references" \
    || fail "missing readonly ChangeRecords policy"

  check_rg "readonly ChangeRecords blocked by broad Change rule" \
    '禁止.*`Change`|`Change`.*写操作|名称含.*`Change`'
}

# eval 数量不少于 semantic 实体数
check_eval_entity_coverage() {
  need_cmd python3
  python3 - "$EVALS_FILE" "$SKILL_DIR" <<'PY'
import json, sys
from pathlib import Path

evals = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["evals"]
entities = len(list(Path(sys.argv[2], "references/semantic").glob("*.yml")))
if len(evals) < entities:
    raise SystemExit(f"eval count {len(evals)} < semantic entities {entities}")
print(f"eval entity coverage ok: {len(evals)} evals >= {entities} entities")
PY
}

# semantic YAML 中的 source_operation 必须在 related-commands.md 出现
check_semantic_routing() {
  need_cmd python3
  python3 - "$SKILL_DIR" <<'PY'
import re, sys
from pathlib import Path

skill = Path(sys.argv[1])
cmds = (skill / "references/related-commands.md").read_text(encoding="utf-8")
missing = []
for yml in sorted((skill / "references/semantic").glob("*.yml")):
    text = yml.read_text(encoding="utf-8")
    ops = re.findall(r"source_operations?:\s*\n((?:\s+-\s+.+\n)+)|source_operation:\s*(.+)", text)
    found = []
    for block, single in ops:
        if single:
            found.append(single.strip())
        if block:
            found.extend(re.findall(r"-\s*(.+)", block))
    for op in found:
        name = op.split("/")[-1].strip()
        if name and name not in cmds:
            missing.append(f"{yml.name}: {name}")
if missing:
    print("\n".join(missing), file=sys.stderr)
    sys.exit(1)
print(f"semantic routing ok: {len(list((skill / 'references/semantic').glob('*.yml')))} entities")
PY
}

# skill-scanner：阻断 CRITICAL/HIGH 发现
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

# 模拟 npx skills add，确认安装包纯净
run_npx_install_check() {
  need_cmd npx
  local tmp_home tmp_project
  tmp_home=$(mktemp -d)
  tmp_project=$(mktemp -d)
  (cd "$tmp_project" && HOME="$tmp_home" npx skills add "$SKILL_DIR" \
    --skill huawei-cloud-billing-scout --agent cursor --yes --copy)
}

# 可选：真实 BSS 只读调用（需本机 hcloud 凭据）
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
check_semantic_routing
check_eval_entity_coverage
run_verify_ops
if [[ "${HUAWEICLOUD_BILLING_SCOUT_VERIFY_HELP:-0}" == "1" ]]; then
  run_verify_ops --with-help
fi
# 命令文档中不得出现可变 BSS 写操作示例
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
