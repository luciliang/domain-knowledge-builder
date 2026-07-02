---
id: judg-teng-shorter-not-better
type: judgment
label: 更短的预测区间一定更好吗——不一定
status: verified
trigger: "平均区间更短的 CP 方法一定更好吗 / 为什么不能只看 interval length"
derived_from: mm-teng-question-standard-metric
judgment: "不一定。Prejudicial Trick 证明：coverage 可保持 valid，但 length 能被欺骗性降低（用 null/单点区间以一定概率替换），同一输入多次运行得到完全不同区间。更短可能伴随 stability 灾难——必须引入 interval stability 度量检测"
reasoning: "Bob 以 0.75 概率给 [0,5]、0.25 给 [0,0]，平均长度 3.75 < Alice 的 4，coverage 期望相同，但同一病人多次查询结果完全不同。PT 把这个直觉形式化：以概率 p 返回紧区间、1-p 返回 null，coverage 由 α'=1-(1-α)/p 调整保持 valid，length 在一般条件下（可微/不可微/model misspecification）欺骗性降低。滕佳烨引入 interval stability 度量，检测新方法是否隐式用了 PT-like 技巧"
grounded_in:
  - node: thm-teng2026-prejudicial-trick
    role: supports
    quote: "PT 在 coverage valid 下欺骗性降 length，证明 coverage-length 度量不充分"
  - node: meth-teng2025-scd-split
    role: supports
    quote: "SCD-split 引入 connectivity，证明 length 不是唯一目标——更短可能伴随碎片化"
  - node: thm-split-cp-coverage
    role: context
    quote: "PT 也保持 coverage valid——质疑的是 length 度量，非 coverage 度量（coverage 仍是底线）"
counter_evidence:
  - node: thm-teng2023-feature-cp-advantage
    role: context
    note: "Feature CP/FFCP 也降 length，但 stability 高（非 PT 技巧）——并非所有更短都是假改进，需 stability 审视区分"
confidence: high
provenance:
  sources:
    - src-teng2026-questioning-metric
    - src-teng2025-smoothing-cp
---

## 判断背景

「更短的区间一定更好吗」是滕佳烨 ICML 2026 论文的核心批判问题，针对 CP 社区对 coverage-length 度量的盲信。

## 判断立场

**不一定**。更短可能是欺骗（PT）或牺牲可解释性（碎片化）换来的。

## 推理链

1. **Example 1（Alice vs Bob）**：Bob 更短但同输入多次结果不同，实用性脆弱
2. **PT 形式化**：概率 p 返回紧区间、1-p 返回 null，coverage valid 但 length 欺骗性降
3. **Theorem 1.1**：一般条件下 PT provably 降 length（可微/不可微/misspecification）
4. **新度量**：interval stability 检测 PT-like 技巧

## 诚实边界

- 并非所有更短都是假改进（Feature CP 是真改进，stability 高）
- PT 是反面教材，非推荐方法
- interval stability 度量仍在发展（如何量化、阈值）
