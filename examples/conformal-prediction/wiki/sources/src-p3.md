---
id: src-teneggi2025
type: paper
title: "Conformal Risk Control for Semantic Uncertainty Quantification in Computed Tomography"
authors: ["Jacopo Teneggi", "J Webster Stayman", "Jeremias Sulam"]
year: 2025
venue: "arXiv:2503.00136 [cs.CV]"
nodes_extracted: ["def-teneggi2025-crc", "def-conformal-coverage", "meth-k-crc", "meth-sem-crc", "thm-sem-crc-validity", "meth-sem-crc-per-organ", "def-semantic-uq", "exp-ct-denoising-reconstruction", "ins-semantic-uq-clinical"]
ingested: 2026-06-23
---

## 核心贡献

本文提出 sem-CRC，一种语义自适应的共形风险控制方法，用于 CT 图像的不确定性量化。通过结合分割模型，sem-CRC 构建器官依赖的不确定性区间，在保证高风险控制的同时产生更紧的区间。方法可特化为逐器官风险控制（sem-CRC̄），在真实 CT 数据（TotalSegmentator、FLARE23）上验证有效。

## 提取的知识节点

| 节点ID | 类型 | 名称 |
|--------|------|------|
| def-teneggi2025-crc | definition | Conformal Risk Control (CRC) |
| def-conformal-coverage | definition | Conformal Risk Control Guarantee |
| meth-k-crc | method | K-CRC (High-Dimensional Risk Control) |
| meth-sem-crc | method | sem-CRC (Semantic Conformal Risk Control) |
| thm-sem-crc-validity | theorem | Proposition 1: Validity of sem-CRC |
| meth-sem-crc-per-organ | method | sem-CRC̄ (Per-Organ Risk Control) |
| def-semantic-uq | definition | Semantic Uncertainty Quantification |
| exp-ct-denoising-reconstruction | experiment | CT Denoising and FBP-UNet Experiments |
| ins-semantic-uq-clinical | insight | Clinical Value of Semantic UQ |

## 与其他来源的关系

- **引用并扩展 Angelopoulos et al. 2024 (CRC)**：将 CRC 从标量参数扩展到语义分组，核心保证基于 CRC 的 Theorem 1
- **扩展 Teneggi et al. 2023 (ICML)**：将 K-CRC 方法（原用于 RCPS/diffusion models）扩展到语义级别
- **使用 SuPrem (Li et al. 2024) 分割模型**：作为语义分组的来源，但不对分割模型进行校准
- **与 Bates et al. 2021 (RCPS) 相关**：CRC 与 RCPS 是等价的框架，本文方法可推广到 RCPS（需多重假设检验校正）
- **CT 数据集**：TotalSegmentator (Wasserthal et al. 2023)、FLARE23 (Ma et al. 2022)、AbdomenAtlas-8K (Qu et al. 2023)

## 未提取的内容

- 分位数回归（quantile regression）的详细训练过程——作为标准方法未展开提取
- 分割模型 SuPrem 的具体架构——非本文贡献，作为工具使用
- FBP-UNet 重建管线的工程细节——辅助实验设置
- 与其他高维 CP 方法（如 Le Bars & Humbert 2025, Kiyani et al. 2024）的详细比较——论文中未深入讨论
