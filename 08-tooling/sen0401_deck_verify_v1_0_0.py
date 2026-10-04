#!/usr/bin/env python3
"""Opens a finished lecture deck with python-pptx and checks what the plan promised is really in the file.

Checked: the file opens; the page is the house 10 x 5.625 inch widescreen page; the slide count equals the
plan's; every shape lies inside the page; every slide that carries content carries speaker notes, in whole
sentences; every slide of the plan has its title on the matching slide of the file; and no run of text is
longer than the box it sits in can hold at its own point size (the same estimate the plan builder used, so
a slide that would overflow its frame is reported rather than shipped).

Usage: sen0401_deck_verify_v1_0_0.py <deck.pptx> <deck_plan_v*.json>
"""
__version__ = "1.0.0"

import json
import os
import sys

from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sen0401_deck_lib_v1_0_0 import text_height  # noqa: E402

EMU = 914400.0


def main(deck, plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    pres = Presentation(deck)
    bad, notes_missing, w, h = [], 0, pres.slide_width / EMU, pres.slide_height / EMU
    if abs(w - 10.0) > 0.01 or abs(h - 5.625) > 0.01:
        bad.append("page is %.3f x %.3f inches, not the house 10 x 5.625" % (w, h))
    if len(pres.slides) != len(plan["slides"]):
        bad.append("%d slides in the file, %d in the plan" % (len(pres.slides), len(plan["slides"])))
    for i, (s, p) in enumerate(zip(pres.slides, plan["slides"]), 1):
        for sh in s.shapes:
            if sh.left is None:
                continue
            x, y = sh.left / EMU, sh.top / EMU
            sw = (sh.width or 0) / EMU
            sh_h = (sh.height or 0) / EMU
            if x < -0.01 or y < -0.01 or x + sw > w + 0.01 or y + sh_h > h + 0.01:
                bad.append("slide %d: a shape leaves the page (x=%.2f y=%.2f w=%.2f h=%.2f)" % (i, x, y, sw, sh_h))
            if not sh.has_text_frame:
                continue
            for para in sh.text_frame.paragraphs:
                size = next((r.font.size.pt for r in para.runs if r.font.size), None)
                if size is None:
                    continue
                txt = "".join(r.text for r in para.runs)
                if txt and text_height(txt, max(0.2, sw - 0.2), size) > sh_h + 0.30:
                    bad.append("slide %d: %r does not fit its box (%.2f in needed, %.2f in high)"
                               % (i, txt[:60], text_height(txt, max(0.2, sw - 0.2), size), sh_h))
        note = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
        if p["kind"] in ("content", "section"):
            if len(note) < 40:
                notes_missing += 1
                bad.append("slide %d (%s): speaker notes missing or too short" % (i, p.get("title")))
            elif "." not in note:
                bad.append("slide %d (%s): speaker notes are not sentences" % (i, p.get("title")))
        if p.get("title"):
            flat = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
            if p["title"] not in flat:
                bad.append("slide %d: the plan's title %r is not on the slide" % (i, p["title"]))
    kinds = {}
    for p in plan["slides"]:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    print("%s: %d slides %s, page %.2f x %.3f in, notes on %d of %d content slides"
          % (os.path.basename(deck), len(pres.slides), kinds, w, h,
             kinds.get("content", 0) + kinds.get("section", 0) - notes_missing,
             kinds.get("content", 0) + kinds.get("section", 0)))
    for b in bad[:40]:
        print("  REFUSED", b)
    if len(bad) > 40:
        print("  ... and %d more" % (len(bad) - 40))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
