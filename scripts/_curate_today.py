"""一次性脚本：基于 today_raw.json 生成 today_curated.json（中文 tldr + domain_tag）。"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def find(section: str, predicate) -> dict:
    for it in raw["sections"].get(section, []):
        if predicate(it):
            return it
    raise SystemExit(f"item not found in section={section}")


def enrich(item: dict, tldr: str, domain_tag: str) -> dict:
    out = dict(item)
    out["tldr"] = tldr
    out["domain_tag"] = domain_tag
    return out


curated_sections = {
    "papers": [],
    "code": [],
    "blogs": [],
    "community": [],
}

# ---- code ----
flashinfer_nightly = find(
    "code",
    lambda it: it.get("source") == "FlashInfer" and "20260531" in it.get("title", ""),
)
curated_sections["code"].append(
    enrich(
        flashinfer_nightly,
        tldr=(
            "FlashInfer 0.6.12 在 5 月 31 日继续滚 nightly（dev20260531），"
            "前几日已合入 SM120 W4A16 b12x MoE、Kimi K2.5 MLA decode、CUTLASS MLA paged FP8 等改动，"
            "本次 nightly 是 0.6.12 正式版前的最后一波回归窗口。"
            "推理侧关注 FlashInfer 的工程节奏：版本号未跳，但 nightly 仍在每日刷出，"
            "意味着 vLLM/SGLang/TRT-LLM 等下游可放心 pin 到 0.6.12 系列做集成。"
        ),
        domain_tag="推理",
    )
)

# ---- community ----
nvfp4_qwen = find(
    "community",
    lambda it: "Qwen3.6-35B-A3B-NVFP4" in it.get("title", ""),
)
curated_sections["community"].append(
    enrich(
        nvfp4_qwen,
        tldr=(
            "NVIDIA 官方用 Model Optimizer 把 Qwen3.6-35B-A3B 量化到 NVFP4（4bit 浮点），"
            "仅量化 MoE 内 transformer block 的 linear 算子权重与激活，"
            "参数位宽 16→4，磁盘与显存约 3.06× 压缩，开箱给 vLLM 推理直用。"
            "工程意义：MoE 模型上 NVFP4 PTQ 已被官方背书可保留主要 MMLU 精度，"
            "Blackwell 上 NVFP4 fused MoE 内核（vLLM 0.22 已正式收口）从此有现成 35B-A3B 权重对齐做端到端验证。"
        ),
        domain_tag="推理",
    )
)

# ---- generated_at: 必须比 raw 新 ----
now = datetime.now(timezone.utc).replace(microsecond=0)
curated = {
    "generated_at": now.isoformat(),
    "lookback_hours": raw.get("lookback_hours"),
    "sections": curated_sections,
    "fetch_stats": raw.get("fetch_stats"),
}

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT}")
print(
    "counts:",
    {k: len(v) for k, v in curated_sections.items()},
    "generated_at=",
    curated["generated_at"],
)
