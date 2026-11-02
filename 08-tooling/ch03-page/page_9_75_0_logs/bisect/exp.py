# diagnostic only: which property of the filled code makes pg.fill slow on the example editors (wall ms of fill, then of a forced layout)
import json, re, sys
from playwright.sync_api import sync_playwright
page = sys.argv[1]; data = json.load(open("/home/claude/sen0401/08-tooling/ch03-page/page_data_v9_74_0.json")); io = {n["id"]: n["io"]["code"] for n in data["nodes"] if "io" in n}
def variants(c):
    lines = c.split("\n"); long_ = max(lines, key=len)
    return [("actual", c), ("hex literal shortened to 20", re.sub(r"[0-9a-f]{60,}", "ab" * 10, c)), ("every line cut to 60 chars", "\n".join(l[:60] for l in lines)),
            ("same chars, 25 short lines", "\n".join(c[i:i + 60] for i in range(0, 1500, 60))), ("one line of 1500 chars", "x = '" + "ab" * 750 + "'"), ("empty", "")]
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1400, "height": 900}); pg = ctx.new_page()
    pg.goto("file://" + page); pg.wait_for_timeout(6000)
    for i in sys.argv[2:]:
        pg.evaluate("id=>goTo(id)", i); pg.wait_for_timeout(300)
        for name, code in variants(io[i]):
            ms = []
            for rep in range(2):
                pg.fill("#w-%s-code" % i, "x"); pg.wait_for_timeout(100)
                t0 = pg.evaluate("performance.now()"); pg.fill("#w-%s-code" % i, code); t1 = pg.evaluate("performance.now()"); ms.append(round(t1 - t0))
            print("%-26s %-34s fill wall ms %s" % (i, name, ms), flush=True)
    b.close()
