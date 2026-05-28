# Changelog

## 3.0.0 - 2026-05-28

### Features

- **huawei-cloud-cost-estimation**: new skill for Huawei Cloud pre-order BSS pricing — period
  (`ListRateOnPeriodDetail`) and on-demand (`ListOnDemandResourceRatings`); Parse / Clarify /
  Spec Review / Estimation workflow; semantic routing via `rfq-*-model.yml`
- **huawei-cloud-cost-estimation**: QA bundle with `validate.sh`, seven offline evals, and
  skillcheck/markdownlint gates

### Changed

- **project**: CI validate workflow installs required Python and Node QA tools; skill-scanner
  install is mandatory
- **project**: tracked `.githooks/pre-commit` runs `validate-all.sh`;
  `tools/install-git-hooks.sh` sets `core.hooksPath`
- **huawei-cloud-billing-scout**: `gate.py full` requires skillcheck, markdownlint, and
  skill-scanner (`require_all=True`)

### Documentation

- **huawei-cloud-cost-estimation**: `docs/skills/huawei-cloud-cost-estimation.md` and
  `docs/catalog.yml` index entry
- **project**: README skill tables list cost-estimation

## 2.3.7 - 2026-05-26

### Changed

- **huawei-cloud-billing-scout**: retract skill to billing-only BSS read scope — drop
  pricing-quote and real-name review (`quote_and_identity`), **53** aligned read-only BSS
  query operations (was 58); sync `billing-ontology.yml`, `catalog.yml`,
  `related-commands.md`, `iam-policies.md`, `fixtures/ops_contracts.yml`
- **huawei-cloud-billing-scout**: `catalog.yml` adds **`provider_gate`** (Huawei Cloud / BSS /
  profile signal before BSS calls), **`out_of_scope`** refusal table, and **华为云‑prefixed**
  entry-point triggers

### qa

- **huawei-cloud-billing-scout**: evals **`refuse-*`** replace removed quote/identity cases;
  `protocol_grading.py`; gate **`53`** needles and `verify_ops` message

### Documentation

- **huawei-cloud-billing-scout**: `docs/skills/huawei-cloud-billing-scout.md`,
  `docs/catalog.yml` **`2.3.7`** summaries; ClawHub publish changelog / clawscan wording


### Features

- **huawei-cloud-billing-scout**: restructure `SKILL.md` (principles, roles, four-stage investigation
  table, red lines, briefing delivery, boundaries); expand `related-commands.md` BSS templates
- **huawei-cloud-billing-scout**: interaction discipline — evals 22–24, `protocol_grading.py`,
  rubric `interaction_discipline`; **24** eval cases total

### Changed

- **qa/huawei-cloud-billing-scout**: gate export count tracks eval count; fail if `skills/*-workspace`
  exists (Skill Creator output belongs at repo root)

### Documentation

- **authoring**: interaction discipline for all skills; SkillsMP monorepo topic indexing note
- **project**: `CLAUDE.md` Skill Creator workspace placement; README and agent guides link
  discipline section

### Template

- **template**: `validate.sh` rejects `*-workspace` under `skills/`

## 2.3.5 - 2026-05-24

### Changed

- **huawei-cloud-billing-scout**: English-first marketplace title
  **Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation**; longer
  English `description` for search and skill routing (Chinese display name unchanged)

## 2.3.4 - 2026-05-24

### Changed

- **huawei-cloud-billing-scout**: marketplace display name **华为云 · 花多少为何扣 · 只读对账**
  (English: *Huawei Cloud: Spend, Charges & Reconcile (Read-Only)*); slug unchanged;
  `description` and `docs/catalog.yml` `display_name*` aligned to user intent keywords
- **huawei-cloud-billing-scout**: ClawHub security-audit alignment — Huawei Cloud-only
  description; enterprise/partner and read-only quote scope; reply language follows user;
  tighter catalog triggers; CLI install doc is user-manual-only (Agent must not run
  install/`sudo`)
- **qa/huawei-cloud-billing-scout**: unified offline gate in `bin/gate.py`
  (`validate.sh` → full; `gate.py style` for skillcheck/markdownlint/skill-scanner)

## 2.3.2 - 2026-05-24

### Changed

- **huawei-cloud-billing-scout**: **IM-safe delivery** — do not use GFM pipe tables
  (`|...|`) in single chat messages (Feishu, WeChat, and similar channels); use a
  short summary plus fact bullets (`·` or paragraphs) instead
- YAGNI **答复格式** replaces the rigid `事实项 | 结果 | 状态` schema; **易懂的事实称呼**
  aligned with dialogue and console wording (no user-facing API names)
- **SKILL.md** reframed for FinOps: 工作准则 / 安全红线 / 查证路径 / 答复格式
- **qa/huawei-cloud-billing-scout**: `llm-rubric.yml`, protocol eval golden answers,
  and `validate.sh` guards aligned with the new contract; offline benchmark records
  real wall-clock for golden-answer generation (not placeholder LLM timing)

### Added

- `qa/huawei-cloud-billing-scout/bin/skillgate.sh` plus `skillcheck.toml`,
  `.markdownlint.json`, and `policy.skill-scanner.yaml` for local audit (not copied
  by `npx skills add`; ClawHub-compatible: no `license` in frontmatter)

### Documentation

- `docs/skills/huawei-cloud-billing-scout.md`, QA READMEs; consolidated release
  history under `2.3.x` (dropped interim `1.0.x` ClawHub republish notes)

## 2.3.1 - 2026-05-23

### Changed

- **huawei-cloud-billing-scout**: semantic layer in `catalog.yml` +
  `billing-ontology.yml` (removed per-entity YAML shards and `billing-playbook.md`);
  streamlined `related-commands.md` with verified KooCLI dot-notation templates
- Compact fact-table output (`已证实` / `待核验`), **21** evals, tighter
  `validate.sh` / `verify_ops.py`; lean `SKILL.md` and routing headers (~1% trim)

### Documentation

- README, catalog, and agent install paths (skills.sh, ClawHub, Hermes direct skill)

## 2.0.0 - 2026-05-22

First public [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills)
release (community, not official Huawei Cloud): ontology-first billing scout with
**58** read-only BSS operations, `skills/` + `qa/` monorepo layout, read-only
guardrails.
