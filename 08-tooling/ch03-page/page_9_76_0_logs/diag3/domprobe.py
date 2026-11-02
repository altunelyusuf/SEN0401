#!/usr/bin/env python3
# diagnostic only (task TK_Repair_Ch03_Page2_Build): size of the DOM of a chapter 3 page after load and the cost of a selector query and of a forced style+layout; prints what it measures
import json, os, re, sys, hashlib as _hl
from playwright.sync_api import sync_playwright
def _cdn(route):
    u = route.request.url; f = "/tmp/cdncache/" + _hl.sha1(u.encode()).hexdigest()
    try: route.fulfill(status=200, body=open(f, "rb").read(), headers={"content-type": open(f + ".ct").read(), "access-control-allow-origin": "*"})
    except Exception: route.continue_()
JS = """()=>{const t=f=>{const a=performance.now();const r=f();return [Math.round((performance.now()-a)*10)/10,r]};const all=document.querySelectorAll('*');
 const byPane={};document.querySelectorAll('[data-pane]').forEach(p=>{byPane[p.dataset.pane]=p.querySelectorAll('*').length});const top=Object.entries(byPane).sort((a,b)=>b[1]-a[1]).slice(0,8);
 return {elements:all.length,hl_spans:[...document.querySelectorAll('.edhl')].reduce((a,e)=>a+e.querySelectorAll('*').length,0),editors:document.querySelectorAll('.ed').length,panes:Object.keys(byPane).length,topPanes:top,
  q_attr:t(()=>document.querySelectorAll('[data-pane]:not([hidden]) .viewsub [data-tab]').length),q_all:t(()=>document.querySelectorAll('[data-run]').length),
  recalc:t(()=>{document.body.classList.toggle('probe-x');return document.body.getBoundingClientRect().height}),recalc2:t(()=>{document.documentElement.style.setProperty('--probe','1');return document.body.getBoundingClientRect().height}),
  svg:document.querySelectorAll('svg').length,imgs:document.querySelectorAll('img').length,heap:performance.memory?Math.round(performance.memory.usedJSHeapSize/1e6):null}}"""
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8")); 
    for path in sys.argv[1:]:
        ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}); ctx.route(re.compile(r"^https://cdn\.jsdelivr\.net/"), _cdn)
        pg = ctx.new_page(); pg.goto("file://" + path); pg.wait_for_timeout(9000)
        r = pg.evaluate(JS); r2 = pg.evaluate(JS)
        print(os.path.basename(path), json.dumps(r), flush=True); print(os.path.basename(path), "second pass", json.dumps({k: r2[k] for k in ("q_attr", "q_all", "recalc", "recalc2")}), flush=True)
        ctx.close()
    b.close()
