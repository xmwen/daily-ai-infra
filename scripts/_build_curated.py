# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成 today_curated.json。
中文 tldr 用「」避开双引号字符串闭合坑。
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 用 link 索引 raw item，方便注入 tldr / domain_tag
def find(section, link):
    for it in raw["sections"].get(section, []):
        if it["link"] == link:
            return it
    return None

# ---------- 手写中文 tldr ----------
# 每条：(section, link, domain_tag, tldr)
picks = [
    # ============ papers (推理) ============
    (
        "papers",
        "https://arxiv.org/abs/2604.09603",
        "推理",
        "ECHO v2 replace 持续刷：把投机解码当成 budgeted scheduling 问题塞进 SGLang，sparse confidence gating 把 batch 当统一 super-tree 弹性管理，针对高并发下「verification 计算才是瓶颈」这一被忽略事实，避开 static tree 验证浪费与 dynamic tree 误判累积；定位为 SGLang 集成式投机解码预算控制器，是本周 SGLang 侧最强推理 release 候选。",
    ),
    (
        "papers",
        "https://arxiv.org/abs/2605.13319",
        "推理",
        "PipeSD v2 replace 接力：云边协同推理框架，把投机解码与 token-batch pipeline 调度耦合，重叠 token 生成与通信解决既有顺序生成低利用率问题；自适应触发云端 NAV（non-autoregressive verification）避免过早 verify 或回滚开销，针对端侧+云端 hybrid SD 部署补齐控制面。",
    ),
    (
        "papers",
        "https://arxiv.org/abs/2511.16964",
        "agent",
        "Optimizing PyTorch Inference w/ Multi-Agent v2 replace：用 LLM 多 agent 系统替代手写 GPU kernel 与专用编译器调优。逻辑框架对比显示 exploit-heavy 策略配合 error-fixing agent 表现最佳，性能与 agent 类型组合强相关；定位为 FACT/KernelBenchX 之后 agent 写 kernel 范式的系统化对比，给「coding agent 接管 infra 工程」提供方法论依据。",
    ),
    (
        "papers",
        "https://arxiv.org/abs/2604.25899",
        "agent",
        "Pythia v2 replace：agent-native LLM serving 利用 multi-agent 结构化拓扑的语义可预测性。基于一线 agent-serving 平台 + 内部 coding assistant 生产 trace 分析，识别现有 serving 系统把 agent 流量当通用 traffic 导致的 prefix cache 命中率低、调度低效等瓶颈，针对结构化 workflow 重新设计调度。",
    ),
    # ============ code (推理) ============
    (
        "code",
        "https://github.com/vllm-project/vllm/releases/tag/v0.21.0",
        "推理",
        "vLLM v0.21.0 正式版（367 commits / 202 contributors / 49 新人）：① 正式 deprecate transformers v4 强制迁 v5；② 编译升 C++20 要求（与 PyTorch 对齐，破坏式 build change）；③ KV Offload 与 Hybrid Memory Allocator 完整融合（含 scheduler 端 sliding-window group + 完整 HMA enable）；④ 投机解码尊重 reasoning/thinking budget，reasoning 模型 spec decode 正确性补齐；⑤ Blackwell TOKENSPEED_MLA backend；本月「feature 落地即 revert」节奏后第一个完整收敛正式版。",
    ),
    (
        "code",
        "https://github.com/vllm-project/vllm/releases/tag/v0.21.1rc0",
        "推理",
        "vLLM v0.21.1rc0：紧随正式版的 ROCm CI Stage B gating 补丁，AMD 路径独立质量门保护，避免 v0.21.0 RTM 之后第一波 ROCm 侧回归。",
    ),
    (
        "code",
        "https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11.post3",
        "推理",
        "FlashInfer v0.6.11.post3：post 系列继续滚动，trtllm FMHA head_dim=512 + MXFP4×BF16 MoE SM90 + DCP All-to-All 主线在 v0.6.11 后持续稳定化，对 NVFP4/MXFP4 主线推理栈持续兜底；当日同时刷出两份 nightly。",
    ),
    # ============ community ============
    (
        "community",
        "https://www.reddit.com/r/LocalLLaMA/comments/1teryn8/llama_spec_mtp_support_by_am17an_pull_request/",
        "推理",
        "llama.cpp MTP 正式合并主线（PR #22673 by am17an）：Multi-Token Prediction 投机解码框架终于在 llama.cpp master 落地，配套 GGUF 释出 Qwen3.6-27B-MTP 与 Qwen3.6-35B-A3B-MTP；意味着消费级单机推理 MTP 进入 stable 渠道，自 5/4 周起持续追踪的「MTP 工程化下沉到 llama.cpp」事件链至此收口。",
    ),
    (
        "community",
        "https://www.reddit.com/r/LocalLLaMA/comments/1te5xpu/orthrusqwen38b_up_to_78tokensforward_on_qwen38b/",
        "推理",
        "Orthrus-Qwen3 系列（1.7B/4B/8B）：在冻结 AR Transformer 每层注入可训练 diffusion attention 模块，两路 head 共享一份 KV cache——diffusion head 一次并行投影 K=32 tokens，AR head 第二 pass 验证取最长匹配前缀，输出分布与 base 完全等价（无损）；MATH-500 上达 7.8× TPF / 约 6× wall-clock，仅训 16% 参数 <1B tokens 24h on 8×H200。相比 Fast-dLLM-v2 等改 base 权重掉精度、相比 EAGLE-3/DFlash 不需外部 drafter，提供新一类「base 模型内嵌 drafter」可证明等价投机解码范式。",
    ),
    (
        "community",
        "https://www.reddit.com/r/LocalLLaMA/comments/1tee5ms/can_a_5090_with_qwen36_achieve_3000_toks_bring/",
        "推理",
        "Open-dLLM × Qwen3.6 5090 探路（仅理论，未实测）：把 Qwen3.6 改造成 diffusion LM 跑 5090，目标 3000+ tok/s——基于 6 个月前 Open-dLLM（已跑 Qwen2.5）框架，混入 LDLM（arxiv 2605.07933）方法，用 opencode + deepseek-flash/GLM5.1 隔夜 agent 自动改 codebase。意义不在数字而是「AR→diffusion LM」改造成本被 coding agent 拉到隔夜级，与本周 Optimizing PyTorch Multi-Agent 形成「agent 写 infra」证据链。",
    ),
    (
        "community",
        "https://www.reddit.com/r/LocalLLaMA/comments/1teqjjl/reduce_your_gpu_power_limit/",
        "推理",
        "RTX 游戏卡 power limit 实测：消费级 GPU（Qwen3.5-9B 测试集）大幅下调 power limit 对 prefill/decode 吞吐影响极小；显存超频 700-1000MHz 可小幅提升 tg。再次实测印证 5/13 arXiv「Power Capping Illusion」paper——decode memory-bound 下功耗 cap 永远触不到 TDP，砍功率几乎免费换续航/温控；本周「power-limit 砍半性能不变」第三起独立社区验证。",
    ),
]

