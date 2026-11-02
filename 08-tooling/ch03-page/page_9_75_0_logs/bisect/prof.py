import json, os, re, sys, hashlib as _hl
from playwright.sync_api import sync_playwright
page = sys.argv[1]; data = json.load(open(sys.argv[2])); ids = sys.argv[3:]
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1400, "height": 900}); pg = ctx.new_page()
    pg.goto("file://" + page); pg.wait_for_timeout(5000)
    for n in data["nodes"]:
        if n["id"] not in ids: continue
        pg.evaluate("id=>goTo(id)", n["id"]); pg.wait_for_timeout(100)
        r = pg.evaluate("""([id,code])=>{const t=x=>{const a=performance.now();x();return Math.round(performance.now()-a)};const ta=document.getElementById('w-'+id+'-code');const o={};
          o.pyHL=t(()=>pyHL(code)); o.setValue=t(()=>{ta.value=code}); o.fitViews=t(()=>fitViews()); o.layout=t(()=>{document.body.offsetHeight}); o.gutter=t(()=>edGutter(ta.closest('.ed'))); o.paint=t(()=>edPaint(ta)); o.lenhl=ta.closest('.ed').querySelector('.edhl').innerHTML.length; return o}""", [n["id"], n["io"]["code"]])
        print(n["id"], len(n["io"]["code"]), r)
    b.close()
