# Changelog

Monorepo **infrastructure** history. Each skill has its own changelog:

| Skill | Changelog |
| --- | --- |
| huawei-cloud-billing-scout | [qa/huawei-cloud-billing-scout/CHANGELOG.md](qa/huawei-cloud-billing-scout/CHANGELOG.md) |
| huawei-cloud-cost-estimation | [qa/huawei-cloud-cost-estimation/CHANGELOG.md](qa/huawei-cloud-cost-estimation/CHANGELOG.md) |
| huawei-cloud-account-onboarding | [qa/huawei-cloud-account-onboarding/CHANGELOG.md](qa/huawei-cloud-account-onboarding/CHANGELOG.md) |
| semantic-km-creator | [qa/semantic-km-creator/CHANGELOG.md](qa/semantic-km-creator/CHANGELOG.md) |
| semantic-pkm-creator | [qa/semantic-pkm-creator/CHANGELOG.md](qa/semantic-pkm-creator/CHANGELOG.md) |
| concept-design | [qa/concept-design/CHANGELOG.md](qa/concept-design/CHANGELOG.md) |
| concept-prd | [qa/concept-prd/CHANGELOG.md](qa/concept-prd/CHANGELOG.md) |
| concept-implementation | [qa/concept-implementation/CHANGELOG.md](qa/concept-implementation/CHANGELOG.md) |
| concept-audit | [qa/concept-audit/CHANGELOG.md](qa/concept-audit/CHANGELOG.md) |
| concept-guardrails | [qa/concept-guardrails/CHANGELOG.md](qa/concept-guardrails/CHANGELOG.md) |
| html-slides | [qa/html-slides/CHANGELOG.md](qa/html-slides/CHANGELOG.md) |

## 4.2.0 - 2026-09-10

### Breaking Changes

- **concept-guardrails** **0.30.0**: drop the `wyx:` mode prefix — invoke `$concept-guardrails <audit|concept|drift|pipeline|sync|map>`; consume Jackson notation only (wyx-native sections are flagged for migration, not parsed). See skill changelog.

### Features

- **concept-design** **0.6.0**: explicit-only (`/concept-design` / `$concept-design`; see skill changelog)
- **concept-prd** **0.5.0**: explicit-only; downstream `wyx:*` references renamed (see skill changelog)
- **concept-implementation** **0.6.0**: explicit-only; `wyx:map` → `concept-guardrails map` (see skill changelog)
- **concept-audit** **0.5.0**: explicit-only (see skill changelog)

## 4.1.0 - 2026-09-09

### Breaking Changes

- Rename installable skill: `semantic-creator` → `semantic-km-creator` (enterprise knowledge from APIs, CLIs, tables/databases). Personal knowledge stays `semantic-pkm-creator`. Install with `--skill semantic-km-creator`.

### Features

- **semantic-km-creator** **0.6.0**: rename from `semantic-creator` to pair with `semantic-pkm-creator` (see skill changelog)
- **html-slides** **0.1.0**: explicit-only single-file HTML decks (see skill changelog)

## 4.0.0 - 2026-09-07

### Breaking Changes

- Rename installable skills: `jackson-concept-*` → `concept-*`, `wyx-zh-cn` → `concept-guardrails`, `sce-creator` → `semantic-pkm-creator`. Install with the new `--skill` names.
- Remove `constraint-charter` from the installable set.

### Features

- **concept-design** **0.5.0**: six-section skeleton; distinguish paper semantics from this repo's dialect; fix flow, bindings, empty query sets, and the coordination graph; filled reserving example (see skill changelog)
- **concept-prd** **0.4.0**: six-section skeleton; Jackson-style CONCEPT.md/SYNCS.md templates; authoritative specs and incremental edits; reserving example as transcribed files (see skill changelog)
- **concept-implementation** **0.5.0**: six-section skeleton; fix transaction/error handling, completion events, and concurrency isolation; correct Spring Modulith and Cargo boundary-check notes (see skill changelog)
- **concept-audit** **0.4.0**: reframe around independence and composition defects; judge by behavior and impact; add binding/conjunction/replay checks (see skill changelog)
- **concept-guardrails** **0.28.0**: rename from wyx-zh-cn; unify Jackson/wyx consumer rules; explicit invocation only (see skill changelog)
- **semantic-pkm-creator** **0.3.0**: rename from semantic-sce-creator for personal knowledge management; six-section skeleton; relations moved to references (see skill changelog)
- Add `skills.sh.json` so the ten skills group on the skills.sh repo page

## 3.14.0 - 2026-08-28

### Features

