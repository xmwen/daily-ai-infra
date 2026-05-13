"""一次性脚本：基于 today_raw.json 写中文 curated。中文引号统一用「」避开 Python 字符串闭合坑。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section, link):
    for it in raw["sections"][section]:
        if it["link"] == link:
            return dict(it)
    raise KeyError(f"not found: {section} {link}")


def add(section, link, tldr, tag):
    it = find(section, link)
    it["tldr"] = tldr
    it["domain_tag"] = tag
    return it


papers = []

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11202",
    "GRIEF：针对 LLM 推理引擎的 greybox fuzzer，把「带时序的多请求 trace」当一等输入，用轻量 oracle 检测崩溃/挂起/性能病态/静默输出腐化，并配合受控重放与 logprob 校验定位 KV cache、batching、prefix sharing、投机解码、adapter、多租户调度等共享状态在并发下才暴露的 serving 层故障——传统单请求 model/safety/API 测试覆盖不到。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.12110",
    "AB-Sparse：长上下文块稀疏 attention 的块大小不能全 head 统一——观察到不同 head 对 block 粒度敏感度差异极大。论文给出 train-free 的逐 head 自适应块大小，按 head 行为挑最合适的 block，在保持精度同时显著减少 KV 加载，命中长上下文 decode 主瓶颈。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11005",
    "DisagMoE：MoE 训练 EP 严重 all-to-all bottleneck，纯靠 FFN/attention overlap 因 attn/FFN 计算-通信比天然失衡仍剩残余 stall。该工作把 MoE 训练做成 attention 与 FFN 解耦的 AF-Pipe（attn-FFN pipe）异构资源池，联合优化模型放置与调度，跨节点带宽受限场景下把通信彻底藏进计算。",
    "训练",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11277",
    "Sieve：现代 MoE 激活专家越来越少而总专家越来越多，形成「少数专家收大量 token + 长尾专家只收 1-2 个 token」的 bimodal 分布。原 PIM 系统按静态规则 offload 内存绑定算子，没考虑负载不均与跨 GPU 通信。Sieve 让 PIM 调度感知专家激活分布与跨 GPU 通信代价，动态决定哪些专家走 PIM、哪些回 GPU，是国产 PIM 芯片对接现代 MoE 的直接方法论。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11335",
    "ChunkFlow：分布式 DiT 推理的分层 offload 依赖「prefetch 隐藏在 per-layer 计算后」假设，但 per-GPU 计算量小或 PCIe 节点上 prefetch 与 all-reduce/all-to-all 共抢 PCIe 时假设失效。论文给出一阶解析模型预测哪些层 prefetch 能被计算覆盖，用 communication-aware 的 chunked prefetching 把 prefetch 与集合通信协同调度。对消费级或非 NVLink 集群部署 DiT/视频模型有直接借鉴。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11999",
    "Power Capping Illusion：四种 attention 架构（GQA/MLA/Gated DeltaNet/Mamba2）在 H200 上 decode 阶段实际功耗仅 137-300W vs 700W TDP——decode 是 memory-bound 跑满 HBM 带宽但远未触达 compute 上限，所以 power cap 永远不会触发，看起来「省电」其实是吞吐被砍带来的副作用。固件级 clock throttling 还会污染吞吐测量。直接锁 SM clock 才能拆解开混淆，给出一套 phase-aware 的 LLM 能耗刻画方法论。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.12464",
    "ScaleSearch：BFP（Block Floating Point）量化默认按块内最大幅值挑 scale，但这对量化误差不是最优。论文用 microscaling 格式的 mantissa 位做细粒度 scale 搜索最小化分布相关误差，可与现有量化流水线组合，对现代 GPU first-class 支持的 microscaling FP4/FP8 是低成本的精度提升。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2510.05497",
    "Forecasting MoE Data Movement：跨 4 个 200B-1000B 大规模 MoE 模型、24000+ 请求做 data-movement profiling，从时间和空间维度提炼 6 条洞见——专家选择虽随机但数据搬运模式可被预测，用于指导多机 MoE serving 的专家放置、KV 路由、跨节点通信调度。给出未来 MoE serving 系统设计的实证基底。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11581",
    "Ada-MK：广告 LLM 推理 ms 级延迟约束下，每 token 上千次 kernel 启动占 14.6% E2E 时延。MegaKernel 把多算子融成一个常驻 kernel 消灭启动开销与 HBM round-trip，但已有手写实现绑死单架构、自动编译又精度不足。该工作用自动 DAG 搜索做 MegaKernel 优化，在 NVIDIA Ada 等资源受限 GPU 上同时拿到 portability 与效率。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2601.21351",
    "AFD Provisioning：Attention-FFN disaggregation（AFD）把状态重 KV-cache 主导的 attention 与无状态算力主导的 FFN 拆开独立扩缩容，但对 attention/FFN 比例配比极敏感——配错就 step-level 阻塞和 device idle。论文在 r-attn-1-FFN 拓扑下给出随机负载（KV 增长 + 完成请求被随机长度 prompt/decode 替换）的解析配比框架。生产 disagg serving 系统直接可用的 sizing 工具。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2604.15408",
    "Dispatch-Aware Ragged Attention（ViT pruned）：token pruning 后序列变短（≤197），FA-2 varlen / PyTorch NestedTensor SDPA 的 host 端 dispatch 开销 ~50µs 反超 GPU 实际计算时间，吞吐节省被 dispatch 吃掉。给出 dispatch floor ~24µs 的轻量双向 Triton attention kernel——把短序列 dispatch 当一等优化目标，对小模型在线推理同样适用。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11733",
    "Position：LLM 推理评测应从「模型/软件问题」升级为「能源-token 生产函数」——把吞吐由 compute-per-token 与 energy-per-token 双天花板共同约束。论文给出维度一致的 Token Production Function 形式化，呼吁把数据中心交付功率/PUE/冷却容量纳入推理 SLO 与定价分析；为大规模部署的成本与碳建模提供可工程化的母题。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2505.05772",
    "Sparse Attn Remap on PIM：现有 PIM 设计对 dense attention 优化，但碰到现代 KV cache 稀疏方法的动态不规则访问就负载失衡。论文用聚类做 sparse attention remapping，把不规则访问重新映射到 PIM 的高内部带宽通道上，恢复 LLM decode 的 PIM 加速比。对国产 PIM/PNM 路线接现代稀疏 KV 直接借鉴。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.12396",
    "NCCLZ：把无损压缩塞进 GPU 集合通信库，但解耦量化和熵编码——量化在 NCCL primitive 上层、熵编码在更下层，避免 MPI-stack 不能用 NCCL、或紧耦合压缩器限制压缩率/灵活性的两难。提供更高的通信-计算 overlap，多机 GPU 集合通信带宽受限场景下进一步缓解 all-reduce 瓶颈。",
    "训练",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.11093",
    "DMI-Lib：把模型内部状态可观测性当一等系统原语而非 hot path 上的旁路。Ring^2 这一 GPU-CPU 内存抽象异步捕获中间张量，配合 policy-controlled host backend 导出，offline batch 推理仅 0.4-6.8% 开销。给 RL training/agent 在线诊断/safety 监控提供低成本的内部张量观测通道。",
    "推理",
))

papers.append(add(
    "papers", "https://arxiv.org/abs/2605.12445",
    "Scalable Packed Layouts（VLA codegen）：Arm SVE 这类向量长度无关 ISA 让单实现适配不同向量长度，但编译期不能固定 tile 与 layout。论文把 vector-length-aware 的 packed layout 与对应编译器扩展集成进 MLIR/IREE，扩展 tiling/fusion/vectorization 与可伸缩向量长度协同。Arm CPU 实测 ML workload 跑赢已有 SVE 实现，对国产 SVE 类 ISA 的 ML 编译栈有直接借鉴。",
    "推理",
))


code = []

code.append(add(
    "code", "https://github.com/NVIDIA/TransformerEngine/releases/tag/v2.15",
    "TransformerEngine v2.15：FlashAttention 4 + MXFP8 attention + QGeGLU 与 GEMM+activation fusion grouped MLP + per-token bias 概率缩放 + NVFP4 权重量化进入 fused Adam optimizer + Manifold-Constrained Hyper-Connections（mHC）Triton kernel + MXFP8 grouped tensor dequant + scaling factor unswizzle。Hopper/Blackwell 训练栈把 FA4 与 NVFP4 训练数值正式落主线。",
    "训练",
))

code.append(add(
    "code", "https://github.com/InternLM/lmdeploy/releases/tag/v0.13.0",
    "LMDeploy v0.13.0：Ascend 后端跟进 Qwen3.5 35BA3B；KV cache **TurboQuant（quant_policy=42）正式合并**，主线第二个推理引擎落地 TurboQuant，与用户 RaBitQ/TurboQuant 研究直连；turbomind 整合 cublasGemmGroupedBatchedEx 给 Qwen3.5 MoE 在 Blackwell 上做 grouped GEMM + memcpy 优化；新增 Anthropic-compatible serving endpoints；kernel block size 可调；引擎 sleep 时拒新请求；InternS2 Preview。",
    "推理",
))

code.append(add(
    "code", "https://github.com/NVIDIA/cutlass/releases/tag/v4.5.0",
    "CUTLASS 4.5.0：CuTe DSL 新增 block_copy() 把 TMA 与 S2T 拷贝抽象到 block 级，用户不用直接写 multicast 与 2CTA partition；BlockScaled MMA 在 SM120（Spark）上正式支持 MXF8/MXF4/MXF6 混合精度；EFC（epilogue functions）支持 broadcast 与 mode 任意置换（C.remap_modes 子脚本语法）；初始 linter 引入。Blackwell 微缩放精度路径与 epilogue 表达力同步收敛。",
    "推理",
))

code.append(add(
    "code", "https://github.com/vllm-project/vllm/releases/tag/v0.21.0rc1",
    "vLLM v0.21.0rc1+rc2：rc1 把 DeepGEMM _C 改成 per-Python 打包，避免一份 wheel 在多 Python 版本下 import 失败；rc2 在 CUDA 13 平台显式装 nvidia-cutlass-dsl[cu13] extra。v0.21 主线开始追 CUDA 13 + DeepGEMM 内嵌路径，是 vLLM 与 NVIDIA 新栈对齐的过渡 RC。",
    "推理",
))

code.append(add(
    "code", "https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta13",
    "FlashAttention 4 beta13：CuTe Bwd Sm100 不再因 CUDA 12 关掉 2CTA + softcap 在 varlen backward 加 guard + Flex 支持 varlen blocksparsity；FA4 hd256 修非连续 qkv 的 backward layout；Sm100 backward 的 n_block global max 计算修正确保 deterministic；varlen + paging split kv 修正；ROCm Windows build。Blackwell 与 Flex 正交能力组合在 hd256 主路上继续收敛。",
    "推理",
))

code.append(add(
    "code", "https://github.com/deepseek-ai/DeepGEMM/releases/tag/nv_dev_67fc648",
    "DeepGEMM nv_dev_67fc648：把 nv_dev 与 upstream #316 合并，包含 Mega MoE 优化与 benchmark。延续上游 Mega MoE Kernel（dispatch + GEMM pipeline + mchunk M=128 分块）下沉到 NV 路径的工程节奏，是 DSV4 推理 stack 中 MoE GEMM 链路的最新基线。",
    "推理",
))

code.append(add(
    "code", "https://github.com/langchain-ai/langgraph/releases/tag/1.2.0",
    "LangGraph 1.2.0 全家桶发布：langgraph 1.2.0 + checkpoint 4.1.0 + checkpoint-postgres 3.1.0 + checkpoint-sqlite 3.1.0 + prebuilt 1.1.0 同步 bump 至正式版。核心是 durable error-handler 在主机崩溃后 resume + StateGraph 新增 set_node_defaults() + delta channel 强制 max-superstep snapshot + sqlite get_delta_channel_history 改 streaming walk + checkpoint-postgres delta UNION ALL 列别名修复。从 4/28 timers revert 起步、经过 6 个 alpha 收敛的完整曲线终于 land。",
    "agent",
))

code.append(add(
    "code", "https://github.com/openai/openai-agents-python/releases/tag/v0.17.2",
    "OpenAI Agents v0.17.2：修复 OpenAI Conversations reasoning 持久化（#3268）、未知 realtime 工具不再触发自动响应、tracing retry backoff 在 shutdown 时被打断、本地 approval 拒绝原因得到保留、AsyncSQLiteSession 尊重 session 设置、避免空 chat tool 输出。延续 0.17 系列在 sandbox/tracing/sessions 三轴的稳定化收敛。",
    "agent",
))


blogs = []

blogs.append(add(
    "blogs", "https://developer.nvidia.com/blog/how-to-eliminate-pipeline-friction-in-ai-model-serving/",
    "NVIDIA Dev Blog：从训练好的模型到生产 serving 之间常出现 export → engine 编译 → triton serving → 在线指标偏差等多段摩擦。文章从 NVIDIA 自家 stack 视角拆解流水线衔接（TRT-LLM/Triton 等环节）减少返工——典型「serving infra 工程化最佳实践」官方背书，对自研推理栈对位 NV 生态有参考。",
    "推理",
))


community = []

community.append(add(
    "community", "https://www.reddit.com/r/LocalLLaMA/comments/1tbzr64/qwen36_just_stops/",
    "vLLM 跑 Qwen3.6-27B 双卡 dflash 配置（FlashInfer + INT4 + torch_compile + Triton cache）任务中途莫名停止，qwen-code CLI 与 opencode 都能复现。docker compose 给出完整复现镜像（vllm/vllm-openai:nightly-1acd67a795...）。是 vLLM nightly + dflash + Qwen3.6 路径在长任务下的真实 bug 信号点，vLLM/SGLang 用户值得跟进。",
    "推理",
))

community.append(add(
    "community", "https://www.reddit.com/r/LocalLLaMA/comments/1tayu5t/stop_wasting_electricity/",
    "RTX 4090 跑 llama.cpp + Qwen3.6-27B-UD-Q4_K_XL（flash-attn + KV q4_0 + 262K ctx）实测：通过 nvidia-smi -pl 把 power limit 砍到 ~40% 性能几乎不变。和今日 arXiv「Power Capping Illusion」paper 对照——decode 是 memory-bound 跑满 HBM 但远未压满 compute，所以 power cap 砍掉的是 idle 算力而非实际吞吐。社区实测刚好印证 paper 结论。",
    "推理",
))

community.append(add(
    "community", "https://www.reddit.com/r/LocalLLaMA/comments/1tb9b0r/needle_we_distilled_gemini_tool_calling_into_a/",
    "Needle：26M 参数专攻 function-calling 的纯 attention+gating 模型（无 MLP），消费设备 6000 tok/s prefill / 1200 tok/s decode。论点是 tool calling 本质是「检索-装配」（match query→tool name + 提取参数→生成 JSON），不是推理任务，cross-attention 才是合适原语，FFN 在该尺度纯属浪费。预算手机上的 agent 基础设施信号——把 tool call 从大模型里彻底剥离。",
    "agent",
))

community.append(add(
    "community", "https://www.reddit.com/r/LocalLLaMA/comments/1tbv9zg/server_webui_support_continue_generation_on/",
    "llama.cpp PR #22727：server/webui 给 reasoning 模型增加「继续生成」按钮，长 CoT 被截断后可接续而非重新生成，对长 reasoning 与 coding agent 工作流体感优化明显。配合 MTP 即将合入主线，llama.cpp 在「reasoning 友好」方向继续收敛。",
    "推理",
))


curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "source_raw_generated_at": raw["generated_at"],
    "sections": {
        "papers": papers,
        "code": code,
        "blogs": blogs,
        "community": community,
    },
}

OUT.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

total = sum(len(v) for v in curated["sections"].values())
print(f"curated total={total}")
print(f"  papers={len(papers)} code={len(code)} blogs={len(blogs)} community={len(community)}")
tags = {}
for sec in curated["sections"].values():
    for it in sec:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"  domain_tag={tags}")
print(f"  generated_at={curated['generated_at']}")
print(f"  raw_generated_at={raw['generated_at']}")
