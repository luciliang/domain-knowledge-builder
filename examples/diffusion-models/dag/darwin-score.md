---
stage: S6.5-darwin
role: independent-scoring (fresh context, dual-source)
domain: diffusion-models
run_id: 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9
run_ids: [09207eda-1bc6-46b7-a8f3-779abb928d4f, 9bab0aa5-cf9d-4d60-af8b-1d19de0dd9f9]
scored_at: 2026-06-28
scorer: darwin 2.0 fresh-context independent agent
rubric: engines/darwin-rubric.md §1 (9-dim) + §2.3 (generator-skill subclass)
eval_mode: full_test
total_score: 84.70
grade: B+
passes_gate: true
prior_score: 80.35
prior_grade: B+
delta: +4.35
---

# Darwin 2.0 独立评分报告 — diffusion-models 知识库（双源重评）

> **Fresh-context 独立评分**。本评分由无构建过程记忆的独立 agent 完成，所有结论均基于亲自读文件 / 跑脚本 / 核原文得出。
> 评分对象：**双源**——DDPM（Ho et al. NeurIPS 2020，pdftotext text_fallback）+ Score-SDE（Song et al. ICLR 2021，ar5iv HTML）。声明产出：30 节点 / 53 边（含 11 跨源）/ 4 心智模型 / 9 决策启发式 / 662 LaTeX 公式保留。
> **未采信 S6 validation-report 与 worker 自述**——D7 四支柱、结构校验、跨源方向、公式、provenance 均由本 agent 重新独立验证（见 §3 独立验证记录）。
>
> ⚠️ **SKILL.md 仍待 S7**（本 agent 确认：根目录无 SKILL.md）。依赖 SKILL.md 的维度（①结构完整性的顶层 frontmatter、②④⑦ 的查询协议部分）按「当前可用产物」评分，并注明 S7 待跑。

---

## §0 结论速览

| 维度 | 权重 | 得分(1-10) | 加权 | 单源基线 | Δ | 等级锚点 | 扣分点 |
|------|:----:|:----------:|:----:|:--------:|:--:|----------|--------|
| ① 结构完整性 | 15% | **7.5** | 1.125 | 7.5 | — | 合格+ | SKILL.md 待 S7；无 CHANGELOG |
| ② 清晰度 | 15% | **8.5** | 1.275 | 8.0 | +0.5 | 优秀 | 查询协议继承 schema 非在 skill 内 |
| ③ 内容完整性 | 15% | **8.5** | 1.275 | 7.0 | **+1.5** | 优秀 | guidance/latent/DDIM 仍缺（已诚实标注） |
| ④ 可操作性 | 15% | **8.0** | 1.200 | 8.0 | — | 优秀 | 无 in-skill 查询协议（SKILL.md 待 S7） |
| ⑤ 准确性 | 10% | **9.5** | 0.950 | 9.0 | **+0.5** | 优秀 | source_span.file 命名歧义 |
| ⑥ 一致性 | 10% | **9.5** | 0.950 | 9.0 | **+0.5** | 优秀 | Lsimple 记号跨文件不统一（表面） |
| ⑦ 执行效率 | 8% | **7.5** | 0.600 | 7.5 | — | 合格+ | 无紧凑 SKILL.md 锚点（<4K）聚合入口 |
| ⑧ 鲁棒性 | 7% | **8.5** | 0.595 | 8.0 | +0.5 | 优秀 | 无显式环路检测说明（实测 0 环路） |
| ⑨ 元技能合规(generator) | 5% | **10.0** | 0.500 | 10.0 | — | 满分 | 四支柱全 ✓（独立验证，见 §2） |

**加权总分 = 8.470 × 10 = 84.70 / 100**

**等级：B+（≥80）— ✅ 通过质量门**（较单源 80.35 → 84.70，**+4.35**）。

> 距 A-(85) 仅 **0.30 分**。唯一结构性瓶颈 = SKILL.md 未生成（①②④⑦ 四维被该 pending 项封顶）。S7 跑完预计 +3~5 分跨过 A-。**双源增量本身在可评分维度（③⑤⑥②⑧）全部持平或提升，无任何维度退步。**

---

## §1 维度详评（双源）

