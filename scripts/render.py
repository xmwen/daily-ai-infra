"""
AI Infra Daily News - Renderer
---------------------------------
读取 cache/today_curated.json (优先) 或 cache/today_raw.json，
渲染成美观的 HTML 日报并写入 D:\\workbuddy\\daily_news\\<YYYY-MM-DD>.html。
同时更新 index.html 作为历史归档入口。
"""

from __future__ import annotations

import json
import re
import html as html_mod
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT   = Path(__file__).resolve().parent.parent
CACHE  = ROOT / "cache"
ARCHIVE = ROOT / "archive"
ARCHIVE.mkdir(parents=True, exist_ok=True)

# curated 相比 raw 最多允许落后多少小时。超过则判定 curated 为 stale，
# 回退使用 raw。防止历史遗留的 curated 文件永远覆盖最新 fetch 结果。
CURATED_STALE_HOURS = 2

# 看板统一使用北京时间（东八区）展示
CST = timezone(timedelta(hours=8))

SECTION_META = {
    "papers":    {"title": "📄 重点论文",     "icon": "📄", "color": "#6366f1"},
    "code":      {"title": "🚀 代码更新",     "icon": "🚀", "color": "#10b981"},
    "blogs":     {"title": "📝 技术博客",     "icon": "📝", "color": "#f59e0b"},
    "community": {"title": "💬 社区热议",     "icon": "💬", "color": "#ec4899"},
}

SECTION_ORDER = ["papers", "code", "blogs", "community"]

# 每个分区展示上限（papers 放宽到 8，其它保持 8）
SECTION_TOP_N = {
    "papers": 8,
    "code": 8,
    "blogs": 8,
    "community": 8,
}
DEFAULT_TOP_N = 8

# 领域标签：值域固定为 推理/训练/agent，配不同配色
DOMAIN_TAG_META = {
    "推理": {"label": "推理", "bg": "rgba(99,102,241,.22)",  "fg": "#c7d2fe", "border": "rgba(99,102,241,.55)"},
    "训练": {"label": "训练", "bg": "rgba(16,185,129,.22)",  "fg": "#a7f3d0", "border": "rgba(16,185,129,.55)"},
    "agent": {"label": "Agent", "bg": "rgba(236,72,153,.22)", "fg": "#fbcfe8", "border": "rgba(236,72,153,.55)"},
}


def esc(s: str) -> str:
    return html_mod.escape(s or "")


def md_inline(s: str) -> str:
    """先 HTML 转义，再把轻量 markdown 标记转回 HTML：
       **bold** → <strong>, `code` → <code>。"""
    out = html_mod.escape(s or "")
    # `code`
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    # **bold**
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


def _parse_ts(s: str) -> datetime | None:
    """解析 ISO 时间戳，容错无时区（视为 UTC）。失败返回 None。"""
    if not s or not isinstance(s, str):
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_data() -> dict:
    """按数据新鲜度选择 curated 或 raw：
       - 只有 raw：用 raw
       - 只有 curated：用 curated
       - 两个都在：比较 generated_at，如果 curated 比 raw 老 > 2h，用 raw
       这样避免 bootstrap/陈旧的 curated 文件永远覆盖最新 fetch 结果。
    """
    curated = CACHE / "today_curated.json"
    raw     = CACHE / "today_raw.json"

    reason = ""
    if curated.exists() and raw.exists():
        with open(curated, "r", encoding="utf-8") as f:
            cd = json.load(f)
        with open(raw, "r", encoding="utf-8") as f:
            rd = json.load(f)
        c_ts = _parse_ts(cd.get("generated_at", ""))
        r_ts = _parse_ts(rd.get("generated_at", ""))
        use_curated = True
        if c_ts is None and r_ts is not None:
            use_curated = False
            reason = "curated 缺少 generated_at"
        elif c_ts is not None and r_ts is not None:
            if r_ts - c_ts > timedelta(hours=CURATED_STALE_HOURS):
                use_curated = False
                reason = f"curated stale (落后 raw {(r_ts - c_ts).total_seconds()/3600:.1f}h)"
        if use_curated:
            data, path, has_llm = cd, curated, True
        else:
            data, path, has_llm = rd, raw, False
            print(f"[render] fallback to raw: {reason}")
    elif curated.exists():
        with open(curated, "r", encoding="utf-8") as f:
            data = json.load(f)
        path, has_llm = curated, True
    else:
        with open(raw, "r", encoding="utf-8") as f:
            data = json.load(f)
        path, has_llm = raw, False

    data["_source_file"] = path.name
    data["_has_llm"] = has_llm
    return data


