---
id: ins-intrinsic-error-necessity
type: insight
label: Intrinsic Conditional-Mismatch Error is the Key Bottleneck
source: min2026
section: Section 3
tokens: 800
created: 2026-06-24
---

## 精确表述

"Theorem 2 shows that any method aiming for asymptotic conditional validity should, through an appropriate choice of score function and weighting scheme, make the intrinsic conditional-mismatch error asymptotically negligible. In contrast, the remaining terms arise purely from estimation uncertainty: the score-estimation error term $\varepsilon + n\delta_n(\varepsilon) + \varepsilon_n^e + \delta_n^e$ vanishes as the relevant training and/or calibration sample sizes increase, while the finite-sample calibration error term $\Gamma_n(w)$ converges to zero as $n \to \infty$."

## 适用条件

General principle under Assumptions 1–4.

## 直觉解释

This is the central insight of the unified theory. The first two errors (score estimation and calibration) are "mechanical" — they vanish with more data. The intrinsic mismatch error is "structural" — it persists regardless of sample size and must be addressed through methodological design (choice of score and weighting). Methods that make the oracle conditional quantile constant across t (CQR, GLCP) achieve zero intrinsic error by design.

## 与其他知识的关系

← thm-three-term-decomposition（从三误差分解定理得出的关键洞察）
→ def-three-errors（内在误差的定义）
→ meth-model-selection-cc（模型选择的目标就是最小化此误差）

## 来源引用

Min et al. (2026), Section 3, paragraph following Theorem 2. arXiv:2605.11602v3.
