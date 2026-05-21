#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 2026-05-21 raw 生成中文 curated（domain_tag 版）"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"


def find(items, key):
    for it in items:
        if key in it.get("title", "") or key in it.get("link", ""):
            return it
    raise KeyError(key)


raw = json.loads(RAW.read_text(encoding="utf-8"))
papers = raw["sections"]["papers"]
code = raw["sections"]["code"]
blogs = raw["sections"]["blogs"]
community = raw["sections"]["community"]

curated_papers = []
seen_links = set()

def add_paper(item, tldr, tag):
    if item["link"] in seen_links:
        return
    seen_links.add(item["link"])
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    curated_papers.append(new)

# 1. Frontier 推理仿真器
add_paper(
    find(papers, "Frontier: Towards Comprehensive"),
    "面向现代 disagg+复杂并行+stateful（reasoning/agent/RL rollout）serving 的离散事件仿真器，认为 monolithic-replica 抽象+均值代价模型会反转优化结论；Frontier 用 disagg 一等抽象捕获多元拓扑动态，目标是给 SLA 决策级保真度；与 5/5 LLM-Emu / 5/12 Dooly 同母题继续推进 LLM serving 模拟器化。",
    "推理",
)

# 2. NanoCP request-level dynamic CP
add_paper(
    find(papers, "NanoCP"),
    "MoE serving 把 attention 长度延迟与 MoE 通信批大小延迟同绑定到一个实例，会同时引发 EP straggler 与 KV 跨实例碎片化；NanoCP 提出请求级动态 context parallelism——每个请求独立选 CP 度数，按 KV 负载与到达分布解耦 attention/MoE 调度，缓解长 ctx tail 与 EP 不均双瓶颈。",
    "推理",
)

# 3. Multi-node LLM Inference NVRAR
add_paper(
    find(papers, "Multi-node LLM Inference"),
    "GPU 超算多节点分布式推理实测：all-reduce 是主要瓶颈；提出 NVRAR 层级化 all-reduce（节点内 NVLink + 节点间 InfiniBand 树形）+ YALIS 实验引擎，强 scaling 给出真实曲线，对国产芯片多节点 TP+SP 可借鉴的层级集合通信骨架。",
    "推理",
)

# 4. SSV sparse speculative verification
add_paper(
    find(papers, "SSV: Sparse Speculative"),
    "投机解码与动态稀疏 attention 直接组合存在结构错配——投机依赖跨 query 共性、动态稀疏每 query 独立布局，导致 KV block 复用差且 NSA 分支开销放大；SSV 把动态稀疏 attention 改造成 verification-friendly workload，在 H100 上恢复 KV 复用并稳定 verification 策略选择，延续 5/12 SPECTRE/5/15 ECHO/5/20 SpecSA 投机解码×稀疏 attn 母题。",
    "推理",
)

# 5. LlamaWeb WebGPU
add_paper(
    find(papers, "Llamas on the Web"),
    "llama.cpp 的 WebGPU 后端，浏览器端跨厂商 GPU 通用 LLM 推理：静态内存规划+高效模型加载压缩内存开销，模板化 GPU kernel 支持多种量化格式+按设备 tunable kernel 库做性能可移植；浏览器端「私有+便携」推理工程参考。",
    "推理",
)

# 6. Silent Hyperparameter
add_paper(
    find(papers, "The Silent Hyperparameter"),
    "调研 200 个推理引擎 + 35000 篇 ML paper，发现绝大多数论文不报告推理后端，而 vLLM/SGLang 自定义 CUDA kernel+降精度算术会改变 token 概率并引入非确定性，导致 SOTA 1pp 提升被 backend 选择吞没；呼吁 inference backend 列入 first-class 复现性元数据。延续 5/13 GRIEF/5/19 Hawkeye 同母题。",
    "推理",
)

# 7. DODOCO MoE dispatch observatory
add_paper(
    find(papers, "Diagnosing Overhead in Dispatch"),
    "MoE all-to-all dispatch 优化的两个常见假设（routing imbalance 系统层可纠正、mock-token 反映生产 routing）实证检验：在 5 个 MoE checkpoint（DSV2-Lite MLA、DS-MoE-16B、Qwen3-30B GQA、Nemotron-30B Mamba2、Qwen3.5-35B GDN）× 5×6 数据条件下挑战这两条假设，结论对预测 placement/自适应 relayout/层级集合通信/EP-aware topology 四类方案适用边界做出修正。",
    "推理",
)

