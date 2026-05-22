# -*- coding: utf-8 -*-
"""一次性生成 today_curated.json：手写中文 tldr + domain_tag。
中文双引号统一用「」避开 Python 字符串闭合坑。"""

from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with RAW.open("r", encoding="utf-8") as f:
    raw = json.load(f)


def by_link(section_name: str):
    return {it["link"]: it for it in raw["sections"][section_name]}


P = by_link("papers")
C = by_link("code")
B = by_link("blogs")
M = by_link("community")


def pick(d, link, tldr, tag):
    if link not in d:
        raise KeyError(f"link not in raw: {link}")
    item = dict(d[link])
    item["tldr"] = tldr
    item["domain_tag"] = tag
    return item


papers = [
    pick(
        P,
        "https://arxiv.org/abs/2605.22416",
        "AVMP（Asymmetric Virtual Memory Paging）针对 Jamba 等 Mamba+Transformer 混合架构推理：KV cache 线性增长 vs SSM state 每层定长，统一池子按 attention page 对齐填充 SSM 浪费高达 7.3× 显存，静态双池又无法跟随 prompt 分布漂移。方案：两类 cache 物理分两池但共享统一虚拟地址空间，仅在分配失败时触发迁移，行为确定性。命中用户 vLLM × Hybrid Mamba+Attention KV 工程方向。",
        "推理",
    ),
    pick(
        P,
        "https://arxiv.org/abs/2512.09472",
        "WarmServe 针对多 LLM 共享 GPU 集群 serving 的 TTFT 退化问题——现有系统在提升利用率时牺牲 TTFT，本质是缺乏对未来 workload 的感知。基于「真实 serving workload 强周期性+长期可预测」的实证观察，提出 one-for-many GPU prewarming：按预测把多模型参数主动预装到 GPU，需要时迅速实例化，避免冷启动等加载。多模型 serving 调度的「预装一对多」抽象，对位标准 LRU 模型 cache。",
        "推理",
    ),
    pick(
        P,
        "https://arxiv.org/abs/2511.02043",
        "Flashlight 是 PyTorch 生态内 compiler-native 的 attention 变体加速框架——FlashAttention/FlexAttention 仅支持有限静态变体，新变体仍需手写 kernel。Flashlight 自动生成融合 kernel，把 attention 变体支持从「静态模板+少数变体」推到「编译期自动生成」，理论上覆盖 FlashAttention-like 的整族。延续 CUTLASS/cuTile/TLX 之后第四条「attention 变体自动化」工程路径。",
        "推理",
    ),
    pick(
        P,
        "https://arxiv.org/abs/2605.22014",
        "LiveR 解决弹性训练的「stop-and-restart」痼疾：现有系统遇到 spot 实例回收/扩缩容时通过 checkpoint→重建分布式 runtime→重启走完整 CUDA init+communicator setup，每次 resize 都是存储重活+长 downtime。LiveR 提出 live reconfiguration 细粒度弹性，在运行时直接重配并行拓扑，避开 ckpt I/O 与冷启动。对位 Megatron 弹性 PP 与 5/20 DynaTrain 是同期不同思路答卷。",
        "训练",
    ),
    pick(
        P,
        "https://arxiv.org/abs/2605.07985",
        "Dooly v2 接续 5/12 首版的「配置无关 LLM 推理仿真器」工作——profile-based simulator 把 op 集合硬编到具体配置导致每个配置都要重新 profile，但 head size/layer count 等大量配置值跨模型复用，同一 op 在多种配置下其实在跑。v2 升级跨配置共享 op profile，模型架构/serving engine/attention backend/硬件四维探索成本大幅下降，配 5/13 GRIEF/5/19 Hawkeye/5/21 Silent Hyperparameter 同母题。",
        "推理",
    ),
    pick(
        P,
        "https://arxiv.org/abs/2602.23200",
        "InnerQ 是硬件感知免调优的 KV cache 量化方案：transformer 解码期 KV cache 显存占主导，prior 工作压缩 KV 时往往牺牲精度。InnerQ 沿 cache 矩阵不同轴做 group-wise 量化，更贴近硬件存取模式，decode latency 直降但下游评测无损。延续用户 RaBitQ/TurboQuant/OCTOPUS 的 KV codec 母题，免调优属性对生产 drop-in 部署友好。",
        "推理",
    ),
    pick(
        P,
        "https://arxiv.org/abs/2605.21603",
        "DynaFlow 处理 intra-device 并行普及痛点——现有框架是静态顺序模型，开启 op 重叠需要侵入式重写且对 workload/model/硬件高度敏感，工程不可维护。DynaFlow 提供透明可编程的 op 调度抽象，把策略与模型解耦，让 intra-device 并行真正可移植。对位 PyTorch CUDA Graph 静态切分与 vLLM piecewise compile，是策略层的工程化答卷。",
        "推理",
    ),
]

