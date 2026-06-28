---
id: src-teng2023-feature-cp
type: paper
value: both
channel: user
file: inputs/papers/teng2023-feature-cp.pdf
locator:
  page: 1
  section: "Abstract + §1 Introduction + §3 Preliminaries + Algorithm 1"
collected_at: 2026-06-28
format: pdf
title: "Predictive Inference with Feature Conformal Prediction (ICLR 2023)"
authors: ["Jiaye Teng", "Chuan Wen", "Dinghuai Zhang", "Yoshua Bengio", "Yang Gao", "Yang Yuan"]
year: 2023
venue: "ICLR 2023 (arXiv:2210.00173)"
---

## 来源摘要

**滕佳烨代表作**（ICLR 2023，合著 Bengio/袁洋）。提出 **Feature Conformal Prediction (FCP)**——把 conformal prediction 从输出空间扩展到语义特征空间，利用深度表示的归纳偏置。

### 核心贡献

- **Feature CP 框架**：把 `µ̂ = ĝ ∘ f̂` 拆成 feature function `f̂`（前几层）和 prediction head `ĝ`（后几层），在 feature space 而非 output space 做 CP
- 解决两个问题：(a) feature space 无 ground truth → 提出 **surrogate feature** 作为 non-conformity score 的替代项；(b) feature space 的 confidence band 转 output space 非平凡 → 提出 **Band Estimation**（算上界）与 **Band Detection**（判定响应是否落在 band 内）
- **理论（Theorem 6）**：在 **cubic conditions**（length preserving / expansion / quantile stability）下，Feature CP provably 返回比 vanilla CP 更短的 confidence band，且 coverage 有效
- 实验：合成 + ImageNet 分类 + Cityscapes 像素级分割，SOTA；可插入 CQR 等 adaptive CP

### 覆盖范围

本来源覆盖知识节点 `thm-teng2023-feature-cp-advantage`、`meth-teng2023-surrogate-feature`、`meth-teng2023-band-estimation`，是滕佳烨「特征空间优于输出空间」核心心智（`mm-teng-feature-space-superior`）的直接依据。

### 可信度

**高**。ICLR 2023 正式发表（Published as a conference paper at ICLR 2023），Bengio 合著。代码开源（github.com/AlvinWen428/FeatureCP）。PDF 由用户提供。是滕佳烨研究主线的奠基工作。
