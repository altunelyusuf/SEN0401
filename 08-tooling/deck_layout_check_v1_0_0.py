"""Layout and completeness check for the SEN0401 lecture decks: it opens a finished .pptx with python-pptx and,
for every text frame, estimates how tall the text will set and compares that with the frame it was given, so that a
slide that overflows is found before a class sees it. It also reports slides without speaker notes and any text that
runs outside the slide.

The estimate is deliberately pessimistic. Line width is taken as the average advance of the font at its size
(0.60 of the size for Courier New, which is monospaced, 0.50 for Cambria and 0.48 for Calibri), a line is 1.22 times
the size, and a paragraph takes at least one line. A frame is reported when the estimate exceeds its height, and the
report says by how much, so a borderline case can be judged rather than merely flagged.
Usage: deck_layout_check_v1_0_0.py <deck.pptx> [first-content-slide-number]
"""
__version__ = "1.0.0"
import math, sys
from pptx import Presentation
from pptx.util import Emu

WIDTH = {"Courier New": 0.60, "Cambria": 0.50, "Calibri": 0.48}
LINE = 1.22


def frames(slide):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            yield sh


def estimate(sh, default_size=13.0, default_font="Calibri"):
    w_pt = Emu(sh.width).pt
    h_pt = Emu(sh.height).pt
    total = 0.0
    for p in sh.text_frame.paragraphs:
        runs = p.runs
        if not runs:
            continue
        size = max([(r.font.size.pt if r.font.size else default_size) for r in runs])
        face = next((r.font.name for r in runs if r.font.name), default_font)
        adv = WIDTH.get(face, 0.48) * size
        text = "".join(r.text for r in runs)
        per = max(1, int((w_pt - 4) / adv))
        total += max(1, math.ceil(len(text) / per)) * size * LINE
    return total, h_pt, w_pt


def main(path, first_content=2):
    pres = Presentation(path)
    sw, sh_ = Emu(pres.slide_width).inches, Emu(pres.slide_height).inches
    over, outside, nonotes = [], [], []
    for i, slide in enumerate(pres.slides, 1):
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        if not notes:
            nonotes.append(i)
        for shp in frames(slide):
            need, have, _ = estimate(shp)
            if need > have + 0.5:
                over.append((i, shp.text_frame.text[:60].replace("\n", " "), round(need, 1), round(have, 1)))
            x, y = Emu(shp.left).inches, Emu(shp.top).inches
            if x < -0.01 or y < -0.01 or x + Emu(shp.width).inches > sw + 0.01 or y + Emu(shp.height).inches > sh_ + 0.01:
                outside.append((i, shp.text_frame.text[:40].replace("\n", " "),
                                round(x, 2), round(y, 2), round(x + Emu(shp.width).inches, 2), round(y + Emu(shp.height).inches, 2)))
    print("%s: %d slides, %.2f x %.2f in" % (path.rsplit("/", 1)[-1], len(pres.slides._sldIdLst), sw, sh_))
    print("  text frames estimated to overflow their box: %d" % len(over))
    for o in over:
        print("    slide %-3d  needs %6.1f pt in %6.1f pt  %r" % (o[0], o[2], o[3], o[1]))
    print("  shapes reaching outside the slide: %d" % len(outside))
    for o in outside:
        print("    slide %-3d  %r  x %.2f..%.2f  y %.2f..%.2f" % (o[0], o[1], o[2], o[4], o[3], o[5]))
    print("  slides without speaker notes: %s" % (nonotes if nonotes else "none"))
    bad = len(over) + len(outside) + len([n for n in nonotes if n >= first_content])
    print("  RESULT:", "clean" if bad == 0 else "%d item(s) to look at" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2))
