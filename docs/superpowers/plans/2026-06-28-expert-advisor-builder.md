# Expert Advisor Builder Implementation Plan (MVP)

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 domain-knowledge-builder 扩展为 expert-advisor-builder，能生成「专家心智(主体) + 知识依据(底盘) + 紧耦合关联(judgment)」的专家顾问 skill。

**Architecture:** 方案 A——以 DKB 现有 ingest pipeline 为骨架，新增专家心智维度（恢复 nuwa 人物 DNA）、紧耦合 judgment 层、网采通道。知识 DAG/darwin 门/D7 可控性继承不动。

**Tech Stack:** Markdown 契约文档（SKILL/schema/pipeline/engines）+ Python（lint_d7.py 扩展）+ WebSearch/webReader（网采）+ docling/unlimited-OCR（提取）。基于 spec `docs/superpowers/specs/2026-06-28-expert-advisor-builder-design.md`。

**TDD 适配：** 契约文档（.md）用「验收检查」（grep 字段 / 对照 spec / 结构校验）；Python 脚本用严格 TDD（pytest）。所有任务频繁 commit。

---

## File Structure

**新建文件：**
| 文件 | 职责 |
|------|------|
| `schema/source.md` | 来源打标 schema（§4.6：id/type/value/channel/url/file/locator/collected_at/format）|
| `schema/expert-mind.md` | 专家心智元素 schema（§4.2：mental_model/heuristic/anti_pattern + verification + grounded_in）|
| `schema/coupling.md` | judgment schema（§4.3：紧耦合枢纽，derived_from 继承验证）|
| `engines/expert-mind-rubric.md` | 专家心智提炼契约（从 nuwa 恢复人物 DNA，三重验证）|
| `engines/web_collector.md` | 网采契约（MVP 3 路：论文/访谈/博客）|
| `pipeline/state/test_lint_d7.py` | lint_d7.py 扩展的单元测试（pytest，TDD）|

**修改文件：**
| 文件 | 改动 |
|------|------|
| `schema/schema.md` | 加交叉引用：指向 expert-mind.md / coupling.md / source.md |
| `pipeline/ingest.md` | S1 双通道 + 来源打标；S2 双轨；S5 拆三步（a/b/c）+ 降级规则引用 |
| `pipeline/query.md` | 意图路由三模式 + 推断落盘（构建期写/运行期只读）|
| `pipeline/state/lint_d7.py` | 扩展硬门③（grounded_in 存在性）+ 孤儿判断 + frontmatter 校验 |
| `engines/darwin-rubric.md` | 硬门①② + 专家忠实度（locator 锚点）|
| `SKILL.md` | 触发词/路由加「专家顾问」；区分领域知识库 vs 专家顾问 |

**黄金参照（最后）：**
| 文件 | 职责 |
|------|------|
| `examples/<expert>-advisor/` | 人工策展 A 级参照（Hinton 首选，定理依据充分）|

---

## Chunk 1: Schema 层（数据契约）

> 目标：建立三层实体的 schema 文档。所有下游任务依赖这些契约。

### Task 1.1: 创建 `schema/source.md`（来源打标）

**Files:**
- Create: `schema/source.md`

- [ ] **Step 1: 写 schema 文档**

内容要点（对照 spec §4.6）：
- frontmatter 字段定义表：`id`（必填，src-<slug>）/ `type`（paper|book|interview|blog|social|review|timeline）/ `value`（knowledge|mind|both）/ `channel`（web|user）/ `url`（web 源必填）/ `file`+`locator{page,section}`（user 源必填）/ `collected_at` / `format`
- `both` 源切片契约：S2 worker 按段落语义切片，知识性段落→knowledge 通道，判断性段落→mind 通道，S3 去重
- 字段必填矩阵（按 channel：web 需 url；user 需 file+locator）
- 一个完整 frontmatter 示例（web interview + user pdf 各一）

- [ ] **Step 2: 验收检查**

Run: `grep -E "^# |value:|channel:|locator:" schema/source.md`
Expected: 含来源打标、value/channel/locator 字段定义。

- [ ] **Step 3: Commit**

```bash
git add schema/source.md
git commit -m "feat(schema): add source tagging schema (§4.6)"
```

### Task 1.2: 创建 `schema/expert-mind.md`（专家心智元素）

**Files:**
- Create: `schema/expert-mind.md`

- [ ] **Step 1: 写 schema 文档**

