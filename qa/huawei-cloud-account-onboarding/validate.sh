#!/usr/bin/env bash
# 通用 skill QA 模板：布局 + skills-ref + markdownlint + skillcheck + scripts 冒烟/e2e。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/huawei-cloud-account-onboarding" && pwd)"

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

run_local_or_npx() {
  local bin=$1; shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else need_cmd npx; npx "$bin" "$@"; fi
}

# skill 安装包纯度：不含 eval/qa/.workspaces 等。
# 本技能例外：scripts/ 是运行时载荷（mock server + QR/poll 客户端），允许存在。
check_skill_layout() {
  [[ -f "$SKILL_DIR/SKILL.md" ]] || fail "missing SKILL.md"
  [[ -f "$QA_DIR/README.md" ]] || fail "missing QA README"
  local item
  local forbidden=(.DS_Store .agents analysis evals qa tests .workspaces)
  for item in "${forbidden[@]}"; do
    [[ ! -e "$SKILL_DIR/$item" ]] || fail "forbidden in skill dir: $item"
  done
  local sibling
  for sibling in "$SKILL_DIR"/*-workspace; do
    [[ -e "$sibling" ]] || continue
    fail "Skill Creator workspace belongs at repo root, not skills/: $(basename "$sibling")"
  done
  [[ -f "$QA_DIR/evals/evals.json" ]] || fail "missing evals file: $QA_DIR/evals/evals.json"
  [[ -f "$QA_DIR/assertions/README.md" ]] || fail "missing assertions guide"
  [[ ! -f "$QA_DIR/evals.json" ]] || fail "duplicate eval source: $QA_DIR/evals.json"
  # node_modules 只允许本地存在，绝不能进 git
  if git -C "$ROOT" ls-files --error-unmatch "skills/huawei-cloud-account-onboarding/scripts/node_modules" >/dev/null 2>&1; then
    fail "node_modules must not be committed"
  fi
}

check_version_sync() {
  need_cmd python3
  QA_DIR="$QA_DIR" ROOT="$ROOT" SKILL_DIR="$SKILL_DIR" python3 - <<'PY'
import os, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("FAIL: PyYAML required for version sync check")
qa = Path(os.environ["QA_DIR"])
root = Path(os.environ["ROOT"])
skill = Path(os.environ["SKILL_DIR"])
expected = (qa / "VERSION").read_text(encoding="utf-8").strip()
catalog = yaml.safe_load((root / "docs/catalog.yml").read_text(encoding="utf-8"))
entry = next(x for x in catalog.get("skills", []) if x.get("id") == "huawei-cloud-account-onboarding")
if entry.get("version") != expected:
    sys.exit(f"FAIL: docs/catalog.yml version {entry.get('version')!r} != qa/VERSION ({expected})")
body = skill.joinpath("SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
meta = yaml.safe_load(body).get("metadata") or {}
if meta.get("version") != expected:
    sys.exit(f"FAIL: SKILL.md metadata.version != qa/VERSION ({expected})")
PY
}

# 脚本冒烟：语法 + 端到端（创建 → 扫码 → 通过 → 轮询终态）
check_scripts() {
  need_cmd node
  need_cmd curl
  local s
  for s in mock-server.js create-verification.js poll-verification.js; do
    node --check "$SKILL_DIR/scripts/$s" || fail "syntax error in scripts/$s"
  done
  [[ -d "$SKILL_DIR/scripts/node_modules/qrcode" ]] || (cd "$SKILL_DIR/scripts" && npm install --no-fund --no-audit >/dev/null)

  local port=3931 base="http://127.0.0.1:3931"
  HUAWEICLOUD_ONBOARDING_MOCK_PORT=$port HUAWEICLOUD_ONBOARDING_QR_TTL_SECONDS=60 \
    node "$SKILL_DIR/scripts/mock-server.js" >/dev/null 2>&1 &
  local server_pid=$!
  disown "$server_pid" 2>/dev/null || true
  trap 'kill "$server_pid" 2>/dev/null || true' RETURN
  local i
  for i in $(seq 1 20); do
    curl -sf "$base/healthz" >/dev/null 2>&1 && break
    [[ $i -lt 20 ]] || fail "mock server did not start"
    sleep 0.2
  done

  local vid
  vid=$(HUAWEICLOUD_ONBOARDING_BASE_URL=$base node "$SKILL_DIR/scripts/create-verification.js" \
    | sed -n 's/^VERIFICATION_ID=//p')
  [[ -n "$vid" ]] || fail "create-verification.js did not output VERIFICATION_ID"
  curl -sf "$base/verify/$vid" >/dev/null || fail "verify page unreachable"
  curl -sf -X POST "$base/verify/$vid/decision" -H 'Content-Type: application/json' \
    -d '{"action":"approve"}' >/dev/null || fail "decision endpoint failed"
  HUAWEICLOUD_ONBOARDING_BASE_URL=$base HUAWEICLOUD_ONBOARDING_POLL_INTERVAL_SECONDS=1 \
    node "$SKILL_DIR/scripts/poll-verification.js" "$vid" >/dev/null \
    || fail "poll-verification.js did not exit 0 on approved session"
  curl -sf "$base/v1/customers/me/verification-status" | rg -q '"verified": true' \
    || fail "account status did not flip to verified"
  kill "$server_pid" 2>/dev/null || true
}

need_cmd rg
check_skill_layout
check_version_sync
check_scripts
run_local_or_npx skills-ref validate "$SKILL_DIR"
(cd "$SKILL_DIR" && run_local_or_npx markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" "**/*.md" "!scripts/node_modules")
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: huawei-cloud-account-onboarding validation passed\n'
