# AI Infra / LLM / Agent 系统每日动态

每日 **22:00（北京时间）** 由 WorkBuddy Automation 自动执行：拉取 RSS → Agent 手写中文 tldr 精筛 → 渲染 HTML 日报 → 推送到本仓库触发 GitHub Pages。

**在线看板**：https://xmwen.github.io/daily-ai-infra/

## 内容方向

聚焦**系统基础设施层**，分量参考：推理 ~60% / 训练 ~25% / Agent 系统 ~15%，curated 上限 ≤25 条。

- 📄 **重点论文**：arXiv cs.DC / cs.AR / cs.PF / cs.LG 的推理/训练/系统方向
- 🚀 **代码更新**：vLLM / SGLang / TensorRT-LLM / Megatron-LM / CUTLASS / DeepGEMM / FlashInfer / PyTorch / Triton / LLVM / LangGraph / AutoGen / OpenAI Agents / MCP SDK / XGrammar / Outlines 等
- 📝 **技术博客**：NVIDIA / PyTorch / Meta Eng / Google Research / HuggingFace / LangChain / Anthropic
- 💬 **社区热议**：HN LLM infra、HN Agent infra（MCP / LangGraph / tool use / Claude Code 专搜）、r/LocalLLaMA、r/MachineLearning

**Agent 方向的筛选规则**：只看 agent 系统基础设施（调度算法 / 协议 / runtime / 结构化输出 / 沙箱 / tracing），**不看** agent 应用案例 / 能力排行榜 / 客服 & 写周报类 demo。

**用户视角重点话题**：ScaleUp 统一内存引擎、MoE kernel 重叠、DeepGemm、FlashAttention、MLIR、PIM、NURBS 光追、昇腾/寒武纪/摩尔线程等国产芯片、MCP、LangGraph、Claude Code / Cursor / Devin 等 coding agent 系统设计。

## 目录结构

```
daily-ai-infra/
├── index.html           # 看板首页（最新一期 + 历史归档索引）
├── latest.html          # 跳转到最新一期
├── YYYY/MM/             # 按月组织的历史日报
│   └── YYYY-MM-DD.html
├── archive/             # 扁平备份（兼容旧流程）
└── scripts/
    ├── feeds.json       # RSS 源与关键词打分配置
    ├── fetch.py         # 拉 RSS → cache/today_raw.json（英文原文 + 打分）
    ├── render.py        # curated/raw → HTML，带 LLM 摘要 ✓ 徽章
    └── publish.py       # git add / commit / push → GitHub Pages
```

## Pipeline

```powershell
$PY = "C:\Users\hughxmwen\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

& $PY scripts/fetch.py     # 1) 抓 RSS，产出 cache/today_raw.json（英文）
# 2) Agent 读 raw，为每条筛后条目手写 ≤80 字中文 tldr
#    产出 cache/today_curated.json（generated_at 必须晚于 raw）
& $PY scripts/render.py    # 3) 渲染 HTML。成功标志：LLM 摘要 ✓ 徽章、无 [render] fallback to raw
& $PY scripts/publish.py   # 4) commit + push origin main
```

### 关键约束

- **中文 tldr 是硬性要求**。`render.py` 带 `CURATED_STALE_HOURS=2` 兜底：curated 若比 raw 老 >2h，会自动 fallback 到英文 raw —— 这是**错误信号**，说明 curated 没及时生成。
- **publish 真假校验**：`publish.py` 打印"成功" ≠ 真的 push 成功。必须用 `git log -1 --stat` 校验当天 `2026/MM/*.html` 与 `archive/*.html` 有真实 diff，并确认 `git rev-parse HEAD == origin/main`。
- **宁缺毋滥**：周末/节假日 release 稀少属于正常，0 条就 0 条，禁止塞应用层/评测榜凑数。

## 自动化

WorkBuddy automation `llm` 每日 22:00（北京时间）触发，cwd = `D:/workbuddy/daily_news`。任务结束会输出结构化运行回执（Raw / Curated / Render / Publish / Top 3 推荐 / 异常降级明细），按以下硬规则判定状态：

| 情况 | 状态 |
|---|---|
| 任一 RSS 源抓取失败 | ⚠️ |
| `[render] fallback to raw` 出现 | ❌ |
| `HEAD != origin/main` | ❌ |
| `git log -1 --stat` 无当天 HTML diff | ❌ |
| Curated 0 条但 Raw > 0 条 | ⚠️ |
