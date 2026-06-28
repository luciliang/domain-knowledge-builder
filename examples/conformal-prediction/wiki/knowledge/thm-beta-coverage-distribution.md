---
id: thm-beta-coverage-distribution
type: theorem
label: Beta Distribution of Coverage (Vovk 2012)
source: angelopoulos2022
section: Section 3.2
tokens: 1000
created: 2026-06-24
---

## 精确表述

"The distribution of coverage has an analytic form, first introduced by Vladimir Vovk in [14]:

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}}) | \{(X_i, Y_i)\}_{i=1}^n) \sim \text{Beta}(n + 1 - l, l),$$

where $l = \lfloor(n+1)\alpha\rfloor$."

The conditional expectation is the coverage with an infinite validation set, holding the calibration data fixed. Furthermore, for finite validation, the empirical coverage over $n_{\text{val}}$ points is beta-binomial:

$$C_j \sim \frac{1}{n_{\text{val}}} \text{Binom}(n_{\text{val}}, \mu), \text{ where } \mu \sim \text{Beta}(n + 1 - l, l).$$

## 适用条件

1. $n$ calibration points, i.i.d. with test point
2. $l = \lfloor(n+1)\alpha\rfloor$
3. The calibration data is held fixed

## 直觉解释

The coverage conditional on a fixed calibration set is random—it depends on which specific calibration points were sampled. The Beta distribution quantifies these fluctuations. Larger $n$ makes the distribution tighter around $1-\alpha$. For $n=1000$ with $\alpha=0.1$, coverage is typically between 0.88 and 0.92.

## 与其他知识的关系

→ def-marginal-coverage (explains fluctuations around the marginal coverage guarantee)
→ thm-split-cp-coverage (complements Theorem 1 by characterizing finite-sample variability)
→ def-fsc-metric (beta distribution helps set expectations for FSC evaluation)
→ def-ssc-metric (beta distribution helps set expectations for SSC evaluation)

## 来源引用

Angelopoulos & Bates (2022), Section 3.2, Equation after "namely"; Figure 11; Table 1; Appendix C; cites Vovk (2012)
