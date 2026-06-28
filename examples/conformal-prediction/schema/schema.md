# Schema — 领域知识库知识提取规范

> 本文件是 LLM 维护知识库时遵循的规则。LLM 负责所有 bookkeeping，人类只做质量审核。

## 1. 知识节点类型

每篇来源提取的知识分为 5 种类型：

| type | 含义 | 粒度 | 文件路径 |
|------|------|------|---------|
| `definition` | 核心概念的精确定义 | 段落级（500-1000 tokens） | `wiki/knowledge/def-<slug>.md` |
| `theorem` | 定理、引理、命题及其条件 | 段落级（500-2000 tokens） | `wiki/knowledge/thm-<slug>.md` |
| `method` | 方法论、算法、流程 | 段落级（500-2000 tokens） | `wiki/knowledge/meth-<slug>.md` |
| `experiment` | 实验设置、结果、数值发现 | 段落级（500-1500 tokens） | `wiki/knowledge/exp-<slug>.md` |
| `insight` | 作者的判断、观点、推荐 | 段落级（500-1000 tokens） | `wiki/knowledge/ins-<slug>.md` |

## 2. 知识节点模板

每个 `wiki/knowledge/*.md` 文件必须包含以下 YAML frontmatter + 正文结构：

```markdown
---
id: <唯一ID，如 thm-glivenko-cantelli>
type: definition|theorem|method|experiment|insight
label: <人类可读名称>
source: <来源论文/书籍标识，如 vovk2005>
section: <原文中的章节位置，如 Section 3.2>
tokens: <估计token数>
created: <YYYY-MM-DD>
---

## 精确表述
<原文的精确表述，不 paraphrase。如果是公式，用 LaTeX 格式写。如果原文是英文，保留英文原文，可在下方补充中文说明。>

## 适用条件
<本定理/定义/方法成立的前提条件。如果有隐含条件也要写出。>

## 直觉解释
<用 1-3 句话解释为什么这个定理成立/这个方法有效。帮助理解，不是严格证明。>

## 与其他知识的关系
<列出与本文库中其他知识节点的关系。格式：→ 表示"推出/保证"，← 表示"被...保证"，↔ 表示"等价/对偶"。例：thm-gc → def-coverage ↔ def-validity>

## 来源引用
<原文中的具体位置：页码/章节/公式编号。便于人工追溯验证。>
```

## 3. DAG 关系类型

`dag/dag-index.json` 中的边（edges）使用以下关系类型：

| relation | 含义 | 方向 | 示例 |
|----------|------|------|------|
| `guarantees` | A 成立则 B 成立（理论保证） | A → B | GC 定理 → coverage 一致性 |
| `evaluates` | B 是 A 的度量/评估方法 | A → B | coverage → ECE |
| `generalizes` | B 是 A 的推广形式 | A → B | marginal → conditional |
| `specializes` | B 是 A 的特例 | A → B | CP → split CP |
| `contradicts` | A 和 B 在某些条件下矛盾 | A ↔ B | t-dist MLE ↔ split CP 最优 |
| `does_not_guarantee` | A 不提供 B 的保证（弱于 contradicts，是"不保证"而非"矛盾"） | A → B | scalar uncertainty → conditional coverage |
| `extends` | B 在 A 基础上改进/扩展 | A → B | CP → adaptive CP |
| `depends_on` | 理解 B 必须先理解 A | A → B | ECE → coverage |
| `compares_with` | A 和 B 可对比（优劣各有场景） | A ↔ B | split CP vs weighted CP |
| `cites` | B 的结果引用了 A | A → B | Vovk 2005 → Shafer 2008 |
| `applies_to` | B 将 A 应用于具体场景 | A → B | CP theory → medical calibration |

## 4. dag-index.json 结构

```json
{
  "meta": {
    "domain": "统计校准与共形预测",
    "created": "YYYY-MM-DD",
    "last_updated": "YYYY-MM-DD",
    "total_nodes": 0,
    "total_edges": 0
  },
  "nodes": [
    {
      "id": "thm-glivenko-cantelli",
      "type": "theorem",
      "label": "Glivenko-Cantelli Theorem",
      "file": "wiki/knowledge/thm-glivenko-cantelli.md",
      "tokens": 1200,
      "source": "vovk2005",
      "created": "YYYY-MM-DD"
    }
  ],
  "edges": [
    {
      "id": "e-gc-coverage",
      "from": "thm-glivenko-cantelli",
      "to": "def-coverage",
      "relation": "guarantees",
      "desc": "GC 定理为经验覆盖率的一致收敛提供理论保证",
      "source": "vovk2005",
      "confidence": "high"
    }
  ]
}
```

**confidence 字段**：`high`（原文明确表述）、`medium`（推断但合理）、`low`（推测，需验证）。

## 5. 来源摘要模板

