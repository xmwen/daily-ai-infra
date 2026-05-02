# 自动化执行历史 - 每日 LLM 推理与训练动态看板

## 2026-04-22 22:00（执行于 19:16）
- fetch: 68 条原始 item（papers 32 / code 15 / blogs 5 / community 16）
- render: 筛出 13 条卡片，输出 `2026/04/2026-04-22.html`
- publish: 成功推送 origin/main，GitHub Pages 已刷新
- 结果 URL: https://xmwen.github.io/daily-ai-infra/
- 状态: ✅ 正常（但那次是中文摘要固化前，HTML 实际是英文 raw fallback）

## 2026-04-22 22:00（执行于 20:34，新 prompt 首跑）
- fetch: 69 条 raw（papers 32 / code 17 / blogs 4 / community 16），无 RSS 源失败
- curated: 17 条中文 tldr（papers 5 / code 6 / blogs 1 / community 5），generated_at 比 raw 新
- render: `LLM 摘要 ✓` 徽章存在，无 fallback，source=today_curated.json
- publish: commit `975bcb4`，HEAD==origin/main，`git log -1 --stat` 含今日两份 HTML（各 267 行 diff）
- 结果 URL: https://xmwen.github.io/daily-ai-infra/
- 状态: ✅ 成功（真正中文 curated 首次完整落地）

## 2026-04-22 22:00（执行于 21:09，domain_tag 版 prompt 第 2 跑）
- fetch: 88 条 raw（papers 32 / code 16 / blogs 3 / community 37），无 RSS 源失败
- curated: 20 条（papers 6 / code 6 / blogs 1 / community 7），domain_tag 分布 推理 9 / 训练 4 / agent 7
- render: `LLM 摘要 ✓`，无 fallback
- publish: commit `04b4ee7`，HEAD==origin/main，HTML diff 208 行 × 2
- 状态: ✅ 成功。用一次性脚本 `scripts/_build_curated.py` 生成 curated，中文引号用「」避开双引号陷阱

## 2026-04-22 22:00（执行于 22:00，domain_tag 版 prompt 第 3 跑）
- fetch: 70 条 raw（papers 32 / code 16 / blogs 3 / community 19），无 RSS 源失败
- curated: 19 条（papers 7 / code 8 / blogs 1 / community 3），domain_tag 分布 推理 10 / 训练 3 / agent 6
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳 22 处
- publish: commit `e48a9ae`，HEAD==origin/main，HTML diff 231 行 × 2
- 状态: ✅ 成功。agent 方向命中较多（ARGUS GPU agent、UniEP MoE EP、ReasoningBank agent memory、LangGraph fix、OpenAI Agents sandbox、harness mismatch 讨论）

## 2026-04-23 22:00（domain_tag 版 prompt 第 4 跑）
- 前置：python shim 指向 3.13.12 但只有 `.installing.*` 目录，用 install_binary 重装 3.13.12 后恢复
- fetch: 97 条 raw（papers 36 / code 16 / blogs 5 / community 40），无 RSS 源失败
- curated: 19 条（papers 6 / code 8 / blogs 1 / community 4），domain_tag 分布 推理 12 / 训练 4 / agent 3
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳正常
- publish: commit `872ae56`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +571 行
- 亮点：FASER 动态投机解码、PayPal EAGLE3 H100 benchmark、Super Apriel 多 mixer supernet、Megatron 26.04-alpha HybridEP+a2a 高优先级流、PyTorch _FastCudaLauncher、DeepEP V2+TileKernels、OpenAI Agents v0.14.5 Modal sandbox timeout
- 状态: ✅ 成功

## 2026-04-25 22:00（周六跑）
- fetch: 36 条 raw（papers 0 / code 14 / blogs 2 / community 20），无 RSS 源失败；papers 0 条是周六 arXiv 不更新
- curated: 12 条（papers 0 / code 9 / blogs 1 / community 2），domain_tag 分布 推理 5 / 训练 5 / agent 2
- render: `LLM 摘要 ✓`，无 fallback，14 处 CST 时间戳
- publish: commit `f89fa68`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +420 行
- 亮点：FlashInfer v0.6.9 SM120 Blackwell fused MoE+FP4 GEMM+routing_replay、LangGraph prebuilt 1.0.11 ToolNode 返回 Command+ToolMessage、OpenAI Agents v0.14.6、PyTorch Inductor combo kernel 迭代（revert+fix）、PyTorch ROCm FlexAttention target-dependent forward config、PGNCCL×SymmetricMemory×IntraNodeComm 测试参数化、NVIDIA DeepSeek-V4 Blackwell 部署、Qwen3.6-27B NVFP4+MTP vLLM 0.19 单卡 5090 80tps@218k
- 状态: ✅ 成功。周末条数天然少，严格执行「宁缺毋滥」，排除大量水贴/商业讨论/AGI 梗图

