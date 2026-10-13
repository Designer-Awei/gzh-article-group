# 生图配置与流程 · image-gen

## 前提（二选一，缺一不可）
1. **智能体自带生图能力**：你运行的平台提供内置的图片生成工具。
2. **用户自行配置生图 API**：常见可选服务（仅举例，具体接口、模型名和参数以各家官方文档为准）：
   - OpenAI 的 gpt-image 系列
   - Google 的 Imagen / Gemini 图像模型
   - Flux（如通过 Replicate 等托管平台）
   - Midjourney（需第三方代理服务）
   - 即梦（Jimeng）、豆包 Seedream 等国内服务

   配置写在环境变量里，不要写进仓库：

   | 变量 | 含义 |
   |---|---|
   | `IMAGE_API_KEY` | 服务的 API 密钥 |
   | `IMAGE_API_BASE` | 接口地址（按服务文档填写） |
   | `IMAGE_MODEL` | 模型名 |

**两者都没有时：停下，不要伪造图片**（不用占位图、不从网上找图冒充、不写“已生成”）。通知 00-chief-of-staff，由它告诉用户需要开启平台生图或配置上面的环境变量。

## 流程
1. 读 `visual-style.md` 和 `ip/ip-spec.md`（如存在），读定稿 `projects/<slug>/draft/draft.md`。
2. 写提示词：画面描述用英文；画面里要出现的中文标题单独给出原文，并要求手写体、字少而清晰。每次给 2–3 个场景方案。
3. 角色一致性：设定了 IP 时，**只要模型支持图像参考 / 图像编辑，就必须把 ip-spec.md 指定的标准参考图传进去**；不支持时在提示词里完整描述形象，并在自检时重点比对。
4. 封面：用模型支持的最宽比例生成（如 16:9），主体放在竖向中间带，再裁成 2.35:1（如 2350×1000）。保存到 `projects/<slug>/cover/cover-2.35.jpg`。
5. 正文配图：比例由视觉官按内容选择（16:9、4:3、1:1、竖版），保存到 `projects/<slug>/illustration/`。
6. 自检：角色与参考图一致；中文标题清晰可读、无错字；没有多余文字、水印、logo；只用规定的一种强调色；裁切后主体完整。不合格就重生成。
7. 记录：把每张图的提示词、模型、比例、是否用了参考图写入 `projects/<slug>/illustration/prompts.md`（封面也记在这里），然后交付排版官。

## 风格参考
默认手绘画风的灵感来自 [Jacky-illustration](https://github.com/Jackywxsz/Jacky-illustration) 与 [visual-ip-illustrations](https://github.com/yangchuansheng/visual-ip-illustrations)。只借鉴画法和流程思路，不使用其中的角色形象。
