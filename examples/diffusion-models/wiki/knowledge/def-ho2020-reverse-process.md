---
id: def-ho2020-reverse-process
type: definition
label: Reverse Generative Process
source: ho2020
section: Section 2 (Background), Section 3.2
tokens: 700
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 88
  end_line: 97
  page: "2"
---

## 精确表述

扩散模型是一个潜变量模型，其生成过程为**反向过程**（reverse process）$p_\theta(x_{0:T})$，定义为一条从高斯先验出发、由学习到的高斯转移构成的马尔可夫链：

$$p_\theta(x_0) := \int p_\theta(x_{0:T})\, dx_{1:T}$$

$$p_\theta(x_{0:T}) := p(x_T) \prod_{t=1}^{T} p_\theta(x_{t-1}|x_t), \quad p(x_T) = \mathcal{N}(x_T;\, 0, I)$$

其中每个反向转移取为高斯条件分布：

$$p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1};\, \mu_\theta(x_t, t),\, \Sigma_\theta(x_t, t))$$

$\mu_\theta$ 和 $\Sigma_\theta$ 由神经网络参数化（参数在所有时间步 $t$ 上共享）。论文将 $\Sigma_\theta(x_t,t) = \sigma_t^2 I$ 设为与时间有关的常数（不学习，见 → meth-ho2020-variance-schedule），只学习均值 $\mu_\theta$。

## 适用条件

- 反向过程转移取为高斯；当 $\beta_t$ 较小时前向过程也是高斯条件分布，二者函数形式近似一致，故高斯条件足以表达反向过程。
- 起点先验 $p(x_T) = \mathcal{N}(0,I)$，要求前向过程在 $x_T$ 处几乎完全破坏信号（$D_{KL}(q(x_T|x_0)\,\|\,\mathcal{N}(0,I)) \approx 0$）。

## 直觉解释

反向过程是前向加噪过程的"逆运算"：从纯噪声 $x_T$ 出发，逐步去噪，最终生成干净样本 $x_0$。由于不知道真实的反向转移，用神经网络学习它（用变分推断训练，见 → thm-ho2020-elbo-variational-bound）。把转移限制为高斯、只学均值，使问题大幅简化。

## 与其他知识的关系

→ 反转 → def-ho2020-forward-diffusion-process。
→ 其变分下界 → thm-ho2020-elbo-variational-bound。
→ 其均值参数化 → meth-ho2020-epsilon-prediction。
→ 由 → thm-ho2020-score-matching-langevin-equivalence 证明可类比于 Langevin dynamics 采样。
← $\Sigma_\theta$ 选择见 → meth-ho2020-variance-schedule。

## 来源引用

Ho et al. 2020, Section 2 (Background), Eqs. (1)-(2)；Section 3.2。full-text.txt lines 88-97, 159-160。
