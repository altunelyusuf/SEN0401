#!/usr/bin/env python3
"""deck_ex12_fix v1.0.0 (chapter 13) - task TK_Deck13_Ex12_Build: makes the NEW deck 2.2.0, the NEW plan 2.2.0 and the NEW chapter-code manifest 1.1.0 from deck/plan 2.1.0 and manifest 1.0.0 (all three stay unchanged).
ONE kind of change: example 12 (slide 24) cuts its two refusal messages with .removeprefix('Error: '), so the slide prints (1.0, 'Please enter the wallet') and, in the chapter code tab, 'The wallet passphrase entered was incorrect.'.
Changed on slide 24 only: the code frames (same number of lines per frame, none above 56 characters), the note of the first frame, the printed output line and the result sentence. Notes of the slide and every other slide stay as they are.
The listing comes from examples_v2_2_0.py and the expected values from examples_out_v2_2_0.json (examples_run_v2_2_0.py), nothing is typed twice. Usage: python3 -B deck_ex12_fix_v1_0_0.py"""
__version__ = "1.0.0"
import copy, json, os, re, shutil, subprocess, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); D = os.path.join(ROOT, "03-materials", "ch13")
sys.path.insert(0, HERE)
import examples_v2_2_0 as X
OUT = json.load(open(os.path.join(HERE, "examples_out_v2_2_0.json")))
OLD = os.path.join(D, "SEN0401_Ch13_BitcoinSecurity_3e_v2_1_0.pptx"); NEW = os.path.join(D, "SEN0401_Ch13_BitcoinSecurity_3e_v2_2_0.pptx")
MOLD = os.path.join(D, "page", "chapter_code_ch13_v1_0_0.json"); MNEW = os.path.join(D, "page", "chapter_code_ch13_v1_1_0.json")
PNEW = os.path.join(HERE, "deck_plan_v2_2_0.json")
for p in (NEW, MNEW, PNEW):
    if os.path.exists(p): sys.exit("REFUSED: %s exists" % p)
ex = [e for e in X.EXAMPLES if e["id"] == "ex12"][0]
groups = [g["lines"] for g in ex["groups"]]; notes = [g["note"] for g in ex["groups"]]
final_out = OUT["ex12"][0][1]
assert final_out == "(1.0, 'Please enter the wallet')" and OUT["ex12"][1][1] == "'The wallet passphrase entered was incorrect.'"
assert all(len(l) <= 56 for g in groups for l in g)
body = 'Sending is refused with: "Please enter the wallet". The wrong passphrase gives: "The wallet passphrase entered wa"'

# ---- plan 2.2.0
plan = json.load(open(os.path.join(HERE, "deck_plan_v2_1_0.json"))); sl = plan["slides"][23]
assert sl["title"] == "A locked wallet still shows the balance"
cb = [i for i in sl["items"] if i["t"] == "codeblocks"][0]
assert [len(g["rows"]) for g in cb["groups"]] == [len(g) for g in groups]
for g, lines, note in zip(cb["groups"], groups, notes):
    g["rows"] = [[l, ""] for l in lines]; g["note"] = note
cb["groups"][-1]["rows"][-1][1] = final_out
[i for i in sl["items"] if i["t"] == "text" and i["body"].startswith("Sending is refused")][0]["body"] = body
plan["meta"]["version"] = "2.2.0"; plan["meta"]["sub"] = "SEN0401, third-edition deck 2.2.0"
plan["meta"]["revision"] = "2026-10-27, task TK_Deck13_Ex12_Build: example 12 on slide 24 cuts its two refusal messages with removeprefix('Error: '); nothing else changed"
json.dump(plan, open(PNEW, "w"), ensure_ascii=False, indent=1)

# ---- deck 2.2.0 (copy of 2.1.0, slide 24 patched in place)
shutil.copy(OLD, NEW); pr = Presentation(NEW); s = pr.slides[23]
sh = {x.shape_id: x for x in s.shapes}
tok = re.compile(r"('[^']*'|\b\d+\b)")
def style(par):  # one template run per colour from a paragraph that has all four kinds
    d = {}
    for r in par.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r"):
        c = r.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr").get("val"); d.setdefault(c, r)
    return d
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
tpl = style(sh[9].text_frame.paragraphs[0]._p)
PROMPT, PLAIN, STR, NUM = [copy.deepcopy(tpl[c]) for c in ("D97A14", "E6EDF3", "9ECBFF", "FFD28A")]
def setpar(p, parts):  # parts: list of (template, text); replaces all runs, keeps pPr and endParaRPr
    for r in p.findall(A + "r"): p.remove(r)
    end = p.find(A + "endParaRPr")
    for t, text in parts:
        r = copy.deepcopy(t); r.find(A + "t").text = text
        end.addprevious(r) if end is not None else p.append(r)
def code_parts(line):
    parts = [(PROMPT, ">>> ")]; pos = 0
    for m in tok.finditer(line):
        if m.start() > pos: parts.append((PLAIN, line[pos:m.start()]))
        parts.append((STR if m.group(0).startswith("'") else NUM, m.group(0))); pos = m.end()
    if pos < len(line): parts.append((PLAIN, line[pos:]))
    return parts
for sid, lines in ((7, groups[0]), (9, groups[1]), (11, groups[2])):
    ps = sh[sid].text_frame.paragraphs
    assert len(ps) == len(lines) + (1 if sid == 11 else 0), (sid, len(ps))
    for p, l in zip(ps, lines): setpar(p._p, code_parts(l))
out_p = sh[11].text_frame.paragraphs[-1]._p; outrun = out_p.find(A + "r"); setpar(out_p, [(outrun, final_out)])
assert sh[14].text_frame.text.startswith("The recorded wallet"); sh[14].text_frame.paragraphs[0].runs[0].text = notes[0]
assert sh[24].text_frame.text.startswith("Sending is refused"); sh[24].text_frame.paragraphs[0].runs[0].text = body
pr.save(NEW)
subprocess.check_call(["python3", os.path.join(os.path.dirname(HERE), "office_stamp_v1_0_0.py"), NEW, "2.2.0", "SEN0401 Chapter 13"])

# ---- manifest 1.1.0 (only example 12 and the names of the files it points to)
m = json.load(open(MOLD))
m["manifest"] = "chapter_code_ch13_v1_1_0"; m["deck"] = "SEN0401_Ch13_BitcoinSecurity_3e_v2_2_0.pptx"; m["deck_version"] = "2.2.0"
e12 = [e for e in m["examples"] if e["id"] == "ex12"][0]
e12["code"] = "\n".join(l for g in groups for l in g)
assert len(e12["show"]) == len(OUT["ex12"])
for sw, (expr, val) in zip(e12["show"], OUT["ex12"]): sw["expression"] = expr; sw["expected"] = val
json.dump(m, open(MNEW, "w"), ensure_ascii=False, indent=1)
print("written", NEW, PNEW, MNEW)
