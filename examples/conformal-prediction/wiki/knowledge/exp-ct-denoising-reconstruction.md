---
id: exp-ct-denoising-reconstruction
type: experiment
label: "CT Denoising and FBP-UNet Reconstruction Experiments"
source: teneggi2025
section: Section 4, Table 1, Figures 2-3
tokens: 1400
created: 2026-06-23
---

## 精确表述

**Datasets**: TotalSegmentator (1,429 scans) and FLARE23 (first 1,000 scans from training split). Resolution resampled to 1.5mm × 1.5mm × 3.0mm, windowed between −175 HU and 250 HU.

**Tasks**:
- **Denoising**: Add independent Gaussian noise with σ = 0.2
- **FBP-UNet reconstruction**: Simulated helical cone beam geometry (ODL + ASTRA), 8 turns, 1,000 angles, detector 512×128 pixels, low-dose Poisson noise with $I_0 = 1,000$

**Training**: 3D UNet (~5M parameters, ROI 96³ voxels) with quantile regression (α = 0.1) on AbdomenAtlas-8K (5,195 scans)

**Segmentation**: 9 structures (spleen, kidneys, gallbladder, liver, stomach, aorta, IVC, pancreas) using SuPrem model; remaining non-background voxels labeled "body". Mean structure-wise F1: 0.85±0.07 (TotalSegmentator denoising), 0.83±0.08 (FBP-UNet), 0.88±0.06 / 0.87±0.07 (FLARE23).

**Calibration setup**: ϵ = 0.10, n_cal = 512 scans, n_test = 128 scans, n_opt = 32 samples. K = 4 groups for K-CRC. 20 independent runs.

### Key Results (Table 1, ϵ = 0.10):

| Task | Method | TS Risk | TS Length (×10⁻²) | FL Risk | FL Length (×10⁻²) |
|------|--------|---------|-------------------|---------|-------------------|
| Denoising | CRC | 0.095±0.006 | 11.60±0.21 | 0.096±0.004 | 9.16±0.09 |
| Denoising | K-CRC | 0.097±0.006 | 9.37±0.20 | 0.096±0.006 | 6.81±0.21 |
| Denoising | sem-CRC | 0.098±0.006 | **8.72±0.18** | 0.095±0.006 | **6.36±0.11** |
| Denoising | sem-CRC̄ | 0.055±0.004 | 11.84±0.20 | 0.056±0.003 | 8.06±0.16 |
| FBP-UNet | CRC | 0.098±0.007 | 10.43±0.23 | 0.095±0.006 | 6.19±0.09 |
| FBP-UNet | K-CRC | 0.098±0.009 | 9.32±0.13 | 0.095±0.003 | 6.20±0.14 |
| FBP-UNet | sem-CRC | 0.097±0.007 | **8.95±0.19** | 0.095±0.006 | **6.18±0.13** |
| FBP-UNet | sem-CRC̄ | 0.059±0.005 | 12.43±0.20 | 0.057±0.003 | 7.72±0.17 |

**Main findings**:
1. All procedures achieve valid risk control (Risk ≤ ϵ = 0.10)
2. sem-CRC consistently provides the **shortest intervals** (24-32% reduction vs CRC)
3. sem-CRC̄ (per-organ) increases mean interval length but provides per-organ guarantee
4. Uncertainty maps from sem-CRC are sharper and contain fewer artifacts
5. λ̂_sem reveals organ-specific uncertainty patterns that differ across populations (Fig 2)
6. Only sem-CRC̄ achieves risk control for each organ; all other methods overcover background and undercover organs (Fig 3)

## 适用条件

- 实验在真实 CT 数据上验证，非合成数据
- 分割模型质量影响 sem-CRC 的效果（F1 ≈ 0.83-0.88）
- 需要足够的校准数据（n_cal = 512）
- 结果可能不直接推广到其他成像模态

## 直觉解释

实验清晰地展示了从 CRC → K-CRC → sem-CRC 的渐进改进：每一步都保持了风险控制保证，但区间越来越紧。sem-CRC 的优势在 CT 上尤为明显，因为不同器官的重建难度差异很大。更重要的是，λ̂_sem 向量本身就是有价值的临床信息。

## 与其他知识的关系

← meth-sem-crc（验证 sem-CRC 方法）
← meth-k-crc（K-CRC 作为对比基线）
← def-teneggi2025-crc（CRC 作为对比基线）
← meth-sem-crc-per-organ（sem-CRC̄ 的实验验证）
evaluates → meth-sem-crc（实验证明 sem-CRC 优于 K-CRC 和 CRC）

## 来源引用

- Teneggi et al. 2025, Section 4, Table 1, Figures 2-3
- Datasets: TotalSegmentator (Wasserthal et al. 2023), FLARE23 (Ma et al. 2022)
- Segmentation: SuPrem (Li et al. 2024)
