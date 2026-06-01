import re, sys
sys.stdout.reconfigure(encoding="utf-8")
p = "2026/06/2026-06-01.html"
t = open(p, encoding="utf-8").read()
print("badge LLM 摘要:", "LLM 摘要" in t, "checkmark:", "\u2713" in t)
print("fallback raw:", "[render] fallback" in t)
print("CST count:", t.count("CST"))
print("domain-tag count:", len(re.findall(r"domain-tag", t)))
print("rendered_at:", re.search(r"rendered_at[^<]+", t).group(0) if re.search(r"rendered_at[^<]+", t) else "none")
