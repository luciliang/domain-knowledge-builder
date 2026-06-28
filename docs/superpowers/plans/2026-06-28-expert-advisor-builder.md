# Expert Advisor Builder Implementation Plan (MVP)

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 domain-knowledge-builder 扩展为 expert-advisor-builder，能生成「专家心智(主体) + 知识依据(底盘) + 紧耦合关联(judgment)」的专家顾问 skill。

**Architecture:** 方案 A——以 DKB 现有 ingest pipeline 为骨架，新增专家心智维度（恢复 nuwa 人物 DNA）、紧耦合 judgment 层、网采通道。知识 DAG/darwin 门/D7 可控性继承不动。

**Tech Stack:** Markdown 契约文档（SKILL/schema/pipeline/engines）+ Python（lint_d7.py 扩展，pytest TDD）+ WebSearch/webReader（网采）+ docling/unlimited-OCR（提取）+ PyYAML（frontmatter 解析）。基于 spec `docs/superpowers/specs/2026-06-28-expert-advisor-builder-design.md`。

**TDD 适配：** 契约文档（.md）用「验收检查」（增强 grep：验结构非仅关键词）；Python 脚本用严格 TDD（pytest，RED-GREEN-COMMIT）。所有任务频繁 commit。

> **v2 修订（plan-review round 1）：** 补 Chunk 4 Task 4.3（lint 接入 main + frontmatter 解析，TDD）、修 Task 5.1 命令、增强各 task 验收 grep、明确 S6 判定表、注明 Hinton 首选理由、Task 3.1 拆 commit。

---

## File Structure

**新建文件：**
| 文件 | 职责 |
|------|------|
| `schema/source.md` | 来源打标 schema（§4.6）|
| `schema/expert-mind.md` | 专家心智元素 schema（§4.2）|
| `schema/coupling.md` | judgment schema（§4.3）|
| `engines/expert-mind-rubric.md` | 专家心智提炼（恢复 nuwa 人物 DNA）|
| `engines/web_collector.md` | 网采契约（MVP 3 路）|
| `pipeline/state/test_lint_d7.py` | lint 单元测试（pytest，TDD）|

**修改文件：**
| 文件 | 改动 |
|------|------|
| `schema/schema.md` | 加交叉引用 |
| `pipeline/ingest.md` | S1 双通道 + S2 双轨 + S5 三步 + S6 判定表 |
| `pipeline/query.md` | 三模式路由 + 推断落盘 + 诚实边界 |
| `pipeline/state/lint_d7.py` | 新增 2 check 函数 + frontmatter 解析 + 接入 main() |
| `engines/darwin-rubric.md` | 硬门①②③ + 专家忠实度 |
| `SKILL.md` | 触发词/路由 |

**黄金参照：** `examples/hinton-advisor/`（Hinton 首选，理由见 Task 5.1）

---

## Chunk 1: Schema 层（数据契约）

### Task 1.1: 创建 `schema/source.md`（来源打标）

**Files:** Create `schema/source.md`

- [ ] **Step 1: 写 schema 文档**（对照 spec §4.6）
  - frontmatter 字段表：`id`(src-<slug>)/`type`(paper|book|interview|blog|social|review|timeline)/`value`(knowledge|mind|both)/`channel`(web|user)/`url`(web必填)/`file`+`locator{page,section}`(user必填)/`collected_at`/`format`
  - `both` 切片契约：S2 worker 按段落语义切片，S3 去重
  - 字段必填矩阵（web→url；user→file+locator）
  - 两例 frontmatter（web interview + user pdf）

- [ ] **Step 2: 验收检查**

Run: `grep -nE "value:|channel:|locator:|both" schema/source.md`
Expected: value/channel/locator 字段 + both 切片契约均在。

- [ ] **Step 3: Commit**
```bash
git add schema/source.md && git commit -m "feat(schema): add source tagging schema (§4.6)"
```

### Task 1.2: 创建 `schema/expert-mind.md`（专家心智元素）

**Files:** Create `schema/expert-mind.md`

- [ ] **Step 1: 写 schema 文档**（对照 spec §4.2、§4.4）
  - 三 type：`mental_model`(3重全过,必 grounded_in≥1)/`heuristic`(1-2重,可选)/`anti_pattern`(排他性必过,role: refutes)
  - frontmatter：`id`(mm-/heur-/ap-)/`type`/`label`/`statement`/`status`(verified|demoted|inferred|contradicted)/`verification{cross_scene,generative,exclusive}`/`grounded_in`(对象数组)/`confidence`/`provenance`
  - grounded_in **对象数组**结构 `{node, role, quote}`，role ∈ supports|refutes|context
  - 降级规则引用（§4.4）
  - 完整示例（如 LeCun 能量世界观）

