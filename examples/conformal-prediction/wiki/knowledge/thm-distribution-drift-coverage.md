---
id: thm-distribution-drift-coverage
type: theorem
label: Theorem 4: Conformal Prediction Under Distribution Drift
source: angelopoulos2022
section: Section 4.6
tokens: 1100
created: 2026-06-24
---

## 精确表述

"Theorem 4 (Conformal prediction under distribution drift [Barber et al. 2022]). Suppose $\epsilon_i = d_{\text{TV}}((X_i, Y_i), (X_{\text{test}}, Y_{\text{test}}))$. Then the choice of $C$ above satisfies

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1 - \alpha - 2\sum_{i=1}^n \tilde{w}_i \epsilon_i."$$

The weighted quantile uses weight schedule $w_1, \ldots, w_n$ with normalized weights $\tilde{w}_i = w_i / (w_1 + \ldots + w_n + 1)$.

## 适用条件

1. Calibration data drawn from different distributions $\{P_i\}_{i=1}^n$
2. Test point drawn from $P_{\text{test}}$
3. $\epsilon_i$ = total variation distance between $P_i$ and $P_{\text{test}}$
4. Weight schedule available (e.g., rolling window or exponential decay)

## 直觉解释

Old or dissimilar data points get low weights, reducing their contribution to the quantile. The coverage loss is bounded by $2\sum \tilde{w}_i \epsilon_i$—when drift is small or old points are discounted, the loss is negligible. When there is no drift ($\epsilon_i = 0$), there is no loss regardless of weights.

## 与其他知识的关系

→ def-marginal-coverage (provides approximate marginal coverage under drift)
← thm-split-cp-coverage (extends to distribution drift)
← thm-covariate-shift-coverage (special case when drift is a known covariate shift)
→ thm-beta-coverage-distribution (effective sample size $n_{\text{eff}}$ affects variance)

## 来源引用

Angelopoulos & Bates (2022), Section 4.6, Theorem 4; cites Barber et al. (2022)
