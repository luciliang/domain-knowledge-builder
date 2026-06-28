# Ingest 工作流 — 从专家材料到专家顾问 skill

> 本文件是 expert-advisor-builder meta-skill 的**核心生成流程**（由 domain-knowledge-builder 扩展而来）。
> 输入：专家名 + 种子材料（网采链接 + 用户 PDF/书）→ 输出：同时拥有「专家心智（主体）+ 知识依据（底盘）+ 紧耦合关联」的专家顾问 skill。
> 对应 schema §6 的 7 步流水线，按 D3 阶段性质拆分编排（确定性阶段 workflow / 交互阶段 subagent）。
>
> **相对 DKB 的扩展点**：S1 加双通道采集、S2 双轨提取、S5 拆三步（S5a 领域镜片 + S5b 专家心智 + S5c 紧耦合融合）。字段/方法论定义在 `schema/` 与 `engines/`，本文件只编排 pipeline 时序与契约，不重抄。

---

## 0. 前置检查（每次 ingest 必做）

### 0.1 专家 + 来源确认（交互，subagent）
- 与用户确认：专家名、领域、种子材料清单（网采链接 + 用户 PDF/书）、目标用途（研究/教学/工程参考）
- 检查是否已有同专家顾问 skill（`~/.pi/agent/skills/<expert>-advisor/` 存在？）→ 决定新建 or 增量

### 0.2 提取器 preflight（generator-skill 合规 §12.4）
```bash
cd <meta-skill-root>
python3 -m engines.book_to_skill --check
```
- 输出 per-format 提取器可用性报告
- docling 不可用（technical 模式必需，保 LaTeX）→ **报错 + 安装指引**，不静默退化
- unlimited-ocr 不可用（扫描书/图片专用）→ 警告但允许继续（仅 born-digital 论文时不影响）
- pdftotext 不可用（text 模式 fallback）→ 警告但允许继续（仅 text 论文）

### 0.3 初始化 git + run-manifest（D7 可回滚/可审计）
```bash
cd <target-skill-root>
[ -d .git ] || git init
git checkout -b ingest/<run_id>
```
- 生成本次 `run_id`（UUID）
- 创建 `pipeline/state/run-manifest.json`（空 stages 数组）
- 每个 stage 完成后 append 记录 + `git commit`

---

## 1. 7 步流水线总览

```
┌─────────────────────────────────────────────────────────────┐
│  确定性阶段（workflow JS fan-out）                            │
│                                                              │
│  S1 双通道 ──┬──▶ S2-knowledge_Pn ──┐  （value 打标分流）   │
│  网采+用户   ├──▶ S2-mind_Pn ────────┤                      │
│              └──▶ ... ──────────────┼──▶ S3 合并（交互）    │
└──────────────────────────────────────┼──────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────┐
│  交互/判断阶段（subagent chain）                              │
│                                                              │
│  S3 合并 ──▶ S4 导航 ─┬─▶ S5a 领域镜片 ──┐                   │
│  (人工确认            └─▶ S5b 专家心智 ──┼─▶ S5c 融合        │
│   contradicts)              （可并行）     │  (依赖S5a/b+S3) │
│                                            ▼                 │
│                                  S6 验证 ──▶ S7 组装         │
│                                (fresh-context                │
│                                 独立评分 + lint)             │
└──────────────────────────────────────────────────────────────┘
```

**阶段性质拆分理由（D3）**：
- S1/S2×N/S4 是确定性/可并行的 → `workflow`（JS fan-out，高效）
- S3 合并遇 contradicts/does_not_guarantee 边必须人工确认 → `subagent`（可暂停 checkpoint）
- S5a/S5b 是两个独立 subagent（上下文不同，可并行）；S5c 依赖两者 + S3 完成 → 必须**串行**在 S3 之后
- S6 验证/S7 组装需要判断力 → `subagent`

---

## S1. 双通道采集（workflow，确定性）

