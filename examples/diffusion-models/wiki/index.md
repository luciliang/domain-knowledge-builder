---
title: Diffusion Models — Knowledge Index
domain: diffusion-models
last_updated: 2026-06-28
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
sources: [ho2020, song2021]
---

# Diffusion Models — 知识索引

> 知识节点按类型分组。每行：ID（链接到 `knowledge/` 下对应文件）· 一句话摘要 · 来源 [ho2020 DDPM / song2021 Score-SDE]。
> 双源知识库：30 节点 / 53 边（含 11 跨源）。遍历关系见 `dag/dag-index.json`。

## Definitions（7）

- [`def-ho2020-forward-diffusion-process`](knowledge/def-ho2020-forward-diffusion-process.md) — 固定高斯加噪马尔可夫链，含闭式边际 q(x_t|x_0)。[ho2020] Updated 2026-06-28
- [`def-ho2020-reverse-process`](knowledge/def-ho2020-reverse-process.md) — 学习到的高斯反向马尔可夫链，先验 N(0,I)。[ho2020] Updated 2026-06-28
- [`def-ho2020-forward-posterior`](knowledge/def-ho2020-forward-posterior.md) — 可解析前向后验 q(x_{t-1}|x_t,x_0)，KL 比较目标。[ho2020] Updated 2026-06-28
- [`def-song2021-forward-sde`](knowledge/def-song2021-forward-sde.md) — 连续时间前向扩散 SDE dx=f(x,t)dt+g(t)dw（Eq 5），DDPM/SMLD 的连续化母体。[song2021] Updated 2026-06-28
- [`def-song2021-score-function`](knowledge/def-song2021-score-function.md) — 时间依赖 score 梯度场 ∇_x log p_t(x)，reverse-time SDE 与 PF-ODE 的唯一依赖。[song2021] Updated 2026-06-28
- [`def-song2021-ve-sde`](knowledge/def-song2021-ve-sde.md) — Variance Exploding SDE（Eq 9），零漂移、SMLD/NCSN 的连续极限。[song2021] Updated 2026-06-28
- [`def-song2021-vp-sde`](knowledge/def-song2021-vp-sde.md) — Variance Preserving SDE（Eq 11），线性漂移、DDPM 的连续极限（+ sub-VP）。[song2021] Updated 2026-06-28

## Theorems（5）

- [`thm-ho2020-elbo-variational-bound`](knowledge/thm-ho2020-elbo-variational-bound.md) — NLL 变分下界 L = L_T + ΣL_{t-1} + L_0 的全闭式 KL 分解。[ho2020] Updated 2026-06-28
- [`thm-ho2020-score-matching-langevin-equivalence`](knowledge/thm-ho2020-score-matching-langevin-equivalence.md) — ε 参数化下：训练 ⟺ 多尺度去噪 score matching，采样 ⟺ Langevin dynamics。[ho2020] Updated 2026-06-28
- [`thm-song2021-reverse-time-sde`](knowledge/thm-song2021-reverse-time-sde.md) — Anderson 1982 reverse-time SDE（Eq 6）：只依赖 score 即可把噪声变回数据，整个生成框架的引擎。[song2021] Updated 2026-06-28
- [`thm-song2021-probability-flow-ode`](knowledge/thm-song2021-probability-flow-ode.md) — probability flow ODE（Eq 13）：与 SDE 共享边际的确定性 ODE（=neural ODE），解锁精确似然/唯一编码。[song2021] Updated 2026-06-28
- [`thm-song2021-sde-discretization-equivalence`](knowledge/thm-song2021-sde-discretization-equivalence.md) — SMLD→VE-SDE、DDPM→VP-SDE：两大离散方法是两个 SDE 的离散化（统一框架基石）。[song2021] Updated 2026-06-28

## Methods（8）

