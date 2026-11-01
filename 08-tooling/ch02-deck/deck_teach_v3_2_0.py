#!/usr/bin/env python3
"""Chapter 2 deck v3.2.0 (a NEW tool file; task TK_Ch02_DeckTeach_Build). The deck v3.1.0 is read, never written; its SHA-256 is printed before and after.
It applies the chapter 6 Friday method (08-tooling/ch06-deck: deck_lib and deck_enhance helpers):
 (1) the three true stories are told as sentences with real names, dates and places; the picture and the live source link stay;
 (2) 23 concept slides are added, drawn with native shapes and tables (no pictures of charts), so that every concept node of the page is explained;
 (3) the two lambdas of slides 25 and 30 become def functions (same results, same last expressions); the results of slides 9 and 30 get the full content width;
 (4) no text run below 9 pt (captions, table cells, chart text, the two 7.5 pt results); (5) short speaker notes that carry clues; (6) numbers and the route follow the new order.
Usage: deck_teach_v3_2_0.py OLD NEW"""
__version__ = "3.2.0"
import copy, hashlib, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ch06-deck")); sys.path.insert(0, os.path.dirname(HERE))
from deck_lib_v2_3_0 import *
from deck_enhance_v2_3_0 import P, R, T, A, settext, delete
import deck_teach_content_v3_2_0 as C
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import hashlib as H
import sen0401_ch02_tx_lib_v1_0_0 as TX

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
LINEU = 152400 / U      # one 10 pt code line in units
MONO = "Courier New"


import math
WID = {"Courier New": 0.60, "Cambria": 0.50, "Calibri": 0.48}


def _greedy(par, size, w_pt, adv):
    n = 1; cur = 0.0
    for wd in par.split(" "):
        wl = (len(wd) + 1) * adv * size
        if cur + wl - adv * size > w_pt and cur > 0: n += 1; cur = wl
        else: cur += wl
    return n


def est_h(txt, size, w_units, face="Calibri"):
    """height in UNITS that BOTH estimators of the checks ask for: the layout check (chars per line = (width pt - 4) / (advance * size)) and the overlap check (greedy word wrap, 0.50 em); line 1.22 size, plus 1.5 pt"""
    per = max(1, int((w_units * 0.72 - 4) / (WID[face] * size))); n = 0
    for l in txt.split("\n"):
        n += max(max(1, math.ceil(len(l) / per)), _greedy(l, size, w_units * 0.72 - 1, max(WID[face], 0.5) if face != "Courier New" else 0.6))
    return (n * size * 1.22 + 1.5) / 0.72


# ------------------------------------------------------------------ the code slides: lambdas, widths
def set_code(shape, lines):
    tf = shape.text_frame
    ps = tf._txBody.findall(qn("a:p"))
    for p in ps[1:]: tf._txBody.remove(p)
    p0 = tf.paragraphs[0]
    for r in list(p0._p.findall(qn("a:r"))): p0._p.remove(r)
    first = True
    for runs in code_paras(lines, 10):
        para = p0 if first else tf.add_paragraph(); first = False
        for t, size, color, bold, italic, font in runs:
            r = para.add_run(); r.text = t; set_run(r, size, color, bold, italic, font)
    shape.height = Emu(int(len(lines) * 152400 + 25400))


NEWCODE = {
    25: {"code 25-1": ["data = 'Hello, world! '", "def ok(n, z):", "    return T.sha(data + str(n)).startswith('0' * z)"],
         "code 25-2": ["def find(z):", "    return next(n for n in range(10**7) if ok(n, z))", "[find(z) for z in (1, 2, 3, 4)]"]},
    30: {"code 30-1": ["era = T.HALVING_INTERVAL", "def reward(h):", "    return 50 * T.COIN >> h // era"]},
}


def fix_code(prs):
    log = {}
    for no, boxes in NEWCODE.items():
        s = prs.slides[no - 1]; by = {sh.name: sh for sh in s.shapes}
        for name, lines in boxes.items():
            b = by[name]; old_h = b.height; set_code(b, lines)
            delta = (len(lines) - round((old_h - 18288) / 152400)) * 152400
            if delta:
                frame = [sh for sh in s.shapes if sh.name.startswith("Rounded Rectangle") and abs(sh.left - (b.left - 146304)) < 40000 and abs(sh.top - (b.top - 91440)) < 40000][0]
                frame.height = Emu(frame.height + delta)
                for sh in s.shapes:
                    if sh is b or sh is frame: continue
                    if sh.left < 5700000 and sh.top >= old_top(frame, delta) and sh.top > b.top and sh.top < 495 * U: sh.top = Emu(sh.top + delta)
            log[name] = lines
    return log


def old_top(frame, delta): return frame.top + frame.height - delta


def widen(prs, no, y_card=448):
    """the result of slides 9 and 30 gets the full content width, one line, 10 pt, under the code and the explanation; the right column makes room"""
    s = prs.slides[no - 1]
    for sh in s.shapes:
        if 630 <= sh.left // U <= 700 and 180 <= sh.top // U < 495:
            if sh.has_chart: sh.height = Emu(190 * U)
            elif sh.has_text_frame and sh.top // U > 360: sh.top = Emu(382 * U if no == 30 else 360 * U); sh.height = Emu(58 * U)
    r = [sh for sh in s.shapes if sh.name == "result %d" % no][0]
    r.left = Emu(50 * U); r.width = Emu(900 * U); r.top = Emu(y_card * U); r.height = Emu(30 * U)
    for run in r._element.iter(qn("a:rPr")): run.set("sz", "1000")


def floor_sizes(prs, floor=9.0):
    """no text run below 9 pt: runs, table cells and chart text"""
    n = 0
    for s in prs.slides:
        for el in s._element.iter(qn("a:rPr"), qn("a:endParaRPr"), qn("a:defRPr")):
            v = el.get("sz")
            if v and int(v) < int(floor * 100): el.set("sz", str(int(floor * 100))); n += 1
        for sh in s.shapes:
            if sh.has_chart:
                for el in sh.chart._chartSpace.iter(qn("a:rPr"), qn("a:defRPr"), qn("a:endParaRPr")):
                    v = el.get("sz")
                    if v and int(v) < int(floor * 100): el.set("sz", str(int(floor * 100))); n += 1
    return n


# ------------------------------------------------------------------ stories
def stories(prs):
    for n, (head, paras, lesson) in C.STORY.items():
        s = prs.slides[n - 1]; kill = []
        for sh in s.shapes:
            if sh.has_text_frame and re.match(r"(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b", sh.text_frame.text): kill.append(sh)
        assert len(kill) == 6, n
        for sh in kill: delete(sh)
        x, w = 375, 575
        T(s, "story head", x, 133, w, 20, [P(head, 12, ORANGE, True)]); y = 156
        for p in paras:
            hh = est_lines(p, 11.5, w, 0.49) * 11.5 * 1.2 / 0.72 + 2
            T(s, "story", x, y, w, hh, [P(p, 11.5, INK)]); y += hh + 3
        ly = y + 2; lh = est_lines(lesson, 12, w - 20, 0.55) * 12 * 1.2 / 0.72 + 19
        assert ly + lh <= 449, (n, ly, lh)
        R(s, "lesson", x, ly, w, lh, fill=SOFT, line=TEAL, paras=[P(lesson, 12, INK, True)], inset=10)


