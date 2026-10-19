#!/usr/bin/env python3
"""sen0401_commons_fetch v1.0.0 - fetches Wikimedia Commons files politely (the egress address is rate limited: 429 with Retry-After): for each File: title it saves the original (or, with width, the
thumbnail) and the file page's own wikitext (author, licence, source, date), waiting as long as Retry-After says. Output: <outdir>/<local name> and <outdir>/<local name>.meta.txt.
Usage: sen0401_commons_fetch_v1_0_0.py <outdir> <title>=<local name>[@width] ...      (title without 'File:', underscores or spaces)"""
__version__ = "1.0.0"
import hashlib, os, sys, time, urllib.parse
import requests
H = {"User-Agent": "SEN0401-course-materials/1.0 (altunel.yusuf@gmail.com; teaching materials, CC BY 4.0)"}
def get(url, params=None):
    for k in range(12):
        r = requests.get(url, params=params, headers=H, timeout=60)
        if r.status_code != 429: return r
        w = int(r.headers.get("retry-after", "30")); print("   429, waiting", min(w, 300), flush=True); time.sleep(min(w, 300) + 2)
    return r
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for a in sys.argv[2:]:
    t, _, local = a.partition("="); width = None
    if "@" in local: local, width = local.split("@"); width = int(width)
    t = t.replace(" ", "_")
    if os.path.exists(os.path.join(out, local)): print("have", local); continue
    m = get("https://commons.wikimedia.org/w/index.php", {"title": "File:" + t, "action": "raw"})
    open(os.path.join(out, local + ".meta.txt"), "w").write(m.text)
    h = hashlib.md5(t.encode()).hexdigest()
    if width: url = "https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/%dpx-%s%s" % (h[0], h[:2], urllib.parse.quote(t), width, urllib.parse.quote(t), ".png" if t.lower().endswith((".svg", ".tif", ".tiff")) else "")
    else: url = "https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s" % (h[0], h[:2], urllib.parse.quote(t))
    r = get(url)
    if r.status_code == 200 and r.content[:5] != b"<!DOC":
        open(os.path.join(out, local), "wb").write(r.content); print("ok  ", local, len(r.content), "meta", len(m.text), flush=True)
    else: print("FAIL", t, r.status_code, flush=True)
    time.sleep(6)
