# 概念 PRD

`concept-prd` · **Concept PRD**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-prd/SKILL.md`](../../skills/concept-prd/SKILL.md)。

**Version:** 0.5.0 · Changelog:
[qa/concept-prd/CHANGELOG.md](../../qa/concept-prd/CHANGELOG.md)

## 一句话

把已确认的概念模型转录为 PRD 文档族：总体 PRD 集中，每概念一份 Jackson 格式的 CONCEPT.md（模块目录存在时与代码共存），全部 sync 单文件 SYNCS.md 按 flow 分组。只转录，不发明。

## 启用方式

本技能默认不自动启动。Cursor 用 `/concept-prd`，Codex 用 `$concept-prd`。

## 适用场景

- 概念模型已确认，需要可导航、可验收的规格文档。
- 后续要按概念独立验证，或按 flow 看出欠同步与过同步。
- 发现模型缺口时应回到 `concept-design`，而不是在文档里填补。

## 方法

1. 总体 PRD 收录需求与 misfits、概念索引、依赖图与排除项——依赖信息只在这里，不进概念规格。
2. 每概念一份 CONCEPT.md，四节零点名其他概念（可选 notes 段放上下文备注）；代表性验收来自 OP，边界验收来自 actions/state。
3. sync 转录期单文件、同步图只在总体 PRD 派生、按 flow 聚合不按域分节（实现期 syncs 拆包时由实现技能按 flow 群随包拆分）；由护栏按 Jackson 方言解析，可被 `concept-guardrails` 的 `drift` / `map` 模式直接消费。
4. 不写代码；落地用 `concept-implementation`。

## 安装载荷

```text
skills/concept-prd/
├── SKILL.md                 # 目标 / 原则 / 流程 / 命题 / 记法与模板 / 参考
├── agents/openai.yaml
└── references/
    ├── templates.md         # CONCEPT.md / SYNCS.md 模板（Beyond Objects 记法）
    ├── example-reserving.md # 填好的餐厅订位例（转录后的文件形态）
    └── sources.md           # 取用原则的出处
```

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-prd \
  --agent cursor \
  --copy -y
```

Local checkout:

```bash
npx skills add ./skills/concept-prd \
  --skill concept-prd \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills/concept-prd)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`
- [ClawHub](https://clawhub.ai/agenticweb4/concept-prd)

## 2026-09-07 修订

明确权威规格与增量编辑；修复验收追溯、错误查询和文件格式；压缩重复示例。

依据与检索边界见[研究记录](../references/jackson/2026-09-07-concept-research.md)。
