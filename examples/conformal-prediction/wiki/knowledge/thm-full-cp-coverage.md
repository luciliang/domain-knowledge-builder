---
id: thm-full-cp-coverage
type: theorem
label: Full Conformal Prediction Coverage Guarantee
source: angelopoulos2022
section: Section 3
tokens: 1200
created: 2026-06-25
---

## 精确表述

Full (transductive) conformal prediction computes the conformity score for every possible test label $y$ by refitting on the augmented set $\{(X_1,Y_1),\ldots,(X_n,Y_n),(X_{\text{test}},y)\}$. The prediction set is:

$$C(X_{\text{test}}) = \{y : s(X_{\text{test}}, y) \leq q^+(n,\alpha)\}$$

where $q^+(n,\alpha)$ is the $\lceil(n+1)(1-\alpha)\rceil$-th smallest value among $s(X_1,Y_1),\ldots,s(X_n,Y_n),s(X_{\text{test}},y)$.

The coverage guarantee is identical to split CP:

$$\mathbb{P}(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1 - \alpha$$

with the upper bound $1 - \alpha + 1/(n+1)$, but full CP uses all $n$ data points for both fitting and calibration (no train/calibration split needed).

## 适用条件

1. $(X_1, Y_1), \ldots, (X_n, Y_n), (X_{\text{test}}, Y_{\text{test}})$ are exchangeable
2. The conformity score function $s(x, y)$ can be computed for any $(x, y)$ pair, including with the fitted model
3. The fitted model must be refit for each candidate $y$ — **computational cost $O(n)$ model refits per test point**

## 直觉解释

Full CP tests each candidate label $y$ by asking: "If $y$ were the true label, how well would it conform to the observed data?" Because the augmented set (including $(X_{\text{test}}, y)$) is exchangeable when $y = Y_{\text{test}}$, the rank of $s(X_{\text{test}}, y)$ among all $n+1$ scores is uniform, giving exact coverage. Split CP trades statistical efficiency (uses only $n/2$ calibration points) for computational efficiency (no refitting).

## 与其他知识的关系

← def-split-conformal-prediction (split CP is the computationally efficient approximation)
→ thm-split-cp-coverage (split CP inherits the same coverage guarantee)
→ def-marginal-coverage (guarantees marginal coverage)
→ thm-covariate-shift-coverage (weighted variant extends full CP to covariate shift)

## 来源引用

Angelopoulos & Bates (2022), Section 3, "Full conformal prediction"; Vovk, Gammerman & Saunders (2005)
