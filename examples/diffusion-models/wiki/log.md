---
title: Diffusion Models — Ingest Log
domain: diffusion-models
---

# Ingest 日志

| 日期 | 来源 | 新增节点 | 新增边 | run_id | 模式 | 摘要 |
|------|------|----------|--------|--------|------|------|
| 2026-06-28 | ho2020 — Denoising Diffusion Probabilistic Models (Ho et al. NeurIPS 2020) | 15 | 22 | `09207eda-1bc6-46b7-a8f3-779abb928d4f` | text_fallback | 初始化领域知识库。单源 DDPM：3 def / 2 thm / 4 meth / 3 exp / 3 ins。S1 pdftotext 提取；S2 结构化提取（provenance 完整）；S3 单源结构化校验通过（0 断裂/重复/孤立，meta 计数一致）；S4 导航；S5 心智模型三重验证。 |
| 2026-06-28 | song2021 — Score-Based Generative Modeling through SDEs (Song et al. ICLR 2021) | 15 | 31 | `9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9` | ar5iv_html | **增量 ingest，知识库升级为双源**。+Score-SDE：4 def / 3 thm / 4 meth / 2 exp / 2 ins（连续时间统一框架、reverse-time SDE、probability flow ODE、PC 采样器）。S2 ar5iv HTML 提取（663 LaTeX 公式完整保留）；**S3 增量合并**：DAG 30 节点/53 边，含 11 跨源（10 `generalizes`/`extends` 经 schema §3 方向归一翻转），无 contradicts，校验全过（0 断裂/重复/孤立/路径违规）；**S4** 导航双源化；**S5** 重提炼（双源 4 心智模型，新增 M4 连续时间统一）。 |

## 待补

- **Song et al. 2021 (Score-SDE)** — ✅ **已完成（2026-06-28 增量 ingest）**：连续时间统一视角、reverse-time SDE/ODE、probability flow ODE、PC 采样器已覆盖（见上行）。建立的 11 条离散↔连续跨源 `generalizes`/`extends`/`compares_with` 边已写入 `dag/dag-index.json`（`xsrc-*`）。
- **DDIM**（Song et al. 2021, ICLR）：非马尔可夫快速/确定性采样——Score-SDE 的 PF-ODE 提供了 ODE 视角的确定性采样，但 DDIM 具体的非马尔可夫前向族仍未单独 ingest。
- **引导采样**：classifier guidance（Dhariwal & Nichol 2021）/ classifier-free guidance（Ho & Salimans 2022）。
- **潜空间扩散**：latent diffusion / Stable Diffusion（Rombach et al. 2022）。
