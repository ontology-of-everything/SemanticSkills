# 组合缺陷检查表

流程第 4 步（组合缺陷维度）读本文。对象是 sync 层——`SYNCS.md` 与组合层代码（mediator 函数 / 规则引擎规则 / 接口适配器）。概念自身的独立性归「独立性」维度；这里只查概念**如何被组合**。

判据来自 sync 的因果语义：when 匹配已完成动作、where 只经 queries 读状态、then 触发已声明动作；应用动作 = `Requesting` 触发的 sync；错误是可匹配输出。凡违背其中一条即缺陷。

## 检查表

| 类别 | 如何识别 | 严重度 | 路由 |
| --- | --- | --- | --- |
| **行为保持违规** | sync 调用概念未声明的动作，或绕过 queries 直读概念内部状态 | High | 规格漏声明 → `concept-design`；代码越权 → `concept-implementation` |
| **隐式组合** | 跨概念联动写在某个概念内部（概念 A 的 action 里触发 B），未以 sync 声明 | Critical | `concept-implementation`（同时记入独立性维度） |
| **缺错误 sync** | 可失败动作的 `(error: …)` case 无 sync 匹配，且未记入排除表 | High | `concept-design` |
| **入口无响应** | `Requesting` 入口触发的 flow 没有成功路径或错误路径的响应 sync | High | `concept-design` |
| **冲突 sync** | 同一 when 触发的多条 sync，then 效果互斥或结果依赖执行顺序 | High | `concept-design` |
| **死 sync** | when 匹配的动作没有任何 flow / 入口会产生 | Low | `concept-prd`（规格过期）或 `concept-design` |
| **级联无界** | sync 链成环，或实现未声明级联深度上限 | High | `concept-implementation` |
| **欠同步** | 用户需手工重复本应自动的联动（规格与代码都缺） | Medium | `concept-design` |
| **过同步** | 自动化抢走用户控制且不可关闭 / 配置 | Medium | `concept-design` |
| **sync 含业务不变量** | 组合层里出现本属概念 domain 的校验或规则 | Medium | `concept-implementation` |
| **sync 积攒状态** | 组合层持有自有持久状态（升格为概念的信号） | High | `concept-design` |
| **直通概念动作** | 外部 API / 端点直接调用概念动作，不经 sync | Critical | `concept-implementation` |
| **排除动作被组合** | 模型标为排除的动作被 sync 调用或经 API 暴露 | High | `concept-design` |
| **flow 拆散或同步图不符** | 同一 flow 的 sync 散落多处；同步图与 sync 块 / 代码不一致 | Medium | `concept-prd` |
| **流程脚本化** | 一条 sync 长成多步流程，或一个 flow 触达概念过多（经验 ≥5） | Medium | `concept-design`（分解线索：可能缺概念） |
| **synergy 反噬** | 概念借用另一概念实现功能后，被借用方的 purpose 被扭曲 | Medium | `concept-design` |

## 校准

- 严重度逐字采用表中取值；比类别更严重的发现重新归类，不在类别内升级。
- 「规格的沉默不是漂移」同样适用：规格未提的 sync 是未记录（归漂移维度的 Missing sync），不是组合缺陷；只有违背因果语义或用户可感的联动缺失才算缺陷。
- 欠 / 过同步是设计判断：报告时必须写出用户视角的场景（谁在什么时候被迫手工做什么 / 被抢走什么控制），无场景不报。
- 报 Medium 及以上前，用 grep 或读文件确认发现存在于**当前**代码。

## 与其他维度的分工

- 概念模块互引、共享表、DTO 进签名、规格点名其他概念 → **独立性**维度。
- `SYNCS.md` 引用的动作在目标 `CONCEPT.md` 不存在 → **规格漂移**的跨规格校验；若代码里该调用真实发生且动作未声明，同时记一条**行为保持违规**。
- 依赖图与代码不符、Parnas 违规 → **依赖与子集**维度。
