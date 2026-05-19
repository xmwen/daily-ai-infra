# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 写中文 curated。
中文 tldr 用「」做强调，避免英文双引号闭合。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section, link_substr=None, title_substr=None):
    for it in raw["sections"][section]:
        if link_substr and link_substr in it["link"]:
            return it
        if title_substr and title_substr.lower() in it["title"].lower():
            return it
    return None


def mk(item, tldr, tag):
    out = dict(item)
    out["tldr"] = tldr
    out["domain_tag"] = tag
    return out


curated = {"papers": [], "code": [], "blogs": [], "community": []}

# ============ papers ============
p = find("papers", link_substr="2605.17757")  # OSCAR INT2 KV 旋转
curated["papers"].append(mk(p,
    "INT2 KV cache 量化：Hadamard 等通用旋转在 INT2 仍崩。OSCAR 离线估计「attention 实际消耗」的 covariance 结构，"
    "据此推 fixed rotation + clip 阈值，让 KV 量化方向与下游 attention 对齐；并配套了一份可部署 INT2 attention kernel，"
    "长上下文 LLM serving 把 KV 显存压到 1/8 的同时保住精度。",
    "推理"))

p = find("papers", link_substr="2605.17613")  # VeriCache
curated["papers"].append(mk(p,
    "无损 KV 压缩推理框架：现有 KV drop/quant 在长输出会逐步发散，code 生成与 tool calling 处崩。VeriCache 用压缩 KV 当 drafter 起草，"
    "再用完整 KV 做 verify，从而保证输出比特级等价于「全 KV」decode；保留压缩侧吞吐的同时把 lossy 组件套进可验证投机解码壳。",
    "推理"))

p = find("papers", link_substr="2605.17170")  # TriAxialKV
curated["papers"].append(mk(p,
    "Agent 推理 KV 量化新范式：agent workload 的 token 沿「时间近-远 / 模态文-图 / 角色 user-tool-obs-reason」三轴异质，"
    "对压缩敏感度截然不同。TriAxialKV 把三轴异质同时建模，对 SGLang/vLLM 类 serving 的 multi-turn tool use 给出 INT4/INT2 共存配方，"
    "在 agentic-bench 上无损同时显存大降。",
    "推理"))

p = find("papers", link_substr="2605.16637")  # HexAGenT
curated["papers"].append(mk(p,
    "Agent 工作流 prefill-decode 分离 serving 调度：agent 一个请求是多步 plan/tool/branch/refine 流水，用户感知是「整条 workflow 端到端延迟」"
    "而非单次 LLM call。HexAGenT 在异构 PD-disagg 集群上做 workflow- 与 heterogeneity-aware 调度，揭示依赖增量到达 + 输出长度未知 + KV 跨阶段差异同时存在时的最优 routing。",
    "推理"))

p = find("papers", link_substr="2605.16819")  # AgentKernelArena
curated["papers"].append(mk(p,
    "GPU kernel 优化 coding agent 基准：196 任务覆盖 HIP-to-HIP / Triton-to-Triton / PyTorch-to-HIP 翻译，"
    "评测的是完整 agent workflow（读码-编译-profile-改）而非单次 LLM call，且引入「未见配置 generalization」测试。"
    "为 Claude Code/Cursor/Codex 写 GPU kernel 的实际能力提供了可对比的硬尺子。",
    "agent"))

p = find("papers", link_substr="2605.17076")  # S-Bus
curated["papers"].append(mk(p,
    "多 agent 共享 NL 状态的「写写竞争 + 跨 shard 旧读」结构性 race condition：LangGraph/CrewAI/AutoGen 都没有写所有权语义。"
    "S-Bus 是 HTTP middleware，用 server-side DeliveryLog 记录每个 agent 的 GET，commit 时自动重建 read-set，提供 Observable-Read Isolation 偏因果一致性，"
    "无需改 agent SDK 即可拦截这类 silent corruption。",
    "agent"))

p = find("papers", link_substr="2605.18053")  # Protection KV Eviction
curated["papers"].append(mk(p,
    "KV cache 驱逐 7 大策略（LRU/H2O/SnapKV/StreamingLLM/Ada-KV/QUEST/Random）共有 prompt-boundary 漏洞：无结构保护时 6 个 transformer 上 F1 ≤ 0.064 全崩。"
    "在每个边界保留 10% cache 即可在 LongBench 7 模型 13% retention 下恢复 69-90% 全 cache 质量。"
    "实证：position-0 sink 占 ~75% 注意力 mass，attention scorer 留住 sink 却仍丢边界，本质问题在「保护」而不在「打分」。",
    "推理"))

