"""dulwich 校验：HEAD vs origin/main、最近一次 commit 的文件 + 行数 diff。"""
from pathlib import Path
import sys
import io

from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.diff_tree import tree_changes

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "git@github.com:xmwen/daily-ai-infra.git"

repo = Repo(str(ROOT))
head = repo.head().decode()
print(f"[verify] HEAD = {head}")

refs = porcelain.ls_remote(REMOTE)
remote_main = refs[b"refs/heads/main"].decode()
print(f"[verify] origin/main = {remote_main}")
match = head == remote_main
print(f"[verify] HEAD == origin/main: {match}")

commit = repo[head.encode()]
print(f"[verify] commit message = {commit.message.decode().strip()}")

if not commit.parents:
    print("[verify] no parent commit; abort")
    sys.exit(1)

parent = commit.parents[0]
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

buf = io.BytesIO()
porcelain.diff_tree(repo, old_tree, new_tree, outstream=buf)
patch = buf.getvalue().decode("utf-8", errors="replace")
added_lines = sum(1 for line in patch.splitlines() if line.startswith("+") and not line.startswith("+++"))
removed_lines = sum(1 for line in patch.splitlines() if line.startswith("-") and not line.startswith("---"))
print(f"[verify] lines: +{added_lines} -{removed_lines}")

today_files = [
    "2026/06/2026-06-01.html",
    "archive/2026-06-01.html",
]
files_set = {p.replace("\\", "/") for _, p in files_in_commit}
print("[verify] today HTML present in commit:")
for f in today_files:
    print(f"  {f}: {f in files_set}")
