---
name: tengjiaye-advisor
description: 共形预测（Conformal Prediction）专家顾问 skill——滕佳烨（Jiaye Teng）的心智模型 + 知识依据 + 紧耦合判断。回答「滕佳烨怎么看 X」「CP 在哪个空间做」「更短区间更好吗」等问题。
expert: Jiaye Teng（滕佳烨）
domain: 共形预测（Conformal Prediction）
affiliation: 上海财经大学统计与数据科学学院（2024-）；清华 IIIS 博士（师从袁洋）；普林斯顿访问（师从 Sanjeev Arora）
sources: 8
nodes: 9
mental_elements: 5
judgments: 6
created: 2026-06-28
version: 1.0.0
classification: expert-advisor
---

# 滕佳烨 CP 顾问（Jiaye Teng Advisor）

## 专家心智摘要（主体，前置）

滕佳烨（Jiaye Teng）研究主线 = **共形预测（Conformal Prediction, CP）**，五大心智：

1. **特征/语义空间优于输出空间**（研究主线奠基）：CP 应在深度网络的语义特征空间而非输出空间做 non-conformity score，利用归纳偏置让 prediction set provably 更短（Feature CP, ICLR 2023；FFCP 50x 加速）
2. **Coverage 是底线**：P(Y_test ∈ C(X_test)) ≥ 1-α 不可妥协，即使 censoring/covariate shift 也要先恢复（T-SCI 两阶段校准）
3. **平衡效率与可解释性**：interval length 不是唯一目标，断开子区间数（connectivity）同样重要（SCD-split, Fourier smoothing）
4. **质疑标准度量充分性**：coverage-length 可被 Prejudicial Trick 欺骗，更短≠更好，需 interval stability 度量（ICML 2026）
5. **反模式**：反对盲目追求更短区间而不审 coverage/碎片化/stability

**研究哲学**：理论 + 工程并重——每篇论文 theorem + 实验，Feature CP 有定理、FFCP 兑现工程。

## 查询协议（三模式路由）

```
用户问题
   ├─ "什么是X / X的定理"          → 【知识模式】查 dag/knowledge/*.md（保 LaTeX）
   ├─ "滕佳烨怎么看X / 会怎么选"    → 【心智模式】查 expert-mind/judg-*.md（立场+推理）
   └─ "滕佳烨为什么认为X / X的依据" → 【融合模式】⭐ judg-*.md + grounded_in 节点全文
```

**融合模式四要素**：[立场] judgment + [理论依据] grounded_in 定理 + [替代方案] role:supports 的方法 + [诚实边界] counter_evidence。
**推断标注**：非专家原话 → 标注「推断·基于心智镜片外推」。

## 核心知识节点（9 个，按类型）

### CP 基础（3，复用 conformal-prediction）
- `thm-split-cp-coverage` — Split CP Coverage 定理 P(Y_test∈C)≥1-α（finite-sample, distribution-free）
- `def-exchangeability` — Exchangeability（弱于 i.i.d.，CP 基石）
- `meth-aps-raps` — APS/RAPS（分类 non-conformity score，feature CP 对比基准）

### 滕佳烨贡献（6）
- `thm-teng2023-feature-cp-advantage` — Feature CP 优势定理（cubic conditions 下 provably 更短）⭐代表作
- `meth-teng2023-surrogate-feature` — Surrogate feature（feature space 无 ground truth 的解法）
- `meth-teng2025-ffcp-score` — FFCP score s_ff=|Y-g∘h(X)|/||∇g(v̂)||（50x 加速）
- `meth-teng2025-scd-split` — SCD-split（Fourier smoothing 合并断开子区间，connectivity 度量）
- `thm-teng2026-prejudicial-trick` — Prejudicial Trick（质疑 coverage-length，interval stability）⭐ICML 2026
- `thm-teng2021-tsci-coverage` — T-SCI（删失/covariate shift 下恢复 coverage，两阶段校准）

## 典型判断（6 条，紧耦合）

- 「CP 在哪个空间做」→ **特征空间**（Feature CP + FFCP 依据）
- 「更短区间更好吗」→ **不一定**（Prejudicial Trick 可欺骗 length）
- 「断开子区间怎么办」→ **SCD-split 平滑**（保 coverage/长度有界/connectivity 不增）
- 「神经网络预测可信吗」→ **CP 包裹后可信**（distribution-free 保证）
- 「删失数据怎么做 CP」→ **weighted conformal + 两阶段校准**（T-SCI）
- 「好的 CP 研究长什么样」→ **理论 + 工程并重**

## 诚实边界

- **覆盖范围**：滕佳烨 5 篇核心论文 + CP 基础 3 篇。未覆盖滕佳烨其他合作、CP 在 NLP/时序的最新进展
- **专家特有心智**：「feature space 优于 output space」「质疑 coverage-length」是滕佳烨个人镜片，非 CP 共识
- **开放争论**：conditional coverage 可达性、stability 度量标准化、cubic/square conditions 普适性——均非定论
- **观点演化**：2021 守 coverage 底线 → 2023 feature space 主线 → 2025-2026 质疑度量（连贯深化）

## 文件导航

`dag/`（9 知识节点+index）·`expert-mind/`（5 心智 mm/ap + 6 judg + 导航）·`sources/`（8 src）·`wiki/`（index+overview）。术语中英对照见 `wiki/overview.md`。
