# Expert Advisor Builder — 设计文档

| 项目 | 值 |
|------|-----|
| 日期 | 2026-06-28 |
| 状态 | Draft v2（spec review 第 2 轮修订） |
| 目标 meta-skill | `expert-advisor-builder`（由 `domain-knowledge-builder` 扩展而来） |
| 命名 | 工作名，待定 |
| 设计方式 | 与用户协作 brainstorm，五段设计逐段确认 |

> **v2 修订**：根据 spec-document-reviewer 第 1 轮反馈，补齐 schema 字段、统一 `grounded_in` 结构、定义 sources 打标 schema、写清 S5c 降级规则与 S6 语义匹配判定、澄清 dag/wiki 职责。

---

## 1. 背景与目标

### 1.1 问题陈述

用户已有两个成熟 meta-skill：

- **nuwa-skill**（女娲）：蒸馏**人物心智模型**（「一个人怎么想」）。6 路并行采集 + 三重验证 + 5 层认知 OS。但**缺乏扎实的领域知识底座**（定理、公式、严格推导）——产出的人物 skill 能"像他那么想"，但不能"像他那样用定理支撑判断"。
- **domain-knowledge-builder (DKB)**：蒸馏**领域知识 + 领域镜片**。7 步 ingest pipeline + DAG（5 节点类型 + 10 关系）+ darwin 9 维质量门 + D7 可控性。但 S5（心智模型提炼）**故意剔除了人物 DNA**（表达/判断/反模式），只保留"领域镜片"。

两者各自只覆盖一半：nuwa 有心智无知识，DKB 有知识无人物。

### 1.2 目标

构建「**顶级专家顾问生成器**」：输入专家名 + 材料，产出一个同时拥有「专家心智（主体）+ 知识依据（底盘）+ 紧耦合关联」的 skill。该 skill 能回答：

- 「什么是 X」（知识查询）→ 定理/方法原文
- 「专家怎么看 X」（心智查询）→ 专家判断 + 推理链
- 「专家为什么认为 X / X 的依据」（融合查询）→ **专家判断 + 支撑该判断的理论依据节点**

终极目的：像 nuwa 那样作为**元 skill**，批量生成不同专家的顾问 skill，供未来复用。

### 1.3 非目标（YAGNI）

- 不做通用 skill 生成（只生成"专家顾问"这一类 skill）
- MVP 不做完整 nuwa 6 路网采（V1 再补全）
- MVP 不做多专家批量（先单专家跑通闭环）
- 不替代 nuwa-skill（nuwa 继续做纯人物蒸馏，本 skill 是 DKB 的扩展分支）
- 不做实时专家观点监控（V2 考虑演化追踪）

---

## 2. 核心决策（已与用户确认）

| 决策点 | 选择 | 理由 |
|--------|------|------|
| **核心定位** | 思维为主 + 知识支撑 | 用户要"为心智模型配上领域知识"，心智是主体镜片，知识是判断的理论依据。数学/严肃科学场景知识要硬 |
| **来源** | 网采为主 + 用户材料补充 | nuwa 式 6 路网络采集专家全网信息 + 用户提供的 PDF/书作为种子/补充 |
| **融合粒度** | 紧耦合（判断 + 依据） | 每个专家判断关联具体定理/方法节点；回答"专家怎么看 X"= 判断 + 依据节点 ID。最像真专家（有观点且有据）|
| **架构方案** | A：扩展 DKB | 知识基础设施（DAG/darwin/D7/公式严谨）已就绪，作为骨架；心智（nuwa 人物 DNA）作加法嫁接。工程最稳、复用最多 |

### 2.1 为什么选方案 A（扩展 DKB）而非扩展 nuwa 或新建

核心洞察：紧耦合的「依据」必须是结构化知识节点（DAG 定理/方法）。因此 DKB 那套知识基础设施（DAG + darwin 质量门 + D7 可控性 + docling 公式严谨）是绕不开的硬骨头。

- 把**难的部分（知识基础设施）当骨架**（DKB 已就绪），把**容易加的部分（心智）作嫁接**——工程最稳
- DKB 已内置 S5 三重验证（nuwa 方法论早就迁过来了），「专家心智」只需**恢复 nuwa 被 DKB 剔除的人物 DNA**，不是从零写
- 「紧耦合」天然落在 DKB 的 DAG 上——每个专家判断挂到定理/方法节点，DAG 即依据载体
- 增量 ingest 机制正好服务"在世专家持续更新"

