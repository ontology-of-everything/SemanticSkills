# concept* 技能审查与压缩记录

日期：2026-09-07。覆盖五个技能、全部参考文件、示例、UI 提示、运行时说明、QA 与仓库文档。以任务开始时的工作树为基线，包含原有未提交修改；未提交或发布。

## 目标与论文依据

技能族的目的：把用户需要建模为有意义且独立的功能单元，以因果同步组合，再将模型持久化、实现和审计。建模语义、应用组合、工程封装与工具限制须分别陈述。

核验 WYSIWID v2、Beyond Objects v1、Making Software Meaningful v1，并检查更近的 Cunha 2026-07 研究；其 reaction/error 语义不同，没有拼接成统一标准。详细版本、出处、检索边界见[独立研究](2026-09-07-concept-research.md)。

## 主要修复

| 维度 | 已修复问题 |
| --- | --- |
| 概念正确性 | 五要素/四节和 principle 同义；局部参数同名不误判；OP 不等于完整行为契约；判据分组明确为本仓综合 |
| 组合语义 | flow 类型分组与执行实例分开；多 when 合取及请求隔离；空查询不产生 error；禁止使用 then 的未来输出 |
| 可执行性 | 写动作原子维护不变量；响应、重放和部分失败明确；同步图保留规则节点与查询边 |
| 依赖一致性 | 产品依赖不从调用边推导，依赖闭包不等于可交付产品，分组不自动具有业务语义 |
| 工程说明 | Modulith 默认 verify 的限制；事件监听不等于完整引擎；Cargo 包级工具不能检查同 crate 层次；事务不替代失败契约 |
| 审计质量 | 移除循环、无 depth limit、运行日志、目录分布等自动误报；按证据和真实影响校准严重度 |
| 护栏 | Jackson/wyx 消费规则一致；地图读取新 sync 且考虑删除/改名；只读不写历史；已授权不重复确认 |
| 内容工程 | 共用约定集中于入口，按模式读取参考；删除重复操作段落；示例改写并标明范围；来源与工程约定区分 |

## Token 测量

编码：`o200k_base`；按文件分别编码后求和，不使用字数/4 估算，不把移入 references 计作删除。

| 口径 | 修改前 | 修改后 | 减少 |
| --- | ---: | ---: | ---: |
| 五份 SKILL.md | 7,880 | 5,560 | 29.44% |
| 全部技能 Markdown（含 references） | 37,607 | 25,799 | 31.4% |
| 全部安装载荷（含未压缩 runtime） | 46,603 | 34,796 | 25.34% |

| 技能 Markdown | 修改前 | 修改后 | 减少 |
| --- | ---: | ---: | ---: |
| concept-audit | 4,039 | 3,094 | 23.4% |
| concept-design | 6,220 | 5,028 | 19.16% |
| concept-guardrails | 19,432 | 9,909 | 49.01% |
| concept-implementation | 5,127 | 4,804 | 6.3% |
| concept-prd | 2,789 | 2,964 | -6.27% |

目标按技能族汇总实现，不强制每个文件同比裁剪；PRD 因补充独立可读的契约说明略增。runtime 保持原样，通常执行而非加载为指导文本；把它纳入全载荷后，降幅如上单列。没有将删减内容迁往仓库文档再要求每次加载。

基线 token 数和内容哈希：[token-baseline.json](../../../qa/concept-design/token-baseline.json)。复核：[measure-tokens.py](../../../qa/concept-design/measure-tokens.py)。

## 验证与局限

- 五套 `qa/concept-*/validate.sh` 全部通过：布局、skills-ref、Markdownlint、skillcheck；guardrails 另验证原样 hooks 脚本语法与 JSON。
- 技能内本地 Markdown 链接有效；评估 JSON/案例 ID 有效；runtime 与任务开始快照逐文件相同；版本与目录说明同步。
- 独立子代理实际完成三类前向任务：共享设备并发预约模型、合法循环/flow 日志的只读审计、Jackson 多 when 地图及独立产品依赖矩阵。未发现阻塞性语义矛盾；步骤编号错误已修复。
- 新增五类回归案例；其中 PRD/Java 的新增案例本轮仅校验案例文件与人工契约，未声称全部自动执行。前向验证是代理产出与状态推演，不是 Java/Rust/TS 运行时测试或形式证明。
- skill-creator 通用 quick_validate 四个技能通过；guardrails 被其旧字段白名单拒绝 `compatibility`。此字段已由仓库支持的 skills-ref/skillcheck 校验通过，因此保留兼容性元数据，不为旧校验器删字段。

工程依据：[Spring Modulith verification](https://docs.spring.io/spring-modulith/reference/verification.html)、[module fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html)、[Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)、[cargo-deny bans](https://embarkstudios.github.io/cargo-deny/checks/bans/cfg.html)。