- [ ] **Step 2: 验收检查（增强：验结构非仅关键词）**

Run: `grep -nE "role: (supports|refutes|context)|node:|quote:|mental_model|heuristic|anti_pattern" schema/expert-mind.md`
Expected: 对象数组三字段（node/role/quote）+ role 枚举 + 三 type 均在。

人工对照：确认 anti_pattern 段写明 `role: refutes`（spec §4.4 表）。

- [ ] **Step 3: Commit**
```bash
git add schema/expert-mind.md && git commit -m "feat(schema): add expert-mind element schema (§4.2)"
```

### Task 1.3: 创建 `schema/coupling.md`（judgment 紧耦合枢纽）

**Files:** Create `schema/coupling.md`

- [ ] **Step 1: 写 schema 文档**（对照 spec §4.3、§4.4、§4.5）
  - judgment = 立场 + 推理 + 依据；**不独立验证**，`derived_from` 继承心智元素 verification
  - frontmatter：`id`(judg-)/`type: judgment`/`label`/`status`(verified|inferred|contradicted)/`trigger`/`derived_from`/`judgment`/`reasoning`/`grounded_in`(对象数组)/`counter_evidence`(role:context)/`confidence`/`provenance`
  - 边界澄清：judgment **无 demoted**、不参与 §4.4 降级；§4.4 优先于 §6.2 推断落盘
  - 独立成层不污染 DAG（§4.5）
  - 完整示例（judg-lecun-llm-cant-reason）

- [ ] **Step 2: 验收检查（增强：验边界澄清文字）**

Run: `grep -nE "derived_from|type: judgment|无 demoted|不参与 §4.4|优先于 §6.2|counter_evidence" schema/coupling.md`
Expected: derived_from + judgment 类型 + 两条 round-2 边界澄清 + counter_evidence 均在。

- [ ] **Step 3: Commit**
```bash
git add schema/coupling.md && git commit -m "feat(schema): add judgment coupling schema (§4.3)"
```

### Task 1.4: `schema/schema.md` 加交叉引用

**Files:** Modify `schema/schema.md`

- [ ] **Step 1: 顶部加「相关 schema」段**（指向 expert-mind.md/coupling.md/source.md，说明四者协作）

- [ ] **Step 2: 验收检查**
Run: `grep -nE "expert-mind.md|coupling.md|source.md" schema/schema.md`
Expected: 三交叉引用在。

- [ ] **Step 3: Commit**
```bash
git add schema/schema.md && git commit -m "docs(schema): cross-reference expert-mind/coupling/source"
```

---

## Chunk 2: Engines 层（方法论引擎）

### Task 2.1: 创建 `engines/expert-mind-rubric.md`

**Files:** Create `engines/expert-mind-rubric.md`

- [ ] **Step 1: 写引擎契约**
  - 职责：S5b 加载，从心智候选提炼专家心智
  - **恢复 nuwa 人物 DNA**：判断/直觉/反模式/决策启发式
  - 复用 `nuwa-validation.md` 三重验证，锚点从「领域镜片」调到「专家个人镜片」
  - 锚点迁移：「换领域不成立」→「这位专家特有」
  - 分级：3重→mental_model；1-2重→heuristic；排他性→anti_pattern
  - 与 S5c 衔接（输出喂 S5c 做 grounded_in 挂接）

- [ ] **Step 2: 验收检查**
Run: `grep -nE "人物 ?DNA|判断|反模式|三重验证|锚点" engines/expert-mind-rubric.md`
Expected: 人物 DNA + 三重验证 + 锚点迁移均在。

- [ ] **Step 3: Commit**
```bash
git add engines/expert-mind-rubric.md && git commit -m "feat(engines): add expert-mind rubric (recover nuwa persona DNA)"
```

### Task 2.2: 创建 `engines/web_collector.md`

**Files:** Create `engines/web_collector.md`

