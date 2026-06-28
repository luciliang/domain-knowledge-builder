---
id: def-ho2020-forward-diffusion-process
type: definition
label: Forward Diffusion Process
source: ho2020
section: Section 2 (Background), Section 3.1
tokens: 750
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 88
  end_line: 120
  page: "2"
---

## 精确表述

扩散模型（diffusion model）的**前向过程**（forward process / diffusion process）是一个固定的（无可学习参数的）马尔可夫链 $q(x_{1:T}|x_0)$，它逐步向数据 $x_0 \sim q(x_0)$ 中添加高斯噪声：

$$q(x_{1:T}|x_0) := \prod_{t=1}^{T} q(x_t|x_{t-1}), \quad q(x_t|x_{t-1}) = \mathcal{N}(x_t;\, \sqrt{1-\beta_t}\, x_{t-1},\, \beta_t I)$$

其中 $\beta_1,\dots,\beta_T$ 是预先固定的**方差表（variance schedule）**，控制每步添加噪声的量。

记 $\alpha_t := 1 - \beta_t$，$\bar{\alpha}_t := \prod_{s=1}^{t} \alpha_s$。前向过程的一个关键性质是：任意时间步 $t$ 的样本 $x_t$ 可由 $x_0$ **闭式（closed form）**采样得到（Eq. 4）：

$$q(x_t|x_0) = \mathcal{N}(x_t;\, \sqrt{\bar{\alpha}_t}\, x_0,\, (1-\bar{\alpha}_t) I)$$

等价地，$x_t(x_0,\epsilon) = \sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1-\bar{\alpha}_t}\,\epsilon$，其中 $\epsilon \sim \mathcal{N}(0,I)$。

## 适用条件

- 噪声为高斯噪声，且每步方差 $\beta_t$ 为常数（论文中固定为常数，不通过重参数化学习，见 → meth-ho2020-variance-schedule）。
- $\beta_t$ 取较小值，使前向与反向过程具有近似相同的函数形式（→ def-ho2020-reverse-process）。
- 数据 $x_0$ 线性缩放到 $[-1,1]$（见 Section 3.3）。

## 直觉解释

前向过程是一个"加噪"过程：从干净图像 $x_0$ 出发，经 $T$ 步逐步添加微小高斯噪声，最终在 $x_T$ 处信号被完全破坏，接近纯高斯白噪声 $\mathcal{N}(0,I)$。因为每步都是线性高斯，多步叠加仍是高斯，所以可跳过中间步骤直接由 $x_0$ 算出任意 $x_t$——这正是高效训练的基础。

## 与其他知识的关系

→ 定义了 → def-ho2020-reverse-process 要反转的噪声过程。
→ 其闭式边际 → thm-ho2020-elbo-variational-bound（高效训练）和 → meth-ho2020-epsilon-prediction（重参数化）的基础。
→ 其条件后验 → def-ho2020-forward-posterior（训练目标中的 KL 项）。
← 由 → meth-ho2020-variance-schedule 参数化（β 表）。

## 来源引用

Ho et al. 2020, Section 2 (Background), Eqs. (1)-(2), (4)；Section 3.1。full-text.txt lines 88-120。
