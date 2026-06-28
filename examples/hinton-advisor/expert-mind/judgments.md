# Hinton 专家判断（导航）

> 本文件是 Hinton judgment 的**导航与说明**。每个 judgment 的 frontmatter 数据定义在独立文件中（见下表），供 `lint_d7.py` 扫描校验。
> 完整导航见 `index.md`。

---

## judgment 清单（6 个）

每条 judgment = 立场 + 推理链 + `grounded_in` 依据节点，通过 `derived_from` 继承心智元素验证。

| ID | 文件 | 标签 | 触发问题 | derived_from |
|----|------|------|---------|--------------|
| `judg-hinton-distributed-vs-symbolic` | `judg-hinton-distributed-vs-symbolic.md` | 分布式 vs 符号 | 分布式表示和符号表示哪个更好 | `mm-hinton-distributed-representation` |
| `judg-hinton-depth-over-width` | `judg-hinton-depth-over-width.md` | 深度优于宽度 | 深度网络为什么比浅层宽网络好 | `mm-hinton-depth-beats-breadth` |
| `judg-hinton-prefers-generative` | `judg-hinton-prefers-generative.md` | 偏好生成式 | Hinton 为什么偏好生成式模型 | `mm-hinton-generative-energy-model` |
| `judg-hinton-dropout-intuition` | `judg-hinton-dropout-intuition.md` | Dropout 直觉 | Dropout 的直觉是什么 | `mm-hinton-distributed-representation` |
| `judg-hinton-capsule-over-pooling` | `judg-hinton-capsule-over-pooling.md` | Capsule 替代池化 | Capsule 为什么替代池化 | `mm-hinton-distributed-representation` |
| `judg-hinton-backprop-legacy` | `judg-hinton-backprop-legacy.md` | 反传历史地位 | Hinton 怎么评价反向传播 | `mm-hinton-distributed-representation` |

---

## 查询路由

- 问「Hinton 怎么看 X」→ 在上表找匹配 trigger 的 judgment 文件
- 问「Hinton 为什么认为 X / X 的依据」→ 融合查询：读 judgment 文件 + 其 `grounded_in` 节点全文
- 无现成 judgment → 加载心智元素镜片推断，标注「推断·非原话」

详见各独立 judgment 文件。
