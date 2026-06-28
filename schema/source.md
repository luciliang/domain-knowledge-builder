# 来源打标 Schema — Source Tagging

> 本文件定义专家顾问生成器中**来源打标规范**。每个采集/提供的来源存一个 `src-*.md`，frontmatter 打标决定 S2 分流（knowledge/mind/both），是 S1→S2 的核心契约。

---

## 0. 定位与职责

| 维度 | 说明 |
|------|------|
| **目的** | 为每个来源打标，决定其内容流向（knowledge 通道、mind 通道，或 both 双通道）|
| **时机** | S1 采集阶段：网采通道（`engines/web_collector.md`）+ 用户材料通道（`engines/book_to_skill/`） |
| **产物** | `sources/src-*.md`（每个来源一个文件） |
| **关键作用** | `value` 字段决定 S2 分流；`both` 源触发段落语义切片（§3） |

---

## 1. Frontmatter 字段定义

每个 `sources/src-*.md` 文件必须包含以下 YAML frontmatter：

### 必填字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 唯一标识，格式 `src-<slug>`（如 `src-lecun-lex-2023`） |
| `type` | enum | ✅ | 来源类型：`paper` \| `book` \| `interview` \| `blog` \| `social` \| `review` \| `timeline` |
| `value` | enum | ✅ | 内容价值：`knowledge` \| `mind` \| `both`（**决定 S2 分流**）|
| `channel` | enum | ✅ | 采集通道：`web`（网采）\| `user`（用户材料） |
| `collected_at` | date | ✅ | 采集日期（YYYY-MM-DD） |
| `format` | enum | ✅ | 格式：`html` \| `pdf` \| `txt` \| `image` |

### 条件必填字段

| 字段 | 类型 | 适用条件 | 说明 |
|------|------|----------|------|
| `url` | string | `channel: web` | 网采源的 URL（**硬门② 可 HTTP 验证**） |
| `file` | string | `channel: user` | 用户材料源：本地文件路径（相对 skill 根目录） |
| `locator` | object | `channel: user` | 用户材料源：定位信息 `{page: <页码>, section: <章节>}`（**硬门② 核对依据**） |

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 来源标题 |
| `authors` | list | 作者列表（人名或机构） |
| `year` | number | 发布年份 |
| `venue` | string | 发布平台/期刊/会议 |

---

## 2. 字段枚举值说明

### type（来源类型）

| 值 | 含义 | 典型示例 |
|------|------|----------|
| `paper` | 学术论文 | arxiv 论文、期刊论文 |
| `book` | 书籍 | 教材、专著 |
| `interview` | 长访谈 | 播客访谈、文字专访 |
| `blog` | 博客文章 | 个人博客、技术博客 |
| `social` | 社交媒体碎片 | Twitter/X、LinkedIn 短文 |
| `review` | 他者评论 | 第三方评论、综述文章 |
| `timeline` | 观点时间线 | 按时间整理的观点演化 |

### value（内容价值）——**核心分流字段**

| 值 | 含义 | S2 流向 | 典型内容 |
|------|------|---------|----------|
| `knowledge` | 知识性来源 | S2-knowledge | 定理、方法、实验、定义 |
| `mind` | 判断性来源 | S2-mind | 专家观点、判断、决策启发式 |
| `both` | 混合来源 | **双通道**（§3 切片规则）| 研究论文（方法+作者动机）、深度访谈（技术+观点） |

### channel（采集通道）

| 值 | 必填字段组合 | 验证方式 |
|------|-------------|----------|
| `web` | `url` | HTTP 可达性（硬门②） |
| `user` | `file` + `locator` | 文件存在 + 页码/章节可定位（硬门②） |

---

## 3. `both` 源的切片契约（S2 分流机制）

**问题**：`value: both` 的源（如研究论文）既含知识性内容（定理/方法），也含判断性内容（作者主张/怀疑）。如何分流？

**解决方案**：S2 worker 按**段落语义切片**，分别喂双通道。

### 切片规则

| 段落语义 | 示例 | S2 流向 |
|----------|------|---------|
| 知识性段落 | 「定理 3.1：在能量函数满足 Lipschitz 连续条件下...」、「实验设置：我们使用 ResNet-50...」 | S2-knowledge（提炼 DAG 节点） |
| 判断性段落 | 「我们认为当前的自回归方法无法真正推理」、「未来方向应关注 latent space 预测」 | S2-mind（提炼心智候选） |

### 切片边界标注

