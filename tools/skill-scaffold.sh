#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="${1:?usage: skill-scaffold.sh <skill-name>}"

if [[ ! "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  printf 'invalid skill name (use kebab-case): %s\n' "$NAME" >&2
  exit 1
fi

SKILL_DIR="$ROOT/skills/$NAME"
QA_DIR="$ROOT/qa/$NAME"

[[ ! -e "$SKILL_DIR" ]] || { printf 'exists: %s\n' "$SKILL_DIR" >&2; exit 1; }
[[ ! -e "$QA_DIR" ]] || { printf 'exists: %s\n' "$QA_DIR" >&2; exit 1; }

cp -R "$ROOT/template/skill" "$SKILL_DIR"
mkdir -p "$QA_DIR/evals" "$QA_DIR/assertions"
cp "$ROOT/template/qa/validate.sh" "$QA_DIR/validate.sh"
cp "$ROOT/template/qa/evals/evals.json" "$QA_DIR/evals/evals.json"
cp "$ROOT/template/qa/assertions/README.md" "$QA_DIR/assertions/README.md"
chmod +x "$QA_DIR/validate.sh"

replace() {
  local file=$1
  if sed --version >/dev/null 2>&1; then
    sed -i "s/skill-template/$NAME/g; s/__SKILL_NAME__/$NAME/g" "$file"
  else
    sed -i '' "s/skill-template/$NAME/g; s/__SKILL_NAME__/$NAME/g" "$file"
  fi
}

replace "$SKILL_DIR/SKILL.md"
replace "$QA_DIR/validate.sh"
replace "$QA_DIR/evals/evals.json"

printf 'Scaffolded skill: %s\n' "$NAME"
printf '  skills/%s/\n  qa/%s/\n' "$NAME" "$NAME"
printf 'Next: edit SKILL.md, add evals, register in docs/catalog.yml\n'
