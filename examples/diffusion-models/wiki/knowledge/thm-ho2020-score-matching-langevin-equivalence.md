---
id: thm-ho2020-score-matching-langevin-equivalence
type: theorem
label: Diffusion-ScoreMatching-Langevin Equivalence
source: ho2020
section: Section 3.2, Appendix C
tokens: 1500
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 157
  end_line: 237
  page: "3"
---

## 精确表述

论文的核心理论贡献：在 → meth-ho2020-epsilon-prediction 参数化下，扩散模型的训练目标与**去噪 score matching** 等价，采样过程与 **Langevin dynamics** 类似。$\epsilon_\theta$ 起到数据密度"学习到的梯度"的作用。

**推导（Eqs. 8-12）。** 将 $\Sigma_\theta = \sigma_t^2 I$ 代入 $L_{t-1}$（→ thm-ho2020-elbo-variational-bound），并用前向闭式边际 $x_t(x_0,\epsilon) = \sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\epsilon$ 与前向后验（→ def-ho2020-forward-posterior）展开，得（Eq. 10）：

$$L_{t-1} - C = \mathbb{E}_{x_0,\epsilon}\!\left[\frac{1}{2\sigma_t^2}\left\| \frac{1}{\sqrt{\alpha_t}}x_t(x_0,\epsilon) - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\epsilon - \mu_\theta(x_t(x_0,\epsilon), t)\right\|^2\right]$$

从而选择参数化使 $\mu_\theta$ 转而预测 $\epsilon$（Eq. 11），目标简化为（Eq. 12）：

$$\mathbb{E}_{x_0,\epsilon}\!\left[\frac{\beta_t^2}{2\sigma_t^2 \alpha_t (1-\bar{\alpha}_t)}\left\|\epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon,\, t)\right\|^2\right]$$

这正是跨多个噪声尺度（以 $t$ 为索引）的**去噪 score matching** 形式（[55] NCSN）。

**采样 ↔ Langevin。** 采样步骤 $x_{t-1} = \frac{1}{\sqrt{\alpha}_t}(x_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\epsilon_\theta(x_t,t)) + \sigma_t z$ 类比于以 $\epsilon_\theta$ 为学习到的数据密度梯度的 **Langevin dynamics**。且因 Eq.(12) 恰是此类 Langevin-like 反向过程的变分下界，故"优化一个类似去噪 score matching 的目标"等价于"用变分推断拟合一个类似 Langevin dynamics 的采样链的有限时间边际"。

## 适用条件

- 采用 $\epsilon$-预测参数化（→ meth-ho2020-epsilon-prediction）。
- 前向过程为高斯、$\beta_t$ 较小且 $L_T \approx 0$（先验与聚合后验匹配）。
- 反向过程方差 $\Sigma_\theta = \sigma_t^2 I$ 固定。

## 直觉解释

扩散模型表面上是一个潜变量模型，但在 $\epsilon$-参数化下，训练目标变成"从带噪图像预测当初加入的那份噪声"，这与去噪 score matching（学数据密度的梯度）逐字对应；而逐步去噪采样则与 Langevin dynamics（沿密度梯度走 + 加噪）逐字对应。于是扩散模型 = score matching 训练 + Langevin 采样，且采样的学习率/噪声尺度由前向 $\beta_t$ 严格推导而非手工设定（区别于 NCSN，见 Appendix C）。

## 与其他知识的关系

← 依赖 → meth-ho2020-epsilon-prediction、→ def-ho2020-reverse-process、→ def-ho2020-forward-posterior。
→ 其采样含义 → meth-ho2020-ddpm-sampling。
→ 驱动 → ins-ho2020-simplified-objective-downweights（Lsimple 形式源于此）。
→ 被 → exp-ho2020-cifar10-results、→ exp-ho2020-ablation 验证（最佳样本质量来自此参数化）。

## 来源引用

Ho et al. 2020, Section 3.2, Eqs. (8)-(12)；Related Work (Section 5)；Appendix C。full-text.txt lines 157-237, 883-903。
