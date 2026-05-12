# -*- coding: utf-8 -*-
"""一次性 curated 生成脚本 - 2026-05-12"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with RAW.open("r", encoding="utf-8") as f:
    raw = json.load(f)


def find_item(section, title_contains=None, link_contains=None):
    for it in raw["sections"][section]:
        if title_contains and title_contains.lower() in it["title"].lower():
            return it
        if link_contains and link_contains in it["link"]:
            return it
    return None


def enrich(item, tldr, domain_tag):
    out = dict(item)
    out["tldr"] = tldr
    out["domain_tag"] = domain_tag
    return out


curated_papers = []
curated_code = []
curated_blogs = []
curated_community = []

# ===== papers =====
# 1. SPECTRE 多租推理利用 tail model 作 remote drafter
it = find_item("papers", link_contains="2605.08151")
if it:
    curated_papers.append(enrich(
        it,
        "多模型云服务推理框架 SPECTRE：把利用率低的小尾部模型当作大热门模型的远程 draft model，混合「顺序+并行」投机解码并通过吞吐量分析阈值切换。draft 与 verify 真正并行运行，化「闲置 tail 容量」为大模型加速燃料，针对长尾多租场景规避对额外 drafter 的训练与部署。",
        "推理",
    ))

# 2. Surviving Partial Rank Failures in Wide EP MoE Inference
it = find_item("papers", link_contains="2605.10670")
if it:
    curated_papers.append(enrich(
        it,
        "宽 EP MoE 推理的部分秩故障容错：现有 EP 栈把 rank 集合固定到初始化阶段，单节点失败拖垮整服务。论文把 communicator、专家放置、CUDA Graph 路由元数据全部解耦，让 EP 在故障时缩容继续提供服务而非整体重启——MoE 大规模 EP 推理生产化的关键基建（直接命中 DeepEP / SGLang 路线）。",
        "推理",
    ))

# 3. Continuum agent KV TTL 调度（V5 replace，4/28、5/6 同名 v3/v4 是同篇升级）
it = find_item("papers", link_contains="2511.02230")
if it:
    curated_papers.append(enrich(
        it,
        "Continuum v5 升级：agent 工作流 LLM 调用穿插 tool call 导致传统 KV 驱逐 + 队列等待两难。本版本把「重算/重载成本 vs GPU 等待成本」纳入统一 TTL 决策，对 tool 调用时长方差做内部分布建模；对 agent serving 场景的 KV 利用率天花板再抬一档。",
        "推理",
    ))

# 4. SplitZip 无损 KV 压缩 PD 分离（v2 replace，5/5 首次覆盖，今日 v2 更新）
it = find_item("papers", link_contains="2605.01708")
if it:
    curated_papers.append(enrich(
        it,
        "SplitZip v2：PD 分离架构下，prefill→decode worker 间 KV 跨机传输成为瓶颈，离线权重压缩用的 CPU 变长编码完全不适用。SplitZip 给 GPU 原生超快无损 KV 编码方案，与 disagg/long-context/agent workload 直接相关，本版本扩 FP8 KV 支持。",
        "推理",
    ))

# 5. Sparse Attention as Range Searching - KV Cache index
it = find_item("papers", link_contains="2605.06763")
if it:
    curated_papers.append(enrich(
        it,
        "把稀疏注意力建模成「区间搜索」问题：在 fixed/adaptive token budget 下选 top-k key 时漏掉关键 token 误差激增，尤其长 reasoning 中重要 token 集合随 decode step 漂移。论文给推理高效索引，保证零假阴性（critical key 不丢），针对长上下文 reasoning 调用直接补齐稀疏 attention 准确性证明。",
        "推理",
    ))

# 6. KernelBenchX (cs.PF + cs.LG 同 ID 去重)
it = find_item("papers", link_contains="2605.04956")
if it:
    curated_papers.append(enrich(
        it,
        "KernelBenchX 全面评测 LLM 写 Triton GPU kernel：176 任务跨 15 类，对比 5 种方法。核心发现：任务结构对正确性影响是方法设计的 3 倍（9.4% vs 3.3% 解释方差），Fusion 类 72% 全员失败、Math 类基本都对。补齐 5/7 KernelBench-X 的 categorical 维度，对 coding agent 写 kernel 的能力边界给出可复现 benchmark。",
        "agent",
    ))

# 7. Priming Hybrid SSM from pretrained transformer
it = find_item("papers", link_contains="2605.08301")
if it:
    curated_papers.append(enrich(
        it,
        "Priming：把 Hybrid（Attn+SSM）架构设计从「从头预训练问题」变成「知识迁移问题」——拿预训练 Transformer 初始化 Hybrid 模型，做短期对齐+后训练阶段即可恢复下游质量。对 KV cache 更小、decode 更快的 Hybrid 工程化路径直接降本，给 Mamba/Falcon-Mamba 类后续推广扫清成本障碍。",
        "训练",
    ))

# 8. Nautilus Compass agent memory drift (cs.LG + cs.CL 同 ID 去重)
it = find_item("papers", link_contains="2605.09863")
if it:
    curated_papers.append(enrich(
        it,
        "Nautilus Compass：生产 coding agent 长会话「persona drift」黑盒检测——纯 prompt 文本层用 BGE-m3 embedding 算用户 prompt 与行为 anchor 的 cosine top-k 加权均值，无需模型权重所以可用于 Claude/GPT-4 闭源 API。对 Mem0/Letta/Cognee/Zep/MemOS 路线是首个可量化 drift 监控层。",
        "agent",
    ))

# 9. KV-RM static graph KV movement (cs.AR + cs.OS 同 ID 去重)
it = find_item("papers", link_contains="2605.09735")
if it:
    curated_papers.append(enrich(
        it,
        "KV-RM：静态图 LLM decoder 启动开销低、tensor shape 固定，但在线 decode 的 KV 行为天然不规则（请求长度异质 + EOS 异步 + 逻辑历史碎片化）。KV-RM 在固定 decode 接口下解耦逻辑 KV 与物理存储，吸收变动性而保留静态图低延迟优势——给「静态图执行器+动态请求」的鸿沟一个新工程方案。",
        "推理",
    ))

# 10. Value-Aware KV Eviction Fixed-Contract Diagnostic
it = find_item("papers", link_contains="2605.08234")
if it:
    curated_papers.append(enrich(
        it,
        "提出 KV 驱逐 selector 失效的三步诊断：漏证据、误打高分给无影响 token、把相关证据切散。在 fixed-contract 框架下逐项分离贡献，给 value 排名用「block attention mass × 移除后输出变化」组合指标；LongBench 跨 3 模型 2 budget 实证 value-aware 选择何时真正有用、何时是噪声。",
        "推理",
    ))

# 11. TLX hardware-native MIMW GPU compiler for Triton
it = find_item("papers", link_contains="2605.10905")
if it:
    curated_papers.append(enrich(
        it,
        "TLX（Triton 低层语言扩展，围绕 MIMW Multi-Instruction Multi-Warp）：在 warp-group 粒度表达数据搬运、tensor core 计算、同步的编排，保留 Triton 块编程模型同时把 Hopper/Blackwell 异步硬件机制显式暴露。给大型生产环境一条「让编译器不必追赶硬件」的可演化通路。",
        "推理",
    ))

# 13. ReRAM-on-Logic LLM Accelerator with speculative decoding
it = find_item("papers", link_contains="2605.09375")
if it:
    curated_papers.append(enrich(
        it,
        "55nm ReRAM-on-logic 堆叠 LLM 加速芯片：14.08-135.69 tok/s。本地 rotation 单元实现「免离群点」低 bit 量化，stacking-aware PNM 配合 blockwise vector quantization 降权重 EMA 开销，自适应并行投机解码+乱序调度提升资源带宽利用率，相比 vanilla 投机解码 4.46-7.17×。把 PIM/堆叠+投机解码完整跑通的 ISSCC 级硬件信号。",
        "推理",
    ))

# 15. Not All Thoughts Need HBM: tier-aware reasoning KV
it = find_item("papers", link_contains="2605.09490")
if it:
    curated_papers.append(enrich(
        it,
        "Reasoning LLM 千级思维 token KV 都要驻 HBM 才行？永久驱逐 50% 半精度 token 准确率崩到 0-2.5%。论文提语义感知存储分层（HBM/DDR/压缩/驱逐 四档），累积 attention 评分排序，低权重 token 下沉 CPU 内存 + 每 attention step 全精度 prefetch 回 GPU，等价零误差——对 reasoning 长输出 KV 工程是「不丢精度+不爆 HBM」的双赢方案。",
        "推理",
    ))

# 17. Test-Time Speculation (speculator 长输出衰减问题)
it = find_item("papers", link_contains="2605.09329")
if it:
    curated_papers.append(enrich(
        it,
        "Test-Time Speculation：当前 SOTA 投机解码器（DFlash/EAGLE-3/PARD）在几千 token 后接受长度衰减到接近 1，long-response 任务彻底失速——根因是 draft 离线短序列训练而 inference 走长序列分布外。提推理时自适应方案修复 long-response 投机解码可用性，对 reasoning model 部署直接 actionable。",
        "推理",
    ))

# 18. Hidden States Drift speculative decoding rescue
it = find_item("papers", link_contains="2604.26412")
if it:
    curated_papers.append(enrich(
        it,
        "针对投机解码 SOTA hidden-state drafter 的「长距离衰减」：target hidden state 是带偏的上下文压缩（按当前位置 attention query 聚合历史），TTT 训练也救不回来。论文从上下文信息保留角度引入 KV cache 增援机制，把长距离投机解码 draft 精度拉回——补 5/11 DP 负载均衡之后投机解码长上下文链路。",
        "推理",
    ))

# 19. TiledAttention cuTile Python SDPA kernel
it = find_item("papers", link_contains="2603.01960")
if it:
    curated_papers.append(enrich(
        it,
        "TiledAttention：用 cuTile Python（TileIR）写的 SDPA forward 算子，FlashAttention 风格 online-softmax + tiled K/V streaming，作为 PyTorch 可调用函数暴露。schedule 级（tile shape / staging / shared memory layout）Python 端可直接改，比 CUDA 模板低门槛但保留真实行为——对 attention 研究 reproducible benchmark 路线的官方推广作。",
        "推理",
    ))

# 20. AGoQ 4-bit activation + 8-bit gradient
it = find_item("papers", link_contains="2605.00539")
if it:
    curated_papers.append(enrich(
        it,
        "AGoQ：4-bit 激活 + 8-bit 梯度训练量化——分层感知给各层激活按 type+pipeline stage 自适应 bit 宽（近 4-bit 储存）、8-bit 梯度 + 精度保持 8-bit All-Reduce 通信压缩。比单纯量化更精细且通信侧也省，5/4 同名 paper 今日 v2 替换，对 Megatron-LM 类训练栈直接接入有参考。",
        "训练",
    ))

# 21. FCP flexible context parallelism
it = find_item("papers", link_contains="2605.08524")
if it:
    curated_papers.append(enrich(
        it,
        "FCP（Flexible Context Parallelism）：现有 CP 设计要么把短序列过度切片、要么把长短序列分开处理无 bin-packing 引发负载不均。FCP 在 block 粒度分片+调度，抛弃环形等刚性拓扑允许任意 P2P 通信，灵活映射放置——对长上下文 pretraining 序列长度高方差的训练栈是新基建。",
        "训练",
    ))

# 22. Lakestream brokerless training data plane
it = find_item("papers", link_contains="2605.09994")
if it:
    curated_papers.append(enrich(
        it,
        "Lakestream：大基模训练数据 plane 重构。共址 dataloader 无故障隔离、消息队列式 disagg dataloader 表达不了 batch-level 语义。Lakestream 用 Transactional Global Batch（基于 lakehouse ACID + 训练特化一致性，原子 all-rank batch 可见性）替代 record/offset 抽象——给百万卡级训练数据 plane 一条无 broker、object-store 原生的工程路线。",
        "训练",
    ))

# 23. MegaScale-Omni multimodal LLM training
it = find_item("papers", link_contains="2605.08962")
if it:
    curated_papers.append(enrich(
        it,
        "字节 MegaScale-Omni：工业级 MLLM 训练系统应对动态模态混合比与样本长度分布。Encoder-LLM 复用方案三关键创新——长短序列并行的解耦并行策略、动态资源分配、模型并行随负载漂移——把 hyper-scale 部署下「encoder/LLM 静态切分」打破，对生产级 MLLM 训练直接参考价值。",
        "训练",
    ))

# ===== code =====
# 24. LMDeploy v0.13.0
it = find_item("code", title_contains="v0.13.0")
if it and "lmdeploy" in it["link"].lower():
    curated_code.append(enrich(
        it,
        "LMDeploy v0.13.0：Ascend 后端支持 Qwen3.5 35B-A3B；turbomind 集成 cublasGemmGroupedBatchedEx 给 Qwen3.5 MoE 在 Blackwell 上做内存拷贝优化；新增 TurboQuant（quant_policy=42）KV cache 量化（与用户 RaBitQ/TurboQuant 方向直连，继 vLLM #39931 之后第二个主线推理引擎落地）；Anthropic 兼容 serving 端点；kernel block size 支持。国产芯片 + TurboQuant + MoE 三线齐发的版本。",
        "推理",
    ))

# 25. OpenAI Agents v0.17.1 + v0.17.2 合并
it1 = None
it2 = None
for it in raw["sections"]["code"]:
    if it["source"] == "OpenAI Agents":
        if "v0.17.1" in it["title"]:
            it1 = it
        elif "v0.17.2" in it["title"]:
            it2 = it
if it2:
    curated_code.append(enrich(
        it2,
        "OpenAI Agents Python 一晚连发 v0.17.1 + v0.17.2：sandbox 三轴（archive 提取上限、GitRepo subpath 校验、空 subpath 处理）+ tracing（进程退出 best-effort、BatchTraceProcessor exporter 错误后 worker 存活、no-op span ID 守卫、shutdown 时打断 retry backoff）+ sessions（hosted tool ID 保留、corrupt item pop 跳过、MongoDB metadata 时间戳）+ realtime（未知工具不自动回应）+ MCP/sandbox 错误细节传递。延续本周三轴持续加固节奏。",
        "agent",
    ))

# 26. LangGraph 1.2.0 + checkpoint family（合并 6 个 release）
it = None
for r in raw["sections"]["code"]:
    if r["source"] == "LangGraph" and r["title"] == "langgraph==1.2.0":
        it = r
        break
if it:
    curated_code.append(enrich(
        it,
        "LangGraph 1.2.0 全家桶正式版：langgraph==1.2.0 + checkpoint==4.1.0 + checkpoint-postgres==3.1.0 + checkpoint-sqlite==3.1.0 + prebuilt==1.1.0 + cli 0.4.26 一晚一齐 bump 出 alpha。核心特性——主机崩溃后 durable error-handler 跨进程 resume / StateGraph.set_node_defaults() / checkpoint 强制 delta channel snapshot 每隔 max supersteps（避免 delta 链过长重建慢）/ checkpoint-sqlite 重写 get_delta_channel_history 为 streaming walk。1.1 timers 重构 → 4/28 revert → 5/2 6 个 alpha → 5/11 a7 → 今日 1.2.0 正式版的完整收敛曲线。",
        "agent",
    ))

# ===== blogs =====
# 27. NVIDIA Fleet Intelligence
it = raw["sections"]["blogs"][0] if raw["sections"]["blogs"] else None
if it:
    curated_blogs.append(enrich(
        it,
        "NVIDIA Fleet Intelligence：大型 GPU 集群实时可见性与优化平台，作 GPU fleet 级监控/优化中枢。对 100k+ GPU 数据中心做集群健康+利用率统一观测，与 OpenAI/MS MRC+SRv6 之类生产级集群观测层互补。给 GPU 集群运维「再上一层 fleet 控制平面」的官方信号。",
        "推理",
    ))

# ===== community =====
# 28. r/ML hackable LLM compiler 6 IRs
it = find_item("community", link_contains="1tag07l")
if it:
    curated_community.append(enrich(
        it,
        "可 hack 的 LLM 编译器从零写：TVM 50 万+ 行 C++ / PyTorch 堆 Dynamo+Inductor+Triton，作者自建 6 层 IR 把 TinyLlama / Qwen2.5-7B 端到端降为一串 CUDA kernel。RTX 5090 上 FP32 几何平均 1.11×（vs PyTorch eager）+ 1.20×（vs torch.compile），小规约/SDPA/kv-projection 最高 4.7×，dense matmul seq=512 略输。第二部分深入 Tile IR/Kernel IR 与 lowering 规则——对内部教学+理解 Inductor/TVM/XLA 替代栈的极好阅读资料。",
        "推理",
    ))

# 29. Gemma 4 MTP vs DFlash on H100
it = find_item("community", link_contains="1tb160j")
if it:
    curated_community.append(enrich(
        it,
        "Gemma 4 31B / 26B-A4B 在 1×H100 80GB + vLLM 上跑 SPEED-Bench 880 prompt 跨 11 类的 MTP vs DFlash 投机解码对照。dense 31B：MTP 3.11× / DFlash 3.03×（baseline 40.3→125.3 tok/s @ MTP 8 / DFlash 15 spec token）。两套投机解码方案在 dense 模型上几乎打平，给「MoE 还是 dense / spec token 数怎么选」一手数据，对 vLLM MTP 路线选型直接 actionable。",
        "推理",
    ))

# 30. Optane PMem 1T model 4 tok/s
it = find_item("community", link_contains="1taeg8h")
if it:
    curated_community.append(enrich(
        it,
        "Intel Optane Persistent Memory（DIMM 介乎 DRAM 与 SSD）二手买配 768GB 跑 Kimi K2.5 万亿参数模型 4 tok/s。Optane 走 Memory Mode 暴露给系统作 DRAM-级（DRAM 当 cache）——对内存墙极致预算场景给一个 cost/GB 极低的 LLM 推理替代路线。Optane 虽 EOL 二手仍流通，对 ScaleUp 统一内存方向与国产 CXL 内存池路径都是实测参考。",
        "推理",
    ))

# 31. KV entropy coder lossless ~4×
it = find_item("community", link_contains="kv-entropy-coder")
if it:
    curated_community.append(enrich(
        it,
        "Speculative KV coding 博客实现：用一个小模型对 KV cache 做投机式熵编码，无损压缩约 4×。把投机解码的「target 模型预测分布近似」思路反向用到 KV 存储——decode 时小模型预测 KV 分布、用真实 KV 与预测差分编码。给 KV cache 无损压缩链路再加一个工程化思路（与 SplitZip 的 GPU 原生编码、ZipCCL 集合通信无损压缩形成完整 sub-track）。",
        "推理",
    ))

# 32. VibeServe agent build serving systems
it = find_item("community", link_contains="vibe-serve")
if it:
    curated_community.append(enrich(
        it,
        "UW SyFI 实验室 VibeServe：让 AI agent 自动构建定制 LLM serving 系统。把 agent 写代码能力推到「写自己的推理引擎+调度」这种系统级 infra 任务上的实验，对 FACT（agent 驱动 CUTLASS 合成）/ KernelBenchX（LLM 写 Triton kernel 评测）形成上层一致路线——agent 写 infra 已从单 kernel 上升到完整 serving stack。",
        "agent",
    ))

# 33. ubatch prompt processing on gpt-oss-120B
it = find_item("community", link_contains="1tany5t")
if it:
    curated_community.append(enrich(
        it,
        "gpt-oss-120B-F16 在 RTX 3090 24GB 部分卸载 MoE 到 CPU 的 llama.cpp 实测：把物理 micro-batch -ub 从默认 512 拉到 4096-8192 并同步抬 --n-cpu-moe 到 26-28，prefill 吞吐 380→2090 tok/s（5.5×）而 decode 基本不动。对 partial offload MoE 推理调优是直接可复用配方——MoE prefill 是 CPU↔GPU 拷贝-launch 联合瓶颈，大 ubatch 摊平 launch 与拷贝最有效。",
        "推理",
    ))

# now check counts
print(f"papers: {len(curated_papers)}")
print(f"code: {len(curated_code)}")
print(f"blogs: {len(curated_blogs)}")
print(f"community: {len(curated_community)}")

# domain_tag stats
all_items = curated_papers + curated_code + curated_blogs + curated_community
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for it in all_items:
    tag_count[it["domain_tag"]] = tag_count.get(it["domain_tag"], 0) + 1
print(f"domain_tag: {tag_count}")
print(f"total: {len(all_items)}")

out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {
        "papers": curated_papers,
        "code": curated_code,
        "blogs": curated_blogs,
        "community": curated_community,
    },
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"wrote {OUT}")
