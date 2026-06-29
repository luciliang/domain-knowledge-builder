---
id: judg-teng-censoring-coverage-recovery
type: judgment
label: 删失/covariate shift 下如何恢复 coverage——weighted conformal + 两阶段校准
status: verified
trigger: "生存分析的删失数据怎么做 CP / covariate shift 下 coverage 失效怎么办"
derived_from: mm-teng-coverage-as-floor
judgment: "在 strong ignorability（T⊥Δ|X）下，用 weighted conformal inference（基于偏似然的 non-conformity score）处理 covariate shift 恢复 coverage，再用 quantile conformal inference 两阶段校准得到 nearly perfect coverage（既有 lower 也有 upper bound）"
reasoning: "censoring 导致 (X|Δ=1)≠(X|Δ=0) 的 covariate shift，破坏 exchangeability，Cox-MLP 失去 guaranteed coverage。滕佳烨的 T-SCI：阶段1 WCCI 用 weighted conformal（Tibshirani-Foygel 2019）+ 基于 partial likelihood 的 score 处理 shift；阶段2 quantile conformal（Romano 2019）校准，返回 nearly perfect coverage。关键是不放弃 coverage 底线，即使在最易失效的场景也要恢复保证"
grounded_in:
  - node: thm-teng2021-tsci-coverage
    role: supports
    quote: "T-SCI 在 milder 假设下恢复 nearly perfect guaranteed coverage（WCCI + 两阶段校准）"
  - node: def-angelopoulosbates2022-exchangeability
    role: supports
    quote: "censoring 破坏 exchangeability（covariate shift），weighted conformal 是修复机制"
  - node: thm-split-cp-coverage
    role: supports
    quote: "T-SCI 恢复的就是 split CP 的 coverage 保证——在困难场景守住底线"
counter_evidence:
  - node: thm-teng2021-tsci-coverage
    role: context
    note: "依赖 strong ignorability 假设（T⊥Δ|X）；若假设不成立则失效。Candès et al. (2021) 走另一条路（放松 strong ignorability 但要求删失时间信息完全）"
confidence: high
provenance:
  sources:
    - src-teng2021-tsci
---

## 判断背景

「删失/covariate shift 下如何恢复 coverage」是滕佳烨第一作者早期工作 T-SCI 的核心问题，确立了他"coverage 是底线"的心智。

## 判断立场

**weighted conformal + 两阶段校准**。不放弃 coverage，用 weighted CP 修复 shift，再用 quantile CP 收紧。

## 推理链

1. **问题**：censoring → covariate shift → exchangeability 破坏 → coverage 失效
2. **阶段1 WCCI**：weighted conformal（Tibshirani-Foygel）+ partial likelihood score 处理 shift
3. **阶段2 quantile CP**：校准 WCCI，得 nearly perfect coverage（lower + upper bound）
4. **底线意识**：即使最困难场景也要恢复 guaranteed coverage

## 诚实边界

- 依赖 strong ignorability（T⊥Δ|X），假设不成立则失效
- 基于 Cox/偏似然框架，非任意删失机制
- 与 Candès et al. (2021) 是不同假设下的平行工作
