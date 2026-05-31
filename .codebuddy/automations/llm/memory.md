# 自动化执行历史 - 每日 LLM 推理与训练动态看板

## 2026-05-30 22:00（周六）
- fetch 25 raw（papers 0 / code 6 / blogs 1 / community 18，周末 arXiv 停更）/ curated 9 / render LLM 摘要 ✓ no fallback / publish 走 dulwich 兜底（git.exe 连续第 13 天失效），当日 HTML commit `5575d314`（HEAD~1），HEAD `1d8144d5` == origin/main，HEAD~1 +882 -5 行真实 diff，2026/05/2026-05-30.html + archive/2026-05-30.html + 12 处 CST + 10 处 domain-tag pill
- domain_tag 推理 8 / 训练 0 / agent 1（papers 0 / code 3 / blogs 1 / community 5）
- 周末分量轻属正常，按宁缺毋滥纪律：弃掉 4 条 GPU 选购/散热讨论 + 角色扮演模型 + IBM Quantum 噱头 + Codex 替代问询 + 8GB 训 25M tinystories 等应用层/玩具
- 亮点：vLLM v0.22.0 正式版（DeepSeek V4 单独包 + NVFP4 fused MoE + full/piecewise CUDA Graph + MTP）/ FlashInfer v0.6.12（SM120 W4A16 b12x MoE + Kimi K2.5 MLA + CUTLASS MLA paged FP8）/ MCP Python v1.27.2（transport session 绑 principal + experimental task scope，agent runtime 多租户硬化）/ NVIDIA DynoSim Pareto 模拟器/ **KOG.ai 三连**（MI300X monokernel 3300 tok/s + Delayed TP + Real-time 3K tok/s 总览，latency-first 推理派的整套方法论，HN 双热帖 167+205 分）/ Tiny-vLLM 教学实现 / Qwen3.6-27B GGUF 量化 KLD + Same-Top-P 双指标横评
- 踩坑：verify 脚本最初 `from _dulwich_publish import open_ssh_client` 触发模块顶层 publish 副作用，又跑了一次 dulwich.push（只 stage 了 verify 脚本本身，造成 HEAD `1d8144d5` 这个小补丁 commit）。当日 HTML 真实落在 HEAD~1 `5575d314`，两个 commit 都已推到 origin/main，HEAD == origin/main 校验通过，看板内容正确。后续若再用 dulwich 校验，**不要 import publish 脚本**。
- 状态: ✅ 成功（带⚠️ git 工具失效连续 13 天，长期 TODO 用户修复 Git for Windows；带💡 verify 脚本误触发 publish 副作用已规避）

## 2026-05-28 22:00（周四）
- fetch 53 raw / curated 32 / render LLM 摘要 ✓ no fallback / publish 走 dulwich 兜底（git.exe 连续第 11 天失效），commit `0ab7e97d`，HEAD == origin/main，2026/05 + archive 各 +810 行真实 diff，35 处 CST
- domain_tag 推理 29 / 训练 3 / agent 0（papers 14 / code 9 / blogs 1 / community 8）
- agent 0 是合规结果：今日 HN Agent infra 全部命中 MCP 应用层（颜色档案/SEO Skill/jensenify/favorite MCP 调研），无 agent 系统基础设施类内容，按筛选纪律全弃，宁缺毋滥
- 亮点：arXiv MoE serving 三连（AFD 设计空间 / SiDP DP 共享权重换大 batch / GQLA 让 MLA 权重等价暴露 MQA-absorb + GQA per-group expand 双解码路径解 H20 适配） / FCDC 铁电 PIM attention 全替换 + KV 协处理两模式 / Hurwitz 24-cell 四元数 KV 量化 / OpenURMA UB 协议 clean-room 实现（华为 Unified Bus 替 RDMA QP-over-PCIe）/ NVIDIA Blackwell STAC-AI 金融推理纪录 / TritonMoE 89-131% Megablocks 跨 NV+AMD 零改动 / Zai 千卡 GLM-5.1 集群 ZCube 网络替 ROFT（PD 解耦推理流量优化，吞吐 +15%、P99 -40.6%、成本 -33%）/ NVIDIA SOL-ExecBench AI 生成 CUDA kernel 在真实分布下 silently 破坏训练（fused embed-grad+RMSNorm 案例）/ DeepSpeed v0.19.1 ZeRO-3 走 mori SDMA allgather + Evoformer CUTLASS auto-detect / CUTLASS 4.5.1 Blackwell 低延迟 GQA paged KV + UE8M0 / FA4 beta15 sm_110 Blackwell-family 收口 / vLLM 0.22.0rc1-rc3 三连补丁
- 状态: ✅ 成功（带⚠️ git 工具失效连续 11 天，长期 TODO 用户修复 Git for Windows）

## 2026-05-27 22:00（周三）
- fetch 43 raw / curated 23 / render LLM 摘要 ✓ no fallback / publish 走 dulwich 兜底（git.exe 连续第 10 天失效），commit `10dc0111`，HEAD == origin/main，2026/05 + archive 各 +639 行真实 diff，26 处 CST
- domain_tag 推理 16 / 训练 2 / agent 5（papers 10 / code 7 / blogs 3 / community 3）
- 亮点：NVIDIA CUDA 13.3 + Tile programming in C++ + CompileIQ Auto-Tuning 三连（NVIDIA 官方 tile DSL 路线 vs 开源 TileLang v0.1.10 双栈对照） / TRT-LLM v1.3.0rc16 多模态 KV reuse + KV manager v2 + sharding-IR canonical / SGLang v0.5.12.post1 V4 cherry-pick（MTP × disagg KV pool 边界 bug 修复） / Llama-3.1 全家族量化系统评测（FP8 无损 / INT8 1-3% / W4A16 与 8bit 持平） / agent serving 实证两连（Stateful Inference + Agentic Workload Char） / Triton MoE 89-131% Megablocks 跨 NVIDIA+AMD 零改动 / OpenAI Agents v0.17.4 + LangGraph 1.2.2 + checkpoint 4.1.1 SDK 补漏期持续 / 100MW AI Cluster v2 + ECHO-2 distributed RL bounded staleness / Cassandra edge reasoning + ReMoE router fine-tuning
- 状态: ✅ 成功（带⚠️ git 工具失效连续 10 天，长期 TODO 用户修复 Git for Windows）

## 2026-05-26 22:00（周二跑）
- fetch 53 raw / curated 28 / render LLM 摘要 ✓ no fallback / publish 走 dulwich 兜底（git.exe 连续第 9 天失效），commit `3b8f3777`，HEAD == origin/main，2026/05 + archive 各 +735 行真实 diff
- domain_tag 推理 19 / 训练 3 / agent 6（papers 16 / code 4 / blogs 0 / community 8）
- 亮点：TileLang v0.1.10 真正完成「NV+AMD+Apple+老卡」一统 tile DSL；arXiv 同日 4 篇 KV cache/sparse attention paper（Adaptive Reuse / IndexMem / Resident KV Claims / Context Sparsity Position）；agent 方向今日命中较多（Polar agentic RL on any harness + Spice decision layer + SkillOpt + Operational Docker MCP + EAGLE 3.1 vLLM × TorchSpec）；TRT-LLM v1.3.0rc16 多模态 + Qwen3.5 MTP + sharding-IR canonical + KV manager v2 + disagg block reuse；FlashInfer v0.6.12rc1 SM120 W4A16 b12x MoE + Kimi K2.5 MLA decode + CUTLASS MLA paged FP8；antirez DwarfStar HN 多次置顶；Strix Halo PR #21344 给 MoE PP +30%
- 状态: ✅ 成功
