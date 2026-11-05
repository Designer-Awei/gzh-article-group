# Hermes / 非 Grok Bot 环境重建指南

本仓库的实际运行环境基于 Grok Bot 的原生能力（生图、X 搜索）。如果你在 Hermes、Codex、Claude Code、Cursor 或其他非 Grok Bot 环境下重建此工作流，需要注意以下几点。

## 核心架构：单智能体 + Subagent

推荐使用**单智能体**扮演所有角色，按流程依次切换，交接通过 `projects/<slug>/` 目录下的文件和 `handoff.json` 完成。

如果宿主平台支持子智能体（如 Codex Task、Cursor Agent），可以为每个角色创建独立子智能体，但主控仍然是单一编排者（00-chief-of-staff）。

## 关键能力外部化

### 1. 图片生成

**问题**：视觉官（05-visual）需要生图能力，用于正文配图。

**解决方案**：

- **优先方案**：使用宿主平台原生生图能力
  - Codex / Claude Code：如果订阅包含生图，直接调用原生工具
  - Cursor：配置环境变量 `IMAGE_API_KEY` / `IMAGE_API_BASE` / `IMAGE_MODEL`
  - Hermes / OpenClaw：检查是否支持 MCP 图片生成工具或原生生图

- **备选方案**：外接生图 API
  - OpenAI DALL-E 3：`IMAGE_API_BASE=https://api.openai.com/v1` + `IMAGE_MODEL=dall-e-3`
  - Replicate / Stability AI：配置对应 API endpoint 和 key
  - 见 [bots/05-visual/config/image-gen.md](../bots/05-visual/config/image-gen.md) 完整配置说明

- **底线规则**：**无生图能力时，视觉官必须停下，禁止伪造图片或假装已生成**

### 2. X（Twitter）素材检索

**问题**：素材官（03-research）需要从 X 上搜索案例、截图、引用。

**解决方案**：

- **优先方案**：使用宿主平台原生 X 检索
  - Codex / Claude Code：如果订阅包含 X 集成，直接调用
  - 检查是否有 MCP 工具支持 X API

- **备选方案**：外接 X API
  - X API v2（需要 Bearer Token）：配置环境变量或在素材官启动时声明
  - 第三方 X 搜索服务（如 nitter 实例、searchtweet.io）

- **手动方案**：用户手贴链接
  - 如果无法自动检索，素材官在 `source/materials.md` 中列出「待核实 X 链接」
  - 用户手动搜索后贴入链接，素材官再做截图和引用

- **底线规则**：**不得假装已核实 X 内容、不得编造 X 用户账号或帖子链接**

### 3. 封面设计

**问题**：封面始终由用户自制，工作流不产出封面。

**解决方案**：

- 视觉官只产出正文配图（16:9），不产出封面（2.35:1）
- 排版官交付的 HTML 不嵌入封面
- 大管家交付时明确告知用户：「封面请自制，推荐比例 2.35:1」

## 文件路径约定

所有产出优先落入 `projects/<slug>/` 对应子目录：

```
projects/<slug>/
  brief/research-brief.md     # 主编研究简报
  source/materials.md         # 素材官素材包
  source/shots/               # 截图
  draft/                      # 文案官初稿与润色稿
  illustration/               # 视觉官配图
  layout/preview-standalone.html  # 排版官交付物
  review/editor-redteam.md    # 主编反向审稿
  handoff.json                # 流水线日志
```

过渡期允许 `materials/`、`drafts/`、`visual/out/`、`layout/out/` 并存，但新期优先全部落入 `projects/`。

## 工作流程（完整版）

```
资讯官（01-news）
  ↓ 每工作日 11:00 发早报
灵感官（02-ideation）
  ↓ 预备 2–3 个角度，等用户来聊
【用户拍板】
  ↓
主编（08-editor）
  ├─ 选题评分卡（topic-scorecard.md）
  └─ 研究简报（research-brief.md）
【用户确认简报】
  ↓
素材官（03-research）
  └─ 素材包（materials.md + shots/）
【需要 X 检索或手贴链接】
  ↓
文案官（04-copywriter）
  └─ 初稿（draft/）
【用户审稿或 AI 改写】
  ↓
视觉官（05-visual）
  └─ 正文配图（illustration/）
【需要生图能力】
  ↓
排版官（06-layout）
  └─ HTML（layout/preview-standalone.html）
  ↓
审核官（07-reviewer）
  └─ 验收报告（review/）
【不通过打回相关角色】
  ↓
主编（08-editor）
  └─ 反向审稿（editor-redteam.md）
【找最弱三论点，必要时打回】
  ↓
大管家（00-chief-of-staff）
  └─ 交付 HTML + 摘要
【封面用户自制】
  ↓
排期官（09-calendar）
  └─ 更新排期表（已发布）
```

