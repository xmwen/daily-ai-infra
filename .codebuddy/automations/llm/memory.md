# 自动化执行历史 - 每日 LLM 推理与训练动态看板

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
