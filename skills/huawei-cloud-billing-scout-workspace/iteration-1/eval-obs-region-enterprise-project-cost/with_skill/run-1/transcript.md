## Eval Prompt

上个月华南一区 OBS 花了多少钱，按企业项目拆一下。

## Steps

1. 载入技能默认时间口径：`上个月`→最近完整账期（本题注明 2026-04）。
2. 对齐术语：OBS、`cn-south-1`/`REGION_CODE`、`ENTERPRISE_PROJECT_ID`。
3. 采用 playbook「月花费」路径：**月汇总成本分析先于详单**；引用 `references/related-commands.md` 中 `ListCosts` / `ShowCustomerMonthlySum`，不执行真实 CLI。
4. 输出：**结果表（按企业项目金额+占比）→ 小结 → 统计范围说明**。
5. 强调结论依赖查询回填，控制台数字不得直接当作最终答案。

## Result

已给出符合 BSS 多维拆分的占位表与只读命令链；无实时 API。
