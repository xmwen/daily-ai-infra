"""
一次性脚本：读 today_raw.json，按筛选偏好挑选条目，写中文 tldr + domain_tag，
输出 today_curated.json。generated_at 必须比 raw 新。
"""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

# 建 link -> raw item 的索引
idx = {}
for sec, items in raw["sections"].items():
    for it in items:
        idx[it["link"]] = it

# (link, tldr, domain_tag)
picks = [
    # ===== papers (6) =====
    (
        "https://arxiv.org/abs/2604.18616",
        "Argus：用 data-flow invariant 作为编译期规约约束 LLM agent 生成 GPU kernel，针对 matmul/attention/MoE 做 tile+shared memory+软流水协同优化，补齐 pass/fail 反馈不足的短板。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.19241",
        "UniEP：面向 Megatron-LM 的 MoE MegaKernel，把 expert parallel 的通信压缩与计算-通信重叠收进统一 kernel，解决现有 EP 方案适配差、易牺牲数值稳定的老问题。",
        "训练",
    ),
    (
        "https://arxiv.org/abs/2604.18655",
        "高通 SM8650/8750 上 LLaMA 端侧推理方案：多 LoRA 作为运行时输入共享冻结计算图，任务切换无需重编译；配合多流解码并发生成风格变体，工程化很扎实。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2505.16968",
        "CASS：首个 CUDA↔HIP、SASS↔RDNA3 源码/汇编双层翻译的数据集与模型套件，6 万对已验证代码，CUDA→HIP 准确率 88.2%，显著优于 GPT-5.1/Claude-4.5/Hipify，对国产 GPU 生态迁移有参考意义。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.19004",
        "Ocean：GPU SpGEMM 用估算代替两遍 symbolic pass（原本占 28% 耗时），直接基于估值分配输出空间，H100 实测明显提速；稀疏算子走向「估算优先」的新范式。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2604.18909",
        "ChipLight：chiplet + 光互联协同设计，把 scale-up die 间带宽与 scale-out 长距链路统一建模，跨层优化 LLM 训练集群的并行策略与互联拓扑，思路和 ScaleUp 统一内存同源。",
        "训练",
    ),

    # ===== code (6) =====
    (
        "https://github.com/pytorch/pytorch/releases/tag/trunk%2F0274ad69c3effaef66b5776db5f752b6cf7d8154",
        "PyTorch Inductor 修复 combo kernel 的 optimize_mem 传递链：之前该标志被 cached_autotune 默认改写为 True，现已显式透传 is_inference/is_backward，保持与独立 kernel 行为一致。",
        "训练",
    ),
    (
        "https://github.com/pytorch/pytorch/releases/tag/trunk%2F89ed986a77847a4cec520920f6d27baa72102995",
        "PyTorch Inductor：combo kernel 的 jit_line 改用统一的 triton_meta_common()，消除 codegen 路径分叉，后续 Inductor 元信息调整只需改一处。",
        "训练",
    ),
    (
        "https://github.com/langchain-ai/langgraph/releases/tag/1.1.9",
        "LangGraph 1.1.9：修复普通 resume 场景下 ReplayState 错误传递给子图的 bug，回退了一处不必要的 stream handler 改动；影响状态机回放正确性，生产用户建议升级。",
        "agent",
    ),
    (
        "https://github.com/vllm-project/vllm/releases/tag/v0.20.0rc1",
        "vLLM v0.20.0rc1：本轮 RC 主要是 revert 「把 pyav/soundfile 挪到通用依赖」 的改动，说明新版对多模态栈的依赖边界还在调整，升级前先看清依赖面。",
        "推理",
    ),
    (
        "https://github.com/openai/openai-agents-python/releases/tag/v0.14.4",
        "OpenAI Agents SDK 0.14.4：沙箱子系统重构——BoxMount、ephemeral mount 生命周期共享、tar exclude 复用、session helper 抽离，computer-use agent 运行时更接近生产级。",
        "agent",
    ),
    (
        "https://github.com/llvm/llvm-project/releases/tag/llvmorg-22.1.4",
        "LLVM 22.1.4 发布：MLIR/编译器栈上游稳定版推进，Triton/Inductor/vLLM 等生态升级的上游依赖基线跟进点。",
        "推理",
    ),

    # ===== blogs (1) =====
    (
        "https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/",
        "Google ReasoningBank：把 agent 的成功/失败轨迹抽象成可复用「推理记忆条目」供后续任务检索，属于 agent memory 工程化的又一范式尝试，和 MemFactory 形成对照。",
        "agent",
    ),

    # ===== community (7) =====
    (
        "https://www.reddit.com/r/LocalLLaMA/comments/1ss5j2x/moonshot_opensourced_flashkda_cutlass_kernels_for/",
        "Moonshot 开源 FlashKDA：Kimi Delta Attention 的 CUTLASS C++ 前向 kernel，H20 上相对 FLA 的 Triton 基线最高 2.22× 加速，并作为 FLA 后端集成；线性注意力落到生产 kernel 的典型案例。",
        "推理",
    ),
    (
        "https://www.reddit.com/r/MachineLearning/comments/1ssdt0z/int3_compressionfused_metal_kernels_r/",
        "Spiral：Qwen 7B 的 INT3 权重（+0.14 nats）+ INT2 KV cache，配 Apple Metal 融合 kernel，在 M 系列 Mac 上端到端跑通；极端量化配专用 kernel 的工程实践。",
        "推理",
    ),
    (
        "https://arxiv.org/abs/2603.29493",
        "MemFactory：首个面向「记忆增强 agent」的统一训练/推理框架，把 memory 提取/更新/检索抽成原子可插拔组件，支持在其上跑 RL（含 GRPO）；对标 LLaMA-Factory 的 agent memory 版。",
        "agent",
    ),
    (
        "https://burnish-demo.fly.dev",
        "Burnish：通用 MCP 服务器 UI，从 tool JSON schema 自动渲染表单并按响应结构渲染卡片/表格/图表，无需 LLM 或 chat 客户端——适合调试任意 MCP server 暴露的工具。",
        "agent",
    ),
    (
        "https://github.com/panpeter/sift-skill",
        "Sift：agentic coding 场景的「子 agent 日志压缩」脚手架，cargo test/pytest 等长输出先喂给便宜模型总结再回注主 thread，作者自测某工作流总 token 成本约降 45%。",
        "agent",
    ),
    (
        "https://zainhas.github.io/blog/2026/inside-claude-code-architecture/",
        "Claude Code 架构深度解析：工具调度、context 管理、子任务编排等 coding agent 关键 runtime 设计被系统整理，是研究 Claude Code/Cursor/Codex 这类系统的必读参考。",
        "agent",
    ),
    (
        "https://github.com/NVlabs/parrot",
        "NVlabs Parrot：C++ 库，把一串 Thrust/CUDA 数组操作融合成单 kernel，避免中间落地；适合做数据预处理/后处理管线融合，思路和 CUB 的 device-wide 原语互补。",
        "推理",
    ),
]

