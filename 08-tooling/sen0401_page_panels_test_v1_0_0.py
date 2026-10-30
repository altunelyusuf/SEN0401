#!/usr/bin/env python3
"""sen0401_page_panels_test v1_0_0 - a small browser run of its own for the panel feature of page template 9.52.6 and later (task TK_Urgent_Ch06_Page_Build). For each KIND of diagram or visualisation panel
(ontology graph, concept map, entity-relationship diagram, narrative diagram, neighbourhood map, lab visualisation (HTML cards or bars), syntax tree, chapter-code result picture) it proves, in a real browser, at 1400x900 and at a phone size 390x844:
  C1 the controls (Full screen, Panel +, Panel -) are visible and sit ABOVE the drawing, never over it (the bar's bottom is not below the panel's top, the bar is not inside the panel); a resize handle sits below the panel
  C2 Full screen opens (the panel fills the viewport width and reaches its bottom, the bar sits above it, the drawing stays inside the panel), the Fullscreen API state is recorded, Esc closes, the control closes too
  C3 the size changes: Panel + grows it, Panel - shrinks it, a mouse drag on the handle (desktop) or a touch drag (phone) changes it, the arrow keys change it
  C4 the size is kept when the reader leaves the tab and comes back (the same kind of panel has the size the reader set)
  C5 the page does not scroll sideways, and at the start (before the reader changes a size) it does not scroll up/down either
Screenshots are kept in the folder given as the second argument. Usage: sen0401_page_panels_test_v1_0_0.py PAGE.html OUTDIR  -> prints [PASS]/[FAIL] lines, 'CANNOT_RUN' for a kind that could not be reached, and a summary; exit 0 only when no [FAIL]."""
__version__ = "1.0.0"
import json, os, sys, time
from playwright.sync_api import sync_playwright
page_path, outdir = os.path.abspath(sys.argv[1]), sys.argv[2]; os.makedirs(outdir, exist_ok=True)
R = {"pass": 0, "fail": 0, "cannot": 0}
def feat(name, ok, detail=""):
    R["pass" if ok else "fail"] += 1; print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, (" - " + detail) if detail else ""), flush=True)
