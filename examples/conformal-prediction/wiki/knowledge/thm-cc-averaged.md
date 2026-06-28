---
id: thm-cc-averaged
type: theorem
label: Corollary 1: Averaged Conditional Miscoverage of CC
source: min2026
section: Section 3.1
tokens: 900
created: 2026-06-24
---

## 精确表述

Suppose that, for constant $M > 0$, $|v(X,Y)| \leq M$ and $\|\eta(X)\|_2 \leq M$ almost surely for $(X,Y) \sim P_{X \times Y|X}$. Assume the conditional density of $v(X,Y)$ given $X = x$ is bounded below by $\underline{L}$ and above by $\overline{L}$ on its support, for positive constants $\underline{L}$ and $\overline{L}$. Then there exists a constant $C > 0$ such that

$$\mathbb{E}[\Pr(Y_{n+1} \in \hat{C}_{CC}(X_{n+1})|X_{n+1}) - (1-\alpha)]$$

$$\leq C\sqrt{\inf_{f \in \mathcal{F}} R(f) - R(Q_\alpha^\star) + \{d_0 \log(n)/n\}^{1/3}}.$$

## 适用条件

1. CC with penalized quantile regression estimator in RKHS
2. Score class $\mathcal{F} = \{f_\kappa : f_\kappa(x) = \sum_{i=1}^{d_0} \kappa_i \eta_i(x), \|\kappa\|_2 \leq B\}$
3. Base score bounded, conditional density bounded away from 0 and ∞

## 直觉解释

The bound decomposes into approximation error ($\inf_{f \in \mathcal{F}} R(f) - R(Q_\alpha^\star)$, from restricting to function class $\mathcal{F}$) and estimation error ($\{d_0 \log(n)/n\}^{1/3}$). If the approximation error is negligible, CC's averaged conditional miscoverage converges to zero. This provides the first unconditional non-asymptotic averaged miscoverage guarantee for CC.

## 与其他知识的关系

← thm-averaged-miscoverage（从 Theorem 3 特化得到）
→ ins-method-comparison-table（CC 在 Table 1 中的条目）

## 来源引用

Min et al. (2026), Section 3.1, Corollary 1. arXiv:2605.11602v3.