### ① 结构完整性 (15%) — 7.5/10（持平）

**正确点**：
- 节点 frontmatter **30/30 规范完整**：9 基础字段 + 4 D7 provenance 字段，脚本批检全通过。
- `dag-index.json` meta 丰富：domain/created/last_updated/total_nodes(30)/total_edges(53)/sources(双)/run_id + run_ids[] 数组（双 run 可追溯）。
- 导航结构合理：`index.md`（30 节点按类型分组带链接+摘要+来源标注）/ `overview.md`（双源领域概览）/ `mental-models.md`（4 镜片）/ `sources/{ho2020,song2021}.md` / `log.md` / 入口提示。
- 节点正文统一五段结构（精确表述/适用条件/直觉解释/与其他知识的关系/来源引用）。

**扣分（−2.5）**：
- **SKILL.md 未生成（S7 待跑）**——rubric ① 满分要点要求「YAML frontmatter 规范完整(name/description/domain/sources/nodes/edges/version)」，该规范 frontmatter 宿主即 SKILL.md，当前缺失。已知 pending 非缺陷，取 7.5。
- 无 CHANGELOG（`log.md` 部分替代）、无 Getting-Started 示例。

### ② 清晰度 (15%) — 8.5/10（+0.5）

**正确点**：
- 4 心智模型均「一句话开头」再展开：M1「一旦固定那条前向破坏过程…全部件由它派生耦合」、M2「…score 被确立为整个生成框架的唯一依赖量」、M3「扩散生成天然是一个率-失真过程」、M4「扩散生成的本质是一条前向 SDE + reverse-time SDE…统一即力量」。✅
- **§0 三重验证总表带「双源评级变化」列**——逐模型标注单源→跨源的证据强化（M1/M2 caveat 解除、M4 升格），可读性极高。
- 9 条决策启发式全 actionable，每条带「触发场景」+「支撑节点」+ "若 X 则 Y" 格式；H5–H8 为 song2021 新增。
- 术语中英对照充分（forward SDE / drift / diffusion coefficient / probability flow ODE / Predictor-Corrector / variance exploding/preserving）。

**扣分（−1.5）**：
- 查询/工作流步骤（分析→遍历→加载→综合→存档）+ 剪枝规则（3-5 节点）+ 优先级排序在继承的 meta-skill schema §7，**未在 skill 内复述**（SKILL.md 待 S7）。

### ③ 内容完整性 (15%) — 8.5/10（**+1.5，最大提升**）

**正确点**：
- **双源覆盖扩散/score 生成范式的两大奠基论文**：DDPM（离散）+ Score-SDE（连续统一），30 节点无空壳。
- song2021 补全了单源版缺失的全部现代热点：连续时间前向 SDE、reverse-time SDE（Anderson）、probability flow ODE、VE/VP/sub-VP SDE、离散-连续等价定理、PC 采样器、conditional SDE、精确似然（瞬时变量替换）、唯一可识别编码、统一框架洞察。
- 节点密度高，与论文结构 1:1 对应（def 7 + thm 5 + meth 8 + exp 5 + ins 5）。
- 11 条跨源关系（generalizes/extends/compares_with）把离散↔连续真正连接，非简单堆叠。
- **诚实边界范例级**：§4 列 6 项未覆盖（DDIM/guidance/latent/闭式细节/M3 单源降权/提取模式限制）+ 开放问题 + 来源清单 + 双 run_id 时间。

**扣分（−1.5）**：
- 仍缺领域现代应用主线：classifier(-free) guidance、latent diffusion/Stable Diffusion、DDIM（虽已诚实标注边界，但 rubric 扣分点「遗漏领域当前热点」部分命中）。
- M3 率-失真分解视角仍主要由 ho2020 单方面刻画（song2021 仅确认粗→细+精确码长），已诚实降权。

### ④ 可操作性 (15%) — 8.0/10（持平）

