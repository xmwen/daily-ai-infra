# -*- coding: utf-8 -*-
"""一次性脚本：手写中文 curated。中文双引号用「」避免转义坑。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "cache" / "today_raw.json"
OUT_PATH = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))


def find(section, key_in_title):
    for it in raw["sections"][section]:
        if key_in_title in it["title"]:
            return it
    return None


def find_by_link(section, key_in_link):
    for it in raw["sections"][section]:
        if key_in_link in it["link"]:
            return it
    return None


curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {
        "papers": [],
        "code": [],
        "blogs": [],
        "community": [],
    },
    "fetch_stats": raw.get("fetch_stats", {}),
}


def add(section, item, tldr, domain_tag):
    if item is None:
        return
    new_item = dict(item)
    new_item["tldr"] = tldr
    new_item["domain_tag"] = domain_tag
    curated["sections"][section].append(new_item)


# ============ code ============
add(
    "code",
    find("code", "v0.6.12rc1"),
    "FlashInfer v0.6.12rc1：补齐 Kimi K2.5 H64 CuTe DSL MLA decode 路径、CUTLASS MLA paged attention 加 FP8 输出、SM120 上 b12x W4A16 MoE kernel、TRTLLM-GEN GQA 动态 tokens-per-page，并放宽 trtllm_ragged_attention_deepseek 的 shape 断言。一条覆盖 K2.5 / DeepSeek / SM120 三栈持续推进。",
    "推理",
)
add(
    "code",
    find("code", "langgraph-checkpoint==4.1.1"),
    "LangGraph 同日发 checkpoint 4.1.1 + sdk 0.3.15 + langgraph 1.2.1：checkpoint 把 lc:2 envelope revival 限制为默认构造器，避免反序列化时被任意构造器执行；sdk 给 caller-supplied identifier 在 URL 路径里强制 percent-encode 防注入。延续本月 agent SDK「补漏期」节奏，安全边界从 sandbox 推到反序列化与 URL 解析层。",
    "agent",
)
add(
    "code",
    find("code", "Mooncake") or find("code", "v0.3.11.post1"),
    "Mooncake v0.3.11.post1：基于 mlx5dv 暴露的 QP path diversity，用 UDP sport 哈希 + LAG port balance 做 RDMA 多路径，对 KV cache 跨节点 fetch 的尾延迟与突发瓶颈直接受益；TENT 加 QoS 与 slice spraying，npu 发布流水线接入。Mooncake 的 KV pool 仍是 SGLang/vLLM PD 分离的主流落地选项之一。",
    "推理",
)

# ============ community ============
# 合并 Qwen3.6-35B-A3B 8GB 与 Qwen3.6-27B 16GB 两条到 1 条 MoE 边缘部署配方
qwen_35b = find_by_link("community", "qwen3635ba3b_q4_262k_context_on_8gb")
qwen_27b = find_by_link("community", "qwen36_27b_pure_quant")
# 取后者主条目（信号更聚焦），把前者作为补充写进 tldr
if qwen_27b is not None:
    add(
        "community",
        qwen_27b,
        "Qwen3.6-27B Q4_K_M pure 量化在 RTX 5060 Ti 16GB 单卡跑出 40 tok/s（MTP/non-MTP 双版 GGUF），关键配方是 ctk/ctv q5_0 + --no-mmap --mlock + preserve_thinking；同日 r/LocalLLaMA 还有一例 Qwen3.6-35B-A3B Q4 在 8GB 3070 Ti 跑 30+ tok/s @ 262K（active 3.5B MoE 块进 VRAM + KV 池压 DDR4 4 通道，实测可顶到 1M）。两条共同坐实「MoE active expert 留 GPU + KV 量化下沉」是消费级长 ctx 的稳定范式。",
        "推理",
    )
add(
    "community",
    find_by_link("community", "beellama_v020"),
    "BeeLlama v0.2.0：投机解码引擎单卡 RTX 3090 实测 Qwen3.6-27B 164 tok/s（4.40×）/ Gemma 4 31B 177.8 tok/s（4.93×），prefill 接近 baseline。本次重点：drafter K/V projection 缓存、reduced verifier path 严格化（grammar/sampler/reasoning 触发安全 fallback 到 full logits）、draft/target 校验与 draft-model 自动发现，DFlash GGUF 上游架构兼容。把投机解码工程化的「draft KV 复用 + 触发条件回退」做到位。",
    "推理",
)

OUT_PATH.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT_PATH}")
print(
    f"counts: papers={len(curated['sections']['papers'])} code={len(curated['sections']['code'])} blogs={len(curated['sections']['blogs'])} community={len(curated['sections']['community'])}"
)
tags = {}
for sec in curated["sections"].values():
    for it in sec:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"domain_tag: {tags}")
