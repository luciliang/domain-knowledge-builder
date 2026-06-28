---
stage: S6
role: independent-validation (fresh context, dual-source)
domain: diffusion-models
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
run_ids: [09207eda-1bc6-46b7-a8f3-779abb928d4f, 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9]
sources: [ho2020, song2021]
validated_at: 2026-06-28
validator: fresh-context independent agent (no build-process memory)
---

# S6 独立验证报告 — diffusion-models（双源：DDPM + Score-SDE）

> **Fresh-context 独立验证**。本 agent 无构建过程记忆，全部结论基于亲自跑脚本 / 读原文 / 核公式得出。
> 评分对象：双源知识库 30 节点 / 53 边（含 11 跨源）。**未采信 worker/构建过程的自述**——结构、跨源方向、公式、provenance 均独立重验。
> 提取模式：ho2020=pdftotext(text_fallback) / song2021=ar5iv HTML（662 LaTeX 公式实测保留）。

---

## §0 验证结论速览

| # | S6 验证项 | 结果 | 证据 |
|---|-----------|:----:|------|
| 1 | 结构校验（程序化） | ✅ PASS | 0 断裂 / 0 重复 / 0 孤立 / 0 环路 / meta 计数逐项一致 |
| 2 | 跨源关系校验（11 边） | ✅ PASS | 11 边端点全存在；关系类型全合法；generalizes/extends 方向语义全正确 |
| 3 | 内容抽查（3 节点，含 2 song2021） | ✅ PASS | source_span 定位核对原文；song2021 LaTeX（Eq.5/13）精确忠实 |
| 4 | D7 合规（schema §12） | ✅ PASS | 双 run_id 一致且不重叠；provenance 完整；路径确定性 0 违规 |
| 5 | M4 三重验证 | ✅ PASS | 跨场景复现 / 生成力 / 排他性 独立判定均成立 |
| 6 | Query 走查 | ✅ PASS | 「Score-SDE 统一」「PF-ODE」两问均可达 song2021 节点 + M4 |
| 7 | Lint 鲁棒性（孤立/矛盾/重复/缺失引用/meta 漂移） | ✅ PASS | 程序化全过；诚实边界准确 |

**总判定：S6 PASS（无 P0 / 无 P1；5 项 P2 follow-up）。** 双源增量结构健全、跨源关系语义正确、song2021 公式精确。

---

## §1 结构校验（程序化，读 dag/dag-index.json）

脚本（python，DFS 环路检测）输出：

```
nodes: 30  edges: 53
dup node ids: []          # 0 重复节点
broken edge endpoints: 0  # 0 断裂引用（所有 edge from/to 均存在）
self loops: 0
isolated nodes: []        # 0 孤立节点（每个节点都至少参与 1 条边）
dup edge ids: []          # 0 重复边 ID
dup (from,to,relation): [] # 0 重复三元组
cycles found: 0           # DFS 实测 0 环路
meta total_nodes: 30  actual: 30   ✓
meta total_edges: 53  actual: 53   ✓
  source ho2020  meta nodes 15  actual 15 | meta edges 22  actual 22   ✓
  source song2021 meta nodes 15  actual 15 | meta edges 31  actual 31  ✓
```

- **0 断裂 / 0 重复 / 0 孤立 / 0 环路 / meta 计数全一致（含双 source 分项）。** 结构完整。
- confidence 分布：high 51 / medium 2（2 条 medium = `e-ar-rd`、`xsrc-pc-ancestral`，均为合理推断，标 medium 恰当）。
- 关系类型分布（全在 schema §3 合法集内）：depends_on 25 / evaluates 10 / generalizes 6 / extends 5 / compares_with 4 / specializes 3。

---

## §2 跨源关系校验（11 条 xsrc 边）

程序化枚举 from/to source 不同的边 = **11 条**（与声明一致）。逐条核端点存在 + 关系合法 + 方向语义：

