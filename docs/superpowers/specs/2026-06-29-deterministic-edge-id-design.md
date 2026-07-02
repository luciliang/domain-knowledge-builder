# 设计：确定性边 ID 公式（Deterministic Edge ID Formula）

> 状态：已批准（2026-06-29）｜规模：小（1 lint 函数 + 4 测试 + 4 处 schema 文档）
> 来源：对比 Hyper-Extract 的 `identifiers: {relation_id: '{source}|{type}|{target}'}` 机制，补齐 DKB §10 Determinism 在**边层面**的缺口。
> 父 spec：`2026-06-28-expert-advisor-builder-design.md`

---

## 1. 动机：现状盲区

探索 `pipeline/state/lint_d7.py` 发现两个问题，其中第一个是本次要补的**真实盲区**：

1. **边 ID 完全没有校验** —— `check_deterministic`（lint_d7.py:110）只遍历 `dag-index.json` 的 `nodes`，从未碰 `edges`。schema §4 的边 ID 是 `e-gc-coverage` 这种**手写 slug**，同一条逻辑边重跑必然产生不同 ID → 增量合并时无法去重 → §10 Determinism 在边层面失效。
2. **节点 ID 格式校验形同虚设**（lint_d7.py:126-128）—— 命中 `NODE_ID_RE` 不匹配时直接 `pass`，仅为容忍 CP 实例的旧格式 `<type>-<term>`。本次**不修**（见 §6 已知后续项）。

## 2. 决策（已与用户确认）

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 边 ID 公式形式 | `{from}\|{relation}\|{to}`（管道符、无前缀） | `\|` 不在节点 ID 字符集 `[a-z0-9-]` 内 → 零歧义、可 `split('\|')` 反解析、与节点 ID 天然不冲突；与 Hyper-Extract 一致 |
| 现有 examples 处理 | **全不动**，只对新生成强制 | 4 个 examples 走 `--legacy-ok` 宽容；零迁移风险，golden reference 物理不变 |

## 3. 公式

```python
def compute_edge_id(edge) -> str:
    return f"{edge['from']}|{edge['relation']}|{edge['to']}"
```

- 纯函数、确定性：同一 `{from, relation, to}` 永远产生同一 `edge_id`
- 可反解析：`edge_id.split('|')` 无损还原三元组（三字段内部均无 `|`）
- 幂等去重：增量合并时按 `edge_id` 判等，同逻辑边不重复入库

## 4. 改动清单

### 4.1 `pipeline/state/lint_d7.py`
- 新增 `compute_edge_id(edge) -> str`
- `check_deterministic(target_root, legacy_ok)`：
  - 签名加 `legacy_ok`（与 `check_auditable` 对齐）
  - 遍历 `edges`：若 `e["id"] != compute_edge_id(e)` → `legacy_ok` 为真计 `legacy_edges`（警告），否则计 `bad_edge_id`（error）
  - 边 ID 去重：重复 `edge_id` 计 `duplicate_edges`（error，幂等的另一面）
- `main()`：`check_deterministic(target, args.legacy_ok)`；输出新增 `bad_edge_id` / `legacy_edges` / `duplicate_edges` 统计

### 4.2 `pipeline/state/test_lint_d7.py`（TDD，先写先红）
- `test_compute_edge_id_formula`
- `test_check_deterministic_flags_non_formula_edge_id`（严格模式报错）
- `test_check_deterministic_legacy_ok_tolerates_old_edge_id`（legacy 宽容）
- `test_check_deterministic_flags_duplicate_edge_id`

### 4.3 `schema/schema.md`（4 处措辞级）
- **§3** 关系类型表后补边 ID 规范一句，指向 §10
- **§4** edge 的 `id` 注释从手写 slug 改为公式生成 + 公式化例子
- **§10** 新增 §10.2「边 ID 确定性」：公式 + 幂等去重 + lint + legacy 宽容
- **§12.3** 四支柱之"确定性"加边 ID 公式校验条目

## 5. Legacy 策略

- `--legacy-ok` 语义顺势扩展：**容忍历史数据的所有旧格式**（缺 provenance 节点 + 旧 slug 边 ID），一处开关管到底
- 现有 4 个 examples（conformal-prediction / hinton-advisor / tengjiaye-advisor / diffusion-models）跑 lint 时带 `--legacy-ok`
- 新生成 skill 默认严格（不带 `--legacy-ok`）

## 6. 明确不做（YAGNI）

- 不迁移任何现有 examples 的边 ID
- 不修节点 ID 格式校验的空操作 bug（lint_d7.py:126 `pass`）—— 涉及 CP 旧格式 `<type>-<term>` 与新格式 `<type>-<source>-<term>` 的区分，独立议题，留后续
- 不引入运行时抽取（Hyper-Extract 理念不抄，DKB 是构建时生成器）

## 7. 验收标准

- [ ] 4 个新测试全绿
- [ ] 现有测试全绿（不回归）
- [ ] 现有 examples 带 `--legacy-ok` 跑 lint 不报边 ID error
- [ ] schema §3/§4/§10/§12.3 四处更新，措辞与现状一致
