---
id: thm-covariate-shift-marginal
type: theorem
label: Theorem 4: Marginal Coverage under Covariate Shift
source: min2026
section: Section 4.2
tokens: 800
created: 2026-06-24
---

## 精确表述

Suppose Assumption 7 holds (calibration from $P_{X,1} \times P_{Y|X}$, test from $P_{X,2} \times P_{Y|X}$, density ratio $r_X(x) = dP_{X,2}/dP_{X,1}(x)$ known). For $X \sim P_{X,1}$, define $W_X = \{w_0(\cdot) \geq 0 : \mathbb{E}\{w_0(X)|w_0\} = 1 \text{ and } \mathbb{E}\{w_0(x)\} = r_X(x) \text{ for all } x \in \mathcal{X}\}$. Then

$$1 - \alpha - \inf_{w_0 \in W_X} \mathbb{E}\{d_Z(w, w_0)\} \leq \Pr(Y_{n+1} \in \hat{C}(X_{n+1}))$$

$$\leq 1 - \alpha + \inf_{w_0 \in W_X} \mathbb{E}\{d_Z(w, w_0)\} + \mathbb{E}\{\hat{w}_{\max}(Z)\}.$$

Marginal coverage is guaranteed under covariate shift when $\mathbb{E}\{\bar{w}(x)\} = r_X(x)$ for all $x \in \mathcal{X}$.

## 适用条件

1. Assumption 7: known density ratio $r_X(x)$
2. Score permutation invariance

## 直觉解释

This extends Theorem 1 to covariate shift by replacing the normalization condition from 1 to $r_X(x)$. The key insight: w(x) = r_X(x) restores marginal coverage, but small conditional miscoverage further requires the weighted quantile to align with the conditional quantile — motivating combined density-ratio + localization approaches.

## 与其他知识的关系

← thm-marginal-coverage-weighted（i.i.d. 版本的协变量偏移推广）
→ meth-covariate-shift-conditional（指导条件覆盖方法设计）
→ def-conformal-coverage（在协变量偏移下保持边际覆盖）

## 来源引用

Min et al. (2026), Section 4.2, Theorem 4. arXiv:2605.11602v3.
