"""一次性脚本：读取 today_raw.json，按筛选偏好生成 today_curated.json。
每条补 tldr（≤80 字中文）与 domain_tag（推理/训练/agent）。
"""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 按 link 匹配，给每条补 tldr + domain_tag
CURATED = {
    # ======= papers =======
    "https://arxiv.org/abs/2604.18616": {
        "tldr": "ARGUS 用 data-flow invariants 作为编译期规范，让 coding agent 协同优化 tiling/shared-mem/流水线，弥补 GPU kernel 生成的稀疏 pass/fail 反馈；给 MoE/attention 等关键算子提供结构化诊断信号。",
        "domain_tag": "agent",
    },
    "https://arxiv.org/abs/2604.19241": {
        "tldr": "UniEP 把 MoE expert parallel 拆散的通信压缩、计算通信 overlap 统一到一个 megakernel 里，兼顾数值稳定性，目标是让 Megatron-LM 能产品级接入，而不是堆 ad-hoc kernel。",
        "domain_tag": "训练",
    },
    "https://arxiv.org/abs/2604.19004": {
        "tldr": "Ocean 质疑 SpGEMM 两趟 workflow 里 symbolic pass（占 28% 时间）的必要性，用估算取代精确符号阶段，在 H100 上加速稀疏矩阵乘；对稀疏 MoE/GNN kernel 有直接参考价值。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2505.16968": {
        "tldr": "CASS 放出 6 万对 CUDA↔HIP、SASS↔RDNA3 验证过的 host-device 代码对，训出跨架构转译模型，CUDA→HIP 88.2% 正确率，显著优于 GPT-5.1 / Claude-4.5 / Hipify。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.19337": {
        "tldr": "POLAR-PIC 针对 Matrix Processing Unit 重构 PIC 场插值为外积形式，物理有序粒子布局减少不规则访存；是 MPU 类硬件（PIM 近亲）做 co-design 的范式参考。",
        "domain_tag": "推理",
    },
    "https://arxiv.org/abs/2604.18909": {
        "tldr": "ChipLight 协同设计 chiplet + 光互连集群：package 内高带宽 scale-up、package 间光链路 scale-out，联合优化架构/并行/拓扑，面向大规模 LLM 训练通信瓶颈。",
        "domain_tag": "训练",
    },
    "https://arxiv.org/abs/2604.19181": {
        "tldr": "YAIFS 把 MCP（Model Context Protocol）作为 agent 与仿真环境的标准交互层，让异构 agent 能统一 observe/control 分布式仿真；对 MCP 在 runtime 侧的集成模式有参考意义。",
        "domain_tag": "agent",
    },

    # ======= code =======
    "https://github.com/pytorch/pytorch/releases/tag/trunk%2F0274ad69c3effaef66b5776db5f752b6cf7d8154": {
        "tldr": "PyTorch Inductor 修复 combo kernel 的 optimize_mem 未透传 bug：之前被 cached_autotune 默认设为 True，现在按 is_inference/is_backward 正确传入，和独立 kernel 的行为对齐。",
        "domain_tag": "推理",
    },
    "https://github.com/pytorch/pytorch/releases/tag/trunk%2F89ed986a77847a4cec520920f6d27baa72102995": {
        "tldr": "PyTorch Inductor combo kernel 的 jit_line 改用 triton_meta_common() 统一生成 disabled 元信息，减少 combo/standalone kernel 之间 Triton meta 生成路径的分叉。",
        "domain_tag": "推理",
    },
    "https://github.com/pytorch/pytorch/releases/tag/trunk%2F9c406e3429630d5c45ba57d2fd987177e12bb676": {
        "tldr": "PyTorch 为 Tag.out 自定义算子自动生成 fake kernel：按声明顺序返回 out= 参数，省掉用户手写 meta kernel；对做自定义算子接入 Inductor/torch.compile 的同学省事。",
        "domain_tag": "推理",
    },
    "https://github.com/pytorch/pytorch/releases/tag/trunk%2F50294ed45005ceb3b8669c68b408236e3f06d6b1": {
        "tldr": "PyTorch MPS 后端把 BatchNorm3d 的 5D 张量 reshape 成 4D 再调 MPSGraph normalization，M4 Pro 上 fwd+bwd 从 8.7ms 降到 3.5ms（2.4x），吃的就是 MPSGraph 对高维张量不友好这个坑。",
        "domain_tag": "推理",
    },
    "https://github.com/langchain-ai/langgraph/releases/tag/1.1.9": {
        "tldr": "LangGraph 1.1.9 修了一个 bug：plain resume 场景下 ReplayState 不该传播到 subgraph，否则会串状态。属于 agent runtime 里 checkpoint/resume 语义边界的清理。",
        "domain_tag": "agent",
    },
    "https://github.com/openai/openai-agents-python/releases/tag/v0.14.4": {
        "tldr": "OpenAI Agents SDK 0.14.4 加 BoxMount 支持，重构 sandbox 临时 mount 生命周期 / tar exclude 参数 / session helper；对 computer-use agent 的沙箱 runtime 细节有直接影响。",
        "domain_tag": "agent",
    },
    "https://github.com/flashinfer-ai/flashinfer/releases/tag/nightly-v0.6.8-20260421": {
        "tldr": "FlashInfer v0.6.8 nightly：vLLM/SGLang 主用的注意力 kernel 库持续迭代，关注最新 paged-KV / MLA / FP8 路径的性能回归基线。",
        "domain_tag": "推理",
    },
    "https://github.com/llvm/llvm-project/releases/tag/llvmorg-22.1.4": {
        "tldr": "LLVM 22.1.4 发布：下游 Triton/MLIR/CUDA-Clang 依赖的编译器底座补丁更新，做 GPU kernel DSL 的同学升级前按惯例看下 release note。",
        "domain_tag": "推理",
    },

    # ======= blogs =======
    "https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/": {
        "tldr": "Google 提出 ReasoningBank，让 agent 把成功/失败轨迹沉淀成可检索的推理记忆，下次遇到同类任务直接召回策略；属于 agent memory 的工程化方案。",
        "domain_tag": "agent",
    },

    # ======= community =======
    "https://www.reddit.com/r/MachineLearning/comments/1ssdt0z/int3_compressionfused_metal_kernels_r/": {
        "tldr": "独立作者放出 INT3 权重压缩 + INT2 KV cache + 自写 Metal fused kernel，Mac M 系列端侧跑 Qwen 7B；做 Apple Silicon 端侧推理可关注其 Triton GPU 版本跟进。",
        "domain_tag": "推理",
    },
    "https://www.reddit.com/r/MachineLearning/comments/1srz54u/we_opensourced_chaperonethinkinglq10_a_4bit_gptq/": {
        "tldr": "Chaperone-Thinking-LQ-1.0 在 DeepSeek-R1-Distill-Qwen-32B 上跑 4bit GPTQ + QAT 校准 + QLoRA 医学微调，把 60GB 压到 20GB，MedQA 84%；是一条完整量化训练 pipeline 示例。",
        "domain_tag": "训练",
    },
    "https://www.reddit.com/r/LocalLLaMA/comments/1ssilc3/qwen3635b_becomes_competitive_with_cloud_models/": {
        "tldr": "实证：同一个 9B Qwen 模型，只换 agent scaffold（harness）benchmark 就从 19% 拉到 45%；35B 换对 harness 冲进 Polyglot 前十。本地 coding agent 差距可能是 harness mismatch，不是模型本身。",
        "domain_tag": "agent",
    },
}

# 按分区遍历 raw，选出有 tldr 的条目，保留原字段并补 tldr/domain_tag
out_sections = {}
counts = {"papers": 0, "code": 0, "blogs": 0, "community": 0}
domain_counts = {"推理": 0, "训练": 0, "agent": 0}

for sec, items in raw["sections"].items():
    picked = []
    for it in items:
        info = CURATED.get(it["link"])
        if not info:
            continue
        new_item = dict(it)
        new_item["tldr"] = info["tldr"]
        new_item["domain_tag"] = info["domain_tag"]
        picked.append(new_item)
        counts[sec] += 1
        domain_counts[info["domain_tag"]] += 1
    out_sections[sec] = picked

result = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "source": "curated",
    "sections": out_sections,
}

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

total = sum(counts.values())
print(f"[curated] 总 {total} 条 | papers {counts['papers']} / code {counts['code']} / blogs {counts['blogs']} / community {counts['community']}")
print(f"[curated] domain_tag: 推理 {domain_counts['推理']} / 训练 {domain_counts['训练']} / agent {domain_counts['agent']}")
print(f"[curated] generated_at = {result['generated_at']}")
print(f"[curated] raw generated_at = {raw['generated_at']}")
print(f"[curated] saved: {OUT}")
