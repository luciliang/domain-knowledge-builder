---
id: thm-conformal-risk-control
type: theorem
label: Theorem 2: Conformal Risk Control
source: angelopoulos2022
section: Section 4.3
tokens: 1000
created: 2026-06-24
---

## 精确表述

"Theorem 2 (Conformal Risk Control [Angelopoulos et al. 2022]). Suppose $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are an i.i.d. sample from some distribution. Further, suppose $\ell$ is a monotone function of $\lambda$, i.e., one satisfying

$$\ell(C_{\lambda_1}(x), y) \geq \ell(C_{\lambda_2}(x), y)$$

for all $(x, y)$ and $\lambda_1 \leq \lambda_2$. Then

$$\mathbb{E}[\ell(C_{\hat{\lambda}}(X_{\text{test}}), Y_{\text{test}})] \leq \alpha,$$

where $\hat{\lambda}$ is picked as in:

$$\hat{\lambda} = \inf\left\{\lambda : \hat{R}(\lambda) \leq \alpha - \frac{B - \alpha}{n}\right\},$$

and $\hat{R}(\lambda) = (\ell(C_\lambda(X_1), Y_1) + \ldots + \ell(C_\lambda(X_n), Y_n))/n$ is the empirical risk."

## 适用条件

1. i.i.d. calibration and test data
2. Loss function $\ell$ is bounded above by $B < \infty$
3. Loss function is non-increasing as a function of $\lambda$ (monotone)
4. Prediction set $C_\lambda(x)$ parameterized by $\lambda$, more conservative for larger $\lambda$

## 直觉解释

The algorithm picks the smallest $\lambda$ such that the empirical risk is slightly below $\alpha$ (adjusted by $B/n$). The monotonicity ensures the risk is controlled. The $B/n$ correction is analogous to the $(n+1)$ correction in standard conformal prediction.

## 与其他知识的关系

→ def-crc (P3's CRC definition; this theorem provides its theoretical foundation)
← def-split-conformal-prediction (CRC generalizes conformal prediction to arbitrary losses)
→ thm-split-cp-coverage (special case when $\ell$ = miscoverage loss)
→ meth-selective-classification (applied to selective classification)

## 来源引用

Angelopoulos & Bates (2022), Section 4.3, Theorem 2; cites Angelopoulos et al. (2022)
