# 华为云成本估算

`huawei-cloud-cost-estimation` · **Huawei Cloud Pre-Order Cost Estimation — Period & On-Demand via hcloud (Read-Only)**

通过 hcloud BSS 进行确定性的华为云下单前询价（包年/包月 与 按需）。**切勿臆造价格——始终以本次 hcloud 响应为准；模糊不开价——四元未齐先问，再取数。**

*社区技能，非华为云官方；需 hcloud ≥7.2 与 BSS 询价只读 IAM。*

**North Star** — 询价员之笔：四元未齐不开价，价有所本、口径写明；模糊先问，越界不替。

## 能力域

- **Period 包年/包月询价** — `BSS/ListRateOnPeriodDetail`；主 fact `RFQ_Header` / `RFQ_Line`。
- **On-Demand 按需询价** — `BSS/ListOnDemandResourceRatings`；主 fact `RFQ_OnDemand_Header` / `RFQ_OnDemand_Line`。
- **维度查询** — `cloud_service_type` / `resource_type` / `measure_unit` / `usage_type` 字典与换算。
- **规格查询** — ECS/RDS/DCS/EVS flavor 与 AZ；带宽与 EIP 走编码常量表。

## 工作机制

**Phase 1 Analysis → Phase 2 Estimation → Iteration 微调**。

- **Phase 1**：Parse 四元组 + Clarify（一轮问完）+ Spec Review（已确认 / 待补 / 默认）。
- **Phase 2**：最小 hcloud 命令取价；分项展示、分步验算、口径标注。
- **Iteration**：换 region / 改规格只跑受影响项。

## 安全红线

只读 · 不收凭证 · 不泄密 · 不越界（估价不是最终账单；**本技能仅覆盖未发生报价**；历史账单/余额/对账 → 费用中心或 BSS 账单只读 API）· **IM 交付不出 GFM 表格**（`·` 分项 / 短段换行）。

**Version:** 0.3.1
