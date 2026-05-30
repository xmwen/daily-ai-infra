"""dulwich 校验：HEAD vs origin/main、最近一次 commit 改了哪些文件、行数 diff。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dulwich_publish import open_ssh_client  # 复用 SSHVendor 配置  # noqa: E402

from dulwich import porcelain  # noqa: E402
from dulwich.repo import Repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "git@github.com:xmwen/daily-ai-infra.git"

repo = Repo(str(ROOT))
head = repo.head().decode()
print(f"[verify] HEAD = {head}")

open_ssh_client()
refs = porcelain.ls_remote(REMOTE)
remote_main = refs[b"refs/heads/main"].decode()
print(f"[verify] origin/main = {remote_main}")
print(f"[verify] HEAD == origin/main: {head == remote_main}")

# 拉最近 commit 的 stat（含哪些文件 + 行数 diff）
commit = repo[head.encode()]
print(f"[verify] commit message = {commit.message.decode().strip()}")

parent = commit.parents[0] if commit.parents else None
if parent is None:
    print("[verify] no parent commit")
    sys.exit(1)

from dulwich.diff_tree import tree_changes  # noqa: E402

old_tree = repo[parent].tree
new_tree = commit.tree

added = modified = deleted = 0
files_in_commit = []
for change in tree_changes(repo.object_store, old_tree, new_tree):
    if change.type == "add":
        added += 1
        files_in_commit.append(("A", change.new.path.decode()))
    elif change.type == "delete":
        deleted += 1
        files_in_commit.append(("D", change.old.path.decode()))
    else:
        modified += 1
        files_in_commit.append(("M", change.new.path.decode()))

print(f"[verify] files changed: +{added} ~{modified} -{deleted}")
for tag, path in files_in_commit:
    print(f"  {tag} {path}")

# 行数 diff（dulwich patch）
import io  # noqa: E402
buf = io.BytesIO()
porcelain.diff_tree(repo, old_tree, new_tree, outstream=buf)
patch = buf.getvalue().decode("utf-8", errors="replace")

added_lines = sum(1 for line in patch.splitlines() if line.startswith("+") and not line.startswith("+++"))
removed_lines = sum(1 for line in patch.splitlines() if line.startswith("-") and not line.startswith("---"))
print(f"[verify] lines: +{added_lines} -{removed_lines}")

# 当日 HTML 是否在 commit 内
today_files = [
    "2026/05/2026-05-30.html",
    "archive/2026-05-30.html",
]
files_set = {p.replace("\\", "/") for _, p in files_in_commit}
print("[verify] today HTML present in commit:")
for f in today_files:
    print(f"  {f}: {f in files_set}")
