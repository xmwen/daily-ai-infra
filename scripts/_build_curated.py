"""
一次性脚本：读取 cache/today_raw.json，挑选并为每条写中文 tldr + domain_tag，
输出 cache/today_curated.json。确保 generated_at 比 raw 新。
"""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cache" / "today_raw.json"
OUT = ROOT / "cache" / "today_curated.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))


def pick(section_items, title_contains, tldr, domain_tag):
    for it in section_items:
        if title_contains in it["title"]:
            new = dict(it)
            new["tldr"] = tldr
            new["domain_tag"] = domain_tag
            return new
    return None


def pick_by_link(section_items, link_part, tldr, domain_tag):
    for it in section_items:
        if link_part in it["link"]:
            new = dict(it)
            new["tldr"] = tldr
            new["domain_tag"] = domain_tag
            return new
    return None


code = raw["sections"]["code"]
community = raw["sections"]["community"]

curated_code = []
curated_community = []

# --- code 分区 ---
# 1. PyTorch FakeTensor C++ 迁移（TensorImpl 扩展）
it = pick(code, "FakeTensor C++ Migration",
          "PyTorch 把 FakeTensorMode 下沉到 C++ TensorImpl：新增 fake_device_/fake_tensor_mode_ 与 is_fake() 接口，meta tensor 可原地变成 fake tensor，Dynamo/Inductor 追踪路径将摆脱 Python 层开销。",
          "训练")
if it: curated_code.append(it)

# 2. PyTorch 新增 nn.LinearCrossEntropyLoss（融合算子，显存/算力双省）
it = pick(code, "Add nn.LinearCrossEntropyLoss",
          "PyTorch 合入 nn.LinearCrossEntropyLoss 融合算子：线性投影+交叉熵一步算完，避免显式物化 [B,T,V] logits，LLM 训练末端 head 显存与带宽压力显著下降。",
          "训练")
if it: curated_code.append(it)

# 3. PyTorch CI 12.8 → 13.0 迁移（2.11 版本基建信号）
it = pick(code, "Migrate 12.8 CI jobs to 13.0",
          "PyTorch 把 CI 从 CUDA 12.8 全量切到 13.0，作为 2.11 稳定版的 1/2 步；意味着下一版 wheel 将默认 CUDA 13，下游 vLLM/SGLang 镜像需要同步升级。",
          "推理")
if it: curated_code.append(it)

# 4. PyTorch 重新启用 XPU workflows（Intel GPU 回归 CI）
it = pick(code, "Reenable XPU workflows",
          "PyTorch 恢复 XPU（Intel GPU）workflows，意味着 oneAPI/SYCL 后端重新进入主干 CI 保护，多硬件后端竞争格局继续维持。",
          "推理")
if it: curated_code.append(it)

# 5. FlashInfer nightly v0.6.9-20260425
it = pick(code, "Nightly Release v0.6.9-20260425",
          "FlashInfer v0.6.9 nightly 滚动发布：持续跟进 Blackwell SM120 融合 MoE、FP4 GEMM 与 routing_replay 等昨日已合入的大特性，供 vLLM/SGLang 拉取验证。",
          "推理")
if it: curated_code.append(it)

# 6. OpenAI Agents v0.14.6
it = pick(code, "v0.14.6",
          "OpenAI Agents Python SDK v0.14.6：放宽 websockets 版本上限至 <17、示例默认模型切到 GPT-5.5、新增 MongoDB session 文档，agent runtime 持续小步迭代。",
          "agent")
if it: curated_code.append(it)

# --- community 分区 ---
# 1. Qwen3.6-27B INT4 256k @ 5090 100tps
it = pick(community, "Qwen3.6-27B-INT4 clocking 100 tps",
          "Qwen3.6-27B INT4 (AutoRound) 在单卡 5090 上通过 vLLM 0.19 跑出 100+ tps 的 TG 吞吐，并能吃下原生 256k 上下文；MTP 推测解码 + 小权重，是当前单卡推理性价比新标杆。",
          "推理")
if it: curated_community.append(it)

# 2. DeepSeek-V4 KV cache 明细 vs vLLM
it = pick(community, "exact KV cache usage of DeepSeek V4",
          "社区根据 vLLM 官方 blog 推算 DSV4 在 1M 上下文下 KV cache 仅 6.72 GiB（Flash）/9.62 GiB（Pro），较 V3.2 省约 7.9×；KV 占比降到 0.3%，几乎抹平 Transformer-SSM 混合架构的显存优势。",
          "推理")
if it: curated_community.append(it)

# 3. lmsys: SGLang × Miles — DSV4 Day0 推理+Verified RL
it = pick(community, "DeepSeek-V4 on Day 0: From Fast Inference to Verified RL",
          "lmsys 放出 SGLang+Miles 对 DSV4 的 Day0 支持：推理侧接入新 MLA/稀疏 MoE 路由，并打通 Verified RL 训练回路；开源栈首个端到端跑通 DSV4 inference+post-training 的方案。",
          "推理")
if it: curated_community.append(it)

# 4. AutoMuon: Muon optimizer 一行替换 AdamW
it = pick(community, "Introducing AutoMuon",
          "AutoMuon 封装 Muon 优化器为 AdamW 的一行替换：自动识别 2D 权重矩阵用 Muon、embedding/norm/bias 仍走 AdamW，降低 Muon 在任意 PyTorch pipeline 的落地门槛。",
          "训练")
if it: curated_community.append(it)

# 5. Routiium tool_result_guard（agent infra 安全）
it = pick(community, "Routiium",
          "Routiium 是自托管 OpenAI 兼容 LLM 网关，核心亮点是 tool_result_guard：把 MCP/web-fetch/shell 返回内容独立扫一遍，防止 prompt injection 从工具返回通道污染模型上下文——补上 agent runtime 的经典缺口。",
          "agent")
if it: curated_community.append(it)

# 6. MCP Spine 中间件代理
it = pick(community, "MCP Spine",
          "MCP Spine 是 LLM tool call 的中间件代理，面向 agent 场景做安全校验与 token 额度控制；当 MCP server 直接暴露给模型不安全时，这种网关式拦截层正在成为工程刚需。",
          "agent")
if it: curated_community.append(it)

# 7. Nemotron 3 Nano 混合 Mamba+MoE 微调讨论
it = pick(community, "Nemotron 3 Nano",
          "讨论：Nemotron 3 Nano（23 Mamba-2 + 23 MoE + 6 GQA 混合架构）下 LoRA 该怎么贴——不同层类型权重形状迥异，标准 LoRA recipe 需拆分处理，是混合架构训练工程化的新挑战。",
          "训练")
if it: curated_community.append(it)


# 保留空的 papers / blogs 分区
curated = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "lookback_hours": raw.get("lookback_hours", 36),
    "source": "today_curated.json",
    "sections": {
        "papers": [],
        "code": curated_code,
        "blogs": [],
        "community": curated_community,
    },
}

OUT.write_text(
    json.dumps(curated, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 统计
total = sum(len(v) for v in curated["sections"].values())
by_section = {k: len(v) for k, v in curated["sections"].items()}
by_tag = {"推理": 0, "训练": 0, "agent": 0}
for sec in curated["sections"].values():
    for it in sec:
        by_tag[it["domain_tag"]] = by_tag.get(it["domain_tag"], 0) + 1

print(f"curated total: {total}")
print(f"by section: {by_section}")
print(f"by domain_tag: {by_tag}")
print(f"generated_at: {curated['generated_at']}")
print(f"raw generated_at: {raw['generated_at']}")
