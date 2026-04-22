"""一次性迁移脚本：把根目录里的 YYYY-MM-DD.html 移到 YYYY/MM/ 下。
执行一次就删，主流程后续走 render.py 直接按月目录写。"""
from __future__ import annotations
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pat = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})\.html$")

moved = 0
for f in list(ROOT.glob("*.html")):
    m = pat.match(f.name)
    if not m:
        continue
    yyyy, mm, _ = m.groups()
    dst_dir = ROOT / yyyy / mm
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f.name
    shutil.move(str(f), str(dst))
    moved += 1
    print(f"moved: {f.name} -> {dst.relative_to(ROOT).as_posix()}")

print(f"done, {moved} files migrated.")
