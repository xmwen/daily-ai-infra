# -*- coding: utf-8 -*-
"""一次性 curated 构建脚本：读 today_raw.json，按 link 去重，写中文 tldr + domain_tag。"""
import json
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section: str, key: str):
    for it in raw["sections"].get(section, []):
        if key in it["link"] or key in it["title"]:
            return it
    return None


def C(section, key, tldr, tag):
    it = find(section, key)
    if it is None:
        raise SystemExit(f"missing {section}: {key}")
    new = dict(it)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    return new


curated = {
    "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "source": "today_curated.json",
    "sections": {
        "papers": [],
        "code": [],
        "blogs": [],
        "community": [],
    },
}

# ============== papers ==============
P = curated["sections"]["papers"]

P.append(C(
    "papers", "2605.19481",
    "C2CServe：把 NVLink-C2C（GH200/GB200 Superchip 的 CPU-GPU 高带宽直连）当 MIG 多实例 GPU 的弹性 serverless LLM serving 扩展通道——模型权重常驻 CPU 内存，按需流式推到指定 MIG slice，把模型驻留约束从稀缺 HBM 移到丰沛主存，绕开「单 MIG slice HBM 装不下现代大模型权重」与「GPU 时间切片冷启动加载在关键路径」的两难。直接命中国产 ScaleUp 统一内存路线的 serverless 推理设计参考。",
    "推理"
))

P.append(C(
    "papers", "2605.19537",
    "Silent Hyperparameter：调研 200 个不同推理引擎、扫 35000 篇 ML 论文，发现「用什么 backend 跑」几乎从不在论文 reproducibility section 出现，但 vLLM/SGLang/llama.cpp/TensorRT-LLM 等系统级 CUDA kernel 优化与降精度算术会改变 token 概率引入非确定性，并在长生成中级联放大到完全分歧。把推理 backend 列为「沉默超参数」，主张评测必须把 inference engine 作为 first-class 报告字段。基础设施层「评测可重复性」对比 5/13 GRIEF greybox fuzz 与 4/29 vLLM TurboQuant 实测的工程同源问题。",
    "推理"
))

P.append(C(
    "papers", "2605.19893",
    "SpecSA：投机解码与动态稀疏 attention 直接组合存在结构错配——投机 verification 依赖跨 query commonality，动态稀疏 attention 给出 query-specific 稀疏布局，两者拼起来 KV-block reuse 极差且放大 NSA branch-wise 开销。SpecSA 把动态稀疏 attention 重塑为面向 verification 的 workload，给出与「verification-aware 稀疏布局」共享 sparse skeleton 的 kernel 路径，让 SD×sparse-attn 两条母题首次工程兼容。延续 5/12 SPECTRE / 5/14 PipeSD / 5/15 ECHO 投机解码母题。",
    "推理"
))

P.append(C(
    "papers", "2601.20309",
    "SuperInfer：面向 NVIDIA GH200 这类 GPU-CPU NVLink-C2C 紧耦合 Superchip 的 SLO-aware LLM 推理系统。提出 RotaSched——首个 proactive、SLO-aware rotary 调度器，KV cache 在 GPU 与 CPU 之间按 TTFT/TBT 双 SLO 主动迁移，避免高请求率下 KV 预算耗尽产生 head-of-line blocking；与 PCIe 经典 offload 思路对照展示 C2C 高带宽下「主动 rotary」比「被动 LRU offload」在长尾 SLO 上的本质优势。与 C2CServe 同日命中 GH200/GB200 推理母题。",
    "推理"
))

P.append(C(
    "papers", "2605.19775",
    "Inference Scaling for Reasoning LLMs：在 GPU 集群上评测 8B-671B 参数模型，系统刻画 reasoning workload 把推理从「prefill compute-bound」彻底搬进「Capacity-Bound regime」的瓶颈结构，扫 DP/TP/PP 三轴显示数据并行 throughput 随 reasoning 长度反向衰减，给出与传统 scaling heuristic 完全相反的容量瓶颈结论。是 reasoning 长输出主导推理时代的「新 scaling law」基础设施视角答卷。",
    "推理"
))

P.append(C(
    "papers", "2508.06526",
    "PiKV：面向 MoE 架构的并行分布式 KV cache serving 框架。MoE 计算稀疏化但 KV cache 仍是 dense+全局同步的内存与通信瓶颈，PiKV 用 expert-sharded KV 存储跨 GPU 切分缓存、PiKV routing 减少 token-to-KV 访问、PiKV scheduling 自适应保留 query-relevant entry，并复用 MoE 专家激活稀疏性继续压缩 KV 内存。延续 5/19 OSCAR/VeriCache/TriAxialKV/Protection-Capped/KVDrive 与 5/12 KV-RM 的 KV cache 母题。",
    "推理"
))

