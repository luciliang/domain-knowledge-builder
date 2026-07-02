# Schema — Domain Knowledge Builder Meta-Skill 知识规范

> 本文件是 meta-skill 生成知识库时遵循的规则。它定义了**生成器**如何产出符合质量标准的领域知识库 skill。
> 继承自 CP 实例（`examples/conformal-prediction/schema/schema.md`）的 5 节点类型 + 10 关系类型 + 3 工作流，**新增 D7 可控性层**（§10 Determinism、§11 Provenance、§12 Generator 合规）。
> 生成的每个知识库 skill 必须满足本规范才能通过 darwin 质量门（≥B+ 80 分）。

---

## 相关 schema

本知识节点规范（schema.md）与以下三个 schema 文件协作完成知识库构建：

| schema 文件 | 核心内容 | 职责 |
|------------|---------|------|
| **schema.md**（本文件） | 5 类型知识节点（definition/theorem/method/experiment/insight）+ 10 种 DAG 关系 + D7 可控性层 | 知识底盘：定义知识节点结构、关系类型、命名规范、生成可控性 |
| **expert-mind.md** | 专家心智元素（mental_model/heuristic/anti_pattern）+ 三重验证 + grounded_in | 专家心智：定义领域专家的心智模型、启发式和反模式 |
| **coupling.md** | judgment 紧耦合枢纽 | 知识枢纽：用 judgment 关系将专家心智（expert-mind）紧耦合到知识节点 |
| **source.md** | 来源打标规范（sources/src-*.md）+ S1→S2 分流 | 来源追踪：定义来源文档的打标规范和提取流程 |

**四者协作关系**：source.md 负责来源打标和分流 → schema.md 定义知识节点和关系 → expert-mind.md 提炼专家心智元素 → coupling.md 用 judgment 关系将心智紧耦合到知识节点，形成「知识+心智」的完整体系。

---

## 0. 与 CP 实例 schema 的关系

| 项 | CP schema（query-skill） | 本 schema（meta-skill，generator） |
|----|-------------------------|------------------------------------|
| ①-⑨ 节点/关系/工作流 | 完整 | 完整继承 |
| 节点 frontmatter | 9 字段 | 9 字段 + 4 个 provenance 字段（§10） |
| 关系类型 | 10 种 | 10 种（一致） |
| 命名规范 | §9 | §9 + Determinism 强化（§10） |
| Lint | §8（结构检查） | §8 + §12 Generator 合规检查 |
| 生成可控性 | N/A（人工策展） | §10/§11/§12（checkpoint/rollback/provenance/determinism） |

**向后兼容**：CP 实例的节点（无 provenance 字段）在本 schema 下仍合法——这些字段对历史数据是 optional，对新 ingest 必填。

---

## 1. 知识节点类型

每篇来源提取的知识分为 5 种类型（继承自 CP，未变）：

| type | 含义 | 粒度 | 文件路径 |
|------|------|------|---------|
| `definition` | 核心概念的精确定义 | 段落级（500-1000 tokens） | `wiki/knowledge/def-<slug>.md` |
| `theorem` | 定理、引理、命题及其条件 | 段落级（500-2000 tokens） | `wiki/knowledge/thm-<slug>.md` |
| `method` | 方法论、算法、流程 | 段落级（500-2000 tokens） | `wiki/knowledge/meth-<slug>.md` |
| `experiment` | 实验设置、结果、数值发现 | 段落级（500-1500 tokens） | `wiki/knowledge/exp-<slug>.md` |
| `insight` | 作者的判断、观点、推荐 | 段落级（500-1000 tokens） | `wiki/knowledge/ins-<slug>.md` |

---

## 2. 知识节点模板（含 D7 Provenance 字段）

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
# === D7 Provenance 字段（新 ingest 必填，历史数据 optional）===
generated_by_step: S2|S3|S5      # 哪个 pipeline step 产出（S2 提取/S3 合并/S5 心智模型）
run_id: <UUID>                    # 构建 run 标识，可追溯到完整 pipeline 执行
source_span:                      # 原文定位，便于追溯验证
  file: <raw 文件名，如 p1-angelopoulos-2022.pdf>
  start_line: <起>
  end_line: <止>
  page: <页码或 Unknown>
