---
id: thm-covariate-shift-coverage
type: theorem
label: Theorem 3: Conformal Prediction Under Covariate Shift
source: angelopoulos2022
section: Section 4.5
tokens: 1100
created: 2026-06-24
---

## 精确表述

"Theorem 3 (Conformal prediction under covariate shift [Tibshirani et al. 2019]). Suppose $(X_1, Y_1), \ldots, (X_n, Y_n)$ are drawn i.i.d. from $P \times P_{Y|X}$ and that $(X_{\text{test}}, Y_{\text{test}})$ is drawn independently from $P_{\text{test}} \times P_{Y|X}$. Then the choice of $C$ above satisfies

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1 - \alpha."$$

The weighted conformal quantile is:

$$\hat{q}(x) = \inf\left\{s_j : \sum_{i=1}^n p_i^w(x) \mathbf{1}\{s_i \leq s_j\} \geq 1 - \alpha\right\},$$

where weights are based on the likelihood ratio $w(x) = dP_{\text{test}}(x)/dP(x)$.

## 适用条件

1. Calibration data from $P$, test data from $P_{\text{test}}$
2. The conditional distribution $P_{Y|X}$ stays fixed (only $X$ distribution changes)
3. The likelihood ratio $w(x) = dP_{\text{test}}(x)/dP(x)$ is known or estimable
4. Score function $s$ only depends on $(x, y)$

## 直觉解释

By reweighting calibration scores with the likelihood ratio, we make the calibration data "look like" the test distribution. Points more likely under $P_{\text{test}}$ get higher weight, shifting the quantile appropriately.

## 与其他知识的关系

→ def-marginal-coverage (preserves marginal coverage under covariate shift)
← thm-split-cp-coverage (extends standard CP to covariate shift)
→ thm-distribution-drift-coverage (further generalization to unknown drift)
← def-split-conformal-prediction (special case when $P = P_{\text{test}}$)

## 来源引用

Angelopoulos & Bates (2022), Section 4.5, Theorem 3; cites Tibshirani et al. (2019)
