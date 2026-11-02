# diagnostic only: what the main thread does during page.fill of an example's code (CPU profile of JS + trace events by name)
import json, os, sys, collections
from playwright.sync_api import sync_playwright
page = sys.argv[1]; ids = sys.argv[2:]; data = json.load(open("/home/claude/sen0401/08-tooling/ch03-page/page_data_v9_74_0.json")); io = {n["id"]: n["io"]["code"] for n in data["nodes"] if "io" in n}
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1400, "height": 900}); pg = ctx.new_page()
    pg.goto("file://" + page); pg.wait_for_timeout(6000)
    cdp = ctx.new_cdp_session(pg)
    for i in ids:
        pg.evaluate("id=>goTo(id)", i); pg.wait_for_timeout(300)
        cdp.send("Profiler.enable"); cdp.send("Profiler.setSamplingInterval", {"interval": 200}); cdp.send("Profiler.start")
        t0 = pg.evaluate("performance.now()"); pg.fill("#w-%s-code" % i, io[i]); t1 = pg.evaluate("performance.now()")
        prof = cdp.send("Profiler.stop")["profile"]; cdp.send("Profiler.disable")
        nodes = {n["id"]: n for n in prof["nodes"]}; self_t = collections.Counter()
        dts = prof["timeDeltas"]; 
        for s, dt in zip(prof["samples"], dts): cf = nodes[s]["callFrame"]; self_t[(cf["functionName"] or "(anon)", cf["url"].split("/")[-1][:30], cf["lineNumber"])] += dt
        tot = sum(self_t.values()) / 1000
        print("==", i, "fill wall ms", round(t1 - t0), "profile total ms", round(tot))
        for k, v in self_t.most_common(6): print("   %7.1f ms  %s" % (v / 1000, k))
    b.close()
