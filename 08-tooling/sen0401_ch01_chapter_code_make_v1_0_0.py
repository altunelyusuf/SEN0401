#!/usr/bin/env python3
"""sen0401_ch01_chapter_code_make v1.0.0 - writes, as a NEW file, 03-materials/ch01/page/chapter_code_ch01_v1_2_0.json: the chapter-code manifest of the deck 3.6.0 and the library 1.1.0.
The code of each example is the code of its slide, read from the deck file (sen0401_chbuild_v1_4_0.py codeslides), and must equal the code of the same example in chapter_code_ch01_v1_1_0.json.
Every example is run under the interpreter given (setup + listing, the library imported as the page does) and each 'show' expression must print the expected value of the old manifest.
Usage: sen0401_ch01_chapter_code_make_v1_0_0.py <python3.14>"""
__version__ = "1.0.0"
import hashlib, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H)
PY = sys.argv[1]; DECK = "SEN0401_Ch01_Introduction_3e_v3_6_0.pptx"; WH = "sen0401_ch01_lib-1.1.0-py3-none-any.whl"
old = json.load(open(os.path.join(REPO, "03-materials", "ch01", "page", "chapter_code_ch01_v1_1_0.json")))
cs = subprocess.run([sys.executable, os.path.join(H, "sen0401_chbuild_v1_4_0.py"), "codeslides", "01", os.path.join(REPO, "03-materials", "ch01", DECK), "--out", "/tmp/c1_cs_make.json"], capture_output=True, text=True)
if cs.returncode: raise SystemExit("codeslides failed: " + cs.stdout + cs.stderr)
ex = json.load(open("/tmp/c1_cs_make.json"))["examples"]; os.remove("/tmp/c1_cs_make.json")
if len(ex) != len(old["examples"]): raise SystemExit("the deck has %d code slides, the old manifest %d" % (len(ex), len(old["examples"])))
SETUP = ("# setup: the chapter library of the page (helper functions, the saved block-0 script and the documented prices); the page runs this before every example\n"
         "import hashlib\nfrom decimal import Decimal\nfrom sen0401_ch01_lib_v1_1_0 import *")
RUN = "import sys, json\nsys.path.insert(0, %r)\ng = {}\nexec(sys.argv[1], g)\nexec(sys.argv[2], g)\nprint(json.dumps([repr(eval(e, g)) for e in json.loads(sys.argv[3])]))"
out = []; bad = 0
for e, o in zip(ex, old["examples"]):
    if e["code"] != o["code"]: raise SystemExit("example %s: the deck code differs from the old manifest code" % o["id"])
    r = subprocess.run([PY, "-c", RUN % H, SETUP, e["code"], json.dumps([s["expression"] for s in o["show"]])], capture_output=True, text=True, timeout=300, cwd="/tmp")
    if r.returncode: raise SystemExit("listing failed:\n%s\n%s" % (e["code"], r.stderr[-600:]))
    got = json.loads(r.stdout); want = [s["expected"] for s in o["show"]]
    ok = got == want; bad += not ok
    print("slide %2d  %-5s %-52s show values equal the old manifest: %s" % (e["slide"], o["id"], o["name"][:52], "yes" if ok else "NO %r vs %r" % (got, want)))
    d = dict(o); d["order"] = e["order"]; d["slide"] = e["slide"]; d["library"] = "sen0401_ch01_lib_v1_1_0"; out.append(d)
if bad: raise SystemExit("%d example(s) print other values than the manifest expects" % bad)
wsha = hashlib.sha256(open(os.path.join(REPO, "03-materials", "ch01", "assets", WH), "rb").read()).hexdigest()
man = dict(old); man["manifest"] = "chapter_code_ch01_v1_2_0"; man["deck"] = DECK; man["deck_version"] = "3.6.0"
man["library"] = {"module": "sen0401_ch01_lib", "file": "03-materials/ch01/assets/" + WH, "sha256": wsha, "modules": ["sen0401_ch01_lib_v1_1_0"], "import": "from sen0401_ch01_lib_v1_1_0 import *"}
man["setup"] = dict(old["setup"]); man["setup"]["code"] = SETUP
man["examples"] = out
f = os.path.join(REPO, "03-materials", "ch01", "page", "chapter_code_ch01_v1_2_0.json")
if os.path.exists(f): raise SystemExit("refusing to overwrite " + f)
json.dump(man, open(f, "w"), indent=1, ensure_ascii=False)
print("wrote", os.path.relpath(f, REPO), len(out), "examples")
