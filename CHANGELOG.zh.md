## 1.0.5 - 2026-05-21

### 修复
- 收紧 `huawei-cloud-billing-scout` 只读边界，避免将 BSS `List*ChangeRecords` 流水证据查询误判为写操作
- 修正 `ResourceBillDetail` 中 `resource_type_code` 的语义路径

### 测试
- 增加只读 ChangeRecords 策略和资源详单字段路径的防回归验证

## 1.0.4 - 2026-05-21

### 重构
- 优化 `huawei-cloud-billing-scout` 输出结构：用用户可读说明替代固定查询口径表达，默认隐藏技术细节，并仅在影响结论时追加待核验边界

### 文档
- 更新 README、技能文档与 QA 断言，说明用户可读账务输出和证据边界规则

## 1.0.3 - 2026-05-21

### 重构
- 将 `billing-scenarios` 与 `billing-scout-workflow` 合并为 `billing-playbook`，按协作能力（查事实、归因、对账、咨询）组织

### 文档
- 更新 README、技能文档与验证布局，采用协作手册优先架构

## 1.0.2 - 2026-05-21

### 文档
- README / README-CN 新增本体语义驱动设计说明：语义分层、运行时流程、`skills/` 与 `qa/` 分工

## 1.0.1 - 2026-05-21

### 重构
- 采用标准 monorepo 布局（方案 B）：`qa/`、`docs/`、`tools/`、`template/` 与 GitHub 验证工作流

### 文档
- README、README-CN 与 `huawei-cloud-billing-scout` SKILL.md 添加社区版本声明（非华为云官方）

## 1.0.0 - 2026-05-21

### 新功能
- [SemanticSkills](https://github.com/ontology-of-everything/SemanticSkills) 首次发布，包含 `huawei-cloud-billing-scout`：基于 KooCLI/BSS 的华为云账务只读侦察（找事实、做归因、做对账、做咨询）

### 文档
- README / README-CN：单仓布局、SkillsMP 收录说明与 GitHub 安装方式
- SKILL.md frontmatter 对齐 agentskills.io 与 SkillsMP 索引要求

### 测试
- 验证流程：`skills-ref validate`、skillcheck、markdownlint、skill-scanner、Cursor 安装烟测
- `skillcheck.toml` 声明 agentskills.io 扩展字段（`license`、`compatibility`、`metadata`）

### 维护
- 本地路径不入库：`dev/`、`.agents/`、`.workspaces/`、`.credentials/`
