# huawei-cloud-cost-estimation 更新日志

仅本技能变更。仓库级变更见 [../../CHANGELOG.zh.md](../../CHANGELOG.zh.md)。

## 1.0.1 - 2026-05-29

对照官方 BSS 文档与 hcloud 7.2.2 `--help`/`--dryrun` 的语义/命令一致性修订。

### 修复

- 包年 ECS 示例错用 `period_type=2`（月）→ 改为 `period_type=3`（年）
- `ListUsageTypes` 分页修正：实际支持 `--limit/--offset`（原标注无分页）
- 按需 `usage_measure_id` 去掉误导性 `max: 4`（那是字段位数，不是取值上限）

### 变更

- `related-commands.md` 新增 `response_contract` 段（官网价 vs 折后成交价，两接口的精确字段路径）
- ECS OS 默认统一为 safe-default `.linux`（Spec Review 披露），SKILL.md 与 `rfq-shared-dimensions.yml` 一致
- `iam-policies.md`：补 `ListOnDemandResourceRatings`；修正失效的 `rfq-operations.yml` / `quote_gate` 引用
- 补充 GPSSD2 云硬盘规格常量（`GPSSD2.storage/.iops/.throughput`）
- SKILL.md：定义确认话术与响应读数指针
- Universal Trap 用错参数 `region_id` → `region`（与 API/CLI/示例一致）
- Eval 扩至 10 条并含 `expectations` 可编程断言；A/B 工具链（`bin/grade_response.py` 等）
- DRY/分层：把具体 spec/code/measure/枚举值移出 `semantic/*.yml`（删除与 `related-commands.md` 重复且已漂移的 `documented_examples` 清单与枚举映射），语义层改为引用命令层这一唯一真源；OS 默认策略统一到 SKILL.md；规则写入仓库 `CLAUDE.md`。

## 1.0.0 - 2026-05-28

首个稳定版（**华为社区版**）。

### 新功能

- 下单前 BSS 询价 — 包年/包月（`ListRateOnPeriodDetail`）与按需（`ListOnDemandResourceRatings`）
- 工作流：Phase 1（Parse、Clarify、Spec Review）→ Phase 2（Query、Calculate、Verify、Present）
- `rfq-*-model.yml` 语义路由；ECS/RDS/DCS/EVS/盘/带宽/EIP
- **独立技能** — 不与 billing-scout 互路由；历史账务 → 费用中心 / BSS 账单只读 API

### qa

- `validate.sh`（layout、skills-ref、markdownlint、skillcheck）
- `evals/evals.json` 七条离线 eval

### 文档

- `docs/skills/huawei-cloud-cost-estimation.md`；`docs/catalog.yml` 索引；README 安装说明
