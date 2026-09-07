# concept-prd Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.3.0 - 2026-09-07

### Changed

- Rename the installable skill from `jackson-concept-prd` to `concept-prd`
  (concept-* family prefix); companion references updated. The old name
  stays a trigger keyword; content is unchanged

## 0.2.1 - 2026-08-28

### Changed

- Clarify the SYNCS.md lifecycle: single file with a full coordination graph
  at transcription time; when the syncs layer is later split into per-group
  packages, jackson-concept-implementation splits the file by flow groups
  (flows stay intact, coordination graphs localize per package)

## 0.2.0 - 2026-08-28

### Changed

- Dual-track placement: per-concept CONCEPT.md colocates with module code
  when the directory exists (central docs/prd/ only as staging), syncs live
  in a single SYNCS.md with a coordination graph, grouped by flow
- Output is wyx-compatible (file names and section headers consumable by
  wyx:concept drift and wyx:map) but deliberately emits no
  interactions/dependencies sections; cross-concept edges live only in
  SYNCS.md and the overall PRD dependency graph
- Per-concept spec adopts the structured format from jackson-concept-design
  0.3.0 (relational state, error cases, queries, after/then OP, notes)

## 0.1.0 - 2026-08-28

### Added

- Initial Jackson concept-prd skill: transcribe a confirmed concept model into
  a PRD document family without inventing content
- Document set: overall PRD, one sub-PRD per concept (no cross-concept
  naming), and syncs grouped by flow
- Acceptance scenarios are derived mechanically from operational principles;
  model gaps route back to `jackson-concept-design`
