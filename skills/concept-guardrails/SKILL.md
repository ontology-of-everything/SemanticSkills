---
name: concept-guardrails
description: Run wyx spec guardrails only when the user explicitly invokes $concept-guardrails. / 仅在用户显式调用 $concept-guardrails 时运行 wyx 规格护栏。
compatibility: 只需读写文件与 Grep/Glob；可选的边界注入运行时需要 Claude Code hooks 与 jq。
metadata:
  author: ontology-of-everything
  version: "0.28.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/concept-guardrails
---

# 概念护栏

把模块边界声明为共存规格，核对规格与代码，派生架构地图。源自 [jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0（MIT，见 `LICENSE.upstream`）；本文适配了 Jackson 记法与执行流程，运行时脚本仍保留上游版本。仅在用户显式调用 `$concept-guardrails` 时运行。

## 选择模式

| 模式 | 任务与产出 | 执行前读 |
| --- | --- | --- |
| `wyx:audit` | 覆盖审计，输出补规格的行动计划；只读 | [audit.md](references/audit.md) |
| `wyx:concept` | 回填或更新模块的 `CONCEPT.md` | [concept.md](references/concept.md) |
| `wyx:concept drift` | 对照规格与代码，输出漂移报告；只读 | [drift-detection.md](references/drift-detection.md) |
| `wyx:pipeline` | 数据阶段、质量不变量与 `PIPELINE.md` | [pipeline.md](references/pipeline.md) |
| `wyx:sync` | 跨概念协调与 `SYNCS.md` | [sync.md](references/sync.md) |
| `wyx:map` | 派生 `ARCHITECTURE.md` | [map.md](references/map.md) |

未指定模块且没有规格时先做覆盖审计。需求拆分用 `concept-design`；已确认模型批量转录用 `concept-prd`；全面独立性与组合审计用 `concept-audit`。伴生技能未安装时报告缺口与交接内容，不假定其文件可读。

## 共用执行约定

- 先读已有规格、实现与项目约定。回填描述现状，并单列缺陷；更新既有模块时先改规格再改实现。
- 写规格前呈现草案或 diff。用户已授权创建、更新或修复时直接完成；只有模型取舍未定或写入超出授权时才请求确认。只读审计不写历史文件，也不自动修复。
- `CONCEPT.md` 放所属模块，`PIPELINE.md` 与所属概念共目录；跨模块管道放组合层。避免根目录概念规格成为无关模块的兜底边界。
- 每个概念一份权威规格；每个 syncs 包一份 `SYNCS.md`，按 flow 归组、保持规则可追踪。规格变化且已有地图时，指出需运行 `wyx:map`；已要求更新地图则一并完成。

## 记法与兼容

先识别现有格式，再选择消费者规则。新建采用 Jackson 方言；保留已有 wyx 原生格式，迁移时处理完整文档族，不能只改标题。混合仓库按文件识别并报告迁移边界。

| 内容 | Jackson 方言（concept-*） | wyx 原生兼容 |
| --- | --- | --- |
| 概念 | `purpose / principle / state / actions`，可选 `notes`；类型参数抽象上下文，定义不依赖其他概念 | 可含 `operational principle`、`interactions / dependencies / known coupling` |
| 组合 | `app / include / sync`；`when / where / then`，`// flow:` 分组 | `dispatching`、`coordination graph` 与 `## sync:` 条目 |
| 图 | 从 sync 块派生同步图；产品依赖以总体 PRD 为准 | 从既有协调图和边界段提取，分别标注关系类型 |
| hooks | 列规格，但不解析四节或 sync；必须主动读规格 | 注入 interactions / dependencies；管道注入 data boundary |

`principle` 与 `operational principle` 表示同一术语；新写用前者，读取兼容后者。所谓“零点名”检查的是语义依赖：局部类型参数恰好名为 User 不算引用 User 概念。

## 完成条件

产出符合所选模式、方言与授权；位置和引用有效；回填未把现有缺陷合理化。报告注明扫描范围、未核实项和修复方向。地图按来源重建，不能凭时间戳宣称语义最新。

需要自动注入时读 [hooks-runtime.md](references/hooks-runtime.md)；hooks 是可选提示层，不是边界验证器。
