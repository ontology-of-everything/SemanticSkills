# Semantic Skills

> 社区版本，非华为云官方。

云场景里 Agent 常犯同类错误：账期粒度选错、对账步骤跳过、没有证据就下结论，或在飞书/微信里用 Markdown 管道表导致排版错乱。SemanticSkills 用 [Agent Skills](https://agentskills.io/) 把领域语义放进可版本化的 `references/`，而不是堆在臃肿的 `SKILL.md` 里——先对齐「查什么事实」，再执行 CLI。

English: [README.md](README.md).

## 设计思路

**本体语义先行。** 在 `references/semantic/*.yml` 定义事实、粒度、维度、指标与只读 Operation；命令模板在 `related-commands.md`。`SKILL.md` 写安全边界、查证路径与**答复格式**（如简报式、聊天渠道禁用 `|...|` 表）。

```text
用户问题
     │
     ▼
catalog.yml ──────► 按 scope / 账期 / 金额口径路由
     │
     ▼
billing-ontology.yml ► 事实 + evidence_boundary + source_operation(s)
     │
     ▼
related-commands.md ► 最小只读 CLI（禁止先 --help）
     │
     ▼
答复格式 ► 先结论，后事实要点，一条只读补证
```

| 层 | 作用 | 典型文件 |
| --- | --- | --- |
| 路由 | 入口与 triggers | `references/semantic/catalog.yml` |
| 本体 | 事实、范围、口径、证据边界 | `references/semantic/billing-ontology.yml` |
| 命令 | 参数模板与安全上限 | `related-commands.md`、`cli-installation.md`、`iam-policies.md` |
| 协议 | North star、工作流、答复格式 | `SKILL.md` |

`skills/<name>/` 是**安装载荷**（`npx skills add` 只复制此目录）。`qa/<name>/` 放 `validate.sh`、eval 与审计配置（`bin/gate.py`、`skillcheck.toml` 等），**不会**随技能安装。

示例技能：[huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md)（**v2.3.6**）。编写规范：[docs/authoring.md](docs/authoring.md)。**Interaction discipline**（一次只问一事）：[authoring § Interaction discipline](docs/authoring.md#interaction-discipline-all-skills)。

## 仓库布局

```text
SemanticSkills/
├── skills/<name>/       # SKILL.md + references/（安装包）
├── qa/<name>/           # validate.sh、evals/、bin/gate.py、lint 配置
├── docs/                # catalog.yml、编写规范、各 Agent 安装说明
├── tools/               # validate-all.sh、skill-scaffold.sh
├── template/{skill,qa}/
├── *-workspace/         # Skill Creator 评测输出（不入库）
├── .agents/             # 本地 npx skills add 副本（不入库）
└── .credentials/        # 本地凭据样例（不入库）
```

## 技能

| 技能 | 版本 | 摘要 | 文档 |
| --- | --- | --- | --- |
| `huawei-cloud-billing-scout` | 2.3.5 | **华为云 · 花多少为何扣 · 只读对账** — KooCLI BSS 一页简报 | [详情](docs/skills/huawei-cloud-billing-scout.md) |

机器可读索引：[docs/catalog.yml](docs/catalog.yml)。

## 安装

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

**GitHub**（[Cursor](docs/agents/cursor.md)、[Claude Code](docs/agents/claude-code.md)、[Codex](docs/agents/codex.md)）：

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

将 `--agent cursor` 换成 `claude-code` 或 `codex`。列出本仓库技能：

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

**本地路径**（开发）：

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y
```

**Hermes**（[Hermes 说明](docs/agents/hermes.md)）：`hermes skills install ontology-of-everything/SemanticSkills/huawei-cloud-billing-scout -y`，或将本地 `skills/<name>/` rsync 到 `~/.hermes/skills/`。

## 验证

全部技能：

```bash
./tools/validate-all.sh
```

单技能（布局、契约、eval、可选风格门禁）：

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

仅风格审计（skillcheck + markdownlint + skill-scanner）：

```bash
python3 qa/huawei-cloud-billing-scout/bin/gate.py style
```

可选真实 BSS 烟测：

```bash
HUAWEICLOUD_BILLING_SCOUT_REAL=1 \
HUAWEICLOUD_BILLING_SCOUT_CYCLE=2025-04 \
./qa/huawei-cloud-billing-scout/validate.sh
```

离线协议评测（Skill Creator 目录）：

```bash
# 查看器：huawei-cloud-billing-scout-workspace/iteration-1/benchmark-review.html
```

## 贡献

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

新建技能：

```bash
./tools/skill-scaffold.sh <skill-name>
```

每次改技能须同步：`skills/`、`qa/`、`docs/catalog.yml`、`docs/skills/<name>.md`。

## 市场收录

| 渠道 | 说明 |
| --- | --- |
| [skills.sh](https://www.skills.sh/ontology-of-everything/SemanticSkills) | 已收录；`npx skills add ontology-of-everything/SemanticSkills --skill <name>` |
| [SkillsMP](https://skillsmp.com/) | 仓库已设 topic `claude-skills`、`claude-code-skill`；`SKILL.md` frontmatter；爬虫同步有周期 |
| [ClawHub](https://clawhub.ai/) | `clawhub skill publish`；`metadata.openclaw`；ClawHub 发布包为 **MIT-0**（仓库源码 Apache-2.0） |
| Cursor / Claude Code / Codex | `npx skills add ... --agent <agent>` |
| Hermes | `hermes skills install` 或复制 `skills/<name>/` — 见 [docs/agents/hermes.md](docs/agents/hermes.md) |

发布流程参考：[docs/skills/huawei-cloud-billing-scout.md](docs/skills/huawei-cloud-billing-scout.md)。
