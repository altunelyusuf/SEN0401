#!/usr/bin/env python3
"""deck_rerun v2.3.0 (a NEW tool file): re-runs every example of the chapter 6 deck v2.3.0 and compares with the result shown. For each 'code N' shape the listing is read from the deck, run in ONE FRESH namespace
after the chapter prelude (the setup of the chapter code manifest, with the library import), and each 'result N' row 'expression  ->  value' is evaluated in that namespace and compared with the value shown (repr).
Also prints per example: lines, longest line, lambda, prompt, indentation. Usage: python3.14 deck_rerun_v2_3_0.py DECK.pptx"""
import json, os, re, sys, ast, subprocess
PY = "/root/.local/bin/python3.14"
RUNNER = "import sys, json; j = json.load(sys.stdin); sys.path.insert(0, j[\"tool\"]); g = {}; exec(j[\"prelude\"], g); exec(j[\"src\"], g); print(json.dumps([repr(eval(e, g)) for e in j[\"exprs\"]]))"
sys.dont_write_bytecode = True
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from pptx import Presentation
man = json.load(open(os.path.join(ROOT, "03-materials/ch06/page/chapter_code_ch06_v1_1_0.json")))
prelude = "from sen0401_ch06_tx_lib_v1_0_0 import *\n" + man["setup"]["code"]
pr = Presentation(sys.argv[1]); bad = 0; n_ex = 0; n_rows = 0
for i, s in enumerate(pr.slides, 1):
    code = res = None
    frames = sorted([sh for sh in s.shapes if re.fullmatch(r"code \d+", sh.name)], key=lambda sh: sh.top)
    rrows = sorted([sh for sh in s.shapes if re.fullmatch(r"result \d+", sh.name) and sh.has_text_frame and "  →  " in sh.text_frame.text], key=lambda sh: sh.top)
    if not frames: continue
    N = int(frames[0].name.split()[1]); n_ex += 1
    lines = ["".join(r.text for r in p.runs) for fr in frames for p in fr.text_frame.paragraphs]
    src = "\n".join(lines)
    ast.parse(src)
    paras = [sh.text_frame.text for sh in rrows]
    ok = True
    exprs = [row.split("  →  ", 1)[0] for row in paras]
    job = json.dumps({"tool": os.path.join(ROOT, "08-tooling"), "prelude": prelude, "src": src, "exprs": exprs})
    out = subprocess.run([PY, "-I", "-c", RUNNER], input=job, capture_output=True, text=True, cwd=os.path.join(ROOT, "08-tooling"))
    if out.returncode: print(out.stderr[-600:]); ok = False; gots = []
    else: gots = json.loads(out.stdout)
    for row, got in zip(paras, gots):
        expr, val = row.split("  →  ", 1); n_rows += 1
        if got != val: ok = False; print("  MISMATCH ex%02d slide %d: %s shown %r got %r" % (N, i, expr, val, got))
    flags = []
    if "lambda" in src: flags.append("LAMBDA")
    if any(l.lstrip().startswith((">>>", "...")) for l in lines): flags.append("PROMPT")
    print("ex%02d slide %2d: lines %2d longest %2d result rows %d -> %s %s" % (N, i, len(lines), max(map(len, lines)), len(paras), "PASS" if ok and not flags else "FAIL", " ".join(flags)))
    bad += (not ok) or bool(flags)
print("EXAMPLES %d, RESULT ROWS COMPARED %d, FAILING %d -> %s" % (n_ex, n_rows, bad, "PASS" if bad == 0 and n_ex == 18 else "FAIL"))
sys.exit(1 if bad or n_ex != 18 else 0)
