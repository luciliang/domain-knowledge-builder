---
id: meth-class-conditional-cp
type: method
label: Class-Conditional Conformal Prediction
source: angelopoulos2022
section: Section 4.2
tokens: 1000
created: 2026-06-24
---

## 精确表述

For classification with $Y \in \{1, \ldots, K\}$, class-conditional CP calibrates within each class separately. Unlike group-balanced CP, the true class is unknown at test time, so the algorithm iterates through classes using their class-specific thresholds:

$$\hat{q}^{(k)} = \text{Quantile}(s_1^{(k)}, \ldots, s_{n(k)}^{(k)}; \frac{(n^{(k)}+1)(1-\alpha)}{n^{(k)}}),$$

where $n^{(k)}$ is the number of calibration examples of class $k$. The prediction set:

$$C(x) = \{y : s(x, y) \leq \hat{q}^{(y)}\}.$$

Note: we take a provisional value of $y$ and use the threshold $\hat{q}^{(y)}$ specific to that class.

## 适用条件

1. Classification setting with $K$ classes
2. Sufficient calibration examples per class
3. True class unknown at test time (unlike group-balanced where group is observed)

## 直觉解释

Each class gets its own conformal threshold calibrated on its own examples. At test time, for each candidate class $y$, we check if the score $s(x, y)$ is below that class's threshold $\hat{q}^{(y)}$. This ensures coverage is balanced across all true classes.

## 与其他知识的关系

→ thm-class-conditional-coverage (guarantees class-balanced coverage)
← thm-split-cp-coverage (extends standard CP)
→ def-conditional-coverage (achieves conditional coverage on $Y$)
↔ meth-group-balanced-cp (analogous but group is observed, class is not)
→ def-fsc-metric (FSC metric can evaluate per-class coverage)

## 来源引用

Angelopoulos & Bates (2022), Section 4.2, Equation (9); Proposition 2; cites Vovk (2012), Sadinle et al. (2019)
