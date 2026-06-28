---
id: thm-group-balanced-coverage
type: theorem
label: Proposition 1: Group-Balanced CP Validity
source: angelopoulos2022
section: Section 4.1
tokens: 800
created: 2026-06-24
---

## 精确表述

"Proposition 1 (Error control guarantee for group-balanced conformal prediction). Suppose $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are an i.i.d. sample from some distribution. Then the set $C$ defined above satisfies the error control property in (8),"

where (8) is:

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}}) | X_{\text{test},1} = g) \geq 1 - \alpha, \text{ for all groups } g \in \{1, \ldots, G\}.$$

## 适用条件

1. $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are i.i.d.
2. Groups defined by discrete feature $X_{i,1}$
3. Each group has sufficient calibration samples

## 直觉解释

Within each group, the standard conformal argument applies—exchangeability ensures the test score falls below the group-specific quantile with probability at least $1-\alpha$. Since this holds for every group simultaneously, we get group-balanced coverage.

## 与其他知识的关系

→ meth-group-balanced-cp (this theorem guarantees the method's validity)
→ def-conditional-coverage (achieves conditional coverage for the known grouping)
← thm-split-cp-coverage (specialization of the standard CP guarantee)
→ thm-class-conditional-coverage (analogous guarantee for class-conditional setting)

## 来源引用

Angelopoulos & Bates (2022), Section 4.1, Proposition 1; cites Vovk (2012)