扩展 nuwa（方案 B）的致命伤：nuwa 没有知识严谨性传统，要重建 DAG+darwin+D7+公式四件套，比"加一层心智"难得多。

---

## 3. 整体架构

### 3.1 定位

把 `domain-knowledge-builder` 从「领域知识库生成器」升级为「专家顾问生成器」。输入 = 专家名 + 种子材料 → 输出 = 一个同时拥有「专家心智（主体）+ 知识依据（底盘）+ 紧耦合关联」的 skill。

### 3.2 meta-skill 自身的扩展

```
expert-advisor-builder/  (原 domain-knowledge-builder 扩展)
├── SKILL.md                     # 改：触发词/路由加"专家顾问"
├── schema/
│   ├── schema.md                # 原：5节点+10关系+D7（知识底盘，不动）
│   ├── expert-mind.md           # 🆕 专家心智 schema（§4.2）
│   ├── coupling.md              # 🆕 紧耦合关联 schema（judgment §4.3）
│   └── source.md                # 🆕 来源打标 schema（§4.6）
├── pipeline/
│   ├── ingest.md                # 改：S1 加双通道、S5 拆三步
│   ├── query.md                 # 改：查询协议加"专家判断+依据"模式
│   └── state/                   # 原：D7 不动
├── engines/                     # 命名统一为单文件 + 子目录混合（见下）
│   ├── book_to_skill/           # 原：多格式提取（目录，因含脚本）
│   ├── web_collector.md         # 🆕 nuwa 6路采集契约（单文件）
│   ├── expert-mind-rubric.md    # 🆕 专家心智提炼（恢复 nuwa 人物DNA）
│   ├── nuwa-validation.md       # 原：三重验证
│   └── darwin-rubric.md         # 改：第9维加专家忠实度硬门
└── examples/
    └── <某专家>/                 # 🆕 黄金参照（建议 karpathy-advisor）
```

> **engines 命名约定**：含可执行脚本的用目录（`book_to_skill/`、未来的 `web_collector/scripts/`），纯方法论契约用单 `.md`（`web_collector.md`、`expert-mind-rubric.md`、`nuwa-validation.md`、`darwin-rubric.md`）。

### 3.3 生成的产物 skill 结构（专家顾问 skill）

```
<expert>-advisor/
├── SKILL.md                 # 入口(<4K)：专家心智摘要 + 查询协议 + 诚实边界
├── dag/                     # 知识节点定义 + dag-index.json（单一数据源）
│   ├── dag-index.json       #   节点/边索引（DAG 主数据）
│   └── knowledge/           #   节点定义文件（def-/thm-/meth-/exp-/ins-）
├── expert-mind/             # 🆕 专家心智（主体）
│   ├── mental-models.md     #   心智模型/启发式/反模式（§4.2）
│   ├── judgments.md         #   judgment 索引（§4.3，紧耦合枢纽）
│   └── index.md             #   心智导航（只引用 ID）
├── wiki/                    # 导航层（不存数据，只引用 dag 节点 ID）
│   ├── index.md             #   按类型分组的节点导航
│   └── overview.md          #   领域全局概览
└── sources/                 # 🆕 来源打标（§4.6，网采URL + 用户PDF provenance）
    └── src-*.md
```

> **dag/ vs wiki/ 职责澄清**（解决数据双写）：`dag/` 是知识节点的**单一数据源**（节点定义 + index）；`wiki/` 是**纯导航层**（index/overview 只引用 dag 节点 ID，不复制节点内容）。心智在 `expert-mind/`，judgment 在 `expert-mind/judgments.md`。三层数据不重叠。

### 3.4 数据流总览

