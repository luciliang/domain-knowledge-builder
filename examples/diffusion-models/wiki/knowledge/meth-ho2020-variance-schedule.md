---
id: meth-ho2020-variance-schedule
type: method
label: Fixed Variance Schedule (Forward β and Reverse σ)
source: ho2020
section: Section 3.1, Section 3.2, Section 4
tokens: 800
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 151
  end_line: 165
  page: "3"
---

## 精确表述

论文把方差都设为**固定常数**而非学习：

**前向方差 $\beta_t$。** $T=1000$，$\beta_t$ 从 $\beta_1 = 10^{-4}$ 到 $\beta_T = 0.02$ **线性**递增。相对缩放到 $[-1,1]$ 的数据取较小值，保证反向与前向过程函数形式近似一致，并使 $x_T$ 处信噪比尽量小：$L_T = D_{KL}(q(x_T|x_0)\,\|\,\mathcal{N}(0,I)) \approx 10^{-5}$ bits/dim。

**反向方差 $\Sigma_\theta$。** 设 $\Sigma_\theta(x_t,t) = \sigma_t^2 I$ 为不学习的与时间有关的常数。两种选择：

- $\sigma_t^2 = \beta_t$：对 $x_0 \sim \mathcal{N}(0,I)$ 最优；
- $\sigma_t^2 = \tilde{\beta}_t = \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t$：对 $x_0$ 为确定一点最优。

二者是单位坐标方差数据的反向过程熵的上下界，实验上样本质量相近。学习对角 $\Sigma_\theta$ 反而导致训练不稳定、样本质量变差（→ exp-ho2020-ablation）。

**β 表选择。** 从常数/线性/二次表中按"$L_T\approx 0$"约束挑选，最终选线性（未对 $T$ 扫描）。

## 适用条件

- 数据线性缩放到 $[-1,1]$。
- 固定常数使前向过程 $q$ 无可学习参数，故 $L_T$ 为常数（→ thm-ho2020-elbo-variational-bound 可忽略）。

## 直觉解释

让方差固定不动，模型只专心学"去噪方向"（均值）。前向 β 缓慢线性增长，确保每步只加一点点噪声、整个过程最终完全毁掉信号；反向方差用同一套常数的两种合理近似即可，没必要学——学了反而难训。

## 与其他知识的关系

→ 参数化 → def-ho2020-forward-diffusion-process（β）与 → def-ho2020-reverse-process（σ²）。
→ 供 → meth-ho2020-ddpm-sampling、→ meth-ho2020-ddpm-training 使用。
→ 学习 vs 固定 Σ 由 → exp-ho2020-ablation 对比（固定更稳）。

## 来源引用

Ho et al. 2020, Section 3.1, 3.2；Section 4；Appendix B。full-text.txt lines 151-165, 318-323, 852-854。
