# Semantic Skills

[![skills.sh](https://skills.sh/b/ontology-of-everything/SemanticSkills)](https://skills.sh/ontology-of-everything/SemanticSkills)

> 面向编码 Agent 的语义技能 —— 本体与概念设计。

10 个 [Agent Skills](https://agentskills.io/)，让 Agent 在写代码、跑 CLI、起草规格之前先说清一件东西*意味着什么*：哪个 purpose、哪个粒度、哪份证据。每个技能把协议留在轻薄的 `SKILL.md`，体量大的领域材料放在 `references/`，只在任务需要时加载。

概念设计几个技能改编自 Daniel Jackson 的 concepts 与 synchronizations 模型 —— [The Essence of Software](https://essenceofsoftware.com/)（2021），sync 采用 *Beyond Objects*（[arXiv:2606.27258](https://arxiv.org/abs/2606.27258)）里现行的 when/where/then 记法 —— 面向 Agent 改编，未获作者背书。

English: [README.md](README.md)。

## 目录

- [技能](#技能)
- [安装](#安装)
- [用法](#用法)
- [贡献](#贡献)
- [许可](#许可)

## 技能

### 概念设计

从需求到模块，以概念模型为契约。每个技能停在自己的边界上交棒：`design` → `prd` / `implementation` → `audit`。

| 技能 | 版本 | 做什么 |
| --- | --- | --- |
| [`concept-design`](docs/skills/concept-design.md) | 0.4.0 | 把需求建成 concepts（purpose、operational principle、state、actions），用 sync 组合，给出依赖图与产品子集。停在模型确认——不出 PRD，不出代码 |
| [`concept-prd`](docs/skills/concept-prd.md) | 0.3.0 | 把已确认的模型转录为集中的总体 PRD，加每概念一份共存的 `CONCEPT.md` 与一份按 flow 分节的 `SYNCS.md`。有缺口就退回建模 |
| [`concept-implementation`](docs/skills/concept-implementation.md) | 0.4.0 | 把模型映射为模块单体：一个 concept 一个模块，sync 落在 mediator 或规则引擎，规格与代码共存。带 Rust、Java/Spring Modulith、TypeScript 说明 |
| [`concept-audit`](docs/skills/concept-audit.md) | 0.3.0 | 只读五维审计代码与模型的偏差——漂移、边界、判据、组合、依赖——带严重度校准与修复路由 |
| [`concept-guardrails`](docs/skills/concept-guardrails.md) | 0.27.0 | 仅显式调用；用同目录的 `CONCEPT.md` / `PIPELINE.md` / `SYNCS.md` 声明模块边界并检测规格与代码的漂移。五种模式：audit、concept、pipeline、sync、map |

### 本体与语义

| 技能 | 版本 | 做什么 |
| --- | --- | --- |
| [`semantic-creator`](docs/skills/semantic-creator.md) | 0.5.1 | 把一套接口、CLI 或表做成粒度先行的 Kimball 语义层，经 HTML 决策工作台推进，输出 OKF 或 YAML，每个字段可追溯到观察到的证据 |
| [`semantic-pkm-creator`](docs/skills/semantic-pkm-creator.md) | 0.3.0 | 两轮从原文萃取场景、概念、实体：先扫骨架给人确认，再回填 IPO、分解、组装与八种关系 |

### 华为云

社区维护，非华为云官方。默认只读；报出的每个数字都可追溯到当次 KooCLI/BSS 响应。

| 技能 | 版本 | 做什么 |
| --- | --- | --- |
| [`huawei-cloud-billing-scout`](docs/skills/huawei-cloud-billing-scout.md) | 2.3.9 | 钱已经花到哪了——余额、账单、归因、对账、代金券、储值卡、伙伴账务。53 个只读 BSS 操作出一页简报；拒绝支付、续费、退款、删除 |
| [`huawei-cloud-cost-estimation`](docs/skills/huawei-cloud-cost-estimation.md) | 3.2.4 | 买之前算钱：包年包月与按需报价；白名单创建须先 `--dryrun`、费用复核、显式确认。退订只引导控制台，绝不代执行 |
| [`huawei-cloud-account-onboarding`](docs/skills/huawei-cloud-account-onboarding.md) | 1.0.0 | 只读查实名认证状态，未实名时把人脸二维码渲染到终端并轮询到通过。不收身份证、证件、银行卡与短信码 |

各技能细节与安全边界见 [docs/skills/](docs/skills/)，机器可读索引见 [docs/catalog.yml](docs/catalog.yml)，变更记录在 `qa/<name>/CHANGELOG.md`。

## 安装

需要 Node.js（用 `npx`）；华为云系技能另需 [KooCLI](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html) 7.2+，Agent 不会替你安装。

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill <skill-name> \
  --agent cursor \
  --copy -y
```

`--agent` 可填 `cursor`、`claude-code` 或 `codex`。一次装多个；加 `--global` 装到 `~/.agents/skills/`（Cursor 与 Codex 都会扫描），而不是项目的 `.agents/skills/`：

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-design concept-prd concept-guardrails \
  --agent cursor codex \
  --global --copy -y
```

列出可装技能，或开发时从本地目录安装：

```bash
npx skills add ontology-of-everything/SemanticSkills --list
npx skills add ./skills/<skill-name> --skill <skill-name> --agent cursor --copy -y
```

[Hermes](docs/agents/hermes.md)：`hermes skills install ontology-of-everything/SemanticSkills/<skill-name> -y`。各 Agent 说明：[Cursor](docs/agents/cursor.md) · [Claude Code](docs/agents/claude-code.md) · [Codex](docs/agents/codex.md)。

使用前先读一遍技能内容——技能以你的 Agent 权限运行。

## 用法

技能通常按 description 自动触发，正常说话就够。在 Codex 中 `concept-guardrails` 例外，必须显式指名：

```text
把这个需求建成概念模型                      → concept-design
模型定了，出一份 PRD 规格                   → concept-prd
$concept-guardrails 给 src/orders 写概念规格，然后查漂移
把这套接口做成语义层                        → semantic-creator
3 月华为云为什么扣了这笔                     → huawei-cloud-billing-scout
```

要指名某个技能：Cursor 里用 `/skill-name`，Codex 里用 `$skill-name`。

## 贡献

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

```bash
./tools/skill-scaffold.sh <skill-name>   # 新建技能
./tools/install-git-hooks.sh             # pre-commit → validate-all.sh
./tools/validate-all.sh                  # 全部技能，与 CI 一致
./qa/<skill-name>/validate.sh            # 单个技能
```

`skills/<name>/` 是安装载荷；门禁与 eval 放在 `qa/<name>/`，不随安装分发。每次改技能须同步：`skills/`、`qa/`（`VERSION`、`CHANGELOG.md`）、`docs/catalog.yml`、`docs/skills/<name>.md`。

## 许可

[Apache-2.0](LICENSE) © SemanticSkills contributors。发布到 [ClawHub](https://clawhub.ai/) 的技能包在该平台为 MIT-0；仓库源码仍为 Apache-2.0。
