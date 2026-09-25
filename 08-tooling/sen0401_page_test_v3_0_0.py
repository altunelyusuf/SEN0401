#!/usr/bin/env python3
"""Browser tests for version 3 of a SEN0401 page - the owner's rules of 2026-09-25 made checkable:
code the student edits really runs (edited code must change the result); agents answer from their own
slice, so different questions get different answers; a menu click changes the main area and leaves the
detail card closed; the card opens only on an explicit request; the tab row is the sub-menu of the
selected top-level item. Every stored result must also equal what the build's interpreter printed."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
N = sys.argv[1]; NUM = N; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, os.environ.get("PAGE_VER", "3_0_0"))))
d = json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "page_data_v2.json")))
AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
R = {"widgets": {}, "features": {}, "gates": {}}
feat = lambda k, ok, det="": R["features"].__setitem__(k, {"passed": bool(ok), "detail": det})
nodes = d["nodes"]; tops = [n for n in nodes if n["level"] == 1]
in_view = "id=>{const e=document.getElementById(id);if(!e)return false;const r=e.getBoundingClientRect();return r.height>0&&r.top<innerHeight&&r.bottom>0&&!e.closest('[hidden]')}"
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}); pg = ctx.new_page(); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto("file://" + page_path); pg.wait_for_timeout(400)
    # one top-level menu; tabs inside a subject are its sub-menu
    labels = [pg.locator("#groups button").nth(k).get_attribute("data-tab") for k in range(pg.locator("#groups button").count())]
    top2 = next(t for t in tops if len([n for n in nodes if n["parent"] == t["id"]]) >= 2)
    pg.click('#groups [data-tab="%s"]' % top2["id"])
    mids = [n for n in nodes if n["parent"] == top2["id"]]
    sub_in_pane = pg.locator('[data-pane="%s"] .subtabs button' % top2["id"]).count()
    pg.click('[data-sub="%s"]' % mids[-1]["id"])
    feat("one top menu; the tab row is the selected item's sub-menu", pg.locator("#tabs").count() == 0 and labels[0] == "intro" and all(t["id"] in labels for t in tops) and sub_in_pane == len(mids)
         and pg.locator('[data-subpane="%s"]' % mids[-1]["id"]).is_visible() and not pg.locator('[data-subpane="%s"]' % mids[0]["id"]).is_visible(), "top menu: %s" % ", ".join(labels))
    # the explorer drives the main area; the card stays closed
    leaf = [n for n in nodes if n["level"] == 3 and n["parent"] != mids[-1]["id"]][0]
    pg.click("#expandAll"); pg.click('#tree .tn[data-c="%s"]' % leaf["id"]); pg.wait_for_timeout(300)
    feat("menu click changes the main area first, card stays closed", pg.evaluate(in_view, "s-" + leaf["id"]) and pg.locator("#card").is_hidden(), leaf["label"])
    pg.click('[data-detail="%s"]' % leaf["id"]); opened = pg.locator("#card").is_visible() and leaf["label"] in pg.text_content("#card")
    pg.click("#card [data-close]"); closed = pg.locator("#card").is_hidden()
    pg.click('[data-detail="%s"]' % leaf["id"]); pg.keyboard.press("Escape")
    feat("detail card only on explicit request; closes by button and Esc", opened and closed and pg.locator("#card").is_hidden())
    pg.click('#tree .tn[data-c="%s"]' % leaf["id"], button="right"); menu_ok = pg.is_visible("#ctx"); pg.locator('#ctx [data-cmd^="card:"]').click()
    feat("context menu offers details on request", menu_ok and pg.locator("#card").is_visible()); pg.keyboard.press("Escape")
    pg.hover('#tree .tn[data-c="%s"]' % leaf["id"]); feat("tooltips", pg.is_visible("#tip"))
    pg.click('#groups [data-tab="map"]'); g = pg.locator("#graph g.gn").nth(4); gid = g.get_attribute("data-c"); g.click(); pg.wait_for_timeout(300)
    feat("map node navigates the main area, card stays closed", pg.evaluate(in_view, "s-" + gid) and pg.locator("#card").is_hidden(), gid)
    pg.click('#groups [data-tab="taxonomy"]'); feat("taxonomy diagram", pg.locator("#taxo svg g.n").count() == len(nodes))
    # widgets
    for n in nodes:
        w = "w-" + n["id"]; ok = False; why = ""
        try:
            pg.evaluate("id=>goTo(id)", n["id"])
            if "io" in n:
                pg.fill("#%s-code" % w, n["io"]["code"]); pg.fill("#%s-guess" % w, n["io"]["out"]); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent&&o.textContent!=='running...'}", arg=w + "-out", timeout=120000)
                got = pg.text_content("#%s-out" % w); ok = got == n["io"]["out"] and "matched" in pg.text_content("#%s-verdict" % w); why = "printed %r" % got
                pg.fill("#%s-code" % w, "2 + 2"); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent!=='running...'}", arg=w + "-out", timeout=60000)
                edited = pg.text_content("#%s-out" % w); ok = ok and edited == "4"; why += "; edited to 2 + 2 printed %r" % edited
                pg.click('[data-reset="%s"]' % n["id"]); ok = ok and pg.input_value("#%s-code" % w) == n["io"]["code"]
                pg.click('[data-detail="%s"]' % n["id"]); shown = pg.locator("#card output.out").first.text_content().split("\n", 1)[-1]; pg.keyboard.press("Escape")
                ok = ok and shown == n["io"]["out"]; why += "; card shows %r" % shown
            elif n.get("chart"):
                pg.wait_for_function("id=>{const c=document.getElementById(id);const ch=c&&window.Chart&&Chart.getChart(c);return ch&&ch.data.datasets.some(x=>x.data&&x.data.length)&&c.offsetWidth>0}", arg=n["chart"], timeout=20000)
                ok = True; why = "chart %s drawn" % n["chart"]
            elif n["level"] == 3:
                pg.click('[data-step="%s"]' % w); ok = pg.locator("#%s li" % w).nth(1).is_visible(); why = "second step revealed"
            else:
                chip = pg.locator("#%s .chip" % w).first; cid = chip.get_attribute("data-c"); chip.click(); pg.wait_for_timeout(200)
                ok = pg.evaluate(in_view, "s-" + cid) and pg.locator("#card").is_hidden(); why = "chip navigates to its section"
        except Exception as e:
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:100])
        R["widgets"][w] = {"passed": ok, "detail": why}
    ios = [n for n in nodes if "io" in n]
    feat("edited code really runs: every example re-run after editing prints the new result", all(R["widgets"]["w-" + n["id"]]["passed"] for n in ios), "%d examples" % len(ios))
    pg.click('#groups [data-tab="play"]'); pg.fill("#pcode", "x = 7\nx * 6"); pg.click("#prun")
    pg.wait_for_function("()=>document.getElementById('pout').textContent!=='running...'", timeout=60000); free = pg.text_content("#pout")
    feat("playground runs code typed from scratch", free == "42", repr(free))
    # agents answer from their own slice: different questions, different answers
    a = max(d["agents"], key=lambda x: len(x["covers"])); pg.click('#groups [data-tab="agents"]')
    q1 = [n for n in nodes if n["id"] == a["covers"][0]][0]["label"]; q2 = [n for n in nodes if n["id"] == a["covers"][-2]][0]["label"] if len(a["covers"]) > 2 else a["covers"][-1]
    def ask(q):
        before = pg.locator("#%s-log .msg" % a["id"]).count(); pg.fill("#%s-q" % a["id"], q); pg.click('[data-ask="%s"]' % a["id"])
        pg.wait_for_function("([id,n])=>document.querySelectorAll('#'+id+'-log .msg').length>=n+2&&!document.querySelector('#'+id+'-log').textContent.endsWith('...')", arg=[a["id"], before], timeout=60000)
        return pg.locator("#%s-log .msg" % a["id"]).last.text_content()
    ans1, ans2, ans3 = ask("what is " + q1.lower()), ask("explain " + q2.lower()), ask("how do I bake bread")
    feat("agents answer from their own slice; different questions get different answers", ans1 != ans2 and len(ans1) > 40 and len(ans2) > 40 and ("nothing on that" in ans3),
         "%s | %s | %s" % (ans1[:60], ans2[:60], ans3[:60]))
    pg.click('#groups [data-tab="quiz"]'); fs = pg.locator("fieldset"); qok = True
    for k in range(fs.count()):
        f = fs.nth(k); f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("button").click(); qok &= pg.text_content("#q%d-fb" % k) == "Correct."
    feat("quiz", qok)
    R["gates"]["Stage4.C console errors"] = errors
    R["gates"]["Stage4.D dialogs"] = pg.locator('[role="dialog"],dialog').count()
    R["gates"]["Stage4.E sections"] = pg.locator("section[data-source]").count()
    m = ctx.new_page(); m.set_viewport_size({"width": 390, "height": 844}); m.goto("file://" + page_path)
    R["gates"]["Stage4.F top menu visible on mobile without clicks"] = m.locator("#groups button").first.is_visible()
    pg.click('#groups [data-tab="intro"]'); pg.add_script_tag(path=AXE)
    R["gates"]["WCAG 2 AA (axe-core)"] = pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length])}")
    b.close()
json.dump(R, open(os.environ.get("RESULTS", os.path.join(REPO, "08-tooling", "%s-page" % N, "test_results_v2.json")), "w"), indent=1)
bad = [k for k, v in R["widgets"].items() if not v["passed"]]
print("widgets: %d tested, %d passed; failing: %s" % (len(R["widgets"]), len(R["widgets"]) - len(bad), [(k, R["widgets"][k]["detail"][:120]) for k in bad[:3]]))
for k, v in R["features"].items(): print("  [%s] %s  %s" % ("PASS" if v["passed"] else "FAIL", k, v["detail"][:150]))
for k, v in R["gates"].items(): print("  %-52s %s" % (k, v))
