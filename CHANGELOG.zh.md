# 更新日志

Monorepo **基础设施**变更。各技能独立 changelog：

| 技能 | 更新日志 |
| --- | --- |
| huawei-cloud-billing-scout | [qa/huawei-cloud-billing-scout/CHANGELOG.zh.md](qa/huawei-cloud-billing-scout/CHANGELOG.zh.md) |
| huawei-cloud-cost-estimation | [qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md](qa/huawei-cloud-cost-estimation/CHANGELOG.zh.md) |
| huawei-cloud-account-onboarding | [qa/huawei-cloud-account-onboarding/CHANGELOG.md](qa/huawei-cloud-account-onboarding/CHANGELOG.md) |
| semantic-creator | [qa/semantic-creator/CHANGELOG.md](qa/semantic-creator/CHANGELOG.md) |
| semantic-pkm-creator | [qa/semantic-pkm-creator/CHANGELOG.md](qa/semantic-pkm-creator/CHANGELOG.md) |
| concept-design | [qa/concept-design/CHANGELOG.md](qa/concept-design/CHANGELOG.md) |
| concept-prd | [qa/concept-prd/CHANGELOG.md](qa/concept-prd/CHANGELOG.md) |
| concept-implementation | [qa/concept-implementation/CHANGELOG.md](qa/concept-implementation/CHANGELOG.md) |
| concept-audit | [qa/concept-audit/CHANGELOG.md](qa/concept-audit/CHANGELOG.md) |
| concept-guardrails | [qa/concept-guardrails/CHANGELOG.md](qa/concept-guardrails/CHANGELOG.md) |

## 3.14.0 - 2026-08-28

### 新功能

- **jackson-concept-design** **0.2.0**：扩充 Sync 记法（include/when、反应式/原子/行为保持）、欠同步/过同步/flow/synergy，以及 Parnas 依赖图子集（MVP 与讲解顺序）；模型确认后路由到伴生技能（详见技能 changelog）
- **jackson-concept-prd** **0.1.0**：新增转录技能，把已确认的概念模型写成 PRD 文档族——总体 PRD、每概念一份子 PRD、syncs 按 flow 分组；不发明模型外内容（详见技能 changelog）
- **jackson-concept-implementation** **0.1.0**：新增映射技能，把已确认的概念模型落地为模块单体——一个 concept 一个模块，sync 落在组合层（mediator 或规则引擎）；按需加载 Rust、Java/Spring Modulith、TypeScript 说明（详见技能 changelog）
- **jackson-concept-audit** **0.1.0**：新增只读五维审计，对照概念模型或 PRD 与代码，给出带证据的发现并路由到 design / prd / implementation（详见技能 changelog）

## 3.13.0 - 2026-08-27

### 新功能

- **wyx-zh-cn** **0.26.0**：新增 [jlifyio/wyx](https://github.com/jlifyio/wyx) v0.26.0 的中文改写版
  —— 用与代码同目录的 CONCEPT/PIPELINE/SYNCS 规格声明模块边界，审计覆盖缺口并按依赖排序给出命令计划，
  用校准过的严重度与跨规格引用校验检测规格漂移，生成 Mermaid 架构地图；上游五条斜杠命令合并为一个技能的
  六种路由模式，上游 Claude Code hooks 运行时逐字节原样收录于 `runtime/`，作为可选的边界注入层
  （保留 MIT 声明，详见技能 changelog）

## 3.12.0 - 2026-08-27

### 新功能

- **jackson-concept-design** **0.1.0**：新增 Jackson 概念建模技能，以 Purpose、Operational
  Principle、State 和 Actions 定义独立 concepts，用专一、完整、独立、熟悉审查边界，通过
  synchronizations 组合应用行为，并在 PRD、架构或代码之前停于模型确认（详见技能 changelog）

## 3.11.0 - 2026-08-24

### 新功能

- **huawei-cloud-account-onboarding** **1.0.0**：重写为真实的只读 BSS 人脸认证命令（`ShowRealNameAuthStatus` + `ShowRealNameAuthQrCode`）——概念层/命令层参考拆分、SKILL.md 收为精炼入口、TypeScript 终端二维码渲染器为唯一脚本、`--cli-waiter` 轮询、跨层命令合同与可选真实冒烟；取码命令自身不设的门禁改由技能承担，移除本地 mock 服务；已发布至 ClawHub（详见技能 changelog）

## 3.10.1 - 2026-08-24

### 修复

- **huawei-cloud-cost-estimation** **3.2.4**：IAM 权限文档上提为技能级横切（开通写权限原则 + 询价只读分层）；参数类 CBC 错误迁入 pricing 陷阱；Reference Index 按概念层/命令层同构（详见技能 changelog）

## 3.10.0 - 2026-08-18

### 新功能

- **sce-creator** **0.1.0**：新增两轮萃取技能，从原文提取可调用的场景、概念与实体（详见技能 changelog）

## 3.9.3 - 2026-08-03

### 修复

- **huawei-cloud-cost-estimation** **3.2.3**：在过滤后的 `ListUsageTypes` 之后补 Measure Resolve（用量槽/容量槽、因子族→度量/`usage_value`）；压缩 pricing commands；OBS 探针要求 `usage_measure_id=10`

## 3.9.2 - 2026-08-03

### 修复

- **huawei-cloud-cost-estimation** **3.2.2**：询价解析链写死（`ListServiceResources` → `ListResourceSpecs` → 带 filter 的 `ListUsageTypes` → 询价）；禁止默认 Duration/小时；新增 eval #20–29 与 OBS/RDS 解析探针 grader 分支

## 3.9.1 - 2026-08-01

### 修复

- **huawei-cloud-cost-estimation** **3.2.1**：将密集的 Call Budget 标签改为两句易懂的执行节奏规则，保持命令限量与安全门禁不变

## 3.9.0 - 2026-08-01

### 新功能

- **constraint-charter** **0.1.0**：把 Uncle Bob 式审计目标与数值门禁固化为版本化 `GATES.md`，并接入 pre-commit/CI
- **huawei-cloud-cost-estimation** **3.2.0**：为长 `hcloud` 命令链增加有界渐进执行协议，同时保留完整批次 dry-run 与确认门禁（详见技能 changelog）

## 3.8.0 - 2026-07-14

### 新功能

- **huawei-cloud-cost-estimation** **3.1.0**：新增 `CloudIDE/CreateInstance`；全面精修 74 个生命周期命令语义（官方产品名、API 版本、计费边界）；CodeArts 普通 `Create*` 继续排除；退订仍仅控制台指引（详见技能 changelog）

## 3.7.0 - 2026-07-14

### 新功能

- **huawei-cloud-cost-estimation** **3.0.0**：退订降级为仅控制台指引 — 不运行或输出退订 CLI/API；73 个白名单开通命令保留 `--dryrun`/费用/确认门禁；更新 eval #17 与写边界校验（详见技能 changelog）

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
