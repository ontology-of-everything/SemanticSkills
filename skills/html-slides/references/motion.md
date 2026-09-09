# motion.md — 手动推进动画：build 与 layer

**动画只靠讲者手动推进，绝不自动循环。** 目的是控制讲课节奏，不是炫技。汇报与自读默认全静态；只有授课场景按讲课节拍设计。页面上**不写任何操作提示**（「点击查看」「点击切换」）。运行时实现见 `deck-format.md` §5，本文只讲写法与设计法。

## 1. 放映键位（交付时告诉用户）

| 操作 | 效果 |
| --- | --- |
| `P` / 右上 ▶ | 进入放映（自动全屏）；`P` / ☰ 回滚动阅读 |
| `→` / `PageDown` / 空格 / 点击空白 / 向下滚轮 | 前进一拍；本页拍完翻下一页 |
| `←` / `PageUp` / 向上滚轮 | 回退一拍；本页回完翻回上一页（落在末拍） |
| `Home` / `End` | 首页 / 末页 |
| `F` | 切换全屏 |
| 刷新 | 回到上次所在页（`#页号` 优先，其次 localStorage） |

滚动模式下所有 build 已显示、layer 可点击切换，便于阅读、审阅与 `?debug`。

## 2. build：逐步揭示

元素加 `class="build"` 与 `data-step="N"`；同一 `data-step` 的多个元素同拍齐现。示例见 `assets/core/skeletons.html`「流程条」段。

- 放映态 `level` 从 0 起，每前进一拍 +1；`level > data-step` 的 build 显示。
- **初始就该显示的元素不要加 `class="build"`**。
- **版块的外层框也要挂 build**，不能只挂框内内容，否则进页时空框先露出来。
- 拍数 = 页内最大 `data-step` + 2（进页空场 1 拍 + 讲完翻页 1 拍）。

## 3. layer：页内互斥画面

标签页、方案切换、阶段视图、题卡翻面——所有「一个区域多个画面互斥」都用这一套，不自造状态机。按钮 `data-layer-btn="key"`、面板 `data-layer-panel="key"`，二者同 `data-layer-group`；示例见 `assets/core/skeletons.html`「layer 互斥画面」段。

- 按钮与面板同 key 同 group 配对；每组恰有一个默认按钮 + 面板带 `data-active`，默认按钮**不写** `data-step`，其余从 0 连续编号。
- **给按钮加 `data-step` 才会被方向键推进**；引擎选组内 `data-step < level` 的最大者，没有则回默认层。全不挂 `data-step` 的组只靠手点。
- 按钮和面板从初始 DOM 起固定存在，切换只增删 `data-active`；不得点击时用 `innerHTML` 重建。
- 一页可放多组，靠 `data-layer-group` 隔离。

**混合链**：同页 build 与 layer 共享 `level`。layer 按钮吃掉前几拍（整版切换），某面板内的 build 用更大的 `data-step` 接着逐条出现。例：3 标签（step 0,1）+ 面板内 3 个 build（step 2,3,4）= 6 拍。

## 4. 「先排拍后编号」

1. 先列**讲稿节拍表**：第 1 拍讲什么、出现哪些元素；第 2 拍……直到讲完。一个知识节拍里相关的 bullet、箭头、caption 归**同一拍**，别把一句话拆成三次点击。
2. 把表翻译成编号：每拍一个 `data-step`，从 0 连续递增；layer 按钮先占位，面板内 build 接后。
3. 检查进页空场（level=0）该显示什么——没挂 build 的元素就是空场内容。
4. 逐页表「拍数」列同步。

## 5. 验证与铁律

- 放映模式从该页第一拍手动按到翻页，对着节拍表核对每拍出现的内容；拍数对不上通常是编号跳号 / 重复，或该挂 build 的元素漏挂。
- `?debug` 在滚动模式测量：非激活 layer 面板不参与，**每个标签手动切一遍**再看溢出。
- 不用 `:has()` 控制 opacity；SVG 元素既是 `.build` 又带 `transform` 时，把 transform 移到外层非 build 的 `<g>`。
- 不写 SMIL / CSS 循环动画作为内容表达；确需装饰性连续动效时不得占节拍、不得抢注意力。
- 汇报导 PPTX 时 build 全部展开、layer 每标签一页（`tools/export_pptx.py` 自动处理）。
