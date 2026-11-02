# diagnostic only: browser trace (devtools.timeline) of one pg.fill of an example's code: the native events by name, with the largest ones listed
import json, os, sys, collections, tempfile
from playwright.sync_api import sync_playwright
page = sys.argv[1]; i = sys.argv[2]; data = json.load(open("/home/claude/sen0401/08-tooling/ch03-page/page_data_v9_74_0.json")); code = [n["io"]["code"] for n in data["nodes"] if n["id"] == i][0]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(viewport={"width": 1400, "height": 900}).new_page()
    pg.goto("file://" + page); pg.wait_for_timeout(6000); pg.evaluate("id=>goTo(id)", i); pg.wait_for_timeout(300)
    f = tempfile.mktemp(suffix=".json"); b.start_tracing(page=pg, path=f, categories=["devtools.timeline", "disabled-by-default-devtools.timeline"])
    pg.fill("#w-%s-code" % i, code); pg.wait_for_timeout(300); b.stop_tracing()
    ev = json.load(open(f))["traceEvents"]; os.remove(f)
    tot = collections.defaultdict(lambda: [0, 0]); big = []
    for e in ev:
        if e.get("ph") == "X" and e.get("dur") and e.get("name") in ("Layout", "UpdateLayoutTree", "FunctionCall", "EventDispatch", "Paint", "PrePaint", "Layerize", "RunTask", "HitTest", "ParseHTML", "RecalculateStyles", "ScheduleStyleRecalculation", "UpdateLayer", "Commit"):
            t = tot[e["name"]]; t[0] += e["dur"] / 1000; t[1] += 1
            if e["dur"] > 20000: big.append((round(e["dur"] / 1000), e["name"], {k: v for k, v in (e.get("args") or {}).get("beginData", e.get("args") or {}).items() if k in ("elementCount", "dirtyObjects", "totalObjects", "partialLayout", "functionName", "type", "url", "lineNumber")} if isinstance(e.get("args"), dict) else ""))
    for k, v in sorted(tot.items(), key=lambda x: -x[1][0]): print("%-22s %8.1f ms in %d events" % (k, v[0], v[1]))
    for x in sorted(big, reverse=True)[:12]: print("BIG", x)
    b.close()
