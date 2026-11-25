#!/usr/bin/env python3
"""chapter_code_make v1_2_0 (SEN0401 chapter 4 page). Writes, as a NEW file, 03-materials/ch04/page/chapter_code_ch04_v1_2_0.json: the chapter-code manifest of the deck v3_8_0.
Over v1_1_0: the library is sen0401_ch04_lib 1.1.0 (Bitcoin Core pointers in the docstring, code unchanged), the deck gains the code box of slide 10 (def and its run line), which becomes example ex22 listed first
(order 1; the other orders move up by one; ids stay). The code of each example is the code of its slide, read from the deck (the shapes named code, joined by newlines, in slide order); every example is run under
the interpreter given (setup + listing, the library imported as the page does) and each 'show' expression must print the expected value.
Usage: chapter_code_make_v1_2_0.py <python3.14>"""
__version__ = "1.2.0"
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); REPO = os.path.dirname(T)
PY = sys.argv[1]; DECK = "SEN0401_Ch04_KeysAndAddresses_3e_v3_8_0.pptx"
old = json.load(open(os.path.join(REPO, "03-materials", "ch04", "page", "chapter_code_ch04_v1_1_0.json")))
cs = subprocess.run([sys.executable, os.path.join(T, "sen0401_chbuild_v1_4_0.py"), "codeslides", "04", os.path.join(REPO, "03-materials", "ch04", DECK), "--out", "/tmp/c4_cs_make.json"], capture_output=True, text=True)
if cs.returncode: raise SystemExit("codeslides failed: " + cs.stdout + cs.stderr)
ex = json.load(open("/tmp/c4_cs_make.json"))["examples"]; os.remove("/tmp/c4_cs_make.json")
new10 = {"id": "ex22", "name": "A lambda and the same helper with def", "slide": 10, "branch": "Public Key Cryptography", "library": "sen0401_ch04_lib", "needs": ["setup"],
         "code": "def ok(x):\n    return 0 < x < K.N\n[ok(x) for x in (0, 1, K.BOOK_K, K.N - 1, K.N)]",
         "show": [{"expression": "[ok(x) for x in (0, 1, K.BOOK_K, K.N - 1, K.N)]", "expected": "[False, True, True, True, False]"}], "result_picture": "table"}
recs = [new10] + old["examples"]
if len(ex) != len(recs): raise SystemExit("the deck has %d code slides, the manifest %d" % (len(ex), len(recs)))
setup = old["setup"]["code"].replace("sen0401_ch04_lib_v1_0_0", "sen0401_ch04_lib_v1_1_0")
RUN = "import sys, json\nsys.path.insert(0, %r)\ng = {}\nexec(sys.argv[1], g)\nexec(sys.argv[2], g)\nprint(json.dumps([repr(eval(e, g)) for e in json.loads(sys.argv[3])]))"
out = []; bad = 0
for e, o in zip(ex, recs):
    if e["slide"] != o["slide"]: raise SystemExit("slide order differs: deck %s manifest %s" % (e["slide"], o["slide"]))
    if e["code"] != o["code"]: raise SystemExit("deck code of slide %d differs from the manifest code" % e["slide"])
    r = subprocess.run([PY, "-c", RUN % T, setup, e["code"], json.dumps([s["expression"] for s in o["show"]])], capture_output=True, text=True, timeout=300, cwd="/tmp")
    if r.returncode: raise SystemExit("listing failed:\n%s\n%s" % (e["code"], r.stderr[-600:]))
    got = json.loads(r.stdout); want = [s["expected"] for s in o["show"]]
    ok = got == want; bad += not ok
    print("slide %2d  %-5s %-52s show values as expected: %s" % (e["slide"], o["id"], o["name"][:52], "yes" if ok else "NO %r vs %r" % (got, want)))
    d = dict(o); d["order"] = e["order"]; out.append(d)
if bad: raise SystemExit("%d example(s) print other values than expected" % bad)
man = dict(old); man["manifest"] = "chapter_code_ch04_v1_2_0"; man["deck"] = DECK; man["deck_version"] = "3.8.0"; man["examples"] = out
lib = dict(old["library"]); import hashlib
w = os.path.join(REPO, "03-materials", "ch04", "assets", "sen0401_ch04_lib-1.1.0-py3-none-any.whl"); s = os.path.join(T, "sen0401_ch04_lib_v1_1_0.py")
lib.update({"file": "03-materials/ch04/assets/sen0401_ch04_lib-1.1.0-py3-none-any.whl", "sha256": hashlib.sha256(open(w, "rb").read()).hexdigest(), "modules": ["sen0401_ch04_lib_v1_1_0"],
            "source": "08-tooling/sen0401_ch04_lib_v1_1_0.py", "source_sha256": hashlib.sha256(open(s, "rb").read()).hexdigest(), "import": "import sen0401_ch04_lib_v1_1_0 as K"})
man["library"] = lib; man["setup"] = dict(old["setup"], code=setup)
f = os.path.join(REPO, "03-materials", "ch04", "page", "chapter_code_ch04_v1_2_0.json")
if os.path.exists(f): raise SystemExit("refusing to overwrite " + f)
json.dump(man, open(f, "w"), indent=1, ensure_ascii=False)
print("wrote", os.path.relpath(f, REPO), len(out), "examples")
