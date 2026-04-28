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
