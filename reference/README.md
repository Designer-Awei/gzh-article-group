# reference/ · 作者语料库、偏好样本与写作风格

文案官（bots/04-copywriter）每次动笔前读 `reference/writing-style.md`，它由下面两类素材生成。

```
reference/
├── corpus/                     作者本人的声音和观点（最高权重，观点的唯一来源）
│   ├── articles/   过往文章（.md / .txt / .html / .pdf）
│   ├── links/      作者自己文章的链接 links.md（每行 URL + 备注）
│   ├── notes/      日记、长评论、口喷转写
│   └── imgs/       作者自己的文字/帖子截图（智能体读图或 OCR 后当语料）
├── prefer/                     用户喜欢的第三方风格样本（只借鉴形式）
│   ├── links/      links.md（URL + 用户原话，如「这个风格不错」+ 日期）
│   ├── articles/   保存下来的第三方文章正文
│   └── imgs/       第三方内容截图
├── writing-style.template.md   风格指南结构模板
└── writing-style.md            生成的风格指南（文案官读取）
```

## corpus 与 prefer 的区别
| | corpus/ | prefer/ |
|---|---|---|
| 是谁写的 | 作者本人 | 第三方 |
| 学什么 | 观点、立场、语言 DNA、口头禅、红线、金句 | 结构、节奏、开头钩子、小标题、转场、版式感 |
| 权重 | 最高；与 prefer 冲突时以 corpus 为准 | 只作补充，不改变作者的声音 |
| 禁止 | — | 不得复制他人的观点、原句、人设、口头禅、梗 |

## 如何生成 / 刷新 writing-style.md（给智能体）
1. 盘点 `corpus/` 与 `prefer/` 全部文件。`links/` 中的链接逐个抓取正文，分别存为 `corpus/articles/` 或 `prefer/articles/` 下的 `<日期-标题>.md`；`imgs/` 中的截图读图或 OCR 成文字后再分析。抓不到、看不清就标注，不编造。
2. 只用 corpus：按体裁分原型，统计结构骨架；提炼写作者画像、观点内核（附出处）、语言 DNA、红线、金句与签名句。
3. 只用 prefer：提炼可借鉴的形式技巧，并写明每条来自哪个样本、明确不借鉴什么。
4. 按 `writing-style.template.md` 输出 `reference/writing-style.md`：第二至八节只来自 corpus，第九节「偏好风格借鉴」只来自 prefer。每条规则附 1 个短例句与文件名；prefer 的例句只用来说明形式，不进入成稿。
5. 文末写「语料版本」：参与学习的文件清单与日期。

权重：观点和语气 100% 来自 corpus；prefer 只在 corpus 没有覆盖的形式问题上生效。corpus 为空、只有 prefer 时，声音用默认风格 [khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)，形式参考 prefer。

## 持续迭代
两个文件夹都可以随时追加。追加后重新执行上面的流程：对比旧版，保留仍成立的规则、修订冲突项、补充新规律，并在文末记录变更。用户对稿件的修改意见也回写到这里。

## 收到链接或截图时（所有角色都适用）
用户在任何对话里发来链接或截图：
- 说是「我写的 / 我发的」→ 存入 `corpus/`（links 写入 `corpus/links/links.md`，截图存 `corpus/imgs/`）。
- 说「这个风格不错 / 我喜欢这种写法」→ 存入 `prefer/`（links 写入 `prefer/links/links.md` 并记下用户原话，截图存 `prefer/imgs/`）。
- 分不清时问用户一句。
存好后通知 00-chief-of-staff，由它安排 04-copywriter 刷新 `writing-style.md`。

## 默认风格（跳过语料时）
初始化时跳过，`writing-style.md` 只写一行指向默认风格：[khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)。之后补充语料再生成个人风格。

## 隐私与版权
`corpus/` 与 `prefer/` 的内容默认被 .gitignore 忽略（只保留 .gitkeep）。私人日记不要推到公开仓库；第三方样本只供本地学习，不要再发布。
