---
name: huawei-cloud-billing-scout
description: Read-only Huawei Cloud / 华为云 billing and FinOps via KooCLI (hcloud) BSS — balance, invoice, monthly bill, cost allocation, coupon, resource package, reconciliation. Use when user mentions 余额、扣费、账单、成本、对账、代金券、资源包, Huawei Cloud billing, BSS, or FinOps. Refuse payment, delete, refund, or any write operation. Agent does not auto-install hcloud.
license: Apache-2.0
compatibility: Requires hcloud (KooCLI), read-only BSS IAM, outbound network to Huawei Cloud API; user installs CLI manually — agent must not run install scripts.
metadata:
  author: ontology-of-everything
  version: "2.0.0"
  openclaw:
    requires:
      bins:
        - hcloud
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/huawei-cloud-billing-scout
    envVars:
      - name: HUAWEICLOUD_SDK_AK
        required: false
        description: Optional when not using hcloud configure profile; never paste in chat.
      - name: HUAWEICLOUD_SDK_SK
        required: false
        description: Optional when not using hcloud configure profile; never paste in chat.
      - name: HUAWEICLOUD_SDK_REGION
        required: false
        description: Default region (e.g. cn-north-1) when using env-based auth.
---

# 华为云账务技能

> 社区版本，非华为云官方。 / Community edition — not official Huawei Cloud.

只读调查华为云账务（余额、账单、扣费、对账、代金券、资源包等）。按团队约定的顺序：先定事实与口径，再查 BSS，最后给表格证据和小结——不把用户原话当成固定问法去套模板。

## 验收标准

- 从问题中抽出事实、维度、指标、时间、账号范围；路由依据语义实体，而非话术相似度。
- 仅 BSS/KooCLI 只读；拒绝支付、续费、退款、回收及一切写操作。
- 先表格证据后结论；无查询或官网依据不下结论。
- 用户可读说明写清时间范围、账号范围、TopN/行数；对话默认不写 API/字段名（复现/排错/审计时附 `技术细节`）。
- 不输出完整 AK/SK、Token、账号/资源/订单/交易 ID。

## 能力边界

四类目标：找事实、做归因、做对账、做咨询（步骤见 `references/billing-playbook.md` §1）。操作类（支付、删资源等）只留只读证据，引导控制台、工单或账号经理。

## 前置检查

未通过则停止，读 `references/cli-installation.md`；不自动安装。

1. `hcloud version`
2. `hcloud configure list`

## 执行协议

1. **目标**：找事实 / 归因 / 对账 / 咨询（一句可含多目标）。
2. **槽位**：时间、账号/企业范围、云服务、资源、区域、企业项目、计费模式、金额口径。
3. **实体**：`references/billing-semantics.md` + `references/semantic/*.yml`
  → 最小事实实体（粒度、维度、指标、`source_operation(s)`）。
4. **命令**：`references/related-commands.md` 按 Operation + §默认口径；扩大范围或改结论时再问。
5. **编排**：多事实链用 `references/billing-playbook.md`，先汇总后钻取。
6. **输出**：用 `dimensions` / `measures` 制表 → 小结；区分已证实 / 可能解释 / 待核验。
  仅报错、缺 Operation 或核对参数时用 `hcloud BSS <Op> --help`。

## 参考文件

| 用途 | 文件 |
| --- | --- |
| 事实定义 | `references/semantic/*.yml` |
| 命令模板 | `references/related-commands.md` |
| 多步编排 | `references/billing-playbook.md` |
| 术语口径 | `references/billing-semantics.md` |
| 安装凭据 | `references/cli-installation.md` |
| 最小权限 | `references/iam-policies.md` |

## 默认口径

本月→当前月；上月→最近完整月；最近→近 7 天。账号→当前 profile。
查询 `limit=10`，验证 `limit<=3`。多账号默认 `method=oneself`，明确企业范围才 `all`。先汇总后明细。

## 大结果与拒绝

超 50 行 / 8 列 / 3 主维度：对话 TopN + playbook §6；全表写本地报告。
删资源/付款/退款/改余额/导他人账单：拒执行，只给只读路径。