内容要点（对照 spec §4.2、§4.4）：
- 三种 type：`mental_model`（3 重全过，必须 grounded_in ≥1）/ `heuristic`（1-2 重，grounded_in 可选）/ `anti_pattern`（排他性必过，grounded_in 用 role: refutes）
- frontmatter 字段：`id`（mm-/heur-/ap-）/ `type` / `label` / `statement` / `status`（verified|demoted|inferred|contradicted）/ `verification{cross_scene,generative,exclusive}` / `grounded_in`（对象数组 `{node, role, quote}`，role ∈ supports|refutes|context）/ `confidence` / `provenance{sources}`
- `grounded_in` 统一结构说明（与 judgment 一致）
- 降级规则引用（§4.4：无依据→dropped，语义不匹配→demoted）
- 完整 frontmatter 示例（mental_model 一例，如 LeCun 能量世界观）

- [ ] **Step 2: 验收检查**

Run: `grep -E "mental_model|heuristic|anti_pattern|grounded_in|verification" schema/expert-mind.md`
Expected: 三种 type + grounded_in 对象数组 + verification 三重均定义。

- [ ] **Step 3: Commit**

```bash
git add schema/expert-mind.md
git commit -m "feat(schema): add expert-mind element schema (§4.2)"
```

### Task 1.3: 创建 `schema/coupling.md`（judgment 紧耦合枢纽）

**Files:**
- Create: `schema/coupling.md`

- [ ] **Step 1: 写 schema 文档**

内容要点（对照 spec §4.3、§4.5）：
- judgment 定义：一条判断 = 立场 + 推理链 + 依据节点；**不独立跑三重验证**，通过 `derived_from` 继承心智元素 verification
- frontmatter 字段：`id`（judg-）/ `type: judgment`（固定）/ `label` / `status`（verified|inferred|contradicted，**无 demoted**）/ `trigger` / `derived_from`（心智元素 id）/ `judgment`（立场）/ `reasoning` / `grounded_in`（对象数组，同心智元素结构）/ `counter_evidence`（role: context）/ `confidence` / `provenance`
- 边界澄清：judgment 不参与 §4.4 降级；§4.4 优先于 §6.2 推断落盘
- 为什么独立成层不污染 DAG（§4.5）
- 完整 frontmatter 示例（如 judg-lecun-llm-cant-reason）

- [ ] **Step 2: 验收检查**

Run: `grep -E "derived_from|type: judgment|grounded_in|counter_evidence" schema/coupling.md`
Expected: derived_from 继承机制 + judgment 不参与降级说明都在。

- [ ] **Step 3: Commit**

```bash
git add schema/coupling.md
git commit -m "feat(schema): add judgment coupling schema (§4.3)"
```

### Task 1.4: `schema/schema.md` 加交叉引用

**Files:**
- Modify: `schema/schema.md`

- [ ] **Step 1: 在 schema.md 顶部加「相关 schema」段**

加一段指向 expert-mind.md / coupling.md / source.md 的引用，说明知识节点 schema（本文）+ 专家心智 schema + judgment schema + 来源 schema 四者协作。

- [ ] **Step 2: Commit**

```bash
git add schema/schema.md
git commit -m "docs(schema): cross-reference expert-mind/coupling/source schemas"
```

---

## Chunk 2: Engines 层（方法论引擎）

> 目标：专家心智提炼契约 + 网采契约。

### Task 2.1: 创建 `engines/expert-mind-rubric.md`（专家心智提炼）

**Files:**
- Create: `engines/expert-mind-rubric.md`

- [ ] **Step 1: 写引擎契约**

内容要点：
- 职责：S5b 加载本契约，从心智候选提炼专家心智模型
- **恢复 nuwa 人物 DNA**：判断/直觉/反模式/决策启发式（DKB 原 nuwa-validation.md 剔除的部分）
- 复用 `nuwa-validation.md` 三重验证（跨场景/生成力/排他性），但锚点从「领域镜片」调到「专家个人镜片」
- 锚点迁移说明：「换个人就不这么想」（nuwa 原版）vs 本 skill 用「这位专家特有的」
- 分级输出：3 重→mental_model；1-2 重→heuristic；排他性→anti_pattern
- 与 S5c 衔接：输出喂给 S5c 做 grounded_in 挂接

- [ ] **Step 2: 验收检查**

Run: `grep -E "人物DNA|判断|反模式|三重验证|锚点" engines/expert-mind-rubric.md`
Expected: 人物 DNA 恢复 + 三重验证 + 锚点迁移均在。

- [ ] **Step 3: Commit**

