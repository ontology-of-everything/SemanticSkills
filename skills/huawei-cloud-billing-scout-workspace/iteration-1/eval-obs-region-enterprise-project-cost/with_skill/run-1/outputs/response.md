## 结果表（占位示例 — 需 KooCLI 只读回填）

以下为**示意结构**；数值非真实查询结果。**未执行真实 hcloud**。请在你侧以只读 BSS 调用 `ShowCustomerMonthlySum` / `ListCosts`（`GROUPBY ENTERPRISE_PROJECT_ID`，并限定云服务与 region）生成的行替换。

| 企业项目 | 企业项目 ID（尾号） | OBS 应付金额(元) | 占华南一区 OBS 小计 |
| --- | --- | --- | --- |
| default | …`0001` | 312.80 | 52.1% |
| prd-data | …`88ac` | 186.40 | 31.0% |
| shared-tools | …`42f0` | 101.50 | 16.9% |
| **合计** | — | **600.70** | **100%** |

*金额口径：示例按**应付/官网成本类展示**；实付需含券/储值/授信维度时在 `amount_type` 上与财务口径对齐后再出表。*

## 小结

这是**多维成本查询**：把「上月 + 华南一区 + OBS + 按企业项目拆分」落到 BSS 成本分析/月汇总的**分组证据**上。先月级或 `ListCosts` 聚合到企业项目，再视需要下钻 `ListCustomerselfResourceRecordDetails` 查资源级差异。无查询结果前**不对控制台概览数字下结论**。

## 用户可读说明（统计范围）

- **“上个月”口径**：在 2026-05 询问时，解析为**最近完整自然月/账期 2026-04**（若你司账期与自然月不一致，以 BSS `bill_cycle` 字段为准并替换起止日）。
- **地域**：**华南一区**映射为 `cn-south-1`（广州）；所有行必须带该 `region`/区域过滤或通过成本维度 `REGION_CODE` 限定。
- **产品**：云服务维度限定为 **OBS / Object Storage Service**（具体 `cloud_service_type` 编码以 `hcloud BSS ... --help` 与实际返回为准）。
- **分组**：主维度为 **`ENTERPRISE_PROJECT_ID`**；表内给出每项目金额与占比，总行数为你的项目数量（示例 3 行 + 合计）。

## 建议的只读下一步（KooCLI）

1. **月汇总或过账期切片**：`hcloud BSS ShowCustomerMonthlySum --bill_cycle=2026-04 …` 快速核对 OBS 在华南是否集中（参数组合以控制台同等筛选为准）。
2. **首选成本分析**：`hcloud BSS ListCosts` — `time_condition` 覆盖 **2026-04-01 至 2026-04-30**（或与账期等价窗口），`--groupby` 先用 `CLOUD_SERVICE_TYPE` + `REGION_CODE`，再第二层 `ENTERPRISE_PROJECT_ID`; 可加 `--cli-query` 做 JMESPath 脱敏导出。
3. **钻取**：对占比异常项目，再用 `ListCustomerselfResourceRecordDetails` **同周期、同 region、OBS、同 enterprise_project_id** 定位资源热点。
