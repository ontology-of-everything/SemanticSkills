# Semantic Skills

> 社区版本，非华为云官方。

云场景里 Agent 出错方式很固定：账期粒度选错、对账步骤跳过、表格没出来就敢下结论。SemanticSkills 用 [Agent Skills](https://agentskills.io/) 把领域语义放进可版本化的 `references/`，而不是堆在 `SKILL.md` 里——先对齐「查什么事实」，再决定「怎么查命令」。

English: [README.md](README.md).

## 设计思路

**本体语义先行。** 每个技能在 `references/semantic/*.yml` 里定义事实实体（粒度、维度、指标、来源 Operation）；命令参数单独一层。`SKILL.md` 写执行协议；协作手册负责多步编排与输出形态。

运行时一条问题走这条链：

```text
用户问题
     │
     ▼
语义层 ────────► 抽取事实/维度/指标 → source_operation(s)
     │
     ▼
命令层 ──────────► related-commands.md 取模板 → 直接执行（禁止先 --help）
     │
     ▼
协作手册（多步时）──► 查询顺序 + 输出结构
     │
     ▼
同一 yml ────────► 解析 dimensions/measures → 结论 → 事实依据
```


| 层    | 放什么               | 典型文件                                         |
| ---- | ----------------- | -------------------------------------------- |
| 本体语义 | 事实定义 + 响应解析 | `references/semantic/*.yml` |
| 命令   | API/CLI 模板      | `related-commands.md`、IAM、安装说明               |
| 协作手册 | 多步编排、用户可读输出 | `*-playbook.md`                              |
| 目录/术语 | 领域路由、语义模型和可选术语口径 | `semantic/catalog.yml`、`*-semantics.md` |


`skills/<name>/` 是可安装运行时包；`qa/<name>/` 放 eval 与验证脚本，不会被 `npx skills add` 复制。可出现在 [skills.sh](https://www.skills.sh/)、由 [SkillsMP](https://skillsmp.com/) 抓取，并可发布到 [ClawHub](https://clawhub.ai/)。

示例：[huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md)。编写规范：[docs/authoring.md](docs/authoring.md)。

## 仓库布局

```text
SemanticSkills/
├── skills/              # 可安装运行时包（SKILL.md + references/）
├── qa/                  # 各技能验证（evals、assertions、validate.sh）
├── docs/                # 贡献指南、编写规范、catalog、各 agent 安装说明
├── tools/               # validate-all.sh、skill-scaffold.sh
├── template/skill/      # 新技能脚手架（不可安装）
├── .workspaces/         # Skill Creator 运行结果（不入库）
├── .agents/             # 本地 npx skills add 副本（不入库）
└── .credentials/        # 本地凭据样例（不入库）
```

## 技能


| 技能                           | 路径                                   | 摘要                    | 文档                                              |
| ---------------------------- | ------------------------------------ | --------------------- | ----------------------------------------------- |
| `huawei-cloud-billing-scout` | `skills/huawei-cloud-billing-scout/` | 华为云账务只读侦察（KooCLI/BSS） | [详情](docs/skills/huawei-cloud-billing-scout.md) |


机器可读索引：[docs/catalog.yml](docs/catalog.yml).

## 安装

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

从 GitHub 安装（[Cursor 说明](docs/agents/cursor.md)）：

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

Claude Code 或 Codex：

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent claude-code \
  --copy -y

npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent codex \
  --copy -y
```

安装前先列出本仓库可用技能：

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

本地路径：

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

## 验证

全部技能：

```bash
./tools/validate-all.sh
```

单个技能：

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

可选真实 BSS 烟测：

```bash
HUAWEICLOUD_BILLING_SCOUT_REAL=1 \
HUAWEICLOUD_BILLING_SCOUT_CYCLE=2025-04 \
./qa/huawei-cloud-billing-scout/validate.sh
```

## 贡献

见 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) 与 [docs/authoring.md](docs/authoring.md).

新建技能：

```bash
./tools/skill-scaffold.sh <skill-name>
```

## 市场收录

- [skills.sh](https://www.skills.sh/)：
  公开 GitHub + `npx skills add`；需要有效的
  `skills/<name>/SKILL.md` 与 README 安装命令。
- [SkillsMP](https://skillsmp.com/)：
  GitHub 爬虫和语义搜索；需要 `SKILL.md` frontmatter，并添加
  `claude-skills` 或 `claude-code-skill` GitHub topic。
- [ClawHub](https://clawhub.ai/)：
  `clawhub skill publish <path>`；需要 GitHub 账号年龄、semver 版本、
  纯文本包和准确的 `metadata.openclaw`。
- Cursor：
  `npx skills add ... --agent cursor`；也发现 `.cursor/skills/` 与
  `.agents/skills/`。
- Claude Code：
  `npx skills add ... --agent claude-code`；本轮不需要插件市场包装。
- Codex：
  `npx skills add ... --agent codex`；直接技能安装不需要 Codex 插件包装。

每个技能位于 `skills/<name>/SKILL.md`，包含 `name`、带触发词的
`description`、精简的 `compatibility`，以及需要时的 registry metadata。
ClawHub 发布版本统一按 MIT-0 授权，因此可安装技能 frontmatter 不写冲突的
license；本仓库源码仍保留 Apache-2.0。参考技能见
[docs/skills/huawei-cloud-billing-scout.md](docs/skills/huawei-cloud-billing-scout.md)。