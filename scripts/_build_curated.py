# -*- coding: utf-8 -*-
"""一次性脚本：读 today_raw.json，手写中文 tldr 与 domain_tag，输出 today_curated.json。

硬性要求：
- tldr ≤ 200 字中文，聚焦「这是什么 + 方法 + 效果」
- domain_tag ∈ {推理, 训练, agent}
- generated_at 比 raw 新
- tldr 中所有强调词用中文「」引号，避开英文双引号字符串闭合坑
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 按 link 对 papers 去重（跨分区重复是 arXiv 常态）
def dedupe_by_link(items):
    seen = set()
    out = []
    for it in items:
        link = it.get("link", "")
        if link in seen:
            continue
        seen.add(link)
        out.append(it)
    return out

# ========== papers 手写 tldr ==========
papers_pool = dedupe_by_link(raw["sections"]["papers"])

# link -> (tldr, domain_tag)；未选中的 link 不写入
paper_notes = {
    "https://arxiv.org/abs/2605.01708": (
        "「SplitZip」针对 PD 分离后 prefill→decode 的跨机 KV 传输瓶颈，给出面向 disagg serving 的超快无损 KV 压缩。现有 codec 大多针对离线权重、跑在 CPU 侧或用变长编码导致解压串行，不适配 disagg 的在线传输。SplitZip 做了 GPU 原生的定长编码路径，让解压可与 RDMA 流水并行。对长输入与 agentic workload（长上下文）场景的 KV 搬运开销下降最明显，是 PD 分离架构底层工程补齐的一块关键拼图。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.01910": (
        "「SANTA」把 decode 阶段 value-cache 的访存从「全读 + MAC」改成「从 post-softmax 分布采样 S≪n_k 个索引 + gather-and-add」，给出 post-softmax value 聚合的无偏估计，本质是把 value 一侧的乘加替换成聚集加。配合分层采样做方差缩减与 GPU 友好化，RTX 6000 Ada 上 decode attention kernel vs FlashInfer/FlashDecoding 快 1.5×，32k 上下文保精度。稀疏注意力在 decode memory-bound 阶段的新范式，可直接接 FlashInfer。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.02568": (
        "「StreamIndex」解决 DeepSeek V3.2/V4 Compressed Sparse Attention 的工程硬伤：公开实现要先物化 [B,S,H_I,T] 的 FP32 打分张量再 top-k，H_I=64、m=4、S=65k 时中间张量 256GB 超过任何单卡 HBM。作者给出 Triton 实现 chunked partition-merge top-k driver，永不物化全量中间张量，在 V4 形状输入下既跑得动又保精度。是国内复现 V4-Flash CSA 推理栈绕不开的一条参考路径。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.02189": (
        "「PipeMax」针对 commodity GPU server 的离线推理，首次联合优化流水并行 + offload。PP 天然通信低且每卡一刻只保留一个 batch 活跃，其余 batch 的 KV cache 可主动 offload 到 host/NVMe，把 GPU 显存当成活跃窗口。与 offload/并行各管一段的现有做法相比，PipeMax 把计算与 offload 数据搬运协同调度，在 offline batch 推理吞吐上显著扩容 GPU 显存。对大规模离线生成/评估/数据合成栈非常实用。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.02329": (
        "「Kairos」针对 disagg LLM serving 的尾部 SLO 难题：请求长度长尾导致 prefill 侧队头阻塞、decode 侧 straggler 拉垮利用率。现有系统对 prefill 用 FCFS、对 decode 用 continuous batching，没有不平衡感知。Kairos 给 prefill + decode 两侧各配一套互补机制做 SLO-aware 调度。在生产 workload 上同时改善 SLO 达成率与吞吐，比之前 SkyServe 等工作更贴近真实 request 长尾分布。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00827": (
        "「MCP Workflow Engine」把 agent「思考什么」与「执行什么」解耦：agent 只推理一次产出声明式 workflow blueprint（JSON 描述 MCP tool 调用序列，支持模板参数、循环、并行分支、数据 piping），后续同类任务直接复放这份 blueprint 不再走 LLM。本质是 agent 系统把 tool-use 工作流「静态图化」做缓存，属于 MCP 协议层 orchestration 基础设施。对 agent 运行时 token 消耗与延迟优化直接。",
        "agent",
    ),
    "https://arxiv.org/abs/2605.00831": (
        "「GhostServe」给长生命周期 agent LLM 推理提供 KV cache 容错：对流式 KV cache 做 erasure coding，把 parity shards 放在 host memory 做「影子」副本，GPU 侧主副本故障可从 host 恢复而不用 checkpoint 整次重跑。针对 million-token agent 长任务的硬件/软件故障场景，比传统 checkpoint/restart 粒度更细且对 serving 吞吐干扰更小。disagg serving 架构的容错基础设施补齐。",
        "推理",
    ),
    "https://arxiv.org/abs/2603.11438": (
        "「NCCLbpf」把 eBPF 放进 NCCL：当前 NCCL plugin 在 NCCL 地址空间内跑未验证原生代码，容易崩、静默污染状态或因策略更新停机。NCCLbpf 在现有 plugin 接口里嵌 userspace eBPF runtime，加载时静态验证不安全插件、提供结构化 cross-plugin map 让策略可组合 + 闭环自适应、支持原子热切换。集合通信运行时的可编程性 + 安全性基础设施，对大规模训练栈运维价值明确。",
        "训练",
    ),
    "https://arxiv.org/abs/2605.01938": (
        "Grace Hopper GH200 多模态训练能耗跨层分析：DeepSpeed 的 CPU offload + activation checkpointing + 通信优化虽解显存与带宽瓶颈，但会引入额外系统活动干扰能效。作者在 GH200 紧耦合 CPU-GPU NVLink + 统一内存架构下，跨层测量哪些优化实际省能哪些反而亏，给出在超级芯片上选择训练策略的参数化建议。对国产 ScaleUp 统一内存路线的能耗建模有直接参考价值。",
        "训练",
    ),
    "https://arxiv.org/abs/2511.06838": (
        "「P3-LLM」NPU + DRAM-PIM 集成加速器做边缘 LLM 推理：现有 NPU+PIM 设计的 PIM 高精度计算单元在 DRAM 工艺下面积/功耗开销大限制吞吐。P3-LLM 提出灵活混合精度量化方案，不同 operand 用不同数值格式在不同单元上算，把 PIM 专注低精度 + NPU 吃高精度。对国产 PIM 芯片落地边缘 LLM 推理的精度-面积-功耗 trade-off 有工程参考。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.02162": (
        "「AAFLOW」给 agentic workflow 一个高性能分布式 runtime，把 workflow 建模成 operator 抽象，用 Apache Arrow + Cylon 构造 zero-copy 数据平面，让预处理/embedding/向量召回可直接零拷贝互操作。核心打的是现有 agent 框架「数据编排碎片化 + 序列化开销 + 非确定执行」三大可扩展性痛点，属于把 HPC 执行模型迁移到 agent 基础设施的一条主线。",
        "agent",
    ),
    "https://arxiv.org/abs/2605.01280": (
        "Position 论文，立场：LLM serving 的算法内核至今仍是经典分布式计算那一套——路由用 JSQ/round-robin、调度默认 FIFO、KV 驱逐默认 LRU，完全忽视 LLM 推理的独特结构（KV 动态增长、prefill/decode 相位不对称、输出长度未知、continuous batching 约束）。呼吁整个领域转向数学最优化与算法基础（而非纯启发式）来重建 serving 核心。给 vLLM/SGLang 下一代调度器定调，方向性参考。",
        "推理",
    ),
}

# Silicon Showdown / Sim-FA / Tempus 5/4 已覆盖，今日是 v2/v3 replace 无新增量，不重复收

paper_items = []
for it in papers_pool:
    note = paper_notes.get(it["link"])
    if not note:
        continue
    tldr, tag = note
    new_it = dict(it)
    new_it["tldr"] = tldr
    new_it["domain_tag"] = tag
    paper_items.append(new_it)

# ========== code 手写 tldr ==========
code_pool = raw["sections"]["code"]
code_notes_by_link = {
    "https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.10": (
        "「FlashInfer v0.6.10 正式版」相对 rc1 收敛：新增 trtllm attention head_dim=512 支持、MXFP4×BF16 与 INT4×FP8 CUTLASS MoE backend 在 SM90 的性能优化、DCP All-to-All kernel 给 context-parallel attention 归约、context SWA 修复。autotuner 加了 profile 输入张量 cache 前的命中检查，trtllm-gen FMHA cubins 头文件同步。正式版意味着下游 vLLM/SGLang 的 FlashInfer 依赖线可以从 rc 升上来。",
        "推理",
    ),
    "https://github.com/vllm-project/vllm/releases/tag/v0.20.1": (
        "「vLLM v0.20.1」patch：DeepSeek V4 Base 模型支持、multi-stream pre-attention GEMM（配合可调 token 阈值 VLLM_MULTI_STREAM_GEMM_TOKEN_THRESHOLD）、BF16/MXFP8 A2A 给 FlashInfer one-sided 通信、PTX cvt 做 FP32→FP4 更快转换、head_compute_mix_kernel 整合、临时 guard 掉 v0.20.0 新上的 persistent topk（TopK=1024 cooperative 死锁 + RadixRowState inter-CTA init race）。本月第 4 次「feature 落地即回滚」。",
        "推理",
    ),
    "https://github.com/dottxt-ai/outlines/releases/tag/1.2.13": (
        "「Outlines v1.2.12」结构化生成一轮 bugfix：llama.cpp EOS attention mask + 词表截断修复、DSL 容器类型内字符串字面量补 JSON 双引号、词表构造累积重复 token ID、transformer 兼容时 inline SPIECE_UNDERLINE fallback、多 BPE token 解码到同一字符串时保留全部 token ID、chat template 检查重构。structured output 栈在 constrained decoding 精度边界上的持续收敛，vLLM/SGLang 对接 Outlines 的下游会直接吃到。",
        "agent",
    ),
    "https://github.com/langchain-ai/langgraph/releases/tag/1.2.0a7": (
        "「LangGraph 1.2.0a7 + checkpoint 4.1.0a4 + checkpoint-postgres 3.1.0a4」三连 alpha 推进：新增 public get_writes_history saver API 暴露每次 super-step 的 writes，配合 delta cadence 重做（就是 DeltaChannel sentinel + checkpoint_writes 重建链路的延续）。让外部调度器/tracing 可以拿到 checkpoint writes 历史做细粒度回放与分支。timers 重构后 1.2 线的稳定收敛。",
        "agent",
    ),
    "https://github.com/sgl-project/sglang/releases/tag/v0.5.11": (
        "「SGLang v0.5.11」release。官方 changelog 极简只一行标题，但落在 5/5 早间是本周 SGLang 正式版节点信号，下游 DeepSeek V4/Qwen3.6 部署链路会跟进。本条保留作节奏标记，具体 changelog 待 GitHub release note 展开或下一跑覆盖。",
        "推理",
    ),
}

code_items = []
for it in code_pool:
    note = code_notes_by_link.get(it["link"])
    if not note:
        continue
    tldr, tag = note
    new_it = dict(it)
    new_it["tldr"] = tldr
    new_it["domain_tag"] = tag
    code_items.append(new_it)

# ========== community 手写 tldr ==========
comm_pool = raw["sections"]["community"]
comm_notes_by_link = {
    "https://www.reddit.com/r/LocalLLaMA/comments/1t3zu7u/vllm_just_merged_turboquant_fix_for_qwen_35/": (
        "「vLLM 合并 TurboQuant KV cache 量化 for Qwen3.5+」之前因 Mamba 层抛 NotImplemented 跑不起来，PR #39931 把 hybrid 路径补齐；实测 Qwen3.6 27B 通过 --kv-cache-dtype turboquant_4bit_nc 可用，可选 k8v4 / 4bit_nc / k3v4_nc / 3bit_nc 四档。配 --enable-chunked-prefill 时要把 --max-num-batched-tokens 提到 4096 以上过 mamba align。TurboQuant 作为 per-vector min-max 3/4-bit 方案在 vLLM 主线 hybrid Mamba+Attn 模型上首次可用，直接落到 Qwen3.5+/Qwen3.6 产线。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1t46klu/qwen36_27b_fp8_runs_with_200k_tokens_of_bf16_kv/": (
        "「Qwen3.6 27B FP8 + 200k BF16 KV on 单卡 RTX 5000 PRO 48GB 80 TPS」官方 FP8 权重 + Blackwell FP8 加速 + 非量化 KV，拿 48GB 卡绕开 24GB 的 KV 量化精度劣化。对比之前大家在 24GB 卡上各种 Q4/Q8 KV 量化追精度，48GB 档是当前消费级单卡跑 agentic coding 的精度-显存甜点。对评估消费级推理卡买点与国产 48GB 显存方案定位有直接参考。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1t3guzw/llamacpp_mtp_support_now_in_beta/": (
        "「llama.cpp MTP 正式进 beta」Qwen3.5 MTP 先落地，后续模型跟进中，叠加成熟的 TP 支持，llama.cpp 与 vLLM 在 token 生成速度上的差距有望抹平。配合同日 r/LocalLLaMA 「MTP 支持模型清单」帖（DeepSeek V3/V3.2/V4、Qwen3.5+、GLM4.5+、MiniMax2.5+、Step3.5Flash、Mimo v2+），预示消费级 llama.cpp 侧投机解码统一到 MTP 原生权重路线。",
        "推理",
    ),
}

comm_items = []
for it in comm_pool:
    note = comm_notes_by_link.get(it["link"])
    if not note:
        continue
    tldr, tag = note
    new_it = dict(it)
    new_it["tldr"] = tldr
    new_it["domain_tag"] = tag
    comm_items.append(new_it)

# blogs 今日 0 条
blogs_items = []

curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {
        "papers": paper_items,
        "code": code_items,
        "blogs": blogs_items,
        "community": comm_items,
    },
}

OUT.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for sec in ["papers", "code", "blogs", "community"]:
    for it in curated["sections"][sec]:
        tag_count[it["domain_tag"]] += 1

print(
    f"curated 总计 {sum(len(curated['sections'][s]) for s in ['papers','code','blogs','community'])} 条"
    f"（papers {len(paper_items)} / code {len(code_items)} / blogs 0 / community {len(comm_items)}）"
)
print(f"domain_tag 分布：推理 {tag_count['推理']} / 训练 {tag_count['训练']} / agent {tag_count['agent']}")
print(f"generated_at = {curated['generated_at']}")
print(f"raw generated_at = {raw['generated_at']}")
