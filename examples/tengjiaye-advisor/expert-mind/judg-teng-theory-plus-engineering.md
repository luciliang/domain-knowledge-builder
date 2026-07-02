---
id: judg-teng-theory-plus-engineering
type: judgment
label: 好的 CP 研究是理论 + 工程并重——有定理还要能跑
status: verified
trigger: "如何评价一个好的 CP 研究 / Feature CP 之后为什么要做 FFCP"
derived_from: mm-teng-feature-space-superior
judgment: "好的 CP 研究必须理论 + 工程并重。Feature CP 有定理（cubic conditions 下更短）但 Band Estimation 依赖 LiPRA 耗时长，FFCP 用 Taylor 展开近似实现 50x 加速——理论保证 + 工程可用缺一不可。滕佳烨每篇论文都是 theorem + 实验，反对只有理论或只有 empirical 的工作"
reasoning: "Feature CP (ICLR 2023) 确立 feature space 更优的理论，但 Band Estimation 的 LiPRA 非线性操作使实际应用受限。FFCP (2025) 用 Taylor 展开近似得到 s_ff=|Y-g∘h(X)|/||∇g(v̂)||，在 square conditions 下同样保证更短（Theorem 5），且 ~50x 加速。这体现滕佳烨的研究哲学：定理证明优势 + 工程实现可用性，两者缺一不可。SCD-split 同样如此——Theorem 4.1-4.4 四重保证 + Fourier smoothing 可实现"
grounded_in:
  - node: thm-teng2023-feature-cp-advantage
    role: supports
    quote: "Feature CP 的理论保证（cubic conditions 下更短）——理论侧"
  - node: meth-teng2025-ffcp-score
    role: supports
    quote: "FFCP 的 Taylor 展开近似 + 50x 加速——工程侧，兑现理论承诺"
  - node: meth-teng2023-surrogate-feature
    role: supports
    quote: "surrogate feature 是理论到实现的桥梁——既有数学构造又有算法"
  - node: meth-teng2025-scd-split
    role: context
    quote: "SCD-split 四重定理 + Fourier smoothing 可实现——同样的理论+工程并重范式"
confidence: high
provenance:
  sources:
    - src-teng2023-feature-cp
    - src-teng2025-fast-feature-cp
    - src-teng2025-smoothing-cp
---

## 判断背景

「如何评价好的 CP 研究」反映滕佳烨的方法论——理论 + 工程并重，反对偏废。

## 判断立场

**理论 + 工程并重**。有定理证明优势，还要有可跑的实现。

## 推理链

1. **Feature CP 的理论**：cubic conditions 下 provably 更短（Theorem 6）
2. **实用性瓶颈**：Band Estimation 依赖 LiPRA，耗时长
3. **FFCP 的工程兑现**：Taylor 展开近似，s_ff 简单可算，50x 加速
4. **理论不破**：FFCP 在 square conditions 下同样保证更短（Theorem 5）
5. **范式一致性**：SCD-split 也是四重定理 + Fourier smoothing 实现

## 诚实边界

- FFCP 的 Taylor 展开是一阶近似，严重非线性时有误差
- 工程优化可能引入超参（如 FFCP 的梯度计算、SCD-split 的 smoothing 强度）
- "并重"是理想，实际论文可能有侧重（Feature CP 偏理论，FFCP 偏工程）