---

## 精确表述
<原文的精确表述，不 paraphrase。如果是公式，用 LaTeX 格式写。>

## 适用条件
<本定理/定义/方法成立的前提条件。>

## 直觉解释
<用 1-3 句话解释为什么这个定理成立/这个方法有效。>

## 与其他知识的关系
<列出与本文库中其他知识节点的关系。格式：→ 推出，← 被保证，↔ 等价。>

## 来源引用
<原文中的具体位置：页码/章节/公式编号。>
```

---

## 3. DAG 关系类型

`dag/dag-index.json` 中的边（edges）使用以下关系类型（10 种，继承自 CP）：

| relation | 含义 | 方向 | 示例 |
|----------|------|------|------|
| `guarantees` | A 成立则 B 成立（理论保证） | A → B | GC 定理 → coverage 一致性 |
| `evaluates` | B 是 A 的度量/评估方法 | A → B | coverage → ECE |
| `generalizes` | B 是 A 的推广形式 | A → B | marginal → conditional |
| `specializes` | B 是 A 的特例 | A → B | CP → split CP |
| `contradicts` | A 和 B 在某些条件下矛盾 | A ↔ B | t-dist MLE ↔ split CP 最优 |
| `does_not_guarantee` | A 不提供 B 的保证（弱于 contradicts） | A → B | scalar uncertainty → conditional coverage |
| `extends` | B 在 A 基础上改进/扩展 | A → B | CP → adaptive CP |
| `depends_on` | 理解 B 必须先理解 A | A → B | ECE → coverage |
| `compares_with` | A 和 B 可对比（优劣各有场景） | A ↔ B | split CP vs weighted CP |
| `cites` | B 的结果引用了 A | A → B | Vovk 2005 → Shafer 2008 |
| `applies_to` | B 将 A 应用于具体场景 | A → B | CP theory → medical calibration |

> **边 ID 确定性规范（§10.2）**：每条边的 `id` 必须由公式 `edge_id = {from}|{relation}|{to}` 纯函数生成，而非手写 slug。详见 §10.2。

---

## 4. dag-index.json 结构

```json
{
  "meta": {
    "domain": "<领域名>",
    "created": "YYYY-MM-DD",
    "last_updated": "YYYY-MM-DD",
    "total_nodes": 0,
    "total_edges": 0,
    "sources": [
      {"id": "<source-id>", "paper": "<title>", "nodes": 0, "edges": 0}
    ],
    "run_id": "<本次构建的 UUID，追溯用>"
  },
  "nodes": [
    {
      "id": "thm-glivenko-cantelli",
      "type": "theorem",
      "label": "Glivenko-Cantelli Theorem",
      "file": "wiki/knowledge/thm-glivenko-cantelli.md",
      "tokens": 1200,
      "source": "vovk2005",
      "created": "YYYY-MM-DD",
      "generated_by_step": "S2",
      "run_id": "<UUID>",
      "source_span": {"file": "...", "start_line": 0, "end_line": 0, "page": "12"}
    }
  ],
  "edges": [
    {
      "id": "thm-glivenko-cantelli|guarantees|def-coverage",
      "from": "thm-glivenko-cantelli",
      "to": "def-coverage",
      "relation": "guarantees",
      "desc": "...",
      "source": "vovk2005",
      "confidence": "high"
    }
  ]
}
```

**confidence 字段**：`high`（原文明确表述）、`medium`（推断但合理）、`low`（推测，需验证）。

**edge `id` 字段（§10.2）**：必须由公式 `edge_id = {from}|{relation}|{to}` 生成（如上例），禁止手写 slug（如 `e-gc-coverage`）。`|` 不在节点 ID 字符集 `[a-z0-9-]` 内，故三元组与 id 双射、可 `split('|')` 反解析，增量合并按 id 去重即幂等。

---

## 5. 来源摘要模板

（继承自 CP，未变）每篇来源文档生成 `wiki/sources/<source-slug>.md`，含 id/type/title/authors/year/venue/nodes_extracted/ingested 字段 + 核心贡献/提取的知识节点/与其他来源的关系/未提取内容。

---

## 6. Ingest 工作流

### Step 1: 提取文本（preflight + 提取）
- **preflight**（generator-skill 合规 §12.4）：先跑 `python -m engines.book_to_skill --check` 确认 docling 等 hard 依赖可用；缺则报错指引安装，不静默失败
- 用 `python -m engines.book_to_skill <paths> --mode technical` 提取（technical 保留公式/表格）
- 输出 `full-text.txt` + `metadata.json`
- **run_id 生成**：本次 ingest 产生一个 UUID，记录到 `pipeline/state/run-manifest.json`

### Step 2: 结构化知识提取（并行，per-source）
- 读取 `full-text.txt` 和本 schema（§2 节点模板）
- 逐源并行提取知识节点（每个 source 一个 fan-out task）
- **Determinism**（§10）：节点 ID = `<type前缀>-<source-slug>-<canonical-term>`，canonical-term 经 LLM 抽取后确定性命名（同论文同概念再 ingest 产生同 ID）
- **Provenance**：每个节点写 generated_by_step=S2 + run_id + source_span（grep 定位原文行）
- 输出 `extraction-<source>.json`（节点+关系）+ `wiki/sources/<source>.md`

### Step 3: DAG 合并（交互式，subagent）
- 读取 schema §3 关系规范 + 各 extraction-<source>.json + 现有 dag-index.json
- 合并规则：新节点追加；同 ID 比对（一致跳过，不一致标注冲突）；新关系追加
- **contradicts/does_not_guarantee 边必须人工确认**（schema §6 Step 3 强制，故此步用 subagent 非 workflow）
- 输出更新后的 `dag/dag-index.json` + `merge-report.md`

### Step 4: 更新导航
- 更新 `wiki/index.md`（按类型分组，带链接+摘要）
- 追加 `wiki/log.md`（本次 ingest 摘要）
- 生成/更新 `wiki/overview.md`（领域概览）

### Step 5: 心智模型提炼（subagent）
- 加载 `engines/nuwa-validation.md`（领域化三重验证）
- 从所有 knowledge 节点提炼 3-7 个心智模型 + 5-10 条决策启发式
- 三重验证：跨场景复现/生成力/领域排他性
- 输出 `wiki/mental-models.md`

### Step 6: 验证（独立子 agent）
- fresh-context 验证：定理表述 vs 原文（抽查 3 节点）、关系方向、index 一致性、孤立节点、Query 工作流走查
- 输出 `validation-report.md`

### Step 7: SKILL.md 组装（subagent）
- 组装 frontmatter（name/description foreground 动词"构建"或领域名）+ 核心心智模型 + 查询协议 + 知识节点索引 + 术语映射 + 诚实边界
- SKILL.md <4K tokens（compaction 从末尾截断，重要内容前置）

---

## 7. Query 工作流（心智模型引导 DAG 遍历）

### Step 1: 问题分析
- 判断问题涉及哪些概念/知识类型
- 关系类型定义见本文件 §3（仅首次或遗忘时查阅；日常查询不读 schema.md，直接按 dag-index.json 的 edges 字段遍历）

### Step 2: DAG 遍历（读 dag-index.json）
- 从问题中的概念出发，沿关系边扩展
- 剪枝：3-5 个节点（每个 ~1K tokens → 总共 ~3-5K tokens）
- 优先级：theorem > definition > method > experiment > insight
- contradicts/does_not_guarantee 命中 → 同时加载双方

### Step 3: 按需加载
- 只读取选中的 `wiki/knowledge/*.md`，必要时从 `wiki/sources/*.md` 补充

### Step 4: 心智模型综合分析
- 用心智模型 + 加载的知识给出有理有据的回答
- 每个论点引用具体节点 ID；知识不足则明确说明

### Step 5: 可选——回答存档
- 有长期价值的回答写入 `wiki/syntheses/`

---

## 8. Lint 工作流

### 结构检查（继承自 CP）
- 孤立节点（无 edge 的节点）
- 矛盾关系（contradicts 边）是否仍成立
- 重复节点（不同 ID 但内容相同）
- 缺失引用（knowledge/*.md 引用不存在的节点 ID）
- 来源覆盖（哪些来源 ingest 但提取不完整）
- **meta 计数漂移**（v1.1.0 新增）：`dag-index.json` 的 `meta.sources[].nodes/edges` 和 `total_nodes/edges` 与实际统计是否一致；不一致则警告（CP v1.0→v1.1 的教训）

### Generator 合规检查（D7 新增，见 §12）
- 路径确定性：generated skill 的节点文件是否只用 skill-root-relative 路径（无绝对路径、无 meta-skill-root-relative 路径）
- Provenance 完整性：新 ingest 的节点是否全部含 generated_by_step/run_id/source_span
- Determinism：同源重跑是否产生同 node ID（§10）+ 边 ID 符公式（§10.2）
- 输出 `lint-report.md`

---

## 9. 命名规范

- 节点 ID：`<type前缀>-<source-slug>-<canonical-term>`（Determinism 强化，见 §10）
- type 前缀：`def`（定义）、`thm`（定理）、`meth`（方法）、`exp`（实验）、`ins`（洞察）
- 来源 ID：`src-<作者年分>`，如 `src-vovk2005`
- slug 用小写英文 + 连字符，不含空格和特殊字符
- 同一概念在不同来源中出现 → 用同一个节点 ID，在来源摘要中注明

---

## 10. Determinism 规范（D7 核心机制）

**目标**：同论文 + 同 schema 重跑产生完全相同的 node ID（幂等），避免重 ingest 导致 DAG 膨胀。

### 节点 ID 生成策略

```
node_id = <type前缀>-<source-slug>-<canonical-term>
```

- `<type前缀>`：由 LLM 判定节点类型（def/thm/meth/exp/ins），确定
- `<source-slug>`：来源论文的稳定 slug（如 `angelopoulos2022`），确定
- `<canonical-term>`：LLM 从节点内容抽取的规范术语（如 `glivenko-cantelli`、`split-cp-coverage`）

**canonical-term 的确定性保证**：
- 抽取 prompt 要求"用论文原文的最具区分度的命名实体"（如定理名、方法名），不用泛词
- 同一概念在不同 run 里应抽取出同一 canonical-term（论文原文是确定的）
- 若两次抽取不一致 → Lint 报告"determinism 违规"，人工裁定

### 冲突处理

- 同 ID 节点内容一致（token-level）→ 跳过（幂等成功）
- 同 ID 节点内容不一致 → 标注冲突，通知人类（不能自动覆盖）
- 新概念 → 新 ID，追加

### 不允许的命名

- ❌ 时间戳命名（`thm-20260627-001`）
- ❌ 随机后缀（`thm-foo-a3b2`）
- ❌ 流水号（`thm-001`、`thm-002`）

### 边 ID 确定性（§10.2）

**目标**：同一逻辑边（同 `from→relation→to`）重跑永远产生同一 `edge_id`，增量合并可按 id 去重，避免边层面 DAG 膨胀（补 §10 节点 ID 之外的边层面幂等）。

**公式**（纯函数、确定性）：

```
edge_id = {from}|{relation}|{to}
```

- `from`/`relation`/`to` 均属 `[a-z0-9-]`，内部无 `|` → 三元组与 `edge_id` 双射，可 `split('|')` 反解析
- 与节点 ID（`def-`/`thm-`/...）天然不冲突：边 ID 含 `|`，节点 ID 不含
- 借鉴 Hyper-Extract 的 `identifiers: {relation_id: '{source}|{type}|{target}'}` 机制

**幂等去重**：增量 ingest 时，新边的 `edge_id` 若已存在于 `dag-index.json` → 跳过（同逻辑边不重复入库）。

**Legacy 宽容**：现有 examples 的边 ID 是历史手写 slug（如 `e-gc-coverage`），不迁移；跑 lint 时带 `--legacy-ok` 宽容，新生成 skill 默认严格。详见 §12.3 Lint。

---

## 11. Provenance 规范（D7 核心机制）

**目标**：6 个月后能追溯任何节点到生成时刻的输入、step、原文位置。

### 必填字段（新 ingest）

每个节点 frontmatter 必须含：
- `generated_by_step`：S2（提取）/ S3（合并时新增的边节点）/ S5（心智模型衍生的 insight）
- `run_id`：本次构建的 UUID（同一次 pipeline 所有节点共享一个 run_id）
- `source_span`：原文定位 `{file, start_line, end_line, page}`

### run-manifest.json

每次 pipeline 执行产生 `pipeline/state/run-manifest.json`：

```json
{
  "run_id": "<UUID>",
  "started_at": "<ISO>",
  "domain": "<领域>",
  "sources": ["p1-xxx.pdf", "p2-yyy.pdf"],
  "stages": [
    {"stage": "S1_extract", "status": "done", "started_at": "...", "completed_at": "...", "commit": "<git-sha>", "artifacts": ["full-text.txt"]},
    {"stage": "S2_extract_p1", "status": "done", ...},
    ...
  ],
  "darwin_score": 88,
  "accepted": true
}
```

用途：失败恢复（从最后 done 的 stage 重跑）、审计、回滚（revert 某个 commit）。

### 历史数据兼容

CP 实例的 50 节点无 provenance 字段——合法，但 Lint 会标注 `[legacy]`，不视为缺陷。
新 ingest 的节点缺 provenance = Lint 报错。

---

## 12. Generator 合规（D7 核心机制，darwin 第 9 维 generator-skill 子类）

**对应 darwin-rubric.md §2.3 的四支柱**。本节定义每支柱的 Lint 检查。

### 12.1 可回滚（Reversible）
- 每个 pipeline stage 产出独立 git commit
- commit message 规范：`<stage>: <摘要>`（如 `S2-extract: p1-angelopoulos 22 nodes`）
- Lint 检查：`git log --oneline` 是否有 commit-per-stage；某 stage 退步可 `git revert <sha>` 独立回滚

### 12.2 可审计（Auditable）
- 每节点有完整 provenance（§11）
- 每次 darwin 评分记入 `results.tsv`
- Lint 检查：抽查节点的 source_span 是否能定位到原文（grep 验证）
- **硬门④**：judgment/心智元素的 `provenance.sources` 必须指向存在的 `src-*.md`（`check_provenance_sources_exist`，硬门③对称物）

### 12.3 确定性（Deterministic）
- node ID 遵循 §10 规范（lint 强制 `NODE_ID_RE` 三段格式 `<type>-<source>-<term>`，不符严格模式报 `bad_node_format`）
- **edge ID 遵循 §10.2 公式** `edge_id = {from}|{relation}|{to}`（手写 slug 不允许）
- Lint 检查：node ID 格式（`NODE_ID_RE`）+ 同源重跑一致性；边 ID 符公式 + 无重复 edge ID
- Legacy：`--legacy-ok` 时容忍历史 examples 的旧格式（短节点 id 计 `legacy_node_ids` + 旧 slug 边 ID 计 `legacy_edges`），新生成 skill 默认严格

### 12.4 预检（Preflight）
- pipeline S1 先跑 `python -m engines.book_to_skill --check` 确认依赖
- docling / pdftotext 不可用 → 明确报错 + 安装指引，**不静默退化**
- schema 版本不匹配 → 报错（避免用旧 schema 生成的节点污染新 schema 库）
- Lint 检查：preflight 是否在 run-manifest.json 里有记录

### 12.5 路径确定性（D7 防链接断裂）
- **generated skill 的节点文件只能用 skill-root-relative 路径**（如 `wiki/knowledge/xxx.md`，相对 skill 根目录）
- ❌ 禁止绝对路径（`/Users/.../xxx.md`）
- ❌ 禁止 meta-skill-root-relative 路径（`../../examples/...`）
- Lint 确定性检查：扫描所有节点 .md 的路径引用，违规则报错并拒绝 commit

---

## 13. 何时触发 darwin 评分（质量门）

- **初始化新领域知识库**：必跑（pipeline S6 之后），目标 ≥B+（80）才算生成成功
- **schema 变化**：必须重评（第 9 维对 schema 敏感）
- **用户触发 `lint --score`**：可选
- **棘轮机制**：darwin 评分 <B+ 则 `git revert` 最后 stage，不进 main

评分用 `engines/darwin-rubric.md` 的 9 维体系，第 9 维按 generator-skill 子类（§12 四支柱）评。

---

_本 schema 版本：meta-skill v0.1 | 继承自 CP schema v1.1.0 + D7 可控性层扩展 | 维护：domain-knowledge-builder meta-skill_
