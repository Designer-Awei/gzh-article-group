# 安装后初始化 / Post-install initialization

由 00-chief-of-staff 执行（见 bots/00-chief-of-staff/init/SKILL.md）。每一步都可以跳过，跳过时使用中性默认值。

## 初始化清单
- [ ] **第 0 步 · 生图能力**
  - 检查平台是否自带生图，或 `IMAGE_API_KEY` / `IMAGE_API_BASE` / `IMAGE_MODEL` 是否已配置。
  - 都没有 → 提示用户开启或配置（可选服务见 [bots/05-visual/config/image-gen.md](../bots/05-visual/config/image-gen.md)）；可先跳过，视觉官出图前会再次检查，没有能力就停下，不伪造。
- [ ] **第 1 步 · 写作风格**（文案官依赖）
  - 向用户索取原始语料：过往博客/公众号文章、日记、长评论、口喷转写、文章链接。
  - 文件放入 `reference/corpus/articles|notes/`，自己的帖子截图放 `reference/corpus/imgs/`，链接写入 `reference/corpus/links/links.md`。
  - 再问一句：有没有喜欢的别人的文章或账号？有就放入 `reference/prefer/`（只借鉴形式，不借观点）。
  - 按 `reference/README.md` 生成 `reference/writing-style.md`，给用户看摘要确认。
  - 用户跳过 → `reference/writing-style.md` 写明使用默认风格 [khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)（卡兹克公开写作 skill），并提示以后可补语料。
- [ ] **第 2 步 · 账号定位与 IP**（由 05-visual 发问）
  - 问：账号写什么领域、给谁看、希望读者记住的一个词、喜欢/讨厌的视觉风格。
  - 建议一个与定位匹配的 IP 形象，出 2–3 个草图方案让用户挑；定稿后写 `bots/05-visual/config/ip/ip-spec.md`（模板见同目录 ip-spec.template.md）和标准参考图，并更新 `visual-style.md`。
  - 用户跳过 → 不用 IP 角色，使用中性默认：白底、黑色线条、单一强调色，配图以图表/示意为主；从 ip-spec.template.md 生成 ip-spec.md 并写明「未设定 IP」。
- [ ] **第 3 步 · 资讯信源**：复制 `bots/01-news/config/news-sources.example.md` 为 `news-sources.md` 填入用户信源；跳过则保留示例并提示。
- [ ] **第 4 步 · 确认**：汇总以上结果给用户，并在 `reference/writing-style.md` 与 `ip-spec.md` 末尾记下初始化日期。

---

English summary: step 0 check image-generation capability (built-in, or IMAGE_API_KEY / IMAGE_API_BASE / IMAGE_MODEL); step 1 collect the user's own corpus (text, links, screenshots) into `reference/corpus/` plus optional liked third-party samples into `reference/prefer/` (form only) and build `reference/writing-style.md` (skip → default [khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)); step 2 the visual role asks about account positioning and proposes a matching IP character (skip → neutral, no mascot); step 3 news sources; step 4 confirm.
