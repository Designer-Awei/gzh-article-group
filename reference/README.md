# reference/ · 作者语料库与写作风格

用户上传的原始语料放这里，用来学习作者的声音和观点。文案官（bots/04-copywriter）每次动笔前读 `reference/writing-style.md`。

```
reference/
├── corpus/
│   ├── articles/   过往文章（.md / .txt / .html / .pdf）
│   ├── links/      文章链接清单 links.md（每行一个 URL + 一句备注）
│   └── notes/      日记、长评论、口喷转写
├── writing-style.template.md   风格指南结构模板
└── writing-style.md            生成的风格指南（文案官读取；初始化时生成）
```

## 如何从语料生成 writing-style.md（给智能体）
1. 盘点 `corpus/` 全部文件；`links/` 中的链接逐个抓取正文，存为 `corpus/articles/<日期-标题>.md`（抓不到就标注，不编造）。
2. 按体裁给文章分原型（如：工具分享型、观点输出型、其他），统计各自的结构骨架（开头方式、小标题、结尾方式、篇幅）。
3. 提炼：写作者画像、观点内核（反复出现的立场，附出处）、语言 DNA（高频口语词、比喻习惯、句长节奏、标点习惯）、红线（AI 腔禁用词、不能编造的内容、隐私边界）、金句与签名句。
4. 严格按 `writing-style.template.md` 的章节输出 `reference/writing-style.md`；每条规则附 1 个语料原文短例句并注明文件名。只写能从语料证实的规律。
5. 文末写「语料版本」：参与学习的文件清单与日期。

## 持续迭代
语料可以随时追加。追加后重新执行上面的流程：对比旧版 writing-style.md，保留仍成立的规则、修订冲突项、补充新规律，并在文末记录变更。用户对稿件的修改意见也应回写到这里。

## 默认风格（跳过语料时）
用户在初始化时选择跳过，则 `writing-style.md` 只写一行指向默认风格，文案官改用卡兹克公开的写作 skill：[khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)。之后用户补充语料，再按上面流程生成个人风格。

## 隐私
`corpus/` 默认被 .gitignore 忽略（只保留 .gitkeep），不要把私人日记推到公开仓库。
