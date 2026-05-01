# -*- coding: utf-8 -*-
"""一次性生成 today_curated.json（2026-05-01）。

手写中文 tldr + domain_tag，按 link 去重，保留 raw 原始字段。
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with open(RAW, "r", encoding="utf-8") as f:
    raw = json.load(f)

# (link, extra_tldr, domain_tag)
# section 根据 raw 中首次出现的 section 决定
SELECTED = [
    # ========== papers（推理） ==========
    (
        "https://arxiv.org/abs/2604.26968",
        "Predictive Multi-Tier KV Cache。把 MLA 纳入统一 KV sizing 模型（指出 DeepSeek MLA 在通用框架里被过度分配最高 57× 显存），再把 KV 池下沉到 HBM→DRAM→CXL→NVMe GDS→RDMA fabric→并行文件系统多层次，用预测式淘汰替代被动 eviction。对 MLA × 大规模 serving 场景是硬正交工作。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.26103",
        "AMMA 多芯粒 memory-centric 1M 上下文 attention serving。反 GPU 中心范式：承认 decode-phase attention 是 memory-bound，把 compute 掏空、memory 堆到芯粒上，GPU 只剩路由/控制。对 NVIDIA Rubin GPU-LPU 与现有 PIM/PNM 思路都是直接挑战，面向 reasoning/agentic 推理到 1M token 的瓶颈。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.27384",
        "RCW-CIM 数字 CIM LLM 加速器，引入读-算/写（Read-Compute/Write）架构：权重更新和计算解耦，再叠加非线性算子融合缓解依赖延迟。在 Llama2-7B 上 decode 延迟降 21.59%。对 DCIM 路线「权重更新是隐藏成本」这个盲点补了一刀。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.25326",
        "AHASD 移动端 NPU+PIM 异构投机解码，任务级（不是算子级）异步：DLM 跑 PIM 草稿、TLM 在 NPU 批量验证，用 Entropy-History 自适应调 draft 长度，避开算子级同步 idle 与异步下 draft 波动浪费。移动侧 NPU+PIM 解耦 speculative decoding 的系统蓝图。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.02715",
        "FluxMoE 把 expert 参数和 GPU 常驻解绑，引入 expert paging 抽象，权重按需流式物化、用完即驱逐，为 KV cache 腾出 HBM。解决 MoE 推理「巨量 expert 常驻却多数空闲 + 挤占 KV」的老问题，与 FaaSMoE 的 scale-to-zero 是同一斜率的两条路线。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.27396",
        "VitaLLM 三元（BitNet b1.58 风格）LLM 端侧加速器，Dual-Core：TINT-Core 吃巨量三元投影，BoothFlex-Core 吃混精度 attention；再加 dependency-aware 调度消除 workload imbalance/bandwidth-bound decode。为三元量化在通用硬件上的部署困境给出一套专用硬件对照答卷。",
        "推理",
    ),
    # ========== papers（训练） ==========
    (
        "https://arxiv.org/abs/2604.27089",
        "AutoSP 编译器驱动的长上下文训练自动化：把 sequence parallelism 与 ZeRO-3/FSDP/TP/PP 拼装自动化。解决「为了长上下文训练要手写并行策略组合」的开发成本问题，定位是首个 SP-centric 自动化方案，填长上下文训练工具链的空白。",
        "训练",
    ),
    (
        "https://arxiv.org/abs/2604.27085",
        "RoundPipe 消费级 GPU 多卡训练：打破 pipeline schedule 的 weight-binding 约束（LM head 太大导致 stage 不均衡→按最慢卡瓶颈）。把 GPU 当作 stateless 执行池轮转权重，显著缓解 bubble。对 consumer GPU + PCIe 受限场景的 PP 优化是实用工程答卷。",
        "训练",
    ),
    (
        "https://arxiv.org/abs/2604.27844",
        "ZipCCL 首个把无损压缩塞进集合通信库的方案。基于「训练中 activation/grad/param 都近似高斯分布」这一观察做理论有依据的压缩，把 compress/decompress 开销压到小于通信减量收益。对大模型训练通信瓶颈提供「无损而非有损」的新路径。",
        "训练",
    ),
    (
        "https://arxiv.org/abs/2510.19322",
        "SWOT 光网络 demand-aware intra-collective 重构框架。反对「全静态 topology 低效 vs 每步重配开销大」两极，在 CC 算法内部做「集合间」动态对齐。对可重构光网络做 DML 集合通信的工程可行性给出中间路径。",
        "训练",
    ),
    # ========== papers（agent 基础设施） ==========
    (
        "https://arxiv.org/abs/2604.26963",
        "MARS 异构 agent workload 协同调度：agent 把推理从单轮推到多轮 LLM+tool loop、执行从 GPU-only 扩到 GPU-CPU 共享，传统调度器在这两种位移下都失衡。MARS 建立 GPU 推理 × CPU tool 执行的统一信息视图做全局调度，是 agent serving 系统的核心基础设施方向。",
        "agent",
    ),
    (
        "https://arxiv.org/abs/2604.28138",
        "Crab 语义感知的 agent sandbox checkpoint/restore runtime。痛点：应用级 recovery 丢 OS 副作用、全量 per-turn checkpoint 太贵；观察到 >75% agent turn 无 recovery-relevant 状态。Crab 弥合 agent 框架与 OS 的语义 gap，做 RL rollout branching / 容错 / spot 执行的通用基础设施。",
        "agent",
    ),
    # ========== code ==========
    (
        "https://github.com/kvcache-ai/ktransformers/releases/tag/v0.6.1",
        "KTransformers v0.6.1 大 MoE LoRA SFT 全重构：后端改到 kt-kernel，保持 LLaMA-Factory 训练入口兼容。实测 vs ZeRO-Offload 基线 6-12× 训练吞吐、CPU 内存降到一半、GPU 内存压力也小。把大 MoE + LoRA SFT 的单机工程可行性又往前拉了一档。",
        "训练",
    ),
    (
        "https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.10rc1",
        "FlashInfer v0.6.10rc1：trtllm attention kernel 加 head_dim=512（为 MLA/大头维度铺路）、MXFP4×BF16/INT4×FP8 CUTLASS MoE SM90 优化、新增 DCP All-to-All kernel（context-parallel attention reduction）、trtllm-gen FMHA cubins 更新 + context SWA 修复，集合通信新增 allreduce/allgather/reducescatter 组合支持。",
        "推理",
    ),
    (
        "https://github.com/langchain-ai/langgraph/releases/tag/1.2.0a2",
        "LangGraph 1.2.0a2：把 NodeTimeoutError 改为默认可重试（回应 4/29 revert 的 node-level timeouts 路线）、StreamChannel projection 改成 arrival-ordered interleave、正式引入 node-level error handlers（#7233）。是 timers 重构链路的继续推进，agent 框架错误处理基础设施收敛中。",
        "agent",
    ),
    (
        "https://github.com/openai/openai-agents-python/releases/tag/v0.15.0",
        "OpenAI Agents v0.15.0：model refusal 由「空字符串/结构化输出死循环 MaxTurnsExceeded」改为显式抛出 ModelRefusalError，可通过 error_handlers={'model_refusal': ...} 兜底。对 agent runtime 的错误语义是个重要收敛：拒答从 silent failure 变为显式控制流，利于生产环境观测与降级策略。",
        "agent",
    ),
    # ========== blogs ==========
    (
        "https://developer.nvidia.com/blog/automating-gpu-kernel-translation-with-ai-agents-cutile-python-to-cutile-jl/",
        "NVIDIA cuTile Python → cuTile.jl 的自动化 AI agent 翻译链路。tile-level GPU kernel 编程模型跨语言移植，用 coding agent 做转写而非手工重写。是「AI agent 生成 kernel」路线上的实际工程落地，也是 cuTile 生态扩到 Julia 的手段。",
        "推理",
    ),
    # ========== community ==========
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1t0r5nl/got_dflash_speculative_decoding_working_on/",
        "DFlash speculative decoding 在 2080 SUPER 8GB 跑通 Qwen3.5-35B-A3B Q5_K_M（24.44 GiB 原本塞不下）：靠 MoE expert CPU offload + DFlash 草稿，基线 26.8 tok/s 下实测 DFlash 带来实质提升。llama.cpp PR#22105 把 DFlash 路径打通，极限 VRAM 下 MoE 推理的新玩法。",
        "推理",
    ),
    (
        "https://www.reddit.com/r/MachineLearning/comments/1t07zff/a_hackable_ml_compiler_stack_in_5000_lines_of/",
        "5000 行纯 Python 实现 LLM 编译器参考栈，6 层 IR 从 TinyLlama/Qwen2.5-7B 一路 lower 到 raw CUDA kernel。目标不是干翻 Triton，而是为理解 TVM/Inductor/XLA/MLIR 提供最小可读样本，对想摸清 LLM 编译器全貌的工程师是难得的教学级读物。",
        "推理",
    ),
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1t0lwx6/16x_spark_cluster_build_update/",
        "16 台 DGX Spark 组 fabric 的实战记录：QSFP56 dual-rail 单线 200 Gbps，每节点 Ubuntu 开箱即用。重点论据是 unified memory 而非 H100/GB300——512 GB 统一内存池的系统延迟/带宽平衡点与数据中心卡路线明显不同。对国产 ScaleUp 统一内存路线有直接参考意义。",
        "推理",
    ),
]

out_sections = {"papers": [], "code": [], "blogs": [], "community": []}
link_seen = set()

# 扁平所有 raw 条目，按 link 查找
index = {}  # link -> (section, item)
for sec, items in raw["sections"].items():
    for it in items:
        if it["link"] not in index:
            index[it["link"]] = (sec, it)

for link, tldr, tag in SELECTED:
    if link in link_seen:
        continue
    if link not in index:
        print(f"[WARN] link not in raw: {link}")
        continue
    sec, it = index[link]
    new_it = dict(it)  # 保留原字段
    new_it["tldr"] = tldr
    new_it["domain_tag"] = tag
    out_sections[sec].append(new_it)
    link_seen.add(link)

now = datetime.now(timezone.utc).isoformat()
out = {
    "generated_at": now,
    "source": "curated",
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": out_sections,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

counts = {k: len(v) for k, v in out_sections.items()}
tag_counts = {"推理": 0, "训练": 0, "agent": 0}
for v in out_sections.values():
    for it in v:
        tag_counts[it["domain_tag"]] += 1
total = sum(counts.values())
print(f"[curated] total={total} {counts}")
print(f"[curated] domain_tag={tag_counts}")
print(f"[curated] generated_at={now}")
print(f"[curated] saved to {OUT}")
