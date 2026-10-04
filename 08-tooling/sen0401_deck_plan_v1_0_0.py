#!/usr/bin/env python3
"""Builds the slide plan of a SEN0401 lecture deck (chapters 1 to 3) from the chapter's own material.

What it reads, and nothing else:
  * the chapter corpus `sen0401_chNN_corpus_v*.py` - the taxonomy, and for every concept its four to six
    paragraphs (what it is, why it matters, where you meet it, how it works, what to watch for);
  * the chapter deck's `examples_out_v*.json` - every worked example, executed, with its real output;
  * the chapter's research record `03-materials/chNN/rdodi/sen0401_chNN_research_v*.ttl` - the publication
    behind every author-year citation the prose uses;
  * the course learning outcomes `01-outcomes/sen0401_outcomes_v1_0_0.ttl`, the chapter's own objectives,
    its question bank and its discussion prompts in `chNN-page/`.

What it writes: `chNN-deck/deck_plan_v<ver>.json`, a list of slides with every box placed and every font
size chosen, having checked that each piece of text fits the box it is placed in. The renderer
`chNN-deck/deck_v<ver>.js` draws exactly what is in the plan and invents nothing.

Usage: sen0401_deck_plan_v1_0_0.py <NN> <plan version, e.g. 1_2_0>
"""
__version__ = "1.0.0"

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from sen0401_deck_lib_v1_0_0 import facet, sentences, take, text_height, wrap_lines  # noqa: E402

# ----------------------------------------------------------------------------------------------------
# the frame every slide is drawn in (inches, on the 10 x 5.625 widescreen page the house uses)
# ----------------------------------------------------------------------------------------------------
LEFT, RIGHT = 0.5, 9.5
WIDE = RIGHT - LEFT                       # 9.0
TOP = 1.40                                # first line under the slide title
BOTTOM = 5.08                             # last line a box may reach
FOOT_Y = 4.76
COL_W = 4.35                              # a two-column slide
COL2_X = 5.15
PAD_H, PAD_B = 0.58, 0.18                 # a card's head band and its bottom padding
CODE_PAD = 0.26                           # a code card's top and bottom padding together

CHAPTERS = {
    "01": dict(corpus="sen0401_ch01_corpus_v1_2_0", research="ch01/rdodi/sen0401_ch01_research_v1_2_0.ttl",
               bank="ch01-page/question_bank_v1_1_0.json", quiz="ch01-page/quiz_v1_0_0.json",
               objectives="ch01-page/objectives_v1_0_0.json", discussion="ch01-page/discussion_v1_0_0.json",
               book_chapter="1, Introduction", outcome="LO1",
               title="Chapter 1: Introduction",
               sub="What Bitcoin is, what it is made of, and why every part of it exists",
               nxt="Next week: Chapter 2 - How Bitcoin Works",
               nxt_sub="Before then: work through the chapter 1 page, and run its examples in the playground."),
    "02": dict(corpus="sen0401_ch02_corpus_v1_2_0", research="ch02/rdodi/sen0401_ch02_research_v1_2_0.ttl",
               bank="ch02-page/question_bank_v1_0_0.json", quiz="ch02-page/quiz_v1_0_0.json",
               objectives="ch02-page/objectives_v1_0_0.json", discussion="ch02-page/discussion_v1_0_0.json",
               book_chapter="2, How Bitcoin Works", outcome="LO2",
               title="Chapter 2: How Bitcoin Works",
               sub="One real payment, followed from Alice's wallet to a block, with every figure recomputed",
               nxt="Next week: Chapter 3 - Bitcoin Core, the reference implementation",
               nxt_sub="Before then: work through the chapter 2 page, and follow the transaction in its Code Lab."),
    "03": dict(corpus="sen0401_ch03_corpus_v1_1_0", research="ch03/rdodi/sen0401_ch03_research_v1_1_0.ttl",
               bank="ch03-page/question_bank_v1_0_0.json", quiz="ch03-page/quiz_v1_0_0.json",
               objectives="ch03-page/objectives_v1_0_0.json", discussion="ch03-page/discussion_v1_0_0.json",
               book_chapter="3, Bitcoin Core: The Reference Implementation", outcome="LO3",
               title="Chapter 3: Bitcoin Core",
               sub="Building, configuring and questioning the reference node - checked against release 31.1",
               nxt="Next week: Chapter 4 - Keys and Addresses",
               nxt_sub="Before then: work through the chapter 3 page, and decode the transaction in its Code Lab."),
}

BOOK = "Mastering Bitcoin, 3rd edition, chapter %s (Antonopoulos and Harding, 2023)"


