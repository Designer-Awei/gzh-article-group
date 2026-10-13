# AGENTS.md — 智能体总规范

本仓库是一套公众号文章多智能体工作流。`bots/NN-role/` 是角色定义（subagent），装载其 `SKILL.md` 即可工作；文章产出全部在 `projects/<slug>/`。

## 首次使用：初始化
仓库刚安装、`reference/writing-style.md` 不存在时，先由 00-chief-of-staff 执行 [bots/00-chief-of-staff/init/SKILL.md](bots/00-chief-of-staff/init/SKILL.md)，清单见 [docs/INIT.md](docs/INIT.md)：
1. 向用户要本人原始语料（博客、日记、长评论、链接、截图）→ `reference/corpus/`，以及喜欢的第三方风格样本（可选）→ `reference/prefer/`； → 按 [reference/README.md](reference/README.md) 生成 `reference/writing-style.md`。可跳过，跳过则默认用卡兹克的 [khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)。
2. 05-visual 询问账号定位，建议匹配的 IP 形象 → `bots/05-visual/config/ip/ip-spec.md`。可跳过，跳过则中性默认、不用 IP。

## 目录约定
| 路径 | 内容 |
|---|---|
| `bots/NN-role/` | SKILL.md、spec.md、agent-card.json、config/（只放定义，不放产出） |
| `projects/<slug>/` | 一篇文章；固定子目录见 [projects/README.md](projects/README.md) |
| `projects/_template/` | 新项目脚手架，`scripts/new-project.py` 使用 |
| `reference/` | `corpus/`（作者本人语料，观点来源）、`prefer/`（第三方风格样本，只借鉴形式）、生成的 `writing-style.md` |
| `protocol/` | A2A 消息 schema 与示例 |
| `scripts/` | 工具脚本 |
| `docs/` | INIT.md 与 showcase/ 展示图 |

## 流转顺序
01-news / 02-ideation → 用户拍板 → 00-chief-of-staff `scripts/new-project.py` 开项目并派 task-card → 03-research → 04-copywriter → 05-visual → 06-layout → 07-reviewer →（通过）00-chief-of-staff 交付 `layout/` 的 HTML + `cover/` 的封面；（不通过）rejection 打回负责角色，返工后重新验收。每条消息追加到 `projects/<slug>/handoff.json`。

## 谁能写哪里
| 角色 | 可写 |
|---|---|
| 00-chief-of-staff | `projects/<slug>/README.md`、`handoff.json`；运行 new-project.py；初始化时写 `reference/` |
| 01-news | `news/`（本地，不入库） |
| 02-ideation | `projects/<slug>/brief/` |
| 03-research | `projects/<slug>/source/` |
| 04-copywriter | `projects/<slug>/draft/`；按用户反馈更新 `reference/writing-style.md` |
| 05-visual | `projects/<slug>/illustration/`、`cover/`；`bots/05-visual/config/ip/` |
| 06-layout | `projects/<slug>/layout/` |
| 07-reviewer | `projects/<slug>/review/`；只验收与打回，不改别人的产出 |
| 所有角色 | 追加 `handoff.json` 的 `log`；不改 `protocol/` 与他人 `config/`，除非用户要求 |

分工归属：截图 → 03-research；文字 → 04-copywriter；配图与封面 → 05-visual；排版 → 06-layout。

## 收到链接或截图
任何角色收到用户发来的链接或截图：本人作品存入 `reference/corpus/`，用户说「这个风格不错」的第三方内容存入 `reference/prefer/`（links 写入对应 `links/links.md` 并记下用户原话），分不清就问；存好后通知 00-chief-of-staff 触发风格刷新（规则见 [reference/README.md](reference/README.md)）。prefer 只借鉴结构、节奏、钩子等形式，绝不复制他人观点或原句。所有角色都可写这两个文件夹。

## 公开内容红线
发布给读者的内容（排版 HTML、正文、封面）禁止出现：截图文件名、`source/shots/` 等内部路径、「初稿」「待补」「待查」「以截图为准」等内部标记、引用清单里的「来源」「截图」列、句首圆点、私密信息。需要用户判断的问题由 00-chief-of-staff 汇总成一条编号消息，不留在稿件里。

## 不做
不对外发布、不替用户发消息、不编造事实、链接、引语或截图。
