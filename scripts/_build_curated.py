# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成中文 curated。中文引号用「」避开字符串闭合坑。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
raw_path = ROOT / "cache" / "today_raw.json"
out_path = ROOT / "cache" / "today_curated.json"

raw = json.loads(raw_path.read_text(encoding="utf-8"))

# link → (tldr, domain_tag)
ANNOT = {
    # ===== papers =====
    "https://arxiv.org/abs/2605.13734": (
        "KVServe：首个面向 disaggregated LLM serving 的「服务感知 + 自适应」KV 通信压缩框架。指出 PD 分离与 KV 解耦把 KV 变成跨网络/存储的显式 payload，成为端到端瓶颈，而现有 KV 压缩是静态运行时配置，在 workload mix/带宽/SLO 漂移下会反而增延迟；KVServe 把不同 KV 压缩统一到自适应策略层，按服务上下文动态选档。直接对接 PD-分离推理与 vLLM/SGLang/TRT-LLM 类工程线。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.13784": (
        "Attention Once Is All You Need：把传统 request-driven 推理引擎改成 data-driven「有状态会话」模型——KV cache 随数据增量推进，prefill 离开关键路径，query 延迟变 O(|q|) 与累积上下文无关；并提出 Flash Queries 利用数据到达间空闲 GPU 周期对预注册问题预先求值返回缓存答案，结构上 stateless 引擎做不到。瞄准流式工作负载与 RAG/agent 长会话场景，是有状态 serving 引擎的范式提案。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.13319": (
        "PipeSD：云-边协同投机解码推理框架，针对现有协同推理「顺序生成-通信资源利用率低」+「云端非自回归验证触发僵硬，过早验证或回滚代价高」两个问题，给出 token-batch pipeline 调度把生成和通信重叠 + 自适应 NAV 触发策略；适合端侧 drafter + 云端 verifier 的 LLM 推理部署，对端云协同 LLM 服务的 SLO/隐私/离线鲁棒性场景有工程价值。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.13779": (
        "MinT：面向「百万级 LoRA 策略 × 少量昂贵 base 部署」的托管推理与训练基础设施。不把每个策略 merge 成完整 ckpt，而是 base 常驻 + 导出 LoRA adapter revision 流过 rollout/update/export/eval/serving/rollback；Scale Up 把 LoRA RL 推到 frontier 级 dense+MoE（含 MLA/DSA 注意力路径），把分布式训练/服务/调度/数据搬运封装到服务接口后。直接命中 LoRA 大规模在线 RL 工程化痛点。",
        "训练",
    ),
    "https://arxiv.org/abs/2512.16056": (
        "MMA（Multipath Memory Access）：首个软件定义的多路径 host-GPU 数据传输系统。指出现有 host-GPU 拷贝只走目标 GPU 自己的 PCIe，而多 GPU 服务器内 peer GPU 的 PCIe 与高带宽 GPU 互连其实闲置；MMA 把单路径扩成多路径，对模型权重搬运与 KV cache offload/fetch 的 host-GPU 带宽瓶颈直接补齐——对长上下文 KV offload、消费卡多 GPU 推理路线有直接工程意义。",
        "推理",
    ),
    "https://arxiv.org/abs/2603.07770": (
        "ArcLight：面向 many-core CPU 平台的轻量 LLM 推理架构。指出现有 CPU 推理框架忽略 NUMA 跨节点访问开销，限制了 web 服务器/高端网络设备等多 NUMA core 平台的扩展性；ArcLight 从内存管理、线程调度、精细 tensor 划分三层重做，针对 NUMA 拓扑深度感知调度，是 CPU-only LLM 推理工程值得对照的设计点。",
        "推理",
    ),
    "https://arxiv.org/abs/2603.15854": (
        "FlashSampling：把分类采样融合进 LM-head matmul，从不在 HBM 物化 logits。tile-by-tile 算 logits、加 Gumbel、每行每 vocab tile 只保留一个最大者，最后小 reduction；TP decode 下用流式 P2P 写替代 all-gather 把 GPU 间通信与计算/HBM 加载重叠，最多 8 GPU 近线性。是 LM head 与采样融合的精确版本（exact），与 sampler 旁路重叠通信的工程范式。",
        "推理",
    ),
    "https://arxiv.org/abs/2605.11581": (
        "Ada-MK：自动 DAG 搜索做 MegaKernel，兼顾 portability 与 efficiency，专攻 NVIDIA Ada 类资源受限 GPU。把 decode 阶段每 token 上千次 kernel launch（占端到端 14.6%）融成单个 persistent kernel，避开手调与现有 auto-compile 在 Ada 上的紧耦合/低效问题。对 inference 阶段 launch-bound 工作负载与多代 GPU 共线生产部署直接有用。",
        "推理",
    ),
    "https://arxiv.org/abs/2511.09861": (
        "Lit Silicon：揭示单节点多 GPU LLM 训练中 kernel 级性能波动与 concurrent compute+comm（C3）高度相关，并把根因归到「热不均」耦合 C3 引起 straggler。是 GPU 集群 LLM 训练性能波动与通信计算 overlap 失效的系统级诊断与建模工作，对训练通信优化与硬件供电/温控规划有直接参考。",
        "训练",
    ),
}

# Outlines / vLLM / TRT-LLM 等 code 条目
ANNOT.update({
    "https://github.com/NVIDIA/TransformerEngine/releases/tag/v2.15": (
        "TransformerEngine v2.15：PyTorch 端加入 FlashAttention 4 支持 + MXFP8 attention；fused grouped MLP 路径走 GEMM+activation fusion 增加 QGeGLU 与 per-token bias 概率缩放；fused Adam 加 NVFP4 权重量化；新增 mHC（Manifold-Constrained Hyper-Connections）Triton kernel；MXFP8 grouped tensor 反量化支持等。是 NVIDIA 训练栈把 FA4 + MXFP8 attention + NVFP4 优化器联动的关键节点版本，对 FP8/FP4 MoE 训练流水线有直接收益。",
        "训练",
    ),
    "https://github.com/NVIDIA/cutlass/releases/tag/v4.5.0": (
        "CUTLASS 4.5.0：CuTe DSL 新增 block_copy()，把 TMA 与 S2T copy 多播/2CTA 分区细节封装；BlockScaled MMA 在 SM120（Spark）上支持 MXF8/MXF6/MXF4 混合精度；EFC epilogue 加 broadcast 与 mode permutation（C.remap_modes[:, 0, 1]）支持转置等任意模式重映射，PyTorch 参考评估器同步。是 Blackwell/Spark 上 mixed-precision GEMM 与 epilogue 灵活性的关键能力扩展。",
        "推理",
    ),
    "https://github.com/vllm-project/vllm/releases/tag/v0.21.0rc3": (
        "vLLM v0.21.0rc3：新增 TOKENSPEED_MLA backend，针对 DeepSeek R1 与 Kimi K2.5 类 MLA 模型加专属 attention 后端。DeepSeek/Kimi 这一脉 MLA 推理在主线 vLLM 0.21 节点上获得独立优化后端。",
        "推理",
    ),
    "https://github.com/vllm-project/vllm/releases/tag/v0.21.0rc2": (
        "vLLM v0.21.0rc2：CUDA 13 平台 cutlass-dsl 装包修复（nvidia-cutlass-dsl[cu13] extra），是 0.21 系列把 CUDA 13 与 DeepGEMM 内嵌路线推到 rc 阶段的工程修复。",
        "推理",
    ),
    "https://github.com/dottxt-ai/outlines/releases/tag/1.3.0": (
        "Outlines v1.3.0：跨 model provider（OpenAI、Anthropic 等 API-based 模型）统一异常类到 outlines.exceptions——结构化输出库把 provider 差异收敛到一致错误语义。minor breaking change：原来抓 provider 专属 exception 的代码需迁移。是 constrained decoding 库工程化方向的清理性 release。",
        "agent",
    ),
    "https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta13": (
        "FA4 beta13：ROCm Windows 构建修复、SM100 backward 2CTA 在 CUDA 12 下不再强制关闭、CuTe varlen backward softcap guard、Flex varlen blocksparsity、hd256 非连续 QKV backward layout 修复、SM100 backward deterministic n_block global max 修正、varlen + paged split-KV bug 修复。是 FA4 在 SM100/varlen/Flex/ROCm 多轴一起收敛的稳定版。",
        "推理",
    ),
    "https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11.post2": (
        "FlashInfer v0.6.11.post2：在 hd512+MXFP4×BF16+DCP All-to-All 主线之上的 post 修复版，是 0.6.11 系列继续收敛 trtllm head_dim=512 与 MoE 量化主线的工程小步迭代。",
        "推理",
    ),
    "https://github.com/deepseek-ai/DeepGEMM/releases/tag/nv_dev_67fc648": (
        "DeepGEMM nv_dev_67fc648：合并上游 #316 Mega MoE 优化与 benchmark，DeepGEMM 的 NVIDIA 开发分支与上游 Mega MoE kernel 路径同步；与用户当前 Mega MoE kernel 工程方向直连，是 DSV4 系列推理底层 GEMM 调优的持续节点。",
        "推理",
    ),
})

# community
ANNOT.update({
    "https://www.reddit.com/r/LocalLLaMA/comments/1tc9j6u/mi50s_qwen_36_27b_528_tps_tg_1569_tps_pp_no_mtp/": (
        "MI50 + Qwen 3.6 27B 实测：TP8 不量化 / 不 MTP / 不 DFlash 下，1k prompt 52.8 tok/s TG + 1569 tok/s PP；TP2 不量化也能 ~34 tok/s。基于 vLLM v0.20.1 ROCm 7.2.1 的 gfx906 fork（vllm-gfx906-mobydick）。把 2018 年的老 MI50 推到「Claude Code/Hermes agent harness 可用」档位，是 AMD ROCm 老卡 LLM 推理工程化的关键路径数据点。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1tcc7h5/24_toks_from_30b_moe_models_on_an_old_gtx_1080_8/": (
        "GTX 1080 8GB 跑 30B MoE 24 tok/s：Qwen 3.6 35B-A3B 在 i7-6700+1080+32GB 上 ~24 tok/s @128k，靠 llama.cpp 的 TurboQuant/RotorQuant KV 量化（K=turbo4 V=turbo3）把 KV 塞进 8GB。Gemma 4 26B-A4B + MTP 修正后 24.5 tok/s（关键是用 --override-tensor-draft 把 draft 模型 embedding 锁到 GPU，避免静默落 CPU）。MoE 冷专家 RAM offload + PCIe 流式 + KV 量化是消费级老卡跑 30B MoE 的成熟配方。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1tcpgsv/computeruse_mcp_that_can_control_multiple/": (
        "opendesk：computer-use MCP 服务，AI agent 通过 MCP 在多台机器之间「看-点-输入-导航」，pair 一次后单条会话可控制多机；无云、无登录、无中间服务器，本地网络全加密，Mac/Linux/Windows 开源。computer-use agent 走 MCP 标准把多机控制做成 protocol 级 mesh，是 MCP 协议在 computer use 场景的工程落地样本。",
        "agent",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1tcxb77/nvfp4_kimi26_and_kimi_25_released_by_nvidia/": (
        "NVIDIA 释出 Kimi K2.5/K2.6 NVFP4 量化版本：用 Model Optimizer 把 Moonshot Kimi-K2.6 从原生 INT4 量化到 NVFP4。GPQA Diamond 90.4 vs INT4 baseline 90.9、SciCode 54.4 vs 52.6、τ²-Bench Telecom 98.0 vs 98.2、IFBench 73.9 持平——NVFP4 在万亿级 Kimi 上精度几乎无损，NV 把 NVFP4 推到大模型量化主线的官方背书。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1tcvji7/benchmark_5090rtx_promt_parsing_token_generation/": (
        "RTX 5090 power-level benchmark：在 llama.cpp 上扫 TDP-tg/pp 曲线，发现 5090 把功率限到 400W 左右性能基本不变，与近期 arXiv「Power Capping Illusion」（H200 decode 仅 137-300W vs 700W TDP，cap 永不触发）形成同周完整证据链——decode memory-bound 阶段 GPU 实际能耗远低于 TDP，power cap 在多数 LLM 推理路径下根本触发不到。",
        "推理",
    ),
    "https://www.reddit.com/r/LocalLLaMA/comments/1tckzy2/multitoken_prediction_mtp_for_qwen_on_llamacpp/": (
        "Qwen MTP on llama.cpp + TurboQuant 在 M5 Max 64GB 上落地：Qwen 3.6 27B GGUF 21 → 34 tok/s（+40%），接受率 90%。MTP 与 TurboQuant 同栈组合在 Apple Silicon 上跑通，与用户 RaBitQ/TurboQuant + LMDeploy 主线 KV 量化方向形成跨平台对照——MTP × KV 量化已成消费端 MoE 推理标准配方。",
        "推理",
    ),
})

curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}
seen_links = set()
for section, items in raw["sections"].items():
    for item in items:
        link = item["link"]
        if link in seen_links:
            continue
        if link not in ANNOT:
            continue
        tldr, dom = ANNOT[link]
        new_item = dict(item)
        new_item["tldr"] = tldr
        new_item["domain_tag"] = dom
        curated_sections[section].append(new_item)
        seen_links.add(link)

curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "source": "today_curated.json",
    "sections": curated_sections,
}

out_path.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8"
)

counts = {k: len(v) for k, v in curated_sections.items()}
domain_dist = {"推理": 0, "训练": 0, "agent": 0}
for items in curated_sections.values():
    for it in items:
        domain_dist[it["domain_tag"]] += 1
print(f"curated 写入：{out_path}")
print(f"sections counts: {counts}")
print(f"domain_tag: {domain_dist}")
print(f"generated_at: {curated['generated_at']}")
print(f"raw generated_at: {raw['generated_at']}")
