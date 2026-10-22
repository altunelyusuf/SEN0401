import sys, json
from playwright.sync_api import sync_playwright
page = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(locale="en-US", viewport={"width":1400,"height":900}); pg = ctx.new_page()
    pg.goto("file://"+page); pg.wait_for_timeout(1500)
    GROUP = pg.evaluate("GROUP_OF")
    def view(k):
        g = GROUP.get(k)
        if g:
            view(g)
            if not pg.locator('[data-pane="%s"]' % k).is_visible(): pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="%s"]' % k)
        else: pg.click('#groups [data-tab="%s"]' % k)
    pg.on("console", lambda m: print("CONSOLE", m.type, m.text[:200]) if m.type=="error" else None); pg.on("pageerror", lambda e: print("PAGEERR", str(e)[:300]))
    view("ontoerd"); pg.wait_for_function("()=>document.querySelectorAll('#oerd [data-ent]').length>0", timeout=120000)
    pg.click('[data-erd="sections"]'); pg.wait_for_function("()=>document.querySelectorAll('#oerd [data-ent]').length>0", timeout=60000); pg.wait_for_timeout(1500)
    M = """()=>{const R=[...document.querySelectorAll('#oerd .oe-e')].map(g=>{const r=g.querySelector('rect').getBoundingClientRect();return {e:g.dataset.ent,x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),p:[OE_ENT[g.dataset.ent].x,OE_ENT[g.dataset.ent].y]}});const ov=[];for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const a=R[i],b=R[j];if(!(a.x+a.w<=b.x||b.x+b.w<=a.x||a.y+a.h<=b.y||b.y+b.h<=a.y))ov.push([a.e,b.e])}return {n:R.length,ov,R}}"""
    m0 = pg.evaluate(M); print("ERD entities", m0["n"], "overlapping pairs BEFORE drag:", m0["ov"])
    g0 = pg.locator("#oerd .oe-e").first; bb = g0.bounding_box(); ent0 = g0.get_attribute("data-ent")
    _box = pg.locator("#oerd").bounding_box(); _dx = 1 if bb["x"] + bb["width"] / 2 < _box["x"] + _box["width"] / 2 else -1
    print("dragged (first entity):", ent0, "bbox", bb, "dx", _dx)
    pg.mouse.move(bb["x"]+12, bb["y"]+10); pg.mouse.down(); pg.mouse.move(bb["x"]+_dx*60, bb["y"]+40, steps=5); pg.mouse.move(bb["x"]+_dx*120, bb["y"]+70, steps=5); pg.mouse.up(); pg.wait_for_timeout(600)
    m1 = pg.evaluate(M); print("overlapping pairs AFTER drag:", m1["ov"])
    ti = pg.evaluate("()=>{const r=document.querySelector('#oerd .oe-r');if(!r)return 2;const i=[...document.querySelectorAll('#oerd .oe-e')].findIndex(e=>e.dataset.ent===r.dataset.a);return i<0?2:i}")
    tgt = pg.locator("#oerd .oe-e").nth(ti); tb = tgt.bounding_box(); print("click target index", ti, tgt.get_attribute("data-ent"), tb)
    hit = pg.evaluate("p=>{const e=document.elementFromPoint(p[0],p[1]);const g=e.closest('[data-ent]');return {tag:e.tagName,ent:g?g.dataset.ent:null}}", [tb["x"]+tb["width"]/2, tb["y"]+tb["height"]/2]); print("element at target centre:", hit)
    for r in m1["R"]: print("  ", r)
    b.close()
