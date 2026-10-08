#!/usr/bin/env python3
"""deck_notes_check v1.0.0 - the speaker notes of a published deck are written for the student who reads them.

The owner's ruling of 2026-10-08: the decks are published and the students should benefit from the notes, so the notes
carry no presenter directives ("SAY:", "ASK:", "TELL:", "SHOW:", "STORY (date):", "FULL TEXT:", "CUE:", "DEMO:" and the
like) - they are reader's prose in full sentences; and a slide must be understandable on its own, so the notes add to the
slide rather than replace it. This check reads the finished .pptx and refuses:
  1. a content slide (from --first-content, default 2) without notes;
  2. a note containing a directive label at the start of a line - a word or short phrase in capitals, or one of the
     known cue words in any case, followed by a colon;
  3. a note that is not prose: fewer than two sentences, or any line that does not end a sentence (., !, ?, a closing
     quote or bracket after one), or a bare URL line (URLs belong in the slide's resources, or inside a sentence);
  4. a note repeating the slide's own title as its whole content.
Usage: deck_notes_check_v1_0_0.py <deck.pptx> [--first-content N]
Exit 0 when every note passes; 1 otherwise, listing each slide and the reason. Standard library plus python-pptx."""
__version__ = "1.0.0"
import re, sys
from pptx import Presentation

CUE = re.compile(r"^\s*(?:[A-Z][A-Z \-/&()0-9]{1,24}|say|ask|tell|show|story|cue|demo|note|full text|read|point|click|pause|transition|timing)\s*(?:\([^)]*\))?\s*:", re.M)
SENT_END = re.compile(r"[.!?…][\"'”’)\]]*\s*$")
URL_LINE = re.compile(r"^\s*(?:https?://|www\.)\S+\s*$", re.M)

def problems(title, notes):
    out = []
    if not notes.strip():
        return ["no notes"]
    m = CUE.search(notes)
    if m:
        out.append("directive label %r" % m.group(0).strip())
    lines = [l for l in notes.splitlines() if l.strip()]
    for l in lines:
        if not SENT_END.search(l.strip()):
            out.append("line does not end a sentence: %r" % l.strip()[:60]); break
    if URL_LINE.search(notes):
        out.append("bare URL line")
    sentences = [s for s in re.split(r"(?<=[.!?…])\s+", notes.strip()) if s.strip()]
    if len(sentences) < 2:
        out.append("fewer than two sentences")
    if title and notes.strip().rstrip(".").lower() == title.strip().lower():
        out.append("repeats the title only")
    return out

def main(path, first_content=2):
    prs = Presentation(path); bad = []
    for i, slide in enumerate(prs.slides, 1):
        notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        title = slide.shapes.title.text if slide.shapes.title is not None else ""
        if i < first_content and not notes.strip():
            continue
        p = problems(title, notes)
        if p:
            bad.append((i, p))
    n = len(prs.slides)
    print("deck_notes_check %s: %d slides, %d with notes written for the reader" % (__version__, n, n - len(bad)))
    for i, p in bad:
        print("  slide %d: %s" % (i, "; ".join(p)))
    print("  VERDICT: %s" % ("PASS" if not bad else "FAIL (%d slide(s))" % len(bad)))
    return 0 if not bad else 1

if __name__ == "__main__":
    a = sys.argv[1:]; fc = 2
    if "--first-content" in a:
        fc = int(a[a.index("--first-content") + 1]); a = [x for x in a if x not in ("--first-content", str(fc))]
    sys.exit(main(a[0], fc))