- S2 worker 在切片时标注 `slice_type: knowledge \| mind`
- S3 合并时去重：同一源的不同切片可能产生相同节点（去重保留 provenance）

### 为什么不简单复制到双通道？

**避免污染**：
- 知识通道不应混入专家主观判断（DAG 纯知识图谱）
- 心智通道不应混入纯技术细节（心智模型不是技术手册）

**语义切片的价值**：
- 保留上下文（判断性段落中的技术术语仍是判断的一部分）
- 提高提取精度（LLM 在纯语境下提取更准）

---

## 4. 完整示例

### 示例 1：网采源（Web Interview）

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
```

**说明**：
- `value: both`：访谈既含技术细节（JEPA 架构，knowledge），也含判断（LLM 不能推理，mind）
- S2 worker 按段落语义切片，分别喂双通道

### 示例 2：用户材料源（User PDF）

```yaml
---
id: src-lecun-jepa-2022
type: paper
value: knowledge
channel: user
file: inputs/papers/lecun-jepa-arxiv-2022.pdf
locator:
  page: 1
  section: "§1 Introduction"
collected_at: 2026-06-28
format: pdf
title: "Joint Embedding Predictive Architectures"
authors: ["Yann LeCun", " et al."]
year: 2022
venue: "arXiv:2211.12345"
---
```

**说明**：
- `channel: user`：用户提供的技术论文，`file` + `locator` 必填
- `locator.page` + `locator.section`：硬门② 可精确定位到"这条判断/定理来自第几页第几节"

---

## 5. 字段必填矩阵

| channel | 必填字段 | 条件必填字段 |
|---------|---------|-------------|
| `web` | `id`, `type`, `value`, `channel`, `url`, `collected_at`, `format` | — |
| `user` | `id`, `type`, `value`, `channel`, `file`, `locator`, `collected_at`, `format` | — |

**核心逻辑**：
- 网采源靠 `url` 验证（HTTP 200）
- 用户材料源靠 `file` + `locator` 验证（文件存在 + 页码可 grep）

---

## 6. 质量保证（硬门②：judgment 忠实度）

**问题**：如何防止编造的 judgment（假称专家说过某话）？

**解决**：`provenance` 追溯，每条 judgment 必须能定位到具体来源。

### 验证方式

| channel | 验证手段 | 对应字段 |
|---------|----------|----------|
| `web` | **HTTP 可达性检查**（`curl -f` 返回 200） | `url` |
| `user` | **文件存在 + 页码定位**（`grep -n` 在指定页码找到原文） | `file` + `locator.{page, section}` |

### S6 校验流程

1. **程序化验证**（快速、确定）：
   - 网采源：`curl -f <url>` → HTTP 200
   - 用户材料源：`test -f <file>` → 文件存在

2. **Fresh subagent 抽查**（慢、需判断力）：
   - 抽 N 条 judgment（MVP 建议 N=5-10）
   - 核对 `judgment.judgment` 是否能在 `source.locator` 定位到原文
   - 发现编造 → **硬门② 失败，darwin 评分 <B+，回滚**

---

## 7. 与其他 Schema 的关系

| Schema | 关系 |
|--------|------|
| `schema.md` | 知识节点 schema（不变），`source.md` 是其**输入**（S1→S2） |
| `expert-mind.md` | 专家心智 schema（§4.2），judgment 的 `provenance.sources` 引用 `src-*.md` 的 `id` |
| `coupling.md` | 紧耦合 schema（§4.3），judgment 的 `grounded_in` 关联知识节点 |

**数据流**：
```
S1 采集 → sources/src-*.md（本 schema）
         ↓
S2 分流（knowledge/mind/both）
         ↓
S5a/b/c → expert-mind/judgments.md（judgment.provenance.sources 引用 src-*.md）
```

---

## 8. 命名规范

| 对象 | 命名格式 | 示例 |
|------|---------|------|
| 文件名 | `src-<slug>.md` | `src-lecun-lex-2023.md` |
| 文件 ID | `src-<slug>` | `src-lecun-lex-2023` |
| slug | 小写 + 连字符，含时间/标识符 | `lecun-lex-2023`, `karpathy-blog-2024` |

**slug 生成规则**：
- 网采源：`<主体>-<平台>-<年份>`（如 `lecun-lex-2023`）
- 用户材料源：`<作者>-<关键词>-<年份>`（如 `lecun-jepa-2022`）

---

_本 schema 版本：expert-advisor-builder v0.1 | 维护：domain-knowledge-builder 扩展为 meta-skill_
