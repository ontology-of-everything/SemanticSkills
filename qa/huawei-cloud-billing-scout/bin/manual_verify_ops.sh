#!/usr/bin/env bash
# huawei-cloud-billing-scout 维护者辅助：列出 Operation、打印命令模板、可选 help 校验。
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QA_DIR="$(cd "$BIN_DIR/.." && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/huawei-cloud-billing-scout" && pwd)"
VERIFY_PY="$BIN_DIR/verify_ops.py"
CONTRACTS_FILE="$QA_DIR/fixtures/ops_contracts.yml"

run_verify() { python3 "$VERIFY_PY" "$SKILL_DIR" "$CONTRACTS_FILE" "$@"; }

usage() {
  cat <<'EOF'
Manual operation verifier for huawei-cloud-billing-scout.

Usage:
  ./bin/manual_verify_ops.sh ListCosts
  ./bin/manual_verify_ops.sh --list
  ./bin/manual_verify_ops.sh --verify-help
EOF
}

[[ "${1:-}" == "--help" || "${1:-}" == "-h" || $# -eq 0 ]] && { usage; exit 0; }

# 列出 ops_contracts.yml 中全部 Operation 及对应 semantic 实体
[[ "${1:-}" == "--list" ]] && {
  python3 - "$CONTRACTS_FILE" <<'PY'
import sys, yaml
for name, spec in sorted(yaml.safe_load(open(sys.argv[1], encoding="utf-8"))["operations"].items()):
    print(f"{name}\t{spec.get('entity', '')}")
PY
  exit 0
}

# 对照本机 hcloud --help（需安装 KooCLI）
[[ "${1:-}" == "--verify-help" ]] && exec run_verify --with-help

run_verify --print-command "$1"