P.append(C(
    "papers", "2605.18825",
    "SAECache：观察 prompt 内 system prompt / user query / tool output / model response / chain-of-thought 五类 token 的 reuse rate 跨类差距高达 756×，但现存 LRU/LFU 等 prefix cache eviction 全部把它们等同看待。SAECache 给出 semantic-aware eviction policy——按 token 类型语义打 reuse 概率分，agent workflow（多 tool call + CoT）下 prefix cache 命中率显著抬升。是「prompt 结构感知缓存」首作，与 5/14 KVServe disagg KV 通信压缩共构 KV 工程化二级母题。",
    "推理"
))

P.append(C(
    "papers", "2605.19049",
    "KVBuffer：linear attention 长上下文 serving 的 IO-aware 机制——现有 linear attention serving 每步 decode 都要重算并更新庞大的 linear state（远大于单 token kv），递归 decode 内存访问极重。KVBuffer 把最近 key/value buffer 起来，让 serving 系统按窗口灵活组合 linear-state 更新与显式 key/value 计算，prefill/decode 双阶段都拿到更高 IO 效率。是 linear attention 从 paper 走向工业 serving 的关键一步。",
    "推理"
))

P.append(C(
    "papers", "2605.19593",
    "Multi-Model LLM Schedulers：实证研究多模型在异构硬件共享部署下的资源分配/调度行为，重点是 GPU 内存约束下的 partial CPU-GPU offload 与 preemption。给出跨平台 LLM 行为差异图谱，揭示 throughput 单模型 oracle 下做出的调度决策在多模型场景下显著次优——offload 与 preempt 的代价模型必须模型敏感。为多租户 multi-model serving 调度器（Coral/HFX 等）提供 baseline 实证基础。",
    "推理"
))

P.append(C(
    "papers", "2605.19660",
    "OScaR：揭示「per-channel KV 量化」在极致压缩下失效的根因是 Token Norm Imbalance（TNI）——共享量化参数被迫跨度差异极大的 token group，系统性放大量化误差。给出 Occam's Razor 风格简洁修复，附 CUDA kernel 实现。延续 5/19 OSCAR 同日的 KV 极致量化母题；OScaR 与 OSCAR 是同期命名撞车，注意区分（OScaR=Occam's Razor，OSCAR=旋转 INT2）。",
    "推理"
))

P.append(C(
    "papers", "2605.19945",
    "GEM（GPU-Variability-Aware Expert to GPU Mapping）：MoE serving 中跨 GPU 的 lock-step 同步障碍把整 batch 卡死在最慢 straggler 上——以往 expert placement 只看 token 负载均衡，忽视了 GPU 个体性能波动（频率/温度/调度抖动）。GEM 把 GPU variability 作为 expert mapping 一等输入，与 5/14 Lit Silicon 的「热不均→C3 straggler」诊断同源。直接对位 4/30 RaMP MoE 路由感知 kernel dispatch。",
    "推理"
))

P.append(C(
    "papers", "2605.18815",
    "DynaTrain：弹性 LLM 训练的 sub-second 在线并行重配框架。提出 Virtual Parameter Space（VPS）抽象——把所有分布式训练状态统一到一个逻辑坐标空间，任意并行配置变成确定性映射，复杂跨 DP/TP/PP/EP 重配化简为可管理的几何相交问题。在 RLHF 阶段切换、cluster 弹性伸缩、resource 抖动下做到秒级在线 reshape。是 5/12 LangGraph 1.2.0「durable error-handler resume」之后训练侧的弹性答卷。",
    "训练"
))

P.append(C(
    "papers", "2510.18830",
    "MTraining：分布式动态稀疏 attention 训练 ultra-long 上下文。指出动态稀疏 attention 在分布式训练中遇到 worker-level 与 step-level 双重不平衡（不同 token 选不同稀疏 mask 导致 worker 计算量天差地别）。MTraining 提出动态平衡机制，让 ring attention 在长上下文+稀疏 mask 下仍能高效跨 worker 协同，是把 cs.LG 推理侧的稀疏 attention 母题正式落到训练栈的关键一步。",
    "训练"
))

# ============== code ==============
CC = curated["sections"]["code"]

