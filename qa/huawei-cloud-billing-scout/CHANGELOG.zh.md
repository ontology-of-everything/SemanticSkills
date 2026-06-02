# huawei-cloud-billing-scout 更新日志

仅本技能变更。仓库级变更见 [../../CHANGELOG.zh.md](../../CHANGELOG.zh.md)。

## 2.3.9 - 2026-06-02

### 新增

- **SKILL.md**：BSS 端点规则 — 所有 `hcloud BSS` 固定 `--cli-region=cn-north-1`
- **eval #25** `bss-cli-region-not-profile-default` + cli-region 断言；真实 hcloud A/B
- **qa**：A/B 工具链 — `run_ab_eval.py`、`grade_response.py`、`aggregate_ab.py`；`assertions/README.md` 说明 Skill Creator 流程

### 变更

- **semantic**：瘦身 `billing-ontology.yml` / `catalog.yml`（事实、粒度、`source_operations`；查证流在 SKILL.md）
- **gate**：`HUAWEICLOUD_BILLING_SCOUT_REAL=1` 时 `gate full` 执行 `smoke_real_bss.py`

## 2.3.8 - 2026-05-28

### 变更

- **SKILL.md**：**华为社区版** 声明；边界节删除重复的「官方身份」（DRY）
- **qa**：`gate.py full` 强制 skillcheck、markdownlint、skill-scanner（`require_all=True`）
- **版本**：独立 `qa/huawei-cloud-billing-scout/VERSION`（与仓库根 `VERSION` 解耦）

### 文档

- `docs/skills/huawei-cloud-billing-scout.md` 版本 **2.3.8**；询价指向 cost-estimation 技能
- README 技能表与 `docs/catalog.yml` 对齐

## 2.3.7 - 2026-05-26

### 变更

- 收回到**仅账务**只读 BSS 边界 — 移除报价试算与实名审核；**53** 个只读 op（原 58）；同步本体、命令、IAM、契约
- `catalog.yml`：`provider_gate`、`out_of_scope`、华为云前缀 triggers

### 新功能

- 重组 `SKILL.md`（原则 / 分工 / 四阶段查证 / 红线 / 答复 / 边界）
- 对话推进纪律 — eval 22–24；共 **24** 条 eval

### qa

- **`refuse-*`** 替代已删用例；门禁 **53** 针脚；更新 `protocol_grading.py`

## 2.3.5 - 2026-05-24

### 变更

- ClawHub 英文展示名与加长 `description`（中文展示名不变）

## 2.3.4 - 2026-05-24

### 变更

- 展示名 **华为云 · 花多少为何扣 · 只读对账**；ClawHub 安全审计对齐；离线门禁 `bin/gate.py`

## 2.3.2 - 2026-05-24

### 变更

- **IM 交付** — 禁用 GFM 管道表；简报式 **答复格式**；FinOps 结构重组
- rubric、协议 eval 金答案、style 审计配置

## 2.3.1 - 2026-05-23

### 变更

- 语义层合并为 `catalog.yml` + `billing-ontology.yml`；精简命令附录；**21** 条 eval

## 2.0.0 - 2026-05-22

首次公开发布：本体语义驱动、**58** 个 BSS 只读 Operation、只读边界。
