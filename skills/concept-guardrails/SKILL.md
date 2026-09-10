---
name: concept-guardrails
description: Run concept-spec guardrails (audit, concept, drift, pipeline, sync, map) only when the user explicitly invokes $concept-guardrails. / 仅在用户显式调用 $concept-guardrails 时运行概念规格护栏。
compatibility: 只需读写文件与 Grep/Glob；可选的边界注入运行时需要 Claude Code hooks 与 jq。
metadata:
  author: ontology-of-everything
  version: "0.30.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/concept-guardrails
---

# 概念护栏

把模块边界声明为与代码共存的规格，核对规格与代码，派生架构地图。流程源自 [jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0（MIT，见 `LICENSE.upstream`），记法改为本仓 Jackson 方言，`runtime/` 脚本保留上游版本。仅在用户显式调用 `$concept-guardrails` 时运行。

## 选择模式

调用形式 `$concept-guardrails <模式> [路径或描述]`。

| 模式 | 任务与产出 | 执行前读 |
| --- | --- | --- |
| `audit` | 覆盖审计：列已有规格、候选与按依赖排序的命令计划；只读 | [audit.md](references/audit.md) |
| `concept` | 回填 / 新建 / 发现概念候选，产出 `CONCEPT.md` | [concept.md](references/concept.md) |
| `drift` | 对照三类规格与代码，输出漂移报告；只读 | [drift-detection.md](references/drift-detection.md) |
| `pipeline` | 回填 / 新建 / 发现数据管道，产出 `PIPELINE.md` | [pipeline.md](references/pipeline.md) |
| `sync` | 回填 / 新建 / 发现跨概念协调，产出 `SYNCS.md` | [sync.md](references/sync.md) |
| `map` | 从全部规格派生 `ARCHITECTURE.md` | [map.md](references/map.md) |

参数路由：路径 → 回填；描述 → 新建；无参数 → 该模式的发现子模式（只列候选，不写规格）。未指定模式、或项目尚无任何规格时走 `audit`。需求拆分用 `concept-design`；已确认模型批量转录用 `concept-prd`；全面独立性与组合审计用 `concept-audit`。伴生技能未安装时报告缺口与交接内容，不假定其文件可读。

## 共用执行约定

- 先读已有规格、实现与项目约定。回填描述现状，并单列缺陷；更新既有模块时先改规格再改实现。
- 写规格前呈现草案或 diff。用户已授权创建、更新或修复时直接完成；只有模型取舍未定或写入超出授权时才请求确认。只读审计不写历史文件，也不自动修复。
- `CONCEPT.md` 放所属模块，`PIPELINE.md` 与所属概念共目录；跨模块管道放组合层。避免根目录概念规格成为无关模块的兜底边界。
- 每个概念一份权威规格；每个 syncs 包一份 `SYNCS.md`，按 flow 归组、保持规则可追踪。规格变化且已有地图时，指出需运行 `map`；已要求更新地图则一并完成。

## 记法

只消费和产出本仓 Jackson 方言，与 `concept-design` / `concept-prd` 一致：

| 内容 | 记法 |
| --- | --- |
| 概念 | `purpose / principle / state / actions`，可选 `notes`；类型参数抽象上下文，四节不依赖其他概念定义 |
| 组合 | `app / include / sync`；`when / where / then`，`// flow:` 分组；跨概念边只在 `SYNCS.md` |
| 管道 | `purpose / sources / stages / outputs / invariants / triggers / data boundary` |
| 图 | 从 `sync` 块派生同步图；产品依赖以总体 PRD 为准，不从 sync 推导 |

`principle` 与 `operational principle` 是同一术语；新写用前者，读取兼容后者。所谓"零点名"检查的是语义依赖：局部类型参数恰好名为 User 不算引用 User 概念。

不消费 wyx 原生格式。遇到 `## interactions` / `## dependencies` / `## known coupling` / `## dispatching` / `## coordination graph` / `## sync:` 等旧段落，标为待迁移并报告；用户授权迁移时按本记法重写整份文档族（CONCEPT、SYNCS、PIPELINE 一起），逐条保留触发、绑定、效果与错误路径，不能只改标题或混写两种格式。

## 完成条件

产出符合所选模式、记法与授权；位置和引用有效；回填未把现有缺陷合理化。报告注明扫描范围、未核实项和修复方向。地图按来源重建，不能凭时间戳宣称语义最新。

需要自动注入时读 [hooks-runtime.md](references/hooks-runtime.md)；hooks 是可选提示层，只能列规格与注入 `PIPELINE.md` 的 data boundary，不解析四节或 sync，不是边界验证器。
