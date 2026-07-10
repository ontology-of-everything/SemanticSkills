#!/usr/bin/env bash
# 通用 skill QA 模板：布局 + skills-ref + markdownlint + skillcheck。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/semantic-creator" && pwd)"

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
entry = next(x for x in catalog.get("skills", []) if x.get("id") == "semantic-creator")
if entry.get("version") != expected:
    sys.exit(f"FAIL: docs/catalog.yml version {entry.get('version')!r} != qa/VERSION ({expected})")
body = skill.joinpath("SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
meta = yaml.safe_load(body).get("metadata") or {}
if meta.get("version") != expected:
    sys.exit(f"FAIL: SKILL.md metadata.version != qa/VERSION ({expected})")
PY
}

check_review_workbench() {
  need_cmd python3
  need_cmd node
  SKILL_DIR="$SKILL_DIR" QA_DIR="$QA_DIR" python3 - <<'PY'
import json
import os
from pathlib import Path

skill = Path(os.environ["SKILL_DIR"])
qa = Path(os.environ["QA_DIR"])
template = skill.joinpath("assets/review-template.html").read_text(encoding="utf-8")
review = skill.joinpath("references/review.md").read_text(encoding="utf-8")

if template.count("/*__MODEL_JSON__*/") != 1:
    raise SystemExit("FAIL: review template must contain exactly one model placeholder")

required_template = [
    "allApproved()", "depends_on", "confirm", "select", "correct", "supplement",
    "reject", "approved: !!approve", "d._action = ''", "findDecision(r.target)",
    "接口明证（explicit）", "待决（pending）", ':disabled="!allApproved()"',
]
for token in required_template:
    if token not in template:
        raise SystemExit(f"FAIL: review template missing decision contract: {token}")

required_review = [
    "object", "decision", "option", "relation", "constraint", "evidence",
    "basis", "confidence", "status", "risk", "approved:true",
]
for token in required_review:
    if token not in review:
        raise SystemExit(f"FAIL: review spec missing ontology concept: {token}")

for stale in ("approved_rest", "verdicts.json", "c.verdict"):
    if stale in template or stale in review:
        raise SystemExit(f"FAIL: stale review contract remains: {stale}")

evals = json.loads(qa.joinpath("evals/evals.json").read_text(encoding="utf-8"))
review_eval = next(e for e in evals["evals"] if e["id"] == 6)
if len(review_eval.get("expectations", [])) < 7:
    raise SystemExit("FAIL: review eval does not cover the decision workbench")
PY

  local js
  js="${TMPDIR:-/tmp}/semantic-review-check-$$.js"
  python3 - "$SKILL_DIR/assets/review-template.html" >"$js" <<'PY'
import re
import sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding="utf-8")
for attrs, body in re.findall(r"<script([^>]*)>(.*?)</script>", html, re.S):
    if "application/json" not in attrs:
        print(body)
PY
  node --check "$js" || { rm -f "$js"; return 1; }
  rm -f "$js"
}

need_cmd rg
check_skill_layout
check_version_sync
check_review_workbench
run_local_or_npx skills-ref validate "$SKILL_DIR"
run_local_or_npx markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" "$SKILL_DIR/**/*.md"
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: semantic-creator validation passed\n'
