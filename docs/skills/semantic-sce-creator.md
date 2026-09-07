# 场景-概念-实体萃取

`semantic-sce-creator` · **Semantic SCE Creator — Scene, Concept, Entity Extract**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/semantic-sce-creator/SKILL.md`](../../skills/semantic-sce-creator/SKILL.md)。

**Version:** 0.2.0 · Changelog:
[qa/semantic-sce-creator/CHANGELOG.md](../../qa/semantic-sce-creator/CHANGELOG.md)

## 一句话

按两轮流程把线性原文萃成可调用的场景、概念与实体：先扫骨架等人确认，再回查原文填 IPO、分解、组装与关系。

三层划分灵感来自「人月聊 IT」《三层架构：场景、概念与实体》。

## 三层

| 层 | 角色 |
| --- | --- |
| 概念 | 中枢：可执行动作；IPO 或分解 |
| 实体 | 可指认实例：人 / 工具 / 产品 / 具名框架 |
| 场景 | 组装：问题 + 编排规则，只调用已成立的概念与实体 |

## 安装载荷

```text
skills/semantic-sce-creator/
└── SKILL.md
```

```bash
npx skills add ./skills/semantic-sce-creator \
  --skill semantic-sce-creator \
  --agent cursor \
  --copy
```