```
专家名 + 种子材料(PDF/书/链接)
      ↓
[S1 采集·双通道]
   ├─ 网采通道: WebSearch+webReader, nuwa 6路(论文/访谈/博客/推文/他评/时间线)
   └─ 用户材料: docling(born-digital,保LaTeX) / OCR(扫描书) / pdftotext(fallback)
      ↓ raw corpus → sources/src-*.md（每源打标 value, §4.6）
[S2·双轨提取]
   ├─ knowledge/both 源 ──▶ 知识 DAG 节点(定理/方法/公式, 带provenance)
   └─ mind/both 源     ──▶ 专家心智候选(判断/直觉/反模式)
      ↓（both 源按段落语义切片，分别喂两通道，§5.2）
[S3 合并]  DAG合并(contradicts人工确认) + 心智候选去重
[S4 导航]  知识导航(wiki/) + 心智导航(expert-mind/index)
      ↓
[S5·三步]  ← 核心
   S5a 领域镜片(现有三重验证)         ─┐ 两个独立 subagent，可并行
   S5b 专家心智(nuwa人物DNA, 三重验证) ─┘
   S5c 🆕紧耦合融合(依赖 S5a/S5b): 建立 judgment + 降级规则(§4.4)
      ↓
[S6 验证·fresh] [S7 组装] → darwin门(三硬门, §7)
      ↓
专家顾问 skill
```

---

## 4. 数据结构与紧耦合建模（核心）

### 4.1 三层实体 + 连接关系

```
专家心智(expert-mind/)  ──grounded_in──▶  知识节点(dag/knowledge/)   ← DKB 原生，不动
   ↑                                          ↑
   └──────── judgment(expert-mind/) ──────────┘
              ↑ 紧耦合的"枢纽"：一条专家判断 = 立场 + 推理 + 依据节点
```

知识节点 schema 完全继承 DKB（5 类型 def/thm/meth/exp/ins + 10 关系 + D7 provenance），**不动**。

### 4.2 专家心智元素 schema（`expert-mind/mental-models.md`）

```yaml
---
id: mm-lecun-energy-based-worldview
type: mental_model            # mental_model | heuristic | anti_pattern
label: 能量模型世界观
statement: "智能 = 在能量函数上做优化/约束满足，而非自回归预测下一token"
status: verified              # verified | demoted | inferred | contradicted（§4.4 降级规则）
verification:                 # nuwa 三重验证（S5b 跑）；judgment 继承此结果，不独立验证
  cross_scene: { pass: true, evidence: [JEPA架构, 反对LLM推理, LatentEBM] }
  generative: { pass: true, predicts: "对任何新架构先问能量/目标函数" }
  exclusive:  { pass: true, vs: "贝叶斯派靠先验、生成式派靠似然" }
grounded_in:                  # 紧耦合：结构同 judgment.grounded_in（统一对象数组）
  - { node: thm-ebm-as-energy-minimization, role: supports, quote: "..." }
  - { node: meth-jepa-latent-predictive,     role: supports, quote: "..." }
confidence: high              # high | medium | low
provenance: { sources: [lecun-2022-jepa, lex-interview-2023] }
---
<展开：核心思想 / 跨场景证据 / 局限 / 支撑节点>
```

### 4.3 judgment schema——紧耦合的枢纽（`expert-mind/judgments.md`）

回答「专家怎么看 X」的载体：**一条判断 = 立场 + 推理链 + 依据节点**。

**judgment 不独立跑三重验证**，而是通过 `derived_from` 继承其所属心智元素（§4.2）的 `verification` 结果。judgment 自身的质量由 `provenance`（忠实度，硬门②）+ `grounded_in`（紧耦合，硬门①）保证。

```yaml
---
id: judg-lecun-llm-cant-reason
type: judgment                # 固定值 judgment（与心智元素 type 区分）
label: LLM不能真正推理
status: verified              # verified | inferred | contradicted（推断结果落盘为 inferred，§6.2）
trigger: "LLM 能做真正的推理吗 / 为什么 LLM 不会规划"
derived_from: mm-lecun-energy-based-worldview   # 所属心智元素（继承其 verification）
judgment: "不能。纯自回归续写缺乏世界模型，无法预测后果做规划"
reasoning: "推理 = 在抽象空间预测后果+规划路径；自回归只做token级概率续写，
           没有世界模型的 forward 模拟，故外推时暴露"
grounded_in:                  # 依据：统一对象数组（与心智元素同结构）
  - { node: thm-planning-needs-world-model, role: supports, quote: "..." }
  - { node: meth-jepa-latent-predictive,     role: supports, quote: "..." }
counter_evidence:             # 诚实：列反方（role 用 context）
  - { node: exp-gpt4-planning-benchmarks, role: context, note: "CoT下部分规划任务可通过" }
confidence: high
provenance: { sources: [lex-interview-2023, ieee-spectrum-2022] }
---
```

