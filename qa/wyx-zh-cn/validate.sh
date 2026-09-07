#!/usr/bin/env bash
# 通用 skill QA：布局 + skills-ref + markdownlint + skillcheck + runtime 语法。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/wyx-zh-cn" && pwd)"

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

run_local_or_npx() {
  local bin=$1; shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else need_cmd npx; npx "$bin" "$@"; fi
}

check_skill_layout() {
  [[ -f "$SKILL_DIR/SKILL.md" ]] || fail "missing SKILL.md"
  [[ -f "$SKILL_DIR/agents/openai.yaml" ]] || fail "missing agents/openai.yaml"
  [[ -f "$QA_DIR/README.md" ]] || fail "missing QA README"
  local item
  local forbidden=(.DS_Store .agents analysis evals qa scripts tests .workspaces)
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
  rg -q '^name: wyx-zh-cn$' "$SKILL_DIR/SKILL.md" || fail "frontmatter name mismatch"
  ! rg -q '^license:' "$SKILL_DIR/SKILL.md" || fail "SKILL.md must omit license to avoid ClawHub MIT-0 conflict"
  rg -q '\$wyx-zh-cn' "$SKILL_DIR/agents/openai.yaml" || fail "default prompt must name the skill"
  rg -q '^  allow_implicit_invocation: false$' "$SKILL_DIR/agents/openai.yaml" || fail "Codex implicit invocation must be disabled"
}

# 六个模式各有一份参考文件，SKILL.md 的路由表必须指得到实处。
check_references() {
  local ref
  for ref in audit concept drift-detection pipeline sync map hooks-runtime; do
    [[ -f "$SKILL_DIR/references/$ref.md" ]] || fail "missing reference: references/$ref.md"
    rg -q "references/$ref\.md" "$SKILL_DIR/SKILL.md" || fail "SKILL.md does not route to references/$ref.md"
  done
}

# runtime/ 是上游原样收录的 bash：至少保证它能被解析，且 hooks 注册完整。
check_runtime() {
  local script
  for script in session-start drift-context post-check; do
    [[ -f "$SKILL_DIR/runtime/scripts/$script.sh" ]] || fail "missing runtime script: $script.sh"
    bash -n "$SKILL_DIR/runtime/scripts/$script.sh" || fail "runtime script syntax error: $script.sh"
  done
  [[ -f "$SKILL_DIR/runtime/hooks/hooks.json" ]] || fail "missing runtime/hooks/hooks.json"
  [[ -f "$SKILL_DIR/runtime/.claude-plugin/plugin.json" ]] || fail "missing runtime plugin manifest"
  local hook
  for hook in SessionStart PreToolUse PostToolUse; do
    rg -q "\"$hook\"" "$SKILL_DIR/runtime/hooks/hooks.json" || fail "hooks.json missing $hook registration"
  done
  need_cmd python3
  python3 -c 'import json,sys; json.load(open(sys.argv[1])); json.load(open(sys.argv[2]))' \
    "$SKILL_DIR/runtime/hooks/hooks.json" "$SKILL_DIR/runtime/.claude-plugin/plugin.json" \
    || fail "runtime JSON is not parseable"
  [[ -f "$SKILL_DIR/LICENSE.upstream" ]] || fail "missing upstream MIT notice: LICENSE.upstream"
}

need_cmd rg
check_skill_layout
check_references
check_runtime
run_local_or_npx skills-ref validate "$SKILL_DIR"
run_local_or_npx markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" "$SKILL_DIR/**/*.md"
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: wyx-zh-cn validation passed\n'
