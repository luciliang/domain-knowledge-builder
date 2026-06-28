---
id: judg-teng-nn-prediction-trust
type: judgment
label: 神经网络的预测可信吗——CP 提供分布无关保证
status: verified
trigger: "神经网络的预测可信吗 / 如何给深度学习模型加不确定性保证 / CP 为什么适合校准神经网络"
derived_from: mm-teng-coverage-as-floor
judgment: "单独的神经网络预测不可信（over-confidence），但用 CP 包裹后，可在分布无关、finite-sample 下保证 P(Y_test ∈ C(X_test)) ≥ 1-α。CP 是 post-hoc 校准层，不重训模型，适合任何黑盒预测器"
reasoning: "神经网络普遍 over-confidence，直接部署到医疗/金融高风险场景不可靠。CP 的优势：(1) distribution-free——不假设数据分布；(2) finite-sample——任意样本量成立；(3) post-hoc——不重训，包裹任意模型；(4) exchangeability 弱于 i.i.d.。滕佳烨所有工作（T-SCI/Feature CP/FFCP/SCD-split/PT）都以这条 coverage 保证为底线，即使在 censoring/covariate shift 等困难场景也要先恢复保证"
grounded_in:
  - node: thm-split-cp-coverage
    role: supports
    quote: "P(Y_test ∈ C(X_test)) ≥ 1-α，finite-sample distribution-free——CP 校准神经网络的理论基础"
  - node: def-exchangeability
    role: supports
    quote: "exchangeability 弱于 i.i.d.，是 CP 保证的基石，适用范围广"
  - node: thm-teng2021-tsci-coverage
    role: supports
    quote: "T-SCI 在 Cox-MLP（神经网络）上恢复 guaranteed coverage——CP 校准神经网络的实例"
counter_evidence:
  - node: thm-split-cp-coverage
    role: context
    note: "coverage 是 marginal（非 conditional）——对子群可能欠覆盖；exchangeability 在分布漂移下失效，需 weighted/online CP 变体"
confidence: high
provenance:
  sources:
    - src-angelopoulos-bates-2022
    - src-teng2021-tsci
---

## 判断背景

「神经网络预测可信吗」是滕佳烨所有论文的引言动机——ML 模型 over-confidence，高风险场景需不确定性量化。

## 判断立场

**单独不可信，CP 包裹后可信**。CP 提供 distribution-free、finite-sample 的 coverage 保证。

## 推理链

1. **问题**：神经网络 over-confidence，直接部署不可靠
2. **CP 的保证**：split CP 在 exchangeability 下 finite-sample distribution-free 保证 coverage
3. **post-hoc 优势**：不重训，包裹任意黑盒模型
4. **滕佳烨的实践**：T-SCI 校准 Cox-MLP，Feature CP 校准 ImageNet/Cityscapes——都是 CP 包裹神经网络

## 诚实边界

- coverage 是 marginal 非 conditional（子群可能欠覆盖）
- exchangeability 在分布漂移下失效（需 weighted/online CP）
- CP 提供的是区间/预测集，非点预测的"置信度校准"（后者是 calibration，不同概念）
