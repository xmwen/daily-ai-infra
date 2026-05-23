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

## 2026-05-02 22:00（周六跑，五一假期第二天）
- fetch: 22 条 raw（papers 0 / code 12 / blogs 0 / community 10），无 RSS 源失败；周六 arXiv 不更新（papers 0）+ 假期 blogs 0 双断流，HN LLM/Agent infra 也是 0，community 仅 r/LocalLLaMA 10 条
- curated: 9 条（papers 0 / code 5 / blogs 0 / community 4），domain_tag 分布 推理 5 / 训练 0 / agent 4；训练 0 是今日 Megatron/PyTorch/DeepSpeed/TransformerEngine 全无 release 的客观事实
- render: `LLM 摘要 ✓`，无 fallback，12 处 CST 时间戳，source=today_curated.json
- publish: commit `347ef3c`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +375 行 diff
- 亮点：**vLLM v0.20.1** 紧急 revert persistent topk（v0.20.0 次日 hotfix，延续最近「feature 落地即回滚」节奏）、**OpenAI Agents v0.15.0** 把模型拒答提升为显式 ModelRefusalError（silent failure→控制流可观测）、**OpenAI Agents v0.15.1** Responses WebSocket keepalive + UnixLocal PTY SIGINT 恢复、**LangGraph 一晚连发 6 个 alpha**（stream_events v3 dispatch / DeltaChannel sentinel+checkpoint_writes 重建 / node-level error handlers / two phase read / NodeTimeoutError 默认可重试——timers 重构在 4/28 revert 之后继续收敛）、**XGrammar v0.2.0** 高 tool 数量 structural-tag 编译耗时大降 + GrammarMatcher 暴露 draft tree traversal 给投机解码接 constrained decoding、**PFlash**（Luce 纯 C++/CUDA 投机式 prefill，3090 Qwen3.6-27B Q4_K_M 128K TTFT 10.4×，NIAH 保真，"投机"从 decode 扩到 prefill 的工程化落地）、**MiniMax M2.7 AWQ-4bit 2×DGX Spark vs 2×RTX 6000 96GB 实测**（Spark unified memory fabric 在 MoE 推理上差距比预期小，对国产 ScaleUp 路线直接参考）、**Qwen3.6-27B native vLLM Windows**（72 tok/s 3090 无 WSL）、**Mistral Medium 3.5 YaRN mscale_all_dim=1→0 跨实现 bug**（transformers + llama.cpp 同时中招，典型 RoPE 扩展解析默认值不一致导致长上下文崩坏）
- 状态: ✅ 成功。严格排除 TTS 模型/设置分享网站/Qwen 路线猜测/社区规则 check-in/VSCode 日常使用体验等非基础设施内容；LangGraph 合并 6 条 alpha/prebuilt/checkpoint 为 1 条避免版本号轰炸；Mistral 两条重复 GGUF 修复帖合并 1 条

## 2026-05-05 22:00（周二跑）
- fetch: 46 条 raw（papers 25 / code 9 / blogs 0 / community 12），无 RSS 源失败；blogs 源全 0（HF 774 项时间窗过滤 + PyTorch/LangChain/Anthropic/Fireworks/HazyResearch 源今日全空）+ HN LLM/Agent infra 双 0
- curated: 20 条（papers 12 / code 5 / blogs 0 / community 3），按 link 跨分区去重后 papers 唯一 18 条，扔 5/4 已覆盖的 v2 replace（Silicon Showdown / Sim-FA / Tempus）+ SURGE / gem5 / GPIR / RL adaptive speculative 等弱相关；domain_tag 分布 推理 14 / 训练 2 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳齐全
- publish: commit `fe7b6f3`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +583 行 diff
- 亮点：arXiv 推理侧密集爆发——**SplitZip**（PD 分离 GPU 原生超快无损 KV 压缩）、**SANTA**（decode value-cache 采样+gather-and-add 1.5×@32k）、**StreamIndex**（V4 CSA Triton chunked top-k driver 不物化 256GB 中间张量）、**PipeMax**（PP+offload 联合优化离线推理）、**Kairos**（disagg 长尾感知 SLO 调度）、**GhostServe**（KV erasure coding + host parity 影子，million-token agent 容错）、**NCCLbpf**（eBPF 嵌进 NCCL plugin 接口，静态验证+cross-plugin map+原子热切换）、**MCP Workflow Engine**（agent 思考与执行解耦，workflow blueprint 静态图化复放）、**AAFLOW**（Arrow+Cylon zero-copy agent 数据平面）、**P3-LLM**（NPU+PIM 边缘混合精度）、**GH200 多模态训练能耗跨层分析**（统一内存路线建模参考）、**LLM Serving Position Paper**（呼吁推理调度从启发式转数学最优化）；release 侧 **FlashInfer v0.6.10 正式版**（trtllm head_dim=512+MXFP4×BF16 SM90+DCP A2A）、**vLLM v0.20.1**（V4 Base+multi-stream GEMM+持续 guard topk 死锁，本月第 4 次 feature 落地即回滚）、**Outlines v1.2.12** bugfix、**LangGraph 1.2.0a7+checkpoint 4.1.0a4+checkpoint-postgres 3.1.0a4 三连 alpha**（public get_writes_history saver API + delta cadence 重做）、**SGLang v0.5.11**；community 侧 **vLLM TurboQuant fix for Qwen3.5+/Qwen3.6 合并**（PR #39931，--kv-cache-dtype turboquant_4bit_nc/k8v4/k3v4_nc/3bit_nc 四档可用，TurboQuant per-vector min-max 3/4-bit 在主线 hybrid Mamba+Attn 模型首次落产线，与用户 RaBitQ/TurboQuant 研究直连）、**Qwen3.6 27B FP8+200k BF16 KV @ 单卡 RTX 5000 PRO 48GB 80 TPS**（48GB 档绕 24GB 量化精度劣化）、**llama.cpp MTP beta**（Qwen3.5 先落地，与 TP 一起抹平 vs vLLM 速度差距）
- 状态: ✅ 成功。推理 14 偏重是今日 arXiv 推理方向客观爆发；训练 2 偏少是 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS 全无 release + blogs 全 0 + HN 双 0 的客观底；TurboQuant fix 是用户方向最强信号

## 2026-05-04 22:00（周一跑，五一假期后首个工作日）
- fetch: 38 条 raw（papers 18 / code 8 / blogs 0 / community 12），无 RSS 源失败；blogs 0 是 HF 774 项被时间窗过滤的客观结果，PyTorch/LangChain/Anthropic/Fireworks/HazyResearch 源今日全空
- curated: 17 条（papers 9 / code 5 / blogs 0 / community 3），按 link 去重后 papers 唯一 11 条，扔 Lottery BP（QEC）+ AgentFactory-HLS（应用）；domain_tag 分布 推理 13 / 训练 2 / agent 2
- render: `LLM 摘要 ✓`，无 fallback，CST 时间戳齐全
- publish: commit `e9b210d`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +526 行 diff
- 亮点：arXiv 推理侧密集爆发——**TokenWeave v5**（vLLM/SGLang/TRT-LLM 默认关闭 TP overlap 的真相，低延迟下 decompose 反而更慢；自适应只在通信主导区启用）、**LLM-Emu**（vLLM serving-native 模拟器，保留真实 HTTP/scheduler/KV cache 只替换 forward）、**SAGA**（agent workflow 作为调度单元，KV 复用达 Bélády 最优 1.31× 内）、**Eliminating Hidden Serialization in Multi-Node Megakernel**（MoE megakernel 多机 RDMA proxy 隐藏 serialization 致 8 节点退化 10×，给去序列化方案）、**AGoQ**（layer-aware 4-bit act + 8-bit grad All-Reduce）、**Silicon Showdown**（Blackwell NVFP4 1.6× vs BF16 但 Backend Dichotomy 跨多门槛）、**Sim-FA**（warp specialization cycle-accurate 前端）、**VitaLLM**（BitNet 三元 Dual-Core ASIC）、**Tempus**（Versal AIE 时间扩展不堆核）；release 侧 **vLLM v0.20.1** DeepSeek V4 稳定化 + multi-stream pre-attn GEMM + 临时 guard v0.20.0 刚上的 persistent topk（本月第 4 次 feature 落地即回滚）、**KTransformers v0.6.2 + post1** V4-Flash MXFP4 原生 + 8×5090 prefill 16k→2011/65k→2798/262k→2154 tok/s + post1 修复 fallback 硬编 FP8/INT4 layout bug、**LangGraph 1.2.0a6** stream_events v3 kwargs、**Triton gfx950-tutorial-v0.1**；community 侧 **torch-nvenc-compress**（NVENC 当 PCIe 带宽倍增器，延续 LLM.265 路线，GEMM+encode overlap 67%）、**llama.cpp MTP beta**（Qwen3.5 先落地）、**SSM Parameter Golf 实证**（SSM in_proj LZMA 压缩比差 Attn QKV 3.26×，附 Mamba-3 Triton backward fusion SMEM 压力反慢 16%）
- 状态: ✅ 成功。推理 13 偏重是 arXiv 今日客观事实（多篇新 paper 集中 cs.DC/cs.AR），严格排除应用层；build 脚本仍用中文「」引号规避 Python 字符串闭合坑