### 4.4 紧耦合分级与降级规则（解决 S5c 边界 case）

**强度按验证分级**：

| 心智元素 | 三重验证 | 与知识的耦合要求 |
|----------|----------|------------------|
| 心智模型 (mental_model) | 3 重全过 | **必须** `grounded_in ≥1` 节点（强耦合，有硬依据）|
| 启发式 (heuristic) | 1-2 重 | `grounded_in` 可选（可能只有经验依据，标注）|
| 反模式 (anti_pattern) | 排他性必过 | `grounded_in` 用 `role: refutes` 指向反对的方法节点 |

**降级规则**（S5c 执行，处理"3 重过但依据不足"的边界）：

| 情况 | 处理 | status |
|------|------|--------|
| 3 重全过，但 `grounded_in` **完全找不到**任何相关节点 | **丢弃**（纯口嗨，无任何知识锚点）| dropped（不入库）|
| 3 重全过，找到候选节点但 S6 判定**语义不匹配** | **降级为 heuristic**，保留原 verification + 标注降级原因 | demoted（`demote_reason: semantic_mismatch`）|
| 降级后的 heuristic | `grounded_in` 变可选，但 `provenance` 必须保留；不重跑验证 | demoted |

**关键约束**：没有 `grounded_in` 依据的判断，**不能冒充心智模型**——这是"有依据"的硬闸，由 S6 + darwin 门强制。

**两条边界澄清**（reviewer round-2 建议）：
- **降级只作用于心智元素（§4.2），不作用于 judgment**：judgment 的 status 枚举为 `verified | inferred | contradicted`（**无 `demoted`**）。降级/丢弃由 S5c 在心智元素层面执行；judgment 通过 `derived_from` 继承其所属心智元素的最终 status，自身不参与 §4.4 降级。
- **§4.4 降级/丢弃规则优先于 §6.2 推断落盘**：若一条判断同时落在「3 重过但 grounded_in 完全找不到」情形又被推断机制触及，以 §4.4 为准——即无依据的推断判断**不落盘 `inferred`**，而是按 §4.4 丢弃或降级为 heuristic。

### 4.5 judgment 独立成层、不污染知识 DAG

DKB 的 DAG 边是「知识↔知识」。如果把「专家判断」塞进 DAG 当节点，会污染纯知识图谱、query 时难剪枝。所以 judgment 作为**独立关联层**（`expert-mind/judgments.md`），通过 `grounded_in` 引用知识节点 ID——知识图谱保持干净，紧耦合关系单独可查、可验证。

### 4.6 来源打标 schema（`sources/src-*.md`）——S1→S2 的契约

每个采集/提供的来源存一个 `src-*.md`，frontmatter 打标决定 S2 分流：

```yaml
---
id: src-lecun-lex-2023
type: interview              # paper | book | interview | blog | social | review | timeline
value: mind                  # knowledge | mind | both（决定喂哪个 S2 通道）
channel: web                 # web（网采）| user（用户材料）
url: https://lexfridman.com/lecun-2023  # 网采源：URL（硬门②可 HTTP 验证）
file: lecun-jepa.pdf         # 用户材料源：本地文件 + 页码锚点
locator: { page: 12, section: "§3" }   # 用户材料必填（硬门②核对依据）
collected_at: 2026-06-28
format: html                 # html | pdf | txt | image
---
<来源摘要：核心贡献 / 覆盖范围 / 可信度>
```

**`both` 源的分流契约**（解决开放问题 5）：`value: both` 的源（如研究论文：既含方法也含作者动机）在 S2 由 worker **按段落语义切片**——知识性段落（定理/方法/实验）喂 S2-knowledge，判断性段落（作者主张/怀疑/动机）喂 S2-mind。切片边界由 S2 worker 标注，S3 合并时去重。

---

## 5. Pipeline 契约

相对 DKB 的改动集中在 **S1（采集）** 和 **S5（心智）**。

### 5.1 S1 采集·双通道（新）+ 来源打标

