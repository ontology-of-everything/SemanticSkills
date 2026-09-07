# Jackson 概念设计原始文献（本仓研究用镜像）

`jackson-concept-*` 四技能重构（2026-08-28）所依据的作者原文镜像与中文翻译。
每篇一对文件：`*.en.md`（原文抓取）与 `*.zh-CN.md`（中文全译）。
版权归原作者（Daniel Jackson 等）；本目录仅供本仓库研究与核证引用，不作再分发。

## 目录

| 文档 | 来源 | 文件 |
| --- | --- | --- |
| 资格判据（Concept criteria） | <https://essenceofsoftware.com/tutorials/concept-basics/criteria/> | `tutorials/criteria.en.md` / `.zh-CN.md` |
| Sync 组合（Concept composition） | <https://essenceofsoftware.com/tutorials/concept-basics/sync/> | `tutorials/sync.en.md` / `.zh-CN.md` |
| 依赖与子集（Dependencies and subsets） | <https://essenceofsoftware.com/tutorials/concept-basics/dependency/> | `tutorials/dependency.en.md` / `.zh-CN.md` |
| 概念设计综述（The Essence of the Essence） | <https://essenceofsoftware.com/posts/distillation/> | `posts/distillation.en.md` / `.zh-CN.md` |
| 设计动作（Design moves） | <https://essenceofsoftware.com/posts/design-moves/> | `posts/design-moves.en.md` / `.zh-CN.md` |
| WYSIWID 论文（Meng & Jackson, Onward! 2025；CC BY-NC 4.0，全文 + 全译） | <https://arxiv.org/abs/2508.14511> | `papers/2508.14511-wysiwid.en.md` / `.zh-CN.md` |
| Beyond Objects 论文（Jackson, 2026；Springer 版权，**逐节详细摘要**非全文） | <https://arxiv.org/abs/2606.27258> | `papers/2606.27258-beyond-objects.en.md` / `.zh-CN.md` |
| 6.1040 概念评分标准（concept rubric） | <https://61040-fa25.github.io/resources/concept-rubric> | `course/concept-rubric.en.md` / `.zh-CN.md` |
| 6.1040 概念规格模板说明 | <https://github.com/61040-fa25/concept_backend/blob/main/design/background/concept-specifications.md> | `course/concept-specifications.en.md` / `.zh-CN.md` |

## 未镜像、仅存链接

- Making Software Meaningful（Meng/Namazov/Schare/Cunha/Jackson, 2026）：<https://arxiv.org/abs/2606.11051>
- A Concept Experiment at Palantir：<https://essenceofsoftware.com/posts/palantir/>
- 官方课程模板仓库 conceptbox：<https://github.com/61040-fa25/conceptbox>

## 完整性说明（2026-08-28 抓取）

- 教程、博客、课程材料六篇：全文抓取无截断；仅 dependency 篇的两张依赖图**插图**无法以文本保留（正文文字完整）。
- WYSIWID：CC BY-NC 4.0 许可下全文转录 + 全译（摘要、§1–9、附录 A–C）；附录 A.2 两个行内 IRI 在 arXiv HTML 渲染中本身缺失，见文末声明。
- Beyond Objects：受版权限制未逐字转录，为**逐节详细摘要**（摘要、§1–14、全部脚注；规格与 sync 代码块原样保留）；引用原句请回原文核对。

## 翻译约定

- 全文忠实翻译，不删节；术语首次出现保留英文（concept、synchronization/sync、purpose、
  operational principle/OP、state、actions、queries）。
- 代码块、规格示例、记法原样保留不翻译。
- 每篇文件头注明来源 URL 与抓取日期；抓取如有截断在文末声明。