**目标**：从两条通道采集专家材料，每源存 `sources/src-*.md`（带 `value` 打标，决定 S2 分流），并提取文本供 S2 双轨使用。

**两通道并行**：

### 通道 A：网采（`engines/web_collector.md`）
- MVP 3 路：① 论文著作 ② 长访谈 ③ 博客文章（V1 补全 nuwa 6 路）
- 工具：WebSearch + webReader（`mcp__web_reader`）
- 每源存 `sources/src-*.md`（`channel: web` + `url`，**硬门② 可 HTTP 验证**）

### 通道 B：用户材料（`engines/book_to_skill/` 按格式路由）
```bash
python3 -m engines.book_to_skill raw/user/ --mode technical --install-missing ask
# 按格式路由（docling 保 LaTeX 优先）：
#   born-digital PDF ─▶ docling（保 LaTeX，technical 模式）
#   arxiv 论文      ─▶ ar5iv HTML（公式最准）
#   扫描书/图片     ─▶ unlimited-ocr（无文本层专用，不替代 docling）
#   纯文本          ─▶ pdftotext（fallback）
```
- 每源存 `sources/src-*.md`（`channel: user` + `file` + `locator: {page, section}`，**硬门② 核对依据**）

### 来源打标（S1→S2 的核心契约）
- 字段定义见 `schema/source.md` §1-2，本文件不重抄
- **关键字段**：`value = knowledge | mind | both`（决定 S2 分流，见 `source.md` §2）
- `both` 源（如研究论文：方法+作者动机）在 S2 由 worker 按段落语义切片（`source.md` §3）

**REPL 探测（>50K tokens 必用，book-to-skill 实践）**：
- 大论文（如 Min 2026 的 157 页 ~67K tokens）禁止 `read(full_text.txt)` 全读
- 用 `grep -n -E "^(Chapter|Section|定理|Theorem)" full_text.txt | head` 定位章节
- 用 `sed -n '<start>,<end>p' full_text.txt` 按段读

**产出**：
- `sources/src-*.md`（每源一个，打标 `value`）
- `full-text.txt`（合并全文，带来源分隔符）
- `metadata.json`（每源 token 数/页数/格式）

**run-manifest 记录**：
```json
{"stage": "S1_collect", "status": "done", "commit": "<sha>", "artifacts": ["sources/","full-text.txt","metadata.json"]}
```

---

## S2. 双轨提取（workflow，并行 fan-out × N）

**目标**：按来源 `value` 打标分流为两条独立提取轨道，分别产出知识 DAG 节点与心智候选。

**双轨对照**：

| 通道 | 输入 | 提取什么 | 输出 |
|------|------|----------|------|
| **S2-knowledge**（继承 DKB S2）| `knowledge` 源 + `both` 源的知识切片 | 定理/方法/公式（docling 保 LaTeX）| 知识 DAG 节点（`extraction-<source>.json`）|
| **S2-mind**（新）| `mind` 源 + `both` 源的判断切片 | 专家判断/直觉/反模式/决策启发式 | 心智候选（带 provenance）|

**`both` 源切片**（契约见 `schema/source.md` §3）：
- worker 按**段落语义**切片：知识性段落（定理/方法/实验）→ S2-knowledge；判断性段落（作者主张/怀疑/动机）→ S2-mind
- 切片边界由 S2 worker 标注 `slice_type: knowledge | mind`，S3 合并时去重

**编排**（`pipeline/run-dag-pipeline.js` 的核心）：
- 为每个 source × 每个适用通道启动一个 worker（`parallel()` fan-out）
- 知识 worker 读 `schema/schema.md`（§2 节点模板 + §3 关系类型）；心智 worker 读 `schema/expert-mind.md` §1 字段定义

