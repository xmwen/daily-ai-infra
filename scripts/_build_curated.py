# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成中文 curated。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with open(RAW, "r", encoding="utf-8") as f:
    raw = json.load(f)


def pick(section_name, wants):
    """从 raw[section_name] 按 link 选出 wants 指定的条目，附加 tldr/domain_tag。
    wants: list of (link, tldr, domain_tag)
    """
    by_link = {}
    for it in raw["sections"].get(section_name, []):
        by_link.setdefault(it["link"], it)  # 同 link 只取第一次出现，避开跨分区重复
    out = []
    for link, tldr, tag in wants:
        src = by_link.get(link)
        if not src:
            print(f"[warn] link not found in {section_name}: {link}")
            continue
        item = dict(src)
        item["tldr"] = tldr
        item["domain_tag"] = tag
        out.append(item)
    return out


# ============== papers ==============
# 注意：arXiv 同一 ID 会在 cs.DC/cs.AR/cs.PF/cs.LG/cs.CL 多个分区重复，
# 去重后按「推理/训练/agent」维度挑最有工程价值的，其余丢弃凑数（宁缺毋滥）。
papers_wants = [
    (
        "https://arxiv.org/abs/2602.10718",
        "SnapMLA：针对 DeepSeek MLA 解码的 FP8 硬件感知量化流水线。识别 MLA 解码 FP8 化的三大障碍——位置编码解耦导致数值异质、FP8 PV GEMM 量化 scale 对齐困难、系统级支持缺失，提出 RoPE-aware per-token KV 量化 + 算法-kernel 协同优化，把 long-context MLA decode 推进到 FP8 全链路。对 SGLang/vLLM 里 MLA 路径的 FP8 落地有直接参考价值。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.25080",
        "CacheFlow：把 KV cache 恢复重构为三维并行执行问题。现有方案在 recompute vs 远端 offload 之间做单请求 tradeoff，忽略 token/layer/分布式部署三个维度的并行性和 batch 下的资源争抢。CacheFlow 统一 3D 并行恢复框架，针对 multi-turn/RAG/agentic 等长上下文 serving 把 restore bottleneck 卸下。和 Mooncake/LMCache 的 KV 迁移是同一条赛道。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.24820",
        "Salca：长上下文 attention 解码的稀疏感知硬件加速器。软硬件协同——软件侧双压缩动态稀疏注意力（ultra-low-precision 量化 + 特征稀疏），硬件侧针对 decode 阶段 KV cache 带宽压力设计专用流水线。面向长上下文 decode 带宽瓶颈，和 PIM/SSD-attention 之类 near-data 方案同一思路。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.24971",
        "PolyKV：多 agent 共享一份非对称压缩 KV cache 池。不再每个 agent 独立一份 cache，而是写一次压缩后注入 N 个 agent 上下文（HuggingFace DynamicCache）。压缩非对称：Key 走 int8（保 softmax 稳定）、Value 走 TurboQuant MSE（Fast Walsh-Hadamard + 3-bit Lloyd-Max 量化）。多 agent 批量推理场景下压 cache 池成本的直接方案。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2512.13525",
        "Janus：MoE 推理把 attention 和 experts 拆到独立 GPU worker 池。monolithic 部署强行让两类层共享资源配置，但它们 scaling 行为和 bottleneck 完全不同。Janus 三原则：解耦 attention/MoE 层资源、独立调度、动态调度 MoE 工作负载。和近期 UniEP/MegaScale 的 EP 独立部署趋势一脉相承。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.25326",
        "AHASD：移动端 NPU+PIM 异构的自适应投机解码。识别 operator-level 同步执行的 idle 开销和异步执行因 draft 长度波动导致的计算浪费，提出 task-level DLM-TLM 解耦——PIM 跑并行 drafting，NPU 跑 verification。配 Entropy-History-Aware draft 长度自适应，是端侧 spec-decode 的系统级优化。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.25306",
        "QFlash：把 FlashAttention 全量量化到 integer。识别三大障碍——tile-wise 累加 scale 爆炸、GPU 上移位指数低效、integer 比较对量化粒度的统一 scale 要求。解法是整型域 softmax + 单 Triton kernel 实现。ViT/DeiT/Swin 7 个 workload 上 vs I-ViT 最高 6.73×。把 FA 的数值稳定性障碍搬到全整型域。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2601.14910",
        "PipeWeave：analytical + learning 混合的 GPU 性能预测统一框架。纯数据驱动方法跨硬件泛化差、对现代推理栈里复杂 production kernel 建模不足。PipeWeave 先用 analytical model 量化 kernel 对 GPU 异构指令流水线的需求，再交给 learning model。做国产芯片性能建模对齐 NVIDIA 时这个思路可以直接借鉴（topsAnalytics/VisitorBound 类建模）。",
        "推理",
    ),
]

