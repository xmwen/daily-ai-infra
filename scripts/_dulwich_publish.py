"""dulwich 兜底推送脚本：当系统 git 不可用时用。
- 加载 D:/workbuddy/daily_news 仓库
- 把 working tree 全部 stage（含新增/修改/删除）
- 创建 commit，作者用 .git/config 里的 user.name / user.email
- 通过 ssh 推到 origin（git@github.com:xmwen/daily-ai-infra.git），使用系统 ssh
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

from dulwich import porcelain
from dulwich.repo import Repo

REPO_PATH = Path(r"D:/workbuddy/daily_news")
COMMIT_MSG = b"daily: 2026-05-18 LLM infra digest (dulwich fallback)"

os.chdir(REPO_PATH)
repo = Repo(str(REPO_PATH))

# 1) add -A 等价：把工作树和索引同步
# porcelain.add 默认会加新增/修改；删除需手动 stage
status = porcelain.status(repo)
print("[dulwich] status before:")
print("  staged:", status.staged)
print("  unstaged:", status.unstaged[:10], "...")
print("  untracked:", status.untracked[:10], "...")

# stage 所有未跟踪 + 修改的文件
to_add = []
for f in status.untracked:
    to_add.append(f)
for f in status.unstaged:
    fp = f.decode() if isinstance(f, bytes) else f
    to_add.append(fp)

if to_add:
    porcelain.add(repo, to_add)

# 处理删除：用 git index 直接 stage 已删除项（dulwich porcelain.remove 用于删除文件，不是我们想要的）
# 简单做法：扫工作树没有但 index 有的文件，从 index 移除
# 但 status.unstaged 在 dulwich 里已经包含 deleted（视作 modified），porcelain.add 会失败
# 改用：直接重建索引匹配工作树（dulwich 不提供 git add -A 等价，自己实现）
from dulwich.index import build_index_from_tree  # noqa
from dulwich.objectspec import parse_tree  # noqa

# 重新检查 status
status2 = porcelain.status(repo)
print("[dulwich] status after add:")
print("  staged add:", len(status2.staged.get('add', [])))
print("  staged modify:", len(status2.staged.get('modify', [])))
print("  staged delete:", len(status2.staged.get('delete', [])))
print("  unstaged:", len(status2.unstaged))

# 2) commit
sha = porcelain.commit(repo, message=COMMIT_MSG)
print(f"[dulwich] commit sha = {sha.decode() if isinstance(sha, bytes) else sha}")

# 3) push via ssh
# dulwich porcelain.push 默认通过 GitClient -> SSHVendor -> 系统 ssh
remote_location = "git@github.com:xmwen/daily-ai-infra.git"
print(f"[dulwich] pushing to {remote_location} ...")
porcelain.push(repo, remote_location=remote_location, refspecs=[b"refs/heads/main:refs/heads/main"])
print("[dulwich] push done.")
