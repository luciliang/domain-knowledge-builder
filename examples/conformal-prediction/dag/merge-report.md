# DAG Merge Report

**Generated:** 2026-06-24
**Source Files:** extraction-p1.json, extraction-p3.json, extraction-p4.json
**Output:** dag/dag-index.json

## Summary

| Metric | P1 (angelopoulos2022) | P3 (teneggi2025) | P4 (min2026) | Merged Total |
|--------|----------------------|-------------------|---------------|-------------|
| Nodes  | 21             | 9            | 20            | 49 (after dedup) |
| Edges  | 72             | 21            | 42            | 135 (after dedup + normalization) |

## Cross-Paper Duplicate Nodes (same ID, merged)

| Node ID | Found In | Resolution |
|---------|----------|------------|
| `def-conditional-coverage` | p1, p4 | Kept most complete version |

## Relation Normalization (invalid → schema-valid)

54 edges had relation types not in the schema-defined 10 types. All were successfully mapped:

| Normalized Relation | Count | Original Types Mapped |
|---------------------|-------|---------------------|
| `compares_with` | 1 | analogous_to |
| `contradicts` | 2 | contrasts_with, does_not_guarantee |
| `depends_on` | 1 | affected_by |
| `evaluates` | 5 | evaluated_by, measured_by |
| `extends` | 15 | approximated_by, complements, composable_with, extended_by, extends_to, informs, motivates |
| `generalizes` | 7 | approximates, characterized_by, characterizes, includes_special_case, limited_by, weaker_than |
| `guarantees` | 18 | achieves, approximately_preserves, guaranteed_by, preserved_by, preserves, satisfies, underpins, validates |
| `specializes` | 5 | is_a, special_case_of, specializes_to |

## Full Relation Mapping Details

| Edge ID | Original | Normalized | Source |
|---------|----------|------------|--------|
| `e-split-cp-marginal` | `achieves` | `guarantees` | p1 |
| `e-split-cp-aps` | `extends_to` | `extends` | p1 |
| `e-split-cp-cqr` | `extends_to` | `extends` | p1 |
| `e-split-cp-unc` | `extends_to` | `extends` | p1 |
| `e-split-cp-bayes` | `extends_to` | `extends` | p1 |
| `e-thm1-conformal-cov` | `is_a` | `specializes` | p1 |
| `e-thm1-split-cp` | `validates` | `guarantees` | p1 |
| `e-thm1-covshift` | `extended_by` | `extends` | p1 |
| `e-thm1-drift` | `extended_by` | `extends` | p1 |
| `e-thm1-group-bal` | `specializes_to` | `specializes` | p1 |
| `e-thm1-class-cond` | `specializes_to` | `specializes` | p1 |
| `e-thm1-outlier` | `specializes_to` | `specializes` | p1 |
| `e-marginal-conditional` | `weaker_than` | `generalizes` | p1 |
| `e-marginal-beta` | `characterized_by` | `generalizes` | p1 |
| `e-marginal-covshift` | `preserved_by` | `guarantees` | p1 |
| `e-marginal-drift` | `preserved_by` | `guarantees` | p1 |
| `e-conditional-impossible` | `limited_by` | `generalizes` | p1 |
| `e-conditional-fsc` | `measured_by` | `evaluates` | p1 |
| `e-conditional-ssc` | `measured_by` | `evaluates` | p1 |
| `e-conditional-group-bal` | `approximated_by` | `extends` | p1 |
| `e-conditional-class-cond` | `approximated_by` | `extends` | p1 |
| `e-impossible-marginal` | `contrasts_with` | `contradicts` | p1 |
| `e-impossible-fsc` | `motivates` | `extends` | p1 |
| `e-impossible-ssc` | `motivates` | `extends` | p1 |
| `e-impossible-aps` | `motivates` | `extends` | p1 |
| `e-aps-thm1` | `satisfies` | `guarantees` | p1 |
| `e-aps-conditional` | `approximates` | `generalizes` | p1 |
| `e-cqr-thm1` | `satisfies` | `guarantees` | p1 |
| `e-cqr-conditional` | `approximates` | `generalizes` | p1 |
| `e-cqr-group-bal` | `composable_with` | `extends` | p1 |
| `e-unc-thm1` | `satisfies` | `guarantees` | p1 |
| `e-unc-conditional` | `does_not_guarantee` | `contradicts` | p1 |
| `e-bayes-thm1` | `satisfies` | `guarantees` | p1 |
| `e-fsc-group-bal` | `evaluated_by` | `evaluates` | p1 |
| `e-fsc-class-cond` | `evaluated_by` | `evaluates` | p1 |
| `e-ssc-group-bal` | `evaluated_by` | `evaluates` | p1 |
| `e-beta-marginal` | `characterizes` | `generalizes` | p1 |
| `e-beta-thm1` | `complements` | `extends` | p1 |
| `e-beta-fsc` | `informs` | `extends` | p1 |
| `e-beta-ssc` | `informs` | `extends` | p1 |
| `e-group-bal-thm` | `guaranteed_by` | `guarantees` | p1 |
| `e-group-bal-conditional` | `achieves` | `guarantees` | p1 |
| `e-group-bal-thm-conditional` | `achieves` | `guarantees` | p1 |
| `e-group-bal-thm-class-cond` | `analogous_to` | `compares_with` | p1 |
| `e-class-cond-thm` | `guaranteed_by` | `guarantees` | p1 |
| `e-class-cond-conditional` | `achieves` | `guarantees` | p1 |
| `e-class-cond-thm-conditional` | `achieves` | `guarantees` | p1 |
| `e-crc-thm2` | `underpins` | `guarantees` | p1 |
| `e-crc-thm1` | `includes_special_case` | `generalizes` | p1 |
| `e-covshift-marginal` | `preserves` | `guarantees` | p1 |
| `e-covshift-split-cp` | `special_case_of` | `specializes` | p1 |
| `e-drift-marginal` | `approximately_preserves` | `guarantees` | p1 |
| `e-drift-beta` | `affected_by` | `depends_on` | p1 |
| `e-outlier-thm` | `guaranteed_by` | `guarantees` | p1 |

