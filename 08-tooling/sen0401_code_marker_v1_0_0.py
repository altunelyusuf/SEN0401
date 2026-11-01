#!/usr/bin/env python3
"""sen0401_code_marker v1.0.0 - THE ONE PLACE where the marker of a slide code box and of a result line is defined (task TK_Code_Gate_Build, owner's word relayed 2026-10-30:
slide code without the prompts '>>> ' and '... ', the result shown apart). The successor checks (sen0401_deck_check v1.2.0, sen0401_deck_standard_check v1.3.0,
sen0401_lineage_chapter_check v1.5.0 through the deck check, sen0401_chbuild v1.4.0) import this file and define nothing of their own.

THE MARKER (stated once, both forms accepted)
  FORM 1, with prompts (the form of the committed decks, unchanged): a code box is a text box with a paragraph that starts with '>>> '; the line after a '>>> ' row is its result.
  FORM 2, without prompts (the form of the chapter 6 deck v2_3_0, built on Friday 2026-10-30):
    code box    : a shape with text whose NAME starts with 'code' (e.g. 'code 1'; several code shapes of one slide are read top to bottom, left to right, joined by line breaks
                  into ONE listing, which is run once, in the slide's fresh namespace after the chapter prelude);
    result line : a shape with text whose NAME starts with 'result' AND whose text reads 'EXPRESSION  ->  VALUE' (the expression, two spaces, the arrow U+2192, two spaces, the value),
                  placed directly under the code boxes (its top is not above the bottom of the lowest code box, 0.05 inch of slack); the check evaluates EXPRESSION in the namespace
                  the listing left and VALUE must equal repr() of what Python answers. Any other shape whose name starts with 'result' (a frame, a header, a label) carries no
                  arrow and is decoration: it is not compared.
A deck with neither form is a deck without examples (0 examples re-run)."""
__version__ = "1.0.0"
from xml.dom import minidom

CODE_PREFIX = "code"
RESULT_PREFIX = "result"
ARROW = "  →  "
PROMPT_INPUT = ">>> "
PROMPT_MORE = "... "
UNDER_SLACK_EMU = 45720          # 0.05 inch


def is_code_name(name):
    return (name or "").startswith(CODE_PREFIX)


def is_result_name(name):
    return (name or "").startswith(RESULT_PREFIX)


def split_result(text):
    """'EXPR  ->  VALUE' -> (EXPR, VALUE); None when the text has no arrow."""
    if ARROW in text:
        e, v = text.split(ARROW, 1)
        return e, v
    return None


def xml_shapes(dom):
    """Every p:sp of a parsed slide (groups included): dicts name, top, left, height, paras (one string per a:p)."""
    out = []
    for sp in dom.getElementsByTagName("p:sp"):
        nm = ""
        for c in sp.getElementsByTagName("p:cNvPr"):
            nm = c.getAttribute("name"); break
        top = left = height = 0
        for x in sp.getElementsByTagName("a:xfrm"):
            o = x.getElementsByTagName("a:off"); e = x.getElementsByTagName("a:ext")
            if o and e:
                left, top, height = int(o[0].getAttribute("x") or 0), int(o[0].getAttribute("y") or 0), int(e[0].getAttribute("cy") or 0)
            break
        paras = ["".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in sp.getElementsByTagName("a:p")]
        out.append({"name": nm, "top": top, "left": left, "height": height, "paras": paras})
    return out


def form2(shapes):
    """From a slide's shapes (xml_shapes) -> (listing, rows). listing = the code shapes' lines joined by line breaks ('' when none);
    rows = [(expression, value, under)] of the result lines, top to bottom; under = the row is not above the lowest code box."""
    codes = sorted((s for s in shapes if is_code_name(s["name"]) and "".join(s["paras"]).strip()), key=lambda s: (s["top"], s["left"]))
    listing = "\n".join(p for s in codes for p in s["paras"])
    bottom = max((s["top"] + s["height"] for s in codes), default=0)
    rows = []
    for s in sorted((s for s in shapes if is_result_name(s["name"])), key=lambda s: (s["top"], s["left"])):
        r = split_result("\n".join(s["paras"]))
        if r:
            rows.append((r[0], r[1], s["top"] >= bottom - UNDER_SLACK_EMU))
    return listing, rows


def pptx_shapes(slide):
    """The same dicts from a python-pptx slide (used by the builder reader)."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    def walk(shs):
        for sh in shs:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from walk(sh.shapes)
            else:
                yield sh
    return [{"name": sh.name, "top": sh.top or 0, "left": sh.left or 0, "height": sh.height or 0,
             "paras": ["".join(r.text for r in p.runs) for p in sh.text_frame.paragraphs]} for sh in walk(slide.shapes) if sh.has_text_frame]
