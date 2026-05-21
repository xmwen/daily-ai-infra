# -*- coding: utf-8 -*-
"""dulwich 真推校验脚本：HEAD vs origin/main 对齐 + 当日 HTML diff 行数。"""
import os
from pathlib import Path
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich import client as dulwich_client
from dulwich.client import SSHVendor
import subprocess

# 用 5/18 修好的 OpenSSH SSHVendor
class OpenSSHVendor(SSHVendor):
    def run_command(self, host, command, username=None, port=None, password=None, key_filename=None, ssh_command=None, protocol_version=None):
        from dulwich.client import SubprocessWrapper
        ssh = r"C:\Windows\System32\OpenSSH\ssh.exe"
        args = [ssh, "-x"]
        if port: args += ["-p", str(port)]
        if key_filename: args += ["-i", key_filename]
        target = f"{username}@{host}" if username else host
        if isinstance(command, (bytes, bytearray)):
            command = [command.decode() if isinstance(command, (bytes, bytearray)) else command]
        elif isinstance(command, list):
            command = [c.decode() if isinstance(c, (bytes, bytearray)) else c for c in command]
        args += [target] + list(command)
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=0)
        return SubprocessWrapper(proc)

dulwich_client.get_ssh_vendor = lambda: OpenSSHVendor()

ROOT = Path(__file__).resolve().parent.parent
repo = Repo(str(ROOT))
head_sha = repo.head().decode()
print(f"HEAD = {head_sha}")

# ls-remote origin
remote_url = "git@github.com:xmwen/daily-ai-infra.git"
refs = porcelain.ls_remote(remote_url)
remote_main = refs[b"refs/heads/main"].decode() if b"refs/heads/main" in refs else "<missing>"
print(f"origin/main = {remote_main}")
print(f"HEAD == origin/main: {head_sha == remote_main}")

# 看最新 commit 改了哪些文件 + 行数
last_commit = repo[repo.head()]
parent = repo[last_commit.parents[0]]
print(f"\nlast commit message: {last_commit.message.decode().strip()}")
print(f"author: {last_commit.author.decode()}")

from dulwich.patch import write_tree_diff
import io
buf = io.BytesIO()
write_tree_diff(buf, repo.object_store, parent.tree, last_commit.tree)
diff_text = buf.getvalue().decode("utf-8", errors="replace")

# 统计每文件 +/- 行
files = {}
current = None
plus = minus = 0
for line in diff_text.splitlines():
    if line.startswith("diff --git"):
        if current:
            files[current] = (plus, minus)
        # diff --git a/path b/path
        parts = line.split(" ")
        current = parts[-1][2:] if len(parts) >= 4 else "<?>"
        plus = minus = 0
    elif line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
        continue
    elif line.startswith("+"):
        plus += 1
    elif line.startswith("-"):
        minus += 1
if current:
    files[current] = (plus, minus)

print("\n=== files in last commit ===")
for f, (p, m) in files.items():
    print(f"  +{p:5d} -{m:5d}  {f}")

today_html_2026 = "2026/05/2026-05-20.html"
today_html_arch = "archive/2026-05-20.html"
print(f"\n2026/05 HTML diff: {today_html_2026 in files} ({files.get(today_html_2026, (0,0))})")
print(f"archive HTML diff: {today_html_arch in files} ({files.get(today_html_arch, (0,0))})")
