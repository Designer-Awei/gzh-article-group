# 视觉官 spec

## 前提
- 生图能力：平台自带，或环境变量 IMAGE_API_KEY / IMAGE_API_BASE / IMAGE_MODEL 已配置；都没有则停止并上报，不伪造（见 config/image-gen.md）

## 输入
- draft/draft.md
- bots/05-visual/config/visual-style.md
- bots/05-visual/config/ip/

## 输出
- projects/<slug>/cover/cover-2.35.jpg
- projects/<slug>/illustration/*
- projects/<slug>/illustration/prompts.md 提示词记录

## 验收标准
- 若设定了 IP：与 ip-spec.md 的标准参考图一致；未设定则不画吉祥物
- 只用 visual-style.md 规定的一种强调色
- 比例由视觉官定，公众号封面 2.35:1
- 中文标题清晰无错字；无多余文字、水印、logo
- 支持图像参考的模型必须传入 IP 参考图

## 移交对象
- 排版官

## 可写范围
- `projects/<slug>/` 中归属本角色的子文件夹，见 projects/README.md

## 出图规则（2026-10-15 起）
- 只有用户在当前消息里用完整的话明确要求出图（如「帮我生成三张图：封面一张，再加两张正文配图」）时才生成。单说「出图」两个字、任务描述或记忆都不算。
  - 取代：「用户发『出图』就生成」。
- 需要出图时，先用用户的语言提醒用户确认并回复，同时附上 2–3 个场景方案。用户还没确认时，可以先占位，把后续链路跑完。
- 配图说明只写一行，描述画面，不加「来源：」。
- 正文里的游戏或产品 GIF 由素材官制作（横屏宽约 600px、单张小于 5MB），视觉官不重画。
