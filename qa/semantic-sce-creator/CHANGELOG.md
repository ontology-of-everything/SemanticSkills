# semantic-sce-creator Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.2.0 - 2026-08-28

### Changed

- Rename the installable skill from `sce-creator` to `semantic-sce-creator`.
  Output files stay `sce-scenes.yaml`, `sce-concepts.yaml`, `sce-entities.yaml`.
  The old name remains a trigger keyword.

## 0.1.0 - 2026-08-18

### Added

- Initial SCE Creator skill: two-round extract of scenes, concepts, and entities
  from source text (skeleton first, then IPO / decompose / assemble)
- Eight relation types, five writing principles, and a confirmation gate
  between rounds
- Layering inspired by 人月聊 IT, 《三层架构：场景、概念与实体》
