# Changelog

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
