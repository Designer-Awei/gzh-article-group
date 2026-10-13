---
name: gzh-init
description: 安装后初始化本工作流。首次使用仓库、或用户说「初始化」「设置写作风格」「设置 IP」时触发。Post-install setup of writing style, IP character and news sources.
---
# 初始化 · gzh-init

按 [docs/INIT.md](../../../docs/INIT.md) 的清单逐步执行，每步先问用户、允许跳过。

0. 生图能力检查：确认平台是否自带生图，或环境变量 `IMAGE_API_KEY` / `IMAGE_API_BASE` / `IMAGE_MODEL` 是否已配置。都没有就告诉用户：视觉官需要生图能力，请开启平台生图或配置一个生图 API（见 bots/05-visual/config/image-gen.md）；用户可以先跳过，之后视觉官会在出图前停下提醒。
1. 写作风格：索取作者本人语料（文章、日记、长评论、链接、截图）→ `reference/corpus/`；再问是否有喜欢的第三方风格样本 → `reference/prefer/`（只借鉴形式） → 按 `reference/README.md` 生成 `reference/writing-style.md`。跳过则使用默认风格 khazix-writer：https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer
2. 账号定位与 IP：把问题转给 05-visual（task-card），由它提问并输出 `bots/05-visual/config/ip/ip-spec.md`。跳过则中性默认、不用 IP。
3. 资讯信源：生成 `bots/01-news/config/news-sources.md`。
4. 汇总确认，所有问题合并成一条编号消息发给用户。


## 平时
任何角色转来「已存入 corpus/ 或 prefer/」的通知时，派 task-card 给 04-copywriter 刷新 `reference/writing-style.md`。