- [`meth-ho2020-epsilon-prediction`](knowledge/meth-ho2020-epsilon-prediction.md) — 反向均值 ε-预测参数化（Eq.11），统一钥匙。[ho2020] Updated 2026-06-28
- [`meth-ho2020-ddpm-training`](knowledge/meth-ho2020-ddpm-training.md) — Algorithm 1 + 简化目标 L_simple（Eq.14）。[ho2020] Updated 2026-06-28
- [`meth-ho2020-ddpm-sampling`](knowledge/meth-ho2020-ddpm-sampling.md) — Algorithm 2 ancestral sampling（T=1000 步）。[ho2020] Updated 2026-06-28
- [`meth-ho2020-variance-schedule`](knowledge/meth-ho2020-variance-schedule.md) — 固定线性 β 表（10⁻⁴→0.02）+ 固定反向 σ²。[ho2020] Updated 2026-06-28
- [`meth-song2021-score-based-training`](knowledge/meth-song2021-score-based-training.md) — 连续去噪 score matching 训练（Eq 7），ε-预测的连续时间推广。[song2021] Updated 2026-06-28
- [`meth-song2021-pc-sampler`](knowledge/meth-song2021-pc-sampler.md) — Predictor-Corrector 采样器（Sec 4.2）：数值 SDE solver + score MCMC 纠正，统一改进 SMLD/DDPM 采样器。[song2021] Updated 2026-06-28
- [`meth-song2021-pf-ode-sampling`](knowledge/meth-song2021-pf-ode-sampling.md) — PF-ODE 快速自适应采样 + 黑盒 ODE solver 精确似然（Sec 4.3）。[song2021] Updated 2026-06-28
- [`meth-song2021-conditional-sde`](knowledge/meth-song2021-conditional-sde.md) — 条件 reverse-time SDE（Eq 14）：单一无条件 score 模型做类条件生成/补全/着色。[song2021] Updated 2026-06-28

## Experiments（5）

- [`exp-ho2020-cifar10-results`](knowledge/exp-ho2020-cifar10-results.md) — 无条件 CIFAR-10 FID 3.17 / IS 9.46（Table 1，当时 SOTA）。[ho2020] Updated 2026-06-28
- [`exp-ho2020-lsun-results`](knowledge/exp-ho2020-lsun-results.md) — LSUN Church 7.89 / Bedroom 4.90 / CelebA-HQ 256，质量比肩 ProgressiveGAN。[ho2020] Updated 2026-06-28
- [`exp-ho2020-ablation`](knowledge/exp-ho2020-ablation.md) — 参数化×目标消融（Table 2）：ε+L_simple 必须**同时启用**才协同生效。[ho2020] Updated 2026-06-28
- [`exp-song2021-cifar10-results`](knowledge/exp-song2021-cifar10-results.md) — CIFAR-10 IS 9.89 / FID 2.20（无条件新纪录，超类条件 GAN）+ 精确 NLL 2.99 bits/dim。[song2021] Updated 2026-06-28
- [`exp-song2021-sampler-comparison`](knowledge/exp-song2021-sampler-comparison.md) — 采样器对比（Table 1）：predictor/corrector/PC/PF 四类在不同 NLL-FID 取舍。[song2021] Updated 2026-06-28

## Insights（5）

- [`ins-ho2020-simplified-objective-downweights`](knowledge/ins-ho2020-simplified-objective-downweights.md) — L_simple 降低小-t 权重，用码长换样本质量（FID 3.17 vs 13.51）。[ho2020] Updated 2026-06-28
- [`ins-ho2020-progressive-lossy-compression`](knowledge/ins-ho2020-progressive-lossy-compression.md) — ELBO = 率(ΣL_t)+失真(L_0)，扩散天生是有损压缩器（过半 bit 仅精修不可感知细节）。[ho2020] Updated 2026-06-28
- [`ins-ho2020-autoregressive-generalization`](knowledge/ins-ho2020-autoregressive-generalization.md) — 高斯扩散是「广义比特排序」的自回归解码（Eq.16）。[ho2020] Updated 2026-06-28
- [`ins-song2021-unified-continuous-framework`](knowledge/ins-song2021-unified-continuous-framework.md) — 连续时间统一框架：SMLD & DDPM 仅是不同 SDE 的离散特例，统一即力量。[song2021] Updated 2026-06-28
- [`ins-song2021-uniquely-identifiable-encoding`](knowledge/ins-song2021-uniquely-identifiable-encoding.md) — PF-ODE 给出唯一可识别编码（前向 SDE 无可训练参数 + 确定性 ODE）。[song2021] Updated 2026-06-28

## 入口提示

- **快速理解全貌**：读 `overview.md`（双源：DDPM 离散 + Score-SDE 连续，统一于 SDE 视角）。
- **查关系/遍历**：读 `dag/dag-index.json` 的 edges（跨源边见 `xsrc-*`）。
- **看提炼的思维方式**：读 `mental-models.md`（双源 4 心智模型）。
- **看来源与覆盖范围**：读 `sources/ho2020.md` / `sources/song2021.md`。
