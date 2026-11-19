#!/usr/bin/env python3
"""Apply speech balloons to the concept-card and code slides of chapter 7 or 8 (no new slides) and write the next versions.
Usage: python3 sen0401_ch78_balloons_apply_v1_0_0.py 7|8
Reads the newest deck, page and manifest of the chapter; each output continues from its OWN predecessor by one minor step.
Card slides: a term block on the left, two balloons (one sentence each) on the right.
Code slides: a story balloon beside each code box, the verdict table or chart lower right, two result balloons under the code.
Reader notes of changed slides = the old note without the sentences that the balloons now say, plus one paragraph of further detail."""
import sys, os, re, glob, json, math, importlib.util
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
E = 914400
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); TOOL = os.path.join(REPO, "08-tooling")
def load(name):
    sp = importlib.util.spec_from_file_location(name, os.path.join(TOOL, name + "_v1_0_0.py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
CARDS = load("sen0401_ch78_balloons_cards"); CODE = load("sen0401_ch78_balloons_code")
ch = int(sys.argv[1])
CARD = {7: CARDS.CARDS7, 8: CARDS.CARDS8}[ch]; CEX = {7: CARDS.EXTRA7, 8: CARDS.EXTRA8}[ch]; CODEC = {7: CODE.CODE7, 8: CODE.CODE8}[ch]
INK = RGBColor(0x2B, 0x26, 0x22); ORANGE = RGBColor(0xD9, 0x7A, 0x14); CARDF = RGBColor(0xF2, 0xEC, 0xE1); EDGE = RGBColor(0xDF, 0xD6, 0xC7)
BAL = RGBColor(0xFF, 0xFB, 0xEF); BEDGE = RGBColor(0xE8, 0xB8, 0x78); VOICE = "Trebuchet MS"
WARN = []

def box(s, shape, x, y, w, h, fill, line=None, lw=0.9):
    b = s.shapes.add_shape(shape, Emu(int(x * E)), Emu(int(y * E)), Emu(int(w * E)), Emu(int(h * E)))
    b.fill.solid(); b.fill.fore_color.rgb = fill
    if line is None: b.line.fill.background()
    else: b.line.color.rgb = line; b.line.width = Pt(lw)
    b.shadow.inherit = False; return b
def plain(t): return t.replace("**", "")
def nlines(t, size, w):
    """greedy word wrap estimate for Trebuchet MS (average glyph about 0.54 em; bold slightly wider)"""
    cw = size * 0.54 * 1.03 / 72.0; avail = w - 0.22; lines = 1; cur = 0.0
    for word in plain(t).split():
        L = (len(word) + 1) * cw
        if cur + L > avail + cw and cur > 0: lines += 1; cur = L
        else: cur += L
    return lines
def need_h(t, size, w): return nlines(t, size, w) * size * 1.2 / 72.0 + 0.08
def fit(t, w, h, sizes):
    for sz in sizes:
        if need_h(t, sz, w) <= h: return sz
    WARN.append("text does not fit (%.2f x %.2f): %s" % (w, h, plain(t)[:50])); return sizes[-1]
def text(b, t, size, font=VOICE, bold=False, anchor=MSO_ANCHOR.MIDDLE, m=0.1):
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Emu(int(m * E)); tf.margin_top = tf.margin_bottom = Emu(int(0.03 * E))
    pa = tf.paragraphs[0]; pa.alignment = PP_ALIGN.LEFT
    for i, p in enumerate(t.split("**")):
        if not p: continue
        r = pa.add_run(); r.text = p; r.font.size = Pt(size); r.font.name = font; r.font.bold = bold or (i % 2 == 1); r.font.color.rgb = INK
def balloon(s, x, y, w, h, t, sizes, tail=False, name="Balloon"):
    if tail:
        b = box(s, MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, x, y, w, h, BAL, BEDGE); b.adjustments[0] = -0.56 if w > 4 else -0.6; b.adjustments[1] = 0.0; b.adjustments[2] = 0.16667
    else: b = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, BAL, BEDGE)
    text(b, t, fit(t, w, h, sizes), anchor=MSO_ANCHOR.MIDDLE); b.name = name; return b
def drop(sh): sh._element.getparent().remove(sh._element)
def setpos(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = Emu(int(x * E))
    if y is not None: sh.top = Emu(int(y * E))
    if w is not None: sh.width = Emu(int(w * E))
    if h is not None: sh.height = Emu(int(h * E))

def card_slide(s, n):
    pairs = CARD[n]
    cards = [sh for sh in s.shapes if sh.has_text_frame and sh.name.startswith("Text") and 1.3 * E <= sh.top < 4.98 * E and sh.left < 9.5 * E and sh.text_frame.text.strip()]
    cards.sort(key=lambda sh: (round(sh.top / E, 1), sh.left))
    terms = [c.text_frame.paragraphs[0].text.strip() for c in cards]
    assert len(terms) == len(pairs), (n, len(terms), len(pairs), terms)
    for sh in list(s.shapes):
        if 1.3 * E <= sh.top < 4.98 * E and sh.top + sh.height < 5.0 * E: drop(sh)
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith("Each card"): sh.text_frame.paragraphs[0].runs[0].text = "What each term means, in plain words"
    k = len(pairs); top = 1.36; gap = 0.12
    if k == 4:      # 2 x 2 grid: term block on top of each card, two balloons below it
        cw = 4.4; xs = [0.5, 5.1]; ch_ = (4.92 - top - gap) / 2; th = 0.46
        for idx, (term, (a, b)) in enumerate(zip(terms, pairs)):
            x = xs[idx % 2]; y = top + (idx // 2) * (ch_ + gap)
            tsz = fit(term, cw - 0.2, th, [13, 12, 11, 10.5]); t = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, th, CARDF, EDGE); text(t, term, tsz, "Cambria", True, m=0.2); t.name = "Term"
            bar = box(s, MSO_SHAPE.RECTANGLE, x + 0.02, y + 0.06, 0.06, th - 0.12, ORANGE); bar.name = "Term bar"
            bh = (ch_ - th - 0.16) / 2; sizes = [12, 11.5, 11, 10.5, 10]; sz = min(fit(a, cw, bh, sizes), fit(b, cw, bh, sizes))
            b1 = balloon(s, x, y + th + 0.08, cw, bh, a, [sz], tail=True); b1.adjustments[0] = -0.38; b1.adjustments[1] = -0.66
            b2 = balloon(s, x, y + th + 0.08 + bh + 0.08, cw, bh, b, [sz])
            g = s.shapes.add_group_shape([t, bar, b1, b2]); g.name = "Card: " + term
        return [x for pr in pairs for x in pr]
    rowh = (4.92 - top - gap * (k - 1)) / k; y = top
    tw = 2.55; bx = 0.5 + tw + 0.4; bw = 9.5 - bx
    sizes = {2: [14, 13, 12], 3: [13, 12, 11.5, 11]}[k]
    for term, (a, b) in zip(terms, pairs):
        t = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5, y, tw, rowh, CARDF, EDGE); text(t, term, 15, "Cambria", True, m=0.2); t.name = "Term"
        if need_h(term, 15, tw - 0.2) > rowh: WARN.append("term too long: %s" % term)
        bar = box(s, MSO_SHAPE.RECTANGLE, 0.52, y + 0.1, 0.07, rowh - 0.2, ORANGE); bar.name = "Term bar"
        bh = (rowh - 0.08) / 2; sz = min(fit(a, bw, bh, sizes), fit(b, bw, bh, sizes))
        b1 = balloon(s, bx, y, bw, bh, a, [sz], tail=True); b2 = balloon(s, bx, y + bh + 0.08, bw, bh, b, [sz])
        g = s.shapes.add_group_shape([t, bar, b1, b2]); g.name = "Card: " + term      # one group per card: the card moves as a unit
        y += rowh + gap
    return [x for pr in pairs for x in pr]

def code_slide(s, n):
    story, res, extra = CODEC[n]
    by = {sh.name: sh for sh in s.shapes}; K = sorted(int(m.group(1)) for nm in by for m in [re.match(r"Code box (\d+)$", nm)] if m)
    assert len(K) == len(story), (n, K, len(story))
    # right-hand objects: the verdict table or chart, its label, and the old result sentence
    obj = next((sh for sh in s.shapes if sh.has_table or sh.has_chart), None); assert obj is not None, n
    label = None; olds = []
    for sh in s.shapes:
        if sh is obj or not sh.has_text_frame: continue
        if sh.name.startswith(("Code", "Step", "Explanation", "Run note")): continue
        if 1.2 * E <= sh.top < 4.98 * E and sh.text_frame.text.strip():
            (label := sh) if sh.text_frame.text.startswith("Result:") else olds.append(sh)
    labtxt = label.text_frame.text.strip() if label is not None else "Result"
    for sh in olds + ([label] if label is not None else []): drop(sh)
    for nm in list(by):
        if nm.startswith("Explanation"): drop(by[nm])
    # stack the code boxes; each unit is as high as its box or its story balloon
    maxc = max(len(pa.text) for i in K for pa in by["Code %d" % i].text_frame.paragraphs)
    bw_code = min(5.6, max(3.3, maxc * 0.0795 + 0.35)); RX = 0.5 + bw_code + 0.3; RW = 9.5 - RX
    for i in K:
        setpos(by["Code box %d" % i], w=bw_code); setpos(by["Code %d" % i], w=bw_code - 0.1)
    y = 1.26; units = []
    for i in K:
        lines = len(by["Code %d" % i].text_frame.paragraphs); hb = lines * 0.146 + 0.14
        sb = max(need_h(story[i - 1], sz, 3.2) for sz in [10.5]) if True else 0
        hs = min(max(need_h(story[i - 1], 10.5, RW), 0.46), 0.9); unit = max(hb, hs)
        units.append((y, unit, hb, hs)); y += unit + 0.08
    code_end = y - 0.08
    for i, (yy, unit, hb, hs) in zip(K, units):
        cb, ct, st, sn = by["Code box %d" % i], by["Code %d" % i], by["Step %d" % i], by["Step number %d" % i]
        by0 = yy + (unit - hb) / 2
        by0 = yy + (unit - hb) / 2 if hs > hb else yy
        setpos(cb, y=by0, h=hb); setpos(ct, y=by0 + 0.06, h=hb - 0.1)
        for pa in ct.text_frame.paragraphs:
            for r in pa.runs: r.font.size = Pt(9.5)
        setpos(st, y=by0 - 0.07); setpos(sn, y=by0 - 0.07)
        balloon(s, RX, yy, RW, hs, story[i - 1], [10.5, 10, 9.5, 9], tail=True, name="Story balloon %d" % i)
    # right column: label and the table or chart below the story
    ry = max(yy + hs for (yy, unit, hb, hs) in units) + 0.08; avail = 4.97 - ry - 0.26
    is_chart = obj.has_chart; left_layout = False
    if is_chart and avail < 1.45:
        la = 4.97 - (code_end + 0.08) - 0.26 - 0.24   # chart under the code box instead, balloons on the right
        if la > avail + 0.2: left_layout = True
    rows = 0 if is_chart else len(obj.table.rows)
    if not is_chart:
        rh = min(0.23, avail / rows)
        if rh < 0.19: WARN.append("slide %d: table rows %.2f in" % (n, rh))
    if left_layout:
        cy = code_end + 0.08; lab = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5, cy, bw_code, 0.24, BAL); text(lab, labtxt, 10, bold=True); lab.name = "Result label"
        ch_h = 4.97 - (cy + 0.26) - 0.24; setpos(obj, x=0.5, y=cy + 0.26, w=bw_code, h=ch_h)
        rn = by.get("Run note");
        if rn is not None: setpos(rn, x=0.5, y=4.97 - 0.2, w=5.55, h=0.2)
        h1 = 0.55
        balloon(s, RX, ry + 0.05, RW, h1, res[0], [11, 10.5, 10]); balloon(s, RX, ry + 0.05 + h1 + 0.1, RW, h1, res[1], [11, 10.5, 10])
        if ry + 0.05 + 2 * h1 + 0.1 > 4.97: WARN.append("slide %d: right result balloons low (%.2f)" % (n, ry + 0.05 + 2 * h1 + 0.1))
        return story + res
    lab = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, RX, ry, RW, 0.24, BAL); text(lab, labtxt, 9.5, bold=True); lab.name = "Result label"
    if is_chart:
        setpos(obj, x=RX, y=ry + 0.26, w=RW, h=max(4.97 - ry - 0.26, 0.9))
        if 4.97 - ry - 0.26 < 1.3: WARN.append("slide %d: small chart %.2f in" % (n, 4.97 - ry - 0.26))
    else:
        setpos(obj, x=RX, y=ry + 0.26, w=RW)
        for r in obj.table.rows:
            r.height = Emu(int(rh * E))
            for c in r.cells:
                for pa in c.text_frame.paragraphs:
                    for rn_ in pa.runs: rn_.font.size = Pt(9 if rh >= 0.2 else 8.5)
                c.margin_top = c.margin_bottom = Emu(int(0.02 * E))
    yb = code_end + 0.08; rw2 = (bw_code - 0.1) / 2; rh2 = max(need_h(res[0], 10.5, rw2), need_h(res[1], 10.5, rw2), 0.38)
    balloon(s, 0.5, yb, rw2, rh2, res[0], [10.5, 10, 9.5]); balloon(s, 0.5 + rw2 + 0.1, yb, rw2, rh2, res[1], [10.5, 10, 9.5])
    rn = by.get("Run note")
    if rn is not None: setpos(rn, x=0.5, y=yb + rh2 + 0.05, w=bw_code, h=0.2)
    if yb + rh2 + 0.25 > 5.0: WARN.append("slide %d: left stack ends %.2f" % (n, yb + rh2 + 0.25))
    return story + res

SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
def toks(t): return set(w for w in re.findall(r"[a-z0-9_]+", t.lower()) if len(w) >= 3)
LINK = re.compile(r"[Ss]lide|[Cc]hapter|Compare|[Rr]emember|Keep |BIP|older|Both |Modern|simple way|Bitcoin Core")
def new_note(old, ball, extra, thr=0.75, cards_only=False):
    bt = [toks(plain(b)) for b in ball]; out = []
    for para in old.strip().split("\n\n"):
        keep = []
        for sent in SPLIT.split(para.strip()):
            ts = toks(sent)
            if ts and any(len(ts & b) / len(ts) >= thr for b in bt): continue
            if cards_only and not LINK.search(sent): continue   # card slides: the notes keep the connections, the balloons carry the definitions
            keep.append(sent)
        if keep: out.append(" ".join(keep))
    out.append(extra.strip()); txt = "\n\n".join(out)
    if len(txt.split()) > 140:   # trim: drop old sentences by decreasing overlap with the balloons until the note fits
        sents = [(sn, max((len(toks(sn) & b) / max(len(toks(sn)), 1)) for b in bt)) for pa in out[:-1] for sn in SPLIT.split(pa)]
        for sn, _ in sorted(sents, key=lambda z: -z[1]):
            if len(txt.split()) <= 140: break
            txt = txt.replace(sn, "", 1)
        txt = re.sub(r"[ ]{2,}", " ", re.sub(r"\n\n(\s*\n)+", "\n\n", txt)).strip()
    return txt

