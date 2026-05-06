# -*- coding: utf-8 -*-
"""一次性 curated 构建脚本：读 today_raw.json → 写 today_curated.json。
中文 tldr 用「」避开双引号陷阱。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 按 link 索引 raw item，便于精确取出
by_link = {}
for sec, items in raw["sections"].items():
    for it in items:
        by_link[it["link"]] = it

def pick(link, tldr, domain_tag):
    src = by_link[link]
    out = dict(src)
    out["tldr"] = tldr
    out["domain_tag"] = domain_tag
    return out

curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}

# ---------- papers (10) ----------
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2605.03375",
    "Tutti 把 NVMe 做成长上下文 KV cache 的实用 backing 层。诊断现有 SSD-KV 卡在 GPU 内存碎片化导致海量小随机 IO 上，CPU 启动每个 IO 是真瓶颈，连 GDS 都没绕过。Tutti 让 GPU 自主发起 IO 并把碎片小块合并成大块物理读，去掉 critical path 上 CPU 介入，prefix cache restore 时 GPU stall 显著下降，给国产 ScaleUp+大池存储路线一个直接对标方案。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2511.02230",
    "Continuum 给 multi-turn agent 工作负载定制 KV cache 调度。现有引擎 finished 即驱逐对人类多轮聊天合理，但 agent 的 tool 调用通常只有几百毫秒到几秒空档，重算/reload 反而比保留代价更高。Continuum 给每条 KV 打 TTL 并联合考虑队列延迟、tool 时长方差、offload 成本做保留决策，在 agent 工作流上端到端吞吐显著提升，是 vLLM/SGLang 后续给 agent serving 的直接借鉴。",
    "agent"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2604.26666",
    "FACT 提出 agent 驱动的三阶段 CUTLASS 合成框架，思路是别让 LLM 重发明轮子。Stage1 子图模式发现把 PyTorch traced graph 匹到优化 rule，Stage2 grounded 到 CUTLASS C++ 模板（不是裸 CUDA），Stage3 多模式组合并自动调参。相对 KernelBench 系列把 LLM 直接当 CUDA 写手的路子，FACT 承认 CUTLASS 已封装的 microarchitecture 知识，让 agent 只做 transpilation，是 coding agent 在 kernel 领域的更稳设计模式。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2605.03190",
    "VDCores 重新组织 GPU 异步硬件单元的编程模型。核心观察：现代 GPU 有 TMA、async copy、tensor core、DMA 多种异步引擎，但今天软件栈用的还是单体 kernel 抽象，硬件单元普遍 underutilized。VDCores 把每个异步单元抽成 resource-isolated 虚拟核，工作负载用 micro-op 依赖图描述，自动 overlap 内存与计算。这是把 ThunderKittens/CUTLASS 手工 overlap 思路上升到编程模型层，对国产芯片对齐 NVIDIA 异步语义路线有直接参考。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2604.21231",
    "SparKV 解决端侧 LLM 推理 prefill 瓶颈。设备端跑不动长上下文 prefill，纯云 KV streaming 又受限于无线波动。SparKV 给每个 KV chunk 建 cost 模型决定云算还是本地算，并 overlap 两条路径；运行时根据带宽/资源动态重平衡 offline 调度。是端云协同 LLM 推理的工程化方案，对 PIM/移动端 NPU 路线有借鉴。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2605.02960",
    "ZeRO-Prefill 针对生产环境 MoE prefill-only 任务（分类、推荐、verifier 单 forward 读 logits）做零冗余服务。观察现有 TP/EP/PP 都是 decoding 时代设计，专家放置与同步路由耦合，prefill 上长链激活路由产生大量冗余通信。ZeRO-Prefill 解耦 expert placement 与激活路由（异步），消除冗余 compute/communication/sync。对 vLLM 给 verifier RM 这类生产高频 prefill 场景的优化是直接参考。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2604.21072",
    "BloomBee 做 Internet 规模分布式 LLM 推理，跨节点带宽是死敌。把模型分层、micro-batching、tensor offloading 联合建模为优化问题，用动态规划求解；额外集成无损压缩与投机解码以适配低带宽链路。是分布式异构 GPU 池（家庭、社区算力）做 LLM serving 的实用框架，对国产 ScaleUp 跨节点 InfiniBand 替代路径有借鉴。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2602.22457",
    "CCCL 用 CXL 共享内存池替代 RDMA 做跨节点 GPU 集合通信。设计同步、数据 interleave 与并行化以适配 CXL 内存语义，在 TITAN-II CXL 交换机上多节点验证。这是把 ScaleUp 统一内存路线推到节点间集合通信的直接尝试，对昇腾 UB/HCCS 与寒武纪集合通信库有直接参考意义——绕开 InfiniBand 控制面、走内存 load/store 语义。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2603.26498",
    "TCM-Serve 给多模态 LLM serving 做 modality-aware 调度。视频请求像「卡车」、图像像「轿车」、文本像「摩托车」——资源消耗差几个数量级，混在一起跑会被大请求 head-of-line blocking。TCM-Serve 给每种模态独立队列与资源预留，并按 modality 维度做 batching 与 preempt。对 GPT-5/Gemini/Qwen-VL 类工作负载在 vLLM/SGLang 后端上的扩展是直接参考。",
    "推理"))
curated_sections["papers"].append(pick(
    "https://arxiv.org/abs/2605.02888",
    "SpecKV 给投机解码做自适应 γ 选择。现有系统几乎都用固定 γ=4，但实测最优值随任务类型与目标模型压缩等级显著漂移。SpecKV 用 draft 模型自身信号（hidden state 距离/熵）建轻量 controller，每步独立选 γ。在 4 种任务+多种压缩配置下端到端加速优于固定值，是 EAGLE3/MTP 路线之后投机解码可控性的工程化补全。",
    "推理"))

# ---------- code (5) ----------
curated_sections["code"].append(pick(
    "https://github.com/openai/openai-agents-python/releases/tag/v0.15.3",
    "OpenAI Agents Python v0.15.3 紧急修一批 MCP 端的 corner case：避免 mutate tool input schema、reject 非对象 tool input JSON、duplicate tool 错误确定性化、ModelAudio 在格式协商前能容忍音频 deltas。这些都是 v0.15.0 ModelRefusalError 重构后第一波线上反馈暴露的供应链一致性问题，agent runtime 与 MCP 协议边界继续收敛。",
    "agent"))
curated_sections["code"].append(pick(
    "https://github.com/openai/openai-agents-python/releases/tag/v0.15.2",
    "OpenAI Agents Python v0.15.2 引入 context management model setting（推理时上下文裁剪策略可配置），并修一批安全/健壮性问题：拒绝 string-like shell 命令、disabled function tool 执行前 block、ToolContext hashable 对齐 RunContextWrapper、handoff filter 过滤 custom_tool_call、redact MCP invalid JSON 与 tool span 错误。是 sandbox/工具执行边界与可观测性的持续加固。",
    "agent"))
curated_sections["code"].append(pick(
    "https://github.com/langchain-ai/langgraph/releases/tag/sdk%3D%3D0.3.14",
    "LangGraph SDK 0.3.14 + 主仓 1.2.0a6/a7 alpha 矩阵：threads update 加 return_minimal 参数（减客户端流量），dispatch stream_events v3 落到 Pregel（事件流统一新版本），timers 重构在前几日 revert 之后继续 alpha 收敛。delta cadence rework + checkpoint/checkpoint-postgres 同步 alpha bump 保证多 saver 行为一致。",
    "agent"))
curated_sections["code"].append(pick(
    "https://github.com/langchain-ai/langgraph/releases/tag/checkpointsqlite%3D%3D3.1.0a1",
    "LangGraph checkpoint-sqlite 3.1.0a1 把 get_delta_channel_history 改成 streaming walk（避免一次性全量加载），配合 public get_writes_history saver API 与 delta cadence rework，是把 checkpoint 增量化彻底贯穿到 SQLite 后端，对长 agent 会话的 history reload 内存占用是直接收益。",
    "agent"))
curated_sections["code"].append(pick(
    "https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta12",
    "FA4 beta12 继续 head_dim=256 路线：SM100 2CTA forward 加 TMA paged KV 支持，hd256 backward 用 TMA bulk-store 写回 epilogue + LSE/dpsum coalesce，CuTe Bwd Sm90 GQA 决定性修复（port Sm100 方案），blocksparse backward 决定性。Windows MSVC 长链接命令也修了。Hopper/Blackwell 双线推进，长头维度 + paged KV 是 DSV3.2/MLA 类工作负载的关键能力。",
    "推理"))

# ---------- community (4) ----------
curated_sections["community"].append(pick(
    "https://www.reddit.com/r/LocalLLaMA/comments/1t57xuu/25x_faster_inference_with_qwen_36_27b_using_mtp/",
    "Qwen3.6-27B MTP（multi-token prediction）通过未合并的 llama.cpp PR 在 M2 Max 96GB 跑出 2.5× 推理加速，48GB VRAM 跑 262k 上下文；MTP 用模型内置 tensor 层做投机解码。原贴提到的 turboquant KV 路线因 PR 不稳暂时回退到 q4_0 KV cache 压缩。是 MTP 在消费级硬件上首个端到端 chat template 修复版本，与昨日 Gemma 4 MTP 一起标志 MTP 正成为本地推理新标配。",
    "推理"))
curated_sections["community"].append(pick(
    "https://www.reddit.com/r/LocalLLaMA/comments/1t5ageq/qwen3627b_with_mtp_grafted_on_unsloth_ud_xl_25x/",
    "另一组 Qwen3.6-27B MTP 工程化：把 Unsloth UD XL 量化（base 低位）与 Q8_0 MTP draft 头嫁接（保证 speculative 精度），开源 grafting 脚本+原始 MTP_Q8_0.gguf+定制 llama.cpp 构建说明。揭示一个工程经验：MTP 三层 draft 头放高精度（Q8）而 base 模型仍可激进量化，组合性最优。",
    "推理"))
curated_sections["community"].append(pick(
    "https://www.reddit.com/r/MachineLearning/comments/1t4kalf/tritonsigmoid_a_fast_paddingaware_sigmoid/",
    "TritonSigmoid 开源 padding-aware sigmoid attention kernel。H100 实测 515 TFLOPS，对比 FlashAttention-2 361 / FlashSigmoid 440。原生处理变长 padding（200 到 16k+ token），不浪费空 position 算力。设计动机虽是单细胞基因建模，但 sigmoid attention（多 token 同时高响应而非 softmax 互斥）在工具调用/检索 attention 上同样有用，是 FA 系 sigmoid 变体里少有的开源工程实现。",
    "推理"))
curated_sections["community"].append(pick(
    "https://www.recursant.ai/",
    "Recursant 开源 agent 服务网格，给跨栈 agent 治理提供 control plane。问题域：大企业 LangGraph/CrewAI/AgentForce/Databricks Agent Bricks 多栈并存，需要统一 policy、单一审计 trail、统一 guardrail。Recursant 用 sidecar 拦截所有流量+registry+mesh 两组件，是把 service mesh 模式套到 agent 系统的直接尝试，对照 A2A/MCP 协议层是更上层的运行时治理层。",
    "agent"))

# ---------- 输出 ----------
out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours"),
    "source_raw_generated_at": raw["generated_at"],
    "sections": curated_sections,
}

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[curated] wrote {OUT}")
total = sum(len(v) for v in curated_sections.values())
print(f"[curated] total={total} papers={len(curated_sections['papers'])} code={len(curated_sections['code'])} blogs={len(curated_sections['blogs'])} community={len(curated_sections['community'])}")

# domain_tag 分布
tags = {}
for sec_items in curated_sections.values():
    for it in sec_items:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"[curated] domain_tag={tags}")
