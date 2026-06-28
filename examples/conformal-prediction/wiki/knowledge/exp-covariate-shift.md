---
id: exp-covariate-shift
type: experiment
label: Conditional Methods under Covariate Shift (Synthetic)
source: min2026
section: Section 5.1.1, Table 2
tokens: 1200
created: 2026-06-24
---

## 精确表述

Experiments compare 11 conformal procedures under covariate shift ($X_{train} \sim N_d(0, I_d)$, $X_{test} \sim N_d(0, \sigma^2 I_d)$, $\sigma \in \{0.8, 1.0, 1.2\}$) with $d \in \{5, 10, 15, 20\}$, $n = 500$. Methods include five conditional methods (LCP, GLCP, CQR-LR, CQR-RF, CQR-LGB) without covariate-shift adjustment, their density-ratio-weighted counterparts, and standard WCP.

Key findings from Table 2 (n=500, d=10):
- Methods without covariate-shift adjustment can deviate substantially from nominal 90% marginal coverage when σ ≠ 1
- Density-ratio-weighted counterparts recover valid marginal coverage
- Most density-ratio-weighted conditional methods have smaller conditional miscoverage than WCP
- CQR-LR is less stable under complex DGPs due to linear misspecification
- Best performers include density-ratio-weighted GLCP and CQR-LGB

## 适用条件

Synthetic regression: $Y = \mu(X) + \epsilon(X)$, three DGPs with heteroscedastic noise. 50 repetitions, nominal coverage 1−α = 90%.

## 直觉解释

Experiments validate the theoretical guidance from Section 4.2: combining density-ratio correction with conditional adaptation yields better performance than WCP alone. The benefit of density-ratio weighting is clearest when σ deviates most from 1.0.

## 与其他知识的关系

← meth-covariate-shift-conditional（验证协变量偏移条件方法的理论指导）
← thm-covariate-shift-marginal（验证边际覆盖恢复）

## 来源引用

Min et al. (2026), Section 5.1.1, Table 2. arXiv:2605.11602v3.
