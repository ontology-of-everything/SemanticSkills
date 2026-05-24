# Changelog

## 2.3.3 - 2026-05-24

### Changed

- **huawei-cloud-billing-scout**: YAGNI briefing-style **输出合同** (summary, fact
  bullets, one follow-up); drop rigid `事实项 | 结果 | 状态` schema; **易懂的事实称呼**
  aligned with dialogue and console wording (no user-facing API names); chat-safe
  formatting without GFM pipe tables
- **qa/huawei-cloud-billing-scout**: `llm-rubric.yml`, `run_protocol_eval.py`,
  `export_llm_eval.py`, expanded eval assertions; validate guards aligned with the
  new contract

### Documentation

- `CLAUDE.md`, `docs/skills/huawei-cloud-billing-scout.md`, QA READMEs

## 2.3.2 - 2026-05-23

### Documentation

- Consolidate release notes: drop interim `1.0.x` ClawHub republish entries; history
  lives under `2.3.x` only

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
