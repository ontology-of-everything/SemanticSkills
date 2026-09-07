# 边界自动注入运行时（hooks）

`runtime/` 目录是上游 wyx 插件的 hooks 机制，**逐字节原样收录，未作任何翻译或改动**（脚本内的注释与输出仍是英文，改动它们会带来行为风险）。唯一被改写的文件是 `runtime/.claude-plugin/plugin.json` 的插件标识，改为 `concept-guardrails` 以避免与上游插件同名冲突。

本技能的其余部分（规格格式、设计规则、漂移检测、地图生成）与 agent 无关，任何 agent 都能执行；只有下面这套自动注入依赖 Claude Code 的 hooks 与 `jq`。

## 收录内容

```text
runtime/
├── .claude-plugin/plugin.json   # 插件清单（标识已改名为 concept-guardrails）
├── hooks/hooks.json             # SessionStart + PreToolUse + PostToolUse 注册
└── scripts/
    ├── session-start.sh         # 规格覆盖 + 漂移新鲜度 + 未覆盖模块报告
    ├── drift-context.sh         # 写入前注入边界（PreToolUse）
    └── post-check.sh            # 写入后重申依赖清单（PostToolUse）
```

上游还有一个 `scripts/check-rules.sh`，那是 wyx 自己仓库的开发期门禁（它扫描插件根下的 `skills/` 目录检查子 agent 模型固定规则），与运行时无关，因此未收录。

## 三个 hook 各做什么

### SessionStart

会话开始（`startup|resume|clear|compact`）时输出一段项目规格状态：

- 已有规格的数量与路径（CONCEPT / PIPELINE / SYNCS 分类）
- 上次漂移检查的时间与结果；若最后一条历史记录是 `fix`，报告的是 `specs_remaining`
- 上次漂移检查之后被修改过的规格，以及被修改过的代码目录
- `ARCHITECTURE.md` 是否可能已陈旧
- 未覆盖模块（源文件超过 2 个、且没有任何规格的目录）
- 规格遮蔽告警（子目录只有 `PIPELINE.md` 而没有 `CONCEPT.md`）
- 若 `jq` 缺失，警告边界注入已被禁用（每会话一次）

漂移历史读自项目内 `.claude/wyx-drift-history.jsonl`。

### PreToolUse（Write / Edit / NotebookEdit）

在写入发生**之前**，从被编辑文件所在目录向上找规格，把 `CONCEPT.md` 的 `## interactions`、`## dependencies` 与 `PIPELINE.md` 的 `## data boundary` 作为 `additionalContext` 注入。

- 在第一个含 `CONCEPT.md` 或 `PIPELINE.md` 的目录停止向上；`SYNCS.md` 只被列出，不终止查找
- 只有 `PIPELINE.md` 而没有同目录 `CONCEPT.md` 时，继续向上找祖先 `CONCEPT.md`，并带 `[SHADOWED]` 标注注入其边界
- 编辑规格文件本身时，注入内容改为提示「确认改动反映当前实现」
- 跳过 `*.json`、`*.jsonl`、`*.lock`、`*.log`、`*.txt`
- 不越过项目根向上查找；`CLAUDE_PROJECT_DIR` 为空或为 `/` 时直接静默退出

### PostToolUse（Write / Edit / NotebookEdit）

在写入**之后**，重新注入最近 `CONCEPT.md` 的 `## dependencies` 作为聚焦提醒，用于捕捉多文件连续编辑过程中溜过去的越界引用。它不解析 import、与语言无关；没找到规格或规格没有 `## dependencies` 时静默退出。编辑规格文件本身时不触发。

## 接线方式

### 方式一：作为插件目录加载（推荐）

```bash
claude --plugin-dir /绝对路径/skills/concept-guardrails/runtime
```

只对该次会话生效，无需安装。`runtime/` 的布局就是插件根布局，`hooks.json` 里的 `${CLAUDE_PLUGIN_ROOT}` 会解析到它。

### 方式二：手工写进项目设置

把 `runtime/hooks/hooks.json` 的 `hooks` 内容合并进项目 `.claude/settings.json`，并把 `${CLAUDE_PLUGIN_ROOT}` 替换为 `runtime/` 的绝对路径。当发行渠道剥掉了隐藏目录（`.claude-plugin/` 因此丢失）导致方式一不可用时，用这一种。

### 自检

```bash
CLAUDE_PROJECT_DIR=/绝对路径/你的项目 bash runtime/scripts/session-start.sh
```

它应当打印规格清单与覆盖状态。没有输出通常意味着项目里还没有任何规格文件。

## 前置条件与已知边界

- 需要 `bash` 与 `jq`。`jq` 缺失时 SessionStart 会警告，边界注入被禁用（其余模式仍可用）。
- **只匹配 Write / Edit / NotebookEdit。** 通过 Bash 改文件（`echo > file`、`sed -i`）或通过 MCP 的文件写入工具（`mcp__server__*`）完全绕过这套 hook。
- **它是建议性的，不是强制的。** hook 只把边界送到模型眼前，不阻断任何写入；最终是否遵守取决于模型。
- 插件机制是 Claude Code 专有的。其他 agent 请依赖本技能的规格与漂移流程，主动读取规格而非依赖自动注入。
