#!/usr/bin/env python3
"""Build index.html for a folder of chapter pages, in the same look as the pages (navy header, yellow pills, cards, text-size control, light theme).
usage: sen0401_index_build_v1_0_0.py FOLDER   (FOLDER holds sen0414_chNN_page_vX_Y_Z.html files and optionally the exam desk)"""
import sys, os, re, glob, json, html
__version__ = "1.0.0"
folder = sys.argv[1]
pages = {}
for f in glob.glob(os.path.join(folder, "sen0401_ch*_page_v*.html")):
    m = re.match(r"sen0401_ch(\d\d)_page_v(\d+)_(\d+)_(\d+)\.html$", os.path.basename(f))
    if m:
        k = int(m.group(1)); v = tuple(int(x) for x in m.groups()[1:])
        if k not in pages or v > pages[k][0]: pages[k] = (v, os.path.basename(f))
cards = []
for k in range(1, 25):
    if k == 12:
        cards.append('<div class="ch off"><span class="n">12</span><b>Command-line programs</b><small>Not built: the course does not cover this chapter.</small></div>'); continue
    if k not in pages: continue
    fn = pages[k][1]; t = ""; nc = ne = 0
    txt = open(os.path.join(folder, fn), encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', txt, re.S)
    if m:
        d = json.loads(m.group(1)); t = d.get("title", ""); nc = len([n for n in d["nodes"] if n.get("level") == 3]); ne = len([n for n in d["nodes"] if n.get("io")])
    ver = ".".join(map(str, pages[k][0]))
    cards.append('<a class="ch" href="%s" data-t="%s"><span class="n">%02d</span><b>%s</b><small>%d concepts · %d executed examples · page %s</small></a>' % (fn, html.escape((t + " chapter " + str(k)).lower()), k, html.escape(t), nc, ne, ver))
desk = [f for f in os.listdir(folder) if f.startswith("sen0401_exam_desk_v") and f.endswith(".html")]
deskhtml = '<a class="ch desk" href="%s"><span class="n">🎓</span><b>Exam desk (instructor)</b><small>Open student result files (drop them in, or zips), see every answer and mark, make release codes, work out the bonus.</small></a>' % sorted(desk)[-1] if desk else ""
page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SEN0401 chapters</title>
<style>
:root{color-scheme:light;--ink:#1F2933;--mute:#5B6B7B;--navy:#1E2A3A;--blue:#306998;--yellow:#FFD43B;--card:#F1F4F8;--line:#D0D7DE;--bg:#FFFFFF;--panel:#FAFBFC;box-sizing:border-box}
*{box-sizing:inherit}html{font-size:100%}body{margin:0;font:1rem/1.55 Calibri,Arial,sans-serif;color:var(--ink);background:var(--bg)}
header.top{background:var(--navy);color:#fff;padding:.5rem 1rem;position:sticky;top:0;z-index:5}header.top h1{margin:0;font:600 1.1rem Cambria,Georgia,serif}header.top .sub{font-size:.8rem;color:#C9D4E0}
.titlebar{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}.titlebar h1{flex:1 1 12rem;min-width:0}
.fsctl{margin-left:auto;display:flex;gap:.25rem}.fsctl button{background:transparent;color:#fff;border:1px solid #ffffff66;border-radius:8px;min-width:2.4rem;min-height:2rem;font-weight:700;cursor:pointer;font-size:.9rem}
main{max-width:70rem;margin:0 auto;padding:.8rem 1rem 3rem}h2{font:600 1.35rem Cambria,Georgia,serif;color:var(--blue);margin:.6rem 0}
.note{color:var(--mute);font-size:.94rem}input[type=search]{font:inherit;border:1px solid var(--line);border-radius:8px;padding:.35rem .6rem;width:100%;max-width:22rem;min-height:2.2rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:.5rem;margin-top:.6rem}
.ch{display:flex;flex-direction:column;gap:.15rem;text-align:left;text-decoration:none;color:var(--ink);border:1px solid var(--line);background:var(--bg);border-radius:12px;padding:.6rem .8rem;position:relative}
a.ch:hover,a.ch:focus-visible{border-color:var(--blue);box-shadow:0 0 0 2px var(--yellow)}.ch .n{align-self:flex-start;background:var(--navy);color:#fff;border-radius:999px;min-width:1.9rem;padding:0 .5rem;text-align:center;font-weight:700;font-size:.9rem}
.ch b{font:600 1.05rem Cambria,Georgia,serif}.ch small{color:var(--mute);line-height:1.4}.ch.off{background:var(--card);opacity:.85}.ch.desk{border-color:var(--blue);background:var(--card)}
@media (max-width:700px){main{padding:.6rem .7rem 3rem}.grid{grid-template-columns:1fr}}
</style></head><body>
<header class="top"><div class="titlebar"><h1>SEN0401 Special Topics: Block Chain</h1><div class="fsctl" role="group" aria-label="Text size"><button id="fsDown" aria-label="Smaller text">A−</button><button id="fsReset" aria-label="Default text size"><span id="fsVal">100%</span></button><button id="fsUp" aria-label="Larger text">A+</button></div></div><div class="sub">Chapter pages for <i>Automate the Boring Stuff with Python</i>, 3rd edition · every example was run in Python 3.14.4 · each page opens on its own and links back here</div></header>
<main><h2>Chapters</h2><p class="note">Choose a chapter. Each page needs an internet connection to run Python and to search; it links back to this list.</p>
<p><input type="search" id="q" placeholder="Find a chapter…" aria-label="Find a chapter"></p><div class="grid" id="g">%CARDS%</div>
%DESK%<h2>Instructor</h2><div class="grid">%DESKCARD%</div></main>
<script>
(function(){var K='sen0414-index-fs',fs=100;try{fs=+localStorage.getItem('course-page-fs')||+localStorage.getItem(K)||100}catch(e){}
function set(v){fs=Math.max(80,Math.min(180,v));document.documentElement.style.fontSize=fs+'%';document.getElementById('fsVal').textContent=fs+'%';try{localStorage.setItem(K,fs)}catch(e){}}
set(fs);document.getElementById('fsDown').onclick=function(){set(fs-10)};document.getElementById('fsUp').onclick=function(){set(fs+10)};document.getElementById('fsReset').onclick=function(){set(100)};
document.getElementById('q').addEventListener('input',function(e){var v=e.target.value.toLowerCase();document.querySelectorAll('#g .ch').forEach(function(c){c.style.display=(!v||(c.dataset.t||c.textContent.toLowerCase()).indexOf(v)>=0)?'':'none'})})})();
</script></body></html>"""
page = page.replace("%CARDS%", "\n".join(cards)).replace("%DESKCARD%", deskhtml).replace("%DESK%", "")
open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(page)
print("index.html:", len(pages), "chapter pages")
