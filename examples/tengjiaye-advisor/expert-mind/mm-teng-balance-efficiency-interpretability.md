---
id: mm-teng-balance-efficiency-interpretability
type: mental_model
label: 保证 coverage 底线，但要在效率与可解释性之间求平衡
statement: "interval length（效率）不是 CP 的唯一优化目标——prediction set 的可解释性（如断开子区间数量 connectivity）同样重要。好方法是在守住 coverage 的前提下，平衡长度与可解释性"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "SCD-split (2025)：引入 connectivity（断开子区间数）作为新度量，与 interval length 共同刻画 interpretability"
      - "Feature CP/FFCP：追求更短 band，但不引入碎片化（feature space 的 band 经映回 output 自然连贯）"
      - "Questioning-metric (2026)：质疑'更短=更好'，与 SCD-split 的'connectivity 也重要'一脉相承"
  generative:
    pass: true
    predicts: "评估一个 CP 方法时，滕佳烨不会只看平均长度，还会看预测集结构（是否碎片化、是否稳定）"
  exclusive:
    pass: true
    vs: "纯长度极小化派：只优化 interval length，无视预测集可解释性（CD-split 在多模态下生成大量碎片）"
grounded_in:
  - node: meth-teng2025-scd-split
    role: supports
    quote: "SCD-split 用 Fourier smoothing 合并断开子区间，Theorem 4.2 证明 connectivity 不增，4.3 证明严格减少"
  - node: thm-teng2026-prejudicial-trick
    role: supports
    quote: "Prejudicial Trick 揭示 length 可被欺骗——支撑'length 不是唯一目标'的判断"
  - node: thm-split-cp-coverage
    role: supports
    quote: "平衡的前提是守住 coverage 底线（SCD-split Theorem 4.1 保持 marginal coverage）"
confidence: high
provenance:
  sources:
    - src-teng2025-smoothing-cp
    - src-teng2026-questioning-metric
---

## 核心思想

滕佳烨的思路演化：早期（T-SCI/Feature CP）追求"更短更精确"，后期（SCD-split/PT）意识到**效率不是全部**——预测集是否可解释、是否稳定，同样影响实际可用性。

### SCD-split 的三维度框架

| 维度 | 含义 | SCD-split 保证 |
|------|------|----------------|
| validity | coverage | Theorem 4.1：smoothing 保持 ≥ 1-α |
| efficiency | interval length | Theorem 4.4：有上界 |
| **connectivity** | 断开子区间数 | Theorem 4.2/4.3：不增/严格减少 |

### 动机场景

- **医疗**：疾病预后"快速恶化"或"长期康复"，医生要 2 个清晰区间而非 1 个宽区间或 10 个碎片
- **金融**：股价"大涨"或"大跌"，投资者要 2 个区间区分上下行

## 支撑节点

- `meth-teng2025-scd-split`：connectivity 度量 + smoothing 方法
- `thm-teng2026-prejudicial-trick`：质疑 length 唯一论
- `thm-split-cp-coverage`：balance 的前提是守底线

## 诚实边界

- connectivity 度量主要面向回归任务（分类预测集结构不同）
- smoothing 引入超参，需 validation 调参
- "平衡"无唯一解，依赖应用场景对长度 vs 可解释性的权重
