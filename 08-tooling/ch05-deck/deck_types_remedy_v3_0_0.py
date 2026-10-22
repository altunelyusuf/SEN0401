#!/usr/bin/env python3
"""Chapter 5 deck v3.0.0 - the slide types built on the drawing kit: title, divider, analogy table, 5N1K story, concept cards."""
__version__ = "3.0.0"
from deck_kit_remedy_v3_0_0 import *


def title_slide(title, sub, line, picture_file, cap, notes, src):
    s = new_slide(title, None, src, notes, chip=False)
    t = s.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.6), Inches(1.0), Inches(5.2), Inches(1.5)
    t.text_frame.paragraphs[0].runs[0].font.size = Pt(34)
    band = card(s, 0.6, 0.55, 0.9, 0.12, C["orange"], "accent")
    tb(s, 0.6, 2.6, 5.2, 0.9, sub, 18, C["slate"], italic=True, name="subtitle")
    tb(s, 0.6, 3.75, 5.2, 0.75, line, 12, C["mute"], name="course line")
    picture(s, picture_file, 6.0, 0.7, 3.5, 3.9, cap)
    return s


def divider(title, sub, items, flow_labels, notes, src, hot=()):
    """one divider (no brand chip): each concept as a short name pill plus one line of meaning, and one native table as the visual"""
    s = new_slide(title, sub, src, notes, chip=False)
    t = s.shapes.title
    t.left, t.width = Inches(0.5), Inches(9.0)
    for sh in s.shapes:
        if sh.name == "subtitle":
            sh.left, sh.width = Inches(0.5), Inches(9.0)
    n = len(items)
    h = min(0.55, 3.5 / n - 0.05)
    y0 = 1.3
    for i, (name, meaning) in enumerate(items):
        assert len(name.split()) <= 4 and len(meaning.split()) >= 5, (name, meaning)
        y = y0 + i * (h + 0.05)
        card(s, 0.5, y, 5.95, h, C["card"], "concept row")
        card(s, 0.5, y, 0.07, h, C["orange"], "concept accent")
        tb(s, 0.65, y, 1.75, h, name, 11.5, C["dark"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="concept")
        tb(s, 2.4, y, 4.0, h, meaning, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="concept meaning")
    rows = [["How they fit together"]] + [["%d.  %s" % (k + 1, lab)] for k, lab in enumerate(flow_labels)]
    table(s, 6.75, 1.3, 2.75, rows, [1], 11.5, min(0.5, 3.5 / len(rows)), name="visual: how the concepts fit")
    return s


def analogy_slide(title, sub, rows, notes, src, take=None):
    """rows: (concept label, everyday analogy, what it is in the wallet)"""
    s = new_slide(title, sub, src, notes)
    data = [["Concept", "In everyday life", "In the wallet"]] + [list(r) for r in rows]
    rh = min(0.5, 3.6 / len(data))
    table(s, 0.5, 1.3, 9.0, data, [2.2, 3.5, 3.3], 11.5, rh, name="analogy table", bold_first=True)
    if take:
        takeaway(s, take)
    return s


def story_slide(sid, rows, notes, linktext=None):
    """5N1K: who, what, when, where, why, how; a real picture, a credit, a live link. rows[2] is (date, rest): the date is its own run."""
    st = STORY_DATA[sid]
    s = new_slide(st["title"], "A true story, told as who, what, when, where, why and how", None, notes)
    pw = 3.3
    picture(s, st["photo"], 0.5, 1.28, pw, 3.4, st["credit"])
    labels = ["WHO", "WHAT", "WHEN", "WHERE", "WHY", "HOW"]
    y = 1.26
    rh = 0.5
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    for lab, txt in zip(labels, rows):
        card(s, 3.95, y, 5.55, rh, C["card"], "5N1K row")
        tb(s, 4.02, y, 0.8, rh, lab, 12, C["orange"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="5N1K label")
        body = [[(txt[0], {"bold": True, "color": C["slate"]}), (txt[1], {})]] if isinstance(txt, tuple) else txt
        tb(s, 4.8, y, 4.65, rh, body, 11, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="5N1K text")
        y += rh + 0.04
    tb(s, 3.95, y + 0.02, 5.55, 0.3, [[("READ  ", {"bold": True, "color": C["orange"]}), (st["linkLabel"], {"link": st["link"], "color": C["slate"], "bold": True}), ("   " + host, {"color": C["mute"], "size": 10.5})]], 12, name="live link")
    takeaway(s, st["lesson"], 4.9)
    return s


def cards(s, items, x, y, w, h, cols=2, fs=12, gap=0.12, head_color=None):
    """items: (heading, body) cards in a grid"""
    n = len(items); rows = math.ceil(n / cols)
    bw = (w - (cols - 1) * gap) / cols; bh = (h - (rows - 1) * gap) / rows
    for i, (hd, body) in enumerate(items):
        r, c = divmod(i, cols)
        cx, cy = x + c * (bw + gap), y + r * (bh + gap)
        card(s, cx, cy, bw, bh, C["card"], "card")
        tb(s, cx + 0.1, cy + 0.05, bw - 0.2, 0.3, hd, fs + 1, head_color or C["orange"], bold=True, name="card heading", font=HF)
        tb(s, cx + 0.1, cy + 0.36, bw - 0.2, bh - 0.4, body, fs, C["ink"], name="card text")


STORY_DATA = STORY
