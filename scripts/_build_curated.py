# -*- coding: utf-8 -*-
"""One-shot curated builder for 2026-05-02.

Reads cache/today_raw.json, picks items matching the AI-infra focus
(inference / training / agent infrastructure), writes Chinese tldr and
domain_tag for each, emits cache/today_curated.json with a fresh
generated_at timestamp so render.py will not fallback to raw.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"


def _find(items, predicate):
    for it in items:
        if predicate(it):
            return it
    return None


def main() -> None:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    raw_sections = raw.get("sections", {})
    code_items = raw_sections.get("code", [])
    community_items = raw_sections.get("community", [])

    curated_sections = {
        "papers": [],
        "code": [],
        "blogs": [],
        "community": [],
    }

    # ========= CODE =========
    # 1) vLLM v0.20.1 — revert persistent topk
    vllm = _find(code_items, lambda x: x.get("source") == "vLLM" and "v0.20.1" in x.get("title", ""))
    if vllm:
        item = dict(vllm)
        item["tldr"] = (
            "vLLM v0.20.1 紧急回滚 v0.20.0 里合进去的 persistent topk（#41442），撤掉"
            "跨 step 复用 topk buffer 的优化。该优化原本目的是减少 sampling 阶段的"
            "重复分配与 top-k 排序开销，但在高并发或特殊采样配置下会引入正确性问题，"
            "于是 v0.20.0 发布次日就 hotfix 发 v0.20.1 单点 revert。又一个「feature 落"
            "地即回滚」的基础设施层案例，和最近 PyTorch、LangGraph 节奏同频。"
        )
        item["domain_tag"] = "推理"
        curated_sections["code"].append(item)

    # 2) OpenAI Agents v0.15.0 — ModelRefusalError
    oa_150 = _find(
        code_items,
        lambda x: x.get("source") == "OpenAI Agents" and x.get("title") == "v0.15.0",
    )
    if oa_150:
        item = dict(oa_150)
        item["tldr"] = (
            "OpenAI Agents SDK v0.15.0 把模型拒答从 silent failure 提升为显式控制流："
            "原本拒答会被当成空 final_output，结构化输出场景下还会触发 run loop 重试"
            "直到 MaxTurnsExceeded；现在统一抛 ModelRefusalError。使用方可在 Runner.run"
            "传 error_handlers={「model_refusal」: fn} 接管，fn 返回值直接当 final output"
            "并走 schema 校验。Agent runtime 对拒答语义的规范化，避免 silent 状态污染"
            "下游记忆与 trace。"
        )
        item["domain_tag"] = "agent"
        curated_sections["code"].append(item)

    # 3) OpenAI Agents v0.15.1 — WebSocket keepalive + UnixLocal PTY signal defaults
    oa_151 = _find(
        code_items,
        lambda x: x.get("source") == "OpenAI Agents" and x.get("title") == "v0.15.1",
    )
    if oa_151:
        item = dict(oa_151)
        item["tldr"] = (
            "OpenAI Agents v0.15.1 暴露 Responses WebSocket keepalive 选项，给长会话"
            "提供主动心跳；同时修复 UnixLocal PTY 终端信号默认值（SIGINT 恢复），让本"
            "地 computer-use agent 在 Linux/Mac 上跑子进程时 Ctrl+C 行为正常，不会被"
            "SDK 静默屏蔽。两处都是长跑 agent runtime 稳定性细节。"
        )
        item["domain_tag"] = "agent"
        curated_sections["code"].append(item)

    # 4) LangGraph 1.2.0a3 — merge the a3/a4/a5 + prebuilt a1/a2 + checkpoint a3
    lg_a3 = _find(
        code_items,
        lambda x: x.get("source") == "LangGraph" and "langgraph==1.2.0a3" in x.get("title", ""),
    )
    if lg_a3:
        item = dict(lg_a3)
        item["title"] = "langgraph 1.2.0a3~a5 + prebuilt 1.1.0a1/a2 + checkpoint 4.1.0a3"
        item["tldr"] = (
            "LangGraph 一晚连发 6 个 alpha：核心 feat 是 stream_events(version='v3') "
            "dispatch 到 Pregel + DeltaChannel 用 sentinel+checkpoint_writes 重建、"
            "node-level error handlers、graph graceful shutdown/drain；chore 侧做了"
            "checkpoint two phase read 减少不必要数据搬运、dynamic push-task timeouts、"
            "idle timeout；修复 NodeTimeoutError 默认可重试、arrival-ordered interleave"
            "for StreamChannel projections、_messages_delta_reducer 的 dict/str 强转。"
            "timers 重构在 4/28 revert 之后继续收敛，整条时间轴是 agent runtime 在流"
            "式/超时/通道调度上的系统级打磨。"
        )
        item["domain_tag"] = "agent"
        curated_sections["code"].append(item)

    # 5) XGrammar v0.2.0 — structural tag perf + gpt-oss tool-calling fix
    xg = _find(
        code_items,
        lambda x: x.get("source") == "XGrammar" and x.get("title") == "v0.2.0",
    )
    if xg:
        item = dict(xg)
        item["tldr"] = (
            "XGrammar v0.2.0 大版本：在高 tool 数量下大幅降低 structural-tag 的编译耗"
            "时（perf 侧对 tool use 场景直接减尾延迟）、修复 gpt-oss 的 tool-calling"
            "格式、把 builtin structural tags 对齐 chat templates 的 reasoning 与"
            "tool calls；同时 refactor 了 reasoning 参数并在 GrammarMatcher 上暴露"
            "draft tree traversal，给投机解码接 constrained decoding 打基础。"
        )
        item["domain_tag"] = "agent"
        curated_sections["code"].append(item)

    # ========= COMMUNITY =========
    # 6) PFlash — Luce 10x prefill speedup on 3090 Qwen3.6-27B 128K
    pflash = _find(
        community_items,
        lambda x: "PFlash" in x.get("title", "") and "10x prefill" in x.get("title", ""),
    )
    if pflash:
        item = dict(pflash)
        item["tldr"] = (
            "Luce-Org 发布 PFlash（MIT，纯 C++/CUDA，不走 Triton/PyTorch），把长上下文 "
            "prefill 做成投机式：小 drafter 进程内对整份 prompt 打 token 重要性分，重"
            "型 target 只在关键 span 上做 prefill。实测 RTX 3090 Qwen3.6-27B Q4_K_M，"
            "128K 上 TTFT 24.8s vs 原生 llama.cpp 257s，约 10.4×；64K 上 13.5s vs 135s，"
            "NIAH 检索端到端保真。是 DFlash 之后同一团队把「投机」从 decode 扩到 prefill"
            "的工程化产物。"
        )
        item["domain_tag"] = "推理"
        curated_sections["community"].append(item)

    # 7) MiniMax M2.7 AWQ-4bit 2x Spark vs 2x RTX 6000 96GB
    spark = _find(
        community_items,
        lambda x: "MiniMax M2.7" in x.get("title", "") and "Spark" in x.get("title", ""),
    )
    if spark:
        item = dict(spark)
        item["tldr"] = (
            "社区用 cyankiwi/MiniMax-M2.7-AWQ-4bit 做了 2×DGX Spark unified memory "
            "fabric vs 2×RTX 6000 96GB 的对比基准：6000 在 prompt 处理上领先 2.7×、"
            "token 生成领先 4.88×；价格差约 2.9×、功耗 6000 贵得多，Spark 在同等能"
            "效预算下追得很近。对正在做 ScaleUp 统一内存与国产芯片路线的工程决策"
            "直接可参考——unified memory fabric 在中等量化 MoE 推理上并非远落后于"
            "离散 HBM 大卡。"
        )
        item["domain_tag"] = "推理"
        curated_sections["community"].append(item)

    # 8) Qwen3.6-27B native vLLM on Windows 3090
    native_win = _find(
        community_items,
        lambda x: "Qwen3.6-27B" in x.get("title", "") and "Windows" in x.get("title", ""),
    )
    if native_win:
        item = dict(native_win)
        item["tldr"] = (
            "devnen 给出 Windows 原生 vLLM 方案（无 WSL/Docker），RTX 3090 跑 "
            "Qwen3.6-27B：短 prompt 72 tok/s、25k 上下文 64.5 tok/s、127k 单卡 "
            "53.4 tok/s、双 3090 PP=2 可到 160k 上下文；对比 Linux 5090 + TurboQuant"
            "3-bit KV 的 160 tok/s 社区纪录，Windows 单 3090 大概差一档但工程门槛低。"
            "patch 过的 vLLM + 便携 launcher 是 Windows 本地部署能从 Linux 基线收敛过来"
            "的一个工程样本。"
        )
        item["domain_tag"] = "推理"
        curated_sections["community"].append(item)

    # 9) Mistral Medium 3.5 YaRN mscale_all_dim fix — merge two duplicate posts
    yarn_fix = _find(
        community_items,
        lambda x: "Unsloth solved bug" in x.get("title", ""),
    )
    if yarn_fix:
        item = dict(yarn_fix)
        item["title"] = "Mistral Medium 3.5 YaRN mscale_all_dim=1→0 修复（Unsloth + Mistral 联合）"
        item["tldr"] = (
            "Mistral Medium 3.5 发布时 transformers 与 llama.cpp 上均出现长上下文输出"
            "崩坏，根因是 YaRN 解析时 mscale_all_dim 被当成 1；Unsloth 协同 Mistral "
            "修复，把 mscale_all_dim 改为 0 才还原官方行为，同时修了 mmproj 未正确生"
            "成。GGUF 全量重刷后长上下文稳定性明显回归。一个典型的 RoPE 扩展实现细"
            "节跨仓库一致性 bug——实现不同、解析默认值不同，模型权重完全相同也会"
            "给出截然不同的结果。"
        )
        item["domain_tag"] = "推理"
        curated_sections["community"].append(item)

    # ========= write =========
    curated = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lookback_hours": raw.get("lookback_hours"),
        "sections": curated_sections,
        "fetch_stats": raw.get("fetch_stats", {}),
        "source": "today_curated.json",
    }
    OUT.write_text(
        json.dumps(curated, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    total = sum(len(v) for v in curated_sections.values())
    by_tag = {"推理": 0, "训练": 0, "agent": 0}
    for items in curated_sections.values():
        for it in items:
            tag = it.get("domain_tag")
            if tag in by_tag:
                by_tag[tag] += 1
    print(
        f"curated total={total} "
        f"papers={len(curated_sections['papers'])} "
        f"code={len(curated_sections['code'])} "
        f"blogs={len(curated_sections['blogs'])} "
        f"community={len(curated_sections['community'])} "
        f"| tag 推理={by_tag['推理']} 训练={by_tag['训练']} agent={by_tag['agent']}"
    )
    print(f"generated_at={curated['generated_at']}")
    print(f"raw generated_at={raw.get('generated_at')}")


if __name__ == "__main__":
    main()
