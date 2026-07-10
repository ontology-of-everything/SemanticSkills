# semantic-creator Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.5.1 - 2026-07-10

### Added

- Fact, dimension, measure, and routing sections now expose compact fixed guidance with
  plain-language terminology, evidence criteria, YAGNI boundaries, and short examples
- Guidance tooltips support hover, keyboard focus, click, and Escape without changing
  the decision model or approval semantics

### QA

- Review validation and eval assertions now require all four guidance topics and
  non-hover-only access

## 0.5.0 - 2026-07-10

### Changed

- Phase 2 is now a decision workbench rather than a conclusion ledger: object containers
  hold atomic decisions with explicit questions, impacts, risks, evidence basis,
  confidence, priority, and user status
- Uncertain decisions present 2–4 mutually exclusive options; every option states its
  applicability, benefit, cost, risk, evidence references, and recommendation reason
- Decision relations model dependencies, conflicts, and trade-offs; unresolved
  dependencies hard-block downstream decisions
- Approval is fully explicit: decisions start pending, non-recommended selections require
  reasons, unresolved feedback exports as a draft, and only a complete user action set can
  emit `approved:true`
- User actions now distinguish confirm, select, correct, supplement, and reject; rejection
  requests a reframed decision instead of silently deleting an object

### QA

- Review eval now checks the decision ontology, hard blocking, explicit approval, and
  offline decision export/import

## 0.4.0 - 2026-07-08

### Changed

- Phase 2 review report rebuilt as template + data: agent no longer hand-writes HTML — it emits a compact model JSON and injects it into the fixed shell `assets/review-template.html` (inline CSS + vendored petite-vue ~6KB, still self-contained, no CDN, no network); shrinks per-iteration output and stabilizes report structure
- Report UX: sections collapsed by default with anchor nav and text filter; annotation export degrades gracefully when clipboard is unavailable under `file://` (select-all textarea + `verdicts.json` download); previous-round verdicts can be re-imported to refill card state
- Review gate hardened: after emitting the report the agent MUST STOP and wait for user verdicts/approval (`approved_rest: true`); entering Phase 3 without approval is forbidden (SKILL.md Critical Rule 6 + review.md §5)
- `amendments.md` location fixed: written next to the report in `$TMPDIR` during Phase 2, copied into the output directory at Phase 3 emit
- Eval #6 rewritten for the template+data flow (export usable via clipboard or fallback; hard stop before approval)

### Added

- `assets/review-template.html` — review report shell (inline renderer + vendored petite-vue), the only new install-payload file

## 0.3.0 - 2026-07-08

### Changed

- Phase 2: four sequential chat confirmations replaced by a single interactive HTML design-review report (`references/review-report.md`) — per-card evidence, confidence badges (confirmed/inferred/assumed), verdict controls; annotations returned via clipboard JSON and persisted to `amendments.md` as iteration input
- Default emit target flipped: Google OKF v0.1 bundle is now the default; repo-YAML demoted to optional target (eval #3 rewritten)
- References restructured phase-aligned (one file per phase, each with entry/exit criteria): `ingest.md` (Phase 1), `review.md` (Phase 2 interview + HTML review + amendments), `emit-okf.md` / `emit-yaml.md` (Phase 3), `verify.md` (Phase 4, all checks consolidated); replaces `elicitation-playbook.md` / `okf-emitter.md` / `schema-spec.md`
- Conformance extended with semantic lint: naming consistency (one business_key = one dimension name), dimension reuse (no redefinition of existing shared dimensions), escalation loop (non-mechanical failures go back to One blocking ask)
- Multi-bundle support: thin root index (one line per bundle) generated only when ≥2 bundles exist
- `semantic_catalog` slimmed to routing essentials (dropped constant `modeling_method` and derivable `primary_operations` / `primary_doc_urls`); OKF root `index.md` gains an `# Entry Points` section so both targets carry the same routing

### Added

- HTML review report spec in `references/review.md` (self-contained, inline CSS/JS, no CDN)
- Eval #6 `review-report-before-emit`

## 0.2.0 - 2026-06-29

### Changed

- Focus on Kimball methodology: dimension `kind` reduced to `conformed` / `snowflake` / `degenerate`
- Default emit target is repo-YAML Kimball star/constellation; Google OKF v0.1 demoted to optional export
- Phase 2 Confirm simplified from 5 to 4 steps (removed Selection & Pairing)

### Removed

- Non-Kimball dimension extensions: `abstract_dimension` + `selection_rule` / `resolved_by`, `encoded_constant_dimension`, `scope_dimension`, `dimension_catalog`; `scope` frame role
- `schema-spec.md` §5 `selection_rule` section and its Conformance check (Conformance renumbered §6 → §5)

## 0.1.1 - 2026-06-29

### Changed

- Rename skill id `semantic-layer-builder` → `semantic-creator` (skills/, qa/, docs/catalog.yml, docs/skills/, evals, validate)

## 0.1.0 - 2026-06-29

First release — meta-skill that turns an interface into a governed semantic layer.

### Features

- Guided, one-fact-at-a-time interview: Ingest → Frame → Confirm (facts/grain/dimensions/measures/routing) → Emit
- Schema constraints for semantic objects (Kimball star/constellation): `catalog` (thin router) → shared-dimensions → model, in `references/schema-spec.md` with a Conformance checklist
- Google OKF v0.1 export (recommended): concept-per-file mapping, reserved files, frontmatter, and OKF §9 hard-constraint check in `references/okf-emitter.md`
- Evidence-only discipline: refuses to invent fields, grain, enums, or values; missing sources marked `TODO(verify)`
- Ingest rules for REST/OpenAPI, CLI, and table/DDL inputs; end-to-end worked example (`references/examples.md`)

### qa

- `validate.sh` (layout, version sync, skills-ref, markdownlint, skillcheck)
- Five offline evals in `evals/evals.json` (grain-first, no-invented-fields, OKF default target, one-blocking-ask, layer-split)

### Documentation

- `docs/skills/semantic-creator.md`; `docs/catalog.yml` index entry
