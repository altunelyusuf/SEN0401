#!/usr/bin/env python3
"""sen0401_deck_group v1.0.0 - post-render step of the deck builders (owner ruling of 2026-11-14: something to look at on every slide). On a slide that has no picture, chart, table, group or code frame, every card
(a rectangle of 0.5 to 9 in by 0.3 to 4 in) is turned into one GROUP together with the text boxes and shapes whose centre lies inside it, so the card moves and is edited as one object and counts as a visual.
Usage: python3 sen0401_deck_group_v1_0_0.py IN.pptx OUT.pptx"""
import sys
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
E = 914400


def has_visual(s):
    for sh in s.shapes:
        if sh.shape_type in (T.PICTURE, T.CHART, T.TABLE, T.GROUP): return True
        if sh.has_text_frame and any(r.font.name == 'Courier New' for p in sh.text_frame.paragraphs for r in p.runs): return True
    return False


def main(src, dst):
    prs = Presentation(src); made = 0; slides = []
    for i, s in enumerate(prs.slides, 1):
        if has_visual(s): continue
        shapes = list(s.shapes)
        cards = [x for x in shapes if x.shape_type == T.AUTO_SHAPE and 0.5 * E < x.width < 9 * E and 0.3 * E < x.height < 4 * E]
        used = set(); n = 0
        for c in sorted(cards, key=lambda x: -x.width * x.height):
            if id(c._element) in used: continue
            inside = [x for x in shapes if x is not c and id(x._element) not in used and x.left is not None
                      and c.left <= x.left + x.width // 2 <= c.left + c.width and c.top <= x.top + x.height // 2 <= c.top + c.height
                      and x.width < c.width * 1.01]
            if not inside: continue
            members = [c] + inside
            g = s.shapes.add_group_shape(shapes=members); g.name = "Card"
            for m in members: used.add(id(m._element))
            n += 1
        if n: made += n; slides.append(i)
    prs.save(dst); print("grouped %d cards on slides %s" % (made, slides))


if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