## 2026-05-03 22:00（周日跑，五一假期第三天）
- fetch: 17 条 raw（papers 0 / code 7 / blogs 0 / community 10），无 RSS 源失败；周日 arXiv 不更新 + 假期 blogs 源全 0 + HN 双 0，community 仅 r/LocalLLaMA
- curated: 5 条（papers 0 / code 4 / blogs 0 / community 1），domain_tag 分布 推理 4 / 训练 0 / agent 1；训练 0 连续第二天（客观事实：Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS 全无 release）
- render: `LLM 摘要 ✓`，无 fallback，8 处 CST 时间戳
- publish: commit `e9ee3b7`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +299 行
- 亮点：**vLLM v0.20.1** DeepSeek V4 稳定化 + multi-stream pre-attn GEMM + FP32→FP4 PTX cvt + head_compute_mix_kernel + 临时 guard 掉昨日刚上的 persistent topk（TopK=1024 死锁 + RadixRowState race，"feature 落地即 guard"本月第 4 次）、**KTransformers v0.6.2** DeepSeek-V4-Flash 直通 kt-kernel MXFP4 MoE 原生消费 E2M1+ue8m0 权重 + 8×RTX 5090 SM_120 + AVX2/AVX-VNNI RAWINT4 扩消费 CPU、**KTransformers v0.6.2.post1** V4-Flash MXFP4 full-GPU prefill fallback 修复（硬编 FP8/INT4 layout bug），8×5090 实测 16k→2011 / 65k→2798 / 262k→2154 tok/s prefill、**Triton gfx950-tutorial-v0.1** AMD CDNA4 教学 kernel pin 分支（LLIR scheduler + amdgcnas + RA-hints + buffer_store inst_offset fold，绕开 hoistVoffsetCompute dominance bug）、**MDA** agent 持久记忆基础设施（Oja 规则在线更新 + 激活概念图召回 + MCP server + 多 agent 激活共享而非检索共享）
- 状态: ✅ 成功。5 条是绝对低位但严格符合「宁缺毋滥」——周日+假期第三天的客观信号底；排除 Qwen vs Coder-Next 能力对比/GPT 5.5 CoT 八卦/llama.cpp ban phrases/Upskill skill registry/Tinygrad 闲聊/fine-tuning guide/HF visualizer/FlashInfer nightly 无 changelog/vLLM v0.20.2rc0 单 commit/OpenAI Agents v0.15.1（昨已覆盖）

## 2026-05-01 22:00（周五跑，劳动节假期）
- fetch: 44 条 raw（papers 24 / code 8 / blogs 1 / community 11），无 RSS 源失败；五一假期节奏，HN LLM/Agent infra 双 0 是常态，code 侧只有 FlashInfer/LangGraph/OpenAI Agents/KTransformers 四家有 release
- curated: 20 条（papers 12 / code 4 / blogs 1 / community 3），按 link 去重后 papers 实际唯一 12 条全收（AMMA/AHASD 已在 4/30 覆盖过但是 v2 replace/v3 replace 今日再现，保留）；domain_tag 分布 推理 11 / 训练 5 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，23 处 CST 时间戳
- publish: commit `dc3d6ba`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +582 行
- 亮点：arXiv 推理侧 **Predictive Multi-Tier KV Cache**（MLA 统一 sizing + 六级存储层次 + 预测淘汰，揭示 MLA 在通用框架被高估 57× 显存）、**FluxMoE**（expert paging，expert 非 GPU 常驻 vs FaaSMoE 的另一斜率）、**RCW-CIM**（DCIM 架构补齐权重更新延迟盲点，Llama2-7B decode -21.59%）、**VitaLLM**（BitNet 三元专用加速器 Dual-Core）、**RoundPipe**（消费级 GPU 打破 PP weight-binding，stateless 执行池）、**ZipCCL**（首个把无损压缩塞进集合通信库，基于高斯分布假设）、**SWOT**（光网络 intra-collective 重构中间路径）；agent 基础设施侧 **MARS**（GPU-CPU 异构 agent workload 协同调度）+ **Crab**（agent sandbox C/R runtime，75% agent turn 无 state 观察，用于 RL rollout 分支/容错/spot）；code 侧 **OpenAI Agents v0.15.0**（ModelRefusalError 显式化，拒答从 silent failure 到控制流）、**LangGraph 1.2.0a2**（NodeTimeoutError 默认可重试，timers 重构继续收敛）、**FlashInfer v0.6.10rc1**（trtllm FMHA head_dim=512 + MXFP4×BF16 MoE SM90 + DCP All-to-All CP kernel）、**KTransformers v0.6.1**（kt-kernel 重构 vs ZeRO-Offload 6-12×）；blogs 侧 **NVIDIA cuTile Python→cuTile.jl 自动 agent 翻译**（coding agent 做 kernel 跨语言移植的首个 NVIDIA 官方样本）；community 侧 DFlash Qwen3.5-35B-A3B 在 2080 SUPER 8GB 跑通、5000 行 Python 实现 6 层 IR LLM 编译器参考栈（TVM/Inductor/XLA 替代教学读物）、16×DGX Spark unified memory fabric 实战（对国产 ScaleUp 统一内存路线有直接参考意义）
- 状态: ✅ 成功。严格排除 Sigmoid single-cell/Hyperledger/Affinity Tailor/HASE/r/LocalLLaMA 的 Packman 对比/MiMo 能力榜/算力涨价吐槽/open models 汇总/MacBook 买买买吐槽 等非基础设施内容
- 注意：踩坑——Python 脚本里 tldr 含英文双引号会触发字符串提前闭合（SyntaxError），中文双引号要用「」避开。已固化：本次需要 3 轮 replace_in_file 才把 7 处英文双引号全换完；后续 `_build_curated.py` 只用中文「」或 em-dash 包裹强调词


## 2026-05-06 22:00（周三跑）
- fetch: 33 条 raw（papers 12 / code 6 / blogs 0 / community 15），无 RSS 源失败；blogs 全 0 + HN LLM infra 0
- curated: 19 条（papers 10 / code 5 / blogs 0 / community 4），按 link 去重 papers 唯一 11 条扔 Lottery BP（QEC）+ FACT 跨分区合并；domain_tag 分布 推理 13 / 训练 0 / agent 6
- render: LLM 摘要 ✓，无 fallback，CST 时间戳齐全
- publish: commit 20debe，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +564 行
- 亮点：Tutti（NVMe SSD KV cache 实用化 GPU 自主 IO）/ Continuum（agent KV cache TTL 调度）/ FACT（agent 驱动 CUTLASS 合成）/ VDCores（异步 GPU 单元 micro-op DAG）/ ZeRO-Prefill（MoE prefill-only 零冗余）/ SparKV（端云协同 KV chunk cost 模型）/ BloomBee（Internet 规模分布式推理 DP）/ CCCL（CXL 共享内存池替代 RDMA 跨节点 collective）/ TCM-Serve（多模态 modality-aware 调度）/ SpecKV（投机解码自适应 γ）；release 侧 OpenAI Agents v0.15.3+v0.15.2、LangGraph SDK 0.3.14+checkpoint-sqlite 3.1.0a1（streaming walk + delta cadence rework）、FA4 beta12（hd256 backward TMA + GQA determinism）；community 侧 Qwen3.6-27B MTP llama.cpp PR（M2 Max 96GB 2.5×）+ MTP grafted on Unsloth UD XL + TritonSigmoid（H100 515 TFLOPS）+ Recursant agent service mesh
- 状态: ✅ 成功。训练 0 条是 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS 全无 release 的客观底；严格排除 SubQ BS / Apple Mac Studio / DeepSeek V4 cost / Ollama CVE / Gemma 4 用途讨论 / blockchain VLM 应用等非基础设施内容

