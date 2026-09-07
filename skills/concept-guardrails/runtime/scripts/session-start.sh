#!/bin/bash
set -eu
# Avoid pipefail: internal pipes use head -N which closes early, causing
# SIGPIPE for upstream commands (sort, sed). This is normal and not an error.
# wyx SessionStart hook — report existing wyx artifact coverage

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
PROJECT_DIR="${PROJECT_DIR%/}"

# Hook input source (startup|resume|clear|compact) — used to gate the no-specs
# hint below. TTY guard keeps manual `bash session-start.sh` runs from blocking
# on stdin; empty/unparseable input degrades to "" which is treated as startup.
hook_source=""
if [ ! -t 0 ]; then
  input=$(cat) || input=""
  if [ -n "$input" ] && command -v jq &>/dev/null; then
    hook_source=$(echo "$input" | jq -r '.source // empty' 2>/dev/null) || hook_source=""
  fi
fi

# Directories pruned from all find calls. -prune stops descent entirely;
# the previous -not -path form still walked every file inside node_modules/.git
# on each session start, only to filter matches afterwards.
PRUNE_DIRS=(
  -name node_modules -o -name .git
  -o -name dist -o -name build
  -o -name .next -o -name vendor
  -o -name .venv -o -name venv
)

# Warn if jq is missing (drift context hook depends on it)
if ! command -v jq &>/dev/null; then
  echo "wyx: jq not found — drift context (boundary checking) is disabled. Install jq for full protection."
fi

# Find wyx spec files, excluding common build/dependency directories.
# -mindepth 1 keeps the prune predicate off the start directory itself: without
# it, a project whose own root basename matches a PRUNE_DIRS name (e.g. a
# workspace literally named `build`) would prune the whole tree and emit nothing.
find_specs() {
  find "$PROJECT_DIR" -mindepth 1 \( "${PRUNE_DIRS[@]}" \) -prune -o -name "$1" -print \
    2>/dev/null | sort || true
}

concepts=$(find_specs "CONCEPT.md")
pipelines=$(find_specs "PIPELINE.md")
syncs=$(find_specs "SYNCS.md")

count_lines() {
  if [ -z "$1" ]; then echo 0; else echo "$1" | wc -l | tr -d ' '; fi
}

concept_count=$(count_lines "$concepts")
pipeline_count=$(count_lines "$pipelines")
sync_count=$(count_lines "$syncs")

total=$((concept_count + pipeline_count + sync_count))

# No artifacts found — suggest getting started, but only on real session
# startup. The plugin is enabled globally (user scope) by default, so this
# fires in every spec-less project; re-printing on resume/clear/compact is
# pure noise. Empty/unparseable source (old CLI, missing jq) still shows it.
if [ "$total" -eq 0 ]; then
  case "$hook_source" in
    ""|startup)
      echo "wyx: No specs found. Try /wyx:audit to discover modules that could benefit from specs."
      ;;
  esac
  exit 0
fi

# Build report
report="wyx artifacts:"

# Strip PROJECT_DIR prefix using parameter expansion (avoids sed metacharacter issues)
strip_prefix() {
  printf '%s\n' "$1" | while IFS= read -r line; do printf '%s\n' "${line#"$PROJECT_DIR"/}"; done | tr '\n' ',' | sed 's/,$//'
}

if [ "$concept_count" -gt 0 ]; then
  names=$(strip_prefix "$concepts")
  report="$report CONCEPT($concept_count: $names)"
fi

if [ "$pipeline_count" -gt 0 ]; then
  names=$(strip_prefix "$pipelines")
  report="$report PIPELINE($pipeline_count: $names)"
fi

if [ "$sync_count" -gt 0 ]; then
  names=$(strip_prefix "$syncs")
  report="$report SYNCS($sync_count: $names)"
fi

echo "$report"

