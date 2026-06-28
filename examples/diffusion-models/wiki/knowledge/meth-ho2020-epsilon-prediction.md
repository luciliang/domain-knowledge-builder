---
id: meth-ho2020-epsilon-prediction
type: method
label: Epsilon-Prediction Parameterization
source: ho2020
section: Section 3.2
tokens: 850
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 166
  end_line: 237
  page: "3"
---

## 精确表述

反向过程均值 $\mu_\theta$ 有两种等价参数化。最直接的是让网络预测前向后验均值 $\tilde{\mu}_t$（→ def-ho2020-forward-posterior）。论文提出关键的 **$\epsilon$-预测参数化**（Eq. 11）：用一个函数逼近器 $\epsilon_\theta$ 从 $x_t$ 预测当初前向加入的噪声 $\epsilon$，并把均值表为：

$$\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\epsilon_\theta(x_t, t)\right)$$

在此参数化下，$L_{t-1}$ 化简为去噪 score matching 形式（Eq. 12，见 → thm-ho2020-score-matching-langevin-equivalence）。

网络实现：U-Net 主干（类 PixelCNN++），时间步 $t$ 经 Transformer 正弦位置嵌入注入每个残差块，在 $16\times16$ 分辨率用自注意力；参数在所有 $t$ 共享（→ exp-ho2020-cifar10-results 附录细节）。

## 适用条件

- 前向过程闭式边际可用（→ def-ho2020-forward-diffusion-process 的 Eq. 4），以构造带噪输入 $\sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$。
- 与 $\mũ$-预测、$x_0$-预测是三种可选参数化；论文实验表明预测 $x_0$ 早期样本质量较差。

## 直觉解释

与其让网络预测一个复杂的均值向量，不如让它预测"图像里掺了多少噪声"（一个更易学的目标），再用固定公式把噪声折算回均值。这一改写既简化了目标，又揭示了与 score matching 的等价性。

## 与其他知识的关系

→ 其均值代入 → meth-ho2020-ddpm-sampling 的采样公式。
→ 其训练目标（去噪 MSE）即 → meth-ho2020-ddpm-training 的 Lsimple。
→ 由此推出 → thm-ho2020-score-matching-langevin-equivalence。
→ 由 → exp-ho2020-ablation 对比 $\mũ$-预测（ε 预测 + Lsimple 最佳）。

## 来源引用

Ho et al. 2020, Section 3.2, Eq. (11)；Appendix B。full-text.txt lines 166-237, 832-841。
