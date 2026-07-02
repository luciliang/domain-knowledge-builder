---
id: src-angelopoulos-bates-2022
type: paper
value: knowledge
channel: user
file: inputs/papers/p1-angelopoulos-bates-2022.pdf
locator:
  page: 1
  section: "Abstract + §1-2 (split CP, exchangeability, coverage theorem)"
collected_at: 2026-06-28
format: pdf
title: "A Gentle Introduction to Conformal Prediction: Distribution-Free, Finite-Sample Validity Guarantees"
authors: ["Anastasios N. Angelopoulos", "Stephen Bates"]
year: 2022
venue: "Foundations and Trends in Machine Learning (arXiv:2107.07511)"
---

## 来源摘要

CP 入门权威综述（Angelopoulos-Bates）。系统介绍 split CP 的 exchangeability 假设、finite-sample distribution-free coverage 保证、APS/RAPS 等非一致性分数。是 conformal-prediction 知识节点的核心来源，滕佳烨论文反复引用。

### 核心贡献（CP 基础，被滕佳烨复用）

- **Split CP coverage 定理**：在 exchangeability 下，`P(Y_test ∈ C(X_test)) ≥ 1-α`（finite-sample, distribution-free）
- **exchangeability**：比 i.i.d. 更弱，是 CP 保证的基石
- **APS / RAPS**：分类任务的非一致性分数，RAPS 在 APS 基础上做正则化缩短预测集

### 覆盖范围

本来源覆盖知识节点 `thm-split-cp-coverage`、`def-angelopoulosbates2022-exchangeability`、`meth-aps-raps`（CP 基础，复用 conformal-prediction 示例），为滕佳烨所有工作提供理论底盘。

### 可信度

**高**。Foundations and Trends 正式发表，CP 领域标准入门。PDF 由用户提供。
