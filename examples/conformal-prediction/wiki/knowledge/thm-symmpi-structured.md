---
id: thm-symmpi-structured
type: theorem
label: Theorem 5: Marginal Coverage under SymmPI (Structured Data)
source: min2026
section: Section 4.3
tokens: 900
created: 2026-06-24
---

## 精确表述

Suppose Assumption 8 holds (data Z is (G,ρ)-distributionally invariant and score map V is (G,ρ,$\hat{\rho}$)-distributionally equivariant). Then the marginal coverage of $\hat{C}(z^{obs})$ satisfies

$$1 - \alpha \leq \Pr(Z \in \hat{C}(\Omega(Z))) \leq 1 - \alpha + \mathbb{E}\{\hat{\gamma}_{\max}(Z)\},$$

where $\hat{\gamma}_{\max}(z) = \sup_c |\{g \in G : \psi(\hat{\rho}(g, V(z))) = c\}| / |G|$.

## 适用条件

1. Assumption 8: (G,ρ)-distributional invariance and (G,ρ,$\hat{\rho}$)-distributional equivariance
2. Finite symmetry group G acting on data Z
3. Score extractor ψ maps score vector to test score

## 直觉解释

This extends conformal prediction from i.i.d. exchangeability to general structural symmetry. The marginal coverage guarantee holds with the same structure as classical CP: $1-\alpha$ lower bound plus a tie-related upper term. The key is that symmetry under group actions replaces sample exchangeability as the foundation for validity.

## 与其他知识的关系

← def-unified-cp-framework（将统一框架从 i.i.d. 推广到结构化数据）
→ thm-symmpi-conditional（支撑结构化数据上的条件覆盖分解）
→ thm-marginal-coverage-weighted（i.i.d. 情形的特殊情况）

## 来源引用

Min et al. (2026), Section 4.3, Theorem 5. arXiv:2605.11602v3.
