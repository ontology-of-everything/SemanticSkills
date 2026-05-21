# Semantic Skills

> 社区版本，非华为云官方。

云场景里 Agent 出错方式很固定：账期粒度选错、对账步骤跳过、表格没出来就敢下结论。SemanticSkills 用 [Agent Skills](https://agentskills.io/) 把领域语义放进可版本化的 `references/`，而不是堆在 `SKILL.md` 里——先对齐「查什么事实」，再决定「怎么查命令」。

English: [README.md](README.md).

## 设计思路

**本体语义先行。** 每个技能在 `references/semantic/*.yml` 里定义稳定的事实实体（粒度、维度、指标）；命令参数单独一层，语义层不复制 API 字段。协作手册叠在上面：负责把用户意图分流到协作能力、查询顺序和输出形态，不重复语义模型。

运行时一条问题走这条链：

```text
用户问题
     │
     ▼
协作手册 ──► 能力 → 内部口径 → 查询顺序 → 用户可读输出
     │
     ▼
本体语义 ──► 选定事实实体（references/semantic/*.yml）
     │
     ▼
命令层 ────► 只读操作（如 hcloud BSS）
     │
     ▼
证据表 → 小结 → 用户可读说明 → 证据边界
```


| 层    | 放什么               | 典型文件                                         |
| ---- | ----------------- | -------------------------------------------- |
| 本体语义 | Agent 可引用的事实实体    | `references/semantic/*.yml`、`*-semantics.md` |
| 协作手册 | 协作能力、内部口径、查询顺序、用户可读输出 | `*-playbook.md`                              |
| 命令   | 仅 API/CLI 映射      | `related-commands.md`、IAM、安装说明               |


`skills/<name>/` 是可安装运行时包；`qa/<name>/` 放 eval 与验证脚本，不会被 `npx skills add` 复制。兼容 Claude Code、Cursor、Codex CLI 与 [SkillsMP](https://skillsmp.com/) 收录。

示例：[huawei-cloud-billing-scout](docs/skills/huawei-cloud-billing-scout.md)。编写规范：[docs/authoring.md](docs/authoring.md)。

## 仓库布局

```text
SemanticSkills/
├── skills/              # 可安装运行时包（SKILL.md + references/）
├── qa/                  # 各技能验证（evals、assertions、validate.sh）
├── docs/                # 贡献指南、编写规范、catalog、各 agent 安装说明
├── tools/               # validate-all.sh、skill-scaffold.sh
├── template/skill/      # 新技能脚手架（不可安装）
├── .workspaces/         # Skill Creator 运行结果（不入库）
├── .agents/             # 本地 npx skills add 副本（不入库）
└── .credentials/        # 本地凭据样例（不入库）
```

## 技能


| 技能                           | 路径                                   | 摘要                    | 文档                                              |
| ---------------------------- | ------------------------------------ | --------------------- | ----------------------------------------------- |
| `huawei-cloud-billing-scout` | `skills/huawei-cloud-billing-scout/` | 华为云账务只读侦察（KooCLI/BSS） | [详情](docs/skills/huawei-cloud-billing-scout.md) |


机器可读索引：[docs/catalog.yml](docs/catalog.yml).

## 安装

从 GitHub 安装（[Cursor 说明](docs/agents/cursor.md)）：

```bash
npx skills add ontology-of-everything/SemanticSkills \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy
```

本地路径：

```bash
npx skills add ./skills/huawei-cloud-billing-scout \
  --skill huawei-cloud-billing-scout \
  --agent cursor \
  --copy
```

## 验证

全部技能：

```bash
./tools/validate-all.sh
```

单个技能：

```bash
./qa/huawei-cloud-billing-scout/validate.sh
```

可选真实 BSS 烟测：

```bash
HUAWEICLOUD_BILLING_SCOUT_REAL=1 \
HUAWEICLOUD_BILLING_SCOUT_CYCLE=2025-04 \
./qa/huawei-cloud-billing-scout/validate.sh
```

## 贡献

见 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) 与 [docs/authoring.md](docs/authoring.md).

新建技能：

```bash
./tools/skill-scaffold.sh <skill-name>
```

## SkillsMP

每个技能位于 `skills/<name>/SKILL.md`，包含 `name`、带触发词的 `description`，以及可选的 `license` / `compatibility` / `metadata` 便于市场收录。