## 2026-04-26 22:00（周日跑）
- fetch: 41 条 raw（papers 0 / code 12 / blogs 0 / community 29），无 RSS 源失败；周日 papers+blogs 双 0 是常态
- curated: 13 条（papers 0 / code 6 / blogs 0 / community 7），domain_tag 分布 推理 6 / 训练 4 / agent 3
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳正常
- publish: commit `001d722`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +459 行
- 亮点：Qwen3.6-27B INT4 单卡 5090 100+ tps + 256k ctx、DSV4 KV cache 1M ctx 0.3% 占比（vs V3.2 降 7.9×）、lmsys×SGLang×Miles DSV4 Day0 推理+Verified RL、PyTorch FakeTensor C++ 迁移到 TensorImpl、PyTorch nn.LinearCrossEntropyLoss 融合算子、PyTorch CI CUDA 12.8→13.0、AutoMuon 一行替换 AdamW、Routiium tool_result_guard 防 tool-return prompt injection、Nemotron 3 Nano 混合 Mamba+MoE LoRA 讨论
- 状态: ✅ 成功。周日水贴比例高，严格排除 paper-lantern bench/VLA 综述/金融应用/rebuttal 投诉/abliteration 抄袭事件等应用层内容

## 2026-04-27 22:00（周一跑）
- fetch: 67 条 raw（papers 34 / code 13 / blogs 0 / community 20），无 RSS 源失败；周一 blogs 0 常态（周末没人发博客）
- curated: 17 条（papers 8 / code 5 / blogs 0 / community 4），domain_tag 分布 推理 12 / 训练 5 / agent 0
- render: `LLM 摘要 ✓`，无 fallback，20 处 CST 时间戳
- publish: commit `efac95a`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +534 行
- 亮点：**vLLM v0.20.0**（CUDA 13 默认+PyTorch 2.11+Python 3.14+Transformers v5 全栈大迁徙，752 commits）、GVR Blackwell sparse-attention data-aware Top-K、GICC GPU-initiated Slingshot 通信 runtime、HFX multi-SLO serving、Kernel Contracts 跨硅片规约语言、LayerBoost 层感知 attention 替换、FlashSpread Triton 单 kernel 融合、UCX+CUDA Graphs multi-path intra-node、PyTorch nn.linear_cross_entropy 被 autorevert（昨日刚 land 今日打回）、Skymizer HTX301 prefill/decode 分芯卡 6 芯片×64GB=384GB@240W 跑 700B、AMD Hipfire 社区 ROCm 推理引擎
- agent 方向 0 条：今日 LangGraph/AutoGen/OpenAI Agents/MCP/XGrammar/Outlines 全部无 release，HN Agent infra 也无有效信号，严格执行「宁缺毋滥」不塞应用层凑数
- 状态: ✅ 成功。vLLM v0.20.0 是本周最重要节点信号

## 2026-04-28 22:00（周二跑）
- fetch: 92 条 raw（papers 34 / code 16 / blogs 2 / community 40），无 RSS 源失败
- curated: 18 条（papers 8 / code 6 / blogs 0 / community 4），domain_tag 分布 推理 10 / 训练 3 / agent 5
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳正常
- publish: commit `be5360a`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +553 行
- 亮点：arXiv 一批新 paper 集中爆发——**GVR**（Blackwell data-aware 精确 Top-K 稀疏注意力 decode，利用时序相关性 secant 式收敛）、**GICC**（Slingshot OFI 上的 GPU-initiated 通信 runtime，补齐 kernel 自主跨节点协调）、**FlashSpread**（多阶段 pipeline 压成寄存器级 fused Triton kernel 的范式）、**HFX**（multi-SLO + 弹性伸缩 cluster-level serving 控制面）、**Kernel Contracts**（跨硅片 kernel 一致性规约语言，对国产芯片对齐 NVIDIA 语义有用）、**LayerBoost**（层感知注意力替换，避开全局 retrain）、CUDA Graph × UCX 节点内多路径通信、**LangGraph 1.1.10 紧急 revert node-level timeouts**（1.1.9 昨日 land 今日打回）、LangGraph prebuilt 1.0.12 ToolNode channel hydration 修复、Luce DFlash 单卡 3090 + Qwen3.6-27B 投机解码 1.98×、SGLang 70x 冷启动、Anthropic prompt-cache 一致性可见性缺陷、Lightport MCP gateway
- 状态: ✅ 成功。与昨日对照有意思：昨日 PyTorch nn.linear_cross_entropy 刚 land 就 revert，今日 LangGraph node-level timeouts 也是 24h 内 revert——"feature 落地即回滚"在基础设施层最近特别高频

