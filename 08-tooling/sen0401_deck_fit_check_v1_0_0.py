#!/usr/bin/env python3
"""sen0401_deck_fit_check v1.0.0 - port of SEN0414's deck_fit_check_v1_0_0.py, code unchanged (SEN0401 has deck_layout_check and deck_notes_check as byte-identical copies, but never had this one).
Refuses a deck whose text does not fit the box it was put in, whose text boxes print on top of one another, or
whose content slide carries no speaker notes. The deck is re-opened from the finished file and every text frame re-measured, independently of the
renderer that wrote it: for each frame the text is wrapped greedily at the frame's own width using the average advance
width of its font at its own size, the resulting line count is turned back into a height, and the frame is refused
when that height is more than the frame's height plus a tolerance. Monospaced text is measured at its exact advance
width, so a code box that overflows cannot pass.

Measurement is an estimate, deliberately a pessimistic one: the average advance used for the proportional faces is
wider than the real average of English prose, so the check errs towards refusing a frame that would in fact fit.
Usage: deck_fit_check_v1_0_0.py <deck.pptx> [tolerance-inches, default 0.06]"""
__version__ = "1.0.0"
import math
import sys
from pptx import Presentation
from pptx.util import Emu

EM = {"Calibri": 0.50, "Cambria": 0.52, "Courier New": 0.60}
DEFAULT_EM = 0.52
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def wrap_lines(text, w_in, size, face):
    cw = EM.get(face, DEFAULT_EM) * size / 72.0
    per = max(1, int(w_in / cw))
    lines = 0
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines += 1
            continue
        cur, n = 0, 1
        for word in words:
            add = len(word) + 1 if cur else len(word)
            if cur + add > per and cur > 0:
                n += 1
                cur = len(word)
            else:
                cur += add
        lines += n
    return lines


def main():
    path = sys.argv[1]
    tol = float(sys.argv[2]) if len(sys.argv) > 2 else 0.06
    pres = Presentation(path)
    over, no_notes, overlaps, frames, shrink = [], [], [], 0, 0
    for i, slide in enumerate(pres.slides, 1):
        has_text = False
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            tf = shape.text_frame
            text = tf.text
            if not text.strip():
                continue
            has_text = True
            frames += 1
            if tf._bodyPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}normAutofit") is not None:
                shrink += 1
                continue                                   # PowerPoint shrinks these itself
            w_in = Emu(shape.width).inches
            h_in = Emu(shape.height).inches
            # per-paragraph measurement, each at its own largest run size, its own first named face, and the
            # line spacing and space-after the file itself records for it
            total, paras, gaps, last_after = 0.0, 0, 0, 0.0
            for para in tf.paragraphs:
                runs = [r for r in para.runs if r.text]
                after = 0.0
                ppr = para._p.find(A + "pPr")
                if ppr is not None:
                    spc = ppr.find(A + "spcAft")
                    if spc is not None:
                        pts = spc.find(A + "spcPts")
                        if pts is not None:
                            after = int(pts.get("val")) / 100.0 / 72.0
                if not runs:
                    total += 0.08
                    last_after = after
                    paras += 1
                    gaps += 1
                    continue
                size = max((r.font.size.pt for r in runs if r.font.size), default=18.0)
                face = next((r.font.name for r in runs if r.font.name), "Calibri")
                lh = size * 1.21 / 72.0
                exact = False
                if ppr is not None:
                    lns = ppr.find(A + "lnSpc")
                    if lns is not None:
                        pts = lns.find(A + "spcPts")
                        if pts is not None:
                            lh = int(pts.get("val")) / 100.0 / 72.0
                            exact = True
                line = "".join(r.text for r in runs)
                total += wrap_lines(line, max(0.2, w_in - 0.04), size, face) * lh
                total += last_after
                last_after = after
                # a paragraph whose line spacing the file states exactly takes exactly that; only the paragraphs
                # whose spacing PowerPoint works out for itself get the small allowance
                if not exact:
                    gaps += 1
                paras += 1
            total += 0.02 * max(0, gaps - 1)
            if total > h_in + tol:
                over.append((i, round(total, 2), round(h_in, 2), text.replace("\n", " ")[:70]))
        if has_text and not (slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip()):
            no_notes.append(i)
        # two text frames that overlap each other print on top of each other, which no measurement of one frame
        # alone can catch, so the frames of each slide are compared with one another as well
        boxes = []
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text_frame.text.strip():
                boxes.append((Emu(shape.left).inches, Emu(shape.top).inches,
                              Emu(shape.width).inches, Emu(shape.height).inches, shape.text_frame.text.replace("\n", " ")[:40]))
        for p in range(len(boxes)):
            for q in range(p + 1, len(boxes)):
                a1, b1, w1, h1, t1 = boxes[p]
                a2, b2, w2, h2, t2 = boxes[q]
                ow = min(a1 + w1, a2 + w2) - max(a1, a2)
                oh = min(b1 + h1, b2 + h2) - max(b1, b2)
                if ow > 0.05 and oh > 0.05:
                    overlaps.append((i, round(ow * oh, 2), t1, t2))
    print("%d slides, %d text frames measured (%d left to PowerPoint's own shrink-to-fit); "
          "%d frame(s) overflowing by more than %.2f in; %d pair(s) of text frames overlapping; "
          "%d slide(s) with text but no speaker notes"
          % (len(pres.slides._sldIdLst), frames, shrink, len(over), tol, len(overlaps), len(no_notes)))
    for o in over[:25]:
        print("  REFUSED slide %d: text needs %.2f in, box is %.2f in - %s" % o)
    for o in overlaps[:25]:
        print("  REFUSED slide %d: two text frames overlap over %.2f sq in - '%s' and '%s'" % o)
    if no_notes:
        print("  REFUSED slides with no notes:", no_notes[:25])
    sys.exit(1 if (over or overlaps or no_notes) else 0)


if __name__ == "__main__":
    main()
