#!/usr/bin/env bash
# 遍历 qa/*/validate.sh，与 GitHub validate workflow 一致。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0

for validate in "$ROOT"/qa/*/validate.sh; do
  [[ -f "$validate" ]] || continue
  name=$(basename "$(dirname "$validate")")
  printf '==> %s\n' "$name"
  if ! "$validate"; then
    status=1
  fi
  printf '\n'
done

[[ "$status" -eq 0 ]] || exit "$status"
printf 'OK: all skill QA passed\n'
