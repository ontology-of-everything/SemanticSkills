---
name: huawei-cloud-billing-scout
description: 查询华为云 BSS 账务：余额、扣费、账单、成本、资源包、券、储值卡、订单、企业/伙伴费用和对账归因。只读非官方。
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
        description: 可选临时 AK；优先用本机 profile。
      - name: HUAWEICLOUD_SDK_SK
        required: false
        description: 可选临时 SK；禁止暴露到对话或日志。
      - name: HUAWEICLOUD_SDK_REGION
        required: false
        description: 可选默认区域；通常用当前 profile。
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/huawei-cloud-billing-scout
---

# 华为云计费技能

社区版本，非华为云官方。

用于查找账务事实、解释扣费归因、做口径对账，并给出安全的下一步建议。BSS 是账务事实源；产品 API 和字典只提供上下文。

触发场景包括“为什么一直扣钱”“帮我查上月 OBS”“对不上账”
“这个资源还在收费吗”等口语化表达。

## 原则

- 证据优先。只陈述 BSS 查询结果或官方文档能支撑的结论。证据不完整时，区分已证实、可能解释、待核验。
- 只读边界。只执行 `List*` 和 `Show*` 查询。拒绝支付、续费、退款、退订、回收、更新、创建、删除、发送验证码、改余额、改资源等操作。
- 最小范围。默认当前 profile、窄时间窗、小分页、先汇总。只有问题需要时才扩大范围。
- 保护标识。绝不输出 AK/SK 或 Token。账号、客户、资源、订单、交易、券、伙伴 ID 默认脱敏；用户明确确认后才可用完整 ID 做本机核验。
- 先建模问题，再选命令。先确定意图、事实、维度、金额口径、时间窗和账号范围，再选择 Operation。
- 模糊就协作。扩大到企业 `all`、伙伴客户列表、跨账号数据、大结果导出，或结论依赖缺失前提时，先澄清。

## 资料入口

- 意图和事实路由：先读 `references/semantic/Catalog.yml`，再读匹配的 `references/semantic/*.yml`。
- 命令事实：`references/related-commands.md`。
- 判断原则：`references/billing-playbook.md`。
- 安装与凭据：`references/cli-installation.md`。
- 权限口径：`references/iam-policies.md`。

如果 KooCLI help 与 API Explorer 不一致，说明分歧，并优先采用更窄、更安全的查询。

## 执行边界

环境未知时，先确认 `hcloud version` 和 `hcloud configure list`。不要自动安装 KooCLI，不要让用户在对话里粘贴密钥。

真实查询默认边界：

- `--cli-output=json`, `--limit<=10`, `--offset=0`.
- 为找前置 ID 扩大发现时：最多近 3 个账期、每命令 3 页、每页 `limit<=50`。
- 大结果先摘要；全量导出需确认；评测产物不保存原始账务响应。

## 输出口径

优先给紧凑表格，再给短结论。区分：

- 已证实：查询结果直接支持。
- 可能解释：与事实一致，但尚未被直接证明。
- 待核验：权限、前置 ID、官方文档分歧、产品侧状态或用户范围选择仍缺失。

不要为了模板牺牲清晰度。不要把原始 JSON 倾倒到对话里。
