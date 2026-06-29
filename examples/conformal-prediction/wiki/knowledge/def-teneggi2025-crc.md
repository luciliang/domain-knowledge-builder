---
id: def-teneggi2025-crc
type: definition
label: Conformal Risk Control (CRC)
source: teneggi2025
section: Section 2 (Conformal risk control)
tokens: 900
created: 2026-06-23
---

## 精确表述

Conformal risk control (CRC) [Angelopoulos et al., 2024] post-processes a fixed set predictor $g$ to bound the expectation of its error. Given a family of nested predictors $\{g_\lambda\}_{\lambda \in \mathbb{R}_{\geq 0}}$ with

$$g_\lambda(y)_j = [\hat{q}_\alpha(y)_j - \lambda, \hat{q}_{1-\alpha}(y)_j + \lambda],$$

and a bounded, non-increasing loss function $\ell(g_\lambda(y), x)$, CRC seeks to find the parameter $\hat{\lambda}$ that controls the loss. Specifically, given a calibration set $S_{\text{cal}} = \{(X^{(i)}, Y^{(i)})\}_{i=1}^{n_{\text{cal}}}$ and a test point $(X, Y)$ of exchangeable observations independent of $g$, the choice of

$$\hat{\lambda} = \inf\left\{\lambda \in \mathbb{R}_{\geq 0} : \frac{n_{\text{cal}}}{n_{\text{cal}}+1} \hat{\ell}_{\text{cal}}(\lambda) + \frac{1}{n_{\text{cal}}+1} \leq \epsilon\right\}$$

guarantees that

$$\mathbb{E}[\ell_{01}(g_{\hat{\lambda}}(Y), X)] \leq \epsilon,$$

where the expectation is taken over $S_{\text{cal}}$ and $(X, Y)$.

The specific loss function used is the proportion of ground-truth pixels falling outside their intervals:

$$\ell_{01}(g_\lambda(y), x) = \frac{1}{d} \sum_{j \in [d]} \mathbb{1}\{x_j \notin g_\lambda(y)_j\},$$

which is monotonically non-increasing in $\lambda$ and bounded by 1.

CRC 的目标是通过后处理一个固定的集合预测器，使其误差的期望被控制在不超过用户指定的容差 $\epsilon > 0$。它不需要假设预测分布，适用于黑箱系统。

## 适用条件

- 校准集 $S_{\text{cal}}$ 和测试点 $(X, Y)$ 是可交换的 (exchangeable) 观测
- 预测器 $g$ 与校准集和测试点独立
- 损失函数 $\ell$ 必须有界且关于 $\lambda$ 单调非递增
- 容差 $\epsilon > 0$

## 直觉解释

CRC 的核心思想是：给定一个初始的预测区间（如分位数回归的输出），通过在校准数据上找到一个统一的调整参数 $\lambda$，使得"真实值落在区间外"的比例不超过 $\epsilon$。这不需要任何分布假设，只需要可交换性。

## 与其他知识的关系

→ def-conformal-coverage（CRC 保证风险控制）
← def-quantile-regression（分位数回归提供初始集合预测器）
→ meth-k-crc（K-CRC 将 CRC 扩展到高维）
→ meth-sem-crc（sem-CRC 将 CRC 扩展到语义级别）

## 来源引用

- Teneggi et al. 2025, Section 2, Equations (1)-(4)
- Original CRC: Angelopoulos et al. 2024 (ICLR), Theorem 1
