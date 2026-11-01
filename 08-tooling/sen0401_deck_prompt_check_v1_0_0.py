#!/usr/bin/env python3
"""sen0401_deck_prompt_check v1.0.0 (task TK_Deck_Checks_Build, owner 2026-10-30: no '>>>' prompts on the slides). Reads a deck (.pptx); no line of a code box (both forms: a text shape with a paragraph that starts
with '>>> ', or a shape named code...) begins with the prompt '>>> ' or '... ' (a bare '>>>' counts too; in a box that holds prompts a bare '...' continuation row counts). A deck without any code box passes.
Prints 'FINDING slide N box NAME: text' per finding, a COUNTS line, then 'VERDICT: PASS' or 'VERDICT: FAIL'. Exit 0 PASS, 1 FAIL, 2 cannot read.
Usage: sen0401_deck_prompt_check_v1_0_0.py DECK.pptx"""
__version__ = "1.0.0"
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_deck_code_read_v1_0_0 as RD


def main(argv):
    if len(argv) != 1:
        print(__doc__); return 2
    try:
        slides = RD.decks_slides(argv[0])
    except Exception as e:
        print("VERDICT: CANNOT_RUN %s" % e); return 2
    boxes = rows = nf = 0
    print("sen0401_deck_prompt_check %s | %s | %d slides" % (__version__, os.path.basename(argv[0]), len(slides)))
    for i, s in enumerate(slides, 1):
        for b in RD.code_boxes(s):
            boxes += 1
            for l in b["raw"]:
                rows += 1
                if l.startswith((">>> ", "... ")) or l.strip() == ">>>" or (b["form"] == "prompt" and l.strip() == "..."):
                    nf += 1; print("FINDING slide %d box '%s': a code line begins with a prompt: %s" % (i, b["name"], l.strip()[:70]))
    print("COUNTS code_boxes=%d rows_read=%d prompt_rows=%d findings=%d" % (boxes, rows, nf, nf))
    print("VERDICT: %s" % ("PASS" if nf == 0 else "FAIL"))
    return 0 if nf == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
