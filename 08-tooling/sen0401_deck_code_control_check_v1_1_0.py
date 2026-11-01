#!/usr/bin/env python3
"""sen0401_deck_code_control_check v1_1_0 (over v1_0_0: a monospaced shape of the OLD deck with no prompt line is a diagram label, not a code box; it must stay with the same text on the same slide in the new deck and is not counted as a code box; found on chapter 3, whose slides 14 and 24 carry four monospaced hash boxes) - the lineage agent's own control of a 'code-only deck' (chapter code without prompts, results in result shapes). Usage: deck_code_control_check NN OLD.pptx NEW.pptx [OLD_COMMIT_REF]. Prints PASS/FAIL lines, exit 1 on any FAIL. Checks: slide count; no prompt line in any code box; every old code line (prompt stripped) in the same slide's new code boxes in order; every old result row on the new slide; code shapes named 'code N' and result shapes 'result line N' (count of code boxes equals the old count); all other text and all notes unchanged; hyperlinks per slide unchanged; layout check clean; notes check PASS; the old deck equals its committed blob. Lambdas are reported as INFO (they are removed by the Teach step)."""
__version__ = "1.1.0"
import re, sys, subprocess, hashlib, os
from pptx import Presentation
nn, old, new = sys.argv[1:4]; ref = sys.argv[4] if len(sys.argv) > 4 else "HEAD"; fails = 0
def out(ok, msg):
    global fails; fails += (not ok); print(("PASS  " if ok else "FAIL  ") + msg)
isc = lambda sh: sh.has_text_frame and any(r.font.name and "Courier" in r.font.name for pa in sh.text_frame.paragraphs for r in pa.runs)
A = Presentation(old); B = Presentation(new)
out(len(A.slides) == len(B.slides), "slide count %d -> %d" % (len(A.slides), len(B.slides)))
try:
    blob = subprocess.run(["git", "show", "%s:%s" % (ref, os.path.relpath(old))], capture_output=True).stdout
    out(hashlib.sha256(blob).hexdigest() == hashlib.sha256(open(old, "rb").read()).hexdigest(), "old deck equals its committed blob at %s" % ref)
except Exception as e: out(False, "old deck blob: %s" % e)
strip = lambda l: re.sub(r"^(>>> |\.\.\. )", "", l)
pr = lam = nold = nnew = lines_missing = rows_missing = badnames = 0
for k, (a, b) in enumerate(zip(A.slides, B.slides), 1):
    dg = [sh for sh in a.shapes if isc(sh) and not any(l.startswith((">>> ", "... ")) for l in sh.text_frame.text.split("\n"))]; dgt = [sh.text_frame.text for sh in dg]; oc = [sh for sh in a.shapes if isc(sh) and sh not in dg]; nc = [sh for sh in b.shapes if isc(sh) and sh.name.startswith("code")]; rs = [sh for sh in b.shapes if sh.has_text_frame and sh.name.startswith("result line")]
    nold += len(oc); nnew += len(nc)
    for sh in b.shapes:
        if isc(sh) and sh.name.startswith("code"):
            t = sh.text_frame.text; pr += t.count(">>>") + t.count("\n... ") + (1 if t.startswith("...") else 0); lam += len(re.findall(r"\blambda\b", t))
        elif isc(sh) and not sh.name.startswith(("code", "result")) and sh.text_frame.text not in dgt: badnames += 1
    badnames += sum(1 for x in dgt if x not in [sh.text_frame.text for sh in b.shapes if sh.has_text_frame])
    oldl = [strip(l) for sh in oc for l in sh.text_frame.text.split("\n") if l.startswith((">>> ", "... "))]
    newl = [l for sh in nc for l in sh.text_frame.text.split("\n")]
    it = iter([x.rstrip() for x in newl])
    for l in oldl:
        if not any(l.rstrip() == x for x in it): lines_missing += 1
    oldr = [l for sh in oc for l in sh.text_frame.text.split("\n") if l.strip() and not l.startswith((">>> ", "... "))]
    allt = " ".join(sh.text_frame.text for sh in b.shapes if sh.has_text_frame)
    rows_missing += sum(1 for r in oldr if r.strip() not in allt)
out(pr == 0, "prompt lines in code boxes of the new deck: %d" % pr)
out(nold == nnew, "code boxes old %d, new %d (named 'code N')" % (nold, nnew))
out(badnames == 0, "monospaced shapes with a name that is neither code nor result: %d" % badnames)
out(lines_missing == 0, "old code lines (prompts stripped) not found in order in the new code boxes of their slide: %d" % lines_missing)
out(rows_missing == 0, "old result rows not found on the new slide: %d" % rows_missing)
lost = changed = 0
for a, b in zip(A.slides, B.slides):
    ta = [sh.text_frame.text for sh in a.shapes if sh.has_text_frame and not isc(sh)]; tb = " ".join(sh.text_frame.text for sh in b.shapes if sh.has_text_frame and not isc(sh))
    lost += sum(1 for x in ta if x not in tb)
    na = a.notes_slide.notes_text_frame.text if a.has_notes_slide else ""; nb = b.notes_slide.notes_text_frame.text if b.has_notes_slide else ""
    changed += (na != nb)
out(lost == 0, "non-code text shapes of the old deck missing on the new slide: %d" % lost)
out(changed == 0, "slides whose notes changed: %d" % changed)
hl = lambda P: [sorted(r.target_ref for r in s.part.rels.values() if r.is_external) for s in P.slides]
out(hl(A) == hl(B), "hyperlinks per slide identical (%d total)" % sum(len(x) for x in hl(B)))
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_layout_check_v1_0_0.py"), new], capture_output=True, text=True).stdout
out("RESULT: clean" in r, "layout check: " + [l.strip() for l in r.splitlines() if "RESULT" in l or "outside" in l][-1])
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_notes_check_v1_0_0.py"), new], capture_output=True, text=True).stdout
out("VERDICT: PASS" in r, "notes check: " + r.strip().splitlines()[-1].strip())
print("INFO  lambdas left in code boxes: %d (removed by the Teach step)" % lam)
print("RESULT", "FAIL" if fails else "PASS"); sys.exit(1 if fails else 0)
