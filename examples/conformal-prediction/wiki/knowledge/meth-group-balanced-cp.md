---
id: meth-group-balanced-cp
type: method
label: Group-Balanced Conformal Prediction
source: angelopoulos2022
section: Section 4.1
tokens: 1000
created: 2026-06-24
---

## 精确表述

Given groups defined by feature $X_{i,1} \in \{1, \ldots, G\}$, group-balanced CP runs conformal prediction separately for each group. The score is stratified by group:

$$s_i^{(g)} = s(X_j, Y_j), \text{ where } X_{j,1} \text{ is the } i\text{th occurrence of group } g.$$

Within each group, the conformal quantile is:

$$\hat{q}^{(g)} = \text{Quantile}(s_1^{(g)}, \ldots, s_{n(g)}^{(g)}; \frac{(n^{(g)}+1)(1-\alpha)}{n^{(g)}}),$$

where $n^{(g)}$ is the number of examples of group $g$. The prediction set uses the group-specific threshold:

$$C(x) = \{y : s(x, y) \leq \hat{q}^{(x_1)}\}.$$

## 适用条件

1. Known group membership for each data point (observed feature $X_{i,1}$)
2. Sufficient calibration points per group
3. Group can be a post-processing of original features (e.g., binning)

## 直觉解释

Each group gets its own conformal threshold, ensuring equal coverage across groups. This prevents the scenario where marginal coverage is satisfied but all errors concentrate in one group.

## 与其他知识的关系

→ thm-group-balanced-coverage (guarantees group-balanced coverage)
← thm-split-cp-coverage (extends standard CP)
→ def-conditional-coverage (achieves conditional coverage for the known grouping)
↔ meth-class-conditional-cp (similar idea but groups by true class, which is unknown at test time)
→ def-fsc-metric (FSC metric evaluates whether group-balanced CP succeeded)

## 来源引用

Angelopoulos & Bates (2022), Section 4.1, Equation (8); Proposition 1; cites Vovk (2012)