## 2026-04-28 22:00（周二跑，第 2 次——同一天再次触发）
- fetch: 49 条 raw（papers 27 / code 6 / blogs 0 / community 16），无 RSS 源失败；第二次抓取量比第一次 92 条少是正常现象（HN/reddit 热度消退 + arXiv 时间窗滚出）
- curated: 20 条（papers 12 / code 4 / blogs 0 / community 4），domain_tag 分布 推理 13 / 训练 3 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，19 处 CST 时间戳，source=today_curated.json
- publish: commit `3595b88`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 218 行 diff
- 亮点（新增/深化）：**CuTile**（跨架构 GEMM/FA/LLM inference 实测 vs cuBLAS/Triton/WMMA，H100/B200）、**ELSA**（tensor-core independent 线性扫描 attention，Triton+CUDA 精确 softmax）、**ClusterFusion++**（Transformer-block 级全块融合，CUDA Graph+TMA）、**RetroInfer**（向量存储引擎长上下文，CPU offload+稀疏 attention 检索）、**FlashNorm**（RMSNorm weight fold 进 linear 并行执行）、**FlashOverlap**（TP 通信计算 overlap 最小化尾延迟）、**InfiniPipe**（elastic PP，token/batch 粒度混合调度）、**MoE expert 激活**（Llama4/DSV3/Qwen3 多节点推理实测）、LongFlow（reasoning 长输出 KV cache 压缩）、**PTQ outlier 校准**（weighted set cover 选 channel）、Hybrid JIT+CUDA Graph（partition 静态/动态 dual-path）
- 本次 agent 命中：LangGraph 三连（1.1.10 revert timeouts / 4.0.3 checkpoint lc=2 revive / 1.0.12 ToolNode hydration）+ Lightport MCP gateway
- 状态: ✅ 成功。第二次跑信号质量仍高，推理方向新增多个 kernel 级别 paper，训练方向有 FlashOverlap+InfiniPipe+MoE expert 三条链路

## 2026-04-29 22:00（周三跑）
- fetch: 40 条 raw（papers 21 / code 6 / blogs 3 / community 10），无 RSS 源失败；papers 跨分区重复严重（同一 arXiv ID 出现在 cs.DC/cs.AR/cs.PF/cs.LG/cs.CL）需在 curated 阶段按 link 去重
- curated: 18 条（papers 8 / code 5 / blogs 1 / community 4），domain_tag 分布 推理 15 / 训练 1 / agent 2
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳正常
- publish: commit `406ec13`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +544 行
- 亮点：今日 arXiv 推理侧集中爆发——**SnapMLA**（DeepSeek MLA decode FP8 量化流水线，RoPE-aware per-token KV 量化）、**CacheFlow**（KV cache restoration 升级到 3D 并行）、**PolyKV**（多 agent 共享 Key int8+Value TurboQuant MSE 压缩 KV cache 池）、**Janus**（MoE attention/experts 独立 worker 池）、**Salca**（长上下文 decode 稀疏加速器）、**AHASD**（移动端 NPU+PIM 投机解码 task-level 解耦）、**QFlash**（FA 全整型化单 Triton kernel）、**PipeWeave**（analytical+learning 混合 GPU 性能建模）；release 侧 TensorRT-LLM v1.3.0rc13 补齐 Nemotron 3 Nano Omni + GLM-4.7/GLM-5 + DSV3.2 Blackwell chunked-prefill、FA4 beta11 CUTE head_dim=256 + Flex autograd、OpenAI Agents v0.14.8 MCP re-export + 供应链收紧、XGrammar v0.1.34 Gemma 4 structural tag；社区侧 Qwen FlashQLA TileLang 线性注意力 + llama.cpp b8967 Blackwell NVFP4 native（实测 **prefill +43~68% / decode 基本不变**，符合 compute-bound vs memory-bound 区分）+ Qwen3.6-27B 双卡 5060 Ti vLLM 204k 上下文
- 状态: ✅ 成功。domain_tag 偏推理是今日客观情况（训练/agent 信号天然少），严格执行「宁缺毋滥」不塞应用层凑数。PolyKV 把 TurboQuant 用到多 agent KV cache 共享，是用户近期 TurboQuant 研究的新工程组合方向

