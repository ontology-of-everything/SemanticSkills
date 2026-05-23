# 命令合同附录

本文件只保留 operation 合同：用途、必填、模板和限制。问题路由看 `semantic/catalog.yml`，语义边界看 `semantic/billing-ontology.yml`。

## 命令格式标准

**核心格式**：`hcloud BSS <Operation> --param=value --cli-region=<region> --cli-output=json`

### 格式规则

| 元素 | 格式 | 示例 |
| --- | --- | --- |
| 服务名 | 固定 `BSS` | `hcloud BSS ShowCustomerAccountBalances` |
| 操作名 | `List*` / `Show*` | `ListCosts`, `ShowCustomerMonthlySum` |
| 普通参数 | `--key=value` | `--bill_cycle=2024-12`, `--limit=10` |
| 数组参数 | `--key.1=value1` | `--resource_ids.1=<resource_id>` |
| 嵌套对象 | `--key.sub_key=value` | `--time_condition.begin_time=2024-12-01` |

## 全局约束

- 只执行 `List*` / `Show*`；拒绝支付、续费、退款、退订、回收、创建、更新、删除、发送验证码、改余额或资源。
- 默认 `limit<=10`、`offset=0`；找前置 ID 最多近 3 个账期、每命令 3 页、每页 `limit<=50`。
- 数组和对象参数只用已验证的 dot notation；没有模板就停下，不试 JSON 字符串。
- 账号、客户、资源、订单、交易、券、卡、伙伴 ID 默认脱敏。

## customer_billing

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ShowCustomerAccountBalances` | 余额、欠费、账户构成快照 | - | 当前 profile；只回答当前时点快照 |
| `ShowCustomerMonthlySum` | 月度消费汇总 | `bill_cycle` | 适合总览；多账号前先确认范围 |
| `ListCustomerBillsFeeRecords` | 账期流水、支付状态、交易对账 | `bill_cycle` | 账期日期必须同月 |
| `ListCustomerselfResourceRecords` | 定位持续扣费资源 | `cycle` | 资源 ID 默认脱敏 |
| `ListCustomerselfResourceRecordDetails` | 资源详单日级 | `cycle` | 明细与汇总可能有精度差 |
| `ListCustomerBillsMonthlyBreakDown` | 月度摊销 | `shared_month` | 近 18 月；非现金扣费口径 |
| `ListCustomerAccountChangeRecords` | 账户流水 | `balance_type` | 只读；伙伴转售客户不适用 |
| `ListStoredValueCards` | 储值卡状态和面额 | `status` | 卡 ID 默认脱敏 |

## cost_and_usage

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListCosts` | 成本分析聚合、TopN、趋势 | 见模板 | dot notation；`operator=0` 包含、`1` 排除 |
| `ListResourceUsageSummary` | CDN/OBS/IEC/VPC 用量汇总 | 见模板 | 95 计费与用量核验 |
| `ListResourceUsage` | 资源使用量明细 | 见模板 | 先汇总或详单拿资源与用量类型 |

### cost_and_usage 示例模板

#### `ListCosts`

```bash
hcloud BSS ListCosts \
  --amount_type=<amount_type> \
  --cost_type=<cost_type> \
  --time_condition.begin_time=YYYY-MM-DD \
  --time_condition.end_time=YYYY-MM-DD \
  --time_condition.time_measure_id=1 \
  --groupby.1.key=CLOUD_SERVICE_TYPE \
  --groupby.1.type=dimension \
  --filters.1.filter_factor.key=REGION_CODE \
  --filters.1.filter_factor.value.1=cn-north-1 \
  --filters.1.operator=0 \
  --cli-region=<region> \
  --cli-output=json
```

