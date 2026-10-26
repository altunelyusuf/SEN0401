#!/usr/bin/env python3
"""sen0401_erd_collision_probe v1_0_0 (the lineage agent's, over the executor's erd_diag_v1_0_0.py of the ch11 page 9.79.0): for the NEWEST page of each given chapter (or the page file named), opens the sections ERD, drags the first entity as the page test does, and reports, for the entity the test then taps (the first relationship's entity), whether the element on top at its centre is that entity. Prints: chapter page, entity count, widest and narrowest box, pitch, tap target, top element, COLLISION or CLEAR. Exit 0 always (it measures). Run only under the lock.
Usage: sen0401_erd_collision_probe_v1_0_0.py NN [NN..]  |  FILE.html"""
import glob, os, re, sys
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.html", p).groups()]
def probe(pg, P):
    pg.goto("file://" + P); pg.wait_for_timeout(2500)
    try:
        pg.evaluate("showTab('ontoerd')"); pg.wait_for_timeout(1200); pg.click('[data-erd="sections"]'); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{ERD_LAY.sel=null;erdRender()}")
        g0 = pg.locator("#oerd .oe-e").first; bb = g0.bounding_box(); box = pg.locator("#oerd").bounding_box(); dx = 1 if bb["x"] + bb["width"]/2 < box["x"] + box["width"]/2 else -1
        pg.mouse.move(bb["x"]+12, bb["y"]+10); pg.mouse.down(); pg.mouse.move(bb["x"]+dx*60, bb["y"]+40, steps=5); pg.mouse.move(bb["x"]+dx*120, bb["y"]+70, steps=5); pg.mouse.up(); pg.wait_for_timeout(500)
        ents = pg.evaluate("()=>[...document.querySelectorAll('#oerd .oe-e')].map(g=>{const r=g.getBoundingClientRect();return [g.dataset.ent,r.x,r.y,r.width,r.height]})")
        ti = pg.evaluate("()=>{const r=document.querySelector('#oerd .oe-r');if(!r)return 2;const i=[...document.querySelectorAll('#oerd .oe-e')].findIndex(e=>e.dataset.ent===r.dataset.a);return i<0?2:i}")
        t = pg.locator("#oerd .oe-e").nth(ti); tb = t.bounding_box(); cx, cy = tb["x"]+tb["width"]/2, tb["y"]+tb["height"]/2
        top = pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);const g=e&&e.closest('.oe-e');return g?g.dataset.ent:(e?e.tagName:'none')}", [cx, cy])
        tgt = t.get_attribute("data-ent"); ws = [e[3] for e in ents]
        return "entities %d, box width %d to %d, target %s, element on top at its centre: %s -> %s" % (len(ents), min(ws), max(ws), tgt, top, "CLEAR" if top == tgt else "COLLISION")
    except Exception as e:
        return "NOT_MEASURED: " + str(e)[:160]
with sync_playwright() as p:
    b = p.chromium.launch()
    for a in sys.argv[1:]:
        P = a if a.endswith(".html") else sorted(glob.glob(os.path.join(R, "03-materials", "ch" + a, "page", "sen0401_ch%s_page_v*.html" % a)), key=vk)[-1]
        pg = b.new_page(viewport={"width": 1400, "height": 900}); print(os.path.basename(P), probe(pg, P), flush=True); pg.close()
    b.close()
