---
id: meth-model-selection-cc
type: method
label: Conditional-Coverage-Oriented Model Selection
source: min2026
section: Section 4.1
tokens: 1200
created: 2026-06-24
---

## 精确表述

For a collection of candidate score functions $\mathcal{S}$, define $\hat{\zeta}_s(x, y; Z) = \mathbf{1}(s(x, y; Z) \leq q_s(Z;\alpha)) - (1-\alpha)$. The model selection criterion is a lack-of-fit statistic $L(s; Z)$ measuring violation of the conditional mean restriction $\mathbb{E}\{\hat{\zeta}_s(X, Y; Z) | Z, w, X = x\} = 0$.

The selected score and prediction set are:

$$\hat{s}^y = \arg\min_{s \in \mathcal{S}} L(s; Z^y),$$

$$\hat{C}_{Sel}(X_{n+1}) = \{y : \hat{s}^y(X_{n+1}, y; Z^y) \leq q_{\hat{s}^y}(Z^y; \alpha)\}.$$

If $L(s; Z^y)$ is permutation invariant, then marginal validity is preserved.

The concrete implementation uses the Tripathi & Kitamura (2003) localized conditional-moment statistic with kernel-based aggregation at multiple bandwidths.

## 适用条件

1. Candidate scores must be permutation invariant
2. Lack-of-fit statistic $L(s; Z^y)$ must be permutation invariant for marginal coverage preservation
3. Computationally requires evaluating $L(s; Z^y)$ for each trial value y (efficient approximation available per Section S5.3)

## 直觉解释

Model selection is reframed as comparing violations of a conditional mean restriction — a classical nonparametric lack-of-fit test perspective. The selection criterion explicitly favors scores better aligned with test-conditional validity, unlike efficiency-driven selection (EffSize) which picks by interval size. Experiments show AvgLoss/AvgRankLoss consistently select near-best conditional performers.

## 与其他知识的关系

← thm-three-term-decomposition（由三误差分解中的内在误差分量驱动）
→ exp-model-selection（在实验中验证）
↔ meth-sem-crc（与 P3 的 sem-CRC 方法比较：此方法不需要独立 hold-out 集合）

## 来源引用

Min et al. (2026), Section 4.1, Equation (8). arXiv:2605.11602v3.