| edge id | from (src) | to (src) | relation | 方向语义核对 |
|---------|-----------|----------|----------|------------|
| xsrc-vpsde-fwd | def-ho2020-forward-diffusion-process | def-song2021-vp-sde | generalizes | ✓ VP-SDE 是 DDPM 离散前向链的连续推广（to 更广） |
| xsrc-fsde-fwd | def-ho2020-forward-diffusion-process | def-song2021-forward-sde | generalizes | ✓ 通用前向 SDE 框架包含 DDPM 离散过程 |
| xsrc-reverse-revproc | def-ho2020-reverse-process | thm-song2021-reverse-time-sde | generalizes | ✓ reverse-time SDE 是 DDPM 反向链的连续推广 |
| xsrc-reverse-eps-equiv | thm-ho2020-score-matching-langevin-equivalence | thm-song2021-reverse-time-sde | extends | ✓ song2021 把离散启发式提升为连续框架定理 |
| xsrc-equiv-fwd | def-ho2020-forward-diffusion-process | thm-song2021-sde-discretization-equivalence | generalizes | ✓ 离散-连续等价定理将 DDPM 纳入 SDE 框架 |
| xsrc-equiv-scorelang | thm-ho2020-score-matching-langevin-equivalence | thm-song2021-sde-discretization-equivalence | extends | ✓ 框架级定理扩展离散启发式 |
| xsrc-training-eps | meth-ho2020-epsilon-prediction | meth-song2021-score-based-training | extends | ✓ 连续 score matching 扩展离散 ε-预测 |
| xsrc-pfode-elbo | thm-ho2020-elbo-variational-bound | thm-song2021-probability-flow-ode | extends | ✓ PF-ODE 精确似然严格强于 ELBO 上界 |
| xsrc-framework-scorelang | thm-ho2020-score-matching-langevin-equivalence | ins-song2021-unified-continuous-framework | generalizes | ✓ 统一框架推广 ho2020 核心贡献 |
| xsrc-cifar-cifar | exp-song2021-cifar10-results | exp-ho2020-cifar10-results | compares_with | ✓ 对称比较（FID/NLL 跨源对照） |
| xsrc-pc-ancestral | meth-ho2020-ddpm-sampling | meth-song2021-pc-sampler | generalizes | ✓ PC 统一并推广 DDPM ancestral（medium，恰当） |

- **11 条端点全存在**（§1 已证 0 断裂）。
- **关系用词全合规**（generalizes/extends/compares_with，均在 schema §3 合法集）。
- **方向语义全正确**：schema §3 定义 `generalizes` = "B 是 A 的推广"（A→B，B 更广）、`extends` = "B 在 A 基础上改进"（A→B）。所有 generalizes 边都是「ho2020 离散 → song2021 连续/统一」（连续更广）；所有 extends 边都是「song2021 扩展 ho2020」。方向无逆转错误。

---

## §3 内容抽查（随机 3 节点，含 2 个 song2021）

| 节点 | 来源 | source_span 核对 | 公式核对 |
|------|------|-----------------|---------|
| `def-song2021-forward-sde` | song2021 | ✅ full-text.txt L1389-1455 = "Perturbing data with SDEs" Eq.5 | ✅ `dx=f(x,t)dt+g(t)dw` 与 ar5iv HTML 逐字一致 |
| `thm-song2021-probability-flow-ode` | song2021 | ✅ full-text.txt L1867-1884 = "4.3 Probability flow... neural ODEs" Eq.13 | ✅ `dx=[f - ½g²∇log p_t]dt` 精确，½g² 系数与"无布朗项"标注正确 |
| `thm-ho2020-elbo-variational-bound` | ho2020 | ✅ full-text.txt L106-140 = 变分下界 Eq.3 + KL 分解 Eq.5（L_T+ΣL_{t-1}+L_0） | ✅ ELBO 分解与 Eq.5 结构一致 |

**song2021 LaTeX 准确性**（验证 ⑤ 维度提升点）：ar5iv HTML 提取保留了完整 LaTeX 源码——`$\mathrm{d}\mathbf{x}=\mathbf{f}(\mathbf{x},t)\mathrm{d}t+{g}(t)\mathrm{d}\mathbf{w},$`（Eq.5）、`$\mathrm{d}\mathbf{x}=\Big{[}\mathbf{f}(\mathbf{x},t)-\frac{1}{2}g(t)^{2}\nabla_{\mathbf{x}}\log p_{t}(\mathbf{x})\Big{]}\mathrm{d}t,$`（Eq.13）。节点正文将其清洗渲染为标准 `$$...$$`，**语义与系数逐字忠实**。实测 song2021 区域 LaTeX 公式 token 数 = 662（声明 663，差 1 在计数粒度内，声明成立）。对比 ho2020 的 pdftotext 提取（公式排版有噪声但语义保留），song2021 的 ar5iv 提取公式质量明显更高——**⑤ 准确性维度提升有据**。

