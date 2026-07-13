# 更新日志

Monorepo **基础设施**变更。各技能独立 changelog：

| 技能 | 更新日志 |
| --- | --- |
| huawei-cloud-billing-scout | [qa/huawei-cloud-billing-scout/CHANGELOG.zh.md](qa/huawei-cloud-billing-scout/CHANGELOG.zh.md) |
| huawei-cloud-cost-estimation | [qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md](qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md) |
| huawei-cloud-account-onboarding | [qa/huawei-cloud-account-onboarding/CHANGELOG.md](qa/huawei-cloud-account-onboarding/CHANGELOG.md) |
| semantic-creator | [qa/semantic-creator/CHANGELOG.md](qa/semantic-creator/CHANGELOG.md) |

## 3.6.0 - 2026-07-13

### 新功能

- **huawei-cloud-cost-estimation** **2.0.0**：在询价之上加入受控生命周期 — 73 个白名单开通命令 + `BSS CancelResourcesSubscription`；强制本地 `--dryrun`、费用回表（未知费用额外确认）与显式确认；`pricing/` 与 `lifecycle/` 参考分离；写白名单门禁与 dry-only evals #13–18（详见技能 changelog）

## 3.5.0 - 2026-07-13

### 新功能

- **huawei-cloud-cost-estimation** **1.1.0**：`resource_spec` 解析统一为 `BSS/ListResourceSpecs` — 模糊检索实查、限流友好查询纪律、语义层单维度收敛；eval #12（详见技能 changelog）

## 3.4.1 - 2026-07-10

### 新功能

- **semantic-creator** **0.5.1**：事实/维度/度量/路由分区增加固定 YAGNI 决策指导 — 白话术语、证据判据、短例与键盘/触屏可访问提示；eval 与 validate 门禁同步更新（详见技能 changelog）

## 3.4.0 - 2026-07-10

### 新功能

- **semantic-creator** **0.5.0**：Phase 2 重构为 HTML 决策工作台 — 原子决策、互斥候选、依赖硬阻塞、显式批准（`approved:true`）、五种用户行动与中文标签；eval 与 validate 门禁同步更新（详见技能 changelog）

## 3.3.0 - 2026-07-08

### 新功能

- **semantic-creator** **0.4.0**：Phase 2 评审改为模板+数据 — agent 将 model JSON 注入 `assets/review-template.html`（内联 vendored petite-vue，离线无 CDN）；剪贴板不可用时导出降级；支持上轮批注回填；未批准硬停不 Emit；eval #6 改写（详见技能 changelog）

## 3.2.0 - 2026-07-08

### 新功能

- **huawei-cloud-account-onboarding** **0.1.0**：扫码实名认证 mock 全流程 — mock 服务、创建/轮询脚本、终端二维码引导、QA 门禁（详见技能 changelog）
- **semantic-creator** **0.3.0**：四阶段对齐工作流（Ingest → Review → Emit → Verify）；交互式 HTML 评审报告（剪贴板 JSON 批注 + `amendments.md` 迭代）；默认导出 OKF v0.1；语义 lint 与 catalog 路由精简并对齐 OKF Entry Points（详见技能 changelog）

## 3.1.1 - 2026-06-29

### 变更

- **semantic-creator** **0.2.0**：聚焦 Kimball 星型语义层 — 默认输出 repo YAML；OKF 改为可选导出；维度 kind 精简为 conformed / snowflake / degenerate；Confirm 阶段简化（详见技能 changelog）
- **semantic-creator** **0.1.1**：由 `semantic-layer-builder` 更名（skills/、qa/、docs/）

## 3.1.0 - 2026-06-29

### 新功能

- **semantic-creator** **0.1.0**：元技能 — 引导式接口转 Kimball 语义层建模，支持 OKF 导出（详见技能 changelog；0.1.1 起由 `semantic-layer-builder` 更名）
- **huawei-cloud-account-onboarding** **0.1.0**：华为云实名认证准入技能空脚手架（占位载荷）

## 3.0.3 - 2026-06-02

### 变更

- **huawei-cloud-billing-scout** **2.3.9**：BSS `--cli-region=cn-north-1`、eval #25、语义层 DRY、A/B 评分工具链（详见技能 changelog）
- **huawei-cloud-cost-estimation** **1.0.2**：BSS cli-region 规则与 eval #11（详见技能 changelog）

## 3.0.2 - 2026-05-29

### 变更

- **huawei-cloud-cost-estimation** **1.0.1**：BSS 命令/语义对齐、`response_contract`、CLAUDE 分层 DRY、10 条 eval 与 A/B 评分工具（详见技能 changelog）

## 3.0.1 - 2026-05-28

### 变更

- **版本**：各技能 `qa/<name>/VERSION`；billing-scout **2.3.8**、cost-estimation **1.0.0**（与误绑定的 repo v3.0.0 技能版本解耦）
- **changelog**：拆分到 `qa/<name>/CHANGELOG.md`（及 `.zh.md`；本文件为仓库索引）

### 文档

- README：双技能设计、安装、验证与版本表更新

## 3.0.0 - 2026-05-28

### 变更

- **CI**：validate 工作流安装必需 QA 工具；skill-scanner 必装
- **hooks**：`.githooks/pre-commit` → `validate-all.sh`；`tools/install-git-hooks.sh`

### 新功能

- monorepo 新增 **huawei-cloud-cost-estimation** 技能与 QA（详见该技能 changelog **1.0.0**）
