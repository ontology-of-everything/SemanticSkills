# 概念护栏 · wyx 架构护栏中文版

`concept-guardrails` · **Concept Guardrails — wyx Architecture Guardrails (Chinese)**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-guardrails/SKILL.md`](../../skills/concept-guardrails/SKILL.md)。

**Version:** 0.28.0 · Changelog:
[qa/concept-guardrails/CHANGELOG.md](../../qa/concept-guardrails/CHANGELOG.md)

## 一句话

把模块边界写成放在代码旁边的规格（`CONCEPT.md` / `PIPELINE.md` / `SYNCS.md`），让 agent 动手前就看见边界，并能定期核对规格是否已和代码脱节。

## 启用方式

本技能在 Codex 中默认不参与自动选择，需用 `$concept-guardrails` 显式启用；在其他客户端使用对应的手动技能调用语法。
下文的可选 hooks 运行时也不会随技能自动开启。

## 适用场景

- agent 反复伸手进别的模块内部（直接 import 仓储、绕过 service API），需要把边界固化下来。
- 项目已经有一批模块，但没人说得清谁拥有哪份状态、谁能读谁的数据。
- 文档与实现悄悄分叉，需要一次能给出严重度分级的规格-代码核对。
- 数据流程的质量假设只存在于口头（「这里不会有 null」），需要写成可断言的不变量。
- 需要一张能反映真实依赖的架构图，而不是手画后就过时的图。

## 六种模式

| 模式 | 产出 | 说明 |
| --- | --- | --- |
| `wyx:audit` | 行动计划 | 只读扫描覆盖缺口，按依赖顺序输出该跑哪些命令 |
| `wyx:concept` | `CONCEPT.md` | 回填存量模块 / 设计新模块 / 发现概念候选 |
| `wyx:concept drift` | 漂移报告 | 逐份规格核对 + 跨规格引用校验 + 系统性模式聚合 |
| `wyx:pipeline` | `PIPELINE.md` | 数据来源、阶段、输出与可运行断言的不变量 |
| `wyx:sync` | `SYNCS.md` | 跨概念协调的触发时机、数据流向、错误策略 |
| `wyx:map` | `ARCHITECTURE.md` | 从全部规格合成 Mermaid 关系图与依赖矩阵 |

## 与上游的差异

本技能是 [jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0 的中文改写版，遵循上游 MIT 许可（`skills/concept-guardrails/LICENSE.upstream`）。本次适配同时修正语义与执行规则：

- 六种模式共用授权、落位与交付约定，保留显式启用策略。
- Jackson 新建采用四节和因果规则；已有原生格式按文件识别，完整迁移才切换。
- 地图解析 when/where/then，保留联合触发；产品依赖不从同步边推导。
- 审计按证据与实际影响校准，不因耦合已记录就掩盖风险；只读检查不写历史。
- `runtime/` 脚本仍原样保留，只注入旧边界段；Jackson 规格需主动读取，不能宣称自动解析兼容。

## 与 concept-* 其他技能的分工

| 用户要的是 | 用 |
| --- | --- |
| 哪些模块还没规格（覆盖审计） | 本技能 `wyx:audit` |
| 对照概念模型审计代码：独立性、组合缺陷、五维度 | `concept-audit`（漂移检查表与本技能同源） |
| 为存量代码回填规格、改单个模块规格、查单模块漂移 | 本技能 `wyx:concept` / `wyx:concept drift` |
| 从需求设计新概念、拆边界 | `concept-design` → `concept-prd` |

## 边界自动注入（可选）

规格与漂移流程与 agent 无关，任何 agent 都能执行。上游那套「每次写入前后自动把边界送进上下文」的机制依赖 Claude Code hooks 与 `jq`，接线方式见 [`references/hooks-runtime.md`](../../skills/concept-guardrails/references/hooks-runtime.md)：

```bash
claude --plugin-dir /绝对路径/skills/concept-guardrails/runtime
```

注意它只匹配 Write / Edit / NotebookEdit；经由 Bash（`sed -i`、`echo >`）或 MCP 写入工具的改动会完全绕过它，而且它是建议性的，不阻断写入。

## 安装载荷

```text
skills/concept-guardrails/
├── SKILL.md
├── LICENSE.upstream
├── agents/openai.yaml
├── references/
│   ├── audit.md
│   ├── concept.md
│   ├── drift-detection.md
│   ├── hooks-runtime.md
│   ├── map.md
│   ├── pipeline.md
│   └── sync.md
└── runtime/
    ├── .claude-plugin/plugin.json
    ├── hooks/hooks.json
    └── scripts/
        ├── drift-context.sh
        ├── post-check.sh
        └── session-start.sh
```

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill concept-guardrails \
  --agent cursor \
  --copy -y
```

Local checkout:

```bash
npx skills add ./skills/concept-guardrails \
  --skill concept-guardrails \
  --agent cursor \
  --copy -y
```

## Marketplaces

- [skills.sh](https://skills.sh/ontology-of-everything/SemanticSkills/concept-guardrails)
- [SkillsMP](https://skillsmp.com/) — repo topics `claude-skills`, `claude-code-skill`
- [ClawHub](https://clawhub.ai/agenticweb4/concept-guardrails)

## 来源

- **WYSIWID** —— Eagon Meng & Daniel Jackson, "What You See Is What It Does"（MIT, Onward! 2025）。
- **WYWIWID** —— Dr. Ernie, "What You Write Is What It Did"。

## 2026-09-07 修订

统一 Jackson/wyx 消费规则；修复地图遗漏与新鲜度、只读历史冲突、重复授权及严重度；压缩共用流程。

依据与检索边界见[研究记录](../references/jackson/2026-09-07-concept-research.md)。
