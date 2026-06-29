# 设计：增量 ingest — computeDelta + run_type + §4 细化（收窄版）

> 状态：已批准（2026-06-29）｜规模：小（1 纯函数 + pipeline 接入 + 文档）
> 前序：本次会话 lint 强化系列（确定性边 id / 节点格式 / 硬门④）

---

## 1. 动机

`ingest.md §4` 已有增量 ingest 设计（S1–S3 只处理新源、S3 幂等合并），但缺：**增量 delta 的程序化计算与记录**——增完后不知道"本次到底新增了什么"。本次补这个可验证的核心，跳过不可验证的 stage prompt 增量分支。

## 2. 探索发现（支撑收窄）

- `run-dag-pipeline.js` 支持 `resume_from`（失败恢复）+ S3 增量合并，但**不计算/记录 Δ**
- S5 心智提炼**本质全局**（新材料可能带来全新模型）→ 真增量不可能，只能半全量
- stage prompt 增量分支是 LLM 文本指导，**端到端不可验证**（无 pi runtime）
- → 收窄到：可单测的 `computeDelta` + run_type 标记 + §4 细化

## 3. 改动清单

### 3.1 `computeDelta(oldDag, newDag)` 纯函数（`run-dag-pipeline.js` export）
```js
// 返回
{ added_node_ids: [...], added_edge_ids: [...], modified_node_ids: [...] }
```
- 节点/边按 id 比：新 id → added；同 id 内容（label/source/tokens 等）变 → modified
- 纯函数、确定性、可单测

### 3.2 pipeline 最小接入（避免死代码）
- `args.run_type = initial | incremental`
- incremental 模式：S3 前读现有 dag-index 作快照；S3 后调 `computeDelta(snapshot, newDag)`，Δ 摘要记入 `run-manifest.json`（type + added/modified 计数）

### 3.3 `ingest.md §4` 细化
- 加「各 stage 增量性」表（S4 真增量 / **S5 半全量** / S6 抽查聚焦 Δ / S7 半全量）
- 加「Δ 计算与记录」说明（computeDelta + run-manifest type 字段）

## 4. 跳过（用户决策）

- S4–S7 stage prompt 的增量分支文本（不可验证，留待 pi 环境真跑时再做）

## 5. 可验证性边界（诚实）

- `computeDelta` 纯函数：**node:test 单测** ✓
- pipeline 接入 + §4 细化：静态审查（workflow 脚本，本环境无 pi runtime）
- 端到端增量 run：依赖 pi 环境，本环境无法验证

## 6. 测试（TDD）

`computeDelta` 4 个用例：
- added_nodes（新节点）
- added_edges（新边）
- 无变化（幂等：old==new → 空 Δ）
- modified_nodes（同 id 内容变）

## 7. 不做（YAGNI）

- 不做 S5 纯增量（全局性质，不可能）
- 不做 stage prompt 增量分支（不可验证）
- 不做端到端增量测试（无 pi runtime）
