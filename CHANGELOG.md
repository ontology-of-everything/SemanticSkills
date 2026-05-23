# Changelog

## 2.3.0 - 2026-05-23

### Changed

- **huawei-cloud-billing-scout**: consolidate semantics into `catalog.yml` +
  `billing-ontology.yml`; remove per-entity YAML shards and `billing-playbook.md`;
  streamline `related-commands.md` with verified KooCLI dot-notation templates
- **Output & QA**: compact fact-based replies (`已证实` / `待核验`), 21 evals, and
  tighter `validate.sh` / `verify_ops.py` operation contracts

### Documentation

- README, catalog, and agent install notes (skills.sh, ClawHub, Hermes direct
  skill symlink)

## 2.1.0 - 2026-05-23

- Expand to **58** read-only BSS query operations; rebuild QA verifier, eval
  suite, and marketplace-ready skill docs

## 2.0.0 - 2026-05-22

First public [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills)
release (community, not official Huawei Cloud): ontology-first billing scout,
`skills/` + `qa/` monorepo layout, read-only BSS guardrails.