- [ ] **Step 1: 写网采契约**
  - MVP 3 路：①论文(WebSearch scholar/arxiv)②访谈(webReader transcript)③博客(WebSearch+webReader)
  - 每路 → `sources/src-*.md`(channel:web, url, §4.6)
  - provenance：URL + collected_at（硬门② HTTP 可达）
  - 反爬 fallback：403/限流记录失败+标注，不阻塞
  - V1 扩展位：④社媒⑤他评⑥时间线（MVP 不实现）

- [ ] **Step 2: 验收检查**
Run: `grep -nE "论文|访谈|博客|src-|url|collected_at" engines/web_collector.md`
Expected: 3 路 + sources 打标 + provenance。

- [ ] **Step 3: Commit**
```bash
git add engines/web_collector.md && git commit -m "feat(engines): add web_collector contract (MVP 3 routes)"
```

---

## Chunk 3: Pipeline 层（工作流契约）

### Task 3.1: 改 `pipeline/ingest.md`（S1 双通道 + S2 双轨 + S5 三步 + S6 判定表）

**Files:** Modify `pipeline/ingest.md`

> **commit 粒度**：ingest.md 改动大但高度耦合，拆 2 个 commit（S1+S2 / S5+S3-S7增量）。

- [ ] **Step 1: 加 S1 双通道**（网采引用 web_collector.md；用户材料引用 book_to_skill/ 路由 docling/OCR/pdftotext/ar5iv；每源 sources/src-*.md 引用 schema/source.md 打标）

- [ ] **Step 2: 加 S2 双轨**（S2-knowledge 继承 + S2-mind 新；both 源按段落语义切片引用 schema/source.md）

- [ ] **Step 3: Commit（S1+S2）**
```bash
git add pipeline/ingest.md && git commit -m "feat(pipeline): S1 dual-channel + S2 dual-track"
```

- [ ] **Step 4: 改 S5 拆三步**（S5a 领域镜片/S5b 专家心智加载 expert-mind-rubric.md/S5c 紧耦合建 judgment+§4.4降级；S5a/S5b 独立 subagent 并行，**S5c 依赖两者 + S3 合并完成后启动**）

- [ ] **Step 5: 改 S3/S4/S6/S7 增量**（S3 心智去重；S4 expert-mind/index；S7 专家心智摘要）

- [ ] **Step 6: S6 段必须含三行判定表**（对照 spec §5.4）：
  - grounded_in **存在性** = lint 程序化（硬门③）
  - **语义匹配** = fresh subagent 抽查（硬门①）
  - **忠实度** = fresh subagent 抽查 provenance（硬门②）

- [ ] **Step 7: 验收检查**
Run: `grep -nE "S2-mind|S5a|S5b|S5c|双通道|judgment|存在性.*程序化|语义匹配.*抽查|忠实度.*抽查" pipeline/ingest.md`
Expected: S2-mind/S5a-c/双通道/judgment + S6 三行判定表均在。

- [ ] **Step 8: Commit（S5+增量）**
```bash
git add pipeline/ingest.md && git commit -m "feat(pipeline): S5 three-step + S6 coupling check decision table"
```

### Task 3.2: 改 `pipeline/query.md`（三模式路由 + 推断落盘）

**Files:** Modify `pipeline/query.md`

- [ ] **Step 1: 加意图路由**（spec §6.1：知识/心智/融合，模糊默认融合）

- [ ] **Step 2: 加三模式 + 推断落盘**（spec §6.2：融合=立场+依据+边界；推断构建期写 status:inferred / 运行期只读）

- [ ] **Step 3: 加诚实边界规则**（spec §6.4 表）

- [ ] **Step 4: 验收检查**
Run: `grep -nE "知识模式|心智模式|融合模式|status: inferred|诚实边界|推断.*非原话" pipeline/query.md`
Expected: 三模式 + 推断落盘 + 诚实边界均在。

- [ ] **Step 5: Commit**
```bash
git add pipeline/query.md && git commit -m "feat(pipeline): tri-mode query routing + inferred persistence"
```

### Task 3.3: 改 `SKILL.md`（触发词/路由）

**Files:** Modify `SKILL.md`

- [ ] **Step 1: 改 frontmatter + 何时用**（加「专家顾问」触发词；区分领域知识库 vs 专家顾问；路由专家视角问题→本扩展）

- [ ] **Step 2: 验收检查**
Run: `grep -nE "专家顾问|advisor|专家视角" SKILL.md`
Expected: 专家顾问触发词/路由在。

