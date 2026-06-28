---
id: def-split-conformal-prediction
type: definition
label: Split Conformal Prediction (Inductive)
source: angelopoulos2022
section: Section 1
tokens: 800
created: 2026-06-24
---

## 精确表述

Split conformal prediction (also called inductive conformal prediction) is the most widely-used version of conformal prediction. It works with a pre-trained model $\hat{f}$ and a separate calibration dataset of $n$ fresh i.i.d. pairs $(X_1, Y_1), \ldots, (X_n, Y_n)$ unseen during training. Using $\hat{f}$ and the calibration data, we construct a prediction set $C(X_{\text{test}})$ that satisfies:

$$1 - \alpha \leq \mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \leq 1 - \alpha + \frac{1}{n+1},$$

where $(X_{\text{test}}, Y_{\text{test}})$ is a fresh test point from the same distribution, and $\alpha \in [0,1]$ is a user-chosen error rate. The procedure requires only one model fitting step (no data reuse for calibration).

## 适用条件

1. A pre-trained model $\hat{f}$ (any model, no assumptions on correctness)
2. $n$ calibration points that are i.i.d. and exchangeable with the test point
3. A score function $s(x, y) \in \mathbb{R}$ (larger = worse agreement)
4. The quantile is computed as the $\lceil(n+1)(1-\alpha)\rceil/n$ empirical quantile of calibration scores

## 直觉解释

The holdout set provides an honest appraisal of the model's performance. We compute conformal scores that grow when the model is uncertain, then take the $1-\alpha$ quantile. A new test point is covered if its score falls below this quantile. The data splitting ensures the calibration scores are exchangeable with the test score.

## 与其他知识的关系

→ thm-split-cp-coverage (guarantees marginal coverage)
← def-marginal-coverage (split CP achieves this property)
→ meth-aps (extends to adaptive prediction sets)
→ meth-cqr (extends to conformalized quantile regression)
→ meth-conformalize-uncertainty (extends to uncertainty scalars)
→ meth-conformalize-bayes (extends to Bayesian models)
← thm-full-cp-coverage (full CP is more general but less efficient)
→ meth-full-cp (full CP extends split CP)
→ meth-cv-jackknife (CV+/Jackknife+ are intermediate between split and full CP)
↔ def-conditional-coverage (split CP only guarantees marginal, not conditional coverage)

## 来源引用

Angelopoulos & Bates (2022), Section 1, Equations (1)–(2); Theorem 1
