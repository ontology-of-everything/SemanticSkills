#!/bin/bash
# wyx drift context — PreToolUse hook for Write|Edit
# When a file is written near a CONCEPT.md or PIPELINE.md, outputs spec
# context including boundary declarations so the LLM can self-check
# boundary compliance. SYNCS.md is listed in spec context but does not
# stop traversal or inject boundaries. This replaces aspirational
# CLAUDE.md rules with a mechanical checkpoint.

set -euo pipefail

# Guard against stdin failure (closed pipe, exotic exec env). Empty input is
# treated as no-op — the hook produces no additionalContext rather than dying
# silently under set -euo pipefail.
input=$(cat) || input=""
if [ -z "$input" ]; then
  exit 0
fi
# jq is required — if missing, file_path stays empty and we exit below.
# This is intentional: SessionStart hook warns about missing jq (fires once per session).
# NotebookEdit uses notebook_path instead of file_path — try both.
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null) || file_path=""

if [ -z "$file_path" ]; then
  exit 0
fi

# Skip inert files (but allow .md edits — editing specs should show context)
case "$file_path" in
  *.json|*.jsonl|*.lock|*.log|*.txt) exit 0 ;;
esac

# Resolve project directory — CLAUDE_PROJECT_DIR is set by Claude Code for hooks
# Fall back to cwd from hook input, then to current directory
if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
  PROJECT_DIR="${CLAUDE_PROJECT_DIR%/}"
else
  PROJECT_DIR=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null) || PROJECT_DIR=""
  if [ -z "$PROJECT_DIR" ]; then
    PROJECT_DIR="$(pwd)"
  fi
  PROJECT_DIR="${PROJECT_DIR%/}"
fi

# Guard against PROJECT_DIR="" (CLAUDE_PROJECT_DIR="/" strips to empty) or
# PROJECT_DIR="/" (literal root). Either makes the upward-traversal stop
# condition match every absolute path, so the hook would scan ancestors of
# the edited file up to filesystem root. Silent exit is safer than leaking
# unrelated CONCEPT.md content into context.
if [ -z "$PROJECT_DIR" ] || [ "$PROJECT_DIR" = "/" ]; then
  exit 0
fi

