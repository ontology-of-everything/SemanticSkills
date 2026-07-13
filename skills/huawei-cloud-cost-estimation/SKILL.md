---
name: huawei-cloud-cost-estimation
description: Quotes Huawei Cloud pre-order pricing and runs controlled provisioning/unsubscribe via hcloud. Use whenever the user mentions 华为云 / Huawei Cloud / hcloud with 报价/询价/多少钱/价格/quote/pricing/budget, or asks to 开通/购买/创建 (provision/create) an allowlisted resource (ECS/RDS/CCE/EIP/WAF etc.), or to 退订 (unsubscribe) a yearly/monthly resource. Writes require allowlist + runtime help + --dryrun + explicit confirmation. Refuses cross-cloud, AK/SK intake, payment/renewal/delete, non-allowlisted writes.
compatibility: hcloud KooCLI 7.2+, IAM permissions matching requested read/write operations, outbound network; no agent auto-install
metadata:
  author: ontology-of-everything
  version: "2.0.0"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/huawei-cloud-cost-estimation
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云成本估算与资源开通

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud 响应为准。

价格只认当次响应，**不臆造、不类比、不记忆**；写操作只认白名单 + 运行时 help + `--dryrun` + 用户确认。

## Route

- **询价 / 预算 / 比价** → Pricing。
- **开通 / 购买 / 创建资源** → Lifecycle Create（仅 `references/lifecycle/commands.md` 白名单内）。
- **退订包年/包月资源** → Lifecycle Cancel（仅 `BSS CancelResourcesSubscription`）。
- 历史账单/余额/对账 → 费用中心或 BSS 账单只读 API；非华为云 → 拒绝；白名单外写操作 → 给控制台指引。

## Pricing

1. **Parse** — 抽取四元组 `cloud_service_type / resource_type / region / resource_spec` + 周期或使用量；读 `references/pricing/semantic/catalog.yml` 路由到 period / on-demand 模型。
2. **Clarify** — 缺 region/数量/周期或用量/线性 size，或产品类目模糊、多变种未定 → 停下一轮问完（带 2–4 候选）。仅 safe-default 缺失（OS=linux、AZ=空、`fee_installment_mode=NA`）→ 披露后继续。确认话术用口语四元组，不暴露内部名。
3. **Query** — 按 `references/pricing/commands.md`：先 `BSS/ListResourceSpecs` 实查规格，再询价（period → `ListRateOnPeriodDetail`；on-demand → `ListOnDemandResourceRatings`）；多产品一次放进 `product_infos.N.*`。
4. **Verify & Present** — 分项加和 = 总价；币种/周期/数量对齐用户口径。分项 `[服务] [规格] [region] [数量×周期] = ¥<金额>` + 加总 + 「非最终账单」；默认官网价，响应有折扣才附折后。

## Lifecycle Create

读 `references/lifecycle/concepts.md` 后按序执行，跳步即违规：

1. **Allowlist** — 意图映射到 `references/lifecycle/commands.md` 命令主体；未命中即拒绝。
2. **Help** — `hcloud <Service> <Operation> --help` 取必填/条件必填；`[APIE_ERROR]` 或无 schema 即停止，不猜参数。
3. **Resolve** — 自动跑必要只读依赖查询（VPC/子网/AZ/镜像/规格等）；多候选让用户选，缺失项一轮问完。
4. **Cost** — 能询价先走 Pricing 回表；不能询价则声明「价格未知且可能收费」并取得额外确认。
5. **Dry** — 完整命令强制加全局 `--dryrun`（本地构造请求，非接口级 `dry_run`）；失败则修正重跑，不得转正式。
6. **Confirm** — 回显资源/region/规格/数量/计费/金额或未知费用/批次顺序，等用户明确确认。
7. **Execute** — 仅移除 `--dryrun`，其余不变；多命令顺序执行、失败即停、不自动回滚，报告成功/失败/未执行。

任何参数、region、数量或 operation 变化 → dry 与确认作废，回到 Help 重来。

## Lifecycle Cancel

独立于开通批次，仅 `BSS CancelResourcesSubscription`：help → `--dryrun` → 独立回显（主资源、可能连带资源、退款未知、不可恢复）→ 用户输入明确退订确认 → 移除 `--dryrun` 执行。模糊批量退订（「全部退掉」）不执行；订单 ID ≠ 已停止/已退款，如实转述响应。

## Critical Rules

1. **Never guess prices / params** — 价格只来自当次响应；参数只来自当次 help。
2. **Never skip dry & confirm** — 无 `--dryrun` 成功 + 用户确认，不产生任何真实写调用。
3. **Never accept credentials in chat** — AK/SK/Token 立即拒收，指向 `references/cli-installation.md` 自行配置。
4. **BSS 端点** — `hcloud BSS` 固定 `--cli-region=cn-north-1`；`product_infos.N.region` 仍是资源部署区。
5. **Route, don't refuse blankly** — 超范围请求给出正确去向（费用中心/控制台/只读账单）。

> 输出禁忌：对用户消息不用 GFM 表格，用 `·` 分项或编号；命令级陷阱（dot notation、无分页、code 大小写）见 `references/pricing/commands.md` 顶部。

## Reference Index（按需加载）

| 何时读 | 文件 |
| --- | --- |
| 询价入口 | `references/pricing/semantic/catalog.yml` + `rfq-*.yml` |
| 询价命令 / 响应字段 / 陷阱 | `references/pricing/commands.md` |
| 开通/退订语义与安全 | `references/lifecycle/concepts.md` |
| 开通/退订命令白名单与依赖 | `references/lifecycle/commands.md` |
| 403 或权限问题 | `references/pricing/iam-policies.md` |
| hcloud 未就绪 | `references/cli-installation.md`（**仅转述给用户**，不代为执行） |
