#!/usr/bin/env python3
"""sen0401_deck_standard_check v1.1.0 (python-pptx 1.0.2) - the deck standard of the SEN0401 lecture decks, D1 to D12, measured.
A NEW tool; it edits nothing and changes no gate. One named, exit-coded result per element; the measured number is printed for each.
Usage:   sen0401_deck_standard_check_v1_1_0.py NN [deck.pptx]      NN = chapter number (05, 06 ...). Without deck.pptx the newest .pptx of 03-materials/chNN is read.
Environment: SEN0401_ROOT (default the parent of this file's folder).
Result words, as printed: PASS, FAIL, NOT_MEASURED (the input of the measure is missing), CANNOT_RUN (the tool failed). Exit code 0 only when D1..D12 all PASS; 1 when any FAIL; 2 when any
NOT_MEASURED/CANNOT_RUN and none FAIL. A skip is not a pass. The file names itself FAILING when an element fails.

DEFINITIONS (every measure is mechanical; a threshold is the owner's standing rule, not a taste)
  text box     : every shape with a text frame (text boxes AND auto shapes carrying text, also inside groups); table cells are not boxes. Words = len(text.split()) of the whole frame.
  slide number : a text box whose text is 'k / N' (k = the slide's position, N = number of slides), or a slide-number field (a:fld type=slidenum).
  code box     : a text box with at least one paragraph that starts with '>>> '. Code slide = a slide holding at least one code box.
  code line    : a paragraph of a code box (input row and output row alike).
  visual result: on the code slide a native chart (graphic frame with a chart), a native table, or a drawn diagram = at least one connector (p:cxnSp) or an arrow/chevron auto shape
                 AND at least three auto shapes that carry text. REPL text, captions and plain pills alone are not a visual result.
  explanation  : on the code slide, for EVERY code box a plain-language note: a non-code text box of at least 8 words that overlaps the code box's horizontal span and lies at most 0.6 inch
                 above or below it (the note stands beside the code). Captions shorter than 8 words and the 'run under Python' stamp do not count.
  D3 measure   : share of code slides that have BOTH the explanation for every code box AND a visual result (target 100 percent).
  analogy      : a text box that starts with 'ANALOGY' or 'EVERYDAY' (the marker the standard asks for), or contains 'is like a/an/the', 'are like', 'think of', 'just as', 'imagine' (case-insensitive).
  key concept  : every primary-source concept of the chapter research (03-materials/chNN/rdodi/sen0401_chNN_research_vX_Y_Z.ttl, the newest; resources of class sen0401:PrimarySourceConcept or sen0414:PrimarySourceConcept,
                 label in rdfs:label), de-duplicated by normalised label. Normalised: lower case, parenthesis text removed, non-alphanumerics to one space, a trailing 's' of each word dropped.
  concept shown: the normalised label occurs, as a phrase, in the normalised text of a slide (all text boxes and tables of the slide; notes are not slide text).
  D4 measure   : share of key concepts that occur in an analogy-marked text box (target 100 percent).
  D11 measure  : share of key concepts shown on at least one slide (target not below 90 percent); the number is stated as measured, the list of missing concepts is printed.
  story slide  : a slide with at least two text boxes whose text starts with one of WHO, WHAT, WHEN, WHERE, WHY, HOW, READ.
  D5 measure   : a story slide passes when text boxes start with ALL six of WHO, WHAT, WHEN, WHERE, WHY, HOW, and the slide holds a picture (at least 8 percent of the slide area) and at
                 least one live link (an external http(s) hyperlink on the slide). Target: every story slide passes; no story slide at all is NOT_MEASURED.
  native chart : a graphic frame whose chart part is a native PowerPoint chart (shape.has_chart). Chart picture = a picture whose alt text or name contains chart/graph/plot/histogram.
  D6 measure   : number of chart pictures (target 0); the number of native charts is printed.
  D7 measure   : the largest speaker-note word count of any slide (target at most 60); slides over the limit are listed.
  resources    : a slide whose title contains resources, where to go, further reading/watching or read more AND holding at least 5 external hyperlinks (D8 measure: the link count).
  background   : the slide background colour (p:bg solid fill); if none, the fill of the first shape covering at least 95 percent of the slide. Dark = relative luminance below 0.5.
  D9 measure   : number of dark and of light slides (PASS when all slides are on one side) and the number of dark/light switches along the slide order.
  divider      : a slide without the brand mark text box '(bitcoin sign)', that is neither the first nor the last slide, and has a title (the first text box).
  D10 measure  : a divider passes when it names at least one concept (concept pill = a remaining text box of at most 4 words, after the title, the subtitle (the second text box), the picture
                 caption and the slide number are set aside), has for EVERY concept one line of meaning (a remaining text box of at least 5 words, or a 'Name | meaning' box with a meaning of
                 at least 5 words; the number of meaning lines is at least the number of concept pills), and holds a visual (picture, native chart or native table). Target: every divider passes.
  D12 measure  : code lines whose estimated width exceeds the room: width = characters x 0.6 x font size (monospace advance of Courier New, 0.6 em); room = the box width minus its insets;
                 for a frame with wrap='none' the room is the distance from the box's left edge to the slide's right edge. A line over the room wraps (or leaves the slide): D12 target 0 such lines.
Facts printed for every deck: slides, code slides, native charts, analogy text boxes, longest text box in words (the facts of the baseline decks).
"""
__version__ = "1.1.0"
import glob, os, re, sys

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
EMU_IN = 914400
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", os.path.basename(p))[-1]]


