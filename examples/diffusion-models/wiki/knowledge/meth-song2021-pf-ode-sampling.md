---
id: meth-song2021-pf-ode-sampling
type: method
label: Probability Flow ODE Sampling (Fast Adaptive Sampling)
source: song2021
section: Section 4.3
tokens: 1000
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 2098
  end_line: 2166
  page: "Unknown"
---

## 精确表述

利用 probability flow ODE（→ thm-song2021-probability-flow-ode）进行采样的两种方式：

1. **固定离散化**：用与 reverse-time SDE 类似函数形式的离散化积分 Eq. 13 逆向，可结合 corrector（Table 1 "probability flow sampler"，Section D.3）。
2. **黑盒自适应 ODE 求解器**（如 Dormand-Prince RK45）：因为是确定性 ODE / neural ODE，可用任意黑盒求解器，并**显式地在精度与效率间权衡**——增大误差容差可把函数求值次数（NFE）减少 **90% 以上**而不明显损害样本视觉质量（Fig. 3）。

此外，积分 Eq. 13 可把任意数据点 $\mathbf{x}(0)$ 编码到 latent $\mathbf{x}(T)$，反向积分解码，支持 latent 插值与温度缩放（→ ins-song2021-uniquely-identifiable-encoding）。同样地，瞬时变量替换公式给出**精确对数似然**。

## 适用条件

- 已有 score 模型（与 reverse-time SDE 相同）。
- 纯 ODE 采样通常 FID 略逊于 SDE 采样器，需配合 corrector 或仅在需要精确似然/快速采样的场景使用。
- 对 VE-SDE 的样本质量差于 VP-SDE（高维数据尤甚）。

## 直觉解释

reverse-time SDE 是随机的，要走很多步；probability flow ODE 是确定性的，可用自适应步长——平缓处大步、陡峭处小步，从而大幅减少步数。代价是丢了随机性带来的"去噪纠错"，样本质量稍降。最大好处是它是可逆的 neural ODE，所以能精确算似然、能编码解码。

## 与其他知识的关系

← 基于 → thm-song2021-probability-flow-ode。
↔ 与 → meth-song2021-pc-sampler 是 SDE 随机采样 vs ODE 确定性采样的两种路线（`compares_with`，见 → exp-song2021-sampler-comparison）。
→ 驱动 → ins-song2021-uniquely-identifiable-encoding（可逆编码）。
→ **跨源（→ meth-ho2020-ddpm-sampling）**：DDPM 只有 ancestral sampling（慢、1000 步）；PF-ODE 提供了 DDPM 框架所没有的快速自适应采样与精确似然（`extends`）。

## 来源引用

Song et al. 2021, Section 4.3, Sections D.2-D.4；Fig. 3。full-text.txt lines 2098-2166。
