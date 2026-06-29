// run-dag-pipeline.js — domain-knowledge-builder meta-skill 的 7 步流水线编排脚本
//
// 这是 pi `workflow` tool 的执行脚本，编排 Ingest 工作流（pipeline/ingest.md）的 7 步：
//   S1 提取 → S2×N 并行知识提取 → S3 DAG 合并 → S4 导航 → S5 心智模型 → S6 验证 → S7 组装
//
// 阶段性质拆分（D3 决策）：
//   - 确定性/可并行阶段（S1/S2×N/S4）→ parallel() fan-out
//   - 交互/判断阶段（S3/S5/S6/S7）→ 顺序 agent()，S3 可 contact_supervisor 暂停
//
// 输入（通过 args 全局）：
//   args.domain — 领域名（如 "diffusion-models"）
//   args.sources — 来源论文数组 [{slug, path}]
//   args.target_skill_root — 目标知识库 skill 根目录
//   args.meta_skill_root — 本 meta-skill 根目录（读 schema/engines）
//   args.run_id — 本次构建的 UUID（外部生成，保证全 pipeline 一致）
//   args.resume_from — 可选，从某 stage 恢复（如 "S3"）
//   args.run_type — 可选，'initial'（默认，首次全量）| 'incremental'（已存在 skill 补料，S3 后算 Δ）
//
// 输出：生成的知识库 skill（target_skill_root 下完整的 wiki/dag/schema/SKILL.md）

import { readFileSync } from 'node:fs';
import { computeDelta } from './delta.mjs';

export const meta = {
  name: 'domain-knowledge-dag-pipeline',
  description: 'domain-knowledge-builder 的 7 步 Ingest 流水线编排（确定性 parallel + 交互 subagent 混合）',
  phases: [
    { title: 'S1: 文本提取' },
    { title: 'S2: 并行知识提取' },
    { title: 'S3: DAG 合并（交互）' },
    { title: 'S4: 导航文件' },
    { title: 'S5: 心智模型' },
    { title: 'S6: 独立验证' },
    { title: 'S7: SKILL.md 组装' },
    { title: 'darwin 质量门' }
  ]
}

// ========== 工具函数 ==========

function stagePrompt(stage, instruction) {
  // 给每个 stage agent 的公共上下文
  return [
    `你是 domain-knowledge-builder pipeline 的 ${stage} 阶段执行 agent。`,
    ``,
    `**全局上下文**：`,
    `- 领域: ${args.domain}`,
    `- meta-skill 根目录: ${args.meta_skill_root}（读 schema/engines 用）`,
    `- 目标知识库根目录: ${args.target_skill_root}（写产物用）`,
    `- run_id: ${args.run_id}`,
    ``,
    `**规范文件**（按需读）：`,
    `- ${args.meta_skill_root}/schema/schema.md（节点模板/关系类型/Determinism/Provenance）`,
    `- ${args.meta_skill_root}/pipeline/ingest.md（本 stage 的详细契约）`,
    `- ${args.meta_skill_root}/engines/nuwa-validation.md（S5 用）`,
    `- ${args.meta_skill_root}/engines/darwin-rubric.md（质量门用）`,
    ``,
    `**D7 Provenance 要求**（schema §11，所有新节点必填）：`,
    `- generated_by_step: "${stage}"`,
    `- run_id: ${args.run_id}`,
    `- source_span: {file, start_line, end_line, page}`,
    ``,
    `**本 stage 任务**：`,
    instruction
  ].join('\n')
}

function recordStage(stage, status, extra) {
  // 记录到 run-manifest.json（通过 agent 执行 bash）
  // extra 可含 commit/artifacts/note
  return stagePrompt(stage + '_record', `更新 ${args.target_skill_root}/pipeline/state/run-manifest.json：append ${JSON.stringify({stage, status, ...extra})} 到 stages 数组。若 status=done 则 git commit（message: "${stage}: ${extra.note || ''}"）。`)
}

// ========== S1: 文本提取（确定性，单 agent） ==========

async function S1_extract() {
  phase('S1: 文本提取')
  log(`S1 开始：提取 ${args.sources.length} 个来源的文本`)

  const result = await agent(
    stagePrompt('S1', [
      `1. preflight: cd ${args.meta_skill_root} && python3 -m engines.book_to_skill --check`,
      `   - docling 不可用 → 报错终止（schema §12.4，不静默退化）`,
      `2. 提取: python3 -m engines.book_to_skill ${args.sources.map(s => s.path).join(' ')} --mode technical --install-missing ask`,
      `3. 把 <tempdir>/book_skill_work/{full_text.txt, metadata.json} 复制到 ${args.target_skill_root}/`,
      `4. REPL 探测（如 full_text.txt > 50K tokens）：grep -n -E "^(Chapter|Section|Theorem)" 定位章节，记录章节偏移到 metadata.json 的 sections 字段`,
      `5. 记录 S1 到 run-manifest.json + git commit`,
      ``,
      `返回: {full_text_path, total_tokens, sources_meta, preflight_ok}`
    ].join('\n')),
    { label: 'S1 提取', tier: 'medium' }
  )

  log(`S1 完成: ${result}`)
  return result
}

