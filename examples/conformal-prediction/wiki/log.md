# MVP 构建日志

> 知识库领域：统计校准与共形预测
> 构建日期：2026-06-24

---

## 步骤 1：论文解析与知识提取（2026-06-24）

**任务：** 从三篇论文中提取结构化知识节点和关系。

**产出：**
- `extraction-p1.json` — angelopoulos2022（21 节点，72 边）
- `extraction-p3.json` — teneggi2025（9 节点，21 边）
- `extraction-p4.json` — min2026（20 节点，42 边）

**关键决策：**
- 采用 5 种节点类型（definition / method / theorem / insight / experiment）和 10 种关系类型的 schema
- 每个节点包含 id、type、label、file 路径、tokens 估算、来源论文标识
- 每条边包含 from/to 节点 ID、关系类型、描述文本、来源、置信度

---

## 步骤 2：DAG 合并与校准（2026-06-24）

**任务：** 合并三篇论文的提取结果，归一化关系类型，去重，校验完整性。

**产出：**
- `dag/dag-index.json` — 合并后的完整 DAG 索引（49 节点，135 边）
- `dag/merge-report.md` — 合并报告（统计、去重、归一化详情）

**关键决策与操作：**
1. **跨论文去重：** `def-conditional-coverage` 同时出现在 P1 和 P4，保留最完整版本
2. **关系归一化：** 54 条边的关系类型不在 schema 10 种类型中，全部成功映射：
   - `achieves` → `guarantees`（18 条涉及）
   - `extends_to` → `extends`
   - `is_a` / `specializes_to` / `special_case_of` → `specializes`
   - `contrasts_with` / `does_not_guarantee` → `contradicts`
   - `motivates` / `complements` / `informs` → `extends`
   - `evaluated_by` / `measured_by` → `evaluates`
   - 等等（详见 merge-report.md 完整映射表）
3. **完整性校验：**
   - 所有边引用的节点均存在（0 悬挂边）
   - 所有关系类型均符合 schema（0 未解析关系）
   - 0 重复边
   - 0 孤立节点

---

## 步骤 3：知识节点文件生成（2026-06-24）

**任务：** 为每个 DAG 节点生成独立的 Markdown 知识文件。

**产出：**
- `wiki/knowledge/` 目录下 49 个 `.md` 文件，对应 49 个节点
- 每个文件包含：节点 ID、类型、名称、来源论文、定义/描述、关键公式（如适用）、与其他节点的关系摘要

**关键决策：**
- 文件命名与节点 ID 保持一致，便于引用
- 每个文件独立可读，同时通过 DAG 索引提供导航

---

## 步骤 4：导航文件生成（2026-06-24）

**任务：** 生成知识库的入口导航文件。

**产出：**
- `wiki/index.md` — 按 5 种类型分类的节点索引表（节点 ID | 名称 | 一句话摘要）
- `wiki/overview.md` — 领域全局概览（背景、论文贡献、结构说明、统计数据）
- `wiki/log.md` — 本构建日志

**关键决策：**
- index.md 按类型分组，每组内按字母排序，便于按类别浏览
- overview.md 采用 4 段式结构，兼顾入门读者和有经验的研究者
- 摘要从 DAG 节点的 label 和关系描述中提炼，保持简洁准确

---

## 总结

| 步骤 | 产出 | 状态 |
|------|------|------|
| 1. 论文解析与提取 | extraction-p1/p3/p4.json | ✅ 完成 |
| 2. DAG 合并与校准 | dag-index.json + merge-report.md | ✅ 完成 |
| 3. 知识节点文件生成 | wiki/knowledge/*.md (49 files) | ✅ 完成 |
| 4. 导航文件生成 | wiki/index.md + overview.md + log.md | ✅ 完成 |

MVP 知识库构建完成。包含 49 个知识节点、135 条关系边、3 篇来源论文、9 条跨论文连接。

---

## 达尔文进化 Round 1（2026-06-25）

**评估基线：** 87/100（A级），基于达尔文.skill 2.0 的 9 维评分体系

**执行改进：**

### 改进 1：🔴 修复断裂引用 [优先级：高] ✅
- **问题：** `thm-split-cp-coverage` 引用了不存在的 `thm-full-cp-coverage`
- **方案：** 创建 `thm-full-cp-coverage` 节点（Full CP 是 Split CP 的理论推广，有独立价值）
- **新增边：** e-fullcp-splitcp (generalizes), e-fullcp-marginal (guarantees), e-fullcp-splitcp-def (specializes)

### 改进 2：🔴 修复关系类型精确性 ✅
- **问题：** e-unc-conditional 使用 `contradicts` 描述 meth-conformalize-uncertainty → def-conditional-coverage
- **修复：** 改为 `does_not_guarantee`（不保证而非矛盾，语义更精确）

### 改进 3：🟡 增加示例查询与加载效率提示 ✅
- **新增：** 3 个示例查询（概念查询、跨论文比较、实验设计），覆盖 3 种典型使用场景
- **新增：** 加载效率提示，明确不同操作的 token 预算
- **原则：** schema 细节仅在 Ingest/Lint 时加载，查询时不需要

### 统计变化
| 指标 | MVP (v1.0) | 进化后 (v1.1) |
|------|-----------|--------------|
| 节点数 | 49 | 50 |
| 边数 | 135 | 138 |
| 断裂引用 | 1 | 0 |
| 示例查询 | 0 | 3 |
| 加载效率指引 | 无 | 有 |