# ---------- 构造 curated ----------
out_sections = {"papers": [], "code": [], "blogs": [], "community": []}
seen_links = set()
for section, link, tag, tldr in picks:
    if link in seen_links:
        continue
    seen_links.add(link)
    src = find(section, link)
    if src is None:
        print(f"WARN: {link} not found in raw[{section}], skip")
        continue
    item = dict(src)  # 保留所有原始字段
    item["tldr"] = tldr
    item["domain_tag"] = tag
    out_sections[section].append(item)

result = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "source": "today_curated.json",
    "sections": out_sections,
    "fetch_stats": raw.get("fetch_stats", {}),
}

OUT.write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
total = sum(len(v) for v in out_sections.values())
tag_dist = {"推理": 0, "训练": 0, "agent": 0}
for sec in out_sections.values():
    for it in sec:
        tag_dist[it["domain_tag"]] = tag_dist.get(it["domain_tag"], 0) + 1
print(f"curated total: {total}")
print(f"  papers={len(out_sections['papers'])} code={len(out_sections['code'])} blogs={len(out_sections['blogs'])} community={len(out_sections['community'])}")
print(f"  domain_tag: 推理={tag_dist['推理']} 训练={tag_dist['训练']} agent={tag_dist['agent']}")
print(f"  generated_at: {result['generated_at']}")
print(f"  raw    generated_at: {raw['generated_at']}")
print(f"Saved: {OUT}")