def render_card(item: dict, has_llm: bool) -> str:
    title   = esc(item.get("title", ""))
    link    = esc(item.get("link", "#"))
    source  = esc(item.get("source", ""))
    domain  = esc(item.get("domain", ""))
    hits    = item.get("hits", [])
    pub     = item.get("published", "")
    score   = item.get("score", 0)
    if pub:
        try:
            dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            pub_display = dt.astimezone(CST).strftime("%m-%d %H:%M CST")
        except Exception:
            pub_display = pub[:16]
    else:
        pub_display = "—"

    # 摘要：优先 LLM 产生的 tldr（支持多段：用 \n\n 分段、\n 换行），
    # 支持轻量 markdown：**bold**、`code`。
    tldr_raw = item.get("tldr") or item.get("summary") or ""
    if item.get("tldr"):
        # LLM 摘要：允许较长，保留段落结构
        tldr_raw = tldr_raw[:1500] + ("…" if len(tldr_raw) > 1500 else "")
        paragraphs = [p.strip() for p in tldr_raw.split("\n\n") if p.strip()]
        tldr_html = "".join(
            f"<p>{md_inline(p).replace(chr(10), '<br>')}</p>"
            for p in paragraphs
        )
    else:
        # summary fallback：单段 + 短截断
        short = tldr_raw[:320] + ("…" if len(tldr_raw) > 320 else "")
        tldr_html = f"<p>{esc(short)}</p>" if short else ""

    # 标签
    tag_html = ""
    if hits:
        tag_html = "".join(
            f'<span class="tag">{esc(h)}</span>' for h in hits[:6]
        )

    relevance = ""
    if has_llm and "relevance" in item:
        r = item["relevance"]
        relevance = f'<span class="rel rel-{r}">LLM {r}/10</span>'

    # 领域标签：推理 / 训练 / agent
    domain_tag_html = ""
    dt_val = (item.get("domain_tag") or "").strip().lower()
    # 兼容中英文写法
    dt_key = {
        "inference": "推理", "推理": "推理",
        "training":  "训练", "训练": "训练",
        "agent":    "agent", "agents": "agent",
    }.get(dt_val, "")
    if dt_key and dt_key in DOMAIN_TAG_META:
        m = DOMAIN_TAG_META[dt_key]
        domain_tag_html = (
            f'<span class="domain-tag" '
            f'style="background:{m["bg"]};color:{m["fg"]};'
            f'border:1px solid {m["border"]};">{m["label"]}</span>'
        )

    return f"""
    <article class="card">
      <div class="card-head">
        <a class="card-title" href="{link}" target="_blank" rel="noopener">{title}</a>
        <div class="card-meta">
          {domain_tag_html}
          <span class="src">{source}</span>
          <span class="dot">·</span>
          <span class="time">{pub_display}</span>
          <span class="dot">·</span>
          <span class="domain">{domain}</span>
          {relevance}
          <span class="score">kw {score}</span>
        </div>
      </div>
      <div class="card-body">{tldr_html}</div>
      <div class="card-tags">{tag_html}</div>
    </article>
    """


