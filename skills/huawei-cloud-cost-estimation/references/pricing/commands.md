# 命令合同（RFQ 询价）

每个 op 一段：**contract**（必填 / 条件必填 / 分页）+ **CLI 模板**。事实/维度看 `semantic/*.yml`。

## Universal Traps（每次询价必看）

1. **数组参数仅 dot notation** — `--product_infos.1.region=xxx`；JSON 串或 `[...]` 形式 KooCLI 不识别。
2. **询价 API 无分页** — `ListRateOnPeriodDetail` / `ListOnDemandResourceRatings` 不接受 `--limit/--offset`；多项一次性放进 `product_infos.N.*`。
3. **code 大小写敏感** — `cloud_service_type` (`hws.service.type.ec2`)、`resource_type`、`region`、spec 必须按维度查询返回的原文，不能小写化或拼接。
4. **`resource_spec` 只认实查** — 询价模板中的规格值仅示意格式；实际取值必须来自当次 `BSS/ListResourceSpecs` 返回（见 resource_spec_lookup），不得凭记忆或文档填写。

## CLI 格式要点

- 数组参数用 dot notation 递增：`--product_infos.1.id=1`、`--product_infos.2.id=2`。
- 默认分页 `--limit=10 --offset=0`；每命令 ≤3 页。`ListMeasureUnits` / `ListConversions` 无分页参数；`ListUsageTypes` 有 `--limit/--offset`。
- 输出 `--cli-output=json`；`table` 仅人眼用。

---

## rfq_quote_execution

### `BSS/ListRateOnPeriodDetail` —— 包年/包月询价

