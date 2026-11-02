#!/usr/bin/env python3
"""Screenshots (brief point 8): student view, after the check, print view at 390 px and 1280 px. Run under flock /tmp/page_test.lock. Usage: HTML OUTDIR"""
import sys, os, json, random
from playwright.sync_api import sync_playwright
html, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w, h in ((390, 800), (1280, 900)):
        pg = br.new_context(viewport={"width": w, "height": h}).new_page()
        pg.goto("file://" + html + "#k=2&seed=1074"); pg.wait_for_selector("#paper .item")
        sw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        fs = pg.evaluate("parseFloat(getComputedStyle(document.body).fontSize)")
        pg.screenshot(path="%s/student_%d.png" % (out, w), full_page=True)
        # fill about half: choice 0, numeric 12, selects 1
        pg.evaluate("""() => { const m = MockApp.getMock(), a = {}; let i = 0;
          m.questions.forEach(Q => Q.items.forEach(it => { i++;
            if (it.type==='choice') a[it.uid] = (i%3===0)? it.correct : (it.correct+1)%5;
            else if (it.type==='numeric') a[it.uid] = (i%2===0)? String(it.key) : '12';
            else a[it.uid] = it.correct.map((c,j)=> (j%2===0)? (it.type==='ordering'? c : c) : null); }));
          MockApp.apply(a); }""")
        pg.click("#btn-check")
        pg.screenshot(path="%s/checked_%d.png" % (out, w), full_page=True)
        pg.close(); pg = br.new_context(viewport={"width": w, "height": h}).new_page()
        pg.goto("file://" + html + "#k=2&seed=1074"); pg.wait_for_selector("#paper .item")
        pg.emulate_media(media="print")
        pg.screenshot(path="%s/print_%d.png" % (out, w), full_page=True)
        print(w, "scrollWidth/clientWidth", sw, "body font px", fs)
        pg.close()
    br.close()
