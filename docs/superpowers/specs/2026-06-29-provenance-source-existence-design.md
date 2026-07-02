# 设计：provenance/source 孤儿检查（硬门④，D7 可审计支柱对称强化）

> 状态：已批准（2026-06-29）｜规模：小（lint 2 函数 + 2 测试 + schema 1 处）
> 前序：`2026-06-29-deterministic-edge-id-design.md` / `2026-06-29-node-id-strict-and-tengjiaye-edges-design.md`

---

## 1. 动机

D7 四支柱中「可审计」是半成品：`check_auditable` 查节点 provenance 字段完整性（generated_by_step/run_id/source_span），但 **judgment/心智元素的 `provenance.sources` 引用的 `src-*.md` 是否真实存在无人查**（V1 backlog 第 1 项，靠 golden reference 人工核对）。

本次补硬门④，与硬门③（`check_grounding_existence`：grounded_in 节点存在）**完全对称**——把"引用必须指向真实存在的实体"这条原则从 knowledge 节点扩展到 source 文件。

## 2. 探索发现（支撑"无需 legacy 宽容"）

4 个 examples 当前 provenance.sources 引用**零孤儿**：

| example | src 文件 | expert-mind 引用 | 孤儿 |
|---------|---------|-----------------|------|
| conformal-prediction | 3 | 0（DKB 原模式无 expert-mind） | 0 |
| hinton-advisor | 12 | 12 | **0** |
| tengjiaye-advisor | 8 | 6 | **0** |
| diffusion-models | 0 | 0（DKB 原模式） | 0 |

→ 新检查上线不会误报现有数据，可像硬门③一样直接严格，无需 `--legacy-ok` 宽容。

## 3. 设计（硬门③对称物）

### `collect_source_ids(skill_root) -> set`（新 helper）
- 遍历 `skill_root` 下所有 `src-*.md`，收集合法 source id 集合
- id 来源：frontmatter `id` 优先 + 文件 stem 兜底（双保险，容错 yaml 解析）

### `check_provenance_sources_exist(src_ids, artifacts) -> list[str]`（硬门④）
- 输入：src_ids 集合 + `load_mind_artifacts` 的 judgments/elements（**复用已有**）
- 逻辑：每个 artifact 的 `provenance.sources` 每个 src id 必须在 src_ids，孤儿报 issue
- 签名与硬门③ `check_grounding_existence(dag_index, judgments)` 对称

### `main()` 接入
- 新增检查项「硬门④ provenance.sources 存在」

## 4. 决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 检查范围 | judgment + 心智元素（expert-mind/） | 与硬门③对称；节点 `source` 是单值非 src 列表，不在此列 |
| legacy 宽容 | **无**（孤儿即 error） | 探索确认零孤儿，不误报；与硬门③一致 |
| src id 来源 | frontmatter id + stem 兜底 | source.md schema 规定 id = stem，双保险 |

## 5. 改动清单

- `pipeline/state/lint_d7.py`：`collect_source_ids` + `check_provenance_sources_exist` + `main()` 接入
- `pipeline/state/test_lint_d7.py`：2 测试（passes / flags_orphan）
- `schema/schema.md` §12.2：可审计支柱补「source 引用存在性 lint」

## 6. 验收标准

- [ ] 2 新测试绿，全量测试无回归
- [ ] 4 examples lint 不报 source 孤儿（当前都干净）
- [ ] schema §12.2 同步

## 7. 不做（YAGNI）

- 不查节点 `source` 单值字段（不同机制，§5 来源摘要）
- 不查 src-*.md 内部质量（只查存在性）
- 不做 source 内容/忠实度校验（硬门②忠实度仍由 fresh subagent 兜底）