# ----------------------------------------------------------------------------------------------------
# reading the chapter's material
# ----------------------------------------------------------------------------------------------------

def load_corpus(name):
    mod = __import__(name)
    nodes = []
    for nid, label, level, parent, leaf, paras in mod.NODES:
        nodes.append(dict(id=nid, label=label or re.sub(r"(?<!^)(?=[A-Z])", " ", nid),
                          level=level, parent=parent, leaf=leaf, paras=[(f, t) for f, t in paras]))
    return mod, nodes


def publications(path):
    """author-year string -> the publication label the research record gives it."""
    text = open(path, encoding="utf-8").read()
    out = {}
    for label in re.findall(r'a res:Publication ;\s*rdfs:label "((?:[^"\\]|\\.)*)"', text):
        label = label.replace('\\"', '"')
        for cite in re.findall(r"\(([^()]{3,70}?, (?:19|20)\d\d[a-z]?)\)", label):
            out.setdefault(cite, label)
    return out


def outcomes(path, want):
    text = open(path, encoding="utf-8").read()
    out = {}
    for ident, code, statement in re.findall(
            r"sen0401:(LO\d+) a case:dtCFItem ; case:humanCodingScheme \"([^\"]+)\"[^.]*?"
            r"case:fullStatement \"((?:[^\"\\]|\\.)*)\"", text, re.S):
        out[ident] = (code, statement.replace('\\"', '"'))
    return out[want], out


def citations_used(nodes):
    found = []
    for node in nodes:
        for _f, t in node["paras"]:
            found += re.findall(r"\(([A-Z][^()]{2,68}?, (?:19|20)\d\d[a-z]?)\)", t)
    seen = []
    for c in found:
        if c not in seen:
            seen.append(c)
    return seen


# ----------------------------------------------------------------------------------------------------
# fitting
# ----------------------------------------------------------------------------------------------------

def card_height(body, width, size):
    return PAD_H + text_height(body, width - 0.4, size) + PAD_B


