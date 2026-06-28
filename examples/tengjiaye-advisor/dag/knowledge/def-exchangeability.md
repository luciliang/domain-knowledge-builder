# Exchangeability（可交换性）

> 节点 ID: `def-exchangeability` | type: definition | 来源: `src-angelopoulos-bates-2022`

## 定义

随机变量序列 $(Z_1, Z_2, \dots, Z_n)$ 称为 **exchangeable（可交换）**，若其联合分布在任意置换 $\pi$ 下不变：

$$
(Z_1, \dots, Z_n) \stackrel{d}{=} (Z_{\pi(1)}, \dots, Z_{\pi(n)}) \quad \forall \pi
$$

## 与 i.i.d. 的关系

- i.i.d.（独立同分布）⇒ exchangeable，但反之不成立
- exchangeability **弱于** i.i.d.：允许序列内有依赖，只要"谁在前谁在后"不影响联合分布
- de Finetti 定理：可交换序列可表示为某个参数下的 i.i.d. 混合

## 为何是 CP 的基石

Split CP 的 coverage 保证（`thm-split-cp-coverage`）**只需 exchangeability，不需 i.i.d.**。这是 CP 相对参数方法的优势：假设更弱，适用更广。

## 何时被破坏

- **时间序列**：有序列依赖，exchangeability 失效（需 weighted / online CP 变体）
- **covariate shift**：训练/测试分布协变量不同（T-SCI 的 censoring 场景，`thm-teng2021-tsci-coverage`，用 weighted conformal 修复）
- **分布漂移**：test 与 calibration 不同分布

## 在滕佳烨工作中的地位

- T-SCI 的核心挑战就是 censoring 导致 covariate shift、exchangeability 受威胁，滕佳烨用 weighted conformal inference（基于 strong ignorability `T ⊥ \Delta | X`）恢复保证
- Feature CP / FFCP / SCD-split / PT 都在标准 exchangeability 下工作，把精力放在效率/可解释性/度量充分性上
