# -*- coding: utf-8 -*-
"""一次性脚本：基于 today_raw.json 生成中文 curated。"""
import json, datetime, pathlib

RAW = pathlib.Path("cache/today_raw.json")
OUT = pathlib.Path("cache/today_curated.json")

raw = json.loads(RAW.read_text(encoding="utf-8"))

def pick(section, link_sub, tldr, domain_tag):
    for item in raw["sections"].get(section, []):
        if link_sub in item["link"]:
            new = dict(item)
            new["tldr"] = tldr
            new["domain_tag"] = domain_tag
            return new
    return None

curated = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {"papers": [], "code": [], "blogs": [], "community": []},
}

# ============ papers ============
papers_specs = [
    ("2604.22312", "GVR（Guess-Verify-Refine）是面向 Blackwell 稀疏注意力 decode 的 data-aware 精确 Top-K 算法。利用连续 decode 步间的时序相关性：用上一步 Top-K 作预测信号，结合预索引统计，以 secant 式计数在 1-2 次 global pass 内收敛到合法阈值，再用无 ballot 收集器验证候选。把长上下文 LLM serving 中「一次 decode 一次 Top-K」的瓶颈压到最小，工程意义是把 kernel 已充分优化后的剩余长尾进一步拿掉。", "推理"),
    ("2604.22126", "GICC 针对 HPE Slingshot 这类 OFI 互联给 GPU kernel 提供真正的 GPU-initiated 跨节点通信 runtime。痛点：host-driven progress + 缺乏 pre-staged NIC work 的有界回收机制，导致 kernel 无法自主触发分布式协调；InfiniBand 现有实现又带不必要的 sync/lock 开销。GICC 让 distributed GPU app 的 launch overhead 降下来、计算-通信 overlap 更彻底，对 DeepSeek 级别的大规模训练/RL 流程是直接增益。", "训练"),
    ("2604.22092", "FlashSpread 把非马尔可夫（renewal）疫情仿真的每步 pipeline（CSR 遍历、数值稳定 erfcx 风险评估、Bernoulli tau-leaping、状态转移、下一步感染性写回）融合进单个 Triton kernel，中间结果全程驻留 SM 寄存器不回显存，配合 block-scalar skip 保持 CUDA Graph 可捕获。虽是疫情场景，但把多阶段 IO-bound pipeline 压成一个寄存器级 fused Triton kernel 的范式，对 LLM 推理的 prefill/decode 融合同样有参考价值。", "推理"),
    ("2604.22228", "把 CUDA Graph 集成进 UCX 框架，在节点内同时利用 NVLink 与 PCIe-through-host 两条路径做 GPU-to-GPU 点对点通信。相比单路径，多路径+CUDA Graph 把通信开销显著压低。意义在于把 CUDA Graph 从 kernel launch 层面扩展到节点内通信层面，对 MPI-based HPC 和大模型 TP 通信都有启发。", "训练"),
    ("2508.15919", "HFX 是 production LLM serving 系统，联合优化请求调度和模型副本弹性伸缩以满足多样 SLO。核心是两级：scheduler 做 proactive budget estimation + 优先级保证新老请求 SLO 合规；elastic scaling 针对异构请求、变长 prompt、动态扩缩容决定何时起/停副本。定位类似 vLLM/SGLang 外围的 cluster-level serving 控制面，工程上把 single-task 静态调度升级成多 SLO 多任务。", "推理"),
    ("2604.22032", "Kernel Contracts 提出为 ML kernel 写正式合约的规约语言，8 部分：identifier/scope/precondition/postcondition/tolerance/reference oracle/measurement protocol/violation signature。针对「AMD matmul 梯度和 NVIDIA 不一致」「fused attention 静默下转累加器」「越界返零 vs 返垃圾」等跨硅片一致性灰色地带，给出可仲裁的形式产物。对昇腾/寒武纪/摩尔线程等国产芯片对齐 NVIDIA 语义尤其有用。", "推理"),
    ("2604.22050", "LayerBoost 是层感知的注意力简化方法：先对预训练模型做系统敏感度分析，识别对性能关键的 attention 层；对不敏感的层才替换为线性/混合注意力变体。思路是把「全局统一换线性注意力」的性能崩塌问题拆成「逐层条件替换」，避开大规模 retrain。对长序列推理/部署的 softmax 二次复杂度瓶颈是实用折中。", "推理"),
    ("2604.21952", "Focus Session 面向多模态基础模型给出硬件-软件协同加速方法论：transformer block 硬软协同设计 + 层次感知混合精度量化 + 结构化剪枝 MLP channel + 投机解码 + 小-大模型 cascading routing。把 MFM 压缩/部署的常见优化手段做系统性整合。工程价值在流程层面——部署一条龙而非单点技术。", "推理"),
]
for link_sub, tldr, tag in papers_specs:
    item = pick("papers", link_sub, tldr, tag)
    if item:
        curated["sections"]["papers"].append(item)