## 2026-05-09 22:00（周六跑）
- fetch: 18 条 raw（papers 0 / code 6 / blogs 1 / community 11），无 RSS 源失败；周六 arXiv 不更新（papers 0）+ HN LLM/Agent infra 双 0 + blogs 仅 NVIDIA Dev 1 条；HuggingFace 777 项被时间窗过滤、Together AI/Google Research/Meta Eng 全部时间窗过滤
- curated: 9 条（papers 0 / code 4 / blogs 1 / community 4），domain_tag 分布 推理 5 / 训练 1 / agent 3
- render: LLM 摘要 ✓，无 fallback，12 处 CST 时间戳，source=today_curated.json
- publish: commit `823bd07`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +374 行 diff
- 亮点：**KTransformers v0.6.2.post2** 把 V4-Flash 启动样例从 8×RTX 5090 切到「单卡 decode 20+ tok/s」+ Ada Lovelace SM_89 升 validated（DSV4-Flash MoE+SWA 推理工程从集群下放消费卡的拐点信号）、**OpenAI Agents v0.17.0** RealtimeAgent 默认切 gpt-realtime-2 + sandbox 局部源物化关闭 host 文件越界拷贝（延续 sandbox boundary 收紧节奏）、**MCP Python v1.27.1** pydantic 2.13 兼容 + OAuth 空字符串 URL 强制 None、**FlashInfer v0.6.11rc1** 接续 hd512+MXFP4×BF16+DCP A2A、**NVIDIA Dev Blog Grammar-Constrained Decoding 改 SLM Bash 生成**（NV 首个把 constrained decoding 推到 coding agent shell tool use 的官方背书，命中 XGrammar/Outlines 路线）、**DeepSeek V4 完整论文释出**（FP4 QAT 进训练后期 + MoE 专家 FP4 + CSA QK FP4 99.7% recall 2× selector 加速 + 1M 上下文 V4-Pro KV cache 10% / V4-Flash 7% of V3.2 baseline + anticipatory routing 与 loss spike 显式诱发-恢复双稳定机制治 trillion-param MoE）、**TurboQuant TBQ4_0 KV + MTP @ Qwen3.6-27B 单卡 4090 80-87 tok/s @ 262K**（用户 RaBitQ/TurboQuant 方向直连工程验证）、**Qwen3.6 35B-A3B + llama.cpp MTP 12GB 档双实测**（4070 Super 80 tok/s @ 128K + 3060 12GB pp512 914/tg128 47，MoE 推理「保 MoE 块在 GPU + KV 量化」配方在主线已成熟）、**vLLM ROCm 入 Lemonade**（AMD 推理栈 ROCm 侧首次有 vLLM 一键体验，对位 llama.cpp）
- 状态: ✅ 成功。9 条是周六的客观信号底（arXiv 0 + HN 双 0 + blogs 几乎全 0），严格执行「宁缺毋滥」——排除 Qwen NVFP4/GPTQ 多格式分发（应用层）、DGX Spark 社区情怀贴、April 致敬 meme、DeepSeek 拒阿里融资（商业新闻）、Pi+Qwen 装 Arch（agent 应用案例）、Qwen 不工作梗图、FlashInfer 两条同源 nightly 合并到 rc1
- 观察：DSV4 完整论文 + KTransformers 把 V4-Flash 单卡化两件事在同一天命中——DSV4-Flash 的 KV cache 7% baseline 与 8 卡→单卡的工程拐点形成完整故事链

## 2026-05-10 22:00（周日跑）
- fetch: 15 条 raw（papers 0 / code 4 / blogs 0 / community 11），无 RSS 源失败；周日 arXiv 不更新 + blogs 全 0（HF 777 项时间窗过滤，其余时间窗/无更新）+ HN LLM/Agent infra 双 0，客观低信号日
- curated: 8 条（papers 0 / code 2 / blogs 0 / community 6），domain_tag 分布 推理 8 / 训练 0 / agent 0——训练/agent 双 0 是今日 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS/LangGraph/OpenAI Agents/XGrammar/Outlines 全无 release 的客观事实
- render: LLM 摘要 ✓，无 fallback，CST 时间戳齐全
- publish: commit `d482d0a`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +356 行
- 亮点：**vLLM v0.20.2**（DeepSeek V4 MTP=1 hang + V1 KV 块分配失败 + gpt-oss MXFP4×torch.compile + Qwen3-VL deepstack 边界 4 项修复，延续本月 feature 落地即 revert→重上节奏）、**NVIDIA Star Elastic**（单 ckpt 塞 30B/23B/12B，zero-shot slicing 切层降档，三档共享 KV cache）、**llama.cpp b9095 NCCL-Free TP on Dual Blackwell**（消费级双 Blackwell TP 走自己的 CUDA IPC+P2P 绕开 NCCL，对国产芯片 P2P+host-staging 无 NCCL 方案直接参考）、**DeepSeek V4-Pro Q4_K_M 单卡 RTX PRO 6000 Max-Q 跑通**（Epyc 9374F+12×96GB RAM+97GB VRAM，antirez ds4/LegacyRemaster Q4_K_M 分支首个单卡家用 V4-Pro）、**DS4 (antirez)**（Redis 作者开源 V4-Flash on Mac Metal 1M ctx，OpenAI+Anthropic 端点，V4-Flash 第三个独立栈 KTransformers/SGLang/DS4）、**Qwen3.6 35B-A3B + llama.cpp MTP @ 12GB 80 tok/s 128K**（RTX 4070 Super 单卡稳定达标，MTP 接受率 80%+）、**MiniMax M2.7 on Strix Halo 100k**（AMD 统一内存 serving 参数调优，对 ScaleUp 统一内存路线借鉴）、**FlashInfer v0.6.11rc1** 正式 rc
- 状态: ✅ 成功。周日 8 条是客观信号底，严格执行「宁缺毋滥」——排除 MCP server 一周年情怀、Harnesses 抱怨、OpenWebUI tool library 应用、3080 20GB mod 购买咨询、DeepSeek V4 论文 r/ML 版本（昨日 r/ML 已覆盖）
- 观察：vLLM 本周曲线 5/2 v0.20.1 revert persistent topk → 5/10 v0.20.2 重启 persistent topk 并补 memset CUDA graph capture，"落地→revert→修根因→重上" 典型 V4 级 feature 曲线

## 2026-05-11 22:00（周一跑）
- fetch: 43 条 raw（papers 20 / code 4 / blogs 0 / community 19），无 RSS 源失败；blogs 全 0（NVIDIA Dev 100 项 / Google Research 100 项 / HF 776 项 / Together AI 100 项全部时间窗过滤，PyTorch/LangChain/Anthropic/Fireworks/HazyResearch 源全空）+ HN LLM/Agent infra 7 条 + r/LocalLLaMA 10 条
- curated: 19 条（papers 13 / code 2 / blogs 0 / community 4），按 link 去重 papers 唯一 13 条（Fluxion cs.PF×cs.LG 合并、AccelSync 跨 cs.DC×cs.AR 同 ID 合并）；扔 MERBIT（SpMV graph 应用 不属 LLM 推理）+ AccelSync（accelerator 编译验证，更偏 verification 不偏 infra）+ FATE（multi-stage workflow scheduler 偏 application）；domain_tag 分布 推理 15 / 训练 3 / agent 1
- render: LLM 摘要 ✓，无 fallback，22 处 CST 时间戳，source=today_curated.json
- publish: commit `85e2938`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +564 行
- 亮点：**arXiv 推理侧大爆发**——**DP 负载均衡 online routing**（TP/EP+DP 复制下 KV 迁移成本+非平稳到达+sub-100ms 决策预算的在线路由）、**Fluxion**（CPU-resident KV 长上下文 CPU-GPU 混合稀疏 attention，output-aware budget + head/granularity 独立配置）、**KV cache range-search index**（稀疏 attention 零假阴性保证，针对长 reasoning 中 important token 漂移）、**MISA**（DSA indexer 64-head 共享改 MoE 池化，drop-in 替换大幅降本）、**ThinKV**（CoT 思维重要性自适应 KV 压缩 + PagedAttention kernel 扩展支持已驱逐 token 内存复用）、**Star Elastic**（单 ckpt N 个嵌套子模型 + 弹性 budget control）、**RcLLM**（生成式推荐 Beyond-Prefix KV，user-history 复制+item similarity-aware 分片）、**TAPER**（branch externality 量化 + per-step admission control）、**Dooly**（配置无关推理 simulator，跨配置共享 op profile）、**SOCKET**（LSH 软碰撞核+Triton kernel）、**Ascend MoE relay-free 通信**（围绕 globally pooled HBM 直接落入/读取 expert window，国产 MoE 通信路径直接信号）；**训练**——HexiSeq（异构 GPU 集群 CP+HP 完全非对称切分，约束优化+层级调度器）、SuperMUC-NG Phase 2 训练 recipe（Intel Ponte Vecchio GPU Max 1550，非 NVIDIA 训练栈参考）；**code**——vLLM v0.20.2 紧续 5/10 的 V4 sparse attention persistent topk + V1 KV block 分配 + gpt-oss MXFP4×torch.compile + Qwen3-VL deepstack（本月 V4 级 feature 落地→revert→重上节奏第 5 次）、OpenAI Agents v0.17.1 sandbox/tracing/sessions 三轴持续加固；**community**——MTP 系统 benchmark 300+ 测试得「任务文本熵决定 MTP 加速比」结论（coding 3× / creative 反慢）、Tracing Llama 3.1 8B on H100 全链路教学、ExLlamaV3 DFlash 2.5-3× 加速（投机解码单卡量化推理引擎工程化跟踪）、llama.cpp Grinder12 0.96-bit KV cache 极端 sub-bit 路线信号点
- 状态: ✅ 成功。推理 15 偏重是 arXiv 今日客观爆发（cs.DC 10 + cs.LG 7 + cs.PF 1 + cs.AR 2），训练/agent 偏少是 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS/LangGraph/XGrammar/Outlines/MCP Python 全无 release 的客观底；严格排除 Markdown browser/knowledge-hub MCP 配置/PSA chat-template 空格/opencode 慢/Qwen 35B distill 求版本/tokenspeed 速度感受工具/Claude Code SSH+Nix/Claude Code 大项目工作流/FLOX C++ trading/AI-FI secure boot/AI Agents long context 新闻汇总/Atlas Rust 推理引擎/Parallel Verification 新闻汇总 等应用层与非基础设施内容
- 观察: arXiv 今日同时出现 Fluxion + KV range-search + MISA + ThinKV 四篇 KV cache/sparse attention 路线 paper，体现长上下文 KV 管理已成「主流推理 paper 母题」；TAPER + DP 负载均衡 + Dooly 三篇都在解 LLM serving 一线运维瓶颈

