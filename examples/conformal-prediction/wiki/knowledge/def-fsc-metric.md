---
id: def-fsc-metric
type: definition
label: Feature-Stratified Coverage (FSC) Metric
source: angelopoulos2022
section: Section 3.1
tokens: 800
created: 2026-06-24
---

## 精确表述

The FSC metric measures the worst-case coverage across $G$ groups defined by a discrete feature:

$$\text{FSC metric}: \min_{g \in \{1,...,G\}} \frac{1}{|I_g|} \sum_{i \in I_g} \mathbf{1}\{Y_i^{(\text{val})} \in C(X_i^{(\text{val})})\},$$

where $I_g \subset \{1, \ldots, n_{\text{val}}\}$ is the set of observations where the discrete feature takes value $g$. If conditional coverage were achieved, this would be $1-\alpha$, and values farther below $1-\alpha$ indicate greater violation.

## 适用条件

1. A discrete feature $X_{i,1}$ taking values in $\{1, \ldots, G\}$
2. For continuous features, bin them into $G$ categories
3. Validation set of size $n_{\text{val}}$

## 直觉解释

This metric checks whether prediction sets have equal coverage across different groups (e.g., race, age bins). It directly measures the worst subgroup's coverage—if one group is severely under-covered, the FSC metric will be low.

## 与其他知识的关系

→ def-conditional-coverage (FSC measures approximation to conditional coverage)
↔ def-ssc-metric (FSC is feature-based, SSC is set-size-based)
← meth-angelopoulos2022-aps (APS performance can be evaluated with FSC)
← meth-group-balanced-cp (group-balanced CP aims to improve FSC)
← meth-class-conditional-cp (class-conditional CP aims to improve per-class FSC)

## 来源引用

Angelopoulos & Bates (2022), Section 3.1