**知识 worker 任务契约**（继承 DKB S2）：
```
输入：schema/schema.md（§2 节点模板 + §3 关系类型）+ full-text.txt 中该源的知识切片
输出：extraction-<source>.json（nodes + edges）

约束：
- 定理表述必须原文精确（LaTeX 保留）
- 每节点 500-2000 tokens
- 节点 ID 遵 schema §10 Determinism：<type>-<source-slug>-<canonical-term>
- 必填 provenance（schema §11）：generated_by_step=S2, run_id=<本次>, source_span={file,start_line,end_line,page}
- 关系必须有 confidence（high/medium/low）
```

**心智 worker 任务契约**（新，S2-mind）：
```
输入：schema/expert-mind.md（字段定义，不含三重验证——验证在 S5b）+ 该源的判断切片
输出：mind-candidate-<source>.json（候选心智元素，无 verification）

约束：
- 候选类型：mental_model | heuristic | anti_pattern（expert-mind.md §2）
- 每候选附 provenance.sources 引用 src-*.md 的 id（忠实度依据，硬门②）
- 不在此步验证三重——S5b 跑验证
- 三重验证的「锚点」是专家个人镜片（这位专家特有，换人就不成立），见 engines/expert-mind-rubric.md
```

**跨源 ID 一致性**（继承 DKB schema §10）：
- 不同来源的同一概念 → 同一 node ID（如 P1/P3/P4 都谈 split CP → 都用 `thm-angelopoulos2022-split-cp-coverage` 或合并到主源 slug）
- worker 间不通信，依赖 schema §10 的命名规范保证幂等

**产出**（per source × track）：
- 知识：`extraction-<source>.json`（nodes + edges）
- 心智：`mind-candidate-<source>.json`（候选心智元素 + provenance）

---

## S3. 合并（subagent，交互式 checkpoint）

**目标**：把 N 个 extraction-<source>.json 合并成统一的 `dag/dag-index.json`；把 N 个 mind-candidate-<source>.json 去重为心智候选池供 S5b 提炼。

**为什么必须 subagent 非 workflow**：
- schema §6 Step 3 强制：`contradicts` / `does_not_guarantee` 边**必须人工确认**
- workflow fire-and-forget 无法暂停做 checkpoint
- subagent 可在遇冲突时 `contact_supervisor(reason: "need_decision")` 暂停

**知识 DAG 合并规则**（schema §6 Step 3，继承）：
1. 新节点 → 追加到 `dag-index.json.nodes`
2. 同 ID 节点 → token-level 比对：一致跳过（幂等成功），不一致标注冲突
3. 新关系 → 追加到 `edges`
4. `contradicts` / `does_not_guarantee` 关系 → **暂停，contact_supervisor 请用户确认**

**心智候选去重**（spec §5.4 新增）：
- 同一专家判断在多个来源出现（如访谈+博客都说「LLM 不能推理」）→ **合并为一条候选，多源 provenance 加强证据**
- 不同切片产生的同义候选去重（保留合并后的 provenance.sources 列表）
- 心智候选去重**不触发人工确认**（无 contradicts 边）——确认发生在 S5b 三重验证后

**产出**：
- `dag/dag-index.json`（含 meta.run_id）
- `dag/merge-report.md`（新增节点数/冲突数/关系数/人工确认记录）
- `mind-candidates.json`（去重后的心智候选池，供 S5b）

---

## S4. 导航文件更新（workflow，确定性）

**目标**：基于 dag-index.json + mind-candidates.json 生成知识导航与心智导航（spec §5.4 新增 `expert-mind/index`）。

**任务**（可 workflow 并行 4 个子任务）：
1. 生成 `wiki/index.md`：按节点类型分组（def/thm/meth/exp/ins），每节点一行带链接 + 一句话摘要（纯导航层，不复制节点内容，spec §3.3）
2. 追加 `wiki/log.md`：本次 ingest 摘要（日期/来源/新增节点数/总节点数）
3. 生成/更新 `wiki/overview.md`：领域全局概览（3-5 段，基于 dag-index 的 meta + sources）
4. 生成 `expert-mind/index.md`：心智导航（只引用心智元素 ID + judgment ID，**S5 完成后回填**；此处先建空骨架）

