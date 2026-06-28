---
id: def-three-errors
type: definition
label: Three Components of Conditional Miscoverage
source: min2026
section: Section 3
tokens: 1000
created: 2026-06-24
---

## 精确表述

Under the unified framework, conditional miscoverage decomposes into three interpretable components:

1. **Score-estimation error**: $\varepsilon + n\delta_n(\varepsilon) + \varepsilon_n^e + \delta_n^e$. Captures the discrepancy between the learned score $s(X_i, Y_i; Z)$ and its oracle target $s^\star(X_i, Y_i)$. Vanishes as training/calibration sample sizes increase.

2. **Finite-sample calibration error**: $\Gamma_n(w) = (\sigma_w B_w^{-1} n^{-1/2} + M_w B_w^{-1} n^{-1})\sqrt{\log(n)}$. Reflects error in estimating $Q(1-\alpha; F_{w \circ s^\star})$ using calibration scores. Characterizes effective sample-size behavior induced by weighting scheme w. For w ≡ 1: $\Gamma_n = O(n^{-1/2}\sqrt{\log n})$.

3. **Intrinsic conditional-mismatch error**: $\mathbb{E}\{|Q(1-\alpha; F_{s^\star|\phi(t)}) - Q(1-\alpha; F_{w \circ s^\star})| \mid \phi(t)\}$. Persists even with oracle score and noise-free calibration. When w ≡ 1, reduces to gap between conditional and marginal quantiles of $s^\star$. For CQR/GLCP/LCP with appropriate oracle scores, this is zero.

## 适用条件

All three terms apply under Assumptions 1–4 of the unified framework.

## 直觉解释

Any method achieving asymptotic conditional validity must make the intrinsic conditional-mismatch error asymptotically negligible. The remaining two errors arise purely from estimation uncertainty and vanish with more data. This decomposition clarifies why some methods (CQR, GLCP) have zero mismatch error (their oracle score removes conditional heterogeneity), while others (RLCP) trade off nonzero mismatch against lower score-estimation error.

## 与其他知识的关系

← thm-three-term-decomposition（由三误差分解定理定义）
→ ins-method-comparison-table（指导方法比较）
→ meth-model-selection-cc（内在误差是模型选择的关键目标量）

## 来源引用

Min et al. (2026), Section 3, following Theorem 2. arXiv:2605.11602v3.
