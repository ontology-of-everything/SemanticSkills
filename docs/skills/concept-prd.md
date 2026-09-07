# 概念 PRD

`concept-prd` · **Concept PRD**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-prd/SKILL.md`](../../skills/concept-prd/SKILL.md)。

**Version:** 0.3.0 · Changelog:
[qa/concept-prd/CHANGELOG.md](../../qa/concept-prd/CHANGELOG.md)

## 一句话

把已确认的概念模型转录为 PRD 文档族：总体 PRD 集中，每概念一份 wyx 兼容的 CONCEPT.md（模块目录存在时与代码共存），全部 sync 单文件 SYNCS.md 按 flow 分节。只转录，不发明。

## 适用场景

- 概念模型已确认，需要可导航、可验收的规格文档。
- 后续要按概念独立验证，或按 flow 看出欠同步与过同步。
- 发现模型缺口时应回到 `concept-design`，而不是在文档里填补。

## 方法

1. 总体 PRD 收录需求与 misfits、概念索引、依赖图与排除项——依赖信息只在这里，不进概念规格。
2. 每概念一份 CONCEPT.md，四节零点名其他概念（可选 notes 段放上下文备注）；验收场景由 OP 的 after/then 场景机械导出。
3. sync 转录期单文件、带 coordination graph、按 flow 聚合不按域分节（实现期 syncs 拆包时由实现技能按 flow 群随包拆分）；文件名与段落头与 wyx 架构护栏兼容，可被 `wyx:concept drift` / `wyx:map` 直接消费。
4. 不写代码；落地用 `concept-implementation`。

## 安装载荷

```text
skills/concept-prd/
├── SKILL.md                 # 目标 / 原则 / 流程 / 命题 / 记法与模板 / 参考
├── agents/openai.yaml
└── references/
    ├── templates.md         # CONCEPT.md 与 SYNCS.md 模板
    └── sources.md           # 取用原则的出处
```

```bash
npx skills add ./skills/concept-prd \
  --skill concept-prd \
  --agent codex \
  --copy
```
