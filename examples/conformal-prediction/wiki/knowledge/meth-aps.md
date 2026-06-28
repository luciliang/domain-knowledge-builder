---
id: meth-aps
type: method
label: Adaptive Prediction Sets (APS)
source: angelopoulos2022
section: Section 2.1
tokens: 1200
created: 2026-06-24
---

## 精确表述

APS is a conformal procedure that produces prediction sets with smaller sizes for easy inputs and larger sizes for hard inputs. Following Romano, Sesia & Candès (2020) and Sadinle et al. (2019), the score function is defined as:

$$s(x, y) = \sum_{j=1}^{k} \hat{f}(x)_{\pi_j(x)}, \text{ where } y = \pi_k(x),$$

where $\pi(x)$ is the permutation of $\{1, \ldots, K\}$ sorting $\hat{f}(x)_{\text{test}}$ from most to least likely. The prediction set is:

$$C(x) = \{\pi_1(x), \ldots, \pi_k(x)\}, \text{ where } k = \sup \left\{k': \sum_{j=1}^{k'} \hat{f}(x)_{\pi_j(x)} < \hat{q} + 1\right\} + 1.$$

## 适用条件

1. Classification setting with $K$ classes
2. Pre-trained classifier with softmax outputs $\hat{f}(x) \in [0,1]^K$
3. Calibration data of $n$ i.i.d. pairs
4. $\hat{q}$ = quantile of calibration scores at level $\lceil(n+1)(1-\alpha)\rceil/n$

## 直觉解释

We greedily include classes from most to least likely until cumulative softmax exceeds a threshold. Unlike the simple "1 - softmax of true class" score, APS uses all softmax outputs, producing sets whose size naturally reflects the model's uncertainty. Hard inputs get larger sets; easy inputs get smaller sets.

## 与其他知识的关系

→ thm-split-cp-coverage (satisfies Theorem 1's marginal coverage guarantee)
→ def-conditional-coverage (better approximates conditional coverage than standard CP)
← def-split-conformal-prediction (APS is a specialization of split CP)
← def-fsc-metric (APS performance evaluated via FSC/SSC metrics)
← def-ssc-metric (APS performance evaluated via FSC/SSC metrics)
↔ meth-cqr (different CP method for regression)

## 来源引用

Angelopoulos & Bates (2022), Section 2.1, Equation (3); Figures 3–4; cites Romano, Sesia & Candès (2020), Sadinle et al. (2019)
