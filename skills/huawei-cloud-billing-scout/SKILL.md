---
name: huawei-cloud-billing-scout
description: >-
  Verify Huawei Cloud BSS billing (read-only). Use for 余额, 账单, 对账, 储值卡,
  coupons, enterprise fees, or unexpected charges; refuse pay, refund, or delete.
compatibility: hcloud 7.2+；BSS 只读。
metadata:
  openclaw:
    requires:
      bins:
        - hcloud
    primaryEnv: HUAWEICLOUD_SDK_AK
    envVars:
      - name: HUAWEICLOUD_SDK_AK
        required: false
      - name: HUAWEICLOUD_SDK_SK
        required: false
      - name: HUAWEICLOUD_SDK_REGION
        required: false
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/huawei-cloud-billing-scout
---

# 华为云计费技能

社区版、非官方。先按语义本体定事实、范围与金额口径，再最小只读取证，输出事实表与小结。

## 何时使用

- 核对余额、欠费、储值卡和账户流水。
- 解释本月/上月账单、服务排行、摊销成本和成本趋势。
- 定位“为什么扣钱”“删了资源还扣费”“资源包/券没抵扣”。
- 处理控制台、导出、订单、明细之间的对账差异。
- 查询企业主、子账号、伙伴、代售客户的账务范围和费用。
- 只读报价、折扣策略和实名认证结果咨询。

## 核心流程

1. `references/semantic/catalog.yml`：问题类型、范围、时间窗、金额口径。
2. `references/semantic/billing-ontology.yml`：事实、证据边界、BSS operation。
3. `references/related-commands.md`：最小只读查询；复杂参数仅用已验证 dot notation 模板。
4. 按「输出合同」交付；有 `待核验` 时再给最小下一步。

## 核心规则

1. 证据优先：只写 BSS 或官方文档支撑的判断；已证实与 `待核验` 进事实表，未证实解释仅写小结。
2. 只读边界：仅 `List*` / `Show*`；拒绝支付、续费、退款、退订、回收、创建、更新、删除、验证码、改余额或资源。
3. 最小范围：默认当前 profile、窄时间窗、小分页、先汇总；扩企业 `all`、伙伴或跨账号前先确认。
4. 标识保护：不输出 AK/SK/Token；账号、客户、资源、订单、交易、券、卡、伙伴 ID 默认脱敏。
5. 事实不明先协作：缺权限、范围、前置 ID、产品状态或官方口径时澄清，不猜结论。

## 输出合同

- 先归并判断项，再出事实表；不外发原始 JSON、命令过程、完整业务 ID。
- 小结 1–2 句；未证实解释只写小结，带「更可能 / 倾向于」等限定词。
- 仅有 `待核验` 时写「下一步」，且只给最小只读补证。
- 不要把调查负担转交给接收人；profile/region 与调试字段不进答复。

## 运行与输出边界

- 认证用有效 AK/SK profile；未知环境先 `hcloud version` 与 `hcloud configure list`，勿自动安装 CLI。
- 默认 `--cli-output=json`、`--limit<=10`、`--offset=0`；扩 ID 时 ≤3 账期、≤3 页/命令、`limit<=50`。
- 范围受限结果不得扩大成整月、所有服务、最终出账或已确认账单。