# ------------------------------------------------------------------ building blocks for the concept slides
def new_slide(prs, src, title, sub, take):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for sh in list(s.shapes): delete(sh)
    bg = src._element.cSld.find(qn("p:bg"))
    if bg is not None: s._element.cSld.insert(0, copy.deepcopy(bg))
    for sh in src.shapes:
        Tp = sh.top // U
        if Tp < 125 or Tp >= 500: s.shapes._spTree.append(copy.deepcopy(sh._element))
    for sh in s.shapes:
        L, Tp = sh.left // U, sh.top // U
        if L == 125 and Tp == 26:
            settext(sh, title); sh.text_frame.paragraphs[0].runs[0].font.size = Pt(28 if len(title) <= 32 else (24 if len(title) <= 40 else 21))
        elif L == 125 and Tp == 88: settext(sh, sub)
        elif L == 72 and Tp == 503: settext(sh, take)
        elif L == 860 and Tp == 508: sh.name = "number"
    return s


def node(s, name, x, y, w, h, label, fill=CARD, line=LINE, color=INK, size=11, bold=False, align="c", lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, inset=4):
    paras = [P(l, size, color, bold, align=align) for l in label.split("\n")]
    return R(s, name, x, y, w, h, fill=fill, line=line, paras=paras, adj=0.12, lw=lw, inset=inset, shape=shape)


def mono(s, name, x, y, w, h, txt, size=10.5, color=INK, fill=WHITE, line=LINE):
    return R(s, name, x, y, w, h, fill=fill, line=line, paras=[P(txt, size, color, False, font=MONO, align="c")], adj=0.1, inset=3)


def lab(s, x, y, w, txt, size=11, color=MUTE, bold=False, italic=False, align="l", h=None):
    h = h or est_h(txt, size, w)
    return T(s, "label", x, y, w, h, [P(txt, size, color, bold, italic, align=align)])


def need_h(item, w, size=11):
    return 5 + est_h(item[1] + ". " + item[2], size, w - 26) + 2 + est_h("Think of " + item[3] + ".", 10.5, w - 26) + 4


def concept(s, x, y, w, item, size=11, h=None):
    nid, name, text, think = item
    h1 = est_h(name + ". " + text, size, w - 26); ha = est_h("Think of " + think + ".", 10.5, w - 26)
    need = 5 + h1 + 2 + ha + 4; h = max(h or 0, need)
    R(s, "card " + nid, x, y, w, h, fill=WHITE, line=LINE, adj=0.05)
    R(s, "bar " + nid, x, y + 6, 5, h - 12, fill=TEAL, line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "concept " + nid, x + 16, y + 5, w - 26, h1, [{"runs": [(name + ". ", size, TEAL, True), (text, size, INK)]}])
    T(s, "analogy " + nid, x + 16, y + 5 + h1 + 2, w - 26, ha, [P("Think of " + think + ".", 10.5, MUTE, False, True)])
    return need


def hx(b): return H.sha256(b).hexdigest()


# ------------------------------------------------------------------ the 23 pictures
def v_S1(s):
    sc = 0.0084; x0 = 110
    lab(s, 40, 138, 700, "Alice's one input and two outputs, drawn to scale (satoshis)", 12, INK, True)
    node(s, "in label", 40, 168, 64, 40, "In", fill=INK, line=None, color=WHITE, bold=True, size=12)
    node(s, "in bar", x0, 168, 100000 * sc, 40, "input Tx1:0  ·  100,000", fill=TEAL, line=None, color=WHITE, bold=True, size=12)
    node(s, "out label", 40, 224, 64, 40, "Out", fill=INK, line=None, color=WHITE, bold=True, size=12)
    node(s, "out bob", x0, 224, 75000 * sc, 40, "output to Bob's Store  ·  75,000", fill="5F8F86", line=None, color=WHITE, bold=True, size=12)
    node(s, "out change", x0 + 75000 * sc, 224, 20000 * sc, 40, "change 20,000", fill=SOFT, line=TEAL, color=INK, bold=True, size=10.5, inset=1)
    node(s, "out fee", x0 + 95000 * sc, 224, 5000 * sc, 40, "", fill=ORANGE, line=None)
    lab(s, x0 + 95000 * sc - 120, 268, 150, "fee 5,000 (implied)", 11, ORANGE, True, align="r")
    node(s, "sum", 40, 262, 520, 30, "100,000 in  =  75,000 + 20,000 out  +  5,000 fee", fill=CREAM, line=LINE, size=12, bold=True)


def v_S3(s):
    lab(s, 40, 135, 440, "The coins: outputs no later input has spent", 12, INK, True)
    for i, (o, v) in enumerate((("Tx1:1", 500000), ("Tx2:0", 20000), ("Tx3:0", 67000))):
        node(s, "utxo " + o, 40 + i * 150, 164, 140, 62, "%s\n%s sat" % (o, format(v, ",")), fill=SOFT, line=TEAL, bold=True, size=12)
    lab(s, 40, 232, 440, "Together they are the unspent output set that every full node keeps.", 11, MUTE, False, True)
    lab(s, 500, 135, 460, "An outpoint names one of them: txid, colon, number", 12, INK, True)
    shown = TX.PREV_RAW and bytes.fromhex(TX.PREV_RAW)[::-1].hex()
    node(s, "txid", 500, 164, 250, 44, shown[:8] + "…" + shown[-5:], fill=TEAL, line=None, color=WHITE, bold=True, size=13)
    node(s, "colon", 752, 164, 30, 44, ":", fill=CREAM, line=None, bold=True, size=18)
    node(s, "index", 784, 164, 70, 44, "1", fill=ORANGE, line=None, color=WHITE, bold=True, size=14)
    lab(s, 500, 212, 250, "transaction id, 32 bytes", 10.5, MUTE, align="c"); lab(s, 770, 212, 100, "output no.", 10.5, MUTE, align="c")
    node(s, "stored", 500, 246, 250, 36, TX.PREV_RAW[:8] + "…" + TX.PREV_RAW[-5:], fill=WHITE, line=LINE, bold=True, size=12)
    A(s, "reverse", 735, 210, 735, 246, ORANGE, 2.0)
    lab(s, 758, 244, 200, "stored form: the same bytes in reverse order", 10.5, ORANGE, True)


def v_S2(s):
    sc = 1.7
    lab(s, 40, 135, 440, "Alice's transaction: 194 bytes on the wire", 12, INK, True)
    node(s, "plain", 40, 160, 125 * sc, 38, "125 plain bytes", fill=TEAL, line=None, color=WHITE, bold=True, size=11.5)
    node(s, "wit", 40 + 125 * sc, 160, 69 * sc, 38, "69 witness", fill=ORANGE, line=None, color=WHITE, bold=True, size=11, inset=1)
    rows = [("125 × 4 + 69 × 1", "weight 569"), ("569 ÷ 4, rounded up", "143 virtual bytes"), ("5,000 ÷ 143", "34.97 sat per vbyte")]
    for i, (a, b) in enumerate(rows):
        y = 218 + i * 84
        node(s, "calc %d" % i, 40, y, 200, 44, a, fill=WHITE, line=LINE, size=12)
        A(s, "calc arrow %d" % i, 244, y + 22, 288, y + 22, ORANGE, 2.0)
        node(s, "res %d" % i, 292, y, 188, 44, b, fill=SOFT, line=TEAL, bold=True, size=12)
        if i < 2: A(s, "down %d" % i, 386, y + 46, 386, y + 82, MUTE, 1.2)


