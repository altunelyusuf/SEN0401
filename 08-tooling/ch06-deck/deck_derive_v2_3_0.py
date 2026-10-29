#!/usr/bin/env python3
"""Chapter 6 deck v2.3.0 (a NEW tool file; urgent task TK_Urgent_Ch06_Deck_Build). The deck v2.2.0 is read, never written; its SHA-256 is printed before and after.
STEP 1 (code corrections): on the 18 code slides the prompt-bearing code frames are replaced by ONE code box per example ('code N', the example of the page's chapter code tab, PEP 8 indentation,
no lambda, no '>>> ' or '... ' prompts) with the executed result apart, directly under it ('result N'), and the explanation of each group of lines beside it; the native chart or table of the result stays.
It also writes the chapter-code manifest 03-materials/ch06/page/chapter_code_ch06_v1_2_0.json (the corrected code, the shown results, the slide numbers).
STEP 2 (enhancement): see deck_enhance_v2_3_0.py, which runs after this on the same output when --step2 is given.
Usage: deck_derive_v2_3_0.py [--step2]"""
__version__ = "2.3.0"
import hashlib, json, os, re, sys, zipfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from deck_lib_v2_3_0 import *
from pptx import Presentation

SRC = os.path.join(ROOT, "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_2_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx")
MAN_NEW = os.path.join(ROOT, "03-materials/ch06/page/chapter_code_ch06_v1_2_0.json")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def build_examples():
    man = json.load(open(MANIFEST_OLD)); ex = []
    for e in man["examples"]:
        lines = e["code"].split("\n"); cl, st = corrected(lines)
        if e["id"] == "ex12":
            cl, mp = fix_ex12(lines); st = [mp[i] for i in range(len(lines))]
            assert "lambda" not in "\n".join(cl)
        ex.append({"order": e["order"], "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": e["branch"], "code_old": lines, "code": cl, "start": st, "show": e["show"]})
    return man, ex


def step1(prs, ex):
    for e in ex:
        s = prs.slides[e["slide"] - 1]; N = e["order"]
        frames = []; expl = []; delete_these = []
        for sh in s.shapes:
            L, T, W, H = [v // U for v in (sh.left, sh.top, sh.width, sh.height)]
            if sh.has_text_frame and sh.text_frame.text.startswith(">>> "): frames.append(sh)
            if L < 620 and 125 < T < 500 and not (L == 50 and T >= 500):
                delete_these.append(sh)
                if sh.has_text_frame and L == 80: expl.append(sh.text_frame.text)
        cnt = [sum(1 for p in f.text_frame.paragraphs if "".join(r.text for r in p.runs).startswith(">>> ")) for f in sorted(frames, key=lambda f: f.top)]
        assert sum(cnt) == len(e["code_old"]) and len(cnt) == len(expl), (N, cnt, len(e["code_old"]), len(expl))
        for sh in delete_these: delete(sh)
        # groups -> line ranges of the corrected code
        idx = 0; rng = []
        for c in cnt:
            a = e["start"][idx]; idx += c; b = (e["start"][idx] if idx < len(e["start"]) else len(e["code"])) - 1; rng.append((a + 1, b + 1))
        # layout: the largest type size at which code, result and explanation fit the left column
        longest = max(len(l) for l in e["code"]); assert longest <= 56, (N, longest)
        rows = [(w["expression"], w["expected"]) for w in e["show"]]
        done = False
        for fs, rfs, efs_list in ((11, 10.5, (12, 11.5, 11, 10.5)), (10.5, 10, (12, 11.5, 11, 10.5)), (10, 10, (11, 10.5, 10)), (10, 9.5, (10, 9.5)), (9.5, 9, (9.5,))):
            pitch = fs * 1.25 / 0.72; ch = round(len(e["code"]) * pitch + 16, 1); y0 = 133
            rp = rfs * 1.25 / 0.72; per = int(535 * 0.72 / (rfs * 0.6))
            nl = sum(max(1, -(-(len(a) + 3 + len(b)) // per)) for a, b in rows)
            rh = round(nl * rp + 14 + 12, 1); ry = round(y0 + ch + 7, 1); ey = round(ry + rh + 7, 1); eh = 498 - ey
            if len(e["code"]) and max(len(l) for l in e["code"]) * fs * 0.6 / 0.72 > 530: continue
            for efs in efs_list:
                need = sum(est_lines("Lines 10-10  " + t, efs, 565, 0.47) for t in expl) * efs * 1.2 / 0.72 + 3 * 4 / 0.72
                if need <= eh: done = True; break
            if done: break
        assert done, ("explanation too tall", N)
        code = box(s, "code %d" % N, 40, y0, 565, ch, fill=CODEBG, line=CODEBG, adj=0.04)
        text(s, "code %d" % N, 0, 0, 0, 0, code_paras(e["code"], fs), anchor="m", wrap=False, inset=12, shape=code)
        res = box(s, "result %d" % N, 40, ry, 565, rh, fill=WHITE, line=TEAL, adj=0.06, lw=1.25)
        paras = [{"runs": [("RESULT  ", 8.5, TEAL, True), ("Python 3.14.6 · the chapter setup defines ALICE, PREV, FIRST and tx", 8.5, MUTE, False, True)], "space": 2}]
        for a, b in rows: paras.append({"runs": [(a, rfs, MUTE, False, False, "Courier New"), ("  →  ", rfs, ORANGE, True, False, "Courier New"), (b, rfs, INK, True, False, "Courier New")]})
        text(s, "result %d" % N, 0, 0, 0, 0, paras, anchor="m", wrap=True, inset=10, shape=res)
        ep = []
        for (a, b), t in zip(rng, expl):
            lab = ("Line %d" % a) if a == b else ("Lines %d-%d" % (a, b))
            ep.append({"runs": [(lab + "  ", efs, ORANGE, True), (t, efs, INK)], "space": 3})
        text(s, "explanation %d" % N, 40, ey, 565, eh, ep)
        e["layout"] = {"code": (y0, ch), "result": (ry, rh), "expl": (ey, eh), "ranges": rng}
    return prs


def main():
    before = sha(SRC)
    man, ex = build_examples()
    prs = Presentation(SRC)
    step1(prs, ex)
    if "--step2" in sys.argv:
        import deck_enhance_v2_3_0 as E
        E.step2(prs, ex)
    prs.core_properties.version = "2.3.0"
    prs.save(DST)
    new = {"manifest": "chapter_code_ch06_v1_2_0", "chapter": 6, "deck": os.path.basename(DST), "deck_version": "2.3.0", "python_of_expected_values": man["python_of_expected_values"],
           "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page; no lambda, PEP 8 indentation, no prompts",
           "library": man["library"], "setup": man["setup"],
           "examples": [{"order": e["order"], "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": e["branch"], "library": man["library"]["module"], "needs": ["setup"],
                         "code": "\n".join(e["code"]), "show": e["show"]} for e in ex]}
    if not os.path.exists(MAN_NEW):
        json.dump(new, open(MAN_NEW, "x"), indent=1, ensure_ascii=False)
    print("SHA-256 of v2_2_0 before:", before); print("SHA-256 of v2_2_0 after: ", sha(SRC)); print("written", DST)


if __name__ == "__main__": main()
