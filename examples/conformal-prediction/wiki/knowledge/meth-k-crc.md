---
id: meth-k-crc
type: method
label: K-CRC (High-Dimensional Risk Control via K Groups)
source: teneggi2025
section: Section 2 (High-dimensional risk control), Eq (5)-(6), (PK)
tokens: 1200
created: 2026-06-23
---

## 精确表述

To address the limitation that using a single scalar $\lambda$ for all pixels inflates the mean interval length, K-CRC assigns each pixel to one of $K$ groups with shared statistics. Given a partition matrix $M \in \{0, 1\}^{d \times K}$ and a vector-valued parameter $\lambda_K = [\lambda_1, \ldots, \lambda_K] \in \mathbb{R}_{\geq 0}^K$ such that $\lambda = M\lambda_K \in \mathbb{R}_{\geq 0}^d$:

$$g_\lambda(y)_j = [\hat{q}_\alpha(y)_j - \lambda_j, \hat{q}_{1-\alpha}(y)_j + \lambda_j].$$

For a fixed anchor point $\tilde{\lambda}_K \in \mathbb{R}_{\geq 0}^K$, choosing:

$$\hat{\lambda} = \inf\left\{\lambda \in M\tilde{\lambda}_K + \omega\mathbf{1}_d, \omega \in \mathbb{R} : \frac{n_{\text{cal}}}{n_{\text{cal}}+1}\hat{\ell}_{\text{cal}}(\lambda) + \frac{1}{n_{\text{cal}}+1} \leq \epsilon\right\}$$

controls risk as in the standard CRC guarantee.

The anchor $\tilde{\lambda}_K$ is found by solving a convex optimization problem (PK):

$$\tilde{\lambda}_K = \arg\min_{\lambda_K \in \mathbb{R}_{\geq 0}^K} \sum_{k \in [K]} n_k \lambda_k \quad \text{s.t.} \quad \hat{\ell}_\gamma^{\text{opt}}(M\lambda_K) \leq \epsilon,$$

where $n_k$ is the number of pixels in group $k$, and $\ell_\gamma$ for $\gamma \in (0,1)$ is a convex upper-bound to $\ell_{01}$.

**Key constraint**: The calibration set $S_{\text{cal}}$ must be split into $S_{\text{opt}}$ (for solving PK) and $S_{\text{ecal}}$ (for finding $\hat{\lambda}$).

K-CRC 通过将像素分组并使用向量化的参数 $\lambda_K$ 来减少区间长度。每组共享一个调整参数，通过凸优化找到使总区间长度最小的锚点参数。

## 适用条件

- 分组矩阵 $M$ 不依赖于测量 $y$（固定分组）
- 校准集必须分成优化集 $S_{\text{opt}}$ 和校准集 $S_{\text{ecal}}$
- 凸上界 $\ell_\gamma$ 用于使优化可行

## 直觉解释

单一 $\lambda$ 对所有像素一视同仁，但不同区域的预测难度不同。K-CRC 将像素按某种统计量（如损失分位数）分成 K 组，每组有自己的 $\lambda_k$，从而在保证整体风险控制的同时减小平均区间长度。

## 与其他知识的关系

← def-teneggi2025-crc（K-CRC 基于 CRC 框架）
extends → meth-sem-crc（sem-CRC 将固定分组扩展为实例依赖的语义分组）
compares_with → meth-sem-crc（K-CRC 使用固定分组 vs. sem-CRC 使用语义分组）

## 来源引用

- Teneggi et al. 2025, Section 2, Equations (5)-(6), (PK)
- Original method: Teneggi et al. 2023 (ICML), for RCPS