## 2026-05-12 22:00（周二跑）
- fetch: 64 条 raw（papers 35 / code 10 / blogs 1 / community 18），无 RSS 源失败；blogs 仅 NVIDIA Dev 1 条（Fleet Intelligence），HF/Google Research/Together AI 时间窗全过滤；HN LLM 3 + HN Agent 4 + r/LocalLLaMA 10 + r/ML 1
- curated: 30 条（papers 20 / code 3 / blogs 1 / community 6），按 link 跨分区去重 papers 唯一 20 条（KV-RM cs.AR×cs.OS、KernelBenchX cs.PF×cs.LG、Apple MPS cs.AR×cs.PF、AURORA cs.DC×cs.PF、Cloud Performance cs.DC×cs.PF、Nautilus Compass cs.LG×cs.CL）；扔 Multi-Tier LEO/Orbital Anomaly/MBA Synthesis/Cloud Perf Decomposition/MARLaaS/AURORA/Nemotron Omni（应用层或非 LLM infra）+ TLX/FlashSVD/Apple MPS/RDKV（papers 上限收敛砍掉）；domain_tag 分布 推理 20 / 训练 5 / agent 5
- render: LLM 摘要 ✓，无 fallback，33 处 CST 时间戳，source=today_curated.json
- publish: commit `107627a3`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +772 行 diff
- 亮点：**arXiv 投机解码+KV cache 双线大爆发**——**SPECTRE**（多模型云端把闲置 tail-model 当远程 drafter，hybrid 顺序-并行投机解码）/ **Surviving Partial Rank Failures**（宽 EP MoE 推理首次解耦 communicator/expert placement/CUDA Graph 路由元数据，故障缩容继续服务，直接命中 DeepEP/SGLang）/ **Continuum v5**（agent KV TTL 加入重算 vs 排队成本权衡 + tool 调用方差建模）/ **SplitZip v2**（PD 分离 GPU 原生超快无损 KV 编码）/ **Range Searching KV index**（稀疏 attention 零假阴性证明）/ **KernelBenchX**（LLM 写 Triton 176 任务测，任务结构 3× 解释正确性）/ **KV-RM**（静态图 LLM decoder 下逻辑 KV 与物理存储解耦）/ **Value-Aware KV 三步失效诊断**（fixed-contract 框架）/ **Not All Thoughts Need HBM**（reasoning KV 四档存储分层 + 零误差 prefetch 回 GPU）/ **Test-Time Speculation**（DFlash/EAGLE-3/PARD 长输出衰减到 1 的根因+修复）/ **Hidden States Drift KV rescue**（target hidden state 作偏压缩，KV 增援长距离投机）/ **TiledAttention**（cuTile Python 写 SDPA forward，schedule 级 Python 端可改）/ **ReRAM-on-Logic 加速芯片**（55nm 14-135 tok/s，PIM+投机解码+adaptive scheduler）；**训练**——**Priming**（预训练 Transformer 初始化 Hybrid SSM+短期对齐）/ **FCP**（block 粒度灵活 CP 任意 P2P 通信替环形）/ **AGoQ v2**（4-bit 激活+8-bit 梯度+精度保持 All-Reduce）/ **Lakestream**（brokerless object-store 原生训练数据 plane + Transactional Global Batch）/ **MegaScale-Omni**（字节工业级 MLLM encoder-LLM 长短并行解耦）；**code**——**LMDeploy v0.13.0**（Ascend + Qwen3.5 35B-A3B + Blackwell cublasGemmGroupedBatchedEx + **TurboQuant quant_policy=42** KV 量化主线第二个推理引擎落地，与用户 RaBitQ/TurboQuant 直连）+ **OpenAI Agents v0.17.1+v0.17.2**（sandbox/tracing/sessions/realtime 多轴加固）+ **LangGraph 1.2.0 全家桶**（6 个 release 一齐 bump，主机崩溃 durable error-handler resume + set_node_defaults + delta channel 强制 snapshot + sqlite streaming walk，1.1 timers revert 后完整收敛）；**blogs**——**NVIDIA Fleet Intelligence**（GPU fleet 级实时观测控制平面）；**community**——hackable 6 IRs LLM 编译器（Qwen2.5-7B 在 5090 跑 1.11× eager / 1.20× compile）/ Gemma 4 MTP vs DFlash on H100 SPEED-Bench 实测（dense 31B 3.11× vs 3.03× 几乎打平）/ Optane PMem 768GB 跑 Kimi K2.5 万亿参数 4 tok/s（CXL/统一内存路线实测信号）/ Speculative KV coding 4× 无损（小模型预测 KV 分布差分编码博客实现）/ VibeServe agent 写 LLM serving 系统（FACT/KernelBenchX 之后 agent 写 infra 升级到 stack 级）/ ubatch=4096 gpt-oss-120B partial offload prefill 380→2090 tok/s（5.5× MoE CPU 卸载推理调优配方）
- 状态: ✅ 成功。papers 严格控在 20 条上限；LMDeploy TurboQuant 落地是用户方向直连最强信号；LangGraph 1.2.0 正式版收敛完成 4/28 revert 之后的完整曲线；arXiv 今日同日 7 篇 KV cache/sparse attn paper（Range Search/KV-RM/Value-Aware/Not All HBM/RDKV/Continuum/SplitZip 母题持续）+ 4 篇投机解码 paper（SPECTRE/Test-Time Spec/Hidden Drift/ReRAM 投机）说明 KV+spec decode 仍是推理基建主流

