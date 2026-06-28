---
id: meth-covariate-shift-conditional
type: method
label: Conditional Methods under Covariate Shift (Density-Ratio + Localization)
source: min2026
section: Section 4.2
tokens: 1000
created: 2026-06-24
---

## 精确表述

Under covariate shift, two design principles for the weight function w(·):

1. **For scores removing conditional heterogeneity** (CQR, LCP, DCP, GLCP): The oracle conditional quantile $Q(1-\alpha; F_{s^\star|X_{n+1}=t})$ is constant across t. Setting $w(\cdot) = r_X(\cdot)$ suffices to remove both marginal and intrinsic conditional-mismatch errors.

2. **For scores not removing conditional heterogeneity** (e.g., pre-trained v(x,y) with $s^\star(x,y) = v(x,y)$): Combine density-ratio correction with localization: $w(x) = r_X(x) \cdot K(\tilde{x}, X_n+1; h)$, where $\tilde{x}$ is drawn from density proportional to $K(\cdot, X_{n+1}; h)$.

The conditional-miscoverage decomposition (Theorem 2) applies unchanged after replacing Assumption 1 with Assumption 7.

## 适用条件

1. Known density ratio $r_X(x) = dP_{X,2}/dP_{X,1}(x)$
2. $P_{Y|X}$ unchanged between calibration and test distributions

## 直觉解释

Density-ratio correction alone (WCP) restores marginal validity but does not guarantee small conditional miscoverage. The unified framework shows that combining density-ratio correction with conditional adaptation (localization or score-based heterogeneity removal) yields better conditional performance than WCP alone.

## 与其他知识的关系

← thm-covariate-shift-marginal（基于边际覆盖定理设计）
← thm-three-term-decomposition（利用三误差分解指导设计）
→ exp-covariate-shift（实验验证密度比加权条件方法优于 WCP）

## 来源引用

Min et al. (2026), Section 4.2. arXiv:2605.11602v3.
