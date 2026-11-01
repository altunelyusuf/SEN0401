#!/usr/bin/env python3
"""Chapter 4 deck v3.6.0, kit (a NEW tool file; task TK_Ch04_DeckTeach_Build): the helpers of the chapter 6 Friday method and of the chapter 3 teaching build (08-tooling/ch06-deck, 08-tooling/ch03-deck) re-exported for the chapter 4 slides,
plus three drawing helpers (horizontal bars, byte strips, stack chips) made of native shapes. Units: 1 unit = 1/100 inch (the slide is 1000 x 562.5 units); the content area is x 50 to 950, y 135 to 495."""
__version__ = "3.6.0"
import copy, hashlib, json, math, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLING = os.path.dirname(HERE)
for p in (HERE, os.path.join(TOOLING, "ch03-deck"), os.path.join(TOOLING, "ch06-deck"), TOOLING):
    if p not in sys.path: sys.path.insert(0, p)
from deck_teach_base_v3_2_0 import *                                   # chapter 3 helpers (which re-export the chapter 6 Friday helpers)
from deck_teach_slides_v3_2_0 import hdr, col_chart, real_bullets, flow, new_slide   # chapter 3 drawing helpers (their SPECS are not used); card, bullets, table, codecard are re-made below with measured text
import sen0401_ch04_lib_v1_0_0 as K
from PIL import ImageFont
X0, XW = 50, 900
_F = {}
def _font(bold, size, mono=False):
    k = (bold, size, mono)
    if k not in _F:
        path = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf" if mono else "/usr/share/fonts/truetype/crosextra/Carlito-%s.ttf" % ("Bold" if bold else "Regular")
        _F[k] = ImageFont.truetype(path, int(round(size * 20)))
    return _F[k]
def mlines(text, size, width_pt, bold=False, mono=False):
    """lines a text sets when word-wrapped into width_pt points. The advance is the SAFER of the real face and the deck checks' model (0.50 em per character proportional, 0.60 em monospace), so no checker estimates a spill"""
    f = _font(bold, size, mono); n = 0; em = (0.60 if mono else 0.50) * size
    adv = lambda w: max(f.getlength(w) / 20.0, len(w) * em)
    for para in text.split("\n"):
        line = 0.0; cnt = 1
        for w in re.findall(r"\S+\s*", para) or [""]:
            ww = adv(w.rstrip()); wf = adv(w)
            if line + ww > width_pt and line > 0: cnt += 1; line = 0.0
            if ww > width_pt: cnt += int(ww // max(width_pt, 1.0)); line = ww % max(width_pt, 1.0)
            else: line += wf
        n += cnt
    return n
def th(text, size, width_units, inset_units=0, bold=False, lh=1.22):
    """height in units of a text of `size` pt in a box width_units wide with the given inset on each side"""
    return mlines(text, size, (width_units - 2 * inset_units) * 0.72, bold) * size * lh / 0.72


def card(s, name, x, y, w, title, body, fill=WHITE, line=TEAL, size=11.5, tcolor=TEAL, minh=0, tsize=12.5):
    h = 8 + th(title, tsize, w, 10, True) + 4 + th(body, size, w, 10) + 10
    h = max(h, minh)
    R(s, name, x, y, w, h, fill=fill, line=line, anchor="t", paras=[P(title, tsize, tcolor, True), P(body, size, INK)], inset=10)
    return y + h


def bullets(s, items, y, size=12, x=X0, w=XW, gap=4, limit=496):
    """bullet lines; when they would run past the limit the size drops to 11 and then 10.5, and the block is lifted so that it ends at the limit"""
    if y is None: y = below(s, x, w) + 8
    for sz in (size, 11, 10.5):
        hs = [th(t, sz, w - 18, 0) + 4 for t in items]
        if y + sum(hs) + gap * (len(items) - 1) <= limit: break
    y = min(y, limit - sum(hs) - gap * (len(items) - 1))
    for t, hh in zip(items, hs):
        T(s, "reading", x, y, w, hh, [{"runs": [("\u25aa  ", sz, ORANGE, True), (t, sz, INK)]}]); y += hh + gap
    return y


def table(s, name, x, y, widths, rows, rh, size=11, hh=26, first_bold=True):
    """a native table whose row heights are measured: every cell's text is word-wrapped into its column with real font metrics, so the frame height equals what is drawn; the attribute .bottom holds the bottom edge in units"""
    tbl = s.shapes.add_table(len(rows), len(widths), Emu(u(x)), Emu(u(y)), Emu(u(sum(widths))), Emu(u(hh + rh * (len(rows) - 1)))); tbl.name = name
    t = tbl.table; tot = 0.0
    for c, w in enumerate(widths): t.columns[c].width = Emu(u(w))
    for r, row_ in enumerate(rows):
        need = hh if r == 0 else rh; lines = 1
        for c, v in enumerate(row_):
            bold = r == 0 or (c == 0 and first_bold)
            lines = max(lines, mlines(v, size, widths[c] * 0.72 - 8.64, bold, mono=False))
            cell = t.cell(r, c); cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else (WHITE if r % 2 else CARD))
            para = cell.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.LEFT
            run = para.add_run(); run.text = v; set_run(run, size, WHITE if r == 0 else INK, bold)
            cell.margin_top = Emu(30000); cell.margin_bottom = Emu(30000); cell.margin_left = Emu(54864); cell.margin_right = Emu(54864); cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        need = max(need, lines * size * 1.22 / 0.72 + 7.5); t.rows[r].height = Emu(u(need)); tot += need
    tbl.height = Emu(u(tot)); tbl.bottom = y + tot
    return tbl