## 2026-05-13 22:00（周三跑）
- fetch: 52 条 raw（papers 26 / code 15 / blogs 1 / community 10），无 RSS 源失败；blogs 仅 NVIDIA Dev 1 条（其余源时间窗过滤）+ HN LLM/Agent infra 双 0 + r/MachineLearning 0
- curated: 29 条（papers 16 / code 8 / blogs 1 / community 4），按 link 跨分区去重后 papers 唯一 16 条（DisagMoE/ChunkFlow/Power Capping Illusion/ScaleSearch 跨 cs.DC×cs.LG×cs.PF 同 ID 合并）；domain_tag 分布 推理 23 / 训练 3 / agent 3
- render: LLM 摘要 ✓，无 fallback，32 处 CST 时间戳
- publish: commit `05497b9`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +753 行 diff
- 亮点：arXiv 推理侧再次大爆发——**GRIEF**（推理引擎 greybox fuzzer，timed multi-request trace 第一公民，覆盖 KV cache/batching/prefix sharing/spec decode/adapter/多租户调度并发故障）、**AB-Sparse**（每 head 自适应 block size 长上下文稀疏 attn）、**Sieve**（PIM 适配现代 MoE bimodal 专家分布，国产 PIM 接 MoE 直接方法论）、**Power Capping Illusion**（4 attention 架构 H200 decode 仅 137-300W vs 700W TDP，cap 永不触发是错觉，需 SM clock lock 才能拆混淆）、**ScaleSearch**（BFP microscaling scale 细粒度搜索）、**Forecasting MoE Data Movement**（4 个 200B-1000B MoE 24k 请求 profiling 提炼 6 洞见）、**Ada-MK**（自动 DAG 搜索做 MegaKernel 兼顾 portability/efficiency 在 NVIDIA Ada）、**AFD Provisioning**（attn-FFN disagg r-attn-1-FFN 拓扑 stochastic workload analytical sizing）、**Dispatch-Aware Ragged Attn**（ViT pruned ≤197 token，FA-2 varlen / NestedTensor 50µs dispatch 反超 GPU compute；24µs Triton kernel）、**Token Production Function** position paper（推理评测升「能源-token 双天花板」）、**Sparse Attn Remap on PIM**（KV 稀疏聚类映射到 PIM 高内带宽通道）、**NCCLZ**（NCCL 集合通信解耦量化+熵编码无损压缩）、**DisagMoE**（attn/FFN disagg AF-Pipe MoE 训练把 all-to-all 藏进异构池）；code——**TransformerEngine v2.15**（FA4+MXFP8 attention+NVFP4 fused Adam+mHC Triton）、**LMDeploy v0.13.0**（**TurboQuant quant_policy=42 KV 量化主线第二个推理引擎落地**，与用户 RaBitQ/TurboQuant 研究直连；turbomind cublasGemmGroupedBatchedEx Qwen3.5 MoE on Blackwell；Anthropic-compatible serving；Ascend Qwen3.5 35BA3B）、**CUTLASS 4.5.0**（CuTe DSL block_copy + SM120 MXF8/MXF4/MXF6 BlockScaled MMA + EFC mode permutation）、**vLLM v0.21.0rc1+rc2**（CUDA 13 + DeepGEMM 内嵌）、**FA4 beta13**（hd256+Flex varlen blocksparsity+Sm100 backward 2CTA+deterministic）、**LangGraph 1.2.0 全家桶 land**（5 个包同步 bump 至正式版，4/28 timers revert 后 6 个 alpha 完整收敛）、OpenAI Agents v0.17.2、DeepGEMM nv_dev Mega MoE 同步；community——vLLM nightly+dflash+Qwen3.6-27B 长任务停机 bug、RTX 4090 power-limit 砍 60% 性能不变（与同日 Power Capping Illusion paper 实测对照印证完整证据链）、Needle 26M 纯 attention+gating function-calling 模型（tool call 是检索-装配不是 reasoning，FFN 该尺度浪费）、llama.cpp reasoning continue generation
- 状态: ✅ 成功。LMDeploy TurboQuant 是用户方向直连最强信号；arXiv 同日 Power Capping paper + r/LocalLLaMA 4090 实测形成「decode memory-bound → power cap 永不触发」完整证据链；LangGraph 1.2.0 正式版收敛完成 4/28 revert 之后曲线
- 观察：r/MachineLearning 全月持续 0 命中（min_score=6 太高？），后续可考虑微调阈值

## 2026-05-14 22:00（周四跑）
- fetch: 35 raw（papers 16 / code 9 / blogs 0 / community 10），blogs 全 0 + HN LLM/Agent infra 双 0；arXiv cs.LG 492→3、cs.CL 212→1（min_score=6 严格筛工作正常）
- curated: 23 条（papers 9 / code 8 / blogs 0 / community 6），按 link 跨分区去重 papers 唯一 9 条（MMA cs.DC×cs.PF / Lit Silicon cs.DC×cs.AR / MinT cs.DC×cs.LG 合并）；扔 ChipMATE/MARLIN/Hierarchical Transformer/TurboGR 应用层；domain_tag 推理 18 / 训练 3 / agent 2
- render: LLM 摘要 ✓，无 fallback，26 处 CST 时间戳
- publish: commit `11a56895`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +640 行 diff
- 亮点：**KVServe**（disagg serving 服务感知自适应 KV 通信压缩首作）/ **Attention Once**（有状态推理引擎 + Flash Queries 范式）/ **PipeSD**（云边协同投机解码 token-batch pipeline）/ **MinT**（百万 LoRA × 少量 base 部署，覆盖 MLA/DSA frontier MoE）/ **MMA**（软件定义多路径 host-GPU 数据传输，补齐 KV offload PCIe 带宽闲置）/ **ArcLight**（many-core CPU NUMA 感知推理）/ **FlashSampling**（exact 采样融合 LM-head matmul，TP 流式 P2P 替 all-gather）/ **Ada-MK**（DAG 自动搜索 MegaKernel for NVIDIA Ada）/ **Lit Silicon**（多 GPU 训练性能波动 ↔ 热不均耦合 C3 straggler 系统级诊断）；code—**TransformerEngine v2.15**（FA4 + MXFP8 attention + NVFP4 fused Adam + mHC Triton）+ **CUTLASS 4.5.0**（CuTe block_copy + SM120 MXF8/F6/F4 BlockScaled MMA + EFC mode permutation）+ **vLLM v0.21.0rc3 TOKENSPEED_MLA backend for DSR1/Kimi K2.5** + rc2 CUDA 13 cutlass-dsl + **Outlines v1.3.0** 统一 provider 异常 + **FA4 beta13**（hd256 + Flex varlen blocksparsity + SM100 deterministic）+ DeepGEMM nv_dev 同步 Mega MoE；community—MI50 + Qwen 3.6 27B 52.8 tps TG（gfx906 fork ROCm 7.2.1）/ GTX 1080 8GB 跑 30B MoE 24 tok/s（TurboQuant KV K=turbo4 V=turbo3 + MTP draft embedding 锁 GPU 修正）/ opendesk computer-use MCP / NVIDIA Kimi K2.5/K2.6 NVFP4 释出（GPQA 90.4 vs INT4 90.9 无损）/ 5090 power-level benchmark 400W 性能不变（印证 Power Capping Illusion paper）/ Qwen MTP × TurboQuant on M5 Max 64GB +40%（21→34 tok/s 接受率 90%）
- 状态: ✅ 成功。推理 18 偏重是 arXiv 今日推理 paper 集中爆发，训练 3 / agent 2 反映 Megatron/PyTorch/DeepSpeed/LangGraph/AutoGen/OpenAI Agents/MCP Python/XGrammar 全无 release 客观底；Outlines v1.3.0 + opendesk MCP 代表 agent 方向；MMA + Attention Once 同日命中 KV offload + 流式 serving 两条母题
- 观察：HuggingFace Blog 又是 777 项全部时间窗过滤——已连续多日，blogs 源利用率持续偏低

## 2026-05-15 22:00（周五跑）
- fetch: 35 raw（papers 20 / code 5 / blogs 0 / community 10），无 RSS 源失败；blogs 全 0（NVIDIA Dev 100 / Google Research 100 / HF 779 / Together AI 100 全部时间窗过滤）+ HN LLM/Agent infra 双 0 + r/MachineLearning 0
- curated: 20 条（papers 12 / code 4 / blogs 0 / community 4），按 link 跨分区去重 papers 唯一 12 条（ECHO cs.DC×cs.LG / SD latency cs.PF×cs.LG / PreFT cs.LG×cs.CL / Apple MPS cs.AR×cs.PF 合并）；扔 Mat2Boundary（PDE 应用层）+ Hierarchical Transformer（物理仿真）+ VectraYX-Nano（西语网安 SLM 训练非 infra）+ EMA（网络仿真 ML 非 LLM infra）；domain_tag 推理 18 / 训练 0 / agent 2
- render: LLM 摘要 ✓，无 fallback，23 处 CST 时间戳，source=today_curated.json
- publish: commit `99593fed`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +583 行 diff
- 亮点：**vLLM v0.21.0 正式版**（367 commits/202 contributors，本月最强 release——正式 deprecate Transformers v4 + 编译升 C++20 + KV Offload×HMA 完整融合 + 投机解码尊重 reasoning/thinking budget + Blackwell TOKENSPEED_MLA backend；v0.20.x「feature 落地即 revert」节奏后第一个完整收敛正式版）+ v0.21.0rc3 TOKENSPEED_MLA for DSR1/Kimi K2.5 + v0.21.1rc0 ROCm CI hotfix；arXiv 推理侧密集爆发——**ECHO**（SGLang 集成投机解码预算调度，sparse confidence gating + super-tree 弹性管理高并发 verification compute-bound）/ **PipeSD**（云边协同 SD token-batch pipeline + 自适应 NAV 触发）/ **Multi-Scale Dequant MSD**（Ascend NPU 把 dequant 移出 GEMM 关键路径，BF16 激活拆低精度分量）/ **SD latency model**（Little 定律推 batch + load-aware 分量分解，何时启用 SD 量化决策面）/ **PreFT**（多 adapter serving prefill-only 应用 adapter，绕开 decode 退化）/ **TLX**（Triton Low-level Language Extensions × MIMW warp-group 编排）/ **XFP**（quality-targeted 自动量化 codebook + outlier budget，Qwen3.5-122B-A10B）/ **Apple MPS decode 21× 非单调延迟**（仅 decode 不仅内存压力，CUDA 后端无）/ **EnergyLens**（einsum 接口多 GPU 能耗预测）/ **Pythia**（agent-native serving 利用 workflow 可预测性）/ **Optimizing PyTorch Inference w/ Multi-Agent**（exploit-heavy + error-fixing agents 组合写 GPU kernel 最优）/ **SOP per-layer LUT PTQ**（4.5-6 bpw 近无损 + HIF 输出格式）；code—FlashInfer v0.6.11.post2；community—**2×2080 Ti 22GB Qwen3.6 27B IQ4_XS+f16 KV+MTP 38 tok/s @ 150W**（power-limit 砍半性能不变，再次印证 decode memory-bound）+ **Qwen3.6 27B INT8 AutoRound 部分层 BF16 思考更少答案更准**（reasoning 模型量化对关键层 BF16 留白敏感）+ **DSV4-Pro 单卡 RTX PRO 6000 Max-Q + KTransformers/sglang+kt-kernel pp512=39.76 / tg32=7.54**（继 5/10 antirez 之后第二个家用单卡 V4-Pro 案例）+ **TurboQuant 首份系统对比**（FP8 仍是默认最优，4bit-nc 边缘部署最实用，与 5/13 LMDeploy quant_policy=42 落地形成完整外部独立评估闭环）
- 状态: ✅ 成功。推理 18 偏重是 arXiv 今日推理 paper 集中爆发 + vLLM v0.21.0 正式版双轴客观主导；训练 0 是 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS 全无 release 客观底（与 5/10、5/6 周日同样状况）；严格排除 Pi rm-rf 梗、SupraLabs 创业贴、Cola DLM/Intern-S2 模型发布、China modded 4090 硬件咨询、self-train math 论文实验贴等非基础设施内容
- 观察：vLLM 完整收敛曲线——5/2 v0.20.1 revert persistent topk → 5/10 v0.20.2 重启 → 5/13-14 v0.21.0rc1/rc2/rc3 → 5/15 v0.21.0 正式版 + 当日 v0.21.1rc0 ROCm hotfix；TurboQuant 用户方向连续命中第三天（5/13 LMDeploy 落地 + 5/15 r/LocalLLaMA 系统对比）

