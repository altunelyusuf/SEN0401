# diagnostic only: the beforeinput / input events one pg.fill of a multi-line text produces in an example editor, and what a single typed key produces
import json, sys
from playwright.sync_api import sync_playwright
page = sys.argv[1]; i = "TransactionSerialization"; data = json.load(open("/home/claude/sen0401/08-tooling/ch03-page/page_data_v9_74_0.json")); code = [n["io"]["code"] for n in data["nodes"] if n["id"] == i][0]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(viewport={"width": 1400, "height": 900}).new_page()
    pg.goto("file://" + page); pg.wait_for_timeout(5000); pg.evaluate("id=>goTo(id)", i); pg.wait_for_timeout(300)
    pg.evaluate("""()=>{window.__ev=[];for(const t of ['beforeinput','input'])document.addEventListener(t,e=>window.__ev.push([t,e.inputType,e.data===null?null:e.data.length,e.timeStamp]),true)}""")
    pg.fill("#w-%s-code" % i, code); ev = pg.evaluate("window.__ev")
    print("fill: events", len(ev)); print(ev[:6]); print("types:", sorted(set((e[0], e[1], e[2] is None) for e in ev)))
    print("span of timestamps ms", round(ev[-1][3] - ev[0][3], 1))
    pg.evaluate("window.__ev=[]"); pg.click("#w-%s-code" % i); pg.keyboard.type("ab"); print("typed:", pg.evaluate("window.__ev"))
    b.close()
