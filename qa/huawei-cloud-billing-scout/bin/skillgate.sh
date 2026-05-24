#!/usr/bin/env sh
# Skill-targeted audit (skillcheck + markdownlint + skill-scanner). Lives under qa/, not install bundle.
set -eu
QA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$QA_DIR/../.." && pwd)"
SKILL_DIR="$ROOT/skills/huawei-cloud-billing-scout"

echo "== skillcheck =="
skillcheck "$SKILL_DIR/SKILL.md" --config "$QA_DIR/skillcheck.toml" --ignore disclosure.metadata-budget
test $? -le 0

echo "== markdownlint-cli2 =="
markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" \
  "$SKILL_DIR/SKILL.md" "$SKILL_DIR/references/**/*.md"

echo "== skill-scanner =="
skill-scanner scan "$SKILL_DIR" --policy "$QA_DIR/policy.skill-scanner.yaml" --format json 2>/dev/null \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
bad = [f for f in d.get('findings', []) if f.get('severity') in ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'WARNING')]
if bad:
    print('skill-scanner findings:', bad, file=sys.stderr)
    sys.exit(1)
print('skill-scanner: 0 findings above INFO')
"

echo "OK: skill gate passed (0 errors, 0 warnings)"