```
专家名 + 种子材料
   ├─【通道A：网采】engines/web_collector.md (nuwa 6路, WebSearch+webReader)
   │     ①论文著作 ②长访谈 ③博客文章 ④社媒碎片 ⑤他者评论 ⑥观点时间线
   │     → 每源存 sources/src-*.md（channel: web, url, §4.6）
   │
   └─【通道B：用户材料】engines/book_to_skill/ 按格式路由
         born-digital PDF ─▶ docling (保LaTeX)
         扫描书/图片     ─▶ unlimited-ocr
         arxiv 论文      ─▶ ar5iv HTML (公式最准)
         纯文本          ─▶ pdftotext (fallback)
         → 每源存 sources/src-*.md（channel: user, file, locator, §4.6）
```

打标 `value = knowledge | mind | both`（§4.6）决定 S2 分流。

### 5.2 S2 双轨提取（改，并行 fan-out）

| 通道 | 输入 | 提取什么 | 输出 |
|------|------|----------|------|
| **S2-knowledge**（继承 DKB S2） | knowledge 源 + both 源的知识切片 | 定理/方法/公式（docling 保 LaTeX）| 知识 DAG 节点 |
| **S2-mind**（新） | mind 源 + both 源的判断切片 | 专家判断/直觉/反模式/决策启发式 | 心智候选（带 provenance）|

`both` 源由 worker 按段落语义切片后分别喂两通道（§4.6）。

### 5.3 S5 三步（核心扩展）

原 DKB S5 只做领域镜片，现拆三步。**S5a 与 S5b 是两个独立 subagent**（上下文不同：S5a 用现有 nuwa-validation，S5b 加载 expert-mind-rubric），可并行（契合 dispatching-parallel-agents）；**S5c 依赖两者**完成，且必须等待 **S3 合并完成（含 contradicts 人工确认）后启动**——因为 S5c 要为心智判断挂 `grounded_in` 依据节点，节点必须先在 S3 合并后的 DAG 中存在（避免与 §3.4 数据流"S5 在 S4 之后"的时序误读）。

```
S5a 领域镜片(独立 subagent)  ─┐ 从知识节点提炼「领域怎么思考」(三重验证)  ← 保留
                             │
S5b 专家心智(独立 subagent)  ─┤ 从心智候选提炼「这位专家怎么思考」(三重验证)
                             │  恢复 nuwa 人物DNA, 加载 engines/expert-mind-rubric.md
                             │  → expert-mind/mental-models.md
                             │
S5c 紧耦合融合(依赖 S5a/S5b) ─┘ 对每个心智模型/判断，找支撑它的知识节点
                                建立 judgment(立场+推理+grounded_in)
                                执行降级规则(§4.4): 无依据→丢弃, 语义不匹配→降级heuristic
                                → expert-mind/judgments.md
```

### 5.4 其余 stage 的增量

| Stage | 继承 DKB | 新增 |
|-------|----------|------|
| S3 合并 | 知识 DAG 合并（contradicts 人工确认）| 心智候选去重（同判断多次出现→加强证据）|
| S4 导航 | 知识 wiki/index | `expert-mind/index` |
| S6 验证 | 知识 DAG 校验（fresh subagent）| **紧耦合校验**（判定方式见下）|
| S7 组装 | SKILL.md 框架 | 顶部放专家心智摘要 + 查询协议加"判断+依据"模式 |

**S6 紧耦合校验的判定方式**（解决"语义匹配无操作定义"）：

| 检查 | 判定方式 | 对应硬门 |
|------|----------|----------|
| grounded_in 节点**存在性** | **lint 程序化**（`lint_d7.py` 扫 dag-index，节点 ID 不存在即报）| 硬门③ 无孤儿判断 |
| grounded_in **语义匹配**（节点是否真支撑该判断）| **fresh subagent 抽查**（与忠实度合并，§7 硬门②）| 硬门① 紧耦合完整性 |
| judgment **忠实度**（是否真来自专家，非编造）| **fresh subagent 抽查** provenance（网采 URL HTTP 可达 / 用户材料 locator 可定位）| 硬门② |

> 即：存在性 = 程序化（快、确定）；语义匹配 + 忠实度 = fresh subagent 抽查（慢、需判断力，合并为一次 fresh 校验）。

---

## 6. 查询协议

生成的 `<expert>-advisor` skill 被调用时，按**问题意图路由**到三种模式。

### 6.1 意图路由（query.md 第 0 步）

