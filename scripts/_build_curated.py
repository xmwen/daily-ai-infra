"""一次性脚本：读取 today_raw.json，按偏好挑选并写中文 tldr，输出 today_curated.json。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with RAW.open(encoding="utf-8") as f:
    raw = json.load(f)

# key = link, value = (section, item, tldr, domain_tag)
# 按 link 去重，同一 arXiv ID 在多分区出现时只保留一条（优先 cs.DC/cs.AR/cs.PF）
selections = []

def pick(section, link, tldr, domain_tag):
    selections.append((section, link, tldr, domain_tag))

# ==== papers（推理侧集中爆发）====
pick("papers", "https://arxiv.org/abs/2604.26039",
     "RaMP 针对 MoE 推理提出路由感知 kernel dispatch 框架：现有系统只按 batch size 选 kernel，忽视 expert 路由分布，损失 10-70% 吞吐。RaMP 用 4 参数 wave 代价模型从硬件常量出发推导各优化适用区间，按运行时 expert 直方图选最快配置，在 8 种架构（含 3 个未见架构）上对比 exhaustive search 平均遗憾仅 0.93%，每模型只需 10-24 分钟一次性 profiling。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26557",
     "DUAL-BLADE 把 NVMe offload KV cache 升级为双路径：根据运行时内存压力动态把 KV tensor 分配到 page-cache 路径或 NVMe-direct 路径；direct 路径绕过文件系统，把 KV tensor 映射到连续 LBA，避免 page cache thrashing 与不可预测延迟。面向 edge LLM 推理，补齐长上下文 KV 溢出场景下的 storage stack 工程化短板。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26074",
     "DAK 提出 direct-access 内存 offload：不再 prefetch 到本地 HBM（现有做法会引入 HBM 争用、浪费容量、产生 pipeline bubble），而是复用 TMA 异步从远端内存直接取 offloaded weights 和 KV cache 到 GPU 寄存器。把远端访问做成系统级原语，解决 tiered memory 推理下 HBM 带宽饱和而容量不足的两难。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26666",
     "FACT 提出三阶段 agent 驱动的 kernel 合成流水线：不再让 LLM agent 直接生成 raw CUDA（会重新发明已有优化），而是 grounded 到 CUTLASS C++ 模板库——先 pattern discovery 匹配子图，再多 pattern 组合。把 agent 的作用限定在编译器 catalog 缺失处补洞，对 kernel 生成 agent 的系统设计有启发：库 grounding > 裸 CUDA 生成。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26103",
     "AMMA 提出 multi-chiplet memory-centric 架构服务 1M 上下文 attention：现有 serving（含 NVIDIA Rubin GPU-LPU）仍把 GPU 当中心，但 decode 阶段 attention 是 memory-bound 与 GPU compute-heavy 架构本质错配。AMMA 把 KV cache 下沉到 PIM/PNM chiplet，attention 计算就近执行，用 GPU 只做剩余部分。符合长上下文 + agentic workload 下 attention 成为用户面瓶颈的趋势。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26334",
     "xLM 客户端推理：提出 pipelined sharding——sub-layer 级模型分片 + CPU offload + pipelined copy-compute + VRAM 内优先级张量放置，同时优化 TTFT 与 TPS，适配 dense 与 MoE。面向 VRAM 受限客户端场景（例如 5090/4090 单卡跑 Llama4/DSV3），工程化把 llama.cpp 式 offload 流水线再推一步。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26837",
     "SPIN 统一稀疏 attention + 分层 KV 存储：现有稀疏算法粒度不一只能 ad hoc 实现；分层 KV 存储从 CPU 取 fine-grained 不规则子集又会吃掉稀疏收益。SPIN 把两层一起做 sparse-attention-aware 推理框架，把算法级稀疏收益真正落到端到端。对应用户关注的 per-slot KV cache 布局 + 稀疏检索这条工程链路。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.25326",
     "AHASD 面向移动端 NPU+PIM 投机解码：传统 operator 级同步执行有 idle 开销，异步执行又因 draft 长度波动产生浪费。AHASD 把 drafting 放到 PIM 并行执行、verification 在 NPU 上做，task-level DLM-TLM 解耦；并用 Entropy-History 自适应 draft 长度。是移动端异构硬件上投机解码的又一条工程路径。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26412",
     "长程投机解码新角度：hidden-state-based drafter 的 long-range decay 即使用 test-time training 也修不完。本文把原因归到「target hidden state 是按当前 attention query 做的有偏上下文压缩，擅长下一 token 但压缩了远程信息」，转而用 KV cache 反向恢复远程上下文。对用户关注的 KV cache 量化 + 投机解码精度链路有直接借鉴。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26779",
     "在 NeMo-RL + vLLM 后端实现投机解码做 RL post-training rollout 加速：把 spec decoding 定位成无损加速原语，保留 target 分布；支持同步/异步流水线，在 rollout 阶段用 MTP heads 或小 draft 模型做投机。打通 spec decoding 到 RL 训练 rollout 这条场景，是 vLLM × Megatron/NeMo-RL 推理-训练联动的典型例子。",
     "训练")

pick("papers", "https://arxiv.org/abs/2604.26881",
     "FaaSMoE 把 MoE 专家做成 FaaS stateless function：通过控制面与执行面解耦，按需调用 + scale-to-zero，解决 multi-tenant MoE 服务中激活专家少于常驻专家、资源浪费的矛盾。对应生产级 MoE serving 调度方向，与 Janus（expert 独立 worker 池）思路互补。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26294",
     "TSP 把 tensor parallelism 与 sequence parallelism 叠到同一 device 轴：传统 TP 切 weight、SP 切 token，各用一个 mesh 维度；TSP 让每个 rank 同时持有 weight shard 和 sequence shard，在同一轴上同时降参数与激活内存。attention 用广播 weight+seq-wise KV 通信重建上下文。是 3D 并行之外的新轴折叠范式。",
     "训练")

pick("papers", "https://arxiv.org/abs/2604.26687",
     "COPUS 指出 batch size 与 3D 并行策略本质耦合：过去做法要么固定并行、只调 batch（优化派），要么固定 batch、只调并行（系统派），都是次优。COPUS 联合自适应两者，沿 critical batch size 轨迹动态切换最优并行策略。对大规模 LLM 训练调度有直接工程参考。",
     "训练")

pick("papers", "https://arxiv.org/abs/2604.26256",
     "DORA 面向 RL post-training 异步训练：rollout 阶段占 50-80% 步骤时间，长尾轨迹阻塞整条流水线。DORA 识别出异步训练保持收敛的三个约束——轨迹内策略一致性、数据完整性、有界 staleness，提出针对长尾轨迹的内禀解决方案，而非传统 off-policy/replay 绕开。",
     "训练")

pick("papers", "https://arxiv.org/abs/2604.26889",
     "逆向 NVIDIA 闭源 userspace driver 命令流：利用开源 kernel driver 打桩 memory-mapping 路径 + GPU doorbell 寄存器硬件断点，完整捕获 CUDA API 到硬件命令的翻译链路。对国产芯片做 CUDA 语义对齐、对 kernel 级性能建模（用户 VisitorBound_Scorpiox2 方向）都是难得的白盒材料。",
     "推理")

pick("papers", "https://arxiv.org/abs/2604.26821",
     "Voxel 是 3D 堆叠 AI 芯片（DRAM on compute die 分布式 TSV）的编译器感知模拟器：3D 堆叠打通存储墙，但计算范式、ML 编译器优化、底层硬件三层纠缠难以协同设计。Voxel 为这类 memory-near-compute 架构提供快速探索工具。与 AMMA 一起构成今日 3D/PIM 存算一体的两条工程路径。",
     "推理")

# ==== code ====
pick("code", "https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13",
     "TensorRT-LLM v1.3.0rc13：新增 Nemotron 3 Nano Omni 支持与 ViT attention 优化、GLM-4.7/GLM-5 tool parser、DeepSeek-V3.2 与 V3-Lite 在 Blackwell/SM100 上的 perf + chunked-prefill 修复。昨日 FA4 beta11 在 Blackwell 侧同步推进，TensorRT-LLM 这次把 DSV3.2 chunked-prefill 路径落到 rc 级稳定——对标昨日 SnapMLA 论文，工业栈这条链路几乎同步跟进。",
     "推理")

pick("code", "https://github.com/kvcache-ai/ktransformers/releases/tag/v0.6.1",
     "KTransformers v0.6.1：大 MoE LoRA SFT 重构，后端迁移到 kt-kernel，打包为 ktransformers[sft]。相对 ZeRO-Offload 基线训练性能 6-12×，CPU 内存降一半，GPU 内存压力也更低。延续 LLaMA-Factory 训练入口和 YAML 工作流，是 CPU offload + MoE SFT 路线的重要版本。",
     "训练")

pick("code", "https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.10rc1",
     "FlashInfer v0.6.10rc1：trtllm attention kernel 新增 head_dim=512 支持；SM90 上 MXFP4×BF16 与 INT4×FP8 CUTLASS MoE backend 做了 perf；新增 DCP all-to-all kernel 支持 context-parallel attention reduction；allreduce/allgather/reducescatter 组合路径补齐。继续沿「attention kernel 变种 × MoE 量化 × 通信」三轴扩展。",
     "推理")

pick("code", "https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta11",
     "FA4 v4.0.0 beta11：CUTE DSL 补齐 head_dim=256 正反向；Flex autograd 接入 cute，flash_attn_varlen_func 加 score_mod_bwd 参数；blocksparse 接口在 flash_attn_func 里简化；SM100 MLA kernel stream 修复与 empty-tile 正确性 guard。整体在 Flex 可微 + MLA SM100 + hd256 三条线同步完善。",
     "推理")

pick("code", "https://github.com/langchain-ai/langgraph/releases/tag/1.2.0a1",
     "LangGraph 1.2.0a1 alpha：引入 timers（idle/dynamic push-task timeouts）——这是前天 1.1.10 紧急 revert node-level timeouts 之后，把 timeout 方案重构成 channel-level；新增 DeltaChannel 在 blobs 存 sentinel 并从 checkpoint_writes 重建；streaming transformer 基础设施合入；EventLog 合并进 StreamChannel。前阵子「feature 落地即回滚」事件后，官方给出的工程答卷。",
     "agent")

pick("code", "https://github.com/langchain-ai/langgraph/releases/tag/prebuilt%3D%3D1.0.13",
     "LangGraph prebuilt 1.0.13：修复 ToolRuntime tools 默认为 None 的问题改成空 list；同步合入 timers alpha 与 StreamChannel 重构。前几天 prebuilt 1.0.12 刚修了 ToolNode channel hydration，本次又发现 ToolRuntime 默认参数坑——tool 调用链路的边界条件 bug 在持续暴露。",
     "agent")

pick("code", "https://github.com/openai/openai-agents-python/releases/tag/v0.14.8",
     "OpenAI Agents v0.14.8：修复 MCP re-export 丢失 ImportError 导致上层看不到真正的 import 失败原因；sandbox prompt instruction 段落分隔符修复。延续昨天 v0.14.7 的 tar/zip member 加固、symlink LocalFile reject，本次继续在「MCP 与 sandbox 边界可观测性」上迭代。",
     "agent")

pick("code", "https://github.com/mlc-ai/xgrammar/releases/tag/v0.1.34",
     "XGrammar v0.1.34：EBNF parser 接受 {n,-1} 作无界 repeat；AnyTokensFormat 在 exclude_tokens 下按 self-terminating 处理；新增 Gemma 4 内置 structural tag 支持；binding 逻辑重新迁到 tvm_ffi；去掉 unlimited 限制的结构化输出上限。对结构化输出/constrained decoding 栈继续补齐。",
     "agent")

# ==== community（严格筛，排除非基础设施/水贴）====
pick("community", "https://www.reddit.com/r/LocalLLaMA/comments/1szv6z0/actual_comparison_between_locally_ran_qwen3627b/",
     "作者在单卡 3090 + Xeon 老服务器上长期跑 Qwen3.6-27B，对比云端低档模型做真实工程任务（写代码/agent workflow），得出在日常 coding 任务中本地 27B 量化已能与中档云模型接近的结论，并详细记录了 KV cache/FP8/Claude Code/Codex 搭配经验。是「本地 27B 类模型是否够用」当前比较诚实的实测样本。",
     "推理")

pick("community", "https://www.reddit.com/r/LocalLLaMA/comments/1sznc6q/amd_engineers_directly_seeking_rocm_feedback/",
     "AMD 工程师直接在 r/LocalLLaMA 征集 ROCm 使用反馈。最近一周 ROCm 相关信号（hipfire 社区引擎、Strix Halo HFQ4 MMQ 3×、KTransformers v0.6.1 含 ROCm 支持）持续出现，AMD 侧对本地 AI 硬件生态的态度明显主动化，是国产/非 CUDA 推理生态的一个重要外部参照。",
     "推理")

# 过滤：Mistral-Medium-3.5（商业模型）、Qwen-Scope（SAE 研究非基础设施）、
#       DeepSeek Thinking-with-Visual-Primitives（多模态推理范式非 infra）、
#       5M 模型实验（小模型玩具）、Qwen svg 生成 demo、Qwen sticker、algif 内核漏洞（非 AI infra）

raw_papers = raw["sections"]["papers"]
raw_code = raw["sections"]["code"]
raw_blogs = raw["sections"]["blogs"]
raw_comm = raw["sections"]["community"]

def find_item(section_items, link):
    for it in section_items:
        if it["link"] == link:
            return it
    return None

curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}
seen_links = set()
for section, link, tldr, domain_tag in selections:
    if link in seen_links:
        continue
    seen_links.add(link)
    pool = {"papers": raw_papers, "code": raw_code, "blogs": raw_blogs, "community": raw_comm}[section]
    item = find_item(pool, link)
    if item is None:
        print(f"[warn] missing link: {link}")
        continue
    new_item = dict(item)
    new_item["tldr"] = tldr
    new_item["domain_tag"] = domain_tag
    curated_sections[section].append(new_item)

out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": curated_sections,
    "source": "curated",
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

counts = {k: len(v) for k, v in curated_sections.items()}
tag_dist = {}
for sec in curated_sections.values():
    for it in sec:
        tag_dist[it["domain_tag"]] = tag_dist.get(it["domain_tag"], 0) + 1
total = sum(counts.values())
print(f"curated: {total} items, sections={counts}, domain_tag={tag_dist}")
print(f"generated_at: {out['generated_at']}")
print(f"raw generated_at: {raw['generated_at']}")
