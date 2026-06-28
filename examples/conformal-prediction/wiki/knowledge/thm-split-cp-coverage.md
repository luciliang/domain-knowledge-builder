---
id: thm-split-cp-coverage
type: theorem
label: Theorem 1: Conformal Coverage Guarantee (Split CP)
source: angelopoulos2022
section: Section 1
tokens: 1000
created: 2026-06-24
---

## 精确表述

"Theorem 1 (Conformal coverage guarantee; Vovk, Gammerman, and Saunders). Suppose $(X_i, Y_i)_{i=1,...,n}$ and $(X_{\text{test}}, Y_{\text{test}})$ are i.i.d. and define $\hat{q}$ as in step 3 above and $C(X_{\text{test}})$ as in step 4 above. Then the following holds:

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1 - \alpha."$$

The full coverage property including the upper bound (from Appendix D):

$$1 - \alpha \leq \mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \leq 1 - \alpha + \frac{1}{n+1}.$$

## 适用条件

1. $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are i.i.d. (or more generally, exchangeable)
2. Score function $s(x, y)$ is any function mapping to $\mathbb{R}$
3. $\hat{q}$ is the $\lceil(n+1)(1-\alpha)\rceil/n$ empirical quantile of $s_1, \ldots, s_n$
4. $C(X_{\text{test}}) = \{y : s(X_{\text{test}}, y) \leq \hat{q}\}$

## 直觉解释

By exchangeability, the test score $s_{\text{test}}$ is equally likely to fall anywhere between the ordered calibration scores $s_{(1)}, \ldots, s_{(n)}$. The quantile threshold picks the $\lceil(n+1)(1-\alpha)\rceil$-th smallest score, so $s_{\text{test}}$ falls below it with probability at least $\lceil(n+1)(1-\alpha)\rceil/(n+1) \geq 1-\alpha$.

## 与其他知识的关系

→ def-marginal-coverage (this theorem guarantees marginal coverage)
→ def-conformal-coverage (this is the foundational conformal coverage guarantee)
→ def-split-conformal-prediction (theorem is the validity property of split CP)
→ thm-full-cp-coverage (generalization to full conformal prediction)
→ thm-covariate-shift-coverage (extension under covariate shift)
→ thm-distribution-drift-coverage (extension under distribution drift)
→ thm-group-balanced-coverage (specialization to group-balanced)
→ thm-class-conditional-coverage (specialization to class-conditional)

## 来源引用

Angelopoulos & Bates (2022), Section 1, Theorem 1; Appendix D, Theorems D.1 and D.2
