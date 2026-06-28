# 网采契约 — Web Collector Contract

> Pipeline S1 网采通道（通道 A）的采集规范。定义如何从网络采集专家材料（论文、访谈、博客），
> 并按 `schema/source.md` 标准打标存入 `sources/src-*.md`。

---

## 一、定位与职责

| 维度 | 说明 |
|------|------|
| **目的** | 从网络采集专家全网材料（论文著作、长访谈、博客文章），为 S2 双轨提取提供原始语料 |
| **时机** | Pipeline S1 采集阶段，与用户材料通道（通道 B）并行 |
| **产物** | `sources/src-*.md`（每源一个文件，按 §4.6 打标） |
| **关键约束** | provenance 可追溯（`url` + `collected_at`）｜反爬 fallback 不阻塞整体流程 |

---

## 二、MVP 3 路采集（最小闭环）

### 路径 ①：论文著作（Paper/Book）

**目标**：采集专家发表的学术论文、著作、技术报告。

**采集流程**：

```
WebSearch（scholar/arxiv 关键词）
  → 搜索策略："<专家名> + arxiv", "<专家名> + scholar", "<代表作关键词> + paper"
  → 过滤条件：年份（近 5-10 年）、引用数（>50 或领域前 20%）、venue 顶级（NeurIPS/ICML/CVPR/ICLR）
  → 找到论文 URL（arxiv 页面 / PDF 直链 / 作者主页）
    ↓
WebReader/mcp__web_reader（抓全文）
  → 优先顺序：ar5iv HTML（公式最准）> arxiv PDF > 作者主页 PDF
  → 转换：保留 LaTeX 公式、图片说明、参考文献结构
    ↓
存 sources/src-<slug>.md
  → 打标：type=paper, value=knowledge, channel=web, url=..., collected_at=...
```

**搜索关键词模板**：
- `"Yann LeCun" arxiv`
- `"Yann LeCun" convolutional networks`
- `"Yann LeCun" JEPA`
- `"Yann LeCun" energy-based model`

**打标示例**：

```yaml
---
id: src-lecun-jepa-2022
type: paper
value: knowledge
channel: web
url: https://arxiv.org/abs/2211.12345
collected_at: 2026-06-28
format: pdf
title: "Joint Embedding Predictive Architectures"
authors: ["Yann LeCun", " et al."]
year: 2022
venue: "arXiv:2211.12345"
---
<论文摘要：核心贡献 / 方法架构 / 实验结果>
```

**反爬 fallback**：
- arxiv PDF 403 → 尝试 ar5iv HTML（`https://ar5iv.org/abs/<arxiv-id>`）
- 全部失败 → 记录失败日志（`failed_arxiv_<date>.txt`），标注 `status: failed`，继续下一篇

---

### 路径 ②：长访谈（Interview）

**目标**：采集专家的深度访谈（播客、文字专访），获取专家判断与推理链。

**采集流程**：

```
WebSearch（访谈关键词）
  → 搜索策略："<专家名> + interview", "<专家名> + podcast", "<专家名> + conversation"
  → 过滤条件：时长（>60 分钟或 >5000 字）、平台（Lex Fridman / AI Podcast / 顶级媒体）
  → 找到访谈 URL（文字 transcript / 播客页面带 transcript）
    ↓
WebReader/mcp__web_reader（抓全文）
  → 优先文字 transcript（比音视频更易提取）
  → 若无 transcript → 记录为 V1 扩展项（待人工摘要）
    ↓
存 sources/src-<slug>.md
  → 打标：type=interview, value=mind（或 both，视内容混合度）, channel=web, url=...
```

**搜索关键词模板**：
- `"Yann LeCun" interview`
- `"Yann LeCun" Lex Fridman`
- `"Yann LeCun" podcast transcript`

**打标示例**：

```yaml
---
id: src-lecun-lex-2023
type: interview
value: both
channel: web
url: https://lexfridman.com/lecun-2023
collected_at: 2026-06-28
format: html
title: "Yann LeCun on Lex Fridman Podcast"
authors: ["Yann LeCun", "Lex Fridman"]
year: 2023
venue: "Lex Fridman Podcast"
---
<访谈摘要：核心观点 / 覆盖话题 / 判断性语句摘录>
```

