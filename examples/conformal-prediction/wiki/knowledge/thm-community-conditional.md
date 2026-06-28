---
id: thm-community-conditional
type: theorem
label: Theorem 7: Community-Conditional Miscoverage Convergence
source: min2026
section: Section 4.3.1
tokens: 1000
created: 2026-06-24
---

## 精确表述

Suppose Assumption 10 holds (community recovery and base-score approximation). Assume that for every $I \in [n_{comm}]$, $F_{v^\star|\sigma(W)=I}$ is $L_I$-Lipschitz continuous for some positive constant $L_I$. Then for $\varepsilon \leq p_{comm}/4$, there exists a constant $C > 0$ such that, for every $I \in [n_{comm}]$,

$$\Pr(Y_{n+1} \in \hat{C}_{GraphCP}(X_{n+1})|\sigma(W_{n+1}) = I) - (1-\alpha)$$

$$\leq C\left[\varepsilon + n^{-1} + \delta_{comm}(n, \varepsilon) + \delta(n, \varepsilon) + n_{comm}\exp(-np_{comm}\varepsilon^2)\right].$$

## 适用条件

1. Assumption 10: consistent community recovery and base-score convergence
2. Lipschitz continuous conditional distribution functions per community
3. $\varepsilon \leq p_{comm}/4$ (minimum community proportion sufficient)

## 直觉解释

The bound decomposes into: (1) $\varepsilon + \delta_{comm}(n,\varepsilon) + \delta(n,\varepsilon)$ for community recovery + score estimation; (2) $n^{-1} + n_{comm}\exp(-np_{comm}\varepsilon^2)$ for finite-sample calibration error driven by discreteness and minimum community size. Crucially, the within-community rank score construction makes intrinsic conditional-mismatch error vanish asymptotically.

## 与其他知识的关系

← meth-graphcp（分析 GraphCP 方法的理论保证）
← thm-symmpi-conditional（Theorem 6 在图数据上的具体实例化）

## 来源引用

Min et al. (2026), Section 4.3.1, Theorem 7. arXiv:2605.11602v3.
