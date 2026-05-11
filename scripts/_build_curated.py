"""一次性构建 today_curated.json（中文 tldr + domain_tag）。"""
import json
from datetime import datetime, timezone
from pathlib import Path

RAW = Path("cache/today_raw.json")
OUT = Path("cache/today_curated.json")

raw = json.loads(RAW.read_text(encoding="utf-8"))


def pick(section: str, link: str, tldr: str, domain_tag: str):
    for item in raw["sections"].get(section, []):
        if item["link"] == link:
            new = dict(item)
            new["tldr"] = tldr
            new["domain_tag"] = domain_tag
            return new
    raise SystemExit(f"NOT FOUND {section} {link}")


curated = {"papers": [], "code": [], "blogs": [], "community": []}

# ============ papers（按 link 去重后 13 条 → 选 12 条） ============

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.06113",
    "把 DP 负载均衡当作大规模 LLM serving 的一等瓶颈来治：TP/EP 分片 + DP 复制下每步 decode 同步屏障由最慢 worker 决定，「持续轻微不均衡」会逐步累积成大量浪费。作者形式化在线路由问题——KV cache 迁移昂贵导致分配粘性、单请求负载随时间增长、到达非平稳，路由必须在 100 ms 内对数百待处理请求做决定，给出可上线的实用调度方案。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07719",
    "Fluxion：长上下文 KV 常驻 CPU 场景下的 CPU-GPU 混合稀疏 attention。指出仅靠 sparsity 不够——GPU-only 受 PCIe 与元数据内存约束，CPU-GPU 混合又卡在 CPU 端 top-k 选择与稀疏 attention 计算。三个关键洞察：output-aware KV budget、按 head 与粒度独立配置稀疏度、跨设备协调执行，end-to-end 把 GPU 空转和 PCIe 争用同时打掉。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.06763",
    "把稀疏 attention 重新表述为「range searching」问题：现有 fixed/adaptive budget 方法无法保证 decode 步零假阴性，少选关键 key 就会引发尖峰错误，特别是长推理任务下 important token 集合随步骤漂移。作者据此设计 KV cache 推理高效索引，给出可证明误差边界的 top-k 选择，连续 decode 步全部命中关键 token。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07569",
    "HexiSeq：把长上下文训练的 CP（Context Parallel）+ HP（Head Parallel）扩展到异构 GPU 集群。现有训练系统假设 mesh 同构，但生产环境常混用不同代 GPU 与非均匀网络带宽。HexiSeq 支持完全非对称 CP-HP 切分，按设备 compute/memory/通信能力分配 sequence shard 与 attention head，把异构 CP-HP allocation 形式化为约束优化并给出层级调度器找最优解。",
    "训练",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07363",
    "MISA：把 DeepSeek Sparse Attention（DSA）的 indexer 从 64-head 共享 token 集改为 MoE 池化。DSA 在 V3.2 上 indexer 64 query head 共享同一选中集让 indexer 成为长上下文主导成本；MISA 用 block-level 廉价统计做 router，按 query 仅激活若干 indexer head，drop-in 替换原 indexer 大幅降本同时保持选中质量。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07726",
    "SuperMUC-NG Phase 2 大规模训练实战 recipe：用 Intel Data Center GPU Max 1550 跑 TP+PP+DP 完整并行栈训练 LLM。一万亿参数 GPT 风格模型估算需要 1.2 亿 exaflops，工作给出在 Intel Ponte Vecchio 非主流硬件路线下的可复现训练配方，对国产非 NVIDIA 卡（昇腾/寒武纪等）的训练栈设计有直接参考。",
    "训练",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2510.01290",
    "ThinKV：reasoning 模型长 CoT 输出导致 KV cache 暴涨，本文按「思维类型重要性」做自适应 KV 压缩——观察 attention sparsity 表明 CoT 内不同 thought 重要性差异显著，采用混合量化+驱逐策略：按思维重要性分配 token 精度，随推理轨迹推进渐进驱逐低价值思维 token，并设计扩展 PagedAttention 的 kernel 允许已驱逐 token 的内存高效复用。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07443",
    "RcLLM：生成式推荐场景的 Beyond-Prefix KV cache 分布式推理。前缀 cache 在推荐 workload 收益有限（用户 history × item context 复用非连续），RcLLM 把 prompt 分解为可复用 block，对小巧 user-history cache 做复制实现零延迟检索、对海量 item cache 用 similarity-aware placement 做分片，是把 KV 复用从「线性前缀」推广到「block 级」的产线工程。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07182",
    "Star Elastic：单次 post-training 同时产出 N 个嵌套子模型的 reasoning LLM 训练范式。一个 run 同时训出主模型 + N 个子模型节省 N 倍 compute；推理侧解锁「弹性预算控制」——根据 token 难度动态切档而不再固定架构，适合长 reasoning 任务高低难度混合分布。",
    "训练",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2602.06283",
    "SOCKET：把 LSH 升级为 SOft Collision Kernel EsTimator 用于 sparse attention 长上下文。传统 LSH 二元命中信号限制了 ranking 质量并需大量内存；SOCKET 在多张哈希表上累积 graded collision evidence，保持 top-k 排序质量同时大幅压低内存，配 FlashAttention/Triton kernel 实测可用。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.06914",
    "TAPER：把分支并行（intra-request parallelism）看作机会请求做 per-step admission control。serving 系统目前要么贪心 admit（拉长 shared decode step，伤害同 batch 串行请求），要么硬限上限（牺牲分支带来的 throughput）。论文定义「branch externality」——admit branch 引起的额外 step latency 取决于 batch 组成、上下文长度、累积 slack，且持续变化，TAPER 据此动态裁决何时放分支进 batch。",
    "推理",
))

curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.07985",
    "Dooly：配置无关、冗余感知的 LLM 推理仿真 profile 框架。现有 profile-based simulator 把 op 集合硬编码到某配置，换一个 model/serving engine/attention backend 就要重 profile，成本爆炸。Dooly 注意到很多 op 输入维度由 model 配置或 request 决定，且 head size/layer count 等参数跨模型复用，单次 sweep 即可在多配置间共享，大幅压低做 LLM serving 容量规划/配置选型的 profile 成本。",
    "推理",
))

# Ascend MoE relay-free 通信：用户方向（国产芯片）强信号
curated["papers"].append(pick(
    "papers",
    "https://arxiv.org/abs/2605.06055",
    "Ascend 上的 MoE 推理 relay-buffer-free 通信设计：现有 MoE dispatch/combine 多为 buffer-centric，靠 inter-process 中继与重排 buffer 围绕 collective 传输，本文围绕「直接落入目标 expert 窗口、直接从远端 expert 窗口读」重新组织 dispatch/combine，建在全局池化 HBM 之上避免 routing 引发的布局变换/临时中继/输出复原开销，是国产昇腾 MoE 推理通信路径设计的直接工程信号。",
    "推理",
))

# ============ code ============

curated["code"].append(pick(
    "code",
    "https://github.com/vllm-project/vllm/releases/tag/v0.20.2",
    "vLLM v0.20.2 小补丁：DeepSeek V4 sparse attention 重新启用 Hopper 上 persistent topk 路径，并把 memset kernel 强制放进 CUDA graph capture 阶段而非按 max_seq_len 决定（修 MTP=1 hang，#41665 是 #41605 的 revert）；V4 KV cache 修 V1 引擎 KV block 分配失败；gpt-oss MXFP4 把 hidden_dim_unpadded 接进 moe_forward fake op 让 torch.compile 在 v0.20.x 上工作；Qwen3-VL 去掉重负载下会失败的无效 deepstack 边界检查。延续本月 V4 级 feature「落地→revert→修根因→重上」节奏。",
    "推理",
))

