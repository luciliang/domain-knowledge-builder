---
id: ap-teng-blind-shorter-better
type: anti_pattern
label: 反对盲目追求更短区间而不审度量的充分性
statement: "如果一个 CP 方法仅凭平均 interval length 更短就声称更优，而不审视 coverage 是否被偷换、预测集是否碎片化、区间是否稳定，滕佳烨会持根本怀疑"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "Questioning-metric (ICML 2026)：Prejudicial Trick 是对此反模式的精确刻画——PT 降 length 但引入 stability 问题"
      - "SCD-split (2025)：CD-split 为最短 length 生成大量碎片子区间，损害可解释性——length 优不等于方法优"
      - "Example 1：Bob 的区间更短但同一病人多次查询结果不同，实用性脆弱"
  generative:
    pass: true
    predicts: "对任何'length 创新低'的 CP 论文，滕佳烨会问：是否用 PT-like 技巧？预测集是否碎片化？区间稳定吗？"
  exclusive:
    pass: true
    vs: "length-minimization 派：把 interval length 作为唯一优化目标（滕佳烨明确反对）"
grounded_in:
  - node: thm-teng2026-prejudicial-trick
    role: refutes
    quote: "PT 揭示：coverage valid 但 length 可欺骗性降低，盲目信 length 会被骗"
  - node: meth-teng2025-scd-split
    role: refutes
    quote: "CD-split 为短 length 生成碎片子区间——length 优但可解释性差"
  - node: thm-teng2023-feature-cp-advantage
    role: context
    quote: "Feature CP 也降 length，但 stability 高（非 PT 技巧）——真改进 vs 假改进的区分"
confidence: high
provenance:
  sources:
    - src-teng2026-questioning-metric
    - src-teng2025-smoothing-cp
    - src-teng2023-feature-cp
---

## 反模式核心

滕佳烨明确反对的思维方式：**把 interval length 作为 CP 方法的唯一评判标准**。

### 为何反对

1. **length 可被欺骗**（Prejudicial Trick）：PT 保持 coverage valid 但欺骗性降 length，引入 stability 问题
2. **length 短可能伴随碎片化**（CD-split）：多模态下生成大量断开子区间，不可解释
3. **length 短可能牺牲实用性**（Bob 策略）：同一输入多次结果不同，无法决策

### 正确做法（滕佳烨的主张）

评估 CP 方法应多维度审视：
- **coverage**：底线（不可妥协）
- **length**：效率（重要但非唯一）
- **connectivity**：可解释性（SCD-split 提出）
- **stability**：可靠性（PT 提出）

## 真改进 vs 假改进的区分

| 方法 | length 更短？ | coverage valid？ | stability？ | 判定 |
|------|--------------|------------------|-------------|------|
| Feature CP / FFCP | 是 | 是 | 高 | **真改进**（feature 归纳偏置） |
| SCD-split | 略增 | 是 | 高 | **真改进**（换 connectivity） |
| Prejudicial Trick | 是 | 是 | **极低** | **假改进**（欺骗 length） |

## 诚实边界

- 此反模式针对"仅凭 length 判优劣"，不否定 length 作为度量之一的价值
- 滕佳烨自己的 Feature CP/FFCP 也优化 length，但附 stability/connectivity 审视
- interval stability 度量仍在发展中，判定"假改进"需谨慎
