# Prejudicial Trick（质疑 coverage-length 度量）

> 节点 ID: `thm-teng2026-prejudicial-trick` | type: theorem | 来源: `src-teng2026-questioning-metric`（ICML 2026）

## 核心命题

**coverage-length 这对标准度量可被欺骗**——存在一种构造（Prejudicial Trick），能在保持 coverage valid 的同时欺骗性地降低 average interval length，但引入严重的实用性脆弱。**更短的区间不一定更好。**

## Prejudicial Trick（PT，Algorithm 1）

输入：base CP 算法 $\mathcal{A}_{1-\alpha}(\cdot;\hat{\mu})$，测试点 $x'$，概率 $p$。

```
1. 生成 U ~ Unif([0,1])
2. if U > p:
       返回 null 区间（回归: C(x')=[μ̂(x'),μ̂(x')]；分类: C(x')=∅）
   else:
       计算 adjusted miscoverage α' = 1 - (1-α)/p
       返回 A_{1-α'}(x'; μ̂)  // 用更紧的置信水平
```

## Example 1（医生 Alice vs Bob，直觉说明）

历史数据：60% 病人 4 年内康复，80% 5 年内康复。

- **Alice**：给所有病人区间 $[0, 4]$，平均长度 4
- **Bob**：以 0.75 概率给 $[0,5]$，0.25 概率给 $[0,0]$，平均长度 $5 \times 0.75 = 3.75 < 4$

两者 coverage 期望相同（都 valid），但 **Bob 的平均区间更短**。然而 Bob 有致命缺陷：
- **微观**：同一病人多次查询得到完全不同区间（不稳定）
- **宏观**：部分病人被告知"0 年康复"（null），误导性强

## Theorem 1.1 理论总结

### coverage 方面
- PT **保持** marginal coverage 保证（继承 base CP 的 `thm-split-cp-coverage`）
- PT 甚至在 base 不满足 conditional coverage 时也能改善 conditional coverage

### length 方面
- 在一般条件下（可微 length 函数 Theorem 3.7 / 不可微 Theorem 3.10 / model misspecification Remark 3.11），PT 返回**更短**平均区间
- 局部凹 length 函数（Corollary 3.8）、base 是 VCP（Corollary 3.9）等特例下成立

## 新度量：interval stability

为检测新 CP 方法是否隐式用了 PT-like 技巧，滕佳烨引入 **interval stability（区间稳定性）**：

$$
\text{stability} = \text{同一输入多次运行区间的一致性}
$$

PT 的 stability 极低（同一输入 0.25 概率 null，0.75 概率非 null）。

## 在滕佳烨工作中的地位（批判性思维代表）

这是滕佳烨「**质疑标准度量**」心智的核心依据，也是反模式「盲目追求更短区间」的理论支撑：
- 揭示 "coverage + length" 不足以评判 CP 方法优劣
- 推动社区关注度量充分性（sufficiency of metrics）
- 与 SCD-split（`meth-teng2025-scd-split`）形成互补：SCD-split 加 connectivity 度量，PT 加 stability 度量——都在扩展评估维度

## 诚实边界

- PT 是一个"反面教材"构造，非推荐方法——目的是暴露度量缺陷
- 并非所有"更短区间"方法都用 PT（Feature CP/FFCP 是真改进，因其 stability 高）
- interval stability 度量本身仍有研究空间（如何量化、如何设阈值）
