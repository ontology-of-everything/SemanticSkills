# 账务语义层

> 事实硬定义在 `references/semantic/*.yml`；命令模板在
> `references/related-commands.md`。

语义层的目的，是让 Agent 在调用 CLI 前先确定“要查什么事实”。事实实体有
稳定粒度，维度用于筛选和分组，指标用于汇总或解释金额。它不复制命令参数，
也不把用户话术压成 FAQ。

## 事实实体

| 实体 | 粒度 | 来源 |
| --- | --- | --- |
| `AccountBalance` | 一个账户余额快照 | `ShowCustomerAccountBalances` |
| `MonthlyBillSummary` | 一个账期内服务/资源类型汇总行 | `ShowCustomerMonthlySum` |
| `ResourceBillRecord` | 一个资源消费记录行 | `ListCustomerselfResourceRecords` |
| `ResourceBillDetail` | 一个资源详单行 | `ListCustomerselfResourceRecordDetails` |
| `FreeResourcePackage` | 资源包库存、余量或抵扣记录 | 多 Operation，见 playbook §3 |
| `AccountChangeRecord` | 一条现金/授信/储值收支流水 | `ListCustomerAccountChangeRecords` |
| `CouponChangeRecord` | 一条代金券收支流水 | `ListCustomerCouponChangeRecords` |
| `CostAnalysis` | 一个成本分析分组结果 | `ListCosts` |

每个实体 YAML 只保留事实定义：`grain`、`dimensions`、`measures`、
`source_operation` / `source_operations`。用户问题可以有很多说法，路由时
应比较事实粒度、已知维度和目标指标，而不是查找某个问题样例是否命中。

## 路由语义

先从用户问题抽取这些槽位：

| 槽位 | 用途 |
| --- | --- |
| 目标 | 找事实、做归因、做对账、做咨询 |
| 时间 | 账期、自然日、近 N 天、跨月范围 |
| 范围 | 当前账号、企业主账号、子账号、支付账号 |
| 过滤维度 | 云服务、资源、区域、企业项目、计费模式、账单类型 |
| 指标 | 应付、实付、现金、授信、券、储值、欠费、用量 |
| 证据粒度 | 汇总、资源记录、资源详单、流水、资源包抵扣记录 |

选择事实实体时遵循两个原则：

- 能用更粗粒度回答的问题，先用汇总事实；需要解释来源时再钻明细。
- 一个事实实体无法解释的问题，交给 playbook 组织多事实链路，而不是猜一个万能 API。

## 通用维度

| 维度 | 含义 |
| --- | --- |
| `bill_cycle` / `cycle` | 账期，通常 `YYYY-MM` |
| `bill_date` | 消费/账单日期 |
| `cloud_service_type` | 云服务编码 |
| `resource_type` | 资源类型编码 |
| `region` | 资源区域 |
| `enterprise_project_id` | 企业项目 |
| `charge_mode` / `charging_mode` | 计费模式 |
| `bill_type` | 账单类型 |
| `resource_id` / `res_instance_id` | 资源实例 |
| `trade_id` / `order_id` | 交易/订单 |
| `payer_account_id` | 支付账号 |

## 通用指标

| 指标 | 说明 |
| --- | --- |
| `official_amount` | 官网价/原价 |
| `discount_amount` | 折扣金额 |
| `consume_amount` | 消费金额 |
| `cash_amount` | 现金支付 |
| `credit_amount` | 授信支付 |
| `coupon_amount` | 代金券抵扣 |
| `stored_value_card_amount` | 储值卡支付 |
| `debt_amount` | 欠费 |
| `usage` | 使用量 |
| `free_resource_usage` | 资源包抵扣量 |

## 金额口径

| 术语 | 口径 |
| --- | --- |
| 应付 | 账单应支付金额，可能不同于现金支出 |
| 实付 | 实际支付构成，可能含现金、授信、券、储值卡 |
| 官网价 | 未折扣目录价，不等于合同价 |
| 账期 | 账务归集月份，不总等于自然消费日期 |
| 账单类型 | 新购、续订、使用、退订、调账、支持计划等 |
| 按需 | 使用后计费，释放/删除后仍可能有滞后账单 |
| 包周期 | 包年包月订单，可能按月出账或在订单侧体现 |
| 未归集 | 不支持企业项目或历史数据未归属到项目 |

## 事实口径

每个事实只保留五项硬定义：粒度、时间、维度、指标、来源 Operation。

不在语义层写业务猜测；猜测必须来自查询结果或官网说明。