> **method**: POST · **safety**: readonly · **entities**: `RFQ_Header`, `RFQ_Line` · **pagination**: n/a · **doc**: [bcloud_01002](https://support.huaweicloud.com/api-bpconsole/bcloud_01002.html)
> **required**: `project_id` + 每行 `id` / `cloud_service_type` / `resource_type` / `resource_spec` / `region` / `period_type` / `period_num` / `subscription_num`
> **conditional**: `linear_product` → `resource_size` + `size_measure_id`

ECS 包年示例：

```bash
hcloud BSS ListRateOnPeriodDetail \
  --project_id=<project_id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=hws.service.type.ec2 \
  --product_infos.1.resource_type=hws.resource.type.vm \
  --product_infos.1.resource_spec=c6.2xlarge.2.linux \
  --product_infos.1.region=cn-north-1 \
  --product_infos.1.available_zone=cn-north-1a \
  --product_infos.1.period_type=3 \
  --product_infos.1.period_num=1 \
  --product_infos.1.subscription_num=1 \
  --cli-region=cn-north-1 --cli-output=json
```

混合产品（ECS + EVS + 带宽）：

```bash
hcloud BSS ListRateOnPeriodDetail \
  --project_id=<project_id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=hws.service.type.ec2 \
  --product_infos.1.resource_type=hws.resource.type.vm \
  --product_infos.1.resource_spec=c6.2xlarge.2.linux \
  --product_infos.1.region=cn-north-1 \
  --product_infos.1.period_type=2 --product_infos.1.period_num=1 --product_infos.1.subscription_num=1 \
  --product_infos.2.id=2 \
  --product_infos.2.cloud_service_type=hws.service.type.ebs \
  --product_infos.2.resource_type=hws.resource.type.volume \
  --product_infos.2.resource_spec=GPSSD \
  --product_infos.2.region=cn-north-1 \
  --product_infos.2.resource_size=40 --product_infos.2.size_measure_id=17 \
  --product_infos.2.period_type=2 --product_infos.2.period_num=1 --product_infos.2.subscription_num=1 \
  --product_infos.3.id=3 \
  --product_infos.3.cloud_service_type=hws.service.type.vpc \
  --product_infos.3.resource_type=hws.resource.type.bandwidth \
  --product_infos.3.resource_spec=19_bgp \
  --product_infos.3.region=cn-north-1 \
  --product_infos.3.resource_size=40 --product_infos.3.size_measure_id=15 \
  --product_infos.3.period_type=2 --product_infos.3.period_num=1 --product_infos.3.subscription_num=1 \
  --cli-region=cn-north-1 --cli-output=json
```

字段对照：

| 字段 | 类型 | 取值 | 备注 |
| --- | --- | --- | --- |
| `period_type` | int | 0 天 / 2 月 / 3 年 / 4 小时 | 包年包月通常 2 或 3 |
| `period_num` | int | 1..214783647 | 与 `period_type` 配合 |
| `subscription_num` | int | 1..10000 | 询价数量 |
| `size_measure_id` | int | 15 Mbps / 17 GB / 14 个 | 线性产品必填 |
| `fee_installment_mode` | string | HALF_PAY / ZERO_PAY / NA | 暂仅 CloudPond |

### `BSS/ListOnDemandResourceRatings` —— 按需询价

> **method**: POST · **safety**: readonly · **entities**: `RFQ_OnDemand_Header`, `RFQ_OnDemand_Line` · **pagination**: n/a · **doc**: [bcloud_01001](https://support.huaweicloud.com/api-bpconsole/bcloud_01001.html)
> **required**: `project_id` + 每行 `id` / `cloud_service_type` / `resource_type` / `resource_spec` / `region` / `usage_factor` / `usage_value` / `usage_measure_id` / `subscription_num`
> **conditional**: `linear_product` → `resource_size` + `size_measure_id`
> **optional**: `inquiry_precision`（0 默认 6 位 / 1 全 10 位）

ECS 按需示例：

```bash
hcloud BSS ListOnDemandResourceRatings \
  --project_id=<project_id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=hws.service.type.ec2 \
  --product_infos.1.resource_type=hws.resource.type.vm \
  --product_infos.1.resource_spec=c3.3xlarge.2.linux \
  --product_infos.1.region=cn-north-1 \
  --product_infos.1.usage_factor=Duration \
  --product_infos.1.usage_value=2 \
  --product_infos.1.usage_measure_id=4 \
  --product_infos.1.subscription_num=1 \
  --cli-region=cn-north-1 --cli-output=json
```

混合按需（ECS + EVS + 按流量带宽）：

```bash
hcloud BSS ListOnDemandResourceRatings \
  --project_id=<project_id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=hws.service.type.ec2 \
  --product_infos.1.resource_type=hws.resource.type.vm \
  --product_infos.1.resource_spec=c3.3xlarge.2.linux \
  --product_infos.1.region=cn-north-1 \
  --product_infos.1.usage_factor=Duration --product_infos.1.usage_value=2 --product_infos.1.usage_measure_id=4 \
  --product_infos.1.subscription_num=1 \
  --product_infos.2.id=2 \
  --product_infos.2.cloud_service_type=hws.service.type.ebs \
  --product_infos.2.resource_type=hws.resource.type.volume \
  --product_infos.2.resource_spec=SSD \
  --product_infos.2.region=cn-north-1 \
  --product_infos.2.resource_size=10 --product_infos.2.size_measure_id=17 \
  --product_infos.2.usage_factor=Duration --product_infos.2.usage_value=2 --product_infos.2.usage_measure_id=4 \
  --product_infos.2.subscription_num=1 \
  --product_infos.3.id=3 \
  --product_infos.3.cloud_service_type=hws.service.type.vpc \
  --product_infos.3.resource_type=hws.resource.type.bandwidth \
  --product_infos.3.resource_spec=12_sbgp \
  --product_infos.3.region=cn-north-1 \
  --product_infos.3.resource_size=1 --product_infos.3.size_measure_id=15 \
  --product_infos.3.usage_factor=upflow --product_infos.3.usage_value=4 --product_infos.3.usage_measure_id=10 \
  --product_infos.3.subscription_num=1 \
  --cli-region=cn-north-1 --cli-output=json
```

字段对照（与 period 互补，不重复 common 字段）：

| 字段 | 类型 | 取值 | 备注 |
| --- | --- | --- | --- |
| `usage_factor` | string | `Duration` / `upflow` / 等 | 未知时调 `BSS/ListUsageTypes` |
| `usage_value` | number | - | 使用量数值 |
| `usage_measure_id` | int | 4=小时 / 10=GB / 等 | 与 `usage_factor` 单位匹配 |
| `inquiry_precision` | int | 0 默认 / 1 全 10 位 | 控制精度 |

---

## response_contract（报价怎么读）

只读当次响应，**不臆造折扣**。`measure_id=1`=元；`currency=CNY`（空=人民币）；`id` 回映射请求 `product_infos[].id`。默认报官网价；响应里有折扣才附折后。

| API | 官网价（默认报） | 折后应付（有则报） |
| --- | --- | --- |
| `ListRateOnPeriodDetail` | 总额 `official_website_rating_result.official_website_amount`；分项同对象 `.product_rating_results[].official_website_amount` | `optional_discount_rating_results[]` 非空时取 `best_offer==1`，读组级 `amount` / `discount_amount` / `discount_name` |
| `ListOnDemandResourceRatings` | 总额根级 `official_website_amount`；分项 `product_rating_results[].official_website_amount` | `discount_amount>0` 时读 `amount` / `discount_amount`，明细见 `product_rating_results[].discount_rating_results[]` |

> 校验：分项 `official_website_amount` 之和 = 总额。on-demand `usage_value` 是询价标量，结果即累计，不再二次乘时长。

---

## dimension_lookup

| 操作 | 用途 | 必填 | 分页 |
| --- | --- | --- | --- |
| `BSS/ListServiceTypes` | 翻译/查找 `cloud_service_type` | - | limit/offset |
| `BSS/ListResourceTypes` | 翻译 `resource_type_code` | - | limit/offset |
| `BSS/ListServiceResources` | 服务→资源类型桥 | `service_type_code` | limit/offset |
| `BSS/ListMeasureUnits` | 翻译度量单位 | - | none |
| `BSS/ListConversions` | 度量进制换算 | - | none |
| `BSS/ListUsageTypes` | 翻译按需 usage factor | - | limit/offset |

```bash
hcloud BSS ListServiceTypes --service_type_name=弹性云服务器 \
  --cli-region=cn-north-1 --cli-output=json --limit=10 --offset=0

hcloud BSS ListServiceResources --service_type_code=hws.service.type.ec2 \
  --cli-region=cn-north-1 --cli-output=json --limit=10 --offset=0

hcloud BSS ListResourceTypes --cli-region=cn-north-1 --cli-output=json --limit=10 --offset=0
hcloud BSS ListMeasureUnits  --cli-region=cn-north-1 --cli-output=json
hcloud BSS ListConversions   --cli-region=cn-north-1 --cli-output=json
hcloud BSS ListUsageTypes    --cli-region=cn-north-1 --cli-output=json
```

---

## resource_spec_lookup

### `BSS/ListResourceSpecs` —— 规格解析唯一路径

> **method**: POST · **safety**: readonly · **entities**: `Dim_ResourceSpec` · **pagination**: marker/limit · **doc**: [qct_00008](https://support.huaweicloud.com/api-oce/qct_00008.html)
> **required**: `cloud_service_type` / `resource_type` / `region_code` / `charge_mode`（1 包年包月 / 3 按需）
> **optional**: `filters.[N].key=RESOURCE_SPEC` + `filters.[N].value`、`marker` + `limit`

**契约陷阱**：

1. `marker` 与 `limit` 必须同用；首页不带 `marker`，翻页传上一页响应的 `page_info.next_marker`。
2. `charge_mode` / `region_code` 必须与询价 line 一致。
3. 返回的 `resource_spec` 可直接询价，禁止再拼接 OS 后缀。

**查询纪律**：

- 用户给了任何规格线索时必须带 `filters`；禁止对大目录无过滤全量爬取。
- `limit=100`；带 filter 到第 3 页仍未收敛则停止并让用户选择。
- 429 等 2 秒重试一次；再失败即停止。
- 多候选时回显候选，不自动跨规格族选择。

```bash
hcloud BSS ListResourceSpecs --charge_mode=1 \
  --cloud_service_type=hws.service.type.ec2 --resource_type=hws.resource.type.vm \
  --region_code=cn-north-4 \
  --filters.1.key=RESOURCE_SPEC --filters.1.value=c6.2xlarge \
  --limit=100 --cli-region=cn-north-1 --cli-output=json
```

候选取 `cloud_service_basics[].resource_spec`，向用户复述用 `resource_spec_name`；`page_info.next_marker` 非 null 则有下一页。

### 线性产品配对（`size_measure_id`）

| `resource_type` | `size_measure_id` | 单位 |
| --- | --- | --- |
| `hws.resource.type.volume` | 17 | GB |
| `hws.resource.type.bandwidth` | 15 | Mbps |
| `hws.resource.type.share_bandwidth` | 15 | Mbps |

---

## scope_resolve

```bash
hcloud IAM KeystoneListAuthProjects --cli-region=cn-north-1 --cli-output=json
hcloud IAM KeystoneListProjects --domain_id=<domain_id> --cli-region=cn-north-1 --cli-output=json
```

伙伴代客户询价时，需先通过伙伴 Token 置换出客户 Token、再调用 `KeystoneListAuthProjects` 获取 region 对应的 `project_id`；流程见 `iam-policies.md`。
