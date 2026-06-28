---
id: exp-song2021-sampler-comparison
type: experiment
label: Sampler Comparison (Predictor vs Corrector vs PC vs Probability Flow)
source: song2021
section: Section 4.1-4.2, Table 1
tokens: 1000
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 1747
  end_line: 1865
  page: "Unknown"
---

## 精确表述

Table 1 在 CIFAR-10 上对比不同 reverse-time SDE 求解器（VE-SDE/SMLD 与 VP-SDE/DDPM，相同计算量下比较）。求解器类别：P1000/P2000（仅 predictor，1000/2000 步）、C2000（仅 corrector，2000 步）、PC1000（1000 predictor + 1000 corrector）。关键发现：

- **PC1000 始终优于 P1000**：每个 predictor 步加一个 corrector 步（计算量翻倍但质量持续提升）。例如 VE reverse diffusion：P1000 FID 4.79 → PC1000 3.19；VP reverse diffusion：P1000 3.21 → PC1000 3.18。
- **reverse diffusion sampler 始终略优于 ancestral sampling**（VE: 4.98→4.79；VP: 3.24→3.21）。
- **corrector-only (C2000) 通常劣于** P2000/PC1000（同计算量下）。
- **probability flow（ODE 作为 predictor）单独用时 FID 较差**（VE: 15.41-20.43），但配合 corrector 后大幅改善（PC1000: 3.06-3.23），证明 ODE 需配 corrector 才有竞争力。

## 适用条件

- SMLD/DDPM 模型用原始离散目标（Eq. 1/3）训练，展示 PC 采样器对固定噪声尺度模型的兼容性。
- 五次采样取均值±标准差。

## 直觉解释

实验证明 PC 框架的价值：predictor 和 corrector 各有盲区，交替使用互补最强。probability flow ODE 单独弱，是因为丢失了随机纠错；加上 corrector 后立刻追平 SDE 采样器。这为"何时用 ODE、何时用 SDE"提供了实证依据。

## 与其他知识的关系

← 评估 → meth-song2021-pc-sampler（PC 采样器）并对比 → meth-song2021-pf-ode-sampling（probability flow 作为 predictor）。
→ 经验支持 → ins-song2021-unified-continuous-framework（PC 采样器统一并改进了 SMLD/DDPM 各自的采样器）。

## 来源引用

Song et al. 2021, Section 4.1-4.2, Table 1。full-text.txt lines 1747-1865。
