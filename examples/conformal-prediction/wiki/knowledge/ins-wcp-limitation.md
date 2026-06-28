---
id: ins-wcp-limitation
type: insight
label: WCP Restores Marginal but Not Conditional Coverage under Covariate Shift
source: min2026
section: Section S2.3
tokens: 700
created: 2026-06-24
---

## 精确表述

From Corollary S8: WCP's test-conditional miscoverage bound is

$$\Pr(Y_{n+1} \in \hat{C}_{WCP}(X_{n+1})|X_{n+1} = t) - (1-\alpha) \leq C[\delta_{tr} + n^{-1/2}\sqrt{\log(n)} + |Q(1-\alpha; F_{s^\star|X=t}) - Q(1-\alpha; F_{r_X \circ s^\star})|].$$

The intrinsic conditional-mismatch error $|Q(1-\alpha; F_{s^\star|X=t}) - Q(1-\alpha; F_{r_X \circ s^\star})|$ is generally nonzero for generic pre-trained scores.

"The weight $r_X(\cdot)$ restores marginal validity under covariate shift, but small test-conditional miscoverage further requires this weighted oracle quantile to align with the target conditional quantile."

## 适用条件

WCP with known density ratio, generic pre-trained score.

## 直觉解释

Density-ratio weighting in WCP corrects the marginal calibration distribution toward the test covariate distribution, ensuring marginal coverage. However, it does not address the fundamental gap between conditional and marginal quantiles. Combining WCP's density-ratio correction with conditional adaptation (localization or score-based methods) is necessary for small conditional miscoverage.

## 与其他知识的关系

← thm-covariate-shift-marginal（WCP 基于该定理的边际保证）
← def-three-errors（内在误差是 WCP 的瓶颈）
→ meth-covariate-shift-conditional（引导设计更好的条件方法）

## 来源引用

Min et al. (2026), Section S2.3, Corollary S8 and Analysis. arXiv:2605.11602v3.
