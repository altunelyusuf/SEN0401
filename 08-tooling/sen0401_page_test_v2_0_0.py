#!/usr/bin/env python3
"""Browser tests for version 2 of a SEN0401 chapter page: each capability the owner asked for is exercised
in headless Chromium, and every example widget must print, via Pyodide, exactly what the build's own
interpreter printed. Results go to test_results_v2.json; the page ABox marks a widget tested only on a pass."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0401_ch%s_page_v2_0_0.html" % N))
d = json.load(open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "page_data_v2.json")))
AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
R = {"widgets": {}, "features": {}, "gates": {}}
def feat(k, ok, detail=""): R["features"][k] = {"passed": bool(ok), "detail": detail}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 900}); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto("file://" + page_path); pg.wait_for_timeout(300)
    top = [n for n in d["nodes"] if n["level"] == 1][0]; mid = [n for n in d["nodes"] if n["parent"] == top["id"]][0]
    # explorer tree
    li = pg.locator('#tree li[data-id="%s"]' % top["id"]); li.locator(":scope > .tn > .tw").click()
    opened = pg.locator('#tree li[data-id="%s"] > .tn' % mid["id"]).is_visible()
    pg.click("#collapseAll"); closed = not pg.locator('#tree li[data-id="%s"] > .tn' % mid["id"]).is_visible()
    pg.click("#expandAll"); all_open = all(pg.locator("#tree .tn").nth(k).is_visible() for k in range(pg.locator("#tree .tn").count()))
    feat("explorer tree: expand, collapse, expand all", opened and closed and all_open, "%d nodes" % pg.locator("#tree .tn").count())
    feat("explorer icons by level", all(pg.locator("#tree .ico").nth(k).text_content() in ("📁", "📂", "🔷") for k in range(pg.locator("#tree .ico").count())))
    # tabs and sub-tabs
    pg.click('#tabs [data-tab="%s"]' % top["id"]); mids = [n for n in d["nodes"] if n["parent"] == top["id"]]
    pg.click('[data-sub="%s"]' % mids[-1]["id"])
    feat("subject tabs and sub-tabs", pg.locator('[data-subpane="%s"]' % mids[-1]["id"]).is_visible() and not pg.locator('[data-subpane="%s"]' % mids[0]["id"]).is_visible())
    # right card and jumps
    leaf = [n for n in d["nodes"] if n["level"] == 3 and "io" in n][0]
    pg.click('#tree .tn[data-c="%s"]' % leaf["id"]); card = pg.text_content("#card")
    feat("concept card opens on activation", leaf["label"] in card and leaf["io"]["out"] in card)
    pg.locator("#card [data-go]").first.click(); feat("jump from card to related subject", pg.locator("#card h3").is_visible())
    # context menu and tooltip
    pg.click('#tabs [data-tab="%s"]' % top["id"]); pg.click('#tree .tn[data-c="%s"]' % leaf["id"], button="right")
    feat("right-click context menu", pg.is_visible("#ctx") and pg.locator("#ctx button").count() >= 5, "%d actions" % pg.locator("#ctx button").count())
    pg.keyboard.press("Escape"); pg.hover('#tree .tn[data-c="%s"]' % leaf["id"])
    feat("tooltips", pg.is_visible("#tip") and leaf["label"] in pg.text_content("#tip"))
    # taxonomy and concept map
    pg.click('#tabs [data-tab="taxonomy"]'); feat("chapter taxonomy diagram", pg.locator("#taxo svg g.n").count() == len(d["nodes"]), "%d boxes" % pg.locator("#taxo svg g.n").count())
    pg.click('#tabs [data-tab="map"]'); feat("concept map with evidenced relations", pg.locator("#graph g.gn").count() == len(d["nodes"]) and pg.locator("#graph line").count() == len(d["relations"]),
        "%d nodes, %d edges" % (pg.locator("#graph g.gn").count(), pg.locator("#graph line").count()))
    pg.locator("#graph g.gn").nth(5).click(); feat("map node opens its card", pg.text_content("#card h3") != "Concept details")
    # every example widget: edit-run through Pyodide must print what the build interpreter printed
    t0 = time.time()
    for n in d["nodes"]:
        w = "w-" + n["id"]; ok = False; why = ""
        try:
            goto = n["id"]; pg.evaluate("id=>goTo(id)", goto)
            if "io" in n:
                pg.fill("#%s-guess" % w, n["io"]["out"]); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent&&o.textContent!=='running...'}", arg=w + "-out", timeout=120000)
                got = pg.text_content("#%s-out" % w); ok = got == n["io"]["out"] and "matched" in pg.text_content("#%s-verdict" % w); why = "Pyodide printed %r" % got
                shown = pg.locator("#card output.out").first.text_content().split("\n", 1)[-1]
                ok = ok and shown == n["io"]["out"]; why += "; card shows %r" % shown
                pg.click('[data-diagram="%s"]' % n["id"]); ok = ok and pg.locator("#%s-diagram svg g.n" % w).count() > 0; why += "; diagram drawn"
                pg.fill("#%s-code" % w, n["io"]["code"] + " "); pg.click('[data-reset="%s"]' % n["id"]); ok = ok and pg.input_value("#%s-code" % w) == n["io"]["code"]; why += "; edit and reset"
            elif n["level"] == 3:
                pg.click('[data-step="%s"]' % w); ok = pg.locator("#%s li" % w).nth(1).is_visible(); why = "second step revealed"
            else:
                pg.locator("#%s .chip" % w).first.click(); ok = pg.text_content("#card h3") != "Concept details"; why = "chip opens its card"
        except Exception as e:
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:90])
        R["widgets"][w] = {"passed": ok, "detail": why}
    feat("Pyodide editing and running", all(v["passed"] for k, v in R["widgets"].items() if "io" in d["nodes"][[n["id"] for n in d["nodes"]].index(k[2:])]), "%.0fs incl. load" % (time.time() - t0))
    # playground with input()
    pg.click('#tabs [data-tab="play"]'); pg.select_option("#pex", "first"); pg.click("#pload"); pg.fill("#pin", "SEN0401|4"); pg.click("#prun")
    pg.wait_for_function("()=>document.getElementById('pout').textContent!=='running...'", timeout=60000); out = pg.text_content("#pout")
    feat("playground runs a full program with input()", "nonce 15083 gives 0000" in out, out.replace("\n", " | ")[:120])
    # agents: grounded answer, code run, out-of-scope refusal
    a = [x for x in d["agents"] if any("io" in [n for n in d["nodes"] if n["id"] == c][0] for c in x["covers"])][0]
    pg.click('#tabs [data-tab="agents"]'); pg.fill("#%s-q" % a["id"], "what is %s" % [n for n in d["nodes"] if n["id"] == a["covers"][0]][0]["label"].lower()); pg.click('[data-ask="%s"]' % a["id"])
    ans = pg.text_content("#%s-log" % a["id"])
    code = [n for n in d["nodes"] if n["id"] in a["covers"] and "io" in n][0]["io"]
    pg.fill("#%s-q" % a["id"], "run `%s`" % code["code"]); pg.click('[data-ask="%s"]' % a["id"])
    pg.wait_for_function("id=>document.getElementById(id).textContent.includes('Python printed')", arg=a["id"] + "-log", timeout=60000)
    ran = code["out"] in pg.text_content("#%s-log" % a["id"])
    pg.fill("#%s-q" % a["id"], "how do I bake bread"); pg.click('[data-ask="%s"]' % a["id"]); refused = "outside what I cover" in pg.text_content("#%s-log" % a["id"])
    feat("subject agents: grounded answer, runs code, refuses out-of-scope", len(ans) > 40 and ran and refused, "%d agents: %s" % (len(d["agents"]), ", ".join(x["name"] for x in d["agents"])))
    # quiz
    pg.click('#tabs [data-tab="quiz"]'); fs = pg.locator("fieldset"); qok = True
    for k in range(fs.count()):
        f = fs.nth(k); f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("button").click(); qok &= pg.text_content("#q%d-fb" % k) == "Correct."
    feat("quiz", qok)
    R["gates"]["Stage4.C console errors"] = errors
    R["gates"]["Stage4.D dialogs"] = pg.locator('[role="dialog"],dialog').count()
    R["gates"]["Stage4.E sections"] = pg.locator("section[data-source]").count()
    m = b.new_page(viewport={"width": 390, "height": 844}); m.goto("file://" + page_path)
    R["gates"]["Stage4.F subjects visible on mobile without clicks"] = all(m.locator("#groups button").nth(k).is_visible() for k in range(m.locator("#groups button").count()))
    pg.click('#tabs [data-tab="intro"]'); pg.add_script_tag(path=AXE)
    R["gates"]["WCAG 2 AA (axe-core)"] = pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length])}")
    b.close()
json.dump(R, open(os.environ.get("RESULTS", os.path.join(REPO, "08-tooling", "ch%s-page" % N, "test_results_v2.json")), "w"), indent=1)
bad = [k for k, v in R["widgets"].items() if not v["passed"]]
print("widgets: %d tested, %d passed; failing: %s" % (len(R["widgets"]), len(R["widgets"]) - len(bad), [(k, R["widgets"][k]["detail"]) for k in bad[:3]]))
for k, v in R["features"].items(): print("  [%s] %s  %s" % ("PASS" if v["passed"] else "FAIL", k, v["detail"]))
for k, v in R["gates"].items(): print("  %-52s %s" % (k, v))
