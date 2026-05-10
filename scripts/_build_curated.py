"""一次性脚本：从 today_raw.json 生成 today_curated.json
- 中文 tldr（≤200 字）
- domain_tag ∈ {推理, 训练, agent}
- generated_at 用当前 UTC ISO
"""
import json
from datetime import datetime, timezone
from pathlib import Path

RAW = Path("cache/today_raw.json")
OUT = Path("cache/today_curated.json")

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section, predicate):
    for it in raw["sections"].get(section, []):
        if predicate(it):
            return it
    return None


def pick(section, title_sub):
    for it in raw["sections"].get(section, []):
        if title_sub.lower() in it["title"].lower():
            return it
    return None


curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "source": "manual_curated",
    "sections": {
        "papers": [],
        "code": [],
        "blogs": [],
        "community": [],
    },
}

# ---------- code ----------
code_items = []

it = pick("code", "v0.20.2")
if it:
    c = dict(it)
    c["tldr"] = (
        "vLLM v0.20.2 小步 patch 6 commits：核心两条针对 DeepSeek V4——重新启用 Hopper 上的 persistent "
        "topk 路径并把 memset kernel 强制在 CUDA graph capture 时运行（与 max_seq_len 无关），修复 MTP=1 "
        "时的死锁（#41665 revert 掉前版 #41605）；同时修掉 V1 engine KV cache manager 的块分配失败。"
        "另外 gpt-oss MXFP4 在 torch.compile 下通过 hidden_dim_unpadded plumbing 修好、"
        "Qwen3-VL 移除重载下会误触发的 deepstack 边界检查。属于本月"
        "「feature 落地即 revert」节奏的又一次收敛版本。"
    )
    c["domain_tag"] = "推理"
    code_items.append(c)

# FlashInfer v0.6.11rc1 正式 rc（合并两条 nightly 到这一条）
it = pick("code", "v0.6.11rc1")
if it:
    c = dict(it)
    c["tldr"] = (
        "FlashInfer v0.6.11rc1 正式 release candidate，延续 v0.6.10→v0.6.11 节奏；rc 本体 "
        "changelog 页还未定稿，但对应 nightly-20260509/20260510 已出，工程上对 trtllm FMHA "
        "head_dim=512、MXFP4×BF16 MoE SM90、DCP A2A 等 v0.6.10 新增路径做稳定化收敛。"
        "供下游 vLLM/SGLang/TensorRT-LLM 在 v0.6.11 正式版前锁定依赖。"
    )
    c["domain_tag"] = "推理"
    code_items.append(c)

curated["sections"]["code"] = code_items

# ---------- community ----------
community_items = []

it = pick("community", "star elastic")
if it:
    c = dict(it)
    c["tldr"] = (
        "NVIDIA Star Elastic：单一 checkpoint 同时包含 30B / 23B / 12B 三档推理模型，zero-shot slicing "
        "切层即降档。类比 scalable video coding——一个 stream 里剥层就变 HD/SD。三档共享 KV cache，"
        "推理时可在 12B 以 7000 tok/s 高速展开大量思维分支，再切回 30B 做评估；"
        "对多模型级联 / 投机解码 / draft-target 场景是天然的 serving 侧 elastic 机制，"
        "推理基础设施可直接利用同一权重池做动态质量-吞吐权衡。"
    )
    c["domain_tag"] = "推理"
    community_items.append(c)

it = pick("community", "80 tok/sec and 128k")
if it:
    c = dict(it)
    c["tldr"] = (
        "Qwen3.6 35B-A3B + llama.cpp MTP PR 在 12GB VRAM（RTX 4070 Super）单卡跑 128K 上下文 "
        "实测 80+ tok/s、draft 接受率 80%+。MoE + MTP 推测解码配方在 12GB 档首次稳定达标。"
        "关键路径：llama.cpp 源码编译 + 未合入 master 的 MTP draft PR；把 MoE 块保在 GPU 常驻、"
        "KV 量化 + 小 draft 配合 MTP 一次性消费多 token。用户 MTP/投机解码方向在消费卡上的"
        "最新参考配置。"
    )
    c["domain_tag"] = "推理"
    community_items.append(c)

