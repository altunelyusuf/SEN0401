#!/usr/bin/env python3
"""sen0401_deck_arc_check v1.0.0 - the arc of a SEN0401 chapter deck against the owner's deck rules (new; SEN0414's builders hold these as gates before rendering, SEN0401's chapter builders
hold some of them, no script reads the finished plan and file together). Reads chNN-deck/deck_plan_v*.json and the finished .pptx. It refuses:
  1. a deck that is not 26 slides (--slides N), whose slide 1 is not the title or whose last slide is not the dark closing slide;
  2. no agenda on slide 2, an agenda whose ranges '(slides a-b)' are not contiguous from slide 3 to the last slide, or whose range starts (after the first) are not section slides;
  3. a competency-questions slide (numbered list titled with 'questions') before the first section slide;
  4. a content slide without a takeaway strip, except the story slides (those carrying a WHO/WHERE/WHEN/READ row) and the questions slide;
  5. each story slide without its fact row (who, where, when, link text, link) and picture; fewer than three story slides;
  6. no summary slide immediately before the resources slide; no resources slide with live-link groups covering READ (corpus, the book), STANDARDS or SEMINAL (papers, specifications), COMMUNITY
     (forum, mailing list, discussion) and WATCH (a video or lecture on a video host or a course site) - the owner wants further reading AND watching; every link https;
  7. speaker notes: every slide has notes (deck_notes_check owns the prose rules); and the notes are SHORT - a note of more than --max-notes words (default 120) is reported. This is a WARN by
     default because the owner's standing rule (speaker notes are short notes) and the owner's ruling of 2026-10-08 recorded in chapter 7's review (reader's prose in full sentences, 156 words on
     average) are in tension and only the owner can settle it; --strict-notes makes it a refusal;
  8. an everyday analogy for a key concept: plan meta 'analogies' (a list of {concept, analogy, slide}) must exist, and each analogy text must be on its slide (WARN when the list is absent).
Usage: sen0401_deck_arc_check_v1_0_0.py NN [--slides N] [--max-notes W] [--max-sentences S] [--warn-notes]      Environment: SEN0401_ROOT, SEN0401_DECK (a deck file to check instead of the chapter's newest).  Exit 0 when nothing is refused."""
__version__ = "1.3.0"
# 1.3.0 (over 1.2.0, two changes only): (1) without SEN0401_DECK the deck to check is the newest deck (by version in the file name) of the chapter in 03-materials/chNN, falling back to
#   chNN-deck only when 03-materials has none; (2) a plan and a deck of different length, or a slide index of the plan that is not in the deck, is REFUSED with a message naming both lengths (exit 1), never an IndexError.
#   Every other rule and message is unchanged.
# 1.2.0 (over 1.1.0, two changes only): (1) the number of slides is read from the deck (the finished file) unless --slides N is given, so a deck of any length is checked against the rest of the rule;
#   (2) the last part of the agenda (summary, resources, closing) may start at the summary slide that precedes the resources slide, not only at a section slide. Every other rule and message is unchanged.
# 1.1.0 (over 1.0.0): the notes conflict is settled from the files (2026-10-15): speaker notes are SHORT reader's prose - 2 to 4 full sentences, at most 100 words - which satisfies the owner's
#   "short notes" preference and the ruling of 2026-10-08 (no presenter labels, deck_notes_check). It is now a REFUSAL by default (--warn-notes downgrades it; --max-notes W and --max-sentences S change the limits).
import glob, json, os, re, sys, zipfile
from xml.dom import minidom

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]
newest_of = lambda files: sorted(files, key=vkey)[-1]
VIDEO = re.compile(r"youtube\.com|youtu\.be|vimeo\.com|ocw\.mit\.edu|coursera\.org|edx\.org|video|\.mp4|peertube|media\.ccc\.de|bitcointv|learningbitcoin", re.I)


def texts(deck):
    z = zipfile.ZipFile(deck); out = []
    for n in sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n)); out.append(["".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in d.getElementsByTagName("a:p")])
    return out


