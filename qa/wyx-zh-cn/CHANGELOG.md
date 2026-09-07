# wyx-zh-cn Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

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
