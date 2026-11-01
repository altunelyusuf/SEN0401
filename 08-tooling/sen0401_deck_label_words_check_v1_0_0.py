#!/usr/bin/env python3
"""sen0401_deck_label_words_check v1.0.0 (task TK_Deck_Checks_Build, owner 2026-10-30: 5N1K as human storytelling, never 'WHAT:'-style labels). Reads a deck (.pptx); no text shape (groups included) begins with a 5N1K
label word (WHAT, WHO, WHEN, WHERE, WHY, HOW; any case) followed by a colon or a dash (hyphen, en dash, em dash). A sentence that merely starts with the word (What a block is..., Whenever...) is not a label.
The rule is the one of sen0401_deck_teach_measure_v1_0_0.py. Prints 'FINDING slide N shape NAME: text' per finding, a COUNTS line, then 'VERDICT: PASS' or 'VERDICT: FAIL'. Exit 0 PASS, 1 FAIL, 2 cannot read.
Usage: sen0401_deck_label_words_check_v1_0_0.py DECK.pptx"""
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
    nf = 0; on = set()
    print("sen0401_deck_label_words_check %s | %s | %d slides" % (__version__, os.path.basename(argv[0]), len(slides)))
    for i, s in enumerate(slides, 1):
        for sh in RD.walk(s.shapes):
            if sh.has_text_frame and RD.LABEL.match(sh.text_frame.text.strip()):
                nf += 1; on.add(i); print("FINDING slide %d shape '%s': begins with a label word: %s" % (i, sh.name, sh.text_frame.text.strip()[:70].replace("\n", " ")))
    print("COUNTS label_shapes=%d slides_with_such_shape=%s findings=%d" % (nf, sorted(on), nf))
    print("VERDICT: %s" % ("PASS" if nf == 0 else "FAIL"))
    return 0 if nf == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
