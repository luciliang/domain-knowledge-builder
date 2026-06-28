---
id: meth-cqr
type: method
label: Conformalized Quantile Regression (CQR)
source: angelopoulos2022
section: Section 2.2
tokens: 1200
created: 2026-06-24
---

## 精确表述

CQR uses quantile regression as the base model and conformalizes its output. After training quantile regression to estimate $t_{\alpha/2}(x)$ and $t_{1-\alpha/2}(x)$, the score function is:

$$s(x, y) = \max\{\hat{t}_{\alpha/2}(x) - y, \; y - \hat{t}_{1-\alpha/2}(x)\}.$$

The valid prediction intervals are:

$$C(x) = [\hat{t}_{\alpha/2}(x) - \hat{q}, \; \hat{t}_{1-\alpha/2}(x) + \hat{q}],$$

where $\hat{q}$ is the conformal quantile. The quantile regression loss (pinball loss) is:

$$L_\gamma(\hat{t}_\gamma, y) = (y - \hat{t}_\gamma)\gamma \mathbf{1}_{y > \hat{t}_\gamma} + (\hat{t}_\gamma - y)(1 - \gamma) \mathbf{1}_{y \leq \hat{t}_\gamma}.$$

## 适用条件

1. Regression setting with continuous $Y$
2. Pre-trained quantile regression model outputting two quantiles
3. Calibration data of $n$ i.i.d. pairs
4. Quantile regression preferred when $\alpha$ is known in advance

## 直觉解释

The set $C(x)$ grows or shrinks the distance between the fitted quantiles by $\hat{q}$ to achieve coverage. Quantile regression provides intervals with near-conditional coverage asymptotically, so the conformalized version inherits this good behavior.

## 与其他知识的关系

→ thm-split-cp-coverage (satisfies Theorem 1's coverage guarantee)
← def-split-conformal-prediction (CQR is a specialization of split CP)
→ def-conditional-coverage (quantile regression has asymptotically valid conditional coverage, propagating to CQR)
↔ meth-conformalize-uncertainty (CQR preferred when possible; uncertainty scalars are easier but less precise)
↔ meth-aps (different CP method for classification)
→ meth-group-balanced-cp (can be combined)

## 来源引用

Angelopoulos & Bates (2022), Section 2.2, Equation (4); Figures 5–6; cites Romano, Patterson & Candès (2019)
