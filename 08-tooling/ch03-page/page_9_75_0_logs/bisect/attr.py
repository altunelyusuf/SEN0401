#!/usr/bin/env python3
# diagnostic only: attributes the long tasks of the 87-example loop of page test 9.38.0 to the step that causes them (same actions, same order)
import json, os, re, sys, time, glob, hashlib as _hl, ssl as _ssl, urllib.request as _ur
from playwright.sync_api import sync_playwright
page = sys.argv[1]; data = json.load(open(sys.argv[2])); nodes = data["nodes"]
def _cdn(route):
    u = route.request.url; f = "/tmp/cdncache/" + _hl.sha1(u.encode()).hexdigest()
    try:
        route.fulfill(status=200, body=open(f, "rb").read(), headers={"content-type": open(f + ".ct").read(), "access-control-allow-origin": "*"})
    except Exception: route.continue_()
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8")); ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}); ctx.route(re.compile(r"^https://cdn\.jsdelivr\.net/"), _cdn)
    pg = ctx.new_page(); pg.add_init_script("window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime),Math.round(e.duration)]))).observe({type:'longtask',buffered:true});")
    pg.goto("file://" + page); pg.wait_for_timeout(6000)
    seen = [len(pg.evaluate("window.__lt"))]
    def mark(tag, nid):
        lt = pg.evaluate("window.__lt"); new = [x for x in lt[seen[0]:] if x[1] >= 100]; seen[0] = len(lt)
        if new: print("%-34s %-10s %s" % (nid, tag, new), flush=True)
    for n in nodes:
        w = "w-" + n["id"]
        pg.evaluate("id=>goTo(id)", n["id"]); pg.wait_for_timeout(50); mark("goTo", n["id"])
        if "io" in n:
            pg.fill("#%s-code" % w, n["io"]["code"]); mark("fill", n["id"])
            pg.fill("#%s-guess" % w, n["io"]["out"]); mark("guess", n["id"])
            pg.click('[data-run="%s"]' % n["id"])
            pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent&&o.textContent!=='running...'}", arg=w + "-out", timeout=120000); mark("run", n["id"])
            pg.fill("#%s-code" % w, "2 + 2"); pg.click('[data-run="%s"]' % n["id"])
            pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent!=='running...'}", arg=w + "-out", timeout=60000); mark("run2", n["id"])
            pg.click('[data-reset="%s"]' % n["id"]); mark("reset", n["id"])
            pg.click('[data-detail="%s"]' % n["id"]); mark("detail", n["id"]); pg.keyboard.press("Escape"); mark("esc", n["id"])
    print("DONE longest", max([d for s, d in pg.evaluate("window.__lt")] or [0]), "count", len(pg.evaluate("window.__lt")))
    b.close()
