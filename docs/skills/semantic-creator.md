# 语义创建器（元技能）

`semantic-creator` · **Semantic Creator — Interface to Governed Semantic Layer (Meta-Skill)**

把一份**接口契约**（REST/OpenAPI、CLI 帮助、或数据表/DDL）建成受治理的
Kimball 语义层：访谈锁事实与粒度 → **交互式 HTML 决策工作台**通过固定
YAGNI 指导确认目标、候选、证据、风险、依赖与权衡 → 按 Schema 生成。默认
输出 **Google OKF v0.1** bundle，可选仓库 Kimball 星型 YAML / markdown。
唯一真源是用户给的接口——**不臆造**字段、粒度、枚举或取值。

> **元技能** · 它生产的是「别的领域的语义层」，本身不连任何云或数据库。

**Version:** 0.5.1 · Changelog:
[qa/semantic-creator/CHANGELOG.md](../../qa/semantic-creator/CHANGELOG.md)

## What it does

| Capability | Typical questions |
| --- | --- |
| Ingest interface | 把 REST/OpenAPI、CLI help、表/DDL 归一成操作清单 |
| Interview facts & grain | 「一行 = 什么」？锁定可证伪的 grain |
| Model dimensions / measures | conformed / snowflake / degenerate；additivity + 口径 |
| Decision review | HTML 决策工作台：四类固定判断提示 + 原子决定、候选、证据、风险与关系；显式确认后才 Emit |
| Routing & boundary | entry_points 与 evidence_boundary（不能回答什么） |
| Emit | Google OKF v0.1 bundle（**默认**）；仓库 Kimball 星型 YAML / markdown（可选）；≥2 bundle 生成薄根索引 |
| Out of scope | 不臆造接口未给的字段/枚举/取值；写操作只 frame 不擅自建模 |

## In-skill flow

```text
Interface (REST / CLI / table)
     │
     ▼
Phase 1 · Ingest ── 操作清单 → fact | dimension-lookup（退出条件达成才前进）
     │
     ▼
Phase 2 · Review ── 决策建模（证据/风险/关系）→ HTML 工作台 → 显式行动 → amendments.md → 批准
     │
     ▼
Phase 3 · Emit ── OKF bundle（默认，emit-okf）| repo-YAML（可选，emit-yaml）
     │
     ▼
Phase 4 · Verify ── 结构检查 + 语义 lint + OKF 硬约束；不可机械修复 → 回 Phase 2 提问
```

## SKILL.md structure

| Section | Purpose |
| --- | --- |
| Workflow | 四阶段串行，每阶段一个参考文件 + 退出条件 |
| Critical Rules | Evidence-only；grain first；one blocking ask；layer split；stable names；decision gate（默认 pending） |
| Reference Index | 按阶段加载 ingest / review / emit-okf / emit-yaml / verify / examples |

## Runtime bundle (install payload)

```text
skills/semantic-creator/
├── SKILL.md
├── assets/
│   └── review-template.html   # Phase 2 决策工作台壳（内联渲染器，离线无 CDN）
└── references/
    ├── ingest.md      # Phase 1：物料归一 + 角色判定
    ├── review.md      # Phase 2：决策本体 + HTML 工作台 + amendments 迭代
    ├── emit-okf.md    # Phase 3 默认目标：OKF v0.1 布局/映射
    ├── emit-yaml.md   # Phase 3 可选目标：YAML Schema + 共享字段语义
    ├── verify.md      # Phase 4：结构检查 + 语义 lint + OKF 硬约束 + 升级回路
    └── examples.md    # 四阶段端到端样例
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`.

## QA (not installed with skill)

```text
qa/semantic-creator/
├── validate.sh
├── VERSION
├── .markdownlint.json
├── evals/evals.json             # 6 offline eval cases
└── assertions/README.md
```

```bash
./qa/semantic-creator/validate.sh
```

## Install

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill semantic-creator \
  --agent cursor \
  --copy -y
```

No external tools or network required — pure modeling and file generation; the review report is a self-contained HTML file (inline CSS/JS, no CDN).