// ========== S2: 并行知识提取（fan-out per source） ==========

async function S2_extractParallel(s1Result) {
  phase('S2: 并行知识提取')
  log(`S2 开始：并行提取 ${args.sources.length} 个来源的知识节点`)

  // parallel() 要求函数数组，不是 promise 数组
  const extractTasks = args.sources.map(src => () => agent(
    stagePrompt('S2_' + src.slug, [
      `提取来源 **${src.slug}** 的知识节点。`,
      ``,
      `1. 读 ${args.meta_skill_root}/schema/schema.md 的 §2 节点模板 + §3 关系类型 + §10 Determinism`,
      `2. 用 REPL 探测定位 ${src.slug} 在 ${args.target_skill_root}/full-text.txt 的内容（grep 章节标题 → sed 按段读，禁止全读）`,
      `3. 按节点模板提取知识节点（def/thm/meth/exp/ins），写入 ${args.target_skill_root}/wiki/knowledge/*.md：`,
      `   - 定理表述原文精确（LaTeX 保留）`,
      `   - 节点 ID = <type>-${src.slug}-<canonical-term>（schema §10 幂等）`,
      `   - 必填 provenance: generated_by_step=S2, run_id=${args.run_id}, source_span`,
      `   - 每节点 500-2000 tokens`,
      `4. 同时输出 ${args.target_skill_root}/extraction-${src.slug}.json（nodes + edges 数组）`,
      `5. 写 ${args.target_skill_root}/wiki/sources/${src.slug}.md（来源摘要，schema §5）`,
      `6. 跨源一致性：若 ${src.slug} 谈的概念在其他来源已有节点，用同 node ID（schema §10）`,
      ``,
      `返回: {nodes_count, edges_count, extraction_json, source_md}`
    ].join('\n')),
    { label: 'S2_' + src.slug, tier: 'medium' }
  ))

  const results = await parallel(extractTasks)
  log(`S2 完成: ${results.length} 个来源并行提取完`)

  // 记录每个 source 的 S2 完成
  await agent(stagePrompt('S2_record', `记录所有 S2_<source> 到 run-manifest.json + 各自 git commit`), { label: 'S2 记录', tier: 'small' })

  return results
}

// ========== S3: DAG 合并（交互式，可 contact_supervisor） ==========

async function S3_mergeDAG(s2Results) {
  phase('S3: DAG 合并（交互）')
  log('S3 开始：合并各 extraction-*.json 到 dag-index.json（遇 contradicts 暂停确认）')

  const result = await agent(
    stagePrompt('S3', [
      `合并 ${args.sources.length} 个来源的 extraction 到统一 DAG。`,
      ``,
      `1. 读 ${args.meta_skill_root}/schema/schema.md §3 关系规范 + §4 dag-index 结构`,
      `2. 读所有 ${args.target_skill_root}/extraction-*.json`,
      `3. 读现有 ${args.target_skill_root}/dag/dag-index.json（若存在，增量合并；不存在则新建）`,
      `4. 合并规则（schema §6 Step 3）：`,
      `   - 新节点 → 追加`,
      `   - 同 ID 节点 → token-level 比对：一致跳过（幂等），不一致标注冲突`,
      `   - 新关系 → 追加`,
      `   - **contradicts / does_not_guarantee 关系 → 必须 contact_supervisor(reason:"need_decision") 请用户确认**`,
      `5. 输出 ${args.target_skill_root}/dag/dag-index.json（meta.run_id=${args.run_id}）`,
      `6. 输出 ${args.target_skill_root}/dag/merge-report.md（新增/冲突/人工确认记录）`,
      `7. 程序化校验：0 断裂/0 重复/0 孤立（schema §8）`,
      ``,
      `返回: {total_nodes, total_edges, conflicts_resolved, human_confirmations}`
    ].join('\n')),
    { label: 'S3 合并', tier: 'big' }  // big tier：合并需要全局视角 + 判断
  )

  log(`S3 完成: ${result}`)
  return result
}

// ========== S4: 导航文件（确定性，可并行 3 个） ==========