- **jackson-concept-design** **0.2.0**: expand Sync notation (include/when, reactive/atomic/behavior-preserving rules), undersync/oversync/flow/synergy signals, and Parnas dependency-graph subsets for MVP and teaching order; route a confirmed model to companion skills (see skill changelog)
- **jackson-concept-prd** **0.1.0**: add a transcription skill that turns a confirmed concept model into a PRD family — overall PRD, one sub-PRD per concept, syncs grouped by flow — without inventing content (see skill changelog)
- **jackson-concept-implementation** **0.1.0**: add a mapping skill that lands a confirmed concept model on a modular monolith — one module per concept, syncs as mediators or a rule engine, language notes for Rust, Java/Spring Modulith, and TypeScript (see skill changelog)
- **jackson-concept-audit** **0.1.0**: add a read-only five-dimension audit of a codebase against its concept model or PRD, with evidenced findings routed to design, prd, or implementation (see skill changelog)

## 3.13.0 - 2026-08-27

### Features

- **wyx-zh-cn** **0.26.0**: add a Chinese adaptation of [jlifyio/wyx](https://github.com/jlifyio/wyx)
  v0.26.0 — module boundaries declared as colocated CONCEPT/PIPELINE/SYNCS specs,
  coverage audit with dependency-ordered command plans, drift detection with
  calibrated severities and cross-spec reference validation, and Mermaid
  architecture maps; upstream's five slash commands become one skill with six
  routed modes, and the upstream Claude Code hooks runtime ships verbatim under
  `runtime/` as an optional boundary-injection layer (MIT notice retained; see
  skill changelog)

## 3.12.0 - 2026-08-27

### Features

- **jackson-concept-design** **0.1.0**: add a Jackson-inspired concept-modeling skill
  that defines independent concepts through Purpose, Operational Principle,
  State, and Actions; critiques boundaries by specificity, completeness,
  independence, and familiarity; composes application behavior with
  synchronizations; and stops before PRD, architecture, or code (see skill
  changelog)

## 3.11.0 - 2026-08-24

### Features

- **huawei-cloud-account-onboarding** **1.0.0**: rewrite onto the real read-only BSS face-scan commands (`ShowRealNameAuthStatus` + `ShowRealNameAuthQrCode`) — concepts/commands reference split with SKILL.md kept as a compact entry point, TypeScript terminal QR renderer as the only script, `--cli-waiter` polling, cross-layer command contract and optional real BSS smoke; the skill now owns the gate the QR command lacks, and the local mock server is removed; published to ClawHub (see skill changelog)

## 3.10.1 - 2026-08-24

### Fixes

- **huawei-cloud-cost-estimation** **3.2.4**: lift IAM policies to a skill-level reference (create write principle + RFQ read layers); move parameter CBC errors into pricing traps; make the Reference Index concept/command-layer symmetric (see skill changelog)

## 3.10.0 - 2026-08-18

### Features

- **sce-creator** **0.1.0**: add a two-round skill that extracts callable scenes, concepts, and entities from source text (see skill changelog)

## 3.9.3 - 2026-08-03

### Fixes

- **huawei-cloud-cost-estimation** **3.2.3**: add Measure Resolve after filtered `ListUsageTypes` (usage vs size slots, factor-family → measure/`usage_value`); densify pricing commands; probe OBS `usage_measure_id=10`

## 3.9.2 - 2026-08-03

### Fixes

- **huawei-cloud-cost-estimation** **3.2.2**: make the pricing resolve chain explicit (`ListServiceResources` → `ListResourceSpecs` → filtered `ListUsageTypes` → quote); stop defaulting Duration/hour; add evals #20–29 and grader branches for OBS/RDS resolve probes

## 3.9.1 - 2026-08-01

### Fixes

- **huawei-cloud-cost-estimation** **3.2.1**: replace the dense Call Budget labels with two plain-language execution-pacing sentences while preserving command limits and safety gates

## 3.9.0 - 2026-08-01

### Features

- **constraint-charter** **0.1.0**: add a skill that turns Uncle Bob-style audit goals and numeric gates into a versioned `GATES.md` contract wired to pre-commit/CI
- **huawei-cloud-cost-estimation** **3.2.0**: add a bounded progressive-execution contract for long `hcloud` command chains while preserving complete-batch dry-run and confirmation gates (see skill changelog)

## 3.8.0 - 2026-07-14

### Features

- **huawei-cloud-cost-estimation** **3.1.0**: add `CloudIDE/CreateInstance`; rewrite all 74 lifecycle command semantics with official product names, API versions, and billing boundaries; ordinary CodeArts `Create*` stay excluded; unsubscribe remains console-guidance-only (see skill changelog)

## 3.7.0 - 2026-07-14

### Features

- **huawei-cloud-cost-estimation** **3.0.0**: unsubscribe downgraded to console-guidance-only — no CLI/API execution or preview; 73 allowlisted create ops keep `--dryrun`/fee/confirmation gates; updated eval #17 and write-boundary validation (see skill changelog)

## 3.6.0 - 2026-07-13

### Features

- **huawei-cloud-cost-estimation** **2.0.0**: controlled lifecycle on top of RFQ — 73 allowlisted create ops + `BSS CancelResourcesSubscription`; mandatory local `--dryrun`, fee echo (or unknown-fee extra confirm), explicit confirmation; `pricing/` + `lifecycle/` reference split; write allowlist gate and dry-only evals #13–18 (see skill changelog)

## 3.5.0 - 2026-07-13

### Features

- **huawei-cloud-cost-estimation** **1.1.0**: `resource_spec` resolution unified on `BSS/ListResourceSpecs` — live fuzzy search, throttle-aware query discipline, collapsed semantic dimension; eval #12 (see skill changelog)

## 3.4.1 - 2026-07-10

### Features

- **semantic-creator** **0.5.1**: fixed YAGNI guidance tooltips on fact/dimension/measure/routing sections — plain-language terminology, evidence criteria, short examples, keyboard/touch access; eval and validate gate updated (see skill changelog)

## 3.4.0 - 2026-07-10

### Features

- **semantic-creator** **0.5.0**: Phase 2 rebuilt as an HTML decision workbench — atomic decisions with mutually exclusive options, dependency blocking, explicit approval (`approved:true`), five user actions, and Chinese-labeled enums; eval and validate gate updated (see skill changelog)

## 3.3.0 - 2026-07-08

### Features

- **semantic-creator** **0.4.0**: Phase 2 review rebuilt as template+data — agent injects model JSON into `assets/review-template.html` (inline vendored petite-vue, offline, no CDN); annotation export degrades when clipboard unavailable; previous-round verdicts re-importable; hard stop before Emit; eval #6 rewritten (see skill changelog)

## 3.2.0 - 2026-07-08

### Features

- **huawei-cloud-account-onboarding** **0.1.0**: real-name verification QR mock workflow — mock server, create/poll scripts, terminal QR flow, QA gate (see skill changelog)
- **semantic-creator** **0.3.0**: phase-aligned four-stage workflow (Ingest → Review → Emit → Verify); interactive HTML design-review report with clipboard-JSON annotations and `amendments.md` iteration; OKF v0.1 default emit; semantic lint and slim catalog routing aligned with OKF Entry Points (see skill changelog)

## 3.1.1 - 2026-06-29

### Changed

- **semantic-creator** **0.2.0**: Kimball star-schema focus — default emit is repo YAML; OKF optional; dimension kinds reduced to conformed / snowflake / degenerate; Confirm phase simplified (see skill changelog)
- **semantic-creator** **0.1.1**: rename from `semantic-layer-builder` (skills/, qa/, docs/)

## 3.1.0 - 2026-06-29

### Features

- **semantic-creator** **0.1.0**: meta-skill — guided interface-to-Kimball semantic layer modeling with OKF export (see skill changelog; renamed from `semantic-layer-builder` in 0.1.1)
- **huawei-cloud-account-onboarding** **0.1.0**: scaffold empty skill for Huawei Cloud real-name account onboarding (placeholder payload)

## 3.0.3 - 2026-06-02

### Changed

- **huawei-cloud-billing-scout** **2.3.9**: BSS `--cli-region=cn-north-1` rule, eval #25, semantic DRY, A/B grading harness (see skill changelog)
- **huawei-cloud-cost-estimation** **1.0.2**: BSS cli-region rule and eval #11 (see skill changelog)

## 3.0.2 - 2026-05-29

### Changed

- **huawei-cloud-cost-estimation** **1.0.1**: BSS command/semantic alignment, `response_contract`, DRY layer split in `CLAUDE.md`, 10 eval cases with A/B grading harness (see skill changelog)

## 3.0.1 - 2026-05-28

### Changed

- **versioning**: per-skill `qa/<name>/VERSION`; billing-scout **2.3.8**, cost-estimation **1.0.0** (decoupled from repo tag v3.0.0 skill bumps)
- **changelog**: split skill histories into `qa/<name>/CHANGELOG.md` (+ `.zh.md`; repo index here)

### Documentation

- README: dual-skill design, install, validate, and version tables updated

## 3.0.0 - 2026-05-28

### Changed

- **CI**: validate workflow installs required Python/Node QA tools; skill-scanner mandatory
- **hooks**: `.githooks/pre-commit` → `validate-all.sh`; `tools/install-git-hooks.sh`

### Features

- **huawei-cloud-cost-estimation** skill and QA bundle added to the monorepo (see skill changelog for **1.0.0** scope)
