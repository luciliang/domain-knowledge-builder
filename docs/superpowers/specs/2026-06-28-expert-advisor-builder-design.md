# Expert Advisor Builder — 设计文档

| 项目 | 值 |
|------|-----|
| 日期 | 2026-06-28 |
| 状态 | Draft（待 spec review） |
| 目标 meta-skill | `expert-advisor-builder`（由 `domain-knowledge-builder` 扩展而来） |
| 命名 | 工作名，待定 |
| 设计方式 | 与用户协作 brainstorm，五段设计逐段确认 |

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

### 3.2 meta-skill 自身的扩展（在 DKB 5 层上加 3 件事）

```
expert-advisor-builder/  (原 domain-knowledge-builder 扩展)
├── SKILL.md                     # 改：触发词/路由加"专家顾问"
├── schema/
│   ├── schema.md                # 原：5节点+10关系+D7（知识底盘，不动）
│   ├── expert-mind.md           # 🆕 专家心智 schema（5层OS结构）
│   └── coupling.md              # 🆕 紧耦合关联 schema（判断↔依据节点）
├── pipeline/
│   ├── ingest.md                # 改：S1 加双通道、S5 拆三步
│   ├── query.md                 # 改：查询协议加"专家判断+依据"模式
│   └── state/                   # 原：D7 不动
├── engines/
│   ├── book_to_skill/           # 原：docling/OCR/pdftotext 路由
│   ├── web_collector/           # 🆕 nuwa 6路采集的领域化版（WebSearch+webReader）
│   ├── expert-mind-rubric.md    # 🆕 专家心智提炼（恢复 nuwa 人物DNA，三重验证）
│   ├── nuwa-validation.md       # 原：三重验证（S5 复用）
│   └── darwin-rubric.md         # 改：第9维加"专家忠实度"要求
└── examples/
    └── <某专家>/                 # 🆕 黄金参照（建议 karpathy-advisor）
```

### 3.3 生成的产物 skill 结构（专家顾问 skill）

```
<expert>-advisor/
├── SKILL.md                 # 入口(<4K)：专家心智摘要 + 查询协议 + 诚实边界
├── dag/                     # 知识 DAG（定理/方法/公式）—— 依据底盘（docling 保 LaTeX）
├── expert-mind/             # 🆕 专家心智（主体）
│   ├── mental-models.md     #   思维镜片（判断/直觉，三重验证过）
│   ├── decision-heuristics.md  # 决策启发式
│   ├── anti-patterns.md     #   反模式（专家反对什么、为什么）
│   └── index.md             #   心智导航
├── judgments/               # 🆕 紧耦合关联（核心枢纽）
│   └── judg-*.md            #   每条专家判断 → 挂支撑它的定理/方法节点ID
├── wiki/                    # 知识节点 + 导航
└── sources/                 # 来源 provenance（网采URL + 用户PDF）
```

### 3.4 数据流总览

```
专家名 + 种子材料(PDF/书/链接)
      ↓
[S1 采集·双通道]
   ├─ 网采通道: WebSearch+webReader, nuwa 6路(论文/访谈/博客/推文/他评/时间线)
   └─ 用户材料: docling(born-digital,保LaTeX) / OCR(扫描书) / pdftotext(fallback)
      ↓ raw corpus（每源打标 knowledge/mind/both）
[S2·双轨提取]
   ├─ 论文/教材(knowledge/both) ──▶ 知识 DAG 节点(定理/方法/公式, 带provenance)
   └─ 访谈/博客(mind/both)     ──▶ 专家心智候选(判断/直觉/反模式)
      ↓
[S3 合并]  DAG合并(contradicts人工确认) + 心智候选去重
[S4 导航]  知识导航 + 心智导航
      ↓
[S5·三步]  ← 核心
   S5a 领域镜片(现有三重验证)
   S5b 专家心智(nuwa人物DNA, 三重验证)
   S5c 🆕紧耦合融合: 每个专家判断 → 关联支撑它的定理/方法节点
      ↓
[S6 验证·fresh] [S7 组装] → darwin门(加专家忠实度硬门)
      ↓
专家顾问 skill
```

