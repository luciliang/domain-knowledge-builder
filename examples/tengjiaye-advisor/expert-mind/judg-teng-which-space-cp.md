---
id: judg-teng-which-space-cp
type: judgment
label: CP 该在哪个空间做——特征空间而非输出空间
status: verified
trigger: "conformal prediction 应该在输出空间还是特征空间做 / Feature CP 为什么更好"
derived_from: mm-teng-feature-space-superior
judgment: "应在语义特征空间做 CP。深度表示的归纳偏置能让 prediction set provably 更短，同时 coverage 有效——这是滕佳烨研究主线的核心主张"
reasoning: "经典 CP 把模型当黑盒，在 output space 计算 non-conformity score，导致所有像素/样本返回相同不确定性。但深度网络的中间层特征携带语义信息，在 feature space 做 CP 后经非线性变换映回 output，不确定性自然分化。Feature CP 在 cubic conditions 下 provably 更短，FFCP 用 Taylor 展开近似实现 50x 加速且精度持平。关键是用 surrogate feature 解决 feature space 无 ground truth 的难题"
grounded_in:
  - node: thm-teng2023-feature-cp-advantage
    role: supports
    quote: "cubic conditions 下 Feature CP provably 比 vanilla CP 更短，coverage 有效"
  - node: meth-teng2023-surrogate-feature
    role: supports
    quote: "surrogate feature 解决 feature space 无 ground truth——技术核心"
  - node: meth-teng2025-ffcp-score
    role: supports
    quote: "FFCP 的 s_ff=|Y-g∘h(X)|/||∇g(v̂)|| 实现 50x 加速，证明 feature 思路工程可行"
  - node: thm-split-cp-coverage
    role: supports
    quote: "feature CP 的 coverage 仍由 exchangeability 保证——换空间不破底线"
counter_evidence:
  - node: meth-aps-raps
    role: context
    note: "经典 APS/RAPS 在 output space 工作，对完全 black-box 模型仍有价值（不需访问内部特征）；feature CP 需访问模型内部，非完全 model-agnostic"
confidence: high
provenance:
  sources:
    - src-teng2023-feature-cp
    - src-teng2025-fast-feature-cp
---

## 判断背景

「CP 在哪个空间做」是滕佳烨代表作 Feature CP（ICLR 2023）的核心问题，也是他研究主线的奠基。

## 判断立场

**特征空间**。利用深度表示的归纳偏置，prediction set provably 更短且 coverage 有效。

## 推理链

1. **output-space CP 的局限**：黑盒处理，所有样本相同不确定性，无视语义
2. **feature-space 的优势**：语义特征空间可区分区域，映回 output 后不确定性分化
3. **技术可行性**：surrogate feature 解决无 ground truth；FFCP 50x 加速
4. **理论保证**：cubic conditions 下 provably 更短，coverage 由 exchangeability 保证

## 诚实边界

- feature CP 需访问模型内部（非完全 black-box agnostic）
- cubic conditions 是温和假设，实证满足但非普适
- 对纯黑盒部署场景，output-space APS/RAPS 仍有价值
