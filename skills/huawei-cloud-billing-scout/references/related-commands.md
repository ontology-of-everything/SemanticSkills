# BSS 查询命令目录

命令层只记录事实：Operation、用途、必填、关键筛选、限制、前置依赖。意图路由看
`semantic/*.yml`；账务判断看 `billing-playbook.md`。本文件来自 KooCLI 7.2.2
`hcloud BSS --help` 与 `hcloud BSS <Operation> --help`。

## 全局约束

```bash
hcloud BSS <Operation> --cli-region=<region> --cli-output=json
```

- 只执行 `List*` / `Show*`。拒绝 `Pay*`、`Create*`、`Update*`、`Cancel*`、`Renewal*`、`Reclaim*`、`Set*`、`Send*`、`Change*`。
- 探索默认 `limit<=10`、`offset=0`；为找前置 ID 最多近 3 个账期、每命令 3 页、每页 `limit<=50`。
- 账号、客户、资源、订单、交易、券 ID 默认脱敏；用户明确确认后才可用完整 ID 做本机核验。
- KooCLI help 与官方 API Explorer 不一致时，标出分歧，不猜参数。

## 普通客户账务事实

### `ShowCustomerAccountBalances`

- 事实：余额、欠费、账户构成
- 必填：无
- 筛选：无
- 备注：当前 profile；余额是快照，不解释扣费原因

### `ShowCustomerMonthlySum`

- 事实：月度消费汇总
- 必填：
  - `bill_cycle`
- 筛选：
  - `service_type_code`
  - `enterprise_project_id`
  - `method`
  - `sub_customer_id`
  - `limit`
  - `offset`
- 备注：适合总览；多账号需明确范围

### `ListCustomerBillsFeeRecords`

- 事实：消费流水账单
- 必填：
  - `bill_cycle`
- 筛选：
  - `bill_date_begin/end`
  - `service_type_code`
  - `resource_type_code`
  - `region_code`
  - `enterprise_project_id`
  - `method`
  - `sub_customer_id`
  - `trade_id`
  - `status`
  - `limit`
  - `offset`
- 备注：适合对账；账期日期必须同月

### `ListCustomerselfResourceRecords`

- 事实：资源消费记录
- 必填：
  - `cycle`
- 筛选：
  - `bill_date_begin/end`
  - `cloud_service_type`
  - `resource_type`
  - `resource_id`
  - `region`
  - `enterprise_project_id`
  - `charge_mode`
  - `bill_type`
  - `trade_id`
  - `method`
  - `sub_customer_id`
  - `limit`
  - `offset`
- 备注：定位持续扣费资源；资源 ID 脱敏

### `ListCustomerselfResourceRecordDetails`

- 事实：资源详单
- 必填：
  - `cycle`
- 筛选：
  - `query_type`
  - `bill_cycle_begin/end`
  - `cloud_service_type`
  - `resource_type`
  - `res_instance_id`
  - `region`
  - `enterprise_project_id`
  - `charge_mode`
  - `bill_type`
  - `payer_account_id`
  - `method`
  - `sub_customer_id`
  - `limit`
  - `offset`
- 备注：明细金额可能保留多位小数，不宜逐行硬对汇总

### `ListCustomerBillsMonthlyBreakDown`

- 事实：月度摊销成本
- 必填：
  - `shared_month`
- 筛选：
  - `service_type_code`
  - `resource_type_code`
  - `resource_id`
  - `region_code`
  - `enterprise_project_id`
  - `method`
  - `sub_customer_id`
  - `limit`
  - `offset`
- 备注：近 18 个月；摊销口径不同于现金扣费

### `ListCustomerAccountChangeRecords`

- 事实：现金/授信/储值流水
- 必填：
  - `balance_type`
- 筛选：
  - `trade_time_begin/end`
  - `trade_type`
  - `revenue_expense_type`
  - `trade_id`
  - `payment_channel_id`
  - `limit`
  - `offset`
- 备注：只读流水；不适用于伙伴转售类客户

### `ListCustomerCouponChangeRecords`

- 事实：代金券流水
- 必填：
  - `balance_type`
