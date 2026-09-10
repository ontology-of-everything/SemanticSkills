# 概念审计

`concept-audit` · **Concept Audit**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-audit/SKILL.md`](../../skills/concept-audit/SKILL.md)。

**Version:** 0.5.0 · Changelog:
[qa/concept-audit/CHANGELOG.md](../../qa/concept-audit/CHANGELOG.md)

## 一句话

只读对照概念模型（或 PRD 文档族）与代码，回答两个主问题——**概念是否真独立**、**概念的组合是否有缺陷**——再加规格漂移、判据重审、依赖与子集，五维给出带证据的发现，并路由到 design / prd / implementation 修复。

## 启用方式

本技能默认不自动启动。Cursor 用 `/concept-audit`，Codex 用 `$concept-audit`。

## 适用场景

- 已有概念模型或 PRD，需要核对应代码是否仍一一对应。
- 模块互引、共享表、DTO 进概念签名等边界问题需要定位，而不是立刻改代码。
- 持续看护已由 CI 架构测试承担，需要一次周期或按需的人工审计。

## 方法

1. 定位规格（与代码共存的 CONCEPT.md / SYNCS.md 加 `docs/prd/`）与工程自带的模块/依赖图素材。
2. 规格漂移按校准过的检查表逐类别对账（默认类别与实际影响共同校准）；规格多时可分批或委派只读检查。
3. 独立性：每个概念模块查互引、共享表、DTO 进签名、规格点名其他概念。
4. 组合缺陷：对 SYNCS.md 与组合层代码过组合缺陷检查表——行为保持违规、缺错误 sync、入口无响应、冲突 / 死 sync、级联无界、欠 / 过同步、sync 自有业务状态、直通概念动作等。
5. 跨规格校验 sync 引用、系统性模式聚合、跨维度合并根因，修复顺序上游优先。
6. 全程只读，不修改任何文件。

## 安装载荷

```text
skills/concept-audit/
├── SKILL.md                         # 目标 / 原则 / 流程 / 命题 / 记法与模板 / 参考
├── agents/openai.yaml
└── references/
    ├── drift-checklist.md           # 漂移检查表、严重度校准、并行扫描
    ├── composition-checklist.md     # 组合缺陷检查表
    └── sources.md                   # 取用原则的出处
```

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-audit \
  --agent cursor \
  --copy -y
```

Local checkout:

```bash
npx skills add ./skills/concept-audit \
  --skill concept-audit \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills/concept-audit)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`
- [ClawHub](https://clawhub.ai/agenticweb4/concept-audit)

## 2026-09-07 修订

审计按行为与影响判定；补充绑定/合取/重放检查，消除合法循环、日志与组织方式误报。

依据与检索边界见[研究记录](../references/jackson/2026-09-07-concept-research.md)。
