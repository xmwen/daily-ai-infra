# -*- coding: utf-8 -*-
"""一次性脚本：根据 today_raw.json 生成 today_curated.json（中文 tldr + domain_tag）。"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "cache" / "today_raw.json"
OUT_PATH = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))


def find(section, key_in_title):
    items = raw["sections"].get(section, [])
    for it in items:
        if key_in_title.lower() in it["title"].lower():
            return dict(it)
    raise KeyError(f"{section}: {key_in_title} not found")


def find_link(section, link_substr):
    items = raw["sections"].get(section, [])
    for it in items:
        if link_substr in it["link"]:
            return dict(it)
    raise KeyError(f"{section}: link contains {link_substr} not found")


curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw["lookback_hours"],
    "sections": {"papers": [], "code": [], "blogs": [], "community": []},
    "fetch_stats": raw.get("fetch_stats", {}),
    "source": "today_curated.json",
}

# ---------------- Papers ----------------
p_modeswitch = find_link("papers", "2605.23057")
p_modeswitch["tldr"] = (
    "ModeSwitch-LLM 在单 A100 上做请求边界级模式切换控制器：用廉价工作负载特征（输入长度、batch、prefix 命中率）"
    "把每个请求路由到 FP16 / GPTQ+prefix cache / INT8+continuous batching / speculative decoding 等固定模式。"
    "Llama-3.1-8B 上相对 FP16 取得 2.10× 平均时延加速、每 token 能耗降 51.7%。意义在于把"
    "「单一 serving 配置」证伪：不同请求适合不同执行模式，工程化的离线 profile + 在线轻量路由比追求一个万能模式更有性价比。"
)
p_modeswitch["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_modeswitch)

p_aligned = find_link("papers", "2605.23389")
p_aligned["tldr"] = (
    "AlignedServe 提出 prefix-aware batching：把 KV cache 长度相近的请求归到同一个 decode batch，"
    "缓解 iteration 内部的「长 KV 拖慢短 KV」气泡（同一 step 里长 KV token 成为瓶颈，迫使整个 batch 等待）。"
    "为了支撑这个策略，用大 CPU 内存维持足够的 in-flight 请求池来做长度匹配。"
    "是 continuous batching 之后的下一层细化：从 request-level → iteration-level bubble 治理。"
)
p_aligned["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_aligned)

p_object = find_link("papers", "2605.22850")
p_object["tldr"] = (
    "ObjectCache 把 prefix KV cache 直接放到 S3 兼容对象存储里：协议侧让 storage server 按 GPU 真实消费顺序"
    "流式投递 KV，传输调度与 attention 计算重叠以保 TTFT 不退化。意义是给「prefix cache 容量被远程 DRAM 池限制」"
    "提供新解：用对象存储的近无限容量换 cluster 缩容，前提是协议改造让顺序投递成为可能，"
    "代价从 DRAM 池规模转嫁到对象存储 IO 调度复杂度。"
)
p_object["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_object)

p_fk = find_link("papers", "2605.23215")
p_fk["tldr"] = (
    "FastKernels 是面向 LLM kernel 生成 agent 的新基准：直接对接 vLLM/SGLang 真实编译栈，"
    "用 46 个生产代表性 kernel 评测，揭示既有基准的奖励信号「在沙盒里好看、集成进真实系统就编译失败/接口不兼容/静默精度退化」。"
    "延续看板上 KernelBenchX→Hawkeye→Silent Hyperparameter→Dooly 的"
    "「LLM 生成 kernel 难复现/难落地」母题，把基准本身的 production fidelity 作为 LLM-as-kernel-author 的正名前提。"
)
p_fk["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_fk)

p_ams = find_link("papers", "2605.23200")
p_ams["tldr"] = (
    "AMS KV Compression 指出现有 token-importance + 全局 Top-k 驱逐策略会触发 Region Wipe-out："
    "连续推理段被整段清掉、逻辑断裂。它把范式从 token-level 竞争换成 region-aware quota：按 attention mass 空间分布"
    "自适应分区，结构上重要的推理片段获得保底配额。是长上下文 reasoning 场景下 KV 压缩的下一步：从打分驱逐转向区域配额。"
)
p_ams["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_ams)

p_dcc = find_link("papers", "2511.15503")
p_dcc["tldr"] = (
    "DCC 是面向 PIM（存内计算）的 ML kernel 编译框架，正式定型 v2 替换稿。核心矛盾："
    "Host CPU 要求元素跨 DRAM bank 分布、PIM 核要求元素本地连续，跨设备数据重排成性能 + 编程性双瓶颈。"
    "DCC 用数据中心化的 IR 系统化处理多 PIM 设备 + 多 ML kernel 的重排优化。延续 ScaleUp 统一内存母题，"
    "PIM 编译栈正在补齐「多目标后端 + 数据布局自动化」的工程缺口。"
)
p_dcc["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_dcc)

p_hpmoe = find_link("papers", "2605.23764")
p_hpmoe["tldr"] = (
    "HyperParallel-MoE 针对昇腾 NPU 上的 MoE 训练，把「逐 kernel 串行执行」改成 tile 级异构 taskflow："
    "AIC（矩阵）+ AIV（向量）跨队列同步，AIV 侧做 driving，调度器编译期静态分配，"
    "把昇腾片上异构资源打满。意义是国产芯片的 MoE 训练栈在补齐编译 + 调度自动化缺口，"
    "对标 NV 上 Megatron HybridEP 的多流编排。是看板「国产芯片训练栈」线索的新数据点。"
)
p_hpmoe["domain_tag"] = "训练"
curated["sections"]["papers"].append(p_hpmoe)

p_zipmoe = find_link("papers", "2601.21198")
p_zipmoe["tldr"] = (
    "ZipMoE 在边缘设备上做 MoE 无损部署：联合设计无损压缩 + cache-affinity 调度，"
    "把 on-device MoE 推理从 IO-bound 翻转成 compute-centric。前提是「不能用有损量化保留模型行为」的场景"
    "（比如对模型行为有合规/精度要求的边缘端）。延续看板边缘 MoE 部署线索，与 NASiC 3D NAND CIM 互为软硬两路解。"
)
p_zipmoe["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_zipmoe)

p_nasic = find_link("papers", "2605.23294")
p_nasic["tldr"] = (
    "NASiC 是 3D NAND-based CAM-Selected 多比特 CIM 架构，针对边缘 MoE LLM 推理。"
    "核心把 3D NAND 的高存储密度与 CAM 的内容寻址结合：CAM 选中目标 expert 后再走多比特 CIM 计算，"
    "解决「3D NAND 适合大容量但不擅长 MoE 动态稀疏激活、多比特存储利用率低」的硬件错配。"
    "和 ZipMoE 的软件路径形成存内 MoE 推理的双线推进。"
)
p_nasic["domain_tag"] = "推理"
curated["sections"]["papers"].append(p_nasic)

# ---------------- Code ----------------
c_tile = find("code", "v0.1.10")
c_tile["tldr"] = (
    "TileLang v0.1.10：AMD 全面铺开（RDNA3/3.5 WMMA、gfx950/CDNA4 copy.async、160K LDS、LDS transpose、"
    "INT8 MFMA、MXFP4 E2M1、gfx1151）；Blackwell 上 MXFP8 block-scaled GEMM、FP4 TensorMap TMA、"
    "TMA gather4/scatter4、T.copy_cluster（SM-to-SM cluster copy）；同时补 SM75 MMA GEMM（FP16/INT8/INT4）"
    "和 Metal simdgroup_matrix MMA。autotuner 加入 pipelined / grouped 编译 + 多 GPU benchmarking。"
    "意义是 TileLang 正式从「CUDA 优先」转向「跨 NV/AMD/Apple 三栈统一 tile DSL」，对标 Triton 的多后端定位。"
)
c_tile["domain_tag"] = "推理"
curated["sections"]["code"].append(c_tile)

# ---------------- Community ----------------
co_minicpm = find("community", "MiniCPM-V 4.6 on Orange Pi")
co_minicpm["tldr"] = (
    "开发者从零写 C++ 推理引擎，在 Orange Pi AIPro（昇腾 310B NPU，20 TOPS INT8 / 10 TFLOPS FP16，$149）"
    "跑 MiniCPM-V 4.6，绕开标准框架栈的开销。重点是定制 op + Gradio Web UI 全开源。"
    "是国产边缘 NPU 推理生态的实战数据点：在标准框架性能不达标时，自写引擎 + 定制 kernel 仍是可行路径，"
    "和今天 NASiC/ZipMoE 的边缘 MoE 推理硬件研究互为现实落地侧应。"
)
co_minicpm["domain_tag"] = "推理"
curated["sections"]["community"].append(co_minicpm)

co_oscar = find("community", "OSCAR RotationZoo")
co_oscar["tldr"] = (
    "OSCAR 是 INT2 KV cache 量化方案：在小校准集上抓 Q/K/V 激活，离线估计 attention-aware K/V 协方差，"
    "推导每层正交旋转矩阵，让 INT2 量化方向对齐 attention 实际消费方向。结果是 ~7× KV cache 压缩。"
    "意义是 KV cache 量化路线从「直接 INT4/FP8」往「2-bit + 旋转对齐」推进，"
    "和 AMS region-aware quota 形成 KV 内存治理的两路：要么压更狠（OSCAR），要么按区域配额（AMS）。"
    "RotationZoo 提供预算好的 K/V 旋转矩阵开箱可用。"
)
co_oscar["domain_tag"] = "推理"
curated["sections"]["community"].append(co_oscar)

co_dsv4 = find("community", "DeepSeek-V4 KV Cache Explained")
co_dsv4["tldr"] = (
    "DeepSeek-V4 KV cache 在 1M context 下显存占用反而比短上下文方案更省的工程拆解："
    "围绕 SWA + 稀疏注意力混合架构（LAYER_TYPE_SWAONLY/C4A/C128A 三层）和 compressed attention 做 KV 大幅压缩，"
    "把 KV 增长曲线从线性变成接近常数。是看板长期跟踪的 V4 KV 母题，"
    "今天这篇是社区第一篇相对完整的工程级解释，对接此前 lmsys×SGLang Day0 部署、Qwen3.6 NVFP4+MTP 长上下文的实测线。"
)
co_dsv4["domain_tag"] = "推理"
curated["sections"]["community"].append(co_dsv4)

co_ssv = find("community", "SSV: Sparse Speculative Verification")
co_ssv["tldr"] = (
    "SSV（Sparse Speculative Verification）：把投机解码的 verification 阶段做稀疏化——"
    "不必每个 draft token 都用全 attention 跑 target 模型验证，可基于 attention 稀疏性裁剪验证开销。"
    "延续看板上 5/12 SPECTRE → 5/14 PipeSD → 5/15 ECHO → 5/20 SpecSA → 5/21 NanoCP 的"
    "「投机解码 × 稀疏 attention」母题：稀疏化不仅是推理本体的解药，也是投机验证 compute 爆炸的解药。"
)
co_ssv["domain_tag"] = "推理"
curated["sections"]["community"].append(co_ssv)

co_qwen36 = find("community", "Qwen 3.6 benchmarks on 2x RTX PRO 6000")
co_qwen36["tldr"] = (
    "Qwen 3.6 在 2× RTX PRO 6000 上的 vLLM stable benchmark 实测："
    "27B BF16 关 MTP @ batch 64 → 1600 tps；MTP=2 @ batch 64 → 1800 tps；"
    "35B BF16 关 MTP @ batch 64 → 2700 tps、batch 128 → 3500 tps（prompt processing 30k tps）。"
    "数据点价值在于两张 RTX PRO 6000（96GB 显存）成为 Qwen3.6 27B/35B 中等并发的现实部署选项，"
    "MTP 在 27B 上有提升但 35B 关闭 MTP 反而吞吐更好——MTP 工程化曲线进入边界期延续。"
)
co_qwen36["domain_tag"] = "推理"
curated["sections"]["community"].append(co_qwen36)

co_v100 = find("community", "1000 tps generation on Qwen3.6 27B with V100s")
co_v100["tldr"] = (
    "用多张 V100 跑 Qwen3.6 27B，128 并发场景做到 1000+ tps 总吞吐；单用户 batch=1 约 80 t/s 生成 + 3000 t/s prompt processing，"
    "且没开 MTP。意义是 V100（无 BF16、无 FP8、无 TMA）依然能扛 27B 推理生产，"
    "对中小团队的「老卡复用」场景给了一个相对硬数据：旧 SM70 + 充分并发 ≈ 中等吞吐部署。"
    "和上面 RTX PRO 6000 一起，构成本周 Qwen3.6 部署的「新卡 vs 旧卡」实测两极。"
)
co_v100["domain_tag"] = "推理"
curated["sections"]["community"].append(co_v100)

co_llcp = find("community", "server: fix checkpoints creation")
co_llcp["tldr"] = (
    "llama.cpp PR #22929 修复 server 模式下 checkpoint 创建问题。"
    "背景：coding agent（如 opencode）会主动改写 conversation history 来「优化上下文」，"
    "结果 llama.cpp 不得不从修改点重新 prefill，最坏情况下整段 70k token 全部重算（出现 \"forcing full prompt re-processing...\"）。"
    "PR 让 server 在历史被改写时正确保留 checkpoint，避免全量 reprefill。"
    "意义是 coding agent 与本地推理 backend 的耦合点（context 改写 vs prefix cache 保活）正在产生工程化适配，"
    "属于 agent infra 与 serving 层契约协议成型的早期信号。"
)
co_llcp["domain_tag"] = "agent"
curated["sections"]["community"].append(co_llcp)

# ---------------- 写出 ----------------
OUT_PATH.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 打印统计
counts = {k: len(v) for k, v in curated["sections"].items()}
tags = {"推理": 0, "训练": 0, "agent": 0}
missing_tag = 0
for sec in curated["sections"].values():
    for it in sec:
        t = it.get("domain_tag")
        if t in tags:
            tags[t] += 1
        else:
            missing_tag += 1
total = sum(counts.values())
print(f"curated total: {total}")
print(f"  papers={counts['papers']} code={counts['code']} blogs={counts['blogs']} community={counts['community']}")
print(f"  tags: 推理={tags['推理']} 训练={tags['训练']} agent={tags['agent']} (missing={missing_tag})")
print(f"  generated_at: {curated['generated_at']}")
print(f"  raw generated_at: {raw['generated_at']}")
print(f"saved -> {OUT_PATH}")
