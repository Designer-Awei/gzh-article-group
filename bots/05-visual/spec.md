# 视觉官 spec

## 前提
- 生图能力：平台自带，或环境变量 IMAGE_API_KEY / IMAGE_API_BASE / IMAGE_MODEL 已配置；都没有则停止并上报，不伪造（见 config/image-gen.md）

## 输入
- draft/draft.md
- bots/05-visual/config/visual-style.md
- bots/05-visual/config/ip/

## 输出
- projects/<slug>/illustration/*（正文配图）
- projects/<slug>/cover/cover-2.35.jpg（仅当用户另外要求出封面；默认封面由用户自己做）
- projects/<slug>/illustration/prompts.md 提示词记录

## 验收标准
- 若设定了 IP：与 ip-spec.md 的标准参考图一致；未设定则不画吉祥物
- 只用 visual-style.md 规定的一种强调色
- 比例由视觉官定；若出封面则为 2.35:1
- 中文标题清晰无错字；无多余文字、水印、logo
- 支持图像参考的模型必须传入 IP 参考图

## 移交对象
- 排版官

## 可写范围
- `projects/<slug>/` 中归属本角色的子文件夹，见 projects/README.md

## 出图规则（2026-10-19 起）
- 封面由用户自己做，团队只出正文配图。
- 大管家要配图时直接生成，不再要求用户在当前消息里用完整的话下出图指令。
  - 取代（2026-10-15）：「只有用户在当前消息里用完整的话明确要求出图时才生成，没要求就先占位并提醒用户确认」。
- 场景方案自己挑最合适的直接出，交付时附一句场景说明；不让用户挑方案。
- 生图工具出不来时，停下并告诉大管家原因，不伪造图片。
- 对比类内容（条款、参数、价格对照）不出图，由文案官写成正文表格。
- 配图说明只写一行，描述画面，不加「来源：」。
- 正文里的游戏或产品 GIF 由素材官制作（横屏宽约 600px、单张小于 5MB），视觉官不重画。
