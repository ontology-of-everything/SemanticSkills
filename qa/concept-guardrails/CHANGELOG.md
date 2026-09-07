# concept-guardrails Changelog

## 0.28.0 - 2026-09-07

- 统一 Jackson/wyx 消费规则；修复地图遗漏与新鲜度、只读历史冲突、重复授权及严重度；压缩共用流程。
- 核验最新相关论文，更新行为评估及文档。

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 0.27.0 - 2026-09-07

### Changed

- 技能改名：`wyx-zh-cn` → `concept-guardrails`，与 `concept-design` /
  `concept-prd` / `concept-implementation` / `concept-audit` 共用 concept-*
  前缀；显式调用改为 `$concept-guardrails`
- `runtime/.claude-plugin/plugin.json` 的插件标识同步改为 `concept-guardrails`
- 内容仍对应上游 jlifyio/wyx v0.26.0；版本号不再与上游同步
- `SKILL.md` 改为六节骨架（目标 / 原则 / 流程 / 命题 / 记法与模板 / 参考），
  正文压缩约 16%（7.2 KB → 6.0 KB；原有内容压缩逾三成，新增下述对齐内容）；
  目录树与放置反模式并入 `references/concept.md`
- 与 concept-* 链对齐：新增「方言」——wyx 原生（含 interactions / dependencies）
  与零点名（`concept-prd` 产出，跨概念边只在 SYNCS.md）；一个仓库只用一种。
  `references/concept.md`、`sync.md`、`drift-detection.md` 各加一段零点名方言
  下的差异（不写边界段；SYNCS.md 按 flow 分节、按 syncs 包各一份、flow 不拆散；
  级联合法但须声明 depth-limit；New dependency / CONCEPT→CONCEPT 校验改为
  Spec naming violation）
- 新增与 `concept-audit` / `concept-design` 的分工表，消除 `wyx:audit` 与
  概念审计、`wyx:concept` 与概念设计的同名歧义

## 0.26.1 - 2026-09-03

### Changed

- 默认不再参与模型的自动技能选择；只有用户显式指名 `$wyx-zh-cn`
  时才加载，并在 Codex 元数据中同步禁用隐式调用
- 移除安装载荷中的 `license` frontmatter，避免与 ClawHub 的 MIT-0
  技能包许可冲突；上游 MIT notice 继续保留在 `LICENSE.upstream`

## 0.26.0 - 2026-08-27

### Added

- 初始版本：[jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0 的中文改写版，
  上游 MIT 许可随 `LICENSE.upstream` 一并保留
- `SKILL.md` 把上游五个斜杠命令合并成一个技能的六种模式路由
  （audit、concept、drift、pipeline、sync、map）
- `references/` 收录六篇完整中文译文：审计与命令排序、概念规格设计、
  漂移检测程序与严重度校准、数据管道不变量、sync 协调映射、架构地图生成
- `references/hooks-runtime.md` 说明边界自动注入的接线方式与已知边界
- `runtime/` 逐字节原样收录上游 hooks 与脚本（仅插件标识改名为 `wyx-zh-cn`）；
  上游的开发期门禁 `check-rules.sh` 与运行时无关，未收录
