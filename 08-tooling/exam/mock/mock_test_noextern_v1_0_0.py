#!/usr/bin/env python3
"""No external requests (X3b). Each given HTML is opened in headless Chromium (file://), the page is exercised (load, derive a new mock, check my answers), and every network request the page makes is recorded:
only file:, data: and about: are allowed; any http(s) request, websocket or beacon fails. Static scan: no http:// or https:// or // url in src/href/@import/url() attributes. Planted defect: a copy with an external script tag must be caught (tested on a temporary copy).
Run under: flock /tmp/page_test.lock nice -n 10 python3 mock_test_noextern_v1_0_0.py HTML [HTML ..] [--log F]"""
import sys, re, os, tempfile
from playwright.sync_api import sync_playwright
files = [x for x in sys.argv[1:] if x.endswith(".html")]
lines = []
def log(x): print(x, flush=True); lines.append(x)
EXT = re.compile(r'(?:src|href)\s*=\s*["\']\s*(?:https?:)?//|@import\s+["\']?(?:https?:)?//|url\(\s*["\']?(?:https?:)?//', re.I)
def probe(pw, path):
    br = pw.chromium.launch(); reqs = []
    ctx = br.new_context(viewport={"width": 1280, "height": 900}); pg = ctx.new_page()
    pg.on("request", lambda r: reqs.append(r.url)); pg.on("websocket", lambda w: reqs.append("ws:" + w.url))
    pg.goto("file://" + path); pg.wait_for_selector("#paper .item")
    pg.click("#btn-derive"); pg.wait_for_selector("#paper .item"); pg.click("#btn-check"); pg.wait_for_timeout(300)
    br.close()
    return [u for u in reqs if not u.startswith(("file:", "data:", "about:", "blob:"))], len(reqs)
ok = True
with sync_playwright() as pw:
    for f in files:
        src = open(f, encoding="utf-8").read()
        static = len(EXT.findall(src))
        bad, n = probe(pw, f)
        good = static == 0 and not bad; ok &= good
        log("%s: requests %d, non-local requests %d, static external references %d -> %s" % (os.path.basename(f), n, len(bad), static, "OK" if good else "FAIL"))
    # planted: an external script tag in a temporary copy
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "planted.html"); s = open(files[0], encoding="utf-8").read().replace("<body>", '<body><script src="https://example.invalid/x.js"></script>', 1)
        open(p, "w", encoding="utf-8").write(s)
        bad, n = probe(pw, p); static = len(EXT.findall(s))
        caught = bool(bad) or static > 0
        log("PLANTED DEFECT external script tag in a temporary copy: static %d, non-local requests %d -> %s" % (static, len(bad), "CAUGHT" if caught else "NOT CAUGHT")); ok &= caught
log("NO-EXTERNAL TEST " + ("PASS" if ok else "FAIL"))
if "--log" in sys.argv: open(sys.argv[sys.argv.index("--log") + 1], "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
