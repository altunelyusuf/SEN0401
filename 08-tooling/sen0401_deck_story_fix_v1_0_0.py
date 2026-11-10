#!/usr/bin/env python3
"""sen0401_deck_story_fix v1.0.0 - applies the Ch7/8 D5 fix (owner's ruling 2026-11-09, commit 0278076) to a deck
that already has story slides built with the OLD pattern: four beat text boxes labelled WHAT:/WHY:/HOW:/SO WHAT:,
and a factrow of WHO/WHERE/WHEN/READ chips. For each story slide this script:
  - rewrites the WHAT/WHY/HOW beat text boxes into label-free narrative sentences (supplied by the caller),
    renames each to 'Story Text N' and tags it with its 5N1K coverage via the shape's alt-text/description
    (p:cNvPr/@descr), per sen0401_story_marker_v1_0_0.py - the union of the three must cover all six of
    who/what/when/where/why/how.
  - rewrites the SO WHAT beat into a label-free plain sentence (left as an ordinary, un-named text box).
  - deletes the WHO/WHERE/WHEN chip-and-text shape pairs (visible on-screen labels banned by D5 v2.0.0) and
    widens/repositions the surviving READ chip-and-text pair to span the freed row ('READ' is not a 5N1K word
    and stays, per the marker module).
Nothing else on the slide (picture, title, sub-title, link) is touched.
"""
__version__ = "1.0.0"
import sys
from pptx import Presentation
from pptx.util import Inches

LABELS = ("WHAT:", "WHY:", "HOW:", "SO WHAT:")
CHIP_LABELS = ("WHO", "WHERE", "WHEN", "READ")


def shape_text(sh):
    return sh.text_frame.text if sh.has_text_frame else ""


def set_descr(shape, tags):
    shape._element.nvSpPr.cNvPr.set("descr", " ".join(sorted(tags)))


def rewrite_beat(shape, new_text, name=None, tags=None):
    tf = shape.text_frame
    p = tf.paragraphs[0]
    # keep the first run's formatting, drop any extra runs/paragraphs
    r0 = p.runs[0]
    r0.text = new_text
    for r in list(p.runs[1:]):
        r._r.getparent().remove(r._r)
    for extra in list(tf.paragraphs[1:]):
        extra._p.getparent().remove(extra._p)
    if name:
        shape.name = name
    if tags:
        set_descr(shape, tags)


def find_beat_shapes(slide):
    out = {}
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        t = shape_text(sh)
        for lab in LABELS:
            if t.startswith(lab):
                out[lab] = sh
    missing = [l for l in LABELS if l not in out]
    if missing:
        raise SystemExit("REFUSED: beat labels not found: %s" % missing)
    return out


def find_chip_shapes(slide):
    """Return {label: (rect_shape, text_shape)} for WHO/WHERE/WHEN/READ."""
    texts = {}
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        t = shape_text(sh)
        for lab in CHIP_LABELS:
            if t.startswith(lab):
                texts[lab] = sh
    missing = [l for l in CHIP_LABELS if l not in texts]
    if missing:
        raise SystemExit("REFUSED: chip labels not found: %s" % missing)
    out = {}
    for lab, tsh in texts.items():
        ty = tsh.top
        best = None
        for sh in slide.shapes:
            if sh is tsh or sh.has_text_frame and shape_text(sh).startswith(CHIP_LABELS):
                continue
            if sh.shape_type is None:
                continue
            if abs(sh.top - ty) < Inches(0.05) and sh.left <= tsh.left and sh.left > tsh.left - Inches(0.3):
                best = sh
        if best is None:
            raise SystemExit("REFUSED: no chip rectangle found for %s" % lab)
        out[lab] = (best, tsh)
    return out


def fix_slide(slide, beats, so_what_text):
    """beats: dict WHAT:/WHY:/HOW: -> (new_text, tags-set)"""
    bshapes = find_beat_shapes(slide)
    order = {"WHAT:": 1, "WHY:": 2, "HOW:": 3}
    for lab, (new_text, tags) in beats.items():
        rewrite_beat(bshapes[lab], new_text, name="Story Text %d" % order[lab], tags=tags)
    rewrite_beat(bshapes["SO WHAT:"], so_what_text)

    chips = find_chip_shapes(slide)
    rects = {lab: chips[lab][0] for lab in CHIP_LABELS}
    left0 = min(r.left for r in rects.values())
    right0 = max(r.left + r.width for r in rects.values())
    for lab in ("WHO", "WHERE", "WHEN"):
        rect, txt = chips[lab]
        rect._element.getparent().remove(rect._element)
        txt._element.getparent().remove(txt._element)
    read_rect, read_txt = chips["READ"]
    new_w = right0 - left0
    read_rect.left = left0
    read_rect.width = new_w
    read_txt.left = left0 + Inches(0.1)
    read_txt.width = new_w - Inches(0.16)


def run(pptx_in, pptx_out, slide_fixes):
    """slide_fixes: {slide_index(0-based): (beats_dict, so_what_text)}"""
    prs = Presentation(pptx_in)
    for idx, (beats, so_what) in slide_fixes.items():
        fix_slide(prs.slides[idx], beats, so_what)
    prs.save(pptx_out)
    print("written", pptx_out)


if __name__ == "__main__":
    raise SystemExit("import this module from a per-chapter driver; it defines no CLI of its own")
