// pipeline/test-delta.mjs — computeDelta 纯函数单测（node:test）
// 跑：node --test pipeline/test-delta.mjs
import test from 'node:test';
import assert from 'node:assert';
import { computeDelta } from './delta.mjs';

test('computeDelta: 新节点 → added_node_ids', () => {
  const old = { nodes: [{ id: 'a', type: 'def', label: 'A' }], edges: [] };
  const neu = { nodes: [{ id: 'a', type: 'def', label: 'A' }, { id: 'b', type: 'thm', label: 'B' }], edges: [] };
  const d = computeDelta(old, neu);
  assert.deepEqual(d.added_node_ids, ['b']);
  assert.deepEqual(d.modified_node_ids, []);
});

test('computeDelta: 新边 → added_edge_ids', () => {
  const old = { nodes: [], edges: [{ id: 'a|r|b', from: 'a', relation: 'r', to: 'b' }] };
  const neu = { nodes: [], edges: [
    { id: 'a|r|b', from: 'a', relation: 'r', to: 'b' },
    { id: 'a|r|c', from: 'a', relation: 'r', to: 'c' },
  ] };
  const d = computeDelta(old, neu);
  assert.deepEqual(d.added_edge_ids, ['a|r|c']);
});

test('computeDelta: 无变化 → 空 Δ（幂等，old===new）', () => {
  const dag = { nodes: [{ id: 'a', type: 'def', label: 'A' }], edges: [{ id: 'a|r|b' }] };
  const d = computeDelta(dag, dag);
  assert.deepEqual(d.added_node_ids, []);
  assert.deepEqual(d.added_edge_ids, []);
  assert.deepEqual(d.modified_node_ids, []);
});

test('computeDelta: 同 id 语义变 → modified_node_ids（忽略 run_id 等易变字段）', () => {
  // label 变（语义变）→ modified；run_id 变（易变）→ 不报 modified
  const old = { nodes: [{ id: 'a', type: 'def', label: 'old-label', run_id: 'R1' }], edges: [] };
  const neu = { nodes: [{ id: 'a', type: 'def', label: 'new-label', run_id: 'R2' }], edges: [] };
  const d = computeDelta(old, neu);
  assert.deepEqual(d.added_node_ids, []);
  assert.deepEqual(d.modified_node_ids, ['a']);  // label 变 → modified
});

test('computeDelta: 仅 run_id 变（语义不变）→ 不报 modified', () => {
  const old = { nodes: [{ id: 'a', type: 'def', label: 'A', run_id: 'R1' }], edges: [] };
  const neu = { nodes: [{ id: 'a', type: 'def', label: 'A', run_id: 'R2' }], edges: [] };
  const d = computeDelta(old, neu);
  assert.deepEqual(d.modified_node_ids, []);  // 语义指纹同，增量重跑不误报
});
