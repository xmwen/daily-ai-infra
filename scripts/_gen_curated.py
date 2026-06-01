# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成中文 curated（手写筛选）。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with RAW.open("r", encoding="utf-8") as f:
    raw = json.load(f)


def find_paper(title_substr):
    for it in raw["sections"]["papers"]:
        if title_substr.lower() in it["title"].lower():
            return it
    return None


def find_code(source_substr, title_substr=""):
    for it in raw["sections"]["code"]:
        if source_substr.lower() in it["source"].lower() and title_substr.lower() in it["title"].lower():
            return it
    return None


def find_blog(title_substr):
    for it in raw["sections"]["blogs"]:
        if title_substr.lower() in it["title"].lower():
            return it
    return None


def find_community(title_substr):
    for it in raw["sections"]["community"]:
        if title_substr.lower() in it["title"].lower():
            return it
    return None


def annotate(item, tldr, domain_tag):
    if item is None:
        return None
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = domain_tag
    return new


# ============ Papers（推理为主，去重） ============
papers_curated = []

# 1. batch-1 decode 物理 AI 推理 gap
p = find_paper("Memory-Bound but Not Bandwidth-Limited")
papers_curated.append(annotate(
    p,
    "面向机器人/边缘 copilot 等 batch-1 自回归 decode 场景，重新审视\"内存带宽受限\"的传统结论。在 H100/A100/L40S/L4 四卡、3 个 7-8B GQA 模型、上下文 2048-16384 的 44 个有效配置下系统测量：实测带宽利用率与峰值 HBM 带宽差距巨大，瓶颈不仅是带宽而是 kernel 启动开销与 SM 占用率不足。给出 physical AI 推理的真实 roofline 边界，对端侧 LLM serving 部署有直接指导意义。",
    "推理"
))

# 2. Deterministic Inference across TP sizes
p = find_paper("Deterministic Inference across Tensor Parallel")
papers_curated.append(annotate(
    p,
    "解决 TP size 变化导致的 LLM 推理结果非确定性，对 RL 训练（vLLM rollout 与 FSDP train engine TP 不同）尤其关键。根因是浮点不可结合 + 跨 GPU reduction 顺序不一致。提出 TP-invariant kernel：固定 reduction 树结构与累加顺序，让任意 TP size 在贪心解码下输出比特一致。在 vLLM 验证可消除训练-推理 mismatch，开销 < 5%。",
    "推理"
))

# 3. MixFP4
p = find_paper("MixFP4")
papers_curated.append(annotate(
    p,
    "NVFP4 单一 micro-format（E2M1）无法适配所有 block 的统计分布。MixFP4 在 NVFP4 框架内按 block 自适应选择 E2M1 或 E1M2，复用 FP8 E4M3 scale 的符号位编码格式选择，零额外元数据；解码到统一 E2M2 内部表示参与 MMA，保留标准 block-scaled GEMM 执行路径。在 LLM 量化精度上一致优于纯 NVFP4，硬件改动几乎为零。",
    "推理"
))

# 4. ParisKV
p = find_paper("ParisKV")
papers_curated.append(annotate(
    p,
    "长上下文 LLM 推理的 KV cache 检索框架。两阶段：先做基于碰撞的候选选择（GPU 原生），再用量化内积重排估计器精修。百万 token 长度下用 UVA 把 KV cache 卸载到 CPU 内存，按需 top-k 抓取最小化 PCIe 流量。在 long-input 与 long-generation benchmark 上质量持平或优于 full attention，batch=1 长上下文 decode 速度首次匹敌甚至超过 full attention。",
    "推理"
))

# 5. StiefAttention - KV 低秩压缩
p = find_paper("Don't be so Stief")
papers_curated.append(annotate(
    p,
    "针对 KV cache 在 HBM 容量与带宽双重瓶颈的低秩压缩方法。传统做法是 SVD 拟合每头投影矩阵，但 SVD 代理目标无法反映 softmax + value mixing + 后续 decoder 层变换后的端到端误差。StiefAttention 在 Stiefel 流形上学习正交投影基，直接最小化 decoder 层输出重构误差，post-training 即可，比 SVD 路线在同压缩比下质量显著更好。",
    "推理"
))

# 6. Mellum 2 (JetBrains coding-focused MoE) - 包含工程要点
p = find_paper("Mellum2 Technical Report")
papers_curated.append(annotate(
    p,
    "JetBrains 开源 12B MoE 编码模型（64 专家激活 8 个，2.5B active），系统设计含工程亮点：GQA + 4 KV head、3/4 层 Sliding Window Attention、单 MTP 头同时做预训练辅助目标和内置 draft model（推理时直接复用做 speculative decode）、FP8 训练。SWA + MTP + 内置 draft 这套组合直接降低了部署侧的 KV 容量与延迟。",
    "推理"
))

# 7. Kernel Foundry
p = find_paper("Kernel Foundry")
papers_curated.append(annotate(
    p,
    "LLM 自动生成 GPU kernel 的多专家进化框架。流程：专家引导 + 检索增强初始化 → 多岛进化搜索 → 结构化诊断反馈迭代精修；中央经验库累积可复用优化知识，并设防作弊机制阻止绕过 kernel 路径的取巧。比起单轮代码生成，能给出兼顾正确性与性能的 kernel，是把 agent runtime 用在 HPC kernel 自动化的代表作。",
    "推理"
))

