# 更新日志

## 3.0.0 - 2026-05-28

### 新功能

- **huawei-cloud-cost-estimation**：新增华为云下单前 BSS 询价技能 — 包年/包月
  （`ListRateOnPeriodDetail`）与按需（`ListOnDemandResourceRatings`）；Parse / Clarify /
  Spec Review / Estimation 工作流；`rfq-*-model.yml` 语义路由
- **huawei-cloud-cost-estimation**：QA 包 — `validate.sh`、7 条离线 eval、skillcheck/markdownlint 门禁

### 变更

- **project**：CI validate 工作流安装必需的 Python/Node QA 工具；skill-scanner 必装
- **project**：跟踪 `.githooks/pre-commit` 跑 `validate-all.sh`；
  `tools/install-git-hooks.sh` 设置 `core.hooksPath`
- **huawei-cloud-billing-scout**：`gate.py full` 强制 skillcheck、markdownlint、skill-scanner
  （`require_all=True`）

### 文档

- **huawei-cloud-cost-estimation**：`docs/skills/huawei-cloud-cost-estimation.md` 与
  `docs/catalog.yml` 索引
- **project**：README 技能表增加 cost-estimation

## 2.3.7 - 2026-05-26

### 变更

- **huawei-cloud-billing-scout**：收回到**仅账务**只读 BSS 边界 — 移除报价试算与实名审核
 （`quote_and_identity`），对齐 **53** 个只读 BSS 查询操作（原为 58）；同步本体、路由、命令附录、
 IAM 与 `ops_contracts`
- **huawei-cloud-billing-scout**：`catalog.yml` 增加 **`provider_gate`**（未表明华为云/BSS/ profile
  前须澄清）、**`out_of_scope`** 拒答说明，以及带 **华为云** 前缀的入口 `triggers`

### qa

- **huawei-cloud-billing-scout**：以 **`refuse-*`** eval 替代已删除的报价/实名用例；更新
  `protocol_grading.py`；门禁文档针脚与 **53** 操作、`verify_ops` 输出一致

### 文档

- **huawei-cloud-billing-scout**：`docs/skills/...md`、`docs/catalog.yml` 版本 **2.3.7**；
 ClawHub 发布说明与 clawscan 文案


### 新功能

- **huawei-cloud-billing-scout**：重组 `SKILL.md`（原则 / 分工 / 四阶段查证表 / 红线 / 答复 / 边界）；扩充 `related-commands.md` BSS 模板
- **huawei-cloud-billing-scout**：对话推进纪律 — eval 22–24、`protocol_grading.py`、rubric `interaction_discipline`；共 **24** 条 eval

### 变更

- **qa/huawei-cloud-billing-scout**：gate 导出条数随 eval 数量；禁止 `skills/*-workspace`（Skill Creator 输出须在仓库根目录）

### 文档

- **authoring**：全技能对话推进纪律；SkillsMP 单仓 topic 索引说明
- **project**：`CLAUDE.md` 明确 Skill Creator workspace 位置；README 与各 agent 指南链到纪律章节

### 模板

- **template**：`validate.sh` 拒绝 `skills/` 下的 `*-workspace`

## 2.3.5 - 2026-05-24

### 变更

- **huawei-cloud-billing-scout**：ClawHub 以英文展示名为主
  **Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation**；加长英文
  `description` 便于搜索与技能路由（中文展示名 **华为云 · 花多少为何扣 · 只读对账** 不变）

## 2.3.4 - 2026-05-24

### 变更

- **huawei-cloud-billing-scout**：ClawHub 展示名 **华为云 · 花多少为何扣 · 只读对账**
  （英文：*Huawei Cloud: Spend, Charges & Reconcile (Read-Only)*）；slug 不变；
  `description` 与 `docs/catalog.yml` 的 `display_name*` 对齐用户意图词
- **huawei-cloud-billing-scout**：对齐 ClawHub 安全审计 — 仅华为云边界、description 与
  catalog 范围一致、答复语言跟随用户、收紧触发词；安装文档仅用户执行（Agent 禁止安装/`sudo`）
- **qa/huawei-cloud-billing-scout**：离线门禁统一为 `bin/gate.py`（`validate.sh` → full；
  `gate.py style` 负责 style 工具）

## 2.3.2 - 2026-05-24

### 变更

- **huawei-cloud-billing-scout**：**修复 IM 交付** — 聊天单条消息禁用 GFM 管道表
  （`|...|`），适配飞书、微信等渠道；改为简短小结 + 事实要点（`·` 或分段）
- YAGNI **答复格式** 取代僵硬三列表头；**易懂的事实称呼**（与对话/控制台一致，正文不写 API 名）
- **SKILL.md** 按 FinOps 重组：工作准则 / 安全红线 / 查证路径 / 答复格式
- **qa/huawei-cloud-billing-scout**：对齐 `llm-rubric.yml`、协议 eval 金答案与
  `validate.sh` 门禁；离线 benchmark 记录金答案生成的真实耗时（非占位 LLM 时间）

### 新增

- `qa/huawei-cloud-billing-scout/bin/skillgate.sh` 及 `skillcheck.toml`、`.markdownlint.json`、
  `policy.skill-scanner.yaml`（本地审计，不随 `npx skills add` 安装；ClawHub 兼容：frontmatter 不含 `license`）

### 文档

- 更新 `docs/skills/huawei-cloud-billing-scout.md` 与 QA README；发布记录合并至 `2.3.x`（移除 interim `1.0.x` ClawHub 重发条目）

## 2.3.1 - 2026-05-23

### 变更

- **huawei-cloud-billing-scout**：语义层合并为 `catalog.yml` +
  `billing-ontology.yml`（移除按实体 YAML 与 `billing-playbook.md`）；精简
  `related-commands.md` 并补齐已核验 KooCLI dot-notation 模板
- 压缩事实表输出（`已证实` / `待核验`）、**21** 条 eval，加强
  `validate.sh` / `verify_ops.py`；精简 `SKILL.md` 与路由头部（约 1% 降噪）

### 文档

- 更新 README、catalog 与各 Agent 安装说明（skills.sh、ClawHub、Hermes）

## 2.0.0 - 2026-05-22

[SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) 首次公开发布（社区版，非华为云官方）：本体语义驱动的计费侦察技能、**58** 个 BSS 只读 Operation、`skills/` + `qa/` 布局、只读 BSS 边界。
