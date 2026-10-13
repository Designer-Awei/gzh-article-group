# 资讯信源配置（示例）

> 把下面的占位换成你自己的信源。资讯官每个工作日按此抓取并输出早报。

## 信源列表
| 名称 | 类型 | 地址 | 语言 | 抓取方式 |
|---|---|---|---|---|
| 示例中文聚合站 | RSS | `https://example.com/feed.xml` | 中文 | HTTP GET 解析 XML |
| 示例海外科技媒体 AI 栏目 | 网页 | `https://example.com/ai` | 英文 | 抓标题+摘要 |
| 示例创投媒体 AI 栏目 | 网页 | `https://example.org/category/ai/` | 英文 | 抓标题+摘要 |
| 示例技术社区搜索 API | JSON API | `https://example.net/api/search?query=AI` | 英文 | 按热度过滤近 24h |

## 输出格式
文件：`news/YYYY-MM-DD.md`，精选 5–8 条，每条：
1. **标题**：发生了什么（一句话，结论先行）
2. 出处：`[来源名](URL)`
3. 为什么值得关注：1–2 句
4. 可能的切入角度：一句