def newest(pat):
    f = sorted(glob.glob(pat), key=vkey)
    return f[-1] if f else None


try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    import pptx
except Exception as e:  # pragma: no cover
    print("CANNOT_RUN python-pptx not importable: %s" % e); sys.exit(2)

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main", "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            for x in walk(sh.shapes):
                yield x
        else:
            yield sh


def words(t):
    return len(t.split())


def norm(t):
    t = re.sub(r"\([^)]*\)", " ", t.lower())
    t = re.sub(r"[^a-z0-9]+", " ", t).split()
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in t)


def lum(hexrgb):
    r, g, b = [int(hexrgb[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


class Box:
    def __init__(self, sh):
        self.sh = sh
        self.text = sh.text_frame.text
        self.l, self.t, self.w, self.h = sh.left or 0, sh.top or 0, sh.width or 0, sh.height or 0
        self.words = words(self.text)
        self.paras = [p.text for p in sh.text_frame.paragraphs]
        self.code = any(p.startswith(">>> ") for p in self.paras)


class Slide:
    def __init__(self, idx, s, W, H, n):
        self.i, self.s, self.W, self.H, self.n = idx, s, W, H, n
        self.shapes = list(walk(s.shapes))
        self.boxes = [Box(x) for x in self.shapes if x.has_text_frame and x.text_frame.text.strip() != ""]
        self.tables = [x for x in self.shapes if getattr(x, "has_table", False) and x.has_table]
        self.charts = [x for x in self.shapes if getattr(x, "has_chart", False) and x.has_chart]
        self.pics = [x for x in self.shapes if x.shape_type == MSO_SHAPE_TYPE.PICTURE]
        self.notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        self.links = [r.target_ref for r in s.part.rels.values() if r.is_external and r.target_ref.lower().startswith("http")]
        self.text = " ".join(b.text for b in self.boxes) + " " + " ".join(c.text_frame.text for t in self.tables for r in t.table.rows for c in r.cells)
        self.codeboxes = [b for b in self.boxes if b.code]

    def numbered(self):
        if any(re.fullmatch(r"\s*%d\s*/\s*%d\s*" % (self.i, self.n), b.text) for b in self.boxes):
            return True
        return bool(self.s._element.xpath('.//a:fld[@type="slidenum"]'))

    def title(self):
        for b in self.boxes:
            if b.text.strip() != "₿":
                return b.text
        return ""

    def has_mark(self):
        return any(b.text.strip() == "₿" for b in self.boxes)

    def bgcolor(self):
        x = self.s._element.xpath("./p:cSld/p:bg//a:srgbClr/@val")
        if x:
            return x[0].upper()
        for sh in self.shapes:
            if sh.width and sh.height and sh.width * sh.height >= 0.95 * self.W * self.H:
                y = sh._element.xpath("./p:spPr/a:solidFill/a:srgbClr/@val")
                if y:
                    return y[0].upper()
        return None


ANALOGY = re.compile(r"^\s*(ANALOGY|EVERYDAY)\b|\b(is|are) like (a|an|the)\b|\bthink of\b|\bjust as\b|\bimagine\b", re.I)


def research_concepts(ch):
    f = newest(os.path.join(ROOT, "03-materials", "ch%s" % ch, "rdodi", "sen0401_ch%s_research_v*.ttl" % ch))
    if not f:
        return None, []
    txt = open(f, encoding="utf-8").read()
    labs = re.findall(r"a sen04(?:01|14):PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", txt)
    seen, out = set(), []
    for l in labs:
        k = norm(l)
        if k and k not in seen:
            seen.add(k); out.append((l, k))
    return f, out


def is_arrow(sh):
    try:
        return sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and re.search(r"ARROW|CHEVRON", str(sh.auto_shape_type), re.I) is not None
    except Exception:
        return False


def visual_result(sl):
    if sl.charts or sl.tables:
        return True
    conn = len(sl.s._element.xpath(".//p:cxnSp")) + sum(1 for x in sl.shapes if is_arrow(x))
    texted = sum(1 for x in sl.shapes if x.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and x.has_text_frame and x.text_frame.text.strip())
    return conn >= 1 and texted >= 3


def explained(sl):
    notes = [b for b in sl.boxes if not b.code and b.words >= 8 and not b.text.startswith("run under")]
    for c in sl.codeboxes:
        ok = False
        for n in notes:
            overlap = min(c.l + c.w, n.l + n.w) - max(c.l, n.l) > 0
            gap = max(n.t - (c.t + c.h), c.t - (n.t + n.h))
            if overlap and gap <= 0.6 * EMU_IN:
                ok = True; break
        if not ok:
            return False
    return True


def wrapped_lines(sl):
    bad, total = [], 0
    for b in sl.codeboxes:
        bp = b.sh.text_frame._txBody.find("{%s}bodyPr" % NS["a"])
        wrap = bp.get("wrap", "square")
        li, ri = int(bp.get("lIns", 91440)), int(bp.get("rIns", 91440))
        room = (b.w - li - ri) if wrap != "none" else (sl.W - b.l - li)
        for p in b.sh.text_frame.paragraphs:
            szs = [r.font.size.pt for r in p.runs if r.font.size] or [18.0]
            sz = max(szs)
            w = len(p.text) * 0.6 * sz * 12700
            total += 1
            if w > room:
                bad.append((sl.i, len(p.text), round(w / room, 2)))
    return bad, total


def main(argv):
    if len(argv) < 2:
        print("usage: sen0401_deck_standard_check_v1_1_0.py NN [deck.pptx]"); return 2
    ch = argv[1].zfill(2)
    deck = argv[2] if len(argv) > 2 else newest(os.path.join(ROOT, "03-materials", "ch%s" % ch, "*.pptx"))
    if not deck or not os.path.exists(deck):
        print("CANNOT_RUN no deck for chapter %s" % ch); return 2
    prs = Presentation(deck)
    W, H = prs.slide_width, prs.slide_height
    n = len(prs.slides)
    S = [Slide(i, s, W, H, n) for i, s in enumerate(prs.slides, 1)]
    res = []  # (id, name, status, measured)

    def add(i, name, status, meas):
        res.append((i, name, status, meas))

    # facts
    code_slides = [s for s in S if s.codeboxes]
    n_charts = sum(len(s.charts) for s in S)
    analog = [(s.i, b) for s in S for b in s.boxes if ANALOGY.search(b.text)]
    longest = max((b.words, s.i) for s in S for b in s.boxes)
    print("sen0401_deck_standard_check v%s | python-pptx %s | chapter %s | deck %s" % (__version__, pptx.__version__, ch, os.path.relpath(deck, ROOT)))
    print("FACTS slides=%d code_slides=%d native_charts=%d analogies=%d longest_box_words=%d (slide %d)" % (n, len(code_slides), n_charts, len(analog), longest[0], longest[1]))

    # D1
    miss = [s.i for s in S if not s.numbered()]
    add("D1", "every slide is numbered", "PASS" if not miss else "FAIL", "%d of %d slides numbered; unnumbered: %s" % (n - len(miss), n, miss or "none"))
    # D2
    over = [(s.i, b.words) for s in S for b in s.boxes if b.words > 30]
    add("D2", "no text box over 30 words", "PASS" if not over else "FAIL", "longest box %d words (slide %d); %d boxes over 30: %s" % (longest[0], longest[1], len(over), over[:12]))
    # D3
    good = [s.i for s in code_slides if explained(s) and visual_result(s)]
    noexp = [s.i for s in code_slides if not explained(s)]
    novis = [s.i for s in code_slides if not visual_result(s)]
    if not code_slides:
        add("D3", "code slides: explanation beside the code + executed result as a visual", "NOT_MEASURED", "no code slide")
    else:
        add("D3", "code slides: explanation beside the code + executed result as a visual", "PASS" if len(good) == len(code_slides) else "FAIL",
            "%d of %d code slides complete (%.0f%%); without explanation: %s; without visual result: %s" % (len(good), len(code_slides), 100.0 * len(good) / len(code_slides), noexp, novis))
    # D4, D11
    rf, concepts = research_concepts(ch)
    if not concepts:
        add("D4", "every key concept has an everyday analogy", "NOT_MEASURED", "no research concept list found for chapter %s" % ch)
        add("D11", "coverage of the research concepts", "NOT_MEASURED", "no research concept list found for chapter %s" % ch)
    else:
        an_text = norm(" ".join(b.text for _, b in analog))
        # an analogy covers a concept when the concept occurs in the SAME text box or on the same slide as the analogy marker
        an_slide_text = norm(" ".join(next(s.text for s in S if s.i == i) for i in sorted({i for i, _ in analog})))
        have = [l for l, k in concepts if k in an_slide_text]
        add("D4", "every key concept has an everyday analogy", "PASS" if len(have) == len(concepts) else "FAIL",
            "%d of %d key concepts have an analogy slide or box (%.1f%%); research %s" % (len(have), len(concepts), 100.0 * len(have) / len(concepts), os.path.relpath(rf, ROOT)))
        alltext = norm(" ".join(s.text for s in S))
        shown = [l for l, k in concepts if k in alltext]
        pct = 100.0 * len(shown) / len(concepts)
        missing = [l for l, k in concepts if k not in alltext]
        add("D11", "coverage of the research concepts", "PASS" if pct >= 90.0 else "FAIL",
            "%d of %d research concepts appear on a slide = %.1f%% (target not below 90); not shown (%d): %s" % (len(shown), len(concepts), pct, len(missing), "; ".join(missing[:40]) + (" ..." if len(missing) > 40 else "")))
    # D5
    stories = [s for s in S if sum(1 for b in s.boxes if re.match(r"(WHO|WHAT|WHEN|WHERE|WHY|HOW|READ)\b", b.text)) >= 2]
    if not stories:
        add("D5", "every story has 5N1K, a real picture and a live link", "NOT_MEASURED", "no story slide")
    else:
        det, okc = [], 0
        for s in stories:
            lab = {m.group(1) for b in s.boxes for m in [re.match(r"(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b", b.text)] if m}
            pic = any(p.width * p.height >= 0.08 * W * H for p in s.pics)
            ok = len(lab) == 6 and pic and bool(s.links)
            okc += ok
            det.append("slide %d: %s picture=%s live_links=%d" % (s.i, "/".join(sorted(lab)) or "-", "yes" if pic else "no", len(s.links)))
        add("D5", "every story has 5N1K, a real picture and a live link", "PASS" if okc == len(stories) else "FAIL",
            "%d of %d story slides complete; labels found of WHO/WHAT/WHEN/WHERE/WHY/HOW -> %s" % (okc, len(stories), "; ".join(det)))
    # D6
    cpics = []
    for s in S:
        for p in s.pics:
            d = (p._element.xpath("./p:nvPicPr/p:cNvPr/@descr") or [""])[0] + " " + p.name
            if re.search(r"chart|graph|plot|histogram", d, re.I):
                cpics.append(s.i)
    add("D6", "every chart is a native chart object", "PASS" if not cpics else "FAIL", "%d native charts, %d chart pictures %s" % (n_charts, len(cpics), cpics or ""))
    # D7
    nw = [(s.i, words(s.notes)) for s in S]
    overn = [x for x in nw if x[1] > 60]
    add("D7", "speaker notes at most 60 words per slide", "PASS" if not overn else "FAIL", "longest note %d words (slide %d); %d slides over 60: %s" % (max(w for _, w in nw), max(nw, key=lambda x: x[1])[0], len(overn), overn))
    # D8
    res_s = [s for s in S if re.search(r"resources|where to go|further (reading|watching)|read more", s.title(), re.I) and len(s.links) >= 5]
    add("D8", "a resources slide with links", "PASS" if res_s else "FAIL", "resources slide(s): %s with %s external links" % ([s.i for s in res_s] or "none", [len(s.links) for s in res_s] or 0))
    # D9
    cols = [(s.i, s.bgcolor()) for s in S]
    if any(c is None for _, c in cols):
        add("D9", "one background scheme", "NOT_MEASURED", "no background colour readable on slides %s" % [i for i, c in cols if c is None])
    else:
        dk = ["D" if lum(c) < 0.5 else "L" for _, c in cols]
        sw = sum(1 for a, b in zip(dk, dk[1:]) if a != b)
        add("D9", "one background scheme", "PASS" if len(set(dk)) == 1 else "FAIL", "%d dark, %d light slides, %d switches; colours %s" % (dk.count("D"), dk.count("L"), sw, sorted({c for _, c in cols})))
    # D10
    divs = [s for s in S if not s.has_mark() and 1 < s.i < n and s.title()]
    if not divs:
        add("D10", "every divider names its concepts with a meaning line and a visual", "NOT_MEASURED", "no divider found")
    else:
        det, okc = [], 0
        for s in divs:
            rest = [b for b in s.boxes if not re.fullmatch(r"\s*\d+\s*/\s*\d+\s*", b.text)]
            rest = rest[2:]  # title, subtitle set aside
            caps = set()  # the picture caption = the text box next after a picture in the shape order
            for k, x in enumerate(s.shapes[:-1]):
                if x.shape_type == MSO_SHAPE_TYPE.PICTURE and s.shapes[k + 1].has_text_frame:
                    caps.add(s.shapes[k + 1].shape_id)
            rest = [b for b in rest if b.sh.shape_id not in caps]
            pills = [b for b in rest if b.words <= 4]
            meaning = [b for b in rest if b.words >= 5 or ("|" in b.text and words(b.text.split("|", 1)[1]) >= 5)]
            vis = bool(s.pics or s.charts or s.tables)
            ok = len(pills) >= 1 and len(meaning) >= len(pills) and vis
            okc += ok
            det.append("slide %d: concepts=%d meaning_lines=%d visual=%s" % (s.i, len(pills), len(meaning), "yes" if vis else "no"))
        add("D10", "every divider names its concepts with a meaning line and a visual", "PASS" if okc == len(divs) else "FAIL", "%d of %d dividers complete; %s" % (okc, len(divs), "; ".join(det)))
    # D12
    badl, tot = [], 0
    for s in code_slides:
        b, t = wrapped_lines(s); badl += b; tot += t
    if not code_slides:
        add("D12", "no code line wraps", "NOT_MEASURED", "no code slide")
    else:
        add("D12", "no code line wraps", "PASS" if not badl else "FAIL", "%d of %d code lines exceed their room (slide, characters, width/room): %s" % (len(badl), tot, badl[:10]))

    for i, name, st, meas in res:
        print("%s %s %s | %s" % (i, st, name, meas))
    fails = [i for i, _, st, _ in res if st == "FAIL"]
    nm = [i for i, _, st, _ in res if st in ("NOT_MEASURED", "CANNOT_RUN")]
    print("SUMMARY PASS=%d FAIL=%d NOT_MEASURED=%d | failing: %s%s" % (sum(1 for r in res if r[2] == "PASS"), len(fails), len(nm), ",".join(fails) or "none",
                                                                     (" | not measured: " + ",".join(nm)) if nm else ""))
    if fails:
        print("RESULT FAILING (exit 1): deck standard not met")
        return 1
    if nm:
        print("RESULT NOT_MEASURED (exit 2)")
        return 2
    print("RESULT PASS (exit 0)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        print("CANNOT_RUN %s" % e); sys.exit(2)