# 8. Lossless compression for ML PCIe
p = find_paper("Reducing the GPU Memory Bottleneck with Lossless Compression")
papers_curated.append(annotate(
    p,
    "ML 训练/推理常因数据集超 GPU 显存而依赖 PCIe 按需 tensor 传输形成关键瓶颈。本工作明确把无损压缩集成进 ML pipeline 以避免有损压缩的精度损失与部署复杂度，给出 IBP（Invariant Bit Packing）算法专为最小化 ML 数据传输时间设计；论文系统讨论压缩点位以及对 GPU 执行的最小干扰，对 CPU-offload 与 PCIe-over-RDMA 部署有直接价值。",
    "训练"
))

# 9. Roofline to Ruggedness
p = find_paper("From Roofline to Ruggedness")
papers_curated.append(annotate(
    p,
    "提出 performance ruggedness 分析框架补充经典 roofline：相邻 GEMM 仅在 N 维差 128-element 就能跑出 30% 吞吐差距，roofline 完全看不见。作者主张把整张多维性能曲面当研究对象，把表面纹理拆解成可归因机制，并区分软件可消除的与硬件锁死的成分。这是一套面向 kernel auto-tuning 与编译器后端的新分析方法论。",
    "推理"
))

# 10. Near-Free Parallelism
p = find_paper("Near-Free Parallelism")
papers_curated.append(annotate(
    p,
    "并行 decoding 加速汇报通常把算法 token 利用率与系统多位置执行成本混在一起。本工作引入 Near-Free Parallelism (NFP) 概念：定义为以近零延迟可执行的最大位置数。在 dense FFN / MoE FFN / attention 三类组件上对照 idle-compute baseline 分析，发现 NFP 不只受内存带宽 slack 决定，还受 kernel 粒度 slack 影响，给出从硬件平衡度与实现粒度预测 NFP 边界的原则，对 speculative decoding / Medusa 类工作的真实加速天花板分析很有价值。",
    "推理"
))

# ============ Code ============
code_curated = []

# 11. LMDeploy v0.14.0a1
c = find_code("LMDeploy", "0.14.0a1")
code_curated.append(annotate(
    c,
    "InternLM 推理引擎版本号跨入 0.14 alpha。亮点：FP8 KV cache 量化、turbomind 建模基础设施重构、CUDA 错误集中处理 + 手动 stacktrace、Qwen3.5 MoE lite AWQ、sleep engine 时排空队列、chat completions 接口扩展（token-in/out + 暴露被 routed expert）、按 OpenAI spec 加 AllowedToolChoice、health endpoint 改进、metrics 增加 spec stats、修复 anthropic adapter 与 structured output。一次性把 KV 量化、MoE AWQ、speculative decoding metrics 与 OpenAI 兼容性一起推进。",
    "推理"
))

# ============ Blogs ============
blogs_curated = []

# 12. NVIDIA Vera CPU for agentic workloads
b = find_blog("Vera CPU")
blogs_curated.append(annotate(
    b,
    "NVIDIA 抛出新一代为 agentic workload 定制的 Vera CPU 架构定位：在每一代 AI scaling law 中（pretrain → 后训练 → 推理 → agent），CPU 在 AI Factory 里承担的角色不再是配角而是规划/调度/工具调度循环的核心。文章给出 Vera CPU 在 GB300/GB400 系列与 GPU 协同的 cache 一致性设计与 agent loop 关键路径优化（tool routing、KV 查表、scheduler 决策），是 NVIDIA 把 \"agent\" 概念正式写进硬件 roadmap 的一篇宣言。",
    "agent"
))

# ============ Community ============
community_curated = []

# 13. DeepSeek V4 Flash on DGX Spark - 实战数据
co = find_community("Deepseek V4 flash performance on DGX Spark")
community_curated.append(annotate(
    co,
    "用户实测在 DGX Spark（ASUS GX10 双台用 ConnectX-7 docker 互联）跑 DeepSeek V4 Flash 原生 MXFP8 × MXFP4 模型，最大可塞 1M token KV cache，实际跑 256k 并发；社区合作（local-inference-lab）解决了一周内的部署难题；提到 NVFP4 变体在更高并发下应该更香但等软件成熟。是 Spark + V4 Flash 真机第一手吞吐数据的难得样本。",
    "推理"
))

# 过滤 None
def clean(lst):
    return [x for x in lst if x is not None]

papers_curated = clean(papers_curated)
code_curated = clean(code_curated)
blogs_curated = clean(blogs_curated)
community_curated = clean(community_curated)

curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": {
        "papers": papers_curated,
        "code": code_curated,
        "blogs": blogs_curated,
        "community": community_curated,
    },
    "fetch_stats": raw.get("fetch_stats", {}),
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(curated, f, ensure_ascii=False, indent=2)

# 统计
total = sum(len(curated["sections"][k]) for k in ("papers", "code", "blogs", "community"))
tags = {}
for k in ("papers", "code", "blogs", "community"):
    for it in curated["sections"][k]:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1

print(f"curated total: {total}")
print(f"  papers: {len(curated['sections']['papers'])}")
print(f"  code: {len(curated['sections']['code'])}")
print(f"  blogs: {len(curated['sections']['blogs'])}")
print(f"  community: {len(curated['sections']['community'])}")
print(f"  domain_tag: {tags}")
print(f"  generated_at: {curated['generated_at']}")
print(f"  raw    generated_at: {raw['generated_at']}")
print(f"OK -> {OUT}")