# ============== code ==============
# FlashInfer nightly 日级别意义不大，OpenAI Agents 0.14.7/0.14.8 合并一条覆盖
code_wants = [
    (
        "https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13",
        "TensorRT-LLM v1.3.0rc13：Nemotron 3 Nano Omni 支持与初步优化（audio 从 video 抽取、ViT attention 优化、Nemotron/Nano VL 初始化显存下降）；GLM-4.7/GLM-5 tool parser；DeepSeek-V3.2 与 V3-Lite 在 Blackwell/SM100 上的 perf + chunked-prefill 修复；Nemotron-H Python 层执行优化。Blackwell 上 DeepSeek 路径的持续打磨节奏。",
        "推理",
    ),
    (
        "https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta11",
        "FlashAttention 4 beta11：CUTE DSL 下 head_dim=256 支持（fwd+bwd）——对 Qwen3/Llama3 之外大 head_dim 模型补齐；Flex autograd 接口接入、flash_attn_varlen_func 增加 score_mod_bwd；SM100 上 MLA kernel 传 stream 修复、clc 调度请求 bug；MLA absorbed test 补齐覆盖。FA4 往 flex + MLA 生产可用方向再推一步。",
        "推理",
    ),
    (
        "https://github.com/openai/openai-agents-python/releases/tag/v0.14.8",
        "OpenAI Agents Python v0.14.8（合并 v0.14.7）：MCP re-export import error 保留（便于定位 MCP 装配失败）；sandbox prompt 指令分节分隔；tool item 加 tool_name/call_id 便捷属性；Phase 2 memory consolidation turn 上限上调；tar/zip member 校验收紧、拒绝 symlink LocalFile 源；Responses API 调用剔除 unset 字段。供应链加固 + agent memory 工程细节持续完善。",
        "agent",
    ),
    (
        "https://github.com/mlc-ai/xgrammar/releases/tag/v0.1.34",
        "XGrammar v0.1.34：EBNF 解析接受 {n,-1} 作无上界重复、AnyTokensFormat+exclude_tokens 作为 self-terminating 处理、解除 `.` 的 unlimited 限制、Gemma 4 内置 structural tag 支持；绑定层重新迁到 tvm_ffi。constrained decoding 引擎层面 grammar 语义和结构化输出 tag 都在补齐 Gemma 4。",
        "agent",
    ),
    (
        "https://github.com/flashinfer-ai/flashinfer/releases/tag/nightly-v0.6.9-20260428",
        "FlashInfer nightly v0.6.9-20260428：延续 Blackwell SM120 fused MoE + FP4 GEMM + routing_replay 路径的日常修复。nightly 标签本身信号弱，但每日 build 表明 Blackwell/FP4 在 FlashInfer 里仍是最活跃的开发主线。",
        "推理",
    ),
]

