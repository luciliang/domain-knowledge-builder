---
id: meth-conformalize-uncertainty
type: method
label: Conformalizing Scalar Uncertainty Estimates
source: angelopoulos2022
section: Section 2.3
tokens: 1100
created: 2026-06-24
---

## 精确表述

Given a point prediction $\hat{f}(x)$ and an uncertainty scalar $u(x)$ (larger = more uncertain), the score function is:

$$s(x, y) = \frac{|y - \hat{f}(x)|}{u(x)}.$$

The prediction sets are:

$$C(x) = [\hat{f}(x) - u(x)\hat{q}, \; \hat{f}(x) + u(x)\hat{q}].$$

Uncertainty scalar sources include: (1) estimated standard deviation $\hat{\sigma}(x)$ from Gaussian modeling, (2) residual model $\hat{r}(x)$, (3) ensemble variance, (4) MC-Dropout variance, (5) adversarial perturbation magnitude, etc.

## 适用条件

1. Regression setting with continuous $Y$
2. A point predictor $\hat{f}(x)$ and an uncertainty scalar $u(x)$
3. $u(x)$ does not need to be a valid statistical estimate

## 直觉解释

The score $s(x,y)$ is a multiplicative correction factor: $s(x,y) \cdot u(x) = |y - \hat{f}(x)|$. The conformal quantile $\hat{q}$ adjusts the uncertainty scalar to achieve exact coverage. Uncertainty scalars are easier to deploy than quantile regression but don't scale properly with $\alpha$.

## 与其他知识的关系

→ thm-split-cp-coverage (satisfies Theorem 1's coverage guarantee)
← def-split-conformal-prediction (specialization of split CP)
↔ meth-cqr (quantile regression preferred when possible; uncertainty scalars easier but less precise)
→ def-conditional-coverage (does_not_guarantee: scalar uncertainty scaling provides marginal but not conditional coverage)

## 来源引用

Angelopoulos & Bates (2022), Section 2.3, Equation (5); Figures 7–8