## discount_entitlement

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListFreeResourceInfos` | 资源包列表 | - | 数组参数只用 `.1`、`.2` 递增；见下方模板 |
| `ListFreeResourceUsages` | 资源包余量 | `free_resource_ids.1` | 通常不分页；见下方模板 |
| `ListFreeResourcesUsageRecords` | 包抵扣明细 | 见模板 | 跨度 ≤90 天 |
| `ListCustomerCouponChangeRecords` | 代金券流水 | `balance_type` | 券 ID、交易 ID 默认脱敏 |
| `ListQuotaCoupons` | 伙伴优惠券额度 | - | 只读额度；见下方模板 |
| `ListIssuedCouponQuotas` | 已发放券额度 | - | 总经销商场景 |
| `ListCouponQuotasRecords` | 券额度操作记录 | - | 只读记录 |
| `ListIssuedPartnerCoupons` | 已发放优惠券 | - | 券 ID、客户 ID 默认脱敏 |
| `ListPartnerCouponsRecord` | 优惠券发放/回收记录 | - | 只读记录；见下方模板 |
| `ListSubCustomerCoupons` | 伙伴自身优惠券 | - | 只读 |
| `ListOrderCouponsByOrderId` | 订单可用券 | `order_id` | 靠近支付，只读解释 |

### discount_entitlement 示例模板

#### `ListFreeResourceInfos`

```bash
hcloud BSS ListFreeResourceInfos \
  --service_type_code_list.1=hws.service.type.obs \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListFreeResourceUsages`

```bash
hcloud BSS ListFreeResourceUsages \
  --free_resource_ids.1=<free_resource_id> \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListQuotaCoupons`

```bash
hcloud BSS ListQuotaCoupons \
  --quota_ids.1=<quota_id> \
  --quota_status_list.1=0 \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListPartnerCouponsRecord`

```bash
hcloud BSS ListPartnerCouponsRecord \
  --coupon_ids.1=<coupon_id> \
  --operation_types.1=1 \
  --cli-region=<region> \
  --cli-output=json
```

## order_evidence

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListCustomerOrders` | 订单列表 | - | 仅查证据，不引导支付 |
| `ShowCustomerOrderDetails` | 订单详情 | `order_id` | 订单 ID 默认脱敏 |
| `ShowRefundOrderDetails` | 退订/降配退款详情 | `order_id` | 只解释退款证据，不执行退订退款 |
| `ListOrderDiscounts` | 订单可用折扣 | `order_id` | 靠近支付，只读解释 |

## enterprise_multi_account

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListEnterpriseOrganizations` | 企业组织结构 | - | 企业主账号场景 |
| `ListEnterpriseSubCustomers` | 企业子账号列表 | - | 子账号 ID 默认脱敏 |
| `ListEnterpriseMultiAccount` | 子账号可回收余额 | 见模板 | 只读；不回收 |
| `ShowMultiAccountTransferAmount` | 主账号可拨款 | `balance_type` | 只读；不划拨 |
| `ListMultiAccountTransferCoupons` | 主账号可拨券 | - | 只读；不发放 |
| `ListMultiAccountRetrieveCoupons` | 子账号可回收券 | `sub_customer_id` | 只读；不回收 |
| `ListConsumeSubCustomers` | 有消费子客户 | `bill_cycle` | 企业/伙伴入口 |
| `ListSubcustomerMonthlyBills` | 子客户月账单 | `cycle`, `charge_mode` | 客户 ID 脱敏 |
| `ListSubCustomerBillDetail` | 子客户明细 | `bill_cycle`, `customer_id` | 先确认授权 |

## partner_resale

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListSubCustomers` | 伙伴客户列表 | - | 客户信息敏感，默认摘要 |
| `ListSubCustomerNewTag` | 新客标签 | - | 只读；见模板 |
| `ListCustomerOnDemandResources` | 代售按需资源 | `customer_id` | 资源 ID 脱敏；见模板 |
| `ListPayPerUseCustomerResources` | 包年包月资源 | - | 历史命名；见模板 |
| `ListCustomersBalancesDetail` | 代售余额 | 见模板 | 敏感；见模板 |
| `ListPartnerBalances` | 伙伴/经销商余额 | - | 伙伴视角 |
| `ListPartnerAccountChangeRecords` | 伙伴收支流水 | `balance_type` | 只读流水 |
| `ListPartnerAdjustRecords` | 伙伴调账记录 | - | 只读记录；不执行拨款或回收 |
| `ListIndirectPartners` | 二级经销商列表 | - | 总经销商场景 |

### partner_resale 示例模板

#### `ListSubCustomerNewTag`