---

## 4. 数据结构与紧耦合建模（核心）

### 4.1 三层实体 + 连接关系

```
专家心智(expert-mind/)  ──grounded_in──▶  知识节点(dag/wiki/)   ← DKB 原生，不动
   ↑                                          ↑
   └──────── judgment(judgments/) ────────────┘
              ↑ 紧耦合的"枢纽"：一条专家判断 = 立场 + 推理 + 依据节点
```

知识节点 schema 完全继承 DKB（5 类型 def/thm/meth/exp/ins + 10 关系 + D7 provenance），**不动**。

### 4.2 专家心智元素 schema（`expert-mind/*.md`）

```yaml
---
id: mm-lecun-energy-based-worldview
type: mental_model            # mental_model | heuristic | anti_pattern
label: 能量模型世界观
statement: "智能 = 在能量函数上做优化/约束满足，而非自回归预测下一token"
verification:                 # nuwa 三重验证（S5b 跑）
  cross_scene: { pass: true, evidence: [JEPA架构, 反对LLM推理, LatentEBM] }
  generative: { pass: true, predicts: "对任何新架构先问能量/目标函数" }
  exclusive:  { pass: true, vs: "贝叶斯派靠先验、生成式派靠似然" }
grounded_in:                  # 紧耦合：这条心智挂到哪些定理/方法节点
  - thm-ebm-as-energy-minimization
  - meth-jepa-latent-predictive
confidence: high              # high | medium | low
provenance: { sources: [lecun-2022-jepa, lex-interview-2023] }
---
<展开：核心思想 / 跨场景证据 / 局限 / 支撑节点>
```

### 4.3 judgment schema——紧耦合的枢纽（`judgments/*.md`）

回答「专家怎么看 X」的载体：**一条判断 = 立场 + 推理链 + 依据节点**。

```yaml
---
id: judg-lecun-llm-cant-reason
trigger: "LLM 能做真正的推理吗 / 为什么 LLM 不会规划"
judgment: "不能。纯自回归续写缺乏世界模型，无法预测后果做规划"
reasoning: "推理 = 在抽象空间预测后果+规划路径；自回归只做token级概率续写，
           没有世界模型的 forward 模拟，故 shot-hole 在外推时暴露"
grounded_in:                  # 依据：挂到具体定理/方法节点
  - { node: thm-planning-needs-world-model, role: supports, quote: "..." }
  - { node: meth-jepa-latent-predictive,     role: supports, quote: "..." }
counter_evidence:             # 诚实：列反方
  - { node: exp-gpt4-planning-benchmarks, note: "CoT下部分规划任务可通过" }
confidence: high
provenance: { sources: [lex-interview-2023, ieee-spectrum-2022] }
---
```

### 4.4 紧耦合的「强度按验证分级」（防滥竽）

| 心智元素 | 三重验证 | 与知识的耦合要求 |
|----------|----------|------------------|
| 心智模型 (mental_model) | 3 重全过 | **必须** `grounded_in ≥1` 定理/方法节点（强耦合，有硬依据）|
| 启发式 (heuristic) | 1-2 重 | `grounded_in` 可选（可能只有经验依据，标注）|
| 反模式 (anti_pattern) | 排他性必过 | `grounded_in` 指向它反对的方法节点 |

**关键约束**：没有 `grounded_in` 依据的判断，**不能冒充心智模型**——这是"有依据"的硬闸，由 S6 验证 + darwin 门强制。纯口嗨/无定理支撑的观点只能降级为启发式或丢弃。

### 4.5 为什么用 judgment 作枢纽、而不在 DAG 里加跨层边

DKB 的 DAG 边是「知识↔知识」（定理 A 推出定理 B）。如果把「专家判断」也塞进 DAG 当节点，会污染纯知识图谱、query 时难剪枝。所以 judgment 作为**独立关联层**，通过 `grounded_in` 引用知识节点 ID——知识图谱保持干净，紧耦合关系单独可查、可验证。

