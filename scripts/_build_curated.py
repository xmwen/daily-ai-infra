# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 构建中文 curated。"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

with RAW.open("r", encoding="utf-8") as f:
    raw = json.load(f)

# 用 link 作为唯一键从 raw 里找回完整 item
def find(section: str, link: str) -> dict | None:
    for it in raw["sections"].get(section, []):
        if it.get("link") == link:
            return it
    return None

# (section, link, tldr, domain_tag)
picks = [
    # ===== papers =====
    ("papers",
     "https://arxiv.org/abs/2604.20503",
     "FASER 提出面向动态 LLM serving 的细粒度投机解码阶段管理，解耦 draft/verify 并按请求调整 spec 长度，低负载减尾延迟、高负载减浪费。",
     "推理"),
    ("papers",
     "https://arxiv.org/abs/2604.19767",
     "PayPal 在 2×H100 上用 EAGLE3+vLLM 对比 NVIDIA NIM，gamma=3 时吞吐涨 22-49%、延迟降 18-33%，给工业界投机解码选参提供基准。",
     "推理"),
    ("papers",
     "https://arxiv.org/abs/2604.19877",
     "Super Apriel：15B supernet 每层提供 FA/SWA/KDA/GDN 四种 mixer，单 checkpoint 通过切换 placement 在请求级动态换档，decode 吞吐覆盖 2.9×-10.7×。",
     "推理"),
    ("papers",
     "https://arxiv.org/abs/2604.20105",
     "EnergAIzer：GPU 功耗估算框架，用轻量模型预测 kernel 利用率输入，把预估从小时级压到秒级，为数据中心功耗管理提供实用工具。",
     "推理"),
    ("papers",
     "https://arxiv.org/abs/2604.20032",
     "LEO 跨 NVIDIA/AMD/Intel GPU 做 stall 根因分析，通过 backward slicing 把停顿指令归因到源代码，给多厂商 GPU 性能调优提供统一工具链。",
     "推理"),
    ("papers",
     "https://arxiv.org/abs/2604.19835",
     "Expert Upcycling：在继续预训练阶段把已训 E-expert MoE 扩展到 mE-expert，降低 MoE 扩容的通信与显存开销，属于 MoE 训练可用的工程方法。",
     "训练"),
    # ===== code =====
    ("code",
     "https://github.com/vllm-project/vllm/releases/tag/v0.20.0",
     "vLLM v0.20.0 正式版：默认 CUDA 切到 13.0 并更新 CUDA 架构列表，部署端需同步升级构建工具链与镜像。",
     "推理"),
    ("code",
     "https://github.com/NVIDIA/Megatron-LM/releases/tag/26.04-alpha.rc1",
     "Megatron-LM 26.04-alpha：新增高优先级 all-to-all 通信流选项和 HybridEP 预处理 SM 配置，面向 MoE 大规模训练的 EP 通信优化。",
     "训练"),
    ("code",
     "https://github.com/pytorch/pytorch/releases/tag/trunk%2F4918ae2275816ece67672c0dc4891889cda297f0",
     "PyTorch Inductor 新增 _FastCudaLauncher：基于 vectorcall 的 C 扩展，为预绑定 CUDA kernel 降低 Python 侧启动开销。",
     "推理"),
    ("code",
     "https://github.com/pytorch/pytorch/releases/tag/trunk%2F54995bf85913f90777eace2ced0d2c7854d083a6",
     "PyTorch DeviceMesh 强制 2 级 Layouts：顶层分离 mesh 逻辑维度、内层走 canonical 扁平形式，消除递归 IntTuple 的歧义，提升分布式代码鲁棒性。",
     "训练"),
    ("code",
     "https://github.com/pytorch/pytorch/releases/tag/trunk%2F3646a5df996c7ed344fbaba6b35ecd6164181e48",
     "PyTorch Inductor 引入 CacheabilityValidator：统一 FX 图缓存可用性判定，把 FxGraphCache、AOTAutograd、pickler 全路由到同一校验器。",
     "推理"),
    ("code",
     "https://github.com/deepseek-ai/DeepGEMM/releases/tag/nv_dev_c491439",
     "DeepGEMM nv_dev 分支新快照：DeepSeek 自研 FP8 GEMM kernel 库持续迭代，是 DeepSeek 推理栈核心算子组件。",
     "推理"),
    ("code",
     "https://github.com/openai/openai-agents-python/releases/tag/v0.14.5",
     "OpenAI Agents Python v0.14.5：新增 Modal sandbox idle timeout 选项，修复 HITL 恢复时 tool output 的 serve 问题，以及流式终端输出回填。",
     "agent"),
    ("code",
     "https://github.com/langchain-ai/langgraph/releases/tag/cli%3D%3D0.4.24",
     "LangGraph CLI 0.4.24：小版本发布，主要是 CLI 格式化和 pip 依赖组升级，面向本地 graph 开发与部署流程稳定性。",
     "agent"),
    # ===== blogs =====
    ("blogs",
     "https://developer.nvidia.com/blog/advancing-emerging-optimizers-for-accelerated-llm-training-with-nvidia-megatron/",
     "NVIDIA 在 Megatron 里集成 Shampoo 等高阶优化器用于加速 LLM 训练，讨论工程落地与收敛质量权衡，是 MoE/超大模型训练优化器选型参考。",
     "训练"),
    # ===== community =====
    ("community",
     "https://www.reddit.com/r/LocalLLaMA/comments/1ste9zs/deepseek_has_released_deepep_v2_and_tilekernels/",
     "DeepSeek 发布 DeepEP V2 与 TileKernels：MoE EP 通信与 tile 级 kernel 两个核心组件同步迭代，是 DeepSeek 推理/训练栈的关键工程产出。",
     "推理"),
    ("community",
     "https://www.reddit.com/r/LocalLLaMA/comments/1stcer1/qwen3627b_llamacpp_speculative_decoding/",
     "llama.cpp 上用 Qwen3.6-27B 开投机解码，decode 速度从 13.6 t/s 翻到 25.5 t/s，本地部署开 spec 基本是白嫖收益的真实案例。",
     "推理"),
    ("community",
     "https://www.reddit.com/r/MachineLearning/comments/1stfk9y/optimizing_transformer_model_size_inference/",
     "工程讨论：FP16+ONNX+剪枝瓶颈后接下来的路线，涉及 GPTQ/AWQ/SmoothQuant INT8-INT4 量化、低秩分解、蒸馏、TensorRT/FlashAttention 等推理优化栈选型。",
     "推理"),
    ("community",
     "https://www.band.ai/blog/dags-wrong-abstraction-multi-agent-systems",
     "band.ai 观点文：DAG 不是多 agent 系统的正确抽象，讨论 agent 运行时需要动态拓扑、事件驱动和环状反馈，属于 agent runtime 设计层面的讨论。",
     "agent"),
]

# 构建 curated 结构
curated_sections: dict[str, list[dict]] = {"papers": [], "code": [], "blogs": [], "community": []}
missing = []
for section, link, tldr, tag in picks:
    item = find(section, link)
    if item is None:
        missing.append((section, link))
        continue
    new_item = dict(item)
    new_item["tldr"] = tldr
    new_item["domain_tag"] = tag
    curated_sections[section].append(new_item)

if missing:
    raise SystemExit(f"missing items: {missing}")

out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "sections": curated_sections,
    "source": "agent_curated",
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# 打印统计
total = sum(len(v) for v in curated_sections.values())
by_tag: dict[str, int] = {}
for section_items in curated_sections.values():
    for it in section_items:
        by_tag[it["domain_tag"]] = by_tag.get(it["domain_tag"], 0) + 1
print(f"curated total={total}")
for s, items in curated_sections.items():
    print(f"  {s}: {len(items)}")
print(f"by_tag: {by_tag}")
print(f"generated_at={out['generated_at']}")
print(f"raw.generated_at={raw['generated_at']}")
