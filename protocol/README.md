# A2A 消息约定 / A2A message conventions

角色之间只通过三种消息通信，作为 A2A `Message` 的 `DataPart` 载荷发送。
Roles talk only through three message types, sent as the `DataPart` payload of an A2A `Message`.

| type | 方向 direction | 用途 purpose | Schema | 示例 example |
|---|---|---|---|---|
| task-card | 大管家 → 角色 | 派活 / assign work | [task-card.schema.json](task-card.schema.json) | [example](examples/task-card.example.json) |
| delivery | 角色 → 下游 / 大管家 | 交付 / hand off output | [delivery.schema.json](delivery.schema.json) | [example](examples/delivery.example.json) |
| rejection | 审核官 → 负责角色 | 打回 / send back for rework | [rejection.schema.json](rejection.schema.json) | [example](examples/rejection.example.json) |

每个项目文件夹里的 `handoff.json` 是这次流转的落盘状态，格式见 [handoff.schema.json](handoff.schema.json)。
`handoff.json` in each project folder records the persisted handoff state; see [handoff.schema.json](handoff.schema.json).

状态 status：`pending → in_progress → delivered → accepted | rejected`，最后 `delivered_to_user`；跳过的环节用 `skipped`。
