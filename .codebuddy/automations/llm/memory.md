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
