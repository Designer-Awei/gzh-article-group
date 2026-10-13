# 02 素材包片段（素材官）

> 节选自完整素材包。每条素材带编号（M1…）、原文链接、可信度；截图只在内部素材包里登记，公开文章里不出现截图文件名。

## 一、产品与技术
- Jev 基于 Transformer，但**不是 LLM**：它不输出文本，只输出概率，也就是官方所说的「校准过的决策」（calibrated decisions）。[TechCrunch](https://techcrunch.com/2026/10/09/the-maker-of-non-text-ai-model-jev-valued-at-7-5b-just-weeks-after-launch/)
- 输出直接是代码可用的带类型的值（typed value）。决策类型有三种：选择、打分、是/否。一次调用可以并行问多个问题，输出不会越出事先定义的 schema。训练方法官方称为 RLCD（Reinforcement Learning for Calibrated Decisions）。[T. Hempel](https://thorstenhempel.de/en/blog/jev-classifier/)
- 名字取自「杰文斯悖论」（Jevons paradox）。[superglue](https://superglue.ai/blog/jev-system-one-benchmark/)
- 价格：输入每百万 token 0.042 美元，输出免费。[FourWeekMBA](https://fourweekmba.com/ai-jev-maker-typesafe-raises-870m-at-a-7-5b-valuation/)
- a16z 称：成本约为前沿模型的 1/100～1/500；在分类任务上、准确率相当时，速度快 100 倍。[a16z](https://a16z.com/announcement/investing-in-typesafe-ai/)

## 二、正方（真创新／有价值）
- 传统分类器的类别是固定的，新增类别要重新训练；Jev 在调用时才指定类别，不用重新训练。它把基础模型的知识、校准过的概率和面向软件的接口结合在一起。[Hempel](https://thorstenhempel.de/en/blog/jev-classifier/)
- superglue 自测：输入量大、输出受限、请求量高的负载下，质量、延迟和成本三者组合有竞争力。另外它是 Vercel AI Gateway 上采用最快的模型；9 月 22 日曾因需求过高暂停新账号注册。[superglue](https://superglue.ai/blog/jev-system-one-benchmark/)
- 校准审计预印本：在全部 16 种标签措辞与决策规则组合下，Jev 都比「未用这些任务样本训练过」的开源 checkpoint 更准；AG News 上约 +5.72 个百分点。[预印本 PDF](https://lsmeng.github.io/pdf/preprint-jev-calibration-audit.pdf)
- 引用：Almeida 说 "We have been super good at human language for four years, but it's not useful for automation because computers speak a different language."（[TechCrunch](https://techcrunch.com/2026/10/09/the-maker-of-non-text-ai-model-jev-valued-at-7-5b-just-weeks-after-launch/)）

