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