- [ ] **Step 3: Commit**
```bash
git add SKILL.md && git commit -m "feat(skill): add expert-advisor triggers/routing"
```

---

## Chunk 4: 质量层（lint 扩展 TDD + 接入 + darwin 门）

> 目标：lint_d7.py 扩展 2 check 函数（TDD）+ **frontmatter 解析并接入 main()**（TDD，round-1 review 补的关键 piece）+ darwin 门。

### Task 4.1: check_grounding_existence（硬门③，TDD）

**Files:** Create `pipeline/state/test_lint_d7.py`；Modify `pipeline/state/lint_d7.py`

- [ ] **Step 1: 写失败测试**
```python
# pipeline/state/test_lint_d7.py
import importlib.util
def _load_lint(path):
    spec = importlib.util.spec_from_file_location("lint_d7", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def test_check_grounding_existence_passes_when_node_exists():
    lint = _load_lint("pipeline/state/lint_d7.py")
    dag = {"nodes": [{"id": "thm-foo"}, {"id": "meth-bar"}]}
    judgments = [{"id": "judg-1", "grounded_in": [{"node": "thm-foo", "role": "supports"}]}]
    assert lint.check_grounding_existence(dag, judgments) == []

def test_check_grounding_existence_flags_orphan():
    lint = _load_lint("pipeline/state/lint_d7.py")
    dag = {"nodes": [{"id": "thm-foo"}]}
    judgments = [{"id": "judg-1", "grounded_in": [{"node": "thm-NONEXISTENT", "role": "supports"}]}]
    issues = lint.check_grounding_existence(dag, judgments)
    assert len(issues) == 1 and "thm-NONEXISTENT" in issues[0]
```

- [ ] **Step 2: 运行确认失败**
Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py::test_check_grounding_existence_flags_orphan -v`
Expected: FAIL（AttributeError: check_grounding_existence 不存在）。

- [ ] **Step 3: 实现**
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

- [ ] **Step 4: 运行确认通过**
Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py -v`
Expected: PASS（2 tests）。

- [ ] **Step 5: Commit**
```bash
git add pipeline/state/lint_d7.py pipeline/state/test_lint_d7.py
git commit -m "feat(lint): check_grounding_existence (hard gate ③, TDD)"
```

### Task 4.2: check_mind_element_grounding（硬门①，TDD）

**Files:** Modify `pipeline/state/lint_d7.py`、`pipeline/state/test_lint_d7.py`

- [ ] **Step 1: 写失败测试**
```python
def test_check_mental_model_requires_grounding():
    lint = _load_lint("pipeline/state/lint_d7.py")
    elements = [{"id": "mm-1", "type": "mental_model",
                 "verification": {"cross_scene":{"pass":True},"generative":{"pass":True},"exclusive":{"pass":True}},
                 "grounded_in": []}]
    assert any("mm-1" in i for i in lint.check_mind_element_grounding(elements))

def test_check_heuristic_grounding_optional():
    lint = _load_lint("pipeline/state/lint_d7.py")
    assert lint.check_mind_element_grounding([{"id": "heur-1", "type": "heuristic", "grounded_in": []}]) == []
```

- [ ] **Step 2: 运行确认失败**
Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py::test_check_mental_model_requires_grounding -v`
Expected: FAIL（函数不存在）。

- [ ] **Step 3: 实现**
```python
def check_mind_element_grounding(elements):
    """硬门①：3重过的 mental_model 必须 grounded_in ≥1（heuristic 可选）。
    注：anti_pattern 的 role:refutes 约束、judgment 的 derived_from 继承正确性
    由 fresh subagent 抽查兜底（硬门①②），lint 不程序化校验。"""
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

### Task 4.3: frontmatter 解析 + 接入 main()（TDD，round-1 关键补充）

> **为什么必须做**：Task 4.1/4.2 的函数输入是 Python dict，但真实数据是 `expert-mind/*.md` 的 YAML frontmatter。不解析+接入 main()，黄金参照过 lint 是假通过。

**Files:** Modify `pipeline/state/lint_d7.py`、`pipeline/state/test_lint_d7.py`

