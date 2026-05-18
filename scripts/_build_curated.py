"""一次性脚本：根据 today_raw.json 生成 today_curated.json（中文 tldr + domain_tag）。
本次手写筛选，运行后即可丢弃，下次自动化会再生成。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with RAW.open("r", encoding="utf-8") as f:
    raw = json.load(f)


def find(section, *kw_any):
    """在 raw[section] 里找 title 含任意关键字的第一条。"""
    items = raw["sections"].get(section, [])
    for it in items:
        title = it.get("title", "").lower()
        for kw in kw_any:
            if kw.lower() in title:
                return it
    return None


def attach(it, tldr, domain_tag):
    new = dict(it)
    new["tldr"] = tldr
    new["domain_tag"] = domain_tag
    return new


curated = {"papers": [], "code": [], "blogs": [], "community": []}

# ====== papers（最多 20 条，今日实选 9 条）======
seen_links = set()

def add_paper(it, tldr, tag):
    if it is None:
        return
    if it["link"] in seen_links:
        return
    seen_links.add(it["link"])
    curated["papers"].append(attach(it, tldr, tag))


add_paper(
    find("papers", "LMDeploy Accelerates Mixed-Precision"),
    "LMDeploy 团队提出 TurboMind：一套硬件自适应的混精度 LLM 推理引擎，核心是两条流水线——GEMM pipeline 用 hardware-aware 的精度组合（W/A/KV 任意 INT/FP 配比）自动生成 kernel，避免人手调优；attention pipeline 与之解耦做 KV 量化与 paged 调度。论文给出在多代 GPU 上对比 vLLM/TRT-LLM 的吞吐与显存利用，强调跨架构泛化能力，是 LMDeploy 全栈混精度路线的官方系统级总结。",
    "推理",
)
add_paper(
    find("papers", "CascadeInfer"),
    "CascadeInfer 指出现有 LLM serving scheduler 忽略了 attention backend 对 batch 内请求长度异质性的敏感度——在 128k+ context 时代这从「可容忍」恶化为主要瓶颈。其方案：把多个同模型实例划分为不同长度档位，跨实例动态重调度请求，使每个实例内部长度更均匀，并据此选 attention 后端。报告显示长上下文下吞吐显著回升、尾延迟降低，是为长 context 时代重新设计 serving 调度面的思路。",
    "推理",
)
add_paper(
    find("papers", "GQLA"),
    "GQLA 针对 MLA 在非 H100 卡上的劣势：MLA 的训练权重只暴露 absorbed-MQA 一条解码路径，绑死 H100 算-带宽比、丧失 head 维 TP、在 H20 等出口型卡上拿不到 MTP 收益。GQLA 用同一套权重暴露两条代数等价的解码路径——absorb-MQA 路径与 per-group expand 的 GQA 路径，硬件适应性切换。这是把「压缩 KV 与硬件友好」两个目标解耦的精彩工程改造，对国产/受限 GPU 上部署 DeepSeek 系特别有意义。",
    "推理",
)
add_paper(
    find("papers", "DualKV"),
    "DualKV 是为 RL 后训练（GRPO/DAPO）量身定做的 FlashAttention 变体。它发现 N 条 rollout 共享同一 P-token prompt 时，标准 FlashAttention 在前后向都把 prompt 复制 N 次，prompt-only 的 norm/MLP/attention 全在重复算。DualKV 利用 decoder-only 因果掩码使 prompt 表示在所有序列每层不变这一性质，让 prompt 只算一次、share 给 N 条 rollout 的 attention kernel。在 N≥16、P≥8K 的大 rollout 长 context RL 训练中，这是 kernel-level 直接砍掉主要冗余。",
    "训练",
)
add_paper(
    find("papers", "Fluid-Guided Online Scheduling"),
    "WAIT（Waiting for Accumulated Inference Tokens）把 LLM serving 形式化为带内生内存增长的多阶段在线调度问题——生成 token 撑大 KV cache，溢出会驱逐进行中的请求并浪费已算量。作者用 fluid model 刻画稳态 batch 组成、内存需求与稳定区域，再据此设计调度器决定何时让请求进入 batch。给出工业部署成本背景下（700k$/day 量级）的理论保证与实测改善，是 KV 受限调度的偏理论侧贡献。",
    "推理",
)
add_paper(
    find("papers", "MoE-Prefill"),
    "MoE-Prefill 关注一类被忽视的 workload：分类/推荐/校验等只读 logits 的 prefill-only MoE 请求。现有 TP/EP/PP 范式继承自 decoding 时代——把 expert placement 与同步 activation routing 耦合，导致 prefill 上重复计算、通信和同步严重浪费。论文提出解耦方案，让 prefill 路径走零冗余执行，给出多 MoE 模型上的吞吐提升。这把 MoE 推理优化从 decode 单点扩展到 prefill 全场景，对生产判别式 workload 有直接价值。",
    "推理",
)
add_paper(
    find("papers", "Adaptive Speculative Training", "When RL Meets"),
    "这篇把 speculator 训练从离线孤立任务搬进线上 serving，提出统一训练-服务系统：speculator 与 target model 共享部署，端到端 decode 加速直接做反馈信号（而非只看 acceptance rate），随域迁移在线再训练抗 stale。系统层处理 time-to-serve、效用反馈延迟、domain drift 三类问题，是把 SGLang/vLLM 等推理栈与投机解码的训练侧合一的工程化探索。",
    "推理",
)
add_paper(
    find("papers", "BatchWeave"),
    "BatchWeave 把分布式大模型训练的 dataloader 重构成 object-store-native 数据面：用 versioned manifest + 条件对象写来协调 batch 发布、恢复与生命周期，并提出 Transactional Global Batch（TGB）抽象——它能表达批级语义（colocated dataloader 没有失败隔离、message-queue 类的 record/offset 抽象又表达不了批），同时具备故障隔离。是为 LFM 训练数据面提出的新存储抽象，直接对位 megatron 类训练的 ckpt/数据一致性痛点。",
    "训练",
)
add_paper(
    find("papers", "Runtime-Orchestrated Second-Order", "Asteria"),
    "Asteria 让二阶优化器（matrix-based preconditioner）首次具备实际可扩展性：把优化器状态在 GPU/CPU/NVMe 间动态分布，按架构约束与运行时压力调度；用 training hook 提前准备 shadow state，让 inverse-root 这种昂贵计算异步与训练前向重叠。把「二阶方法理论上更样本高效但系统代价不可承受」这一长期痛点，从系统侧而非数学侧解。对追求 sample efficiency 的大模型预训练有潜在意义。",
    "训练",
)

# ====== code ======
def add_code(it, tldr, tag):
    if it is None:
        return
    curated["code"].append(attach(it, tldr, tag))


add_code(
    find("code", "v0.2.1") if (find("code", "v0.2.1") and "xgrammar" in find("code", "v0.2.1")["link"].lower()) else None,
    "XGrammar v0.2.1 收一批结构化输出/工具调用相关 fix：Kimi auto tool calls 用 section markers 包装、暴露 normalize_tool_choice 并统一 Qwen XML 结构化标签构建器、JSON 输出停止把斜杠转义为 \\/、修复 RepetitionRangeExpander 的 segfault（错误的 grammar 对象查表）和 FSM 状态合并算法。这次没有大特性但贴近实际 agent runtime 上踩到的 grammar/tool-call 边角坑，对接 Kimi/Qwen 的 agent 部署值得跟进。",
    "agent",
)
# FlashInfer 取最新一条 nightly
fi = find("code", "Nightly Release v0.6.11-20260518")
add_code(
    fi,
    "FlashInfer 0.6.11 nightly 滚动构建：v0.6.11 仍处 dev 阶段，没有 release notes，但每日 nightly 持续推进——上一个 release（0.6.9/0.6.10 线）已带 Blackwell SM120 fused MoE 与 FP4 GEMM。关注 FlashInfer 的可以以这个 tag 监听 SGLang/vLLM 接入下一波 attention/MoE kernel 时机。",
    "推理",
)

# ====== community ======
def add_comm(it, tldr, tag):
    if it is None:
        return
    curated["community"].append(attach(it, tldr, tag))


add_comm(
    find("community", "Qwen 3.6 27B on 24GB VRAM setup"),
    "RTX 3090 24GB 上 Qwen3.6-27B 三种后端实测：ik_llama.cpp + Qwen3.6-27B-MTP-IQ4_KS.gguf 156k context、q8/q8 KV、MTP 开启、vision on CPU，5.9k prompt+1k output 跑出 1261 tok/s prefill、72.9 tok/s decode，是消费卡 24GB 当下最佳组合。llama.cpp 作 baseline 可用，BeeLlama 论文好看实测复现失败，vLLM 在 club-3090 路径上高 context OOM 不稳。是单卡本地部署 27B-class MoE 的实操参考。",
    "推理",
)
add_comm(
    find("community", "Qwen 3.6 27B Q8 on four"),
    "另一组实测：4×RTX A4000 16GB（每卡 140W 限到 125W）跑 Qwen3.6-27B Q8，llama.cpp + MTP `--spec-draft-n-max 4` 配置最佳。要点是低功耗老卡靠多卡显存堆叠 + MTP 投机解码也能稳定跑 27B Q8，单 PCIe slot 单卡的 ThinkStation 拓扑也能撑住。给「老卡 + 大模型」路线提供成本/性能参照。",
    "推理",
)
add_comm(
    find("community", "Quantizing MTP KV Cache"),
    "llama.cpp MTP 实现里 MTP 层有自己的 draft KV cache，可独立量化（`-cache-type-k-draft q8_0 -cache-type-v-draft q8_0`）。Qwen3.6-27B-Q8 短测 9 请求：accept rate 维持 0.735（与 fp draft KV 完全一致），墙钟略快——量化 draft KV 在保持验证质量的前提下省显存近似免费。MTP 投机解码工程实现细节，对扩 context 直接有用。",
    "推理",
)
add_comm(
    find("community", "M5 vs DGX Spark"),
    "硬件 benchmark：M5 Mac vs DGX Spark vs Strix Halo vs RTX 6000 在标准化测试下并列跑 3 天，结论与内存带宽紧密对应——RTX 6000 ~1800 GB/s vs M5 ~600 vs Spark/Strix ~256，tokens/s 几乎按这个比例线性。意外亮点是顶配 M5 在性价比上明显超过 DGX Spark，对生态无强约束的本地推理是务实选项。原帖给出可复现 repo。",
    "推理",
)
add_comm(
    find("community", "I built a coding agent that gets 87"),
    "SmallCode 是面向小本地模型（4B 量级 Gemma/Qwen）的 coding agent harness：原始 OpenCode/Cursor/Claude Code 都假设接 GPT-5.4/Opus，4B 模型 tool call 易失败、长上下文崩。SmallCode 的设计取舍——compound tools 把「找文件→读→编辑→校验」压成单 tool 调用避免多步崩，最终 4B Gemma 跑出 87/100，超过 14B 的 OpenCode（~75）。把「agent 能力来自 harness 而非模型规模」这一论点用工程数据兜住，coding-agent 系统设计参考。",
    "agent",
)


# 写出
generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
out = {
    "generated_at": generated_at,
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": curated,
    "fetch_stats": raw.get("fetch_stats", {}),
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# 简单核对输出
total = sum(len(v) for v in curated.values())
counts = {k: len(v) for k, v in curated.items()}
tags = {}
for sec in curated.values():
    for it in sec:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"curated total={total} sections={counts} domain_tag={tags}")
print(f"generated_at={generated_at} raw_generated_at={raw['generated_at']}")
