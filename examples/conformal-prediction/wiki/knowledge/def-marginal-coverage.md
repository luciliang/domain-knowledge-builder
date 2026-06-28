---
id: def-marginal-coverage
type: definition
label: Marginal Coverage
source: angelopoulos2022
section: Section 1
tokens: 700
created: 2026-06-24
---

## 精确表述

Marginal coverage is the property that the probability the prediction set contains the correct label is almost exactly $1 - \alpha$, where the probability is marginal (averaged) over the randomness in the calibration and test points:

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1 - \alpha.$$

As stated in the paper: "we call this property marginal coverage, since the probability is marginal (averaged) over the randomness in the calibration and test points."

## 适用条件

The property holds for any conformal prediction procedure (split, full, or any variant) as long as the exchangeability assumption is satisfied.

## 直觉解释

Marginal coverage guarantees that on average across all test points, at least $1-\alpha$ fraction will be correctly covered. It does NOT guarantee that coverage is maintained for specific subgroups or difficult inputs.

## 与其他知识的关系

← thm-split-cp-coverage (Theorem 1 guarantees marginal coverage)
↔ def-conditional-coverage (stronger property; marginal coverage allows all errors in one group)
→ thm-beta-coverage-distribution (coverage fluctuations follow Beta distribution)
→ thm-covariate-shift-coverage (covariate shift CP preserves marginal coverage under shift)
→ thm-distribution-drift-coverage (drift CP preserves approximate marginal coverage)
→ def-conformal-coverage (P3's definition; related concept for CRC framework)

## 来源引用

Angelopoulos & Bates (2022), Section 1, Equation (1); Section 3.1
