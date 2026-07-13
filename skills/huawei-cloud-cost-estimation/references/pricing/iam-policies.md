# IAM 最小权限（RFQ 询价）

询价仅使用只读权限。IAM Action 随账号类型、站点和服务版本变化，落地前以 API Explorer 与运行时 `hcloud <Service> <Operation> --help` 为准。

## 权限分层

| 层级 | 操作 | 用途 |
| --- | --- | --- |
| BSS 询价 | `ListRateOnPeriodDetail`, `ListOnDemandResourceRatings` | 取得包周期或按需报价 |
| BSS 字典 | `ListServiceTypes`, `ListResourceTypes`, `ListServiceResources`, `ListResourceSpecs`, `ListMeasureUnits`, `ListConversions` | 解析服务、资源、规格和度量 |
| 产品辅助 | `ECS/NovaListAvailabilityZones` | 用户指定 AZ 时 |
| 身份范围 | `IAM/KeystoneListAuthProjects`, `IAM/KeystoneListProjects` | 解析可访问项目 |

询价常用策略为 `bss:order:view` 加对应 BSS/IAM 只读 Action。不要用写权限补救查询失败。

## 伙伴代客户询价

使用客户授权所得 Token 调 `KeystoneListAuthProjects` 解析目标 region 的客户 `project_id`，再询价。授权失败时停止，不扩大范围。

## 失败处理

| 现象 | 处理 |
| --- | --- |
| `403 Forbidden` / `CBC.0151` | 记录操作与账号范围，建议补对应只读 Action |
| `429` | 等 2 秒重试一次；仍失败则停止 |
| `CBC.0100` | 核对运行时 help 与参数组合 |
| `CBC.99006006` | 回到规格、region、计费模式确认 |
| `CBC.99006055` | 缩小询价批次或周期 |

历史账单、余额和对账不属于 RFQ；使用费用中心或独立只读账单技能。
