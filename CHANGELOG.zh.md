# 更新日志

## 2.3.2 - 2026-05-23

### 文档

- 合并版本记录：移除 interim `1.0.x` ClawHub 重发条目；发布历史统一在 `2.3.x`

## 2.3.1 - 2026-05-23

### 变更

- **huawei-cloud-billing-scout**：语义层合并为 `catalog.yml` +
  `billing-ontology.yml`（移除按实体 YAML 与 `billing-playbook.md`）；精简
  `related-commands.md` 并补齐已核验 KooCLI dot-notation 模板
- 压缩事实表输出（`已证实` / `待核验`）、**21** 条 eval，加强
  `validate.sh` / `verify_ops.py`；精简 `SKILL.md` 与路由头部（约 1% 降噪）

### 文档

- 更新 README、catalog 与各 Agent 安装说明（skills.sh、ClawHub、Hermes）

## 2.0.0 - 2026-05-22

[SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) 首次公开发布（社区版，非华为云官方）：本体语义驱动的计费侦察技能、**58** 个 BSS 只读 Operation、`skills/` + `qa/` 布局、只读 BSS 边界。
