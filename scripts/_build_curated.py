# -*- coding: utf-8 -*-
"""一次性脚本：手写中文 curated。"""
import json, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

def find(section, key):
    for it in raw["sections"][section]:
        if key in it["title"] or key in it["link"]:
            return it
    raise KeyError(f"{section}/{key} not found")

curated_sections = {"papers": [], "code": [], "blogs": [], "community": []}

# ============ code ============
# Mooncake v0.3.11.post1：与昨日重复（昨日已覆盖核心 mlx5dv UDP sport + TENT QoS）。今日只新增几个 chore（WITH_NVIDIA_PEERMEM 默认、release-npu workflow、结构化对象存储 helper），无新工程信号——跳过避免凑数。

# FlashInfer 2 条 nightly 无 changelog，跳过。

# SGLang v0.5.12.post1：昨日刚发，无新独立工程改动——跳过。

# ============ blogs ============
# 空

# ============ papers ============
# 周日 arXiv 不更新

# ============ community ============

# 1. llama.cpp server 内置原生 tools（HN+r/LocalLLaMA 同主题两条合并为 1 条）
it = find("community", "1tluma3")  # r/LocalLLaMA "llama.cpp server have built-in native tools"
itc = dict(it)
itc["tldr"] = (
    "llama.cpp server 通过实验 flag `--tools` 直接内置一批原生 tool：read_file/file_glob_search/grep_search/"
    "exec_shell_command/write_file/edit_file/apply_diff/get_datetime。等于把 llama-server 二进制本身变成一套迷你 "
    "agent harness，运行 GGUF 即可让本地小模型做 file edit + shell exec + grep。与 MCP/OpenAI Agents 等外挂 "
    "runtime 形成对照——「在推理 server 内嵌 tool 执行」是更底层的 agent infra 范式，把工具调用从协议层下沉到 "
    "serving 层。配套 r/LocalLLaMA 另一条帖子用 firejail+独立 linux 用户 vmagents 做多重 sandbox 安全防护，"
    "为本地 agent harness 的边界收紧给出参考。"
)
itc["domain_tag"] = "agent"
curated_sections["community"].append(itc)

# 2. SSV（Sparse Speculative Verification）— HN LLM infra 帖
it = find("community", "2605.19893")
itc = dict(it)
itc["tldr"] = (
    "SSV 把投机解码的 verification 阶段做成稀疏 attention：observation 是 verifier forward 在 draft tokens "
    "上的 attention 远比 prefill 稀疏，因此提出 sparse speculative verification——只对预测高接受率位置做 dense "
    "attention，其余走稀疏路径。延续本月 5/12 SPECTRE→5/14 PipeSD→5/15 ECHO→5/20 SpecSA→5/21 NanoCP 投机解码×"
    "稀疏 attention 母题，把「verification compute 是 SD 新瓶颈」从 5/15 ECHO 的 super-tree 调度延伸到 attention "
    "层稀疏化的工程兼容方向。"
)
itc["domain_tag"] = "推理"
curated_sections["community"].append(itc)

# 3. CodeGraph — Semantic Code Intelligence for Claude Code/Cursor/Codex
it = find("community", "codegraph")
itc = dict(it)
itc["tldr"] = (
    "CodeGraph 提出给 Claude Code/Cursor/Codex 类 coding agent 加一层语义代码图谱——把项目 AST + 调用关系 + "
    "符号定义预构建成图，agent 检索时不再依赖 grep/embedding 召回，而是按图遍历邻接节点。属于 coding agent infra "
    "新一波「retrieval substrate」工作，与 5/19 LangGraph 组织级 agent 实战、5/24 fleet 多 Claude Code 并发 "
    "supervisor 一起，构成 coding agent 周边 infra 三层（检索底座 / 协作调度 / 并发管理）逐步成型的信号。"
)
itc["domain_tag"] = "agent"
curated_sections["community"].append(itc)

