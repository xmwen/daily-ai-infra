"""
AI Infra Daily News - Fetcher
---------------------------------
职责：
1. 读取 feeds.json 中的订阅源
2. 拉取 RSS/Atom feed
3. 基于关键词做粗打分
4. 过滤时间窗口（默认 36 小时内）
5. 按分区 / 按 source 做最小分数门槛 + 负向黑名单 + 标题正则过滤
6. 输出 today_raw.json 供后续 LLM 处理 / HTML 渲染

设计原则：零运行时 LLM 依赖；LLM 摘要由 WorkBuddy Automation 的 Agent 回读 JSON 后完成。

feeds.json 约定（向后兼容）：
- `keywords.strong` / `keywords.medium`：打分词表
- `keywords.deny`：负向黑名单，命中直接丢（大小写不敏感）
- `section_min_score`：{section: int} 分区级最低分数门槛
- 每个 source 可选字段：
    - `min_score`：source 级最低分数（覆盖 section_min_score）
    - `title_regex`：标题必须匹配的正则（不匹配则丢）
    - `weight`：分数乘子（仅影响排序）
"""

from __future__ import annotations

import json
import re
import sys
import time
import html
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

import feedparser
import requests
from dateutil import parser as date_parser

ROOT   = Path(__file__).resolve().parent.parent   # D:\workbuddy\daily_news
CONFIG = Path(__file__).resolve().parent / "feeds.json"
CACHE  = ROOT / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 AI-Infra-DailyNews/1.0"
)

# --------------------------- 工具 ---------------------------

def load_config() -> dict:
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def to_utc(dt_str: str) -> datetime | None:
    if not dt_str:
        return None
    try:
        dt = date_parser.parse(dt_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def score_entry(title: str, summary: str, kw: dict) -> tuple[int, list[str]]:
    """根据关键词做粗打分，返回 (score, hit_keywords)"""
    text = f"{title}\n{summary}".lower()
    hits = []
    score = 0
    for k in kw.get("strong", []):
        if k.lower() in text:
            score += 3
            hits.append(k)
    for k in kw.get("medium", []):
        if k.lower() in text:
            score += 1
            hits.append(k)
    return score, hits


def hit_deny(title: str, summary: str, deny: list[str]) -> str | None:
    """命中任一黑名单关键词返回该词，否则返回 None"""
    if not deny:
        return None
    text = f"{title}\n{summary}".lower()
    for k in deny:
        if k.lower() in text:
            return k
    return None


# --------------------------- 抓取 ---------------------------

def fetch_feed(url: str, timeout: int = 15) -> list[dict]:
    """尝试用 requests 下载后给 feedparser 解析，失败则直接交给 feedparser 走它自己的网络层。"""
    try:
        resp = requests.get(url, timeout=timeout,
                            headers={"User-Agent": USER_AGENT})
        if resp.status_code == 200 and resp.content:
            parsed = feedparser.parse(resp.content)
        else:
            parsed = feedparser.parse(url)
    except Exception:
        parsed = feedparser.parse(url)

    entries = []
    for e in getattr(parsed, "entries", []) or []:
        entries.append({
            "title":   (e.get("title") or "").strip(),
            "link":    e.get("link") or "",
            "summary": strip_html(e.get("summary") or e.get("description") or ""),
            "author":  e.get("author") or "",
            "published": (
                e.get("published") or e.get("updated") or e.get("created") or ""
            ),
        })
    return entries


def collect_section(section: str, sources: list[dict], cfg: dict,
                    cutoff: datetime) -> tuple[list[dict], dict]:
    """返回 (items, stats)。stats 记录每个 source 的抓取/丢弃原因。"""
    kw        = cfg["keywords"]
    deny      = kw.get("deny", [])
    per_max   = cfg["limits"]["per_source_max"]
    section_min = cfg.get("section_min_score", {}).get(section, 0)
    items     = []
    stats     = {}

    for src in sources:
        name   = src["name"]
        url    = src["url"]
        weight = src.get("weight", 1.0)
        src_min = src.get("min_score", section_min)
        title_re = src.get("title_regex")
        title_re_compiled = re.compile(title_re) if title_re else None

        print(f"  [{section}] fetching {name} (min_score={src_min}"
              + (f", regex={title_re}" if title_re else "")
              + ") ...", flush=True)
        try:
            entries = fetch_feed(url)
        except Exception as ex:
            print(f"    ! failed: {ex}", flush=True)
            stats[name] = {"fetched": 0, "kept": 0, "reason": f"failed: {ex}"}
            continue

        fetched = len(entries)
        kept = 0
        drop_time = drop_deny = drop_regex = drop_score = 0
        picked = 0

        for e in entries:
            if picked >= per_max:
                break

            # 1. 时间窗口
            pub = to_utc(e["published"])
            if pub and pub < cutoff:
                drop_time += 1
                continue

            # 2. 标题正则（常用于 code 区滤掉 ciflow/trunk）
            if title_re_compiled and not title_re_compiled.search(e["title"]):
                drop_regex += 1
                continue

            # 3. 负向黑名单
            denied = hit_deny(e["title"], e["summary"], deny)
            if denied:
                drop_deny += 1
                continue

            # 4. 关键词打分
            score, hits = score_entry(e["title"], e["summary"], kw)
            adjusted = score * weight

            # 5. 分数门槛
            if adjusted < src_min:
                drop_score += 1
                continue

            items.append({
                "section":   section,
                "source":    name,
                "title":     e["title"],
                "link":      e["link"],
                "summary":   e["summary"][:800],
                "published": pub.isoformat() if pub else "",
                "score":     round(adjusted, 2),
                "hits":      hits,
                "domain":    urlparse(e["link"]).netloc,
            })
            picked += 1
            kept += 1

        stats[name] = {
            "fetched": fetched,
            "kept":    kept,
            "drop_time":  drop_time,
            "drop_regex": drop_regex,
            "drop_deny":  drop_deny,
            "drop_score": drop_score,
        }
        print(f"    -> kept {kept}/{fetched} "
              f"(time={drop_time} regex={drop_regex} deny={drop_deny} score={drop_score})",
              flush=True)

    return items, stats


# --------------------------- 主流程 ---------------------------

def main():
    cfg   = load_config()
    hours = cfg["limits"]["lookback_hours"]
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lookback_hours": hours,
        "sections": {},
        "fetch_stats": {},
    }

    for section, sources in cfg["sources"].items():
        print(f"== Section: {section} ({len(sources)} sources) ==", flush=True)
        items, stats = collect_section(section, sources, cfg, cutoff)
        items.sort(key=lambda x: (x["score"], x["published"]), reverse=True)
        result["sections"][section] = items
        result["fetch_stats"][section] = stats
        print(f"   -> {len(items)} items", flush=True)

    # 今日 raw 快照（按北京时间日期归档）
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    raw_path = CACHE / f"raw_{today}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 固定入口：today_raw.json
    latest = CACHE / "today_raw.json"
    with open(latest, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in result["sections"].values())
    print(f"\nDone. Total items: {total}")
    print(f"Saved: {raw_path}")
    print(f"Saved: {latest}")


if __name__ == "__main__":
    sys.exit(main())
