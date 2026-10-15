# 04-timeline-ticket

主色：青 #0D9488，强调琥珀 #F59E0B。

## 组件（★ = 01 没有、其他两套也没有）
| 组件 | 说明 |
|---|---|
| ★ 时间线站点章节头 | 34px 青色圆 + 5px 外环（#CCFBF1）+ 「STOP 0N」琥珀标签 + 虚线连接 |
| ★ 票根开头区 | 2px 深色边框 + 5px 青色硬阴影的大票：青色头条「STOP 00 · 出发」+ 右侧「NO.月日」（没有日期写 ADMIT ONE）；正票是「<栏目名> · 导语」+ 16px 加粗导语；✂ 撕票虚线；浅青票根放全程路线（每个编号章节一个圆点，青/琥珀交替，站数自动数）和「全程 N 站 · 阅读约 N 分钟」。不放标题和副标题。参考 references/theme-moyu-ticket.md 组件 2 票据封面 ticket-cover（flex 换成 table） |
| 便签导语卡（备用） | 稿件没有 `# 标题` 行时才用：#FEF3C7 便签底、硬阴影、SVG 图钉 |
| ★ 票根金句卡 | 2px 深色边 + 5px 青色硬阴影 + 「ADMIT ONE · 划重点」票根 + 虚线撕口 |
| ★ 时间线重点卡 | 左侧竖线 + 圆点 + STEP 0N 标签 |
| ★ 胶囊数字 | 数字做成青底白字胶囊，white-space:nowrap 防止底色断成两截 |
| ★ 粗框对比卡 | 两栏 2px 深色粗框、右栏浅青底，中间只留间距（不放 VS） |
| ★ SMIL 跳动三点分隔 | 三个点 translate 上下跳，begin 错开 |
| 无编号小标题 | 4px 琥珀左竖条 |
| 代码窗（2026-10-15h 起统一） | 原「指令票」作废：四套统一用 master/build.py 的终端代码窗（原 02 的窗口外框 + 深色终端，无「复制」、无「左右滑动」），本套 theme.py 不再覆盖 code_card |
| 章节内小标题（途经点） | `###` 或整行 `**…**`：青色空心小圆环 + 16px 加粗（章节头是 34px 实心站点圆 + STOP） |
| 引用 | 上标序号青色粗体；引用表装在 2px 深色圆角框里（浅青硬阴影），表头浅青底 + 虚线，编号青色粗体，行间虚线 |
| 高亮 / 划线 | 浅青底 #CCFBF1 / 3px #FCD34D 下划线 |

## 调性
轻松、好玩、有手作感，像旅行手账。

## 适用
事件经过、发展历程、一年回顾、产品迭代史、活动/上手流程；轻松向的盘点。

## 不适用
事故、伦理、裁员等严肃负面新闻（票根、便签太俏皮）；金融估值类；截图特别密的长文（票根元素太多会显得花）。

## 参考来源（github.com/isjiamu/gzh-design-skill）
- references/theme-moyu-ticket.md：票根、硬阴影
- archive/themes-v1/theme-data-infographic.md（gallery-v1 datainfo.html）：数据胶囊、站点式时间线
- 自己的设计：票根开头区 + 全程路线、粗框对比卡、SMIL 跳动三点；素材截图直接放

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
- 段落开头的 `**引子：**正文`（如游戏变内容第四章「小红书小工具：」「B站 Toy：」「TapTap 制造：」、第二章「B站」「小红书」）：青色空心小圆环 + 青色加粗（同本套小标题的「途经点」圆环，小一号）。还是正文段落，不是小标题；段中间的 `**加粗**` 仍是普通加粗。
- 数据高亮本来就带 white-space:nowrap；publish 的 `[nowrap]` 和 `[leadin]` 检查同 master。四套并排见 `../compare-leadin.png`。

> 注：本仓库没有附带 `compare-*.png`、`preview/` 样张和 `assets/` 头像（含作者署名、IP 和第三方截图）；运行 publish.py 会在输出目录生成自己的预览。
