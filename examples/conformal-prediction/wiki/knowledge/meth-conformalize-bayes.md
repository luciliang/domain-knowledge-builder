---
id: meth-conformalize-bayes
type: method
label: Conformalizing Bayes
source: angelopoulos2022
section: Section 2.4
tokens: 900
created: 2026-06-24
---

## 精确表述

Given a Bayesian model $\hat{f}(y|x)$ estimating the posterior predictive density, the conformal score is:

$$s(x, y) = -\hat{f}(y|x).$$

Prediction sets are:

$$C(x) = \{y : \hat{f}(y|x) > -\hat{q}\}.$$

"This set is valid because we chose the threshold $\hat{q}$ via conformal prediction. Furthermore, when certain technical assumptions are satisfied, it has the best Bayes risk among all prediction sets with $1-\alpha$ coverage."

## 适用条件

1. A Bayesian model $\hat{f}(y|x)$ (e.g., Bayesian neural network)
2. The model may rely on incorrect assumptions—conformal corrects for this
3. Calibration data of $n$ i.i.d. pairs
4. For Bayes optimality: additional technical assumptions from Hoff (2021) must hold

## 直觉解释

Bayesian models give a heuristic notion of uncertainty via the posterior. Conformal prediction turns this into rigorous coverage. The Bayes optimality means that among all valid conformal procedures, this one produces the smallest average-size sets when the Bayesian assumptions are correct—similar to the Neyman-Pearson lemma.

## 与其他知识的关系

→ thm-split-cp-coverage (satisfies Theorem 1's coverage guarantee)
← def-split-conformal-prediction (specialization of split CP)
→ thm-split-cp-coverage (valid regardless of Bayesian assumptions)

## 来源引用

Angelopoulos & Bates (2022), Section 2.4, Equation (6); Figure 9; cites Hoff (2021), Wasserman (2011), Melluish et al. (2001)