**反爬 fallback**：
- 访谈页面需登录/付费 → 记录失败，标注 `status: paywalled`，继续下一个
- transcript 不完整 → 使用现有部分，标注 `coverage: partial`（需人工标注）

---

### 路径 ③：博客文章（Blog）

**目标**：采集专家的个人博客、技术博客文章，获取专家的日常思考与观点。

**采集流程**：

```
WebSearch（博客关键词）
  → 搜索策略："<专家名> + blog", "<专家名> + medium", "<专家名> + substack"
  → 过滤条件：来源（专家个人主页 / Medium / Substack / 顶级技术博客）
  → 找到博客 URL
    ↓
WebReader/mcp__web_reader（抓全文）
  → 提取正文、保留图片说明、忽略评论区噪音
    ↓
存 sources/src-<slug>.md
  → 打标：type=blog, value=mind（技术博客可能是 both）, channel=web, url=...
```

**搜索关键词模板**：
- `"Yann LeCun" blog medium`
- `"Yann LeCun" facebook post`
- `"Yann LeCun" meta ai blog`

**打标示例**：

```yaml
---
id: src-lecun-meta-ai-2023
type: blog
value: mind
channel: web
url: https://about.fb.com/news/2023/03/lecu-meta-ai/
collected_at: 2026-06-28
format: html
title: "Yann LeCun on Meta AI Research Direction"
authors: ["Yann LeCun"]
year: 2023
venue: "Meta AI Blog"
---
<博客摘要：核心观点 / 反应的技术争议 / 专家立场>
```

**反爬 fallback**：
- 博客平台限流 → 等待 30 秒后重试，仍失败则跳过
- 动态加载页面 → 记录为需手动处理，标注 `status: manual_required`

---

## 三、打标规范（按 `schema/source.md` §4.6）

每个采集到的来源必须创建一个 `sources/src-<slug>.md` 文件，包含以下必填字段：

### 网采源必填字段（`channel: web`）

```yaml
---
id: src-<slug>              # 唯一标识
type: paper|book|interview|blog|social|review|timeline
value: knowledge|mind|both   # 决定 S2 分流
channel: web
url: <完整 URL>              # 硬门② 可 HTTP 验证
collected_at: <YYYY-MM-DD>
format: html|pdf|txt|image
---
```

### 条件必填字段

| 字段 | 适用条件 | 说明 |
|------|----------|------|
| `title` | 强烈推荐 | 来源标题 |
| `authors` | 有作者信息时 | 作者列表 |
| `year` | 有发布时间时 | 发布年份 |
| `venue` | 有发布平台时 | 期刊/会议/博客名 |

### 可选字段

| 字段 | 说明 |
|------|------|
| `coverage` | 内容完整度（`full` | `partial`） |
| `status` | 采集状态（`success` | `failed` | `paywalled` | `manual_required`） |
| `fail_reason` | 失败原因（403/限流/登录要求） |

---

## 四、Provenance 可追溯性（硬门②）

### 网采源的验证要求

每条网采源必须满足 **HTTP 可达性验证**（硬门②）：

| 验证项 | 方式 | 失败处理 |
|--------|------|----------|
| URL 存在性 | HTTP HEAD 请求 → 200 状态码 | 404/410 → 标注 `status: failed`，不阻塞整体 |
| URL 可访问性 | WebReader 抓取 → 有内容 | 403/限流 → 记录失败 + 标注，继续下一篇 |
| 内容完整度 | 字数 > 500 字（论文 > 2000 字） | 内容过少 → 标注 `coverage: partial` |

### 验证流程

```
采集时（S1）：
  ├─ WebSearch 找到 URL 候选
  ├─ HTTP HEAD 验证 → 200？
  │    ├─ 是 → WebReader 抓取
  │    └─ 否 → 记录失败，继续下一篇
  └─ 抓取成功 → 写入 src-*.md（url + collected_at）
```

### fresh subagent 抽查（S6）

S6 验证时，fresh subagent 抽查 N 条 judgment：
1. 读取 judgment 的 `provenance.sources`
2. 对每个 `src-*.md` 的 `url` 发 HTTP HEAD
3. 任一 URL 不可达 → 硬门② 失败 → <B+ 回滚

