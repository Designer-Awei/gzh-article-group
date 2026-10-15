# 02-window-terminal

主色：蓝 #2563EB，标题深色 #0F172A，高亮黄 #FDE68A（审核官建议）。

## 组件（★ = 01 没有、其他两套也没有）
| 组件 | 说明 |
|---|---|
| ★ 终端开头区 | 深色终端窗口：「~/column — zsh」标题栏 → 标签胶囊（蓝底「<栏目名>」+ 描边的阅读时长 / 共 N 节 / 日期，没有日期就省略）→ `❯ cat lead.md` → 16px 加粗浅色导语（深色底上的引用序号单独放大到 13px、亮青 #67E8F9）→ 底部「● ready」状态栏 + SMIL 闪烁光标。不放标题和副标题。参考 archive/themes-v1/theme-terminal.md 组件 2「开头引言卡片（终端窗口风格）」 |
| ★ Mac 窗口卡 | 红黄绿三圆点标题栏（#FF5F57 / #FEBC2E / #28C840），只用在正文组件：金句卡（「划重点」）、重点卡、对比卡、代码块。素材截图不再套窗口，直接放 |
| ★ 命令行章节头 | 「❯ cd part-0N ▮」+ 标题 + 36×3px 下划线（审核官建议的 3px 线） |
| ★ 终端代码块 | 深色终端窗：三色圆点 + bash 标题栏；命令亮蓝 #7DD3FC，包 `<code>`；命令在空格处折行（2026-10-15i 起 white-space:pre-wrap，只在空格/逗号后折，不在单词中间断开，不再横向滚动）。2026-10-15h 起去掉「复制」标签和「左右滑动」提示，并作为四套统一的代码窗搬进 master/build.py（本套 theme.py 不再覆盖） |
| 章节内小标题 | `###` 或整行 `**…**`：蓝色「./」路径前缀 + 16px 加粗（章节头是 ❯ cd part-01 + 19px） |
| ★ STEP 编号卡 | 重点卡每条前面一个 STEP n 徽标 |
| ★ SMIL 进度线分隔 | stroke-dashoffset 进度线 + 闪烁光标点（opacity） |
| 无编号小标题 | 前缀「#」 |
| 引用 | 上标序号浅蓝 #3B82F6；引用表表头浅灰蓝底 #F1F5F9，编号蓝色粗体，链接灰蓝 #64748B，横线分隔 |
| 高亮 / 划线 / 数字 | 黄底 #FDE68A / 2px 蓝下划线 / 蓝色 17px 粗体，white-space:nowrap 不拆行 |

## 调性
科技、工具感、明亮，像在看开发者文档。

## 适用
AI 工具/平台盘点、产品实测、教程、上手指南；截图多、有命令或代码的长文。

## 不适用
人物故事、情感/观点评论（窗口框太冷）；事故、伦理等负面新闻；几乎没有截图的纯文字稿（窗口卡会显得空）。

## 参考来源（github.com/isjiamu/gzh-design-skill）
- archive/themes-v1/theme-terminal.md（gallery-v1 rich_terminal.html / heikeji.html）：窗口三圆点、终端代码块、命令行提示符
- references/common-components.md 1a 深色代码块
- references/theme-moyu-green.md：黄色高亮 #FDE68A
- 自己的设计：终端开头区（标签胶囊 + cat lead.md 导语 + 状态栏）、cd part-0N 章节头、STEP 卡、SMIL 进度线

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
- 段落开头的 `**引子：**正文`（如游戏变内容第四章「小红书小工具：」「B站 Toy：」「TapTap 制造：」、第二章「B站」「小红书」）：蓝色「./」前缀 + 蓝色加粗（同本套小标题的「./」）。还是正文段落，不是小标题；段中间的 `**加粗**` 仍是普通加粗。
- 数据高亮本来就带 white-space:nowrap；publish 的 `[nowrap]` 和 `[leadin]` 检查同 master。四套并排见 `../compare-leadin.png`。

> 注：本仓库没有附带 `compare-*.png`、`preview/` 样张和 `assets/` 头像（含作者署名、IP 和第三方截图）；运行 publish.py 会在输出目录生成自己的预览。
