---
id: mm-teng-question-standard-metric
type: mental_model
label: 质疑标准度量的充分性
statement: "coverage-length 这对标准评估度量不足以评判 CP 方法优劣——更短的区间不一定更好。必须审视度量本身是否充分，引入新维度（如 interval stability）防止被欺骗"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "Questioning-metric (ICML 2026)：Prejudicial Trick 证明 coverage valid 但 length 可欺骗性降低"
      - "SCD-split (2025)：引入 connectivity 度量，质疑 interval length 唯一论（2025 先兆）"
      - "Example 1（医生 Alice vs Bob）：用直觉案例说明'更短'可能伴随实用性脆弱"
  generative:
    pass: true
    predicts: "对任何声称'新方法 length 更短所以更优'的论文，滕佳烨会先问'是否引入了 stability/connectivity 问题'"
  exclusive:
    pass: true
    vs: "metric-acceptance 派：默认 coverage+length 足够评判 CP，不质疑度量本身（滕佳烨的核心批判对象）"
grounded_in:
  - node: thm-teng2026-prejudicial-trick
    role: supports
    quote: "PT 在 coverage valid 下欺骗性降低 length，证明 coverage-length 度量不充分"
  - node: meth-teng2025-scd-split
    role: supports
    quote: "SCD-split 引入 connectivity，证明 length 不是唯一目标（质疑度量的早期体现）"
  - node: thm-split-cp-coverage
    role: context
    quote: "coverage 仍是底线（PT 也保持 coverage），质疑的是 length 度量，非 coverage 度量"
confidence: high
provenance:
  sources:
    - src-teng2026-questioning-metric
    - src-teng2025-smoothing-cp
---

## 核心思想

滕佳烨最具批判性的心智：**不盲从社区共识的评估指标**。当大家都用 coverage+length 评判 CP 方法时，他追问这对指标是否充分——并用 Prejudicial Trick 构造反例证明其可被欺骗。

### Prejudicial Trick 的警示

- PT 以概率 p 返回紧区间、1-p 返回 null/单点，coverage 期望 valid，但 length 欺骗性降低
- 同一输入多次运行得到完全不同区间 → interval stability 极低
- **结论**：仅看 coverage+length 会误判 PT 为"更优方法"

### 新度量：interval stability

$$
\text{stability} = \text{同一输入多次运行区间的一致性}
$$

用于检测新 CP 方法是否隐式用了 PT-like 技巧。

### 与 SCD-split 的呼应

SCD-split（2025）引入 connectivity，PT（2026）引入 stability——都在扩展评估维度。滕佳烨的心智是连贯的：**好的 CP 方法不仅要 coverage valid、length 短，还要 connectivity 少、stability 高**。

## 支撑节点

- `thm-teng2026-prejudicial-trick`：核心依据（PT 反例）
- `meth-teng2025-scd-split`：connectivity 度量（早期体现）
- `thm-split-cp-coverage`：coverage 仍是底线（质疑 length 非 coverage）

## 诚实边界

- PT 是"反面教材"构造，非推荐方法
- 并非所有更短区间方法都用 PT（Feature CP/FFCP 是真改进，stability 高）
- interval stability 度量本身仍有研究空间（如何量化、阈值）
