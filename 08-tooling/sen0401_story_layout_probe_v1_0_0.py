#!/usr/bin/env python3
"""sen0401_story_layout_probe v1_0_0 - the owner's story-layout rule as a browser probe (ported from the sister course's probe of Iteration 19, same template family; a NEW tool, edits nothing).
RULE (the purpose: the reader sees the story's text without scrolling past a full-height photograph): for EVERY story of the Stories tab, at 1366x768, 1400x900 and 390x844,
(1) the tallest photograph of the story is shorter than the viewport, and (2) the story's narrative paragraph (the longest paragraph of 60 characters or more that holds no image) begins within the first screen:
its top is above the bottom edge of the viewport. The first story is measured as the reader sees it when the Stories tab is opened; every later story with its card scrolled to the top of the viewport.
Usage: sen0401_story_layout_probe_v1_0_0.py NN [PAGEVER] [LOGFILE]     (PAGEVER like 9_84_0; default the newest page of chapter NN; LOGFILE is written once and must not exist)
Run it ONLY under `flock /tmp/page_test.lock python3 ...` (browser tests run one at a time on the two cores). Exit 0 only when every story passes at every viewport. A page with no story card FAILS."""
__version__ = "1.0.0"
import glob, os, re, sys
T = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(T)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
def main():
    from playwright.sync_api import sync_playwright
    n = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].endswith(".log") else None; lf = sys.argv[-1] if sys.argv[-1].endswith(".log") else None
    pat = os.path.join(REPO, "03-materials/ch%s/page/sen0401_ch%s_page_v%s.html" % (n, n, pv or "*"))
    page = sorted(glob.glob(pat), key=vk)[-1]; out, bad, total = ["page %s" % os.path.relpath(page, REPO)], 0, 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for W, H in ((1366, 768), (1400, 900), (390, 844)):
            c = b.new_context(viewport={"width": W, "height": H}, is_mobile=W < 500, has_touch=W < 500); pg = c.new_page(); pg.goto("file://" + page); pg.wait_for_timeout(800)
            pg.evaluate("showTab('learn')"); pg.wait_for_timeout(200)
            pg.evaluate("showTab('stories')"); pg.wait_for_timeout(500); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(200)
            n_st = pg.locator('[data-pane="stories"] .story').count()
            for i in range(n_st):
                r = pg.evaluate("""i=>{const s=document.querySelectorAll('[data-pane=stories] .story')[i];if(i>0){s.scrollIntoView({block:'start'});window.scrollBy(0,-4);}
                 const imgs=[...s.querySelectorAll('img')].filter(x=>x.getBoundingClientRect().height>0);const ih=imgs.length?Math.max(...imgs.map(x=>x.getBoundingClientRect().height)):0;
                 const ps=[...s.querySelectorAll('p')].filter(e=>!e.querySelector('img')&&e.textContent.trim().length>60);ps.sort((x,y)=>y.textContent.length-x.textContent.length);const r0=ps.length?ps[0].getBoundingClientRect():null;
                 return {ih:ih,imgs:imgs.length,vh:innerHeight,textTop:r0?r0.top:-1}}""", i)
                good = r["textTop"] >= 0 and r["textTop"] <= r["vh"] and r["ih"] < r["vh"]; total += 1; bad += 0 if good else 1
                out.append("%s story %d at %dx%d: photo height %d of %d, narrative top %s, images %d" % ("PASS" if good else "FAIL", i + 1, W, H, r["ih"], r["vh"], r["textTop"], r["imgs"]))
            if n_st == 0: bad += 1; out.append("FAIL no story cards found at %dx%d" % (W, H))
            c.close()
        b.close()
    out.append("CHECKS %d, FAILED %d" % (total, bad)); out.append("RESULT: %s" % ("PASS" if not bad and total else "FAIL"))
    if lf:
        assert not os.path.exists(lf), "log exists: " + lf
        open(lf, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out)); sys.exit(1 if bad or not total else 0)
if __name__ == "__main__": main()