## Dangling Edges (references to nonexistent nodes)

None — all edges reference valid nodes.

## Unresolved Relations (could not map to schema type)

None.

## Duplicate Edges (same from+to+relation after normalization, deduped)

None.

## Isolated Nodes (no edge references them)

None — all nodes are connected.

## Cross-Paper Edges (connecting nodes from different sources)

| Edge ID | From | From Source | To | To Source | Relation |
|---------|------|-------------|----|-----------|----------|
| `e-crc-thm2` | `thm-conformal-risk-control` | angelopoulos2022 | `def-crc` | teneggi2025 | guarantees |
| `e-p4-03` | `def-unified-cp-framework` | min2026 | `def-conformal-coverage` | teneggi2025 | extends |
| `e-p4-04` | `thm-marginal-coverage-weighted` | min2026 | `def-conformal-coverage` | teneggi2025 | extends |
| `e-p4-08` | `thm-three-term-decomposition` | min2026 | `def-conditional-coverage` | angelopoulos2022 | extends |
| `e-p4-16` | `thm-covariate-shift-marginal` | min2026 | `def-conformal-coverage` | teneggi2025 | extends |
| `e-p4-36` | `meth-graphcp` | min2026 | `meth-sem-crc` | teneggi2025 | compares_with |
| `e-p4-37` | `meth-model-selection-cc` | min2026 | `meth-sem-crc` | teneggi2025 | compares_with |
| `e-p4-42` | `def-conditional-coverage` | angelopoulos2022 | `thm-three-term-decomposition` | min2026 | depends_on |
| `e-thm1-conformal-cov` | `thm-split-cp-coverage` | angelopoulos2022 | `def-conformal-coverage` | teneggi2025 | specializes |

## Node Type Distribution

| Type | Count |
|------|-------|
| definition | 10 |
| experiment | 4 |
| insight | 4 |
| method | 13 |
| theorem | 18 |

## Edge Relation Distribution

| Relation | Count |
|----------|-------|
| extends | 37 |
| guarantees | 26 |
| evaluates | 14 |
| compares_with | 12 |
| specializes | 12 |
| depends_on | 12 |
| generalizes | 10 |
| applies_to | 10 |
| contradicts | 2 |

## Validation Status

- [x] dag-index.json is valid JSON
- [x] All edge references point to existing nodes: True
- [x] All relation types are schema-valid: True
- [x] Relation normalization applied: 54 edges remapped
- [x] No duplicate edges: True
- [ ] Isolated nodes: 0 found
- [x] Total counts updated in meta
