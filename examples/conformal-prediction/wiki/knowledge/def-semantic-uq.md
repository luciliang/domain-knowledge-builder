---
id: def-semantic-uq
type: definition
label: Semantic Uncertainty Quantification
source: teneggi2025
section: Section 1 & Section 3
tokens: 800
created: 2026-06-23
---

## 精确表述

Semantic uncertainty quantification (semantic UQ) refers to expressing predictive uncertainty not at the pixel level, but in terms of clinically meaningful anatomical structures (semantic structures). In the context of CT imaging, this means:

1. **Pixel-level UQ** constructs uncertainty intervals for each pixel independently, using a single scalar or fixed-group adjustment parameter. The resulting uncertainty maps are not directly interpretable in clinical terms.

2. **Semantic UQ** leverages segmentation models to construct organ-dependent uncertainty intervals. Each organ $k$ receives its own uncertainty parameter $\lambda_k$, and the assignment of pixels to organs depends on the specific observation $y$ (instance-dependent). This produces uncertainty estimates that:
   - Are adaptive to each patient's anatomy and organ positioning
   - Can be communicated with clinically relevant features (e.g., "the liver has higher uncertainty than the spleen")
   - Enable per-organ risk control rather than only global coverage

The key distinction from pixel-level UQ is the **decoupling of uncertainty estimation from the pixel domain**: uncertainty is expressed in terms of semantic structures (organs), not individual pixels. This is especially important for heterogeneous data like CT scans, where patients' anatomies vary in size, shape, and positioning of organs, and a fixed partition matrix may unnecessarily increase the mean interval length.

语义不确定性量化是指将预测不确定性从像素层面提升到语义结构层面（如器官），使不确定性估计具有临床可解释性。

## 适用条件

- 需要一个固定的分割模型 $s$ 来定义语义结构
- 分割模型必须能识别临床相关的解剖结构
- 适用于解剖结构变异大的成像模态（如 CT）

## 直觉解释

像素级不确定性告诉医生"这个像素有多不确定"，但医生关心的是"这个器官有多不确定"。语义 UQ 将不确定性从像素映射到器官，使结果直接可用于临床决策。例如，λ̂_sem 直接显示哪些器官的不确定性更高，这对跨中心使用 AI 模型至关重要。

## 与其他知识的关系

→ meth-sem-crc（语义 UQ 通过 sem-CRC 方法实现）
contradicts → meth-k-crc（与固定分组的 K-CRC 形成对比：语义分组 vs. 固定分组）
applies_to → exp-ct-denoising-reconstruction（在 CT 实验中验证了语义 UQ 的优势）
depends_on → def-crc（理解语义 UQ 需先理解 CRC 的基本框架）

## 来源引用

- Teneggi et al. 2025, Sections 1 and 3
- Related: Angelopoulos et al. 2022 (image-to-image regression with UQ)
