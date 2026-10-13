# 命名与格式约定 / Conventions

| 对象 | 规则 | 例子 |
|---|---|---|
| 角色目录 | `NN-role`，两位数字表示流转顺序，role 用小写英文+连字符 | `04-copywriter` |
| 项目 slug | `YYYY-MM-DD-kebab-slug`，全小写 | `2026-10-12-jev-valuation` |
| 项目文件夹 | `<role>/projects/<slug>/`，所有角色同名 | `05-visual/projects/2026-10-12-jev-valuation/` |
| 消息 id | `tc-NNN` / `dl-NNN` / `rj-NNN` | `rj-001` |
| 素材编号 | `M1, M2, …`，正文以 `[M1]` 引用 | `[M4]` |
| 图片 | 小写英文+连字符；封面写比例 | `cover-2.35.jpg` |

- 文本统一 UTF-8、Markdown；JSON 两空格缩进，`ensure_ascii=false`。
- 每个角色目录固定包含：`SKILL.md`（frontmatter: name, description）、`agent-card.json`、`spec.md`、`config/`、`projects/`。
- 中文标点用全角；英文原文引语、金额、链接保持半角。
- 公开内容不写句首圆点列表。
