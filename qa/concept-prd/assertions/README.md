# Assertions

Evaluate observable PRD-transcription behavior rather than exact headings.

- The skill runs only on explicit `$concept-prd` / `/concept-prd` invocation.
- The skill transcribes a confirmed model; it does not invent concepts, syncs,
  or exclusions.
- Model gaps route back to `concept-design` instead of being filled in
  the documents.
- Each concept gets its own sub-PRD that does not depend on other concept definitions; same-named local parameters are valid.
- Syncs are grouped by flow, not by domain directory.
- Acceptance scenarios trace to principles or action/state contracts; no code is written.
