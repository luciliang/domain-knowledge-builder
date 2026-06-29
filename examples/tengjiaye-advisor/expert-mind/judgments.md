# 判断索引 — 滕佳烨（Jiaye Teng）

> 本文件是**导航文件**，judgment 实体存储在独立 `judg-*.md` 文件中（顶部裸 frontmatter，供 lint 解析）。
> 对应 schema `coupling.md`。judgment 通过 `grounded_in` 引用知识节点 ID（与 `dag/dag-index.json` 一致）。

## 判断清单（6 条，紧耦合）

| ID | 触发问题 | 立场（一句话） | derived_from | 文件 |
|----|----------|----------------|--------------|------|
| `judg-teng-which-space-cp` | CP 该在哪个空间做 | 特征空间，深度表示归纳偏置让 band provably 更短 | `mm-teng-feature-space-superior` | [`judg-teng-which-space-cp.md`](judg-teng-which-space-cp.md) |
| `judg-teng-scd-split-disconnected` | CD-split 断开子区间怎么办 | SCD-split 用 Fourier smoothing 合并，保 coverage/长度有界/connectivity 不增 | `mm-teng-balance-efficiency-interpretability` | [`judg-teng-scd-split-disconnected.md`](judg-teng-scd-split-disconnected.md) |
| `judg-teng-shorter-not-better` | 更短的区间一定更好吗 | 不一定，Prejudicial Trick 证明 length 可被欺骗 | `mm-teng-question-standard-metric` | [`judg-teng-shorter-not-better.md`](judg-teng-shorter-not-better.md) |
| `judg-teng-nn-prediction-trust` | 神经网络预测可信吗 | 单独不可信，CP 包裹后 distribution-free 保证 coverage | `mm-teng-coverage-as-floor` | [`judg-teng-nn-prediction-trust.md`](judg-teng-nn-prediction-trust.md) |
| `judg-teng-theory-plus-engineering` | 好的 CP 研究长什么样 | 理论 + 工程并重，Feature CP 有定理 FFCP 50x 加速 | `mm-teng-feature-space-superior` | [`judg-teng-theory-plus-engineering.md`](judg-teng-theory-plus-engineering.md) |
| `judg-teng-censoring-coverage-recovery` | 删失/covariate shift 怎么办 | weighted conformal + 两阶段校准恢复 nearly perfect coverage | `mm-teng-coverage-as-floor` | [`judg-teng-censoring-coverage-recovery.md`](judg-teng-censoring-coverage-recovery.md) |

## grounded_in 节点引用映射（硬门③ 无孤儿）

每条 judgment 的 `grounded_in.node` 都在 `dag/dag-index.json` 的 9 个节点内：

| 判断 | 引用的知识节点 |
|------|----------------|
| `judg-teng-which-space-cp` | `thm-teng2023-feature-cp-advantage`, `meth-teng2023-surrogate-feature`, `meth-teng2025-ffcp-score`, `thm-split-cp-coverage` |
| `judg-teng-scd-split-disconnected` | `meth-teng2025-scd-split`, `thm-split-cp-coverage`, `thm-teng2026-prejudicial-trick` |
| `judg-teng-shorter-not-better` | `thm-teng2026-prejudicial-trick`, `meth-teng2025-scd-split`, `thm-split-cp-coverage`, `thm-teng2023-feature-cp-advantage` |
| `judg-teng-nn-prediction-trust` | `thm-split-cp-coverage`, `def-angelopoulosbates2022-exchangeability`, `thm-teng2021-tsci-coverage` |
| `judg-teng-theory-plus-engineering` | `thm-teng2023-feature-cp-advantage`, `meth-teng2025-ffcp-score`, `meth-teng2023-surrogate-feature`, `meth-teng2025-scd-split` |
| `judg-teng-censoring-coverage-recovery` | `thm-teng2021-tsci-coverage`, `def-angelopoulosbates2022-exchangeability`, `thm-split-cp-coverage` |

## 查询路由

- 问「CP 在哪个空间做」→ `judg-teng-which-space-cp`（融合模式：立场 + feature CP 定理依据）
- 问「更短区间更好吗」→ `judg-teng-shorter-not-better`（融合模式：立场 + PT 定理依据）
- 问「删失数据怎么做 CP」→ `judg-teng-censoring-coverage-recovery`（融合模式：立场 + T-SCI 定理依据）
- 完整三模式查询协议见 `SKILL.md` 与 `pipeline/query.md`
