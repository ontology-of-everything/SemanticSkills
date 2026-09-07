# Daniel Jackson concept design：独立研究记录

核验截至 **2026-09-07（Asia/Shanghai）**。由独立研究子代理按 research 技能执行。读取了全部四份 `skills/concept-*/references/sources.md`、本地两篇论文的中英文摘要及相关规格；未找到 Making Software Meaningful 的本地摘要。工作树存在其他修改且研究中仍有变化，下列位置指本次读取的工作树，不代表已修复。

## 版本与检索边界

| 第一手来源 | 当前版本／日期 | 结论与置信 |
| --- | --- | --- |
| [Beyond Objects：提交历史](https://arxiv.org/abs/2606.27258)（Daniel Jackson） | v1，2026-06-25 | 未列出新版；高 |
| [WYSIWID：提交历史](https://arxiv.org/abs/2508.14511)（Eagon Meng、Daniel Jackson） | v1：2025-08-20；v2：2025-08-27 | 当前 v2；更新说明为 DOI、参考文献／排版；高 |
| [Making Software Meaningful：提交历史](https://arxiv.org/abs/2606.11051)（Meng、Namazov、Schare、Cunha、Jackson） | v1，2026-06-09 | 未列出新版；高 |
| [Verified LLM-Driven Synthesis for Concept Design](https://arxiv.org/abs/2607.15718)（Alcino Cunha 独著） | v1，2026-07-17 | 更近的相关第一手研究，**不是 Jackson 新论文或前三篇的修订**；高 |

以三个编号、作者名、concept design／synchronizations、2026-07 至 09 等组合执行 web 搜索，并核对 [arXiv 作者结果](https://arxiv.org/search/?searchtype=author&query=Jackson%2C+Daniel&order=-announced_date_first&size=50)。本次未找到晚于 Beyond Objects 的 Jackson 署名概念设计论文；较新的临床试验／心理测量结果不属本主题。**“未找到”置信中，不等于证明不存在**：索引可能滞后，作者检索混入同名者；[作者主页](https://people.csail.mit.edu/dnj/index.html)可读，但其 SDG publications 链接抓取失败。

以下逐源短归纳，不复制全文，不把同一论文不同 URL 当成新增引用预算；表内版本沿用上表。推论与工程建议另行标明。

## 语义核验

| 主张 | 核验结果、第一手定位与局限 |
| --- | --- |
| 概念的基本语义 | 按功能关注点划分动作及相关事实，个体可跨概念；意义应贯穿用户、代码与日志。[Making §2.5–2.6、§4.4](https://arxiv.org/html/2606.11051v1#S4.SS4)。高；不是按实体分模块。 |
| flow／入口 | flow 是外部动作**发生实例**为根的因果 DAG；多项 when 须同 token，then 继承。[WYSIWID §5.3、§6.3、§6.7](https://arxiv.org/html/2508.14511v2#S6.SS3)。高；入口类型不是单个运行实例。 |
| Requesting | 请求可发生而业务动作不发生；Requesting 是通常采用的伪概念命名。[Beyond §13](https://arxiv.org/html/2606.27258v1#S13)。高；不是一切概念设计唯一合法入口名称。 |
| when／where／then／错误 | when 匹配完成记录的具名输入／输出子集；where 产出绑定集，每组驱动 then 调用；错误可作普通输出匹配。[WYSIWID §5、§6.5](https://arxiv.org/html/2508.14511v2#S5)。高；空绑定不自动生成 error。 |
| 只许经 queries 读状态？ | 否。抽象状态公开，queries 只读且返回绑定集；Fig.3 直接读取关系。[Beyond §13](https://arxiv.org/html/2606.27258v1#S13)。高；这不授权绕过实际系统的访问控制。 |
| 图、环与 depth limit | 多项 when 是合取；运行发生图为 DAG。[WYSIWID §5.3、§6.6](https://arxiv.org/html/2508.14511v2#S5.SS3)。高。**工程推论（中）**：动作类型图成环不等于发生图成环；DAG 也不证明终止。三篇未见强制 depth limit 或 coordination graph 超边定义。 |
| 行为保持 | 组合轨迹仍遵守各概念行为；跨概念性质另依赖组合。[WYSIWID §2](https://arxiv.org/html/2508.14511v2#S2)。高；不是系统性质、活性及既有功能均自动保持的保证。 |
| 四节／五要素／principle | 五项为 Name、Purpose、Principle、State、Actions；queries 可列入 actions，但不是动作。[Beyond §13](https://arxiv.org/html/2606.27258v1#S13)。WYSIWID §4 使用 operational principle；四节不计名称，二者不矛盾。[WYSIWID §4](https://arxiv.org/html/2508.14511v2#S4)。高；固定 Markdown 标题属方言。 |
| notes 的出处 | 使用上下文引用限于 notes，来自 [2025 秋课程 rubric](https://61040-fa25.github.io/resources/concept-rubric)，不是 Beyond 的规格要素。高；网页无版本号，本次 web 抓取失败后，经只读 HTTPS 取得对应条目，并对照本地镜像。 |
| user-facing／基础设施 | [Criteria（2023-09-11）](https://essenceofsoftware.com/tutorials/concept-basics/criteria/)明确 API 程序员也是用户。高；只对应用内部隐藏结构的排除，不能推成“基础设施一概不是概念”。Cunha 的 DLQ 例也提示需先定用户视角，见下节。 |
| 判据命名 | Criteria 实列八项：User facing、Semantic、Independent、Behavioral、Purposive、End-to-end、Familiar、Reusable。[同一作者教程](https://essenceofsoftware.com/tutorials/concept-basics/criteria/)。高；仓库“五条＋四词＋组合后检查”是重组，不能说原文只有五条。 |
| 依赖与子集 | 图表达应用中的纳入条件，概念本身无 intrinsic 依赖；可有互依赖，应合组解释。[Dependency（2023-09-11）](https://essenceofsoftware.com/tutorials/concept-basics/dependency/)。高；闭包子集只满足图上条件，空集也满足，不保证有用或可构建。 |
| 旧事务语义 | Beyond §13 改用因果规则，解释了旧对称／事务方案的问题。[原文](https://arxiv.org/html/2606.27258v1#S13)。高；只说明所选方案演进，不能宣称所有实现禁用事务。 |
| 增量与实现约定 | WYSIWID 说行为扩展**常可**增删／替换 sync，并非等式。[§1、§7.4](https://arxiv.org/html/2508.14511v2#S1)。Making §5.1.5 还允许新增事实／动作；§5.2.1 允许 sync 任意嵌套目录。[原文](https://arxiv.org/html/2606.11051v1#S5)。高；文件集中、每组一个 mediator、阈值 ≥5 都应标工程约定。 |

## 更近论文不能混用的语义

[Cunha v1 §2、§3.2–3.3、§5.7](https://arxiv.org/html/2607.15718v1#S3)给出 reaction monitor：where 检查动作前状态，待办反应优先；特殊 `error` 是无法清偿的义务，实现应在提交效果前拒绝／守卫／中止。它与 WYSIWID 的普通错误输出不是同一机制。验证关注 settled 状态的不变量，并检查 overreaction；“通过不变量检查”仍不等于符合意图。案例含 DeadLetterQueue；评估限于三个应用、十二变体和一种 LLM 配置。以上置信高，不把这套形式语义追认成前三篇的统一标准。

## 需要修复的具体主张（建议，未改技能）

以下路径均相对仓库；位置应以主张文本重新搜索，避免并行编辑造成行号过期。

1. **补 flow 的运行时语义**：`skills/concept-design/SKILL.md` 与 `references/sync-notation.md` 的“一个 Requesting 入口 = 一个 flow”“每条 sync 恰好属于一个 flow”，应区分入口分组与发生实例；同一规则能用于多个运行实例。依据上表 flow 行。
2. **修错误路径和结果绑定示例**：`skills/concept-design/references/sync-notation.md` 的 `_authenticate(...):(error)` 未声明错误查询契约；`Session.start(user), ExpiringResource.allocate(session,300)` 使用了未绑定的 session。建议先匹配认证结果，再匹配 Session.start 的完成输出后 allocate；无查询结果时显式定义失败条件。相关主模板也有 `where ...:(error)`。依据上表匹配语义；此为对仓库例子的推论，高。
3. **撤掉 queries 与行为保持的等同**：design 原则及 audit 的 `composition-checklist.md` 把“非 query 读状态”直接判行为保持违规，应改成“只读公开抽象状态”；若坚持查询 API，则另列工程边界。删除“因此不破坏 Integrity”的无条件推导。依据上表公开状态／行为保持行。
4. **图保留联合触发与读取关系**：`skills/concept-design/references/sync-notation.md` 的逐对 Source→Target 边不足以表达合取。建议规则节点／有向超边，并单独标 where 读取边；这是仓库图表示建议，不是作者指定术语。依据上表匹配语义和 [Making §4.5 的三概念协调例](https://arxiv.org/html/2606.11051v1#S4.SS5)，推论高。
5. **撤掉“成环或无 depth limit 即 High”**：`skills/concept-audit/references/composition-checklist.md` 的“级联无界”需检查可达性与终止依据；深度上限仅属运行预算，不能充当语义终止证明。实现参考中的强制上限若保留，注明截断行为及工程来源。依据上表图／环行，推论中。
6. **修来源映射**：design、prd 的 `references/sources.md` 将 notes 归给 Beyond；audit 将错误匹配归给 Beyond，应分别改引课程 rubric、WYSIWID §5.3。“规范可从代码提取”未在 WYSIWID 找到通用保证；标仓库审计能力／待验证，不再作为论文定论。置信高／后者中。
7. **收窄产品子集与开发顺序**：`skills/concept-design/references/sync-notation.md` 的“每个不缺依赖子集是可行产品”“开发先做被依赖者”，应区分逻辑闭包、产品价值与构建支持；互依赖可成组，开发排序是建议。依据上表 Dependency 行，推论高。
8. **标明版本和工程方言**：各 sources 的“行为增量 = sync 增删”改为有条件表述；“资格五条”注明重组来源；principle／operational principle 作为兼容同义标题；基础设施审计先声明用户视角。当前 guardrails 已写标题兼容规则，不应重复报成尚未修复。依据上表相应行。

局限：这是文献与规格主张核验，没有运行引擎测试、证明终止性或验证任何产品子集可构建；网页日期不等于最后修改日期。本地摘要用于定位与对照，不能代替版本化第一手论文。
