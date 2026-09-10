# 概念护栏

`concept-guardrails` · **Concept Guardrails**

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-guardrails/SKILL.md`](../../skills/concept-guardrails/SKILL.md)。

**Version:** 0.30.0 · Changelog:
[qa/concept-guardrails/CHANGELOG.md](../../qa/concept-guardrails/CHANGELOG.md)

## 一句话

把模块边界写成放在代码旁边的规格（`CONCEPT.md` / `PIPELINE.md` / `SYNCS.md`），让 agent 动手前就看见边界，并能定期核对规格是否已和代码脱节。

## 启用方式

本技能默认不自动启动。Cursor 用 `/concept-guardrails`，Codex 用 `$concept-guardrails`，后接模式与参数：

```text
$concept-guardrails audit
$concept-guardrails concept src/orders/
$concept-guardrails drift src/
$concept-guardrails map
```

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
| `audit` | 行动计划 | 只读扫描覆盖缺口，按依赖顺序输出该跑哪些命令；未指定模式或项目尚无规格时默认走这里 |
| `concept` | `CONCEPT.md` | 路径→回填存量模块；描述→新建；无参数→只列概念候选 |
| `drift` | 漂移报告 | 逐份规格核对 + 跨规格引用校验 + 系统性模式聚合 |
| `pipeline` | `PIPELINE.md` | 数据来源、阶段、输出与可运行断言的不变量 |
| `sync` | `SYNCS.md` | 跨概念协调的 when / where / then、绑定与错误分支 |
| `map` | `ARCHITECTURE.md` | 从全部规格合成 Mermaid 关系图与依赖矩阵 |

## 记法：只有 Jackson 方言

本技能只消费和产出与 `concept-design` / `concept-prd` 相同的记法：`CONCEPT.md` 四节（purpose / principle / state / actions）、`SYNCS.md` 的 `app / include / sync` 与 `when / where / then`、`PIPELINE.md` 的来源 / 阶段 / 不变量 / data boundary。

不消费 wyx 原生格式（`## interactions` / `## dependencies` / `## known coupling` / `## dispatching` / `## coordination graph` / `## sync:`）。遇到这些段落时，审计、漂移与地图都把该文件标为「待迁移」，不纳入检查与建图；用户授权后按本记法整份重写，不做部分修改。

## 与上游的差异

流程改编自 [jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0，遵循上游 MIT 许可（`skills/concept-guardrails/LICENSE.upstream`）：

- 上游五个斜杠命令合并为本技能的六种模式，共用授权、落位与交付约定，显式调用。
- 记法改为 Jackson 方言，不再兼容上游原生格式（见上节）。
- 地图解析 when/where/then，保留联合触发；产品依赖只取自总体 PRD，不从同步边推导。
- 审计按证据与实际影响校准，不因耦合已记录就掩盖风险；只读检查不写历史。
- `runtime/` 脚本原样保留，但它只认旧边界段：对本记法只能列规格、注入 `PIPELINE.md` 的 data boundary。

## 与 concept-* 其他技能的分工

| 用户要的是 | 用 |
| --- | --- |
| 哪些模块还没规格（覆盖审计） | 本技能 `audit` |
| 对照概念模型审计代码：独立性、组合缺陷、五维度 | `concept-audit`（漂移检查表与本技能同源） |
| 为存量代码回填规格、改单个模块规格、查规格漂移 | 本技能 `concept` / `drift` |
| 从需求设计新概念、拆边界 | `concept-design` → `concept-prd` |

## 边界自动注入（可选）

规格与漂移流程与 agent 无关，任何 agent 都能执行。上游那套「每次写入前后自动把边界送进上下文」的机制依赖 Claude Code hooks 与 `jq`，接线方式见 [`references/hooks-runtime.md`](../../skills/concept-guardrails/references/hooks-runtime.md)：

```bash
claude --plugin-dir /绝对路径/skills/concept-guardrails/runtime
```

注意它只匹配 Write / Edit / NotebookEdit；经由 Bash（`sed -i`、`echo >`）或 MCP 写入工具的改动会完全绕过它，而且它是建议性的，不阻断写入。对本记法的 `CONCEPT.md` / `SYNCS.md` 它注入不了边界，只列出文件。

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

## 2026-09-10 修订

模式名去掉 `wyx:` 前缀，改为 `$concept-guardrails <模式>`；`drift` 独立成模式；只保留 Jackson 记法，wyx 原生格式改为标记待迁移；补齐回填 / 新建 / 发现子模式与无参数路由。

## 2026-09-07 修订

统一 Jackson/wyx 消费规则；修复地图遗漏与新鲜度、只读历史冲突、重复授权及严重度；压缩共用流程。

依据与检索边界见[研究记录](../references/jackson/2026-09-07-concept-research.md)。
