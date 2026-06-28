---
stage: S3
mode: dual-source (incremental: ho2020 base + song2021)
domain: diffusion-models
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
run_ids: [09207eda-1bc6-46b7-a8f3-779abb928d4f, 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9]
created: 2026-06-28
last_updated: 2026-06-28
---

# S3 合并报告 — DAG 构建（单源）

> **single-source S3, structural validation only**
> 本领域当前仅 ingest 一篇来源（ho2020，Score-SDE 下载失败待补），故 S3 无多源合并冲突裁决，
> 简化为「结构化校验 + 统一 dag-index.json 生成」。无 `contradicts` / `does_not_guarantee` 边需人工确认。

## 输入

- 来源：`extraction-ho2020.json`（S2 产出，run_id `09207eda-1bc6-46b7-a8f3-779abb928d4f`）
- 节点：15（def×3 / thm×2 / meth×4 / exp×3 / ins×3）
- 边：22

## 输出

- `dag/dag-index.json` — schema §4 结构，从 extraction 规范化（确定性 key 顺序，sort_keys）后写入。
  保持全部 provenance 字段（generated_by_step / run_id / source_span）。

## 程序化校验结果（schema §8 结构检查）

| 检查项 | 期望 | 实际 | 结果 |
|--------|------|------|------|
| 断裂引用（edges from/to 不在 nodes） | 0 | 0 | ✅ |
| 重复 node ID | 0 | 0 | ✅ |
| 重复 edge ID | 0 | 0 | ✅ |
| 孤立节点（无 edge 关联） | 0 | 0 | ✅ |
| 关系类型合法（§3 十一种） | 全合法 | 全合法 | ✅ |
| meta 计数漂移（total/source nodes/edges vs 实际） | 0 | 0 | ✅ |
| Provenance 完整性（新 ingest 三字段齐全） | 15/15 | 15/15 | ✅ |
| 路径确定性（§12.5 仅 skill-root-relative） | 0 违规 | 0 违规 | ✅ |

**结论：ALL_CHECKS_PASS。** dag-index.json 与 meta 计数一致（total_nodes=15 / total_edges=22 / source ho2020: 15 nodes 22 edges）。

## 关系类型分布

- `depends_on` ×14（理解链条）
- `evaluates` ×6（方法被实验评估；方向 meth→exp 符合 schema §3「B 是 A 的度量」）
- `specializes` ×1（Lsimple 是 ELBO 的加权特例）
- `compares_with` ×1（AR 重新诠释 ↔ 率-失真重新诠释）
- `contradicts` / `does_not_guarantee` ×0（无需人工确认）

## 单源限制与待办

- 单源：所有节点/边 provenance `source: ho2020`，未做跨源交叉验证。
- 待 Score-SDE（Song et al. 2021）ingest 后，将新增 `generalizes` / `extends` 边建立离散↔连续时间联系，并可能引入新的跨源心智模型（见 S5 诚实边界）。

---

# S3 合并报告 — 增量合并（双源 → 统一 DAG）

> **dual-source incremental S3, run_id `9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9`**
> 在原 ho2020 单源 DAG（15 节点/22 边）上增量追加 song2021（Score-SDE，15 节点/31 边），
> 建立离散（DDPM）↔ 连续（SDE）统一关系。无 `contradicts` / `does_not_guarantee` 边——ho2020 与 song2021 是统一（非矛盾）关系，无需人工确认。

## 输入

- 基线：`dag/dag-index.json`（ho2020，run_id `09207eda-…`，15 节点/22 边）
- 增量：`extraction-song2021.json`（run_id `9bab0aa5-…`，15 节点/31 边 = 20 源内 + 11 跨源）

## 输出

- `dag/dag-index.json`：合并后 **30 节点 / 53 边**，`meta` 双 run（`run_id` 取增量 run，`run_ids` 保留 [原, 增量]），sources 含 ho2020(15,22) 与 song2021(15,31)。节点 provenance 全保留（generated_by_step / run_id / source_span）。

## 跨源关系（11 条）

> 方向语义按 schema §3 校验：`generalizes` 的 `to` 是推广形式（更一般）、`extends` 的 `to` 是扩展形式。S2 extraction 原把 10 条有向跨源边统一写成 `from=song2021(一般)→to=ho2020(特例)`，与 schema 方向相反（也与 song2021 自身正确的源内 `extends` 边 `reverse-time-sde → conditional-sde` 矛盾）。S3 **翻转这 10 条边的 from/to** 使「一般/扩展 = to = song2021 节点」，relation 与 desc 保持不变（desc 本就以 song2021 为推广方表述，翻转后语义一致）。对称的 `compares_with` 不翻转。

