# Expert-Mind 索引 — 滕佳烨（Jiaye Teng）

> 专家心智导航中枢。心智/judgment 实体均存储为独立 `*.md` 文件（顶部裸 frontmatter，供 lint 解析）。

## 结构

```
expert-mind/
├── index.md                          # 本文件（导航中枢）
├── mental-models.md                  # 心智元素导航（引用独立文件）
├── judgments.md                      # 判断导航（引用独立文件）
├── mm-teng-*.md                      # 4 个心智模型（独立实体）
├── ap-teng-*.md                      # 1 个反模式（独立实体）
└── judg-teng-*.md                    # 6 个判断（独立实体）
```

## 快速入口

### 心智模型（4）
- [`mm-teng-feature-space-superior`](mm-teng-feature-space-superior.md) — 特征空间优于输出空间（研究主线）
- [`mm-teng-coverage-as-floor`](mm-teng-coverage-as-floor.md) — Coverage 是底线
- [`mm-teng-balance-efficiency-interpretability`](mm-teng-balance-efficiency-interpretability.md) — 平衡效率与可解释性
- [`mm-teng-question-standard-metric`](mm-teng-question-standard-metric.md) — 质疑标准度量

### 反模式（1）
- [`ap-teng-blind-shorter-better`](ap-teng-blind-shorter-better.md) — 反对盲目追求更短区间

### 判断（6）
- [`judg-teng-which-space-cp`](judg-teng-which-space-cp.md) — CP 在哪个空间做
- [`judg-teng-scd-split-disconnected`](judg-teng-scd-split-disconnected.md) — 断开子区间怎么办
- [`judg-teng-shorter-not-better`](judg-teng-shorter-not-better.md) — 更短一定更好吗
- [`judg-teng-nn-prediction-trust`](judg-teng-nn-prediction-trust.md) — 神经网络预测可信吗
- [`judg-teng-theory-plus-engineering`](judg-teng-theory-plus-engineering.md) — 好的 CP 研究长什么样
- [`judg-teng-censoring-coverage-recovery`](judg-teng-censoring-coverage-recovery.md) — 删失数据怎么做 CP

## 数据流

```
dag/dag-index.json（9 知识节点，含 LaTeX）
        ↑ grounded_in.node 引用（硬门③ 无孤儿）
        |
expert-mind/judg-*.md（6 判断，紧耦合枢纽）
        ↑ derived_from 继承验证
        |
expert-mind/mm-*.md / ap-*.md（5 心智元素，三重验证）
        ↑ provenance.sources 引用
        |
sources/src-*.md（8 来源，硬门② 溯源）
```