def render_section(section: str, items: list[dict], has_llm: bool,
                   top_n: int) -> str:
    meta = SECTION_META.get(section, {"title": section, "icon": "•",
                                      "color": "#64748b"})
    shown = items[:top_n]
    if not shown:
        cards = '<p class="empty">今日无新条目。</p>'
    else:
        cards = "\n".join(render_card(it, has_llm) for it in shown)

    more = ""
    if len(items) > top_n:
        more = f'<p class="more">... 还有 {len(items) - top_n} 条未显示（见 cache/today_raw.json）</p>'

    return f"""
    <section class="section" style="--accent:{meta['color']}">
      <h2 class="sec-title">{meta['title']}
        <span class="count">{len(shown)}/{len(items)}</span>
      </h2>
      <div class="cards">{cards}</div>
      {more}
    </section>
    """


CSS = """
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei",
               Roboto, Arial, sans-serif;
  background: #0f172a;
  color: #e2e8f0;
  line-height: 1.6;
}
.container { max-width: 1080px; margin: 0 auto; padding: 32px 24px 80px; }

header.hero {
  padding: 28px 32px;
  background: linear-gradient(135deg, #1e3a8a 0%, #6d28d9 50%, #be185d 100%);
  border-radius: 16px;
  margin-bottom: 28px;
  box-shadow: 0 10px 40px rgba(0,0,0,.4);
}
header.hero h1 {
  margin: 0 0 8px;
  font-size: 28px;
  letter-spacing: .5px;
}
header.hero p {
  margin: 0;
  opacity: .9;
  font-size: 14px;
}
header.hero .badges { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
header.hero .badge {
  background: rgba(255,255,255,.15);
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  backdrop-filter: blur(8px);
}

.section {
  margin-bottom: 36px;
  padding: 20px 24px 24px;
  background: #1e293b;
  border-radius: 14px;
  border-left: 4px solid var(--accent);
}
.sec-title {
  margin: 0 0 18px;
  font-size: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.sec-title .count {
  font-size: 12px;
  background: rgba(255,255,255,.08);
  padding: 2px 10px;
  border-radius: 999px;
  color: #94a3b8;
  font-weight: 400;
}

.cards { display: flex; flex-direction: column; gap: 14px; }

.card {
  padding: 16px 18px;
  background: #0f172a;
  border-radius: 10px;
  border: 1px solid #334155;
  transition: all .15s ease;
}
.card:hover {
  border-color: var(--accent);
  transform: translateX(2px);
}
.card-head { margin-bottom: 8px; }
.card-title {
  color: #f1f5f9;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  display: block;
  margin-bottom: 4px;
}
.card-title:hover { color: var(--accent); text-decoration: underline; }
.card-meta {
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}
.card-meta .dot { opacity: .4; }
.card-meta .src { color: #cbd5e1; font-weight: 500; }
.card-meta .score {
  margin-left: auto;
  background: rgba(99,102,241,.15);
  color: #a5b4fc;
  padding: 1px 8px;
  border-radius: 999px;
}
.card-meta .rel {
  background: rgba(16,185,129,.18);
  color: #6ee7b7;
  padding: 1px 8px;
  border-radius: 999px;
}
.card-meta .domain-tag {
  padding: 1px 10px;
  border-radius: 999px;
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: .3px;
}
.card-body {
  margin: 8px 0 10px;
  font-size: 14px;
  color: #cbd5e1;
}
.card-body p { margin: 0 0 6px; }
.card-body p:last-child { margin-bottom: 0; }
.card-body strong { color: #e0e7ff; font-weight: 600; }
.card-body code {
  background: rgba(148,163,184,.12);
  padding: 1px 5px;
  border-radius: 3px;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 12.5px;
  color: #fbbf24;
}
.card-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.tag {
  background: rgba(148,163,184,.12);
  color: #94a3b8;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: ui-monospace, Consolas, monospace;
}

.empty { color: #64748b; font-size: 13px; padding: 12px 0; }
.more  { color: #64748b; font-size: 12px; margin: 8px 0 0; text-align: right; }

footer {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #334155;
  color: #64748b;
  font-size: 12px;
  text-align: center;
}
footer a { color: #94a3b8; }
"""


