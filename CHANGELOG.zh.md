# 更新日志

## 2.0.1 - 2026-05-22

### 文档

- `huawei-cloud-billing-scout`：重构 `SKILL.md`，增加与 eval 对齐的验收标准与六步协议，正文约减 10%
- playbook、语义说明与 QA 断言统一为语义路由表述，移除 FAQ / 经典问题用语

## 2.0.0 - 2026-05-22

[SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) 首次公开发布 — 社区版本，非华为云官方。

### 新功能

- `huawei-cloud-billing-scout`：基于 KooCLI/BSS 的华为云账务只读侦察（找事实、做归因、做对账、做咨询）
- 本体语义驱动：`references/semantic/*.yml` 定义事实实体；`SKILL.md` 承载执行协议；命令与 playbook 分层存放

### 重构

- 标准 monorepo 布局：`skills/`、`qa/`、`docs/`、`tools/`、`template/`；安装包不含 eval 与 QA
- 统一 `billing-playbook.md`（合并原场景/流程文档）；输出表格优先、证据驱动、用户可读
- 按事实/维度/指标/时间/范围路由，不再 FAQ 匹配；实体 YAML 移除 `common_questions`
- 目的驱动执行协议 + 前置检查；优先 `related-commands.md`，`--help` 仅兜底
- 只读边界：允许 BSS `List*ChangeRecords` 流水查询；拒绝可变写操作
- 语义字段补齐：`CouponChangeRecord.trade_id`、资源详单 region/企业项目、`resource_type_code` 路径修正

### 文档

- README / README-CN：语义分层运行时、`npx skills` 安装命令、skills.sh 徽章、三平台市场收录表（skills.sh / SkillsMP / ClawHub）
- 强化 `SKILL.md` frontmatter（`description`、`compatibility`、`metadata.openclaw`）便于检索与 ClawHub 安全审查
- 技能文档、编写规范、catalog、QA 断言与 `CLAUDE.md` 同步语义层模型与 QA 布局

### 测试

- 每 skill 独立 `validate.sh`；仓库级 `./tools/validate-all.sh`（CI）
- Eval、semantic 路由、实体覆盖、只读策略防回归
- 跨层校验：`fixtures/ops_contracts.yml` + `bin/verify_ops.py`（semantic ↔ 命令文档 ↔ 可选 `hcloud --help`）
- 外部门禁：`skills-ref`、skillcheck、markdownlint、skill-scanner、安装烟测

### 维护

- 忽略本地路径：`.agents/`、`.workspaces/`、`.credentials/`、`skills/*-workspace/`、gate 报告
