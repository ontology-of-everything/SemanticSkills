## Eval Prompt

我这个月为什么一直扣钱，帮我看看还有哪些资源在计费。

## Steps

1. 读取 `SKILL.md`：确认只读 BSS、表格优先、结果表→小结→用户可读说明、拒绝写操作与完整 ID 暴露。
2. 读取 `references/billing-playbook.md`：将问题分流为「归因 / 持续扣费」，选择 `ResourceBillRecord` → `ResourceBillDetail` 查询顺序与 TopN 呈现规则。
3. 读取 `references/billing-semantics.md`：对齐账期、区域、企业项目、指标（如 `consume_amount`）等维度表述。
4. 读取 `references/related-commands.md`：引用 `ListCustomerselfResourceRecords`、`ListCustomerselfResourceRecordDetails` 等只读 KooCLI 入口；**不调用真实 hcloud**。
5. 构造占位结果表（脱敏尾号）、小结与查询说明，并列出只读后续命令。

## Result

已输出符合技能结构的归因答复：持续扣费路径、BSS 只读证据链、表格列与时间/账号/TopN 说明、ID 脱敏与写操作拒绝；无真实 API 数据。
