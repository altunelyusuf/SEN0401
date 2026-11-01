#!/usr/bin/env python3
"""chapter_code_make v1_1_0 (SEN0401 chapter 2 page, task TK_Ch02_PageCode_Build). Writes, as a NEW file, 03-materials/ch02/page/chapter_code_ch02_v1_1_0.json: the chapter-code manifest of the deck v3.2.0.
The code of each example is the code of its slide, read from the deck file (sen0401_chbuild_v1_4_0.py codeslides: the shapes named "code", joined by newlines, in slide order), it equals the code of the same
example in chapter_code_ch02_v1_0_0.json (the listings are the old ones except where the deck 3.2.0 rewrote a lambda as def: for those the code differs from the old manifest by intent and the show values must still print the old expected values). Name, branch, library, needs and show come from that file; "slide" is the slide number in the deck v3.2.0.
Every example is run under the interpreter given (setup + listing, the library imported as the page does) and each 'show' expression must print the expected value of the old manifest.
Usage: chapter_code_make_v1_1_0.py <python3.14>"""
__version__ = "1.1.0"
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); REPO = os.path.dirname(T)
PY = sys.argv[1]; DECK = "SEN0401_Ch02_HowBitcoinWorks_3e_v3_2_0.pptx"
old = json.load(open(os.path.join(REPO, "03-materials", "ch02", "page", "chapter_code_ch02_v1_0_0.json")))
cs = subprocess.run([sys.executable, os.path.join(T, "sen0401_chbuild_v1_4_0.py"), "codeslides", "02", os.path.join(REPO, "03-materials", "ch02", DECK), "--out", "/tmp/i52_cs_make2.json"], capture_output=True, text=True)
if cs.returncode: raise SystemExit("codeslides failed: " + cs.stdout + cs.stderr)
ex = json.load(open("/tmp/i52_cs_make2.json"))["examples"]; os.remove("/tmp/i52_cs_make2.json")
if len(ex) != len(old["examples"]): raise SystemExit("the deck has %d code slides, the old manifest %d" % (len(ex), len(old["examples"])))
RUN = "import sys, json\nsys.path.insert(0, %r)\ng = {}\nexec(sys.argv[1], g)\nexec(sys.argv[2], g)\nprint(json.dumps([repr(eval(e, g)) for e in json.loads(sys.argv[3])]))"
out = []; bad = 0
for e, o in zip(ex, old["examples"]):
    if e["code"] != o["code"]: print("NOTE %s: the deck code differs from the old manifest code (lambda rewritten as def in the deck)" % o["id"])
    r = subprocess.run([PY, "-c", RUN % T, old["setup"]["code"], e["code"], json.dumps([s["expression"] for s in o["show"]])], capture_output=True, text=True, timeout=300, cwd="/tmp")
    if r.returncode: raise SystemExit("listing failed:\n%s\n%s" % (e["code"], r.stderr[-600:]))
    got = json.loads(r.stdout); want = [s["expected"] for s in o["show"]]
    ok = got == want; bad += not ok
    print("slide %2d  %-5s %-52s show values equal the old manifest: %s" % (e["slide"], o["id"], o["name"][:52], "yes" if ok else "NO %r vs %r" % (got, want)))
    d = dict(o); d["code"] = e["code"]; d["order"] = e["order"]; d["slide"] = e["slide"]; out.append(d)
if bad: raise SystemExit("%d example(s) print other values than the manifest expects" % bad)
man = dict(old); man["manifest"] = "chapter_code_ch02_v1_1_0"; man["deck"] = DECK; man["deck_version"] = "3.2.0"; man["examples"] = out
f = os.path.join(REPO, "03-materials", "ch02", "page", "chapter_code_ch02_v1_1_0.json")
if os.path.exists(f): raise SystemExit("refusing to overwrite " + f)
json.dump(man, open(f, "w"), indent=1, ensure_ascii=False)
print("wrote", os.path.relpath(f, REPO), len(out), "examples")
