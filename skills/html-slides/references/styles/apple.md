# styles/apple.md — Apple 发布会风格（经验版）

依据：Apple 公开发布会 / Keynote 视觉惯例的经验归纳，**无官方样本逐页分析**，标注为经验版。资产：`assets/apple/`（`vars-dark.css`、`vars-light.css`、`style.css`）；无随包素材、不含任何 Apple 商标。

## 1. 识别特征

纯黑底 + 白字 + 一页一句的超大单点大字；产品图居中、四周大留白；关键词或数字用渐变文字强调；几乎没有卡片边框，靠明度差分区；页面上极少文字，信息密度低、页数多。

## 2. 变量说明

- 默认 `vars-dark.css`（纯黑）；产品白色主题段落或打印用 `vars-light.css`（暖白 `#f5f5f7` 系）。
- `--accent` 蓝 `#2997ff`（深）/ `#0071e3`（浅）；`--accent-2` 紫 `#bf5af2` 只作渐变第二端与次要标签。
- 字体栈优先 SF Pro（macOS 自带），其余平台回退 PingFang / Noto Sans SC；圆角 18px；`--shadow:none`。
- 换主色：只改 `--accent` / `--accent-soft`；渐变端 `--accent-2` 选同明度邻近色。

## 3. 配色公式

深色：黑底 + 白字 + 单点渐变强调；一页最多一处渐变（标题关键词或一个数字）。浅色：暖白底 + 近黑字 + 灰卡（`--surface`）。不用红色作警示；不用表格粗黑边（本风格表格改 1px `--line` 网格、表头 `--table-head` 深灰）。

## 4. 字体与字号档

- 标题 600 字重、`-.03em` 字距；hero 一句 120px；正文短语卡档 18–24px。
- 数字大字 96px 白字（不上色），说明行 24px 灰。
- 文案：短断言（「更快。更轻。」），一页一个主张；不写导语段；不用 eyebrow 编号（可省略 `.eyebrow`）。

## 5. 页型倾向与专属页型

偏好：`quote`（改为 `.ap-hero` 大字页）、`full-image`、`kpi-band`（改用 `.ap-spec` 无边框三联）、`compare`、`image-text`。少用 `dense-columns`、`table-mix`、`case`；不用 `workshop` / `quiz`。允许连续 2 页同为观点家族（hero → 产品图）但仍受「连续 3 页」规则约束。

`style.css` 组件：

| class | 用法 |
| --- | --- |
| `.ap-hero` | 单点大字页：`<section>` 内只放一个 `.ap-hero`，可带 `small` 副句 |
| `.ap-grad` | 渐变文字：套在标题关键词或数字上，一页一处 |
| `.ap-product` | 产品图居中留白：图高 70%，`height:100%;width:auto` |
| `.ap-spec` | 规格三联：`.num` 白色 96px + 一行灰说明，无卡片边框 |
| `.card{border:0}` | 本风格卡片去边框，靠 `--surface` 明度分区 |

无 `patterns.html`；hero / 产品页用 `chapter` / `full-image` 骨架替换主体即可。

## 6. 品牌可替换点与素材

| 元素 | 默认 | 位置 | 替换方式 |
| --- | --- | --- | --- |
| 页脚 | 无（本风格不放页脚） | — | 用户要求页码时只放 `.foot-l` 页码 |
| 封面 | 黑底 + 一句大字 | `.cover` 内 `.ap-hero` | 文本；产品图用户自带 → data URI |
| 致谢 | 黑底一句 | `.thanks` | 文本 |

素材：无随包素材；Apple 商标与产品图一律用户自带且自行确认授权。
