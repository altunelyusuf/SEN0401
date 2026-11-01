#!/usr/bin/env python3
"""chapter_code_make v1_2_0 (SEN0401 chapter 5 page, task TK_Ch05_PageCode_Build). Writes, as a NEW file, 03-materials/ch05/page/chapter_code_ch05_v1_2_0.json: the chapter-code manifest of the deck v3.7.0.
The code of an example is the code of its slide, read from the deck file (sen0401_chbuild_v1_4_0.py codeslides: the shapes named "code", joined by newlines, in slide order), unchanged; no probe, no lambda
wrapper, no sha256_hex helper. Name, concepts, id and library entry come from chapter_code_ch05_v1_1_0.json (the same 27 slides); the prelude is that file's without its sha256_hex line (the deck code
uses hashlib directly). The expected result is what the listing prints, run under the interpreter given (Python 3.14.6) in a fresh namespace made of the chapter library (import *) and the manifest's own
prelude only, which is what the page defines before an example; each listing is also run in the deck check's namespace (examples_v1_2_0.PRELUDE) and the two outputs must be equal.
Usage: chapter_code_make_v1_2_0.py <python3.14>"""
__version__ = "1.2.0"
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); REPO = os.path.dirname(T)
PY = sys.argv[1]; DECK = "SEN0401_Ch05_WalletRecovery_3e_v3_7_0.pptx"
old = json.load(open(os.path.join(REPO, "03-materials", "ch05", "page", "chapter_code_ch05_v1_1_0.json")))
cs = subprocess.run([sys.executable, os.path.join(T, "sen0401_chbuild_v1_4_0.py"), "codeslides", "05", os.path.join(REPO, "03-materials", "ch05", DECK), "--out", "/tmp/i5_cs_make.json"], capture_output=True, text=True)
if cs.returncode: raise SystemExit("codeslides failed: " + cs.stdout + cs.stderr)
ex = json.load(open("/tmp/i5_cs_make.json"))["examples"]; os.remove("/tmp/i5_cs_make.json")
byslide = {e["slide"]: e for e in old["examples"]}
if sorted(byslide) != [e["slide"] for e in ex]: raise SystemExit("the code slides of the deck differ from those of the old manifest: %s vs %s" % ([e["slide"] for e in ex], sorted(byslide)))
prelude = "\n".join(l for l in old["prelude"].split("\n") if "sha256_hex" not in l) + ("\n" if old["prelude"].endswith("\n") else "")
LIB = old["executed_with"]["library"]
sys.path.insert(0, os.path.join(T, "ch05-deck")); import examples_v1_2_0 as E12
RUN = "import sys, io, contextlib, json\nsrc, pre, full = sys.argv[1], sys.argv[2], sys.argv[3] == '1'\nsys.path.insert(0, %r)\ng = {}\nexec(full and pre or 'from %s import *\\n' + pre, g)\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf): exec(src, g)\nsys.stdout.write(buf.getvalue())"
def run(code, pre, full):
    r = subprocess.run([PY, "-c", RUN % (T, LIB), code, pre, "1" if full else "0"], capture_output=True, text=True, timeout=300, cwd="/tmp")
    if r.returncode: raise SystemExit("listing failed:\n%s\n%s" % (code, r.stderr[-600:]))
    return r.stdout
out = []
for e in ex:
    o = byslide[e["slide"]]; code = e["code"]
    if "lambda" in code or "__import__" in code or "sha256_hex" in code or ">>>" in code: raise SystemExit("slide %d: lambda, probe, helper or prompt in the code" % e["slide"])
    a = run(code, prelude, False); b = run(code, E12.PRELUDE, True)
    if a != b: raise SystemExit("slide %d: the page namespace and the deck check namespace print differently:\n%r\n%r" % (e["slide"], a, b))
    d = {"order": e["order"], "id": o["id"], "name": o["name"], "slide": e["slide"], "concepts": o["concepts"], "code": code, "expected": a}
    out.append(d)
    print("slide %2d  %-22s same output as the old manifest: %s" % (e["slide"], o["id"], "yes" if a == o["expected"] else "no (code changed on this slide)"))
man = {"chapter": 5, "version": "1.2.0", "kind": "chapter-code manifest", "deck": "03-materials/ch05/" + DECK,
       "about": "The code examples of the chapter 5 deck v3.7.0, in the order of the code slides (order = slide order): the code of an example is the code of its slide, unchanged (no prompt, no probe line, no lambda, no sha256_hex helper). The page's chapter-code tab lists them by NAME in this order; the code runs in the page with the chapter library and the prelude defined first; the expected result is what the run printed.",
       "executed_with": old["executed_with"], "library": old["library"], "prelude": prelude, "examples": out}
f = os.path.join(REPO, "03-materials", "ch05", "page", "chapter_code_ch05_v1_2_0.json")
if os.path.exists(f): raise SystemExit("refusing to overwrite " + f)
json.dump(man, open(f, "w"), indent=1, ensure_ascii=False)
print("wrote", os.path.relpath(f, REPO), len(out), "examples")
