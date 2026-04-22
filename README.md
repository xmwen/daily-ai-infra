# AI Infra 每日动态

每日 09:00 由 WorkBuddy Automation 自动拉取 RSS、LLM 精筛摘要、渲染成 HTML 日报并推送到本仓库。

**在线看板**：https://<owner>.github.io/daily-ai-infra/

## 内容覆盖

- 📄 **重点论文**：arXiv cs.DC / cs.AR / cs.LG 等 AI 系统/硬件方向
- 🚀 **代码更新**：PyTorch / vLLM / LLVM / CUTLASS 等项目 release
- 📝 **技术博客**：NVIDIA / 社区作者博客
- 💬 **社区热议**：Reddit / HN / Twitter 高热度讨论

关注重点：ScaleUp 统一内存引擎、MoE kernel 重叠、DeepGemm、FlashAttention、MLIR、PIM、NURBS 光追。

## 目录结构

```
daily-ai-infra/
├── index.html           # 看板首页（最新一期 + 历史归档索引）
├── latest.html          # 跳转到最新一期
├── YYYY/MM/             # 按月组织的历史日报
│   └── YYYY-MM-DD.html
├── archive/             # 扁平备份（兼容旧流程）
└── scripts/             # 抓取/渲染/推送脚本
```

## 本地执行

```powershell
$PY = "C:\Users\hughxmwen\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
& $PY scripts/fetch.py     # 拉 RSS
# 然后人工或 LLM 写 cache/today_curated.json
& $PY scripts/render.py    # 渲染 HTML + 更新 index
& $PY scripts/publish.py   # commit + push 到 GitHub
```

自动化任务由 WorkBuddy automation `ai-infra` 每日 09:00 触发。