## 关键差异：Grok Bot vs Hermes

| 能力 | Grok Bot（实际运行） | Hermes / 其他环境 |
|------|---------------------|-------------------|
| 生图 | 原生生图工具 | 需配置外部 API 或使用宿主原生能力 |
| X 检索 | 原生 X 集成 | 需配置 X API 或手贴链接 |
| 封面 | 用户自制（一致） | 用户自制（一致） |
| 角色通信 | 宿主平台 bot 消息 | 单智能体切换或 subagent |
| 交接记录 | handoff.json | handoff.json（一致） |

## 安装后第一步

1. **检测生图能力**：
   ```bash
   # 检查环境变量
   echo $IMAGE_API_KEY
   echo $IMAGE_API_BASE
   echo $IMAGE_MODEL
   ```
   如果全空且宿主无原生生图，按 [bots/05-visual/config/image-gen.md](../bots/05-visual/config/image-gen.md) 配置。

2. **检测 X 检索能力**：
   - 询问宿主是否支持 X API 或 MCP X 工具
   - 如果都没有，确认「手贴链接」模式：素材官列出待核实链接，用户手动搜索后贴入

3. **初始化**：
   ```bash
   # 运行 gzh-init
   # 上传本人语料 → reference/corpus/
   # 生成 reference/writing-style.md
   # 设计 IP 形象 → bots/05-visual/config/ip/ip-spec.md
   ```

4. **试运行**：
   ```bash
   # 开一个测试项目
   python3 scripts/new-project.py 2026-11-05-test-topic
   # 按流程走一遍，确认各角色能读取配置
   ```

## 常见问题

### Q: Hermes 如何加载角色？
A: Hermes 支持 Agent Skills。把每个 `bots/NN-role/` 复制或软链到 Hermes skills 目录，命名 `gzh-<role>`（如 `gzh-editor`）。运行时工作目录保持在仓库根。

### Q: 无法生图怎么办？
A: 优先配置外部 API。如果实在无法生图，视觉官停下并告知用户「无生图能力，无法产出配图」，不继续流程。

### Q: X 检索失败怎么办？
A: 素材官在 `source/materials.md` 列出「待核实 X 链接」清单，用户手动搜索后贴入，素材官再做截图和引用。

### Q: 封面谁做？
A: **始终由用户自制**，工作流不产出封面。视觉官只做正文配图，排版官交付的 HTML 不嵌入封面。

### Q: 如何在 Cursor 中使用？
A: 在 `.cursor/rules/` 新建规则引用 `AGENTS.md`，角色按需用 `@bots/NN-role/SKILL.md` 引入。Cursor 不支持直接装 skills，需要手动加载。

### Q: 能否多智能体并行？
A: 可以，但推荐单智能体依次扮演。如果宿主支持 subagent（如 Codex Task），可以创建子智能体，但主控仍是 00-chief-of-staff。

## 配置检查清单

- [ ] 生图能力已配置（环境变量或原生工具）
- [ ] X 检索能力已配置（X API 或手贴模式）
- [ ] `reference/writing-style.md` 已生成或使用默认
- [ ] `bots/05-visual/config/ip/ip-spec.md` 已设计或跳过
- [ ] `projects/_template/` 脚手架已确认
- [ ] 试运行一个测试项目成功

## 技术细节

### 环境变量（可选）

```bash
# 生图 API
export IMAGE_API_KEY="sk-..."
export IMAGE_API_BASE="https://api.openai.com/v1"
export IMAGE_MODEL="dall-e-3"

# X API（可选）
export X_BEARER_TOKEN="..."
```

### 路径约定

- 仓库根：`/path/to/gzh-article-group/`
- 项目路径：`projects/<slug>/`
- 配置路径：`bots/NN-role/config/`
- 脚本路径：`scripts/`

### Subagent 示例（Codex Task）

```yaml
# 示例：创建主编 subagent
task:
  name: gzh-editor
  skill: bots/08-editor/SKILL.md
  context:
    - projects/<slug>/brief/topic.md
    - bots/08-editor/config/editor-protocol.md
  output: projects/<slug>/brief/research-brief.md
```

## 总结

Hermes 或其他环境下重建工作流的核心是：

1. **单智能体 + Subagent** 架构替代多 bot 通信
2. **外部 API 或宿主原生能力** 替代 Grok Bot 原生生图和 X 检索
3. **projects/<slug>/ 目录交接** 替代消息传递
4. **封面始终用户自制**，工作流不产出

遵循这三点，任何支持文件读写的智能体宿主都能完整复现此工作流。
