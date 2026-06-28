---
id: def-ssc-metric
type: definition
label: Size-Stratified Coverage (SSC) Metric
source: angelopoulos2022
section: Section 3.1
tokens: 800
created: 2026-06-24
---

## 精确表述

The SSC metric measures worst-case coverage across bins of prediction set sizes:

$$\text{SSC metric}: \min_{g \in \{1,...,G\}} \frac{1}{|I_g|} \sum_{i \in I_g} \mathbf{1}\{Y_i^{(\text{val})} \in C(X_i^{(\text{val})})\},$$

where $I_g \subset \{1, \ldots, n_{\text{val}}\}$ is the set of observations falling in bin $g$, and bins $B_1, \ldots, B_G$ discretize the possible cardinalities of $C(x)$. If conditional coverage were achieved, this would be $1-\alpha$.

## 适用条件

1. The user must define $G$ bins for the set sizes $|C(x)|$
2. No need for pre-defined discrete features (general-purpose metric)
3. Validation set of size $n_{\text{val}}$

## 直觉解释

This checks whether prediction sets of the same size have equal coverage. If small sets (presumably easy inputs) have high coverage but large sets (hard inputs) have low coverage, the SSC metric will be low, revealing poor adaptivity.

## 与其他知识的关系

→ def-conditional-coverage (SSC measures approximation to conditional coverage)
↔ def-fsc-metric (SSC is size-based, FSC is feature-based)
← meth-aps (APS performance can be evaluated with SSC)
← meth-group-balanced-cp (group-balanced CP aims to improve SSC)

## 来源引用

Angelopoulos & Bates (2022), Section 3.1; cites Romano, Sesia & Candès (2020)
