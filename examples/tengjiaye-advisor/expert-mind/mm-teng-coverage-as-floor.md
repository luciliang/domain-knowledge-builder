---
id: mm-teng-coverage-as-floor
label: Coverage 是底线，必须先守住再谈其他
statement: "任何 CP 方法的第一要务是保证 P(Y_test ∈ C(X_test)) ≥ 1-α——coverage 是不可妥协的底线。即使在 censoring/covariate shift 等困难场景，也要先恢复 guaranteed coverage，再谈效率"
type: mental_model
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "T-SCI (2021)：删失/covariate shift 下恢复 Cox-MLP 的 guaranteed coverage（WCCI + 两阶段校准）"
      - "SCD-split (2025)：Theorem 4.1 证明 smoothing 保持 marginal coverage（不破坏底线）"
      - "Feature CP (2023)：Theorem 6 在证明更短的同时，coverage 仍由 exchangeability 保证"
  generative:
    pass: true
    predicts: "对任何声称改进 CP 的方法，滕佳烨会先验证 coverage 是否仍 valid，再看效率提升"
  exclusive:
    pass: true
    vs: "激进效率派：为最短区间放松 coverage 保证（滕佳烨明确反对——见 Prejudicial Trick）"
grounded_in:
  - node: thm-split-cp-coverage
    role: supports
    quote: "P(Y_test ∈ C(X_test)) ≥ 1-α 是 finite-sample distribution-free 的底线保证"
  - node: thm-teng2021-tsci-coverage
    role: supports
    quote: "T-SCI 在 milder 假设下恢复 nearly perfect guaranteed coverage——即使删失场景也守住底线"
  - node: meth-teng2025-scd-split
    role: supports
    quote: "SCD-split 的 smoothing 保持 marginal coverage ≥ 1-α（Theorem 4.1），改效率不破底线"
confidence: high
provenance:
  sources:
    - src-teng2021-tsci
    - src-teng2025-smoothing-cp
    - src-angelopoulos-bates-2022
---

## 核心思想

滕佳烨的所有工作都建立在 split CP coverage 保证之上。他从不为效率牺牲 coverage——即使引入 smoothing/feature space 等改进，首要定理都是证明 coverage 仍 valid。

### 时间线证据

1. **T-SCI (2021)**：在 censoring 这种 coverage 最易失效的场景，用 weighted conformal 恢复保证 → 确立底线意识
2. **Feature CP (2023)**：证明更短，但 coverage 定理先行
3. **SCD-split (2025)**：Theorem 4.1（validity）排在 Theorem 4.2/4.3（connectivity）之前
4. **Prejudicial Trick (2026)**：揭示 PT 保持 coverage valid 但欺骗 length——批评的是 length 度量，**而非 coverage 度量**（coverage 仍是神圣底线）

## 支撑节点

- `thm-split-cp-coverage`：底线定义
- `thm-teng2021-tsci-coverage`：困难场景守底线
- `meth-teng2025-scd-split`：改进不破底线

## 诚实边界

- coverage 是 **marginal**（非 conditional）——滕佳烨知道对子群可能欠覆盖，但不放弃 marginal 保证
- "守 coverage 底线"不等于"只看 coverage"——见 `mm-teng-balance-efficiency-interpretability` 和 `mm-teng-question-standard-metric`
