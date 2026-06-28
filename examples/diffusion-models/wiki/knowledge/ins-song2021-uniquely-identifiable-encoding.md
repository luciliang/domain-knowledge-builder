---
id: ins-song2021-uniquely-identifiable-encoding
type: insight
label: Uniquely Identifiable Encoding via Probability Flow ODE
source: song2021
section: Section 4.3
tokens: 900
created: 2026-06-28
generated_by_step: S2
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
source_span:
  file: song2021-score-sde.md
  start_line: 2098
  end_line: 2136
  page: "Unknown"
---

## 精确表述

由 probability flow ODE（→ thm-song2021-probability-flow-ode）编码/解码时，Score-SDE 模型的编码是**唯一可识别的（uniquely identifiable）**：在足够的训练数据、模型容量和优化精度下，一个输入的编码由数据分布唯一决定（Roeder et al. 2020 的定义）。

原因在于：前向 SDE（Eq. 5）**没有可训练参数**，其对应的 probability flow ODE（Eq. 13）在 score 完美估计时给出确定性轨迹，因此相同的输入数据分布 → 相同的编码映射。这与大多数可逆模型（normalizing flows）不同——它们的编码通常依赖可学习变换，可能非唯一。论文在 Section D.5 给出经验验证。

此外，积分 Eq. 13 可把数据编码到 latent、反向积分解码，支持 latent 插值、温度缩放等操控（Fig. 3）。

## 适用条件

- score 完美（或充分）估计。
- 用 probability flow ODE（而非随机 reverse-time SDE）做编码/解码。

## 直觉解释

大多数生成模型（如 normalizing flows）的 latent 编码是"人造"的——依赖网络怎么学，换一次训练编码就变。但 Score-SDE 的编码由数据分布本身决定：因为前向 SDE 是固定的（无可训练参数），给定数据分布，"数据 → 噪声"的确定性轨迹就是唯一的。这让 latent 空间有了真正的语义稳定性。

## 与其他知识的关系

← 由 → thm-song2021-probability-flow-ode 保证（前向 SDE 无可训练参数 + 确定性 ODE）。
↔ 是 Score-SDE 相对 normalizing flows / neural ODEs 的独特性质。
→ **跨源**：DDPM（ho2020）的离散 ELBO 视角不提供可逆编码/唯一性；此洞察是连续框架 + ODE 带来的新能力。

## 来源引用

Song et al. 2021, Section 4.3（Uniquely identifiable encoding），Section D.5；Roeder et al. 2020。full-text.txt lines 2098-2136。