def codecard(s, name, x, y, w, lines, size=10.5):
    """a dark card with coloured, indented Python or text on single lines; named so that it is never read as a chapter code box"""
    h = 14 + len(lines) * size * 1.25 / 0.72 + 4
    R(s, name, x, y, w, h, fill=CODEBG, line=None, adj=0.06)
    text(s, name + " text", x + 14, y + 8, w - 28, h - 12, code_paras(lines, size), anchor="t", wrap=True)
    return y + h


def below(s, x=50, w=900, floor=135):
    """the lowest bottom edge of the content shapes (y from 135 to 500) that overlap the horizontal band x .. x + w"""
    b = floor
    for sh in s.shapes:
        t0 = sh.top / U; b0 = t0 + sh.height / U
        if t0 < 130 or t0 >= 500: continue
        l0 = sh.left / U; r0 = l0 + sh.width / U
        if r0 <= x + 1 or l0 >= x + w - 1: continue
        b = max(b, b0)
    return b
GREY = "B9B0A3"


def hbar(s, name, x, y, w, rows, labw=190, bh=22, gap=9, size=11, hi=None, scale=None, valw=130):
    """horizontal bars: rows of (label, value, shown text); the bar length is value / scale of the room between the label and the value text; returns the y under the last bar"""
    room = w - labw - valw; mx = scale or max(v for _, v, _ in rows)
    for k, (lab, v, shown) in enumerate(rows):
        yy = y + k * (bh + gap)
        T(s, name + " label", x, yy + 1, labw - 8, bh, [P(lab, size, INK, False, align="r")], anchor="m")
        bw = max(3.0, room * v / mx)
        R(s, name + " bar", x + labw, yy, bw, bh, fill=TEAL if k == hi else ORANGE, line=None, adj=0.15)
        T(s, name + " value", x + labw + bw + 8, yy + 1, valw, bh, [P(shown, size, INK, True)], anchor="m")
    return y + len(rows) * (bh + gap)


def strip(s, name, x, y, w, segs, h=40, size=10.5, minw=0):
    """a row of boxes whose widths are proportional to their byte counts; segs = [(label, nbytes, fill, textcolor[, short])]; a label that does not fit the box is replaced by its short form (the full words go in a legend line the slide draws);
    with minw, a part narrower than minw units is drawn minw wide and the others give up the difference in proportion (the slide says so in its legend)"""
    total = sum(sg[1] for sg in segs); raw = [w * sg[1] / total for sg in segs]
    if minw:
        small = [i for i, r in enumerate(raw) if r < minw]; rest = w - minw * len(small); big = sum(raw[i] for i in range(len(raw)) if i not in small)
        raw = [minw if i in small else raw[i] * rest / big for i in range(len(raw))]
    cx = x
    for sg, bw in zip(segs, raw):
        lab, n, fill, tc = sg[:4]; short = sg[4] if len(sg) > 4 else ""
        fits = th(lab, size, bw - 2, 1, True) <= size * 1.3 / 0.72
        R(s, name + " part", cx, y, bw - 2, h, fill=fill, line=None, adj=0.12, paras=[P(lab if fits else short, size, tc, True, align="c")], inset=1)
        cx += bw
    return y + h


def chips(s, name, x, y, items, h=28, w=96, gap=8, size=10.5, top=None):
    """a stack drawn as chips from the bottom (left) to the top (right); the top chip is outlined in orange"""
    for k, (lab, kind) in enumerate(items):
        fill = {"data": CARD, "hash": SOFT, "ok": ORANGE}.get(kind, CARD)
        R(s, name + " chip", x + k * (w + gap), y, w, h, fill=fill, line=ORANGE if k == len(items) - 1 else LINE, lw=2.0 if k == len(items) - 1 else 1.0, adj=0.2,
          paras=[P(lab, size, WHITE if kind == "ok" else INK, True, align="c")], inset=2)


def say(s, x, y, w, text, size=12, color=INK, bold=False, italic=False):
    if y is None: y = below(s, x, w) + 10
    h = th(text, size, w, 0, bold) + 4
    T(s, "reading", x, y, w, h, [P(text, size, color, bold, italic)]); return y + h