**产出**：3 个知识导航文件 + 1 个心智导航骨架。

---

## S5. 三步：领域镜片 + 专家心智 + 紧耦合融合（subagent，判断式）

**目标**：原 DKB 单步 S5 只做领域镜片，现拆三步。S5a/S5b 是两个**独立 subagent**（上下文不同），**可并行**；S5c 依赖两者，且必须**等待 S3 合并完成（含 contradicts 人工确认）后启动**——因为 S5c 要为心智判断挂 `grounded_in` 依据节点，节点必须先在 S3 合并后的 DAG 中存在（spec §5.3 时序澄清）。

```
S5a 领域镜片（独立 subagent）  ─┐ 从知识节点提炼「这个领域怎么思考」(三重验证)  ← 保留 DKB
                               │  加载 engines/nuwa-validation.md
                               │  → wiki/mental-models.md（领域镜片）
                               │
S5b 专家心智（独立 subagent）  ─┤ 从心智候选提炼「这位专家怎么思考」(三重验证)
                               │  恢复 nuwa 人物 DNA, 加载 engines/expert-mind-rubric.md
                               │  三重验证锚点 = 专家个人镜片（换人就不成立）
                               │  → expert-mind/mental-models.md
                               │
S5c 紧耦合融合（依赖 S5a/S5b + S3）┘ 对每个心智模型/判断，找支撑它的知识节点
                                   建立 judgment（立场+推理+grounded_in）
                                   执行降级规则（schema §4.4）
                                   → expert-mind/judgments.md
```

### S5a. 领域镜片（独立 subagent，保留 DKB）

**目标**：从所有 knowledge 节点提炼 3-7 个领域心智模型 + 5-10 条决策启发式。

**加载规范**：`engines/nuwa-validation.md`（领域化三重验证）

**流程**（nuwa-validation.md §6）：
1. 扫描所有 knowledge 节点，识别候选镜片（反复出现的思维框架）
2. 三重验证每个候选：
   - 跨场景复现（≥2 个子问题/来源）
   - 生成力（能推断对新问题的立场）
   - 领域排他性（本领域特有，换领域不成立）
3. 3 重全过 → 心智模型；过 1-2 重 → 降级为决策启发式；0 重 → 丢弃
4. 写 `wiki/mental-models.md`（领域镜片，与 DKB 兼容）

**约束**：
- 心智模型数量 3-7（太少浅，太多没提炼）
- 每模型附跨源证据（哪些节点支撑）
- 诚实边界（未覆盖子领域 + 单一来源结论 + 开放问题）

### S5b. 专家心智（独立 subagent，新）

**目标**：从 S3 去重后的心智候选池提炼专家个人心智模型/启发式/反模式，锚点从「领域镜片」迁移到「专家个人镜片」。

**加载规范**：`engines/expert-mind-rubric.md`（恢复 nuwa 人物 DNA：判断、直觉、反模式、决策启发式）

**三重验证锚点迁移**（spec §5.3）：
- 领域镜片（S5a）：领域共识，任何研究者都这么想
- 专家心智（S5b）：**这位专家特有**，换人就不成立（如 LeCun 的能量世界观非 ML 共识）
- 验证标准见 `expert-mind-rubric.md`，本文件不重抄

**流程**：
1. 读 `mind-candidates.json`（S3 去重后）
2. 三重验证每个候选（cross_scene/generative/exclusive，expert-mind-rubric.md）
3. 落盘 `verification` 对象（schema `expert-mind.md` §1）
4. 3 重全过 → mental_model；1-2 重 → heuristic；排他性必过 → anti_pattern
5. 写 `expert-mind/mental-models.md`

**约束**：
- `grounded_in` 此时**可能为空**（依赖知识节点的关联在 S5c 完成，因为节点需经 S3 合并）
- 每心智元素附 provenance.sources（引用 `src-*.md` 的 id）
- 不在此步建 judgment——S5c 做