---

## 5. Pipeline 契约

相对 DKB 的改动集中在 **S1（采集）** 和 **S5（心智）**，其余 stage 多是继承 + 小扩展。

### 5.1 S1 采集·双通道（新）+ 来源打标

```
专家名 + 种子材料
   ├─【通道A：网采】web_collector (nuwa 6路领域化, WebSearch+webReader)
   │     ①论文著作 ②长访谈 ③博客文章 ④社媒碎片 ⑤他者评论 ⑥观点时间线
   │     → 每条存 sources/，带 URL + 采集时间 provenance
   │
   └─【通道B：用户材料】book_to_skill 按格式路由
         born-digital PDF ─▶ docling (保LaTeX)
         扫描书/图片     ─▶ unlimited-ocr
         arxiv 论文      ─▶ ar5iv HTML (公式最准)
         纯文本          ─▶ pdftotext (fallback)
         ↓
   来源打标（关键）：每源标 value = knowledge | mind | both
      论文/教材→knowledge   访谈/博客/推文→mind   研究论文→both
```

`both`（如研究论文：既含方法也含作者动机/判断）两通道都喂——这是心智的隐藏富矿（作者为什么这么设计、对什么持怀疑）。

### 5.2 S2 双轨提取（改，并行 fan-out）

| 通道 | 输入 | 提取什么 | 输出 |
|------|------|----------|------|
| **S2-knowledge**（继承 DKB S2） | knowledge/both 源 | 定理/方法/公式（docling 保 LaTeX）| 知识 DAG 节点 |
| **S2-mind**（新） | mind/both 源 | 专家判断/直觉/反模式/决策启发式 | 心智候选（带 provenance）|

### 5.3 S5 三步（核心扩展）

原 DKB S5 只做领域镜片，现拆三步：

```
S5a 领域镜片(现有)  ─┐  从知识节点提炼「领域怎么思考」(三重验证)   ← 保留
                    │
S5b 专家心智(新)    ─┤  从心智候选提炼「这位专家怎么思考」(三重验证)
                    │   恢复 nuwa 人物DNA: 判断/直觉/反模式/启发式
                    │   加载 engines/expert-mind-rubric.md
                    │   → expert-mind/*.md
                    │
S5c 紧耦合融合(新)  ─┘  对每个心智模型/判断，找支撑它的知识节点
                        建立 judgment(立场+推理+grounded_in 依据节点)
                        硬闸: 3重过的心智模型必须 grounded_in≥1，否则降级
                        → judgments/*.md
```

- **S5a 与 S5b 可并行**（独立输入）；**S5c 依赖两者**（要心智候选 + 知识节点都在）

### 5.4 其余 stage 的增量

| Stage | 继承 DKB | 新增 |
|-------|----------|------|
| S3 合并 | 知识 DAG 合并（contradicts 人工确认）| 心智候选去重（同判断多次出现→加强证据）|
| S4 导航 | 知识 index/overview/log | `expert-mind/index` |
| S6 验证 | 知识 DAG 校验（fresh subagent）| **紧耦合校验**：grounded_in 节点存在且语义匹配、无孤儿判断、judgment 忠实专家（非编造）|
| S7 组装 | SKILL.md 框架 | 顶部放专家心智摘要 + 查询协议加"判断+依据"模式 |
| darwin 门 | 9 维 | 第9维加 **专家忠实度** 硬门（见 §7）|

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
| **心智模式** | 加载专家心智镜片 + 匹配 judgment | 专家判断 + 推理链 + grounded_in 依据节点；无现成 judgment 则用镜片推断（**标注「推断·非原话」**）|
| **融合模式** ⭐ | 镜片理解→找 judgment→加载依据节点→综合 | 立场 + 理论依据 + 替代方案 + 局限，每论点挂 judgment ID + 节点 ID |

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
| 专家没明确说过的 | 标注「**推断·基于其心智镜片外推，非原话**」，不冒充原话 |
| 知识不足的子领域 | 明说「本库未覆盖此方向」，不补脑 |
| 专家观点演化的 | 标注「早期/近期」，不把旧观点改写成新观点 |
| judgment 互相矛盾 | 并列双方 + 各自适用边界，不编调和 |
| 落在明确反模式上 | 直接说「专家会反对，因为…」+ 反模式依据 |