- 筛选：
  - `trade_time_begin/end`
  - `coupon_id`
  - `trade_type`
  - `revenue_expense_type`
  - `trade_id`
  - `limit`
  - `offset`
- 备注：只读流水；券 ID/交易 ID 脱敏

### `ListStoredValueCards`

- 事实：储值卡列表
- 必填：
  - `status`
- 筛选：
  - `card_id`
  - `limit`
  - `offset`
- 备注：储值卡 ID 脱敏

## 成本、用量、抵扣

### `ListCosts`

- 事实：成本分析聚合
- 必填：
  - `amount_type`
  - `cost_type`
  - `time_condition.begin_time`
  - `time_condition.end_time`
  - `time_condition.time_measure_id`
- 筛选：
  - `groupby.*`
  - `filters.*`
  - `limit`
  - `offset`
- 备注：大结果先用它聚合；`operator=0` 包含，`1` 排除

### `ListResourceUsageSummary`

- 事实：资源使用量汇总
- 必填：
  - `bill_cycle`
  - `service_type_code`
  - `resource_type_code`
  - `usage_type`
- 筛选：
  - `limit`
  - `offset`
- 备注：仅 CDN/OBS/IEC/VPC，主要 95 计费场景

### `ListResourceUsage`

- 事实：资源使用量明细
- 必填：
  - `bill_cycle`
  - `resource_id`
  - `service_type_code`
  - `resource_type_code`
  - `usage_type`
- 筛选：
  - `limit`
  - `offset`
- 备注：先用汇总或详单拿资源与用量类型

### `ListFreeResourceInfos`

- 事实：资源包列表
- 必填：无
- 筛选：
  - `product_id`
  - `product_name`
  - `status`
  - `region_code`
  - `enterprise_project_id`
  - `order_id`
  - `service_type_code_list.*`
  - `limit`
  - `offset`
- 备注：抵扣排查入口

### `ListFreeResourceUsages`

- 事实：资源包余量
- 必填：无
- 筛选：
  - `free_resource_ids.*`
- 备注：先从资源包列表拿资源项 ID；通常不分页

### `ListFreeResourcesUsageRecords`

- 事实：资源包抵扣明细
- 必填：
  - `deduct_time_begin`
  - `deduct_time_end`
- 筛选：
  - `free_resource_id`
  - `product_id`
  - `resource_type_code`
  - `limit`
  - `offset`
- 备注：时间跨度不超过 90 天

## 订单与退款证据

### `ListCustomerOrders`

- 事实：订单列表
- 必填：无
- 筛选：
  - `order_id`
  - `customer_id`
  - `service_type_code`
  - `status`
  - `method`
  - `create_time_begin/end`
  - `limit`
  - `offset`
- 备注：仅查证据，不引导支付

### `ShowCustomerOrderDetails`

- 事实：订单详情
- 必填：
  - `order_id`
- 筛选：
  - `indirect_partner_id`
  - `limit`
  - `offset`
- 备注：订单 ID 默认脱敏

### `ShowRefundOrderDetails`

- 事实：退订/降配退款详情
- 必填：
  - `order_id`
- 筛选：
  - `customer_id`
  - `indirect_partner_id`
- 备注：只解释退款证据，不执行退订退款

### `ListOrderCouponsByOrderId`

- 事实：订单可用券
- 必填：
  - `order_id`
- 筛选：无
- 备注：靠近支付，只读解释

### `ListOrderDiscounts`

- 事实：订单可用折扣
- 必填：
  - `order_id`
- 筛选：无
- 备注：靠近支付，只读解释

## 企业、多账号、伙伴

### `ListEnterpriseOrganizations`

- 事实：企业组织结构
- 必填：无
- 筛选：
  - `parent_id`
  - `recursive_query`
- 备注：企业主账号场景

### `ListEnterpriseSubCustomers`

- 事实：企业子账号列表
- 必填：无
- 筛选：
  - `org_id`
  - `fuzzy_query`
  - `sub_customer_account_name`
  - `sub_customer_display_name`
  - `limit`
  - `offset`
- 备注：子账号 ID 脱敏

### `ListEnterpriseMultiAccount`

- 事实：企业子账号可回收余额
- 必填：
  - `balance_type`
  - `sub_customer_id`
- 筛选：
  - `limit`
  - `offset`
