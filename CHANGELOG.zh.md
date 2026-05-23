# 更新日志

## 1.0.4 - 2026-05-23

### 变更

- **huawei-cloud-billing-scout**：在 `1.0.x` 版本轨上重新发布至 ClawHub；技能内容与
  `1.0.3` 一致（语义本体合并、压缩事实输出、21 条 eval）

## 1.0.3 - 2026-05-23

### 变更

- **huawei-cloud-billing-scout**：语义层合并为 `catalog.yml` +
  `billing-ontology.yml`；移除按实体拆分的 YAML 与 `billing-playbook.md`；
  精简 `related-commands.md` 并补齐已核验的 KooCLI dot-notation 模板
- **输出与 QA**：压缩事实型答复（`已证实` / `待核验`）、21 条 eval，加强
  `validate.sh` / `verify_ops.py` 的 Operation 合约校验

### 文档

- 更新 README、catalog 与各 Agent 安装说明（skills.sh、ClawHub、Hermes 本地符号链接）

## 1.0.0 - 2026-05-22

[SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) 首次公开发布（社区版，非华为云官方）：本体语义驱动的计费侦察技能、58 个 BSS 只读 Operation、`skills/` + `qa/` 布局、只读 BSS 边界。