async function S4_navigation(s3Result) {
  phase('S4: 导航文件')
  log('S4 开始：生成 index/log/overview')

  const navTasks = [
    () => agent(stagePrompt('S4_index', `基于 ${args.target_skill_root}/dag/dag-index.json 生成 ${args.target_skill_root}/wiki/index.md：按 def/thm/meth/exp/ins 分组，每节点一行（ID + 链接 + 一句话摘要）`), { label: 'S4 index', tier: 'small' }),
    () => agent(stagePrompt('S4_log', `追加 ${args.target_skill_root}/wiki/log.md：本次 ingest 摘要（日期/来源/新增节点数/总节点数/darwin 分数占位）`), { label: 'S4 log', tier: 'small' }),
    () => agent(stagePrompt('S4_overview', `生成 ${args.target_skill_root}/wiki/overview.md：领域全局概览（3-5 段，基于 dag-index 的 meta + sources）`), { label: 'S4 overview', tier: 'medium' })
  ]

  await parallel(navTasks)
  log('S4 完成: index/log/overview 三个导航文件生成')
}

// ========== S5: 心智模型（判断式） ==========

async function S5_mentalModels(s3Result) {
  phase('S5: 心智模型')
  log('S5 开始：三重验证提炼心智模型')

  const result = await agent(
    stagePrompt('S5', [
      `用领域化三重验证提炼心智模型。`,
      ``,
      `1. 读 ${args.meta_skill_root}/engines/nuwa-validation.md（领域化三重验证方法论）`,
      `2. 读所有 ${args.target_skill_root}/wiki/knowledge/*.md 和 wiki/sources/*.md`,
      `3. 识别候选镜片（反复出现的思维框架）`,
      `4. 三重验证每个候选：跨场景复现(≥2 子问题) / 生成力 / 领域排他性`,
      `5. 分级：3 重全过→心智模型；1-2 重→决策启发式；0 重→丢弃`,
      `6. 产出 3-7 个心智模型 + 5-10 条决策启发式`,
      `7. 写 ${args.target_skill_root}/wiki/mental-models.md（每模型附跨源证据 + 应用场景 + 局限）`,
      `8. 诚实边界：未覆盖子领域 / 单一来源结论 / 开放问题`,
      ``,
      `返回: {mental_models_count, heuristics_count, dropped_candidates}`
    ].join('\n')),
    { label: 'S5 心智模型', tier: 'big' }
  )

  log(`S5 完成: ${result}`)
  return result
}

// ========== S6: 独立验证（fresh-context） ==========

async function S6_validate(s5Result) {
  phase('S6: 独立验证')
  log('S6 开始：fresh-context 子 agent 独立验证（不看构建过程）')

  const result = await agent(
    stagePrompt('S6', [
      `你是 fresh-context 独立验证 agent。**不要假设构建正确，从零验证产物**。`,
      ``,
      `1. 读 ${args.target_skill_root}/dag/dag-index.json，程序化校验：`,
      `   - 0 断裂引用（edges 的 from/to 全在 nodes）`,
      `   - 0 重复 node/edge ID`,
      `   - 0 孤立节点`,
      `   - meta 计数一致（total_nodes/edges + sources[].nodes/edges）`,
      `2. 随机抽 3 节点：用 source_span 定位原文，验证定理表述一致 + LaTeX 正确 + schema 合规`,
      `3. 检查关系方向（from→to 语义正确）`,
      `4. 检查 wiki/index.md 与 dag-index 一致`,
      `5. 走一个测试查询，验证 Query 工作流（schema §7）能否找到答案`,
      `6. **D7 Provenance 校验**：新节点（非 [legacy]）全含 generated_by_step/run_id/source_span？run_id=${args.run_id}？`,
      `7. 输出 ${args.target_skill_root}/dag/validation-report.md`,
      ``,
      `返回: {structural_ok, content_ok, provenance_ok, query_test_ok, issues:[...]}`
    ].join('\n')),
    { label: 'S6 验证', tier: 'big', context: 'fresh' }  // fresh context：不继承构建历史
  )

  log(`S6 完成: ${result}`)
  if (result && result.includes('issues') && !result.includes('issues:[]')) {
    log(`S6 发现问题，可能需要回退修复`)
  }
  return result
}

// ========== S7: SKILL.md 组装 ==========

async function S7_assembleSkill(s6Result) {
  phase('S7: SKILL.md 组装')
  log('S7 开始：组装最终知识库 skill 入口')

  const result = await agent(
    stagePrompt('S7', [
      `组装 ${args.target_skill_root}/SKILL.md（<4K tokens，compaction 从末尾截断所以重要内容前置）。`,
      ``,
      `结构：`,
      `1. frontmatter: name=${args.domain}, description（foreground 领域名 + 查询语义）`,
      `2. 核心心智模型（<2K tokens，从 wiki/mental-models.md 提炼）`,
      `3. 查询协议（5 步精简版，schema §7）`,
      `4. 知识节点索引表（从 dag-index.json 按 def/thm/meth/exp/ins 分组）`,
      `5. 术语映射（中英对照）`,
      `6. 诚实边界（已覆盖/未覆盖/争议）`,
      ``,
      `约束：SKILL.md body <4K tokens。`,
      `返回: {skill_md_path, token_count}`
    ].join('\n')),
    { label: 'S7 组装', tier: 'medium' }
  )

  log(`S7 完成: ${result}`)
  return result
}