def vk(p, ext): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.%s$" % ext, p).groups())
def newest(pat, ext): return sorted(glob.glob(pat), key=lambda p: vk(p, ext))[-1]
D = os.path.join(REPO, "03-materials", "ch0%d" % ch); PD = os.path.join(D, "page"); DD = os.path.join(TOOL, "ch0%d-page" % ch)
deck = newest(os.path.join(D, "SEN0401_Ch0%d_*_3e_v*.pptx" % ch), "pptx"); page = newest(os.path.join(PD, "sen0401_ch0%d_page_v*.html" % ch), "html"); man = newest(os.path.join(PD, "chapter_code_ch0%d_v*.json" % ch), "json")
dv, pv, mv = vk(deck, "pptx"), vk(page, "html"), vk(man, "json")
deck2 = re.sub(r"_v\d+_\d+_\d+\.pptx$", "_v%d_%d_0.pptx" % (dv[0], dv[1] + 1), deck)
page2 = re.sub(r"_v\d+_\d+_\d+\.html$", "_v%d_%d_0.html" % (pv[0], pv[1] + 1), page)
man2 = re.sub(r"_v\d+_\d+_\d+\.json$", "_v%d_%d_0.json" % (mv[0], mv[1] + 1), man)
data2 = os.path.join(DD, "page_data_v%d_%d_0.json" % (pv[0], pv[1] + 1))
OUT = os.environ.get("BALLOON_OUT")   # preview mode: write only the deck there
if not OUT:
    for f in (deck2, page2, man2, data2): assert not os.path.exists(f), f