| 边 | relation | 方向（合并后） | 说明 |
|----|----------|----------------|------|
| xsrc-vpsde-fwd | generalizes | def-ho2020-forward-diffusion-process → def-song2021-vp-sde | VP-SDE 是 DDPM 前向链的连续推广 |
| xsrc-fsde-fwd | generalizes | def-ho2020-forward-diffusion-process → def-song2021-forward-sde | 一般前向 SDE 框架含括 DDPM 高斯前向 |
| xsrc-reverse-revproc | generalizes | def-ho2020-reverse-process → thm-song2021-reverse-time-sde | reverse-time SDE 是 DDPM 反向链的连续推广 |
| xsrc-equiv-fwd | generalizes | def-ho2020-forward-diffusion-process → thm-song2021-sde-discretization-equivalence | 离散-连续等价证明 DDPM 前向是 VP-SDE 离散化 |
| xsrc-framework-scorelang | generalizes | thm-ho2020-score-matching-langevin-equivalence → ins-song2021-unified-continuous-framework | ho2020 等价被重构为统一框架的一个 SDE 特例 |
| xsrc-pc-ancestral | generalizes | meth-ho2020-ddpm-sampling → meth-song2021-pc-sampler | DDPM ancestral 是 PC 采样器的 predictor-only 退化（medium） |
| xsrc-reverse-eps-equiv | extends | thm-ho2020-score-matching-langevin-equivalence → thm-song2021-reverse-time-sde | 离散 Langevin 等价被连续化为 reverse-time SDE |
| xsrc-equiv-scorelang | extends | thm-ho2020-score-matching-langevin-equivalence → thm-song2021-sde-discretization-equivalence | ho2020 启发式等价提升为框架级定理 |
| xsrc-training-eps | extends | meth-ho2020-epsilon-prediction → meth-song2021-score-based-training | ε-预测即加权去噪 score matching，连续时间推广 |
| xsrc-pfode-elbo | extends | thm-ho2020-elbo-variational-bound → thm-song2021-probability-flow-ode | PF-ODE 给出精确似然，严格强于 ELBO 上界 |
| xsrc-cifar-cifar | compares_with | exp-song2021-cifar10-results ↔ exp-ho2020-cifar10-results | CIFAR-10 直比：FID 2.20/IS 9.89 vs 3.17/9.46；NLL 2.99 vs ≤3.75 |

**方向翻转数：10（5 generalizes + 5 extends）。对称 compares_with 1 条不翻转。无冲突边。**

## 程序化校验结果（schema §8 结构检查 + §10 Determinism + §11 Provenance + §12.5 路径）

| 检查项 | 期望 | 实际 | 结果 |
|--------|------|------|------|
| 断裂引用（edges from/to 不在 nodes） | 0 | 0 | ✅ |
| 重复 node ID | 0 | 0 | ✅ |
| 重复 edge ID | 0 | 0 | ✅ |
| 孤立节点（无 edge 关联） | 0 | 0 | ✅ |
| 关系类型合法（§3） | 全合法 | 全合法 | ✅ |
| meta 计数漂移（total/source vs 实际） | 0 | 0 | ✅（30/53；ho2020 15/22；song2021 15/31）|
| Provenance 完整（song2021 新 ingest 三字段） | 15/15 | 15/15 | ✅ |
| 路径确定性（§12.5 仅 skill-root-relative） | 0 违规 | 0 违规 | ✅ |
| 需人工确认边（contradicts/does_not_guarantee） | 0 | 0 | ✅ |

**结论：ALL_CHECKS_PASS。**

## 关系类型分布（合并后）

- `depends_on` ×25（ho2020 14 + song2021 11 源内）
- `evaluates` ×10（ho2020 6 + song2021 4 源内）
- `generalizes` ×6（song2021，全部为跨源；其中 `xsrc-pc-ancestral` 置信度 medium，余 high）
- `extends` ×5（song2021：源内 1 [`e-reverse-conditional`] + 跨源 4）
- `specializes` ×3（ho2020 1 + song2021 2 源内）
- `compares_with` ×4（ho2020 1 + song2021：源内 2 + 跨源 1）

> 注：跨源 `generalizes`（6 条）与跨源 `extends`（4 条）经方向翻转后，`to` 均指向 song2021（连续/一般/扩展）节点，符合 schema §3 方向语义。对称 `compares_with` 不区分方向。

## 增量原则遵守

- 未修改 ho2020 的任何已有节点/边（provenance `run_id=09207eda-…` 保持不变）。
- song2021 节点/边为新增，`source=song2021`、`run_id=9bab0aa5-…`。
- 合并为纯追加 + 跨源方向归一，可独立回滚（revert 本 stage commit 即恢复单源状态）。