## 2026-05-17 22:00（周日跑）
- fetch: 13 raw（papers 0 / code 3 / blogs 0 / community 10），无 RSS 源失败；周日 arXiv 不更新（papers 0）+ blogs 全 0（HF 779/NVIDIA Dev 100/Google 100/Together 100 时间窗全过滤）+ HN LLM/Agent infra 双 0 + r/ML 0；code 仅 SGLang v0.5.12（重磅）+ FlashInfer 两条无 changelog nightly
- curated: 6 条（papers 0 / code 1 / blogs 0 / community 5），domain_tag 推理 6 / 训练 0 / agent 0——训练/agent 双 0 是今日 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS/LangGraph/AutoGen/OpenAI Agents/MCP Python/XGrammar/Outlines 全无 release 客观底
- render: LLM 摘要 ✓，无 fallback，9 处 CST 时间戳，source=today_curated.json
- publish: commit `5340e6a`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +318 行 diff
- 亮点：**SGLang v0.5.12** DeepSeek V4 Day-0 完整推理路径——TP/EP/CP/DP attention 全 parallelism + B300/B200/H200/H100/GB200/GB300 + AMD MI35X 全栈 + PD 分离 + HiSparse KV cache CPU 卸载 + DeepGEMM/FlashMLA/MegaMoE kernel；Day-0 后又补齐 UnifiedTree HiCache、W4A4 MegaMoE（无损精度）、Hopper Marlin/FlashInfer W4A8 MoE、V2 fused 压缩、H100/H20 TP16、fused SiLU+clamp+FP8——继 KTransformers/DS4(antirez)/LMDeploy 之后**第四个 V4 系列推理引擎完整工程化落地**；**llama.cpp MTP merge 后多平台实测大集合**——5/16 PR #22673 合并入 master 后，今日 r/LocalLLaMA 一日内放出 4 份独立硬件实测：5090 32GB（首发 Blackwell 单卡基线，需 CUDA_DOCKER_ARCH=120 自构 docker）+ 3090 24G（PP 1050→600 -42% / TG 27→50 +85%，85k 任务 39→23 分钟 1.7×，OpenCode 实战）+ 3090Ti（首份 n_max 深度扫描——MTP1 1.28×@95.5% / MTP2 1.79×@91.3%）+ RTX 3060 Laptop 6GB（不值得开，PP 退化压过 TG 收益，副产物：draft KV q4_0 与 q8_0 等效省 VRAM）；MTP 工程曲线至此完整闭环——5/4 KTransformers 首发 → 5/6-7 多平台实测 → 5/11-13 系统 benchmark 出「文本熵决定加速比」结论 → 5/16 llama.cpp master 合并 → 5/17 一日内多硬件档实测出齐
- 状态: ✅ 成功。6 条是周日客观信号底（papers 0 + blogs 0 + HN 双 0 + code 仅 1 强信号），严格执行「宁缺毋滥」——排除 G4-Meromero finetune（应用层）、Qwen 3.6 vs frontier coding canvas（应用层评测对比）、Qwopus3.5-9B-Coder finetune（应用层）、FlashInfer 两条 nightly（无 changelog）、3 条 MTP merge 祝贺贴合并成 1 条
- 观察：MTP 工程化下沉曲线在 5/17 形成完美收口——单日内同主题 4 份独立实测覆盖消费卡全档（6GB Laptop / 3090 / 3090Ti / 5090），是基础设施 feature 「文档级用户验证」最理想的形态

## 2026-05-16 22:00（周六跑）
- fetch: 23 raw（papers 7 / code 5 / blogs 0 / community 11），无 RSS 源失败；arXiv cs.AR/cs.PF/cs.LG/cs.CL/cs.OS 全 0，仅 cs.DC 7 篇；code 大批仓库时间窗过滤（TRT-LLM/TE/Megatron/CUTLASS/SGLang/LMDeploy/Mooncake/KTransformers/DeepSpeed/PyTorch/Triton/LangGraph/AutoGen/OpenAI Agents/MCP Python/XGrammar/Outlines 全空），仅 vLLM 2 + FlashInfer 3；blogs 全 0（HF 779 / NVIDIA Dev 100 / Google 100 / Together 100 全时间窗过滤）；HN LLM/Agent infra 双 0
- curated: 11 条（papers 4 / code 3 / blogs 0 / community 4），domain_tag 推理 9 / 训练 0 / agent 2；扔 EMA（ML 网络应用层）+ Mat2Boundary（PDE 应用层）+ Hierarchical Transformer（物理仿真）+ Jetson Sparky/Opencode/动态 budget HLE（agent 应用层 + 闲聊）
- render: LLM 摘要 ✓，无 fallback，14 处 CST 时间戳，source=today_curated.json
- publish: commit `db6f7c5`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +412 行 diff
- 亮点：papers 今日基本全是 v2 replace（ECHO/PipeSD/Optimizing PyTorch Multi-Agent/Pythia 昨日已覆盖，今日以 v2 增量视角再写）；code 侧 vLLM v0.21.0 正式版（核心信号延续）+ v0.21.1rc0 ROCm CI 紧随 + FlashInfer v0.6.11.post3 滚动；community 真正强信号是 **llama.cpp MTP PR #22673 正式 merge 进 master**（含 Qwen3.6-27B-MTP / Qwen3.6-35B-A3B-MTP GGUF 释出，自 5/4 周追踪的 MTP 工程化下沉事件链至此完整收口）+ **Orthrus-Qwen3 系列**（冻结 AR + 注入 diffusion attention，两路 head 共享 KV cache，7.8× TPF 输出分布等价证明，定位「base 内嵌 drafter」新一类投机解码范式，与 EAGLE-3/DFlash 不需外部 drafter）+ **Open-dLLM × Qwen3.6 5090 探路**（agent 写 infra 隔夜级证据延续）+ **RTX power-limit 实测**（再次印证 5/13 Power Capping Illusion paper，本周第三起独立社区验证）
- 状态: ✅ 成功。11 条是周六客观信号底（arXiv 5/6 分区 0 + code 17 仓库全空 + blogs 全 0 + HN 双 0），严格执行「宁缺毋滥」；训练 0 是 Megatron/PyTorch/DeepSpeed/TransformerEngine/CUTLASS 全无 release 客观底（与 5/10 周日同样状况）
- 观察：MTP 工程曲线完整闭合——5/4 KTransformers 首发 → 5/6-7 Qwen3.6-27B 多平台实测 → 5/11-13 系统 benchmark 出「文本熵决定加速比」结论 → 5/16 llama.cpp master 合并；Orthrus 提供与 MTP/EAGLE/DFlash 正交的「base 内嵌 drafter 等价」第四条投机解码范式

