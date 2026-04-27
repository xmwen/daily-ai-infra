# -*- coding: utf-8 -*-
"""
一次性中文策展脚本：读取 cache/today_raw.json，按筛选偏好挑条目，
为每条补 tldr（≤80 字中文）+ domain_tag（推理/训练/agent），
输出到 cache/today_curated.json。用 json.dump(ensure_ascii=False) 避免转义坑。
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))

def find(section, key_in_title):
    """按 title 关键字精确定位 raw 中的原始条目。"""
    for item in raw["sections"].get(section, []):
        if key_in_title.lower() in item["title"].lower():
            return item
    return None

def find_link(section, link_part):
    for item in raw["sections"].get(section, []):
        if link_part in item["link"]:
            return item
    return None

def enrich(item, tldr, tag):
    if item is None:
        return None
    new = dict(item)
    new["tldr"] = tldr
    new["domain_tag"] = tag
    return new

curated = {"papers": [], "code": [], "blogs": [], "community": []}

# =============== papers ===============
# 1. GVR Top-K Blackwell（cs.DC/cs.AR/cs.PF 三份同文，取一份即可，偏好 cs.DC）
gvr = find("papers", "Guess-Verify-Refine")
curated["papers"].append(enrich(
    gvr,
    "NVIDIA Blackwell 上的 data-aware 精确 Top-K：利用连续 decode 步之间的时间相关性做预测，1-2 轮全局扫描定阈值+ballot-free 收集，专治 sparse-attention decoding 里 Top-K 这段 serving 延迟瓶颈。",
    "推理",
))

# 2. GICC GPU-initiated communication
curated["papers"].append(enrich(
    find("papers", "GICC"),
    "GPU kernel 直接驱动跨节点通信的 runtime：针对 Slingshot OFI（Top500 前三都在用）给出 bounded NIC 工作回收机制，消除 host-driven 进度和 IB 路径上的多余锁，降 launch 开销+提高 compute/communication overlap。",
    "训练",
))

# 3. HFX multi-SLO serving
curated["papers"].append(enrich(
    find("papers", "HFX"),
    "生产级 LLM serving 系统：把请求调度和副本弹性扩缩联合优化，按 SLO 做主动预算估计+优先级排队，同时处理异构请求/变长 prompt/弹性伸缩，主打多任务/多 SLO 场景。",
    "推理",
))

# 4. Kernel Contracts 规约语言
curated["papers"].append(enrich(
    find("papers", "Kernel Contracts"),
    "给 ML kernel 写「合约」的规约语言：8 段式（scope/前后置/容差/reference oracle/测量协议/违约签名）形式化描述算子语义，专治跨 AMD/NVIDIA/Ascend 同算子结果不一致时没有仲裁依据的问题。",
    "推理",
))

# 5. LayerBoost layer-aware attention
curated["papers"].append(enrich(
    find("papers", "LayerBoost"),
    "层感知的 attention 替换：先做敏感度分析找出对性能关键的层，只对不敏感层替换成线性/混合 attention，避免整模型一刀切 linear 化导致的精度大跌或需要大规模重训。",
    "推理",
))

# 6. FlashSpread Triton fused kernel（仿真用但 Triton kernel fusion 工程价值高）
curated["papers"].append(enrich(
    find("papers", "FlashSpread"),
    "把 non-Markov 传染病模拟整条 pipeline（CSR 遍历+erfcx hazard+Bernoulli tau-leaping+状态转移+下一步感染力回写）融进单个 Triton kernel，全部中间量驻留 SM 寄存器+保 CUDA Graph 捕获，属于 Triton fused-kernel 工程范式的好案例。",
    "推理",
))

# 7. UCX+CUDA Graphs multi-path intra-node
curated["papers"].append(enrich(
    find("papers", "Multi-Path Transfers with CUDA Graphs"),
    "把 CUDA Graphs 集成进 UCX：节点内 NVLink+PCIe 多路径 GPU-GPU 点对点通信用 CUDA Graph 统一调度，显著降通信开销，号称首个把 CUDA Graph 无缝接入 UCX 的工作。",
    "训练",
))

# 8. Focus Session MFM 硬软协同加速（综合性但覆盖量化+推测解码+模型级联，工程落地类）
curated["papers"].append(enrich(
    find("papers", "Focus Session: Hardware and Software"),
    "多模态基础模型硬软协同加速方法学综述：transformer block 硬软协设计+hierarchy-aware 混精度量化+结构化剪枝+speculative decoding+model cascading 路由，是一份系统性的 MFM 推理优化工程清单。",
    "推理",
))

# =============== code ===============
# 1. vLLM v0.20.0（当日最重磅，必须进）
curated["code"].append(enrich(
    find("code", "v0.20.0") or find_link("code", "vllm-project/vllm/releases/tag/v0.20.0"),
    "vLLM v0.20.0：752 commits/320 贡献者。CUDA 13.0 成默认（跟 PyTorch 2.11 同步），XPU 也升到 torch 2.11，新增 Python 3.14 支持，跑 HuggingFace Transformers v5。AI Infra 大版本号大迁徙信号。",
    "推理",
))

# 2. vLLM v0.20.1rc0 - OpenAI system_fingerprint（小补丁，skip）
# 3. FlashInfer nightly 空 body（skip）

# 4. PyTorch combo kernel flop metadata（今天真正 landed，昨日是 revert+fix，今天延续）
curated["code"].append(enrich(
    find("code", "combo kernels"),
    "Inductor combo kernel 现在也能把 kernel_num_gb/kernel_flop 带进 inductor_meta：在 benchmark_kernel/profile_bandwidth 开启时，对每个 sub-kernel 调 estimate_kernel_num_bytes/estimate_flops 汇总。此前 combo kernel 在 profiler 和 autotune 带宽日志里没这俩字段。",
    "训练",
))

# 5. PyTorch Revert nn.linear_cross_entropy（昨天刚聊过融合算子新增，今天被 autorevert，延续价值高）
curated["code"].append(enrich(
    find("code", "Revert \"Add naive nn.linear_cross_entropy"),
    "PyTorch 昨日新增的 nn.linear_cross_entropy 融合算子（LLM head 省显存+带宽）今天被 autorevert。意味着这个高关注度算子还需要一轮修复才能重新 land，值得追踪它的下一次 PR。",
    "训练",
))

# 6. PyTorch cu132→cu130 Dockerfile fallback 移除
curated["code"].append(enrich(
    find("code", "cu132->cu130"),
    "PyTorch Dockerfile 删掉 cu132→cu130 的 wheel 回退：CUDA 13.2 nightly 已于 2026-04-20 上架，之前留的临时 fallback 反而让 cuda13.2 镜像装上了 cu130 wheel，导致 smoke_test 报版本不匹配。CUDA 13.x 版本线逐步稳定。",
    "训练",
))

# 7. PyTorch AOTI c_shim v2 for SDPA math（2 份 trunk/viable 重复，取一份）
curated["code"].append(enrich(
    find("code", "BC-safe c_shim v2 for _scaled_dot_product_attention_math") or find_link("code", "22790c5da3d534b53281c0866537154a47b6a1cf"),
    "PyTorch AOTI 给 _scaled_dot_product_attention_math_for_cpu 加 BC-safe c_shim v2：AOTI 生成的 C++ 产物升级到 v2 ABI 后，math SDPA fallback 也有了向后兼容的 C shim，保证 AOTI 编译出的模型跨版本运行时链接稳定。",
    "推理",
))

# 8. PyTorch mimalloc 2.3.0 升级（工程影响面小，但并发 bugfix，收一条）
# 其实昨日 3.0 线路无此，skip 降噪

# 9. PyTorch Inductor materialization heuristic（title 被截断，内容少，skip 降噪）

# =============== blogs ===============
# blogs 今日 0 条，周一常态

# =============== community ===============
# 1. Skymizer HTX301（6 颗 HTX301+384GB，240W 跑 700B decode，prefill 给 GPU）
curated["community"].append(enrich(
    find("community", "Skymizer"),
    "Skymizer HTX301：单 PCIe 卡 6 颗芯片+384GB 内存，240W 本地跑 700B decode，prefill 继续丢给 GPU 做计算密集段、HTX301 专攻带宽密集的 decode 阶段——prefill/decode 分芯设计的又一具象落地，6 月 Computex 见真章。",
    "推理",
))

# 2. AMD Hipfire 新推理引擎（AMD GPU 专用、mq4 量化）
curated["community"].append(enrich(
    find("community", "AMD Hipfire"),
    "AMD Hipfire：社区新出的面向全系 AMD GPU 的推理引擎（非官方），自研 mq4 量化格式，Localmaxxing benchmark 显示对 RDNA3 有明显加速。ROCm 生态里罕见的社区向推理栈补充。",
    "推理",
))

# 3. 16GB+6GB 旧卡混插跑 30B 稠密模型（实用 infra trick，工程向）
curated["community"].append(enrich(
    find("community", "plug in your old GPU"),
    "消费级多卡 infra trick：5070 Ti 16GB + 2060 6GB 混插跑 30B 稠密模型。重点是双卡都必须放 VRAM（哪怕第二张弱 PCIe x4），llama-server 分层映射即可，揭示个人工作站「凑 VRAM」比「对称双卡」更实用。",
    "推理",
))

# 4. AMD Alveo V80 FPGA 推理猜想（虽是 speculation，但 FPGA+LLM 硬件路线讨论有信号价值）
# 权衡：Taalas HC1 是 LLM-burn-onto-chip 的代表性路线，FPGA 模拟这个方向的讨论对推理硬件路线图有参考价值
curated["community"].append(enrich(
    find("community", "Alveo V80"),
    "社区讨论用 AMD Alveo V80 FPGA（~9500 美元）模拟 Taalas HC1「LLM 烧进芯片」思路：Gemini 预估用 speculative decoding 架构跑 Qwen3.5-4B Q4 可达 3200 tk/s、9B ≈1400 tk/s。LLM 专用硬件/FPGA 推理路线的持续探讨。",
    "推理",
))

# 其余 r/ML 的 RAG 吐槽、PhD 申请、SWE-Bench benchmaxx、Claude 梗图、Manus 审查、abliteration 抄袭、INT8>FP16 疑问、Grok3 等—— 都属排除项（应用/商业/评测/meta-讨论），不收

# ============== 输出 ==============
out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "source_raw_generated_at": raw["generated_at"],
    "sections": curated,
}

# 过滤 None（万一 find 没命中）
for sec in out["sections"]:
    out["sections"][sec] = [x for x in out["sections"][sec] if x is not None]

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

# 统计
total = sum(len(v) for v in out["sections"].values())
tag_dist = {"推理": 0, "训练": 0, "agent": 0}
for sec in out["sections"].values():
    for item in sec:
        tag_dist[item["domain_tag"]] = tag_dist.get(item["domain_tag"], 0) + 1

print(f"[curated] 共 {total} 条")
for sec, items in out["sections"].items():
    print(f"  {sec}: {len(items)}")
print(f"[tags] 推理 {tag_dist['推理']} / 训练 {tag_dist['训练']} / agent {tag_dist['agent']}")
print(f"[generated_at] raw={raw['generated_at']}  curated={out['generated_at']}")
