---
id: src-teng2021-tsci
type: paper
value: both
channel: user
file: inputs/papers/teng2021-tsci.pdf
locator:
  page: 1
  section: "Abstract + §1 Introduction + §3 Preliminary"
collected_at: 2026-06-28
format: pdf
title: "T-SCI: A Two-Stage Conformal Inference Algorithm with Guaranteed Coverage for Cox-MLP"
authors: ["Jiaye Teng", "Zeren Tan", "Yang Yuan"]
year: 2021
venue: "arXiv:2103.04556"
---

## 来源摘要

滕佳烨第一作者早期工作（清华 IIIS，师从袁洋）。把 conformal inference 引入 Cox-MLP（神经网络版 Cox 回归）生存分析，恢复被放松线性假设破坏的 guaranteed coverage。

### 核心贡献

- 提出 **WCCI**（Weighted Conformal Censoring Inference）：在 strong ignorability（`T ⊥ Δ | X`）下用基于 partial likelihood 的 non-conformity score + weighted conformal inference 处理 censoring 引起的 covariate shift
- 提出 **T-SCI**（Two-Stage Conformal Inference）：第一阶段跑 WCCI，第二阶段用 quantile conformal inference 校准，返回"nearly perfect" coverage（既有 lower bound 也有 upper bound 保证）
- 理论：WCCI 与 T-SCI 在 milder 假设下都返回 guaranteed coverage
- 实验：合成数据 + 真实数据，T-SCI 在 empirical coverage 和 interval length 上均优

### 覆盖范围

本来源覆盖知识节点 `thm-teng2021-tsci-coverage`、`meth-teng2021-weighted-conformal`、`meth-teng2021-two-stage-calibration`，并体现滕佳烨「coverage 是底线 + 两阶段校准逼近精确」的心智（支撑心智模型 `mm-teng-coverage-as-floor`）。

### 可信度

**高**。滕佳烨本人第一作者，PDF 由用户提供（pdftotext 提取），与 conformal-prediction 经典文献（Vovk、Lei-Candès、Romano）引用链一致。censoring/strong ignorability 是生存分析标准假设。
