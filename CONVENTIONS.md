# 命名与格式约定 / Conventions

| 对象 | 规则 | 例子 |
|---|---|---|
| 角色目录 | `bots/NN-role`，两位数字表示流转顺序，role 小写英文+连字符 | `bots/04-copywriter` |
| 项目 slug | `YYYY-MM-DD-kebab-slug`，全小写 | `2026-10-12-jev-valuation` |
| 项目文件夹 | `projects/<slug>/`，子目录固定：brief/ source/ draft/ illustration/ cover/ layout/ review/ | `projects/2026-10-12-jev-valuation/cover/` |
| 流转日志 | `projects/<slug>/handoff.json` 的 `log` 追加，不改历史 | — |
| 消息 id | `tc-NNN` / `dl-NNN` / `rj-NNN`，项目内递增 | `rj-002` |
| 素材编号 | `M1, M2, …`，正文以 `[M1]` 引用 | `[M4]` |
| 图片 | 小写英文+连字符；封面写比例 | `cover-2.35.jpg` |
| 路径 | 文档与消息里一律写仓库相对路径 | `bots/05-visual/config/visual-style.md` |

- 文本统一 UTF-8、Markdown；JSON 两空格缩进，`ensure_ascii=false`。
- 每个角色目录固定包含：`SKILL.md`（frontmatter: name, description）、`agent-card.json`、`spec.md`、`config/`。
- 中文标点用全角；英文原文引语、金额、链接保持半角。
- 公开内容不写句首圆点列表。

- 交接：默认单智能体模式下通过文件交接，`handoff.json` 的 `log` 条目字段与 protocol/ 的消息一致；A2A 仅在多智能体模式下使用（可选）。
