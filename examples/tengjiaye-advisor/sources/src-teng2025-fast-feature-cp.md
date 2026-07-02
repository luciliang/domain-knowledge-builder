---
id: src-teng2025-fast-feature-cp
type: paper
value: both
channel: user
file: inputs/papers/teng2025-fast-feature-cp.pdf
locator:
  page: 1
  section: "Abstract + §1 Introduction (Eq. 2) + Theorem 4/5"
collected_at: 2026-06-28
format: pdf
title: "Predictive Inference With Fast Feature Conformal Prediction (FFCP)"
authors: ["Zihao Tang", "Boyuan Wang", "Chuan Wen", "Jiaye Teng"]
year: 2025
venue: "arXiv:2412.00653"
---

## 来源摘要

滕佳烨通讯作者（上海财经大学）。FCP 的加速版——**Fast Feature CP (FFCP)**。解决 FCP 的 Band Estimation 依赖 LiPRA 非线性操作导致耗时的实用性瓶颈。

### 核心贡献

- **新 non-conformity score**：`s_ff(X, Y, g∘h) = |Y - g∘h(X)| / ||∇g(v̂)||`，其中 `v̂ = h(X)` 是特征，`∇g(v̂)` 是预测头对特征的梯度
- 用 **Taylor 展开**近似 FCP 的非线性 band 变换，避免 LiPRA；理论上是 FCP 的 fast version
- **Theorem 4**：FFCP 返回的 band empirical coverage ≥ 1-α（有效性）
- **Theorem 5**：在 **square conditions**（expansion + quantile stability）下，FFCP 返回比 vanilla CP 更短的 band（效率性）
- 实验：FFCP ≈ FCP 精度（都优于 vanilla），但 **~50x 加速**；可扩展到 CQR（FFCQR）、LCP（FFLCP）、RAPS（FFRAPS）

### 覆盖范围

本来源覆盖知识节点 `meth-teng2025-ffcp-score`、`thm-teng2025-ffcp-efficiency`，支撑心智模型 `mm-teng-feature-space-superior`（FCP 思路的延续与实用化）与「理论 + 工程并重」。

### 可信度

**高**。滕佳烨通讯作者，arXiv 预印本，代码开源（github.com/ElvisWang1111/FastFeatureCP）。是 Feature CP 主线的工程兑现。
