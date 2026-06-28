---
id: thm-class-conditional-coverage
type: theorem
label: Proposition 2: Class-Conditional CP Validity
source: angelopoulos2022
section: Section 4.2
tokens: 700
created: 2026-06-24
---

## 精确表述

"Proposition 2 (Error control guarantee for class-balanced conformal prediction). Suppose $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are an i.i.d. sample from some distribution. Then the set $C$ defined above satisfies the error control property in (9),"

where (9) is:

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}}) | Y_{\text{test}} = y) \geq 1 - \alpha, \text{ for all classes } y \in \{1, \ldots, K\}.$$

## 适用条件

1. $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are i.i.d.
2. Classification setting
3. Sufficient calibration examples per class

## 直觉解释

Conditioning on the true class, the score for a test point from class $y$ is exchangeable with the calibration scores for class $y$. Thus the standard conformal argument applies within each class.

## 与其他知识的关系

→ meth-class-conditional-cp (this theorem guarantees the method's validity)
→ def-conditional-coverage (achieves conditional coverage conditioned on $Y$)
← thm-split-cp-coverage (specialization)
→ thm-group-balanced-coverage (analogous guarantee for different grouping)

## 来源引用

Angelopoulos & Bates (2022), Section 4.2, Proposition 2; cites Vovk (2012), Sadinle et al. (2019)
