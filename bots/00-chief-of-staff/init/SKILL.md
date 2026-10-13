---
name: gzh-init
description: 安装后初始化本工作流。首次使用仓库、或用户说「初始化」「设置写作风格」「设置 IP」时触发。Post-install setup of writing style, IP character and news sources.
---
# 初始化 · gzh-init

按 [docs/INIT.md](../../../docs/INIT.md) 的清单逐步执行，每步先问用户、允许跳过。

1. 写作风格：索取语料 → 放入 `reference/corpus/` → 按 `reference/README.md` 生成 `reference/writing-style.md`。跳过则使用默认风格 khazix-writer：https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer
2. 账号定位与 IP：把问题转给 05-visual（task-card），由它提问并输出 `bots/05-visual/config/ip/ip-spec.md`。跳过则中性默认、不用 IP。
3. 资讯信源：生成 `bots/01-news/config/news-sources.md`。
4. 汇总确认，所有问题合并成一条编号消息发给用户。
