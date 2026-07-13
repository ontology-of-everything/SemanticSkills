#!/usr/bin/env bash
# 通用 skill QA 模板：布局 + skills-ref + markdownlint + skillcheck。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/huawei-cloud-cost-estimation" && pwd)"

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
entry = next(x for x in catalog.get("skills", []) if x.get("id") == "huawei-cloud-cost-estimation")
if entry.get("version") != expected:
    sys.exit(f"FAIL: docs/catalog.yml version {entry.get('version')!r} != qa/VERSION ({expected})")
body = skill.joinpath("SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
meta = yaml.safe_load(body).get("metadata") or {}
if meta.get("version") != expected:
    sys.exit(f"FAIL: SKILL.md metadata.version != qa/VERSION ({expected})")
PY
}

# 写操作白名单：fixture ↔ lifecycle/commands.md 1:1；evals 写场景必须 dry-only
check_write_allowlist() {
  need_cmd python3
  [[ -f "$QA_DIR/fixtures/ops_contracts.yml" ]] || fail "missing fixtures/ops_contracts.yml"
  QA_DIR="$QA_DIR" SKILL_DIR="$SKILL_DIR" python3 - <<'PY'
import os, re, sys, json
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("FAIL: PyYAML required for allowlist check")
qa = Path(os.environ["QA_DIR"])
skill = Path(os.environ["SKILL_DIR"])
contracts = yaml.safe_load((qa / "fixtures/ops_contracts.yml").read_text(encoding="utf-8"))
create_ops = set(contracts["create_ops"])
cancel_ops = set(contracts["cancel_ops"])
cov = contracts["coverage"]
if len(create_ops) != cov["expected_create_operations"]:
    sys.exit(f"FAIL: create_ops count {len(create_ops)} != coverage {cov['expected_create_operations']}")
if len(cancel_ops) != cov["expected_cancel_operations"]:
    sys.exit(f"FAIL: cancel_ops count {len(cancel_ops)} != coverage {cov['expected_cancel_operations']}")
doc = (skill / "references/lifecycle/commands.md").read_text(encoding="utf-8")
doc_ops = set(re.findall(r"^\| `([A-Za-z]+/[A-Za-z0-9/]+)`", doc, re.M))
doc_ops -= {  # dependency-lookup read commands are not write ops
    op for op in doc_ops
    if re.search(r"/(List|Show|Keystone)", op)
}
want = create_ops | cancel_ops
if doc_ops != want:
    sys.exit("FAIL: lifecycle/commands.md ops != ops_contracts.yml\n"
             f"  only in doc: {sorted(doc_ops - want)}\n"
             f"  only in fixture: {sorted(want - doc_ops)}")
bss_mutable = [op for op in doc_ops if op.startswith("BSS/")] 
if set(bss_mutable) != cancel_ops:
    sys.exit(f"FAIL: BSS mutable ops must be exactly {sorted(cancel_ops)}, got {sorted(bss_mutable)}")
prefixes = tuple(contracts["forbidden_bss_write_prefixes"])
for md in skill.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    for m in re.finditer(r"hcloud BSS (\w+)", text):
        op = m.group(1)
        if op.startswith(prefixes):
            sys.exit(f"FAIL: forbidden BSS write op {op!r} in {md}")
evals = json.loads((qa / "evals/evals.json").read_text(encoding="utf-8"))
for case in evals["evals"]:
    blob = json.dumps(case, ensure_ascii=False)
    if "lifecycle" in case.get("name", "") or "cancel" in case.get("name", "") or "create-" in case.get("name", ""):
        if "--dryrun" not in blob:
            sys.exit(f"FAIL: write-path eval {case['name']!r} must assert --dryrun")
print("OK: write allowlist consistent (73 create + 1 cancel)")
PY
}

need_cmd rg
check_skill_layout
check_version_sync
check_write_allowlist
run_local_or_npx skills-ref validate "$SKILL_DIR"
run_local_or_npx markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" "$SKILL_DIR/**/*.md"
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: huawei-cloud-cost-estimation validation passed\n'