---

## 五、反爬 Fallback 策略（不阻塞整体流程）

### 失败分类与处理

| 失败类型 | 信号 | 处理方式 |
|----------|------|----------|
| **403 Forbidden** | HTTP 状态码 403 | 记录失败，标注 `status: failed`，跳过 |
| **429 Too Many Requests** | 限流信号 | 等待 30 秒后重试 1 次，仍失败则跳过 |
| **404/410 Gone** | 资源不存在 | 记录失败，标注 `status: failed`，跳过 |
| **Paywall/登录要求** | 检测到登录表单 | 标注 `status: paywalled`，建议用户手动提供 |
| **动态加载失败** | WebReader 返回空 | 标注 `status: manual_required`，V1 扩展项 |
| **超时（>30s）** | 请求超时 | 重试 1 次，仍失败则跳过 |

### 失败日志格式

在 `sources/failed_<date>.txt` 记录所有失败项：

```
[2026-06-28 14:23:15] FAILED arxiv:2211.12345 - 403 Forbidden
[2026-06-28 14:25:42] FAILED https://medium.com/@ylecun/xxx - 429 Too Many Requests
[2026-06-28 14:28:03] PAYWALLED https://www.theverge.com/lecun-interview - login required
```

### 不阻塞原则

- 单个源失败 → **不**停止整个采集流程
- 单路失败（如 ② 访谈全 403）→ **不**阻止 ①③ 路继续
- MVP 阶段 3 路全部失败 → 回退到仅用户材料通道（通道 B）

---

## 六、V1 扩展接口（MVP 不实现）

以下 3 路在 MVP 阶段**仅留接口说明**，不实现采集逻辑：

### ④ 社交媒体碎片（Social）

```
WebSearch（Twitter/X, LinkedIn）
  → 搜索策略："<专家名> + Twitter", "<专家名> + X", "<专家名> + LinkedIn post"
  → 过滤条件：高赞推文（>100 likes）、近期（近 1 年）
  → 抓取：WebReader/mcp__web_reader（注意反爬，可能需 API）
  → 存：type=social, value=mind, channel=web, url=...
```

**MVP 限制**：社媒平台反爬严格，需专用 API（Twitter API v2），MVP 不实现，V1 扩展。

### ⑤ 他者评论（Review）

```
WebSearch（第三方评论）
  → 搜索策略："<专家名> + review", "<专家名> + commentary"
  → 过滤条件：权威来源（顶级媒体/学者/同行）
  → 抓取：WebReader/mcp__web_reader
  → 存：type=review, value=mind, channel=web, url=...
```

**MVP 限制**：他者评论质量参差，需人工筛选，MVP 不实现，V1 扩展。

### ⑥ 观点时间线（Timeline）

```
多轮 WebSearch + 排序
  → 搜索策略：按年份搜索 "<专家名> + <年份>", "<代表作> + <年份>"
  → 聚合：按时间排序，识别观点演化（早期 vs 近期）
  → 存：type=timeline, value=mind, channel=web, url=...（多个 URL）
```

**MVP 限制**：观点演化需要交叉验证 + 人工标注，MVP 不实现，V1 扩展。

---

## 七、采集数量建议（MVP）

| 路径 | 目标数量 | 说明 |
|------|---------|------|
| ① 论文 | 5-10 篇 | 覆盖代表作（近 5 年） |
| ② 访谈 | 2-3 个 | 至少 1 个深度访谈（>60 分钟） |
| ③ 博客 | 5-10 篇 | 覆盖不同时期观点 |

**总量**：MVP 建议 **12-23 个源**（3 路合计），确保 S2 有足够语料提炼心智候选。

**过量处理**：若单路搜索结果 >50 个候选 → 加严过滤条件（引用数、年份、venue），避免采集噪音。

---

## 八、与用户材料通道（通道 B）的协作

### 双通道并行

```
S1 采集
  ├─ 通道 A（网采）：engines/web_collector.md（本规范）
  │   → 3 路 WebSearch + WebReader → sources/src-*.md（channel: web）
  │
  └─ 通道 B（用户材料）：engines/book_to_skill/
      → PDF/书/链接 → docling/OCR → sources/src-*.md（channel: user）
```