P = Presentation(deck); say = {}
for n in sorted(set(CARD) | set(CODEC)):
    s = P.slides[n - 1]; old = s.notes_slide.notes_text_frame.text
    if n in CARD:
        ball = card_slide(s, n); ex = CEX[n]
    else:
        ball = code_slide(s, n); ex = CODEC[n][2]
    nn = new_note(old, ball, ex, 0.5 if n in CARD else 0.75, n in CARD); s.notes_slide.notes_text_frame.text = nn
    say[n] = (" ".join(plain(b) for b in ball), nn)
    wc = len(nn.split())
    if not 60 <= wc <= 140: WARN.append("slide %d: note has %d words" % (n, wc))
print("slides changed:", len(say)); print("\n".join(WARN) if WARN else "no layout or note warnings")
if OUT: P.save(OUT); print("preview", OUT); sys.exit(0)
P.save(deck2)
M = json.load(open(man)); M["deck"] = os.path.basename(deck2); M["deck_version"] = "%d.%d.0" % (dv[0], dv[1] + 1); M["manifest"] = os.path.basename(man2)[:-5]
json.dump(M, open(man2, "w"), indent=1, ensure_ascii=False)
H = open(page, encoding="utf-8").read(); tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a)
data = json.loads(H[a:b]); old_ver = data["_version"]; new_ver = "%d.%d.0" % (pv[0], pv[1] + 1)
for L in data["lecture"]:
    if L["n"] in say: L["say"] = say[L["n"]][0] + "\n\n" + say[L["n"]][1]
data["_version"] = new_ver; data["chaptercode"]["file"] = "03-materials/ch0%d/page/%s" % (ch, os.path.basename(man2)); data["chaptercode"]["version"] = "%d.%d.0" % (mv[0], mv[1] + 1)
H2 = H[:a] + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + H[b:]
assert H2.count('<meta name="version" content="%s">' % old_ver) == 1; H2 = H2.replace('<meta name="version" content="%s">' % old_ver, '<meta name="version" content="%s">' % new_ver)
assert "split(/\\n\\n+/)" in H2   # paragraph rendering of notes is already in the predecessor page
open(page2, "w", encoding="utf-8").write(H2); json.dump(data, open(data2, "w"), ensure_ascii=False)
print(os.path.basename(deck2), os.path.basename(page2), os.path.basename(man2), os.path.basename(data2))
