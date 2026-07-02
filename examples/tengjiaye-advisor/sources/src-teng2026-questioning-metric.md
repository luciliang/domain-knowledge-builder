---
id: src-teng2026-questioning-metric
type: paper
value: both
channel: user
file: inputs/papers/teng2026-questioning-metric.pdf
locator:
  page: 1
  section: "Abstract + §1 Introduction (Example 1, Algorithm 1, Theorem 1.1)"
collected_at: 2026-06-28
format: pdf
title: "Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter Intervals Are Not Better (ICML 2026)"
authors: ["Yizhou Min", "Yizhou Lu", "Lanqi Li", "Zhen Zhang", "Jiaye Teng"]
year: 2026
venue: "ICML 2026 (arXiv:2601.21455)"
---

## 来源摘要

滕佳烨通讯作者（上海财经大学）。**反思 CP 的标准评估度量**。证明 coverage-length 指标可被欺骗，更短区间不一定更好。

### 核心贡献

- **Prejudicial Trick (PT)**（Algorithm 1）：对每个测试点，以概率 `p` 返回 adjusted-confidence-level 区间 `A_{1-α'}(x')`（`α' = 1 - (1-α)/p`），以概率 `1-p` 返回 null/单点区间。期望意义下 coverage 仍 valid，但平均 length 可欺骗性降低
- **Example 1（医生 Alice vs Bob）**：Bob 以 0.75 概率返回 [0,5]、0.25 概率返回 [0,0]，平均长度 3.75 < Alice 的 4，coverage 相同，但同一病人多次查询得到完全不同区间——实用性脆弱
- **Theorem 1.1 总结**：
  - coverage：PT 保持 marginal coverage，甚至在 base 不满足时也能改善 conditional coverage
  - length：PT 在一般条件下（可微/不可微 length 函数、model misspecification）返回更短平均区间
- **新度量**：**interval stability**（同一输入多次运行区间的一致性），用于检测新 CP 方法是否隐式用了 PT-like 技巧

### 覆盖范围

本来源覆盖知识节点 `thm-teng2026-prejudicial-trick`、`def-teng2026-interval-stability`，是滕佳烨「质疑标准度量（coverage-length 可被欺骗，更短≠更好）」心智（`mm-teng-question-standard-metric`）的核心依据，也是反模式 `ap-teng-blind-shorter-better` 的来源。

### 可信度

**高**。ICML 2026 正式发表（Proceedings of the 43rd ICML, PMLR 306），滕佳烨通讯作者，代码开源（github.com/benben-cd/PT-Conformal-Prediction）。是滕佳烨批判性思维的代表作。