```bash
git add engines/expert-mind-rubric.md
git commit -m "feat(engines): add expert-mind rubric (recover nuwa persona DNA)"
```

### Task 2.2: 创建 `engines/web_collector.md`（网采契约）

**Files:**
- Create: `engines/web_collector.md`

- [ ] **Step 1: 写网采契约**

内容要点：
- MVP 3 路：①论文（WebSearch scholar/arxiv）②访谈（WebSearch + webReader 抓 transcript）③博客（WebSearch + webReader）
- 每路采集 → 存 `sources/src-*.md`（channel: web, url, §4.6 打标）
- provenance 要求：每条带 URL + collected_at（硬门② HTTP 可达验证）
- 反爬 fallback（开放问题）：遇 403/限流，记录失败 + 标注，不阻塞
- V1 扩展位：④社媒 ⑤他评 ⑥时间线（MVP 不实现，留接口）

- [ ] **Step 2: 验收检查**

Run: `grep -E "论文|访谈|博客|src-|url|collected_at" engines/web_collector.md`
Expected: 3 路 + sources 打标 + provenance。

- [ ] **Step 3: Commit**

```bash
git add engines/web_collector.md
git commit -m "feat(engines): add web_collector contract (MVP 3 routes)"
```

---

## Chunk 3: Pipeline 层（工作流契约）

> 目标：ingest/query/SKILL 改造，串起双通道 + 双轨 + 三步。

### Task 3.1: 改 `pipeline/ingest.md`（S1 双通道 + S2 双轨 + S5 三步）

**Files:**
- Modify: `pipeline/ingest.md`

- [ ] **Step 1: 改 S1 段——加双通道 + 来源打标**

在现有 S1（文本提取）前加 S1 双通道：
- 通道 A 网采（引用 engines/web_collector.md，MVP 3 路）
- 通道 B 用户材料（引用 engines/book_to_skill/ 路由：docling/OCR/pdftotext/ar5iv）
- 每源存 sources/src-*.md（引用 schema/source.md 打标）

- [ ] **Step 2: 改 S2 段——加双轨 + both 切片**

S2 拆为 S2-knowledge（继承现有）+ S2-mind（新，提取判断/直觉/反模式）。both 源按段落语义切片（引用 schema/source.md）。

- [ ] **Step 3: 改 S5 段——拆三步**

S5 拆为 S5a（领域镜片，现有）/ S5b（专家心智，加载 engines/expert-mind-rubric.md）/ S5c（紧耦合融合，建 judgment，执行 §4.4 降级）。注明 S5a/S5b 独立 subagent 并行，S5c 依赖两者 + S3 完成后启动。

- [ ] **Step 4: 改 S3/S4/S6/S7 增量**

按 spec §5.4 表：S3 加心智去重；S4 加 expert-mind/index；S6 加紧耦合校验（引用 §5.4 判定方式）；S7 加专家心智摘要 + 查询协议。

- [ ] **Step 5: 验收检查**

Run: `grep -nE "S1|S2-mind|S5a|S5b|S5c|双通道|judgment" pipeline/ingest.md`
Expected: S1 双通道、S2-mind、S5a/b/c 三步、judgment 均在。

- [ ] **Step 6: Commit**

```bash
git add pipeline/ingest.md
git commit -m "feat(pipeline): S1 dual-channel + S2 dual-track + S5 three-step"
```

### Task 3.2: 改 `pipeline/query.md`（三模式路由 + 推断落盘）

**Files:**
- Modify: `pipeline/query.md`

- [ ] **Step 1: 加意图路由（第 0 步）**

按 spec §6.1：知识模式 / 心智模式 / 融合模式（默认）。

- [ ] **Step 2: 加三模式流程 + 推断落盘**

按 spec §6.2：心智模式匹配 judgment；融合模式立场+依据+边界。推断落盘区分构建期（写 status: inferred）/ 运行期（只读）。

- [ ] **Step 3: 加诚实边界规则**

按 spec §6.4 表（推断非原话标注 / 未覆盖明说 / 观点演化 / 矛盾并列 / 反模式）。

- [ ] **Step 4: Commit**

```bash
git add pipeline/query.md
git commit -m "feat(pipeline): tri-mode query routing + inferred persistence"
```

### Task 3.3: 改 `SKILL.md`（触发词/路由）

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: 改 frontmatter description + 何时用**

加「专家顾问」触发词（「给 X 专家建顾问 skill」「蒸馏专家心智+知识」）。区分：领域知识库（纯知识）vs 专家顾问（心智+知识）。路由：纯领域问题→DKB 原模式；专家视角问题→本扩展。

