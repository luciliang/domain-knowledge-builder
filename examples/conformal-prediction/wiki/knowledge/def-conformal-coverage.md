---
id: def-conformal-coverage
type: definition
label: Conformal Risk Control Guarantee
source: teneggi2025
section: Section 2, Eq (3)-(4)
tokens: 600
created: 2026-06-23
---

## 精确表述

For any tolerance $\epsilon > 0$, the CRC procedure selects $\hat{\lambda}$ as in Equation (3):

$$\hat{\lambda} = \inf\left\{\lambda \in \mathbb{R}_{\geq 0} : \frac{n_{\text{cal}}}{n_{\text{cal}}+1} \hat{\ell}_{\text{cal}}(\lambda) + \frac{1}{n_{\text{cal}}+1} \leq \epsilon\right\}$$

which guarantees risk control:

$$\mathbb{E}[\ell_{01}(g_{\hat{\lambda}}(Y), X)] \leq \epsilon,$$

where the expectation is taken over $S_{\text{cal}}$ and $(X, Y)$.

This is the distribution-free guarantee: the expected proportion of ground-truth pixels falling outside their conformalized intervals is bounded by $\epsilon$ with high probability, without any distributional assumptions beyond exchangeability.

即：在可交换性假设下，CRC 选择的参数 $\hat{\lambda}$ 保证期望损失（真实值落在区间外的比例）不超过用户指定的容差 $\epsilon$。

## 适用条件

- Exchangeability of calibration and test data
- Loss function bounded and non-increasing in $\lambda$
- Predictor $g$ independent of calibration/test data

## 直觉解释

这个保证的关键在于：校准数据上的经验损失（乘以 $n_{\text{cal}}/(n_{\text{cal}}+1)$）加上一个修正项 $1/(n_{\text{cal}}+1)$ 不超过 $\epsilon$ 时，就能保证在新测试点上的期望损失也不超过 $\epsilon$。那个 $1/(n_{\text{cal}}+1)$ 项是有限样本校正。

## 与其他知识的关系

← def-crc（CRC 定义推出了这个保证）
→ thm-sem-crc-validity（sem-CRC 的有效性命题扩展了这个保证）
→ meth-k-crc（K-CRC 同样提供此保证）

## 来源引用

- Teneggi et al. 2025, Section 2, Equations (3)-(4)
- Angelopoulos et al. 2024, Theorem 1
