#!/usr/bin/env python3
"""Version 3 of a SEN0401 page (a chapter, or a named unit such as "numbers"): the course-neutral template
course_page_template_v3_0_0.html - byte-identical to SEN0414's - filled with the unit's page data and
course_page_config.json, plus the unit's extras (the numbers page's charts) when it has them.
Usage: sen0401_page_build_v3_0_0.py <NN|unit>"""
import json, os, sys
N = sys.argv[1]; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(REPO, "08-tooling", "course_page_template_v3_0_0.html")).read()
P = os.path.join(REPO, "08-tooling", "%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v2.json")))
safe = lambda o: json.dumps(o).replace("</", "<\\/")
sub = d["unit"]["sub"] if d.get("unit") else d["course"]["chapter_sub"].replace("{n}", str(d["chapter"]))
h = (T.replace("__TITLE__", d["title"]).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", sub)
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(json.load(open(os.path.join(P, "quiz.json")))))
      .replace("__OBJ__", safe(json.load(open(os.path.join(P, "objectives.json"))))))
X = os.path.join(P, "extra_resolved.html")
h = h.replace("</body></html>", (open(X).read() if os.path.exists(X) else "") + "</body></html>")
out = os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v3_0_0.html" % N)
open(out, "w").write(h); print("written", out, len(h), "bytes")
