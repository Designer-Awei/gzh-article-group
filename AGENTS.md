# AGENTS.md — 智能体总规范

本仓库是一套公众号文章多智能体工作流。每个顶层 `NN-role/` 目录是一个角色（subagent），装载其 `SKILL.md` 即可工作。

## 目录约定
- `NN-role/SKILL.md`：角色技能，装载入口。
- `NN-role/spec.md`：输入、输出、验收标准、移交对象。
- `NN-role/agent-card.json`：A2A Agent Card。
- `NN-role/config/`：角色参考配置（只读，除非用户要求修改）。
- `NN-role/projects/<slug>/`：该角色对某篇文章的产出 + `handoff.json`。
- `protocol/`：A2A 消息 schema 与示例；`templates/project/`：项目脚手架；`scripts/new-project.py`：开新项目。

## 流转顺序
`01-news` / `02-ideation` → 用户拍板 → `00-chief-of-staff` 派 task-card → `03-research` → `04-copywriter` → `05-visual` → `06-layout` → `07-reviewer` →（通过）`00-chief-of-staff` 交付 HTML + 封面 /（不通过）rejection 打回负责角色，返工后重新验收。

## 写权限
| 角色 | 可写 |
|---|---|
| 每个角色 | 只写自己的 `NN-role/projects/<slug>/` |
| 00-chief-of-staff | 另可运行 `scripts/new-project.py` |
| 07-reviewer | 只写验收报告和 rejection，不改别人的产出 |
| 任何角色 | 不改 `config/`、`protocol/`，除非用户明确要求 |

## 分工归属
截图 → 03-research；文字 → 04-copywriter；配图 → 05-visual；排版 → 06-layout。

## 公开内容红线
发布给读者的内容（排版 HTML、正文、封面）禁止出现：截图文件名、`shots/` 等内部路径、「初稿」「待补」「待查」「以截图为准」等内部标记、引用清单里的「来源」「截图」列、句首圆点。需要用户判断的问题由 00-chief-of-staff 汇总成一条编号消息，不留在稿件里。

## 不做
不对外发布、不替用户发消息、不编造事实、链接、引语或截图。