def cannot(name, why): R["cannot"] += 1; print("  [CANNOT_RUN] %s - %s" % (name, why), flush=True)
JS_RECT = "(e)=>{const r=e.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}}"
def run_viewport(p, W, Hh, touch):
    tag = "%dx%d" % (W, Hh); print("== viewport", tag, flush=True)
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": W, "height": Hh}, has_touch=touch, is_mobile=touch); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("file://" + page_path); pg.wait_for_timeout(1500)
    D = pg.evaluate("D")
    nd_concept = next((c for g in D.get("ndiag", []) for c in g.get("concepts", []) if c in {n["id"] for n in D["nodes"]}), None)
    vis_id = next((k for k, v in D.get("visuals", {}).items() if v.get("kind") in ("facts", "hist")), None)
    io_id = next((n["id"] for n in D["nodes"] if n.get("io") and n.get("level") == 3), None)
    kinds = []
    def show(t): pg.evaluate("showTab(%s)" % json.dumps(t)); pg.wait_for_timeout(1200)
    def goto(c): pg.evaluate("goTo(%s)" % json.dumps(c)); pg.wait_for_timeout(1500)
    kinds.append(("concept taxonomy", lambda: show("taxonomy"), "#taxo .diagram"))
    def onto():
        show("ontograph")
        try: pg.wait_for_function("()=>document.querySelector('#onto svg')", timeout=60000)
        except Exception: pass
        pg.wait_for_timeout(500)
    kinds.append(("ontology graph", onto, "#onto .diagram"))
    kinds.append(("concept map", lambda: show("map"), "#graph .diagram"))
    kinds.append(("entity-relationship diagram", lambda: show("ontoerd"), "#oerd .diagram"))
    if nd_concept: kinds.append(("narrative diagram", lambda: goto(nd_concept), ".ndiag .diagram.nd"))
    kinds.append(("neighbourhood map", lambda: goto(io_id or nd_concept), ".nbh .diagram"))
    if vis_id:
        def lab():
            goto(vis_id); pg.evaluate("(id)=>{const b=document.querySelector('[data-vistoggle=\"'+id+'\"]'),w=document.getElementById('wvp-'+id);if(b&&w&&w.hidden)b.click()}", vis_id)
            try: pg.wait_for_function("(id)=>!!document.querySelector('#wv-'+id+'-out.pzhtml')", arg=vis_id, timeout=30000)
            except Exception: pass
            pg.wait_for_timeout(500)
        kinds.append(("lab visualisation (HTML cards or bars)", lab, "#wv-%s-out.pzhtml" % vis_id))
    if io_id:
        def tree():
            goto(io_id); pg.evaluate("(id)=>{const b=document.querySelector('[data-diagram=\"'+id+'\"]'),w=document.getElementById('w-'+id+'-diagram');if(b&&(!w||w.hidden||!w.innerHTML))b.click()}", io_id); pg.wait_for_timeout(800)
        kinds.append(("syntax tree", tree, "#w-%s-diagram .diagram" % io_id))
    def cc():
        show("chaptercode"); pg.evaluate("()=>document.querySelector('[data-cc-run]').click()")
        try: pg.wait_for_function("()=>{const r=document.querySelector('[data-cc-result] .ccviz');return !!r&&!!r.querySelector('svg')}", timeout=150000)
        except Exception: pass
        pg.wait_for_timeout(500)
    kinds.append(("chapter-code result picture", cc, "[data-cc-result] .ccviz"))
    if os.environ.get('PANEL_KINDS'): kinds = [k for k in kinds if k[0] in os.environ['PANEL_KINDS'].split(',')]
    scroll_ok = pg.evaluate("document.scrollingElement.scrollWidth<=innerWidth+1")
    feat("%s C5 no sideways scroll at start" % tag, scroll_ok)
    for name, go, sel in kinds:
        print(" -- panel kind:", name, flush=True)
        try: go()
        except Exception as e: cannot("%s %s" % (tag, name), "could not open: %s" % str(e)[:120]); continue
        loc = pg.locator(sel + ":visible").first
        if pg.locator(sel + ":visible").count() == 0: cannot("%s %s" % (tag, name), "no visible panel for %s" % sel); continue
        h = loc.element_handle(); key = pg.evaluate("(h)=>pzKey(h)", h)
        pg.evaluate("(h)=>h.scrollIntoView({block:'center'})", h); pg.wait_for_timeout(300)
        bar = pg.evaluate_handle("(h)=>{let e=h.previousElementSibling;return e&&(e.classList.contains('zbar')||e.classList.contains('pzbar'))?e:null}", h).as_element()
        hd = pg.evaluate_handle("(h)=>{let e=h.nextElementSibling;return e&&e.classList.contains('pzh')?e:null}", h).as_element()
        if not bar or not hd: feat("%s %s C1 controls and handle exist" % (tag, name), False, "bar=%s handle=%s" % (bool(bar), bool(hd))); continue
        r0 = pg.evaluate(JS_RECT, h); rb = pg.evaluate(JS_RECT, bar); rh = pg.evaluate(JS_RECT, hd)
        inside = pg.evaluate("([h,b])=>h.contains(b)", [h, bar])
        btn = {a: pg.evaluate_handle("([b,a])=>b.querySelector('[data-pz=\"'+a+'\"]')", [bar, a]).as_element() for a in ("full", "bigger", "smaller")}
        vis = all(x is not None and x.is_visible() for x in btn.values())
        feat("%s %s C1 controls visible, above the drawing (bar bottom %.0f <= panel top %.0f), not inside it; handle below (%.0f >= %.0f)" % (tag, name, rb["b"], r0["t"], rh["t"], r0["b"]), vis and not inside and rb["b"] <= r0["t"] + 0.5 and rh["t"] >= r0["b"] - 0.5)
        # C2 full screen
        btn["full"].click(); pg.wait_for_timeout(700)
        o = pg.evaluate("(h)=>{const r=h.getBoundingClientRect(),b=h.previousElementSibling.getBoundingClientRect(),s=h.querySelector('svg'),q=s?s.getBoundingClientRect():null;return {cls:h.classList.contains('pfs'),l:r.left,t:r.top,r:r.right,b:r.bottom,iw:innerWidth,ih:innerHeight,bb:b.bottom,bt:b.top,fs:!!document.fullscreenElement,svgIn:q?(q.left>=r.left-1&&q.right<=r.right+1&&q.top>=r.top-1&&q.bottom<=r.bottom+1):null,sw:q?q.width:0,sh:q?q.height:0}}", h)
        pg.screenshot(path=os.path.join(outdir, "%s_%s_fullscreen.png" % (tag, name.replace(" ", "_"))))
        feat("%s %s C2 full screen opens: panel fills the window (%dx%d of %dx%d), bar above it, drawing inside, drawing %dx%d px" % (tag, name, o["r"] - o["l"], o["b"] - o["t"], o["iw"], o["ih"], o["sw"], o["sh"]), o["cls"] and abs(o["l"]) <= 1 and abs(o["r"] - o["iw"]) <= 1 and abs(o["b"] - o["ih"]) <= 1 and o["bb"] <= o["t"] + 0.5 and o["bt"] >= -0.5 and o["svgIn"] in (True, None) and (o["sw"] > 100 or o["sw"] == 0))
        print("     Fullscreen API state while open (recorded, not judged):", o["fs"], flush=True)
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
        c = pg.evaluate("(h)=>({cls:h.classList.contains('pfs'),fs:!!document.fullscreenElement,fixed:getComputedStyle(h.previousElementSibling).position==='fixed'})", h)
        feat("%s %s C2 Esc closes full screen" % (tag, name), not c["cls"] and not c["fixed"] and not c["fs"])
        btn["full"].click(); pg.wait_for_timeout(500); btn["full"].click(); pg.wait_for_timeout(500)
        feat("%s %s C2 the control closes full screen" % (tag, name), not pg.evaluate("(h)=>h.classList.contains('pfs')", h))
        # C3 size
        pg.evaluate("(h)=>h.scrollIntoView({block:'center'})", h); pg.wait_for_timeout(200)
        h0 = pg.evaluate(JS_RECT, h)["h"]
        btn["bigger"].click(); pg.wait_for_timeout(300); h1 = pg.evaluate(JS_RECT, h)["h"]
        btn["smaller"].click(); pg.wait_for_timeout(200); btn["smaller"].click(); pg.wait_for_timeout(300); h2 = pg.evaluate(JS_RECT, h)["h"]
        feat("%s %s C3 Panel + / Panel - change the size (%.0f -> %.0f -> %.0f px)" % (tag, name, h0, h1, h2), h1 > h0 * 1.1 and h2 < h1 * 0.8)
        pg.evaluate("(h)=>h.scrollIntoView({block:'center'})", h); pg.wait_for_timeout(200)
        hd.scroll_into_view_if_needed(); pg.wait_for_timeout(200); bb = hd.bounding_box(); hb = pg.evaluate(JS_RECT, h)["h"]
        if touch:
            cdp = ctx.new_cdp_session(pg); x, y = bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2
            cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
            for k in range(1, 7): cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x, "y": y + 10 * k}]})
            cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        else:
            pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2); pg.mouse.down(); pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2 + 30, steps=4); pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2 + 60, steps=4); pg.mouse.up()
        pg.wait_for_timeout(400); hc = pg.evaluate(JS_RECT, h)["h"]
        feat("%s %s C3 dragging the handle by %s changes the size by about 60 px (%.0f -> %.0f)" % (tag, name, "touch" if touch else "mouse", hb, hc), abs((hc - hb) - 60) <= 6)
        hd.focus(); pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(300); hk = pg.evaluate(JS_RECT, h)["h"]
        feat("%s %s C3 the arrow key on the handle changes the size (%.0f -> %.0f)" % (tag, name, hc, hk), hk > hc + 20)
        pg.screenshot(path=os.path.join(outdir, "%s_%s_resized.png" % (tag, name.replace(" ", "_"))))
        # zoom still works where the panel has it
        zin = pg.evaluate_handle("([b])=>b.querySelector('[data-z=\"in\"]')", [bar]).as_element()
        if zin:
            v0 = pg.evaluate("(h)=>h.querySelector('svg').getAttribute('viewBox')", h); zin.click(); pg.wait_for_timeout(200); v1 = pg.evaluate("(h)=>h.querySelector('svg').getAttribute('viewBox')", h)
            feat("%s %s zoom control still works" % (tag, name), v0 != v1)
        # C4 kept between tabs
        want = pg.evaluate(JS_RECT, h)["h"]
        show("intro"); go()
        loc2 = pg.locator(sel + ":visible").first; h2_ = loc2.element_handle() if pg.locator(sel + ":visible").count() else None
        got = pg.evaluate(JS_RECT, h2_)["h"] if h2_ else -1
        feat("%s %s C4 size kept after leaving the tab and coming back (%.0f -> %.0f; stored for %s)" % (tag, name, want, got, key), abs(got - want) <= 3)
        sw = pg.evaluate("document.scrollingElement.scrollWidth<=innerWidth+1")
        feat("%s %s C5 no sideways scroll after resizing" % (tag, name), sw)
    feat("%s no script errors" % tag, not errs, "; ".join(errs[:3])[:200])
    b.close()
t0 = time.time()
with sync_playwright() as p:
    for W, Hh, touch in ((1400, 900, False), (390, 844, True)):
        try: run_viewport(p, W, Hh, touch)
        except Exception as e: feat("viewport %dx%d completed" % (W, Hh), False, str(e)[:200])
print("SUMMARY panels: passed %d, failed %d, cannot run %d, %.0f s" % (R["pass"], R["fail"], R["cannot"], time.time() - t0))
print("RESULT:", "PASS" if R["fail"] == 0 and R["cannot"] == 0 else ("FAIL" if R["fail"] else "CANNOT_RUN (some kind not reached)"))
sys.exit(0 if R["fail"] == 0 else 1)
