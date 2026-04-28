"""一次性脚本：基于 cache/today_raw.json 生成中文 curated。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 根据 link 挑选要保留的条目，并附 tldr+domain_tag
# domain_tag ∈ {推理, 训练, agent}
CURATED = {
    # ========= papers（保留 11 条） =========
    "https://arxiv.org/abs/2604.23466": {
        "tldr": "NVIDIA CuTile（Python tile-centric CUDA 抽象）的首次独立跨架构评测，在 H100 NVL / B200 / RTX PRO 6000 Blackwell 三卡上对 GEMM、fused MHA、端到端 LLM 推理与 cuBLAS/Triton/WMMA/raw SIMT 逐一对标。结论是 CuTile 的效果与工作负载和架构强相关——不是「写一版就通吃」，给想迁到 CuTile 的 kernel 工程师提供了第一手 portability 证据。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.24088": {
        "tldr": "TACO 面向 tensor-parallel 训练中间张量通信压缩：观察到 TP intermediate tensor 接近零稠密分布、反复通信累积误差大。做法是 data-driven reshape + Adaptive Scale-Hadamard 变换使 FP8 量化高保真、再用 Dual-Scale Quantization 维持数值稳定，并把压缩融到一个算子里减少显存访问。目标是把大规模 TP 训练里的通信这一关从「算法差 + 开销大」同时解掉。",
        "domain_tag": "训练",
    },
    "https://arxiv.org/abs/2604.23467": {
        "tldr": "Hybrid JIT-CUDA Graph 低延迟推理框架：把 transformer 推理拆成静态部分（CUDA Graph replay）+ 动态部分（JIT 编译 kernel），实现 decoding step 间 graph 的异步 capture 和复用。针对短序列交互场景的 kernel launch overhead 给出混合 runtime 解法，可以和 TensorRT-LLM 的 fixed-shape graph 路线互补。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.24013": {
        "tldr": "FlashOverlap 针对分布式 LLM 训练中 overlap 方案尾延迟问题：指出已有 data slicing 方式在 TP/DP 场景下 tail latency 长。提出一种新的 overlap 技术专门消除这段尾，使 TP 的通信瓶颈和通信-计算重叠的最差情况都被控制。大规模集群里「第 P99 步慢」的结构性成因被直接针对。",
        "domain_tag": "训练",
    },
    "https://arxiv.org/abs/2509.21275": {
        "tldr": "InfiniPipe 弹性流水并行：观察到 batch-level PP 在长上下文场景显存炸、token-level PP 硬件利用率差，数据 seq 长度分布高度倾斜使单一粒度 PP 难以最优。提出 Elastic Pipeline Parallelism 在 token-level 与 batch-level 间自适应切换粒度，专治变长长上下文训练。",
        "domain_tag": "训练",
    },
    "https://arxiv.org/abs/2604.23150": {
        "tldr": "基于 Llama4 Maverick、DeepSeek V3-671B、Qwen3-230B-A22B 等 SOTA MoE 收集 10 万条真实 expert 激活 trace，系统刻画多节点 MoE 推理在 expert 负载不均 + token 路由低效下跨节点 all-to-all 的瓶颈，并提出基于 expert activation pattern 的 scaling 方案。真实 trace 驱动，面向大规模 MoE serving。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2603.11504": {
        "tldr": "LongFlow 针对 reasoning model 长输出场景的 KV cache 压缩：指出已有 KV 优化主要面向「长输入短输出」，对 o1/R1 这类 long-output 推理的带宽压力反而无效，且 token importance 估计代价太高无法持续重估。用更轻的 importance scoring + 结构化压缩，压实 long-output decode 的 KV 带宽问题。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.24008": {
        "tldr": "Coverage-Based PTQ 校准选样：观察到 INT4 PTQ 质量很大程度取决于 calibration sample 有没有「激活 outlier channel」，未激活就会低估 dynamic range 产生 per-channel 误差。把选样建模成 outlier channel 上的加权集合覆盖问题，目标单调次模，用贪心逼近。给 AWQ/GPTQ 之前的数据选择环节提供了理论化框架——和 AWQ 的 salient channel 思路一脉相承但视角放在数据侧。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.23798": {
        "tldr": "ELSA 精确线性扫描 attention：把 online softmax 重写为 $(m, S, W)$ 结合律 monoid 上的 prefix scan，拿到 O(n) 额外显存 + O(log n) 并行深度 + 可证 O(u log n) FP32 误差上界。最大卖点是 tensor-core independent（用 Triton/CUDA C++ 实现），作为 drop-in 替换不改权重。对没有 TC 或 TC 资源紧张场景（如某些国产芯片）的 exact attention 很有价值。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2505.02922": {
        "tldr": "RetroInfer 把长上下文 LLM 推理的 KV cache 当作向量存储引擎：利用 attention 稀疏性，把 KV offload 到 CPU memory、只按需检索 per-step 的关键 token。解决已有 sparse attention 方案在 accuracy 和 retrieval cost 之间不好平衡、GPU-CPU 显存搬运效率差两个痛点，面向长上下文 serving。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.23553": {
        "tldr": "ClusterFusion++ 把 thread-block cluster 级融合从「QKV projection+attention+output projection」扩到完整 Transformer decoder block：LayerNorm → QKV → RoPE → decode attention → output projection → Post-LN → MLP → residual 一个 kernel 跑完。并做了 CUDA-Graph 兼容的执行模式配 persistent TMA descriptor 降低 per-step 开销。对延迟敏感的 decode 是直接打法。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2407.09577": {
        "tldr": "FlashNorm 对 RMSNorm + linear 组合的精确重写：(1) 把 norm weight 吸进后续 linear，消掉 norm weights；(2) 利用 RMS 标度不变性把 scalar RMS 归一化推迟到 matmul 输出端，让 vector 单元的 RMS 计算和 tensor core 的 matmul 并行执行，不再阻塞。对 vector+matrix 单元解耦的硬件（含某些国产 NPU）很直接地解掉「normalization 卡 GEMM」的串行链。",
        "domain_tag": "推理",
    },
    # ========= code（保留 4 条） =========
    "https://github.com/vllm-project/vllm/releases/tag/v0.20.0": {
        "tldr": "vLLM v0.20.0：752 commits / 320 contributors 的年度级大版本。DeepSeek V4 初步支持（含 DSML token leakage、DSA+MTP IMA、shared expert silu clamp 三修），默认 wheel 从 CUDA 12.x 切到 CUDA 13.0 + PyTorch 2.11，XPU 也同步到 torch 2.11。CUDA 版本策略跟 PyTorch；CUDA 12.9 用户推荐用 uv --torch-backend=cu129。属于本周推理栈最重要的节点事件。",
        "domain_tag": "推理",
    },
    "https://github.com/langchain-ai/langgraph/releases/tag/1.1.10": {
        "tldr": "LangGraph 1.1.10 紧急回滚：1.1.9 刚加的 node-level timeouts（#7599）在此版本被整体 revert（#7627），24 小时内进出主线。agent 框架在 runtime 层加 per-node timeout 看似简单，落到实际检查点/调度状态里涉及 pregel 执行循环一致性，社区已有两次尝试失败。infra 层 revert 信号对同类框架设计有参考价值。",
        "domain_tag": "agent",
    },
    "https://github.com/langchain-ai/langgraph/releases/tag/checkpoint%3D%3D4.0.3": {
        "tldr": "LangGraph checkpoint 4.0.3：恢复对 lc=2 JSON blobs 的 safe-types 反序列化支持（#7582），不再强制走 allowlist。agent 状态持久化向后兼容的补救，对已经落盘老版本 checkpoint 的生产环境避免 breaking。",
        "domain_tag": "agent",
    },
    "https://github.com/langchain-ai/langgraph/releases/tag/prebuilt%3D%3D1.0.12": {
        "tldr": "LangGraph prebuilt 1.0.12：修复 ToolNode 从 channels 通过 pregel helper 做 state hydration（#7594），配合 1.0.11 新加的 ToolNode 返回 list[Command | ToolMessage] 一起完善 tool 调用的状态流。agent runtime 侧 tool 语义的打磨仍在持续。",
        "domain_tag": "agent",
    },
    # ========= community（保留 4 条） =========
    "https://www.reddit.com/r/LocalLLaMA/comments/1sx8uok/luce_dflash_qwen3627b_at_up_to_2x_throughput_on_a/": {
        "tldr": "Luce DFlash 把 DFlash 投机解码 port 到 GGUF + 单机 C++/CUDA（基于 ggml），单卡 24GB RTX 3090 跑 Qwen3.6-27B，HumanEval/GSM8K/Math500 三个任务上比 autoregressive 平均 1.98× 吞吐，不需重训。配套 z-lab 2026-04-26 发的 Qwen3.6-DFlash 对齐 draft 还在训，AL 还会上升。对低成本部署长上下文 27B 模型的家用/小规模场景给了 vllm 之外的另一条路径。",
        "domain_tag": "推理",
    },
    "https://www.reddit.com/r/LocalLLaMA/comments/1sxsqux/i_got_3_faster_hfq4_prefill_on_strix_halo_in/": {
        "tldr": "hipfire（RDNA 导向的 LLM 推理引擎）新增 HFQ4-G256 的 MMQ 专用 prefill kernel：以前走通用量化 matmul 路径，Strix Halo 上 prefill 约 310–340 tok/s；新 opt-in MMQ 把工作打成 tiled 量化矩阵乘、预量化激活复用，作者实测 3× 提升。AMD 消费级芯片推理栈 kernel 侧的实际进展，跟 ROCm 生态对标 CUDA 栈 MMQ 路线又近一步。",
        "domain_tag": "推理",
    },
    "https://fergusfinn.com/blog/fast-sglang-starts/": {
        "tldr": "SGLang 冷启动加速 70×：针对 serverless/弹性场景频繁拉起实例的首次加载耗时做系统级优化。文章会涉及 weight loading、CUDA context init、kernel pre-compilation 等常见冷启动热点。对 serverless 推理/多租 GPU 池的部署形态直接相关。",
        "domain_tag": "推理",
    },
    "https://github.com/glama-ai/lightport": {
        "tldr": "Lightport 开源：由 Glama 基于 Portkey fork 而来的 LLM gateway，专注把多家 LLM provider 封成 OpenAI 兼容接口，去除原 Portkey 中 guardrails/billing 等更高层功能，只保留 provider 兼容层并覆盖 80+ provider 的集成测试。面向 MCP 生态作为上游 LLM 入口的基础设施组件。",
        "domain_tag": "agent",
    },
}

# 构造输出
new_sections = {"papers": [], "code": [], "blogs": [], "community": []}
kept_count = 0
for section_name, items in raw["sections"].items():
    seen_links = set()
    for it in items:
        link = it.get("link", "")
        if link in CURATED and link not in seen_links:
            seen_links.add(link)
            enriched = dict(it)
            enriched["tldr"] = CURATED[link]["tldr"]
            enriched["domain_tag"] = CURATED[link]["domain_tag"]
            new_sections[section_name].append(enriched)
            kept_count += 1

# generated_at 必须比 raw 新
raw_gen_at = raw.get("generated_at", "")
now_iso = datetime.now(timezone.utc).isoformat()
assert now_iso > raw_gen_at, f"curated {now_iso} 不比 raw {raw_gen_at} 新"

out = {
    "generated_at": now_iso,
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": new_sections,
    "fetch_stats": raw.get("fetch_stats", {}),
    "source": "agent_curated_zh",
}

OUT.write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# stats
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for sec in new_sections.values():
    for it in sec:
        tag_count[it["domain_tag"]] += 1
print(f"curated 总数: {kept_count}")
for sec_name, sec in new_sections.items():
    print(f"  {sec_name}: {len(sec)}")
print(f"domain_tag: 推理 {tag_count['推理']} / 训练 {tag_count['训练']} / agent {tag_count['agent']}")
print(f"generated_at: {now_iso}")
print(f"raw_gen_at:   {raw_gen_at}")
