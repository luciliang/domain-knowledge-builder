---
id: def-unified-cp-framework
type: definition
label: Unified CP Framework via Weighted Conformal Quantiles
source: min2026
section: Section 2
tokens: 900
created: 2026-06-24
---

## 精确表述

Given a conformity score of the form s(x, y; z), the unified prediction set is:

$$\hat{C}(X_{n+1}) = \{y : s(X_{n+1}, y; Z^y) \leq q(Z^y; \alpha)\},$$

where the "weighted" conformal quantile is:

$$q(Z^y; \alpha) = Q\left(1 - \alpha; \frac{\sum_{i=1}^{n+1} w(X_i)}{\sum_{i=1}^{n+1} w(X_i) \delta_{s(X_i,Y_i;Z^y)}} + w(X_{n+1})\delta_\infty\right),$$

and w(x) can be either a fixed or a random function.

## 适用条件

1. Assumption 1: (i) calibration pairs and test pair are i.i.d. from $P_{X \times Y|X}$; (ii) score s(x, y; z) is permutation invariant in calibration data.
2. w(x) ≥ 0 for all x.

## 直觉解释

This formulation unifies two methodological routes to conditional coverage: score-based methods (CQR, DCP, GLCP) use w(·) ≡ 1 with data-dependent scores, while calibration-based methods (LCP, RLCP, CC) use different weighting schemes w(·). The weight function encodes how localization or correction is applied during calibration.

## 与其他知识的关系

→ thm-marginal-coverage-weighted（保证边际覆盖）
→ thm-three-term-decomposition（支撑条件覆盖误覆盖分解）
↔ def-conformal-coverage（推广了标准共形覆盖的定义）

## 来源引用

Min et al. (2026), Section 2, Equation (2). arXiv:2605.11602v3.
