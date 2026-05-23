---
name: huawei-cloud-billing-scout
description: >-
  Verify Huawei Cloud BSS billing and charge attribution (read-only). Use this
  skill when the user mentions 余额, 账单, 对账, 储值卡, coupons, enterprise
  fees, or unexpected charges; refuse pay, refund, or delete.
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

社区版，非华为云官方。核心方法：先按语义本体确认事实、范围和金额口径，再用最小只读命令取证，最后输出事实表和小结。

## 何时使用

- 核对余额、欠费、储值卡和账户流水。
- 解释本月/上月账单、服务排行、摊销成本和成本趋势。
- 定位“为什么扣钱”“删了资源还扣费”“资源包/券没抵扣”。
- 处理控制台、导出、订单、明细之间的对账差异。
- 查询企业主、子账号、伙伴、代售客户的账务范围和费用。
- 做只读报价、折扣策略和实名认证结果咨询。

## 核心流程

1. 先读 `references/semantic/catalog.yml`，识别问题类型、范围、时间窗和金额口径。
2. 再读 `references/semantic/billing-ontology.yml`，确认事实、证据边界和需要的 BSS operation。
3. 再按 `references/related-commands.md` 执行最小只读查询；复杂参数只用已验证的 dot notation 模板。
4. 最终按「输出合同」交付；有待核验项时再给最小下一步。

## 核心规则

1. 证据优先：只写 BSS 查询或官方文档支撑的判断；证据不足时只把已证实事实和待核验项放进事实表，未直接证实的解释只允许写进小结。
2. 只读边界：只执行 `List*` / `Show*` 查询；拒绝支付、续费、退款、退订、回收、创建、更新、删除、发验证码、改余额或资源。
3. 最小范围：默认当前 profile、窄时间窗、小分页、先汇总；扩大到企业 `all`、伙伴客户、跨账号前先确认。
4. 标识保护：绝不输出 AK/SK/Token；账号、客户、资源、订单、交易、券、卡、伙伴 ID 默认脱敏。
5. 事实不明就协作：权限、范围、前置 ID、产品状态或官方口径缺失时先澄清，不猜测补结论。

## 输出合同

- 先归并判断项，再出事实表；不外发原始 JSON、命令过程、完整业务 ID。
- 小结 1–2 句；未证实解释只写小结，并带「更可能 / 倾向于」等限定词。
- 仅有 `待核验` 时写「下一步」，且只给最小只读补证。
- 不要把调查负担转交给接收人；profile/region 与调试字段不进答复。

## 引用文件

- `references/semantic/catalog.yml`：问题路由。
- `references/semantic/billing-ontology.yml`：事实、范围、金额口径和证据边界。
- `references/related-commands.md`：operation 合同、模板和限制。

## 运行与输出边界

- 认证用有效 AK/SK profile；未知环境先 `hcloud version` 与 `hcloud configure list`，勿自动安装 CLI。
- 默认 `--cli-output=json`、`--limit<=10`、`--offset=0`；扩 ID 时 ≤3 账期、≤3 页/命令、`limit<=50`。
- 只保留帮助判断和行动的信息；范围受限结果不得扩大成整月、所有服务、最终出账或已确认账单。