## 2026-04-30 22:00（周四跑）
- fetch: 45 条 raw（papers 23 / code 12 / blogs 0 / community 10），无 RSS 源失败；papers 跨分区重复严重（RaMP/Folding TSP/DUAL-BLADE/FACT/AMMA/xLM 等多篇同时出现在 cs.DC/cs.AR/cs.PF/cs.LG/cs.CL），curated 阶段按 link 去重
- curated: 26 条（papers 16 / code 8 / blogs 0 / community 2），domain_tag 分布 推理 17 / 训练 5 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳正常
- publish: commit `1c3c8da`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 +697 行
- 亮点：今日 arXiv 推理侧再次集中爆发——**RaMP**（MoE 路由感知 kernel dispatch，4 参数 wave 代价模型，0.93% 平均遗憾 vs exhaustive search）、**DUAL-BLADE**（NVMe KV offload 双路径 page-cache + direct LBA）、**DAK**（TMA 异步直接访问远端内存，不 prefetch 避开 HBM 争用与 pipeline bubble）、**FACT**（agent 驱动 kernel 合成 grounded 到 CUTLASS，避免裸 CUDA 重发明优化）、**AMMA**（multi-chiplet memory-centric 1M 上下文 attention，KV 下沉 PIM/PNM）、**SPIN**（稀疏 attention × 分层 KV 存储统一框架）、**AHASD**（移动端 NPU+PIM 投机解码 task-level 解耦）、**TSP**（TP+SP 折叠到同一 device 轴）、**COPUS**（batch×并行策略联合自适应）、**FaaSMoE**（MoE expert 作 stateless FaaS function scale-to-zero）、逆向 NVIDIA 闭源 driver 命令流（硬件断点+开源 kernel driver 打桩）；code 侧 TensorRT-LLM v1.3.0rc13 Nemotron 3 Nano Omni + GLM-4.7/GLM-5 + DSV3.2 Blackwell chunked-prefill、KTransformers v0.6.1 大 MoE LoRA SFT 6-12× vs ZeRO-Offload、FlashInfer v0.6.10rc1 head_dim=512 + MXFP4×BF16、FA4 beta11 hd256 + Flex autograd、LangGraph 1.2.0a1 timers 重构（前天 revert 之后的答卷）+ prebuilt 1.0.13、OpenAI Agents v0.14.8 MCP re-export 修复、XGrammar v0.1.34 Gemma 4 structural tag
- 状态: ✅ 成功。papers 分区 16 条偏多但均在 20 条上限内，推理/训练/agent = 17/5/4 分布偏推理是今日客观情况（arXiv 今天刷出大量 infra 方向 paper）；社区侧严格过滤掉 Mistral-Medium-3.5/Qwen-Scope SAE/DeepSeek 视觉推理/5M 玩具模型/Qwen sticker 等非基础设施内容，只留 Qwen3.6-27B 实测与 AMD ROCm 工程师征集反馈

