---
id: meth-sem-crc-per-organ
type: method
label: "sem-CRC̄ (Per-Organ Risk Control)"
source: teneggi2025
section: Section 3 (Controlling risk for each organ), Eq (11)-(12)
tokens: 1000
created: 2026-06-23
---

## 精确表述

Clinical tasks may require different organs to have the same level of reconstruction accuracy, but $\hat{\lambda}_{\text{sem}}$ may overcover easy-to-reconstruct organs while undercovering others. The per-organ variant, sem-CRC̄, controls risk for each organ individually.

Define the organ-specific loss:

$$\ell_{01}^k(g_{\lambda_{\text{sem}}}(y), x) = \frac{1}{|S_k(y)|} \sum_{j \in S_k(y)} \mathbb{1}\{x_j \notin g_{\lambda_{\text{sem}}}(y)_j\},$$

the proportion of pixels in organ $k$ that fall outside their intervals. Let $e_k$ be the $k$-th standard basis vector. The choice of $\hat{\lambda}_{\text{sem}} \in \mathbb{R}_{\geq 0}^K$ with

$$\hat{\lambda}_{\text{sem},j} = \inf\left\{\lambda \in \mathbb{R}_{\geq 0} : \frac{n_{\text{cal}}}{n_{\text{cal}}+1}\hat{\ell}_{k,\text{cal}}^{01}(\lambda_{\text{sem}} + \lambda e_k) + \frac{1}{n_{\text{cal}}+1} \leq \epsilon\right\}$$

provides risk control for each organ:

$$\mathbb{E}[\ell_{01}^k(g_{\hat{\lambda}_{\text{sem}}}(Y), X)] \leq \epsilon, \quad k = 1, \ldots, K.$$

This follows by applying Proposition 1 to each dimension of $\hat{\lambda}_{\text{sem}}$.

**Note**: This is different from multiple risk control with one scalar $\lambda$ as in [Angelopoulos et al. 2024]. The equivalent for RCPS requires multiple hypothesis testing correction for uniform coverage.

sem-CRC̄ 是 sem-CRC 的特化版本，保证每个器官（而非整体）的风险都不超过 $\epsilon$。代价是平均区间长度会增加。

## 适用条件

- 同 sem-CRC 的条件
- 每个器官独立控制风险，容差均为 $\epsilon$
- 需要逐器官校准，计算量更大
- 对于 RCPS 框架，需要多重假设检验校正

## 直觉解释

标准 sem-CRC 只保证所有像素的平均风险达标，可能"牺牲"难以重建的器官（用容易重建的器官的低不确定性来"补偿"）。sem-CRC̄ 强制每个器官都达到相同的风险水平，更公平但代价是整体区间更长。

## 与其他知识的关系

← thm-sem-crc-validity（通过将 Proposition 1 应用到每个维度得到）
specializes → meth-sem-crc（sem-CRC̄ 是 sem-CRC 的逐器官特化）
compares_with → meth-sem-crc（sem-CRC̄ 的区间更长但更公平）

## 来源引用

- Teneggi et al. 2025, Section 3, Equations (11)-(12)
