# KooCLI 命令层

只记录查询类命令事实。语义层已经决定要查哪个事实实体后，Agent 才进入本文件
取 Operation 模板；这里不承担用户意图匹配。维护者更新模板前用 `--help`
核对本机 KooCLI。Agent 仅 API 报错、Operation 未知或参数需要核验时才查 help。

## 全局规则

```bash
hcloud configure list
hcloud BSS <Operation> ...   # 见下文各节
# fallback: hcloud BSS <Operation> --help
```

| 参数 | 用途 |
| --- | --- |
| `--cli-region=<region>` | KooCLI 必填区域；BSS 仍需要传 |
| `--limit=<n>` | 探索时小值；用户确认后再分页 |
| `--offset=<n>` | 分页 |
| `--cli-output=json` | 便于解析 |
| `--cli-query=<expr>` | JMESPath 过滤/脱敏 |
| `--cli-read-timeout=<sec>` | 大账单查询可调高 |

默认从小范围、低行数、可解释的汇总开始。需要归因或对账时，再按 playbook
从汇总钻到记录、详单、流水或产品侧只读核验。

禁止执行支付、续费、退款、退订、回收、创建、修改、删除、停用、关闭、
告警配置变更等写操作。`ListCustomerAccountChangeRecords` 和
`ListCustomerCouponChangeRecords` 是只读流水证据，不属于写操作。

## 余额与欠费

```bash
hcloud BSS ShowCustomerAccountBalances --cli-region=<region>
```

用途：当前余额、欠费金额、现金/授信/储值构成。

已验证结构：`account_balances`、`debt_amount`、`measure_id`、`currency`。

## 月度汇总

```bash
hcloud BSS ShowCustomerMonthlySum \
  --bill_cycle=<YYYY-MM> \
  --limit=10 \
  --offset=0 \
  --cli-region=<region>
```

| 参数 | 语义 |
| --- | --- |
| `--service_type_code=<code>` | 云服务类型 |
| `--enterprise_project_id=<id>` | 企业项目 |
| `--method=oneself\|sub_customer\|all` | 查询范围 |
| `--sub_customer_id=<id>` | 指定子客户 |

用途：月度总览、产品占比、计费模式差异、现金/券/储值/欠费拆分。

## 资源消费记录

```bash
hcloud BSS ListCustomerselfResourceRecords \
  --cycle=<YYYY-MM> \
  --limit=10 \
  --offset=0 \
  --cli-region=<region>
```

| 参数 | 语义 |
| --- | --- |
| `--bill_date_begin=<YYYY-MM-DD>` | 月内开始日 |
| `--bill_date_end=<YYYY-MM-DD>` | 月内结束日 |
| `--bill_type=<n>` | 账单类型 |
| `--charge_mode=1\|3\|10\|11` | 包周期/按需/预留/节省计划 |
| `--cloud_service_type=<code>` | 云服务 |
| `--enterprise_project_id=<id>` | 企业项目 |
| `--region=<region-code>` | 资源区域 |
| `--resource_id=<id>` | 资源 ID |
| `--trade_id=<id>` | 订单或交易 ID |
| `--statistic_type=1\|3` | 按账期/按明细 |
| `--method=oneself\|sub_customer\|all` | 查询范围 |
| `--sub_customer_id=<id>` | 指定子客户 |

用途：定位持续扣费资源、产品/区域/资源归因、删除后仍扣费排查。

## 资源详单

```bash
hcloud BSS ListCustomerselfResourceRecordDetails \
  --cycle=<YYYY-MM> \
  --statistic_type=3 \
  --limit=10 \
  --offset=0 \
  --cli-region=<region>
```

日级查询：

```bash
hcloud BSS ListCustomerselfResourceRecordDetails \
  --cycle=<YYYY-MM> \
  --query_type=DAILY \
  --bill_cycle_begin=<YYYY-MM-DD> \
  --bill_cycle_end=<YYYY-MM-DD> \
  --statistic_type=3 \
  --limit=10 \
  --cli-region=<region>
```

用途：用量、金额构成、日级对比、按资源/企业项目/计费模式钻取。

| 参数 | 语义 |
| --- | --- |
| `--bill_type=<n>` | 账单类型 |
| `--charge_mode=1\|3\|10\|11` | 计费模式 |
| `--cloud_service_type=<code>` | 云服务 |
| `--enterprise_project_id=<id>` | 企业项目 |
| `--region=<region-code>` | 资源区域 |
| `--res_instance_id=<id>` | 资源实例 ID |
| `--resource_type=<code>` | 资源类型 |
| `--method=oneself\|sub_customer\|all` | 查询范围 |
| `--sub_customer_id=<id>` | 指定子客户 |
| `--payer_account_id=<id>` | 支付账号 |