CC.append(C(
    "code", "fa4-v4.0.0.beta14",
    "FlashAttention 4 beta14：修 num_splits_heuristic 在空 Q workload 下的 ZeroDivisionError、SM90 Flex 路径修复、varlen batch search 工具拆分、SM100 hd256 kernel 允许 zero-length 序列、为 blocksparse tensor 启用 split-kv。延续 5/13 beta13 的 hd256+Flex+SM100 deterministic 收敛节奏，本周 FA4 进入「细节边界条件补漏期」（zero-length 序列、empty Q workload、Flex+SM90 路径稳定化）。",
    "推理"
))

# ============== blogs ==============
B = curated["sections"]["blogs"]

B.append(C(
    "blogs", "nvidia-verified-agent-skills",
    "NVIDIA Verified Agent Skills：把 agent 的 capability governance 抽象为「verified skill」一等公民，定义可验证签名的 portable skill 包＋MCP 接入＋skill 级 capability policy，让 host application 在加载 skill 前可验证其能力声明与权限边界。是 OpenAI Agents v0.17 sandbox 收紧 + LangGraph 1.2 durable error-handler 之后，NVIDIA 把 agent 安全边界从 sandbox 进一步上推到「能力签名」层的官方背书，对接近期连续命中的 agent SDK「补漏期」节奏。",
    "agent"
))

# ============== community ==============
M = curated["sections"]["community"]

M.append(C(
    "community", "rtx_5080_16gb_qwen36_35b_moe",
    "RTX 5080 16GB 实测 Qwen3.6 35B-A3B MoE @ 128k 上下文 56 tok/s gen + 1584 tok/s prompt。意外发现：在 128k 长上下文下 MTP 与非 MTP 速度收敛，MTP 不再加速（与 5/17 3090Ti n_max 扫描得出的 MTP1 1.28×@95.5% 形成长 ctx vs 短 ctx 对照）。在 5/4 KTransformers 首发 → 5/16 llama.cpp master merge → 5/17 多硬件单日实测之后，本日补齐了「MTP 长上下文边界失效」工程经验，是 MTP 工程化下沉曲线的最后一块拼图。建议加入用户工作的 MTP 配方决策表。",
    "推理"
))

M.append(C(
    "community", "lm_studio_finally_added_support_for_mtp",
    "LM Studio 0.4.14 Beta 2 加入 MTP 投机解码支持（依赖 llama.cpp 引擎 2.15.0+），需「Manually choose model load parameters」手动启用，默认关闭。继 llama.cpp master merge 之后第一个主流桌面 GUI 推理客户端跟进，标志 MTP 从「kernel/引擎层 release」走向「终端用户可一键体验」。",
    "推理"
))

M.append(C(
    "community", "google_ai_edge_gallery",
    "Google AI Edge Gallery v1.0.13 + v1.0.14：Gemma 4 Multi-Token Prediction 支持、Pixel TPU 加速、实验性 MCP 集成、新增 skill 系统、聊天历史持久化。是「移动端 LLM 边缘推理 + agent skill + MCP」三条母题在消费端 app 首次集中落地——MTP 工程化下沉至此覆盖到移动端 NPU/TPU 后端，与同日 NVIDIA Verified Agent Skills 形成「云端 verified skill ↔ 端侧 skill 系统」对照。",
    "agent"
))

M.append(C(
    "community", "cloud-agent-development-environments",
    "Cursor 公布云端 agent 开发环境设计——为 background coding agent 提供托管 dev env、隔离 workspace、可恢复 session 与可观测性，对位 OpenAI Agents v0.17 sandbox 加固 + LangGraph 1.2 durable resume 节奏。延续 coding agent 系统设计母题（Claude Code/Cursor/Codex/Devin），关注点从「IDE 内联 agent」上移至「Cloud-resident agent runtime」。",
    "agent"
))

M.append(C(
    "community", "atlassian/README.md",
    "Atlassian MCP server 审计报告：发现其 OAuth 2.0 资源元数据 RFC 9728 discovery path 全部不可解析，MCP client 走标准发现流程会失败必须 hardcode endpoint。本月持续命中的 MCP 协议合规性 + agent 安全边界母题再添一例（5/17 MCP Python v1.27.1 OAuth 空字符串 URL 强制 None / 4/30 Lightport MCP gateway / 5/3 MDA 多 agent 激活共享）——MCP 生态正进入「协议合规审计期」。",
    "agent"
))

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: {len(P)} papers / {len(CC)} code / {len(B)} blogs / {len(M)} community")
print(f"generated_at = {curated['generated_at']}")
print(f"raw         generated_at = {raw['generated_at']}")

# domain tag stats
from collections import Counter
tags = Counter()
for sec in curated["sections"].values():
    for it in sec:
        tags[it["domain_tag"]] += 1
print(f"domain_tag = {dict(tags)}")
