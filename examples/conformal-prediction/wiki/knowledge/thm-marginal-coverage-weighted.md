---
id: thm-marginal-coverage-weighted
type: theorem
label: Theorem 1: Marginal Coverage of Weighted CP
source: min2026
section: Section 2
tokens: 1100
created: 2026-06-24
---

## 精确表述

Suppose Assumption 1 holds. For $X \sim P_X$, define

$$W_X = \{w_0(\cdot) \geq 0 : \mathbb{E}\{w_0(X)|w_0\} = 1 \text{ and } \mathbb{E}\{w_0(x)\} = 1 \text{ for all } x \in \mathcal{X}\},$$

where $\mathbb{E}\{w_0(X)|w_0\}$ is the expectation over $X \sim P_X$, and $\mathbb{E}\{w_0(x)\}$ is the expectation over the possible randomness of $w_0$ for a fixed $x \in \mathcal{X}$. Then

$$1 - \alpha - \inf_{w_0 \in W_X} \mathbb{E}\{d_Z(w, w_0)\} \leq \Pr(Y_{n+1} \in \hat{C}(X_{n+1}))$$

$$\leq 1 - \alpha + \inf_{w_0 \in W_X} \mathbb{E}\{d_Z(w, w_0)\} + \mathbb{E}\{\hat{w}_{\max}(Z)\},$$

where $d_Z(w, w_0) = \sum_{j=1}^{n+1}\sum_{i=1}^{n+1} w(X_i)[\sum_{i=1}^{n+1} w(X_j)]^{-1} - \sum_{i=1}^{n+1} w_0(X_i)[\sum_{i=1}^{n+1} w_0(X_i)]^{-1}$.

## 适用条件

1. Assumption 1 (i.i.d. + permutation invariance)
2. Weight function w(x) must satisfy that $w_0 \in W_X$ exists such that the gap is small
3. When w(·) ≡ 1 and no ties: classical full-conformal marginal coverage $[1-\alpha, 1-\alpha+1/(n+1)]$

## 直觉解释

The class $W_X$ collects normalized weighting schemes whose average normalized mass per covariate value is one — these preserve label symmetry needed for marginal validity. The term $d_Z(w, w_0)$ measures how far the actual normalized weights deviate from an admissible marginally valid scheme. RLCP achieves $\mathbb{E}\{\bar{w}(x)\} = 1$ for all x (hence valid marginal coverage), while BaseLCP does not.

## 与其他知识的关系

← def-unified-cp-framework（基于统一框架建立）
→ def-conformal-coverage（推广标准边际覆盖保证）
→ thm-three-term-decomposition（为条件覆盖分析提供边际覆盖基线）

## 来源引用

Min et al. (2026), Section 2, Theorem 1. arXiv:2605.11602v3.
