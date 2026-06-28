---
id: thm-symmpi-conditional
type: theorem
label: Theorem 6: Conditional Miscoverage Decomposition under SymmPI
source: min2026
section: Section 4.3
tokens: 1000
created: 2026-06-24
---

## 精确表述

Suppose Assumption 9 holds. If for every $t \in \mathcal{T}$, $F_{\psi(V^\star(\cdot))|\phi(t)}$ is $L_t$-Lipschitz continuous for some positive constant $L_t$, then

$$\Pr(Z \in \hat{C}(\Omega(Z))|\phi(t)) - (1-\alpha)$$

$$\leq \delta(\varepsilon) + 2L_t \varepsilon + L_t \mathbb{E}\{q(V^\star(Z); \alpha) - Q(1-\alpha; F_{\psi(V^\star(\cdot))})|\phi(t)\}$$

$$+ L_t |Q(1-\alpha; F_{\psi(V^\star(\cdot))}) - Q(1-\alpha; F_{\psi(V^\star(\cdot))|\phi(t)})|.$$

## 适用条件

1. Assumption 9: (i) oracle score independent of q conditional on $\phi(t)$; (ii) approximation condition on score and quantile errors
2. Conditional Lipschitz continuity of oracle score distribution

## 直觉解释

The three-term structure mirrors Theorem 2 for i.i.d. data: score-estimation error ($\delta(\varepsilon) + 2L_t\varepsilon$), finite-sample calibration error (gap between q and population quantile), and intrinsic conditional-mismatch error (gap between population and conditional quantiles). The unified theory thus extends naturally to structured data — the same mechanisms drive conditional miscoverage.

## 与其他知识的关系

← thm-symmpi-structured（基于 SymmPI 边际覆盖建立）
← thm-three-term-decomposition（i.i.d. 版本的三误差分解，结构完全对应）
→ thm-community-conditional（图数据上的具体应用）

## 来源引用

Min et al. (2026), Section 4.3, Theorem 6, Equation (9). arXiv:2605.11602v3.
