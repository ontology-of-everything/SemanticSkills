# Assertions

Evaluate observable mapping behavior rather than exact folder names.

- Each concept has a verifiable module boundary; concept modules do not import each
  other.
- Syncs land only in the composition layer (mediator or rule engine).
- Language-specific notes are loaded only for the requested language.
- Concept-boundary questions route back to `concept-design`; the skill
  does not reopen modeling.
- Architecture-guard tests are part of the done criteria, not an optional
  afterthought.
