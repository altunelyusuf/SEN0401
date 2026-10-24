#!/usr/bin/env python3
"""build_fixtures v1_0_0 - builds the three fixtures of criterion AC7R_PageTest937 from the page 9.85.0 of chapter 8 (not edited; copies are written here).
Each fixture keeps ONE chapter-code example. Usage: python3 -B build_fixtures_v1_0_0.py [OUTDIR]"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "03-materials", "ch08", "page", "sen0401_ch08_page_v9_85_0.html")
out = sys.argv[1] if len(sys.argv) > 1 else HERE
s = open(SRC, encoding="utf-8").read()
m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', s, re.S)
D = json.loads(m.group(2))
def make(code, patch=None):
    d = json.loads(json.dumps(D))
    d["chaptercode"]["examples"] = [{"order": 1, "name": "Fixture example", "code": code, "slide": 1}]
    t = s[:m.start(2)] + json.dumps(d, ensure_ascii=False) + s[m.end(2):]
    if patch:
        assert t.count(patch[0]) == 1, patch[0]; t = t.replace(patch[0], patch[1])
    return t
slow = "import time\nt = time.perf_counter()\nwhile time.perf_counter() - t < 1.5:\n    pass\n[3, 1, 4, 1, 5]"
fx = {
 "fixture_a_slow_visual_v1_0_0.html": make(slow),
 "fixture_b_text_only_v1_0_0.html": make("[3, 1, 4, 1, 5]", ("+(err?'':'<div class=\"diagram small ccviz\">'+ccSvg(p)+'</div>')", "+''")),
 "fixture_c_never_ends_v1_0_0.html": make("[3, 1, 4, 1, 5]", ("out=await runPy(ta.value,[])", "out=await new Promise(()=>{})")),
}
for k, v in fx.items():
    open(os.path.join(out, k), "w", encoding="utf-8").write(v); print(k, len(v))