**正确点**：
- **token 约束全达标**：30/30 节点在 schema §1 类型区间内（脚本核对 0 越界）。
- 定理/定义节点保留原文精确表述含 LaTeX：Eq.5（前向 SDE）、Eq.13（PF-ODE）、Eq.3/5（ELBO）、Eq.7（连续 score matching）——公式经核与原文一致。
- 节点模板一致应用；DAG 边带 type + desc + confidence，可遍历。
- 外部依赖有 fallback：docling 不可用→text_fallback，PDF 失败→ar5iv HTML，preflight + incremental_runs 均记录（诚实降级非静默）。

**扣分（−2）**：
- 无 in-skill 查询协议（分析→遍历→加载→综合→存档的逐步可执行约束），SKILL.md 待 S7。

### ⑤ 准确性 (10%) — 9.5/10（**+0.5**）

**正确点**：
- **公式独立核对正确（双源）**：
  - song2021 Eq.5 `dx=f(x,t)dt+g(t)dw` ✅（与 ar5iv HTML 逐字一致）；
  - song2021 Eq.13 `dx=[f−½g²∇log p_t]dt` ✅（½g² 系数与"无布朗项"标注精确）；
  - ho2020 ELBO KL 分解 `L=L_T+ΣL_{t-1}+L_0` ✅；q(x_t|x_0)=N(√ᾱ_t x_0,(1−ᾱ_t)I) ✅。
- **跨源数值核对正确**：`xsrc-cifar-cifar` 记 song2021 FID 2.20/IS 9.89/精确 NLL 2.99 vs ho2020 FID 3.17/IS 9.46/ELBO≤3.75，与两篇论文一致。
- 心智模型与经典理论一致（M1 前向引擎 / M2 变分⟺score / M3 率-失真 / M4 连续统一）。
- **跨源边方向独立校验**：11 条 generalizes/extends/compares_with 方向语义全正确（见 validation-report §2）。
- 来源引用精确到 章节公式 + full-text.txt 行号。
- **song2021 ar5iv LaTeX 质量明显高于 ho2020 pdftotext**——662 公式完整保留、系数逐字忠实，⑤ 准确性提升有据。

**扣分（−0.5）**：
- `source_span.file` 写源文件名（ho2020-ddpm.pdf / song2021-score-sde.md），但 start/end_line 实对应合并的 full-text.txt 行号。可追溯性未受损（正文显式给 full-text.txt 行号），但 frontmatter 字段命名略歧义。

### ⑥ 一致性 (10%) — 9.5/10（**+0.5**）

**正确点**：
- 结构一致性脚本全过：**0 断裂引用 / 0 重复 ID / 0 孤立节点 / meta 计数(30n/53e + 双 source 分项)逐一对账一致**。
- node ID 全遵 `<type>-<source>-<term>`（30/30，正则校验 0 违规，无时间戳/随机/流水号）。
- **run_id 双值可追溯**：ho2020 节点 = 09207eda（原 run）、song2021 节点 = 9bab0aa5（增量 run），disjoint；dag-index.meta.run_ids[] 持双值。
- **跨源关系方向标准化**：11 条 xsrc 边统一用 generalizes（离散→连续推广）/ extends（连续扩展离散）/ compares_with（对称比较），方向语义全正确——一致性较单源实质提升。
- index.md 30 节点 = dag-index nodes，链接 0 断裂。

**扣分（−0.5）**：
- Lsimple 记号跨文件不统一：`Lsimple`(26)/`L_simple`(13)/`$L_{\text{simple}}$`(2)。表面性，不影响语义。

### ⑦ 执行效率 (8%) — 7.5/10（持平）

**正确点**：
- 继承查询设计高效：3-5 节点 × ~1K = 3-5K token/查询预算；优先级剪枝避免全图遍历。
- 心智模型独立文件 `mental-models.md`（4 镜片），可按需加载不每查询重载。
- schema 走按需加载；index.md 紧凑（分组一句话摘要）。
- 跨源关系使离散↔连续查询可 1-2 跳到达（关系密度高，导航效率好）。

**扣分（−2.5）**：
- 无紧凑 SKILL.md 锚点（<4K）聚合查询协议+核心心智模型+索引入口，按需加载缺统一入口（S7 待生成）。
- 节点数翻倍（15→30）使 dag-index 基础加载略增，被关系密度提升部分抵消，净持平。

### ⑧ 鲁棒性 (7%) — 8.5/10（+0.5）

