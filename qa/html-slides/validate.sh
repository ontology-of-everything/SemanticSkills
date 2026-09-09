#!/usr/bin/env bash
# 通用 skill QA 模板：布局 + skills-ref + markdownlint + skillcheck。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/html-slides" && pwd)"

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

run_local_or_npx() {
  local bin=$1; shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else need_cmd npx; npx "$bin" "$@"; fi
}

# skill 安装包纯度：不含 eval/qa/.workspaces 等
check_skill_layout() {
  [[ -f "$SKILL_DIR/SKILL.md" ]] || fail "missing SKILL.md"
  [[ -f "$SKILL_DIR/agents/openai.yaml" ]] || fail "missing agents/openai.yaml"
  rg -q '^name: html-slides$' "$SKILL_DIR/SKILL.md" || fail "frontmatter name mismatch"
  rg -q '\$html-slides' "$SKILL_DIR/agents/openai.yaml" || fail "default prompt must name the skill"
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
}

# 参考文件必须存在且被 SKILL.md 路由到；代码资产与风格文件成对。
check_references() {
  local ref style f
  for ref in process style-guide page-patterns deck-format visuals motion; do
    [[ -f "$SKILL_DIR/references/$ref.md" ]] || fail "missing reference: references/$ref.md"
    rg -q "references/$ref\.md" "$SKILL_DIR/SKILL.md" || fail "SKILL.md does not route to references/$ref.md"
  done
  for f in base.css runtime.js skeletons.html; do
    [[ -f "$SKILL_DIR/assets/core/$f" ]] || fail "missing assets/core/$f"
  done
  for style in generic huawei apple; do
    [[ -f "$SKILL_DIR/references/styles/$style.md" ]] || fail "missing styles/$style.md"
    [[ -f "$SKILL_DIR/assets/$style/vars-light.css" ]] || fail "missing assets/$style/vars-light.css"
  done
  [[ -f "$SKILL_DIR/references/styles/_template.md" ]] || fail "missing styles/_template.md"
  [[ -f "$SKILL_DIR/tools/export_pptx.py" ]] || fail "missing tools/export_pptx.py"
  python3 -m py_compile "$SKILL_DIR/tools/export_pptx.py" || fail "export_pptx.py does not compile"
  # 规则文档不再内嵌 HTML/CSS/JS 代码块：代码只住 assets/
  ! rg -q '^```(html|css|js|javascript)' "$SKILL_DIR"/references || fail "code block in references/*.md; move it to assets/"
  # 变量契约：每个风格变量文件都定义全部契约变量
  local v
  for f in "$SKILL_DIR"/assets/*/vars-*.css; do
    for v in bg bg-alt bg-cover surface line fg fg-body fg-muted accent accent-soft accent-2 font-sans font-mono radius shadow table-head; do
      rg -q -- "--$v:" "$f" || fail "$(basename "$(dirname "$f")")/$(basename "$f") lacks --$v"
    done
  done
  # 核心 CSS 与骨架不得硬编码品牌红
  ! rg -qi '#C7000B' "$SKILL_DIR/assets/core" || fail "brand color hardcoded in assets/core"
}

need_cmd rg
check_skill_layout
check_references
run_local_or_npx skills-ref validate "$SKILL_DIR"
run_local_or_npx markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" "$SKILL_DIR/**/*.md"
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: html-slides validation passed\n'
