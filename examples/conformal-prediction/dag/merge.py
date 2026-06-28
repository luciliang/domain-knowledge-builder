#!/usr/bin/env python3
"""DAG merge script: merge 3 extraction JSONs into unified dag-index.json"""

import json
import os
from collections import defaultdict

BASE = "/media/lzw/9755f264-d29f-4750-a43e-6432766bece3/openclaw/workspace-research/domain-knowledge-skill"

# Schema-defined 10 standard relation types
STANDARD_RELATIONS = {
    "guarantees", "evaluates", "generalizes", "specializes",
    "contradicts", "extends", "depends_on", "compares_with",
    "cites", "applies_to"
}

# Mapping from non-standard relations to closest standard type
RELATION_MAP = {
    # P1 non-standard → standard
    "achieves": "guarantees",
    "extends_to": "extends",
    "specializes_to": "specializes",
    "weaker_than": "compares_with",
    "characterized_by": "evaluates",
    "limited_by": "contradicts",
    "measured_by": "evaluates",
    "approximated_by": "extends",
    "contrasts_with": "compares_with",
    "motivates": "extends",
    "satisfies": "guarantees",
    "approximates": "extends",
    "composable_with": "extends",
    "does_not_guarantee": "contradicts",
    "evaluated_by": "evaluates",
    "characterizes": "evaluates",
    "complements": "compares_with",
    "informs": "extends",
    "guaranteed_by": "guarantees",
    "analogous_to": "compares_with",
    "underpins": "guarantees",
    "includes_special_case": "specializes",
    "preserved_by": "guarantees",
    "preserves": "guarantees",
    "approximately_preserves": "guarantees",
    "affected_by": "depends_on",
    "specializes": "specializes",
    "special_case_of": "specializes",
    "is_a": "specializes",
    "validates": "guarantees",
    "extended_by": "extends",
}

def normalize_relation(rel):
    if rel in STANDARD_RELATIONS:
        return rel
    if rel in RELATION_MAP:
        return RELATION_MAP[rel]
    # Fallback: closest semantic match
    print(f"  [WARN] Unknown relation type '{rel}', defaulting to 'extends'")
    return "extends"

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def merge_nodes(existing_nodes, new_nodes, report):
    """Merge nodes, detect conflicts."""
    node_map = {n['id']: n for n in existing_nodes}
    added = 0
    conflicts = []
    
    for node in new_nodes:
        nid = node['id']
        if nid not in node_map:
            node_map[nid] = node
            added += 1
        else:
            # Check for conflicts
            existing = node_map[nid]
            conflict_fields = []
            for field in ['label', 'type']:
                if existing.get(field) != node.get(field):
                    conflict_fields.append(f"{field}: '{existing.get(field)}' vs '{node.get(field)}'")
            if conflict_fields:
                conflict = {
                    'node_id': nid,
                    'existing_source': existing.get('source', 'unknown'),
                    'new_source': node.get('source', 'unknown'),
                    'differences': conflict_fields
                }
                conflicts.append(conflict)
                report['node_conflicts'].append(conflict)
    
    report['nodes_added'] += added
    report['node_conflicts_count'] += len(conflicts)
    return list(node_map.values())

