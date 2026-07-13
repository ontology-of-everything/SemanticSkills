# Changelog

Monorepo **infrastructure** history. Each skill has its own changelog:

| Skill | Changelog |
| --- | --- |
| huawei-cloud-billing-scout | [qa/huawei-cloud-billing-scout/CHANGELOG.md](qa/huawei-cloud-billing-scout/CHANGELOG.md) |
| huawei-cloud-cost-estimation | [qa/huawei-cloud-cost-estimation/CHANGELOG.md](qa/huawei-cloud-cost-estimation/CHANGELOG.md) |
| huawei-cloud-account-onboarding | [qa/huawei-cloud-account-onboarding/CHANGELOG.md](qa/huawei-cloud-account-onboarding/CHANGELOG.md) |
| semantic-creator | [qa/semantic-creator/CHANGELOG.md](qa/semantic-creator/CHANGELOG.md) |

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
