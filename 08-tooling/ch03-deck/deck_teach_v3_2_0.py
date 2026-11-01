#!/usr/bin/env python3
"""Chapter 3 deck v3.2.0 (a NEW tool file; task TK_Ch03_DeckTeach_Build). The deck v3.1.0 is read, never written; its SHA-256 is printed before and after.
It applies the chapter 6 Friday method (08-tooling/ch06-deck helpers) to the chapter 3 deck:
(1) the three true stories are told as sentences with real names, dates and places (no label words); the picture, its credit and the live source link stay;
(2) nineteen picture slides are added, drawn with native shapes, tables and native charts, for the concepts the earlier deck named without showing (one of them teaches the lambda that the code of the decoding slide uses);
(3) every slide gets short speaker notes that carry clues (deck_teach_content_v3_2_0.py);
(4) no text run below 9 pt anywhere; every result shape 10 pt; a result that does not fit its column gets the full content width; slide 24 has no gap;
(5) the slide numbers 'n / N' and the route slide follow the new order.
The code boxes, their shape names, their texts and the result texts are not touched (the code size of the result shapes rises to 10 pt; the geometry of the result shapes moves).
Usage: deck_teach_v3_2_0.py OLD NEW [MAP_JSON]"""
__version__ = "3.2.0"
import hashlib, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from deck_teach_base_v3_2_0 import *
import deck_teach_slides_v3_2_0 as SL
import deck_teach_content_v3_2_0 as C

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

STORIES = {
    6: ("8 January 2009 · the metzdowd.com cryptography mailing list · SourceForge",
        ["On 8 January 2009 Satoshi Nakamoto, the pseudonymous author of the white paper, announced Bitcoin 0.1 on the metzdowd.com cryptography mailing list.",
         "It was a Windows program that anyone could download from SourceForge and run, and it came five days after the first block had been mined.",
         "Only running software could start the network, so the program came before any written rule.",
         "Later Satoshi wrote that, once 0.1 was out, the core design was set in stone."],
        "A reference implementation: its rules are what that program does.", {}),
    13: ("13 September 2021 · the guix.sigs repository, beside bitcoin/bitcoin on GitHub",
         ["On 13 September 2021 Bitcoin Core released version 22.0, the first release built with Guix, a build system that Carl Dong wrote.",
          "Guix lets anyone rebuild the program from the tagged source and get the same file, bit for bit.",
          "Each independent builder signs the hashes of what they built, and the signatures are collected in the guix.sigs repository on GitHub.",
          "For release 31.1 the SHA256SUMS file carries 11 good signatures, so a download is checked against many builders and not against one person's word."],
         "Several strangers who reach the same hash are harder to fool than one signer.", {"lesson_under_picture": True, "pic_w": 430}),
    22: ("7 April 2014 · the public bitcoin/bitcoin repository on GitHub",
         ["Satoshi Nakamoto handed the project to Gavin Andresen in 2011, and Andresen led the software after him.",
          "On 7 April 2014 Andresen passed the lead-maintainer role of Bitcoin Core to Wladimir van der Laan, who led until 2022.",
          "Andresen wanted to focus on protocol work, and a reference implementation cannot wait for one person.",
          "Every change is reviewed in the open on GitHub, whoever holds the role."],
         "The reference implementation is an institution, not a person.", {}),
}
PARTS = [(3, 4), (5, 8), (9, 14), (15, 22), (23, 27), (28, 31), (32, 36), (37, 39), (40, 42)]


def renumber(prs, N):
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): settext(sh, "%d / %d" % (i, N))


def build(old_path, new_path):
    prs = Presentation(old_path)
    old = list(prs.slides); assert len(old) == 42
    # (1) repairs of the old slides
    slide8(prs); widen_long_results(prs); slide24(prs)
    for n, (head, paras, lesson, kw) in STORIES.items(): story(prs, n, head, paras, lesson, **kw)
    settext(one(old[28], "TextBox 2"), "Decoding Alice's transaction with a lambda")                # the slide whose code uses a lambda names it in its title
    settext(one(old[35], "TextBox 3"), "Block timestamps are guesses; the median time past is not")
    for s in old:
        for sh in s.shapes:
            if getattr(sh, "has_table", False) and sh.has_table: raise_runs(sh, 10.0)
            else: raise_runs(sh, 10.0 if (old.index(s) == 40 and sh.has_text_frame and sh.name.startswith("TextBox") and sh.top / U > 135) else 9.0)
            if sh.has_chart: chart_min(sh.chart, 900)
    # (2) the nineteen picture slides
    src = old[6]; newslides = {}
    for after, key, title, sub, take, fn in SL.SPECS:
        s = SL.new_slide(prs, src, title, sub, take); fn(s)
        s.notes_slide.notes_text_frame.text = C.NEW[key]
        newslides.setdefault(after, []).append((key, s))
    for i, s in enumerate(old, 1): s.notes_slide.notes_text_frame.text = C.NOTES[i]
    lst = prs.slides._sldIdLst; ids = list(lst)
    by_slide = {sl.slide_id: el for sl, el in zip(list(prs.slides), ids)}
    order = []
    for i, sl in enumerate(old, 1):
        order.append(by_slide[sl.slide_id])
        for key, ns in newslides.get(i, []): order.append(by_slide[ns.slide_id])
    for el in ids: lst.remove(el)
    for el in order: lst.append(el)
    prs.part.rename_slide_parts([el.rId for el in lst])
    N = len(order); renumber(prs, N)
    newpos = {sl.slide_id: k for k, sl in enumerate(prs.slides, 1)}; oldpos = {i: newpos[sl.slide_id] for i, sl in enumerate(old, 1)}
    route = prs.slides[1]; k = 0
    for sh in route.shapes:
        if not sh.has_text_frame: continue
        tx = sh.text_frame.text.strip()
        if len(sh.text_frame.paragraphs) > 1 and re.fullmatch(r"\(slides \d+-\d+\)", sh.text_frame.paragraphs[-1].text):
            a, b = PARTS[k]; k += 1
            sh.text_frame.paragraphs[1].runs[0].text = "(slides %d-%d)" % (oldpos[a] if a > 3 else 3, (oldpos[PARTS[k][0]] - 1) if k < len(PARTS) else N)
        elif tx == "42": settext(sh, str(N))
    assert k == 9, k
    prs.core_properties.version = "3.2.0"
    prs.save(new_path)
    return N, oldpos, {key: newpos[s.slide_id] for lst_ in newslides.values() for key, s in lst_}


def main(old, new):
    before = sha(old); print("SHA-256 old deck before:", before)
    N, oldpos, newpos = build(old, new)
    after = sha(old); print("SHA-256 old deck after: ", after, "UNCHANGED" if before == after else "CHANGED")
    assert before == after
    print("wrote", new, sha(new), "slides", N)
    print("new slides:", json.dumps(newpos)); print("old->new:", json.dumps(oldpos))
    if len(sys.argv) > 3: json.dump({"slides": N, "new": newpos, "old_to_new": oldpos, "old_sha256": before, "new_sha256": sha(new)}, open(sys.argv[3], "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
