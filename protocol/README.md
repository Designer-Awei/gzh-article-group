# A2A 消息约定 / A2A message conventions

> **可选。** 默认的单智能体模式不需要发送消息，只需按同样字段把每次交接追加到 `projects/<slug>/handoff.json` 的 `log`。多智能体模式才用 A2A 发送这些消息。参考实现使用宿主平台的智能体消息，并未部署 A2A 服务。
> **Optional.** Single-agent mode (the default) sends no messages; just append each handoff with these fields to `handoff.json` → `log`. Use A2A only in multi-agent mode. The reference implementation used the host platform's agent messaging, not a deployed A2A service.

角色之间只通过三种消息通信，作为 A2A `Message` 的 `DataPart` 载荷发送；每条消息同时追加到 `projects/<slug>/handoff.json` 的 `log`。
Roles talk only through three message types, sent as the `DataPart` of an A2A `Message`, and each is appended to `projects/<slug>/handoff.json` → `log`.

| type | 方向 direction | 用途 purpose | Schema | 示例 example |
|---|---|---|---|---|
| task-card | 大管家 → 角色 | 派活 / assign work | [task-card.schema.json](task-card.schema.json) | [example](examples/task-card.example.json) |
| delivery | 角色 → 下游 / 大管家 | 交付 / hand off output | [delivery.schema.json](delivery.schema.json) | [example](examples/delivery.example.json) |
| rejection | 审核官 → 负责角色 | 打回 / send back for rework | [rejection.schema.json](rejection.schema.json) | [example](examples/rejection.example.json) |

早报自动推送（01-news → 02-ideation）也是一条 delivery，见 [examples/news-digest.example.json](examples/news-digest.example.json)；它不属于某篇文章，`project` 用 `YYYY-MM-DD-news-digest`，不写 handoff.json。
The weekday digest push is also a delivery: [examples/news-digest.example.json](examples/news-digest.example.json).

`handoff.json` 格式见 [handoff.schema.json](handoff.schema.json)，示例见 [Jev 项目](../projects/2026-10-12-jev-valuation/handoff.json)。
状态 status：`pending → in_progress → delivered → accepted | rejected`，最后 `delivered_to_user`；跳过用 `skipped`。