# ============ code ============
code_specs = [
    ("vllm/releases/tag/v0.20.0", "vLLM v0.20.0：752 commits / 320 贡献者的大版本。核心节点信号：(1) DeepSeek V4 初步支持（#40860），含 DSML token-leakage 修复、DSA+MTP IMA 修复、共享专家 silu clamp 限制；(2) PyPI 默认 CUDA wheel 切到 CUDA 13.0（CUDA 12.9 用户要加 --torch-backend=cu129）；(3) PyTorch 2.11 升级，XPU 同步 2.11；(4) 策略上 CUDA 版本跟随 PyTorch。本周最大底座迁徙节点。", "推理"),
    ("langgraph/releases/tag/1.1.10", "LangGraph 1.1.10 紧急 revert：昨天 1.1.9 加的 node-level timeouts（#7599）今天就被 revert（#7627）。同时带 prebuilt 1.0.12 和 checkpoint 4.0.3。昨日 prebuilt 1.0.11 刚 land 的 ToolNode 返回 list[Command | ToolMessage] 特性保留。典型的「feature 落地后 24h 内回滚」信号，说明 node-level timeout 实现细节存在坑。", "agent"),
    ("prebuilt%3D%3D1.0.12", "LangGraph prebuilt 1.0.12：关键修复是 ToolNode state hydration 通过 pregel helpers 从 channels 取值（#7594）。之前 ToolNode 拿 state 的方式绕开了 pregel 的 channel 机制，子图/嵌套场景下会读到过期数据。这种 agent 框架内部 state 同步路径的修复是 agent runtime 基础设施的核心。", "agent"),
    ("checkpoint%3D%3D4.0.3", "LangGraph checkpoint 4.0.3：复活 lc=2 JSON blob 对安全类型的反序列化支持，不强制 allowlist（#7582）。含义是旧版本写入的 checkpoint 能在新版本无感读取，降低 agent 长期运行状态的迁移成本。agent memory / 状态持久化工程细节。", "agent"),
    ("trunk%2F1b2c1d86899613bb95c1548c61a6bf5cdd1857c2", "PyTorch 修复 CUDA Graph 场景下 autograd 中陈旧 stream 引用的检测与修复。场景是图捕获后 stream 对象可能被释放但 autograd 仍持引用，引发 UAF/错流执行。对用 CUDA Graph 加速的训练/推理都是潜在崩溃点修复。", "推理"),
    ("trunk%2F9c3d517dd658453263fa75e99a2b808dd2447f93", "PyTorch Inductor 修复 compiler_bisector 测试：适配新的非 custom pre_grad passes，两个测试改用 CustomGraphPass（#181642）。这是 Inductor 新 pass 机制落地后的配套测试调整，反映 Inductor 编译流水线在持续演进。", "训练"),
]
for link_sub, tldr, tag in code_specs:
    item = pick("code", link_sub, tldr, tag)
    if item:
        curated["sections"]["code"].append(item)

# ============ community ============
community_specs = [
    ("1sx8uok", "Luce DFlash：单卡 RTX 3090 上的 GGUF 版 DFlash 投机解码，基于 ggml 的独立 C++/CUDA 栈，承载 Qwen3.6-27B。在 HumanEval/GSM8K/Math500 上平均 ~1.98x 相对 autoregressive，无需 retraining（z-lab 2026-04-26 发了匹配的 Qwen3.6-DFlash draft，AL 还在涨）。把投机解码的部署门槛压到单张消费卡 + CUDA 12+，对本地推理生态是实用节点。", "推理"),
    ("fast-sglang-starts", "SGLang 冷启动优化实战：70x 加速冷（ish）启动。博客复盘具体瓶颈点和优化手段，典型 serving-side 冷启动场景的工程经验。对 serverless LLM、短驻留推理实例是直接可借鉴的路径。", "推理"),
    ("anthropic-sdk-python/issues/1451", "Anthropic Python SDK issue #1451：Claude prompt-cache 的写入对紧接着的下一次请求可能不立即可见。这是分布式 prompt cache 的一致性缺陷，对高频 multi-turn agent / coding agent 场景影响大——以为命中了实际 miss。agent 基础设施侧需要据此做幂等/重试假设。", "agent"),
    ("lightport", "Lightport：开源 AI gateway（Portkey 的瘦身 fork），核心目标是把 80+ LLM provider 统一成 OpenAI-compatible 接口。去掉了 guardrails/billing 等上层特性，专注 provider 兼容层。MCP 生态相关项目（Glama 出品），tool use / function calling 在异构 provider 间的兼容性是 agent 系统基础设施的关键一环。", "agent"),
]
for link_sub, tldr, tag in community_specs:
    item = pick("community", link_sub, tldr, tag)
    if item:
        curated["sections"]["community"].append(item)

# blogs 今日无合格条目（两条都是营销/应用层）

OUT.write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")

# 统计
total = sum(len(v) for v in curated["sections"].values())
tag_count = {"推理": 0, "训练": 0, "agent": 0}
for section in curated["sections"].values():
    for item in section:
        tag_count[item["domain_tag"]] += 1
print(f"curated total: {total}")
for s, items in curated["sections"].items():
    print(f"  {s}: {len(items)}")
print(f"domain_tag: {tag_count}")
print(f"generated_at: {curated['generated_at']}")
print(f"raw     _at: {raw['generated_at']}")
