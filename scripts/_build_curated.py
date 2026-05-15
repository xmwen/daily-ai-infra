# -*- coding: utf-8 -*-
"""一次性 curated 构建脚本：从 today_raw.json 读原文，注入中文 tldr + domain_tag。
   引号统一用中文「」避免字符串闭合坑。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 按 link 去重的 (tldr, domain_tag) 索引
ANN = {}

def add(link, tldr, tag):
    ANN[link] = (tldr, tag)

# === papers (按 link 去重；跨分区 cs.DC/cs.LG/cs.PF/cs.AR/cs.CL 同 link 合并) ===

add("https://arxiv.org/abs/2604.09603",
    "ECHO 把投机解码重构成「预算调度」问题集成进 SGLang，针对高并发下 verification compute-bound 真相。"
    "稀疏置信度 gating 把整 batch 当统一 super-tree 弹性管理，避开静态树的 verification 浪费与动态树的累积误判+kernel 不兼容。"
    "对生产 serving 的投机解码稳态运行直接命中。",
    "推理")

add("https://arxiv.org/abs/2605.13319",
    "PipeSD 云边协同推理 token-batch pipeline 把生成与通信重叠，"
    "并自适应触发云端非自回归验证（NAV）以避免过早验证或代价高的 rollback。"
    "把投机解码从单机集群扩到边-云链路，资源利用率与 NAV 触发时机两条主轴同时优化。",
    "推理")

add("https://arxiv.org/abs/2605.13915",
    "Multi-Scale Dequant（MSD）把 dequant 从 GEMM 关键路径移开——「不把低位权重抬到 BF16，而是把 BF16 激活拆成多个低精度分量」。"
    "针对 Ascend 等解耦计算单元 NPU（dequant 比 matmul 还耗 cycle 致 tensor core 闲置）的根因修复，"
    "FP8/FP4/W4A16 对 KV cache 与权重双双适用，国产 NPU 推理工程直接参考。",
    "推理")

add("https://arxiv.org/abs/2605.15051",
    "用 Little 定律从请求速率推断有效 batch size，把 SD 单请求需求拆成 prefill/draft/verify 的「负载无关 + 负载相关」分量；"
    "首次给出生产 serving 中 SD 加速比随 batch 漂移的可解释延迟模型，"
    "工程上给「何时启用/降级 SD」一个量化决策面。",
    "推理")

add("https://arxiv.org/abs/2511.16964",
    "用 LLM-based 多 agent 系统替代手写 GPU kernel + 编译器调优。"
    "提出一个对比框架，证明 exploit-heavy + error-fixing agents 组合最优；"
    "性能与 token 预算/agent 数量正相关——延续 FACT/KernelBenchX 的「agent 写 infra」母题，"
    "kernel 合成方法论从 paper 走向系统化对比。",
    "agent")

add("https://arxiv.org/abs/2605.14217",
    "PreFT 揭示多 adapter serving 的根本错配：prefill 吞吐高、decode 吞吐低，"
    "提出「只在 prefill 应用 adapter，decode 路径走纯 base 模型」绕开多 adapter decode 退化。"
    "对 vLLM 等 LoRA 多租户 serving 是直接架构启示——优化目标从「参数数」改为「每秒服务请求」。",
    "推理")

add("https://arxiv.org/abs/2605.10905",
    "TLX（Triton Low-level Language Extensions）围绕 MIMW（Multi-Instruction Multi-Warp）暴露 warp-group 粒度编排，"
    "在保留 Triton 块编程范式同时让程序员控制异步硬件单元与同步原语。"
    "可演进的硬件原生 Triton 扩展，对接 SM90/SM100 一类异步 tensor-core 与 TMA 的工业生产路径。",
    "推理")

add("https://arxiv.org/abs/2605.14844",
    "XFP 把权重量化反过来：用户给 per-channel 余弦相似度质量下限，引擎自动决定 codebook size、outlier budget 与逐层 packing，"
    "无 Hessian、无校准数据、无手动 bit-width。每权重矩阵拆成稀疏 fp16 outlier 残差 + 致密子字节 codebook 索引；"
    "Qwen3.5-122B-A10B 上 V2 模式给出 attention/expert 双阈值 quality-targeted 量化的范例。",
    "推理")

add("https://arxiv.org/abs/2605.08913",
    "实测 Apple MPS decode 延迟非单调：跨临近 decoding 配置可突跳 21×，CPU 与 NVIDIA CUDA 后端均无该现象。"
    "异常源于 decode 阶段而非 prefill，且不可仅用内存压力解释。"
    "对 Apple Silicon 上推理引擎调度（KV cache 管理 + decode budget 选择）有直接警示。",
    "推理")

add("https://arxiv.org/abs/2605.14249",
    "EnergyLens 用 einsum 接口捕获 LLM 规格（fusion/parallelism/通信重叠）+ 多 GPU 能耗预测模型，"
    "无需生产级 profiling 即可决策优化优先级与部署配置选择。"
    "对数据中心可持续性与「能效作为一等推理 SLO」的工程化方向直接相关。",
    "推理")

add("https://arxiv.org/abs/2604.25899",
    "Pythia 利用多 agent workflow 的语义可预测性（结构化拓扑限制了 agent 行为），"
    "针对生产 agent serving trace 中 prefix cache 命中率低、调度盲目等瓶颈做架构级优化。"
    "把 agent workload 从「generic traffic」升为「workflow-aware traffic」处理，"
    "与 SAGA/Continuum/MCP Workflow Engine 共同构成 agent-native serving 母题。",
    "agent")

add("https://arxiv.org/abs/2605.14929",
    "Scaled Outer Product（SOP）逐层 PTQ：固定 + 动态 codebook 对、per-block 选择位、有符号 per-block scale、"
    "激活加权余弦选择 + 多选背包敏感层提升 + outlier/稀疏残差矫正。"
    "硬件高效 LUT 输出格式（HIF）在 6 个开源模型族 4.5–6 bpw 下接近无损。"
    "面向「per-layer LUT decode」类硬件后端的 PTQ 工程参考。",
    "推理")

# === code ===
add("https://github.com/vllm-project/vllm/releases/tag/v0.21.0",
    "vLLM v0.21.0 正式版，367 commits/202 contributors。"
    "重大变化：①正式 deprecate Transformers v4（用户须迁 v5）；"
    "②编译要求升 C++20（与 PyTorch 对齐，breaking）；"
    "③KV Offload 完整融合 Hybrid Memory Allocator（HMA）+ scheduler 侧 sliding window group；"
    "④投机解码尊重 reasoning/thinking budget，让 reasoning 模型 SD 行为正确；"
    "⑤Blackwell TOKENSPEED_MLA backend 落地（DSR1/Kimi K2.5 链路）。"
    "本月最强 release 节点信号——v0.20.x「feature 落地即 revert」节奏后第一个完整收敛正式版。",
    "推理")

add("https://github.com/vllm-project/vllm/releases/tag/v0.21.0rc3",
    "vLLM v0.21.0rc3 把 TOKENSPEED_MLA 后端正式接进 DeepSeek-R1 / Kimi K2.5——"
    "Blackwell 上 MLA decode 路径补齐，配合 v0.21.0 正式版的 KV Offload+HMA 完成 V4 frontier MoE 推理 backend 闭环。",
    "推理")

add("https://github.com/vllm-project/vllm/releases/tag/v0.21.1rc0",
    "vLLM v0.21.1rc0 第一个 hotfix 候选，专门收 ROCm CI Stage B gating，"
    "v0.21.0 正式版次日就为 AMD 端补漏——延续 vLLM 大版本 N+1 hotfix 节奏（4 月 v0.20.0→v0.20.1 同款）。",
    "推理")

add("https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11.post2",
    "FlashInfer v0.6.11.post2 小版本修复，接续 v0.6.11 主线（trtllm head_dim=512 + MXFP4×BF16 + DCP A2A）。"
    "FlashInfer 本周第二个 post 修复，nightly 同步 v0.6.11-20260515 跟进。",
    "推理")

# === community ===
add("https://www.reddit.com/r/LocalLLaMA/comments/1tdty58/2_old_rtx_2080_ti_with_22gb_vram_each_qwen36_27b/",
    "2×旧 RTX 2080 Ti 22GB（150W power-limit）跑 Qwen3.6 27B IQ4_XS + f16 KV cache + MTP draft 达 38 tok/s。"
    "再次印证近期 r/LocalLLaMA 的「decode 是 memory-bound、power cap 永不触发」实证（与 Power Capping Illusion paper 链路一致），"
    "MoE+MTP+量化 KV 配方在二手卡级别已成熟。",
    "推理")

add("https://www.reddit.com/r/LocalLLaMA/comments/1tdhcqb/need_a_second_pair_of_eyes_this_qwen36_27b_quant/",
    "用户实测 Qwen3.6 27B INT8 AutoRound（部分层保 BF16）在 AIME 数学上比 UD Q8 K XL「思考更少答案更准」，"
    "再用 llama.cpp PR 把同一配方移植成 GGUF + MTP。"
    "暗示 reasoning 模型量化精度对「关键层 BF16 留白」高度敏感——"
    "量化 recipe 与 reasoning trace 长度的耦合是新的工程优化变量。",
    "推理")

add("https://www.reddit.com/r/LocalLLaMA/comments/1tdpk3f/i_have_even_faster_deepseek_v4_pro_at_home/",
    "用户在 Epyc 9374F + RTX PRO 6000 Max-Q（96GB）单卡用 KTransformers（sglang+kt-kernel）跑 DSV4-Pro，"
    "Q4_K_M depth 0 上 pp512=39.76 tok/s、tg32=7.54 tok/s（含 ttfr）。"
    "继 5/10 antirez 之后第二个家用单卡 V4-Pro 工程化案例——KV cache 仅 7% baseline 的 V4-Flash 与 V4-Pro 已被两个独立栈下放消费卡。",
    "推理")

add("https://www.reddit.com/r/LocalLLaMA/comments/1tdb4ic/a_first_comprehensive_study_of_turboquant/",
    "首份系统对比 TurboQuant 跨 KV cache 配方：FP8（--kv-cache-dtype fp8）2× KV 容量 + 几乎零精度损失，仍是默认最优；"
    "TurboQuant k8v4 仅多 0.4× 容量却带来一致吞吐/延迟负面，不值；"
    "TurboQuant 4bit-nc 在 KV 内存压力大时最实用，但权衡精度/延迟；"
    "k3v4-nc 与 3bit-nc 仅在极端边缘部署中有意义。"
    "用户 RaBitQ/TurboQuant 方向首份外部独立评估，与 5/13 LMDeploy 落地形成完整闭环。",
    "推理")

# 把 annotations 落到 raw 里
out = json.loads(RAW.read_text(encoding="utf-8"))
out["generated_at"] = datetime.now(timezone.utc).isoformat()
out["lookback_hours"] = raw["lookback_hours"]

new_sections = {"papers": [], "code": [], "blogs": [], "community": []}
seen_links = set()

for sec in ("papers", "code", "blogs", "community"):
    for item in raw["sections"].get(sec, []):
        link = item.get("link")
        if link in seen_links:
            continue
        if link in ANN:
            tldr, tag = ANN[link]
            seen_links.add(link)
            new_item = dict(item)
            new_item["tldr"] = tldr
            new_item["domain_tag"] = tag
            new_sections[sec].append(new_item)

out["sections"] = new_sections
out["fetch_stats"] = raw.get("fetch_stats", {})

# 统计
counts = {sec: len(items) for sec, items in new_sections.items()}
tag_counts = {"推理": 0, "训练": 0, "agent": 0}
for sec_items in new_sections.values():
    for it in sec_items:
        tag_counts[it["domain_tag"]] += 1
print(f"curated counts: {counts}, total={sum(counts.values())}")
print(f"domain_tag: {tag_counts}")
print(f"generated_at: {out['generated_at']}")
print(f"raw    generated_at: {raw['generated_at']}")

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved: {OUT}")
