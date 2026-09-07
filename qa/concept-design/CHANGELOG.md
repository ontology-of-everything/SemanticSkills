# concept-design Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.4.0 - 2026-09-07

### Changed

- Rename the installable skill from `jackson-concept-design` to
  `concept-design`; the concept-* family now shares one prefix with
  `concept-prd`, `concept-implementation`, `concept-audit`, and
  `concept-guardrails`. The old name stays a trigger keyword; content is
  unchanged

## 0.3.0 - 2026-08-28

### Changed

- Adopt the author's current notation (Beyond Objects, 2026): syncs move to
  when/where/then causal-rule semantics with the Requesting pseudo-concept;
  the book's CSP/transactional sync semantics is marked deprecated by the
  author himself
- Structured concept spec format: Alloy-style relational state, action
  signatures with requires/ensures and error output cases, underscore-prefixed
  read-only queries, after/then operational principles
- Concept specs stay zero-naming (no interactions/dependencies sections);
  an optional notes section is the only sanctioned place for context-of-use
  remarks (per the 6.1040 concept rubric); output format is wyx-compatible

## 0.2.0 - 2026-08-28

### Changed

- Expand Sync guidance with include/sync notation, reactive/atomic/behavior-
  preserving semantics, and undersync, oversync, flow, and synergy signals
- Expand the dependency graph into Parnas uses-relation subsets for MVP and
  teaching/build order
- After model confirmation, route documentation to `jackson-concept-prd`,
  code to `jackson-concept-implementation`, and existing-code review to
  `jackson-concept-audit`

## 0.1.0 - 2026-08-27

### Added

- Initial Jackson concept-design skill for turning requirements into concepts
  defined by purpose, operational principle, state, and actions
- Boundary critique using specificity, completeness, independence, and
  familiarity, with application behavior composed through synchronizations
- Explicit stop at model confirmation, before PRD, architecture, or code
