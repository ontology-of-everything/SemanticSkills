# 概念设计

`concept-design` · **Concept Design**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-design/SKILL.md`](../../skills/concept-design/SKILL.md)。

**Version:** 0.5.0 · Changelog:
[qa/concept-design/CHANGELOG.md](../../qa/concept-design/CHANGELOG.md)

## 一句话

把需求转成由独立 concepts 和 synchronizations 组成的概念模型：每个 concept 都用单一 Purpose、端到端 Operational Principle、最小 State 与完整 Actions 定义。模型确认后，文档化用 `concept-prd`，代码落地用 `concept-implementation`，存量审计用 `concept-audit`。

## 适用场景

- 需求还停留在功能、页面或实体清单，需要找到用户真正要掌握的功能单元。
- 已有概念模型出现边界糊模、功能碎片、交叉依赖或命名陌生。
- 需要在进入 PRD、架构或代码前，先确认用户面向的心理模型和行为边界。

## 方法

1. 从受益者、misfit、现有做法和期望结果开始，追问功能背后的需要。
2. 识别有独立目的的候选 concepts，而不把表、页面、实体名或团队边界直接映射成 concepts。
3. 用 Purpose、Operational Principle、关系式 State、带错误 case 与只读 queries 的 Actions 刻画每个 concept；规格四节零点名其他概念，使用上下文备注只进可选的 notes 段。
4. 用专一、完整、独立、熟悉审查边界，并用 split/merge、unify/specialize、tighten/loosen 调整。
5. 把跨 concept 行为写成 when / where / then 因果 sync（基于作者因果语义的本仓记法，书版事务语义已废弃；外部请求具体化为 Requesting 动作、错误由错误 sync 匹配），按 flow 分组并画同步图，再按 Parnas 依赖图圈定 MVP；按用户请求范围交付或继续交接。

## 安装载荷

```text
skills/concept-design/
├── SKILL.md                       # 目标 / 原则 / 流程 / 命题 / 记法与模板 / 参考
├── agents/openai.yaml
└── references/
    ├── criteria.md                # 流程第 4 步：资格五条、四词、误判速查、design moves
    ├── sync-notation.md           # 流程第 5 步：sync 记法、因果语义、信号、依赖图
    ├── example-reserving.md       # 填好的 Beyond Objects 餐厅订位例
    └── sources.md                 # 作者原文与取用原则
```

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-design \
  --agent cursor \
  --copy -y
```

Local checkout:

```bash
npx skills add ./skills/concept-design \
  --skill concept-design \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills/concept-design)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`
- [ClawHub](https://clawhub.ai/agenticweb4/concept-design)

## 2026-09-07 修订

区分论文语义与本仓方言；修复 flow、绑定、查询空集与同步图；压缩模板并重写订位教学例。

依据与检索边界见[研究记录](../references/jackson/2026-09-07-concept-research.md)。