# 8. PALS power-aware MoE serving
add_paper(
    find(papers, "PALS"),
    "把 GPU power cap 从静态约束升为可控旋钮，与 batch size 等软件参数联合优化 MoE serving 能效；离线 power-perf 模型 + feedback 控制器选配置满足吞吐目标的同时最大化能效，集成入 vLLM。延续 5/13 Power Capping Illusion+RTX power-limit 母题，从「实测发现」走到「runtime 可控」。",
    "推理",
)

# 9. OFU Fleet GPU 效率
add_paper(
    find(papers, "Instant GPU Efficiency"),
    "提出 OFU（Overall FLOP Utilization）GPU fleet 级精度无关效率指标——只用 Tensor Pipe Activity + SM clock 两个片内计数器，无需应用 instrument，跨代次跨精度可用；GEMM 控制实验 H100/GB200 FP16/TF32/FP8/NVFP4 验证 tile 量化校正后 OFU 与应用 MFU 偏差 ≤2pp，对 608 个生产训练任务大规模可观测；与昨日 NVIDIA Fleet Intelligence 形成 fleet-level GPU 观测 1+1。",
    "训练",
)

# 10. Runtime-Certified Bounded-Error Quantized Attention
add_paper(
    find(papers, "Runtime-Certified Bounded-Error"),
    "KV cache 量化通常只做经验验证；提出分层 KV 架构——GPU 存 INT8 K + INT4 V，主机 RAM 留 FP16 原值做确定性回退，运行时按头-步级二项分解给 attention 分布失真+value 重构误差的可证误差界，按界做自适应精度选择与多级回退；为长 ctx KV 量化引入 first-class 正确性证书，与 5/19 VeriCache 一脉。",
    "推理",
)

# 11. TokenCake multi-agent KV serving
add_paper(
    find(papers, "TokenCake"),
    "多 agent serving KV cache 双痛点：函数调用期间空闲 KV 占位浪费 GPU 内存（temporal underutilization）+ 关键 agent KV 被驱逐（spatial contention）；TokenCake 用事件驱动 Temporal Scheduler 主动 offload 空闲 KV、预测式上传隐藏传输延迟，与 agent-aware 调度联合优化，命中 multi-agent serving infra。延续 5/6 Continuum 母题。",
    "agent",
)

# 12. OCTOPUS KV cache
add_paper(
    find(papers, "OCTOPUS"),
    "续 TurboQuant/PolarQuant 的 rotation-preconditioned KV codec 路线：OCTOPUS 联合量化旋转后坐标三元组——用八面体参数化把方向映射到方阵，对方阵两坐标+三元组范数分别做 Lloyd-Max 量化匹配实现端边际，per-triplet MSE 最优给出严格非均匀比特分配。直接命中用户 RaBitQ/TurboQuant 研究方向，5/13 LMDeploy quant_policy=42 落地后路线持续演进。",
    "推理",
)

# 13. PulseCol diffusion LLM column-sparse attention
add_paper(
    find(papers, "PulseCol"),
    "diffusion LLM 推理每步重做 full self-attention 且无 KV cache，现有 block-sparse 只能用在后期；PulseCol 提出周期性刷新的列稀疏 attention，从更早迭代起利用可复用的稀疏 pattern 做细粒度稀疏，提升 dLLM 推理效率，dLLM 系 attention 加速首类做法。",
    "推理",
)

# papers section end ----

curated_code = []
def add_code(item, tldr, tag):
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    curated_code.append(new)

# code: FA4 beta14
add_code(
    find(code, "fa4-v4.0.0.beta14"),
    "FlashAttention 4.0 beta14：修复 num_splits_heuristic 在 empty Q workload 的 ZeroDivisionError、SM90 Cute Flex 修复、SM100 hd256 kernel 支持 zero-length 序列、blocksparse tensor 启用 split-kv、varlen batch 搜索抽到 utils；连续 14 次 beta 持续向「v0.21.0+生产就绪」收敛的边界补漏期。",
    "推理",
)

