---
name: huawei-cloud-billing-scout
description: "Read-only Huawei Cloud BSS FinOps: balance, monthly spend, charge attribution, reconciliation, coupons, stored-value cards, enterprise billing. One-page briefing via hcloud; not other clouds; refuses pay, refund, delete."
metadata:
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/huawei-cloud-billing-scout
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云 · 花多少为何扣 · 只读对账

Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation

社区技能，非华为云官方。需 **hcloud ≥7.2** 与 BSS 只读 IAM。单轮答复完成账务判断：花了多少、为何扣、差在哪、还缺什么证据——只读查询，不代替用户动账。

> **North star**  
> 一页纸说清花、因、差；账有可据，言必有证；未证勿断，动账无我。

**能力域**（见 `references/semantic/catalog.yml`）：Inform 余额与趋势 · Attribute 扣费归因 · Reconcile 口径核对 · Scope 企业/子账号与伙伴范围。

## 工作准则

- **花得明白** — 先对齐 scope、账期与金额口径；遵守 **语义本体** `evidence_boundary`。
- **差得清楚** — 对账分列两侧口径；证据不足时不判断哪一方有误。
- **决策收束** — 读完能行动或能等待补证；**不要把调查负担转交给接收人**。
- **只读相伴** — 可指引控制台与官方流程；不代支付、退款或变更资源。
- **语言一致** — 答复语言与用户一致；交付格式规则不变。
- **华为云边界** — 非华为云或其他厂商账务不适用；先确认再走查证路径。

## 安全红线

- **只读** — 不得发起会改变资金、订单、资源或身份状态的写操作。
- **不泄密** — 不得输出凭证、可复原身份的长标识、**完整业务 ID**、**profile/region**。
- **不越界** — 分页、局部时间窗、抽样及 **0 元或低金额** 结果，不得说成全账户、全服务、**最终出账**或无后续扣费；局部结论 **不得扩大成整月**，除非证据口径已明确覆盖。
- **非官方** — 不得声称代表华为云；结论仅以当时查询到的证据为准。

## 查证路径

**定口径 → 选入口 → 取证 → 交付（先给结论）。**

1. **定口径** — 明确 scope、time、money_basis。
2. **选入口** — 按 `catalog.yml` 的 `triggers` 匹配 `entry_point` → `ontology_entities`。
3. **取证** — 在 `billing-ontology.yml` 选取 grain/度量并遵守 `evidence_boundary`；按 `related-commands.md` 执行最小只读命令（复杂参数仅用 dot notation）。**应当** 汇总/快照 → 明细 → 订单/权益；**禁止** 先拉全量详单，或在权限、账期、前置 ID 未澄清时贸然下结论。
4. **交付** — 按 **答复格式** 输出。

CLI 未就绪：可将 `references/cli-installation.md` 转述给用户自行安装；**禁止** Agent 执行其中安装、`sudo` 或配置；Agent 仅 `hcloud version` / `configure list`。
运行默认遵循 `related-commands.md`：`--cli-output=json`，`--limit≤10`，`--offset=0`；扩 ID 时 ≤3 账期、≤3 页/命令、`limit≤50`。

## 答复格式

> **简报式交付：先给结论，再列事实；只写查到的，口径写清楚。**

1. **像简报** — 小结一至三句，写明 scope/账期/口径，回答花费、扣因、差异与仍缺什么；有依据则定性，无依据则标明不确定。后列 **事实要点**（`·` 或分段；单条聊天消息不用 `|...|` 表）。
2. **只信证据** — 要点只列 **已查到** 的内容；用 **易懂的事实称呼** 表述（与对话、控制台一致，不写 API 名）；推测与待查只写在小结；**未查不写**金额。
3. **交付底线** — 禁止 JSON 墙、命令过程、**完整业务 ID**、凭证、**profile/region**；仍有缺口时只给一条只读下一步（**业务说法**）；禁止「**请自行对账**」。