code = [
    pick(
        C,
        "https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc15",
        "TensorRT-LLM v1.3.0rc15 重磅 release——模型侧 Gemma4 多模态（文本/视觉/音频/chunked prefill 全支持）、Kimi K2.5 多模态 vision+reasoning parser、GPT-OSS/Ministral3/Nemotron-H/Nemotron Nano/DeepSeek 全家桶兼容更新、DeepSeek V4 与 V3.2 attention kernel/routing/tokenizer/AutoConfig 全面打磨。API 侧新增 typed 异常层级+typed Slurm 失败、VisualGen public output API、serving batch inference 与 benchmark timing 解耦。frontier MoE 推理引擎的关键里程碑。",
        "推理",
    ),
    pick(
        C,
        "https://github.com/triton-lang/triton/releases/tag/v3.7.0",
        "Triton 3.7 正式发布——前端补齐 tl.squeeze/tl.unsqueeze + scaled batched matmul + FP8 constants + JIT 返回 constexpr；Gluon 与 layout 持续改进、AMD/HIP 与 NVIDIA backend 双轴推进、Proton profiling 升级。kernel 生态继续从 PyTorch ecosystem extension 走向独立的 GPU DSL，是 5/13 TLX/Flashlight 的上游配套。",
        "推理",
    ),
    pick(
        C,
        "https://github.com/langchain-ai/langgraph/releases/tag/1.2.1",
        "LangGraph 1.2.1 续 5/13 正式版 1.2.0 后的首个 patch——新增 before_builtins opt-in 让 stream transformer 在内置处理前介入，并修复 v3 messages 中 tool results 误漏入用户可见消息的边界 bug。延续 4/28 timers revert→1.2.0a→1.2.0→1.2.1 完整收敛节奏，stream/tool 边界继续打磨。",
        "agent",
    ),
    pick(
        C,
        "https://github.com/openai/openai-agents-python/releases/tag/v0.17.3",
        "OpenAI Agents v0.17.3 一波 11+ fix 进入「补漏期」——mountpoint credentials 不进 sandbox 命令、memory 可选依赖统一报错、guardrail 计数与 None text 防护、FunctionTool/Codex output schema 不再 mutate、Vercel sandbox terminal state 跳过 wait_for_status、hosted_tool_call 在 remove_all_tools handoff filter 中正确过滤。延续 v0.17.0-v0.17.2 sandbox/tracing/sessions 收紧路线，agent SDK 进入安全边界与正确性补漏的「成熟期」。",
        "agent",
    ),
]

blogs = [
    pick(
        B,
        "https://developer.nvidia.com/blog/unlock-exascale-performance-on-nvidia-gb200-nvl72-with-slurm-topology-aware-job-scheduling/",
        "NVIDIA 发布 GB200 NVL72 上 Slurm topology-aware 调度方案——AI 模型规模复杂度上升，NVL72 这类紧耦合超节点要发挥性能不仅看硬件，更看 workload 放置策略。topology-aware 调度把 NVLink/NVSwitch 拓扑显式编码到 Slurm 决策面，把同 rack/同 NVL72 内通信亲和提到一等公民。对国产 ScaleUp 超节点训练调度直接参考。",
        "训练",
    ),
    pick(
        B,
        "https://developer.nvidia.com/blog/get-real-time-visibility-into-gpu-usage-across-kubernetes-clusters/",
        "NVIDIA 推出 K8s 集群级 GPU 实时观测方案——AI infra 平台团队跑 K8s workload 时常缺乏 GPU 利用率深度可见性，单 node 工具难以汇聚到 fleet 层。新方案补齐 K8s 原生 GPU usage real-time visibility，与 5/12 NVIDIA Fleet Intelligence/5/21 OFU 形成「fleet 级 GPU 效率」三件套，从指标定义→集群聚合→调度反馈完整可观测闭环。",
        "推理",
    ),
]