# Resolve relative file paths to absolute using PROJECT_DIR
case "$file_path" in
  /*) ;; # already absolute
  *) file_path="$PROJECT_DIR/$file_path" ;;
esac

# Extract a section's content from a wyx spec file (between ## heading and next ##).
# Trailing `|| true` intentionally swallows sed errors — empty result == "section
# absent" by contract. Do not report sed failures separately; downstream code
# treats empty as "no boundary declarations found".
extract_section() {
  local file="$1" section="$2"
  tr -d '\r' < "$file" | sed -n "/^## ${section}[[:space:]]*$/,/^## [^#]/{/^## ${section}[[:space:]]*$/d;/^## [^#]/d;p;}" 2>/dev/null \
    | sed '/^$/d' || true
}

# Case-insensitive section extraction: try lowercase first, then capitalized
# (older specs use `## Purpose`, newer specs use `## purpose`). Capitalizes
# only the first letter — matches both "purpose"→"Purpose" and
# "data boundary"→"Data boundary" (NOT "Data Boundary"; that pattern was
# already absent before this helper).
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

# Search upward from file's directory for wyx spec files
dir=$(dirname "$file_path")
found_specs=""
found_concept=false
spec_context=""
boundary_context=""
# Initialize boundary-section vars so I1 message branching below can probe
# them under set -u even when no CONCEPT.md / PIPELINE.md was matched.
dependencies=""
anc_dependencies=""

# Defense-in-depth: prev_dir guards against an exotic FS or in-place edit
# making `dirname` return the same value twice. Natural termination still
# happens via `/`, `.`, or PROJECT_DIR boundary; this is a belt-and-braces
# stop so the 5s hook timeout never has to kick in.
prev_dir=""
while [ "$dir" != "/" ] && [ "$dir" != "." ] && [ "$dir" != "$prev_dir" ]; do
  # Stop searching above the project root (trailing slash prevents sibling match)
  case "$dir/" in
    "$PROJECT_DIR/"*) ;;
    *) break ;;
  esac

  # SYNCS.md is recognized for spec_context listing but does not stop traversal
  # (it contributes no boundary context — only CONCEPT.md and PIPELINE.md do)
  for spec in "$dir"/CONCEPT.md "$dir"/PIPELINE.md "$dir"/SYNCS.md; do
    if [ -f "$spec" ]; then
      relative_spec="${spec#"$PROJECT_DIR"/}"
      found_specs="${found_specs:+$found_specs, }${relative_spec}"

      # Extract purpose (case-insensitive: lowercase priority, capitalized fallback)
      purpose=$(extract_section_ci "$spec" "purpose")
      if [ -n "$purpose" ]; then
        spec_context="${spec_context}  - ${relative_spec}: ${purpose}
"
      else
        spec_context="${spec_context}  - ${relative_spec}
"
      fi

      # Extract boundary declarations from CONCEPT.md and PIPELINE.md files
      case "$spec" in
        *CONCEPT*)
          found_concept=true
          interactions=$(extract_section_ci "$spec" "interactions")
          if [ -n "$interactions" ]; then
            boundary_context="${boundary_context}  [${relative_spec} ## interactions]
${interactions}
"
          fi
          dependencies=$(extract_section_ci "$spec" "dependencies")
          if [ -n "$dependencies" ]; then
            boundary_context="${boundary_context}  [${relative_spec} ## dependencies]
${dependencies}
"
          fi
          if [ -z "$interactions" ] && [ -z "$dependencies" ]; then
            boundary_context="${boundary_context}  [${relative_spec}: no boundary declarations found]
"
          fi
          ;;
        *PIPELINE*)
          # Extract data boundary (access constraints, not quality invariants)
          data_boundary=$(extract_section_ci "$spec" "data boundary")
          if [ -n "$data_boundary" ]; then
            boundary_context="${boundary_context}  [${relative_spec} ## data boundary]
${data_boundary}
"
          fi
          ;;
      esac
    fi
  done

  # Stop at the first directory with a boundary-contributing spec (CONCEPT.md or PIPELINE.md).
  # SYNCS.md alone does not stop traversal — it contributes no boundary context.
  if [ -f "$dir/CONCEPT.md" ] || [ -f "$dir/PIPELINE.md" ]; then
    break
  fi
  prev_dir="$dir"
  dir=$(dirname "$dir")
done

# DX-1: If boundary-contributing specs found but no co-located CONCEPT.md, look for
# ancestor CONCEPT.md and inject its boundaries with a caveat note.
# This covers: PIPELINE.md-only directories (data boundary present but no interactions).
if [ -n "$found_specs" ] && [ "$found_concept" = false ]; then
  # ancestor_dir starts from dirname(dir) — `dir` is the directory at which the
  # main loop broke. Skipping it avoids re-examining the same directory and
  # short-circuiting on a co-located non-CONCEPT spec's parent.
  ancestor_dir=$(dirname "$dir")
  prev_ancestor=""
  while [ "$ancestor_dir" != "/" ] && [ "$ancestor_dir" != "." ] && [ "$ancestor_dir" != "$prev_ancestor" ]; do
    case "$ancestor_dir/" in
      "$PROJECT_DIR/"*) ;;
      *) break ;;
    esac
    if [ -f "$ancestor_dir/CONCEPT.md" ]; then
      relative_ancestor="${ancestor_dir#"$PROJECT_DIR"/}/CONCEPT.md"
      anc_interactions=$(extract_section_ci "$ancestor_dir/CONCEPT.md" "interactions")
      anc_dependencies=$(extract_section_ci "$ancestor_dir/CONCEPT.md" "dependencies")
      if [ -n "$anc_interactions" ] || [ -n "$anc_dependencies" ]; then
        boundary_context="  [SHADOWED — ancestor boundaries from ${relative_ancestor}, may not fully apply to this subdirectory]
"
        if [ -n "$anc_interactions" ]; then
          boundary_context="${boundary_context}  [${relative_ancestor} ## interactions]
${anc_interactions}
"
        fi
        if [ -n "$anc_dependencies" ]; then
          boundary_context="${boundary_context}  [${relative_ancestor} ## dependencies]
${anc_dependencies}
"
        fi
      fi
      break
    fi
    prev_ancestor="$ancestor_dir"
    ancestor_dir=$(dirname "$ancestor_dir")
  done
fi

if [ -n "$found_specs" ]; then
  # Build context message
  ctx=$'wyx drift context: specs found near this file.\n'
  ctx="${ctx}${spec_context}"

  # Differentiate message for spec edits vs code edits
  case "$file_path" in
    *CONCEPT.md|*PIPELINE.md|*SYNCS.md)
      if [ -n "$boundary_context" ]; then
        ctx="${ctx}"$'\nDeclared boundaries:\n'"${boundary_context}"$'\n'
      fi
      ctx="${ctx}You are editing a spec file. Ensure changes reflect the current implementation and update boundaries if needed." ;;
    *)
      if [ -n "$boundary_context" ]; then
        ctx="${ctx}"$'\nDeclared boundaries:\n'"${boundary_context}"
        # Only mention `## dependencies` when at least one was actually injected
        # (co-located CONCEPT.md or ancestor [SHADOWED] CONCEPT.md). PIPELINE.md
        # only directories with no ancestor CONCEPT.md emit `## data boundary`
        # alone — referencing `## dependencies` there is misleading.
        if [ -n "$dependencies" ] || [ -n "$anc_dependencies" ]; then
          ctx="${ctx}"$'\nBEFORE writing imports, verify each import target against ## dependencies above. Imports from concepts NOT listed in ## dependencies are boundary violations.'
        else
          ctx="${ctx}"$'\nVerify changes respect the boundaries declared above.'
        fi
      else
        ctx="${ctx}Verify changes align with declared actions, invariants, and operational principles."
      fi ;;
  esac

  # Output as structured JSON with additionalContext (official PreToolUse API).
  # `|| true` guards the load-bearing emit: if jq dies (missing binary, OOM, ARG_MAX
  # overflow on huge $ctx), the hook exits 0 without output rather than failing
  # the tool call. SessionStart already warned about missing jq once per session.
  jq -n --arg ctx "$ctx" '{hookSpecificOutput:{hookEventName:"PreToolUse",additionalContext:$ctx}}' || true
fi

exit 0
