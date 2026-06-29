// pipeline/delta.mjs — computeDelta 纯函数（增量 ingest 受影响集 Δ 计算）
//
// 用途：S3 合并后，diff「合并前旧 dag-index 快照」vs「合并后新 dag-index」，
// 算出本次增量新增/修改的节点与边，记入 run-manifest（可审计："本次新增 X 节点/Y 边"）。
//
// modified 用语义指纹（type/label/source/section/tokens），排除 run_id 等易变字段，
// 避免增量重跑（run_id 必变）误报 modified。
//
// 纯函数、确定性、无副作用——可独立单测（见 test-delta.mjs）。

// 节点语义指纹：只取稳定字段，忽略 run_id/generated_by_step/source_span 等易变 provenance
function fingerprint(n) {
  return JSON.stringify([n.type, n.label, n.source, n.section, n.tokens]);
}

export function computeDelta(oldDag, newDag) {
  const oldNodes = new Map((oldDag?.nodes || []).map(n => [n.id, n]));
  const oldEdgeIds = new Set((oldDag?.edges || []).map(e => e.id));

  const added_node_ids = [];
  const modified_node_ids = [];
  const added_edge_ids = [];

  for (const n of (newDag?.nodes || [])) {
    const old = oldNodes.get(n.id);
    if (!old) {
      added_node_ids.push(n.id);
    } else if (fingerprint(old) !== fingerprint(n)) {
      modified_node_ids.push(n.id);
    }
  }

  for (const e of (newDag?.edges || [])) {
    if (!oldEdgeIds.has(e.id)) {
      added_edge_ids.push(e.id);
    }
  }

  return { added_node_ids, added_edge_ids, modified_node_ids };
}
