#!/usr/bin/env python3
"""sen0401_deck_lambda_check v1.0.0 (task TK_Deck_Checks_Build, owner 2026-10-30: no lambda unless the subject teaches lambda). Reads a deck (.pptx); no code line of a code box (both forms: prompts, or a shape
named code...) holds the word lambda (outside strings and comments), unless the slide's title contains 'lambda' or the slide is named in the optional argument --declared N,N (slide numbers; default none).
Prose that mentions lambda and identifiers such as lambda_count are not findings. Prints 'FINDING slide N box NAME: text' per finding, a COUNTS line, then 'VERDICT: PASS' or 'VERDICT: FAIL'. Exit 0 PASS, 1 FAIL, 2 cannot read.
Usage: sen0401_deck_lambda_check_v1_0_0.py DECK.pptx [--declared 3,7]"""
__version__ = "1.0.0"
import os, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_deck_code_read_v1_0_0 as RD


def main(argv):
    declared = set()
    if "--declared" in argv:
        k = argv.index("--declared"); declared = {int(x) for x in argv[k + 1].split(",") if x.strip()}; argv = argv[:k] + argv[k + 2:]
    if len(argv) != 1:
        print(__doc__); return 2
    try:
        slides = RD.decks_slides(argv[0])
    except Exception as e:
        print("VERDICT: CANNOT_RUN %s" % e); return 2
    nf = lam_lines = allowed = 0
    print("sen0401_deck_lambda_check %s | %s | %d slides | declared lambda slides: %s" % (__version__, os.path.basename(argv[0]), len(slides), sorted(declared) or "none"))
    for i, s in enumerate(slides, 1):
        teaches = i in declared or re.search(r"lambda", RD.slide_title(s), re.I) is not None
        for b in RD.code_boxes(s):
            for t, _ in b["lines"]:
                if re.search(r"\blambda\b", RD.strip_code(t)):
                    lam_lines += 1
                    if teaches:
                        allowed += 1
                    else:
                        nf += 1; print("FINDING slide %d box '%s': lambda in a code line of a slide that does not teach it: %s" % (i, b["name"], t.strip()[:80]))
    print("COUNTS code_lines_with_lambda=%d on_slides_that_teach_it=%d findings=%d" % (lam_lines, allowed, nf))
    print("VERDICT: %s" % ("PASS" if nf == 0 else "FAIL"))
    return 0 if nf == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
