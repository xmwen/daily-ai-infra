# -*- coding: utf-8 -*-
"""一次性生成 cache/today_curated.json，中文 tldr + domain_tag。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section, title_sub):
    for it in raw["sections"].get(section, []):
        if title_sub.lower() in it["title"].lower():
            return it
    return None


def enrich(item, tldr, tag):
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    return new


curated = {"papers": [], "code": [], "blogs": [], "community": []}

# ---------------- papers ----------------
P = [
    ("Evaluating CUDA Tile", "推理",
     "NVIDIA CuTile 是 Python 层的 tile-centric GPU kernel 抽象，本文首次在 H100 NVL / B200 / RTX PRO 6000 Blackwell 跨架构实测 CuTile vs cuBLAS / Triton / WMMA / raw SIMT。覆盖 GEMM、fused MHA、端到端 LLM 推理（BF16/FP16）。结论：CuTile 的效率高度依赖 workload 和架构，在部分 Blackwell 场景上能逼近甚至超过 cuBLAS，但不是万能银弹——给国产 tile 语言设计提供了有价值的对照基线。"),
    ("TACO", "训练",
     "TACO 是面向大规模 TP 训练中间张量通信压缩的 FP8 框架。核心三件套：数据驱动 reshape + Adaptive Scale-Hadamard Transform 做高保真 FP8 量化、Dual-Scale Quantization 保证数值稳定、高度融合的压缩算子降内存流量。解决 TP 下中间张量近零分布在频繁通信中误差被放大的痛点，是做 TP 通信-计算 overlap 栈时值得追的 baseline。"),
    ("Hybrid JIT-CUDA Graph", "推理",
     "面向低延迟 LLM 推理，把 transformer 推理拆成 CUDA Graph replay 的静态分量 + JIT 编译 kernel 的动态分量，支持异步 graph capture 和跨 decoding step 复用。本质是把 short-sequence 交互场景的 launch overhead 吃掉同时保留动态性，思路与 vLLM cudagraph capture+piecewise 类似但提出了更 formal 的 partition 策略，可作 LLaMA-2 小 batch 延迟优化参考。"),
    ("FlashOverlap", "训练",
     "针对分布式 LLM 训练中的 TP 通信-计算 overlap，指出现有 data slicing 方案的尾延迟瓶颈。提出新的 overlap 技术消除 tail latency，显著提升 state-of-the-art overlap 方法的有效性。是做 Megatron/DeepEP/通信库调度时的尾延迟优化 baseline，与昨日 FlashOverlap 分析对照有新数据。"),
    ("InfiniPipe", "训练",
     "弹性流水线并行（EPP），针对长上下文训练中 sequence 长度分布严重倾斜的问题，融合 token-level PP 和 batch-level PP，按 token/batch 两种粒度混合调度。batch-level 在 sequence packing 下内存爆，token-level 硬件利用率低——EPP 做动态 granularity 调度折中。做 MoE / 长上下文 pretrain 工程时值得参考。"),
    ("Scaling Multi-Node Mixture-of-Experts", "推理",
     "系统性剖析 Llama 4 Maverick、DSV3-671B、Qwen3-230B-A22B 三个主流 MoE 在多节点推理部署下的 expert 激活模式，收集 10w+ 真实 trace。揭示 expert 负载不均衡和跨节点 all-to-all 通信瓶颈是 MoE inference at scale 的根本制约。给基于 expert activation pattern 做 placement / routing / all-to-all 优化的方案提供了开源 trace 基线。"),
    ("ClusterFusion++", "推理",
     "在 Blackwell/Hopper thread-block cluster 粒度上把 Transformer decode block 全块融合：LayerNorm→QKV→RoPE→decode attention→output proj→Post-LN→MLP→residual 一把梭。配合持久 TMA descriptor 的 CUDA-Graph-compatible 执行模式降 per-step overhead。面向 GPT-NeoX/Pythia，比 prior work 只融 attention-side 更进一步，是 decode 阶段全块融合的最新代表作。"),
    ("RetroInfer", "推理",
     "长上下文 LLM 推理的向量存储引擎。把 KV cache offload 到 CPU，利用 attention 稀疏性只检索当前步重要的 token 子集返回 GPU。针对现有稀疏 attention 方案在精度和检索代价之间难以平衡的痛点，引入向量存储引擎抽象统一管理。是 KV cache offload + 稀疏 attention 检索路径的代表作，适合做超长上下文部署参考。"),
]

for sub, tag, tldr in P:
    it = find("papers", sub)
    if it:
        curated["papers"].append(enrich(it, tldr, tag))

# ---------------- code ----------------
C = [
    ("v0.20.0", "推理",
     "vLLM v0.20.0 本周最重磅节点：752 commits，320 contributors。DeepSeek V4 初始支持（DSML token-leakage 修、DSA+MTP IMA 修、shared expert silu clamp）；默认 CUDA wheel 升级到 CUDA 13.0（含 13.0.2 匹配 PyTorch 2.11）；PyTorch 2.11 升级覆盖 CUDA+XPU；Transformers v5 生态全栈迁徙。对国产芯片 fork vLLM 跟主线是硬工作量节点。"),
    ("langgraph==1.1.10", "agent",
     "LangGraph 1.1.10 紧急 revert 了昨日 1.1.9 刚 land 的 node-level timeouts（#7599→#7627）。结合昨日 PyTorch nn.linear_cross_entropy 的 24h revert，基础设施层「feature 落地即回滚」在最近特别高频，反映 runtime 级 API 改动对上游影响面难以提前验证。做 agent 框架升级要特别警惕本周 minor 版本。"),
    ("langgraph-prebuilt==1.0.12", "agent",
     "LangGraph prebuilt 1.0.12：修复 ToolNode 从 channels 经由 pregel helpers hydrate state 的缺陷（#7594）。这是昨日 ToolNode 返回 list[Command|ToolMessage] 新能力（1.0.11）的后续补丁，说明 ToolNode 的 channel 状态 hydration 路径在多工具并发场景下还存在数据可见性问题。对用 LangGraph 做 computer-use 或 coding agent 的项目直接有感知。"),
    ("langgraph-checkpoint==4.0.3", "agent",
     "LangGraph checkpoint 4.0.3：revive 了安全类型的 lc=2 JSON blobs（无需 allowlist，#7582），dedup warnings。对 agent memory 持久化的兼容性改进——旧 checkpoint 无需白名单也可复活，降低长期任务状态迁移成本。langsmith 同步升到 0.7.31。"),
    ("v0.14.7", "agent",
     "OpenAI Agents Python v0.14.7：给 tool item 加 tool_name/call_id 便利属性（#3027）；Phase 2 memory consolidation turn limit 上调（#3038）——说明 agent memory 分层压缩在实际 workload 中触顶频繁；GPT-5.5 aliases 进 sandbox compaction；强化 tar/zip 成员校验，拒绝 LocalFile 的 symlink source（#2972, #3028）——后者是典型的 computer-use agent 文件系统 sandbox 加固。"),
    ("Nightly Release v0.6.9-20260428", "推理",
     "FlashInfer v0.6.9 Nightly（0428）：Blackwell SM120 + fused MoE + FP4 GEMM + routing replay 持续迭代。作为 vLLM/SGLang 的下层 attention/GEMM 后端，FlashInfer 的 Blackwell FP4 路径是跟进 DSV4 / Qwen3.6 在 5090/B200 上极致性能的关键依赖。"),
]

for sub, tag, tldr in C:
    it = find("code", sub)
    if it:
        curated["code"].append(enrich(it, tldr, tag))

# ---------------- community ----------------
COMM = [
    ("Luce DFlash", "推理",
     "独立作者发布 Luce DFlash：基于 ggml 的 GGUF 端 DFlash 投机解码 C++/CUDA stack，单卡 24GB RTX 3090 跑 Qwen3.6-27B。HumanEval/GSM8K/Math500 上较 autoregressive 均值 ~1.98× 加速，零 retraining（等 z-lab 匹配 draft 训完 AL 还会涨）。面向 Blackwell/Jetson AGX Thor 已就绪。对本地化部署 + 投机解码这个组合是强信号。"),
    ("3× faster HFQ4 prefill on Strix Halo", "推理",
     "hipfire（RDNA 专用 LLM 推理引擎）的 HFQ4-G256 MMQ prefill 路径 PR：在 AMD Strix Halo 上把 HFQ4 prefill 从 ~310-340 tok/s 提升 3×。做法是把 prefill 从通用慢路径改成 tiled MMQ 专用 quantized matmul kernel，pre-quantize + 专门 tile。RDNA 上 HFQ4 量化推理 kernel 优化的公开实测数据，对对标 AMD 路线有参考价值。"),
    ("Qwen3.6-27B IQ4_XS FULL VRAM", "推理",
     "实测定位 llama.cpp 某次 commit（1dab5f5a44）导致 Qwen3.6-27B IQ4_XS 量化从 14.7GB 膨胀到 15.1GB（+400MB），对 16GB VRAM 卡直接打破 110k 上下文+模型共存的临界点。revert 后 KV cache 空间恢复。是 GGUF 量化工程中常见的「看起来无关 commit 意外吃显存」案例。"),
    ("Qwen 3.6 27B BF16 vs Q4_K_M vs Q8_0", "推理",
     "Qwen 3.6 27B 三档量化（BF16/Q4_K_M/Q8_0）在 HumanEval/HellaSwag/BFCL 上的实测：BF16 均值 69.78%、Q4_K_M 66.54%、Q8_0 66.15%；throughput Q4_K_M 最快 22.5 tok/s，BF16 只有 15.5。结论是 Q4_K_M 比 Q8_0 精度相近但吞吐更高，对 27B 级别部署选型有直接参考。"),
]

for sub, tag, tldr in COMM:
    it = find("community", sub)
    if it:
        curated["community"].append(enrich(it, tldr, tag))

now = datetime.now(timezone.utc).isoformat()
out = {
    "generated_at": now,
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": curated,
    "fetch_stats": raw.get("fetch_stats", {}),
}

OUT.write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

total = sum(len(v) for v in curated.values())
print(f"[curated] generated_at={now}")
print(f"[curated] total={total} papers={len(curated['papers'])} code={len(curated['code'])} blogs={len(curated['blogs'])} community={len(curated['community'])}")

tag_stat = {"推理": 0, "训练": 0, "agent": 0}
for sec in curated.values():
    for it in sec:
        tag_stat[it["domain_tag"]] = tag_stat.get(it["domain_tag"], 0) + 1
print(f"[curated] tags: {tag_stat}")
