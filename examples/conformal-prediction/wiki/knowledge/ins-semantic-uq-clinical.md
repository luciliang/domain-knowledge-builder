---
id: ins-semantic-uq-clinical
type: insight
label: "Clinical Value of Semantic Uncertainty in Medical Imaging"
source: teneggi2025
section: Sections 1, 3, 5
tokens: 900
created: 2026-06-23
---

## 精确表述

The authors articulate several key insights about the clinical relevance of semantic uncertainty quantification:

1. **Uncertainty must be clinically meaningful.** "Beyond measuring uncertainty, it is crucial to express it in clinically meaningful terms that provide actionable insights." (Abstract) — Pixel-level uncertainty is insufficient for clinical decision-making; clinicians need organ-level information.

2. **Semantic structure reveals model behavior across populations.** The learned vector $\hat{\lambda}_{\text{sem}}$ "directly informs on which organs have higher levels of uncertainty, depicting how the same model may display different uncertainty patterns across different populations." (Section 4) — This is described as "fundamental to the responsible use of general-purpose machine learning models across centers serving diverse demographics."

3. **Per-organ vs. global trade-off is a clinical choice.** "Our methodology gives users the flexibility to specify which organs they desire to control risk for depending on the clinical task at hand." (Section 4) — The choice between sem-CRC (global) and sem-CRC̄ (per-organ) should be driven by the clinical application.

4. **Standard methods hide organ-specific failures.** "All methods but sem-CRC̄ achieve risk control by overcovering background and undercovering organs." (Section 4, Fig 3) — Global risk control can mask significant organ-specific accuracy issues.

5. **Broad applicability.** "Our contributions apply broadly to any imaging inverse problem and any predictor equipped with a heuristic notion of uncertainty." (Section 1) — The method is not limited to CT or quantile regression.

作者的判断：语义不确定性不仅是技术改进，更是临床部署的必要条件。仅控制全局风险是不够的，因为不同器官的重建难度差异可能被掩盖。

## 适用条件

- These insights apply to medical imaging AI deployment scenarios
- Particularly relevant for regulatory approval and clinical trust-building
- The broad applicability claim requires validation in other modalities

## 直觉解释

如果一个人工智能模型在 CT 重建中总体 90% 像素正确，但脾脏只有 70% 正确，而肝脏有 95% 正确——全局指标看不出问题。语义 UQ 让我们看到每个器官的真实表现，这对临床安全至关重要。

## 与其他知识的关系

→ def-semantic-uq（这些洞察基于语义 UQ 的概念）
→ exp-ct-denoising-reconstruction（实验数据支持这些洞察）
→ meth-sem-crc-per-organ（洞察 3-4 直接导致 sem-CRC̄ 的设计）
applies_to → ins-semantic-uq-clinical（适用于医学影像 AI 的临床部署）

## 来源引用

- Teneggi et al. 2025, Abstract, Sections 1, 4, and 5
