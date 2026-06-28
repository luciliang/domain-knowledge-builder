---
id: ins-ho2020-progressive-lossy-compression
type: insight
label: Diffusion as Progressive Lossy Compression (Rate-Distortion)
source: ho2020
section: Section 4.3
tokens: 900
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 366
  end_line: 430
  page: "6"
---

## 精确表述

作者论证：尽管扩散模型的无损码长不及其它似然模型，但它有极好的**归纳偏置成为优秀的有损压缩器**。把变分下界项按率-失真（rate-distortion）解释（→ thm-ho2020-elbo-variational-bound 的 Eq.5）：

- **率（rate）** = $L_1 + \cdots + L_T$
- **失真（distortion）** = $L_0$

在 CIFAR-10 最佳样本模型上：rate = 1.78 bits/dim，distortion = 1.97 bits/dim（约 0–255 尺度上 RMSE 0.95）。**超过一半的无损码长用于描述不可察觉的失真细节**。

**渐进式有损编码（Algorithms 3-4）。** 引入镜像 Eq.(5) 形式的渐进有损码：发送端逐步发 $x_T,\dots,x_0$，接收端在任意时刻 $t$ 可由已有 $x_t$ 渐进估计 $x_0$（Eq. 15）：

$$\hat{x}_0 = \left(x_t - \sqrt{1-\bar{\alpha}_t}\,\epsilon_\theta(x_t)\right)/\sqrt{\bar{\alpha}_t}$$

在 CIFAR-10 测试集的率-失真曲线上，**低率区失真急剧下降**——确认大部分 bit 确实花在不可感知细节上（Figure 5）。

**渐进生成。** 边采反向过程边预测 $\hat{x}_0$：大尺度结构先出现、细节最后出现（Figures 6,10）。

## 适用条件

- 假设有 minimal random coding 类过程可用 $D_{KL}(q\|p)$ 比特传送 $x\sim q$。
- 率-失真解读是对 L（真下界）的分解；Lsimple 牺牲码长故此分析以 L 模型为准。

## 直觉解释

扩散模型把一张图"拆"成从粗到细的比特流：先几 bit 就能定下大致轮廓，后面的海量 bit 只在精修肉眼几乎看不出的细节。这正是它样本质量高但码长不顶尖的原因——它天生是有损压缩，而非追求极致无损。

## 与其他知识的关系

← 基于分解 → thm-ho2020-elbo-variational-bound（$L_0$ vs $\sum L_t$）。
← 用 → meth-ho2020-ddpm-sampling 与 → meth-ho2020-epsilon-prediction 的 $\hat{x}_0$ 估计（Eq.15）。
↔ 与 → ins-ho2020-simplified-objective-downweights 互补（解释码长-质量权衡）。
↔ 与 → ins-ho2020-autoregressive-generalization 同为对 ELBO 的重新诠释。

## 来源引用

Ho et al. 2020, Section 4.3, Eqs. (15),(16), Algorithms 3-4, Figure 5。full-text.txt lines 366-430。
