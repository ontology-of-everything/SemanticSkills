# Changelog

## 2.3.1 - 2026-05-23

### Changed

- **huawei-cloud-billing-scout**: resync repo semver to `2.3.x`; lean
  `SKILL.md`, `catalog.yml`, and ontology headers (~1% noise trim); unchanged
  semantics, fact-table output contract, and 21 evals

## 1.0.5 - 2026-05-23

### Changed

- **huawei-cloud-billing-scout**: lean `SKILL.md`, `catalog.yml`, and ontology
  headers (~1% noise trim); same semantics, output contract, and 21 evals

## 1.0.4 - 2026-05-23

### Changed

- **huawei-cloud-billing-scout**: ClawHub republish on the `1.0.x` track; package
  matches `1.0.3` skill content (semantic ontology, compact fact output, 21 evals)

## 1.0.3 - 2026-05-23

### Changed

- **huawei-cloud-billing-scout**: consolidate semantics into `catalog.yml` +
  `billing-ontology.yml`; remove per-entity YAML shards and `billing-playbook.md`;
  streamline `related-commands.md` with verified KooCLI dot-notation templates
- **Output & QA**: compact fact-based replies (`已证实` / `待核验`), 21 evals, and
  tighter `validate.sh` / `verify_ops.py` operation contracts

### Documentation

- README, catalog, and agent install notes (skills.sh, ClawHub, Hermes direct
  skill symlink)

## 1.0.0 - 2026-05-22

First public [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills)
release (community, not official Huawei Cloud): ontology-first billing scout with
58 read-only BSS operations, `skills/` + `qa/` monorepo layout, read-only
guardrails.
