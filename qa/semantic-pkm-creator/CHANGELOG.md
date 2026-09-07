# semantic-pkm-creator Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.3.0 - 2026-09-07

### Changed

- Rename the installable skill from `semantic-sce-creator` to
  `semantic-pkm-creator`: the skill serves personal knowledge management;
  `sce` stays as the output-file prefix (`sce-*.yaml`) and a trigger keyword
- Restructure SKILL.md into the six-section skeleton (目标 / 原则 / 流程 /
  命题 / 记法与模板 / 参考) and cut it to ~79% of its size (4.3 KB → 3.4 KB;
  the skill was already lean). The eight relation types move to
  `references/relations.md` with a decision order; the two rounds become one
  numbered flow with a mandatory stop; completion criteria become checkable
  propositions

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
