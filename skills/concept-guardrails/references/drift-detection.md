# 漂移检测（`drift` 模式）

只读对照规格与当前实现；修复是后续有授权的独立步骤。可带路径限定范围。含旧 wyx 段落的文件不进入下列检查表，单列为「待迁移」并注明段名。

## 扫描

1. 定位范围内三类规格及 PRD 暂存文件；补读祖先规格和范围外引用这些概念的 sync/管道。报告范围外代码未核实处。
2. 每份规格连同实现、schema/迁移与测试一起检查。多语言实现各自对账，保留一份权威契约及实现索引，避免复制后漂移。
3. 对下列每个适用类别给出“通过 / 发现 / 未核实”；缺实现不等于动作不存在。再做跨规格检查与根因聚合。
4. 规格多且工具允许时可委派只读扫描，每组 2–3 份相邻规格。继承用户模型设置；提示词附对应检查表、校准与项目约定。主代理核对漏项、跨组引用和重要发现。无委派工具时分批自查。

## CONCEPT.md

| 类别 | 判定依据 | 默认严重度 |
| --- | --- | --- |
| Missing action | 未记录的公开动作；排除内部辅助函数 | Medium |
| Removed action | 已声明动作在当前全部相关实现中不存在 | High |
| Changed signature | 参数、实际返回、错误分支改变契约 | Medium |
| New state | 未记录且影响可观察行为的状态；检查迁移/schema | Medium |
| Boundary violation | 绕过其他概念动作/query 访问其内部状态或实现 | High |
| Cross-cutting parameter | 多个动作的公共参数影响权限、身份等契约却未记录 | Medium |
| Spec naming violation | 四节真正依赖别的概念定义，或混入 interactions / dependencies 等边界段 | Medium |
| Intrinsic coupling | 概念直接调用另一概念的公开 API | High |
| OP 无测试 | principle 的场景无对应行为测试 | Medium |
| 排除动作被使用 | 应用有意排除的动作被调用或暴露 | High |
| Resolved known gap/coupling | 现有实现已解决记录在案的缺口 | Low |

不补 `dependencies` 段来"修复"独立性；跨概念依赖只能出现在 `SYNCS.md`，否则报 Intrinsic coupling。局部类型参数 User 与外部概念同名不构成点名违规。

## PIPELINE.md

| 类别 | 判定依据 | 默认严重度 |
| --- | --- | --- |
| Missing stage | 影响数据契约的新增阶段未记录 | Medium |
| Changed invariant | 当前转换与已声明不变量矛盾 | High |
| New data source | 未声明的表/API/文件输入 | Medium |
| Boundary violation | 跨概念绕过公开接口读写私有数据 | High |

自身存储适配器内的 SQL 不是越界；外部输入不必虚构成概念拥有的表。

## SYNCS.md

| 类别 | 判定依据 | 默认严重度 |
| --- | --- | --- |
| Missing/Removed sync | 新协调未记录 / 已声明协调无实现 | Medium / High |
| Changed trigger | when 与实现的触发不同 | Medium |
| New participant | 实际参与概念未声明 | High |
| Changed binding/effect | where 的资格/绑定或 then 的目标/参数改变 | High |
| Graph inconsistency | 存在的派生图与规则块不符 | Medium |

同步图可在总体 PRD，不要求 SYNCS 内重复一份。响应、错误、循环等语义缺陷需要全面检查时交接 `concept-audit`。

## 跨规格引用

逐条解析 include 实例化、动作、query、参数和输出 case，核对真实声明；`principle` / `operational principle` 视为同一节。`Requesting` 等明确的外部入口契约单独核对，不要求伪概念拥有 CONCEPT.md。

| 类别 | 判定依据 | 默认严重度 |
| --- | --- | --- |
| Missing reference | sync/管道引用不存在的动作或 query | High |
| Missing participant | 内部概念既无规格也无索引说明 | Medium |
| Signature/binding mismatch | 参数、输出 case 或类型实例化不匹配 | High |

## 校准

严重度是本仓审计约定，并非论文结论。表值为默认值，按可复现影响校准：Critical 仅用于有证据的权限绕过、数据破坏或核心功能不可用；High 为明确契约/边界破坏；Medium 为有影响的遗漏；Low 为局部文档维护。记录调整理由，不能仅因“跨模块”就报 Critical，也不能因已记录 coupling 就掩盖真实风险。

- “规格没提”不推出行为被禁止；Missing 类专门记录新增遗漏，与明确矛盾分开。
- 不影响契约的异步/Result 包装、命名映射和私有派生值无需报缺陷；需要维护说明时最多 Low。有显式映射的跨规格名字不误报不存在。
- 授权的架构例外注明来源、范围和后果；概念间公开 API 调用仍破坏独立性，例外不改变类别，只影响修复方向。组合层调用声明接口合法。
- 报 Medium 以上需有当前代码或规格位置与证据。合并同一根因，跨多份规格保留受影响路径；不把遗漏类别算作通过。

## 报告与修复

```text
# Drift Report — <日期>
范围/规格与代码版本：...
Summary: 扫描 N；有漂移 N；Critical N / High N / Medium N / Low N
| 类别 | 规格位置 | 实现证据 | 影响/严重度 | 修复方向 |
跨规格引用：...
系统性模式：...（保留全部受影响路径）
未核实：...
建议的下一步：...
```

模型不合理 → design；文档陈旧 → prd/本技能；代码违约 → implementation。两侧冲突且不能从已确认需求判断时，呈现具体取舍后询问；不能默认让规格追随代码。已授权修复则报告后完成最小改动并重查；未授权则停在报告。

## 可选历史（仅在用户要求持久记录时）

只读扫描不追加 `.claude/wyx-drift-history.jsonl`。要求记录时按已有 JSONL 协议追加真实测量：

```text
{"ts":"<ISO-8601>","action":"detect","specs_scanned":0,"specs_with_drift":0,"critical":0,"high":0,"medium":0,"low":0,"low_by_spec":{},"path":"<范围>"}
{"ts":"<ISO-8601>","action":"fix","specs_fixed":0,"specs_remaining":0,"ref_ts":"<对应 detect ts>"}
```

替换占位数值为实测数；一个规格全部发现解决才计入 specs_fixed。fix 引用本次修复针对的 detect，保留范围，不修改旧行。每条是快照，SessionStart 只读最后一条；局部扫描不能代表全仓清洁。无 action 的旧记录按 detect 理解。清除修复后陈旧提示需重新扫描，不能伪造零漂移记录。去重后 Low 较多可提示重审规格，但条数不自动提高严重度。
