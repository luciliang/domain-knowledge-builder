---
id: exp-hinton2012-dropout
type: experiment
label: Dropout Regularization (Hinton et al. 2012, MNIST/TIMIT/ImageNet)
source: hinton2012
section: Section 4-6 (Experiments)
tokens: 1000
created: 2026-06-28
generated_by_step: S2
run_id: golden-hinton-advisor-0001
source_span:
  file: srivastava2014-dropout.pdf
  start_line: 1
  end_line: 1
  page: "1098-1105"
---

## 实验设置

Dropout：训练时以概率 $p$（通常 0.5）随机置零隐藏单元，测试时用缩放的权重（或所有子网络的平均）。直觉 = "每个前向传播都在训练一个不同的子网络，测试时用其平均"，等价于近似集成大量共享权重的瘦网络。

**数据集与基线**：
- MNIST（手写数字）：强基线已是 ~1.1% 错误率
- TIMIT（语音识别）：音素分类
- ImageNet (AlexNet)：2012 大规模分类
- CIFAR / Reuters 等多个标准基准

## 关键结果

| 任务 | 基线错误率 | 加 Dropout 后 | 降幅 |
|------|-----------|--------------|------|
| MNIST（标准前馈） | ~1.1% | ~0.8% | ~27% |
| TIMIT 音素 | 24.6% | ~21.7% | ~12% |
| ImageNet (AlexNet, 2012) | — | 无 dropout 无法训练到同样精度 | — |

**关键定性发现**：t-SNE 可视化显示，加 dropout 的隐藏单元激活**按类别更清晰地聚类**——即 dropout 不仅降低过拟合，还诱导出更有语义结构的分布式表示。

## 数值发现

- Dropout 几乎"免费"地提升了几乎所有深度网络的泛化性能
- 与 max-norm weight constraint 组合效果最佳
- 高 dropout（0.5-0.8）适用于隐藏层，低 dropout（0.2）适用于输入层

## 与其他知识的关系

→ def-hinton2014-distributed-representation（dropout 强迫每个单元都"独立有用"，强化分布式表示的鲁棒性）
→ thm-rumelhart1986-backprop-chain-rule（dropout 在反传训练流程上加的随机掩码，与反传正交但兼容）
→ meth-hinton2008-tsne（dropout 论文用 t-SNE 可视化证明表示质量提升）

## 来源引用

Hinton et al. (2012), "Improving neural networks by preventing co-adaptation of feature detectors", arXiv:1207.0580。
Srivastava, Hinton et al. (2014), "Dropout: A Simple Way to Prevent Neural Networks from Overfitting", *JMLR* 15, pp. 1929-1958, Sections 4-6。
