#!/usr/bin/env python3
"""sen0401_deck_code_indent_check v1.0.1 (over v1.0.0: the code boxes of a slide are read as ONE listing in slide order, so a compound statement split over code boxes is judged whole; task TK_Deck_Checks_Build, owner 2026-10-30: Python source on slides indented as Python requires). Reads a deck (.pptx) and checks every code line of every code box
(both forms: prompts, or a shape named code...): the body of a compound statement (for, while, if, elif, else, def, class, with, try, except, finally, match, case) stands on its own line(s) below its header and is
indented four spaces more than the header; no body stands on the header line; a continuation line inside brackets is indented more than the line that opened the bracket (a line that only closes a bracket may stand level).
Prints one line per finding ('FINDING slide N box NAME line K: reason') and a COUNTS line, then 'VERDICT: PASS' or 'VERDICT: FAIL'. Exit 0 on PASS, 1 on FAIL, 2 when the deck cannot be read.
Usage: sen0401_deck_code_indent_check_v1_0_1.py DECK.pptx"""
__version__ = "1.0.1"
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_deck_code_read_v1_0_1 as RD


def main(argv):
    if len(argv) != 1:
        print(__doc__); return 2
    try:
        slides = RD.decks_slides(argv[0])
    except Exception as e:
        print("VERDICT: CANNOT_RUN %s" % e); return 2
    boxes = lines_n = indented = compounds = nf = 0
    print("sen0401_deck_code_indent_check %s | %s | %d slides" % (__version__, os.path.basename(argv[0]), len(slides)))
    for i, s in enumerate(slides, 1):
        boxes += len(RD.code_boxes(s))
        pairs = RD.slide_listing(s)
        texts = [t for _, t in pairs]
        f, oc, ind = RD.indent_findings(texts)
        lines_n += sum(1 for t in texts if t.strip()); compounds += oc; indented += ind
        for no, why in f:
            nf += 1; print("FINDING slide %d box '%s' line %d: %s" % (i, pairs[no - 1][0], no, why))
    print("COUNTS code_boxes=%d code_lines=%d lines_with_leading_indentation=%d one_line_compounds=%d findings=%d" % (boxes, lines_n, indented, compounds, nf))
    print("VERDICT: %s" % ("PASS" if nf == 0 else "FAIL"))
    return 0 if nf == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
