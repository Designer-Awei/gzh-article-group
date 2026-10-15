# 03-magazine-feature

主色：玫红 #E11D48，正文/标题近黑 #111，大量细线。

## 组件（★ = 01 没有、其他两套也没有）
| 组件 | 说明 |
|---|---|
| ★ 刊头开头区 | 4px 粗线 + 1px 细线的双线刊头，「FEATURE · 特稿」栏目名 + 右侧日期（可省略）；「编者按」标签 + 20px 加粗导语当作特稿引题（standfirst）；署名栏「文 / <你的名字>」｜「阅读约 N 分钟 · N CHAPTERS」（上黑线下细线）。不放标题和副标题。参考 archive/themes-v1/theme-editorial-feature.md 组件 2/3（报头感、栏目线）和 references/theme-olive-journal.md 组件 4–6（刊头标签条、期号条） |
| ★ 杂志章节头 | 顶部细线 + 52px 细体（字重 200）玫红大数字 + 「CHAPTER 0N」字距标签 + 21px 标题 |
| ★ 杂志拉引（pull quote） | 金句不装卡片：60px 「“」+ 20px 粗体 + 底线 |
| ★ 细线重点列表 | 每条一道细线 + 细体序号 |
| ★ 细线表格 / 顶线对比栏 | 表格只留横线；对比卡改为两栏顶线 |
| ★ SMIL 菱形分隔 | 两条细线中间一个 animateTransform 旋转的菱形 |
| 无编号小标题 | 上方 24px 玫红短条 |
| 图注 | 左对齐、无框 |
| 引用 | 上标序号玫红；引用表上方 2px 黑线、表头 1px 黑线，编号玫红粗体，链接灰色，只有横向细线（和细线表格一致） |
| 高亮 / 划线 / 数字 | 浅玫红底 #FFE4E6 / 玫红字加下划线 / 19px，white-space:nowrap 不拆行 |
| 代码窗（2026-10-15h 起统一） | 原「附录框」作废：四套统一用 master/build.py 的终端代码窗（原 02 的窗口外框 + 深色终端，无「复制」、无「左右滑动」），本套 theme.py 不再覆盖 code_card |
| 章节内小标题 | `###` 或整行 `**…**`：8px 玫红实心方块 + 16px 加粗、字距 1px（章节头是 52px 细体数字 + CHAPTER） |

## 调性
严肃、有分量、留白多，像长篇特稿或杂志专栏。

## 适用
深度解读、行业趋势、长篇观点、人物/公司特写、报告解读；文字为主、截图少的稿子。

## 不适用
截图很多的实测/教程（细线框不住截图）；轻松段子类；需要大量步骤的操作指南。

## 参考来源（github.com/isjiamu/gzh-design-skill）
- archive/themes-v1/theme-editorial-feature.md（gallery-v1 magfeature.html）：刊头线、拉引、编者按
- references/theme-red-white.md：红白配色、细线
- 自己的设计：双线刊头 + 署名栏开头区、CHAPTER 标签、细体大数字模拟衬线感、SMIL 旋转菱形

## 衬线的替代做法（本套重点）
不能用 font-family，于是用：数字字重 200 + 52px、h1 顶 4px 线、细线分隔、「CHAPTER 0N」字距标签、标题 letter-spacing 1px，做出接近衬线杂志的感觉。

## 固定规则：对比卡中间不加 VS（2026-10-15 起）
- 所有版式的对比卡，两栏之间只用普通间距（4% 空白列）隔开，不放 VS、vs、「→」「对比」等任何中间标记。
- 两栏各占 48%，等高并排。

## 固定规则：素材截图不套外框、引用用 [xx] + 引用表（2026-10-15 起）
- 素材截图和 GIF 直接放裁好的图（只有 1px 浅灰细边 + 小圆角），不套窗口、相框；卡片/窗口只用在正文组件（导语、金句、要点、对比、代码）。
- 引用：正文句尾 `[xx]` 渲染成 11px 上标，和前一个字（或数据高亮）粘在一起不换行；文末「参考资料」+ 只有「编号 | 链接」两列的引用表，编号列 white-space:nowrap、宽度/最小宽度 44px，链接按稿件原样输出（纯文字，只在 / . - ? & = 后面断行）。取代旧的「句尾链接、最多 5 个」。
- publish 的 [cite] 检查正文序号和引用表一一对应，[ref] 检查两列格式、编号列 nowrap，并在 390px 下实测编号列不换行。

## 固定规则：不带标题、副标题交付为摘要；长链接只在符号处断行（2026-10-15 12:00 起）
- 成品里不放标题和副标题；副标题原文写进 `summary.txt`。开头区只用标签、日期（可省略）、阅读时长、章节数和导语。
- 参考资料表链接只在 / . - ? & = 后面断行（`<wbr>`），单元格 word-break:normal + overflow-wrap:break-word，不用 break-all。

## SVG 动画（本套用到的规则）
- 只用内联 `<svg>` + SMIL（`<animate>` / `<animateTransform>`），不用 CSS 动画、不用 JS。
- svg 内不准出现 id、class、href/xlink:href、`<defs>`、`<use>`、`<script>`。
- animate 只动白名单属性：opacity、stroke-dashoffset、x/y、d、points、fill 等；不对 width/height 做 `repeatCount="indefinite"` 的动画（微信从 2022-03 起会改写）。
- 无头截图只能看到第一帧，动画效果要在手机上实测。深色模式下微信不处理 SVG 颜色。

## 衬线
- 不写 font-family（微信规范不建议，手机上也没有对应字体会退回苹方/Roboto；vass 的 font-family 规则目前没启用，但 [spec] 仍按 0 处理）。
- 要衬线感只能用字重、细线、字距模拟，真衬线字只能做成图片。

## 用法
```
python3 master/styles/<本目录>/publish.py <out目录> <稿件.md> <素材目录>
```
layout-map.json 字段和 01 一样；写 `"style": "<编号-名称>"`、`"data_cjk": true`；换母版前删掉 card_fit。
- 文末签名卡固定用 01 那张，theme 不改。
- 组件样张见 `preview/components-1.png`、`preview/components-2.png`，整篇示例见 `preview/preview-N.png`（「游戏变内容」，已换正式配图）。

## 固定规则：代码窗 + 章节内小标题（2026-10-15 13:30 起）
Markdown 约定、代码窗做法和 [codebreak] 检查见 master/README.md 同名一节和 styles/INDEX.md。本套样张：preview/sample-code-390.png、preview/sample-subhead-390.png（组件样张），preview/sample-code-taptap-390.png、preview/sample-subhead-ch1-390.png（游戏变内容全文预览）。

## 段首加粗引子（2026-10-15g）
- 段落开头的 `**引子：**正文`（如游戏变内容第四章「小红书小工具：」「B站 Toy：」「TapTap 制造：」、第二章「B站」「小红书」）：6px 玫红实心小方块 + 玫红加粗（同本套小标题的 8px 方块，小一号）。还是正文段落，不是小标题；段中间的 `**加粗**` 仍是普通加粗。
- 数据高亮本来就带 white-space:nowrap；publish 的 `[nowrap]` 和 `[leadin]` 检查同 master。四套并排见 `../compare-leadin.png`。

> 注：本仓库没有附带 `compare-*.png`、`preview/` 样张和 `assets/` 头像（含作者署名、IP 和第三方截图）；运行 publish.py 会在输出目录生成自己的预览。