def build_curated_items():
    out_items = []
    missing = []
    for link, tldr, tag in picks:
        item = idx.get(link)
        if not item:
            missing.append(link)
            continue
        new_item = dict(item)  # 保留全部原始字段
        new_item["tldr"] = tldr
        new_item["domain_tag"] = tag
        out_items.append(new_item)
    if missing:
        raise SystemExit(f"[curated] missing links in raw: {missing}")
    return out_items

curated_items = build_curated_items()

# 按 section 分组
sections = {"papers": [], "code": [], "blogs": [], "community": []}
for it in curated_items:
    sections[it["section"]].append(it)

# generated_at 必须比 raw 新
now_utc = datetime.now(timezone.utc)
raw_gen = raw["generated_at"]
# 简单校验
from datetime import datetime as _dt
raw_dt = _dt.fromisoformat(raw_gen.replace("Z", "+00:00"))
if now_utc <= raw_dt:
    # 强制 +1 分钟（理论不会发生，但兜底）
    from datetime import timedelta
    now_utc = raw_dt + timedelta(minutes=1)

curated = {
    "generated_at": now_utc.isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "source": "agent-curated",
    "sections": sections,
}

OUT.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"[curated] wrote {OUT}")
print(f"[curated] total={len(curated_items)} papers={len(sections['papers'])} code={len(sections['code'])} blogs={len(sections['blogs'])} community={len(sections['community'])}")
# domain_tag 分布
tag_counts = {}
for it in curated_items:
    tag_counts[it["domain_tag"]] = tag_counts.get(it["domain_tag"], 0) + 1
print(f"[curated] tags={tag_counts}")
print(f"[curated] raw.generated_at = {raw_gen}")
print(f"[curated] curated.generated_at = {curated['generated_at']}")