// ========== darwin 质量门 ==========

async function darwinGate(s7Result) {
  phase('darwin 质量门')
  log('darwin 质量门：fresh-context 9 维评分（第 9 维 generator-skill 子类）')

  const result = await agent(
    stagePrompt('darwin', [
      `你是 darwin 2.0 独立评分 agent。加载 ${args.meta_skill_root}/engines/darwin-rubric.md。`,
      ``,
      `对生成的 ${args.domain} 知识库 skill 做 9 维评分：`,
      `- ①②③④⑤⑥⑦⑧ 结构/清晰/完整/可操作/准确/一致/效率/鲁棒`,
      `- ⑨ 元技能合规：本 skill 是 generator-skill 产物，按 §2.3 四支柱评（可回滚/可审计/确定性/预检）`,
      `- fresh-context（不继承构建历史，避免自评偏差）`,
      ``,
      `返回 9 维表 + 总分 + 等级（A+95+/A90+/A-85+/B+80+/B75+）+ 是否过门（≥B+）`,
      `写入 ${args.target_skill_root}/results.tsv 一行`
    ].join('\n')),
    { label: 'darwin 评分', tier: 'big', context: 'fresh' }
  )

  log(`darwin 评分结果: ${result}`)
  return result
}

// ========== 主流程（按依赖顺序，支持 resume） ==========

async function main() {
  log(`=== domain-knowledge-builder pipeline 启动 ===`)
  log(`领域: ${args.domain} | 来源数: ${args.sources.length} | run_id: ${args.run_id}`)
  log(`target: ${args.target_skill_root}`)

  // resume_from 支持：跳过已 done 的 stage
  const resumeFrom = args.resume_from // 如 "S3" 表示从 S3 开始（S1/S2 已 done）
  const stages = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'darwin']
  const startIdx = resumeFrom ? stages.indexOf(resumeFrom) : 0
  if (resumeFrom && startIdx < 0) {
    throw new Error(`无效 resume_from: ${resumeFrom}，应为 ${stages.join('/')}`)
  }

  let s1r, s2r, s3r, s4r, s5r, s6r, s7r, darwinR

  // incremental 模式：S3 前读现有 dag-index 快照（S3 后算 Δ 用）
  let snapshot = null
  if (args.run_type === 'incremental' && startIdx <= 2) {
    try {
      snapshot = JSON.parse(readFileSync(`${args.target_skill_root}/dag/dag-index.json`, 'utf8'))
      log(`incremental 模式：快照 ${snapshot.nodes?.length || 0} 节点 / ${snapshot.edges?.length || 0} 边`)
    } catch {
      log(`incremental 模式但无现有 dag-index，按 initial 处理`)
    }
  }

  if (startIdx <= 0) { s1r = await S1_extract() }
  if (startIdx <= 1) { s2r = await S2_extractParallel(s1r) }
  if (startIdx <= 2) { s3r = await S3_mergeDAG(s2r) }

  // S3 后算增量 Δ（新增/修改节点与边），log 供审计（computeDelta 见 pipeline/delta.mjs）
  if (snapshot) {
    try {
      const newDag = JSON.parse(readFileSync(`${args.target_skill_root}/dag/dag-index.json`, 'utf8'))
      const delta = computeDelta(snapshot, newDag)
      log(`增量 Δ: +${delta.added_node_ids.length} 节点 / +${delta.added_edge_ids.length} 边 / ${delta.modified_node_ids.length} 修改`)
    } catch (e) {
      log(`增量 Δ 计算失败（忽略，不阻塞 pipeline）: ${e}`)
    }
  }
  if (startIdx <= 3) { s4r = await S4_navigation(s3r) }
  if (startIdx <= 4) { s5r = await S5_mentalModels(s3r) }
  if (startIdx <= 5) { s6r = await S6_validate(s5r) }
  if (startIdx <= 6) { s7r = await S7_assembleSkill(s6r) }
  if (startIdx <= 7) { darwinR = await darwinGate(s7r) }

  // 棘轮机制：darwin < B+ 则 git revert 最后 stage（由 darwin agent 报告分数后外部决定）
  log(`=== pipeline 完成 ===`)
  log(`最终 darwin 评分: ${darwinR}`)

  return {
    ok: true,
    domain: args.domain,
    run_id: args.run_id,
    target_skill_root: args.target_skill_root,
    darwin_result: darwinR,
    stages_completed: stages.slice(0, Math.max(startIdx, stages.length))
  }
}

main().catch(err => {
  log(`pipeline 失败: ${err}`)
  return { ok: false, error: String(err), run_id: args.run_id }
})