def code_height(rows, width, size):
    lines = 0
    for stmt, out in rows:
        lines += max(1, int((len(stmt) + 4) / _cpl(width, size)) + (1 if (len(stmt) + 4) % _cpl(width, size) else 0))
        if out:
            lines += max(1, -(-len(out) // _cpl(width, size)))
    return lines * size * 1.22 / 72.0 + CODE_PAD


def prog_height(lines, width, size):
    total = sum(max(1, -(-len(l) // _cpl(width, size))) for l in lines)
    return total * size * 1.22 / 72.0 + CODE_PAD


def _cpl(width, size):
    return max(1, int((width - 0.4) * 72.0 / (size * 0.60)))


def table_height(rows, colW, fs, rowH):
    """How tall the table really becomes once a long cell wraps inside its own column."""
    total = 0.0
    for r in rows:
        lines = max(wrap_lines(c, colW[j] - 0.16, fs) for j, c in enumerate(r))
        total += max(rowH, lines * fs * 1.22 / 72.0 + 0.14)
    return total


def widest(rows):
    return max((len(s) + 4 for s, _ in rows), default=0)


# ----------------------------------------------------------------------------------------------------
# slide builders
# ----------------------------------------------------------------------------------------------------

def card(x, y, w, h, head, body, accent="orange", fs=13):
    return dict(t="card", x=x, y=y, w=w, h=h, head=head, body=body, accent=accent, fs=fs)


def code(x, y, w, h, rows, fs, cap=None):
    return dict(t="code", x=x, y=y, w=w, h=h, rows=rows, fs=fs, cap=cap)


def prog(x, y, w, h, lines, fs, cap=None, out=None, block=None, first=1, total=None):
    return dict(t="prog", x=x, y=y, w=w, h=h, lines=lines, fs=fs, cap=cap, out=out,
                block=block, first=first, total=total or len(lines))


def boxes(x, y, w, h, items, cols, fs=12, subfs=10, arrows=False, accent=None):
    """Place a grid of labelled boxes, trimming each box's second line until it fits its own box."""
    cols = max(1, cols)
    rows_n = -(-len(items) // cols)
    bw = (w - (cols - 1) * 0.16) / cols
    bh = (h - (rows_n - 1) * 0.14) / rows_n
    out = []
    for it in items:
        label, sub = it["label"], it.get("sub")
        room = bh - 0.12 - text_height(label, bw - 0.20, fs)
        if sub:
            sub = " ".join(sub.split())
            cut = False
            while sub and text_height(sub + ("…" if cut else ""), bw - 0.20, subfs) > room:
                words = sub.rsplit(" ", 1)
                if len(words) == 1:
                    sub = ""
                    break
                sub = words[0].rstrip(",;:.")
                cut = True
            if cut and sub:
                sub += "…"
        out.append(dict(label=label, sub=sub or None))
    return dict(t="boxes", x=x, y=y, w=w, h=h, items=out, cols=cols, fs=fs, subfs=subfs,
                arrows=arrows, accent=accent or [], bw=bw, bh=bh)


def table(x, y, w, rows, colW, fs=12, rowH=0.4):
    return dict(t="table", x=x, y=y, w=w, rows=rows, colW=colW, fs=fs, rowH=rowH)


def text(x, y, w, h, body, fs=13, italic=False, bold=False, color="ink", font="B", align="left"):
    return dict(t="text", x=x, y=y, w=w, h=h, body=body, fs=fs, italic=italic, bold=bold,
                color=color, font=font, align=align)


FOOT_H = 0.44          # two lines of 12-point italic, the most a footnote may take


def foot(body):
    """A footnote under the content, trimmed to the two lines the frame leaves for it."""
    body = " ".join(str(body).split())
    while body and text_height(body, WIDE, 12) > FOOT_H and len(sentences(body)) > 1:
        body = " ".join(sentences(body)[:-1])
    while body and text_height(body, WIDE, 12) > FOOT_H:
        words = body.rsplit(" ", 1)
        if len(words) == 1:
            break
        body = words[0].rstrip(",;:.") + "\u2026"
    return dict(t="foot", x=LEFT, y=BOTTOM - FOOT_H, w=WIDE, h=FOOT_H, body=body, fs=12)


def slide(kind, title=None, sub=None, items=None, notes="", bg="light"):
    return dict(kind=kind, title=title, sub=sub, items=items or [], notes=notes, bg=bg)


def notes_of(node, extra=""):
    why = facet(node["paras"], "Why it matters")
    watch = facet(node["paras"], "Watch out")
    where = facet(node["paras"], "Where you meet it")
    parts = [p for p in (why, where if not watch else "", watch, extra) if p]
    return "\n\n".join(parts)


# ----------------------------------------------------------------------------------------------------

def build(nn, ver):
    cfg = CHAPTERS[nn]
    mod, nodes = load_corpus(cfg["corpus"])
    by_id = {n["id"]: n for n in nodes}
    kids = {}
    for n in nodes:
        kids.setdefault(n["parent"], []).append(n)
    branches = kids.get(None, [])

    deck_dir = os.path.join(HERE, "ch%s-deck" % nn)
    ex = json.load(open(os.path.join(deck_dir, "examples_out_v1_1_0.json")))
    py = ex["_python"]
    groups, blocks = ex["groups"], ex["blocks"]

    pubs = publications(os.path.join(REPO, "03-materials", cfg["research"]))
    lo, _all_lo = outcomes(os.path.join(REPO, "01-outcomes", "sen0401_outcomes_v1_0_0.ttl"), cfg["outcome"])
    objectives = json.load(open(os.path.join(HERE, cfg["objectives"])))
    bank = json.load(open(os.path.join(HERE, cfg["bank"])))
    discussion = json.load(open(os.path.join(HERE, cfg["discussion"])))["items"]
    cqs = list(getattr(mod, "CQS", []))
    book_ref = BOOK % cfg["book_chapter"]

    slides = []
    shown_programs = []
    n_leaf = sum(1 for n in nodes if n["leaf"])
    n_ex = len(groups) + len(blocks)

    # ---- 1 title ---------------------------------------------------------------------------------
    slides.append(slide("title", cfg["title"], cfg["sub"], [], bg="dark", notes=(
        "%s, free under CC BY-SA 4.0. This deck follows the chapter's own concept taxonomy: %d concepts in "
        "%d branches, of which %d carry a worked example. Every number, hash, address and output on these "
        "slides was executed under Python %s by the chapter's own examples and checked against the figure "
        "the chapter corpus records; the deck is refused by its checker if any of them stops agreeing."
        % (book_ref, n_leaf, len(branches), n_ex, py))))

    # ---- 2 what the chapter covers --------------------------------------------------------------
    items = [dict(label=b["label"], sub=sentences(facet(b["paras"], "What it is"))[0])
             for b in branches]
    cols = 3 if len(branches) <= 6 else 4
    rows_n = -(-len(branches) // cols)
    about = take(getattr(mod, "DOC_ABOUT", ""), 320)
    about_h = text_height(about, WIDE, 14) + 0.04
    slides.append(slide("content", "What this chapter covers",
                        "%d concepts, in %d branches" % (n_leaf, len(branches)),
                        [text(LEFT, TOP, WIDE, about_h, about, fs=14),
                         boxes(LEFT, TOP + about_h + 0.12, WIDE, BOTTOM - (TOP + about_h + 0.12), items, cols,
                               fs=13, subfs=9.5, accent=list(range(0, len(branches), 2)))],
                        notes=("The branches are the chapter's own: %s. Say at the start that the order of the "
                               "lecture is the order of the taxonomy, so that a student who opens the interactive "
                               "page afterwards finds the same tree. %s"
                               % (", ".join(b["label"] for b in branches), getattr(mod, "PROVENANCE", "")[:600]))))

    # ---- 3 the outcomes ---------------------------------------------------------------------------
    obj_rows = [["Code", "What you should be able to do after this session", "Level"]]
    for key in sorted(k for k in objectives if k.startswith("CO")):
        obj_rows.append([key, objectives[key][0], objectives[key][1]])
    lo_fs = 12
    lo_h = card_height(lo[1], WIDE, lo_fs)
    obj_cols = [0.8, 6.6, 1.6]
    obj_fs, obj_rh = 12, 0.38
    while lo_h + 0.16 + table_height(obj_rows, obj_cols, obj_fs, obj_rh) > BOTTOM - TOP and obj_fs > 10:
        obj_fs -= 0.5
    obj_h = table_height(obj_rows, obj_cols, obj_fs, obj_rh)
    lo_note = ("Course outcome %s is drafted and awaiting the owner's approval; the four objectives are "
               "the chapter's own." % lo[0])
    lo_items = [card(LEFT, TOP, WIDE, lo_h, lo[0], lo[1], "orange", lo_fs),
                table(LEFT, TOP + lo_h + 0.16, WIDE, obj_rows, obj_cols, obj_fs, obj_rh)]
    if TOP + lo_h + 0.16 + obj_h + 0.06 + FOOT_H <= BOTTOM + 0.02:
        lo_items.append(dict(t="foot", x=LEFT, y=TOP + lo_h + 0.16 + obj_h + 0.06, w=WIDE, h=FOOT_H,
                             body=lo_note, fs=12))
    slides.append(slide("content", "The outcomes this session serves",
                        "One course outcome, four chapter objectives", lo_items,
                        notes=("Read the course outcome aloud and say which part of it this chapter reaches. The "
                               "chapter's objectives are the page's own and are what the question bank and the mock "
                               "exam are written against. Course outcome %s is recorded as a draft that the course "
                               "owner has not yet approved, so present it as the direction of the course rather than "
                               "as a settled requirement." % lo[0])))

    # ---- 4 the questions the chapter answers ------------------------------------------------------
    if cqs:
        slides.append(slide("content", "The questions this chapter answers",
                            "The chapter's own competency questions",
                            [dict(t="numlist", x=LEFT, y=TOP, w=WIDE, h=3.4,
                                  items=[take(q, 190) for q in cqs[:5]], fs=14)],
                            notes=("These are the competency questions the chapter's ontology was written to answer, "
                                   "so they are a fair statement of what a student should be able to answer at the "
                                   "end. Come back to them in the recap. A student who can answer all of them has the "
                                   "chapter; a student who can answer none of them has memorised vocabulary.")))

    # ---- the branches -----------------------------------------------------------------------------
    for b in branches:
        secs = kids.get(b["id"], [])
        intro = take(facet(b["paras"], "What it is"), 260)
        while text_height(intro, 8.6, 15) > 0.88 and len(sentences(intro)) > 1:
            intro = " ".join(sentences(intro)[:-1])
        while text_height(intro, 8.6, 15) > 0.88 and " " in intro:
            intro = intro.rsplit(" ", 1)[0].rstrip(",;:.") + "\u2026"
            if text_height(intro, 8.6, 15) <= 0.88:
                break
            intro = intro[:-1].rstrip(",;:. ")
        slides.append(slide("section", b["label"], intro,
                            [boxes(LEFT, 3.05, WIDE, 1.5,
                                   [dict(label=s["label"], sub="%d concepts" % len(kids.get(s["id"], [])))
                                    for s in secs], min(4, max(1, len(secs))), fs=12, subfs=9.5)],
                            bg="dark", notes=notes_of(b)))
        for s in secs:
            children = kids.get(s["id"], [])
            how = take(facet(s["paras"], "How it works"), 200)
            el, bx_h, bx_y = [], 0.0, 0.0
            cols_s = rows_s = 0
            if children:
                cols_s = 4 if len(children) > 8 else (3 if len(children) > 4 else len(children))
                rows_s = -(-len(children) // cols_s)
                bw = (WIDE - (cols_s - 1) * 0.16) / cols_s
                box_fs = 11.5 if rows_s >= 3 else 12.5
                row_h = max(0.34, max(text_height(c["label"], bw - 0.20, box_fs) for c in children) + 0.16)
                bx_h = rows_s * row_h + (rows_s - 1) * 0.14
            room = BOTTOM - TOP - (FOOT_H + 0.06 if how else 0.0) - (0.16 + bx_h if children else 0.0)
            body, h = _shrink(take(facet(s["paras"], "What it is"), 620), WIDE, 13, room)
            el.append(card(LEFT, TOP, WIDE, h, "What this section covers", body, "orange", 13))
            if children:
                bx_y = TOP + h + 0.16
                el.append(boxes(LEFT, bx_y, WIDE, max(bx_h, BOTTOM - bx_y - (FOOT_H + 0.06 if how else 0.0)),
                                [dict(label=c["label"], sub=None) for c in children], cols_s,
                                fs=11.5 if rows_s >= 3 else 12.5))
            if how:
                el.append(foot(how))
            slides.append(slide("content", s["label"],
                                "%s - %d concepts" % (b["label"], len(children)), el,
                                notes=notes_of(s, "Concepts in this section: %s."
                                                  % ", ".join(c["label"] for c in children))))
            slides += concept_slides(children, groups, blocks, py, book_ref, shown_programs)

    # ---- recap ------------------------------------------------------------------------------------
    rec = [["Branch", "What to take away"]]
    for b in branches:
        rec.append([b["label"], take(facet(b["paras"], "Why it matters"), 150)])
    rec_cols, rec_fs, rec_note = [1.9, 7.1], 12, (
        "Close the loop with the competency questions: ask the room to answer one of them out loud before "
        "you move to the questions. A recap is the moment to name what was NOT covered as well: every "
        "concept on these slides is explained in the chapter's interactive page in more depth than a "
        "lecture can give it.")
    while table_height(rec, rec_cols, rec_fs, 0.44) > BOTTOM - TOP and rec_fs > 10:
        rec_fs -= 0.5
    chunks, cur = [], [rec[0]]
    for row in rec[1:]:
        if table_height(cur + [row], rec_cols, rec_fs, 0.44) > BOTTOM - TOP and len(cur) > 1:
            chunks.append(cur)
            cur = [rec[0]]
        cur.append(row)
    chunks.append(cur)
    for j, chunk in enumerate(chunks):
        slides.append(slide("content", "Recap" if j == 0 else "Recap, continued",
                            "One sentence for each branch of the chapter",
                            [table(LEFT, TOP, WIDE, chunk, rec_cols, rec_fs, 0.44)], notes=rec_note))

    # ---- discussion -------------------------------------------------------------------------------
    slides.append(slide("content", "Discussion", "Assess what you have so far",
                        [boxes(LEFT, TOP, WIDE, 3.1,
                               [dict(label=h, sub=t) for h, t in discussion], len(discussion),
                               fs=15, subfs=12, accent=[1])],
                        notes="The chapter page carries the same three prompts, so a student who prepared can lead. "
                              "Give each prompt three minutes and take two answers; do not let the first answer "
                              "settle the question."))

    # ---- questions from the bank -------------------------------------------------------------------
    slides += question_slides(bank, by_id, nn)

    # ---- sources ------------------------------------------------------------------------------------
    used = [c for c in citations_used(nodes) if c in pubs]
    lines = []
    for c in used:
        label = pubs[c].replace("(%s)" % c, "").replace("  ", " ").strip(" -\u2013")
        lines.append("%s \u2014 %s" % (c, label))
    per = 9
    for i in range(0, len(lines), per):
        chunk = lines[i:i + per]
        slides.append(slide("content", "Sources" if i == 0 else "Sources, continued",
                            "Every citation on these slides, as the chapter's research record defines it",
                            [dict(t="bullets", x=LEFT, y=TOP, w=WIDE, h=3.3, items=chunk, fs=11),
                             text(LEFT, 4.92, WIDE, 0.3,
                                  "Slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0; this deck is "
                                  "shared under the same licence.", fs=10, italic=True, color="mute")],
                            notes=("The full record, with the saved copy and the checksum of every source, is "
                                   "03-materials/%s. Every quotation in the chapter is re-read from that saved copy "
                                   "by a check the chapter build executes, so a misquotation stops the build."
                                   % cfg["research"])))

    # ---- closing -------------------------------------------------------------------------------------
    slides.append(slide("closing", cfg["nxt"], cfg["nxt_sub"], [], bg="dark",
                        notes="Point at the chapter page once more: it holds the same taxonomy, the same worked "
                              "examples in a playground the student can edit, and the question bank these "
                              "questions came from."))

    plan = dict(meta=dict(chapter=nn, version=ver.replace("_", "."), python=py,
                          title=cfg["title"], sub=cfg["sub"], book=book_ref,
                          concepts=n_leaf, branches=len(branches), examples=n_ex,
                          corpus=cfg["corpus"], outcome=lo[0]),
                slides=slides)
    check(plan)
    out = os.path.join(deck_dir, "deck_plan_v%s.json" % ver)
    json.dump(plan, open(out, "w"), indent=1, ensure_ascii=False)
    print("written %s: %d slides, %d concepts, %d executed examples"
          % (os.path.basename(out), len(slides), n_leaf, n_ex))


# ----------------------------------------------------------------------------------------------------

def concept_slides(children, groups, blocks, py, book_ref, shown):
    """One slide for a concept with a worked example; two small concepts share a slide; a program too
    long for one slide runs on over as many as it needs, each captioned with the lines it shows."""
    out = []
    i = 0
    while i < len(children):
        c = children[i]
        rows = groups.get(c["id"])
        blk = blocks.get(c["id"])
        nxt = children[i + 1] if i + 1 < len(children) else None
        if nxt is not None and _small(c, groups, blocks) and _small(nxt, groups, blocks):
            out.append(_pair_slide(c, nxt, groups, py))
            i += 2
            continue
        if blk:
            out += _prog_slides(c, blk, py, book_ref, shown)
        else:
            out.append(_full_slide(c, rows, None, groups, py, book_ref))
        i += 1
    return out


PROG_LINE = 0.1535          # the height of one 9-point monospaced line, with the house line spacing


def _prog_slides(c, blk, py, book_ref, shown):
    """A worked example whose program needs indented blocks: show the program itself, in order, in as
    many slides as its length needs, and the output beside the last of them. `shown` carries the
    programs already on the deck, so a program that continues an earlier one starts where that one ended."""
    body_full, out_val = blk
    lines = body_full.split("\n")
    size = 9 if max(len(l) for l in lines) > 95 else 10
    step = PROG_LINE * size / 9.0
    start = 0
    for prev in shown:
        common = 0
        for a, b in zip(prev, lines):
            if a != b:
                break
            common += 1
        if common >= 10 and common > start:
            start = common
    shown.append(lines)
    head = take(facet(c["paras"], "What it is"), 380, 1)
    hsize = 12
    dh = card_height(head, WIDE, hsize)
    while dh > 1.55 and len(sentences(head)) > 1:
        head = " ".join(sentences(head)[:-1])
        dh = card_height(head, WIDE, hsize)
    slides_out = []
    pos = start
    first_slide = True
    note = notes_of(c, "Source: %s." % book_ref)
    while pos < len(lines):
        top = TOP + (dh + 0.16 if first_slide else 0.0)
        per = _cpl(WIDE, size)

        def _fit(reserve):
            room = (BOTTOM - top - reserve) - CODE_PAD
            n, used = 0, 0.0
            while pos + n < len(lines):
                need = max(1, -(-len(lines[pos + n]) // per)) * step
                if n >= 4 and used + need > room:
                    break
                used += need
                n += 1
            return max(1, n)

        take_n = _fit(0.26)
        if pos + take_n >= len(lines):          # the last piece also carries the value of result
            take_n = _fit(0.56)
            if pos + take_n < len(lines):
                take_n = _fit(0.26)
        chunk = lines[pos:pos + take_n]
        last = pos + len(chunk) >= len(lines)
        ph = prog_height(chunk, WIDE, size)
        el = []
        if first_slide:
            el.append(card(LEFT, TOP, WIDE, dh, "What it is", head, "orange", hsize))
        cap = ("program %s, lines %d to %d of %d, run under Python %s"
               % (c["id"], pos + 1, pos + len(chunk), len(lines), py))
        el.append(prog(LEFT, top, WIDE, ph, chunk, size, cap,
                       out=out_val if last else None, block=c["id"], first=pos + 1, total=len(lines)))
        if start and first_slide:
            el.append(foot("Lines 1 to %d are the parser already on the slides; only what follows differs."
                           % start))
        title = c["label"] if len(lines) <= take_n + start else "%s (%d of %d)" % (
            c["label"], len(slides_out) + 1, -(-(len(lines) - start) // take_n) if take_n else 1)
        slides_out.append(slide("content", title,
                                (c["leaf"][0] if c["leaf"] and c["leaf"][0] else None) if first_slide else "continued",
                                el, notes=note if first_slide else
                                ("The program continues. " + note)))
        pos += len(chunk)
        first_slide = False
    return slides_out


def _small(c, groups, blocks):
    if c["id"] in blocks:
        return False
    rows = groups.get(c["id"])
    if rows is None:
        return True
    return len(rows) <= 3 and widest(rows) <= 62 and max((len(o) for _, o in rows), default=0) <= 56


def _shrink(body, width, size, room):
    """Drop whole sentences from the end until the paragraph fits the card it is going into."""
    h = card_height(body, width, size)
    while h > room and len(sentences(body)) > 1:
        body = " ".join(sentences(body)[:-1])
        h = card_height(body, width, size)
    return body, h


def _pair_slide(a, b, groups, py):
    el = []
    for c, x, accent in ((a, LEFT, "orange"), (b, COL2_X, "slate")):
        rows = groups.get(c["id"])
        ch = code_height(rows, COL_W, 10.5) + 0.26 if rows else 0.0
        body, h = _shrink(take(facet(c["paras"], "What it is"), 420, 1), COL_W, 12,
                          BOTTOM - TOP - ch - 0.12 - 0.70)
        el.append(card(x, TOP, COL_W, h, c["label"], body, accent, 12))
        y = TOP + h + 0.12
        if rows:
            el.append(code(x, y, COL_W, code_height(rows, COL_W, 10.5), rows, 10.5,
                           "run under Python " + py))
            y += ch
        how = take(facet(c["paras"], "How it works"), 240, 1)
        hh = text_height(how, COL_W, 11) if how else 0
        while how and hh > BOTTOM - y - 0.04 and len(sentences(how)) > 1:
            how = " ".join(sentences(how)[:-1])
            hh = text_height(how, COL_W, 11)
        if how and hh <= BOTTOM - y - 0.04:
            el.append(text(x, y + 0.04, COL_W, hh, how, fs=11, italic=True, color="mute"))
    return slide("content", "%s and %s" % (a["label"], b["label"]), "Two concepts of this section", el,
                 notes=notes_of(a) + "\n\n---\n\n" + notes_of(b))


def _full_slide(c, rows, blk, groups, py, book_ref):
    """A concept with the whole slide to itself: what it is, the example executed, and how it works."""
    label = c["label"]
    sub = c["leaf"][0] if c["leaf"] and c["leaf"][0] else None
    el = []
    if rows:
        ch_size = 11 if widest(rows) <= 90 else (10 if widest(rows) <= 108 else 9)
        ch = code_height(rows, WIDE, ch_size) + 0.26
        body, h = _shrink(take(facet(c["paras"], "What it is"), 600, 1), WIDE, 13,
                          BOTTOM - TOP - ch - 0.32 - 0.80)
        el.append(card(LEFT, TOP, WIDE, h, "What it is", body, "orange", 13))
        y = TOP + h + 0.16
        el.append(code(LEFT, y, WIDE, ch - 0.26, rows, ch_size, "run under Python " + py))
        y += ch
        _tail(el, c, y, "How it works", "How it works", 460)
    else:
        body, h = _shrink(take(facet(c["paras"], "What it is"), 620, 1), WIDE, 13,
                          BOTTOM - TOP - 0.16 - 0.80)
        el.append(card(LEFT, TOP, WIDE, h, "What it is", body, "orange", 13))
        y = TOP + h + 0.16
        if not _tail(el, c, y, "Where you meet it", "Where you meet it", 520):
            _tail(el, c, y, "How it works", "How it works", 520)
    return slide("content", label, sub, el, notes=notes_of(c, "Source: %s." % book_ref))


def _tail(el, c, y, facet_name, head, budget):
    """Fill the room left under the example with the concept's next paragraph, as a card or, if only a
    line is left, as a footnote. Returns True when something was placed."""
    room = BOTTOM - y
    src = facet(c["paras"], facet_name)
    if not src or room < 0.34:
        return False
    body = take(src, budget, 1)
    if room >= 0.80:
        body, h = _shrink(body, WIDE, 12, room)
        if h <= room:
            el.append(card(LEFT, y, WIDE, h, head, body, "slate", 12))
            return True
    body = take(src, 230, 1)
    th = text_height(body, WIDE, 11)
    while th > room - 0.04 and len(sentences(body)) > 1:
        body = " ".join(sentences(body)[:-1])
        th = text_height(body, WIDE, 11)
    if th <= room - 0.04:
        el.append(text(LEFT, y + 0.04, WIDE, th, body, fs=11, italic=True, color="mute"))
        return True
    return False


BANNED = ("all of the above", "none of the above", "both of the above", "any of the above")


def question_slides(bank, by_id, nn):
    """Nine questions from the chapter's own bank, spread over its concepts and its cognitive levels."""
    usable = [q for q in bank
              if q.get("concept") in by_id and not q.get("code")
              and all(not any(b in o.lower() for b in BANNED) for o in q["options"])
              and max(len(o) for o in q["options"]) <= 115 and len(q["q"]) <= 135]
    picked, seen_concept = [], set()
    for level in ("Understand", "Analyze", "Apply", "Remember"):
        for q in usable:
            if len(picked) >= 9:
                break
            if q["level"] == level and q["concept"] not in seen_concept:
                picked.append(q)
                seen_concept.add(q["concept"])
    out = []
    for i in range(0, len(picked), 3):
        chunk = picked[i:i + 3]
        el, y = [], TOP
        for q in chunk:
            el.append(dict(t="question", x=LEFT, y=y, w=WIDE, h=1.12, q=q["q"],
                           options=q["options"], fs=12.5))
            y += 1.20
        answers = "  ".join("(%d) %s - %s" % (j + 1 + i, chr(65 + q["answer"]), q["why"]) for j, q in enumerate(chunk))
        out.append(slide("content", "Check yourself" if i == 0 else "Check yourself, continued",
                         "From the chapter's own question bank", el,
                         notes="Answers. " + answers + "\n\nEvery option here is a statement the chapter can "
                               "judge: there is no filler option, so a student who guesses has to choose between "
                               "four claims about Bitcoin and defend one."))
    return out


# ----------------------------------------------------------------------------------------------------

def check(plan):
    """Refuse a plan whose boxes leave the frame, whose text does not fit, or whose content slide has no notes."""
    bad = []
    for i, s in enumerate(plan["slides"], 1):
        if s["kind"] == "section" and text_height(s["sub"], 8.6, 15) > 0.90:
            bad.append((i, s.get("title"), "the branch's opening sentences do not fit the divider"))
        if s["kind"] in ("content", "section") and len(s.get("notes", "")) < 40:
            bad.append((i, s.get("title"), "speaker notes missing or too short"))
        for el in s["items"]:
            x, y, w, h = el.get("x", 0), el.get("y", 0), el.get("w", 0), el.get("h", 0)
            if x < 0.3 or x + w > 9.72 or y < 1.0 or y + h > 5.30:
                bad.append((i, s.get("title"), "%s box leaves the frame: x=%.2f y=%.2f w=%.2f h=%.2f"
                            % (el["t"], x, y, w, h)))
            if el["t"] == "card" and card_height(el["body"], w, el["fs"]) > h + 0.02:
                bad.append((i, s.get("title"), "card text overflows: needs %.2f has %.2f"
                            % (card_height(el["body"], w, el["fs"]), h)))
            if el["t"] == "code" and code_height(el["rows"], w, el["fs"]) > h + 0.02:
                bad.append((i, s.get("title"), "code overflows"))
            if el["t"] == "prog" and prog_height(el["lines"], w, el["fs"]) > h + 0.02:
                bad.append((i, s.get("title"), "program overflows"))
            if el["t"] == "boxes":
                for it in el["items"]:
                    need = text_height(it["label"], el["bw"] - 0.20, el["fs"])
                    if it.get("sub"):
                        need += text_height(it["sub"], el["bw"] - 0.20, el["subfs"])
                    if need > el["bh"] - 0.10:
                        bad.append((i, s.get("title"), "box %r overflows: needs %.2f has %.2f"
                                    % (it["label"], need, el["bh"] - 0.10)))
            if el["t"] == "table":
                th = table_height(el["rows"], el["colW"], el["fs"], el["rowH"])
                if y + th > BOTTOM + 0.04:
                    bad.append((i, s.get("title"), "the table runs past the frame: %.2f in from y=%.2f"
                                % (th, y)))
                for other in s["items"]:
                    if other is not el and other.get("y", 0) >= y and other["y"] < y + th - 0.02:
                        bad.append((i, s.get("title"), "a %s box overlaps the table" % other["t"]))
            if el["t"] == "foot" and text_height(el["body"], w, el["fs"]) > h + 0.02:
                bad.append((i, s.get("title"), "footnote overflows"))
            if el["t"] == "text" and text_height(el["body"], w, el["fs"]) > h + 0.02:
                bad.append((i, s.get("title"), "text overflows: needs %.2f has %.2f"
                            % (text_height(el["body"], w, el["fs"]), h)))
    if bad:
        for b in bad[:60]:
            print("  PLAN REFUSED slide %d %r: %s" % b)
        raise SystemExit("%d layout problem(s); nothing written" % len(bad))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
