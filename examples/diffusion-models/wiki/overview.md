---
title: Diffusion Models — Domain Overview
domain: diffusion-models
last_updated: 2026-06-28
sources: [ho2020, song2021]
---

# Diffusion Models — 领域概览（双源：DDPM + Score-SDE）

## 什么是扩散模型

扩散模型（diffusion model）是一类潜变量生成模型，把生成拆成两个互为镜像的过程：一条**固定的前向（加噪）过程**逐步向数据注入噪声直至信号被完全破坏成纯噪声；和一条**学习的反向（去噪）过程**从纯噪声出发逐步还原出干净样本。本知识库的两篇来源，恰好代表这个领域的两个互补视角：

- **离散时间视角（ho2020 DDPM）**：前向/反向都是离散马尔可夫链，训练最小化负对数似然的**变分下界（ELBO）**。因为前向是线性高斯，所有 KL 项可闭式计算。核心定义见 `def-ho2020-forward-diffusion-process` / `def-ho2020-reverse-process` / `def-ho2020-forward-posterior`，理论根基见 `thm-ho2020-elbo-variational-bound`。
- **连续时间视角（song2021 Score-SDE）**：把前向/反向写成**连续时间随机微分方程（SDE）**——前向 SDE `dx=f(x,t)dt+g(t)dw` 平滑破坏数据，其 reverse-time SDE（Anderson 1982）只依赖 score $\nabla_x\log p_t(x)$ 即可生成。见 `def-song2021-forward-sde` / `def-song2021-score-function` / `thm-song2021-reverse-time-sde`。

> **统一点**：song2021 证明 DDPM（VP-SDE）与 SMLD/NCSN（VE-SDE）都只是某个连续 SDE 的离散化（`thm-song2021-sde-discretization-equivalence` / `ins-song2021-unified-continuous-framework`）。离散与连续、概率扩散与 score-based，在连续时间 SDE 框架下被统一为「估计 score $\nabla_x\log p_t(x)$」这同一任务——这就是本领域最具生成力的统一镜片（见 `mental-models.md` M4）。

## ho2020（DDPM）的核心贡献

Ho et al. 2020 使扩散模型首次成为实用的高质量图像生成器，贡献有三条主线：(1) **实证里程碑**——无条件 CIFAR-10 取得 FID 3.17，优于当时多数类条件模型，256×256 LSUN/CelebA-HQ 质量比肩 ProgressiveGAN（`exp-ho2020-cifar10-results` / `exp-ho2020-lsun-results`）。(2) **两个协同设计**——用网络预测加入的噪声 ε（而非均值或 x₀），以去加权的简化目标 L_simple 训练；消融表明二者必须**同时启用**才协同生效（`meth-ho2020-epsilon-prediction` / `meth-ho2020-ddpm-training` / `exp-ho2020-ablation`）。(3) **理论统一（自述首要贡献）**——ε 参数化下，训练目标 ⟺ 跨噪声尺度的去噪 score matching，采样过程 ⟺ Langevin dynamics，且采样系数由前向 β 严格推导而非手工设定（`thm-ho2020-score-matching-langevin-equivalence`）。另把 ELBO 改写为广义自回归解码（`ins-ho2020-autoregressive-generalization`）与渐进有损压缩（率-失真，`ins-ho2020-progressive-lossy-compression`）。

## song2021（Score-SDE）的核心贡献

