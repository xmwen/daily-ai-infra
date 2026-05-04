"""One-shot: build today_curated.json from today_raw.json with Chinese tldr + domain_tag."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# key: link, value: (tldr, domain_tag)
# 按 link 去重，跨分区只留最高 score 的那条保留在 papers
picks = {
    # ===== papers =====
    "https://arxiv.org/abs/2505.11329": (
        "TokenWeave v5 针对 vLLM/SGLang/TensorRT-LLM 默认关闭 TP 通信计算 overlap 的现状：低延迟 serving 下每步 token 数少，传统 decompose+overlap 反而更慢。作者观察通信本身占比随 token 数单调下降，构造仅在通信主导区间启用的自适应 overlap 策略，NVLink 域内 8×H100 TP8 场景默认开启后稳定收益，已对接主流 serving 栈。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00616": (
        "LLM-Emu 为 vLLM 打造 serving-native 模拟器：保留生产 HTTP 入口、scheduler、KV cache、输出后处理全部真实路径，只把 GPU forward 替换为 profile 采样延迟 + 合成 token。两款 GPU、四个模型变体、两种 attention 后端、Poisson/Gamma 到达率全跑通，对比现有 offline/time-warped 模拟器既避免重写调度器也不需要精确算子延迟模型，给 A/B 调度策略提供廉价真实环境。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00528": (
        "SAGA 把 agent workflow 作为调度单元而不是单次 LLM 调用：现有 GPU scheduler 把 agent 每一步当独立请求，丢弃 GB 级中间态使 E2E 延迟膨胀 3-8×。SAGA 用 Agent Execution Graph 预测 tool 调用边界间的 KV cache 复用（达到 Bélády 最优 1.31× 内），加跨 step 状态保活与 workflow 感知批调度，在多租户集群上对 agent 类负载端到端收益显著。跨 cs.DC/cs.OS/cs.LG 三区发表。",
        "agent",
    ),
    "https://arxiv.org/abs/2605.00539": (
        "AGoQ 把分布式训练内存占用砍到底：activation 做 layer-aware 变比特（不同 layer/pipeline stage 分配不同 bit 宽度，近 4-bit 存储），gradient 做 8-bit 存储 + 精度保持的 8-bit All-Reduce 通信。相较已有方案 4bit-act/8bit-grad 收敛慢或掉点的困境，AGoQ 给出同时省显存省通信且收敛可控的组合，Megatron/DeepSpeed 类 ZeRO 栈可直接复用。",
        "训练",
    ),
    "https://arxiv.org/abs/2605.00686": (
        "Megakernel MoE 在单机 fuse 专家计算和 GPU-initiated 通信为一个 persistent kernel 本来是赢单机 collective MoE 的关键，但扩到多机通过 RDMA 后退化严重：8 节点最多 10× 回归。作者追溯到 proxy-based RDMA 传输里 tile 传输与完成信号之间隐藏的 serialization，会强制 fence 排空 NIC 流水线；给出去序列化方案，补齐 MoE megakernel 多机不退化的最后一块。对国产互联栈做多机 EP 路线直接对标。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00519": (
        "Silicon Showdown 实测消费级 70B+ 部署：NVIDIA Blackwell 上 TensorRT-LLM 的 NVFP4 相对优化过的 BF16 有 1.6× 吞吐优势（151 vs 92 tok/s），但要吃到这个收益必须跨过 runtime 约束 + CUDA graph + FA backend + KV cache 布局等复合门槛，作者称为「Backend Dichotomy」。同时与 Apple Silicon 做系统级对比，给出消费硬件跑数据中心级权重的工程套路参考。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00555": (
        "Sim-FA 给异步流水线做 cycle-accurate 模拟器前端：补齐现有学术仿真器对 warp specialization、producer/consumer 时序 overlap、matmul 与 activation 函数算子重叠等 Hopper 级新特性的支持缺口，配套分析模型捕获 workload 特征。对做硅片前架构探索（尤其国产 GPGPU 借鉴 warp specialization 的路线）来说，是直接能用的前端工具。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00320": (
        "VitaLLM 为边端 BitNet 三元权重大模型设计专用加速器：Dual-Core 结构，TINT 核做无乘法三元-INT 投影，BoothFlex 核复用 radix-4 Booth 数通路跑 INT8×INT8 attention 同时兼容三元-INT，避免阵列复制。预测式稀疏 attention 用 leading-one 代替 + 无比较 top-K 剪 KV 提取，把精确 attention 限定在 K 个候选上。head 级流水 + absmax 跨核精度桥接，给端侧 BitNet 推理落地一个完整 ASIC 范本。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.00536": (
        "Tempus 面向 AMD Versal AIE 边端 SoC 的 GEMM 流式框架：现有 SOTA 框架靠空间扩展跨数百核分布 workload，在资源受限 SoC 上会撞物理实现失败、带宽饱和、资源爆表。Tempus 走时间维度扩展保持资源不变，针对 LLM 推理 90% 时间在 GEMM 的客观结构，给自适应引擎架构一个不依赖堆核的 GEMM 加速路径。对 chiplet 小核心多片方向有借鉴。",
        "推理",
    ),
    # ===== code =====
    "https://github.com/vllm-project/vllm/releases/tag/v0.20.1": (
        "vLLM v0.20.1 延续 DeepSeek V4 稳定化线：V4 Base 支持、multi-stream pre-attention GEMM 与可配阈值（VLLM_MULTI_STREAM_GEMM_TOKEN_THRESHOLD 默认调优）、FlashInfer one-sided 通信的 BF16+MXFP8 A2A、PTX cvt 加速 FP32→FP4 转换、head_compute_mix_kernel 集成、megamoe flag 需与 Pure TP 互锁。临时 guard 掉 v0.20.0 刚上的 persistent topk cooperative（TopK=1024 死锁 + RadixRowState inter-CTA init race），本月第 4 次「feature 落地即回滚」。",
        "推理",
    ),
    "https://github.com/kvcache-ai/ktransformers/releases/tag/v0.6.2": (
        "KTransformers v0.6.2 原生对接 DeepSeek-V4-Flash：kt-kernel 新增 MXFP4 MoE 算子直接消费模型原生 E2M1+ue8m0 权重，无需离线转换；CPU/GPU 混推走 SGLang，8×RTX 5090（消费级 Blackwell SM_120）端到端验证；新增 AVX2/AVX-VNNI RAWINT4 MoE 后端，把 kt-kernel 覆盖延伸到没有 AVX-512/AMX 的消费 CPU。对中小团队用消费显卡跑 V4 级 MoE 的路径打通。",
        "推理",
    ),
    "https://github.com/kvcache-ai/ktransformers/releases/tag/v0.6.2.post1": (
        "KTransformers v0.6.2.post1 修复 V4-Flash MXFP4 全 GPU prefill fallback：之前 --kt-gpu-prefill-token-threshold 够低真触发时会 StopIteration/AttributeError 把 TP scheduler 打挂（路径硬编 FP8/INT4 布局）。修复后能识别 MXFP4 并在 256-expert gpu_layer 上重跑 V4 swizzle，跨 prefill chunk 缓存加载。8×5090 threshold=1024 chunked=1024 实测：16k 输入 2011 tok/s，65k 2798，262k 2154 prefill TPS，是长上下文消费集群部署的硬数据。",
        "推理",
    ),
    "https://github.com/langchain-ai/langgraph/releases/tag/1.2.0a6": (
        "LangGraph 1.2.0a6 alpha 继续迭代：stream_events(version=\"v3\") 透传 kwargs，补齐新事件流接口的参数转发路径；同步 bump 依赖组与 notebook 到 7.5.6。是 4/28 node-level timeouts revert 后 1.2 线收敛期的常规维护版。",
        "agent",
    ),
    "https://github.com/triton-lang/triton/releases/tag/gfx950-tutorial-v0.1": (
        "Triton gfx950-tutorial-v0.1 AMD CDNA4 教学 kernel pin 分支快照：LLIR scheduler + amdgcnas，无额外优化，给 ROCm 侧教学与 kernel 开发一个可稳定复现的基线 tag，配合此前 buffer_store inst_offset fold 绕过 hoistVoffsetCompute dominance bug 的方案。",
        "推理",
    ),
    # ===== community =====
    "https://www.reddit.com/r/MachineLearning/comments/1t2zy4h/torchnvenccompress_gpu_nvenc_silicon_as_a_pcie/": (
        "torch-nvenc-compress 把 GPU 上闲置的 NVENC/NVDEC 硬件当 PCIe 带宽倍增器：消费级 4090/5090 砍掉 NVLink 后 P2P 只剩约 30GB/s，双卡 70B 切分会被拖死。库用 NVENC 对 activation 与 KV cache 做视频编码压缩，再通过 PCIe 发小码流，接收端 NVDEC 解回。PCA + 纯 ctypes Video Codec SDK 封装，真实 GEMM+encode workload 上并行路径 overlap 达理论最大值 67%。延续 LLM.265/KVFetcher/CodecFlow 把视频编解码器当张量编解码器的路线。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1t3guzw/llamacpp_mtp_support_now_in_beta/": (
        "llama.cpp MTP（Multi-Token Prediction）支持进 beta，先覆盖 Qwen3.5 MTP，后续模型跟进，合并在即。结合此前逐步成熟的 tensor-parallel 支持，llama.cpp 与 vLLM 在 token 生成速度上的差距会被进一步抹平，对消费级本地推理栈选型影响直接——MTP 是 DeepSeek V3/V4 系原生投机解码的工程基础。",
        "推理",
    ),
    "https://www.reddit.com/r/MachineLearning/comments/1t3hxsy/why_ssms_struggle_in_parameterconstrained/": (
        "OpenAI Parameter Golf 竞赛（10 分钟训练、16MB artifact、25M 参数、8×H100）实证 SSM 相对 Transformer 在参数受限制下结构性吃亏：SSM in_proj 权重 LZMA 压缩比 Attention QKV 差最多 3.26×，直接吃掉压缩参数预算；且在 SP4096 赢的架构改动在 SP8192 目标词表下反转符号。附三个 Mamba-3 Triton kernel 级实验——数值精确的 backward 融合尝试因 SMEM 压力反慢 16%，torch.compile 量化路径也踩坑。是 SSM 工程化落地边界的一手数据。",
        "训练",
    ),
}

# 基础信息从 raw 拷过来并注入 tldr/domain_tag
out_sections = {"papers": [], "code": [], "blogs": [], "community": []}
seen_links = set()

for section_name, items in raw["sections"].items():
    for item in items:
        link = item["link"]
        if link not in picks:
            continue
        if link in seen_links:
            continue  # 跨分区重复只收第一次（优先 papers 分区 score 最高）
        seen_links.add(link)
        tldr, dtag = picks[link]
        enriched = dict(item)
        enriched["tldr"] = tldr
        enriched["domain_tag"] = dtag
        out_sections[section_name].append(enriched)

# 生成时间必须比 raw 新
now_utc = datetime.now(timezone.utc).isoformat()

out = {
    "generated_at": now_utc,
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": out_sections,
    "raw_generated_at": raw["generated_at"],
}

OUT.write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
counts = {k: len(v) for k, v in out_sections.items()}
total = sum(counts.values())
tag_counts = {"推理": 0, "训练": 0, "agent": 0}
for items in out_sections.values():
    for it in items:
        tag_counts[it["domain_tag"]] += 1

print(f"curated total: {total}")
print(f"  by section: {counts}")
print(f"  by domain_tag: {tag_counts}")
print(f"  generated_at: {now_utc}")
print(f"  raw_generated_at: {raw['generated_at']}")
print(f"  picks configured: {len(picks)}, matched: {total}")

# 断言所有 picks 都匹配到
unmatched = set(picks.keys()) - seen_links
if unmatched:
    print(f"  WARN: unmatched picks: {unmatched}")