## 2026-05-07 22:00（周四跑）
- fetch: 42 条 raw（papers 20 / code 10 / blogs 1 / community 11），无 RSS 源失败；blogs 仅 HuggingFace 1 条（ServiceNow vLLM V0→V1 RL correctness）+ HN LLM/Agent infra 双 0
- curated: 26 条（papers 13 / code 8 / blogs 1 / community 4），按 link 去重后 papers 唯一 13 条（扔 HERCULES NAS——"Outlines" 关键词误捕 + Serverless LEO 应用层）；domain_tag 分布 推理 14 / 训练 6 / agent 6
- render: LLM 摘要 ✓，无 fallback，CST 时间戳齐全
- publish: commit `3309709`，HEAD==origin/main，2026/05 + archive 两份 HTML 各 +696 行
- 亮点：**papers 推理爆发**——FASQ（PQ 搬 LLM 权重，免校准连续 27-49% 过 4-bit GPTQ/AWQ）/ KernelBench-X（176 任务测 LLM 写 Triton，task 结构比方法设计重要 3×）/ HELM（生成式推荐 HBM 分配 PPO 三层控制，EMB/KV 最优比跨 workload 0.35）/ Coral（多 LLM×异构 GPU serving 联合优化无损两段分解）/ Microbench 解析模型（B200+MI300A MAE 1.31%/0.09% vs roofline 95%+）/ GRACE-MoE（EP 分组+动态复制+locality 路由）；**训练**——Piper（MoE 训练 cost model + pipeline 混合并行）/ MRC+SRv6（OpenAI+MS 10万+GPU 生产 RDMA 多路径+multi-plane Clos）/ CCL-D（CCL 慢/hang 秒级诊断）；**agent**——KEET（Nsight Compute profile → LLM agent 解释）/ phys-MCP（MCP 外溢到 PNN 编排）/ AgenTEE（edge LLM agent TEE）；**code**——TRT-LLM v1.3.0rc14（Mamba 混合 prefix caching+Qwen3.5 MoE）/ Megatron 26.04-alpha.rc2（MXFP8 param gather eval）/ DeepSpeed v0.19.0（Zero3 defragment+PyTorch 2.9/2.10 兼容）/ OpenAI Agents v0.16.0（默认切 gpt-5.4-mini + max_turns=None）+ v0.16.1 次日 7 项补漏 + v0.15.3 MCP 加固 / FA4 beta12 hd256 全链路 / FlashInfer v0.6.10.post1；**blogs**——ServiceNow vLLM V0→V1 RL correctness checklist；**community**——Qwen3.6-27B MTP 合并代表两条（M2 Max 96GB 2.5× / 3090 Ti 35B-A3B 150 tok/s）/ ParoQuant（pairwise rotation 压缩离群值，与 TurboQuant per-vector min-max 正交）/ Transformer Math Explorer（GPT-2→Qwen3.6 交互 dataflow 工具）
- 状态: ✅ 成功。推理 14 偏重是 arXiv 今日客观事实；cs.LG 379 过 3、cs.CL 132 过 0，分区 min_score 工作正常
- 观察：HERCULES NAS 被 "Outlines" 命中是 false positive——后续建议 `\bOutlines\b` 精确正则避免子串误匹配




## 2026-05-18 22:00（周一）
- fetch: 29 条 raw（papers 15 / code 3 / blogs 0 / community 11），无 RSS 源失败；周末/blogs 0 是常态
- curated: 16 条（papers 9 / code 2 / blogs 0 / community 5），domain_tag 推理 11 / 训练 3 / agent 2
- render: `LLM 摘要 ✓`，无 fallback，CST 19 处，source=today_curated.json
- publish: ⚠️ 系统 git.exe 已卸载（PATH 残留 `D:\Downloads\Git\cmd`），publish.py 报 FileNotFoundError；改用 scripts/_dulwich_publish.py（dulwich + 系统 OpenSSH + id_rsa）兜底
- commit `cc5de01`，HEAD == origin/main（dulwich.ls_remote 校验），2026/05 + archive 两份 HTML 各 +487 行
- 亮点 paper：TurboMind（LMDeploy 混精度全栈）、CascadeInfer（length-aware serving 重调度）、GQLA（MLA→GQA 双路径解码权重）、DualKV（GRPO RL prompt-shared FlashAttention）、MoE-Prefill（prefill 零冗余）、Adaptive Speculative（speculator 训-服合一）、Asteria（二阶优化器 NVMe offload）、BatchWeave（object-store 训练 dataloader）、WAIT（fluid KV 调度）；code 弱：XGrammar v0.2.1（Kimi/Qwen tool-call grammar）+ FlashInfer 0.6.11 nightly；community：Qwen3.6-27B 24GB ik_llama.cpp 三连 + MTP draft KV 量化 + M5 vs DGX Spark + SmallCode 4B agent harness
- 状态: ✅ 成功（带⚠️ git 工具失效，长期需用户修复）

## 2026-05-19 22:00（周二）
- fetch: 45 条 raw（papers 28 / code 3 / blogs 0 / community 14），无 RSS 失败源；blogs 全 0 + HN 双 0
- curated: 21 条（papers 15 / code 2 / blogs 0 / community 4），按 link 跨分区去重 papers 唯一 15 条（OSCAR cs.DC×cs.PF×cs.LG / VeriCache cs.AR×cs.LG / AgentKernelArena cs.LG×cs.CL 合并）；domain_tag 分布 推理 15 / 训练 2 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，24 处 CST 时间戳
- publish: ⚠️ 系统 git.exe 仍未恢复（连续第二天），继续走 scripts/_dulwich_publish.py 兜底
- commit `09672ab1`，HEAD == origin/main（dulwich.ls_remote 校验），2026/05 + archive 两份 HTML 各 602 行（新增文件）
- 亮点：**arXiv KV cache/量化方向同日 6 篇集中爆发**——OSCAR（INT2 KV 旋转 + attention covariance 离线估计 + 部署级 INT2 attention kernel）/ **VeriCache（首个无损 KV 压缩推理框架，压缩 KV 当 drafter + 完整 KV verify 比特等价 full KV decode，把 lossy 套进可验证投机解码壳）** / TriAxialKV（agent 推理三轴异质 KV 量化）/ Protection-Capped KV Eviction（7 大策略共有 prompt-boundary 漏洞，10% boundary 保留即恢复 69-90% 质量；本质在「保护」不在「打分」）/ KVDrive（GPU/host/SSD 三层 KV 管理）/ DashAttention（α-entmax 可微稀疏分层注意力）；agent serving——HexAGenT/GoodServe/S-Bus（多 agent NL state race condition + Observable-Read Isolation）；训练——JanusPipe（MLIP 双反向 PP）/ RRFP（PP readiness-driven runtime）；硬件——FP8 DCIM / Hawkeye GPU 非确定性 CPU 比特复现 / MLIR Arm SVE VLA codegen；agent 写 kernel——AgentKernelArena 196 任务测完整 agent workflow；code 弱——OpenAI Agents v0.17.3 一波 11+ fix 进入「补漏期」+ FlashInfer 0.6.11 nightly；community——CUDA kernel 重写 small-batch runtime（机器人/VLA non-GEMM 瓶颈清单）/ Qwen 3.6 27B F16 vs Q8 实测（Q8 不是无损）/ LangGraph 组织级三类 agent 实战 / llama.cpp MTP PR #23269 工程化下沉延续
- 状态: ✅ 成功（带⚠️ git 工具失效）
- 观察：VeriCache 首次把「无损」作为 first-class goal 引入 KV 压缩，是新范式起点；OpenAI Agents v0.17.3 接续 v0.17.0-v0.17.2 sandbox 加固，本月 agent SDK 进入安全边界收紧的「补漏期」