# blogs: NVIDIA Deep Research Skill on Agent Harnesses
curated_blogs = []
def add_blog(item, tldr, tag):
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    curated_blogs.append(new)

add_blog(
    find(blogs, "Deep Research Skill"),
    "NVIDIA 官方教程：把「专项 deep research skill」加进 agent harness（Claude Code/Codex/LangChain Deep Agents），强调 harness 是 orchestrator 而 skill 是可插拔能力；与 5/20 NVIDIA Verified Skills + 移动端 skill 系统形成「agent skill 作为一等抽象」的官方背书。",
    "agent",
)

# community
curated_community = []
def add_comm(item, tldr, tag):
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    curated_community.append(new)

# c1: ik_llama.cpp 12GB 110 tok/s
add_comm(
    find(community, "110 tok/s with 12GB VRAM"),
    "RTX 4070 Super 12GB 跑 Qwen3.6-35B-A3B：自从 llama.cpp 5/16 合并 MTP PR 后 4070 Super 上 MTP 性能反退到接近 non-MTP；切到 ik_llama.cpp 后 MTP 重新生效 110 tok/s（IQ4_XS 4.19bpw vs Unsloth Q4_K_XL 等精度小 4GB），ik_llama.cpp CPU offloading 优化在 12GB 档拉满；MTP 工程化下沉的「主线 vs ik 分支」差异点。",
    "推理",
)

# c2: StepStone GPU kernel driver fuzzing
add_comm(
    find(community, "StepStone"),
    "Oakland 2026 paper：用 LLM 驱动的 GPU kernel driver fuzzer 通过 user-space 库（CUDA runtime/HIP/oneAPI 等）反向模糊测试内核驱动；agent 写 fuzzer 进入系统软件安全测试栈，与 5/13 GRIEF 推理引擎 fuzzer 母题平行扩展到驱动层。",
    "推理",
)

# c3: KV Cache + Flash Attention interactive diagrams
add_comm(
    find(community, "interactive diagrams"),
    "KV cache + FlashAttention 交互式图解站点：把 GQA、PagedAttention、prefill/decode 算力差异、FA 的 tiling/recompute 都可点击拖拽展示；学习 KV cache+FA 工程语义的轻量参考资料，对面试答疑/onboard 场景实用。",
    "推理",
)

# c4: MoE inference: 15% lower expert load by request reordering
add_comm(
    find(community, "Moe inference optimizations"),
    "Doubleword 工程博客：实测 MoE expert co-activation pattern——在线请求按 expert 共激活相似度重排序，相邻请求批 expert load 不均衡度降 15%，无须改 routing 仅在 batch 调度层动手；与 5/13 RaMP/5/13 Forecasting MoE Data Movement 同母题，给出生产可用的工程化捷径。",
    "推理",
)

# c5: Am I OpenAI compatible
add_comm(
    find(community, "Am I OpenAI compatible"),
    "构建 vLLM/llama.cpp 等开源推理引擎对 OpenAI API 兼容性的现状库——记录已实现签名 vs 缺口，新增 ht-compatibility 与厂商专属扩展；对做 LLM proxy/middleware/agent 编排的工程师列出真实兼容矩阵，避免「号称兼容实际差签名」踩坑。",
    "agent",
)

# Final curated
generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

curated = {
    "generated_at": generated_at,
    "lookback_hours": raw["lookback_hours"],
    "sections": {
        "papers": curated_papers,
        "code": curated_code,
        "blogs": curated_blogs,
        "community": curated_community,
    },
    "fetch_stats": raw["fetch_stats"],
}

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")

# count
total = len(curated_papers) + len(curated_code) + len(curated_blogs) + len(curated_community)
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for sec in (curated_papers, curated_code, curated_blogs, curated_community):
    for it in sec:
        tag_count[it["domain_tag"]] += 1

print(f"curated total={total}")
print(f"  papers={len(curated_papers)} code={len(curated_code)} blogs={len(curated_blogs)} community={len(curated_community)}")
print(f"  tag: 推理={tag_count['推理']} 训练={tag_count['训练']} agent={tag_count['agent']}")
print(f"  generated_at={generated_at}")