- 备注：只读查询；不执行回收

### `ShowMultiAccountTransferAmount`

- 事实：企业主可拨款余额
- 必填：
  - `balance_type`
- 筛选：
  - `limit`
  - `offset`
- 备注：只读查询；不执行划拨

### `ListMultiAccountTransferCoupons`

- 事实：企业主可拨款优惠券
- 必填：无
- 筛选：
  - `limit`
  - `offset`
- 备注：只读查询；不执行发放

### `ListMultiAccountRetrieveCoupons`

- 事实：企业子账号可回收优惠券
- 必填：
  - `sub_customer_id`
- 筛选：
  - `limit`
  - `offset`
- 备注：只读查询；不执行回收

### `ListConsumeSubCustomers`

- 事实：有消费的子客户
- 必填：
  - `bill_cycle`
- 筛选：
  - `limit`
  - `offset`
- 备注：伙伴/企业消费入口

### `ListSubcustomerMonthlyBills`

- 事实：子客户月度账单
- 必填：
  - `cycle`
  - `charge_mode`
- 筛选：
  - `customer_id`
  - `indirect_partner_id`
  - `bill_type`
  - `cloud_service_type`
  - `limit`
  - `offset`
- 备注：伙伴视角；客户 ID 脱敏

### `ListSubCustomerBillDetail`

- 事实：子客户消费明细
- 必填：
  - `bill_cycle`
  - `customer_id`
- 筛选：
  - `bill_date_begin/end`
  - `service_type_code`
  - `region_code`
  - `resource_id`
  - `limit`
  - `offset`
- 备注：伙伴视角；先确认授权关系

### `ListSubCustomers`

- 事实：伙伴客户列表
- 必填：无
- 筛选：
  - `customer_id`
  - `account_name`
  - `associated_on_begin/end`
  - `association_type`
  - `limit`
  - `offset`
- 备注：客户信息敏感，默认摘要

### `ListSubCustomerNewTag`

- 事实：客户新客标签
- 必填：无
- 筛选：
  - `indirect_partner_id`
  - `limit`
  - `offset`
- 备注：只读标签，不做资格承诺

### `ListCustomerOnDemandResources`

- 事实：代售客户按需资源
- 必填：
  - `customer_id`
- 筛选：
  - `service_type_code`
  - `region_code`
  - `status`
  - `limit`
  - `offset`
- 备注：伙伴/代售；资源 ID 脱敏

### `ListPayPerUseCustomerResources`

- 事实：包年包月资源
- 必填：无
- 筛选：
  - `customer_id`
  - `order_id`
  - `service_type_code`
  - `limit`
  - `offset`
- 备注：命名历史原因，实际查包年包月资源

### `ListCustomersBalancesDetail`

- 事实：代售客户余额
- 必填：无
- 筛选：
  - `indirect_partner_id`
- 备注：伙伴视角；客户余额敏感

### `ListPartnerBalances`

- 事实：伙伴/经销商余额
- 必填：无
- 筛选：
  - `indirect_partner_id`
- 备注：伙伴视角

### `ListPartnerAccountChangeRecords`

- 事实：伙伴收支流水
- 必填：
  - `balance_type`
- 筛选：
  - `trade_time_begin/end`
  - `trade_type`
  - `revenue_expense_type`
  - `limit`
  - `offset`
- 备注：只读流水

### `ListPartnerAdjustRecords`

- 事实：伙伴调账记录
- 必填：无
- 筛选：
  - `customer_id`
  - `indirect_partner_id`
  - `operation_time_begin/end`
  - `limit`
  - `offset`
- 备注：只读记录；不执行拨款/回收

### `ListIndirectPartners`

- 事实：二级经销商列表
- 必填：无
- 筛选：
  - `indirect_partner_id`
  - `account_name`
  - `associated_on_begin/end`
  - `limit`
  - `offset`
- 备注：总经销商场景

## 券、额度、伙伴营销

### `ListSubCustomerCoupons`

- 事实：伙伴自身优惠券
- 必填：无
- 筛选：
  - `order_id`
  - `status`
  - `limit`
  - `offset`
- 备注：只读

### `ListIssuedPartnerCoupons`

