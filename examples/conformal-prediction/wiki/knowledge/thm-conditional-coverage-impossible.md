---
id: thm-conditional-coverage-impossible
type: theorem
label: Conditional Coverage Impossibility
source: angelopoulos2022
section: Section 3.1
tokens: 800
created: 2026-06-24
---

## 精确表述

"In the most general case, conditional coverage is impossible to achieve." This result was established by Vovk (2012) and refined by Lei & Wasserman (2014) and Barber et al. (2021). Furthermore:

"vanishing-width intervals are achievable if and only if the effective support size of the distribution of $X_{\text{test}}$ is smaller than the square of the sample size."

## 适用条件

1. No assumptions on the distribution of $(X, Y)$
2. The score function must produce finite-width prediction intervals
3. The result holds for arbitrary continuous distributions

## 直觉解释

To have $1-\alpha$ coverage for every single $x$, the prediction set must adapt perfectly to the local geometry of the data distribution. Without knowing this geometry a priori, this is impossible—there simply aren't enough data points to estimate the local behavior everywhere.

## 与其他知识的关系

→ def-conditional-coverage (explains why this property is generally unattainable)
← def-marginal-coverage (marginal coverage IS achievable, conditional is not)
→ def-fsc-metric (practical metric to measure how close we get)
→ def-ssc-metric (practical metric to measure how close we get)
→ meth-angelopoulos2022-aps (practical method that approximates conditional coverage)

## 来源引用

Angelopoulos & Bates (2022), Section 3.1; cites Vovk (2012), Lei & Wasserman (2014), Barber et al. (2021), Lee & Barber (2021)
