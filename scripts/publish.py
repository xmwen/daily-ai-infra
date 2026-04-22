"""AI Infra Daily - Publish to GitHub
-------------------------------------
把本地 D:\\workbuddy\\daily_news 的日报产物 commit + push 到 GitHub 看板仓库。

首次运行前提：
  1. 仓库已通过 gh CLI 创建：gh repo create <owner>/daily-ai-infra --public
  2. 本地已 git init + git remote add origin ...
  3. gh auth login 已完成

日常使用：直接 `python scripts/publish.py`，会自动添加所有应入库文件、
用今日日期作为 commit message 推送到 origin/main。
"""
from __future__ import annotations
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 在 Windows GBK 控制台下也能正常打印 emoji / 中文
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
GH_EXE = r"C:\Program Files\GitHub CLI\gh.exe"


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> str:
    """跑一条命令，返回 stdout。失败抛异常。"""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[ERR] {' '.join(cmd)}", file=sys.stderr)
        print(r.stdout, file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        raise SystemExit(r.returncode)
    return (r.stdout or "").strip()


def has_changes() -> bool:
    out = run(["git", "status", "--porcelain"], check=True)
    return bool(out.strip())


def main():
    # 基础检查
    if not (ROOT / ".git").exists():
        raise SystemExit("❌ 当前目录不是 git 仓库，请先运行 bootstrap_repo.ps1")

    today = datetime.now().strftime("%Y-%m-%d")

    # 1) 添加所有待入库改动
    run(["git", "add", "-A"])

    # 2) 有改动才 commit
    if not has_changes():
        # add 后如果 porcelain 仍空，代表工作区干净
        staged = run(["git", "diff", "--cached", "--name-only"])
        if not staged:
            print("⏭️  没有需要推送的改动，跳过。")
            return

    msg = f"daily: {today} AI Infra digest"
    run(["git", "commit", "-m", msg])

    # 3) push
    run(["git", "push", "origin", "HEAD:main"])

    # 4) 输出 Pages URL（方便一眼看到）
    try:
        remote = run(["git", "remote", "get-url", "origin"])
        # git@github.com:owner/repo.git 或 https://github.com/owner/repo.git
        owner_repo = remote.split("github.com")[-1].lstrip(":/").replace(".git", "")
        owner, repo = owner_repo.split("/", 1)
        print(f"✅ 已推送 → https://github.com/{owner_repo}")
        print(f"   看板 URL → https://{owner}.github.io/{repo}/")
    except Exception:
        print("✅ 已推送（未能解析 Pages URL）")


if __name__ == "__main__":
    main()
