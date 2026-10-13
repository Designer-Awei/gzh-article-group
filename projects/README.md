# projects/ · 文章项目

一篇文章一个文件夹：`projects/<YYYY-MM-DD-slug>/`。用 `python3 scripts/new-project.py <slug>` 从 `_template/` 创建，结构固定：

```
projects/<slug>/
├── README.md        项目说明 + 交付清单（00-chief-of-staff）
├── handoff.json     A2A 流转日志（所有角色追加，见 protocol/handoff.schema.json）
├── brief/           选题总结 topic.md                     ← 02-ideation
├── source/          素材索引 materials.md + shots/ 截图    ← 03-research
├── draft/           稿件 draft.md                         ← 04-copywriter
├── illustration/    正文配图                              ← 05-visual
├── cover/           2.35:1 公众号封面                      ← 05-visual
├── layout/          排版 HTML + snippets/                 ← 06-layout
└── review/          验收报告 review-report.md              ← 07-reviewer
```

规则：每个角色只写自己负责的子文件夹；写完在 `handoff.json` 的 `log` 里追加一条消息记录（task-card / delivery / rejection）。`source/shots/` 和截图文件名只供内部使用，不进入公开稿件。

示例：[2026-10-12-jev-valuation](2026-10-12-jev-valuation/README.md)

---

One folder per article with the fixed layout above. Each role writes only its own subfolder and appends to `handoff.json`.