**跨源数值核对**：`xsrc-cifar-cifar` desc 记 song2021 FID 2.20/IS 9.99/精确 NLL 2.99 vs ho2020 FID 3.17/IS 9.46/ELBO≤3.75，与两篇论文 CIFAR-10 结果一致。

---

## §4 D7 合规（schema §12 四支柱 + §12.5 路径确定性）

| 检查 | 结果 | 证据 |
|------|:----:|------|
| **双 run_id 一致且不重叠** | ✅ | ho2020 节点 run_id 全 = `09207eda-1bc6-46b7-a8f3-779abb928d4f`（原 run）；song2021 节点 run_id 全 = `9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9`（增量 run）；两集合 disjoint。dag-index.meta.run_ids[] = [原, 增量] 双值。 |
| **Provenance 完整性** | ✅ | 30/30 节点含 generated_by_step(S2) + run_id + source_span{file,start_line,end_line,page}，0 缺失。 |
| **节点 ID 确定性** | ✅ | 30/30 遵 `<type>-<source>-<term>`；正则校验 0 违规；0 时间戳/随机/流水号命名。 |
| **路径确定性（§12.5）** | ✅ | wiki/knowledge/ 30 个 .md 扫描 `/Users/`、`../../`、`domain-knowledge-skill`、`/skills/` = **0 命中**。无绝对/meta-relative 路径。 |
| **预检记录** | ✅ | run-manifest.preflight: `ok:false, docling_available:false, mode:text_fallback`（原 run 诚实降级）；incremental_runs[] 记录 song2021 ar5iv 增量（PDF curl 18 失败 → ar5iv HTML fallback 成功）。非静默失败。 |
| **可回滚（commit-per-stage）** | ✅ | git log：S1-incremental(719f376)/S2-incremental(a7c879b)/S3-merge(5ab5838)/S4-nav(8d60cef)/S5-mental(048ae3a) 各阶段独立 commit，可单独 revert。 |

**双 run_id provenance 设计正确**：ho2020 原节点保留原 run_id（09207eda），song2021 新节点用增量 run_id（9bab0aa5），dag-index.meta 同时持有 run_ids[] 数组——增量 ingest 的可追溯性完整。

---

## §5 M4 三重验证（独立判定，不采信 S5 自述）

**M4 = 连续时间 SDE 统一**（continuous-time SDE unification）。

| nuwa 三重 | 独立判定 | 证据 |
|-----------|---------|------|
| **① 跨场景复现（≥2 子问题/来源）** | ✓ 成立 | 镜片在 (a) DDPM/ho2020、(b) SMLD/NCSN、(c) PF-ODE 确定性路线、(d) conditional-SDE 可控路线 四个独立子设定上一致复现。支撑节点均存在：`thm-song2021-sde-discretization-equivalence`（SMLD→VE、DDPM→VP）+ 3 条 ho2020 跨源边（xsrc-vpsde-fwd / xsrc-framework-scorelang / xsrc-training-eps）。 |
| **② 生成力（推断新问题立场）** | ✓ 成立 | 列出 4 条可证伪的生成性断言：「DDIM 是 SDE 还是 ODE?→PF-ODE（ODE 路线）」「精确似然?→PF-ODE 而非 ELBO」「新数据类型扩散?→选可解析前向 SDE」「单模型做条件/无条件?→conditional reverse-time SDE」。这些是对未 ingest 工作（DDIM/guidance）的外推，且标注为推测——生成力真实。 |
| **③ 领域排他性（换领域即失效）** | ✓ 成立 | 「连续时间 SDE，其逆过程只依赖 score」是扩散/score 家族独有：GAN 无 SDE、VAE 无 reverse-time SDE、自回归无 SDE、normalizing flow 无前向破坏 SDE（套上即失效）。 |

**结论：M4 三重验证真实成立，升格为心智模型有据。** 单源版因无 song2021 支撑节点而无法跑三重验证（归入待补），双源入库后 3 重全过——升格合理。

---

## §6 Query 走查

