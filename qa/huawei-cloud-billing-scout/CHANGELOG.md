# huawei-cloud-billing-scout Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 2.3.8 - 2026-05-28

### Changed

- **SKILL.md**: **华为社区版** blockquote; remove duplicate「官方身份」boundary bullet (DRY)
- **qa**: `gate.py full` requires skillcheck, markdownlint, and skill-scanner (`require_all=True`)
- **versioning**: per-skill `qa/huawei-cloud-billing-scout/VERSION` (decoupled from repo root `VERSION`)

### Documentation

- `docs/skills/huawei-cloud-billing-scout.md`: version **2.3.8**; point pre-order quotes to cost-estimation skill
- README skill table and `docs/catalog.yml` aligned

## 2.3.7 - 2026-05-26

### Changed

- Retract to **billing-only** BSS read scope — drop pricing-quote and real-name review (`quote_and_identity`); **53** read-only query operations (was 58); sync ontology, commands, IAM, `ops_contracts`
- `catalog.yml`: **`provider_gate`**, **`out_of_scope`** table, **华为云**-prefixed entry triggers

### Features

- Restructure `SKILL.md` (principles, roles, four-stage investigation, red lines, briefing delivery, boundaries)
- Interaction discipline — evals 22–24, rubric `interaction_discipline`; **24** eval cases total

### qa

- **`refuse-*`** evals replace removed quote/identity cases; gate **53** needles; `protocol_grading.py` updated

## 2.3.5 - 2026-05-24

### Changed

- English-first marketplace title **Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation**; longer English `description` for routing

## 2.3.4 - 2026-05-24

### Changed

- Display name **华为云 · 花多少为何扣 · 只读对账**; ClawHub security-audit alignment; CLI install doc user-manual-only
- Unified offline gate in `bin/gate.py`

## 2.3.2 - 2026-05-24

### Changed

- **IM-safe delivery** — no GFM pipe tables in chat; briefing-style **答复格式**; FinOps-oriented `SKILL.md` structure
- `llm-rubric.yml`, protocol eval golden answers, skillcheck/markdownlint/skill-scanner configs

## 2.3.1 - 2026-05-23

### Changed

- Semantic layer in `catalog.yml` + `billing-ontology.yml`; streamlined `related-commands.md`; **21** evals

## 2.0.0 - 2026-05-22

First public release: ontology-first billing scout, **58** read-only BSS operations, read-only guardrails.
