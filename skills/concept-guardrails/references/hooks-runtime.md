# 可选 hooks 运行时

`runtime/` 保留 wyx v0.26.0 的英文脚本与 hooks 注册；插件清单仅改名为 concept-guardrails，MIT 通知保留。规格与审计本身不依赖 Claude Code，只有自动注入需要它及 bash/jq。

## 行为与边界

| hook | 实际能力 |
| --- | --- |
| SessionStart | 列规格、覆盖线索、历史最后一次结果、mtime 陈旧提示与遮蔽告警；缺 jq 时警告 |
| PreToolUse | 对 Write/Edit/NotebookEdit，向上找最近 CONCEPT/PIPELINE，注入 interactions/dependencies/data boundary |
| PostToolUse | 编辑后重申最近 CONCEPT 的 dependencies；无该节则静默 |

PreToolUse 到第一个含 CONCEPT 或 PIPELINE 的目录停止；SYNCS 只列名，不提供边界或终止查找。只有 PIPELINE 时另找祖先 CONCEPT，可能标记 SHADOWED。应主动读取当前 PIPELINE，不能假定祖先注入包含全部本地约束。

项目根依次取 CLAUDE_PROJECT_DIR、输入 cwd、当前目录；最终空或 `/` 时退出，不越过根。脚本跳过 json/jsonl/lock/log/txt；编辑规格时给校对提示，PostToolUse 不重申边界。具体提取只兼容脚本支持的大小写形式，不是 Markdown 通用解析器。

## 接线

用户要求启用时，可对单次会话加载：

```bash
claude --plugin-dir /绝对路径/skills/concept-guardrails/runtime
```

若发行渠道漏掉隐藏插件清单，可将 runtime/hooks/hooks.json 的 hooks 合并到项目 `.claude/settings.json`，把 CLAUDE_PLUGIN_ROOT 占位换成 runtime 绝对路径，保留其他设置。

自检：在目标项目设置 CLAUDE_PROJECT_DIR 后运行 `bash runtime/scripts/session-start.sh`，检查规格清单。运行时没有上游开发用 check-rules.sh；本仓验证在 qa 下。

## Jackson 兼容性

脚本不解析四节或 when/where/then。Jackson 规格可能显示 no boundary declarations，PostToolUse 通常静默；这是提取器限制，不能补回跨概念 dependencies。编辑前主动读最近 CONCEPT 及相关 SYNCS；PIPELINE 的 data boundary 仍可读取。

hooks 是建议，不阻断写入、不解析 import，也不验证语义；Bash 或 MCP 写入绕过它，其他客户端不自动执行。边界仍由主动读规格、架构测试和漂移检查验证。

“规格反映实现”的脚本提示用于回填，已确认新行为仍规格先行。SessionStart 只读取 `.claude/wyx-drift-history.jsonl` 最后一条，fix 用 specs_remaining；局部扫描不代表全仓清洁，mtime 不证明语义最新。只读扫描不为清提醒写历史，持久记录须有明确请求并来自真实测量。