### S5c. 紧耦合融合（依赖 S5a/S5b + S3 完成，subagent）

**启动前置**（spec §5.3 时序）：
- **必须等 S3 合并完成**（含 contradicts 人工确认）——节点已在 dag-index 中存在，才能挂 grounded_in
- S5a 与 S5b 都已完成

**目标**：对每个专家心智模型/判断，找支撑它的知识节点，建立 judgment（紧耦合枢纽），并执行降级规则。

**建 judgment**（schema `coupling.md` §1）：
- judgment = 立场 + 推理链 + `grounded_in` 依据节点
- 通过 `derived_from` 继承所属心智元素的 verification（不独立跑三重）
- 写 `expert-mind/judgments.md`

**降级规则**（schema `expert-mind.md` §4 引用 spec §4.4，S5c 执行）：

| 情况 | 处理 | 心智元素 status |
|------|------|----------------|
| 3 重全过，但 `grounded_in` **完全找不到**任何相关节点 | **丢弃**（纯口嗨，无任何知识锚点）| dropped（不入库）|
| 3 重全过，找到候选节点但 S6 判定**语义不匹配** | **降级为 heuristic**，保留原 verification + 标注降级原因 | demoted（`demote_reason: semantic_mismatch`）|
| 降级后的 heuristic | `grounded_in` 变可选，但 `provenance` 必须保留；不重跑验证 | demoted |

**边界澄清**（schema `coupling.md` §4，避免分叉）：
- 降级只作用于**心智元素**（S5c 在 mental-models.md 层），不作用于 judgment
- judgment 的 status 枚举 `verified | inferred | contradicted`（无 demoted），通过 `derived_from` 继承所属心智元素最终 status
- §4.4 降级/丢弃规则优先于 §6.2 推断落盘：无依据的推断判断**不落盘 inferred**

---

## S6. 验证（fresh-context subagent + lint，独立评分）

**目标**：独立验证生成结果，不看构建过程只看产物。继承 DKB 知识 DAG 校验 + 新增紧耦合校验（spec §5.4）。

**fresh-context 子 agent 任务**（继承 DKB 知识校验）：
1. 读 `dag/dag-index.json`，程序化校验：0 悬空引用 / 0 重复 ID / 0 孤立节点 / meta 计数一致
2. 随机抽 3 节点验证：定理表述 vs 原文（用 source_span 定位）、schema 合规、LaTeX 正确
3. 检查关系方向（from→to 语义正确）
4. 检查 `wiki/index.md` 与 dag-index 一致
5. 走一个测试查询，验证 Query 工作流能否找到答案
6. 输出 `validation-report.md`

**紧耦合校验判定表**（spec §5.4，三行不可压缩）：

| 检查 | 判定方式 | 对应硬门 |
|------|----------|----------|
| `grounded_in` 节点**存在性** | **lint 程序化**（`pipeline/state/lint_d7.py` 扫 dag-index，节点 ID 不存在即报）| 硬门③ 无孤儿判断 |
| `grounded_in` **语义匹配**（节点是否真支撑该判断）| **fresh subagent 抽查**（与忠实度合并为一次 fresh 校验，需判断力）| 硬门① 紧耦合完整性 |
| judgment **忠实度**（是否真来自专家，非编造）| **fresh subagent 抽查** provenance（网采 URL HTTP 可达 / 用户材料 `locator` 可定位到页码章节）| 硬门② |

> 即：存在性 = 程序化（快、确定，lint 扩展见 `pipeline/lint.md`）；语义匹配 + 忠实度 = fresh subagent 抽查（慢、需判断力，合并为一次 fresh 校验，MVP 抽 N=5-10 条）。

**D7 Provenance 校验**（schema §11，继承）：
- 所有新节点含 generated_by_step / run_id / source_span？
- run_id 与 run-manifest.json 一致？

---

