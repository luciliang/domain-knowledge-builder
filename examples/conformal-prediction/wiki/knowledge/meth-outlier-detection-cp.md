---
id: meth-outlier-detection-cp
type: method
label: Conformal Outlier Detection
source: angelopoulos2022
section: Section 4.4
tokens: 900
created: 2026-06-24
---

## 精确表述

Conformal outlier detection adapts CP to unsupervised settings. Given clean data $X_1, \ldots, X_n$ and a score function $s: \mathcal{X} \to \mathbb{R}$ (note: score depends only on features, not labels):

$$C(x) = \begin{cases} \text{inlier} & \text{if } s(x) \leq \hat{q} \\ \text{outlier} & \text{if } s(x) > \hat{q} \end{cases},$$

where $\hat{q}$ is the $\lceil(n+1)(1-\alpha)\rceil/n$ quantile of $s(X_1), \ldots, s(X_n)$. This guarantees:

$$\mathbb{P}(C(X_{\text{test}}) = \text{outlier}) \leq \alpha.$$

## 适用条件

1. Clean dataset $X_1, \ldots, X_n$ from the inlier distribution
2. A heuristic outlier detection model
3. Score function $s: \mathcal{X} \to \mathbb{R}$ (unsupervised, no labels)

## 直觉解释

Conformal outlier detection calibrates the outlier score threshold to control the false positive rate. Points with scores exceeding the quantile are flagged as outliers, with a guaranteed bound on the fraction of false alarms among clean data.

## 与其他知识的关系

→ thm-outlier-detection-guarantee (Proposition 3 guarantees error control)
← def-split-conformal-prediction (specialization to unsupervised setting)
↔ meth-cqr (different application of conformal framework)

## 来源引用

Angelopoulos & Bates (2022), Section 4.4, Equation (14); Proposition 3
