# huawei-cloud-cost-estimation 更新日志

仅本技能变更。仓库级变更见 [../../CHANGELOG.zh.md](../../CHANGELOG.zh.md)。

## 3.0.0 - 2026-07-14

破坏性安全调整：退订降级为仅提供控制台指引；技能不再运行、预演或输出任何退订 CLI/API 命令。

### 变更

- 包年/包月引导至「费用中心 → 订单管理 → 云服务退订」，并提醒备份及核对精确资源、关联资源、退款/手续费和退款流向
- 按需资源引导至对应云服务控制台自行处理；删除仍在技能范围外
- 73 个开通主体及其 `--dryrun`、费用回表和确认门禁保持不变
- 退订 eval 改为验证「即使用户坚持也仅给控制台指引」；校验脚本禁止安装包出现破坏性生命周期命令

### 移除

- `BSS/CancelResourcesSubscription` 执行白名单及其 dry-run/确认流程

## 2.0.0 - 2026-07-13

重大能力变更：在询价之上加入受控资源生命周期（开通 + 统一退订）。安全边界从「拒绝一切写操作」改为「白名单写操作 + 强制 `--dryrun` + 显式确认」。证据来自 KooCLI 7.2.2 服务级 help；见 `docs/hcloud/evidence/normative-allowlist.md`。

### 新增

- **references/lifecycle/** — 薄流程、无语义层：`concepts.md`（help/依赖查询/`--dryrun`/费用状态/批次/退订语义）+ `commands.md`（73 个规范开通主体 + `BSS/CancelResourcesSubscription`；只存命令主体与依赖指针，参数一律运行时 `--help` 解析）
- **SKILL.md Route/Lifecycle** — 开通：白名单 → help → 依赖解析 → 费用回表（可询价先报价；未知费用额外确认）→ 强制本地 `--dryrun` → 批次回显统一确认 → 顺序执行失败即停、不自动回滚；退订：独立高强度确认
- **qa/fixtures/ops_contracts.yml** — 写白名单唯一真源（73 开通 + 1 退订）；`validate.sh` 新增 `check_write_allowlist`：fixture ↔ `lifecycle/commands.md` 1:1、BSS 可变仅退订、禁 BSS 写前缀、写场景 eval 必须 dry-only
- **evals #13–18** — 开通费用回显/dry/确认、未知费用额外确认、拒跳过 dry、批次 fail-fast、退订高强度确认、拒白名单外写操作；grader 对应分支
- **docs/hcloud/evidence/normative-allowlist.md** — 手工证据快照（规范清单、`--dryrun` 与服务端 `dry_run` 的区别、已知 help 缺口）

### 变更

- **references/ 按域重组** — 询价文件迁入 `references/pricing/`（`commands.md`、`iam-policies.md`、`semantic/*`）；`related-commands.md` 更名为 `pricing/commands.md`
- **eval #4** 语义调整：仍拒收对话 AK/SK，但下单意图路由到受控开通流程，不再一刀切拒绝
- 原始接口清单对照本机 CLI 归一化：CDN/CSS/MRS/ELB 展开版本后缀；Kafka → `CreatePostPaidKafkaInstance`；RocketMQ → `CreateInstanceByEngine`；删除 `GaussDB CreateClickHouseInstance`（当前 CLI 不存在，StarRocks 非等价替代）

## 1.1.0 - 2026-07-13

`resource_spec` 解析统一到新接口 `BSS/ListResourceSpecs`（[qct_00008](https://support.huaweicloud.com/api-oce/qct_00008.html)）；已对照 hcloud 7.2.2 实调验证（ECS 编码/名称模糊检索、带宽目录）。

### 新增

- **related-commands.md**：`resource_spec_lookup` 围绕 `BSS/ListResourceSpecs` 重写 — 完整契约（四个必填参数、`filters.[N].key=RESOURCE_SPEC` 对规格编码与名称模糊匹配、`marker`+`limit` 必须同用）、查询纪律（有线索必带 filter、`limit=100`、3 页翻页熔断、限流等 2 秒退避重试一次、禁循环重试）、线性产品 `resource_type`→`size_measure_id` 配对小表
- **Universal Trap #4**：询价模板中的规格值仅示意格式，实际取值必须来自当次 `ListResourceSpecs` 返回
- **SKILL.md Critical Rule #7**：规格只认实查（与询价同 region、同计费模式）；不查文档、不凭记忆、不拼 OS 后缀
- **eval #12** `spec-resolve-8c16g-via-listresourcespecs` + 程序化断言（先实查再询价、RESOURCE_SPEC filter、charge_mode 对齐）

### 变更

- **rfq-shared-dimensions.yml**：五个 `Dim_ResourceSpec_*` 雪花收敛为单一 `Dim_ResourceSpec`（来源 `BSS/ListResourceSpecs`），新增 charge_mode/region 对齐配对规则；删除 `flavor_id + os_suffix` 拼接 transform（接口直接返回完整编码）
- **iam-policies.md**：各产品 ListFlavors 权限层由 BSS 字典层的 `ListResourceSpecs` 覆盖（保留 AZ 查询）；错误表补 429 退避、`CBC.0100`、`CBC.0151`
- **catalog.yml**：primary_operations 增加 `BSS/ListResourceSpecs`

### 移除

- 产品 ListFlavors 路径（ECS/RDS/DCS/EVS）与带宽/EIP/云硬盘硬编码常量表 — 规格一律现查；命令层仅保留线性 `size_measure_id` 配对

## 1.0.2 - 2026-06-02

### 新增

- **SKILL.md**：BSS 端点规则 — 所有 `hcloud BSS` 固定 `--cli-region=cn-north-1`；`product_infos.N.region` 仍为资源部署区
- **eval #11** `bss-cli-region-shanghai-period` + cli-region 程序化断言；真实 hcloud A/B

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