# 4. fleet — Python supervisor for running coding agents in parallel
it = find("community", "48256389")
itc = dict(it)
itc["tldr"] = (
    "Fleet 是 Python 写的 coding agent 并发 supervisor，起源于 AMD 在 Claude Code repo 提的 bug——AMD 在用 beads "
    "队列跑 50+ Claude Code session 协同 coding。作者先用 bash loop + beads claim 任务的简陋实现验证，再做成 "
    "Python 中心化 supervisor。意义在于把单 agent CLI（claude/codex/cursor）做成 fleet-level 调度对象，回应了"
    "「企业级 coding agent runtime 缺一个 supervisor 层」的客观需求，对照 OpenAI Agents SDK 的 sandbox 加固，"
    "属于 coding agent infra 另一条「并发执行管理」演进路线。"
)
itc["domain_tag"] = "agent"
curated_sections["community"].append(itc)

# 5. Characterization of ML compilers for LLM inference on NVIDIA GPUs (Springer)
it = find("community", "s11227-026-08559-6")
itc = dict(it)
itc["tldr"] = (
    "对 NVIDIA GPU 上 LLM 推理用的多个 ML 编译器（Triton/TVM/Inductor/XLA 等）做系统性 characterization。"
    "属于「推理后端复现性」母题的最新一作——延续 5/12 KernelBenchX 任务结构分析、5/19 Hawkeye 非确定性 CPU 比特"
    "复现、5/20 Silent Hyperparameter 200 推理引擎调研、5/22 Dooly 跨配置 op profile 共享。Springer 期刊版本"
    "更面向编译器选型与跨编译器性能差异溯源，对国产芯片 MLIR 工具链对齐 NVIDIA 编译器语义有间接参考。"
)
itc["domain_tag"] = "推理"
curated_sections["community"].append(itc)

# 6. Qwen3.6-35B-A3B vs Gemma4-26B-A4B on Radeon 9070 XT
it = find("community", "1tmbola")
itc = dict(it)
itc["tldr"] = (
    "用户在 AMD Radeon 9070 XT + 最新 llama.cpp 上对比 Qwen3.6-35B-A3B 与 Gemma4-26B-A4B：Qwen 结果质量更好但 "
    "Gemma4 跑得快得多。这条实测意义在于 AMD 消费卡 ROCm 路径对两类 MoE 推理性能差异的对照——延续 5/22 "
    "OpenBMB BitCPM-CANN 昇腾 + lemon-mlx-engine ROCm 7.13 等「非 NVIDIA 推理栈实测」母题，是 RDNA4 9070 XT "
    "作为推理卡的早期工程数据点。"
)
itc["domain_tag"] = "推理"
curated_sections["community"].append(itc)

# 7. Qwen3.6 MTP 在 DCSS / tool-call 场景的失效记录
it = find("community", "1tm9nx3")
itc = dict(it)
itc["tldr"] = (
    "用户实测 Qwen3.6-35B-A3B Q4_K_XL 玩 roguelike 游戏 DCSS：非 MTP 版工作良好，但 MTP 版出现 tool call bug，"
    "输出全部塞进 tool/thinking 块导致输出 mangle + 重复错误 tool call，反而抵消 MTP 的加速。这是 5/4-5/23 "
    "整条 MTP 工程化下沉曲线（KTransformers 首发→llama.cpp master merge→多硬件实测→长 ctx 边界→生产稳定性"
    "补漏）后的新边界——「MTP × tool calling 在某些 grammar / chat template 上仍有失配」，与 5/21 ik_llama.cpp "
    "MTP 主线后反退的 12GB 110tps 案例同源，是 MTP 进入生产成熟度评估的新数据点。"
)
itc["domain_tag"] = "推理"
curated_sections["community"].append(itc)

curated = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours"),
    "sections": curated_sections,
    "fetch_stats": raw.get("fetch_stats", {}),
    "source_raw_generated_at": raw.get("generated_at"),
}

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")

total = sum(len(v) for v in curated_sections.values())
by = {k: len(v) for k, v in curated_sections.items()}
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for sec in curated_sections.values():
    for it in sec:
        tag_count[it["domain_tag"]] = tag_count.get(it["domain_tag"], 0) + 1
print(f"curated total: {total}  by_section: {by}  domain_tag: {tag_count}")
print(f"generated_at: {curated['generated_at']}")
print(f"raw generated_at: {curated['source_raw_generated_at']}")
