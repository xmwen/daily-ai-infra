# -*- coding: utf-8 -*-
"""
2026-05-26 curated 一次性构建脚本。
读取 cache/today_raw.json，按筛选偏好写中文 tldr + domain_tag，
输出 cache/today_curated.json。

中文 tldr ≤200 字，强调词用「」避开 Python 字符串闭合坑。
domain_tag ∈ {推理, 训练, agent}。
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "cache" / "today_raw.json"
OUT_PATH = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))

# (link 子串, tldr, domain_tag) —— 用 link 子串匹配以兼容 v1/v2 replace
CURATED_RULES = [
    # ===== papers =====
    (
        "2605.24022",
        "长上下文 LLM 推理 TTFT 已成核心瓶颈，传统 prefix caching 仅适用严格前缀场景，非前缀场景直接复用 KV 会破坏跨 chunk 全局 attention。本文提出 Adaptive KV Cache Reuse，结合「语义一致性恢复」与异构存储层 I/O 调度，在非前缀场景重用 KV 同时保住生成质量；对长上下文 serving prefill 加速是直接答卷。",
        "推理",
    ),
    (
        "2605.24220",
        "Polar 给「任意 agent harness」做大规模异步 RL rollout——把 harness 当黑盒，代理 LLM API 调用、记录 token 级模型交互、重建 token-faithful 轨迹用于训练；rollout 节点并行 prewarming/执行/重建/评估，asynchronous 服务端点。覆盖 Claude Code/Codex/Qwen 等真实 coding agent harness 直接用 GRPO 训，agent infra 与训练栈打通的关键工程节点。",
        "agent",
    ),
    (
        "2605.23911",
        "TritonMoE：纯 OpenAI Triton 写完整 MoE forward（router scoring + token permutation + expert GEMM + 加权 combine），不锁 NVIDIA。关键优化是 fused gate+up GEMM——共享 L2-cached 输入 tile 同时算两路 SwiGLU + 寄存器内 SiLU，砍 35% 全局内存读。MI300X/TPU 等异构硬件上跨平台 expert routing 首作，对国产芯片接 MoE 推理有直接参考价值。",
        "推理",
    ),
    (
        "2603.22774",
        "Multi-GPU LLM 推理被 CPU 拖慢——并非 GPU 饱和，而是 CPU 没喂饱：kernel launch 延迟、通信 stall、tokenization 慢，即便用 process 隔离 + CUDA Graph 仍救不回。文章系统化拆解 multi-GPU serving CPU 路径瓶颈，对 PD 分离/大 batch 调度场景给「CPU side budget」一等公民提示。",
        "推理",
    ),
    (
        "2605.24832",
        "Optimus 给 diffusion LLM (DLLM) serving 做弹性解码——固定 block size diffusion decoding 在低 load 大 block 抢资源、高 load 早饱和导致冗余算。Optimus 动态调整 decoding granularity 适配实时 workload，使 throughput 在饱和后仍可生长。DLLM 推理调度从 AR 范式独立分化的工程化答卷。",
        "推理",
    ),
    (
        "2605.24168",
        "Position paper：长上下文 + agent 化 workload 下，attention 的 dense 假设是不必要的人为约束；O(N) attention 信息其实可投影进 hidden state，未来 LLM 推理应走「极致但有原则」的 context 维度稀疏。论文给经验+理论双线证据，呼吁推理引擎把稀疏 attention 升一等公民——对位最近 SpecSA/SSV/AB-Sparse/Range-Search KV 母题。",
        "推理",
    ),
    (
        "2605.23918",
        "首次跨架构（H100 HBM3 / A100 HBM2e / L40S GDDR6）实测 idle GPU 功耗 vs VRAM 占用——18 天 33 万样本 + 三机 dose-response。结论：idle 功耗在 VRAM 上分段恒定，CUDA context 强制离散 DVFS 跳变；常驻 GPU 模型为避冷启动付的「停车税」可量化、可优化。对推理集群多模型常驻策略与 SLO/能耗权衡是基础数据。",
        "推理",
    ),
    (
        "2605.25475",
        "IndexMem 给长上下文 KV cache eviction 加「learnable indexer」——预测 token 重要性比启发式 H2O/SnapKV 更准，配合「轻量 latent memory」可逆补偿被 evict token 信息，避免不可逆遗忘。延续 5/19 OSCAR/VeriCache、5/11 ThinKV 等学习型 KV 管理母题，KV eviction 从「打分启发」走向「学习+记忆」。",
        "推理",
    ),
    (
        "2605.24259",
        "Resident KV Claims 给 KV cache reuse 定义「一致性合约」——把 priority/duration/offload/routing hints/scheduler mode/event stream 等机制收敛为 future-reuse intent 的形式化承诺，附 lifecycle 状态机+可行性判定+telemetry。vLLM allocator 实测：60-block resident claim + 70-block active prefill 在 80-block 池下，用 write-no-admit 防止 active 污染未来可重用状态。是 KV 池治理走向「契约化」的关键一步。",
        "推理",
    ),
    (
        "2605.24144",
        "EVA 给 LLM decode VQ 推理建专用加速器——decode 是 memory-bound 小 GEMV，weight-only VQ 压到 2bit 仍卡在 GEMV 利用率低 + codebook 检索带宽。架构层面对 VQ 重新设计 dataflow + codebook 局部缓存，让 2bit 权重压缩在硬件上真的把带宽红利落到延迟。位列 RaBitQ/TurboQuant/PolarQuant/OCTOPUS 旋转预条件 codec 母题硬件答卷。",
        "推理",
    ),
    (
        "2605.24391",
        "MX-SAFE：在 OCP MX 标准上做「on-the-fly 指数+尾数位分配」的可变精度 microscaling 格式，统一覆盖 MXINT（高精度）与 MXFP（宽 dynamic range）两类需求。训练+推理双场景通用，FP8/MXFP8/MXFP4 量化栈的下一代格式候选。Blackwell/MXFP8 attention/Adam 已在落，格式设计的灵活度直接决定下一代芯片利用率。",
        "推理",
    ),
    (
        "2605.25522",
        "Co-design：把 graph-based ANNS（10亿规模）落到 PIM——graph traversal 是 memory-bound + 不规则访存，CPU 卡内带宽、GPU HBM 装不下。PIM 把计算放数据旁解锁内带宽，但 PU 本地内存小+跨 PU 通信贵。论文系统化解决这些 PIM 失配。对位用户 RaBitQ/向量检索方向，10 亿向量 PIM ANNS 是 KV cache 检索/RAG 索引的下一站候选硬件。",
        "推理",
    ),
    (
        "2605.24461",
        "首篇端到端公开 100MW+ AI 集群电源管理——150MW 数据中心承载 83K GB200 GPU，从加速器 GA 前 6-12 月的电源容量规划，到大规模部署后调参，再到 runtime 动态电源管理。含详细功耗实测；对国内 GB200/超大集群的电源-散热-工程时间线规划是稀缺一手数据。",
        "训练",
    ),
    (
        "2605.24006",
        "用「表格化 schedule 抽象」统一对比 pipeline parallel 训练调度——把 GPipe/1F1B/Chimera/Hanayo 在 communication-aware 仿真下跨多硬件配置评估。结论：schedule 排名不是抽象不变量，会随系统配置变化。给 Megatron/Megatron-LM 选 PP 调度提供可控可比的方法学，避开「公式 bubble ratio」与「整套实测」之间的成本鸿沟。",
        "训练",
    ),
    (
        "2605.25247",
        "Kavier：cache-aware 离散事件仿真器，建 LLM 生态 digital twin。提出 LLM ecosystem reference architecture 概念模型，覆盖性能/可持续性/经济。延续 5/13 GRIEF / 5/19 Hawkeye / 5/20 Silent Hyperparameter / 5/22 Dooly 推理后端复现性母题，把仿真器升级为「设计阶段一等决策工具」。",
        "推理",
    ),
    (
        "2605.25798",
        "DiSC：分辨率可扩展、稀疏感知的 diffusion model 加速器——用「Cached Token Reuse」消除 step 间空间冗余 token、「Softmax Thresholding + Sparsity Mask Reuse」复用 sparsity pattern 在 attention 上诱导稀疏。Transformer-based diffusion 高分辨率 H100 推理场景，把稀疏从 LLM 母题外溢到生成模型架构。",
        "推理",
    ),
    # ===== code =====
    (
        "TensorRT-LLM/releases/tag/v1.3.0rc16",
        "TRT-LLM v1.3.0rc16 大批量更新——Gemma4 多模态（vision+audio）/ Qwen3.5 MTP / Qwen3.6-27B-FP8 / EXAONE-4.5 / Laguna 模型支持；DeepSeek/NemotronH/Qwen3/Qwen3.5-MoE 切到 sharding-IR canonical 模型；KV cache 侧加「精确多模态 KV block hashing + reuse probing」、「KV cache manager v2 + Python transceiver」、「disaggregated serving + block reuse」。多模态 + MTP + 解耦 serving 三轴同推。",
        "推理",
    ),
    (
        "flashinfer/releases/tag/v0.6.12rc1",
        "FlashInfer v0.6.12rc1：MoE GEMM 优化 + per-token nvfp4 量化 kernel 提速、SM120 W4A16 b12x MoE kernel、TRTLLM-GEN GQA 动态 tokens-per-page、Kimi K2.5 H64 CuTe DSL MLA decode、CUTLASS MLA paged attention FP8 输出、sccache JIT cache 构建加速。Blackwell+Kimi K2.5+CUTLASS DSL 三线持续推进，是 v0.21 时代的核心 attention/MoE 引擎滚动。",
        "推理",
    ),
    (
        "tilelang/releases/tag/v0.1.10",
        "TileLang v0.1.10 跨栈大爆发：AMD RDNA3/RDNA3.5 WMMA、gfx950/CDNA4 copy.async、160K LDS、INT8 MFMA、MXFP4 E2M1、RDNA gfx1151；CUDA/Blackwell MXFP8 block-scaled GEMM、FP4 TensorMap TMA、TMA gather4/scatter4、SM-to-SM cluster copy；SM75 native MMA（FP16/INT8/INT4）；Metal simdgroup_matrix MMA；T.tfloat32 + TCGEN5 F8/F6/F4。tile DSL 真正完成「NVIDIA + AMD + Apple + 老卡」一统，与 Triton/CUTLASS DSL 的下一代 tile-level 编程入口竞争白热化。",
        "推理",
    ),
    (
        "openai-agents-python/releases/tag/v0.17.4",
        "OpenAI Agents v0.17.4：Realtime 自定义 voice 对象支持、function tool 缺失时 opt-in 恢复（修 #3459）、MCP SSE transport 强制 hardened http client 默认值、FunctionSpanData 输出非 None、tracing 函数/类型对外导出（MCPListToolsItem/ToolSearchCallItem/ToolSearchOutputItem）、ModelBehaviorError 中无效 JSON payload 自动 redact。延续 v0.17.x 「sandbox + tracing + MCP 安全边界补漏期」节奏。",
        "agent",
    ),
    # ===== community =====
    (
        "vllm.ai/blog/2026-05-26-eagle-3-1",
        "EAGLE 3.1：EAGLE 团队 × vLLM × TorchSpec 三方合作，把 EAGLE-3 投机解码继续推进到 vLLM 主线生产路径。延续 5/12 SPECTRE → 5/14 PipeSD → 5/15 ECHO → 5/20 SpecSA → 5/24 SSV 投机解码母题，给 vLLM v0.21 时代 spec decode 标准化与 Eagle/EAGLE-3 串接。",
        "推理",
    ),
    (
        "dottxt-ai.github.io/outlines",
        "Outlines 文档站重写——结构化 LLM 输出从早期 regex/CFG 框架发展到完整 provider 适配 + JSON schema/grammar 直连推理引擎。HN 重提说明 constrained decoding 已成 LLM serving 标准能力（XGrammar/Outlines/lm-format-enforcer 三足），与 5/9 NVIDIA SLM Bash + 5/19 OpenAI Agents tool grammar 等结构化输出母题对位。",
        "agent",
    ),
    (
        "antirez.com/news/167",
        "antirez（Redis 作者）DwarfStar 项目首发分布式 LLM inference——继 5/10 DS4 单卡 V4-Flash 后，把 inference 工程进一步外推到「分布式 hobbyist 栈」。HN 同日多次置顶（含 vLLM 自家文章并列），社区视为 V4-Pro/V4-Flash 之外第三类工程化路径。",
        "推理",
    ),
    (
        "PacktPublishing/Operational-AI-with-Docker",
        "Operational AI with Docker：multi-agent LLM orchestration via Docker Compose + MCP——把多 agent 编排下沉到容器编排原语，MCP server 作 sidecar，用 docker-compose 管 agent 拓扑+资源隔离+生命周期。延续 5/24 llama.cpp --tools 内嵌+vmagents firejail 沙箱母题，agent runtime「容器化」工程范式落地。",
        "agent",
    ),
    (
        "1tnfxsc",
        "Spice：开源「agent decision layer」——不替代 Claude Code/Codex/Hermes 等执行 agent，而是在执行之前做「该做什么+为什么」的决策层。把 agent 从执行层往上抽出 plan/decide 一层独立服务，与 5/24 CodeGraph（retrieval substrate）/ Fleet（并发管理）/ llama.cpp --tools（serving 嵌 tool）拼成 coding agent infra 三层 stack 之上的第四层。",
        "agent",
    ),
    (
        "1to1mey",
        "SkillOpt：把 markdown skill 文件当可训练参数——frontier model 提议有界编辑（add/delete/replace），用 held-out 验证集严格 gating，仅严格改进接受。最佳 skill 在 1-4 次 edit 后收敛，预算 4-8/step 最优；Codex 上优化的 skill 零修改迁到 Claude Code 在 SpreadsheetBench 涨 +59.7。把 agent skill 工程化为可优化产物，对位 NVIDIA Verified Skills + Anthropic skill 系统。",
        "agent",
    ),
    (
        "1to00xl",
        "Strix Halo（gfx1151）用户：被 ggml-org 拒掉的 PR #21344 给 MoE PP 提速 30%+——改动极小，可手动 patch 进当前 llama.cpp release。低 ctx 下增益最大，ctx 升高增益衰减。AMD APU 统一内存 MoE 推理工程化继续——继 5/2 MiniMax M2.7 Strix Halo + 5/20 GH200/GB200 NVLink-C2C 后，统一内存 ScaleUp 路线再添一条社区独立验证。",
        "推理",
    ),
    (
        "1to0qpb",
        "Qwen3.6 27B 在单卡 RTX 5090 + 辅卡 RTX4000 做 AR→Diffusion realignment head 训练（基于 open-dllm）——nvfp4 + qlora 形态把 27B 模型本地训练塞进 5090 32GB（原本需 600GB）。虽未训完且烧了一根 GPU 线，但给社区「nvfp4 + qlora」单卡级训练 frontier 模型的可行性 datapoint，延续 5/16 Open-dLLM × Qwen3.6 5090 探路工作。",
        "训练",
    ),
]

# 建立 link → (tldr, tag) 映射；按子串匹配
def find_rule(link: str):
    for sub, tldr, tag in CURATED_RULES:
        if sub in link:
            return tldr, tag
    return None

curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}

# 跨 section 去重（按 link）
seen_links: set[str] = set()

for sec_name, items in raw["sections"].items():
    for item in items:
        link = item.get("link", "")
        if link in seen_links:
            continue
        rule = find_rule(link)
        if rule is None:
            continue
        tldr, tag = rule
        seen_links.add(link)
        new_item = dict(item)
        new_item["tldr"] = tldr
        new_item["domain_tag"] = tag
        curated_sections[sec_name].append(new_item)

now_utc = datetime.now(timezone.utc).isoformat()

curated = {
    "generated_at": now_utc,
    "lookback_hours": raw.get("lookback_hours", 36),
    "source": "agent_curated",
    "sections": curated_sections,
}

OUT_PATH.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
total = sum(len(v) for v in curated_sections.values())
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for items in curated_sections.values():
    for it in items:
        tag_count[it["domain_tag"]] += 1

print(f"curated total: {total}")
for sec, items in curated_sections.items():
    print(f"  {sec}: {len(items)}")
print(f"domain_tag: {tag_count}")
print(f"generated_at: {now_utc}")
print(f"raw generated_at: {raw['generated_at']}")
