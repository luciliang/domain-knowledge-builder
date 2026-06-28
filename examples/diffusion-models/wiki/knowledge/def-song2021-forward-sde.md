---
id: def-song2021-forward-sde
type: definition
label: Forward SDE (Continuous-Time Diffusion Process)
source: song2021
section: Section 3.1
tokens: 900
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1389
  end_line: 1455
  page: "Unknown"
---

## 精确表述

Score-SDE 框架将"逐步加噪"推广到**连续时间**。构造一个由连续时间变量 $t\in[0,T]$ 索引的扩散过程 $\{\mathbf{x}(t)\}_{t=0}^{T}$，其中 $\mathbf{x}(0)\sim p_{0}$（数据分布），$\mathbf{x}(T)\sim p_{T}$（已知的先验分布）。该扩散过程是如下 Itô SDE 的解（Eq. 5）：

$$\mathrm{d}\mathbf{x}=\mathbf{f}(\mathbf{x},t)\,\mathrm{d}t+g(t)\,\mathrm{d}\mathbf{w}$$

其中 $\mathbf{w}$ 是标准维纳过程（布朗运动），$\mathbf{f}(\cdot,t):\mathbb{R}^{d}\to\mathbb{R}^{d}$ 是**漂移系数（drift）**，$g(\cdot):\mathbb{R}\to\mathbb{R}$ 是标量**扩散系数（diffusion）**。该 SDE 无可训练参数、不依赖数据，由设计者预先指定。

只要系数在状态和时间上全局 Lipschitz，SDE 就有唯一强解。记 $p_{t}(\mathbf{x})$ 为 $\mathbf{x}(t)$ 的概率密度，$p_{st}(\mathbf{x}(t)\mid\mathbf{x}(s))$ 为转移核。通常 $p_{T}$ 选为固定均值和方差的高斯先验。

## 适用条件

- 扩散系数为标量（不依赖 $\mathbf{x}$）；论文理论可推广到 $d\times d$ 矩阵情形（Appendix A）。
- 漂移 $\mathbf{f}$ 仿射时，转移核 $p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))$ 恒为高斯，可闭式计算——这是 VE/VP/sub-VP SDE 的共同前提（→ def-song2021-ve-sde、→ def-song2021-vp-sde）。
- 系数全局 Lipschitz（保证唯一强解）。

## 直觉解释

DDPM/SMLD 用有限个噪声尺度（离散马尔可夫链）逐步加噪；Score-SDE 把"噪声尺度的个数"从有限推广到无穷（连续时间 $t$），于是加噪过程变成一条连续随机轨迹——一个 SDE。前向 SDE 没有 trainable 参数，只是一个"把数据平滑地变成噪声"的预设管道。选择不同的漂移/扩散系数就得到不同的 SDE（如 VE、VP），对应不同的"加噪食谱"。

## 与其他知识的关系

→ 由 → def-song2021-ve-sde、→ def-song2021-vp-sde 两个特例实例化。
→ 其反向过程由 → thm-song2021-reverse-time-sde（Anderson 1982）给出。
→ 是连续时间的 → def-song2021-score-function 定义所依附的随机过程。
→ **跨源（→ def-ho2020-forward-diffusion-process）**：本文前向 SDE 是 DDPM 离散前向马尔可夫链的**连续时间推广**；DDPM 的加噪链是 VP-SDE 的离散化（见 → thm-song2021-sde-discretization-equivalence）。

## 来源引用

Song et al. 2021, Section 3.1, Eq. (5)。full-text.txt lines 1389-1455。
