"""一次性 curated 生成脚本（避免手写 JSON 转义）。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = json.loads((ROOT / "cache" / "today_raw.json").read_text(encoding="utf-8"))


def find(section: str, predicate):
    for item in RAW["sections"].get(section, []):
        if predicate(item):
            return item
    return None


def add(item, tldr, domain_tag):
    item = dict(item)
    item["tldr"] = tldr
    item["domain_tag"] = domain_tag
    return item


curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}

# ===== code =====
vllm_v22 = find("code", lambda x: x["source"] == "vLLM" and x["title"].startswith("v0.22.0") and "rc" not in x["title"])
if vllm_v22:
    curated_sections["code"].append(add(
        vllm_v22,
        "vLLM v0.22.0 正式版：459 commits / 230 贡献者。DeepSeek V4 进入成熟阶段——单独抽到 vllm/models/deepseek_v4/ 包，新增 NVFP4 fused MoE、full + piecewise CUDA Graph、MTP 投机解码及 MegaMoE/mhc/Q-norm/indexer/sparse MLA 一组 fused kernel，伴随 ROCm 平价修复与精度回归。Model Runner V2 接近成为默认：oracle 让 Qwen3 dense 默认走 MRv2，并补 sleep-mode 权重重载、update_config 与共享 KV 层。",
        "推理"
    ))

flashinfer_v6 = find("code", lambda x: x["source"] == "FlashInfer" and x["title"] == "Release v0.6.12")
if flashinfer_v6:
    curated_sections["code"].append(add(
        flashinfer_v6,
        "FlashInfer v0.6.12：SM120 W4A16 b12x MoE kernel 落地（Blackwell consumer 拿到 W4A16 大批量解码路径）；Kimi K2.5 H64 CuTe DSL MLA decode 支持；CUTLASS MLA paged attention 加 FP8 输出；TRT-LLM-Gen 新增 dynamic tokens-per-page GQA kernel，per-token NVFP4 量化算子优化，sccache JIT 缓存与 AOT 诊断改善构建体验。MoE/MLA/低比特推理三条主线并行推进。",
        "推理"
    ))

mcp_v1272 = find("code", lambda x: x["source"] == "MCP Python" and x["title"] == "v1.27.2")
if mcp_v1272:
    curated_sections["code"].append(add(
        mcp_v1272,
        "MCP Python SDK v1.27.2：把 transport session 绑定到已认证 principal，experimental tasks 限定到创建它的 session 内，AccessToken 增加 subject 与 claims 字段。这是 MCP runtime 在多租户/会话隔离方向的硬化改动——避免一个会话的工具调用泄漏到另一个 principal，是 agent 系统层面把 MCP 真正搬进生产必须的鉴权基础设施。",
        "agent"
    ))

# ===== blogs =====
dynosim = find("blogs", lambda x: x["title"] == "DynoSim: Simulating the Pareto Frontier")
if dynosim:
    curated_sections["blogs"].append(add(
        dynosim,
        "NVIDIA Dynamo 团队发布 DynoSim：把 LLM serving 的部署调参（model backend、TP 形状、prefill/decode 拆分、worker 数、批策略）抽象成可模拟的设计空间，目标是直接画出 throughput-latency 的 Pareto 前沿，不必每次烧真实集群跑全量扫参。配合 Dynamo 路由器与 PD 解耦，让选型从「经验拍脑袋」变成「模拟器选最优点再落地」，是 serving 调优工程化的官方答卷。",
        "推理"
    ))

# ===== community =====
def comm(title_keyword):
    return find("community", lambda x: title_keyword in x["title"])

monokernel = comm("monokernel for LLM inference on AMD MI300X")
if monokernel:
    curated_sections["community"].append(add(
        monokernel,
        "KOG.ai 发布 MI300X monokernel：把整条 decode 跑成单个 GPU-resident kernel，按 die topology 把内存访问图谱映射到物理布局，CU 按所属 IOD 分组让硬件跑到设计峰值。8x MI300X、batch=1、无投机/无量化的 2B coding 模型上达到 3300 tok/s/请求，单请求吞吐摸到 AMD 推理新天花板。后续打算扩到大型 frontier MoE，是 monolithic kernel 路线对抗 vLLM/TGI 多 kernel 拼接的实证。",
        "推理"
    ))

delayed_tp = comm("Delayed Tensor Parallelism")
if delayed_tp:
    curated_sections["community"].append(add(
        delayed_tp,
        "KOG.ai《Delayed Tensor Parallelism》：传统 TP 在每层 attention/FFN 后都要 all-reduce，跨 GPU 同步是单 token 延迟瓶颈。Delayed TP 把同步推迟到必要点，让计算与通信深度重叠以提升 transformer 单请求推理速度，是配合上面 monokernel 的同源工作——延迟优化派从 kernel 内 / kernel 间两个层面同时压通信开销。",
        "推理"
    ))

real_time_3k = comm("Real-time LLM Inference on Standard GPUs")
if real_time_3k:
    curated_sections["community"].append(add(
        real_time_3k,
        "KOG.ai 总览文：标准 GPU 上做到 3000 tok/s/请求 实时 LLM 推理。HN 205 分热帖，把上面 monokernel + Delayed TP 的整体路线图串起来——单请求超低延迟需要 die topology 感知 kernel + 通信延迟外推 + 全程 GPU-resident，三者缺一不可。代表 latency-first 推理派对抗主流 throughput-first 引擎（vLLM/TGI）的整套方法论。",
        "推理"
    ))

tiny_vllm = comm("Tiny-vLLM")
if tiny_vllm:
    curated_sections["community"].append(add(
        tiny_vllm,
        "Show HN：Tiny-vLLM 用 C++/CUDA 重写一份 minimal vLLM——HN 167 分。教学/可读性优先，把 PagedAttention、continuous batching、KV cache 管理这些 vLLM 核心机制抽到能读懂的代码量内。对想看清现代推理引擎工程拆解的人是好读物，也方便在它上面试新 kernel/调度策略不必啃 vLLM 的 OOP 全家桶。",
        "推理"
    ))

qwen36_quant = comm("Qwen3.6-27B Quantization Benchmark")
if qwen36_quant:
    curated_sections["community"].append(add(
        qwen36_quant,
        "Qwen3.6-27B 全量量化评测：用 llama.cpp 的 perplexity 工具，按 KLD 与 Same-Top-P 双指标比较 unsloth / mradermacher / IQ4_XS / Ununnilium 各家从 Q8 到 Q2 的 GGUF。KLD 比 perplexity 更敏感，能捕捉量化对分布尾部的扭曲，Same-Top-P 直接量化「贪婪解码下 token 选择是否一致」。是 GGUF 量化生态难得的横向对照实验，结论可用来挑本地推理量化档位。",
        "推理"
    ))

# ===== papers =====
# 周末 arXiv 停更，无 papers。

# ===== 写出 =====
out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": RAW.get("lookback_hours"),
    "sections": curated_sections,
    "fetch_stats": RAW.get("fetch_stats"),
}

out_path = ROOT / "cache" / "today_curated.json"
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[curate] saved -> {out_path}")
print(f"[curate] generated_at = {out['generated_at']}")
print(f"[curate] raw      gen = {RAW['generated_at']}")
for sec, items in curated_sections.items():
    print(f"  {sec}: {len(items)}")
total = sum(len(v) for v in curated_sections.values())
print(f"  total: {total}")
tags = {}
for items in curated_sections.values():
    for it in items:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"  domain_tag: {tags}")
