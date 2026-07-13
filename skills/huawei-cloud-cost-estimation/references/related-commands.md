# 命令合同（RFQ 询价）

每个 op 一段：**contract**（必填 / 条件必填 / 分页）+ **CLI 模板**。事实/维度看 `semantic/*.yml`。

## Universal Traps（每次询价必看）

1. **数组参数仅 dot notation** — `--product_infos.1.region=xxx`；JSON 串或 `[...]` 形式 KooCLI 不识别。
2. **询价 API 无分页** — `ListRateOnPeriodDetail` / `ListOnDemandResourceRatings` 不接受 `--limit/--offset`；多项一次性放进 `product_infos.N.*`。
3. **code 大小写敏感** — `cloud_service_type` (`hws.service.type.ec2`)、`resource_type`、`region`、spec 必须按维度查询返回的原文，不能小写化或拼接。
4. **`resource_spec` 只认实查** — 询价模板中的规格值（如 `c6.2xlarge.2.linux`、`GPSSD`、`19_bgp`）仅示意格式；实际取值必须来自当次 `BSS/ListResourceSpecs` 返回（见 resource_spec_lookup），不得凭记忆或文档填写。

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

ECS 包年示例（c6.2xlarge.2.linux，OS 未指定默认取 linux 变体，1 年，1 台 → `period_type=3`）：

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

混合产品（ECS + EVS GPSSD 40GB + 带宽 19_bgp 40Mbps）：

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

ECS 按需示例（c3.3xlarge.2.linux，按小时询 2 小时）：

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

混合按需（ECS Duration + EVS SSD 10GB Duration + 带宽 12_sbgp upflow 4GB）：

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
| `usage_factor` | string | `Duration` / `upflow` / 等 | ECS/EVS/EIP/市场镜像→`Duration`；带宽→`Duration` 或 `upflow`；与话单一致，未知调 `BSS/ListUsageTypes` |
| `usage_value` | number | - | 使用量数值，如 2 小时 → 2 |
| `usage_measure_id` | int | 4=小时 / 10=GB / 等 | 与 `usage_factor` 单位匹配 |
| `inquiry_precision` | int | 0 默认 / 1 全 10 位 | 仅当结果到小数点 7 位以上才有差别 |

---

## response_contract（报价怎么读）

只读当次响应，**不臆造折扣**。`measure_id=1`=元；`currency=CNY`（空=人民币）；`id` 回映射请求 `product_infos[].id`。**默认报官网价；响应里有折扣才附折后（有则报）。**

| API | 官网价（默认报） | 折后应付（有则报） |
| --- | --- | --- |
| `ListRateOnPeriodDetail` | 总额 `official_website_rating_result.official_website_amount`；分项同对象 `.product_rating_results[].official_website_amount` | `optional_discount_rating_results[]` 非空时取 `best_offer==1`，读组级 `amount` / `discount_amount` / `discount_name` |
| `ListOnDemandResourceRatings` | 总额根级 `official_website_amount`；分项 `product_rating_results[].official_website_amount` | `discount_amount>0`（即 `amount≠official_website_amount`）时读 `amount` / `discount_amount`，明细见 `product_rating_results[].discount_rating_results[]` |

> 校验：分项 `official_website_amount` 之和 = 总额。on-demand `usage_value` 是询价标量（如 24h），结果即累计，**不再二次乘时长**。

---

## dimension_lookup

| 操作 | 用途 | 必填 | 分页 |
| --- | --- | --- | --- |
| `BSS/ListServiceTypes` | 翻译/查找 `cloud_service_type` | - | limit/offset |
| `BSS/ListResourceTypes` | 翻译 `resource_type_code` | - | limit/offset |
| `BSS/ListServiceResources` | 服务→资源类型桥 | `service_type_code` | limit/offset |
| `BSS/ListMeasureUnits` | 翻译 `size_measure_id`/`measure_id` | - | none |
| `BSS/ListConversions` | 度量进制换算 | - | none |
| `BSS/ListUsageTypes` | 翻译 on-demand `usage_factor` | - | limit/offset |

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
> **required**: `cloud_service_type` / `resource_type` / `region_code` / `charge_mode`（1 包年包月 / 3 按需，与询价模式对齐）
> **optional**: `filters.[N].key=RESOURCE_SPEC` + `filters.[N].value`（模糊匹配：前缀/后缀/中间，同时匹配规格编码与规格名称）、`marker` + `limit`

**契约陷阱**：

1. `marker` 与 `limit` 必须同用才生效，单独传无效；首页不带 `marker`，翻页传上一页响应的 `page_info.next_marker`；`next_marker=null` 即末页。翻页途中不得改查询条件。
2. `charge_mode` / `region_code` 必须与询价 line 一致，否则拿到的规格询价必报 `CBC.99006006`。
3. 返回的 `resource_spec` 即询价可直接使用的完整编码（ECS 已含 `.linux`/`.win`/`.byol` OS 后缀，禁止再拼接）；`resource_spec_name` 为人类可读描述（ECS 含规格族/vCPU/内存/OS）。

**查询纪律（限流与性能）**：

- **必带 filter**：用户给了任何线索——规格编码片段（`c6.2xlarge`）、规格族（`c7`）、或 CPU/内存描述（转成 `8vCPUs|16GB` 名称片段）——必须带 `filters` 查询。禁止对 ECS 这类大目录做无 filter 全量翻页爬取；带宽/EVS 等小目录可无 filter 一页取全。
- **limit 固定 100**（接口上限），最少调用次数拿最大返回。
- **翻页熔断**：带 filter 仍翻到第 3 页（约 300 条）未收敛，停止翻页，归纳已有候选向用户澄清，不继续消耗配额。
- **限流退避**：遇 429/限流类错误，等待 2 秒重试一次；再失败即停止并如实告知，禁止循环重试。
- **多候选**：同族多 OS 按 safe-default（linux）选定并披露；跨族多候选（模糊匹配副作用，如 `c6` 命中 `ac6`）念候选让用户确认，不自动挑。

命令示例（编码前缀检索 / 名称检索 / 小目录全量）：

```bash
# ECS 包年包月，按规格族检索
hcloud BSS ListResourceSpecs --charge_mode=1 \
  --cloud_service_type=hws.service.type.ec2 --resource_type=hws.resource.type.vm \
  --region_code=cn-north-4 \
  --filters.1.key=RESOURCE_SPEC --filters.1.value=c6.2xlarge \
  --limit=100 --cli-region=cn-north-1 --cli-output=json

# ECS 按需，用户只说"8核16G"→ 名称片段检索
hcloud BSS ListResourceSpecs --charge_mode=3 \
  --cloud_service_type=hws.service.type.ec2 --resource_type=hws.resource.type.vm \
  --region_code=cn-north-4 \
  --filters.1.key=RESOURCE_SPEC --filters.1.value="8vCPUs|16GB" \
  --limit=100 --cli-region=cn-north-1 --cli-output=json

# 带宽小目录，无 filter 一页取全
hcloud BSS ListResourceSpecs --charge_mode=1 \
  --cloud_service_type=hws.service.type.vpc --resource_type=hws.resource.type.bandwidth \
  --region_code=cn-north-4 \
  --limit=100 --cli-region=cn-north-1 --cli-output=json
```

读法：候选取 `cloud_service_basics[].resource_spec`，向用户复述用 `resource_spec_name`；`page_info.next_marker` 非 null 则有下一页。

### 线性产品配对（`size_measure_id`）

ListResourceSpecs 不返回度量单位；线性产品询价须按 `resource_type` 配对（值不随规格变化）：

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
