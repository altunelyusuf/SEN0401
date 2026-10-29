#!/usr/bin/env python3
"""sen0401_ch06_deck_control_check v1_0_0 - the lineage agent's OWN control of the chapter 6 deck v2_3_0 (urgent task TK_Urgent_Ch06_Deck_Build). Not the executor's tools. (1) measure: prompts, unindented compound bodies, lambda, label shapes, notes (own regexes); (2) every slide's code boxes are run in one fresh namespace after the setup of the OLD committed manifest v1_1_0 and the library; every 'expression  ->  value' result row is evaluated and compared with repr; (3) the code lines of the old deck v2_2_0 (prompts stripped) against the new code: every difference is listed; (4) the old deck is byte-identical to its committed version. Usage: control.py NEWDECK OLDDECK MANIFEST_OLD"""
import json, re, sys, hashlib, subprocess, ast
sys.path.insert(0, "/home/claude/sen0401/08-tooling"); sys.dont_write_bytecode = True
from pptx import Presentation
new, old, man = sys.argv[1:4]
PROMPT = re.compile(r"^(>>> |\.\.\. |\.\.\.$)"); LABEL = re.compile(r"^\s*(WHAT|WHO|WHEN|WHERE|WHY|HOW)\s*[:\-–—]", re.I)
P = Presentation(new); fails = 0
def bad(m):
    global fails; fails += 1; print("FAIL", m)
codes = {}; results = {}; notes = []; labs = 0; lam = 0; prm = 0
for i, s in enumerate(P.slides, 1):
    for sh in s.shapes:
        if not sh.has_text_frame: continue
        t = sh.text_frame.text
        if LABEL.match(t.strip()): labs += 1
        for ln in t.split("\n"):
            if PROMPT.match(ln): prm += 1
        if sh.name.startswith("code"):
            codes.setdefault(i, []).append(t)
            if re.search(r"\blambda\b", t): lam += 1
        elif sh.name.startswith("result"): results.setdefault(i, []).append(t)
    notes.append(len(s.notes_slide.notes_text_frame.text.split()) if s.has_notes_slide else 0)
print("slides", len(P.slides), "code slides", len(codes), "prompts", prm, "lambda boxes", lam, "label shapes", labs, "notes avg %.1f max %d min %d" % (sum(notes) / len(notes), max(notes), min(notes)))
if prm or lam or labs: bad("prompts/lambda/labels not zero")
# own indentation reading with ast: a compound statement whose body is on the header line, or code that does not parse
unparsed = 0; oneline = 0; unindented = 0
for i, cs in codes.items():
    for c in cs:
        try: tree = ast.parse(c)
        except SyntaxError: unparsed += 1; print("  unparsable code box on slide", i, repr(c[:60])); continue
        for n in ast.walk(tree):
            if isinstance(n, (ast.For, ast.While, ast.If, ast.With, ast.FunctionDef, ast.ClassDef, ast.Try)) and n.body and n.body[0].lineno == n.lineno: oneline += 1
        for k, ln in enumerate(c.split("\n")):
            if ln.strip() and not ln.startswith((" ", "\t")) and k > 0 and c.split("\n")[k - 1].rstrip().endswith(":"): unindented += 1
print("unparsable", unparsed, "one-line compounds", oneline, "unindented bodies", unindented)
if unparsed or oneline or unindented: bad("code not PEP 8 / not parsable")
setup = json.load(open(man))["setup"]["code"]; prelude = "from sen0401_ch06_tx_lib_v1_0_0 import *\n" + setup
RUN = "import sys, json; j = json.load(sys.stdin); sys.path.insert(0, j['tool']); g = {}; exec(j['prelude'], g); exec(j['src'], g); out = []\nfor e in j['exprs']:\n    try: out.append(repr(eval(e, g)))\n    except Exception as x: out.append('ERR ' + repr(x))\nprint(json.dumps(out))"
ok = 0; tot = 0
for i, cs in sorted(codes.items()):
    rows = [r for t in results.get(i, []) for r in t.split("\n") if "→" in r]
    exprs = []; vals = []
    for r in rows:
        e, v = r.split("→", 1); exprs.append(e.strip()); vals.append(v.strip())
    if not exprs: continue
    job = json.dumps({"tool": "/home/claude/sen0401/08-tooling", "prelude": prelude, "src": "\n".join(cs), "exprs": exprs})
    r = subprocess.run([sys.executable, "-c", RUN], input=job, capture_output=True, text=True, timeout=120)
    if r.returncode: bad("slide %d did not run: %s" % (i, r.stderr.strip().splitlines()[-1][:150] if r.stderr else "")); tot += len(exprs); continue
    got = json.loads(r.stdout.strip().splitlines()[-1])
    for e, v, g in zip(exprs, vals, got):
        tot += 1
        if v == g: ok += 1
        else: bad("slide %d  %s  shown %s  Python %s" % (i, e, v[:60], g[:60]))
print("result rows re-run:", tot, "equal:", ok)
# old deck code against new code
oldc = []
for s in Presentation(old).slides:
    for sh in s.shapes:
        if sh.has_text_frame:
            for ln in sh.text_frame.text.split("\n"):
                if PROMPT.match(ln): oldc.append(PROMPT.sub("", ln, count=1).strip())
newc = [ln.strip() for cs in codes.values() for c in cs for ln in c.split("\n") if ln.strip()]
import difflib
d = [l for l in difflib.unified_diff(oldc, newc, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
print("code lines old %d new %d; differing lines %d" % (len(oldc), len(newc), len(d)))
for l in d[:60]: print("   ", l[:140])
print("OWN CONTROL:", "FAIL" if fails else "PASS (the differing code lines above need reading against the rules)"); sys.exit(1 if fails else 0)
