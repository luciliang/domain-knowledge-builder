---
id: exp-model-selection
type: experiment
label: Conditional-Coverage-Oriented Model Selection Experiments
source: min2026
section: Section 5.1.2, Figure 1
tokens: 1000
created: 2026-06-24
---

## 精确表述

Experiments evaluate the model selection procedure from Section 4.1 under DGP1–DGP3 with 20 candidate CQR-type conformal prediction sets. Selection strategies compared: AvgLoss, AvgRankLoss (proposed), EffSize (efficiency baseline), Rand (random baseline).

Key findings (Figure 1):
- AvgLoss and AvgRankLoss behave similarly and consistently select candidates close to the best-performing region
- EffSize and Rand baselines typically remain near the median of the candidate pool
- Results hold across n = 500, 1000 and d ∈ {1, ..., 20}, with 50 repetitions each
- Efficiency-driven or random selection does not reliably identify candidates with strong conditional coverage performance

## 适用条件

20 CQR candidates with different conditional quantile estimators and tuning parameters. Bandwidths selected by matching effective sample sizes 30, 40, 50.

## 直觉解释

The experimental results validate the theoretical motivation: the lack-of-fit criterion from the conditional-miscoverage decomposition effectively guides selection toward conditionally valid procedures. This complements existing selection approaches (Braun et al. 2025, Zhou et al. 2026) that frame selection as supervised classification on hold-out data.

## 与其他知识的关系

← meth-model-selection-cc（验证 Section 4.1 的模型选择方法）
← thm-three-term-decomposition（选择标准由三误差分解驱动）

## 来源引用

Min et al. (2026), Section 5.1.2, Figure 1. arXiv:2605.11602v3.
