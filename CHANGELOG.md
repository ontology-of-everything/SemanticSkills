# Changelog

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