# Report last drift check date if history exists
drift_history="$PROJECT_DIR/.claude/wyx-drift-history.jsonl"
if [ -f "$drift_history" ] && command -v jq &>/dev/null; then
  last_entry=$(grep -v '^[[:space:]]*$' "$drift_history" | tail -1 || true)
  # Every jq call below uses `|| var=fallback` because set -eu (no pipefail)
  # still aborts on command-substitution failure. A malformed JSONL entry
  # (partial write, manual corruption) would otherwise kill the SessionStart
  # hook silently after printing the artifacts line, hiding all downstream
  # warnings. Treating parse failure as "empty entry" lets the hook degrade
  # gracefully — suggest_drift stays true later, which is the safer default.
  last_ts=$(echo "$last_entry" | jq -r '.ts // empty' 2>/dev/null) || last_ts=""
  # action defaults to "detect" for backward compat with pre-v0.23 entries
  last_action=$(echo "$last_entry" | jq -r '.action // "detect"' 2>/dev/null) || last_action="detect"
  # Scope annotation: a scoped detect entry (path != whole project) can be the latest
  # JSONL entry, so its "0 with drift" must not read as a project-wide all-clear. Show
  # the path so a scoped measurement is not mistaken for full-project clean. Fix entries
  # carry no `path` field, so this stays empty (no annotation) for them by design.
  last_path=$(echo "$last_entry" | jq -r '.path // empty' 2>/dev/null) || last_path=""
  if [ "$last_action" = "fix" ]; then
    # Fix entry: report remaining drift and the originating detect's timestamp
    last_drift=$(echo "$last_entry" | jq -r '.specs_remaining // 0' 2>/dev/null) || last_drift="0"
    ref_ts=$(echo "$last_entry" | jq -r '.ref_ts // empty' 2>/dev/null) || ref_ts=""
    detect_ts="${ref_ts:-$last_ts}"
  else
    last_drift=$(echo "$last_entry" | jq -r '.specs_with_drift // 0' 2>/dev/null) || last_drift="0"
    detect_ts="$last_ts"
  fi
  scope_note=""
  case "$last_path" in
    ""|project|.|"$PROJECT_DIR") ;;  # whole-project measurement — no scope annotation
    *) scope_note=" [scope: $last_path]" ;;
  esac
  if [ -n "$last_ts" ]; then
    if [ "$last_action" = "fix" ]; then
      if [ "$last_drift" = "0" ]; then
        echo "Last drift check: $detect_ts (all fixed at $last_ts)"
      else
        echo "Last drift check: $detect_ts ($last_drift spec(s) pending after fix at $last_ts)"
      fi
    else
      echo "Last drift check: $last_ts ($last_drift spec(s) with drift — rerun to update)$scope_note"
    fi
    # Build a single reference file representing the last drift *measurement*.
    # Always use the detect ts (not fix ts): a fix entry is a mid-workflow
    # marker, not a new measurement. Any spec or code change since the last
    # detect warrants a new scan, even if a fix happened in between.
    # If `touch -d` is unavailable (non-GNU coreutils, missing mktemp, etc.),
    # SKIP the find-newer block entirely. Falling back to $drift_history's
    # mtime would re-introduce the v0.21.0 false-positive bug — JSONL file
    # mtime tracks the most recent append (often a fix entry), not the
    # detect ts that anchors the measurement.
    _ts_ref=$(mktemp 2>/dev/null) || _ts_ref=""
    if [ -n "$_ts_ref" ] && touch -d "$detect_ts" "$_ts_ref" 2>/dev/null; then
      # Warn if specs modified since last drift check
      newer_than_drift=$(find "$PROJECT_DIR" -mindepth 1 \( "${PRUNE_DIRS[@]}" \) -prune -o \
        \( -name "CONCEPT.md" -o -name "PIPELINE.md" -o -name "SYNCS.md" \) \
        -newer "$_ts_ref" -print \
        2>/dev/null | head -1)
      if [ -n "$newer_than_drift" ]; then
        echo "Specs modified since last drift check — consider running /wyx:concept drift"
      fi
      # Report code directories modified since last drift check.
      # dirname via sed (line-based) — `xargs -r dirname` word-splits find
      # output, so paths containing spaces were reported as wrong fragments.
      # -mindepth 1 keeps the '.*' prune off the start directory itself —
      # without it a hidden project root (~/.dotfiles) prunes the whole tree.
      # grep -vxF drops the bare PROJECT_DIR produced by files at the root
      # (the prefix strip can't reduce it to a relative name).
      # Prefix strip uses parameter expansion, NOT sed "s|^$PROJECT_DIR/||":
      # a project path containing a sed metacharacter (| & \) would corrupt the
      # s-command. Same principle as strip_prefix() above.
      changed_dirs=$(find "$PROJECT_DIR" -mindepth 1 \( "${PRUNE_DIRS[@]}" -o -name '.*' \) -prune -o -type f \
        \( -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.svelte" -o -name "*.vue" \) \
        -newer "$_ts_ref" -print \
        2>/dev/null | sed 's|/[^/]*$||' | sort -u | grep -vxF -- "$PROJECT_DIR" \
        | while IFS= read -r p; do printf '%s\n' "${p#"$PROJECT_DIR"/}"; done | head -5)
      rm -f "$_ts_ref" 2>/dev/null
      if [ -n "$changed_dirs" ]; then
        changed_list=$(echo "$changed_dirs" | tr '\n' ',' | sed 's/,$//')
        echo "Code modified since last drift: $changed_list"
      fi
    elif [ -n "$_ts_ref" ]; then
      rm -f "$_ts_ref" 2>/dev/null
    fi
  fi
fi

# Check ARCHITECTURE.md freshness
if [ -f "$PROJECT_DIR/ARCHITECTURE.md" ]; then
  newer_specs=$(find "$PROJECT_DIR" -mindepth 1 \( "${PRUNE_DIRS[@]}" \) -prune -o \
    \( -name "CONCEPT.md" -o -name "PIPELINE.md" -o -name "SYNCS.md" \) \
    -newer "$PROJECT_DIR/ARCHITECTURE.md" -print \
    2>/dev/null | head -1)
  if [ -n "$newer_specs" ]; then
    echo "Warning: ARCHITECTURE.md may be stale — specs modified since last /wyx:map run."
  fi
fi

# Suggest uncovered modules (directories with >2 source files but no CONCEPT.md, PIPELINE.md, or SYNCS.md)
# Single-pass: find all source files, extract dirs, count per dir, filter — no nested find
if [ "$concept_count" -gt 0 ]; then
  # Collect dirs with specs (for exclusion). Newline-fed read avoids word-splitting
  # on spec paths containing whitespace — `$concepts $pipelines $syncs` unquoted
  # would corrupt entries like `My Project/src/auth/CONCEPT.md`.
  # Store newline-delimited (not pipe-joined): the membership test below uses a
  # fixed-string match, so a dir path containing regex metacharacters — e.g. a
  # SvelteKit route group `src/routes/(app)/` — can never inject into an ERE and
  # cause a spec'd directory to be misreported as uncovered.
  spec_dirs=""
  while IFS= read -r spec_file; do
    [ -z "$spec_file" ] && continue
    spec_dirs="$spec_dirs$(dirname "$spec_file")"$'\n'
  done <<< "$(printf '%s\n%s\n%s' "$concepts" "$pipelines" "$syncs")"

  uncovered=$(find "$PROJECT_DIR" -mindepth 1 \
    \( "${PRUNE_DIRS[@]}" -o -name target -o -name __pycache__ -o -name '.*' \) -prune -o \
    -type f \
    \( -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" \
       -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.java" \
       -o -name "*.svelte" -o -name "*.vue" -o -name "*.jl" \) -print \
    2>/dev/null \
    | sed 's|/[^/]*$||' \
    | sort | uniq -c | sort -rn \
    | awk -v threshold=2 '$1 > threshold' \
    | sed 's/^[[:space:]]*[0-9][0-9]* //' \
    | while IFS= read -r d; do
        # Skip dirs that have a spec
        if [ -n "$spec_dirs" ] && grep -qxF -- "$d" <<<"$spec_dirs"; then
          continue
        fi
        # Files directly at project root: the prefix strip below would leave
        # the absolute path — loose root files are not a module, skip.
        [ "$d" = "$PROJECT_DIR" ] && continue
        rel="${d#"$PROJECT_DIR"/}"
        # Skip well-known non-concept directories. Matched against "/$rel/"
        # so each name is excluded at ANY depth including top level — bare
        # top-level dirs (rel="tests") previously slipped through `tests/*`.
        case "/$rel/" in
          */tests/*|*/test/*|*/spec/*|*/__tests__/*|*/docs/*|*/build/*) continue ;;
          */migrations/*) continue ;;
          */components/ui/*) continue ;;
          */types/*|*/e2e/*|*/cypress/*) continue ;;
          */fixtures/*|*/stubs/*|*/mocks/*) continue ;;
          */utils/*|*/util/*|*/helpers/*) continue ;;
          */scripts/*|*/schema/*|*/schemas/*) continue ;;
          */constants/*|*/config/*) continue ;;
        esac
        printf '%s\n' "$rel"
      done \
    | head -10 \
    | tr '\n' ',' | sed 's/,$//')
  if [ -n "$uncovered" ]; then
    echo "Uncovered modules (>2 source files, no CONCEPT/PIPELINE/SYNCS): $uncovered"
  fi
fi

# Detect spec shadowing: PIPELINE.md without co-located CONCEPT.md stops hook traversal,
# hiding ancestor boundary checking. SYNCS.md does not stop traversal so cannot cause shadowing.
# (The outer `for spec_list in "$pipelines"` loop was removed in v0.23.2 — vestigial
# from when SYNCS.md was iterated too, removed per v0.17.1 traversal fix.)
if [ "$concept_count" -gt 0 ] && [ -n "$pipelines" ]; then
  shadows=""
  while IFS= read -r spec_file; do
    [ -z "$spec_file" ] && continue
    spec_dir=$(dirname "$spec_file")
    # Safe if this directory already has CONCEPT.md
    [ -f "$spec_dir/CONCEPT.md" ] && continue
    # Walk up to check for ancestor CONCEPT.md
    check_dir=$(dirname "$spec_dir")
    prev_check=""
    while [ "$check_dir" != "$prev_check" ]; do
      case "$check_dir/" in "$PROJECT_DIR/"*) ;; *) break ;; esac
      # Guard: dirname(".") returns "." — stop when we can't go higher
      [ "$check_dir" = "$PROJECT_DIR" ] && break
      if [ -f "$check_dir/CONCEPT.md" ]; then
        rel_spec="${spec_file#"$PROJECT_DIR"/}"
        rel_concept="${check_dir#"$PROJECT_DIR"/}/CONCEPT.md"
        shadows="${shadows:+$shadows; }$rel_spec hides $rel_concept"
        break
      fi
      prev_check="$check_dir"
      check_dir=$(dirname "$check_dir")
    done
  done <<< "$pipelines"
  if [ -n "$shadows" ]; then
    echo "Warning: Spec shadowing detected — $shadows. Files in these directories won't get boundary checking from the ancestor CONCEPT.md. Fix: add a CONCEPT.md to the shadowing directory, or move the spec."
  fi
fi

# Contextual next-step suggestion based on project state
if [ "$concept_count" -gt 0 ]; then
  # Check if drift was *measured* today. Compare against detect_ts (not
  # last_ts) — a fix entry is a mid-workflow marker, not a new measurement,
  # so fix ts is not a valid "last measurement" anchor. This matches the
  # `_ts_ref`/`detect_ts` block above which uses the same invariant.
  # If the earlier parse failed (malformed entry) or detect_ts is unset,
  # suggest_drift stays true, the safer default. Bash variable scope is
  # function-level, so detect_ts is visible across the if-blocks.
  suggest_drift=true
  if [ -n "${detect_ts:-}" ]; then
    last_date="${detect_ts:0:10}"
    today=$(date -u +%Y-%m-%d 2>/dev/null || true)
    if [ "$last_date" = "$today" ]; then
      suggest_drift=false
    fi
  fi
  if [ "$suggest_drift" = true ]; then
    echo "Suggestion: Run /wyx:concept drift to check specs and update this status."
  fi
else
  echo "Suggestion: Run /wyx:concept to create your first concept spec."
fi