Song et al. 2021 把 score-based 生成统一到连续时间 SDE 框架，是 DDPM 之后的理论里程碑：(1) **连续时间统一框架**——SMLD 与 DDPM 被证明是 VE-SDE / VP-SDE 两个不同 SDE 的离散化（`thm-song2021-sde-discretization-equivalence`），统一了此前独立的两大方法。(2) **灵活采样**——Predictor-Corrector（PC）采样器（数值 SDE solver + score MCMC 纠正）统一并改进了 SMLD/DDPM 各自的采样器（`meth-song2021-pc-sampler`）。(3) **probability flow ODE**——与 SDE 共享边际分布的确定性 ODE（=neural ODE），带来精确似然、唯一可识别编码、latent 操控、快速自适应采样（`thm-song2021-probability-flow-ode` / `meth-song2021-pf-ode-sampling` / `ins-song2021-uniquely-identifiable-encoding`）。(4) **可控生成**——conditional reverse-time SDE 使单一无条件 score 模型做类条件生成/补全/着色（`meth-song2021-conditional-sde`）。(5) **SOTA**——CIFAR-10 IS 9.89 / FID 2.20（无条件新纪录，超类条件 GAN）、精确似然 2.99 bits/dim（新纪录）（`exp-song2021-cifar10-results`）。

## 双源如何互相对齐（跨源关系）

song2021 的核心价值之一就是把 DDPM 纳入连续时间统一框架。11 条跨源边（见 `dag/dag-index.json` 的 `xsrc-*`，方向已按 schema §3 归一）建立离散↔连续联系，要点：

- **前向过程**：DDPM 高斯前向链是 VP-SDE 的离散化（`def-ho2020-forward-diffusion-process` → `def-song2021-vp-sde`，generalizes）。
- **反向过程**：DDPM 学习到的反向链是 reverse-time SDE 的离散化（`def-ho2020-reverse-process` → `thm-song2021-reverse-time-sde`，generalizes）；DDPM ancestral sampling 是 PC 采样器的 predictor-only 退化（`meth-ho2020-ddpm-sampling` → `meth-song2021-pc-sampler`，generalizes）。
- **score 等价**：ho2020 的启发式等价（训练≈score matching、采样≈Langevin，离散）被提升为框架级定理（`thm-ho2020-score-matching-langevin-equivalence` → `thm-song2021-sde-discretization-equivalence`，extends）；ε-预测即加权去噪 score matching（`meth-ho2020-epsilon-prediction` → `meth-song2021-score-based-training`，extends）。
- **似然**：DDPM 只给 ELBO 上界，PF-ODE 给出**精确**似然，严格更强（`thm-ho2020-elbo-variational-bound` → `thm-song2021-probability-flow-ode`，extends）。
- **实证对比**：CIFAR-10 直比 FID 2.20 vs 3.17、NLL 2.99 vs ≤3.75（`exp-song2021-cifar10-results` ↔ `exp-ho2020-cifar10-results`，compares_with）。

## 应用与影响

扩散模型确立了「高质量、稳定训练、无需对抗」的生成范式，奠定了后续 latent diffusion / Stable Diffusion、条件生成（classifier / classifier-free guidance）、快速采样（DDIM）等技术的基础。其「粗→细」的渐进生成（大尺度结构先现、细节最后补全）与天然的有损压缩归纳偏置（`ins-ho2020-progressive-lossy-compression`），使其在图像合成上特别有效；连续时间 SDE 视角进一步把生成、似然、可控、编码统一在 score 框架下（`ins-song2021-unified-continuous-framework`）。

## 本知识库覆盖范围

- **已覆盖（双源）**：DDPM 的前向/反向/后验、ELBO 分解、ε-预测、L_simple、ancestral 采样、固定方差表、CIFAR-10/LSUN/ablation 实验；Score-SDE 的前向/VE/VP SDE、reverse-time SDE、probability flow ODE、离散-连续等价、score 训练、PC 采样器、PF-ODE 采样、conditional SDE、CIFAR-10 SOTA 实验；以及率-失真/自回归推广/统一框架/唯一编码等洞察。提炼出的双源思维镜片见 `mental-models.md`（4 心智模型）。
- **未覆盖（诚实边界）**：DDIM（非马尔可夫快速/确定性采样的具体前向族，虽 PF-ODE 提供 ODE 视角但 DDIM 本身未单独 ingest）、classifier / classifier-free guidance、latent diffusion / Stable Diffusion、各 SDE 反向 SDE 闭式（Appendix E 推导未提取）。