def render(data: dict, out_path: Path):
    now_cst = datetime.now(CST)
    today = now_cst.strftime("%Y-%m-%d %A")
    rendered_at = now_cst.strftime("%Y-%m-%d %H:%M:%S")
    gen_at_raw = data.get("generated_at", "")
    # 数据生成时间：尝试转换为 CST 展示
    gen_at_display = gen_at_raw[:19].replace("T", " ")
    try:
        _g = datetime.fromisoformat(gen_at_raw.replace("Z", "+00:00"))
        if _g.tzinfo is None:
            _g = _g.replace(tzinfo=timezone.utc)
        gen_at_display = _g.astimezone(CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        pass
    hours  = data.get("lookback_hours", 36)
    has_llm = data.get("_has_llm", False)
    llm_badge = "LLM 摘要 ✓" if has_llm else "关键词打分"

    total = sum(len(v) for v in data.get("sections", {}).values())

    parts = [f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Infra 每日动态 - {today}</title>
<!-- rendered_at: {rendered_at} CST -->
<!-- source: {esc(data.get('_source_file',''))} data_generated_at: {gen_at_raw} -->
<style>{CSS}</style>
</head>
<body>
<div class="container">
  <header class="hero">
    <h1>🧠 AI Infra 每日动态</h1>
    <p>{today} · 回溯 {hours}h · 共 {total} 条</p>
    <div class="badges">
      <span class="badge">{llm_badge}</span>
      <span class="badge">Data: {gen_at_display} CST</span>
      <span class="badge">Rendered: {rendered_at} CST</span>
      <span class="badge">Source: {esc(data.get('_source_file',''))}</span>
    </div>
  </header>
"""]

    top_n = 8  # 每个分区展示上限（与 feeds.json 对齐）
    for sec in SECTION_ORDER:
        items = data.get("sections", {}).get(sec, [])
        parts.append(render_section(sec, items, has_llm,
                                    SECTION_TOP_N.get(sec, DEFAULT_TOP_N)))

    parts.append("""
  <footer>
    AI Infra Daily · powered by WorkBuddy Automation ·
    <a href="./archive/">历史归档</a>
  </footer>
</div>
</body>
</html>""")

    out_path.write_text("".join(parts), encoding="utf-8")


def update_index(root: Path):
    """扫描 YYYY/MM/YYYY-MM-DD.html 文件，生成首页 index.html：
       - 最新一期置顶（大卡片，直接嵌入链接）
       - 历史按月分组列表
       同时写 latest.html → 重定向到最新一期，方便固定链接。"""
    # 匹配 YYYY/MM/YYYY-MM-DD.html
    files = sorted(root.glob("20[0-9][0-9]/[01][0-9]/20[0-9][0-9]-[01][0-9]-[0-3][0-9].html"),
                   reverse=True)
    if not files:
        return

    latest = files[0]
    latest_rel = latest.relative_to(root).as_posix()
    latest_stem = latest.stem

    # 按月分组
    from collections import OrderedDict
    groups: "OrderedDict[str, list]" = OrderedDict()
    for f in files:
        ym = f.parent.relative_to(root).as_posix()  # 2026/04
        groups.setdefault(ym, []).append(f)

    group_html_parts = []
    for ym, fs in groups.items():
        items = "\n".join(
            f'<li><a href="./{fp.relative_to(root).as_posix()}">{fp.stem}</a></li>'
            for fp in fs
        )
        group_html_parts.append(
            f'<section class="month"><h3>{ym}</h3><ul>{items}</ul></section>'
        )
    groups_html = "\n".join(group_html_parts)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Infra 每日动态 · 看板</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: -apple-system, "Segoe UI", "PingFang SC",
        "Microsoft YaHei", Roboto, sans-serif;
        background: #0f172a; color: #e2e8f0; line-height: 1.6; }}
.wrap {{ max-width: 960px; margin: 0 auto; padding: 40px 24px 80px; }}
.hero {{
  padding: 28px 32px;
  background: linear-gradient(135deg, #1e3a8a 0%, #6d28d9 50%, #be185d 100%);
  border-radius: 16px;
  margin-bottom: 32px;
  box-shadow: 0 10px 40px rgba(0,0,0,.4);
}}
.hero h1 {{ margin: 0 0 6px; font-size: 28px; }}
.hero p {{ margin: 0; opacity: .9; font-size: 14px; }}
.latest-card {{
  padding: 22px 26px;
  background: #1e293b;
  border-radius: 14px;
  border-left: 4px solid #6366f1;
  margin-bottom: 36px;
}}
.latest-card h2 {{ margin: 0 0 6px; font-size: 14px; color: #94a3b8;
  font-weight: 500; letter-spacing: .5px; text-transform: uppercase; }}
.latest-card a.big {{
  display: inline-block; font-size: 22px; color: #f1f5f9;
  text-decoration: none; font-weight: 600; margin-bottom: 10px;
}}
.latest-card a.big:hover {{ color: #a5b4fc; text-decoration: underline; }}
.latest-card .meta {{ color: #94a3b8; font-size: 13px; }}
.archive-title {{ margin: 0 0 16px; font-size: 18px; color: #cbd5e1; }}
.month {{ background: #1e293b; border-radius: 10px;
  padding: 14px 20px; margin-bottom: 14px; border: 1px solid #334155; }}
.month h3 {{ margin: 0 0 10px; font-size: 15px; color: #a5b4fc;
  font-family: ui-monospace, Consolas, monospace; }}
.month ul {{ list-style: none; padding: 0; margin: 0;
  display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 6px 14px; }}
.month li a {{ color: #93c5fd; text-decoration: none;
  font-family: ui-monospace, Consolas, monospace; font-size: 13px; }}
.month li a:hover {{ color: #f472b6; }}
footer {{ margin-top: 48px; padding-top: 20px;
  border-top: 1px solid #334155; color: #64748b;
  font-size: 12px; text-align: center; }}
</style></head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>🧠 AI Infra 每日动态</h1>
    <p>每日 22:00 自动更新 · 共 {len(files)} 期 · powered by WorkBuddy</p>
  </header>

  <section class="latest-card">
    <h2>最新一期</h2>
    <a class="big" href="./{latest_rel}">{latest_stem}</a>
    <div class="meta">点击查看今日重点论文 / 代码更新 / 博客 / 社区热议</div>
  </section>

  <h2 class="archive-title">📚 历史归档</h2>
  {groups_html}

  <footer>
    Auto-published from <code>D:\\workbuddy\\daily_news</code> ·
    <a href="./latest.html" style="color:#94a3b8">latest.html</a>
  </footer>
</div>
</body></html>"""
    (root / "index.html").write_text(html, encoding="utf-8")

    # latest.html：指向最新一期的跳转页（方便固定链接）
    redirect = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=./{latest_rel}">
<title>Latest - AI Infra Daily</title>
</head><body>Redirecting to <a href="./{latest_rel}">{latest_stem}</a>...</body></html>"""
    (root / "latest.html").write_text(redirect, encoding="utf-8")


def main():
    data = load_data()
    now = datetime.now(CST)
    today = now.strftime("%Y-%m-%d")
    year = now.strftime("%Y")
    month = now.strftime("%m")  # 零填充两位月份

    # 按月目录：ROOT/YYYY/MM/YYYY-MM-DD.html
    month_dir = ROOT / year / month
    month_dir.mkdir(parents=True, exist_ok=True)
    out = month_dir / f"{today}.html"
    render(data, out)

    # 同时在 archive/ 下留一份扁平备份（兼容已有流程）
    (ARCHIVE / f"{today}.html").write_text(
        out.read_text(encoding="utf-8"), encoding="utf-8")

    update_index(ROOT)
    print(f"HTML rendered: {out}")
    print(f"Archive:       {ARCHIVE / (today + '.html')}")
    print(f"Index:         {ROOT / 'index.html'}")
    print(f"Latest:        {ROOT / 'latest.html'}")


if __name__ == "__main__":
    main()
