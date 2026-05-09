# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成 today_curated.json（中文 tldr + domain_tag）"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def by_link(section, link):
    for it in raw["sections"].get(section, []):
        if it["link"] == link:
            return dict(it)
    raise KeyError(f"{section}:{link} not found in raw")


def add(items, section, link, tldr, domain_tag):
    item = by_link(section, link)
    item["tldr"] = tldr
    item["domain_tag"] = domain_tag
    items.append(item)


curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {"papers": [], "code": [], "blogs": [], "community": []},
    "fetch_stats": raw["fetch_stats"],
}

# === papers（周六 arXiv 不更新，0 条是客观事实） ===

# === code ===
add(
    curated["sections"]["code"],
    "code",
    "https://github.com/kvcache-ai/ktransformers/releases/tag/v0.6.2.post2",
    "KTransformers v0.6.2.post2 把 V4-Flash 启动样例从 8×RTX 5090 切到「单卡 decode 20+ tok/s」，并把 Ada Lovelace SM_89 行升为 validated；底层 sglang 子模块升到 0.6.2.post2，修了 V4-Flash hybrid SWA chunked-prefill hang 与 DSV4 plugin registry refactor。意义：DSV4-Flash 从「8 卡集群」下放到「单消费级 GPU 可跑」是 MoE+SWA 推理工程的拐点信号。",
    "推理",
)
add(
    curated["sections"]["code"],
    "code",
    "https://github.com/openai/openai-agents-python/releases/tag/v0.17.0",
    "OpenAI Agents v0.17.0：RealtimeAgent 默认切到 gpt-realtime-2；sandbox 局部源物化加固——LocalFile.src/LocalDir.src 默认必须落在 materialization base_dir（即 SDK 进程 CWD）内，绝对路径必须已在 base_dir 下或被 Manifest.extra_path_grants 显式授权，关闭了 agent host 文件越界拷贝路径。延续此前 sandbox boundary 收紧节奏。",
    "agent",
)
add(
    curated["sections"]["code"],
    "code",
    "https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.27.1",
    "MCP Python SDK v1.27.1：兼容 pydantic 2.13（catch PydanticUserError 生成 output schema 时）、OAuthClientMetadata 把空字符串可选 URL 字段强制 coerce 成 None、httpx 锁到 <1.0.0、SSEError 改从 httpx_sse 公共 API 导入。纯依赖与 OAuth 鲁棒性 bugfix，跟着上游升 pydantic 必带。",
    "agent",
)
add(
    curated["sections"]["code"],
    "code",
    "https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11rc1",
    "FlashInfer v0.6.11rc1 候选发布（含 nightly 20260508/20260509 同源 cut）。具体 commit list 仅指向 v0.6.11 区间，无独立 changelog；接续 v0.6.10 的 trtllm head_dim=512 + MXFP4×BF16 SM90 + DCP A2A 主线，rc1 阶段重点观察 Blackwell SM_120 与 hd512 路径稳定性。",
    "推理",
)

# === blogs ===
add(
    curated["sections"]["blogs"],
    "blogs",
    "https://developer.nvidia.com/blog/improving-bash-generation-in-small-language-models-with-grammar-constrained-decoding/",
    "NVIDIA 官方博客：用 Grammar-Constrained Decoding 改 SLM 生成 Bash 的合法率。把 grep/curl/tar/管道等 shell 算子建模为 CFG，在解码每步用 grammar 掩码非法 token，让小模型直接产出可执行 shell 而不是「看似对、实际语法错」的字符串。命中 agent 系统的 tool use 底层（XGrammar/Outlines/lm-format-enforcer 路线），是 NV 首个把 constrained decoding 推到 coding agent shell 工具调用的官方背书。",
    "agent",
)

# === community ===
add(
    curated["sections"]["community"],
    "community",
    "https://www.reddit.com/r/MachineLearning/comments/1t7yrvr/deepseek_v4_paper_full_version_is_out_fp4_qat/",
    "DeepSeek V4 完整论文释出（4 月预览 58 页，全本加大量训练 infra 细节）。要点：FP4 QAT 直接进入训练后期，MoE 专家权重量化到 FP4，CSA indexer 的 QK 路径用 FP4 激活，QK selector 实现 2× 加速 + 99.7% recall；推理直接吃 FP4 权重。1M 上下文效率：V4-Pro FLOPs 27%、KV cache 10% of V3.2 baseline；V4-Flash FLOPs 10%、KV cache 7%。训练稳定性两板斧：anticipatory routing 与 loss spike 显式诱发-恢复机制，专治 trillion-param MoE 不可预测发散。",
    "训练",
)
add(
    curated["sections"]["community"],
    "community",
    "https://www.reddit.com/r/LocalLLaMA/comments/1t7kyju/got_mtp_turboquant_running_qwen3627b_80_ts_at/",
    "民间工程：把 MTP 和 TurboQuant 的 TBQ4_0（4.25 bpv 无损 KV cache）同时栓在 Qwen3.6-27B 上，单卡 RTX 4090 24GB 跑出 80–87 tok/s @ 262K 上下文，MTP 接受率 ≈73%。栈：Q4_K_M 权重 + grafted MTP heads + TBQ4_0 KV + draft 3 + CUDA 12.x。直接验证 vLLM 主线刚合的 TurboQuant per-vector min-max 4-bit KV 在 hybrid Mamba+Attn 风格 MoE 上的工程可用性。",
    "推理",
)
add(
    curated["sections"]["community"],
    "community",
    "https://www.reddit.com/r/LocalLLaMA/comments/1t82zxv/80_toksec_and_128k_context_on_12gb_vram_with/",
    "Qwen3.6 35B-A3B + llama.cpp MTP PR 在 RTX 4070 Super 12GB 跑出 80 tok/s + 128K 上下文 + 80%+ MTP 接受率；同期另一组在 RTX 3060 12GB 上靠 -ncmoe 18 / ctk q8_0 / ctv q8_0 拿到 pp512 ≈914 tok/s + tg128 ≈46.8 tok/s。说明 MoE 推理 12GB 档「保 MoE 块在 GPU + KV 量化」的两条腿在主线 llama.cpp 已基本成熟，是 35B 级 MoE 在消费卡落地的清晰配方。",
    "推理",
)
add(
    curated["sections"]["community"],
    "community",
    "https://www.reddit.com/r/LocalLLaMA/comments/1t7g70j/vllm_rocm_has_been_added_to_lemonade_as_an/",
    "AMD/Lemonade 把 vLLM ROCm 实验性后端塞进 lemonade backends（lemonade backends install vllm:rocm 一行装好，run Qwen3.5-0.8B-vLLM 即起服务）。意义：safetensors 直跑不再强制转 GGUF，AMD 推理栈在 ROCm 侧首次有了与 llama.cpp 对位的 vLLM 一键体验。",
    "推理",
)

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  papers: {len(curated['sections']['papers'])}")
print(f"  code:   {len(curated['sections']['code'])}")
print(f"  blogs:  {len(curated['sections']['blogs'])}")
print(f"  community: {len(curated['sections']['community'])}")
total = sum(len(v) for v in curated["sections"].values())
print(f"  total:  {total}")
tags = {}
for sec in curated["sections"].values():
    for it in sec:
        tags[it["domain_tag"]] = tags.get(it["domain_tag"], 0) + 1
print(f"  domain_tag: {tags}")
print(f"  generated_at: {curated['generated_at']}")
print(f"  raw generated_at: {raw['generated_at']}")
