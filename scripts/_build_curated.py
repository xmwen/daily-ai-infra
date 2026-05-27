# -*- coding: utf-8 -*-
"""
2026-05-27 curated build script.
读取 cache/today_raw.json，按筛选偏好挑出条目并写中文 tldr+domain_tag，输出 cache/today_curated.json。
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section, key_in_title):
    for it in raw["sections"][section]:
        if key_in_title.lower() in it["title"].lower():
            return dict(it)
    raise KeyError(key_in_title)


def find_by_link(section, link_substr):
    for it in raw["sections"][section]:
        if link_substr in it["link"]:
            return dict(it)
    raise KeyError(link_substr)


curated = {"papers": [], "code": [], "blogs": [], "community": []}

# ---------------- papers ----------------
# 1. ReMoE — MoE expert reuse via router fine-tuning（cs.DC 主分区）
p = find_by_link("papers", "2605.27081")
p["tldr"] = "针对内存受限场景下 MoE 推理频繁从外存（UFS）拉 expert 的 I/O 瓶颈，ReMoE 通过 router 微调引入「最近选过的 expert 偏置」，让路由时间序列更稳定，匹配 cache 局部性，减少 expert 换页而不改推理时延。是把 cache locality 作为 first-class loss 信号嵌进路由器的工程范式，对边缘 MoE/UFS offload/PIM expert pool 路线均有借鉴。"
p["domain_tag"] = "推理"
curated["papers"].append(p)

# 2. BF16 vs FP8/INT8/INT4 — Llama-3.1 全家族量化精度系统评测（v4 replace）
p = find_by_link("papers", "2411.02355")
p["tldr"] = "Llama-3.1 全家族 50 万次评测系统对比 FP8/INT8/INT4：FP8 (W8A8-FP) 全尺度无损 / 调优 INT8 退化仅 1-3% / W4A16-INT 与 8bit 持平。结论是 FP8 仍为最强默认，INT4 weight-only 工程性价比突出。与 5/15 r/LocalLLaMA TurboQuant 系统对比独立印证，给生产侧量化选型一锤定音的对照表。"
p["domain_tag"] = "推理"
curated["papers"].append(p)

# 3. MinT — Managed infra for millions of LoRA × frontier-scale base
p = find_by_link("papers", "2605.13779")
p["tldr"] = "MinT 把上百万 LoRA 适配器作为可推可训可服务的一等资源——base 常驻不展开，LoRA 经 rollout/update/export/eval/serve/rollback 全生命周期通过服务接口流转。Scale Up 把 LoRA RL 推到 frontier MoE（含 MLA/DSA），与 5/14 MinT v1 工程化路径一致，对应 LMDeploy/SGLang 的 multi-LoRA serving 一线落地。"
p["domain_tag"] = "推理"
curated["papers"].append(p)

# 4. Cassandra — Self-spec decoding for reasoning LLM at edge（co-design HW）
p = find_by_link("papers", "2605.26558")
p["tldr"] = "Cassandra 是面向边缘推理的 reasoning LLM 自投机解码 + 硬件协同设计：免训练 drafter 通过精细化数据选择 + 优化剪枝 + 修改 mask 构造，专攻低 batch 场景。对位 5/15 ECHO/5/24 SSV 投机解码母题，把投机解码从 H100 数据中心栈下放到消费端 reasoning workload，与 Qwen3.6/DeepSeek 思考模型边缘部署直连。"
p["domain_tag"] = "推理"
curated["papers"].append(p)

# 5. Xe-Forge — Multi-stage LLM agent kernel optimization for Intel GPU
p = find_by_link("papers", "2605.26118")
p["tldr"] = "Xe-Forge 用 LLM agent 把 Triton kernel 自动迁移到 Intel GPU：9 个优化阶段（量化/合并访存/tile 调优/架构 workaround）解决跨设备移植反复人工试错。延续 4/30 FACT/5/12 KernelBenchX/5/26 Polar agentic RL 母题，把 coding agent 写 GPU kernel 推到 Intel Xe 后端，对国产芯片 ROCm/MUSA 移植有方法论参考。"
p["domain_tag"] = "agent"
curated["papers"].append(p)

# 6. Stateful Inference for Multi-Agent Tool Calling
p = find_by_link("papers", "2605.26289")
p["tldr"] = "针对 multi-agent tool calling 每次重算整段 prompt 的浪费（85-95% prompt 不变），提出有状态推理架构：跨 turn 持久 KV cache 仅消化新 token、radix prefix cache 跨多 agent 流复用、prompt-lookup 投机解码加速结构化输出。把 5/12 SPECTRE/5/27 Agentic Workload 的「decode-dominated」诊断推到生产 serving，对比 vLLM/SGLang 实测验证。"
p["domain_tag"] = "agent"
curated["papers"].append(p)

# 7. Agentic AI Workload Characteristics
p = find_by_link("papers", "2605.26297")
p["tldr"] = "对 ReAct 风格 agent 端到端 tracing：在 Gemma/Qwen reasoning 与非 reasoning 上跑 5 个 agent benchmark，发现 agent 不是简单长 prompt——有效 prefix cache 下大部分 input token 在 turn 间复用，执行变 decode-dominated 但更依赖长寿命 KV cache；tool 调用有清晰时序结构（read/write 阶段切换）。是把 agent serving 从启发式调度推到「长寿命 KV cache + tool 阶段调度」的实证基础。"
p["domain_tag"] = "agent"
curated["papers"].append(p)

# 8. ECHO-2 — Distributed RL framework with bounded staleness（v5 replace）
p = find_by_link("papers", "2602.02192")
p["tldr"] = "ECHO-2 是大规模分布式 RL 后训练框架：rollout 在远程廉价推理资源、中心化训练，把策略陈旧度作为用户可控参数允许 rollout/分发/训练三流水线 overlap。对 GRPO/veRL 链路下「跨地域低延迟分发 + bounded staleness」给出系统化答卷，与 5/22 LiveR/5/19 OSCAR INT2 RL 合流，是 RL 训练栈走向 wide-area 的工程关键。"
p["domain_tag"] = "训练"
curated["papers"].append(p)

# 9. Production LLM Inference Benchmark Bias（M/G/1 queue diagnostic, v2 replace）
p = find_by_link("papers", "2605.24217")
p["tldr"] = "诊断主流 LLM 推理 benchmark 工具的客户端测量偏差：单进程 asyncio 架构受 Python GIL 限制，在高并发下产生 M/G/1 队列瓶颈，使 TTFT/TPOT 测量值随 QPS 虚高。延续 5/13 GRIEF/5/19 Hawkeye/5/20 Silent Hyperparameter/5/22 Dooly v2 推理后端复现性母题，把矛头指向客户端，给 benchmark 工具升级提出强制要求。"
p["domain_tag"] = "推理"
curated["papers"].append(p)

# 10. Provisioning to Runtime Optimization of 100MW-Scale AI Cluster（v2 replace）
p = find_by_link("papers", "2605.24461")
p["tldr"] = "150MW 数据中心 83K GB200 全链路电源管理工程纪实：从下一代加速器 6-12 个月前的电力规划、大规模部署后的电源调优、到运行时随 workload 演化的动态功控。延续 5/13 Power Capping Illusion/5/26 Model Parking Tax 母题，把 GPU 集群「电力 first-class budget」从单机推到 hyper-scale，对国产数据中心建设直接参考。"
p["domain_tag"] = "推理"
curated["papers"].append(p)

# ---------------- code ----------------
# 1. TensorRT-LLM v1.3.0rc16 — Gemma4 multimodal + Qwen3.5 MTP + KV manager v2
c = find_by_link("code", "TensorRT-LLM/releases/tag/v1.3.0rc16")
c["tldr"] = "本周最强 release 之一：新增 Gemma4 多模态（vision+audio）、Qwen3.5 MTP、Qwen3.6-27B-FP8、EXAONE-4.5/Laguna；DeepSeek/NemotronH/Qwen3/Qwen3.5-MoE 切到 sharding-IR canonical models；新增精确多模态 KV block hashing + KV cache reuse probing；KV cache manager v2（Python transceiver）；disaggregated serving 支持 block reuse。多模态 KV reuse + KV manager v2 是 TRT-LLM 这一版的两大轴线。"
c["domain_tag"] = "推理"
curated["code"].append(c)

# 2. FlashInfer v0.6.12rc1
c = find_by_link("code", "flashinfer/releases/tag/v0.6.12rc1")
c["tldr"] = "v0.6.12rc1：SM120 W4A16 b12x MoE kernel、TRTLLM-GEN GQA 动态 tokens-per-page、Kimi K2.5 H64 CuTe DSL MLA decode、CUTLASS MLA paged attention 支持 FP8 输出、per-token NVFP4 量化 kernel 优化、cute_dsl/moe autotuner 去偏。SM120 (Blackwell consumer) MoE + MLA paged FP8 是消费卡侧 frontier MoE 推理收尾的关键拼图，5/26 已覆盖延续。"
c["domain_tag"] = "推理"
curated["code"].append(c)

# 3. SGLang v0.5.12.post1 — DSV4 stability cherry-pick
c = find_by_link("code", "sglang/releases/tag/v0.5.12.post1")
c["tldr"] = "v0.5.12.post1 是 V4 系列稳定性补丁：DSV4-Pro B200/B300 单 token decode 乱码（deep_gemm UE8M0 scale-packing 路径，激活 scale 打包前需向上取整修复）、DSV4 + EAGLE/MTP 在 disagg decode 跑到 ~2000 请求 SWA allocator 崩（被回收 KV pages 残留 stale sliding-window mappings）、NSA prefill CP 启动崩、HiSparse + COMPRESSOR_V2 GSM8K 0.825→0.960 精度修复。MTP/spec decode × disagg KV pool 的边界 bug 集中暴露并修复，5/27 SGLang 仍是 V4 全栈最完整答卷。"
c["domain_tag"] = "推理"
curated["code"].append(c)

# 4. CUTLASS 4.5.1 — paged KV for Blackwell low-latency GQA
c = find_by_link("code", "cutlass/releases/tag/v4.5.1")
c["tldr"] = "CUTLASS 4.5.1：CuTe DSL 一批 bug 修（SM120 MXFP8/F6/F4 BlockScaled MMA 缺失补齐）、SM100 F8F6F4 SS MMA 切 typed op templates、UE8M0 张量初始化、cvt.rn.bf16x2.e4m3x2 转换指令、example 93 Blackwell low-latency GQA 加 paged KV cache 支持。SM100/SM120 MX 系列 MMA + paged KV 在 CUTLASS 主线持续收敛，是 vLLM/SGLang/TRT-LLM 复用底座。"
c["domain_tag"] = "推理"
curated["code"].append(c)

# 5. DeepSpeed v0.19.1
c = find_by_link("code", "DeepSpeed/releases/tag/v0.19.1")
c["tldr"] = "v0.19.1：单子 MoE collectives 优化、ZeRO-3 SDMA allgather via mori (sdma_allgather)、CUTLASS EvoformerAttention 自动检测、ZeRO-3 forward 在 _parameters 是 plain dict 时崩溃修复、aio_fd 关闭 fd 泄漏。SDMA allgather 是 ROCm 平台 ZeRO-3 通信侧实质增量；与 5/19 OpenMP BSP/JanusPipe 共同构成训练栈底层通信进化轨迹。"
c["domain_tag"] = "训练"
curated["code"].append(c)

# 6. OpenAI Agents v0.17.4
c = find_by_link("code", "openai-agents-python/releases/tag/v0.17.4")
c["tldr"] = "v0.17.4：Realtime 自定义 voice 对象、function tool 缺失 opt-in 恢复、MCP SSE 套用 hardened http client 默认值、FunctionSpanData output 用非 None 值、ModelBehaviorError data 中无效 JSON 载荷脱敏、span slots/tracing 类型导出补齐。延续 v0.17.x 「sandbox+tracing+MCP 安全边界补漏期」节奏，是连续第 4 个 patch 修补 SDK 边角。"
c["domain_tag"] = "agent"
curated["code"].append(c)

# 7. LangGraph 1.2.2
c = find_by_link("code", "langgraph/releases/tag/1.2.2")
c["tldr"] = "langgraph 1.2.2：为 id=None 的 BaseMessages 在 DeltaChannel checkpoint writes 前分配稳定 ID（避免序列化层重放歧义）、checkpoint 4.1.1 一并发布。延续 5/22 1.2.1 / 5/23 checkpoint 4.1.1（封死 lc:2 envelope revival）的「补漏期」节奏，agent SDK 进入消息 ID 与序列化合约层加固阶段。"
c["domain_tag"] = "agent"
curated["code"].append(c)

# ---------------- blogs ----------------
# 1. NVIDIA CUDA Tile in C++ — develop high-perf GPU kernels with tile programming
b = find_by_link("blogs", "develop-high-performance-gpu-kernels-in-cpp-with-nvidia-cuda-tile")
b["tldr"] = "NVIDIA 把 CUDA Tile 编程从 Python (cuTile) 推到 C++ 主线：开发者可在大型 C++ GPU codebase 内用 tile-based 编程开发高性能 kernel。配合同日 CUDA 13.3 发布的 tile programming 入口，把 5/4 CUTLASS CuTe DSL 路线推到生产 C++ 栈，与 TileLang v0.1.10 跨硅片 tile DSL 路线（5/26）形成 NVIDIA 官方 vs 开源社区双栈对照。"
b["domain_tag"] = "推理"
curated["blogs"].append(b)

# 2. NVIDIA CUDA 13.3 — Tile Programming + Compiler Autotuning + Python Updates
b = find_by_link("blogs", "nvidia-cuda-13-3-enhances-gpu-development")
b["tldr"] = "CUDA 13.3 三大轴：CUDA Tile programming in C++（tile DSL 进官方）、Compiler Autotuning（CompileIQ 自动调编译参数）、Python 更新。Tile DSL + 编译器自调优是这版主线，把 NVIDIA 在 GPU kernel 开发栈的「易用性 × 性能」从 cuTile/cuBLAS API 推到 tile-level Python+C++ 双入口。"
b["domain_tag"] = "推理"
curated["blogs"].append(b)

# 3. NVIDIA CompileIQ Auto-Tuning — extract more kernel performance
b = find_by_link("blogs", "extract-more-kernel-performance-with-nvidia-compileiq-auto-tuning")
b["tldr"] = "CompileIQ 把「找最优 nvcc 编译选项」自动化——针对特定 kernel 探索编译参数空间。是 NVIDIA 把 4/30 FACT/5/12 KernelBenchX/5/26 Polar harness RL「LLM/agent 写 kernel」之外的另一条路径——「AI 调编译器」。两条路并行：人类写 kernel 让 agent 自动改、人类写 kernel 让编译器自动调。"
b["domain_tag"] = "推理"
curated["blogs"].append(b)

# ---------------- community ----------------
# 1. Triton MoE dispatch kernel 89-131% Megablocks（A100 + AMD MI300X 跨平台）
co = find_by_link("community", "1tp4u0u")
co["tldr"] = "纯 Triton 写 MoE fused dispatch kernel（不写 CUDA），在 A100 上 Mixtral-8x7B 跑到 Stanford Megablocks（CUDA 优化）的 89-131%（≤512 tokens batch），同份 kernel 在 MI300X 零改动跑通。最大收益来自 gate+up projection 融合让 SwiGLU 中间值不离寄存器（-35% 全局内存流量）；2048+ tokens 与 64+ experts 重路由偏斜下回退。延续 5/26 TritonMoE paper 母题，给 cross-vendor MoE kernel 路线再添社区独立验证。"
co["domain_tag"] = "推理"
curated["community"].append(co)

# 2. CUDA 13.3 landed (社区简短信号合并到 tile blog 之外，作为补充线下确认 — 这条作为 tile 的补充 datapoint)
co = find_by_link("community", "1tp0vk1")
co["tldr"] = "CUDA 13.3 已落地，社区在跟进 llama.cpp 等推理引擎是否兼容。配合同日 NVIDIA 三篇 blog（Tile programming in C++/CompileIQ/CUDA 13.3 总览），是 NVIDIA tile DSL 路线在用户侧的首个工程化触达信号点。"
co["domain_tag"] = "推理"
curated["community"].append(co)

# 3. llama.cpp Console — Windows GUI 推理客户端（轻量 datapoint，反映 llama.cpp 用户面继续下沉）
co = find_by_link("community", "1tp60hn")
co["tldr"] = "llama.cpp Console — 面向 Windows 的 llama.cpp 控制台 GUI 客户端开源。延续 5/20 LM Studio 0.4.14 加 MTP / Google AI Edge Gallery 等桌面端接 llama.cpp 后端的下沉曲线，是 llama.cpp 生态从 server 向客户端 GUI 工具链不断延伸的小拐点。"
co["domain_tag"] = "推理"
curated["community"].append(co)

# ---------- finalize ----------
out = dict(raw)
out["sections"] = curated
out["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
out["source_tag"] = "today_curated"

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

total = sum(len(v) for v in curated.values())
print(f"curated written: {OUT}")
print(f"counts: papers={len(curated['papers'])} code={len(curated['code'])} "
      f"blogs={len(curated['blogs'])} community={len(curated['community'])} total={total}")
tags = {}
for sec in curated.values():
    for it in sec:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"domain_tag: {tags}")
print(f"generated_at: {out['generated_at']}")
print(f"raw generated_at: {raw['generated_at']}")