it = pick("community", "nccl-free tensor parallelism")
if it:
    c = dict(it)
    c["tldr"] = (
        "llama.cpp b9095 让 `-sm tensor`（tensor parallelism）在双 Blackwell PCIe 消费卡上"
        "绕开 NCCL 直接工作。过去双 GPU TP 要么依赖 NCCL、要么 pipeline-parallel 串行；"
        "b9095 走 llama.cpp 自己的 CUDA IPC + point-to-point 通信，消费级 Blackwell "
        "（5060Ti/5070Ti/5080/5090）配对即可启用 TP，避免 NCCL 在消费驱动上的各种坑。"
        "对国产芯片做 P2P + CPU-host-staging 无 NCCL 方案是直接可参考的工程模板。"
    )
    c["domain_tag"] = "推理"
    community_items.append(c)

it = pick("community", "deepseek v4 pro at home")
if it:
    c = dict(it)
    c["tldr"] = (
        "Epyc 9374F + 12×96GB DDR5 + 单卡 RTX PRO 6000 Max-Q（97GB VRAM）用 antirez ds4 "
        "/ LegacyRemaster Q4_K_M 分支把 DeepSeek V4-Pro Q4_K_M 跑起来——MoE + CSA 稀疏索引 "
        "全路径在 llama.cpp CUDA fork 上首个报告的「单卡家用 V4-Pro」案例。模型权重近 "
        "400GB 靠 CPU RAM offload + 单 GPU KV+active-expert，与昨天 MacMetal + DGX 的 "
        "V4-Flash 路线平行，验证 V4 KV cache 7-10% baseline 的压缩效果在消费路线也扩展良好。"
    )
    c["domain_tag"] = "推理"
    community_items.append(c)

it = pick("community", "minimax 2.7 at 100k")
if it:
    c = dict(it)
    c["tldr"] = (
        "Strix Halo（AMD 统一内存）上 llama.cpp 跑 MiniMax M2.7 UD-IQ3_XXS @ 100k 上下文"
        "的 serving 参数调优总结：`--kv-unified` 让多会话共享 KV、`--cache-ram 0` 禁止 KV 换出到"
        "系统 RAM（解决 OOM）、`--no-mmap --no-context-shift` 防 silently 截断、"
        "`-b 1024 -ub 1024` 优化 prefill、`--cache-reuse 256` 智能重用。"
        "是 AMD Strix Halo 统一内存 fabric 做长上下文 MoE serving 的最新实战基线，"
        "对国产 ScaleUp 统一内存推理路线参数调优可直接借鉴。"
    )
    c["domain_tag"] = "推理"
    community_items.append(c)

it = pick("community", "ds4")
# 注意：帖子标题 "DS4"——用完整匹配
it = None
for x in raw["sections"]["community"]:
    if x["title"].strip() == "DS4":
        it = x
        break
if it:
    c = dict(it)
    c["tldr"] = (
        "Redis 作者 Salvatore Sanfilippo 开源新项目 DS4（github.com/antirez/ds4/），把 "
        "DeepSeek V4-Flash 1M 上下文在 Mac Metal 跑起来，同时在 DGX 上也验证运行。"
        "server 原生暴露 OpenAI + Anthropic 兼容端点可直接对接 agentic 编码工具链（Claude Code / Codex 等）。"
        "是 DeepSeek V4-Flash 的 Metal 端首个独立实现，与 KTransformers v0.6.2 NVIDIA 路线、"
        "lmsys SGLang Day0 路线形成 V4 推理的三栈分支，工程上验证 V4 CSA indexer + MoE "
        "在 unified memory 架构上的可移植性。"
    )
    c["domain_tag"] = "推理"
    community_items.append(c)

curated["sections"]["community"] = community_items

# ---------- 写入 ----------
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
from collections import Counter
total = sum(len(v) for v in curated["sections"].values())
tags = Counter()
for sec in curated["sections"].values():
    for it in sec:
        tags[it["domain_tag"]] += 1
print(f"curated total: {total}")
for k, v in curated["sections"].items():
    print(f"  {k}: {len(v)}")
print(f"domain_tag: {dict(tags)}")
print(f"generated_at: {curated['generated_at']}")
print(f"raw generated_at: {raw['generated_at']}")
