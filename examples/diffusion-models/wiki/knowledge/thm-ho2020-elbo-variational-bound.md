---
id: thm-ho2020-elbo-variational-bound
type: theorem
label: ELBO / Variational Bound on Negative Log-Likelihood
source: ho2020
section: Section 2 (Background), Appendix A
tokens: 1200
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 106
  end_line: 140
  page: "2"
---

## 精确表述

扩散模型通过对负对数似然的标准**变分下界**（ELBO）进行优化来训练（Eq. 3）：

$$\mathbb{E}[-\log p_\theta(x_0)] \le \mathbb{E}_q\!\left[-\log \frac{p_\theta(x_{0:T})}{q(x_{1:T}|x_0)}\right] =: L$$

利用马尔可夫结构与贝叶斯法则，$L$ 可重写为降低方差的 KL 分解（Eq. 5，推导见 Appendix A）：

$$L = \underbrace{D_{KL}(q(x_T|x_0)\,\|\,p(x_T))}_{L_T} + \sum_{t>1} \underbrace{D_{KL}(q(x_{t-1}|x_t,x_0)\,\|\,p_\theta(x_{t-1}|x_t))}_{L_{t-1}} - \underbrace{\log p_\theta(x_0|x_1)}_{L_0}$$

即 $L = L_T + \sum_{t>1} L_{t-1} + L_0$。其中：

- $L_T$：前向过程终态与先验的 KL，因 $\beta_t$ 固定而是常数（训练时可忽略）。
- $L_{t-1}$：学习的反向转移与可解析前向后验（→ def-ho2020-forward-posterior）的 KL，全为高斯对高斯，闭式可算。
- $L_0$：离散解码项（→ meth-ho2020-ddpm-training 的 $t=1$ 情形）。

等价地，$L$ 还可写为关于 $q(x_{t-1}|x_t)$ 的形式（Eq. 16）：$L = D_{KL}(q(x_T)\|p(x_T)) + \mathbb{E}_q\sum_{t\ge 1} D_{KL}(q(x_{t-1}|x_t)\|p_\theta(x_{t-1}|x_t)) + H(x_0)$。

## 适用条件

- $p_\theta$ 为上述高斯反向马尔可夫链，$q$ 为固定高斯前向链（→ def-ho2020-reverse-process, → def-ho2020-forward-diffusion-process）。
- 各 KL 因前向过程为高斯而可解析，故无需蒙特卡洛。

## 直觉解释

扩散模型不直接最大化似然，而是最小化负对数似然的上界。这个上界被拆成每一步去噪的"误差"（$L_{t-1}$）：让学习的反向转移尽量接近真实前向后验。由于每项都是高斯间 KL，训练目标简单、低方差、可随机梯度优化。

## 与其他知识的关系

← 依赖 → def-ho2020-forward-diffusion-process、→ def-ho2020-reverse-process、→ def-ho2020-forward-posterior。
→ 被简化为 → meth-ho2020-ddpm-training 的训练目标（Lsimple，加权变体）。
→ 其分解项 $L_0$/$\sum L_t$ 支撑 → ins-ho2020-progressive-lossy-compression（率/失真）。
→ 其 Eq.16 形式支撑 → ins-ho2020-autoregressive-generalization。
→ 由 → ins-ho2020-simplified-objective-downweights 解释其加权取舍。

## 来源引用

Ho et al. 2020, Section 2, Eqs. (3),(5)；Appendix A, Eqs. (17)-(26)（推导继承自 Sohl-Dickstein et al. [53]）。full-text.txt lines 106-140, 773-830。
