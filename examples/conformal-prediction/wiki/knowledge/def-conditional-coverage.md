---
id: def-conditional-coverage
type: definition
label: Conditional Coverage
source: angelopoulos2022
section: Section 3.1
tokens: 900
created: 2026-06-24
---

## 精确表述

"The adaptivity is typically formalized by asking for the conditional coverage property:

$$\mathbb{P}[Y_{\text{test}} \in C(X_{\text{test}}) | X_{\text{test}}] \geq 1 - \alpha."$$

"That is, for every value of the input $X_{\text{test}}$, we seek to return prediction sets with $1-\alpha$ coverage. This is a stronger property than the marginal coverage property in (1) that conformal prediction is guaranteed to achieve—indeed, in the most general case, conditional coverage is impossible to achieve."

## 适用条件

1. Conditional coverage requires $1-\alpha$ coverage for every specific value of $X_{\text{test}}$
2. In the most general case, conditional coverage is impossible to achieve (Vovk 2012, Lei & Wasserman)
3. Vanishing-width intervals are achievable if and only if the effective support size of $X_{\text{test}}$ is smaller than $n^2$

## 直觉解释

Marginal coverage means 90% overall, but all errors could happen in one subgroup (e.g., rare classes). Conditional coverage demands 90% coverage for every specific input or subgroup, distributing errors evenly. This is much stronger and generally impossible without additional assumptions.

## 与其他知识的关系

→ def-marginal-coverage (conditional coverage implies marginal coverage, but not vice versa)
← meth-aps (APS improves conditional coverage over standard CP)
← thm-conditional-coverage-impossible (conditional coverage is generally impossible)
→ def-fsc-metric (feature-stratified coverage measures conditional coverage approximation)
→ def-ssc-metric (size-stratified coverage measures conditional coverage approximation)
→ meth-group-balanced-cp (achieves conditional coverage for known groups)
→ meth-class-conditional-cp (achieves conditional coverage for known classes)

## 来源引用

Angelopoulos & Bates (2022), Section 3.1, Equation (7); Figure 10
