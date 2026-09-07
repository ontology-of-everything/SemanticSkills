# 规格漂移与校准

每份规格连同当前实现、schema/迁移和测试读取；同时沿总体 PRD 索引查暂存文件。兼容 principle/operational principle；明确旧版格式，不能把已有方言差异当新缺陷。queries 与动作同查签名，但查询不产生完成事件。

## 类别

| 对象/类别 | 判定依据 | 默认严重度 |
| --- | --- | --- |
| CONCEPT / Missing action | 未声明的公开动作 | Medium |
| Removed action | 已声明动作在全部相关实现中不存在 | High |
| Changed signature | 入参、真实返回或错误 case 改变契约 | Medium |
| New state | 未声明且影响可观察行为的状态 | Medium |
| Spec naming violation | Jackson 四节依赖其他概念定义；同名局部参数合法 | Medium |
| Boundary violation | 绕过其他概念公开接口访问其内部状态/实现 | High |
| Intrinsic coupling | 概念直接调用另一概念公开 API | High |
| Cross-cutting parameter | 影响契约的公共参数未记录 | Medium |
| OP 无测试 | 代表性故事无对应行为测试 | Medium |
| 排除动作被使用 | 明确排除的应用动作实际可达 | High |
| SYNCS / Missing/Removed sync | 新增协调未记录 / 旧规则无实现 | Medium / High |
| Changed trigger | when 与真实触发不同 | Medium |
| Changed binding/effect | where 资格/绑定或 then 目标/参数改变 | High |
| New participant | 实际参与概念未声明 | High |
| Graph inconsistency | 存在的派生图与规则不符 | Medium |
| 跨规格 / Missing reference | sync 动作/query 无声明，或签名/实例化不匹配 | High |
| Missing participant | 内部概念无规格或索引 | Medium |

Requesting 等明确的外部入口契约不要求 CONCEPT.md，仍需验证参数、结果与关联。同步图可只在总体 PRD，不要求 SYNCS 重复。PIPELINE 存在时另核对阶段/来源遗漏（Medium）、不变量矛盾或跨概念越界（High）。产品依赖按需求核验，代码耦合不能作为产品必须依赖的证明。

## 严重度校准

这是本仓审计约定，并非论文结论。默认值可按可复现影响调整并说明：Critical 仅用于有证据的权限绕过、数据破坏或核心功能不可用；High 为明确契约/边界破坏；Medium 为有影响的遗漏；Low 为局部文档维护。

- 规格沉默不推出禁止；Missing 类记录新增遗漏，与明确矛盾分开。
- 私有辅助函数、派生缓存、无语义变化的 Result/异步包装或命名映射不构成契约漂移；需维护说明时最多 Low。有显式名称映射时跨规格不误报不存在。
- 记录在案的耦合不自动降级真实风险；标注授权例外的范围及后果。原生公开 API 调用可合法，Jackson 概念互调仍破坏独立性；组合层调用合法。
- Medium 以上附当前代码/规格位置与证据。无法读全相关实现时标未核实，不能把搜索未命中当不存在。
- 合并同一根因并列受影响路径；Low 数量只提示维护负担，不自动升级。

## 分批检查

规格多时可委派只读子代理，每组 2–3 份相邻规格，继承用户模型设置；不可用时主代理分批执行。附检查表、校准及项目约定，每类返回通过/发现/未核实。主代理核对漏项、跨规格引用与重要证据，最后聚合；不以固定模型档位替代验证。