- [ ] **Step 1: 写失败测试（端到端）**
```python
import tempfile, json
from pathlib import Path

def test_load_mind_artifacts_parses_judgments_and_elements(tmp_path):
    lint = _load_lint("pipeline/state/lint_d7.py")
    em = tmp_path / "expert-mind"; em.mkdir()
    (em / "judgments.md").write_text(
        "---\nid: judg-1\ntype: judgment\ngrounded_in:\n  - {node: thm-bar, role: supports}\n---\nbody")
    (em / "mental-models.md").write_text(
        "---\nid: mm-1\ntype: mental_model\ngrounded_in: []\n---\nbody")
    art = lint.load_mind_artifacts(tmp_path)
    assert len(art["judgments"]) == 1 and art["judgments"][0]["id"] == "judg-1"
    assert len(art["elements"]) == 1 and art["elements"][0]["id"] == "mm-1"

def test_end_to_end_lint_flags_orphan_in_temp_skill(tmp_path):
    """端到端：构造 skill 目录，load + check 报孤儿"""
    lint = _load_lint("pipeline/state/lint_d7.py")
    dag_dir = tmp_path / "dag"; dag_dir.mkdir()
    (dag_dir / "dag-index.json").write_text(json.dumps({"nodes": [{"id": "thm-foo"}]}))
    em = tmp_path / "expert-mind"; em.mkdir()
    (em / "judgments.md").write_text(
        "---\nid: judg-1\ntype: judgment\ngrounded_in:\n  - {node: thm-bar, role: supports}\n---\nbody")
    art = lint.load_mind_artifacts(tmp_path)
    dag = json.loads((dag_dir / "dag-index.json").read_text())
    issues = lint.check_grounding_existence(dag, art["judgments"])
    assert any("thm-bar" in i for i in issues)
```

- [ ] **Step 2: 运行确认失败**
Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py::test_load_mind_artifacts_parses_judgments_and_elements -v`
Expected: FAIL（load_mind_artifacts 不存在）。

- [ ] **Step 3: 实现 load_mind_artifacts + 接入 main()**
```python
import re
try:
    import yaml
except ImportError:
    yaml = None  # 无 PyYAML 时 fallback，需 pip install pyyaml

def _parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m: return {}
    if yaml: return yaml.safe_load(m.group(1)) or {}
    return {}  # 无 yaml：返回空，调用方跳过该文件（并在 main 报警告）

def load_mind_artifacts(skill_root):
    """从 expert-mind/*.md 解析 judgments + mind elements 的 frontmatter。"""
    em = Path(skill_root) / "expert-mind"
    judgments, elements = [], []
    if not em.exists(): return {"judgments": [], "elements": []}
    for f in em.glob("*.md"):
        fm = _parse_frontmatter(f.read_text())
        if fm.get("type") == "judgment": judgments.append(fm)
        elif fm.get("type") in ("mental_model", "heuristic", "anti_pattern"): elements.append(fm)
    return {"judgments": judgments, "elements": elements}
