---
id: def-ho2020-forward-posterior
type: definition
label: Tractable Forward Process Posterior
source: ho2020
section: Section 2 (Background)
tokens: 650
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 131
  end_line: 140
  page: "2"
---

## 精确表述

给定数据 $x_0$ 时，前向过程的**反向后验** $q(x_{t-1}|x_t, x_0)$ 是可解析求解（tractable）的高斯分布（Eqs. 6-7）：

$$q(x_{t-1}|x_t, x_0) = \mathcal{N}(x_{t-1};\, \tilde{\mu}_t(x_t, x_0),\, \tilde{\beta}_t I)$$

$$\tilde{\mu}_t(x_t, x_0) := \frac{\sqrt{\bar{\alpha}_{t-1}}\,\beta_t}{1-\bar{\alpha}_t}\, x_0 + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\, x_t$$

$$\tilde{\beta}_t := \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\, \beta_t$$

## 适用条件

- 仅当条件化于 $x_0$ 时成立（即 $q(x_{t-1}|x_t,x_0)$，而非 $q(x_{t-1}|x_t)$）。
- 前向过程为线性高斯马尔可夫链（→ def-ho2020-forward-diffusion-process）。

## 直觉解释

这是变分下界中 KL 散度项的"目标"分布：训练时把学习的反向转移 $p_\theta(x_{t-1}|x_t)$ 与这个可解析的前向后验做 KL 比较（Eq. 5）。因为它能闭式算出，所有 KL 项都可精确计算（Rao-Blackwellized），无需高方差蒙特卡洛估计。

## 与其他知识的关系

← 派生自 → def-ho2020-forward-diffusion-process。
→ 提供 → thm-ho2020-elbo-variational-bound 中 KL 项的可解析比较目标。
→ 其均值 $\tilde{\mu}_t$ 是 → meth-ho2020-epsilon-prediction 的另一种参数化目标（预测 $\tilde{\mu}_t$ vs 预测 $\epsilon$）。

## 来源引用

Ho et al. 2020, Section 2 (Background), Eqs. (6)-(7)。full-text.txt lines 131-140。
