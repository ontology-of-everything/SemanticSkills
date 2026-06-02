# 更新日志

Monorepo **基础设施**变更。各技能独立 changelog：

| 技能 | 更新日志 |
| --- | --- |
| huawei-cloud-billing-scout | [qa/huawei-cloud-billing-scout/CHANGELOG.zh.md](qa/huawei-cloud-billing-scout/CHANGELOG.zh.md) |
| huawei-cloud-cost-estimation | [qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md](qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md) |

## 3.0.3 - 2026-06-02

### 变更

- **huawei-cloud-billing-scout** **2.3.9**：BSS `--cli-region=cn-north-1`、eval #25、语义层 DRY、A/B 评分工具链（详见技能 changelog）
- **huawei-cloud-cost-estimation** **1.0.2**：BSS cli-region 规则与 eval #11（详见技能 changelog）

## 3.0.2 - 2026-05-29

### 变更

- **huawei-cloud-cost-estimation** **1.0.1**：BSS 命令/语义对齐、`response_contract`、CLAUDE 分层 DRY、10 条 eval 与 A/B 评分工具（详见技能 changelog）

## 3.0.1 - 2026-05-28

### 变更

- **版本**：各技能 `qa/<name>/VERSION`；billing-scout **2.3.8**、cost-estimation **1.0.0**（与误绑定的 repo v3.0.0 技能版本解耦）
- **changelog**：拆分到 `qa/<name>/CHANGELOG.md`（及 `.zh.md`；本文件为仓库索引）

### 文档

- README：双技能设计、安装、验证与版本表更新

## 3.0.0 - 2026-05-28

### 变更

- **CI**：validate 工作流安装必需 QA 工具；skill-scanner 必装
- **hooks**：`.githooks/pre-commit` → `validate-all.sh`；`tools/install-git-hooks.sh`

### 新功能

- monorepo 新增 **huawei-cloud-cost-estimation** 技能与 QA（详见该技能 changelog **1.0.0**）