curated["code"].append(pick(
    "code",
    "https://github.com/openai/openai-agents-python/releases/tag/v0.17.1",
    "OpenAI Agents v0.17.1：sandbox 加固一批——把 provider 错误细节带回给上层、限制 sandbox archive 解压、校验 git repo 子路径、允许空 GitRepo 子路径作为 repo root、保留 GitRepo root 子路径别名；tracing 把进程退出时 shutdown 改成 best-effort、保活 BatchTraceProcessor worker 应对 exporter 报错、guard no-op tracing span id；sessions 在 OpenAI conversation session 中保留必需 hosted tool id、pop 时跳过损坏条目、跟踪 MongoDB metadata 时间戳。延续 sandbox/tracing/sessions 持续收紧节奏。",
    "agent",
))

# ============ community ============

# Grinder12 0.96-bit KV cache 压缩（虽热度低但跟用户 TurboQuant/RaBitQ 量化方向直连，且 16.55× VRAM 是极端数字，留作存疑信号）
curated["community"].append(pick(
    "community",
    "https://github.com/ggml-org/llama.cpp/discussions/22891",
    "llama.cpp 社区讨论 Grinder12「0.96-bit 无损流式 KV cache」声称 16.55× VRAM 节省。「sub-bit」无损 KV 极端化路线，与 RaBitQ/TurboQuant per-vector 量化做对比的工程信号点（具体是否真无损待社区复现）。属于持续追踪用户 KV 量化方向的低分位但相关的社区动向。",
    "推理",
))

# MTP 加速速度分布的系统性 benchmark（与 user MTP 兴趣强相关）
curated["community"].append(pick(
    "community",
    "https://www.reddit.com/r/LocalLLaMA/comments/1t9gcar/mtp_benchmark_results_the_nature_of_the/",
    "Qwen 3.6 27B MTP 投机解码系统 benchmark：300+ 次测试得出关键结论——「生成任务性质决定 MTP 是否加速」。F16 + MTP 在 coding 任务下提速近 3 倍，Q4_K_M + MTP 在创意写作下反而更慢——同一特性同一模型同一设置，结果相反。投机解码加速比 = f(草稿接受率, 任务文本熵)，coding 高接受率高加速，creative 低接受率反而被 verify 开销吃掉。",
    "推理",
))

# Tracing tokens through Llama 3.1 8B inference on H100s（推理内部数据流可视化教学）
curated["community"].append(pick(
    "community",
    "https://krithik.xyz/what-is-inference-actually",
    "Tracing Llama 3.1 8B on H100：从 token 进入到 logits 输出全链路追踪，按层展开 attention/MLP/normalization/sampling 实际 GPU 上做什么。对系统学习 LLM 推理 dataflow（embedding → attention → KV update → MLP → sampling）与 Transformer Math Explorer 同类的教学读物。",
    "推理",
))

# ExLlamaV3 DFlash 加速大更新——投机解码工程化跟踪
curated["community"].append(pick(
    "community",
    "https://www.reddit.com/r/LocalLLaMA/comments/1t9voxs/exllamav3_major_updates/",
    "ExLlamaV3 Turboderp 连续更新：Gemma 4 支持、改进 cache 效率、两周前 DFlash 上线，agentic/code 任务 2.5× 加速（55.98→140.61 t/s）、coding 3× 加速（59.21→177.67 t/s）、创意/翻译 1.3-2× 加速。延续 ExLlamaV3 把投机解码工程化做到单卡量化推理引擎的趋势，对位 llama.cpp speculative 路线。",
    "推理",
))

now = datetime.now(timezone.utc).isoformat()
out = {
    "generated_at": now,
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": curated,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK -> {OUT}")
print(f"papers={len(curated['papers'])} code={len(curated['code'])} blogs={len(curated['blogs'])} community={len(curated['community'])}")
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for sec in curated.values():
    for it in sec:
        tag_count[it["domain_tag"]] += 1
print(f"domain_tag: 推理 {tag_count['推理']} / 训练 {tag_count['训练']} / agent {tag_count['agent']}")