## S7. SKILL.md 组装（subagent）

**目标**：组装最终的专家顾问 skill 入口文件（spec §5.4 顶部放专家心智摘要 + 查询协议加「判断+依据」模式）。

**结构**（<4K tokens，compaction 从末尾截断所以重要内容前置）：
1. YAML frontmatter（name=`<expert>-advisor`, description foreground 专家名 + 三模式查询语义）
2. **专家心智摘要**（<2K tokens，来自 S5b 的 `expert-mind/mental-models.md`，前置——专家心智是主体）
3. **查询协议**（三模式路由：知识/心智/融合，`pipeline/query.md` §6；融合模式 = 判断 + grounded_in 依据节点）
4. 核心领域镜片（来自 S5a 的 `wiki/mental-models.md`，作为知识底盘）
5. 知识节点索引表（从 dag-index 生成，按类型分组）
6. 术语映射（中英对照）
7. 诚实边界（已覆盖/未覆盖/争议 + 专家观点演化）

---

## 2. darwin 质量门（S7 之后）

触发 `engines/darwin-rubric.md` 的 9 维评分（第 9 维按 generator-skill 子类，schema §12 四支柱）。

**三硬门**（紧耦合 + 专家忠实度是致命问题，不过即判 <B+ 回滚；判定方式见 S6 三行表，spec §7）：
- **硬门① 紧耦合完整性**：3 重过的心智模型 `grounded_in ≥1` 节点，且语义匹配（S6 fresh subagent 抽查）
- **硬门② judgment 忠实度**：每条 judgment 有真实 provenance（S6 fresh subagent 抽查 URL/locator）
- **硬门③ 无孤儿判断**：judgment 的 `grounded_in` 节点都在 dag-index（S6 lint 程序化）
- darwin 第 9 维可审计支柱：judgment provenance 可追溯到具体来源（URL 或 file+locator）

**评分处置**：
- **≥ B+ (80)** 且三硬门全过 → 接受，`git merge ingest/<run_id>` 到 main，更新 CHANGELOG
- **< B+** 或任一硬门不过 → 棘轮机制：`git revert` 最后 stage，诊断低分维度/失败硬门，修复后重评
- **连续 3 轮无改进** → 提议探索性重写（征得用户同意）

**results.tsv 追加**：
```
<timestamp>  <commit>  <expert>  -  <score>  baseline  -  initial  full_test
```

---

## 3. 失败恢复（D7 Checkpoint）

某 stage 失败 → 读 `pipeline/state/run-manifest.json` 找最后 `status:done` 的 stage → 从下一个 stage 重跑，不从头来。

```bash
# 查看进度
cat pipeline/state/run-manifest.json | jq '.stages[] | {stage, status}'

# 从 S3 重跑（假设 S1/S2 done，S3 失败）
# （由 pipeline 脚本的 --resume <run_id> --from S3 参数支持）
```

---

## 4. 增量 ingest（已存在专家顾问 skill + 新材料）

与首次 ingest 的差异（服务"在世专家持续更新"）：
- S1 双通道只处理**新**材料（网采新链接 + 用户新 PDF）
- S2 双轨只提取**新**源的 knowledge/mind 切片
- S3 合并进**现有** dag-index.json + mind-candidates.json（不是新建）
  - 知识：schema §10 Determinism 保证旧概念用同 node ID，新材料若谈同概念幂等跳过
  - 心智：同判断再次出现 → provenance 加强证据；观点演化（前后矛盾）→ 标注 `status: contradicted`，保留时间线不编调和
- S5c 紧耦合融合需对新心智元素重跑降级规则；已有 judgment 若依据节点变化需重挂 grounded_in
- S4-S7 重新跑（导航/心智/验证/组装可能变化）

---

_本工作流对应 schema §6 | 编排脚本：pipeline/run-dag-pipeline.js | 质量门：engines/darwin-rubric.md | 三硬门判定见 S6 + spec §7_
