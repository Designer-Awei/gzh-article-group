# 公众号排版母版 v2.1（2026-10-13）

v1 已备份在 v1/（build.py、README.md）。风格：白底 + 唯一强调色珊瑚色 #F26B5B，细黑线和不对称圆角带一点手绘感，克制，不用句首圆点列表。全部内联样式，不依赖外部 CSS/JS。

## 文件
- build.py：`python3 build.py 稿件.md out.html layout-map.json`
- **publish.py（一条命令出全套）**：`python3 06-layout/config/master/publish.py <文章输出目录> <稿件.md> [截图目录] [--no-sync]`
  依次：把截图目录里的图覆盖同步到 `<输出目录>/img/` → 按 `<输出目录>/layout-map.json` 生成 article.html、wechat-paste.html（引用 img/）、preview-standalone.html（base64 内嵌、420px 容器、无提示文字）→ 删旧图并重出 preview.png + preview-N.png → 打印泄漏检查（文件名/shots//初稿/以截图为准）、【待补】【待查】计数、规范计数（font-family/渐变/非标准 text-align/flex）
- render.sh：`./render.sh <目录>`，渲染 wechat-paste.html（390px@2x，用公众号默认字体栈模拟），删旧图后切成每段 2400px 的分段图
- assets/octo-sign.png：签名栏用的灰章鱼头像（从 05-visual/config/ip/octo-anchor-v1.jpg 裁出）
- demo/：组件效果测试（用 Jev 稿件）

## 组件和 layout-map.json 字段（所有组件只改样式，不改文字）
| 组件 | 字段 | 说明 |
|---|---|---|
| 开头导语卡片 | `lead: N` | 第一条 --- 之后的 N 段放进黑线卡片，带珊瑚色错位投影 |
| 章节序号大字 | 自动 | `## 一、标题` 渲染成珊瑚色 Georgia 体「01 —」+ 标题；没有序号的小标题渲染成珊瑚色下划线 |
| 重点句底纹 | `highlight: [原句]` | 浅珊瑚色底 #FDE9E6 |
| 马克笔下划线 | `marker: [原句]` | 加粗 + 浅珊瑚 rgba 纯色底 + 2px 珊瑚色下边线（不用渐变） |
| 数据高亮 | `data: [[段落开头, "75 亿美元"]]` | 只在指定段落把第一处出现的数字放大到 17px、加粗、珊瑚色 |
| 金句卡片 | `quote_card: [段落开头]` | 把整段渲染成居中的大字卡片 |
| 要点卡片 | `points_card: {段落开头: {n: 行数}}` | 连续 n 行渲染成带珊瑚色数字圆标的卡片（table 实现） |
| 对比卡片 | `compare_after: {段落开头: {left, right}}` | 左灰右珊瑚两栏，中间是 vs；条目要摘原文（table 实现） |
| 引用块 | `>` | 灰底，左边一条珊瑚色线 |
| 章节分隔 | `---` | 灰-珊瑚-灰三个小圆点 |
| 文末卡片 | `signature: {avatar, name, main, sub}` | 代码排版（table 两栏，没用 flex/整张图）：左边章鱼小图约占 24%，右边「Awei」加珊瑚色小点、主句带 3px 珊瑚色下划线、灰色副句；浅灰虚线圆角框，宽度 100% 自适应（参考 assets/end-card.png）；设为 false 可关闭 |
| 截图/插画 | `shots` / `hero` / `insert_after` | 同 v1 |

## 规范
正文 15px，行距 1.8，左对齐，两侧留白 22px。高亮每节 1-2 句（底纹和马克笔合计），数据高亮全文控制在 8 处以内，金句卡片全文最多 2-3 张。【待补】【待查】用黄底提示，发布前必须清掉。
公开内容（正文、图注、引用清单）里不出现截图文件名、shots/ 路径，也不出现「初稿」「以截图为准」等内部标记；截图图注统一写「截图来源：媒体名，日期（域名）」；引用清单只放「编号 | 链接」两列，编号列不换行。

## v2.1 从 gzh-design-skill 吸收的内容（github.com/isjiamu/gzh-design-skill）
1. 所有文字节点用 `<span leaf="">` 包裹，`<img>` 也包在 leaf 里（防止粘贴后样式丢失）。
2. 平台红线：不用 `<style>`/`<script>`/`<div>`/class/id/position/float/@media/grid/CSS 变量/外部字体。正文片段从全局 `<section>` 开始。
3. 图片写 `max-width:100%;height:auto;display:block;margin:0 auto`，不用 `width:100%` 拉伸小图。
4. 文字和卡片背景只用纯色或 rgba 纯色，不用渐变（马克笔高亮从渐变改成纯色底加下划线）。
5. 视觉层级三层递进：锚点（数据高亮/金句卡，全文不超过约 5–8 处）→ 标记（每节 1–2 句高亮）→ 容器（引用块/要点卡）。
6. 章节自动编号 01/02/…（沿用原有的珊瑚色大号序号）。
7. 交付前跑校验脚本：`python3 /tmp/gzh/scripts/validate_gzh_html.py <html>`，ERROR 清零。
8. 有意没有吸收的：半角标点自动转全角（会改原文，违反不改文字的规则，只报告）；全局「每段 1–3 个下划线」（和本母版每节 1–2 句的规则冲突）；虚线框只保留在文末卡片上，因为它是用户参考图里的样式。
珊瑚色章鱼的视觉（白底、#F26B5B、黑细线、不对称圆角、章鱼签名）不变。

## 微信「内容结构检测」排查（developers.weixin.qq.com/doc/service/guide/product/plugin_spec.html）
| 规则 | 母版处理 |
|---|---|
| 1.1 opacity 隐藏图 | 不用 opacity |
| 1.2 caret-color | 不用 |
| 1.3 line-height 小于字号 | 去掉金句引号的 line-height:0.6；所有多行文字的行高 ≥1 |
| 1.4 固定宽度/溢出 | 容器全部是百分比或自适应；图片 max-width:100% 并带 data-w；表格 width:100%；只保留 22px 圆标、7px 小点这类固定尺寸的行内装饰（官方检测通过） |
| 1.5 height:0/溢出 | 只有一个 20px 的空白段（不含文字） |
| 1.6 text-align start/end | 只用 left/center，并且已去掉 justify |
| 1.8 pre | 不用 |
| 2.1 嵌套超过 10 层 | 最深约 5 层 |
| 2.2/2.3 leaf 规范 | leaf 里只放文字或 img |
| 3 字体 | 删除全部 font-family（含 Georgia），使用公众号默认字体栈 |
| 4.1.2 文字渐变背景 | 0 处渐变 |
| 4.5.2 !important | 不用 |
官方检测工具 github.com/wechatjs/verify-article-structure-spec（在 /tmp/vass/cli 运行：`PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome npm run check <html>`）对 article.html、wechat-paste.html、preview-standalone.html 的结果都是 isValid: true。

## 母版库（styles/）
- 01-珊瑚章鱼-v2：用户认可的第一套母版（2026-10-12，Jev 文章）。重点句高亮、金句卡、对比卡、章鱼签名栏；引用清单只放编号+链接，编号列不换行；公开输出不出现截图文件名等内部标记。
后续新母版按 02-、03- 编号沉淀，排文章前按选题挑一套。
