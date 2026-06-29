# 语义创建器（元技能）

`semantic-creator` · **Semantic Creator — Interface to Governed Semantic Layer (Meta-Skill)**

把一份**接口契约**（REST/OpenAPI、CLI 帮助、或数据表/DDL）通过**逐项确认**的引导式访谈，建成受治理的 Kimball 语义层：先锁事实与粒度，再挂维度与度量，最后按 Schema 生成语义对象。输出本仓 YAML 或 markdown，并可导出 **Google OKF v0.1**（推荐）。唯一真源是用户给的接口——**不臆造**字段、粒度、枚举或取值。

> **元技能** · 它生产的是「别的领域的语义层」，本身不连任何云或数据库。

**Version:** 0.1.1 · Changelog: [qa/semantic-creator/CHANGELOG.md](../../qa/semantic-creator/CHANGELOG.md)

## What it does

| Capability | Typical questions |
| --- | --- |
| Ingest interface | 把 REST/OpenAPI、CLI help、表/DDL 归一成操作清单 |
| Confirm facts & grain | 「一行 = 什么」？锁定可证伪的 grain |
| Model dimensions | conformed / snowflake / scope / degenerate / abstract / encoded_constant |
| Model measures | 可加性（additive / semi / non-additive）+ 口径 |
| Routing & boundary | entry_points 与 evidence_boundary（不能回答什么） |
| Emit | 本仓 Kimball YAML / markdown / **Google OKF v0.1（推荐）** |
| Out of scope | 不臆造接口未给的字段/枚举/取值；写操作只 frame 不擅自建模 |

## In-skill flow

```text
Interface (REST / CLI / table)
     │
     ▼
Phase 1 · Ingest ── 操作清单（name/method/safety/inputs/outputs/doc）
     │
     ▼
Phase 1 · Frame ── fact | dimension-lookup | scope（按 fact·dimension·measure·time·scope 路由）
     │
     ▼
Phase 2 · Confirm ── 一次一问，逐步回显小表：Facts&Grain → Dimensions → Measures → Selection/Pairing → Routing/Boundary
     │
     ▼
Phase 3 · Emit ── 按 schema-spec 生成；okf-emitter 导出 OKF；跑 Conformance
```

## SKILL.md structure

| Section | Purpose |
| --- | --- |
| Workflow | Phase 1 Ingest & Frame → Phase 2 Confirm（逐项）→ Phase 3 Emit |
| Critical Rules | Evidence-only；grain first；one blocking ask；layer split；stable names |
| Reference Index | 何时加载 playbook / schema-spec / okf-emitter / examples |

## Runtime bundle (install payload)

```text
skills/semantic-creator/
├── SKILL.md
└── references/
    ├── elicitation-playbook.md   # 抽取规则 + 确认顺序 + 检查表
    ├── schema-spec.md            # 语义对象 Schema 约束 + Conformance
    ├── okf-emitter.md            # Google OKF v0.1 映射 + 硬约束
    └── examples.md               # 接口 → 确认 → YAML + OKF 端到端样例
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`.

## QA (not installed with skill)

```text
qa/semantic-creator/
├── validate.sh
├── VERSION
├── .markdownlint.json
├── evals/evals.json             # 5 offline eval cases
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

No external tools or network required — pure modeling and file generation.