def hexs(b, n=4):
    h = b.hex(); return h[:2 * n] + "..." if len(b) > n else h


def b58plain(n):
    out = ""
    while n: n, r = divmod(n, 58); out = K.B58[r] + out
    return out


# ---- fit: grow a text box that the deck checks' own estimates find too short (never shrinks, never moves the top edge) -------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import deck_layout_check_v1_0_0 as _LC, deck_overlap_check_v1_0_0 as _OC
from pptx.enum.text import MSO_ANCHOR
def fit(slide):
    grown = 0
    for sh in slide.shapes:
        if not (sh.has_text_frame and sh.text_frame.text.strip()): continue
        need, have, _ = _LC.estimate(sh)
        (_, _, _, total), spill, room = _OC.text_extent(sh)
        bp = sh.text_frame._txBody.find("{http://schemas.openxmlformats.org/drawingml/2006/main}bodyPr")
        ins = (int(bp.get("tIns", 45720)) + int(bp.get("bIns", 45720))) / 914400.0
        want = max(need + 1.0, (total + ins + 0.01) * 72.0)
        if want > have:
            dh = int((want - have) * 12700); top = sh.top
            if sh.text_frame.vertical_anchor == MSO_ANCHOR.MIDDLE: sh.top = top - dh // 2
            sh.height = sh.height + dh; grown += 1
    return grown


# ---- split30: the deck standard allows 30 words per text box; a longer box keeps its fill and first part, and the rest stands in text boxes under it ----------
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
def _wc(p): return len("".join(t.text or "" for t in p.iter("{%s}t" % A_NS)).split())
def _ptext(p): return "".join(t.text or "" for t in p.iter("{%s}t" % A_NS))
def _sentences(p, limit):
    """split one over-long paragraph element into paragraph elements of at most `limit` words, at sentence ends; the marker run in front stays on the first piece"""
    if _wc(p) <= limit: return [p]
    runs = p.findall("{%s}r" % A_NS)
    big = max(runs, key=lambda r: len((r.find("{%s}t" % A_NS).text or "").split()))
    txt = big.find("{%s}t" % A_NS).text
    sents = [x for x in re.split(r"(?<=[.!?])\s+", txt) if x]
    outs = []; cur = []
    for sn in sents:
        if cur and len(" ".join(cur + [sn]).split()) > limit - (_wc(p) - len(txt.split())): outs.append(" ".join(cur)); cur = []
        cur.append(sn)
    if cur: outs.append(" ".join(cur))
    res = []
    for k, o in enumerate(outs):
        q = copy.deepcopy(p); qr = q.findall("{%s}r" % A_NS); qb = qr[runs.index(big)]
        qb.find("{%s}t" % A_NS).text = o
        if k:
            for r in qr:
                if r is not qb: q.remove(r)
        res.append(q)
    return res

def split30(slide, limit=30):
    n = 0
    for sh in list(slide.shapes):
        if not (sh.has_text_frame and len(sh.text_frame.text.split()) > limit): continue
        if sh.name.startswith(("code", "result")): continue
        tx = sh._element.txBody; ps = tx.findall("{%s}p" % A_NS); units = []
        for p in ps: units += _sentences(p, limit)
        chunks = [[]]; cw = 0
        for u in units:
            w = _wc(u)
            if chunks[-1] and cw + w > limit: chunks.append([]); cw = 0
            chunks[-1].append(u); cw += w
        assert len(chunks) > 1, sh.text_frame.text[:40]
        for p in ps: tx.remove(p)
        for u in chunks[0]: tx.append(u)
        prev = sh; ext = None
        for ci, ch in enumerate(chunks[1:], 1):
            (x0, y0, ww, total), _, _ = _OC.text_extent(prev)
            bp = prev.text_frame._txBody.find("{%s}bodyPr" % A_NS); ti = int(bp.get("tIns", 45720)) / 914400.0
            new = copy.deepcopy(sh._element); slide.shapes._spTree.append(new)
            ids = [int(e.get("id")) for e in slide.shapes._spTree.iter() if e.tag.endswith("}cNvPr") and e.get("id")]
            new.xpath(".//p:cNvPr")[0].set("id", str(max(ids) + 1)); new.xpath(".//p:cNvPr")[0].set("name", sh.name + " more")
            nsh = [s for s in slide.shapes if s._element is new][0]
            ntx = nsh._element.txBody
            for p in ntx.findall("{%s}p" % A_NS): ntx.remove(p)
            for u in ch: ntx.append(copy.deepcopy(u))
            nsh.fill.background(); nsh.line.fill.background()
            top = y0 + total - ti + 0.02
            nsh.top = int(top * 914400); nsh.height = max(int((sh.top + sh.height) - nsh.top), 20 * 9144)
            prev = nsh; n += 1
    return n