```bash
hcloud BSS ListSubCustomerNewTag \
  --customer_ids.1=<customer_id> \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListCustomerOnDemandResources`

```bash
hcloud BSS ListCustomerOnDemandResources \
  --customer_id=<customer_id> \
  --resource_ids.1=<resource_id> \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListPayPerUseCustomerResources`

```bash
hcloud BSS ListPayPerUseCustomerResources \
  --resource_ids.1=<resource_id> \
  --status_list.1=2 \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListCustomersBalancesDetail`

```bash
hcloud BSS ListCustomersBalancesDetail \
  --customer_infos.1.customer_id=<customer_id> \
  --cli-region=<region> \
  --cli-output=json
```

## reference_dimensions

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListServiceTypes` | 云服务类型字典 | - | 翻译 `service_type_code` |
| `ListResourceTypes` | 资源类型字典 | - | 翻译 `resource_type_code` |
| `ListUsageTypes` | 使用量类型字典 | - | 翻译 `usage_type` |
| `ListMeasureUnits` | 计量单位字典 | - | 翻译金额和用量单位 |
| `ListConversions` | 计量单位进制换算 | - | 用于单位换算 |
| `ListServiceResources` | 服务到资源类型关系 | `service_type_code` | 价格试算前置字典 |
| `ListProvinces` | 省份字典 | - | 伙伴销售平台地域 |
| `ListCities` | 城市字典 | `province_code` | 伙伴销售平台地域 |
| `ListCounties` | 区县字典 | `city_code` | 伙伴销售平台地域 |

## quote_and_identity

| 操作 | 用途 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ListOnDemandResourceRatings` | 按需价格试算 | 见模板 | 只读报价，不等于账单 |
| `ListRateOnPeriodDetail` | 包年包月开通试算 | 见模板 | 只读报价，不引导下单 |
| `ListRenewRateOnPeriod` | 包年包月续订试算 | 见模板 | 只读报价，不引导续订 |
| `ListIncentiveDiscountPolicies` | 产品折扣/激励策略 | `time` | 伙伴视角；不承诺客户最终价 |
| `ShowRealnameAuthenticationReviewResult` | 实名审核 | `customer_id` | 只读；不提交变更 |

### quote_and_identity 示例模板

#### `ListOnDemandResourceRatings`

```bash
hcloud BSS ListOnDemandResourceRatings \
  --project_id=<project_id> \
  --product_infos.1.id=item-1 \
  --product_infos.1.cloud_service_type=<service> \
  --product_infos.1.resource_type=<resource> \
  --product_infos.1.resource_spec=<spec> \
  --product_infos.1.region=<region> \
  --product_infos.1.subscription_num=1 \
  --product_infos.1.usage_factor=Duration \
  --product_infos.1.usage_measure_id=4 \
  --product_infos.1.usage_value=1 \
  --product_infos.1.available_zone=<az> \
  --product_infos.1.resource_size=10 \
  --product_infos.1.size_measure_id=17 \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListRateOnPeriodDetail`

```bash
hcloud BSS ListRateOnPeriodDetail \
  --project_id=<project_id> \
  --product_infos.1.id=item-1 \
  --product_infos.1.cloud_service_type=<service> \
  --product_infos.1.resource_type=<resource> \
  --product_infos.1.resource_spec=<spec> \
  --product_infos.1.region=<region> \
  --product_infos.1.period_num=1 \
  --product_infos.1.period_type=2 \
  --product_infos.1.subscription_num=1 \
  --product_infos.1.available_zone=<az> \
  --product_infos.1.fee_installment_mode=NA \
  --product_infos.1.resource_size=10 \
  --product_infos.1.size_measure_id=17 \
  --cli-region=<region> \
  --cli-output=json
```

#### `ListRenewRateOnPeriod`

```bash
hcloud BSS ListRenewRateOnPeriod \
  --period_num=1 \
  --period_type=2 \
  --resource_ids.1=<resource_id> \
  --cli-region=<region> \
  --cli-output=json
```

## 产品侧只读交叉验证

BSS 是账务事实源。产品 API 只答「当前能否查到资源」，不推翻历史账单；
仅在 BSS 已有线索后，再查产品侧 `List` / `Show` / `Get`。
