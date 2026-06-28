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
