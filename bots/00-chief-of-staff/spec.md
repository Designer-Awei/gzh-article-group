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
- 交付物固定为：排版 HTML + 2.35:1 封面
- 需要用户判断的问题合并成一条编号消息

## 移交对象
- 用户；各执行角色

## 可写范围
- `projects/<slug>/` 中归属本角色的子文件夹，见 projects/README.md
