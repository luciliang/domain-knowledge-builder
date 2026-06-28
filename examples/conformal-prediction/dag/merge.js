const fs = require('fs');
const path = require('path');

const BASE = '/media/lzw/9755f264-d29f-4750-a43e-6432766bece3/openclaw/workspace-research/domain-knowledge-skill';

const STANDARD_RELATIONS = new Set([
    'guarantees', 'evaluates', 'generalizes', 'specializes',
    'contradicts', 'extends', 'depends_on', 'compares_with',
    'cites', 'applies_to'
]);

const RELATION_MAP = {
    'achieves': 'guarantees',
    'extends_to': 'extends',
    'specializes_to': 'specializes',
    'weaker_than': 'compares_with',
    'characterized_by': 'evaluates',
    'limited_by': 'contradicts',
    'measured_by': 'evaluates',
    'approximated_by': 'extends',
    'contrasts_with': 'compares_with',
    'motivates': 'extends',
    'satisfies': 'guarantees',
    'approximates': 'extends',
    'composable_with': 'extends',
    'does_not_guarantee': 'contradicts',
    'evaluated_by': 'evaluates',
    'characterizes': 'evaluates',
    'complements': 'compares_with',
    'informs': 'extends',
    'guaranteed_by': 'guarantees',
    'analogous_to': 'compares_with',
    'underpins': 'guarantees',
    'includes_special_case': 'specializes',
    'preserved_by': 'guarantees',
    'preserves': 'guarantees',
    'approximately_preserves': 'guarantees',
    'affected_by': 'depends_on',
    'special_case_of': 'specializes',
    'is_a': 'specializes',
    'validates': 'guarantees',
    'extended_by': 'extends',
};

function normalizeRelation(rel) {
    if (STANDARD_RELATIONS.has(rel)) return rel;
    if (RELATION_MAP[rel]) return RELATION_MAP[rel];
    console.log(`  [WARN] Unknown relation type '${rel}', defaulting to 'extends'`);
    return 'extends';
}

const p1 = JSON.parse(fs.readFileSync(path.join(BASE, 'extraction-p1.json'), 'utf8'));
const p3 = JSON.parse(fs.readFileSync(path.join(BASE, 'extraction-p3.json'), 'utf8'));
const p4 = JSON.parse(fs.readFileSync(path.join(BASE, 'extraction-p4.json'), 'utf8'));

const report = {
    sources_merged: ['angelopoulos2022', 'teneggi2025', 'min2026'],
    nodes_added: 0,
    node_conflicts_count: 0,
    node_conflicts: [],
    edges_added: 0,
    edges_invalid_refs: [],
    relations_normalized: [],
    edge_id_collisions: [],
    contradicts_pending: [],
    orphan_nodes: [],
    cross_source_edges: []
};

let allNodes = [];
let allEdges = [];

// === MERGE NODES ===
function mergeNodes(newNodes) {
    const nodeMap = {};
    allNodes.forEach(n => nodeMap[n.id] = n);
    
    for (const node of newNodes) {
        if (!(node.id in nodeMap)) {
            nodeMap[node.id] = node;
            report.nodes_added++;
        } else {
            const existing = nodeMap[node.id];
            const diffs = [];
            for (const field of ['label', 'type']) {
                if (existing[field] !== node[field]) {
                    diffs.push(`${field}: '${existing[field]}' vs '${node[field]}'`);
                }
            }
            if (diffs.length > 0) {
                const conflict = {
                    node_id: node.id,
                    existing_source: existing.source || 'unknown',
                    new_source: node.source || 'unknown',
                    differences: diffs
                };
                report.node_conflicts.push(conflict);
                report.node_conflicts_count++;
            }
        }
    }
    allNodes = Object.values(nodeMap);
}

// === MERGE EDGES ===
function mergeEdges(newEdges) {
    const edgeMap = {};
    allEdges.forEach(e => edgeMap[e.id] = e);
    const allNodeIds = new Set(allNodes.map(n => n.id));
    
    for (let edge of newEdges) {
        const originalRel = edge.relation || '';
        const newRel = normalizeRelation(originalRel);
        if (originalRel !== newRel) {
            report.relations_normalized.push({
                edge_id: edge.id,
                original: originalRel,
                normalized: newRel
            });
        }
        edge.relation = newRel;
        
        if (!allNodeIds.has(edge.from)) {
            report.edges_invalid_refs.push(`${edge.id}: from='${edge.from}' not in nodes`);
        }
        if (!allNodeIds.has(edge.to)) {
            report.edges_invalid_refs.push(`${edge.id}: to='${edge.to}' not in nodes`);
        }
        
        if (!(edge.id in edgeMap)) {
            edgeMap[edge.id] = edge;
            report.edges_added++;
            if (newRel === 'contradicts') {
                report.contradicts_pending.push(edge);
            }
        } else {
            const newId = `${edge.id}-dup`;
            edge.id = newId;
            edgeMap[newId] = edge;
            report.edges_added++;
            report.edge_id_collisions.push({
                original_id: edge.id.replace('-dup', ''),
                new_id: newId,
                source: edge.source || 'unknown'
            });
        }
    }
    allEdges = Object.values(edgeMap);
}

// Phase 1: P1
console.log('=== Phase 1: Merging angelopoulos2022 ===');
console.log(`  Nodes: ${p1.nodes.length}, Edges: ${p1.edges.length}`);
mergeNodes(p1.nodes);
mergeEdges(p1.edges);
console.log(`  After P1: ${allNodes.length} nodes, ${allEdges.length} edges`);

