import json
d = json.load(open(r'D:\workbuddy\daily_news\cache\today_raw.json', 'r', encoding='utf-8'))
for s, v in d['sections'].items():
    if v:
        print(f"[{s}] total={len(v)}  top1: {v[0]['title'][:70]} (score={v[0]['score']}, hits={v[0]['hits'][:3]})")
    else:
        print(f"[{s}] empty")
