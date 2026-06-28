# Lint 工作流 — 知识库质量自检

> 本文件是 domain-knowledge-builder meta-skill 的**质量维护流程**。
> 对应 schema §8。用户触发 `lint` 或 `lint --score` 时执行。

---

## 0. 何时触发

- 用户显式说 "lint" / "检查知识库" / "lint --score"
- pipeline S6 验证阶段（自动）
- schema 变化后（schema §13 强制重评）

---

## 1. 结构检查（继承自 CP，确定性）

### 1.1 图完整性（程序化校验）
```python
# 伪代码
for edge in dag['edges']:
    assert edge['from'] in node_ids, f"断裂 from: {edge}"
    assert edge['to'] in node_ids, f"断裂 to: {edge}"
assert len(set(node['id'] for node in dag['nodes'])) == len(dag['nodes']), "重复 node ID"
assert len(set(edge['id'] for edge in dag['edges'])) == len(dag['edges']), "重复 edge ID"
# 孤立节点
for node in dag['nodes']:
    has_edge = any(node['id'] in (e['from'], e['to']) for e in dag['edges'])
    if not has_edge: report(f"孤立节点: {node['id']}")
```

### 1.2 meta 计数漂移（v1.1.0 新增，CP 教训）
- `meta.total_nodes` == 实际 nodes 数？
- `meta.total_edges` == 实际 edges 数？
- `meta.sources[].nodes/edges` == 按 source 聚合的实际数？
- 不一致 → 警告（非 error，但黄金基线必须修复）

