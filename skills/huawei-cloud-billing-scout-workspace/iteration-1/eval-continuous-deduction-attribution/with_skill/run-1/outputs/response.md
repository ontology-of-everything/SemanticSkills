## 结果表（占位示例 — 真实环境需 `hcloud BSS` 只读拉取）

以下行用于演示输出结构；**未连接真实 API**，执行时请在你本机用只读 BSS IAM 跑 `ListCustomerselfResourceRecords` / `ListCustomerselfResourceRecordDetails` 并替换为真实结果。资源与交易标识已按技能要求只保留尾号。

| 账期/消费日 | 云服务 | 资源名 | 资源 ID（尾号） | 区域 | 企业项目 | 计费模式 | 应付/消费额(元) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05 | Object Storage Service | obs-bucket-a | …`a1b2` | cn-north-4 | prj-default | 按需 | 128.40 |
| 2026-05 | Elastic Cloud Server | ecs-web-01 | …`9f3c` | cn-south-1 | prj-prod | 按需 | 86.20 |
| 2026-05 | Relational Database Service | rds-mysql | …`7d21` | cn-east-3 | prj-prod | 按需 | 54.10 |

*对话仅展示按金额降序 **Top 3**；完整结果请分页或导出本地报告。*

## 小结

当前问题属于**持续扣费 / 资源费用归因**：需要把“本月一直在扣”落到**仍产生消费的资源行**上。优先用 BSS 资源消费记录按账期或近 30 天窗口聚合，再对 Head 项下钻详单；若记录与控制台资源列表不一致，再用产品侧只读 `List`/`Get` 交叉核验。本答复**不执行**关停、删除、支付、退款等任何写操作。

## 用户可读说明（查询说明）

- **时间范围**：默认按**当前账期月**（本月）查看持续消费；如需看删除后滞后账单，可并入**近 7/14/30 天**窗口对比（与 playbook 中“持续扣费”路径一致）。
- **账号范围**：当前 KooCLI 配置的认证 profile / `method=oneself`；若需企业主+子客户范围，需你明确授权后再改 `method`。
- **排序与行数**：表格为**按消费额降序 TopN（本例 N=3）**；超出 50 行将只给 TopN + 本地全量报告指引。
- **脱敏**：凡出现完整资源 ID、账号 ID、订单/交易 ID，输出仅保留**尾号 4–6 位**；AK/SK、Token 永不出现。

## 建议的只读下一步（KooCLI）

1. `hcloud BSS ListCustomerselfResourceRecords --cycle=<YYYY-MM> --limit=10 --cli-region=<region> --cli-output=json`（按需加 `--bill_date_begin` / `--bill_date_end` 收窄到本月已出账段）
2. 对 Top 资源：`hcloud BSS ListCustomerselfResourceRecordDetails` 同周期、同 `resource_id`（命令参数以 `--help` 为准）下钻用量与金额构成。
