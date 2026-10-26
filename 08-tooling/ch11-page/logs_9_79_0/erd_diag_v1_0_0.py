import sys, json
from playwright.sync_api import sync_playwright
P = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1400,"height":900})
    pg.goto("file://" + P); pg.wait_for_timeout(3000)
    pg.evaluate("showTab('ontoerd')"); pg.wait_for_timeout(1500)
    print("visible oerd:", pg.locator("#oerd").is_visible(), pg.locator("#oerd [data-ent]").count())
    pg.click('[data-erd="sections"]'); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ERD_LAY.sel=null;erdRender()}")
    ents = pg.evaluate("()=>[...document.querySelectorAll('#oerd .oe-e')].map(g=>{const r=g.getBoundingClientRect();return [g.dataset.ent,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]})")
    for e in ents[:6]: print(e)
    g0 = pg.locator("#oerd .oe-e").first; bb = g0.bounding_box(); box = pg.locator("#oerd").bounding_box()
    dx = 1 if bb["x"] + bb["width"]/2 < box["x"] + box["width"]/2 else -1
    print("bb", bb, "oerd", box, "dx", dx)
    pg.mouse.move(bb["x"]+12, bb["y"]+10); pg.mouse.down(); pg.mouse.move(bb["x"]+dx*60, bb["y"]+40, steps=5); pg.mouse.move(bb["x"]+dx*120, bb["y"]+70, steps=5); pg.mouse.up(); pg.wait_for_timeout(600)
    ents = pg.evaluate("()=>[...document.querySelectorAll('#oerd .oe-e')].map(g=>{const r=g.getBoundingClientRect();return [g.dataset.ent,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]})")
    for e in ents[:6]: print("after", e)
    _ti = pg.evaluate("()=>{const r=document.querySelector('#oerd .oe-r');if(!r)return 2;const i=[...document.querySelectorAll('#oerd .oe-e')].findIndex(e=>e.dataset.ent===r.dataset.a);return i<0?2:i}")
    print("_ti", _ti)
    t = pg.locator("#oerd .oe-e").nth(_ti); tb = t.bounding_box(); cx, cy = tb["x"]+tb["width"]/2, tb["y"]+tb["height"]/2
    print("target", t.get_attribute("data-ent"), tb, "centre", cx, cy, "top element:", pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);const g=e.closest('.oe-e');return g?g.dataset.ent:e.tagName}", [cx, cy]))
    b.close()
