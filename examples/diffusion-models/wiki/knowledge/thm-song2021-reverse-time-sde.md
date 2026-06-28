---
id: thm-song2021-reverse-time-sde
type: theorem
label: Reverse-Time SDE (Anderson 1982)
source: song2021
section: Section 3.2
tokens: 1100
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1457
  end_line: 1488
  page: "Unknown"
---

## 精确表述

Anderson (1982) 的结果：**扩散过程的逆过程也是扩散过程**，且逆向时间运行，由如下 reverse-time SDE 给出（Eq. 6）：

$$\mathrm{d}\mathbf{x}=\big[\mathbf{f}(\mathbf{x},t)-g(t)^{2}\,\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})\big]\,\mathrm{d}t+g(t)\,\mathrm{d}\bar{\mathbf{w}}$$

其中 $\bar{\mathbf{w}}$ 是当时间从 $T$ 倒流到 $0$ 时的标准维纳过程，$\mathrm{d}t$ 是无穷小负时间步。一旦每个边际分布的 score $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$ 已知（→ def-song2021-score-function），即可由 Eq. 6 推导出逆向扩散过程并模拟它来从 $p_{0}$ 采样。

关键：reverse-time SDE 与 forward SDE 共享同样的漂移 $\mathbf{f}$ 和扩散 $g$，唯一新增项是 $-g(t)^{2}\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$——一个由 score 驱动的"去噪"项。

## 适用条件

- 前向 SDE 满足正则性条件（系数全局 Lipschitz，有唯一强解）。
- 需已知/估计 score $\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})$ 对所有 $t\in[0,T]$。
- 用数值 SDE solver 模拟时需离散化（Euler-Maruyama、stochastic Runge-Kutta 等，→ meth-song2021-pc-sampler）。

## 直觉解释

正向 SDE 把数据变成噪声；Anderson 定理保证"噪声变回数据"的过程也是一个 SDE，而且它的公式几乎是正向 SDE 的镜像——只多了一项"沿 score 方向爬升"。score 指向高密度区，所以这一项就是"去噪力"。由于 score 是唯一未知量，整个生成问题归结为"估计 score"。

## 与其他知识的关系

← 依赖 → def-song2021-forward-sde（前向 SDE）和 → def-song2021-score-function（score）。
→ score 由 → meth-song2021-score-based-training 估计后，才能构造此 reverse-time SDE。
→ 其数值求解驱动 → meth-song2021-pc-sampler（PC 采样器）和 → meth-song2021-conditional-sde（条件采样）。
→ **跨源（→ def-ho2020-reverse-process）**：reverse-time SDE 是 DDPM 离散反向过程 $p_\theta(x_{t-1}|x_t)$ 的**连续时间推广**（`generalizes`）。DDPM 的 ancestral sampling 是 reverse-time VP SDE 的一种特殊离散化（Section 4.1, Appendix E）。
→ **跨源（→ thm-ho2020-score-matching-langevin-equivalence）**：ho2020 在离散框架内发现"采样≈Langevin"；本定理在连续时间严格给出反向过程的 SDE 形式，$-g(t)^2\nabla\log p_t$ 项正是 Langevin-like 去噪力的连续化（`extends`）。

## 来源引用

Song et al. 2021, Section 3.2, Eq. (6)；Anderson 1982 [Reverse-time diffusion equation models]。full-text.txt lines 1457-1488。
