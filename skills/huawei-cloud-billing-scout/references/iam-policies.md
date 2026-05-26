# IAM 最小权限

目标：BSS 账务只读优先；产品资源只读仅用于交叉验证“账单里的资源当前是否还能查到”。

IAM Action 会随账号类型、站点和服务版本变化。本文给权限设计口径；落地前以
[IAM 权限最佳实践](https://support.huaweicloud.com/bestpractice-iam/iam_0426.html)、
[API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/overview)
和 `hcloud <SERVICE> <Operation> --help` 为准。

## 权限分层

| 层级 | 用途 | 何时需要 |
| --- | --- | --- |
| BSS 核心只读 | 余额、账单、明细、成本、订单、代金券、资源包 | 默认必需 |
| 多账号只读 | 企业主/子账号/关联账号账务 | 明确查询多账号或企业分摊 |
| 产品只读 | 资源存在性、状态交叉验证 | BSS 已定位服务和资源 ID 后 |

禁止加入支付、续费、退订、回收、创建、修改、删除、发送验证码、划拨等写权限。

## BSS 核心只读

| KooCLI 操作 | 读取内容 |
| --- | --- |
| `ShowCustomerAccountBalances` | 余额、欠费金额 |
| `ShowCustomerMonthlySum` | 月度汇总账单 |
| `ListCustomerBillsFeeRecords` | 消费流水账单 |
| `ListCustomerselfResourceRecords` | 资源消费记录 |
| `ListCustomerselfResourceRecordDetails` | 资源详单、用量明细 |
| `ListCustomerBillsMonthlyBreakDown` | 月度摊销成本 |
| `ListCustomerAccountChangeRecords` | 现金/授信账户收支 |
| `ListCustomerCouponChangeRecords` | 代金券收支 |
| `ListStoredValueCards` | 储值卡列表 |
| `ListCustomerOrders` | 订单列表 |
| `ShowCustomerOrderDetails` | 订单详情 |
| `ShowRefundOrderDetails` | 退订/退款订单证据 |
| `ListOrderCouponsByOrderId` | 订单可用券 |
| `ListOrderDiscounts` | 订单可用折扣 |
| `ListFreeResourceInfos` | 资源包列表 |
| `ListFreeResourceUsages` | 资源包余量 |
| `ListFreeResourcesUsageRecords` | 资源包抵扣明细 |
| `ListCosts` | 成本分析 |
| `ListResourceUsageSummary` | CDN/OBS/IEC/VPC 使用量汇总 |
| `ListResourceUsage` | CDN/OBS/IEC/VPC 资源使用量明细 |
| `ListQuotaCoupons` | 伙伴优惠券额度 |
| `ListIssuedCouponQuotas` | 已发放券额度 |
| `ListCouponQuotasRecords` | 券额度操作记录 |
| `ListIssuedPartnerCoupons` | 已发放优惠券 |
| `ListPartnerCouponsRecord` | 优惠券发放/回收记录 |
| `ListSubCustomerCoupons` | 伙伴自身优惠券 |
| `ListServiceTypes` | 云服务类型字典 |
| `ListResourceTypes` | 资源类型字典 |
| `ListUsageTypes` | 使用量类型字典 |
| `ListMeasureUnits` | 计量单位字典 |
| `ListConversions` | 计量单位进制换算 |
| `ListServiceResources` | 服务到资源类型关系 |
| `ListProvinces` | 省份字典 |
| `ListCities` | 城市字典 |
| `ListCounties` | 区县字典 |

策略骨架（示意，落地前以 IAM 控制台/API Explorer 的实际 Action 为准）：

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:*:get",
        "bss:*:list"
      ],
      "Resource": "*"
    }
  ]
}
```

如果 IAM 不接受通配只读 Action，按实际 API 显式列出查询类 Action。不要用写操作补权限。

## 多账号只读

仅在企业主/子账号关系和授权成立时使用；普通账号可能返回 403。伙伴/代售接口同样需要确认授权关系和账号范围，不能从当前账号自动扩大到客户列表。

| 操作 | 用途 |
| --- | --- |
| `ListEnterpriseOrganizations` | 企业组织结构 |
| `ListEnterpriseSubCustomers` | 企业子账号列表 |
| `ListEnterpriseMultiAccount` | 企业子账号可回收余额；需 `balance_type`、`sub_customer_id` |
| `ShowMultiAccountTransferAmount` | 企业主可拨款余额 |
| `ListMultiAccountTransferCoupons` | 企业主可拨款优惠券 |
| `ListMultiAccountRetrieveCoupons` | 企业子账号可回收优惠券 |
| `ListConsumeSubCustomers` | 有消费的子客户 |
| `ListSubcustomerMonthlyBills` | 子客户月度账单 |
| `ListSubCustomerBillDetail` | 子客户账单明细 |
| `ListSubCustomers` | 伙伴客户列表 |
| `ListSubCustomerNewTag` | 客户新客标签 |
| `ListCustomerOnDemandResources` | 代售客户按需资源 |
| `ListPayPerUseCustomerResources` | 包年包月资源 |
| `ListCustomersBalancesDetail` | 代售客户余额 |
| `ListPartnerBalances` | 伙伴/经销商余额 |
| `ListPartnerAccountChangeRecords` | 伙伴收支流水 |
| `ListPartnerAdjustRecords` | 伙伴调账记录 |
| `ListIndirectPartners` | 二级经销商列表 |

财务独立子账号、伙伴、代售类客户有额外约束。接口返回无权限时，不绕过，不扩大查询。

## 产品只读

产品 API 只用于交叉验证，不作为账务事实来源。

| 服务 | 只读示例 |
| --- | --- |
| ECS | 云服务器 List/Show |
| EVS | 云硬盘 List/Show |
| EIP/VPC | 弹性 IP、带宽、VPC、子网 List/Show |
| OBS | 桶、用量、统计查询 |
| CDN | 域名、流量、带宽统计查询 |
| RDS | 实例 List/Show |
| DCS | 缓存实例 List/Show |
| LTS | 日志组、日志流 List/Show |
| CBR | 存储库、备份 List/Show |
| ELB/NAT | 负载均衡、监听器、NAT 网关 List/Show |

若产品 API 查不到资源，只能说明“当前该 API 未查到”。账单仍可能来自历史账期、
滞后出账、子资源、共享带宽、备份、快照、流量、云市场或不支持企业项目归集的项目。

## 权限失败处理

| 现象 | 处理 |
| --- | --- |
| `403 Forbidden` | 记录操作名、账号范围、接口族；建议补最小只读权限 |
| 子账号数据为空 | 检查企业主/子账号授权关系和 `method` 参数 |
| 字典查不到服务名 | 保留原始 code，提示需查官方服务类型字典 |
| 产品资源查不到 | 回到 BSS 账单证据，不推断账单错误 |
