# huawei-cloud-cost-estimation 更新日志

仅本技能变更。仓库级变更见 [../../CHANGELOG.zh.md](../../CHANGELOG.zh.md)。

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
