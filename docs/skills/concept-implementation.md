# 概念实现 · 模块单体

`concept-implementation` · **Concept Implementation — Modular Monolith**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-implementation/SKILL.md`](../../skills/concept-implementation/SKILL.md)。

**Version:** 0.6.0 · Changelog:
[qa/concept-implementation/CHANGELOG.md](../../qa/concept-implementation/CHANGELOG.md)

## 一句话

把已确认的概念模型映射为模块单体：一个 concept 一个模块，sync 落在组合层（mediator 或规则引擎），产品依赖图用于验证裁剪条件，实际构建另行检查。

## 启用方式

本技能默认不自动启动。Cursor 用 `/concept-implementation`，Codex 用 `$concept-implementation`。

## 适用场景

- 概念模型已确认，需要代码结构而不是再讨论边界。
- 目标是模块单体 + 端口-适配器，而不是按页面或表结构拆服务。
- 语言细节按需加载：Rust、Java/Spring Modulith、TypeScript。

## 方法

1. 概念模块互不引用；数据与控制流只经组合层。
2. 默认过程式 mediator；行为规则多或需要动作溯源时再选规则引擎。sync 语义为因果规则（when/where/then），错误 sync 是默认失败路径，共享事务仅在契约允许且副作用可控时使用，不能替代错误处理。
3. 对外 API 只暴露应用动作（Requesting 触发的 sync），不直通概念动作。
4. 规格共存落位（模块目录 CONCEPT.md、syncs 目录 SYNCS.md），此后规格先行；边界规则固化为架构看护测试并进入 CI。概念边界有疑问回 `concept-design`。
5. 概念多时按概念分组（俗称分域）扩展：纯工程组织、无架构语义，零引用铁律平坦生效；syncs 按 flow 群拆包，跨组 flow 归入口 Requesting 动作所在组，SYNCS.md 随包走。

## 安装载荷

```text
skills/concept-implementation/
├── SKILL.md                     # 目标 / 原则 / 流程 / 命题 / 记法与模板 / 参考
├── agents/openai.yaml
└── references/
    ├── composition-layer.md     # sync 落地路线、时机与错误隔离、接口层、失败路径、规格共存
    ├── scaling.md               # 概念分组与 syncs 拆包（十余个概念起）
    ├── rust.md
    ├── java-spring.md
    ├── typescript.md
    └── sources.md               # 取用原则的出处
```

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-implementation \
  --agent cursor \
  --copy -y
```

Local checkout:

```bash
npx skills add ./skills/concept-implementation \
  --skill concept-implementation \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills/concept-implementation)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`
- [ClawHub](https://clawhub.ai/agenticweb4/concept-implementation)

## 2026-09-07 修订

修复事务/错误处理、完成事件与并发隔离；纠正 Spring Modulith 与 Cargo 边界检查说明。

依据与检索边界见[研究记录](../references/jackson/2026-09-07-concept-research.md)。
