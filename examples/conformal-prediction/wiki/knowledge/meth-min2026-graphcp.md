---
id: meth-min2026-graphcp
type: method
label: GraphCP: Community-Conditional Conformal Prediction on Graphs
source: min2026
section: Section 4.3.1
tokens: 1300
created: 2026-06-24
---

## 精确表述

Given graph data $Z = \{(W_i, X_i, Y_i)\}_{i=1}^{n+1}, A$ with community structure, the within-community rank score for node $i$ is:

$$s(X_i, Y_i; Z) = \frac{\sum_{j=1}^{n+1} \mathbf{1}(\hat{\sigma}(A)_j = \hat{\sigma}(A)_i \text{ and } v(X_j, Y_j; Z) \leq v(X_i, Y_i; Z))}{\sum_{j=1}^{n+1} \mathbf{1}(\hat{\sigma}(A)_j = \hat{\sigma}(A)_i)}.$$

The GraphCP prediction set is:

$$\hat{C}_{GraphCP}(X_{n+1}) = \left\{y : s(X_{n+1}, y; Z^y) \leq Q\left(1-\alpha; \frac{1}{n+1}\sum_{i=1}^n \delta_{s(X_i,Y_i;Z^y)} + \delta_\infty\right)\right\}.$$

The community-conditional coverage target is $\Pr(Y_{n+1} \in \hat{C}_{GraphCP}(X_{n+1})|\sigma(W_{n+1}) = I)$ for each community $I \in [n_{comm}]$.

## 适用条件

1. Joint exchangeability of graph data (permutation invariance)
2. Community detection algorithm with permutation-equivariant output
3. Non-overlapping communities with $p_{comm} = \inf_{I} \Pr(\sigma(W) = I) > 0$
4. Consistent community recovery (Assumption 10)

## 直觉解释

Within-community ranking removes community-level heterogeneity in the base score distribution, analogous to how CQR uses quantile regression to remove conditional heterogeneity. When communities are correctly recovered and the base score converges to its oracle, the intrinsic conditional-mismatch error vanishes (the oracle rank score has the same conditional distribution across communities).

## 与其他知识的关系

← thm-symmpi-conditional（在 SymmPI 条件覆盖框架下分析）
→ thm-community-conditional（由 Theorem 7 提供理论保证）
→ exp-toloker-graph（在真实图数据集上验证）
→ meth-sem-crc（与 P3 的 sem-CRC 比较：都做子群体覆盖，但 GraphCP 针对图结构）

## 来源引用

Min et al. (2026), Section 4.3.1. arXiv:2605.11602v3.