注意：资源维度可能保留 8 位小数原始金额，账户扣费按分扣减；资源详单与消费汇总不适合直接逐行对账。

## 成本分析

```bash
hcloud BSS ListCosts \
  --amount_type=PAYMENT_AMOUNT \
  --cost_type=ORIGINAL_COST \
  --time_condition.begin_time=<YYYY-MM-DD> \
  --time_condition.end_time=<YYYY-MM-DD> \
  --time_condition.time_measure_id=1 \
  --groupby.1.type=dimension \
  --groupby.1.key=CLOUD_SERVICE_TYPE \
  --limit=10 \
  --cli-region=<region>
```

过滤条件使用 `filters`。`operator=0` 表示仅包含，`operator=1` 表示仅排除。

```bash
--filters.1.filter_factor.key=ENTERPRISE_PROJECT_ID \
--filters.1.filter_factor.value.1=<enterprise-project-id> \
--filters.1.operator=0
```

| 分组维度 | 用途 |
| --- | --- |
| `CLOUD_SERVICE_TYPE` | 云服务 |
| `RESOURCE_TYPE` | 资源类型 |
| `ASSOCIATED_ACCOUNT` | 关联账号 |
| `REGION_CODE` | 区域 |
| `ENTERPRISE_PROJECT_ID` | 企业项目 |
| `CHARGING_MODE` | 计费模式 |
| `USAGE_TYPE` | 使用量类型 |
| `BILL_TYPE` | 账单类型 |
| `PAYER_ACCOUNT_ID` | 支付账号 |
| `RESOURCE_ID` | 资源 |

| 过滤维度 | 用途 |
| --- | --- |
| `CLOUD_SERVICE_TYPE` | 限定云服务，如 OBS |
| `REGION_CODE` | 限定区域，如 `cn-south-1` |
| `ENTERPRISE_PROJECT_ID` | 限定企业项目 |
| `CHARGING_MODE` | 限定计费模式 |
| `RESOURCE_TYPE` | 限定资源类型 |
| `USAGE_TYPE` | 限定使用量类型 |
| `BILL_TYPE` | 限定账单类型 |
| `RESOURCE_ID` | 限定资源 |
| `ASSOCIATED_ACCOUNT` | 限定关联账号 |
| `PAYER_ACCOUNT_ID` | 限定支付账号 |

上月华南一区 OBS 按企业项目拆分：

```bash
hcloud BSS ListCosts \
  --amount_type=PAYMENT_AMOUNT \
  --cost_type=ORIGINAL_COST \
  --time_condition.begin_time=<last-month-YYYY-MM-DD> \
  --time_condition.end_time=<last-month-YYYY-MM-DD> \
  --time_condition.time_measure_id=1 \
  --groupby.1.type=dimension \
  --groupby.1.key=ENTERPRISE_PROJECT_ID \
  --filters.1.filter_factor.key=CLOUD_SERVICE_TYPE \
  --filters.1.filter_factor.value.1=<OBS-service-code> \
  --filters.1.operator=0 \
  --filters.2.filter_factor.key=REGION_CODE \
  --filters.2.filter_factor.value.1=cn-south-1 \
  --filters.2.operator=0 \
  --limit=10 \
  --offset=0 \
  --cli-region=<region>
```

企业项目本月按计费模式拆分：

```bash
hcloud BSS ListCosts \
  --amount_type=PAYMENT_AMOUNT \
  --cost_type=ORIGINAL_COST \
  --time_condition.begin_time=<month-start-YYYY-MM-DD> \
  --time_condition.end_time=<today-YYYY-MM-DD> \
  --time_condition.time_measure_id=1 \
  --groupby.1.type=dimension \
  --groupby.1.key=CHARGING_MODE \
  --filters.1.filter_factor.key=ENTERPRISE_PROJECT_ID \
  --filters.1.filter_factor.value.1=<enterprise-project-id> \
  --filters.1.operator=0 \
  --limit=10 \
  --offset=0 \
  --cli-region=<region>
```

用途：TopN、趋势、多维汇总。大数据量优先用成本分析，再钻详单。

## 代金券、储值卡、资源包