## 2026-05-20 22:00（周三）
- fetch: 40 条 raw（papers 24 / code 3 / blogs 1 / community 12），无 RSS 失败源；code 几乎全空（17 仓库 time 过滤，仅 FA4 beta14 + FlashInfer 2 nightly）
- curated: 20 条（papers 13 / code 1 / blogs 1 / community 5），按 link 跨分区去重 papers 唯一 13 条（PiKV cs.DC×cs.AR / Inference Scaling cs.DC×cs.PF / Fiber Latency cs.DC×cs.PF 合并）；扔 1GC-7RC（agent 应用层）+ TideGS（3DGS 应用）+ Quantum Sensor / Bitcoin V2 / CausalMesh / Near-Memory GNN（非 LLM infra）；domain_tag 分布 推理 14 / 训练 2 / agent 4
- render: `LLM 摘要 ✓`，无 fallback，23 处 CST 时间戳，source=today_curated.json
- publish: ⚠️ 系统 git.exe 仍未恢复（连续第三天），继续 dulwich 兜底
- commit `8c6be264`，HEAD == origin/main（dulwich.ls_remote 校验），2026/05 + archive 两份 HTML 各 +582 行
- 亮点：**arXiv GH200/GB200 NVLink-C2C 推理两连**——**C2CServe**（serverless MIG + 模型权重常驻 CPU 内存按需流式推 MIG slice，绕开「单 slice HBM 不够」与「时间切片冷启动」两难，国产 ScaleUp 统一内存 serverless 推理设计直接参考）+ **SuperInfer**（NVLink-C2C 紧耦合 Superchip 上 RotaSched 主动 SLO-aware KV 迁移 vs PCIe LRU offload）；**Silent Hyperparameter**（200 inference engine + 35000 论文调研，呼吁 inference backend 列为 first-class reproducibility 字段，对位 5/13 GRIEF greybox fuzz）；**SpecSA**（投机解码×动态稀疏 attention 首次工程兼容范式，延续 5/12 SPECTRE / 5/14 PipeSD / 5/15 ECHO 投机解码母题）；**Inference Scaling for Reasoning**（reasoning workload 彻底进 Capacity-Bound regime，与传统 scaling 反向结论）；**SAECache**（prompt 五类 token 复用率差 756×，语义感知 prefix eviction 首作）；**KVBuffer**（linear attention IO-aware serving）；**OScaR**（per-channel KV 量化失效根因 Token Norm Imbalance，与 5/19 OSCAR 命名撞车注意区分）；**PiKV**（MoE expert-sharded KV）；**Multi-Model Schedulers**（多模型异构硬件 offload+preempt 实证）；**GEM**（GPU variability 一等输入 MoE expert mapping，与 5/14 Lit Silicon 热不均同源）；**DynaTrain**（VPS 抽象 sub-second 在线并行重配，训练侧弹性答卷）；**MTraining**（动态稀疏 attention 训练 ultra-long ctx，cs.LG 推理稀疏 attn 母题落训练栈）；code 仅 **FA4 beta14**（zero-length 序列 / empty Q workload / Flex+SM90 边界补漏期）；blogs **NVIDIA Verified Agent Skills**（agent capability governance + MCP 能力签名，安全边界从 sandbox 上推到能力层）；community **RTX 5080 16GB Qwen3.6 35B-A3B MoE @128k 56 tok/s + MTP 在 128k 不再起作用**（MTP 工程化下沉最后一块拼图：长 ctx 边界）/ **LM Studio 0.4.14 加 MTP** 第一个主流桌面 GUI 跟进 / **Google AI Edge Gallery v1.0.13+1.0.14**（Gemma 4 MTP + Pixel TPU + 实验性 MCP + skill 系统，移动端三母题集中落地）/ Cursor cloud agent dev env / Atlassian MCP RFC 9728 audit
- 状态: ✅ 成功（带⚠️ git 工具失效连续 3 天）
- 观察：C2CServe + SuperInfer 同日命中 GH200/GB200 NVLink-C2C 推理母题，与 5/2 Strix Halo / 5/9-10 DGX Spark unified memory 实测形成完整 ScaleUp 证据链；MTP 工程化下沉曲线完整闭环（5/4 KTransformers → 5/16 llama.cpp merge → 5/17 多硬件实测 → 5/20 LM Studio+移动端+长 ctx 边界），覆盖 cloud→edge 全栈；agent 安全边界母题持续（5/17 MCP Python / 5/19 OpenAI Agents v0.17.3 / 5/20 NVIDIA Verified Skills + Atlassian MCP audit，agent SDK 进入「协议合规审计期」）
- 待修：`_dulwich_publish.py` commit message 仍硬编「2026-05-18」（实际 5/20），后续改为动态 CST today；长期 TODO 用户修复 Git for Windows 让原生路径恢复

## 2026-05-21 22:00（周四）
- fetch: 47 raw（papers 22 / code 3 / blogs 1 / community 21），无 RSS 失败源；blogs 几乎全 0（HF 783/Google 100/Together 100 全过滤）
- curated: 20 条（papers 13 / code 1 / blogs 1 / community 5），跨分区去重 papers 唯一 13；domain_tag 推理 16 / 训练 1 / agent 3
- render: LLM 摘要 ✓，无 fallback，23 处 CST 时间戳
- publish: ⚠️ git.exe 仍未恢复（连续第四天）走 dulwich 兜底；commit `048c8927`，HEAD == origin/main，2026/05 + archive 两份 HTML 各 +582 行
- 亮点：Frontier 推理仿真器 / NanoCP 请求级动态 CP / SSV 投机解码×动态稀疏 attn 工程兼容 / Silent Hyperparameter（200 引擎调研呼吁 backend 列入 first-class 复现性）/ DODOCO MoE all-to-all 假设实证检验 / PALS GPU power cap 升一等可控旋钮集成 vLLM / Runtime-Certified KV 量化误差证书 / **OCTOPUS（续 TurboQuant/PolarQuant rotation-preconditioned KV codec，八面体参数化联合量化坐标三元组——用户方向直连最强信号）** / OFU GPU fleet 效率指标 / LlamaWeb WebGPU 浏览器推理 / TokenCake multi-agent KV serving / PulseCol dLLM 列稀疏 attn / FA4 beta14 / NVIDIA Deep Research Skill on Agent Harnesses / ik_llama.cpp 12GB 110 tok/s（MTP 主线合并后反退、ik 分支重新生效，MTP 工程化下沉新拐点）/ Doubleword「请求按 expert 共激活重排序，MoE load 不均 -15%」生产捷径
- 已修：`_dulwich_publish.py`/`_dulwich_verify.py` commit message + HTML 路径都改成动态 CST today，根除硬编日期 bug
- 状态: ✅ 成功（带⚠️ git 工具失效连续 4 天，长期 TODO 用户修复 Git for Windows）

## 2026-05-22 22:00（周五）
- fetch: 36 raw（papers 14 / code 6 / blogs 3 / community 13），无 RSS 失败源；arXiv cs.LG 419→3 / cs.CL 163→2（min_score=6 严格筛工作正常）；code 24 仓库仅 4 命中
- curated: 18 条（papers 7 / code 4 / blogs 2 / community 5），跨分区去重 papers 唯一 7（AVMP cs.DC×cs.PF / HealthCraft cs.LG×cs.CL 合并）；扔 FlashSinkhorn/ORBIS/Tyche/HealthCraft/VectraYX-Nano 等应用层；community 大量 Qwen workflow/DeepSeek 融资/硬件咨询丢；domain_tag 推理 13 / 训练 2 / agent 3
- render: LLM 摘要 ✓，无 fallback，21 处 CST 时间戳，source=today_curated.json
- publish: ⚠️ git.exe 仍未恢复（连续第五天）走 dulwich 兜底；commit `bcea8b6d`，HEAD == origin/main，2026/05 + archive 两份 HTML 各 +544 行真实 diff
- 亮点：**AVMP**（Mamba+Transformer 混合架构推理双 cache 异构虚拟分页 7.3× 显存节省，命中用户 vLLM × Hybrid Mamba+Attention KV 工程方向）/ **WarmServe**（多 LLM 共享 GPU 集群一对多 prewarming）/ **Flashlight**（PyTorch 编译器原生自动生成 FlashAttention-like 融合 kernel 覆盖整族 attention 变体）/ **LiveR**（弹性训练 live reconfiguration 替 ckpt restart，与 5/20 DynaTrain 同期不同思路答卷）/ **Dooly v2**（推理仿真器跨配置共享 op profile，配 5/13 GRIEF/5/19 Hawkeye/5/21 Silent Hyperparameter 同母题）/ **InnerQ**（硬件感知免调优 KV cache group-wise 量化，延续 RaBitQ/TurboQuant/OCTOPUS 母题）/ **DynaFlow**（intra-device 并行可编程 op 调度抽象）；code—TRT-LLM v1.3.0rc15（Gemma4/Kimi K2.5/DSV4 全打磨）/ Triton 3.7 正式 / LangGraph 1.2.1 续 1.2.0 后首个 patch / OpenAI Agents v0.17.3 11+ fix 「补漏期」；blogs—NVIDIA GB200 NVL72 Slurm topology-aware 调度 + K8s 集群级 GPU 实时可观测；community—llama.cpp 非对称 KV 量化 PP 回退 CPU 解法（异步 8/4 bit 仅 1.3% 精度损失）/ llama.cpp b9274 修 MTP VRAM leak（MTP 工程化下沉曲线进入「生产稳定性补漏」新阶段）/ OpenBMB BitCPM-CANN 1.58 bit 在昇腾 910B 跑通（BitNet 国产 NPU 信号点）/ Vibedock macOS 切 Claude Code MCP 开关（MCP 走到桌面 capability governance UX 化）/ lemon-mlx-engine 集成 ROCm 7.13
- 状态: ✅ 成功（带⚠️ git 工具失效连续 5 天，长期 TODO 用户修复 Git for Windows）
- 观察：AVMP 命中用户 Hybrid Mamba+Attention KV 方向最强信号；MTP 工程化曲线进入生产稳定性补漏阶段