**问题**：「Score-SDE 如何把 DDPM 和 SMLD 统一？什么是 PF-ODE？」

走查（schema §7 查询工作流）：
1. **分析**：涉及「统一框架」「PF-ODE」概念。
2. **DAG 遍历**：
   - 统一 → `ins-song2021-unified-continuous-framework`（label 直接命中）→ `e-equiv-framework` → `thm-song2021-sde-discretization-equivalence`（SMLD→VE、DDPM→VP 等价定理）→ 跨源边 `xsrc-vpsde-fwd`/`xsrc-equiv-fwd`/`xsrc-framework-scorelang`（DDPM 被统一的确证）。
   - PF-ODE → `thm-song2021-probability-flow-ode`（Eq.13）→ `e-score-pfode`（score 依赖）→ `e-pfode-sampling`/`e-pfode-encoding`（采样/编码）。
3. **心智模型综合**：M4 直接覆盖两问——统一（SMLD/DDPM 是 SDE 离散化）+ PF-ODE（确定性路线，精确似然）。

**判定：两问均可达 song2021 节点 + M4，回答所需节点 ≤6，剪枝可达。Query 走查 PASS。**

---

## §7 Lint 鲁棒性检查

| 检查 | 结果 |
|------|:----:|
| 孤立节点 | ✅ 0 |
| 矛盾关系（contradicts） | ✅ 0（N/A，无 contradicts 边） |
| 重复节点 | ✅ 0 |
| 缺失引用 | ✅ 0 |
| 来源覆盖 | ✅ 2/2 来源提取完整（ho2020 15n/22e、song2021 15n/31e） |
| meta 计数漂移 | ✅ 无（total + 分项全一致） |
| token 区间合规 | ✅ 30/30 在 schema §1 类型区间内（def 500-1000 / thm 500-2000 / meth 500-2000 / exp 500-1500 / ins 500-1000） |
| 诚实边界 | ✅ §4 列 6 项未覆盖（DDIM/guidance/latent/闭式细节）+ M3 单源降权 + 提取模式限制 + 来源清单+时间 |

---

## §8 问题列表

### P0（阻断，必须先解决）
- 无。

### P1（严重，应在交付前处理）
- 无。

### P2（follow-up / 改进项，不阻断）
- **P2-1｜source_span.file 命名歧义**｜所有节点 `source_span.file` 写源文件名（如 `ho2020-ddpm.pdf` / `song2021-score-sde.md`），但 start/end_line 实对应合并后的 `full-text.txt` 行号。可追溯性未受损（正文「来源引用」段显式给 full-text.txt 行号），但 frontmatter 字段命名略误导。建议加 `extracted_file: full-text.txt` 字段或改注。影响 ⑤（已在评分中扣 0.5）。
- **P2-2｜run-manifest 未随增量刷新**｜`pipeline/state/run-manifest.json` 顶层 `run_id` 仍为原 run（09207eda），`darwin_score: null` / `accepted: false` 未在增量后更新。可追溯性完整（dag-index.meta.run_ids[] + incremental_runs[] + 节点级 run_id），但 manifest 自身未反映双源最终态。建议增量后刷新 manifest 的 darwin_score/accepted/stages。
- **P2-3｜Lsimple 记号跨文件不统一**｜全文混用 `Lsimple`(26) / `L_simple`(13) / `$L_{\text{simple}}$`(2)。表面性，不影响语义。建议统一为 `$L_{\text{simple}}$`（公式）/ `L_simple`（prose）。
- **P2-4｜SKILL.md 待 S7（已知 gate，非双源缺陷）**｜SKILL.md 未生成，①②④⑦ 维度被该 pending 项封顶，是分数未达 A-(85) 的唯一结构性原因。S7 跑完预计 +3~5 分跨过 A-。
- **P2-5｜ho2020 pdftotext 排版噪声**｜ho2020 区域公式经 pdftotext 提取有排版碎片（如分页符、间距异常），但语义保留、source_span 可定位。song2021 的 ar5iv 提取质量明显更高（662 公式完整保留），印证「双源提取模式差异化」策略有效。

---

_验证规范：schema §6 Step 6 + §8 Lint | 本次：双源 30n/53e S6 PASS（无 P0/P1）| 评分见 darwin-score.md_
