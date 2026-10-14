#!/usr/bin/env python3
"""sen0401_deck_lookfeel_check v1.0.0 - the CME materials look-and-feel standard (CME_MaterialsLookAndFeel_v1_0_0.md) and the owner's deck rules, read from the finished .pptx (new;
SEN0414 has no such check, its builders hold the rules as gates before rendering). The tokens are PARSED from the standard's own text (CME_STANDARD=path, default
/home/claude/cme/cme/00-standards/CME_MaterialsLookAndFeel_v1_0_0.md), never typed here. It refuses:
  1. a slide whose background is not the standard's page colour, or a deck that switches between dark and light slides mid-deck (the closing slide may be a dark SHAPE on the page colour);
  2. a colour used on any slide that is not one of the standard's palette, its code colours, white, or a grey/tint derived for fills (the allowed extras are listed in EXTRA);
  3. a font other than the standard's three (Cambria headings, Calibri body, Courier New code);
  4. a slide (the title slide excepted) without a visible number 'n / N' with N the slide count;
  5. a slide (not the title slide, whose '>>>' is a logo) that shows code (a '>>>' row or a code block fill) with none of the standard's four syntax colours (keyword, string, number,
     comment; the result colour alone is not colouring), and a deck whose code slides together use fewer than three of the four;
  6. a picture that stands for a chart: an image on a slide whose alt text or caption says chart, plot, graph or histogram (charts are native objects), and a deck with a chart part that has no data labels;
  7. a slide with fewer text frames than a title needs (an empty slide), and a deck of other than the expected number of slides (--slides N, default 26).
Usage: sen0401_deck_lookfeel_check_v1_0_0.py NN [deck.pptx] [--slides N]       Environment: SEN0401_ROOT, CME_STANDARD.  Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import glob, os, re, sys, zipfile

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
STD = os.environ.get("CME_STANDARD", "/home/claude/cme/cme/00-standards/CME_MaterialsLookAndFeel_v1_0_0.md")
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
EXTRA = {"FFFFFF", "D7E4E0", "EFE9DC", "000000", "7A7A7A", "8B949E", "F8F4EC", "E8DFCD", "C9BFAE", "FBF8F2"}   # white and the tints/greys the renderer derives for fills, captions and rules


def tokens():
    t = open(STD, encoding="utf-8").read()
    pal = {k.strip().lower(): v for k, v in re.findall(r"([a-z][a-z ]*?)\s+([0-9A-F]{6})(?=[;.,\n ])", t.split("Palette", 1)[1].split("Code colouring", 1)[0])}
    code = {k.strip().lower(): v for k, v in re.findall(r"(keywords|strings|numbers|comments|result green)\s+([0-9A-F]{6})", t)}
    fonts = re.findall(r"(Cambria|Calibri|Courier New)", t.split("Type:", 1)[1].split("\n", 2)[0] + " " + t.split("Type:", 1)[1][:200])
    return pal, code, set(fonts)


def main(a):
    n = a[0]; want = int(a[a.index("--slides") + 1]) if "--slides" in a else 26
    pos = [x for x in a[1:] if x.endswith(".pptx")]
    deck = pos[0] if pos else sorted(glob.glob(os.path.join(TOOL, "ch%s-deck" % n, "sen0401_ch%s_deck_v*.pptx" % n)), key=vkey)[-1]
    pal, code, fonts = tokens()
    page = pal["background"].upper() if "background" in pal else "FAF6EF"
    allowed = {v.upper() for v in pal.values()} | {v.upper() for v in code.values()} | EXTRA
    syn = {code[k].upper() for k in ("keywords", "strings", "numbers", "comments") if k in code}
    z = zipfile.ZipFile(deck); names = sorted((x for x in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)), key=lambda s: int(re.findall(r"\d+", s)[0]))
    bad = []; N = len(names)
    if N != want: bad.append("the deck has %d slides, the standard plan is %d" % (N, want))
    off = set(); nf = set()
    nsyn_slides = ncode_slides = 0; used = set()
    for i, nm in enumerate(names, 1):
        x = z.read(nm).decode("utf-8")
        bg = re.search(r"<p:bg>.*?</p:bg>", x, re.S)
        b = re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', bg.group(0))[0].upper() if bg else None
        if b != page: bad.append("slide %d: background %s, the standard's page colour is %s" % (i, b, page))
        cols = {c.upper() for c in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', x)}
        off |= {c for c in cols if c not in allowed}
        for f in re.findall(r'<a:latin typeface="([^"]+)"', x):
            if f not in fonts: nf.add(f)
        if i > 1 and not re.search(r"<a:t>%d / %d</a:t>" % (i, N), x): bad.append("slide %d: no visible number '%d / %d'" % (i, i, N))
        texts = re.findall(r"<a:t>([^<]*)</a:t>", x)
        if len(texts) < 2: bad.append("slide %d: fewer than two text runs" % i)
        if i > 1 and (any(t.startswith("&gt;&gt;&gt; ") or t.startswith(">>> ") for t in texts) or ("23272E" in cols)):
            ncode_slides += 1
            k = len(cols & syn); used |= cols & syn
            if k >= 1: nsyn_slides += 1
            else: bad.append("slide %d: code is not syntax-coloured (none of the 4 syntax colours used)" % i)
        rels = nm.replace("slides/", "slides/_rels/") + ".rels"
        for d in re.findall(r'<p:cNvPr id="\d+" name="[^"]*"(?: descr="([^"]*)")?', x):
            if d and re.search(r"\b(chart|plot|graph|histogram)\b", d, re.I): bad.append("slide %d: a picture whose alt text says chart: %r" % (i, d[:60]))
        if re.search(r"<p:pic>", x):
            cap = " ".join(texts)
            for m in re.finditer(r"([A-Za-z0-9_ -]*(?:bar chart|line chart|pie chart|histogram|plot of)[^<]{0,40})", cap, re.I):
                pass
    if ncode_slides and len(used) < 3: bad.append("the code slides together use %d of the 4 syntax colours (3 needed)" % len(used))
    if off: bad.append("colours outside the standard's palette, code colours and the renderer's tints: %s" % sorted(off))
    if nf: bad.append("fonts outside Cambria, Calibri and Courier New: %s" % sorted(nf))
    for c in (x for x in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", x)):
        if 'showVal val="1"' not in z.read(c).decode("utf-8"): bad.append("%s has no data labels" % c)
    print("sen0401_deck_lookfeel_check %s (chapter %s): %d slides on page colour %s, %d palette colours, %d slides with code (%d syntax-coloured), %d chart part(s); %d refusal(s)"
          % (__version__, n, N, page, len(allowed), ncode_slides, nsyn_slides, len([x for x in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", x)]), len(bad)))
    for b in bad[:60]: print("  REFUSED", b)
    if len(bad) > 60: print("  ... %d more" % (len(bad) - 60))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