```bash
hcloud BSS ListCustomerCouponChangeRecords \
  --balance_type=BALANCE_TYPE_COUPON \
  --trade_time_begin=<YYYY-MM-DD> \
  --trade_time_end=<YYYY-MM-DD> \
  --limit=10 \
  --cli-region=<region>

hcloud BSS ListCustomerAccountChangeRecords \
  --balance_type=BALANCE_TYPE_DEBIT \
  --trade_time_begin=<YYYY-MM-DD> \
  --trade_time_end=<YYYY-MM-DD> \
  --limit=10 \
  --cli-region=<region>

hcloud BSS ListStoredValueCards --status=1 --limit=10 --cli-region=<region>
```

`ListCustomerCouponChangeRecords` 可选参数：

| 参数 | 语义 |
| --- | --- |
| `--offset=<n>` | 分页偏移 |
| `--coupon_id=<id>` | 优惠券 ID |
| `--trade_type=<n>` | 交易类型 |
| `--revenue_expense_type=<n>` | 收入或支出 |
| `--trade_id=<id>` | 交易 ID |

`ListCustomerAccountChangeRecords` 可选参数：

| 参数 | 语义 |
| --- | --- |
| `--offset=<n>` | 分页偏移 |
| `--trade_type=<n>` | 交易类型 |
| `--revenue_expense_type=<n>` | 收入或支出 |
| `--trade_id=<id>` | 交易 ID |
| `--payment_channel_id=<id>` | 支付渠道 |
| `--payment_channel_no=<no>` | 支付渠道号 |

资源包：

```bash
hcloud BSS ListFreeResourceInfos --limit=10 --cli-region=<region>

hcloud BSS ListFreeResourceUsages \
  --free_resource_ids.1=<free-resource-id> \
  --cli-region=<region>

hcloud BSS ListFreeResourcesUsageRecords \
  --deduct_time_begin=<YYYY-MM-DD> \
  --deduct_time_end=<YYYY-MM-DD> \
  --limit=10 \
  --cli-region=<region>
```

`ListFreeResourceInfos` 可选参数：

| 参数 | 语义 |
| --- | --- |
| `--offset=<n>` | 分页偏移 |
| `--product_id=<id>` | 资源包 ID |
| `--product_name=<name>` | 资源包名称 |
| `--status=<n>` | 状态 |
| `--region_code=<code>` | 区域 |
| `--enterprise_project_id=<id>` | 企业项目 |
| `--order_id=<id>` | 订单 ID |
| `--service_type_code_list.1=<code>` | 云服务类型 |

`ListFreeResourceUsages` 必须先从 `ListFreeResourceInfos` 取得资源包 ID，且不支持 `--limit`。

`ListFreeResourcesUsageRecords` 可选参数：

| 参数 | 语义 |
| --- | --- |
| `--offset=<n>` | 分页偏移 |
| `--free_resource_id=<id>` | 资源项 ID |
| `--product_id=<id>` | 资源包 ID |
| `--resource_type_code=<code>` | 资源类型 |

`ListFreeResourcesUsageRecords` 要求抵扣结束时间与起始时间跨度不超过 90 天。

## 订单证据

```bash
hcloud BSS ListCustomerOrders \
  --create_time_begin=<UTC-time> \
  --create_time_end=<UTC-time> \
  --limit=10 \
  --cli-region=<region>

hcloud BSS ShowCustomerOrderDetails --order_id=<order-id> --cli-region=<region>
hcloud BSS ShowRefundOrderDetails --order_id=<order-id> --cli-region=<region>
```

仅用于查证据。禁止 `PayOrders`、退订、续订、自动续费配置等写操作。

## 字典

```bash
hcloud BSS ListServiceTypes --limit=100 --cli-region=<region>
hcloud BSS ListResourceTypes --limit=100 --cli-region=<region>
hcloud BSS ListUsageTypes --limit=100 --cli-region=<region>
hcloud BSS ListMeasureUnits --limit=100 --cli-region=<region>
```

用途：翻译 `service_type_code`、`resource_type`、`usage_type`、`measure_id`。
若 `ListMeasureUnits` 在当前 KooCLI 报 API Explorer 元数据错误，跳过即可。

## 产品只读交叉验证

仅在 BSS 已给出服务和资源 ID 后使用。执行前必须看 help。

| 服务 | 只读模式 |
| --- | --- |
| ECS | `ShowServer` / `ListServersDetails` |
| EVS | 云硬盘 List/Show |
| EIP/VPC | 公网 IP、带宽、VPC、子网 List/Show |
| OBS | 桶、用量、统计查询 |
| CDN | 域名、流量、带宽统计 |
| RDS | 实例 List/Show |
| DCS | 实例 List/Show |
| LTS | 日志组/日志流 List/Show |

只读交叉验证不能替代 BSS 账务事实。