```
在 `main()` 的 checks dict 加（保留现有 check_*）：
```python
dag_path = args.target_skill_root / "dag" / "dag-index.json"
dag = json.loads(dag_path.read_text()) if dag_path.exists() else {"nodes": []}
artifacts = load_mind_artifacts(args.target_skill_root)
checks["hard_gate_3_grounding_existence"] = check_grounding_existence(dag, artifacts["judgments"])
checks["hard_gate_1_mental_model_grounding"] = check_mind_element_grounding(artifacts["elements"])
```

- [ ] **Step 4: 运行确认通过**
Run: `cd pipeline/state && python3 -m pytest test_lint_d7.py -v`
Expected: PASS（6 tests）。

- [ ] **Step 5: 验收端到端 CLI**
Run: 构造临时 skill 目录后 `python3 lint_d7.py --target-skill-root <tmpdir>`
Expected: 输出含 thm-bar 孤儿报告。

- [ ] **Step 6: Commit**
```bash
git add pipeline/state/lint_d7.py pipeline/state/test_lint_d7.py
git commit -m "feat(lint): load_mind_artifacts + wire checks into main() (TDD)"
```

### Task 4.4: 改 `engines/darwin-rubric.md`（硬门①②③ + 专家忠实度）

**Files:** Modify `engines/darwin-rubric.md`

- [ ] **Step 1: 加三硬门段**（spec §7 表）
  - 硬门① 紧耦合完整性（fresh 抽查语义）
  - 硬门② judgment 忠实度（fresh 抽查 provenance，user 源需 locator 锚点；**抽查范围含 anti_pattern 的 role:refutes 约束 + judgment 的 derived_from 继承正确性**）
  - 硬门③ 无孤儿判断（lint 程序化，引用 Task 4.1/4.3）
  - 第 9 维可审计支柱：judgment provenance 可追溯

- [ ] **Step 2: 验收检查**
Run: `grep -nE "硬门①|紧耦合完整性|硬门②|忠实度|硬门③|孤儿|refutes|derived_from" engines/darwin-rubric.md`
Expected: 三硬门 + refutes/derived_from fresh 兜底说明均在。

- [ ] **Step 3: Commit**
```bash
git add engines/darwin-rubric.md && git commit -m "feat(darwin): hard gates ①②③ + expert fidelity (refutes/derived_from via fresh)"
```

---

## Chunk 5: 黄金参照 + MVP 端到端验证

### Task 5.1: 策展黄金参照 `examples/hinton-advisor/`

> **黄金参照首选 Hinton（非 spec §8 默认的 Karpathy）**，理由：Hinton 对反向传播/Boltzmann 机有定理级论述，知识 DAG 的 thm 节点充分，能稳定满足硬门①（mental_model 必须 grounded_in≥1）；Karpathy 偏工程直觉、定理节点偏少，作对照验证「heuristic 占比高的专家」情况。此选择与 spec §8 默认顺序相反，是为降低硬门①风险。

**Files:** Create `examples/hinton-advisor/`

- [ ] **Step 1: 人工策展**（按 spec §3.3 产物结构）
  - `dag/knowledge/`：5-10 知识节点（BP 算法/反传定理/Boltzmann 机/t-SNE/capsule，保 LaTeX）
  - `expert-mind/mental-models.md`：3-5 心智模型（分布式表示/深度优于宽度/判别 vs 生成）+ 启发式 + 反模式
  - `expert-mind/judgments.md`：5-8 judgment（每个 grounded_in 挂知识节点）
  - `sources/src-*.md`：3-5 来源
  - `SKILL.md`：入口（<4K）

- [ ] **Step 2: 跑 lint 验证硬门（命令已修正）**

Run: `cd examples/hinton-advisor && python3 ../../pipeline/state/lint_d7.py --target-skill-root .`
Expected: 硬门③ 0 孤儿、硬门① mental_model 都有 grounded_in（main 现已接入，Task 4.3）。

- [ ] **Step 3: Commit**
```bash
git add examples/hinton-advisor/ && git commit -m "feat(examples): add hinton-advisor golden reference"
```

### Task 5.2: MVP 端到端验证（四层测试）

**Files:** Create `examples/hinton-advisor/validation-report.md`

- [ ] **Step 1: 跑四层测试**
  1. 程序化 lint（Task 4.1/4.2/4.3）：记录 grounded_in 存在性 + mental_model 依据通过
  2. 忠实度 + 语义抽查（fresh subagent/人工）：抽 5-8 judgment 核对 provenance + 语义匹配 + anti_pattern refutes + derived_from 继承
  3. 融合查询端到端：3-5 个「Hinton 怎么看 X」问题，验「立场+依据节点+诚实边界」三要素
  4. darwin 评分：人工/fresh subagent 对照 darwin-rubric.md 9 维打分，确认 ≥B+

- [ ] **Step 2: 写 validation-report.md**（四层结果 + darwin 分数 + 已知不足）

- [ ] **Step 3: Commit**
```bash
git add examples/hinton-advisor/validation-report.md
git commit -m "test(examples): hinton-advisor MVP end-to-end validation"
```

---

## 完成标准（Definition of Done）

- [ ] Chunk 1-4 所有 schema/engines/pipeline/质量文件创建/修改完毕，验收检查通过
- [ ] `lint_d7.py` 新增 2 check 函数 + load_mind_artifacts + 接入 main()，pytest 全绿（≥6 tests，含端到端）
- [ ] hinton-advisor 黄金参照策展完成，`lint_d7.py --target-skill-root .` 过三硬门（真过，非假通过）
- [ ] 四层测试记录在 validation-report.md，darwin ≥B+
- [ ] 全程频繁 commit（每 task 一 commit，ingest.md 拆 2 commit）

## 后续（非 MVP，V1/V2）

- V1：nuwa 完整 6 路网采 + 来源打标自动化 + 多专家增量
- V2：忠实度测试自动化 + 观点演化追踪 + 跨专家交叉验证

---

_本计划 v2 基于 spec v3 + plan-review round 1 反馈。Python 部分严格 TDD；契约文档用增强 grep 验收（验结构非仅关键词）。_
