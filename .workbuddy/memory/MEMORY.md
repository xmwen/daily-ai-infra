# MEMORY — daily_news 看板项目

## 项目定位
AI Infra / LLM 推理&训练系统 + agent 系统基础设施 每日动态看板，抓 RSS → Agent 中文 tldr → 渲染 HTML → 推送 GitHub Pages。
- 仓库：https://github.com/xmwen/daily-ai-infra
- 看板：https://xmwen.github.io/daily-ai-infra/
- 分量参考：推理 60% / 训练 25% / agent 系统 15%，curated 上限 ≤25。

## Pipeline（每日必走三步）
Python venv：`C:\Users\hughxmwen\.workbuddy\binaries\python\envs\default\Scripts\python.exe`

1. `scripts/fetch.py` → `cache/today_raw.json`（英文 RSS 原文）
2. **Agent 手写中文 curated**（硬性要求）→ `cache/today_curated.json`
   - 每条 ≤80 字中文 tldr，聚焦"这是什么 + 工程意义"
   - `generated_at` 必须比 raw 新（否则 render.py 会 fallback 到 raw 英文）
   - 用一次性 Python 脚本 `json.dump(..., ensure_ascii=False)` 生成，避免手写 JSON 转义坑
3. `scripts/render.py` → HTML（必须 `LLM 摘要 ✓` 徽章、无 `[render] fallback to raw`）
4. `scripts/publish.py` → git push origin main

## 自动化任务
- **`llm`（ACTIVE）**：每日 22:00 触发，cwd=`D:/workbuddy/daily_news`，prompt 已包含中文摘要硬性要求。
- `ai-infra`（PAUSED，标记 `[DEPRECATED]`）：误建的重复任务，待手动删除。

## 关键工程约束
- `publish.py` stdout "成功" ≠ 真的 push 了 HTML。必须用 `git log -1 --stat` 校验 `2026/MM/*.html` 与 `archive/*.html` 真实 diff，并比对 `git rev-parse HEAD` == `origin/main`。
- `render.py` 有 `CURATED_STALE_HOURS=2` 兜底：curated 比 raw 老 >2h 会自动 fallback 到英文 raw —— 这是**错误信号**，说明 curated 没及时生成。
- 每份 HTML 都注入 `rendered_at` 徽章和注释，保证字节级非幂等，便于核对 pipeline。
- **时区约定（2026-04-22 起）**：看板所有展示时间统一用东八区（CST）。`render.py` 里 `CST = timezone(timedelta(hours=8))`，卡片 pub_display / hero 徽章 / HTML 注释都走 `astimezone(CST).strftime("... CST")`。`fetch.py` / `publish.py` 的 `today` 日期也按 CST 生成（跨零点机器时区漂移防护）。缓存里的 `generated_at` 仍保留 UTC ISO（机器可解析标准），只在渲染时转 CST。
- **git 不可用兜底（2026-05-18 发现）**：系统 git.exe 在 2026-05-18 期间被卸载，PATH 残留 `D:\Downloads\Git\cmd` 指向不存在目录，`publish.py` 立即 `FileNotFoundError [WinError 2]`。临时方案是 `scripts/_dulwich_publish.py`：venv 装 `dulwich`（pure Python git），通过 SSHVendor 调用系统 OpenSSH（`C:\Windows\System32\OpenSSH\ssh.exe`，9.5p2 自带）+ `~/.ssh/id_rsa` 走 `git@github.com:xmwen/daily-ai-infra.git` 推送。校验则用 `dulwich.porcelain.ls_remote` 替代 `git ls-remote`。**长期需求**：用户应重装 Git for Windows（或修正 PATH），让 publish.py 走原生 git 路径，dulwich 仅作降级兜底。

## 用户工作关联（筛选偏好）
重点保留：
- **推理/训练/硬件**：ScaleUp 统一内存、MoE kernel 重叠、DeepGemm、FlashAttention、MLIR、PIM、CUTLASS、vLLM、SGLang、量化推理、NURBS 光追、昇腾/寒武纪/摩尔线程等国产芯片。
- **agent 系统层（只看基础设施）**：LangGraph/AutoGen/OpenAI Agents/Anthropic Agents SDK、MCP 协议、A2A、tool use & function calling 底层、结构化输出（XGrammar/Outlines/lm-format-enforcer）、constrained decoding、agent memory 工程实现、coding/computer-use agent 系统设计（Claude Code / Cursor / Codex / Devin / browser-use）、tracing（LangSmith/Langfuse/Phoenix）。
直接排除：纯算法论文、数据集/评测榜、RAG 应用、prompt 工程、"用 agent 做 XX" 应用案例、agent 能力排行榜（LMArena）、AI 商业新闻。

**agent 收/弃判断标准**：讲 agent 的**系统基础设施**（调度算法 / 协议 / runtime）就收，讲 agent **应用**（数据分析 / 客服 / 写周报）就丢。

## feeds.json 数据源覆盖（2026-04-22 起）
- **papers**：arXiv cs.DC / cs.AR / cs.PF / cs.LG
- **code（17 个）**：vLLM、TensorRT-LLM、Megatron-LM、CUTLASS、DeepGEMM、DeepEP、FlashInfer、SGLang、PyTorch、Triton、LLVM/MLIR、LangGraph、AutoGen、OpenAI Agents Python、MCP Python SDK、XGrammar、Outlines
- **blogs（7 个）**：NVIDIA Dev、PyTorch、Meta Eng、Google Research、HuggingFace、LangChain Blog、Anthropic News
- **community（4 路）**：HN LLM infra、HN Agent infra（MCP/LangGraph/tool use/Claude Code 专搜）、r/LocalLLaMA、r/MachineLearning
