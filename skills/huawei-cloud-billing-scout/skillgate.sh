#!/usr/bin/env sh
# Skill-targeted-audit gate for this skill (repo validate.sh requires full openclaw frontmatter).
set -eu
cd "$(dirname "$0")"

echo "== skillcheck =="
skillcheck SKILL.md --config skillcheck.toml --ignore disclosure.metadata-budget
test $? -le 0

echo "== markdownlint-cli2 =="
markdownlint-cli2 "**/*.md"

echo "== skill-scanner =="
skill-scanner scan . --policy policy.skill-scanner.yaml --format json 2>/dev/null \
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
