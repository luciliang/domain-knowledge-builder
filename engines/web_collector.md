# 网采契约 — Web Collector Contract

> Pipeline S1 网采通道（通道 A）的采集规范。定义如何从网络采集专家材料（论文、访谈、博客），
> 并按 `schema/source.md` 标准打标存入 `sources/src-*.md`。

---

## 一、定位与职责

| 维度 | 说明 |
|------|------|
| **目的** | 从网络采集专家全网材料（论文著作、长访谈、博客文章），为 S2 双轨提取提供原始语料 |
| **时机** | Pipeline S1 采集阶段，与用户材料通道（通道 B）并行 |
| **产物** | `sources/src-*.md`（每源一个文件） |
| **关键约束** | provenance 可追溯（`url` + `collected_at）｜反爬 fallback 不阻塞整体流程 |

---

## 二、MVP 3 路采集概要

### 路径 ①：论文著作（Paper/Book）

**目标**：采集专家发表的学术论文、著作、技术报告。

**采集流程**：
```
WebSearch（arxiv/scholar）
  → 找到论文 URL（arxiv 页面 / PDF 直链 / 作者主页）
    ↓
WebReader/mcp__web_reader（抓全文）
  → 优先顺序：ar5iv HTML（公式最准）> arxiv PDF > 作者主页 PDF
    ↓
存 sources/src-<slug>.md
  → 打标：type=paper, value=knowledge, channel=web, url=..., collected_at=...
```

### 路径 ②：长访谈（Interview）

**目标**：采集专家的深度访谈（播客、文字专访），获取专家判断与推理链。

**采集流程**：
```
WebSearch（访谈关键词）
  → 找到访谈 URL（文字 transcript / 播客页面带 transcript）
    ↓
WebReader/mcp__web_reader（抓全文）
  → 优先文字 transcript（比音视频更易提取）
    ↓
存 sources/src-<slug>.md
  → 打标：type=interview, value=mind（或 both）, channel=web, url=...
```

### 路径 ③：博客文章（Blog）

**目标**：采集专家的个人博客、技术博客文章，获取专家的日常思考与观点。

**采集流程**：
```
WebSearch（博客关键词）
  → 找到博客 URL（专家个人主页 / Medium / Substack）
    ↓
WebReader/mcp__web_reader（抓全文）
  → 提取正文、保留图片说明、忽略评论区噪音
    ↓
存 sources/src-<slug>.md
  → 打标：type=blog, value=mind（或 both）, channel=web, url=...
```

---

## 三、打标规范（引用 `schema/source.md` §4.6）

每个采集到的来源必须创建一个 `sources/src-<slug>.md` 文件，按 `schema/source.md` §4.6 标准打标。

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

**与通用打标规范的差异**（`schema/source.md` §4.6）：
- `channel` 固定为 `web`
- `url` 为必填字段（硬门② 要求 HTTP 可达）
- `collected_at` 为必填字段（记录采集时间）

其余字段（`title`/`authors`/`year`/`venue`/`coverage`/`status`）按 `schema/source.md` §4.6 规范执行。

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

### 不阻塞原则

- 单个源失败 → **不**停止整个采集流程
- 单路失败（如 ② 访谈全 403）→ **不**阻止 ①③ 路继续
- MVP 阶段 3 路全部失败 → 回退到仅用户材料通道（通道 B）

---

## 六、V1 扩展接口（MVP 不实现）

以下 3 路在 MVP 阶段**仅留接口说明**，不实现采集逻辑：

### ④ 社交媒体碎片（Social）

```
WebSearch（Twitter/X, LinkedIn）→ WebReader 抓取 → 存 type=social, value=mind
```

### ⑤ 他者评论（Review）

```
WebSearch（第三方评论）→ WebReader 抓取 → 存 type=review, value=mind
```

### ⑥ 观点时间线（Timeline）

```
多轮 WebSearch + 排序 → 按时间聚合观点演化 → 存 type=timeline, value=mind
```

**MVP 限制**：社媒反爬严格、他评质量参差、时间线需人工标注，均 V1 扩展。

---

_本规范版本：expert-advisor-builder v0.1 | 维护：domain-knowledge-builder 扩展为 meta-skill | 参考：spec §5.1 + schema/source.md §4.6_
