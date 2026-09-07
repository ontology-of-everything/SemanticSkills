---
name: concept-audit
description: Audits code against a Daniel Jackson concept model for independence, composition defects, spec drift, design criteria, and product dependencies. Use when the user requests 概念审计 or concept-audit; read-only, with evidence and repair routing.
metadata:
  openclaw:
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/concept-audit
---

# 概念审计

只读对照概念模型与代码，回答独立性和组合正确性，并检查漂移、判据与产品子集。输出带证据、影响与修复路由的报告；不修改文件。无规格时只审可验证的代码性质，注明不能判断的契约。

## 执行

1. **范围**：查全部 CONCEPT/SYNCS、总体 PRD 及其暂存规格链接，读取当前实现与测试。记录版本、方言、覆盖与未核实部分。
2. **漂移**：读 [drift-checklist.md](references/drift-checklist.md)，逐规格/实现对账，含 schema、动作/query 签名与错误 case。规格多时按该文分批扫描。
3. **独立性**：逐概念核对互引（包括公开 API）、共享可变状态、私有实现访问、传输类型污染及定义依赖。局部类型参数同名不算引用另一概念。
4. **组合**：读 [composition-checklist.md](references/composition-checklist.md)，检查完成事件、绑定、flow 合取/隔离、失败、重放、循环与用户联动。
5. **判据**：以单一目的、完整行为、独立性、熟悉性检查 conflation/fragmentation；新颖与基础设施身份本身不是缺陷，先明确使用者（含 API 程序员）与价值。
6. **依赖/子集**：分别核验 PRD 产品依赖与代码约束；用具体合理子集判断是否被不当耦合阻断，并检查其剩余 sync/入口与构建支持。不能要求产品图与代码图同构。
7. **聚合**：跨规格核对 include、动作/query、参数、输出与图。合并同一根因，保留受影响位置；未执行类别不算通过。

## 报告

```markdown
# 审计报告 <日期>
范围：<规格/代码版本、未核实与跳过原因>
Summary：<覆盖数量、发现数、严重度分布>

| 维度/发现 | 位置 | 当前证据及影响 | 严重度 | 修复路由 |
| --- | --- | --- | --- | --- |

## 独立性与组合覆盖
<每个概念、入口/规则组的结论或未核实项>

## 跨规格与系统性模式
<合并根因并列受影响路径>

## 修复顺序
<模型 → 文档 → 代码，按实际根因决定>
```

严重度按漂移参考中的影响规则校准；规格沉默不等于禁止，新增遗漏与矛盾分开。没有当前证据不报 Medium 以上；只有完整核验后才断言不存在。每条发现一个当前修复目标：模型 → concept-design；文档 → concept-prd；代码 → concept-implementation。存在连续修复阶段时列依赖顺序，不让路由替代根因判断。

交付须覆盖五维、逐概念独立性与逐入口/规则组组合结论，或注明不足。欠/过同步附用户场景；报告全程只读。核验判据出处时读 [sources.md](references/sources.md)；安装包不依赖伴生技能文件才能审计。