```
用户问题
   ↓ 判断类型
   ├─ "什么是X / X的定义/定理"        ─▶ 【知识模式】
   ├─ "专家怎么看X / 会怎么选 / 怎么办" ─▶ 【心智模式】
   ├─ "专家为什么认为X / X的依据"       ─▶ 【融合模式】
   └─ 模糊                              ─▶ 【融合模式】(默认，最全)
```

### 6.2 三种模式

| 模式 | 流程 | 返回 |
|------|------|------|
| **知识模式**（继承 DKB）| DAG 遍历找节点 | 定理/方法原文（LaTeX）+ 来源 provenance |
| **心智模式** | 加载专家心智镜片 + 匹配 judgment | 专家判断 + 推理链 + grounded_in 依据节点；无现成 judgment 则用镜片推断 |
| **融合模式** ⭐ | 镜片理解→找 judgment→加载依据节点→综合 | 立场 + 理论依据 + 替代方案 + 局限，每论点挂 judgment ID + 节点 ID |

**心智模式/融合模式的推断落盘**（解决测试可复现）：当无现成 judgment、用镜片推断时，推断结果**在构建期/测试期落盘为新 judgment**（`status: inferred`，`derived_from` 指向所用心智模型），供 S6 复审与端到端测试复现。**运行期 skill 被查询时只读不写**——不持久化运行期推断（避免违背 skill 只读惯例 + 并发写冲突），运行期推断仅返回结果并标注「推断·非原话」。构建期落盘使测试可复现，运行期无副作用。

### 6.3 融合模式回答示例

> **问**：LeCun 会怎么看「用 LLM 做世界模型」？
>
> **答**：
> - **[立场]** 大概率反对——自回归 LLM 缺乏世界模型的 forward 模拟 *(judg-lecun-llm-cant-reason)*
> - **[理论依据]** 规划/推理需在抽象空间预测后果 *(thm-planning-needs-world-model)*，而自回归只做 token 续写
> - **[他的替代方案]** JEPA 在 latent 空间做预测式学习 *(meth-jepa-latent-predictive)*
> - **[诚实边界]** 但 CoT 下部分规划任务 GPT-4 可通过 *(exp-gpt4-planning-benchmarks)*，此为开放争论

### 6.4 诚实边界规则（贯穿三模式）

| 情况 | 处理 |
|------|------|
| 专家没明确说过的 | 标注「**推断·基于其心智镜片外推，非原话**」（落盘 status: inferred），不冒充原话 |
| 知识不足的子领域 | 明说「本库未覆盖此方向」，不补脑 |
| 专家观点演化的 | 标注「早期/近期」，不把旧观点改写成新观点 |
| judgment 互相矛盾 | 并列双方 + 各自适用边界，不编调和 |
| 落在明确反模式上 | 直接说「专家会反对，因为…」+ 反模式依据 |

---

## 7. 质量门扩展

紧耦合和专家忠实度是**致命问题**（不是扣分项），设为**硬门**——不过即判 <B+ 回滚。

| 硬门 | 检查项 | 判定方式 | 实现 |
|------|--------|----------|------|
| **① 紧耦合完整性** | 每个 3 重过的心智模型 `grounded_in ≥1` 节点，且**语义匹配** | fresh subagent 抽查语义 | S6 |
| **② judgment 忠实度** | 每条 judgment 有真实 provenance（网采 URL HTTP 可达 / 用户材料 `locator` 可定位到页码章节），非编造 | fresh subagent 抽查 | S6 |
| **③ 无孤儿判断** | judgment 的 `grounded_in` 节点都在 dag-index 里 | **lint 程序化** | `lint_d7.py` 扩展 |
| darwin 第9维可审计支柱 | judgment provenance 可追溯到具体来源（URL 或 file+locator） | darwin-rubric 改 | darwin |

> 用户材料通道的忠实度靠 `locator: {page, section}`（§4.6）保证——fresh subagent 可核对"这条判断真来自该 PDF 第几页"，否则硬门②对用户材料形同虚设。

棘轮机制继承 DKB（<B+ → git revert → 修单一维度 → 重评；连续 3 轮无改进 → 探索性重写）。

---

## 8. 测试策略（四层）

