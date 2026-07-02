---
id: judg-teng-scd-split-disconnected
type: judgment
label: CD-split 的断开子区间怎么办——SCD-split 平滑合并
status: verified
trigger: "CD-split 生成的预测集有很多断开子区间怎么处理 / 如何让预测集更可解释"
derived_from: mm-teng-balance-efficiency-interpretability
judgment: "用 SCD-split——对条件密度做 Fourier smoothing 合并断开子区间。用户指定期望子区间数，smoothing 减少密度峰，validation 调参使子区间数逼近目标。保证 coverage 不破、长度有界、connectivity 不增"
reasoning: "CD-split 为最短 length 用条件密度作 score，多模态下生成大量断开子区间，医生/投资者无法决策。滕佳烨引入 connectivity（断开子区间数）作为新度量，与 length 共同刻画 interpretability。SCD-split 在条件密度上做 Fourier smoothing 去除不必要的峰，Theorem 4.1 保持 coverage，4.2 证明子区间不增，4.3 在窄谷双峰下严格减少，4.4 给长度上界"
grounded_in:
  - node: meth-teng2025-scd-split
    role: supports
    quote: "SCD-split 用 Fourier smoothing 合并断开子区间，引入 connectivity 度量"
  - node: thm-split-cp-coverage
    role: supports
    quote: "Theorem 4.1：smoothing 保持 marginal coverage ≥ 1-α（不破底线）"
  - node: thm-teng2026-prejudicial-trick
    role: context
    quote: "SCD-split 与 PT 一脉相承：都在质疑 interval length 唯一论，扩展评估维度"
counter_evidence:
  - node: meth-teng2025-scd-split
    role: context
    note: "smoothing 引入超参（平滑强度），需 validation 调参；connectivity 度量主要面向回归任务"
confidence: high
provenance:
  sources:
    - src-teng2025-smoothing-cp
---

## 判断背景

「CD-split 的断开子区间怎么办」是滕佳烨 SCD-split 论文（2025）要解决的核心实用性问题。

## 判断立场

**SCD-split 平滑合并**。不放弃 CD-split 的效率优势，但用 smoothing 控制 connectivity。

## 推理链

1. **问题**：CD-split 多模态下生成大量断开子区间，不可解释
2. **新度量**：connectivity（断开子区间数），与 length 共同刻画 interpretability
3. **方法**：Fourier smoothing 去密度峰，用户指定期望子区间数，validation 调参
4. **保证**：coverage 不破（4.1）、connectivity 不增（4.2）、严格减少（4.3）、长度有界（4.4）

## 诚实边界

- smoothing 引入超参，需 validation
- connectivity 主要面向回归任务
- "平衡"无唯一解，依赖应用对 length vs connectivity 的权重
