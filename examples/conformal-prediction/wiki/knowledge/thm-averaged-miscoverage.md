---
id: thm-averaged-miscoverage
type: theorem
label: Theorem 3: Averaged Conditional Miscoverage under Weak Conditions
source: min2026
section: Section 3.1
tokens: 1200
created: 2026-06-24
---

## 精确表述

Suppose Assumptions 1 and 3–6 hold. Assume further that the conditional densities $f_{s(\cdot,\cdot;Z_{n+1}')}|\phi(t)(\cdot)$ and $f_{s^\star}|\phi(t)(\cdot)$ are bounded below by $\underline{L}$ and above by $\overline{L}$ on their supports, for positive constants $\underline{L}$ and $\overline{L}$. Suppose also that $|s(X,Y;Z)| \leq M$ and $\underline{M} \leq w(x) \leq \overline{M}$ uniformly almost surely. Let $T_0, T_0' \sim P_T$ be independent copies of $T$. There exists a constant $C > 0$ such that

$$\mathbb{E}[\Pr(Y_{n+1} \in \hat{C}(X_{n+1})|\phi(T)) - (1-\alpha)]$$

$$\leq C\left[\delta_n^e + \delta_n(\varepsilon) + \varepsilon \mathbb{E}\|r_w\|_{P_T,p/(p-1)} + C\sqrt{n^{-1}\text{Pdim}(\mathcal{S})\log(n)}\right.$$

$$+ C\mathbb{E}\left[\{r_w(T_0)+1\}|q_{s^\star}(T_0) - q_{s^\star}(T_0')|\right]\right].$$

The averaged intrinsic conditional-mismatch error is $\mathbb{E}\{r_w(T_0)+1\}|q_{s^\star}(T_0) - q_{s^\star}(T_0')|$, and the score-estimation error is $\delta_n^e + \delta_n(\varepsilon) + \varepsilon\mathbb{E}\|r_w\|_{P_T,p/(p-1)}$.

## 适用条件

1. Assumptions 1 and 3–6 replace the pointwise Assumption 2 with averaged Assumption 5
2. Assumption 6: score class $\mathcal{S}$ has finite pseudo-dimension
3. Score-estimation error controllable on average w.r.t. $P_T$

## 直觉解释

This is the averaged (weaker) counterpart of the pointwise Theorem 2. The function class complexity enters through $\text{Pdim}(\mathcal{S})$ in the calibration error. The density ratio $r_w$ appears because calibration via w measures convergence under $\|\cdot\|_{P_{T,w},p}$ while the averaged target uses $\|\cdot\|_{P_T,p}$. This form is natural for methods like CC where the error is global rather than pointwise.

## 与其他知识的关系

← thm-three-term-decomposition（平均版本的点wise对应）
→ thm-cc-averaged（特化为 CC 的结果）
→ ins-method-comparison-table（Table 1 中 BatchGCP、CC 使用此平均框架）

## 来源引用

Min et al. (2026), Section 3.1, Theorem 3, Equation (7). arXiv:2605.11602v3.
