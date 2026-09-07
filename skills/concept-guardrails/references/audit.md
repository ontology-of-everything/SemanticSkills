# 项目审计与命令规划（wyx:audit）

扫描项目的 wyx 规格覆盖情况，生成按优先级排序的行动计划。这个模式**不生成规格**——它只识别哪里需要规格，并输出该跑哪些命令。与会话启动报告（只报数量）相比，它多做两件事：基于模式识别管道 / sync 候选，以及按依赖顺序排列命令序列。

**工具约束**：全部发现与计数优先用 Glob、Grep、Read；**不要**派发子 agent。**降级模式** —— 某些环境完全没有 Glob / Grep 工具；这时退回到**只读** shell 做发现（用 `find` / `ls` / `grep -r` 来*列出和读取*文件）。绝不用 shell 写入、编辑、移动或生成文件——审计在任何发现路径上都严格只读：它只报告，绝不产出制品。

## 如何解读用户参数

- **路径**（如 `src/lib/server/`）：把审计范围限定在这棵子树。
- **没有参数**：审计整个项目。

## 第一步：发现现有规格

用 Glob 找出全部 wyx 规格文件（若给了路径则限定范围）：

- `**/CONCEPT.md`
- `**/PIPELINE.md`
- `**/SYNCS.md`

读每份规格的第一个标题，提取概念 / 管道 / sync 的名称。

对每份规格，还要检查它是否含有提供边界的段落（也就是 PreToolUse hook 会提取的那些）：`CONCEPT.md` 应有 `## interactions` 或 `## dependencies`；`PIPELINE.md` 应有 `## data boundary`。记下那些完全没有预期边界段落的规格。

## 第二步：识别未覆盖模块

找出源文件超过 2 个、且没有任何同目录规格（`CONCEPT.md`、`PIPELINE.md` 或 `SYNCS.md`）的目录。这与 SessionStart hook 的排除集一致——三种规格类型中任意一种都能让该目录不被标记。**优先用 Glob**；如果环境里没有 Glob 工具，用只读 shell（`find` / `ls`）做发现，绝不用于写入或修改文件。

用 Glob 统计每个目录源文件数量的方法：

1. 对 `**/*.{ts,js,tsx,jsx,svelte,vue,py,rs,go,java}` 跑 Glob（若给了路径则限定范围）。
2. 把结果按父目录分组，逐目录计数。
3. 源文件超过 2 个、且没有同目录规格的目录即为候选。

排除的目录与 SessionStart hook 一致：任何隐藏目录（以点开头 —— `.git/`、`.svelte-kit/`、`.claude/`、`.next/`、`.venv/` ……）、`node_modules/`、`dist/`、`build/`、`vendor/`、`venv/`、`target/`、`__pycache__/`，以及在任意层级下的 `tests/`、`test/`、`spec/`、`__tests__/`、`docs/`、`migrations/`、`components/ui/`、`types/`、`e2e/`、`cypress/`、`fixtures/`、`stubs/`、`mocks/`、`utils/`、`util/`、`helpers/`、`scripts/`、`schema/`、`schemas/`、`constants/`、`config/`。

在标记某个目录之前，先评估它的行为内聚性——只含类型定义、无状态工具函数、薄 store 包装或 schema 定义的目录，很少值得写概念规格（它们没有「状态归属 + 动作 + operational principle」这套东西）。

评估内聚性时看具体信号：可变状态归属（类字段、实例变量、模块级状态）、生命周期方法（init / reset / destroy）、持久化逻辑（数据库、文件 I/O、缓存）、事件发射（emit / dispatch / publish）。命中多个信号的目录是更强的概念候选；一个都不命中的很可能是支撑代码——跳过时把理由写出来。

## 第三步：识别管道候选

在未覆盖的目录里搜索数据转换模式：

- 聚合：`GROUP BY`、`.groupBy(`、`.agg(`、`.reduce(`
- 多阶段 / ETL：管道式链式调用，文件名含 `*etl*` / `*pipeline*` / `*transform*`
- 跨 2 个以上表 / 数据源做 join 的查询构造器

管道候选 = 含 2 个以上转换阶段的目录。

## 第四步：识别 sync 候选

搜索跨概念协调模式：

- 桥接 2 个以上已被概念覆盖模块的事件处理器 / 监听器
- 从 3 个以上不同模块目录引入内容的文件
- Webhook / 回调处理器，消息队列消费者
- 定时任务 / cron 模式
- 目录名含 `*sync*`、`*handler*`、`*dispatch*`、`*orchestrat*`

sync 候选 = 协调 2 个以上概念动作的处理器。

## 第五步：确定优先顺序

按依赖深度给未覆盖模块排序：

1. 找出每个未覆盖模块里的 import / require 语句。
2. 不从其他未覆盖模块引入任何东西的模块 = 第 1 阶段（叶子）。
3. 引入第 1 阶段模块的 = 第 2 阶段。
4. 依此类推，直到所有模块都分配了阶段。
5. 同一阶段内按字母序排列。

管道候选排在拥有其源数据的概念之后。sync 候选排在它所协调的那些概念之后。

## 第六步：输出行动计划

严格按这个格式呈现。

### 现有规格（发现 {N} 份）

| 规格 | 类型 |
| --- | --- |
| `path/CONCEPT.md` | concept |
| `path/PIPELINE.md` | pipeline |

如果第一步发现有规格缺少提供边界的段落，在表格后注明：

「{N} 份规格没有任何边界声明——PreToolUse hook 对这些目录不会注入任何内容。考虑补上 `## interactions` / `## dependencies`（CONCEPT.md）或 `## data boundary`（PIPELINE.md）。」

### 覆盖状态（仅在第二步没有发现未覆盖模块时）

改为输出：

```text
### Coverage Status
全部 {N} 个领域模块都有规格，未发现未覆盖模块。

下一步：
- `wyx:concept drift` —— 检查规格新鲜度（语义分析）
- `wyx:map` —— 若规格已变更，重新生成 ARCHITECTURE.md
```

然后直接跳到「建议的文档更新」（省略「推荐命令」和漂移那一行）。

**否则**，带上漂移建议，并继续输出下面各节：

跑 `wyx:concept drift` 检查规格新鲜度（语义分析，不是看 mtime）。

### 推荐命令（依赖顺序）

按阶段分组输出命令清单：

```text
# 第 1 阶段：叶子概念（不依赖其他未覆盖模块）
wyx:concept src/lib/auth/
wyx:concept src/lib/db/
# 第 2 阶段：依赖第 1 阶段
wyx:concept src/lib/api/
# 第 3 阶段：数据管道
wyx:pipeline src/lib/analytics/
# 第 4 阶段：sync 协调
wyx:sync src/lib/handlers/
# 第 5 阶段：漂移检查（被标为陈旧的现有规格）
wyx:concept drift
# 第 6 阶段：架构地图（全部规格就位之后）
wyx:map
```

### 建议的文档更新

只建议（**不要**自动更新）与本次审计相关的项：

- 「更新 CLAUDE.md：新增 / 修订模块描述」
- 「更新 README.md：刷新架构概览」
- 「跑 `wyx:map` 重新生成 ARCHITECTURE.md」