community = [
    pick(
        M,
        "https://www.reddit.com/r/LocalLLaMA/comments/1tkih6y/llamacpp_asymmetric_kv_q8q4_cache_current_caveats/",
        "llama.cpp 非对称 KV 量化（-ctk q8 -ctv q4 等组合）当前 CUDA 后端会让 prompt processing 回落到 CPU，PP 性能崩盘。社区 sanmai 给出小评测：异步 8/4 bit KV 量化仅 1.3% 精度损失却省大量显存；解法是编译时 -DGGML_CUDA_FA_ALL_QUANTS=ON 或直接修补 CUDA 源把组合列入。延续用户 KV 量化方向的工程主线，与 OCTOPUS/InnerQ 同期实测信号。",
        "推理",
    ),
    pick(
        M,
        "https://www.reddit.com/r/LocalLLaMA/comments/1tk0grd/latest_b9274_addresses_mtp_vram_leak/",
        "llama.cpp b9274 修复 MTP 模型 VRAM 泄漏——server_context_impl::destroy() 只清理主模型/主 ctx，spec/draft ctx/draft model 未释放，sleep/resume 循环每次新分配但旧资源不回收，VRAM 持续蠕动直至崩溃。PR #23461 让 sleep 时正确释放 draft/MTP 资源。延续 5/4 KTransformers→5/16 llama.cpp merge→5/17 多硬件实测→5/20 LM Studio 跟进→5/21 ik 分支差异 之后 MTP 工程化下沉曲线的「生产稳定性补漏」新阶段。",
        "推理",
    ),
    pick(
        M,
        "https://www.reddit.com/r/LocalLLaMA/comments/1tkjpsh/openbmb_presents_the_model_bitcpmcann_158_bit/",
        "OpenBMB 在华为昇腾 910B 上验证 BitCPM-CANN 1.58 bit 模型——三元权重模型在国产 NPU CANN 栈跑通是 BitNet 路线在非 NVIDIA 硬件落地的关键信号点，延续 5/4 VitaLLM BitNet ASIC 与 4/29 Ascend MoE relay-free 通信方向，对国产芯片走极致量化推理路径直接证据。",
        "推理",
    ),
    pick(
        M,
        "https://vibedock.dev/",
        "Vibedock 是 macOS 菜单栏小工具，用于一键切换 Claude Code 的 MCP server 开关。MCP 协议在桌面 agent 客户端从「能力清单」走向「能力开关」UX 化的早期信号——MCP 生态从协议层进到用户可见的 capability governance 层，与 5/20 NVIDIA Verified Agent Skills + Atlassian MCP audit 同方向。",
        "agent",
    ),
    pick(
        M,
        "https://www.reddit.com/r/LocalLLaMA/comments/1tkbupt/new_release_of_rocm_based_mlx_llm_engine/",
        "lemon-mlx-engine 完成 TheRock/ROCm 7.13 集成发布 b1034-stable——MLX 风格 LLM 推理引擎在 AMD ROCm 栈最新版上跑 Qwen3/3.5/3.6 MoE+dense 全系列，附带 kernel 修复。延续 5/2 vLLM-ROCm 入 Lemonade 之后 AMD 推理栈第二个独立工程化方向，社区 AMD 推理生态在 ROCm 7.13 拐点继续扩张。",
        "推理",
    ),
]

curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {
        "papers": papers,
        "code": code,
        "blogs": blogs,
        "community": community,
    },
    "fetch_stats": raw.get("fetch_stats", {}),
}

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved: {OUT}")
print(f"papers={len(papers)} code={len(code)} blogs={len(blogs)} community={len(community)}")

# domain_tag 分布
tags = {"推理": 0, "训练": 0, "agent": 0}
for sec in curated["sections"].values():
    for it in sec:
        tags[it["domain_tag"]] += 1
print(f"tags: {tags}")