**正确点**：
- **诚实边界范例级**：三段（已覆盖 / 未覆盖 6 项 / 开放问题）+ **双源过渡的显式自评**（M1/M2/M4 caveat 解除、M3 仍 ho2020-weighted 降权）+ 提取模式限制 + 来源清单 + 双 run_id 时间。这种"哪些单源警示已解除、哪些保留"的元级鲁棒性自评很扎实。
- 查询协议要求「知识不足则明确说明」（继承 schema §7 Step4）。
- Lint 覆盖孤立/矛盾/重复/缺失引用/meta 漂移——程序化全过。
- **环路检测实测 0 环路**（本 agent 独立 DFS 验证）。

**扣分（−1.5）**：
- 无显式「环路检测说明」文档（虽实测无环）。

### ⑨ 元技能合规 — generator-skill 子类 (5%) — 10.0/10（持平）

**四支柱独立验证（未采信 S6 结论）**，全部满足：

| 支柱 | 要求 | 本 agent 独立验证 | 结果 |
|------|------|-------------------|:----:|
| **① 可回滚** | commit-per-stage，可 revert | `git log`：S1-incremental(719f376)/S2-incremental(a7c879b)/S3-merge(5ab5838)/S4-nav(8d60cef)/S5-mental(048ae3a) + 原 S1-S6(单源)，每 stage 独立 commit 可单独 `git revert` | ✅ |
| **② 可审计** | provenance 完整 + run_id 可追溯 | 脚本批检 30/30 节点 D7 齐全；**双 run_id 正确分配**（ho2020=原、song2021=增量，disjoint）；source_span grep 可回溯原文（实测定位正确）；results.tsv 追踪 | ✅ |
| **③ 确定性** | ID 遵 `<type>-<source>-<term>` 无随机/时间戳 | 正则校验 30/30 节点 + 53 边 ID 均语义 slug，无时间戳/随机/流水号，可重放同 ID | ✅ |
| **④ 预检** | 依赖缺失有 fallback/报错不静默 | run-manifest preflight：`ok:false, docling_available:false, mode:text_fallback`（原 run 诚实降级）；incremental_runs[] 记 song2021 PDF→ar5iv fallback | ✅ |
| **路径确定性(§12.5)** | 节点 .md 无绝对/meta-relative 路径 | grep `/Users/`、`../../`、`domain-knowledge-skill`、`/skills/` 于 wiki/knowledge = **0 命中** | ✅ |

四支柱全满足 = 10/10。无严重违规（无不可审计/不可回滚/静默失败）。**双源增量在可审计支柱上反而更彻底**——双 run_id provenance + incremental_runs 记录使增量可追溯性强于单源。

---

## §2 总分与等级

```
加权总分 = Σ(维度分 × 权重) × 10
        = (7.5×.15 + 8.5×.15 + 8.5×.15 + 8×.15 + 9.5×.10 + 9.5×.10 + 7.5×.08 + 8.5×.07 + 10×.05) × 10
        = (1.125 + 1.275 + 1.275 + 1.200 + 0.950 + 0.950 + 0.600 + 0.595 + 0.500) × 10
        = 8.470 × 10
        = 84.70 / 100
```

| 等级 | 区间 | 判定 |
|------|------|:----:|
| A+ | ≥95 | |
| A | ≥90 | |
| A- | ≥85 | （差 0.30） |
| **B+** | **≥80** | **✅ 84.70 — 通过质量门** |
| B | ≥75 | |

**质量门（B+ ≥80）：✅ PASS（84.70，较单源 80.35 +4.35）。** 距 A- 0.30 分，瓶颈为 SKILL.md（S7 待跑）。

---

## §3 单源(80.35) → 双源(84.70) 对比