def merge_edges(existing_edges, new_edges, all_node_ids, report):
    """Merge edges, normalize relation types, check references."""
    edge_map = {e['id']: e for e in existing_edges}
    added = 0
    invalid_refs = []
    normalized = []
    contradicts_pending = []
    
    for edge in new_edges:
        eid = edge['id']
        
        # Normalize relation
        original_rel = edge.get('relation', '')
        new_rel = normalize_relation(original_rel)
        if original_rel != new_rel:
            report['relations_normalized'].append({
                'edge_id': eid,
                'original': original_rel,
                'normalized': new_rel
            })
        edge['relation'] = new_rel
        
        # Check node references
        if edge['from'] not in all_node_ids:
            invalid_refs.append(f"{eid}: from='{edge['from']}' not in nodes")
        if edge['to'] not in all_node_ids:
            invalid_refs.append(f"{eid}: to='{edge['to']}' not in nodes")
        
        if eid not in edge_map:
            edge_map[eid] = edge
            added += 1
            if new_rel == 'contradicts':
                contradicts_pending.append(edge)
        else:
            # Edge ID collision - add with suffixed ID
            new_eid = f"{eid}-dup"
            edge['id'] = new_eid
            edge_map[new_eid] = edge
            added += 1
            report['edge_id_collisions'].append({
                'original_id': eid,
                'new_id': new_eid,
                'source': edge.get('source', 'unknown')
            })
    
    report['edges_added'] += added
    report['edges_invalid_refs'].extend(invalid_refs)
    report['contradicts_pending'].extend(contradicts_pending)
    return list(edge_map.values())

def find_orphan_nodes(nodes, edges):
    """Find nodes with no edges."""
    referenced = set()
    for e in edges:
        referenced.add(e['from'])
        referenced.add(e['to'])
    orphans = [n['id'] for n in nodes if n['id'] not in referenced]
    return orphans

