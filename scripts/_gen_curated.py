# -*- coding: utf-8 -*-
"""一次性生成 2026-05-28 中文 curated。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
raw = json.loads((ROOT / "cache" / "today_raw.json").read_text(encoding="utf-8"))


def find(section, key_in_title):
    for it in raw["sections"][section]:
        if key_in_title.lower() in it["title"].lower():
            return it
    raise KeyError(key_in_title)


def enrich(item, tldr, domain_tag):
    out = dict(item)
    out["tldr"] = tldr
    out["domain_tag"] = domain_tag
    return out


# ============ papers ============
papers = []
seen_titles = set()


def add_paper(key, tldr, tag):
    it = find("papers", key)
    if it["title"] in seen_titles:
        return
    seen_titles.add(it["title"])
    papers.append(enrich(it, tldr, tag))


add_paper(
    "How Far Can Disaggregation Go",
    "MoE serving 沿「chunked-prefill → P/D 分离 → Attention-FFN 分离 (AFD)」演进，本文系统刻画 AFD 设计空间：把 memory-bound attention 与 compute-bound MoE-FFN 拆到独立 GPU 组后，调度需在 batch 结构、资源比例、跨组通信间共同寻优。给出可量化的设计探索框架，是 MoE 推理后续工程化部署的方法论拼图。",
    "推理",
)
add_paper(
    "SiDP: Memory-Efficient Data Parallelism",
    "针对吞吐导向的离线 LLM 推理，提出 SiDP：在 DP 组内把权重当成「带宽支撑的共享资源」，不再每卡复制权重，从而把 GPU 内存让给 KV cache 撑更大 batch；同时避免 TP/PP 那种细粒度同步对 DP 调度的破坏。H200/B200 + NVLink 实测在 Qwen/LLaMA 上同尺寸卡能跑更大批，是 vLLM 等 serving 栈的可选 DP 增强路径。",
    "推理",
)
add_paper(
    "Nonvolatile Charge-Domain Attention with HZO",
    "用 HZO 铁电存内计算单元 (FCDC) 直接在电荷域跑 attention 的 q/k/v/o 投影与两次 matmul，支持两种部署模式：全替换 vs 仅 KV 协处理器。NeuroSim+ngspice+CrossSim 联合仿真给出投影噪声预算上界，定量评估 Qwen/LLaMA/Mixtral 上的端到端可行性。是 PIM 路线落地 attention 的具体器件-架构联合方案。",
    "推理",
)
add_paper(
    "GQLA: Group-Query Latent Attention",
    "MLA 训练出的权重只暴露 MQA-absorb 一条解码路径，强绑 H100 算/带宽比，在 H20 等阉割卡上既无法 head 轴张量并行也吃不到 MTP 收益。GQLA 在不改训练目标的前提下让同一份权重等价暴露两条解码路径：MQA-absorb（H100 友好）+ GQA per-group expand（commodity GPU 友好），把硬件适配性下沉到推理时选路。DeepSeek 系 KV 低秩注意力的硬件可携性补丁。",
    "推理",
)
add_paper(
    "Heterogeneous Parallelism for Multimodal",
    "多模态训练中视觉/语音 encoder 与 LLM 主干并行需求差异巨大，统一 TP/CP/PP/DP/EP 切分会让 encoder 被 LLM 拖累、长上下文下尤其严重。本文提出异构并行抽象：端到端图里不同模块可独立选择切分策略并自动衔接通信，避免 encoder 强行继承 LLM 的 sharding 与 placement。Megatron-LM 体系下多模态预训练的关键工程范式。",
    "训练",
)
add_paper(
    "Hurwitz Quaternion Multiplicative",
    "提出 HQMQ：免校准 KV cache 压缩，把 KV 的 4 元素块当作四元数，方向量化为 q_p·q_s 乘积——q_p 取 Hurwitz 24-cell 顶点组、q_s 来自每层每头的随机次级码本，得到 24S 等效码字而只存 S 参数。随机初始化即可，端到端 ppl 差异 <1.5%，是面向 INT4 KV 极致压缩的纯代数构造路线。",
    "推理",
)
add_paper(
    "Mitigating Staleness in Asynchronous Pipeline",
    "异步 PP 通过填满气泡换吞吐，但 gradient staleness 随流水线深度线性增长，把可扩展性反向吃掉。作者将其归因于 Hessian 本征基与标准坐标的错位，提出「基旋转」对延迟梯度做几何对齐。给大规模异步 PP 训练提供了一个不靠加 buffer、纯优化几何角度的失速治理方案。",
    "训练",
)
add_paper(
    "Range, Not Precision: Block-Floating",
    "FP16 跑 FFT/SAR 一直被认为精度不够——本文在 Apple Silicon 上实测证明：FP16 的真正瓶颈不是 10 位尾数而是 5 位指数动态范围，朴素 FP16 SAR pipeline 因匹配滤波幅值放大 5e6× 直接溢出成 NaN。改用 block-floating-point 半精度即可保住 SQNR 56-61dB 且不溢出。对 GPU/TPU 低精度数值实践有方法论价值，FFT 类算子可借鉴。",
    "推理",
)
add_paper(
    "OpenURMA: A Clean-Room Open Implementation",
    "数据中心 RDMA 实际瓶颈在 NIC 而非链路：QP-over-PCIe 抽象让每 (app, endpoint) 连接状态吃几百 MB、64 字节操作付四趟 PCIe 往返。华为 Unified Bus (UB) 2025 公开规范用「per-app endpoint 状态与 per-host transport 状态解耦 + CPU 原生 load/store 到片上总线控制」替代 QP 抽象。OpenURMA 是其干净房间开源实现，是昇腾系互联协议的可观察落地点。",
    "推理",
)
add_paper(
    "Regression Language Models for Code",
    "用单个冻结的 LLM encoder（300M T5Gemma）做 code-to-metric 回归：直接从源码文本预测 Python/C++ 内存占用、Triton GPU kernel 延迟、ONNX 神经网络精度与速度。Spearman > 0.9，免特征工程。是 cost model / autotune 路线里「让 LLM 当性能模型」的扎实样本，对 Triton/CUTLASS 选型有借鉴价值。",
    "推理",
)
add_paper(
    "UNIQUE: Universal Top-k Sparse Attention",
    "Top-k 稀疏 attention 难点是给 KV page 重要性既准确又便宜地打分。UNIQUE 在 KV page 粒度上用「该页 keys 的均值作为代表向量 + 标准差作为偏置项」组合算 importance，同时支持 training-free 与 sparsity-aware training。vLLM + FlashInfer 体系长上下文解码可直接受益的一类轻量稀疏路径。",
    "推理",
)
add_paper(
    "Grounded Cache Routing",
    "RAG 部署的 output-level 语义答案缓存很脆——相似 prompt 答案可能不同、检索证据会漂移、对抗 collision 还能劫持缓存。GroundedCache 把问题重写为「何时复用是安全的」而非「如何复用更快」：用 evidence-grounded 路由判定。是 prefix KV reuse / LMCache / CacheBlend 之外的输出级缓存安全框架。",
    "推理",
)
add_paper(
    "When NPUs Are Not Always Faster",
    "首篇系统刻画移动端 LLM 推理 CPU-NPU 异构 SoC 的 stage 级分解：用 OPMASK 把通信/量化/计算开销隔离测量。反直觉结论：CPU 在计算密集的 Prefill 阶段反而比 NPU 快最多 1.6×，NPU 在内存密集的 Decode 阶段只提供 1.05-1.2× 收益。对端侧 LLM 部署的算子分派策略有直接指导意义。",
    "推理",
)
add_paper(
    "A Paired Testing Protocol for Batch-Conditioned",
    "把「serving 配置」当成可控变量做安全评测：同一 prompt 单独跑 / 同步 batch / 连续 batch 调度结果可能不同。提出配对测试协议含四组研究（本地发现+ scorer 校正、跨模型泛化、连续 batch 组合、batch-invariant kernel 消融）。给 vLLM 等 serving 栈下的安全/鲁棒性评估提供了方法论模板。",
    "推理",
)

# ============ code ============
codes = []
for key, tldr, tag in [
    (
        "v0.19.1",
        "DeepSpeed v0.19.1 发布。亮点：ZeRO-3 通过 mori 走 SDMA allgather（sdma_allgather）；singleton MoE collectives 优化；自动检测 CUTLASS 用于 EvoformerAttention；修复 ZeRO-3 在 plain dict _parameters 模块上的前向崩溃；FastFileWriter 关闭 aio_fd 防 fd 泄漏；配置化 torch-latest 依赖。MoE 训练栈集体通信的细粒度迭代。",
        "训练",
    ),
    (
        "CUTLASS 4.5.1",
        "CUTLASS 4.5.1：CuTe DSL 集中 bug 修复（7 个 issue），修 Jax int64 stride 整除问题；补全 SM120 blockscaled MMA 缺失的 MXFP8MMAOP/MXF8F6F4MMAOP；修 SM100 F8F6F4 SS MMA traits；tensor fill 加 UE8M0 初始化；新增 cvt.rn.bf16x2.e4m3x2；example 93 给 Blackwell 低延迟 GQA 加上 paged KV cache。Blackwell FP8/低延迟 GQA 收口阶段。",
        "推理",
    ),
    (
        "v0.3.11-rc1",
        "Mooncake v0.3.11-rc1 加 pre-release CI：tag 触发，镜像三条正式 release pipeline（CUDA 12 / 非 CUDA / CUDA 13），跑 twine check 但 wheel 仅作为 workflow artifact 不发 PyPI；正式 release 用「tag 含连字符就跳过」的规则避免 pre-release 误发。KV transfer 体系的发布工程基础设施补强。",
        "推理",
    ),
    (
        "v0.22.0rc2",
        "vLLM v0.22.0rc2：修复早期 CUDA 初始化问题（#43791）。v0.22.0 候选版迭代周期内的发布稳定性补丁。",
        "推理",
    ),
    (
        "v0.22.0rc3",
        "vLLM v0.22.0rc3：修复多 API server 启动的硬编码超时（#43768）。配合最近的 multi-API-server 重构修启动竞态。",
        "推理",
    ),
    (
        "v0.22.0rc1",
        "vLLM v0.22.0rc1：MRV2 修复 spec decode 场景下 KV connector 的处理（#43719）。MTP/Spec decoding 与解耦 KV 之间的边界 bug 收尾。",
        "推理",
    ),
    (
        "Nightly Release v0.6.12-20260528",
        "FlashInfer v0.6.12 nightly（dev20260528）：连续日构建，承接 V0.6 系列里 SM120 W4A16 MoE / MLA decode / paged FP8 等近期重要 PR 的集成测试通道。",
        "推理",
    ),
    (
        "fa4-v4.0.0.beta15",
        "FlashAttention 4 beta15：mask 构造函数化以支持 mask 子类化；构建侧 abi3 tag 切 cp310、最低 Python 升到 3.10；CuTe/Flex/SM100 加 vectorized mask_mod；SM103 架构断言更新；显式把 sm_110 纳入 Blackwell-family 门控（用 is_family_of 统一 sm_90/sm_103 判定）。SM10x/11x Blackwell 家族适配收口。",
        "推理",
    ),
    (
        "Nightly Release v0.6.12-20260527",
        "FlashInfer v0.6.12 nightly（dev20260527）：与 20260528 配套的连续构建，便于按日 bisect SM120 W4A16/MLA decode 路径回归。",
        "推理",
    ),
]:
    it = find("code", key)
    codes.append(enrich(it, tldr, tag))

# ============ blogs ============
blogs = []
for key, tldr, tag in [
    (
        "NVIDIA Blackwell Sets STAC-AI Record",
        "NVIDIA Blackwell 在金融行业基准 STAC-AI 上刷新 LLM 推理纪录。是 Blackwell + TensorRT-LLM 在长上下文金融文本分析这类生产 workload 上的官方性能背书，对券商/量化的本地化部署选型有参考价值。",
        "推理",
    ),
]:
    try:
        it = find("blogs", key)
        blogs.append(enrich(it, tldr, tag))
    except KeyError:
        pass

# Google Research 那条是零信任聚合，与本看板无关，丢弃。

# ============ community ============
communities = []
for key, tldr, tag in [
    (
        "AI-generated CUDA kernels silently break",
        "NVIDIA SOL-ExecBench (235 个生产 CUDA kernel) 上得分最高的 AI 生成 kernel 被放进真实训练 loop 后 loss 直接发散：fused embedding-grad + RMSNorm backward 在均匀采样下 OK，真实数据分布下崩；换 AdamW 又掩盖。说明 benchmark verifier 通过 ≠ 生产可用。AI 生成 CUDA kernel 上生产前必须用真实分布+真实优化器复现的硬教训。",
        "推理",
    ),
    (
        "Cross-Platform Fused MoE Dispatch in Triton",
        "TritonMoE：纯 OpenAI Triton 写的 MoE 推理 kernel，跨 NVIDIA/AMD 零厂商代码改动。fused gate+up GEMM 共享 tile load 同时算两路 SwiGLU 投影，消除 35% global memory traffic；A100 上 inference batch ≤512 token 时达到 Megablocks 89-131% 吞吐，同 kernel 直接跑 MI300X；2048+ token / 64+ experts 极端 skew 下回落。给 vLLM/SGLang 的 MoE backend 多硬件统一提供新参照。",
        "推理",
    ),
    (
        "Pushing memory bound CUDA kernels past the speed of light",
        "博文：用数据压缩把 memory-bound CUDA kernel 推过「光速线」（DRAM 带宽极限）。思路是 kernel 内 on-the-fly 解压让有效带宽 > 物理带宽，对量化推理 / KV cache 加载等带宽墙场景有直接借鉴价值。",
        "推理",
    ),
    (
        "Zai replaced the network architecture running GLM-5.1",
        "Zai（智谱）千卡 GLM-5.1 推理集群把网络架构从 ROFT 换成自研 ZCube（与清华+HarnetsAI 合作）：交换机+光模块成本 -33%、GPU 推理吞吐 +15%、P99 首 token 尾延迟 -40.6%。核心针对 Prefill-Decode 解耦推理下 KV cache 跨节点搬运形成的高度不对称流量——ROFT 适合训练流量、PD disaggregation 需要新拓扑。是大规模 PD 解耦推理落地中网络层的实证样本。",
        "推理",
    ),
    (
        "Vulnerability found in framework used by VLLM",
        "vLLM、多个 MCP server 及若干 LLM 工具共同依赖的一个底层框架被披露漏洞。提醒所有用 vLLM/自托管 MCP 的生产环境检查依赖版本并升级。",
        "推理",
    ),
    (
        "Question: Llama cpp, whats good right now for: MTP, KV cache quant, Long context",
        "社区 llama.cpp 现状盘点：mainline + Q4 KV cache 上下文一上来速度从 60 tk/s 跌到 20 tk/s；Indras-Mirror/llama.cpp-mtp 分支跑 Qwen 3.6 27B Q4 在长上下文下能稳定 60 tk/s。是 MTP + KV 量化 + 长上下文三个工程点在 llama.cpp 生态里的实测交叉验证。",
        "推理",
    ),
    (
        "Krasis update: Qwen3.6-35B-A3B",
        "Krasis v1.0：把不入 VRAM 的模型从系统 RAM 高效流式过 VRAM，并把 Prefill/Decode 当成两套独立架构和 use case 单独优化。8GB 3070 Mobile 笔记本 + 32GB RAM 跑 Qwen3.6-35B-A3B Q4 达到「阅读速度」(12.48 tg)；5090 32GB 跑 35B A3B 到 124.9 tg、80B Coder-Next 到 88.6 tg。轻量、面向 weight-streaming + PD 分治的本地 runtime。",
        "推理",
    ),
    (
        "Qwen3.6-35B-A3B-APEX",
        "spiritbuun 的 llama.cpp 分支提供 NVIDIA 专属 CUDA 优化（fused MMA fix、TurboQuant、fattn 改进）+ mudler 的 APEX I-Compact 量化，让 17.3GB 的 Qwen3.6-35B-A3B 在 RTX 3060 12GB 上以 128K ctx 跑出 37 tk/s gen（72k ctx 已填），PPL 3.25。是消费级显存 + MoE 大模型组合的极限工程样本。",
        "推理",
    ),
]:
    try:
        it = find("community", key)
        communities.append(enrich(it, tldr, tag))
    except KeyError:
        pass

# 注：Colour Memory MCP / SEO Skills / jensenify-mcp / favorite MCP server 等
# 属于 agent 应用层（不是 agent 系统基础设施），按筛选偏好直接丢弃。
# r/MachineLearning 的 NeuroFlow / Q-Judger / LocateAnything / Western SOTA / Stress
# 也属于纯算法/评测/无关话题，丢弃。

out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {
        "papers": papers,
        "code": codes,
        "blogs": blogs,
        "community": communities,
    },
    "fetch_stats": raw.get("fetch_stats", {}),
}

dest = ROOT / "cache" / "today_curated.json"
dest.write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"papers={len(papers)} code={len(codes)} blogs={len(blogs)} community={len(communities)}")
print(f"Saved: {dest}")
