---
id: src-angelopoulos2022
type: paper
title: "A Gentle Introduction to Conformal Prediction: Distribution-Free, Finite-Sample Validity Guarantees"
authors: ["Anastasios N. Angelopoulos", "Stephen Bates"]
year: 2022
venue: "arXiv:2107.07511"
nodes_extracted: ["def-split-conformal-prediction", "thm-split-cp-coverage", "def-marginal-coverage", "def-conditional-coverage", "thm-conditional-coverage-impossible", "meth-angelopoulos2022-aps", "meth-angelopoulos2022-cqr", "meth-conformalize-uncertainty", "meth-conformalize-bayes", "def-fsc-metric", "def-ssc-metric", "thm-beta-coverage-distribution", "meth-group-balanced-cp", "thm-group-balanced-coverage", "meth-class-conditional-cp", "thm-class-conditional-coverage", "thm-conformal-risk-control", "thm-covariate-shift-coverage", "thm-distribution-drift-coverage", "meth-outlier-detection-cp", "thm-outlier-detection-guarantee"]
ingested: 2026-06-24
---

## 核心贡献

本文是共形预测（Conformal Prediction）的综合性入门教程，系统覆盖了从基础 split CP 框架到高级扩展的完整知识体系。核心贡献包括：(1) 建立了 split CP 的标准流程与 Theorem 1 的 marginal coverage 保证；(2) 系统分类了四大 conformal 方法——APS（分类自适应集）、CQR（分位数回归共形化）、uncertainty scalars（不确定性标量共形化）、Bayes（贝叶斯模型共形化）；(3) 定义了 marginal vs conditional coverage 的关键区分及 conditional coverage 的不可能性定理；(4) 提出了 FSC/SSC 两类 conditional coverage 近似度量；(5) 给出了 group-balanced CP、class-conditional CP、CRC、covariate shift、distribution drift、outlier detection 六大扩展方向的定理与方法。

## 提取的知识节点

| 节点ID | 类型 | 名称 |
|--------|------|------|
| def-split-conformal-prediction | definition | Split Conformal Prediction (Inductive) |
| thm-split-cp-coverage | theorem | Theorem 1: Conformal Coverage Guarantee (Split CP) |
| def-marginal-coverage | definition | Marginal Coverage |
| def-conditional-coverage | definition | Conditional Coverage |
| thm-conditional-coverage-impossible | theorem | Conditional Coverage Impossibility |
| meth-angelopoulos2022-aps | method | Adaptive Prediction Sets (APS) |
| meth-angelopoulos2022-cqr | method | Conformalized Quantile Regression (CQR) |
| meth-conformalize-uncertainty | method | Conformalizing Scalar Uncertainty Estimates |
| meth-conformalize-bayes | method | Conformalizing Bayes |
| def-fsc-metric | definition | Feature-Stratified Coverage (FSC) Metric |
| def-ssc-metric | definition | Size-Stratified Coverage (SSC) Metric |
| thm-beta-coverage-distribution | theorem | Beta Distribution of Coverage (Vovk 2012) |
| meth-group-balanced-cp | method | Group-Balanced Conformal Prediction |
| thm-group-balanced-coverage | theorem | Proposition 1: Group-Balanced CP Validity |
| meth-class-conditional-cp | method | Class-Conditional Conformal Prediction |
| thm-class-conditional-coverage | theorem | Proposition 2: Class-Conditional CP Validity |
| thm-conformal-risk-control | theorem | Theorem 2: Conformal Risk Control |
| thm-covariate-shift-coverage | theorem | Theorem 3: Conformal Prediction Under Covariate Shift |
| thm-distribution-drift-coverage | theorem | Theorem 4: Conformal Prediction Under Distribution Drift |
| meth-outlier-detection-cp | method | Conformal Outlier Detection |
| thm-outlier-detection-guarantee | theorem | Proposition 3: Outlier Detection Error Control |

## 与其他来源的关系

- **基础于 Vovk et al. (1999, 2005)**：split CP 的 exchangeability 框架源自 online conformal prediction
- **引用 Vovk (2012)**：conditional coverage 不可能性定理与 Beta 分布覆盖
- **引用 Lei & Wasserman (2014), Barber et al. (2021)**：conditional coverage 不可能性的精化
- **引用 Romano, Sesia & Candès (2020)**：APS 方法与 SSC 度量
- **引用 Romano, Patterson & Candès (2019)**：CQR 方法
- **引用 Sadinle et al. (2019)**：class-conditional CP
- **引用 Hoff (2021)**：Bayes 最优性
- **引用 Tibshirani et al. (2019)**：covariate shift CP (Theorem 3)
- **引用 Barber et al. (2022)**：distribution drift CP (Theorem 4)
- **被 Teneggi et al. (2025) 引用**：CRC (Theorem 2) 被 P3 的 sem-CRC 框架直接继承
- **被 Min et al. (2026) 引用**：covariate shift 定理在 P4 的 WCP 分析中被扩展（WCP 恢复 marginal 但不恢复 conditional）

## 未提取的内容

- Full conformal prediction (CV+, Jackknife+) 的详细推导——作为 split CP 的替代方法提及但未单独提取
- Nelson (2020) 的高维扩展（目录中提及但未展开）
- 计算复杂度与实际部署细节的深入讨论
- 论文中的全部实验与图表数据（侧重于理论框架提取）
