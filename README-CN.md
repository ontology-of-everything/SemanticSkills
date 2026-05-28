# Semantic Skills

> **华为社区版** · 社区维护，非华为云官方。

云场景里 Agent 常犯同类错误：账期粒度选错、询价臆造、对账步骤跳过、没有证据就下结论，或在飞书/微信里用 Markdown 管道表导致排版错乱。**SemanticSkills（华为社区版）** 用 [Agent Skills](https://agentskills.io/) 把领域语义放进可版本化的 `references/`，而不是堆在臃肿的 `SKILL.md` 里——先对齐「查什么事实」，再执行 CLI。

English: [README.md](README.md). **仓库发布版本：** v3.0.1 · 见 [CHANGELOG.zh.md](CHANGELOG.zh.md)（各技能 changelog 在 `qa/<name>/CHANGELOG.zh.md`）。

## 设计思路

**本体语义先行，按技能分模型。** 在 `references/semantic/*.yml` 定义事实、粒度、维度与只读 Operation；命令模板在 `related-commands.md`。`SKILL.md` 写安全边界、工作流与**答复格式**（简报式或分项报价；聊天渠道禁用 `|...|` 表）。

**当前两个技能**（独立安装包，互不路由）：

| 技能 | 关心 | 主本体 | 主 BSS 操作 |
| --- | --- | --- | --- |
| [huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md) | **已发生**账务 — 余额/账单/对账/券包 | `billing-ontology.yml` | 53 个只读查询 op |
| [huawei-cloud-cost-estimation](docs/skills/huawei-cloud-cost-estimation.md) | **未发生**报价 — 包年/包月与按需询价 | `rfq-period-model.yml`、`rfq-ondemand-model.yml` | `ListRateOnPeriodDetail`、`ListOnDemandResourceRatings` |

共用路由模式：

```text
用户问题
     │
     ▼
catalog.yml ──────► 按 pricing_mode 或 entry_point / triggers 路由
     │
     ▼
semantic/*.yml ───► 事实 + evidence_boundary + 维度
     │
     ▼
related-commands.md ► 最小只读 hcloud 命令（禁止先 --help）
     │
     ▼
SKILL.md 交付 ────► 先结论 · 标口径 · IM 友好分项
```

| 层 | 作用 | 典型文件 |
| --- | --- | --- |
| 路由 | 入口与 triggers | `references/semantic/catalog.yml` |
| 本体 | 事实、范围、证据边界 | `billing-ontology.yml` 或 `rfq-*-model.yml` + `rfq-shared-dimensions.yml` |
| 命令 | 参数模板与陷阱 | `related-commands.md`、`cli-installation.md`、`iam-policies.md` |
| 协议 | 工作流、答复格式 | `SKILL.md` |

`skills/<name>/` 是**安装载荷**（`npx skills add` 只复制此目录）。`qa/<name>/` 放 `validate.sh`、eval 与审计配置（有则含 `bin/gate.py`、`skillcheck.toml` 等），**不会**随技能安装。

编写规范：[docs/authoring.md](docs/authoring.md)。**Interaction discipline**（一次只问一事）：[authoring § Interaction discipline](docs/authoring.md#interaction-discipline-all-skills)。

## 仓库布局

```text
SemanticSkills/
├── skills/<name>/       # SKILL.md + references/（安装包）
├── qa/<name>/           # validate.sh、evals/、bin/gate.py（可选）、lint 配置
├── docs/                # catalog.yml、编写规范、各 Agent 安装说明
├── tools/               # validate-all.sh、skill-scaffold.sh、install-git-hooks.sh
├── .githooks/           # pre-commit → validate-all.sh（由 install-git-hooks.sh 启用）
├── template/{skill,qa}/
├── *-workspace/         # Skill Creator 评测输出（不入库）
├── .agents/             # 本地 npx skills add 副本（不入库）
└── .credentials/        # 本地凭据样例（不入库）
```

## 技能

| 技能 | 版本 | 摘要 | 文档 |
| --- | --- | --- | --- |
| `huawei-cloud-billing-scout` | 2.3.8 | **华为云 · 花多少为何扣 · 只读对账** — KooCLI BSS 一页简报 | [详情](docs/skills/huawei-cloud-billing-scout.md) · [changelog](qa/huawei-cloud-billing-scout/CHANGELOG.zh.md) |
| `huawei-cloud-cost-estimation` | 1.0.0 | **华为云成本估算** — hcloud BSS 包年/包月与按需询价 | [详情](docs/skills/huawei-cloud-cost-estimation.md) · [changelog](qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md) |

机器可读索引：[docs/catalog.yml](docs/catalog.yml)。

## 安装

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

**GitHub**（[Cursor](docs/agents/cursor.md)、[Claude Code](docs/agents/claude-code.md)、[Codex](docs/agents/codex.md)）：

```bash
# 账务（已发生花费 / 对账）
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy -y

# 询价（包年/包月与按需报价）
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

将 `--agent cursor` 换成 `claude-code` 或 `codex`。列出本仓库技能：

```bash
npx skills add ontology-of-everything/SemanticSkills --list
```

**本地路径**（开发）：

```bash
npx skills add ./skills/huawei-cloud-cost-estimation \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

**Hermes**（[Hermes 说明](docs/agents/hermes.md)）：`hermes skills install ontology-of-everything/SemanticSkills/<skill-name> -y`，或将 `./skills/<name>/` rsync 到 `~/.hermes/skills/`。

## 验证

安装本地 pre-commit（每次 commit 跑 `./tools/validate-all.sh`）：

```bash
./tools/install-git-hooks.sh
```

全部技能（与 CI 一致）：

```bash
./tools/validate-all.sh
```

单技能：

```bash
./qa/huawei-cloud-billing-scout/validate.sh      # 全量：布局、契约、协议 eval、风格
./qa/huawei-cloud-cost-estimation/validate.sh    # layout、skills-ref、markdownlint、skillcheck
```

仅风格审计（billing-scout）：

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

每次改技能须同步：`skills/`、`qa/`（含 `VERSION` 与 `CHANGELOG.md`）、`docs/catalog.yml`、`docs/skills/<name>.md`。

## 市场收录

| 渠道 | 说明 |
| --- | --- |
| [skills.sh](https://www.skills.sh/ontology-of-everything/SemanticSkills) | 已收录；`npx skills add ontology-of-everything/SemanticSkills --skill <name>` |
| [SkillsMP](https://skillsmp.com/) | 仓库已设 topic `claude-skills`、`claude-code-skill`；`SKILL.md` frontmatter；爬虫同步有周期 |
| [ClawHub](https://clawhub.ai/) | `clawhub skill publish`；`metadata.openclaw`；ClawHub 发布包为 **MIT-0**（仓库源码 Apache-2.0） |
| Cursor / Claude Code / Codex | `npx skills add ... --agent <agent>` |
| Hermes | `hermes skills install` 或复制 `skills/<name>/` — 见 [docs/agents/hermes.md](docs/agents/hermes.md) |

发布流程参考：[docs/skills/huawei-cloud-billing-scout.md](docs/skills/huawei-cloud-billing-scout.md)。
