#!/usr/bin/env python3
"""Chapter 6 deck v2.3.0 (a NEW tool file; urgent task TK_Urgent_Ch06_Deck_Build). The deck v2.2.0 is read, never written; its SHA-256 is printed before and after.
STEP 1 (code corrections): on the 18 code slides the prompt-bearing code frames are replaced by ONE code box per example ('code N', the example of the page's chapter code tab, PEP 8 indentation,
no lambda, no '>>> ' or '... ' prompts) with the executed result apart, directly under it ('result N'), and the explanation of each group of lines beside it; the native chart or table of the result stays.
It also writes the chapter-code manifest 03-materials/ch06/page/chapter_code_ch06_v1_2_0.json (the corrected code, the shown results, the slide numbers).
STEP 2 (enhancement): see deck_enhance_v2_3_0.py, which runs after this on the same output when --step2 is given.
Usage: deck_derive_v2_3_1.py [--step2]"""
__version__ = "2.3.1"
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
        # layout: the largest type size at which the code frames, the result and the explanation fit the left column
        longest = max(len(l) for l in e["code"]); assert longest <= 56, (N, longest)
        rows = [(w["expression"], w["expected"]) for w in e["show"]]
        G = len(rng); done = False
        for fs, rfs, efs_list in ((11, 10.5, (12, 11.5, 11, 10.5)), (10.5, 10, (12, 11.5, 11, 10.5)), (10, 10, (11, 10.5, 10)), (10, 9.5, (10, 9.5)), (9.5, 9, (9.5, 9.0)), (9, 9, (9.0,))):
            if longest * fs * 0.6 / 0.72 > 530: continue
            pitch = fs * 1.25 / 0.72
            fh = [round((b_ - a_ + 1) * pitch + 8, 1) for a_, b_ in rng]; y0 = 128; ch = sum(fh) + 3 * (G - 1)
            rp = rfs * 1.25 / 0.72; per = int(530 * 0.72 / (rfs * 0.62))
            rl = [max(1, -(-(len(a_) + 5 + len(b_)) // per)) for a_, b_ in rows]
            rh = round(sum(rl) * rp + 16 + 8, 1); ry = round(y0 + ch + 5, 1); ey = round(ry + rh + 4, 1); eh = 502 - ey
            for efs in efs_list:
                el = [est_lines("Lines 10-10  " + t, efs, 565, 0.52) for t in expl]
                need = sum(l * efs * 1.2 / 0.72 + 8 for l in el)
                if need <= eh: done = True; break
            if done: break
        assert done, ("explanation too tall", N)
        y = y0
        for (a_, b_), h_ in zip(rng, fh):
            fr = box(s, "code %d" % N, 40, y, 565, h_, fill=CODEBG, line=CODEBG, adj=0.05)
            text(s, "code %d" % N, 0, 0, 0, 0, code_paras(e["code"][a_ - 1:b_], fs), anchor="m", wrap=False, inset=12, shape=fr); y += h_ + 3
        box(s, "result %d" % N, 40, ry, 565, rh, fill=WHITE, line=TEAL, adj=0.06, lw=1.25)
        text(s, "result %d" % N, 50, ry + 3, 545, 12, [[("RESULT  ", 8.5, TEAL, True), ("Python 3.14.6 · the chapter setup defines ALICE, PREV, FIRST and tx", 8.5, MUTE, False, True)]])
        yy = ry + 15
        for (a_, b_), l_ in zip(rows, rl):
            hh = l_ * rp + 1
            text(s, "result %d" % N, 50, yy, 545, hh, [[(a_, rfs, MUTE, False, False, "Courier New"), ("  →  ", rfs, ORANGE, True, False, "Courier New"), (b_, rfs, INK, True, False, "Courier New")]]); yy += hh
        yy = ey
        for (a_, b_), t, l_ in zip(rng, expl, el):
            lab = ("Line %d" % a_) if a_ == b_ else ("Lines %d-%d" % (a_, b_)); hh = l_ * efs * 1.2 / 0.72 + 8
            text(s, "explanation %d" % N, 40, yy, 565, hh, [[(lab + "  ", efs, ORANGE, True), (t, efs, INK)]]); yy += hh
        e["layout"] = {"code": (y0, ch), "result": (ry, rh), "expl": (ey, eh), "ranges": rng}
    return prs


def main():
    before = sha(SRC)
    man, ex = build_examples()
    prs = Presentation(SRC)
    step1(prs, ex)
    if "--step2" in sys.argv:
        import deck_enhance_v2_3_0 as E
        N, oldpos = E.step2(prs, ex)
        for e in ex: e["slide"] = oldpos[e["slide"]]
        global MAN_NEW
        MAN_NEW = os.path.join(ROOT, "03-materials/ch06/page/chapter_code_ch06_v1_3_0.json")
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
