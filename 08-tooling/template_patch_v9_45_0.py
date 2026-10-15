#!/usr/bin/env python3
"""template_patch v9_45_0 - writes course_page_template_v9_45_0.html from SEN0401's course_page_template_v9_44_0.html. Five changes, each transplanted from SEN0414's templates 9.43.0 and 9.44.0 or new,
and nothing else (the SEN0414 templates 9.45.0 to 9.50.0 are NOT ported: they concern the Chapter examples pane, pictures in paragraphs and the exercise tokens of examples held in one expression, none of which chapter 8's page uses):
 1. a chapter may ship pure-Python wheels (data.py_wheels: name and hex), unpacked into the Python worker's site-packages at boot, may name Pyodide packages (data.py_packages) and a snippet run once after
    the wheels (data.py_boot)   [SEN0414 9.43.0 and 9.44.0, same code];
 2. a concept example may carry a note (n.io.note) shown above the code   [SEN0414 9.44.0];
 3. a chapter may carry a notice (data.notice) shown at the top of its Overview   [SEN0414 9.44.0];
 5. NEW: the breadcrumb row is compact (smaller gaps, the section name and the part select cut with an ellipsis when long, the full name in a tooltip), so that a chapter whose section names are long (chapter 8's)
    still shows a focused concept's first paragraph near the top instead of spending a second row on "Show all";
 4. NEW: a lecture slide may carry labels (s.labels: [{kind, text}], kind Recorded, NOT EXECUTED or Stand-in picture), shown as marked lines under the slide's text, so that the page reproduces the deck's honesty labels.
Refuses when a text to replace is not found exactly once."""
__version__ = "1.0.0"
import os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, "course_page_template_v9_44_0.html"), encoding="utf-8").read()
def rep(o, n):
    global s
    if s.count(o) != 1: raise SystemExit("REFUSED: %d occurrences of %r" % (s.count(o), o[:80]))
    s = s.replace(o, n)
rep("<!-- course_page_template version 9.44.0:", "<!-- course_page_template version 9.45.0: (SEN0401) a chapter may ship pure-Python wheels (data.py_wheels), Pyodide packages (data.py_packages) and a boot snippet (data.py_boot) for the Python worker, a concept example may carry a note (n.io.note), a chapter may carry a notice (data.notice) at the top of its Overview, and a lecture slide may carry labels (s.labels: Recorded, NOT EXECUTED, Stand-in picture) that the Lecture tab shows under the slide's text; otherwise identical to 9.44.0. Earlier: --><!-- course_page_template version 9.44.0:")
rep("const PY_TIMEOUT_MS=15000, PYODIDE_BASE=", "const PYWHEELS=(D.py_wheels||[]);\nconst PY_TIMEOUT_MS=15000, PYODIDE_BASE=")
rep("try{await py.loadPackage('sqlite3')}catch(e){}\n",
    "try{await py.loadPackage('sqlite3')}catch(e){}\n for(const k of ${JSON.stringify(D.py_packages||[])}){try{await py.loadPackage(k)}catch(e){}}\n"
    " const WHEELS=${JSON.stringify(PYWHEELS)};const SITE=py.runPython(\"import sysconfig;sysconfig.get_path('purelib')\");for(const w of WHEELS){const n=w.hex.length/2,u=new Uint8Array(n);for(let i=0;i<n;i++)u[i]=parseInt(w.hex.substr(2*i,2),16);py.unpackArchive(u,'wheel',{extractDir:SITE})}\n"
    " if(WHEELS.length)py.runPython('import importlib;importlib.invalidate_caches()')\n const BOOTPY=${JSON.stringify(D.py_boot||'')};if(BOOTPY)py.runPython(BOOTPY)\n")
rep("""if(n.io){return '<div class="widget" id="'+w+'"><div class="wl">Edit, predict, run</div>""", """if(n.io){return '<div class="widget" id="'+w+'"><div class="wl">Edit, predict, run</div>'+(n.io.note?'<p class="note" data-standin="1"><b>'+esc(n.io.note)+'</b></p>':'')+'""")
rep("""let P='<div role="tabpanel" data-pane="intro"><h2>'+esc(D.title)+'</h2><p>'""", """let P='<div role="tabpanel" data-pane="intro"><h2>'+esc(D.title)+'</h2>'+(D.notice?'<p class="note" data-notice="1"><b>'+esc(D.notice)+'</b></p>':'')+'<p>'""")
rep("""<p>'+esc(s.say)+'</p>'+(s.concept&&byId[s.concept]""", """<p>'+esc(s.say)+'</p>'+(s.labels&&s.labels.length?s.labels.map(l=>'<p class="note" data-lecture-label="'+esc(l.kind)+'"><b>'+esc(l.kind)+'.</b> '+esc(l.text)+'</p>').join(''):'')+(s.concept&&byId[s.concept]""")
rep(".leafpick button[aria-current=true]{", ".crumbs{gap:.25rem;padding:.25rem .5rem;margin:.05rem 0 .3rem}.crumbs .cb{max-width:11rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.crumbs .cbsel{max-width:11rem;text-overflow:ellipsis}.leafpick{gap:.25rem;margin:0 .2rem}\n.leafpick button[aria-current=true]{")
rep("""let h='<span class="cb">'+ICON[1]+' '+esc(byId[p].label)+'</span>""", """let h='<span class="cb" title="'+esc(byId[p].label)+'">'+ICON[1]+' '+esc(byId[p].label)+'</span>""")
open(os.path.join(H, "course_page_template_v9_45_0.html"), "w", encoding="utf-8").write(s)
print("wrote course_page_template_v9_45_0.html", len(s))
