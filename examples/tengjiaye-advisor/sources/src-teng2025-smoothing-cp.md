---
id: src-teng2025-smoothing-cp
type: paper
value: both
channel: user
file: inputs/papers/teng2025-smoothing-cp.pdf
locator:
  page: 1
  section: "Abstract + §1 Introduction + §3 Method + Theorem 4.1/4.2/4.3/4.4"
collected_at: 2026-06-28
format: pdf
title: "Smoothing-Based Conformal Prediction for Balancing Efficiency and Interpretability (SCD-split)"
authors: ["Mingyi Zheng", "Hongyu Jiang", "Yizhou Lu", "Jiaye Teng"]
year: 2025
venue: "arXiv:2509.22529"
---

## 来源摘要

滕佳烨通讯作者（上海财经大学）。提出 **SCD-split**——在 CD-split（conditional density split CP）基础上引入 smoothing，解决"预测集由多个断开子区间组成、难以解释"的实用性问题。

### 核心贡献

- **问题识别**：CD-split 用 conditional density 作 conformity score 提升效率，但在多模态分布下生成大量断开子区间，损害 interpretability
- **新度量**：把 **断开子区间数量（connectivity/number of disjoint intervals）** 作为 CP 的新度量，与 interval length 共同刻画 interpretability
- **SCD-split 方法**：用户指定期望子区间数 → 对 conditional density 做 Fourier smoothing → validation 调参使子区间数逼近目标
- **理论三保证**：
  - Theorem 4.1（validity）：smoothing 保持 marginal coverage ≥ 1-α
  - Theorem 4.2（connectivity 不增）：smoothing 后子区间数不增
  - Theorem 4.3（narrow-valley double peaks 下严格减少子区间数）
  - Theorem 4.4（length upper bound）：smoothing 后区间长度有上界

### 覆盖范围

本来源覆盖知识节点 `meth-teng2025-scd-split`、`thm-teng2025-smoothing-connectivity`、`def-teng2025-connectivity-metric`，是滕佳烨「coverage 是底线但要平衡效率与可解释性」心智（`mm-teng-balance-efficiency-interpretability`）的直接依据。

### 可信度

**高**。滕佳烨通讯作者，arXiv 预印本。明确了"interval length 不是唯一目标"——这与 questioning-metric 一脉相承，是滕佳烨质疑标准度量的早期体现。
