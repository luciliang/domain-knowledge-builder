---
id: thm-three-term-decomposition
type: theorem
label: Theorem 2: Three-Term Conditional Miscoverage Decomposition
source: min2026
section: Section 3
tokens: 1500
created: 2026-06-24
---

## 精确表述

Suppose Assumptions 1–4 hold. For each $t \in \mathcal{T}$, assume $s^\star(X_{n+1}, Y_{n+1})$ is independent of $q^\star(Z; \alpha)$ conditional on $\phi(t)$. Moreover, assume that $0 \leq w(X_1) \leq M_w$ almost surely, and define $B_w = \mathbb{E}\{w(X_1)|w\}$ and $\sigma_w^2 = \mathbb{E}\{w^2(X_1)|w\}$. Then, for each $t \in \mathcal{T}$, there exists a constant $C_t > 0$ such that

$$\Pr(Y_{n+1} \in \hat{C}(X_{n+1})|\phi(t)) - (1-\alpha)$$

$$\leq C_t \left[\varepsilon + n\delta_n(\varepsilon) + \varepsilon_n^e + \delta_n^e + C_t \mathbb{E}\{\Gamma_n(w)|\phi(t)\}\right.$$

$$+ C_t \mathbb{E}\left\{|Q(1-\alpha; F_{s^\star|\phi(t)}) - Q(1-\alpha; F_{w \circ s^\star})| \big| \phi(t)\right\}\right],$$

where $\Gamma_n(w) = (\sigma_w B_w^{-1} n^{-1/2} + M_w B_w^{-1} n^{-1})\sqrt{\log(n)}$.

## 适用条件

1. Assumptions 1–4 (i.i.d., score approximation, stability, regularity)
2. $w(X_1)$ uniformly bounded by $M_w$
3. $s^\star(X_{n+1}, Y_{n+1})$ conditionally independent of $q^\star(Z; \alpha)$ given $\phi(t)$

## 直觉解释

This is the central result of the paper. It decomposes conditional miscoverage into three interpretable components:

1. **Score-estimation error** ($\varepsilon + n\delta_n(\varepsilon) + \varepsilon_n^e + \delta_n^e$): gap between learned score and oracle target. Vanishes as training/calibration sizes increase.

2. **Finite-sample calibration error** ($\Gamma_n(w)$): quantile estimation error from finite calibration samples. $\Gamma_n(w) = O((\sigma_w B_w^{-1})n^{-1/2}\sqrt{\log n})$; for w ≡ 1, reduces to parametric rate $n^{-1/2}\sqrt{\log n}$.

3. **Intrinsic conditional-mismatch error** ($|Q(1-\alpha; F_{s^\star|\phi(t)}) - Q(1-\alpha; F_{w \circ s^\star})|$): persists even with perfect oracle score and infinite calibration. Measures gap between conditional and weighted-marginal quantiles. Must be made asymptotically negligible for conditional validity.

## 与其他知识的关系

← def-unified-cp-framework（基于统一框架建立）
→ def-three-errors（定义三个误差分量）
→ thm-averaged-miscoverage（对应平均版本）
→ meth-model-selection-cc（指导模型选择）
→ def-conditional-coverage（推广标准条件覆盖理论）

## 来源引用

Min et al. (2026), Section 3, Theorem 2, Equation (3). arXiv:2605.11602v3.