- [ ] **Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat(skill): add expert-advisor triggers/routing"
```

---

## Chunk 4: 质量层（lint 扩展 TDD + darwin 门）

> 目标：lint_d7.py 扩展紧耦合硬门③（TDD），darwin 加硬门①②。

### Task 4.1: lint_d7.py 扩展——grounded_in 节点存在性（TDD）

**Files:**
- Create: `pipeline/state/test_lint_d7.py`
- Modify: `pipeline/state/lint_d7.py`

- [ ] **Step 1: 写失败测试**

```python
# pipeline/state/test_lint_d7.py
import json, os, tempfile
from pathlib import Path
import importlib.util

def _load_lint(path):
    spec = importlib.util.spec_from_file_location("lint_d7", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def test_check_grounding_existence_passes_when_node_exists():
    lint = _load_lint("pipeline/state/lint_d7.py")
    dag_index = {"nodes": [{"id": "thm-foo"}, {"id": "meth-bar"}]}
    judgments = [{"id": "judg-1", "grounded_in": [{"node": "thm-foo", "role": "supports"}]}]
    issues = lint.check_grounding_existence(dag_index, judgments)
    assert issues == []

def test_check_grounding_existence_flags_orphan():
    lint = _load_lint("pipeline/state/lint_d7.py")
    dag_index = {"nodes": [{"id": "thm-foo"}]}
    judgments = [{"id": "judg-1", "grounded_in": [{"node": "thm-NONEXISTENT", "role": "supports"}]}]
    issues = lint.check_grounding_existence(dag_index, judgments)
    assert len(issues) == 1
    assert "thm-NONEXISTENT" in issues[0]
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py::test_check_grounding_existence_flags_orphan -v`
Expected: FAIL（`check_grounding_existence` 不存在 → AttributeError）。

- [ ] **Step 3: 实现 check_grounding_existence**

在 `lint_d7.py` 加（保留现有函数，新增）：

```python
def check_grounding_existence(dag_index, judgments):
    """硬门③：judgment/心智元素的 grounded_in 节点必须存在于 DAG。"""
    valid_ids = {n["id"] for n in dag_index.get("nodes", [])}
    issues = []
    for j in judgments:
        for ref in j.get("grounded_in", []):
            node = ref.get("node") if isinstance(ref, dict) else ref
            if node not in valid_ids:
                issues.append(f"{j['id']}: grounded_in 指向不存在的节点 {node}")
    return issues
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py -v`
Expected: PASS（2 tests）。

- [ ] **Step 5: Commit**

```bash
git add pipeline/state/lint_d7.py pipeline/state/test_lint_d7.py
git commit -m "feat(lint): check_grounding_existence (hard gate ③, TDD)"
```

### Task 4.2: lint_d7.py 扩展——frontmatter 字段校验（TDD）

**Files:**
- Modify: `pipeline/state/lint_d7.py`
- Modify: `pipeline/state/test_lint_d7.py`

- [ ] **Step 1: 写失败测试**

```python
def test_check_mental_model_requires_grounding():
    lint = _load_lint("pipeline/state/lint_d7.py")
    # mental_model (3重过) 必须有 grounded_in
    elements = [{"id": "mm-1", "type": "mental_model",
                 "verification": {"cross_scene":{"pass":True},"generative":{"pass":True},"exclusive":{"pass":True}},
                 "grounded_in": []}]
    issues = lint.check_mind_element_grounding(elements)
    assert any("mm-1" in i for i in issues)

def test_check_heuristic_grounding_optional():
    lint = _load_lint("pipeline/state/lint_d7.py")
    elements = [{"id": "heur-1", "type": "heuristic", "grounded_in": []}]
    issues = lint.check_mind_element_grounding(elements)
    assert issues == []
```

- [ ] **Step 2: 运行确认失败**

Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py::test_check_mental_model_requires_grounding -v`
Expected: FAIL（函数不存在）。

- [ ] **Step 3: 实现 check_mind_element_grounding**

```python
def check_mind_element_grounding(elements):
    """硬门①：3重过的 mental_model 必须 grounded_in ≥1（heuristic 可选）。"""
    issues = []
    for e in elements:
        v = e.get("verification", {})
        all_pass = all(v.get(k, {}).get("pass") for k in ("cross_scene","generative","exclusive"))
        if e.get("type") == "mental_model" and all_pass and not e.get("grounded_in"):
            issues.append(f"{e['id']}: mental_model(3重全过) 缺 grounded_in 依据（硬门①）")
    return issues
```

- [ ] **Step 4: 运行确认通过**

Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py -v`
Expected: PASS（4 tests）。

- [ ] **Step 5: Commit**

```bash
git add pipeline/state/lint_d7.py pipeline/state/test_lint_d7.py
git commit -m "feat(lint): check_mind_element_grounding (hard gate ①, TDD)"
```

### Task 4.3: 改 `engines/darwin-rubric.md`（硬门①② + 专家忠实度）

**Files:**
- Modify: `engines/darwin-rubric.md`

- [ ] **Step 1: 加三硬门段**

按 spec §7 表：硬门①紧耦合完整性（fresh 抽查语义）/ 硬门②judgment 忠实度（fresh 抽查 provenance，user 源需 locator 锚点）/ 硬门③无孤儿判断（lint 程序化，引用 Task 4.1）。第 9 维可审计支柱扩展：judgment provenance 可追溯。

- [ ] **Step 2: Commit**

```bash
git add engines/darwin-rubric.md
git commit -m "feat(darwin): hard gates ①②③ + expert fidelity"
```

---

## Chunk 5: 黄金参照 + MVP 端到端验证

> 目标：策展一个 A 级专家参照，跑通四层测试。

### Task 5.1: 策展黄金参照 `examples/hinton-advisor/`（首选 Hinton，定理依据充分）

**Files:**
- Create: `examples/hinton-advisor/`（含 dag/ + expert-mind/ + judgments + sources/）

- [ ] **Step 1: 人工策展 Hinton 顾问 skill**

按产物结构（spec §3.3）策展：
- `dag/`：5-10 个知识节点（BP 算法、反传定理、Boltzmann 机、t-SNE、capsule 等，保留 LaTeX）
- `expert-mind/mental-models.md`：3-5 心智模型（如「分布式表示」「深度优于宽度」「判别式 vs 生成式」）+ 启发式 + 反模式
- `expert-mind/judgments.md`：5-8 judgment（每个 grounded_in 挂知识节点）
- `sources/src-*.md`：3-5 来源（论文 + 访谈）
- `SKILL.md`：入口（<4K）

> 若 Hinton 材料可得性不足，回退 Karpathy（允许 heuristic 占比高）。

- [ ] **Step 2: 跑 lint 验证硬门**

Run: `cd examples/hinton-advisor && python3 ../../pipeline/state/lint_d7.py .`（或按 lint 接口）
Expected: 硬门③ 0 孤儿、硬门① mental_model 都有 grounded_in。

- [ ] **Step 3: Commit**

```bash
git add examples/hinton-advisor/
git commit -m "feat(examples): add hinton-advisor golden reference"
```

### Task 5.2: MVP 端到端验证（四层测试）

**Files:**
- Create: `examples/hinton-advisor/validation-report.md`

- [ ] **Step 1: 跑四层测试并记录**

1. 程序化 lint（Task 4.1/4.2 函数）：记录 grounded_in 存在性 + mental_model 依据通过
2. 忠实度 + 语义抽查（fresh subagent 或人工）：抽 5-8 judgment，核对 provenance + 语义匹配
3. 融合查询端到端：3-5 个「Hinton 怎么看 X」问题，验证「立场 + 依据节点 + 诚实边界」三要素
4. darwin 评分：对 hinton-advisor 跑 9 维，确认 ≥B+

- [ ] **Step 2: 写 validation-report.md**

记录四层结果 + darwin 分数 + 已知不足。

- [ ] **Step 3: Commit**

```bash
git add examples/hinton-advisor/validation-report.md
git commit -m "test(examples): hinton-advisor MVP end-to-end validation"
```

---

## 完成标准（Definition of Done）

- [ ] Chunk 1-4 所有 schema/engines/pipeline/质量文件创建/修改完毕，验收检查通过
- [ ] `lint_d7.py` 扩展 2 个函数，pytest 全绿（≥4 tests）
- [ ] hinton-advisor 黄金参照策展完成，过三硬门
- [ ] 四层测试记录在 validation-report.md，darwin ≥B+
- [ ] 全程频繁 commit（每 task 一 commit）

## 后续（非 MVP，V1/V2）

- V1：nuwa 完整 6 路网采 + 来源打标自动化 + 多专家增量
- V2：忠实度测试自动化 + 观点演化追踪 + 跨专家交叉验证

---

_本计划基于 spec `docs/superpowers/specs/2026-06-28-expert-advisor-builder-design.md`。实现时遵循 DKB 现有模式（darwin 门 / D7 可控性 / 三重验证）。_
