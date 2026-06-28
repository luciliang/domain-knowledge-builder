---
id: thm-outlier-detection-guarantee
type: theorem
label: Proposition 3: Outlier Detection Error Control
source: angelopoulos2022
section: Section 4.4
tokens: 700
created: 2026-06-24
---

## 精确表述

"Proposition 3 (Error control guarantee for outlier detection). Suppose $X_1, \ldots, X_n, X_{\text{test}}$ are an i.i.d. sample from some distribution. Then the set $C$ defined above satisfies the error control property in (14),"

where (14) is:

$$\mathbb{P}(C(X_{\text{test}}) = \text{outlier}) \leq \alpha.$$

## 适用条件

1. $X_1, \ldots, X_n, X_{\text{test}}$ are i.i.d. from the clean distribution
2. Score function $s$ maps features to reals

## 直觉解释

By exchangeability, the test score $s(X_{\text{test}})$ is equally likely to fall between the calibration scores. At most $1-\alpha$ fraction of it should exceed the quantile threshold, bounding false positives.

## 与其他知识的关系

→ meth-outlier-detection-cp (guarantees the method's validity)
← thm-split-cp-coverage (specialization to unsupervised outlier detection)

## 来源引用

Angelopoulos & Bates (2022), Section 4.4, Proposition 3