p = find("papers", link_substr="2605.18753")  # DashAttention
curated["papers"].append(mk(p,
    "可微自适应稀疏分层注意力：NSA/InfLLMv2 的 top-k 选块假设「相关 token 数量固定」并切断稀疏-密集梯度。"
    "DashAttention 用 α-entmax 在第一阶段按 query 自适应选可变数量块，给第二阶段 softmax 提供 prior，整条层级保持可微。"
    "对长上下文 attention 端到端训练投机式稀疏 backbone 给出干净微分路径。",
    "推理"))

p = find("papers", link_substr="2605.18071")  # KVDrive
curated["papers"].append(mk(p,
    "多层 KV cache 管理 system 视角：现有 offload 系统全 KV 放 host 内存按需取，受 sparsity 上限制约——context 与 batch 一涨，"
    "KV 传输成为 decode 主要延迟。KVDrive 跨 GPU mem / host DRAM / SSD 三层联合编排，不再单点压稀疏，"
    "给长上下文 LLM 推理一份 holistic memory hierarchy 工程方案。",
    "推理"))

p = find("papers", link_substr="2605.16867")  # GoodServe
curated["papers"].append(mk(p,
    "Agentic LLM 异构 GPU serving goodput 优化：agent 请求关注「整条推理是否按时完成」，所以 routing 必须基于输出长度预测 + GPU 状态预测，"
    "而非简单负载。GoodServe 用「predict-and-rectify」机制实时纠偏，从而在异构资源池里把端到端 SLO 满足率最大化。",
    "推理"))

p = find("papers", link_substr="2605.18404")  # JanusPipe
curated["papers"].append(mk(p,
    "MLIP（机器学习原子势）训练 PP 流水：守恒 MLIP 是 double-backward 模式（forward 阶段就要梯度），与现有 pipeline parallelism 严重不匹配。"
    "JanusPipe 是 PP/DP/GP 三维并行系统，专门处理这种前向-反向耦合，把 LLM 类 scaling 训练范式扩展到分子动力学 backbone。",
    "训练"))

p = find("papers", link_substr="2605.18750")  # RRFP
curated["papers"].append(mk(p,
    "Pipeline 训练 readiness-driven runtime：现代 workload 计算/通信都漂移，预提交的静态 schedule 与实际任务 ready 顺序背离会产生「等不该等」的 idle bubble。"
    "RRFP 改 schedule 消费方式——不是按序等而是按 ready 触发，stage 错位、空泡、利用率三者同时改善，是 PP 调度从「计划经济」转「事件驱动」的工程化样本。",
    "训练"))

p = find("papers", link_substr="2602.05743")  # FP8 DCIM
curated["papers"].append(mk(p,
    "FP8 数字存内 DCIM 加速器：现有 DCIM 用统一 alignment 与定精度 MAC 没法吃 FP8 的 variable aligned-mantissa。"
    "本作三件套：动态 shift-aware 位宽预测（权重 2/4/6/8b + 输入 2-12b on-the-fly）+ FIFO 输入对齐替桶形移位 + ... 在 LLaMA 推理上同时改善准确度与能效；"
    "对国产推理芯片做 FP8 native 设计提供了精度-能效平衡的实证参照。",
    "推理"))

p = find("papers", link_substr="2603.20421")  # Hawkeye
curated["papers"].append(mk(p,
    "GPU 级非确定性复现：在 CPU 上比特级重放 NVIDIA GPU 跑过的训练/推理 matmul，无精度损失，无需任何 prover overhead。"
    "核心是一组精心构造的 rounding direction / subnormal / 累加顺序检测序列。"
    "对 verifiable ML、跨芯片对齐、训练 hang 复现都是新一类工具——避开了之前 verifiable ML 的 prover 重负担。",
    "推理"))

p = find("papers", link_substr="2605.12445")  # SVE Packed Layouts
curated["papers"].append(mk(p,
    "向量长度无关 ML codegen：Arm SVE 等 VLA 指令集让一份实现适配多种向量长度，但破坏了「编译期固定 tile / layout」的假设。"
    "本作把 vector-length-aware packed layout 与 tile/fusion/vectorization 集成进 MLIR/IREE，"
    "在 Arm CPU 上跑出与固定向量长度方案竞争甚至更好的代码——长尾推理设备 ML 编译栈的关键缺口被补齐。",
    "推理"))