# ============== blogs ==============
# Nemotron 3 Nano Omni 在 blog + arXiv 都有，blog 里 HuggingFace + NVIDIA 两条重复，只留一条
blogs_wants = [
    (
        "https://developer.nvidia.com/blog/scaling-biomolecular-modeling-using-context-parallelism-in-nvidia-bionemo/",
        "NVIDIA BioNeMo：用 Context Parallelism 扩展生物分子建模。计算生物长期被「单 GPU 显存塞不下复杂生物系统」这个还原论妥协所限制；BioNeMo 把 LLM 训练里已成熟的 context parallel 机制搬到生物分子建模。意义在于：CP 已不只是 LLM 长上下文专属技术，正向科学计算扩散，对训练/推理 CP 工程经验跨域复用是正反馈。",
        "训练",
    ),
]

# ============== community ==============
# 严格筛掉应用层（web search 教程、"跑本地模型的感想"）
community_wants = [
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1syx4sg/qwen_introduced_flashqla/",
        "Qwen 开源 FlashQLA：TileLang 构建的高性能线性注意力 kernel。2-3× fwd、2× bwd；gate-driven 自动 intra-card CP、代数重构硬件友好形式、TileLang fused warp-specialized kernels。没完全 fuse GDN 全流程而是拆成 CP+bwd 两个 kernel，大 batch 下多一点 I/O 但在端侧+长上下文场景整体更优。线性注意力 kernel 工程化又一重要样本。",
        "推理",
    ),
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1sysyz2/qwen36_27b_on_dual_rtx_5060_ti_16gb_with_vllm_60/",
        "Qwen3.6-27B NVFP4+MTP 在双卡 RTX 5060 Ti 16GB 上跑通 vLLM：TP=2、204k 上下文、~60 tok/s、CUDA 13 + Torch 2.11 nightly + vLLM 0.19.2rc1.dev + FP8 KV cache + modelopt + MTP(num_speculative_tokens=3)。工程细节完整：消费级 16GB×2 跑 27B+长上下文+投机解码+NVFP4 量化的端到端可复现配方。",
        "推理",
    ),
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1syxckc/llamacpp_benchmark_native_vs_non_native_nvfp4_on/",
        "llama.cpp Blackwell native NVFP4 vs 非 native 实测（同 Qwen3.6-27B-NVFP4）：b8967 首个 native NVFP4 build 对比 b8966。核心结论：prompt processing 提速 43-68%，但 token generation 基本无变化。拆开说：NVFP4 native 打的是 compute-bound 的 prefill，decode 仍是 memory-bound 瓶颈。量化 native kernel 收益分布符合第一性原理。",
        "推理",
    ),
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1systb1/llamacpp_nvfp4_native_support_on_blackwell_from/",
        "llama.cpp b8967：Blackwell NVFP4 native 支持落地。RTX 5090 上 Qwen3.6-27B-NVFP4（17.5GiB/26.9B）pp512 达 5546 t/s、tg128 73 t/s。和上一条 native vs 非 native 对比互为证据：FP4 原生 kernel 先解决 prefill 吞吐，decode 仍受 KV/权重 带宽制约。消费级 Blackwell 部署量化模型的关键节点。",
        "推理",
    ),
]

# ============== 汇总 ==============
papers = pick("papers", papers_wants)
code = pick("code", code_wants)
blogs = pick("blogs", blogs_wants)
community = pick("community", community_wants)

curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": {
        "papers": papers,
        "code": code,
        "blogs": blogs,
        "community": community,
    },
    "fetch_stats": raw.get("fetch_stats", {}),
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(curated, f, ensure_ascii=False, indent=2)

# 统计
total = sum(len(v) for v in curated["sections"].values())
dist = {"推理": 0, "训练": 0, "agent": 0}
for sec in curated["sections"].values():
    for it in sec:
        tag = it.get("domain_tag")
        if tag in dist:
            dist[tag] += 1
print(f"curated total={total}  papers={len(papers)}  code={len(code)}  blogs={len(blogs)}  community={len(community)}")
print(f"domain_tag: 推理={dist['推理']}  训练={dist['训练']}  agent={dist['agent']}")
print(f"raw.generated_at   = {raw['generated_at']}")
print(f"curated.generated_at = {curated['generated_at']}")