def v_S4(s):
    lab(s, 40, 135, 440, "The output is a lock, the input brings the key", 12, INK, True)
    node(s, "out box", 40, 164, 210, 86, "Output of Tx2\n75,000 satoshis\nscript: “needs Bob's signature”", fill=CARD, line=TEAL, size=11.5, lw=1.5)
    node(s, "in box", 270, 164, 210, 86, "Input of Bob's payment\npoints at Tx2:1\nsignature of Bob", fill=CARD, line=ORANGE, size=11.5, lw=1.5)
    A(s, "unlock", 268, 207, 252, 207, ORANGE, 2.0)
    node(s, "true", 190, 262, 110, 30, "TRUE: spend", fill=SOFT, line=TEAL, bold=True, size=11.5)
    lab(s, 40, 304, 440, "The whole transaction written as one run of bytes", 12, INK, True)
    fields = [("version", 4, TEAL), ("inputs", 8, "5F8F86"), ("outputs", 8, ORANGE), ("witness", 6, "B5651D"), ("lock time", 4, MUTE)]
    x = 40
    for nm, wt, col in fields:
        w = wt * 14.5; node(s, "field " + nm, x, 332, w, 44, nm, fill=col, line=WHITE, color=WHITE, bold=True, size=10.5, inset=1); x += w
    lab(s, 40, 382, 440, "Sent, hashed and stored in exactly this order; the sizes here are only schematic.", 11, MUTE, False, True)


def v_C1(s):
    a, b = "Alice pays Bob 75,000", "Alice pays Bob 75,001"
    lab(s, 40, 138, 440, "One digit changes, the whole fingerprint changes", 12, INK, True)
    for i, t in enumerate((a, b)):
        y = 166 + i * 62
        node(s, "msg %d" % i, 40, y, 190, 44, t, fill=WHITE, line=LINE, size=11.5)
        A(s, "h arrow %d" % i, 232, y + 22, 262, y + 22, ORANGE, 2.0)
        mono(s, "digest %d" % i, 266, y, 214, 44, hx(t.encode())[:16] + "…", 11, TEAL)
    lab(s, 40, 292, 440, "SHA-256 gives 64 hex digits whatever the input; the first 16 are shown.", 10.5, MUTE, False, True)
    lab(s, 500, 138, 460, "Easy one way, impossible the other", 12, INK, True)
    node(s, "priv", 500, 170, 150, 50, "private key\n256-bit secret", fill=INK, line=None, color=WHITE, bold=True, size=11)
    node(s, "pub", 810, 170, 150, 50, "public key\na curve point", fill=TEAL, line=None, color=WHITE, bold=True, size=11)
    A(s, "easy", 652, 186, 808, 186, ORANGE, 2.5); lab(s, 652, 164, 156, "multiply: easy", 10.5, ORANGE, True, align="c")
    A(s, "hard", 808, 210, 652, 210, MUTE, 1.5, dash=True); lab(s, 652, 214, 156, "undo: infeasible", 10.5, MUTE, True, align="c")
    node(s, "addr", 810, 258, 150, 36, "address (a digest)", fill=SOFT, line=TEAL, size=10.5)
    A(s, "to addr", 885, 222, 885, 256, TEAL, 1.5)


def v_C2(s):
    lab(s, 40, 135, 440, "Signing and checking", 12, INK, True)
    node(s, "sm", 40, 164, 130, 44, "message", fill=WHITE, line=LINE, size=11.5); node(s, "sk", 40, 214, 130, 36, "private key", fill=INK, line=None, color=WHITE, size=11.5, bold=True)
    A(s, "sign", 172, 200, 240, 200, ORANGE, 2.0)
    node(s, "sig", 244, 178, 110, 44, "signature", fill=ORANGE, line=None, color=WHITE, bold=True, size=11.5)
    node(s, "vm", 40, 266, 130, 36, "message + signature", fill=WHITE, line=LINE, size=10.5, inset=1); node(s, "vk", 40, 306, 130, 34, "public key", fill=TEAL, line=None, color=WHITE, size=11.5, bold=True)
    A(s, "check", 172, 300, 240, 300, ORANGE, 2.0)
    node(s, "ok", 244, 276, 110, 44, "valid, or not", fill=SOFT, line=TEAL, bold=True, size=11.5)
    lab(s, 40, 352, 440, "A checksum is a short digest kept with the data (sha-256 twice, first 4 bytes):", 11, MUTE, False, True)
    for i, t in enumerate(("pay Bob 75000", "pay Bob 75001")):
        d = H.sha256(H.sha256(t.encode()).digest()).hexdigest()[:8]
        node(s, "cs txt %d" % i, 40, 392 + i * 40, 200, 34, t, fill=WHITE, line=LINE, size=11.5); mono(s, "cs %d" % i, 250, 392 + i * 40, 150, 34, d, 12, ORANGE if i else TEAL)
    node(s, "enc", 372, 160, 108, 112, "Signing is not hiding: every transaction is public", fill=CREAM, line=ORANGE, size=10.5, inset=4)


def v_C3(s):
    lab(s, 40, 135, 440, "One byte, three ways: 0xEB", 12, INK, True)
    rows = [("bits", "1110 1011"), ("hexadecimal", "E  B"), ("decimal", "235")]
    for i, (a, b) in enumerate(rows):
        node(s, "bl %d" % i, 40, 162 + i * 38, 120, 32, a, fill=CARD, line=LINE, size=11.5, bold=True)
        mono(s, "bv %d" % i, 164, 162 + i * 38, 190, 32, b, 13)
    node(s, "ent", 40, 282, 440, 24, "", fill=None, line=None)
    lab(s, 370, 160, 110, "8 bits = 1 byte = 2 hex digits", 10.5, MUTE, False, True, h=60)
    lab(s, 500, 135, 460, "A nonce changes the hash of 'Hello, world! ' + n", 12, INK, True)
    for i, n in enumerate((31, 32, 33)):
        d = TX.sha("Hello, world! " + str(n)); ok = d.startswith("0")
        mono(s, "n %d" % n, 500, 162 + i * 38, 70, 32, "n = %d" % n, 11)
        mono(s, "h %d" % n, 574, 162 + i * 38, 270, 32, d[:20] + "…", 11.5, WHITE if ok else INK, TEAL if ok else WHITE, TEAL if ok else LINE)
        if ok: lab(s, 850, 168, 110, "starts with 0", 11, TEAL, True)
    lab(s, 500, 282, 460, "Entropy: 256 bits are about 77 decimal digits of possibilities (2^256 is roughly 1.16 × 10^77).", 11, MUTE, False, True)


def v_L1(s):
    lab(s, 40, 135, 440, "The chain of figure 2-3 (satoshis); grey is spent, teal is a coin", 11.5, INK, True)
    ch = TX.CHAIN; spent = {i for a, b in ch.values() for i in a}
    for k, (tx, (ins, outs)) in enumerate(ch.items()):
        x = 40 + k * 150
        node(s, "tx " + tx, x, 170, 130, 34, tx, fill=INK, line=None, color=WHITE, bold=True, size=12)
        for j, (o, v) in enumerate(outs.items()):
            used = o in spent
            node(s, "o " + o, x, 212 + j * 54, 130, 46, "%s\n%s" % (o, format(v, ",")), fill=CARD if used else SOFT, line=LINE if used else TEAL, color=MUTE if used else INK, bold=not used, size=11.5)
        if k < 2: A(s, "chain %d" % k, x + 132, 235, x + 148, 235, ORANGE, 2.0)
    lab(s, 40, 336, 440, "Tx2 pays 75,000 to Bob and returns 20,000 to Alice as change; its fee is 100,000 − 95,000 = 5,000.", 11, MUTE, False, True)
    lab(s, 40, 392, 440, "Coin selection chooses which unspent output feeds the next transaction.", 11, MUTE, False, True)