---

## 7. 质量门扩展

紧耦合和专家忠实度是**致命问题**（不是扣分项），设为**硬门**——不过即判 <B+ 回滚。

| 类型 | 检查项 | 实现 |
|------|--------|------|
| **硬门①** 紧耦合完整性 | 每个 3 重过的心智模型必须有 `grounded_in ≥1` **真实存在**的节点 | S6 + `lint_d7.py` 扩展 |
| **硬门②** judgment 忠实度 | 每条 judgment 有真实 provenance（网采 URL / 用户材料），非模型编造 | S6 fresh subagent 抽查 |
| **硬门③** 无孤儿判断 | judgment 的 `grounded_in` 节点都在 DAG 里 | `lint_d7.py` 扩展 |
| darwin 第9维可审计支柱扩展 | judgment provenance 可追溯到具体来源 | darwin-rubric 改 |

棘轮机制继承 DKB（<B+ → git revert → 修单一维度 → 重评；连续 3 轮无改进 → 探索性重写）。

---

## 8. 测试策略（四层）

1. **程序化 lint**（`lint_d7.py` 扩展）：紧耦合完整性 / 孤儿判断 / grounded_in 节点存在性
2. **忠实度抽查**（fresh subagent）：抽 N 条 judgment，核对 provenance 是否真来自专家言论（防幻觉扮演）
3. **融合查询端到端**：K 个「专家怎么看 X」问题 → 融合模式 → 检查「有立场 + 有依据节点 + 有诚实边界」三要素
4. **黄金参照**：选 1 位专家人工策展 A 级参照（建议 **Karpathy**——材料丰富、心智鲜明、有 from-scratch/build-intuition 等强镜片），后续自动生成对标它（类比 DKB 的 conformal-prediction 88/A-）

---

## 9. MVP 里程碑（YAGNI，分阶段）

| 阶段 | 范围 | 目标 |
|------|------|------|
| **MVP** | 单专家 + 用户材料(PDF/书) + **最小网采**(论文/博客/访谈 3 路) + S2 双轨 + S5 三步 + 紧耦合硬门 + Karpathy 黄金参照 | 跑通「专家心智+知识融合」最小闭环，证明核心价值 |
| **V1** | nuwa 完整 6 路网采 + 来源打标自动化 + 多专家增量 ingest | 真正的"元 skill 生成多个专家 skill" |
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
2. **黄金参照专家**：Karpathy（待确认材料可得性 + 是否有足够定理级知识依据；备选 LeCun/Hinton）
3. **judgment 忠实度抽查样本数 N**：MVP 取值（建议 5-10）
4. **网采的反爬/合规**：Twitter/YouTube 等平台采集的可行性与合规边界
5. **`both` 来源的分流粒度**：研究论文里"方法"与"作者动机"如何精确切分喂两通道

---

## 12. 实现顺序建议（供 writing-plans 参考）

1. schema 层：`expert-mind.md` + `coupling.md`（judgment schema）
2. engines 层：`expert-mind-rubric.md`（从 nuwa 恢复人物 DNA）+ `web_collector/`（最小 3 路）
3. pipeline 层：ingest.md 改 S1 双通道 + S5 三步；query.md 加三模式路由
4. 质量层：`lint_d7.py` 扩展三硬门 + darwin-rubric 改
5. 黄金参照：人工策展 karpathy-advisor
6. MVP 端到端验证

---

_本设计文档基于 domain-knowledge-builder (DKB) + nuwa-skill + darwin-skill 三个现有 meta-skill 的融合，遵循 DKB 的 darwin 质量门与 D7 可控性传统。_
