# CHANGELOG — 共形预测领域知识库 Skill

黄金基线版本：**v1.1.0**（50 节点 / 138 边 / Darwin 88 分 A-）
重评日期：2026-06-27（独立 fresh-context reviewer 9 维评分）

---

## [1.1.0] — 2026-06-25

### 修复
- **断裂引用根治**：新增 `thm-full-cp-coverage` 节点 + 3 条关联边（`e-fullcp-*`），消除 v1.0.0 里 `thm-split-cp-coverage` 引用悬空节点的问题（原 Darwin 报告头号功能性缺陷，#1 高优）
- **关系类型精化**：`e-unc-conditional` 从 `contradicts` 改为 `does_not_guarantee`——标量不确定性"不提供"条件覆盖是"不保证"而非"矛盾"，语义更精确
- **meta.sources 计数同步**：angelopoulos2022（21→22 nodes, 72→75 edges）、min2026（20→19 nodes）与实际统计对齐（2026-06-27 修复，黄金基线锁定前）

### 新增
- `thm-full-cp-coverage` — Full Conformal Prediction Coverage Guarantee（split CP 的推广对偶）
- SKILL.md 新增「示例查询」节（3 个完整查询路径：概念查询/跨论文比较/实验设计）
- SKILL.md 新增「加载效率提示」节（核心查询 ~3K tokens / 完整查询 ~8-11K tokens）
- schema.md §3 关系类型表登记 `does_not_guarantee`

### 文档
- schema.md §7 Query Step1 修正：移除"日常查询读 schema.md"指令，与 SKILL.md「schema 仅 Ingest/Lint 加载」声明一致

### 变更
- 节点 49 → 50，边 135 → 138，断裂引用 1 → 0
- Darwin 评分 87 → 88（A- 维持，⑥一致性 +1 驱动）

---

## [1.0.0] — 2026-06-24

### 初始版本
- 3 篇来源论文（Angelopoulos & Bates 2022 / Teneggi 2025 / Min 2026）知识蒸馏
- 49 节点 / 135 边 / 0 孤立 / 0 重复
- 4 心智模型 + 5 步查询协议 + 完整 schema（5 节点类型 + 9→10 关系类型）
- Darwin MVP 评分 87/100（A-）
- 已知缺陷：1 断裂引用（thm-full-cp-coverage 缺失）→ v1.1.0 修复

---

## 黄金基线锁定说明（2026-06-27）

本 v1.1.0 版本经独立 fresh-context reviewer 重评，88 分（A-），0 阻塞问题，5 项 Note 已全部修复。
作为 domain-knowledge-builder meta-skill 的**黄金测试用例**冻结。
后续此实例只读（除非 reviewer 发现新问题或领域知识有重大更新）。