def v_L2(s):
    forms = TX.FORMS; names = {"payment": "Payment", "consolidation": "Consolidation", "batching": "Batching"}
    x = 40
    for k, (ins, outs) in forms.items():
        lab(s, x, 137, 290, names[k], 12.5, INK, True)
        yi = 166
        for v in ins:
            node(s, "in %s %d" % (k, v), x, yi, 84, 28, format(v, ","), fill=TEAL, line=None, color=WHITE, bold=True, size=11); yi += 31
        A(s, "arr " + k, x + 88, 200, x + 118, 200, ORANGE, 2.0)
        yo = 166
        for v in outs:
            node(s, "out %s %d" % (k, v), x + 124, yo, 84, 28, format(v, ","), fill="5F8F86", line=None, color=WHITE, bold=True, size=11); yo += 31
        lab(s, x + 214, 190, 90, "fee\n%s" % format(sum(ins) - sum(outs), ","), 11, ORANGE, True)
        x += 310
    lab(s, 40, 292, 920, "Inputs on the left, outputs on the right, in satoshis; 100,000,000 satoshis make one bitcoin.", 11, MUTE, False, True)


def v_P2(s):
    steps = [("price in dollars", CARD, INK), ("÷ exchange rate at checkout", CARD, INK), ("0.01577764 bitcoin", SOFT, INK), ("× 100,000,000", CARD, INK), ("1,577,764 satoshis", SOFT, INK), ("output locked to Bob's address", TEAL, WHITE)]
    w = 138
    for i, (t, f, c) in enumerate(steps):
        x = 40 + i * (w + 18.4)
        node(s, "step %d" % i, x, 170, w, 70, t, fill=f, line=LINE if f != TEAL else None, color=c, bold=True, size=11.5)
        if i < 5: A(s, "sa %d" % i, x + w + 1, 205, x + w + 17, 205, ORANGE, 2.0)
    lab(s, 40, 256, 920, "The amount in Bob's payment link is exactly the middle box; the wallet converts it to whole satoshis before it builds the output.", 11, MUTE, False, True)


def v_N1(s):
    full = [(150, 158), (270, 138), (360, 192), (240, 226), (130, 226)]
    light = [(60, 148), (440, 160), (430, 236)]
    pts = full + light
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 3), (1, 3), (5, 0), (6, 2), (7, 2)]
    for a, b in edges:
        A(s, "link", pts[a][0] + 15, pts[a][1] + 15, pts[b][0] + 15, pts[b][1] + 15, MUTE, 1.2, head=False)
    for i, (x, y) in enumerate(pts):
        if i < 5: node(s, "full %d" % i, x, y, 34, 34, "", fill=TEAL, line=WHITE, shape=MSO_SHAPE.OVAL)
        else: node(s, "light %d" % i, x, y, 30, 30, "", fill=ORANGE, line=WHITE, shape=MSO_SHAPE.OVAL)
    node(s, "lg1", 500, 170, 24, 24, "", fill=TEAL, line=None, shape=MSO_SHAPE.OVAL); lab(s, 530, 170, 430, "full node: checks every rule, keeps every block", 11.5, INK)
    node(s, "lg2", 500, 210, 24, 24, "", fill=ORANGE, line=None, shape=MSO_SHAPE.OVAL); lab(s, 530, 210, 430, "lightweight client: keeps keys, asks nodes for proofs", 11.5, INK)
    lab(s, 500, 250, 460, "Lines are connections between peers. There is no server in the middle.", 11.5, MUTE, False, True)