### 1.3 内容检查
- 孤立节点（无 edge）
- 矛盾关系（contradicts 边）是否仍成立
- 重复节点（不同 ID 但内容相同/高度相似）
- 缺失引用（knowledge/*.md 引用不存在的节点 ID）
- 来源覆盖（哪些来源 ingest 但提取不完整）

---

## 2. Generator 合规检查（D7 新增，schema §12 四支柱）

### 2.1 可回滚（Reversible）
- `git log --oneline` 有 commit-per-stage？
- commit message 遵 `<stage>: <摘要>`？
- 缺失 → 警告（无法独立 revert stage）

### 2.2 可审计（Auditable）
- 抽查节点的 `source_span` 能否定位原文（grep 验证 start_line/end_line 范围内有该节点的关键术语）
- 新 ingest 节点（非 `[legacy]`）缺 generated_by_step / run_id / source_span → **error**
- run_id 与 `pipeline/state/run-manifest.json` 的 run_id 一致？

### 2.3 确定性（Deterministic）
- node ID 遵 schema §10（`<type>-<source-slug>-<canonical-term>`）？
- ❌ 时间戳命名 / 随机后缀 / 流水号 → error
- 增量 ingest 后无重复/冲突 ID？（同源重跑应幂等）

### 2.4 预检（Preflight）
- `pipeline/state/run-manifest.json` 有 S1 preflight 记录？
- docling 当时可用？（检查 run-manifest 的 preflight 字段）

### 2.5 路径确定性（防链接断裂，D7 关键）
扫描所有节点 .md 文件的路径引用：
- ❌ 绝对路径（`/Users/.../xxx.md`）→ error
- ❌ meta-skill-root-relative（`../../examples/...`）→ error
- ✅ 只允许 skill-root-relative（`wiki/knowledge/xxx.md`）或纯文本 node-ID 引用（`→ def-x`）
- 违规 → 拒绝 commit，报告具体文件 + 行号

---

## 2.6 紧耦合硬门检查（expert-advisor 扩展）

> 本节适用于 `expert-advisor-builder`（DKB 扩展分支）。在 D7 四支柱基础上，新增**三硬门中的程序化部分**。

### 2.6.1 硬门③：无孤儿判断（程序化校验）

**目标**：确保 judgment/心智元素的 `grounded_in.node` 都存在于 dag-index（无断裂引用）。

**检查项**：
- 扫描所有 judgment（`type: judgment`）和心智元素（`type: mental_model/heuristic/anti_pattern`）
- 校验其 `grounded_in` 引用的 `node` 字段是否都在 `dag/dag-index.json` 的 `nodes` 列表中
- 任一不存在 → **error**（硬门③违例）

**实现**：
```python
# pipeline/state/lint_d7.py
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

### 2.6.2 硬门①：mental_model 依据（程序化校验）

**目标**：确保 3 重全过的 mental_model 必须 `grounded_in ≥1`（存在性校验，语义匹配由 fresh subagent 抽查）。

**检查项**：
- 遍历所有心智元素，筛选 `type: mental_model` 且 `verification.{cross_scene,generative,exclusive}.pass` 都为 `true` 的元素
- 校验其 `grounded_in` 字段非空（至少存在 1 个依据节点）
- 任一违反 → **error**（硬门①存在性违例）

**语义匹配判定**：
- **不在 lint 范围**：需要理解节点内容与判断的语义关系
- 由 fresh subagent 抽查兜底（见 `engines/darwin-rubric.md` §8.2）
- 失败示例：判断"LLM 不能推理"挂靠节点"Transformer 架构"（语义不相关）

**实现**：
```python
# pipeline/state/lint_d7.py
def check_mind_element_grounding(elements):
    """硬门①：3重过的 mental_model 必须 grounded_in ≥1（语义匹配由 fresh subagent 抽查）。"""
    issues = []
    for e in elements:
        v = e.get("verification", {})
        all_pass = all(v.get(k, {}).get("pass") for k in ("cross_scene","generative","exclusive"))
        if e.get("type") == "mental_model" and all_pass and not e.get("grounded_in"):
            issues.append(f"{e['id']}: mental_model(3重全过) 缺 grounded_in 依据（硬门①）")
    return issues
```

### 2.6.3 数据加载：frontmatter 解析

**契约**：每个心智元素（judgment/mental_model/heuristic/anti_pattern）是一个独立的 `expert-mind/*.md` 文件，顶部裸 YAML frontmatter。

**实现**：
```python
# pipeline/state/lint_d7.py
def load_mind_artifacts(skill_root):
    """从 expert-mind/*.md 解析 judgments + mind elements 的 frontmatter。

    Returns:
        {"judgments": [...], "elements": [...]}
        judgments: type == "judgment" 的 frontmatter 列表
        elements:  type in ("mental_model", "heuristic", "anti_pattern") 的列表
    """
    em = Path(skill_root) / "expert-mind"
    if not em.exists():
        return {"judgments": [], "elements": []}
    judgments, elements = [], []
    for f in em.glob("*.md"):
        fm = _parse_frontmatter(f.read_text())
        t = fm.get("type")
        if t == "judgment":
            judgments.append(fm)
        elif t in ("mental_model", "heuristic", "anti_pattern"):
            elements.append(fm)
    return {"judgments": judgments, "elements": elements}
```

**frontmatter 解析**：
```python
def _parse_frontmatter(text):
    """解析 .md 文件的 YAML frontmatter，无 frontmatter 或无 PyYAML 时返回 {}。"""
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    if yaml:
        return yaml.safe_load(m.group(1)) or {}
    print("warning: PyYAML 未安装，frontmatter 解析返回空（请 pip install pyyaml）", file=sys.stderr)
    return {}
```

### 2.6.4 接入 main() 与 CLI

**CLI 扩展**：
```bash
# 挂进 checks dict
checks = {
    # ... D7 四支柱 ...
    "硬门③ grounded_in 节点存在 (Grounding Existence)": {
        "ok": len(grounding_issues) == 0,
        "issues": grounding_issues,
        "judgments_count": len(artifacts["judgments"]),
    },
    "硬门① mental_model 3重全过必 grounded_in": {
        "ok": len(mind_grounding_issues) == 0,
        "issues": mind_grounding_issues,
        "elements_count": len(artifacts["elements"]),
    },
}
```

**CLI 参数**：
```bash
python3 pipeline/state/lint_d7.py --target-skill-root <path-to-expert-advisor-skill>
```

### 2.6.5 完整三硬门引用

- **硬门①②（语义匹配 + judgment 忠实度）**：需要 fresh subagent 抽查，见 `engines/darwin-rubric.md` §8
- **硬门③（无孤儿判断）**：本节程序化校验，实现见 `pipeline/state/lint_d7.py:199-210`
- **判定方式差异**：存在性 = lint 程序化（快、确定）；语义匹配 + 忠实度 = fresh subagent 抽查（慢、需判断力）

### 2.6.6 已知盲区

- **provenance.sources 孤儿检查**：lint 不校验 `provenance.sources` 的 URL/引用是否存在（留给硬门② fresh subagent 抽查）
  - 未来增强：`check_provenance_sources_exist`（HTTP 可达性校验 + `sources/src-*.md` 的 `locator` 有效性）

---

## 3. darwin 评分（`lint --score` 时）

加载 `engines/darwin-rubric.md`，按 9 维评分：
- 第 9 维按被评 skill 类型选子类（query-skill / generator-skill）
- fresh-context 子 agent 评分（禁止自评）
- 输出到 `results.tsv` + `lint-report.md`

---

## 4. 输出

`lint-report.md`：
```markdown
# Lint Report — <domain> @ <date>

## 结构检查
- 断裂引用: 0 ✓
- 重复 ID: 0 ✓
- 孤立节点: 0 ✓
- meta 计数: 一致 ✓

## Generator 合规（D7）
- 可回滚: ✓ commit-per-stage 完整
- 可审计: ✓ provenance 完整 (50/50 新节点)
- 确定性: ✓ node ID 合规
- 预检: ✓ docling preflight 有记录
- 路径确定性: ✓ 无绝对/meta-relative 路径

## darwin 评分（如 --score）
- 总分: 88/100 (A-)
- 维度明细: [9 维表]

## 待修复
- (无 / 列表)
```

---

_本工作流对应 schema §8 + §12 | 评分规范：engines/darwin-rubric.md_
