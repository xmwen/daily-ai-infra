# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成 today_curated.json（中文 tldr + domain_tag）。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
CURATED = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 按 link 建索引，方便按 link 挑选
def find(section, link_substr):
    for it in raw["sections"].get(section, []):
        if link_substr in it["link"]:
            return it
    return None

picks = []

# ===== code =====
it = find("code", "vllm/releases/tag/v0.20.1")
if it:
    it = dict(it)
    it["domain_tag"] = "推理"
    it["tldr"] = (
        "vLLM v0.20.1 在 v0.20.0 基础上做 DeepSeek V4 稳定化与性能补强：引入 multi-stream "
        "pre-attention GEMM 并加 knob/默认阈值 VLLM_MULTI_STREAM_GEMM_TOKEN_THRESHOLD、"
        "FlashInfer 单边通信补 BF16/MXFP8 all-to-all、PTX cvt 做 FP32→FP4 快速转换、"
        "集成 head_compute_mix_kernel 优化 head 计算，同时 Pure TP 下守护 megamoe 开关、"
        "修复 persistent topk TopK=1024 协同死锁与 RadixRowState CTA 间 init race（临时禁用）。"
        "延续了最近「feature 落地即回滚」的节奏——v0.20.0 里刚上的 persistent topk 这里就被 guard 掉。"
    )
    picks.append(it)

it = find("code", "ktransformers/releases/tag/v0.6.2")
# 注意 v0.6.2 和 v0.6.2.post1 都包含 v0.6.2 子串，用精确末尾判断
for candidate in raw["sections"]["code"]:
    if candidate["link"].endswith("releases/tag/v0.6.2"):
        it = dict(candidate)
        it["domain_tag"] = "推理"
        it["tldr"] = (
            "KTransformers v0.6.2 把 DeepSeek-V4-Flash 直接接到 kt-kernel MXFP4 MoE 算子——"
            "原生消费模型自带的 E2M1 + ue8m0 权重，省掉离线转换；SGLang 走 CPU/GPU 混合推理路径，"
            "在 8×RTX 5090（消费级 Blackwell SM_120）跑通端到端。另外新增 AVX2 / AVX-VNNI "
            "RAWINT4 MoE backend，把 kt-kernel 覆盖面扩到没有 AVX-512 / AMX 的消费级 CPU，"
            "配套更新 SGLang submodule 带 V4-Flash 支持、SM_120 Triton fallback 与 flashinfer guard。"
        )
        picks.append(it)
        break

for candidate in raw["sections"]["code"]:
    if "v0.6.2.post1" in candidate["link"]:
        it = dict(candidate)
        it["domain_tag"] = "推理"
        it["tldr"] = (
            "KTransformers v0.6.2.post1 补昨天 v0.6.2 的 V4-Flash MXFP4 full-GPU prefill fallback——"
            "之前把路径硬编到 FP8/INT4 layout，只要 --kt-gpu-prefill-token-threshold 低到真会触发，"
            "所有 TP scheduler 立刻 StopIteration/AttributeError 崩掉。修复后显式识别 MXFP4、"
            "重跑 256-expert gpu_layer 的 V4 swizzle 并在 prefill chunk 之间缓存加载。"
            "实测 8×RTX 5090（threshold=1024, chunked=1024）：16k 输入 2011 tok/s、65k 达峰 2798 tok/s、"
            "262k 回落 2154 tok/s，长上下文 prefill 吞吐拐点很明显。"
        )
        picks.append(it)
        break

it = find("code", "triton/releases/tag/gfx950-tutorial-v0.1")
if it:
    it = dict(it)
    it["domain_tag"] = "推理"
    it["tldr"] = (
        "Triton 首次为 AMD gfx950（CDNA4）教学 kernel 打专用 pin 分支 gfx950-tutorial-v0.1："
        "基于 main@19ccc01 叠加 LLIR scheduler、amdgcnas 后汇编工具、"
        "TRITON_ENABLE_AMDGPU_RA_HINTS 寄存器分配 hint 切分，以及 buffer_store 把 per-row N-delta 折成 inst_offset 的 BufferOps 优化——"
        "这是 gfx950-gluon-tutorials 配套的编译栈基线。之前 matmul_4waves tip 里 "
        "hoistVoffsetCompute pass 会让 v6_loop_unroll+LLIR_SCHED 报「Instruction does not dominate all uses」，"
        "在这个分支里该 pass 已从 LLIR scheduler 移除绕开 dominance bug。"
    )
    picks.append(it)

# ===== community =====
for candidate in raw["sections"]["community"]:
    if "persistent_memory_system_for_llms" in candidate["link"]:
        it = dict(candidate)
        it["domain_tag"] = "agent"
        it["tldr"] = (
            "MDA 是一套 agent 持久记忆基础设施，把知识编码为关联实体网络，用 Oja 规则做在线更新（无反传、无 reindex），"
            "检索时通过激活概念图而不是相似度搜索来召回上下文——CPU-first、模型无关，开箱对接 Ollama/OpenAI/Anthropic，"
            "以 MCP server 形式暴露，批处理有 GPU 加速。工程上最值得看的是多 agent 共享同一 MDA 实例：A 学到的东西 B 通过关联遍历"
            "而不是搜索就能拿到，相当于把 agent 之间的知识传递从「检索共享」抽到「激活共享」这一层——"
            "是 RAG 之外另一条 agent memory 工程路径。"
        )
        picks.append(it)
        break

now_utc = datetime.now(timezone.utc).isoformat()

out = {
    "generated_at": now_utc,
    "lookback_hours": raw.get("lookback_hours", 36),
    "source": "curated_from_today_raw",
    "sections": {
        "papers": [],
        "code": [x for x in picks if x["section"] == "code"],
        "blogs": [],
        "community": [x for x in picks if x["section"] == "community"],
    },
}

CURATED.write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

papers = len(out["sections"]["papers"])
code = len(out["sections"]["code"])
blogs = len(out["sections"]["blogs"])
community = len(out["sections"]["community"])
total = papers + code + blogs + community
tags = [x["domain_tag"] for x in picks]
print(f"curated total={total} papers={papers} code={code} blogs={blogs} community={community}")
print(f"domain_tag: 推理={tags.count('推理')} 训练={tags.count('训练')} agent={tags.count('agent')}")
print(f"generated_at={now_utc}")
print(f"raw generated_at={raw['generated_at']}")
