# concept-design Changelog

## 0.5.0 - 2026-09-07

- 区分论文语义与本仓方言；修复 flow、绑定、查询空集与同步图；压缩模板并重写订位教学例。
- 核验最新相关论文，更新行为评估及文档。

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.4.1 - 2026-09-07

### Added

- `references/example-reserving.md`: filled Beyond Objects restaurant
  example (Reserving [User, Slot], Availability [Venue], when/where/then)

## 0.4.0 - 2026-09-07

### Changed

- Rename the installable skill from `jackson-concept-design` to
  `concept-design`; the concept-* family now shares one prefix with
  `concept-prd`, `concept-implementation`, `concept-audit`, and
  `concept-guardrails`
- Restructure SKILL.md into the six-section skeleton (目标 / 原则 / 流程 /
  命题 / 记法与模板 / 参考) and cut it to ~46% of its size (14.0 KB → 6.5 KB).
  The design loop now routes to on-demand references: criteria and
  misjudgment table → `references/criteria.md`; sync notation, causal
  semantics, signals, dependency graph → `references/sync-notation.md`;
  source list with one extracted principle per source →
  `references/sources.md`. Completion conditions become checkable
  propositions; no rules were dropped
- Make sync design explicit: principles now state sync as the sole
  composition mechanism (behavior preservation, Requesting entry, errors as
  matchable outputs) and that composition has structure — syncs grouped by
  flow, plus two deliverables: a coordination graph (who triggers whom) and
  the dependency graph (who cannot ship without whom). Flow step 5 is broken
  into sub-steps; the output template gains a `## 同步图` section and a
  flow-grouped sync block with an error sync; `references/sync-notation.md`
  gains a "结构：flow 与同步图" section (cascade rules, decomposition signals)

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
