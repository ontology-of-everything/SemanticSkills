# 行为断言

以 `../evals/evals.json` 为案例源，评估结果而不是固定措辞。

- 显式启用策略保持；按 `$concept-guardrails <模式>` 识别 audit、concept、drift、pipeline、sync、map，不使用 `wyx:` 前缀。
- 路径→回填、描述→新建、无参数→发现；未指定模式或项目无规格时走 audit。
- 只产出 Jackson 记法；遇到 wyx 原生段落标为待迁移，不消费、不混写、不部分修改。
- 已授权的写入不重复确认；覆盖/漂移只读，不生成历史记录。
- 严重度有当前证据与影响依据，已知 coupling 不自动隐藏风险。
- 地图检查完整来源和删除变化，保留合取、查询与产品依赖的区别。
- 空 query 不产生错误，后台事件不强求响应；需要响应的请求有结果与关联。
- hooks 只能列规格与注入 PIPELINE data boundary，不能宣称已验证概念边界。