def main(a):
    n = a[0]; want = int(a[a.index("--slides") + 1]) if "--slides" in a else None
    maxn = int(a[a.index("--max-notes") + 1]) if "--max-notes" in a else 100; strict_notes = "--warn-notes" not in a
    maxs = int(a[a.index("--max-sentences") + 1]) if "--max-sentences" in a else 4
    chd = os.path.join(TOOL, "ch%s-deck" % n); plan = json.load(open(newest(os.path.join(chd, "deck_plan_v*.json")))); S = plan["slides"]
    delivered = glob.glob(os.path.join(ROOT, "03-materials", "ch%s" % n, "*_v*_*_*.pptx"))
    deck = os.environ.get("SEN0401_DECK") or (newest_of(delivered) if delivered else newest(os.path.join(chd, "sen0401_ch%s_deck_v*.pptx" % n))); T = texts(deck)
    bad, warn = [], []
    if len(S) != len(T):
        bad.append("plan/deck mismatch: the plan has %d slides and the deck file %s has %d slides" % (len(S), os.path.basename(deck), len(T)))
    if want is None: want = len(T)
    if len(S) != want or len(T) != want: bad.append("the plan has %d slides and the file %d, the standard is %d" % (len(S), len(T), want))
    if S[0]["kind"] != "title": bad.append("slide 1 is not the title slide")
    if S[-1]["kind"] != "closing" or S[-1].get("bg") != "dark": bad.append("the last slide is not the dark closing slide")
    sections = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    ag = [p for p in T[1] if re.search(r"\(slides \d+-\d+\)", p)] if len(T) > 1 else []
    if "route" not in S[1]["title"].lower() and "agenda" not in S[1]["title"].lower() or not ag: bad.append("slide 2 is not an agenda with '(slides a-b)' ranges")
    else:
        rg = [tuple(map(int, re.search(r"\(slides (\d+)-(\d+)\)", p).groups())) for p in ag]
        if rg[0][0] != 3 or rg[-1][1] != len(S) or any(rg[i][0] != rg[i - 1][1] + 1 for i in range(1, len(rg))): bad.append("agenda ranges are not contiguous from slide 3 to slide %d: %s" % (len(S), rg))
        rs = [i + 1 for i, s in enumerate(S) if any(it.get("t") == "links" for it in s["items"])]
        closing_start = [rs[0] - 1] if len(rs) == 1 and rs[0] >= 2 and re.search(r"summary|in \w+ lines|chapter in", S[rs[0] - 2]["title"], re.I) else []
        for r in rg[1:]:
            if r[0] not in sections and not (r[0] in closing_start and r is rg[-1]): bad.append("agenda range starting at slide %d does not start at a section slide (sections: %s)" % (r[0], sections))
    q = [i + 1 for i, s in enumerate(S) if s["kind"] == "content" and "question" in s["title"].lower() and any(it.get("t") == "numlist" for it in s["items"])]
    if not q or (sections and q[0] > sections[0]): bad.append("no competency-questions slide before the first section slide")
    stories = [i + 1 for i, s in enumerate(S) if any(it.get("t") == "factrow" for it in s["items"])]
    if len(stories) < 3: bad.append("%d story slide(s) with a fact row, 3 needed" % len(stories))
    for i in stories:
        f = [it for it in S[i - 1]["items"] if it.get("t") == "factrow"][0]; kinds = {it.get("t") for it in S[i - 1]["items"]}
        if not all(f.get(k) for k in ("who", "where", "when", "link", "linkText")) or "img" not in kinds: bad.append("story slide %d lacks a field of its fact row or its picture" % i)
    for i, s in enumerate(S, 1):
        if s["kind"] == "content" and not s.get("take") and i not in stories and i not in q: bad.append("content slide %d (%s) has no takeaway strip" % (i, s["title"][:40]))
    res = [i + 1 for i, s in enumerate(S) if any(it.get("t") == "links" for it in s["items"])]
    if len(res) != 1: bad.append("%d resources slide(s)" % len(res))
    else:
        r = res[0]
        if r < 2 or not re.search(r"summary|in \w+ lines|chapter in", S[r - 2]["title"], re.I): bad.append("slide %d (before the resources slide) is not a summary slide: %r" % (r - 1, S[r - 2]["title"]))
        groups = [it for it in S[r - 1]["items"] if it.get("t") == "links"][0]["groups"]
        rows = [(g["head"], x[0], x[1]) for g in groups for x in g["rows"]]
        if any(not u.startswith("https://") for _, _, u in rows): bad.append("a resources link is not https")
        heads = " ".join(g["head"] for g in groups).lower()
        need = {"READ": re.search(r"read|book|corpus|textbook", heads), "STANDARDS/SEMINAL": re.search(r"standard|seminal|paper|spec|whitepaper|bip", heads),
                "COMMUNITY": re.search(r"communit|forum|discuss|mailing", heads), "WATCH": re.search(r"watch|video|talk|lecture|course", heads) or any(VIDEO.search(u) for _, _, u in rows)}
        for k, v in need.items():
            if not v: bad.append("resources slide %d has no %s group or link (heads: %s)" % (r, k, ", ".join(g["head"] for g in groups)))
        if not any(VIDEO.search(u) for _, _, u in rows): bad.append("no resources link is a video or lecture on a video host (the owner wants further watching)")
    lens = [len(s["notes"].split()) for s in S]
    over = []
    for i, (s, w) in enumerate(zip(S, lens), 1):
        if not s["notes"].strip(): bad.append("slide %d has no notes" % i)
        elif w > maxn or not 2 <= len([x for x in re.split(r"(?<=[.!?])\s+", re.sub(r"\b(Mt|Dr|St|Mr|Mrs|vs|No)\.\s", r"\1.~", s["notes"].strip())) if x]) <= maxs: over.append((i, w))
    if over:
        (bad if strict_notes else warn).append("%d of %d slides have notes outside the short reader's-prose limit (2 to %d sentences, %d words) (longest: slide %d with %d words; slides %s)"
                                              % (len(over), len(S), maxs, maxn, max(over, key=lambda x: x[1])[0], max(w for _, w in over), [i for i, _ in over]))
    an = plan["meta"].get("analogies")
    if not an: warn.append("plan meta has no 'analogies' list: no everyday analogy is declared for any key concept (car keys / house keys style)")
    else:
        for x in an:
            if not 1 <= x["slide"] <= len(T): bad.append("plan/deck mismatch: the analogy for %s is on slide %s, which is not in the deck (%d slides; the plan has %d)" % (x["concept"], x["slide"], len(T), len(S)))
            elif x["analogy"] not in " ".join(T[x["slide"] - 1]): bad.append("analogy for %s is not on slide %s" % (x["concept"], x["slide"]))
    print("sen0401_deck_arc_check %s (chapter %s): %d slides, sections %s, story slides %s, resources slide %s, notes %d..%d words (mean %d); %d refusal(s), %d warning(s)"
          % (__version__, n, len(S), sections, stories, res, min(lens), max(lens), sum(lens) // len(lens), len(bad), len(warn)))
    for b in bad: print("  REFUSED", b)
    for w in warn[:40]: print("  WARN", w)
    if len(warn) > 40: print("  ... %d more warnings" % (len(warn) - 40))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
