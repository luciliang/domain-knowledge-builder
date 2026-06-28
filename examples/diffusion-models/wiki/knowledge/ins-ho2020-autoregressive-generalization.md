---
id: ins-ho2020-autoregressive-generalization
type: insight
label: Gaussian Diffusion Generalizes Autoregressive Decoding
source: ho2020
section: Section 4.3
tokens: 850
created: 2026-06-28
generated_by_step: S2
run_id: 09207eda-1bc6-46b7-a8f3-779abb928d4f
source_span:
  file: ho2020-ddpm.pdf
  start_line: 444
  end_line: 471
  page: "7"
---

## 精确表述

作者指出变分下界（Eq. 5）可改写为（Eq. 16，推导见 Appendix A）：

$$L = D_{KL}(q(x_T)\,\|\,p(x_T)) + \mathbb{E}_q\!\left[\sum_{t\ge 1} D_{KL}(q(x_{t-1}|x_t)\,\|\,p_\theta(x_{t-1}|x_t)) + H(x_0)\right]$$

**关键论证。** 设扩散长度 $T$ 等于数据维度，定义前向过程使 $q(x_t|x_0)$ 把 $x_0$ 的前 $t$ 个坐标遮蔽（$q(x_t|x_{t-1})$ 遮掉第 $t$ 个坐标），$p(x_T)$ 置于全黑图，并令 $p_\theta(x_{t-1}|x_t)$ 为任意全表达条件分布。则：$D_{KL}(q(x_T)\|p(x_T))=0$，最小化各 $D_{KL}(q(x_{t-1}|x_t)\|p_\theta(\cdot))$ 即训练 $p_\theta$ 原样复制坐标 $t{+}1,\dots,T$ 并预测第 $t$ 个坐标——**这正是训练一个自回归模型**。

因此**高斯扩散模型可视为一种具有"广义比特排序"的自回归模型**，且这种排序无法通过重排数据坐标表达。高斯扩散长度不必等于数据维度（论文用 $T=1000$，远小于图像维度），可缩短以加速采样或延长以增强表达力。

## 适用条件

- 论证为概念性（"for the sake of argument"），展示扩散框架的包容性。
- 适用于离散掩蔽前向作为高斯前向的特例类比。

## 直觉解释

自回归模型按像素顺序逐个生成；扩散模型按"噪声层"逐层去噪。数学上后者是前者的推广：把"遮像素"换成"加高斯噪声"，就得到一种更灵活、比特顺序更自由的自回归式生成。这统一了两种看似不同的生成范式。

## 与其他知识的关系

← 基于变形 → thm-ho2020-elbo-variational-bound 的 Eq.16。
← 用 → meth-ho2020-ddpm-sampling 的渐进生成（粗→细）作类比证据。
↔ 与 → ins-ho2020-progressive-lossy-compression 同为对 ELBO 的重新诠释（compares_with）。

## 来源引用

Ho et al. 2020, Section 4.3, Eq. (16)（Appendix A 推导 Eqs. 23-26）。full-text.txt lines 444-471, 809-830。
