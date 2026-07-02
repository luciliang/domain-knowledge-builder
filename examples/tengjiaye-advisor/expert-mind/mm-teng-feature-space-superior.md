---
id: mm-teng-feature-space-superior
type: mental_model
label: 特征/语义空间优于输出空间
statement: "做 conformal prediction 时，应在语义特征空间而非原始输出空间计算 non-conformity score——深度表示的归纳偏置能让 prediction set provably 更短，同时 coverage 有效"
status: verified
verification:
  cross_scene:
    pass: true
    evidence:
      - "Feature CP (ICLR 2023)：cubic conditions 下 provably 比 vanilla CP 更短，ImageNet/Cityscapes SOTA"
      - "Fast Feature CP (2025)：用 Taylor 展开加速 feature CP，50x 加速且精度持平，证明 feature 思路的工程可行性"
      - "FFCP 扩展到 RAPS/CQR/LCP（FFRAPS/FFCQR/FFLCP），证明 feature-level 技术的通用性"
  generative:
    pass: true
    predicts: "对任何新的 CP 任务，滕佳烨会先问'能否在特征空间做'——尤其当模型是深度网络、输出空间无语义结构时"
  exclusive:
    pass: true
    vs: "经典 CP 派（Vovk/Angelopoulos）默认在 output space 做 CP，把模型当黑盒；滕佳烨打破'黑盒'假设，利用模型内部表示"
grounded_in:
  - node: thm-teng2023-feature-cp-advantage
    role: supports
    quote: "在 cubic conditions（length preserving/expansion/quantile stability）下，Feature CP provably 返回比 vanilla CP 更短的 confidence band，且 coverage 有效"
  - node: meth-teng2023-surrogate-feature
    role: supports
    quote: "surrogate feature 解决 feature space 无 ground truth 问题，是 feature CP 的技术核心"
  - node: meth-teng2025-ffcp-score
    role: supports
    quote: "FFCP 用 Taylor 展开近似，s_ff=|Y-g∘h(X)|/||∇g(v̂)||，50x 加速——feature 思路的工程兑现"
confidence: high
provenance:
  sources:
    - src-teng2023-feature-cp
    - src-teng2025-fast-feature-cp
---

## 核心思想

滕佳烨研究主线的奠基：CP 不应止于 output space。深度网络的中间层特征携带语义归纳偏置，在特征空间做 CP 能得到更紧、更有意义的 prediction set。

### 关键区分

- **output-space CP**（经典）：把模型当黑盒，所有像素/样本返回相同不确定性，无视语义区域
- **feature-space CP**（滕佳烨）：拆分模型 μ̂=ĝ∘f̂，在 f̂ 的特征空间做 CP，经 ĝ 映回 output 后不确定性自然分化

### 跨场景复现（3 个独立证据）

1. **Feature CP (ICLR 2023)**：立方条件下定理保证更短 + SOTA 实验
2. **Fast Feature CP (2025)**：工程加速，证明 feature 思路可落地
3. **FFRAPS/FFCQR/FFLCP**：扩展到多种 CP 变体，证明通用性

## 支撑节点

- `thm-teng2023-feature-cp-advantage`：理论保证（更短）
- `meth-teng2023-surrogate-feature`：技术实现（surrogate feature）
- `meth-teng2025-ffcp-score`：工程兑现（50x 加速）

## 诚实边界

- cubic/square conditions 是温和假设，实证满足，但非对所有 feature space 成立
- FFCP 的 Taylor 展开是一阶近似，严重非线性时有误差
- feature space 方法需访问模型内部（非完全 black-box agnostic）