1. **程序化 lint**（`lint_d7.py` 扩展）：grounded_in 节点存在性（硬门③）/ 孤儿判断 / frontmatter 字段完整性
2. **忠实度 + 语义抽查**（fresh subagent）：抽 N 条 judgment，核对 provenance 真实性（硬门②）+ grounded_in 语义匹配（硬门①）。MVP 建议 N=5-10
3. **融合查询端到端**：K 个「专家怎么看 X」问题 → 融合模式 → 检查「有立场 + 有依据节点 + 有诚实边界」三要素。推断结果因落盘（§6.2）可复现
4. **黄金参照**：选 1 位专家人工策展 A 级参照

**黄金参照专家风险**（reviewer 指出）：Karpathy 强在工程直觉，严格定理级节点（thm 类型）可能偏少，导致紧耦合硬门①在黄金参照上难满足。**对策**：黄金参照允许 heuristic 占比高（心智为主、知识为辅的真实专家本就如此），硬门①只要求"3 重过的心智模型有依据"，heuristic 无依据不违规；若 Karpathy 定理依据仍不足，备选 **Hinton**（反向传播/BP 有定理级论述）。

---

## 9. MVP 里程碑（YAGNI，分阶段）

| 阶段 | 范围 | 目标 |
|------|------|------|
| **MVP** | 单专家 + 用户材料(PDF/书) + **最小网采 3 路（①论文 ②访谈 ③博客）** + S2 双轨 + S5 三步 + 三硬门 + Karpathy 黄金参照 | 跑通「专家心智+知识融合」最小闭环，证明核心价值 |
| **V1** | nuwa 完整 6 路网采（+④社媒 ⑤他评 ⑥时间线）+ 来源打标自动化 + 多专家增量 ingest | 真正的"元 skill 生成多个专家 skill" |
| **V2** | 忠实度测试自动化 + 观点演化追踪 + 跨专家交叉验证 | 质量与可信度提升 |

---

## 10. 已验证的技术前提

| 前提 | 状态 | 证据 |
|------|------|------|
| **docling 可用** | ✅ 已验证（修复代理后）| 根因 = `all_proxy=socks://`，httpx 不支持 socks scheme。修复 = `unset all_proxy`（保留 http 代理）+ `HF_ENDPOINT=hf-mirror.com`。修复后 RapidOCR + TableFormer 模型加载完成、转换正常 |
| **docling 公式能力** | ✅（DKB 已验证）| DKB 的 diffusion-models 示例用 docling/ar5iv 保留 662 个 LaTeX 公式 |
| **Unlimited-OCR 定位** | 扫描件/图片专用，**不替代** docling | 实测：5-7 分/页（慢）、输出有重复+幻觉、无公式 LaTeX 证据。仅用于无文本层的扫描书/图片 |
| **nuwa 6 路采集实现** | 用 WebSearch + webReader（mcp__web_reader）| Claude Code 环境已有这两个工具 |
| **三重验证方法论** | DKB 已内置（nuwa-validation.md）| S5b 复用，只需恢复人物 DNA 部分 |

---

## 11. 开放问题（待实现阶段定）

1. **命名**：`expert-advisor-builder` vs `advisor-forge` vs 其他
2. **黄金参照专家**：Karpathy 首选（备选 Hinton）——见 §8 风险对策
3. **judgment 忠实度抽查样本数 N**：MVP 建议取 5-10
4. **网采的反爬/合规**：Twitter/YouTube 等平台采集的可行性与合规边界
5. ~~`both` 来源的分流粒度~~ → **已解决**（§4.6 按段落语义切片）

---

## 12. 实现顺序建议（供 writing-plans 参考）

1. schema 层：`expert-mind.md`（§4.2）+ `coupling.md`（§4.3 judgment）+ `source.md`（§4.6）
2. engines 层：`expert-mind-rubric.md`（从 nuwa 恢复人物 DNA）+ `web_collector.md`（最小 3 路契约）
3. pipeline 层：ingest.md 改 S1 双通道 + S5 三步（S5a/S5b 独立 subagent）；query.md 加三模式路由 + 推断落盘
4. 质量层：`lint_d7.py` 扩展硬门③ + darwin-rubric 加硬门①②
5. 黄金参照：人工策展 karpathy-advisor（允许 heuristic 占比高）
6. MVP 端到端验证（四层测试）

---

_本设计文档基于 domain-knowledge-builder (DKB) + nuwa-skill + darwin-skill 三个现有 meta-skill 的融合，遵循 DKB 的 darwin 质量门与 D7 可控性传统。_