| 维度 | 单源 | 双源 | Δ | 变化归因 |
|------|:----:|:----:|:--:|----------|
| ① 结构 | 7.5 | 7.5 | — | SKILL.md 仍待 S7（瓶颈未变） |
| ② 清晰度 | 8.0 | 8.5 | +0.5 | 4 镜片 + 跨源评级变化列 + 9 启发式更清晰 |
| ③ 内容完整性 | 7.0 | 8.5 | **+1.5** | song2021 补全连续时间/SDE/PF-ODE/PC/精确似然，单源→双源 |
| ④ 可操作性 | 8.0 | 8.0 | — | in-skill 协议仍待 S7 |
| ⑤ 准确性 | 9.0 | 9.5 | **+0.5** | ar5iv LaTeX 公式精确（Eq.5/13 逐字忠实），优于 pdftotext |
| ⑥ 一致性 | 9.0 | 9.5 | **+0.5** | 跨源方向标准化（11 边 generalizes/extends 方向统一） |
| ⑦ 执行效率 | 7.5 | 7.5 | — | SKILL.md 锚点仍缺（节点翻倍被关系密度抵消） |
| ⑧ 鲁棒性 | 8.0 | 8.5 | +0.5 | 双源过渡的元级自评（caveat 解除/保留标注）扎实 |
| ⑨ 元技能合规 | 10.0 | 10.0 | — | 四支柱全 ✓（双 run_id provenance 更彻底） |
| **总分** | **80.35** | **84.70** | **+4.35** | |

**核心结论**：
- **5 维提升**（②③⑤⑥⑧），**0 维退步**，**4 维持平**（①④⑦⑨，全因 SKILL.md 待 S7 封顶）。
- 提升主力 = ③内容完整性（+1.5，单源→双源补全连续时间理论）。
- 双源增量在所有可评分维度（不受 SKILL.md 影响的）全部持平或提升——**增量无任何副作用**。
- 未达 A-(85) 的唯一原因 = SKILL.md 未生成（①②④⑦ 四维封顶）；**非双源工作的缺陷**。S7 预计 +3~5 分跨过 A-。

---

## §4 双源增量是否值得（总体判断）

**值得。三条独立证据**：

1. **M4 心智模型成立**（独立验证三重全过）：连续时间 SDE 统一是扩散/score 范式的核心镜片，单源版因无支撑节点无法建立，双源后真实升格。生成力覆盖 DDIM/guidance 等未 ingest 工作的外推（标注为推测），排他性成立。

2. **分数实质提升 +4.35**（80.35→84.70），5 维提升 / 0 维退步。距 A- 仅 0.30，且瓶颈明确为 S7（SKILL.md），与双源工作无关。

3. **跨源关系价值高**：11 条 generalizes/extends/compares_with 边把离散 DDPM 与连续 SDE 真正连接（非堆叠），方向语义全正确，使「两个看似不同的方法是同一连续理论的离散化」可被查询遍历直接回答。song2021 的 ar5iv LaTeX（662 公式）还把 ⑤ 准确性推到 9.5。

**净判断：双源增量是该知识库从「单篇论文笔记」迈向「领域范式镜片」的关键一步，ROI 高，无副作用。建议续跑 S7（SKILL.md）解锁 A-。**

---

## §5 独立验证记录（不采信 S6 / worker 结论）

本 agent 亲自执行的检查：
- 结构脚本：0 断裂/0 重复/0 孤立/0 环路/meta 计数(含双 source 分项)一致 ✅
- 跨源边：11 条端点全存在 + 关系合法 + 方向语义正确 ✅
- token 区间：30/30 达标 ✅
- node ID 规范：30/30 遵 `<type>-<source>-<term>` ✅
- run_id 双值：ho2020=09207eda(原) / song2021=9bab0aa5(增量)，disjoint ✅
- 路径确定性：wiki/knowledge 0 绝对/meta-relative 路径 ✅
- 公式/数值：独立核对 Eq.5/13(song2021) + Eq.3/5(ho2020) + 跨源 CIFAR-10 数值 ✅
- commit-per-stage：git log S1-S5 增量 + 原单源各阶段独立可 revert ✅
- preflight + incremental_runs：诚实降级 + ar5iv fallback 记录在 ✅
- M4 三重验证：跨场景/生成力/排他性独立判定成立 ✅
- SKILL.md：根目录确认无（S7 未跑）✅

---

_评分规范：darwin-rubric.md v2.0 | 质量门：B+(80/100) | 本次 84.70 B+ PASS（单源 80.35 → 双源 84.70，+4.35；A- 差 0.30，瓶颈 SKILL.md/S7）_