- 事实：已发放优惠券
- 必填：无
- 筛选：
  - `customer_id`
  - `order_id`
  - `status`
  - `limit`
  - `offset`
- 备注：只读；券/客户 ID 脱敏

### `ListPartnerCouponsRecord`

- 事实：优惠券发放/回收记录
- 必填：无
- 筛选：
  - `customer_id`
  - `indirect_partner_id`
  - `operation_time_begin/end`
  - `limit`
  - `offset`
- 备注：只读记录

### `ListQuotaCoupons`

- 事实：伙伴优惠券额度
- 必填：无
- 筛选：
  - `create_time_begin/end`
  - `effective_time_begin/end`
  - `expire_time_begin/end`
  - `limit`
  - `offset`
- 备注：只读额度

### `ListIssuedCouponQuotas`

- 事实：已发放券额度
- 必填：无
- 筛选：
  - `quota_id`
  - `parent_quota_id`
  - `indirect_partner_id`
  - `limit`
  - `offset`
- 备注：总经销商场景

### `ListCouponQuotasRecords`

- 事实：券额度操作记录
- 必填：无
- 筛选：
  - `indirect_partner_id`
  - `operation_time_begin/end`
  - `operation_type`
  - `limit`
  - `offset`
- 备注：只读记录

## 字典、地域、价格、实名

### `ListServiceTypes`

- 用途：云服务类型字典
- 必填：无
- 筛选：
  - `service_type_name`
  - `limit`
  - `offset`
- 备注：翻译 `service_type_code`

### `ListResourceTypes`

- 用途：资源类型字典
- 必填：无
- 筛选：
  - `limit`
  - `offset`
- 备注：翻译 `resource_type_code`

### `ListUsageTypes`

- 用途：使用量类型字典
- 必填：无
- 筛选：
  - `resource_type_code`
  - `limit`
  - `offset`
- 备注：翻译 `usage_type`

### `ListMeasureUnits`

- 用途：计量单位字典
- 必填：无
- 筛选：无
- 备注：翻译金额/用量单位

### `ListConversions`

- 用途：计量单位进制换算
- 必填：无
- 筛选：
  - `measure_type`
- 备注：用于单位换算

### `ListServiceResources`

- 用途：服务到资源类型关系
- 必填：
  - `service_type_code`
- 筛选：
  - `limit`
  - `offset`
- 备注：价格试算前置字典

### `ListProvinces`

- 用途：省份字典
- 必填：无
- 筛选：
  - `limit`
  - `offset`
- 备注：伙伴销售平台地域

### `ListCities`

- 用途：城市字典
- 必填：
  - `province_code`
- 筛选：
  - `limit`
  - `offset`
- 备注：伙伴销售平台地域

### `ListCounties`

- 用途：区县字典
- 必填：
  - `city_code`
- 筛选：
  - `limit`
  - `offset`
- 备注：伙伴销售平台地域

### `ListOnDemandResourceRatings`

- 用途：按需产品价格试算
- 必填：
  - `project_id`
- 筛选：
  - `inquiry_precision`
- 备注：只读报价，不等于实际账单

### `ListRateOnPeriodDetail`

- 用途：包年包月开通价格试算
- 必填：
  - `project_id`
- 筛选：无
- 备注：只读报价，不引导下单

### `ListRenewRateOnPeriod`

- 用途：包年包月续订价格试算
- 必填：
  - `period_num`
  - `period_type`
- 筛选：
  - `include_relative_resources`
- 备注：只读报价，不引导续订

### `ListIncentiveDiscountPolicies`

- 用途：产品折扣/激励策略
- 必填：
  - `time`
- 筛选：
  - `service_type_code`
  - `limit`
  - `offset`
- 备注：伙伴视角；不承诺客户最终价

### `ShowRealnameAuthenticationReviewResult`

- 用途：实名认证审核结果
- 必填：
  - `customer_id`
- 筛选：无
- 备注：只读结果，不提交/变更实名

## 产品侧只读交叉验证

BSS 是账务事实源。产品 API 只回答“当前资源侧能否查到”，不能推翻历史账单。
仅在 BSS 已给出服务和资源线索后，查相应服务的 `List` / `Show` / `Get`。
