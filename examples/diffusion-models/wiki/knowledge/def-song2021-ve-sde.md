---
id: def-song2021-ve-sde
type: definition
label: Variance Exploding (VE) SDE
source: song2021
section: Section 3.4
tokens: 850
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1580
  end_line: 1652
  page: "Unknown"
---

## 精确表述

**Variance Exploding (VE) SDE** 是 SMLD（Song & Ermon 2019，即 NCSN）噪声扰动的连续时间推广。SMLD 的离散马尔可夫链为（Eq. 8）：

$$\mathbf{x}_{i}=\mathbf{x}_{i-1}+\sqrt{\sigma_{i}^{2}-\sigma_{i-1}^{2}}\,\mathbf{z}_{i-1}$$

当噪声尺度数 $N\to\infty$ 时，$\{\sigma_{i}\}$ 变为函数 $\sigma(t)$，该链收敛为如下 SDE（Eq. 9）：

$$\mathrm{d}\mathbf{x}=\sqrt{\frac{\mathrm{d}[\sigma^{2}(t)]}{\mathrm{d}t}}\,\mathrm{d}\mathbf{w}$$

其漂移为零（纯加噪、无收缩），故方差随 $t\to\infty$ **爆炸（exploding）**，因此得名 Variance Exploding。其转移核为高斯 $p_{0t}(\mathbf{x}(t)\mid\mathbf{x}(0))=\mathcal{N}(\mathbf{x}(t);\,\mathbf{x}(0),\sigma^{2}(t)-\sigma^{2}(0)\,\mathbf{I})$。

## 适用条件

- 噪声尺度 $\sigma(t)$ 单调递增，$\sigma_{\min}\approx0$（近似数据分布），$\sigma_{\max}$ 足够大（近似纯高斯先验）。
- 漂移为零，故无"收缩"项；方差无界，需配合大 $\sigma_{\max}$ 的先验。

## 直觉解释

VE-SDE 只往数据里加噪声、不收缩数据本身，所以方差越来越大（"爆炸"）。它对应 SMLD/NCSN 的加噪方式：用一串递增的 $\sigma$ 加高斯噪声。连续化后就是这条"无漂移、纯扩散"的 SDE。

## 与其他知识的关系

→ 是 → def-song2021-forward-sde 的特例（漂移 $\mathbf{f}=0$，扩散 $g(t)=\sqrt{\mathrm{d}[\sigma^{2}(t)]/\mathrm{d}t}$）。
→ 与 → def-song2021-vp-sde 并列，二者构成统一框架的两种典型 SDE（→ thm-song2021-sde-discretization-equivalence）。
→ **跨源（→ def-ho2020-forward-diffusion-process）**：VE-SDE 与 DDPM 的前向过程是**不同**的加噪机制——VE 无收缩（方差爆炸），VP 有收缩（方差保持）。二者被统一为同一 SDE 框架的两种离散化，是连续时间统一视角（→ ins-song2021-unified-continuous-framework）的核心论据。

## 来源引用

Song et al. 2021, Section 3.4, Eqs. (8)-(9)。full-text.txt lines 1580-1652。
