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

账务问题容易答错：粒度不对、口径混用、无表格凭据。本技能在 CLI 层加入
账务语义层，让 Agent 先对齐“要查什么事实”，再选择已验证 BSS 命令，
避免靠 `--help` 猜 API 名或把经典问题当成穷举 FAQ。

需要 KooCLI（`hcloud`）、只读 BSS IAM、网络可达华为云 API。

## 能力边界

支持：找事实、做归因、做对账、做咨询（见 `references/billing-playbook.md` §1）。

不执行支付、续费、退款、回收、创建、修改、删除、停用、关闭、告警配置变更。
遇此类请求，收集只读证据并引导控制台、工单或账号经理。

## 协作模式

1. 只读、授权、最小范围。
2. 将问题映射为事实、维度、指标、时间窗口。
3. 有安全默认时，先说明查询范围再执行。
4. 表格证据先于结论；简单问题短答，复杂归因或对账再展开口径与边界。
5. API 名、字段名、命令摘要默认不进对话；复现/排错/审计时追加 `技术细节`。
6. 无证据禁结论。

## 硬性规则

- 不暴露 AK/SK、Token、完整账号/资源/订单/交易 ID。
- 禁止写操作；`ListCustomerAccountChangeRecords` / `ListCustomerCouponChangeRecords` 是只读流水，允许。
- 产品交叉验证只限 `List` / `Show` / `Get`。
- 没有查询或官网依据时，不下结论。

## 前置检查

未通过则停止，读 `references/cli-installation.md` 指引用户；Agent 不自动安装。

1. `hcloud version` — 确认 CLI 已装。
2. `hcloud configure list` — 确认 profile 与 region。

## 执行协议

执行协议的目的不是把用户话术匹配到 FAQ，而是把问题还原成可查询的账务
事实：事实实体、粒度、时间窗口、账号范围、维度和指标。语义层决定“查什么”，
命令层只负责“怎么查”。

1. 先判断协作目标：找事实、做归因、做对账、做咨询；不要把同一句话强行归到单一经典问题。
2. 从用户问题抽取事实槽位：时间、账号/企业范围、云服务、资源、区域、企业项目、计费模式、金额口径。
3. 用 `references/billing-semantics.md` 和 `references/semantic/*.yml`
   选择最小事实实体；依据是实体粒度、维度、指标和
   `source_operation` / `source_operations`。
4. 在 `references/related-commands.md` 按 Operation 取命令模板，套用
   §默认口径；只在查询会扩大范围或改变结论时追问。
5. 归因链、对账、资源包/代金券抵扣等多事实问题，按
   `references/billing-playbook.md` 组织查询顺序，先汇总后钻取。
6. 用所选事实实体的 `dimensions` / `measures` 组织表格证据，再给小结和
   用户可读说明；证据边界影响结论时才显式列出。
7. 仅 API 报错、Operation 不在命令层、或需要核对本机 KooCLI 参数时，才用
   `hcloud BSS <Op> --help` 兜底。

## 参考文件

| 角色 | 文件 |
| --- | --- |
| 事实硬定义：粒度、维度、指标、来源 Operation | `references/semantic/*.yml` |
| 命令模板 | `references/related-commands.md` |
| 意图判断、多步编排、输出原则 | `references/billing-playbook.md` |
| 语义层说明与术语口径 | `references/billing-semantics.md` |
| 安装与凭据 | `references/cli-installation.md` |
| 最小权限 | `references/iam-policies.md` |

## 默认口径

时间：本月→当前月，上月→最近完整月，最近→近 7 天。账号：当前 profile。
行数：用户查询 `limit=10`，验证 `limit<=3`。多账号：默认 `method=oneself`，
明确企业范围才用 `all`。粒度：先汇总，再钻明细。扩大范围或改变含义时先问。

## 大结果与拒绝

超 50 行 / 8 列 / 3 主维度：对话 TopN + playbook §6；全表写本地报告。
删资源/付款/退款/改余额/导他人账单：拒执行，只给只读路径。