# ============ code ============
c = find("code", link_substr="openai-agents-python/releases/tag/v0.17.3")
curated["code"].append(mk(c,
    "OpenAI Agents Python v0.17.3：一波 11+ 个 fix——sandbox 命令屏蔽 mountpoint 凭证、统一 memory optional 依赖 import 错误、"
    "text_message_output 与 ItemHelpers 防 None text、避免 mutate FunctionTool params_json_schema 与 Codex 输出 schema、"
    "Vercel sandbox 终态时跳过 wait_for_status、handoff filter 过滤 hosted_tool_call、Literal 类型输出 schema 命名等。"
    "继续延续 sandbox 安全边界与 schema 健壮性收紧的节奏，本月 OpenAI Agents 进入「补漏期」。",
    "agent"))

c = find("code", link_substr="flashinfer/releases/tag/nightly-v0.6.11-20260519")
curated["code"].append(mk(c,
    "FlashInfer nightly v0.6.11-20260519：v0.6.11 系列继续滚动，无明确 changelog；接续此前 trtllm head_dim=512 + MXFP4×BF16 SM90 + DCP All-to-All 等改造，"
    "用于追 Blackwell + DSV4-Flash sparse attention 部署。",
    "推理"))

# ============ community ============
co = find("community", link_substr="1tgyx41")  # CUDA kernel rewrite
curated["community"].append(mk(co,
    "小批 / 实时 ML 推理 runtime 用纯 C++/CUDA kernel 重写：作者发现单 GPU 小批量场景下 GEMM 不是唯一瓶颈，"
    "fragmented small kernel、norm/residual/activation 边界、quant/dequant 开销、layout 转换、Python 调度、graph compiler fusion 失败、FP8/FP4 精度区切换"
    "这些「runtime glue」加起来占了大头。云端 LLM serving 靠 batching 能藏住，但机器人/VLA/世界模型的 single-batch 流派藏不住——给国产小批量推理引擎工程化提供了完整的「非 GEMM 瓶颈」清单。",
    "推理"))

co = find("community", link_substr="1thnnjs")  # Pacman Qwen3.6 27b f16 vs 8bit
curated["community"].append(mk(co,
    "Qwen 3.6 27B F16 vs Q8 实测：作者用「单页 Pacman one-shot 实现」当 coding agent 个人 bench，3 次试 2 次几近完美——但量化到 8bit 后 5+ 次都复现不了。"
    "对应近期社区一系列「Q8 不是无损」的非正式证据；提示在 reasoning/coding 场景上 Q8 与 BF16 之间存在一致性鸿沟，"
    "对 KV 量化与权重量化都需独立验证，而非沿用「困惑度无损」结论。",
    "推理"))

co = find("community", link_substr="1thm9ek")  # Multi-Agent Architecture LangGraph
curated["community"].append(mk(co,
    "组织级多 agent 架构实战：三类 agent 共享 context layer——Observer 拉外部信号写结构化 event；Task 从 stream 取活做有界动作回写结果；"
    "Goal 读完整执行历史做 plan、调度 task agent、条件触发 re-plan。Goal 层用 LangGraph 的 stateful graph + checkpoint + 条件分支处理。"
    "是 LangGraph 真正进入工业生产 multi-agent runtime 的实战样本，比单进程「agent loop」高一档。",
    "agent"))

co = find("community", link_substr="1thlmsx")  # llama.cpp MTP PR 23269
curated["community"].append(mk(co,
    "llama.cpp MTP PR #23269：5/16 Qwen3.6 系列 MTP 主线合并之后又一波改进，社区催促「该升 llama.cpp 了」；"
    "延续 5/4 KTransformers 首发→5/6-7 多平台实测→5/11-13 系统 benchmark 出「文本熵决定 MTP 加速比」结论→5/16 master merge→5/17 多硬件档实测的 MTP 工程化下沉曲线，本周仍在持续收敛。",
    "推理"))

# ============ generated_at ============
out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": curated,
    "fetch_stats": raw["fetch_stats"],
}

# 校验所有条目都有 tldr 与 domain_tag
for sec, items in curated.items():
    for it in items:
        assert it.get("tldr"), f"missing tldr in {sec}: {it.get('title')}"
        assert it.get("domain_tag") in {"推理", "训练", "agent"}, f"bad tag in {sec}: {it.get('title')}"

OUT.write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
total = sum(len(v) for v in curated.values())
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for items in curated.values():
    for it in items:
        tag_count[it["domain_tag"]] += 1
print(f"curated total: {total}")
for sec, items in curated.items():
    print(f"  {sec}: {len(items)}")
print(f"domain_tag: {tag_count}")
print(f"generated_at: {out['generated_at']}")
print(f"raw generated_at: {raw['generated_at']}")
