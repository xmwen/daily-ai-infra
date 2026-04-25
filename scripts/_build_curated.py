# -*- coding: utf-8 -*-
"""一次性生成 cache/today_curated.json。Agent 手写中文 tldr + domain_tag。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def pick(section, source_pred, title_pred, tldr, tag):
    """从 raw.sections[section] 里按 source+title 匹配挑一条，加上中文 tldr 和 domain_tag。"""
    for item in raw["sections"].get(section, []):
        if source_pred(item.get("source", "")) and title_pred(item.get("title", "")):
            item = dict(item)
            item["tldr"] = tldr
            item["domain_tag"] = tag
            return item
    return None


curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}

# ===== code =====
# FlashInfer v0.6.9: SM120 Blackwell fused MoE + FP4 GEMM + MoE routing replay
c1 = pick(
    "code",
    lambda s: s == "FlashInfer",
    lambda t: t == "Release v0.6.9",
    "FlashInfer v0.6.9 发布：为 SM120 Blackwell 新增 b12x 后端的 mm_fp4 与 CuTe DSL fused MoE、FP4 GEMM heuristic；MoE kernel 加 routing_replay_out、SM89 预过滤零占用 tactic，推理端 FP4 落地加速。",
    "推理",
)
if c1: curated_sections["code"].append(c1)

# LangGraph prebuilt 1.0.11: ToolNode 返回 list[Command|ToolMessage]，ToolRuntime 暴露可用 tools
c2 = pick(
    "code",
    lambda s: s == "LangGraph",
    lambda t: "prebuilt==1.0.11" in t,
    "LangGraph prebuilt 1.0.11：ToolNode 现在允许工具直接返回 list[Command|ToolMessage]，ToolRuntime 暴露当前可用工具清单，agent runtime 的工具调用协议更贴近 tool use 底层语义。",
    "agent",
)
if c2: curated_sections["code"].append(c2)

# OpenAI Agents v0.14.6: 示例默认 GPT-5.5、uv 依赖收紧、MongoDB session 文档
c3 = pick(
    "code",
    lambda s: s == "OpenAI Agents",
    lambda t: t == "v0.14.6",
    "OpenAI Agents Python v0.14.6：默认模型升级到 GPT-5.5、放宽 websockets 上限到 <17、收紧 uv 依赖解析、新增 MongoDB 作为 agent session 后端的文档，agent SDK 持久化选项扩展。",
    "agent",
)
if c3: curated_sections["code"].append(c3)

# PyTorch [Inductor] update group combo sub-kernels by metadata fingerprint (revert)
c4 = pick(
    "code",
    lambda s: s == "PyTorch",
    lambda t: "3e4bb17451a6e7fd45147e3b5f4fca2bd03103f9" in t,
    "PyTorch 主干回滚 Inductor 按 metadata 指纹更新 group combo 子 kernel 的改动，说明该策略在 combo kernel 场景下引入了回归，combo 调度仍在快速迭代。",
    "训练",
)
if c4: curated_sections["code"].append(c4)

# PyTorch Skip max_persistent_rblock for combo per_subkernel_blocks
c5 = pick(
    "code",
    lambda s: s == "PyTorch",
    lambda t: "57e7ded57bc36ffe709c2fdf5704b558b23b44c2" in t,
    "PyTorch Inductor：combo 内 per-subkernel blocks 模式下跳过 max_persistent_rblock 约束，避免 combo kernel 在持久化 reduction 上被误裁剪，提升融合 kernel 的可调度性。",
    "训练",
)
if c5: curated_sections["code"].append(c5)

# PyTorch ROCm FlexAttention target-dependent default forward config
c6 = pick(
    "code",
    lambda s: s == "PyTorch",
    lambda t: "45e9db74900da0ac0549ab69533cfadc74db0c40" in t,
    "PyTorch Inductor 为 ROCm 的 FlexAttention 引入 target-dependent 默认 forward config，AMD GPU 上的 attention 编译路径不再沿用 NV 的调度参数，跨后端性能收敛。",
    "推理",
)
if c6: curated_sections["code"].append(c6)

# PyTorch Auto-generate fake kernels for Tag.out custom operators
c7 = pick(
    "code",
    lambda s: s == "PyTorch",
    lambda t: "7de21d5cf22abd13bfa388da3811a1afcaf8f4e3" in t,
    "PyTorch：为打了 Tag.out 的 custom operator 自动生成 fake/meta kernel（out= 参数按序返回），用户不再需要手写平凡的 meta 实现，export/编译路径的自定义算子接入成本下降。",
    "训练",
)
if c7: curated_sections["code"].append(c7)

# PyTorch Revert cuBLAS(Lt) thread-local workspace maps
c8 = pick(
    "code",
    lambda s: s == "PyTorch",
    lambda t: "68535d0c7ffbfb8e2094315241b9b84f364734ad" in t,
    "PyTorch 主干回滚 cuBLAS/cuBLASLt 线程局部 workspace map 改动，多线程推理/训练里 cuBLAS workspace 的共享策略仍在权衡 OOM 与正确性。",
    "推理",
)
if c8: curated_sections["code"].append(c8)

# PyTorch PGNCCL Symmetric Memory IntraNodeComm parameterization
c9 = pick(
    "code",
    lambda s: s == "PyTorch",
    lambda t: "0869b243fa8dc23db93d86ca97215b744c3f33b9" in t,
    "PyTorch PGNCCL × Symmetric Memory × IntraNodeComm 测试参数化扩展，节点内对称内存通信（NVL domain 内 allreduce/scatter）的覆盖率提升，分布式训练通信栈稳定性工程。",
    "训练",
)
if c9: curated_sections["code"].append(c9)

# ===== blogs =====
# NVIDIA DeepSeek V4 + Blackwell（偏推理部署基础设施，勉强收）
b1 = pick(
    "blogs",
    lambda s: s == "NVIDIA Developer Blog",
    lambda t: "DeepSeek V4" in t and "Blackwell" in t,
    "NVIDIA 在 Blackwell 和 GPU 加速 endpoint 上适配 DeepSeek-V4-Pro / V4-Flash：聚焦 Blackwell 上 MoE 推理的 kernel/调度栈与 NIM endpoint 部署路径，是推理部署侧的一手工程参考。",
    "推理",
)
if b1: curated_sections["blogs"].append(b1)

# ===== community =====
# Qwen3.6-27B NVFP4+MTP on RTX 5090 via vLLM 0.19 ~80 tps @ 218k ctx
cm1 = pick(
    "community",
    lambda s: s == "r/LocalLLaMA",
    lambda t: "Qwen3.6-27B" in t and "vllm 0.19" in t,
    "Qwen3.6-27B NVFP4+MTP 在单张 RTX 5090 上用 vLLM 0.19.1rc1 跑出 ~80 tps、218k 上下文：NVFP4 量化 + MTP 投机解码 + vLLM 长上下文 paged attention 的组合在消费级 Blackwell 上的实测配方。",
    "推理",
)
if cm1: curated_sections["community"].append(cm1)

# Rose optimizer: stateless, 比 8bit AdamW 还省显存（训练基础设施里的优化器）
cm2 = pick(
    "community",
    lambda s: s == "r/MachineLearning",
    lambda t: "Rose" in t and "Optimizer" in t,
    "Rose 优化器开源：声称无状态、显存低于 8bit AdamW、接近裸 SGD，PyTorch 接口 Apache 2.0。对大模型训练而言是 optimizer state 显存压缩的又一路线候选（需独立验证收敛质量）。",
    "训练",
)
if cm2: curated_sections["community"].append(cm2)


# 统计
counts = {k: len(v) for k, v in curated_sections.items()}
total = sum(counts.values())
tags = {"推理": 0, "训练": 0, "agent": 0}
for v in curated_sections.values():
    for it in v:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1

curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": curated_sections,
}

OUT.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"[curated] total={total} counts={counts} tags={tags}")
print(f"[curated] saved -> {OUT}")
