#!/usr/bin/env python3
"""Version 2 of a SEN0401 chapter page: the template filled with the chapter's page data.
The owner's requirements of 2026-09-24 (explorer tree, sub-tabs, Pyodide editing and running, per-subject
agents, context menu, tooltips, code diagrams, taxonomy, concept map, right-hand concept card, jumps)
live in the template; this script only injects data. Usage: sen0401_page_build_v2_0_0.py <NN>"""
import json, os, sys
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(REPO, "08-tooling", "sen0401_page_template_v2_0_0.html")).read()
P = os.path.join(REPO, "08-tooling", "ch%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v2.json")))
safe = lambda o: json.dumps(o).replace("</", "<\\/")
h = (T.replace("__TITLE__", d["title"]).replace("__CH__", str(d["chapter"])).replace("__PY__", d["python"])
      .replace("__DATA__", safe(d)).replace("__QUIZ__", safe(json.load(open(os.path.join(P, "quiz.json")))))
      .replace("__OBJ__", safe(json.load(open(os.path.join(P, "objectives.json"))))))
out = os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0401_ch%s_page_v2_0_0.html" % N)
open(out, "w").write(h); print("written", out, len(h), "bytes")
