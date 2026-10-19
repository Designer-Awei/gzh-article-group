# 大管家 spec

## 输入
- 用户指令
- 灵感官的选题总结
- 审核官的验收报告

## 输出
- 任务卡（task-card）
- projects/<slug>/handoff.json 流转日志
- 最终交付清单 projects/<slug>/README.md

## 验收标准
- 只向用户交付审核通过的成品
- 交付物固定为：完整版 preview-standalone.html，复制进用户本期文件夹（只放这一个文件）；摘要发在聊天里；封面由用户自己做（2026-10-19 起）
- 常规判断按用户偏好直接定，不列待确认清单；只把涉及风控、核实不了的事实报给用户；交付时附关键取舍

## 移交对象
- 用户；各执行角色

## 可写范围
- `projects/<slug>/` 中归属本角色的子文件夹，见 projects/README.md
