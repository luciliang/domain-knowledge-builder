---
id: ins-method-comparison-table
type: insight
label: Unified Error Decomposition Across Methods (Table 1)
source: min2026
section: Section 3, Table 1
tokens: 1100
created: 2026-06-24
---

## 精确表述

Table 1 of Min et al. (2026) summarizes conditional miscoverage errors for seven methods:

| Method | Score-estimation | Finite-sample calibration | Conditional-mismatch | Total |
|--------|------------------|--------------------------|----------------------|-------|
| LCP | $O((nh^d)^{-1/2} + h)$ | $O(n^{-1/2})$ | 0 | $O((nh^d)^{-1/2} + h)$ |
| RLCP | 0 | $O((nh^d)^{-1/2})$ | $O(h)$ | $O((nh^d)^{-1/2} + h)$ |
| CQR | $O(\delta_{tr})$ | $O(n^{-1/2})$ | 0 | $O(\delta_{tr} + n^{-1/2})$ |
| DCP | $O(\delta_{tr})$ | $O(n^{-1/2})$ | 0 | $O(\delta_{tr} + n^{-1/2})$ |
| GLCP | $O(\delta_{tr})$ | $O(n^{-1/2})$ | 0 | $O(\delta_{tr} + n^{-1/2})$ |
| BatchGCP | $O(n^{-1/2})$ | $O(n^{-1/2})$ | 0 | $O(n^{-1/2})$ |
| CC | $O((n/d_0)^{-1/3})$ | $O(n^{-1/2})$ | $O(\Delta_\mathcal{F})$ | $O((n/d_0)^{-1/3} + \Delta_\mathcal{F})$ |

All rates ignore logarithmic factors.

## 适用条件

Each row requires the specific assumptions for that method (detailed in Section S1).

## 直觉解释

Key pattern: score-based methods (CQR, DCP, GLCP) achieve zero intrinsic mismatch by construction (oracle conditional quantile is constant across t). RLCP has zero score-estimation error (pre-trained score) but nonzero calibration and mismatch. LCP has nonzero score-estimation (kernel c.d.f. estimation) but zero mismatch (rank score is uniform). The tradeoffs are method-specific but analyzable under a single framework.

## 与其他知识的关系

← thm-three-term-decomposition（由三误差分解定理驱动）
← def-three-errors（三个误差分量的定义）
→ exp-covariate-shift（实验验证这些理论速率）

## 来源引用

Min et al. (2026), Section 3, Table 1. arXiv:2605.11602v3.
