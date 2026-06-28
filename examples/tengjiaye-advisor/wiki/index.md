# Wiki 索引 — 滕佳烨 CP 顾问

> 知识导航层。节点实体在 `dag/knowledge/*.md`，此处只做分组导航（一句话摘要）。

## 定义（definition）

| ID | 摘要 | 文件 |
|----|------|------|
| `def-exchangeability` | 可交换性——联合分布在任意置换下不变，弱于 i.i.d.，是 CP 保证的基石 | [`def-exchangeability.md`](../dag/knowledge/def-exchangeability.md) |

## 定理（theorem）

| ID | 摘要 | 文件 |
|----|------|------|
| `thm-split-cp-coverage` | Split CP Coverage：P(Y_test∈C)≥1-α，finite-sample distribution-free（滕佳烨所有工作的底盘） | [`thm-split-cp-coverage.md`](../dag/knowledge/thm-split-cp-coverage.md) |
| `thm-teng2023-feature-cp-advantage` | Feature CP 优势：cubic conditions 下比 vanilla CP provably 更短，coverage 有效（代表作） | [`thm-teng2023-feature-cp-advantage.md`](../dag/knowledge/thm-teng2023-feature-cp-advantage.md) |
| `thm-teng2026-prejudicial-trick` | Prejudicial Trick：coverage valid 但 length 可欺骗，更短≠更好（ICML 2026） | [`thm-teng2026-prejudicial-trick.md`](../dag/knowledge/thm-teng2026-prejudicial-trick.md) |
| `thm-teng2021-tsci-coverage` | T-SCI：删失/covariate shift 下用 weighted conformal + 两阶段校准恢复 nearly perfect coverage | [`thm-teng2021-tsci-coverage.md`](../dag/knowledge/thm-teng2021-tsci-coverage.md) |

## 方法（method）

| ID | 摘要 | 文件 |
|----|------|------|
| `meth-aps-raps` | APS/RAPS：分类任务 output-space non-conformity score，feature CP 对比基准 | [`meth-aps-raps.md`](../dag/knowledge/meth-aps-raps.md) |
| `meth-teng2023-surrogate-feature` | Surrogate feature：解决 feature space 无 ground truth，是 Feature CP 技术核心 | [`meth-teng2023-surrogate-feature.md`](../dag/knowledge/meth-teng2023-surrogate-feature.md) |
| `meth-teng2025-ffcp-score` | FFCP score：s_ff=|Y-g∘h(X)|/||∇g(v̂)||，Taylor 展开近似，50x 加速 | [`meth-teng2025-ffcp-score.md`](../dag/knowledge/meth-teng2025-ffcp-score.md) |
| `meth-teng2025-scd-split` | SCD-split：Fourier smoothing 合并 CD-split 断开子区间，引入 connectivity 度量 | [`meth-teng2025-scd-split.md`](../dag/knowledge/meth-teng2025-scd-split.md) |

## 来源（8 篇）

滕佳烨 5 篇 + CP 经典 3 篇，详见 `sources/src-*.md`。

## 相关导航

- 专家心智：`../expert-mind/index.md`
- 判断：`../expert-mind/judgments.md`
- 领域概览：`overview.md`