每篇来源文档生成 `wiki/sources/<source-slug>.md`：

```markdown
---
id: src-<source-slug>
type: paper|book|survey|thesis
title: <论文/书籍全名>
authors: <作者列表>
year: <年份>
venue: <期刊/会议/出版社>
nodes_extracted: [<本篇提取的所有知识节点ID>]
ingested: <YYYY-MM-DD>
---

## 核心贡献
<1-3 句话概括本篇的核心贡献>

## 提取的知识节点
| 节点ID | 类型 | 名称 |
|--------|------|------|

## 与其他来源的关系
<本篇与知识库中其他来源的关系：引用、推广、矛盾、补充>

## 未提取的内容
<本篇中有价值但未提取为知识节点的内容（原因：超出当前范围/待补充）>
```

## 6. Ingest 工作流

当用户说 "ingest <文件路径>" 时：

### Step 1: 提取文本
- 用 `book-to-skill/scripts/extract.py --mode technical` 提取 PDF
- 输出 `full-text.txt` + `metadata.json`

### Step 2: 结构化知识提取
- 读取 `full-text.txt` 和 `schema/schema.md`（本文件）
- 按"知识节点模板"逐个提取知识节点，写入 `wiki/knowledge/*.md`
- 同时输出 `extraction.json`（节点列表 + 关系列表）
- 约束：每个节点 500-2000 tokens，宁精勿滥
- 约束：定理表述必须是原文精确表述，不可 paraphrase
- 约束：每条关系必须有 confidence 标注

### Step 3: DAG 合并
- 读取现有 `dag/dag-index.json` + 新的 `extraction.json`
- 合并规则：
  - 新节点 → 追加到 nodes
  - 已有节点（同 ID）→ 比对内容：一致则跳过，不一致则标注冲突，通知人类
  - 新关系 → 追加到 edges
  - 冲突关系（contradicts）→ 必须通知人类确认
- 输出更新后的 `dag/dag-index.json`
- 更新 `dag/dag-index.json` 的 `meta.last_updated` 和计数

### Step 4: 更新导航
- 更新 `wiki/index.md`：追加新节点到对应类别
- 更新 `wiki/sources/<source-slug>.md`：写入来源摘要
- 追加 `wiki/log.md`：记录本次 ingest 的摘要

### Step 5: 验证（可选，建议前几篇启用）
- spawn 独立子 agent 验证：
  - 定理表述是否与 full-text.txt 一致（随机抽查 3 个节点）
  - 关系方向是否正确
  - index.md 是否更新
- 输出 `validation-report.md`

## 7. Query 工作流（心智模型引导 DAG 遍历）

当用户提出一个问题时：

### Step 1: 问题分析
- 判断问题涉及哪些概念/知识类型
- 关系类型定义见 `schema/schema.md` §3（仅首次或遗忘时查阅；日常查询不读 schema.md，直接按 dag-index.json 的 edges 字段遍历）

### Step 2: DAG 遍历（读 dag-index.json）
- 从问题中的概念出发，沿关系边扩展
- 剪枝规则：控制在 3-5 个节点（每个 ~1K tokens → 总共 ~3-5K tokens）
- 优先级：theorem > definition > method > experiment > insight
- 如果有 contradicts 关系被命中 → 同时加载矛盾双方

### Step 3: 按需加载
- 只读取选中的 `wiki/knowledge/*.md` 文件
- 如果需要更多上下文，从 `wiki/sources/*.md` 补充

### Step 4: 专家视角综合分析
- 用心智模型 + 加载的知识 → 有理有据的回答
- 每个论点必须引用具体的知识节点 ID
- 如果知识不足以完整回答 → 明确说明缺什么

### Step 5: 可选——回答存档
- 如果回答有长期价值，写入 `wiki/syntheses/` 作为新知识

## 8. Lint 工作流

当用户说 "lint" 时：

- 检查孤立节点（没有任何 edge 的节点）
- 检查矛盾关系（contradicts 边）是否仍然成立
- 检查重复节点（不同 ID 但内容相同或高度相似）
- 检查缺失引用（knowledge/*.md 中引用了不存在的节点 ID）
- 检查来源覆盖（哪些来源被 ingest 但提取不完整）
- 输出 `lint-report.md`

## 9. 命名规范

- 节点 ID：`<type前缀>-<英文slug>`，如 `thm-glivenko-cantelli`、`def-coverage`、`meth-split-cp`
- type 前缀：`def`（定义）、`thm`（定理）、`meth`（方法）、`exp`（实验）、`ins`（洞察）
- 来源 ID：`src-<作者年分>`，如 `src-vovk2005`、`src-sadeghi2023`
- slug 用小写英文 + 连字符，不含空格和特殊字符
- 同一概念在不同来源中出现 → 用同一个节点 ID，在来源摘要中注明"已在 src-xxx 中提取"
