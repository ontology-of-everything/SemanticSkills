#!/bin/bash
# wyx post-edit check — PostToolUse hook for Write|Edit|NotebookEdit
# After a file edit near a CONCEPT.md, reinjects the dependency list as a
# focused reminder for boundary compliance. Complements PreToolUse:
#   PreToolUse = full boundary context before edit (guidance)
#   PostToolUse = dependency list after edit (verification prompt)
# Design: no import parsing, language-agnostic, silent when no spec found.

set -euo pipefail

# Guard against stdin failure (closed pipe, exotic exec env). Empty input is
# treated as no-op rather than aborting under set -euo pipefail.
input=$(cat) || input=""
if [ -z "$input" ]; then
  exit 0
fi
# jq is required — if missing, file_path stays empty and we exit below.
# This is intentional: SessionStart hook warns about missing jq (fires once
# per session). NotebookEdit uses notebook_path instead of file_path — try both.
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null) || file_path=""

if [ -z "$file_path" ]; then
  exit 0
fi

# Skip inert files (non-code)
case "$file_path" in
  *.json|*.jsonl|*.lock|*.log|*.txt) exit 0 ;;
esac

# Skip spec file edits — editing the spec itself doesn't need a dependency reminder
case "$file_path" in
  *CONCEPT.md|*PIPELINE.md|*SYNCS.md) exit 0 ;;
esac

# Resolve project directory
if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
  PROJECT_DIR="${CLAUDE_PROJECT_DIR%/}"
else
  PROJECT_DIR=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null) || PROJECT_DIR=""
  if [ -z "$PROJECT_DIR" ]; then
    PROJECT_DIR="$(pwd)"
  fi
  PROJECT_DIR="${PROJECT_DIR%/}"
fi

# Guard against PROJECT_DIR="" or "/" — would cause upward traversal to
# scan ancestors of the edited file up to filesystem root (matches
# drift-context.sh).
if [ -z "$PROJECT_DIR" ] || [ "$PROJECT_DIR" = "/" ]; then
  exit 0
fi

# Resolve relative file paths to absolute
case "$file_path" in
  /*) ;;
  *) file_path="$PROJECT_DIR/$file_path" ;;
esac

# Extract a section from a spec file (between ## heading and next ##).
# Trailing `|| true` intentionally swallows sed errors — empty result == "section
# absent" by contract.
extract_section() {
  local file="$1" section="$2"
  tr -d '\r' < "$file" | sed -n "/^## ${section}[[:space:]]*$/,/^## [^#]/{/^## ${section}[[:space:]]*$/d;/^## [^#]/d;p;}" 2>/dev/null \
    | sed '/^$/d' || true
}

# Case-insensitive section extraction: lowercase first, capitalized fallback
# (older specs use `## Dependencies`, newer specs use `## dependencies`).
extract_section_ci() {
  local file="$1" section="$2"
  local result="" cap=""
  result=$(extract_section "$file" "$section") || result=""
  if [ -z "$result" ]; then
    # tr-based capitalization instead of ${section^}: that expansion is bash 4+
    # and macOS ships bash 3.2, where it errors and would silently disable
    # this fallback for legacy capitalized-heading specs.
    cap="$(printf '%s' "${section:0:1}" | tr '[:lower:]' '[:upper:]')${section:1}"
    result=$(extract_section "$file" "$cap") || result=""
  fi
  printf '%s' "$result"
}

# Walk upward from file's directory to find nearest CONCEPT.md
dir=$(dirname "$file_path")
concept_path=""

# prev_dir guards against pathological dirname behavior (defense in depth).
prev_dir=""
while [ "$dir" != "/" ] && [ "$dir" != "." ] && [ "$dir" != "$prev_dir" ]; do
  case "$dir/" in
    "$PROJECT_DIR/"*) ;;
    *) break ;;
  esac
  if [ -f "$dir/CONCEPT.md" ]; then
    concept_path="$dir/CONCEPT.md"
    break
  fi
  prev_dir="$dir"
  dir=$(dirname "$dir")
done

if [ -z "$concept_path" ]; then
  exit 0
fi

# Extract dependencies (case-insensitive)
dependencies=$(extract_section_ci "$concept_path" "dependencies")

# No dependencies declared — nothing to remind about
if [ -z "$dependencies" ]; then
  exit 0
fi

# Build post-edit reminder with dependency list
relative_spec="${concept_path#"$PROJECT_DIR"/}"
concept_name=$(basename "$(dirname "$concept_path")")

ctx="wyx post-edit check: file governed by ${concept_name} (${relative_spec}).
Declared dependencies:
${dependencies}
Verify any imports added by this edit target only declared dependencies above. Imports from undeclared concepts are boundary violations."

# `|| true` guards the load-bearing emit: if jq dies the hook exits 0 silently
# rather than failing the user's edit. SessionStart already warned about jq once.
jq -n --arg ctx "$ctx" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$ctx}}' || true

exit 0
