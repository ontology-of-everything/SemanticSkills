# 概念审计（Jackson）

`concept-audit` · **Concept Audit (Jackson)** · 原名 `jackson-concept-audit`

> 本文是给人看的中文说明，**不是** `npx skills add` 安装包内容。Agent 加载 [`skills/concept-audit/SKILL.md`](../../skills/concept-audit/SKILL.md)。

**Version:** 0.3.0 · Changelog:
[qa/concept-audit/CHANGELOG.md](../../qa/concept-audit/CHANGELOG.md)

## 一句话

只读对照概念模型（或 PRD 文档族）与代码，按规格漂移、边界违规、判据重审、组合质量、依赖与子集五维给出带证据的发现，并路由到 design / prd / implementation 修复。

## 适用场景

- 已有 Jackson 模型或 PRD，需要核对应代码是否仍一一对应。
- 模块互引、共享表、DTO 进概念签名等边界问题需要定位，而不是立刻改代码。
- 持续看护已由 CI 架构测试承担，需要一次周期或按需的人工审计。

## 方法

1. 定位规格（与代码共存的 CONCEPT.md / SYNCS.md 加 `docs/prd/`）与工程自带的模块/依赖图素材。
2. 规格漂移按校准过的检查表逐类别对账（严重度只降不升、越级重新归类）；规格 ≥5 份时用只读子代理并行扫描。
3. 跨规格校验 sync 引用、系统性模式聚合、跨维度合并根因，修复顺序上游优先。
4. 全程只读，不修改任何文件。

## 安装载荷

```text
skills/concept-audit/
├── SKILL.md
└── agents/openai.yaml
```

```bash
npx skills add ./skills/concept-audit \
  --skill concept-audit \
  --agent codex \
  --copy
```
