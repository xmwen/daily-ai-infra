# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成 today_curated.json
2026-05-17（周日跑）：低信号日。raw 13 条（papers 0 / code 3 / blogs 0 / community 10）。
  - papers 0 是周日 arXiv 不更新的客观底
  - blogs 全 0 + HN 双 0 同样客观
  - code 仅 SGLang v0.5.12（DSV4 Day-0 重磅）+ FlashInfer 两条无 changelog nightly（弃）
  - community 主线是 llama.cpp MTP merge 后的多平台实测——5090/3090/3090Ti/6GB 笔记本四点完整覆盖
"""
import json
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 用 link 索引 raw 条目，便于挑选
raw_index = {}
for sec, items in raw["sections"].items():
    for it in items:
        raw_index[it["link"]] = (sec, it)

picks = []

def add(link, tldr, domain_tag):
    sec, it = raw_index[link]
    new = dict(it)
    new["tldr"] = tldr
    new["domain_tag"] = domain_tag
    picks.append((sec, new))

# ===== code =====
add(
    "https://github.com/sgl-project/sglang/releases/tag/v0.5.12",
    "SGLang v0.5.12 重磅释出 DeepSeek V4 完整推理路径——TP/EP/CP/DP attention 全 parallelism 覆盖、B300/B200/H200/H100/GB200/GB300 与 AMD MI35X 全栈、PD 分离、HiSparse 把不活跃 KV 卸载到 CPU、DeepGEMM+FlashMLA+MegaMoE kernel；Day-0 后又补齐 V4 在 UnifiedTree 下的 HiCache、W4A4 MegaMoE kernel（无损精度）、Hopper 上 Marlin/FlashInfer W4A8 MoE、V2 fused 压缩 kernel、H100/H20 TP16 与 fused SiLU+clamp+FP8 量化 kernel——继 KTransformers/DS4/LMDeploy 之后第四个 V4 系列推理引擎完整工程化落地",
    "推理",
)

# ===== community =====
# 五条 MTP 主题：四条多平台实测 + 一条 merge 公告（合并三条祝贺贴）
add(
    "https://www.reddit.com/r/LocalLLaMA/comments/1tes1wx/mtp_support_merged_into_llamacpp/",
    "llama.cpp PR #22673 MTP 支持正式合并进 master——继 KTransformers 5/4 首发、Qwen3.6-MTP/Qwen3.6-A3B-MTP GGUF 释出、5/11-13 系统 benchmark 出「文本熵决定加速比」之后，MTP 工程化下沉至 llama.cpp 主线（同主题 Pjotrs/Valuable_Touch5670 两条祝贺贴合并）；MTP 至此对消费级单卡用户完整开放",
    "推理",
)
add(
    "https://www.reddit.com/r/LocalLLaMA/comments/1tfgxc8/testing_llamacpp_mtp_support_on_qwen36_rtx_5090/",
    "RTX 5090 32GB 跑 llama.cpp 4f13cb7 + Unsloth Qwen3.6-27B-MTP-Q5_K_M 与 35B-A3B-MTP-UD-Q4_K_M——同 GGUF 切换 --spec-type draft-mtp --spec-draft-n-max 3 隔离量化变量，128k 上下文 + flash-attn + q8_0 KV，3 seed 平均；首发 Blackwell 单卡 MTP 实测基线，构建 docker 需 CUDA_DOCKER_ARCH=120（官方 cuda 镜像未跟上 merge）",
    "推理",
)
add(
    "https://www.reddit.com/r/LocalLLaMA/comments/1tfilwx/llamacpp_mtp_with_qwen36_27b_on_headless_rtx_3090/",
    "Headless RTX 3090 24G + Qwen3.6-27B-MTP-Q4_K_M + 128k ctx + q8_0 KV + draft-n-max=3：MTP off PP 1050/TG 27 → MTP on PP 600 (-42%)/TG 50 (+85%)，85k token 任务 39 分钟降到 23 分钟（1.7×）；PP 退化但 TG 大幅提升的真实工况数据，OpenCode 之类 PP 偏重场景需谨慎",
    "推理",
)
add(
    "https://www.reddit.com/r/LocalLLaMA/comments/1tfpicu/qwen3627b_mtp_depth_benchmark_rtx_3090ti/",
    "RTX 3090Ti + Qwen3.6-27B-UD-Q4_K_XL MTP 深度扫描——No MTP 41.1 t/s → MTP1 52.5 (1.28×, 接受率 95.5%) → MTP2 73.5 (1.79×, 91.3%) 但 PP 从 175.9 降到 105.0；首份 llama.cpp MTP n_max 深度 vs 接受率 vs PP 退化的系统对照，给消费卡选 depth 提供决策面",
    "推理",
)
add(
    "https://www.reddit.com/r/LocalLLaMA/comments/1tfq683/mtp_for_qwen3635ba3b_on_6gb_vram_laptop_not_worth/",
    "RTX 3060 Laptop 6GB VRAM 跑 Qwen3.6-35B-A3B MTP 实测：PP 退化太重抵消 TG 收益，6GB 档不值得开 MTP；副产物——draft KV 用 q4_0 与 q8_0 等效但省一点 VRAM。证明 MTP 收益对 VRAM 充裕度敏感，与 5/11 「文本熵决定加速比」结论叠加给出第二维度（硬件档位）决策依据",
    "推理",
)

# 写出 curated
out = {
    "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours"),
    "sections": {"papers": [], "code": [], "blogs": [], "community": []},
    "fetch_stats": raw.get("fetch_stats", {}),
}
for sec, item in picks:
    out["sections"][sec].append(item)

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

# 统计
counts = {k: len(v) for k, v in out["sections"].items()}
tags = {"推理": 0, "训练": 0, "agent": 0}
for sec_items in out["sections"].values():
    for it in sec_items:
        tags[it["domain_tag"]] += 1
print("curated counts:", counts, "total:", sum(counts.values()))
print("domain_tag:", tags)
print("generated_at:", out["generated_at"])
print("raw generated_at:", raw["generated_at"])