// Phase 2: P3
console.log('=== Phase 2: Merging teneggi2025 ===');
console.log(`  Nodes: ${p3.nodes.length}, Edges: ${p3.edges.length}`);
mergeNodes(p3.nodes);
mergeEdges(p3.edges);
console.log(`  After P3: ${allNodes.length} nodes, ${allEdges.length} edges`);

// Phase 3: P4
console.log('=== Phase 3: Merging min2026 ===');
console.log(`  Nodes: ${p4.nodes.length}, Edges: ${p4.edges.length}`);
mergeNodes(p4.nodes);
mergeEdges(p4.edges);
console.log(`  After P4: ${allNodes.length} nodes, ${allEdges.length} edges`);

// Orphan nodes
const referenced = new Set();
allEdges.forEach(e => { referenced.add(e.from); referenced.add(e.to); });
const orphans = allNodes.filter(n => !referenced.has(n.id)).map(n => n.id);
report.orphan_nodes = orphans;
console.log(`  Orphan nodes: ${orphans.length}`);
orphans.forEach(o => console.log(`    - ${o}`));

// Cross-source edges
const nodeSourceMap = {};
allNodes.forEach(n => nodeSourceMap[n.id] = n.source || '');
allEdges.forEach(e => {
    const fs = nodeSourceMap[e.from] || '';
    const ts = nodeSourceMap[e.to] || '';
    if (fs && ts && fs !== ts) {
        report.cross_source_edges.push({
            edge_id: e.id, from: e.from, to: e.to,
            relation: e.relation, from_source: fs, to_source: ts
        });
    }
});
console.log(`  Cross-source edges: ${report.cross_source_edges.length}`);

// Final invalid refs check
const allNodeIds = new Set(allNodes.map(n => n.id));
const seenInvalidRefs = new Set();
allEdges.forEach(e => {
    if (!allNodeIds.has(e.from)) {
        const msg = `${e.id}: from='${e.from}' not in nodes`;
        if (!seenInvalidRefs.has(msg)) { report.edges_invalid_refs.push(msg); seenInvalidRefs.add(msg); }
    }
    if (!allNodeIds.has(e.to)) {
        const msg = `${e.id}: to='${e.to}' not in nodes`;
        if (!seenInvalidRefs.has(msg)) { report.edges_invalid_refs.push(msg); seenInvalidRefs.add(msg); }
    }
});

// Build dag-index.json
const dagIndex = {
    meta: {
        domain: "统计校准与共形预测",
        created: "2026-06-24",
        last_updated: "2026-06-24",
        total_nodes: allNodes.length,
        total_edges: allEdges.length
    },
    nodes: allNodes,
    edges: allEdges
};

const dagDir = path.join(BASE, 'dag');
if (!fs.existsSync(dagDir)) fs.mkdirSync(dagDir, { recursive: true });

fs.writeFileSync(path.join(dagDir, 'dag-index.json'), JSON.stringify(dagIndex, null, 2), 'utf8');
console.log(`\n✅ Written: ${path.join(dagDir, 'dag-index.json')}`);

fs.writeFileSync(path.join(dagDir, 'merge-report.json'), JSON.stringify(report, null, 2), 'utf8');
console.log(`✅ Written: ${path.join(dagDir, 'merge-report.json')}`);

// Print summary
console.log('\n=== MERGE SUMMARY ===');
console.log(`Total nodes: ${allNodes.length}`);
console.log(`Total edges: ${allEdges.length}`);
console.log(`Nodes added (beyond P1): ${report.nodes_added - p1.nodes.length}`);
console.log(`Node conflicts: ${report.node_conflicts_count}`);
console.log(`Relations normalized: ${report.relations_normalized.length}`);
console.log(`Edge ID collisions: ${report.edge_id_collisions.length}`);
console.log(`Invalid node refs in edges: ${report.edges_invalid_refs.length}`);
console.log(`Orphan nodes: ${orphans.length}`);
console.log(`Cross-source edges: ${report.cross_source_edges.length}`);
console.log(`Contradicts edges (pending): ${report.contradicts_pending.length}`);

if (report.node_conflicts.length) {
    console.log('\n--- NODE CONFLICTS ---');
    report.node_conflicts.forEach(c => {
        console.log(`  ID: ${c.node_id} | ${c.existing_source} vs ${c.new_source}`);
        c.differences.forEach(d => console.log(`    ${d}`));
    });
}
if (report.edges_invalid_refs.length) {
    console.log('\n--- INVALID EDGE REFERENCES ---');
    report.edges_invalid_refs.forEach(r => console.log(`  ${r}`));
}
if (report.contradicts_pending.length) {
    console.log('\n--- CONTRADICTS EDGES (PENDING CONFIRMATION) ---');
    report.contradicts_pending.forEach(c => console.log(`  ${c.id}: ${c.from} ↔ ${c.to} [${c.source}]`));
}
if (report.relations_normalized.length) {
    console.log('\n--- RELATION NORMALIZATIONS (first 20) ---');
    report.relations_normalized.slice(0, 20).forEach(r => console.log(`  ${r.edge_id}: '${r.original}' → '${r.normalized}'`));
    if (report.relations_normalized.length > 20) console.log(`  ... and ${report.relations_normalized.length - 20} more`);
}