## 2026-04-28 22:00（周二跑，第 3 次——同一天第三次触发）
- fetch: 45 条 raw（papers 27 / code 8 / blogs 0 / community 10），无 RSS 源失败；比第 2 次又少（reddit 热度继续消退）
- curated: 18 条（papers 8 / code 6 / blogs 0 / community 4），domain_tag 分布 推理 11 / 训练 3 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳正常
- publish: commit `c0de9b8`，HEAD==origin/main，2026/04 + archive 两份 HTML 各 194 行 diff
- 亮点（相对前两跑收敛稳定，未新增重大信号）：CuTile / ClusterFusion++ / RetroInfer / Hybrid JIT+CUDA Graph / MoE expert 激活 / FlashOverlap / InfiniPipe / TACO（TP FP8 通信压缩）；code 侧 vLLM v0.20.0 + FlashInfer 0.6.9 + LangGraph 三连（1.1.10 revert / 4.0.3 checkpoint / 1.0.12 prebuilt）+ OpenAI Agents v0.14.7（symlink LocalFile reject、tar/zip member 加固、Phase 2 memory turn limit 上调）；community 侧 Luce DFlash + Strix Halo hipfire HFQ4 MMQ 3× + Qwen3.6-27B IQ4_XS 显存回归 + 三档量化对比
- 状态: ✅ 成功。同一日第 3 跑严格遵守「宁缺毋滥」，条数收敛到 18，丢掉了 ELSA/FlashNorm/LongFlow/PTQ 这类已在前跑覆盖、本次无新信号的 paper
- 观察：同日多次触发的信号冗余度在第 3 次跑明显上升（arXiv 帖子是同一批，GitHub release 一样）；后续建议看板脚本增加「同日去重」或「仅差量输出」能力避免重复 commit 等量信息

## 2026-05-01 22:00（周五跑，劳动节假期）
- fetch: 44 条 raw（papers 24 / code 8 / blogs 1 / community 11），无 RSS 源失败；五一假期节奏，HN LLM/Agent infra 双 0 是常态，code 侧只有 FlashInfer/LangGraph/OpenAI Agents/KTransformers 四家有 release
- curated: 20 条（papers 12 / code 4 / blogs 1 / community 3），按 link 去重后 papers 实际唯一 12 条全收（AMMA/AHASD 已在 4/30 覆盖过但是 v2 replace/v3 replace 今日再现，保留）；domain_tag 分布 推理 11 / 训练 5 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，23 处 CST 时间戳
- publish: commit `dc3d6ba`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +582 行
- 亮点：arXiv 推理侧 **Predictive Multi-Tier KV Cache**（MLA 统一 sizing + 六级存储层次 + 预测淘汰，揭示 MLA 在通用框架被高估 57× 显存）、**FluxMoE**（expert paging，expert 非 GPU 常驻 vs FaaSMoE 的另一斜率）、**RCW-CIM**（DCIM 架构补齐权重更新延迟盲点，Llama2-7B decode -21.59%）、**VitaLLM**（BitNet 三元专用加速器 Dual-Core）、**RoundPipe**（消费级 GPU 打破 PP weight-binding，stateless 执行池）、**ZipCCL**（首个把无损压缩塞进集合通信库，基于高斯分布假设）、**SWOT**（光网络 intra-collective 重构中间路径）；agent 基础设施侧 **MARS**（GPU-CPU 异构 agent workload 协同调度）+ **Crab**（agent sandbox C/R runtime，75% agent turn 无 state 观察，用于 RL rollout 分支/容错/spot）；code 侧 **OpenAI Agents v0.15.0**（ModelRefusalError 显式化，拒答从 silent failure 到控制流）、**LangGraph 1.2.0a2**（NodeTimeoutError 默认可重试，timers 重构继续收敛）、**FlashInfer v0.6.10rc1**（trtllm FMHA head_dim=512 + MXFP4×BF16 MoE SM90 + DCP All-to-All CP kernel）、**KTransformers v0.6.1**（kt-kernel 重构 vs ZeRO-Offload 6-12×）；blogs 侧 **NVIDIA cuTile Python→cuTile.jl 自动 agent 翻译**（coding agent 做 kernel 跨语言移植的首个 NVIDIA 官方样本）；community 侧 DFlash Qwen3.5-35B-A3B 在 2080 SUPER 8GB 跑通、5000 行 Python 实现 6 层 IR LLM 编译器参考栈（TVM/Inductor/XLA 替代教学读物）、16×DGX Spark unified memory fabric 实战（对国产 ScaleUp 统一内存路线有直接参考意义）
- 状态: ✅ 成功。严格排除 Sigmoid single-cell/Hyperledger/Affinity Tailor/HASE/r/LocalLLaMA 的 Packman 对比/MiMo 能力榜/算力涨价吐槽/open models 汇总/MacBook 买买买吐槽 等非基础设施内容
- 注意：踩坑——Python 脚本里 tldr 含英文双引号会触发字符串提前闭合（SyntaxError），中文双引号要用「」避开。已固化：本次需要 3 轮 replace_in_file 才把 7 处英文双引号全换完；后续 `_build_curated.py` 只用中文「」或 em-dash 包裹强调词