def main():
    report = {
        'sources_merged': ['angelopoulos2022', 'teneggi2025', 'min2026'],
        'nodes_added': 0,
        'node_conflicts_count': 0,
        'node_conflicts': [],
        'edges_added': 0,
        'edges_invalid_refs': [],
        'relations_normalized': [],
        'edge_id_collisions': [],
        'contradicts_pending': [],
        'orphan_nodes': [],
        'cross_source_edges': [],
    }
    
    # Load all extraction files
    p1 = load_json(os.path.join(BASE, "extraction-p1.json"))
    p3 = load_json(os.path.join(BASE, "extraction-p3.json"))
    p4 = load_json(os.path.join(BASE, "extraction-p4.json"))
    
    all_nodes = []
    all_edges = []
    
    # Merge in order: P1 (angelopoulos2022) → P3 (teneggi2025) → P4 (min2026)
    # Phase 1: P1
    print("=== Phase 1: Merging angelopoulos2022 ===")
    print(f"  Nodes: {len(p1['nodes'])}, Edges: {len(p1['edges'])}")
    all_nodes = merge_nodes(all_nodes, p1['nodes'], report)
    all_node_ids = {n['id'] for n in all_nodes}
    all_edges = merge_edges(all_edges, p1['edges'], all_node_ids, report)
    all_node_ids = {n['id'] for n in all_nodes}  # refresh
    print(f"  After P1: {len(all_nodes)} nodes, {len(all_edges)} edges")
    
    # Phase 2: P3
    print("=== Phase 2: Merging teneggi2025 ===")
    print(f"  Nodes: {len(p3['nodes'])}, Edges: {len(p3['edges'])}")
    all_nodes = merge_nodes(all_nodes, p3['nodes'], report)
    all_node_ids = {n['id'] for n in all_nodes}
    all_edges = merge_edges(all_edges, p3['edges'], all_node_ids, report)
    all_node_ids = {n['id'] for n in all_nodes}
    print(f"  After P3: {len(all_nodes)} nodes, {len(all_edges)} edges")
    
    # Phase 3: P4
    print("=== Phase 3: Merging min2026 ===")
    print(f"  Nodes: {len(p4['nodes'])}, Edges: {len(p4['edges'])}")
    all_nodes = merge_nodes(all_nodes, p4['nodes'], report)
    all_node_ids = {n['id'] for n in all_nodes}
    all_edges = merge_edges(all_edges, p4['edges'], all_node_ids, report)
    print(f"  After P4: {len(all_nodes)} nodes, {len(all_edges)} edges")
    
    # Find orphan nodes
    orphans = find_orphan_nodes(all_nodes, all_edges)
    report['orphan_nodes'] = orphans
    print(f"  Orphan nodes: {len(orphans)}")
    for o in orphans:
        print(f"    - {o}")
    
    # Find cross-source edges (from and to from different sources)
    node_source_map = {n['id']: n.get('source', '') for n in all_nodes}
    for e in all_edges:
        from_src = node_source_map.get(e['from'], '')
        to_src = node_source_map.get(e['to'], '')
        if from_src and to_src and from_src != to_src:
            report['cross_source_edges'].append({
                'edge_id': e['id'],
                'from': e['from'],
                'to': e['to'],
                'relation': e['relation'],
                'from_source': from_src,
                'to_source': to_src
            })
    print(f"  Cross-source edges: {len(report['cross_source_edges'])}")
    
    # Final invalid refs check
    all_node_ids = {n['id'] for n in all_nodes}
    for e in all_edges:
        if e['from'] not in all_node_ids:
            if f"{e['id']}: from='{e['from']}' not in nodes" not in report['edges_invalid_refs']:
                report['edges_invalid_refs'].append(f"{e['id']}: from='{e['from']}' not in nodes")
        if e['to'] not in all_node_ids:
            if f"{e['id']}: to='{e['to']}' not in nodes" not in report['edges_invalid_refs']:
                report['edges_invalid_refs'].append(f"{e['id']}: to='{e['to']}' not in nodes")
    
    # Build dag-index.json
    dag_index = {
        "meta": {
            "domain": "统计校准与共形预测",
            "created": "2026-06-24",
            "last_updated": "2026-06-24",
            "total_nodes": len(all_nodes),
            "total_edges": len(all_edges)
        },
        "nodes": all_nodes,
        "edges": all_edges
    }
    
    # Write outputs
    dag_dir = os.path.join(BASE, "dag")
    os.makedirs(dag_dir, exist_ok=True)
    
    dag_path = os.path.join(dag_dir, "dag-index.json")
    with open(dag_path, 'w', encoding='utf-8') as f:
        json.dump(dag_index, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Written: {dag_path}")
    
    report_path = os.path.join(dag_dir, "merge-report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"✅ Written: {report_path}")
    
    # Print summary
    print("\n=== MERGE SUMMARY ===")
    print(f"Total nodes: {len(all_nodes)}")
    print(f"Total edges: {len(all_edges)}")
    print(f"Nodes added (not in P1): {report['nodes_added'] - len(p1['nodes'])}")
    print(f"Node conflicts: {report['node_conflicts_count']}")
    print(f"Relations normalized: {len(report['relations_normalized'])}")
    print(f"Edge ID collisions: {len(report['edge_id_collisions'])}")
    print(f"Invalid node refs in edges: {len(report['edges_invalid_refs'])}")
    print(f"Orphan nodes: {len(orphans)}")
    print(f"Cross-source edges: {len(report['cross_source_edges'])}")
    print(f"Contradicts edges (pending confirmation): {len(report['contradicts_pending'])}")
    
    if report['node_conflicts']:
        print("\n--- NODE CONFLICTS ---")
        for c in report['node_conflicts']:
            print(f"  ID: {c['node_id']} | {c['existing_source']} vs {c['new_source']}")
            for d in c['differences']:
                print(f"    {d}")
    
    if report['edges_invalid_refs']:
        print("\n--- INVALID EDGE REFERENCES ---")
        for r in report['edges_invalid_refs']:
            print(f"  {r}")
    
    if report['contradicts_pending']:
        print("\n--- CONTRADICTS EDGES (PENDING CONFIRMATION) ---")
        for c in report['contradicts_pending']:
            print(f"  {c['id']}: {c['from']} ↔ {c['to']} [{c['source']}]")
    
    if report['relations_normalized']:
        print("\n--- RELATION NORMALIZATIONS ---")
        for r in report['relations_normalized']:
            print(f"  {r['edge_id']}: '{r['original']}' → '{r['normalized']}'")

if __name__ == "__main__":
    main()
