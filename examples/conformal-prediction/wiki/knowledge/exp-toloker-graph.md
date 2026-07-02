---
id: exp-toloker-graph
type: experiment
label: GraphCP on Toloker Dataset (Real Graph Data)
source: min2026
section: Section 5.2, Table 3
tokens: 1000
created: 2026-06-24
---

## 精确表述

GraphCP applied to Toloker graph dataset (11,758 nodes, 519,000 edges, crowdsourcing platform). Nodes represent annotators, edges shared task annotations, binary response = banned status. LightGBM classifier with neighborhood features. Louvain community detection yields 8 communities.

Key findings (Table 3):
- GraphCP aggregate miscoverage: 0.0170 vs StdCP: 0.0358 (52% reduction)
- Average prediction-set size: GraphCP 1.3150 vs StdCP 1.2745 (3.2% increase)
- Largest improvement in communities 1–3 (largest communities)
- Community 8 (smallest): StdCP miscoverage 0.131, GraphCP 0.105
- 10 predefined random splits, 2:1:1 train/calibration/test ratio

## 适用条件

Binary classification on graph data with detected community structure.

## 直觉解释

GraphCP achieves substantially better community-conditional coverage with minimal efficiency loss. The improvement validates the within-community ranking approach: calibrating within communities removes community-level heterogeneity, leading to more uniform coverage across communities.

## 与其他知识的关系

← meth-min2026-graphcp（验证 GraphCP 方法）
← thm-community-conditional（验证 Theorem 7 的理论预测）

## 来源引用

Min et al. (2026), Section 5.2, Table 3. arXiv:2605.11602v3.