### 字段差异

| 字段 | 通道 A（web）| 通道 B（user）|
|------|-------------|--------------|
| `channel` | `web` | `user` |
| 必填字段 | `url` | `file` + `locator` |
| 验证方式 | HTTP 可达性 | 文件存在 + 页码可定位 |

### `both` 源的 S2 分流

- ① 论文（`type: paper, value: knowledge`）：喂 S2-knowledge
- ② 访谈（`type: interview, value: both`）：S2 按段落语义切片，分别喂双通道
- ③ 博客（`type: blog, value: mind`）：喂 S2-mind

详见 `schema/source.md` §3。

---

## 九、质量自检清单

采集完成后，逐项自检：

### 完整性
- [ ] 每路（①论文 ②访谈 ③博客）都至少有 **≥2 个源**？
- [ ] 每个 `src-*.md` 都包含必填字段（`id`, `type`, `value`, `channel`, `url`, `collected_at`, `format`）？
- [ ] `url` 字段都是**完整 URL**（含 `https://`）？

### Provenance 可追溯性
- [ ] 每个 `url` 都通过 HTTP HEAD 验证（200 状态码）？
- [ ] `collected_at` 字段格式正确（YYYY-MM-DD）？
- [ ] 失败的源都有记录（`sources/failed_<date>.txt`）？

### 打标准确性
- [ ] 论文源的 `value` 正确（`knowledge` 或 `both`）？
- [ ] 访谈源的 `value` 正确（`mind` 或 `both`）？
- [ ] 博客源的 `value` 正确（`mind` 或 `both`）？

### 反爬处理
- [ ] 遇到 403/限流时，**没有**阻塞整体流程？
- [ ] 失败源都标注了 `status: failed` / `paywalled` / `manual_required`？

### 数量控制
- [ ] ① 论文路：5-10 篇？
- [ ] ② 访谈路：2-3 个？
- [ ] ③ 博客路：5-10 篇？

---

## 十、Pipeline S1 如何调用本规范

### 输入

- 专家名（如 "Yann LeCun"）
- 代表作关键词（如 "JEPA", "Convolutional Networks", "Energy-based Model"）

### 处理流程

1. **路径 ① 论文采集**：
   - WebSearch（arxiv/scholar）→ 找到 5-10 篇论文 URL
   - HTTP HEAD 验证 → 200？
   - WebReader 抓全文 → ar5iv 优先
   - 写入 `sources/src-lecun-jepa-2022.md`（打标 `type=paper, value=knowledge, channel=web`）

2. **路径 ② 访谈采集**：
   - WebSearch（interview/podcast）→ 找到 2-3 个访谈 URL
   - WebReader 抓 transcript → 提取文字内容
   - 写入 `sources/src-lecun-lex-2023.md`（打标 `type=interview, value=both, channel=web`）

3. **路径 ③ 博客采集**：
   - WebSearch（blog/Medium）→ 找到 5-10 个博客 URL
   - WebReader 抓正文 → 忽略评论区
   - 写入 `sources/src-lecun-meta-ai-2023.md`（打标 `type=blog, value=mind, channel=web`）

4. **失败处理**：
   - 记录所有失败源到 `sources/failed_<date>.txt`
   - **不阻塞**整体流程

### 输出

- **12-23 个** `sources/src-*.md` 文件
- **1 个** `sources/failed_<date>.txt` 失败日志
- 每个源都按 `schema/source.md` §4.6 打标

---

## 十一、与 S2 的契约

S2 双轨提取读取本规范产出的 `sources/src-*.md`：

| 源类型 | `value` 字段 | S2 流向 |
|--------|-------------|---------|
| 论文（`type=paper, value=knowledge`）| `knowledge` | S2-knowledge（提炼 DAG 节点）|
| 访谈（`type=interview, value=both`）| `both` | S2 按段落语义切片，分别喂双通道 |
| 博客（`type=blog, value=mind`）| `mind` | S2-mind（提炼心智候选）|

详见 `schema/source.md` §3。

---

_本规范版本：expert-advisor-builder v0.1 | 维护：domain-knowledge-builder 扩展为 meta-skill | 参考：spec §5.1 + §9 + schema/source.md §4.6_
