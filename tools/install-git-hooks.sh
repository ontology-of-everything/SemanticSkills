#!/usr/bin/env bash
# Point this repo at tracked .githooks/ (pre-commit runs validate-all.sh).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$ROOT/.githooks"

chmod +x "$HOOKS_DIR/pre-commit"
git -C "$ROOT" config core.hooksPath .githooks

printf 'OK: git hooksPath -> .githooks (pre-commit = validate-all.sh)\n'
printf 'Tip: bypass once with git commit --no-verify\n'
