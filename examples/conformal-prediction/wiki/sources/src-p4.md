---
id: src-min2026
type: paper
title: A Unified Theory of Conditional Coverage for Conformal Prediction
authors: [Yinjie Min, Liuhua Peng, Changliang Zou]
year: 2026
venue: arXiv:2605.11602v3 [stat.ME]
nodes_extracted: [def-unified-cp-framework, thm-marginal-coverage-weighted, thm-three-term-decomposition, def-three-errors, thm-averaged-miscoverage, thm-cc-averaged, meth-model-selection-cc, thm-covariate-shift-marginal, meth-covariate-shift-conditional, thm-symmpi-structured, thm-symmpi-conditional, meth-min2026-graphcp, thm-community-conditional, ins-method-comparison-table, ins-intrinsic-error-necessity, exp-covariate-shift, exp-model-selection, exp-toloker-graph, def-conditional-coverage, ins-wcp-limitation]
ingested: 2026-06-24
---

## 核心贡献

This paper develops a unified framework for conditional coverage in conformal prediction via weighted conformal quantiles. The central contribution is a non-asymptotic decomposition of conditional miscoverage into three interpretable components: score-estimation error, finite-sample calibration error, and intrinsic conditional-mismatch error. This decomposition clarifies existing methods, provides principled guidance for model selection, and extends naturally to covariate shift and structured data (graphs, hierarchies).

## 提取的知识节点

| 节点ID | 类型 | 名称 |
|--------|------|------|
| def-unified-cp-framework | definition | Unified CP Framework via Weighted Conformal Quantiles |
| thm-marginal-coverage-weighted | theorem | Theorem 1: Marginal Coverage of Weighted CP |
| thm-three-term-decomposition | theorem | Theorem 2: Three-Term Conditional Miscoverage Decomposition |
| def-three-errors | definition | Three Components of Conditional Miscoverage |
| thm-averaged-miscoverage | theorem | Theorem 3: Averaged Conditional Miscoverage under Weak Conditions |
| thm-cc-averaged | theorem | Corollary 1: Averaged Conditional Miscoverage of CC |
| meth-model-selection-cc | method | Conditional-Coverage-Oriented Model Selection |
| thm-covariate-shift-marginal | theorem | Theorem 4: Marginal Coverage under Covariate Shift |
| meth-covariate-shift-conditional | method | Conditional Methods under Covariate Shift |
| thm-symmpi-structured | theorem | Theorem 5: Marginal Coverage under SymmPI |
| thm-symmpi-conditional | theorem | Theorem 6: Conditional Miscoverage under SymmPI |
| meth-min2026-graphcp | method | GraphCP: Community-Conditional CP on Graphs |
| thm-community-conditional | theorem | Theorem 7: Community-Conditional Miscoverage Convergence |
| ins-method-comparison-table | insight | Unified Error Decomposition Across Methods |
| ins-intrinsic-error-necessity | insight | Intrinsic Error is the Key Bottleneck |
| exp-covariate-shift | experiment | Conditional Methods under Covariate Shift (Synthetic) |
| exp-model-selection | experiment | Model Selection Experiments |
| exp-toloker-graph | experiment | GraphCP on Toloker Dataset |
| def-conditional-coverage | definition | Conditional Coverage Notions in CP |
| ins-wcp-limitation | insight | WCP Restores Marginal but Not Conditional Coverage |

## 与其他来源的关系

- **Extends** src-teneggi2025 (P3): P3 focuses on conformal risk control (marginal), P4 provides the unified conditional coverage theory that subsumes marginal as a special case
- **Cites** extensively: Vovk et al. 2005, Lei et al. 2013/2018, Romano et al. 2019, Chernozhukov et al. 2021, Guan 2023, Hore & Barber 2025, Gibbs et al. 2025, Dobriban & Yu 2025, Jung et al. 2023
- **Extends** Angelopoulos et al. 2024 theoretical foundations with a non-asymptotic conditional-specific decomposition

## 未提取的内容

- S1 detailed per-method unified specifications (LCP, RLCP, CQR, DCP, GLCP, BatchGCP, CC) — summarized via Table 1 insight node
- S2.2 CC under covariate shift (Corollary S7)
- S3 Weighted SymmPI framework with ratio functions
- S4 GRLCP (generalized RLCP), localized conformal p-values, two-layer hierarchical model
- S5-S9 Proofs, preliminary lemmas, technical discussions
- S10 Additional numerical experiments (more DGPs, dimensions, implementation details)
- Efficient approximation algorithm for model selection (Section S5.3)
