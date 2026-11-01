#!/usr/bin/env python3
"""Chapter 4 deck v3.6.0 (a NEW tool file; task TK_Ch04_DeckTeach_Build). The deck v3.5.0 is read, never written; its SHA-256 is printed before and after.
It applies the chapter 6 Friday method (08-tooling/ch06-deck helpers, as reused by the chapter 3 teaching build) to the chapter 4 deck:
(1) the three true stories are told as sentences with real names, dates and places (no label words); the picture, its credit and the live source link stay; the credit lines are widened so that none wraps;
(2) thirty-two picture slides are added, drawn with native shapes and tables, for the concepts the earlier deck named without showing; one of them teaches the lambda that three code slides use, whose titles now name it;
(3) every slide gets short speaker notes that carry clues (deck_teach_content_v3_6_0.py);
(4) no text run below 9 pt anywhere; results and code are untouched (they were already 10 pt and on one line in v3.5.0);
(5) the slide numbers 'n / N' and the route slide follow the new order.
Usage: deck_teach_v3_6_0.py OLD NEW [MAP_JSON]"""
__version__ = "3.6.0"
import hashlib, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from deck_teach_kit_v3_6_0 import *
import deck_teach_specs_v3_6_0 as SP
import deck_teach_content_v3_6_0 as C

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

STORIES = {
    8: ("3 June 1976 · Stanford University · IEEE Transactions on Information Theory",
        ["In 1976 Whitfield Diffie and Martin Hellman, cryptographers at Stanford University in California, sent the paper 'New Directions in Cryptography' to the IEEE Transactions on Information Theory.",
         "The journal stamped the manuscript received on 3 June 1976 and printed it in its November issue, volume IT-22.",
         "Until then secret keys travelled to every partner. They proposed a key in two halves: each user publishes one, keeps the other, and a one-way computation links them.",
         "That is the machinery of this chapter: multiply a point, publish the result, keep the multiplier. For this work both received the ACM Turing Award for 2015."],
        "Every address in this chapter stands on one 1976 idea", {}),
    23: ("8 January 2009 · the file src/base58.h in the bitcoin/bitcoin source tree",
         ["Satoshi Nakamoto, the pseudonymous author of Bitcoin's first software, announced version 0.1 on 8 January 2009; the copyright line of base58.h names him.",
          "Right below it sits a design memo with four reasons. People copy addresses by hand, in e-mail and by double-click, so the text must survive all three.",
          "Of 62 letters and digits the four look-alikes 0, O, I and l go, and so does all punctuation, so 58 symbols remain: the alphabet of every legacy address.",
          "The memo's own date is not recorded; the file is public on GitHub."],
         "Address formats are human-factors engineering, written down in the source", {}),
    43: ("6 October 2026 · the Bitcoin main chain · Blockstream Explorer",
         ["Someone spelled a message in base58 letters, 1BitcoinEaterAddressDontSend, and closed it with the six letters f59kuE that make the checksum fit.",
          "The result is a valid address whose key nobody holds, because it was chosen as text and not computed from a key.",
          "Thousands of anonymous senders paid to it anyway. On 6 October 2026 Blockstream Explorer showed 13.41747849 bitcoin in 5,832 outputs, none ever spent.",
          "A checksum catches typing mistakes, not a missing key, so wallets accept the address without a warning."],
         "An address is a commitment to a key, not proof that a key exists", {}),
}
PARTS = [(3, 4), (5, 15), (16, 26), (27, 34), (35, 38), (39, 44), (45, 47)]
NEWTITLES = {9: "Key below n, checked with a lambda", 31: "Collision and preimage work, with lambdas", 34: "Bech32 or Bech32m? A lambda tells them apart"}



def story2(prs, n, head, paras, lesson):
    """the story slide of v3.5.0 told as sentences: the six label boxes (WHO, WHAT, WHEN, WHERE, WHY, HOW) are replaced by a heading line and full sentences; the lesson box stands under the picture;
    the picture credit is a full-width single line at the foot of the slide; the live source link line stays"""
    s = prs.slides[n - 1]
    labels = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b", sh.text_frame.text)]
    assert len(labels) == 6, (n, len(labels))
    for sh in labels: delete(sh)
    pic = [sh for sh in s.shapes if sh.shape_type == 13][0]
    cap = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("Picture:")][0]
    read = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("READ")][0]
    raise_runs(cap, 9.0); raise_runs(read, 10.0)
    tx = 375; tw = 575
    hh0 = est_lines(head, 12, tw, 0.56) * 12 * 1.25 / 0.72 + 4
    T(s, "story head", tx, 135, tw, hh0, [P(head, 12, ORANGE, True)]); y = 135 + hh0 + 6
    for p in paras:
        hh = est_lines(p, 12, tw, 0.5) * 12 * 1.25 / 0.72 + 4
        T(s, "story", tx, y, tw, hh, [P(p, 12, INK)]); y += hh + 4
    assert y <= 452, (n, y)
    R(s, "lesson", 50, top(pic) + hei(pic) + 12, 300, 56, fill=SOFT, line=TEAL, paras=[P(lesson, 12, INK, True)], inset=10)
    setgeo(read, x=tx, y=458, w=tw, h=19); setgeo(cap, x=50, y=481, w=900, h=17)
    return s


def title_size(sh, title):
    for r in sh.text_frame.paragraphs[0].runs: r.font.size = Pt(28 if len(title) <= 32 else (24 if len(title) <= 46 else 21))


def renumber(prs, N):
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): settext(sh, "%d / %d" % (i, N))


def credit_lines(prs, old):
    """every picture credit sets on one line: the story credits go to a full-width line under the link line; slide 1 and slide 25 get a wider box"""
    s = old[0]; cap = one(s, "TextBox 12"); sub = one(s, "TextBox 10")
    setgeo(sub, h=56); setgeo(cap, x=340, y=sub.top / U + 58, w=610, h=18)
    cap.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
    s = old[24]; cap = one(s, "TextBox 8"); setgeo(cap, x=50, w=900, h=18)


def build(old_path, new_path):
    prs = Presentation(old_path)
    old = list(prs.slides); assert len(old) == 47
    for n, (head, paras, lesson, kw) in STORIES.items():
        story2(prs, n, head, paras, lesson)
    credit_lines(prs, old)
    for n in STORIES: split30(old[n - 1]); fit(old[n - 1])
    for n, t in NEWTITLES.items():
        sh = one(old[n - 1], "TextBox 2"); settext(sh, t); title_size(sh, t)
    for i, s in enumerate(old, 1):                                      # no text run below 9 pt
        for sh in s.shapes:
            if getattr(sh, "has_table", False) and sh.has_table: raise_runs(sh, 10.0)
            else: raise_runs(sh, 9.0)
            if sh.has_chart: chart_min(sh.chart, 900)
    # the picture slides
    src = old[8]; newslides = {}
    for after, key, title, sub, take, fn in SP.SPECS:
        s = new_slide(prs, src, title, sub, take); fn(s); split30(s); fit(s)
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
        elif tx == "47": settext(sh, str(N))
    assert k == 7, k
    prs.core_properties.version = "3.6.0"
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
