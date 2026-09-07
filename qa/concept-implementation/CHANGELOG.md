# concept-implementation Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.4.0 - 2026-09-07

### Changed

- Rename the installable skill from `jackson-concept-implementation` to
  `concept-implementation` (concept-* family prefix); companion references
  updated. The old name stays a trigger keyword; content is unchanged

## 0.3.0 - 2026-08-28

### Added

- Scaling section: concept grouping (a.k.a. domain folders) as pure code
  organization with zero architectural semantics — the zero-reference rule
  stays flat across all concepts (no intra-group references, no "group
  interfaces", no new guard rules); directory-only by default, build
  boundaries as an optional upgrade
- Groups derive from the extrinsic dependency graph plus flow affinity,
  team ownership as tie-breaker; groups double as shippable product subsets
- Syncs-layer split: flow modules regroup into per-group sync packages
  (flows never split); cross-group flows land in the group owning the entry
  Requesting action; each sync package carries its own SYNCS.md with a
  local coordination graph (global view = overall PRD graph + wyx:map)
- New violation signal: citing same-group membership to reference a sibling
  concept, or inventing "group interfaces"
- Language references gain nested grouping layouts (cargo glob members,
  Spring Modulith nested application modules, pnpm workspace globs)

## 0.2.0 - 2026-08-28

### Changed

- Sync semantics updated to the author's current causal-rule model
  (when/where/then, Requesting pseudo-concept): transactions are an optional
  single-DB reinforcement, error syncs are the default failure path
- Add implementation-layer timing/error-isolation classification
  (post-action / pre-validation / scheduled), adapted from wyx, explicitly
  marked as engineering taxonomy that does not change design semantics
- Map underscore-prefixed queries to read-only module methods; add a spec
  colocation step (CONCEPT.md into module dirs, SYNCS.md into the syncs dir)
  enabling wyx drift detection and spec-first edits

## 0.1.0 - 2026-08-28

### Added

- Initial Jackson concept-implementation skill: map a confirmed concept model
  onto a modular monolith (one module per concept, syncs as mediators, the
  dependency graph as build/cut order)
- Two official sync landings: procedural mediator (default) and a declarative
  rule engine; concept modules stay mutually unreferenced
- Language notes for Rust, Java/Spring Modulith, and TypeScript, loaded only
  for the target language