def v_N2(s):
    lab(s, 40, 135, 440, "One signed transaction, hop by hop", 12, INK, True)
    node(s, "wallet", 180, 156, 120, 40, "Alice's wallet", fill=ORANGE, line=None, color=WHITE, bold=True, size=11)
    for i in range(3):
        node(s, "hop1 %d" % i, 80 + i * 130, 230, 90, 34, "node", fill=TEAL, line=None, color=WHITE, bold=True, size=11); A(s, "a1 %d" % i, 240, 197, 125 + i * 130, 229, MUTE, 1.2)
    for i in range(6):
        node(s, "hop2 %d" % i, 45 + i * 73, 306, 62, 32, "node", fill="5F8F86", line=None, color=WHITE, bold=True, size=10.5, inset=1)
        A(s, "a2 %d" % i, 125 + (i // 2) * 130, 265, 76 + i * 73, 305, MUTE, 1.0)
    node(s, "miners", 130, 372, 220, 40, "miners pick it up", fill=SOFT, line=TEAL, bold=True, size=11.5)
    lab(s, 40, 420, 440, "Every node checks the transaction before it forwards it.", 11, MUTE, False, True)


def v_N3(s):
    lab(s, 40, 135, 440, "A node's memory pool, best fee rate first (toy numbers)", 11.5, INK, True)
    pool = [("tx a", 52), ("tx b", 35), ("Alice's tx", 34.97), ("tx d", 12), ("tx e", 4)]
    for i, (n, r) in enumerate(pool):
        inb = i < 3
        node(s, "pool " + n, 40, 164 + i * 44, 260, 36, "%s  ·  %s sat/vB" % (n, r), fill=SOFT if inb else CARD, line=TEAL if inb else LINE, bold=inb, size=11.5)
    R(s, "next block", 312, 160, 18, 134, fill=TEAL, line=None, adj=0.4)
    lab(s, 336, 205, 150, "fits the next block", 11, TEAL, True)
    lab(s, 336, 340, 150, "waits for a later one", 11, MUTE, True)
    node(s, "explorer", 40, 396, 440, 40, "explorer: paste a txid → block, depth, fee", fill=WHITE, line=ORANGE, size=11.5, lw=1.5)


def v_M1(s):
    lab(s, 40, 135, 440, "The header: 80 bytes", 12, INK, True)
    hdr = [("version", 4), ("previous block", 32), ("merkle root", 32), ("time", 4), ("target (bits)", 4), ("nonce", 4)]
    for i, (n, b) in enumerate(hdr):
        node(s, "hf " + n, 40, 160 + i * 25, 250, 23, "%s  ·  %d bytes" % (n, b), fill=TEAL if i != 5 else ORANGE, line=WHITE, color=WHITE, size=10.5, bold=True, inset=1)
    lab(s, 520, 135, 440, "The body: the transactions", 12, INK, True)
    for i, t in enumerate(("coinbase transaction (pays the miner)", "Alice's transaction", "other transactions…")):
        node(s, "bt %d" % i, 520, 160 + i * 38, 400, 32, t, fill=SOFT if i == 0 else CARD, line=TEAL if i == 0 else LINE, size=11.5)
    A(s, "to root", 292, 217, 518, 217, ORANGE, 1.5, dash=True)
    lab(s, 296, 190, 220, "summarised by the root", 10.5, ORANGE, True)


def v_X1(s):
    blocks = [("0", "genesis"), ("…", ""), ("277,316", "Alice's block\n1 confirmation"), ("277,317", "2"), ("277,318", "3")]
    node(s, "pending", 40, 180, 150, 84, "mempool\n0 confirmations", fill=CARD, line=ORANGE, size=11, lw=1.5)
    A(s, "to chain", 192, 222, 236, 222, ORANGE, 2.0)
    for i, (h, t) in enumerate(blocks):
        x = 240 + i * 145
        col = TEAL if i != 2 else ORANGE
        node(s, "blk %d" % i, x, 180, 130, 84, "height\n" + h, fill=col, line=None, color=WHITE, bold=True, size=11.5)
        if t: lab(s, x - 5, 270, 140, t, 10.5, INK, True, align="c")
        if i < 4: A(s, "ba %d" % i, x - 14, 222, x - 2, 222, MUTE, 1.2)
    lab(s, 40, 140, 920, "Height counts blocks from the genesis block; confirmations count blocks from Alice's block upwards.", 11.5, MUTE, False, True)


def merkle_hash(a, b): return H.sha256(H.sha256(a + b).digest()).digest()


def v_M2(s):
    lab(s, 40, 134, 440, "Four transactions, one root", 12, INK, True)
    leaves = [H.sha256(H.sha256(t).digest()).digest() for t in (b"tx A", b"tx B", b"tx C", b"tx D")]
    l2 = [merkle_hash(leaves[0], leaves[1]), merkle_hash(leaves[2], leaves[3])]; root = merkle_hash(l2[0], l2[1])
    for i, lf in enumerate(leaves): node(s, "leaf %d" % i, 40 + i * 112, 248, 104, 38, "tx %s %s" % ("ABCD"[i], lf.hex()[:6]), fill=CARD, line=LINE, size=10.5, inset=1)
    for i, h in enumerate(l2):
        node(s, "mid %d" % i, 92 + i * 224, 200, 104, 28, h.hex()[:8], fill=SOFT, line=TEAL, size=10.5)
        for j in (0, 1): A(s, "ma %d%d" % (i, j), 92 + (2 * i + j) * 112, 247, 144 + i * 224, 229, MUTE, 1.0)
    node(s, "root", 205, 154, 130, 28, "root " + root.hex()[:8], fill=TEAL, line=None, color=WHITE, bold=True, size=11)
    for i in (0, 1): A(s, "ra %d" % i, 144 + i * 224, 199, 268, 183, MUTE, 1.0)
    lab(s, 500, 134, 460, "Proof of work: the hash must fall below the target", 12, INK, True)
    g = TX.block_hash(TX.genesis_header())
    node(s, "target", 500, 160, 460, 32, "target    00000000ffff\u2026", fill=WHITE, line=ORANGE, size=12, lw=1.5)
    node(s, "genesis hash", 500, 198, 460, 32, "genesis hash  " + g[:12] + "\u2026", fill=SOFT, line=TEAL, size=12, bold=True)
    lab(s, 500, 236, 460, "Difficulty 1: about 4.3 billion hashes per block,", 11.5, INK)
    lab(s, 500, 256, 460, "roughly 7 million hashes per second over 600 s.", 11.5, INK)


def v_X2(s):
    lab(s, 40, 135, 440, "A fork resolved by the next block", 12, INK, True)
    for i in range(3): node(s, "base %d" % i, 40 + i * 90, 190, 70, 40, "block", fill=TEAL, line=None, color=WHITE, size=11, bold=True)
    for i in range(2): A(s, "bb %d" % i, 112 + i * 90, 210, 128 + i * 90, 210, MUTE, 1.2)
    A(s, "to a", 222, 205, 308, 170, MUTE, 1.2); A(s, "to b", 222, 215, 308, 262, MUTE, 1.2)
    node(s, "alt a", 310, 150, 70, 40, "A", fill=TEAL, line=None, color=WHITE, bold=True, size=12); node(s, "alt b", 310, 242, 70, 40, "B", fill=CARD, line=LINE, color=MUTE, bold=True, size=12)
    A(s, "a next", 382, 170, 406, 170, MUTE, 1.2); node(s, "next", 408, 150, 70, 40, "next", fill=ORANGE, line=None, color=WHITE, bold=True, size=11)
    lab(s, 310, 288, 170, "B is left behind; its transactions return to the pool.", 10.5, MUTE, False, True)
    lab(s, 40, 346, 440, "Double spend: two transactions, one output", 12, INK, True)
    node(s, "ds1", 40, 372, 200, 34, "Tx1:0 → Bob's Store", fill=SOFT, line=TEAL, bold=True, size=11.5); node(s, "ds2", 40, 412, 200, 34, "Tx1:0 → Alice again", fill=CARD, line=LINE, color=MUTE, size=11.5)
    lab(s, 250, 378, 230, "enters block A, so the best chain keeps it", 11, TEAL, True); lab(s, 250, 418, 230, "refused: the output is already spent", 11, MUTE, True)


def v_X3(s):
    lab(s, 40, 135, 440, "Chance that an attacker ever catches up (the white paper's formula, rerun)", 11.5, INK, True)
    rows = [("confirmations", "10% of hash power", "30% of hash power")]
    for z in (0, 1, 2, 4, 6): rows.append((str(z), "%.7f" % TX.catch_up(0.1, z), "%.7f" % TX.catch_up(0.3, z)))
    tbl = s.shapes.add_table(len(rows), 3, Emu(40 * U), Emu(182 * U), Emu(440 * U), Emu(240 * U)); tbl.name = "catch-up table"
    t = tbl.table
    for c, w in enumerate((130, 155, 155)): t.columns[c].width = Emu(w * U)
    for r, row in enumerate(rows):
        t.rows[r].height = Emu(40 * U)
        for c, v in enumerate(row):
            cell = t.cell(r, c); cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else (WHITE if r % 2 else CARD))
            run = cell.text_frame.paragraphs[0].add_run(); run.text = v; set_run(run, 11.5, WHITE if r == 0 else INK, r == 0 or c == 0)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    lab(s, 40, 428, 440, "Example choices: a coffee 0, a laptop 3, a car 6 confirmations.", 11, MUTE, False, True)


def v_M3(s):
    lab(s, 40, 135, 290, "The coinbase transaction", 12, INK, True)
    node(s, "cb in", 40, 166, 130, 44, "input: none\n(coinbase text)", fill=CARD, line=LINE, size=10.5, inset=2)
    A(s, "cb arr", 172, 188, 198, 188, ORANGE, 2.0)
    node(s, "cb out", 200, 166, 120, 44, "reward + fees\nto the miner", fill=TEAL, line=None, color=WHITE, bold=True, size=10.5, inset=2)
    lab(s, 40, 218, 290, "It is where new coins are created.", 11, MUTE, False, True)
    lab(s, 350, 135, 270, "Hard to solve, instant to check", 12, INK, True)
    grid = [[1, 3, 0, 4], [4, 0, 1, 3], [0, 4, 3, 1], [3, 1, 4, 0]]
    for r in range(4):
        for c in range(4):
            v = grid[r][c]
            node(s, "sd %d%d" % (r, c), 350 + c * 32, 166 + r * 32, 30, 30, str(v) if v else "", fill=CARD if v else WHITE, line=LINE if v else ORANGE, bold=True, size=12, inset=0)
    lab(s, 350, 298, 270, "A 4 by 4 sudoku: empty cells are filled by trial, a full grid is checked at a glance.", 10.5, MUTE, False, True)
    lab(s, 650, 135, 310, "A mining pool", 12, INK, True)
    for i in range(3): node(s, "pm %d" % i, 650, 166 + i * 38, 90, 30, "miner %d" % (i + 1), fill=CARD, line=LINE, size=11); A(s, "pa %d" % i, 742, 181 + i * 38, 786, 220, MUTE, 1.2)
    node(s, "pool", 788, 196, 90, 50, "pool", fill=ORANGE, line=None, color=WHITE, bold=True, size=12)
    lab(s, 650, 285, 310, "The reward is shared by shares proved.", 11, MUTE, False, True)


def v_M4(s):
    lab(s, 40, 135, 440, "What every full node checks", 12, INK, True)
    for i, t in enumerate(("proof of work below the target", "no output above its inputs", "coinbase not above the reward", "block within the size limit")):
        node(s, "chk %d" % i, 40, 160 + i * 42, 440, 37, "✓  " + t, fill=SOFT if i != 1 else WHITE, line=TEAL, size=11.5, align="l", inset=10)
    lab(s, 40, 332, 440, "Soft and hard forks, as sets of valid blocks", 12, INK, True)
    R(s, "hard", 40, 358, 440, 118, fill=CARD, line=ORANGE, lw=1.5, adj=0.06); lab(s, 52, 362, 400, "hard fork: wider set, old nodes split away", 10.5, ORANGE, True)
    R(s, "old", 90, 392, 340, 74, fill=WHITE, line=MUTE, adj=0.08); lab(s, 100, 396, 300, "old rules", 10.5, MUTE, True)
    R(s, "soft", 160, 424, 200, 34, fill=SOFT, line=TEAL, paras=[P("soft fork: narrower", 10.5, INK, True, align="c")], adj=0.1, inset=2)


def v_Y1(s):
    lab(s, 40, 135, 440, "Spending onward: the chain grows by one link", 12, INK, True)
    for i, t in enumerate(("Joe", "Alice", "Bob", "Gopesh")):
        node(s, "p " + t, 40 + i * 112, 164, 96, 34, t, fill=TEAL if t != "Bob" else ORANGE, line=None, color=WHITE, bold=True, size=11.5)
        if i < 3: A(s, "pa %d" % i, 138 + i * 112, 181, 150 + i * 112, 181, MUTE, 1.5)
    lab(s, 40, 204, 440, "Bob pays Gopesh 67,000 of the 75,000 he received; the fee is 8,000.", 11, MUTE, False, True)
    lab(s, 40, 250, 440, "A short proof: 3 hashes for 8 transactions", 11.5, INK, True)
    xc = lambda i: 40 + i * 55 + 25
    l1 = [(xc(2 * j) + xc(2 * j + 1)) / 2 for j in range(4)]; l2 = [(l1[2 * k] + l1[2 * k + 1]) / 2 for k in range(2)]; top = (l2[0] + l2[1]) / 2
    for i in range(8): node(s, "t%d" % i, xc(i) - 25, 376, 50, 24, "tx%d" % (i + 1), fill=ORANGE if i == 2 else (SOFT if i == 3 else CARD), line=TEAL if i == 3 else LINE, size=10, color=WHITE if i == 2 else INK, bold=i == 2, inset=0)
    for j in range(4): node(s, "h1%d" % j, l1[j] - 25, 340, 50, 24, "hash", fill=SOFT if j == 0 else CARD, line=TEAL if j == 0 else LINE, size=10, inset=0)
    for k in range(2): node(s, "h2%d" % k, l2[k] - 25, 306, 50, 24, "hash", fill=SOFT if k == 1 else CARD, line=TEAL if k == 1 else LINE, size=10, inset=0)
    node(s, "root", top - 55, 272, 110, 24, "root in header", fill=TEAL, line=None, color=WHITE, bold=True, size=10.5, inset=0)
    for i in range(8): A(s, "e0%d" % i, xc(i), 376, l1[i // 2], 364, MUTE, 0.8, head=False)
    for j in range(4): A(s, "e1%d" % j, l1[j], 340, l2[j // 2], 330, MUTE, 0.8, head=False)
    for k in range(2): A(s, "e2%d" % k, l2[k], 306, top, 296, MUTE, 0.8, head=False)
    lab(s, 40, 406, 440, "Orange: the payment. Teal: the hashes a lightweight client is sent.", 10.5, MUTE, False, True)


def v_Y2(s):
    node(s, "e2", 40, 190, 150, 54, "Entity\noutput Tx2:1", fill=SOFT, line=TEAL, bold=True, size=11.5)
    node(s, "act", 40, 300, 150, 54, "Activity\ntransaction Tx2", fill=CARD, line=ORANGE, bold=True, size=11.5, lw=1.5)
    node(s, "e1", 300, 300, 160, 54, "Entity\noutput Tx1:0", fill=SOFT, line=TEAL, bold=True, size=11.5)
    node(s, "ag", 300, 190, 160, 54, "Agent\nAlice's key holder", fill=CARD, line=MUTE, bold=True, size=11.5)
    A(s, "gen", 115, 300, 115, 246, ORANGE, 2.0); lab(s, 120, 262, 90, "generated by", 10.5, ORANGE, True, h=18)
    A(s, "used", 192, 328, 298, 328, ORANGE, 2.0); lab(s, 196, 306, 100, "used", 10.5, ORANGE, True)
    A(s, "assoc", 192, 308, 300, 244, MUTE, 1.5); lab(s, 306, 250, 150, "associated with", 10.5, MUTE, True, h=20)
    lab(s, 40, 142, 440, "Each arrow is one triple: subject, predicate, object", 12, INK, True)
    lab(s, 40, 380, 440, "Tx2:1  generated by  Tx2;  Tx2  used  Tx1:0;  Tx2  associated with  Alice.", 11, MUTE, False, True)


def v_Y3(s):
    items = C.C["Y3"]
    for i, it in enumerate(items):
        x = 40 + i * 185; y = 300 - i * 24
        node(s, "stair %d" % i, x, y, 175, 24 + i * 24 + 20, "page %d" % (i + 1), fill=[ "5F8F86", TEAL, TEAL, "B5651D", ORANGE][i], line=None, color=WHITE, bold=True, size=12)
    # the ladder is the picture; the concept cards sit below


VIS = {"S1": v_S1, "S3": v_S3, "S2": v_S2, "S4": v_S4, "C1": v_C1, "C2": v_C2, "C3": v_C3, "L1": v_L1, "L2": v_L2, "P2": v_P2, "N1": v_N1, "N2": v_N2, "N3": v_N3, "M1": v_M1, "X1": v_X1,
       "M2": v_M2, "X2": v_X2, "X3": v_X3, "M3": v_M3, "M4": v_M4, "Y1": v_Y1, "Y2": v_Y2, "Y3": v_Y3}



# revised card layout and changed pictures
def cards_B(s, items, y0=298):
    wd = 450; rows = [items[0:2], items[2:4]]; y = y0
    for r in rows:
        h = max(need_h(it, wd) for it in r)
        for x, it in zip((40, 510), r): concept(s, x, y, wd, it, h=h)
        y += h + 4
    assert y - 4 <= 498, ("cards B too tall", y)


def cards_A(s, items, x=505, y0=133, bottom=498):
    wd = 455; n = len(items); hs = [need_h(it, wd) for it in items]; gap = 5
    spare = (bottom - y0 - gap * (n - 1)) - sum(hs); assert spare >= -1, ("cards A too tall", spare)
    extra = max(0, spare) / n; y = y0
    for it, h in zip(items, hs): concept(s, x, y, wd, it, h=h + min(extra, 30)); y += h + min(extra, 30) + gap


def cards_D(s, items, y0=256):
    w = 176; hs = [need_h(it, w) for it in items]; h = max(hs)
    assert y0 + h <= 498, ("cards D too tall", y0 + h)
    for i, it in enumerate(items): concept(s, 40 + i * 184, y0, w, it, h=h)


def v_S1(s):
    sc = 0.0084; x0 = 110
    lab(s, 40, 134, 700, "Alice's one input and two outputs, drawn to scale (satoshis)", 12, INK, True)
    node(s, "in label", 40, 158, 64, 34, "In", fill=INK, line=None, color=WHITE, bold=True, size=12)
    node(s, "in bar", x0, 158, 100000 * sc, 34, "input Tx1:0  ·  100,000", fill=TEAL, line=None, color=WHITE, bold=True, size=12)
    node(s, "out label", 40, 200, 64, 34, "Out", fill=INK, line=None, color=WHITE, bold=True, size=12)
    node(s, "out bob", x0, 200, 75000 * sc, 34, "output to Bob's Store  ·  75,000", fill="5F8F86", line=None, color=WHITE, bold=True, size=12)
    node(s, "out change", x0 + 75000 * sc, 200, 20000 * sc, 34, "change 20,000", fill=SOFT, line=TEAL, color=INK, bold=True, size=10.5, inset=1)
    node(s, "out fee", x0 + 95000 * sc, 200, 5000 * sc, 34, "", fill=ORANGE, line=None)
    lab(s, x0 + 95000 * sc - 140, 236, 180, "fee 5,000 (implied)", 11, ORANGE, True, align="r")
    node(s, "sum", 40, 252, 520, 30, "100,000 in  =  75,000 + 20,000 out  +  5,000 fee", fill=CREAM, line=LINE, size=12, bold=True)


def v_C1(s):
    a, b = "Alice pays Bob 75,000", "Alice pays Bob 75,001"
    lab(s, 40, 134, 440, "One digit changes, the whole fingerprint changes", 12, INK, True)
    for i, t in enumerate((a, b)):
        y = 158 + i * 50
        node(s, "msg %d" % i, 40, y, 190, 40, t, fill=WHITE, line=LINE, size=11.5)
        A(s, "h arrow %d" % i, 232, y + 20, 262, y + 20, ORANGE, 2.0)
        mono(s, "digest %d" % i, 266, y, 214, 40, hx(t.encode())[:16] + "…", 11, TEAL)
    lab(s, 40, 262, 440, "SHA-256 gives 64 hex digits for any input; 16 are shown.", 10.5, MUTE, False, True)
    lab(s, 500, 134, 460, "Easy one way, impossible the other", 12, INK, True)
    node(s, "priv", 500, 162, 150, 46, "private key\n256-bit secret", fill=INK, line=None, color=WHITE, bold=True, size=11)
    node(s, "pub", 810, 162, 150, 46, "public key\na curve point", fill=TEAL, line=None, color=WHITE, bold=True, size=11)
    A(s, "easy", 652, 178, 808, 178, ORANGE, 2.5); lab(s, 652, 156, 156, "multiply: easy", 10.5, ORANGE, True, align="c")
    A(s, "hard", 808, 198, 652, 198, MUTE, 1.5, dash=True); lab(s, 652, 202, 156, "undo: infeasible", 10.5, MUTE, True, align="c")
    node(s, "addr", 810, 240, 150, 32, "address (a digest)", fill=SOFT, line=TEAL, size=10.5)
    A(s, "to addr", 885, 210, 885, 238, TEAL, 1.5)


def v_C3(s):
    lab(s, 40, 134, 440, "One byte, three ways: 0xEB", 12, INK, True)
    for i, (a, b) in enumerate((("bits", "1110 1011"), ("hexadecimal", "E  B"), ("decimal", "235"))):
        node(s, "bl %d" % i, 40, 158 + i * 36, 120, 30, a, fill=CARD, line=LINE, size=11.5, bold=True)
        mono(s, "bv %d" % i, 164, 158 + i * 36, 190, 30, b, 13)
    lab(s, 360, 158, 120, "8 bits = 1 byte = 2 hex digits", 10.5, MUTE, False, True, h=60)
    lab(s, 500, 134, 460, "A nonce changes the hash of 'Hello, world! ' + n", 12, INK, True)
    for i, n in enumerate((31, 32, 33)):
        d = TX.sha("Hello, world! " + str(n)); ok = d.startswith("0")
        mono(s, "n %d" % n, 500, 158 + i * 36, 70, 30, "n = %d" % n, 11)
        mono(s, "h %d" % n, 574, 158 + i * 36, 270, 30, d[:20] + "…", 11.5, WHITE if ok else INK, TEAL if ok else WHITE, TEAL if ok else LINE)
        if ok: lab(s, 850, 163, 110, "starts with 0", 11, TEAL, True)
    lab(s, 40, 272, 920, "Entropy: 256 bits are about 77 decimal digits of possibilities (2^256 is roughly 1.16 × 10^77).", 11, MUTE, False, True)


def v_L2(s):
    names = {"payment": "Payment", "consolidation": "Consolidation", "batching": "Batching"}
    x = 40
    for k, (ins, outs) in TX.FORMS.items():
        lab(s, x, 134, 290, names[k], 12.5, INK, True)
        yi = 158
        for v in ins: node(s, "in %s %d" % (k, v), x, yi, 84, 25, format(v, ","), fill=TEAL, line=None, color=WHITE, bold=True, size=11, inset=1); yi += 28
        A(s, "arr " + k, x + 88, 196, x + 118, 196, ORANGE, 2.0)
        yo = 158
        for v in outs: node(s, "out %s %d" % (k, v), x + 124, yo, 84, 25, format(v, ","), fill="5F8F86", line=None, color=WHITE, bold=True, size=11, inset=1); yo += 28
        lab(s, x + 214, 180, 90, "fee\n%s" % format(sum(ins) - sum(outs), ","), 11, ORANGE, True, h=40)
        x += 310
    lab(s, 40, 276, 920, "Inputs left, outputs right, in satoshis; 100,000,000 satoshis make one bitcoin.", 11, MUTE, False, True)


def v_X1(s):
    lab(s, 40, 134, 920, "Height counts blocks from the genesis block; confirmations count blocks from Alice's block upwards.", 11.5, MUTE, False, True)
    blocks = [("0", "genesis"), ("…", ""), ("277,316", "Alice's block: 1"), ("277,317", "2"), ("277,318", "3")]
    node(s, "pending", 40, 164, 150, 70, "mempool\n0 confirmations", fill=CARD, line=ORANGE, size=11, lw=1.5)
    A(s, "to chain", 192, 199, 236, 199, ORANGE, 2.0)
    for i, (h, t) in enumerate(blocks):
        x = 240 + i * 145
        node(s, "blk %d" % i, x, 164, 128, 70, "height\n" + h, fill=ORANGE if i == 2 else TEAL, line=None, color=WHITE, bold=True, size=11.5)
        if t: lab(s, x - 5, 240, 138, t, 11, INK, True, align="c", h=20)
        if i < 4: A(s, "ba %d" % i, x - 14, 199, x - 2, 199, MUTE, 1.2)


def v_M1(s):
    lab(s, 40, 134, 440, "The header: 80 bytes", 12, INK, True)
    hdr = [("version", 4), ("previous block", 32), ("merkle root", 32), ("time", 4), ("target (bits)", 4), ("nonce", 4)]
    for i, (n, b) in enumerate(hdr):
        node(s, "hf " + n, 40, 156 + i * 23, 250, 21, "%s  ·  %d bytes" % (n, b), fill=TEAL if i != 5 else ORANGE, line=WHITE, color=WHITE, size=10.5, bold=True, inset=0)
    lab(s, 520, 134, 440, "The body: the transactions", 12, INK, True)
    for i, t in enumerate(("coinbase transaction (pays the miner)", "Alice's transaction", "other transactions…")):
        node(s, "bt %d" % i, 520, 158 + i * 36, 400, 30, t, fill=SOFT if i == 0 else CARD, line=TEAL if i == 0 else LINE, size=11.5)
    A(s, "to root", 292, 205, 518, 205, ORANGE, 1.5, dash=True)
    lab(s, 300, 182, 215, "summarised by the root", 10.5, ORANGE, True, h=18)


def v_M3(s):
    lab(s, 40, 134, 290, "The coinbase transaction", 12, INK, True)
    node(s, "cb in", 40, 164, 130, 44, "input: none\n(coinbase text)", fill=CARD, line=LINE, size=10.5, inset=2)
    A(s, "cb arr", 172, 186, 198, 186, ORANGE, 2.0)
    node(s, "cb out", 200, 164, 120, 44, "reward + fees\nto the miner", fill=TEAL, line=None, color=WHITE, bold=True, size=10.5, inset=2)
    lab(s, 40, 216, 290, "It is where new coins are created.", 11, MUTE, False, True, h=18)
    lab(s, 350, 134, 270, "Hard to solve, instant to check", 12, INK, True)
    grid = [[1, 3, 0, 4], [4, 0, 1, 3], [0, 4, 3, 1], [3, 1, 4, 0]]
    for r in range(4):
        for c in range(4):
            v = grid[r][c]
            node(s, "sd %d%d" % (r, c), 350 + c * 30, 158 + r * 30, 28, 28, str(v) if v else "", fill=CARD if v else WHITE, line=LINE if v else ORANGE, bold=True, size=12, inset=0)
    lab(s, 480, 160, 150, "Empty cells are found by trial; a full grid is checked at a glance.", 10.5, MUTE, False, True, h=82)
    lab(s, 650, 134, 310, "A mining pool", 12, INK, True)
    for i in range(3): node(s, "pm %d" % i, 650, 158 + i * 34, 90, 28, "miner %d" % (i + 1), fill=CARD, line=LINE, size=11); A(s, "pa %d" % i, 742, 172 + i * 34, 786, 206, MUTE, 1.2)
    node(s, "pool", 788, 182, 90, 50, "pool", fill=ORANGE, line=None, color=WHITE, bold=True, size=12)
    lab(s, 650, 264, 310, "The reward is shared by shares proved.", 11, MUTE, False, True, h=18)


def v_P1(s):
    lab(s, 40, 134, 920, "Bob's invoice link, taken apart", 12, INK, True)
    u = TX.INVOICE; addr = u.split(":")[1].split("?")[0]
    parts = [("bitcoin:", "scheme", INK, 100), (addr[:12] + "…" + addr[-4:], "address of Bob's Store", TEAL, 250), ("?", "", MUTE, 22), ("amount=0.01577764", "how much", ORANGE, 190), ("&", "", MUTE, 22), ("label=Bob%27s%20Store", "name the payer sees", "5F8F86", 250)]
    x = 40
    for t, cap, col, w in parts:
        mono(s, "seg " + t[:6], x, 164, w, 44, t, 11, WHITE, col, col)
        if cap: lab(s, x, 214, w, cap, 10.5, MUTE, False, True, align="c", h=18)
        x += w + 4
    lab(s, 40, 252, 920, "A QR code on the checkout page holds this same text, so the camera replaces the typing.", 11, MUTE, False, True)


def v_Y3(s):
    for i in range(5):
        h = 30 + i * 20
        node(s, "stair %d" % i, 40 + i * 184, 245 - h, 176, h, "page %d" % (i + 1), fill=["5F8F86", TEAL, TEAL, "B5651D", ORANGE][i], line=None, color=WHITE, bold=True, size=12)
    lab(s, 40, 134, 920, "Each page keeps everything of the one before and adds one idea", 12, INK, True, h=20)


VIS.update({"S1": v_S1, "C1": v_C1, "C3": v_C3, "L2": v_L2, "X1": v_X1, "M1": v_M1, "M3": v_M3, "P1": v_P1, "Y3": v_Y3})


# ------------------------------------------------------------------ assembly
def renumber(prs, N):
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): settext(sh, "%d / %d" % (i, N))


def build(old_path, new_path):
    prs = Presentation(old_path)
    old = list(prs.slides); assert len(old) == 35
    codelog = fix_code(prs); widen(prs, 9); widen(prs, 30)
    stories(prs)
    src = old[11]; newslides = {}; table = []
    for key, title, sub, take, lay, after, group in C.SLIDES:
        s = new_slide(prs, src, title, sub, take); VIS[key](s); items = C.C[key]
        if lay == "B": cards_B(s, items)
        elif lay == "D": cards_D(s, items)
        else: cards_A(s, items)
        s.notes_slide.notes_text_frame.text = C.NOTES_NEW[key]
        newslides.setdefault(after, []).append((key, s)); table.append((key, title, group, items))
    for i, s in enumerate(old, 1): s.notes_slide.notes_text_frame.text = C.NOTES_OLD[i]
    floor_n = floor_sizes(prs)
    lst = prs.slides._sldIdLst; ids = list(lst)
    by_slide = {sl.slide_id: el for sl, el in zip(list(prs.slides), ids)}
    order = []
    for i, sl in enumerate(old, 1):
        order.append(by_slide[sl.slide_id])
        for key, ns in newslides.get(i, []): order.append(by_slide[ns.slide_id])
    for el in ids: lst.remove(el)
    for el in order: lst.append(el)
    prs.part.rename_slide_parts([el.rId for el in lst])
    N = len(order); renumber(prs, N)
    newpos = {sl.slide_id: k for k, sl in enumerate(prs.slides, 1)}; oldpos = {i: newpos[sl.slide_id] for i, sl in enumerate(old, 1)}
    parts = [(3, 4), (5, 9), (10, 16), (17, 19), (20, 22), (23, 28), (29, 32), (33, 35)]
    k = 0
    for sh in prs.slides[1].shapes:
        if not sh.has_text_frame: continue
        tx = sh.text_frame.text.strip()
        if len(sh.text_frame.paragraphs) > 1 and re.fullmatch(r"\(slides \d+-\d+\)", sh.text_frame.paragraphs[-1].text):
            a, b = parts[k]; k += 1
            nxt = oldpos[parts[k][0]] if k < len(parts) else N + 1
            sh.text_frame.paragraphs[-1].runs[0].text = "(slides %d-%d)" % (oldpos[a], nxt - 1)
        elif tx == "35": settext(sh, str(N))
        elif tx == "slides, numbered bottom-right": settext(sh, "slides, 24 of them concept pictures")
    assert k == 8, k
    prs.core_properties.version = "3.2.0"
    prs.save(new_path)
    return N, oldpos, {key: newpos[s.slide_id] for v in newslides.values() for key, s in v}, floor_n, codelog


def main(old, new):
    before = sha(old); print("SHA-256 old deck before:", before)
    N, oldpos, newpos, floor_n, codelog = build(old, new)
    after = sha(old); print("SHA-256 old deck after: ", after, "UNCHANGED" if before == after else "CHANGED")
    assert before == after
    print("wrote", new, sha(new), "slides", N, "runs raised to 9 pt:", floor_n)
    LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_teach_v3_2_0_logs"); os.makedirs(LOGS, exist_ok=True)
    json.dump({"slides": N, "new": newpos, "old_to_new": oldpos, "old_sha256": before, "new_sha256": sha(new), "code_changed": codelog}, open(os.path.join(LOGS, "map.json"), "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
