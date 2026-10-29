"""STEP 2 of the chapter 6 deck v2.3.0 (a NEW tool file): the enhancement. Runs on the presentation already corrected by step 1 (deck_derive_v2_3_0.py) and does, in this order:
(1) the four true stories are told as sentences with real names, dates and places (no 'WHAT:' or 'WHO' labels), the picture and the live source link stay;
(2) nine picture slides are added, one for each part, drawn with native shapes and tables (no pictures of charts), each with three short reading lines, an everyday comparison and a takeaway strip;
(3) every slide gets short speaker notes with explanation clues (deck_notes_v2_3_0.py);
(4) the slide numbers 'n / N', the agenda ranges and the counters of the route slide follow the new order.
Units: 1 unit = 1/1000 of the slide width."""
__version__ = "2.3.0"
import copy, os, re, sys
sys.dont_write_bytecode = True
from deck_lib_v2_3_0 import *
import deck_notes_v2_3_0 as NT
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from lxml import etree

FIELD = {"version": ("2F6D62", WHITE), "marker": (ORANGE, WHITE), "flag": ("F2A860", INK), "input": (INK, WHITE), "output": ("5F8F86", WHITE), "witness": ("B5651D", WHITE), "lock": (MUTE, WHITE)}
BYTES = [("version", 4), ("marker", 1), ("flag", 1), ("input", 42), ("output", 75), ("witness", 67), ("lock", 4)]


def P(t, size=11, color=INK, bold=False, italic=False, font="Calibri", align="l", space=0):
    return {"runs": [(t, size, color, bold, italic, font)], "align": align, "space": space}


def R(s, name, x, y, w, h, fill=None, line=None, paras=None, anchor="m", adj=0.08, lw=1.0, inset=4, shape=MSO_SHAPE.ROUNDED_RECTANGLE, wrap=True):
    sp = box(s, name, x, y, w, h, fill=fill, line=line, shape=shape, adj=adj, lw=lw)
    if paras: text(s, name, 0, 0, 0, 0, paras, anchor=anchor, wrap=wrap, inset=inset, shape=sp)
    return sp


def T(s, name, x, y, w, h, paras, anchor="t", wrap=True):
    return text(s, name, x, y, w, h, paras, anchor=anchor, wrap=wrap)


def A(s, name, x1, y1, x2, y2, color=INK, w=1.5, head=True, dash=False):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1 * U)), Emu(int(y1 * U)), Emu(int(x2 * U)), Emu(int(y2 * U))); c.name = name
    c.line.color.rgb = rgb(color); c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    if dash:
        d = etree.SubElement(ln, qn("a:prstDash")); d.set("val", "dash")
    if head:
        e = etree.SubElement(ln, qn("a:tailEnd")); e.set("type", "triangle"); e.set("w", "med"); e.set("len", "med")
    return c


def bullets(s, items, y, h=None, size=12):
    """one text box per reading line (the deck standard allows at most 30 words in a box)"""
    for t in items:
        n = est_lines(t, size, 900, 0.5); hh = n * size * 1.2 / 0.72 + 6
        T(s, "reading", 40, y, 920, hh, [{"runs": [("\u25aa  ", size, ORANGE, True), (t, size, INK)]}]); y += hh + 3


# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORY = {
    10: ("12 January 2009 · Finney's computer in California · block 170",
         ["On 11 January 2009 the cryptographer Hal Finney posted two words, \u201crunning bitcoin\u201d. The next day, 12 January, the software's author, Satoshi Nakamoto, sent him 10 bitcoins.",
          "The payment went into block 170. Finney had started the software the day before, and it tested the network with real money.",
          "It was the first transaction ever to spend an output: its one input points at the coinbase of block 9.",
          "Its two outputs pay 10 BTC to Finney and 40 BTC back to the sender."],
         "It is a legacy transaction, with no marker, no flag and no witness, so the format this chapter reads is the one from block 170."),
    22: ("22 May 2010 · Jacksonville, Florida · block 57,043",
         ["On 18 May 2010 the programmer Laszlo Hanyecz offered 10,000 bitcoins on the bitcointalk forum to anyone who would send him two pizzas.",
          "Four days later he reported that the deal was done: the forum user jercos had ordered them from a Papa John's on Atlantic Avenue.",
          "The payment confirmed in block 57,043 with 131 inputs, because his wallet had gathered mining rewards of 50 BTC each, and one output of 10,000 BTC.",
          "The remaining 0.99 BTC was the fee, and the community still marks 22 May as Pizza Day."],
         "An input count of 131 is what a one-output payment can look like: a wallet must list every coin it spends."),
    35: ("15 August 2010 · block 74,638 · the bitcointalk forum",
         ["On 15 August 2010 block 74,638 contained a transaction with two outputs of 92 billion bitcoins each, 184 billion in all.",
          "Added as 64-bit integers, the amounts wrapped around to a small negative number, so the check that outputs do not exceed inputs passed.",
          "Jeff Garzik reported the strange block on the forum within two hours, and Satoshi Nakamoto patched the software within about five.",
          "The honest chain overtook the bad one at block 74,691 and erased the transaction."],
         "A signed amount needs a range check: Bitcoin Core's tx_check.cpp still cites the bug, CVE-2010-5139."),
    43: ("10 February 2014 · Shibuya, Tokyo · Zurich",
         ["On 7 February 2014 Mt. Gox, then the largest bitcoin exchange, led by Mark Karpeles in Shibuya, Tokyo, halted withdrawals.",
          "On 10 February it blamed transaction malleability for the missing bitcoins: a stranger can re-encode an input script and change the txid.",
          "Software that tracks payments by txid then believes the payment failed.",
          "Christian Decker and Roger Wattenhofer of ETH Zurich, who had recorded a year of network traffic, found that only 1,811 BTC were hit before the press release.",
          "On 28 February the exchange filed for bankruptcy protection, 850,000 BTC short."],
         "Track outpoints, not txids: segregated witness took the input script out of the txid for good in 2017."),
}


def stories(prs):
    for n, (head, paras, lesson) in STORY.items():
        s = prs.slides[n - 1]; kill = []; link_pair = []
        for sh in s.shapes:
            L, Tp = sh.left // U, sh.top // U
            t = sh.text_frame.text if sh.has_text_frame else ""
            if 330 <= L <= 372 and 135 < Tp < 420: kill.append(sh)               # the four WHAT/WHY/HOW/SO WHAT beats and their diamond bullets
            if 440 <= Tp <= 500 and L < 860: link_pair.append(sh)               # the fact row
        for sh in kill: delete(sh)
        keep = [sh for sh in link_pair if sh.has_text_frame and sh.text_frame.text.startswith("READ")]
        assert len(keep) == 1, n
        rt = keep[0]; bg = [sh for sh in link_pair if not sh.has_text_frame or not sh.text_frame.text.strip()]
        bgk = [b for b in bg if b.left // U == rt.left // U - 10][0]
        for sh in link_pair:
            if sh is not rt and sh is not bgk: delete(sh)
        dx = 340 * U - bgk.left
        for sh in (bgk, rt): sh.left += dx
        bgk.width = Emu(620 * U); rt.width = Emu(600 * U)
        T(s, "story", 340, 133, 620, 16, [P(head, 11, ORANGE, True)]); y = 154
        for p in paras:
            hh = est_lines(p, 12, 620, 0.5) * 12 * 1.2 / 0.72 + 4
            T(s, "story", 340, y, 620, hh, [P(p, 12, INK)]); y += hh + 3
        assert y <= 390, (n, y)
        R(s, "lesson", 340, 391, 620, 54, fill=SOFT, line=TEAL, paras=[P(lesson, 12, INK, True)], inset=10)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# picture slides
# ------------------------------------------------------------------------------------------------------------------------------------------------
def settext(shape, t):
    p = shape.text_frame.paragraphs[0]
    for r in p.runs[1:]: r._r.getparent().remove(r._r)
    p.runs[0].text = t
    for extra in shape.text_frame.paragraphs[1:]: extra._p.getparent().remove(extra._p)


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
        if L == 125 and Tp == 26: settext(sh, title)
        elif L == 125 and Tp == 86: settext(sh, sub)
        elif L == 72 and Tp == 503: settext(sh, take)
        elif L == 860 and Tp == 508: sh.name = "number"
    return s


def d1(s):
    x0, sc = 40, 920 / 194
    T(s, "caption 1", 40, 207, 700, 18, [P("Extended serialization, as it travels on the network: 194 bytes", 11.5, INK, True)])
    x = x0; pos = {}
    for nm, n in BYTES:
        w = n * sc; pos[nm] = (x, w); f, tc = FIELD[nm]
        lab = [P("%s · %d B" % (nm, n), 11, tc, True, align="c")] if w > 90 else None
        R(s, "field " + nm, x, 150, w, 50, fill=f, line=WHITE, paras=lab, adj=0.0, lw=1.0, shape=MSO_SHAPE.RECTANGLE)
        x += w
    T(s, "label version", 40, 128, 100, 16, [P("version · 4 B", 10, INK, True)])
    T(s, "label marker", 150, 128, 190, 16, [P("marker 1 B and flag 1 B", 10, INK, True)])
    A(s, "tick marker", 61.5, 150, 150, 142, MUTE, 0.75, head=False)
    T(s, "label lock", 800, 128, 160, 16, [P("lock time · 4 B", 10, INK, True, align="r")])
    A(s, "tick lock", 950, 142, 950, 150, MUTE, 0.75, head=False)
    # legacy strip
    x = x0; T(s, "caption 2", 40, 304, 700, 18, [P("Legacy serialization: 125 bytes, the bytes the txid hashes", 11.5, INK, True)])
    for nm, n in BYTES:
        if nm in ("marker", "flag", "witness"): continue
        w = n * sc; f, tc = FIELD[nm]
        R(s, "legacy " + nm, x, 247, w, 50, fill=f, line=WHITE, paras=([P("%s · %d B" % (nm, n), 11, tc, True, align="c")] if w > 90 else None), adj=0.0, shape=MSO_SHAPE.RECTANGLE)
        x += w
    R(s, "gap note", 40 + 125 * sc + 14, 247, 920 - 125 * sc - 14, 50, fill=CARD, line=LINE, paras=[P("69 bytes fewer: marker, flag and witness are left out", 11, ORANGE, True, align="c")])
    bullets(s, ["The long strip is the transaction as it travels: seven fields, always in the same order, 194 bytes in all.",
                "The short strip leaves out marker, flag and witness. Those 125 bytes are what the txid hashes.",
                "Think of a letter with a signed slip tucked in at the end: the slip travels with the letter, but the tracking number ignores it."], 340, size=14)


def d2(s):
    cells = [("01", "version"), ("00", "version"), ("00", "version"), ("00", "version"), ("00", "marker"), ("01", "flag")]
    for i, (b, k) in enumerate(cells):
        f, tc = FIELD[k]
        R(s, "byte %d" % (i + 1), 60 + 68 * i, 150, 64, 64, fill=f, line=None, paras=[P(b, 22, tc, True, font="Courier New", align="c")])
    T(s, "label version", 60, 222, 268, 34, [P("version = 1", 12, INK, True, align="c"), P("four bytes, small end first", 10, MUTE, True, align="c")])
    T(s, "label marker", 328, 222, 68, 34, [P("marker", 11, ORANGE, True, align="c"), P("00", 10, MUTE, align="c")])
    T(s, "label flag", 396, 222, 68, 34, [P("flag", 11, ORANGE, True, align="c"), P("01", 10, MUTE, align="c")])
    R(s, "old parser", 520, 135, 440, 80, fill=CARD, line=LINE, paras=[P("A legacy parser", 12, INK, True), P("Reads 00 as an input count of zero, finds an empty transaction and stops.", 11.5, INK)], inset=10)
    R(s, "new parser", 520, 230, 440, 80, fill=SOFT, line=TEAL, paras=[P("A segwit parser", 12, TEAL, True), P("Sees marker 00 and flag 01, knows that a witness follows, then reads the real input count.", 11.5, INK)], inset=10)
    A(s, "arrow old", 466, 182, 518, 175, MUTE, 1.5); A(s, "arrow new", 466, 190, 518, 270, TEAL, 1.5)
    R(s, "little endian", 60, 264, 404, 54, fill=WHITE, line=ORANGE, paras=[P("Little-endian: the number 1 is written 01 00 00 00, the small end first.", 11, INK, True)], inset=8)
    bullets(s, ["Four bytes of version come first, then a marker of 00 and a flag of 01.",
                "No real transaction has zero inputs, so a zero where the input count would be is a signal, not data.",
                "Think of the edition number printed on a form, and a fragile label stuck on the parcel."], 340, size=14)


def d3(s):
    R(s, "earlier tx", 40, 135, 300, 150, fill=CARD, line=LINE, paras=None)
    T(s, "earlier title", 52, 140, 280, 20, [P("An earlier transaction", 12, INK, True)])
    R(s, "output 0", 52, 168, 276, 40, fill=WHITE, line=LINE, paras=[P("output 0 · 18,210,494 satoshis", 11, MUTE)])
    R(s, "output 1", 52, 222, 276, 50, fill=WHITE, line=ORANGE, lw=2.0, paras=[P("output 1 · 100,000 satoshis", 11.5, INK, True), P("the coin Alice spends", 10, MUTE, italic=True)])
    R(s, "input card", 390, 190, 250, 80, fill=SOFT, line=TEAL, paras=[P("Alice's input", 12, TEAL, True), P("points at that txid and index 1; it states no amount", 11, INK)], inset=10)
    A(s, "arrow input", 388, 247, 330, 247, ORANGE, 2.0)
    R(s, "outpoint txid", 40, 298, 240, 34, fill="2F6D62", line=None, paras=[P("32 bytes: the earlier txid", 10.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "outpoint index", 280, 298, 60, 34, fill=ORANGE, line=None, paras=[P("4 B: 1", 10.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "outpoint label", 40, 335, 300, 16, [P("an outpoint: 36 bytes", 10.5, MUTE, True, italic=True)])
    T(s, "compact title", 670, 133, 290, 18, [P("CompactSize: bytes a count takes", 11.5, INK, True)])
    rows = [("0 to 252", "1 byte: the number"), ("253 to 65,535", "3 bytes: fd + 2"), ("to 4,294,967,295", "5 bytes: fe + 4"), ("larger", "9 bytes: ff + 8")]
    for i, (a, b) in enumerate(rows):
        R(s, "compact range %d" % (i + 1), 670, 158 + 44 * i, 130, 38, fill=CARD, line=LINE, paras=[P(a, 10.5, INK, True)], adj=0.1)
        R(s, "compact size %d" % (i + 1), 806, 158 + 44 * i, 154, 38, fill=WHITE, line=LINE, paras=[P(b, 10.5, INK)], adj=0.1)
    bullets(s, ["An outpoint is 36 bytes: the txid of an earlier transaction and the number of one of its outputs, counted from zero.",
                "Think of a street address with building and flat: the input says where the coin lives, and the amount is stored in the coin.",
                "Counts are written as CompactSize: small numbers get a short ticket, and a first byte of fd, fe or ff warns that more bytes follow."], 366, size=11.5)


def coin(s, name, x, y, v):
    return R(s, name, x - 12, y, 120, 56, fill=TEAL, line=None, paras=[P("%s" % v, 13, WHITE, True, align="c"), P("satoshis", 9, SOFT, align="c")], shape=MSO_SHAPE.OVAL, adj=0, inset=0)


def d4(s):
    R(s, "before", 40, 135, 270, 150, fill=CARD, line=LINE)
    T(s, "before title", 52, 142, 250, 20, [P("Unspent outputs, before", 11.5, INK, True)]); coin(s, "coin before", 127, 190, "100,000")
    R(s, "transaction", 365, 135, 270, 150, fill=SOFT, line=TEAL, paras=[P("Alice's transaction", 13, TEAL, True, align="c"), P("removes the coin its input names", 11.5, INK, align="c", space=3), P("adds the two coins its outputs create", 11.5, INK, align="c")], inset=10)
    R(s, "after", 690, 135, 270, 150, fill=CARD, line=LINE)
    T(s, "after title", 702, 142, 250, 20, [P("Unspent outputs, after", 11.5, INK, True)]); coin(s, "coin after 1", 718, 190, "20,000"); coin(s, "coin after 2", 836, 190, "75,000")
    A(s, "arrow 1", 312, 210, 363, 210, ORANGE, 2.5); A(s, "arrow 2", 637, 210, 688, 210, ORANGE, 2.5)
    R(s, "fee", 40, 302, 920, 50, fill=WHITE, line=ORANGE, lw=1.5, paras=[P("Left over: 100,000 − 95,000 = 5,000 satoshis, the fee. No field of the transaction states it.", 12, INK, True, align="c")], inset=8)
    bullets(s, ["Before the payment the set holds the one coin of 100,000 satoshis that Alice's input names.",
                "The transaction removes that coin and adds the two coins its outputs create.",
                "Think of a drawer of banknotes nobody has spent: you take one out and put two back, and what is missing is the fee."], 366, size=13.5)


def d5(s):
    sc = 920 / 32; segs = [(1, "31", ORANGE, WHITE, ""), (8, "30–23", CARD, MUTE, "unused"), (1, "22", "F2A860", INK, ""), (6, "21–16", CARD, MUTE, "unused"), (16, "15–0", TEAL, WHITE, "the value")]
    x = 40
    for n, bits, f, tc, lab in segs:
        R(s, "bits " + bits, x, 178, n * sc, 40, fill=f, line=WHITE, paras=([P(lab, 11, tc, True, align="c")] if lab else None), adj=0.0, shape=MSO_SHAPE.RECTANGLE); x += n * sc
    T(s, "bit label 31", 40, 134, 220, 34, [P("bit 31: the disable flag", 11, ORANGE, True), P("set: no relative timelock", 10, MUTE)])
    A(s, "tick 31", 54, 168, 54, 178, MUTE, 0.75, head=False)
    T(s, "bit label 22", 40 + 9 * sc - 10, 134, 240, 34, [P("bit 22: the type flag", 11, "B5651D", True), P("0: blocks, 1: units of 512 seconds", 10, MUTE)])
    A(s, "tick 22", 40 + 9 * sc + 14, 168, 40 + 9 * sc + 14, 178, MUTE, 0.75, head=False)
    T(s, "bit label 0", 560, 134, 400, 34, [P("bits 15 to 0: how many blocks or units", 11, TEAL, True, align="r"), P("at most 65,535, about a year of blocks", 10, MUTE, align="r")])
    T(s, "wire note", 40, 222, 920, 16, [P("32 bits, written to the wire as four bytes with the lowest byte first", 10, MUTE, italic=True)])
    cards = [("Sequence replacement", "The first use: a later version with a higher number replaces an unfinished transaction.", "Like an order slip you can reissue until the kitchen closes."),
             ("Opt-in replace-by-fee, BIP125", "A value below 0xfffffffe signals that a better-paying transaction may replace this one.", "Like outbidding someone at an auction."),
             ("Relative timelock, BIP68", "With bit 31 clear, the low bits count blocks or 512-second units to wait after confirmation.", "Like a gift card that activates a week after purchase.")]
    for i, (h, b, a) in enumerate(cards):
        R(s, "meaning %d" % (i + 1), 40 + 315 * i, 252, 290, 152, fill=CARD, line=LINE, anchor="t", paras=[P("%d  %s" % (i + 1, h), 12, ORANGE, True, space=4), P(b, 11, INK, space=4), P(a, 10.5, MUTE, italic=True)], inset=10)
    bullets(s, ["The same four bytes were read as a replacement counter, then as an opt-in replace signal, then as a relative timelock.",
                "Bit 31 is the off switch of the timelock, and bit 22 chooses between blocks and 512-second units."], 414, size=11.5)


def d6(s):
    T(s, "bar title", 40, 130, 920, 18, [P("The spent coin: 100,000 satoshis", 11.5, INK, True)])
    sc = 920 / 100000
    R(s, "share bob", 40, 152, 20000 * sc, 44, fill=TEAL, line=WHITE, paras=[P("20,000 to Bob", 11, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "share change", 40 + 20000 * sc, 152, 75000 * sc, 44, fill="5F8F86", line=WHITE, paras=[P("75,000 change, back to Alice", 11.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "share fee", 40 + 95000 * sc, 152, 5000 * sc, 44, fill=ORANGE, line=WHITE, adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "fee label", 700, 199, 260, 18, [P("fee 5,000: no output claims it", 10.5, ORANGE, True, align="r")])
    T(s, "anatomy title", 40, 236, 920, 18, [P("One output, byte by byte (output 0)", 11.5, INK, True)])
    R(s, "amount", 40, 258, 340, 62, fill=TEAL, line=None, paras=[P("8 bytes: the amount", 11.5, WHITE, True, align="c"), P("20 4e 00 00 00 00 00 00 = 20,000", 10, SOFT, font="Courier New", align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "script length", 380, 258, 120, 62, fill=ORANGE, line=None, paras=[P("1 byte", 11.5, WHITE, True, align="c"), P("22 = 34", 10, WHITE, font="Courier New", align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "script", 500, 258, 460, 62, fill=INK, line=None, paras=[P("34 bytes: the lock (the output script)", 11.5, WHITE, True, align="c"), P("51 20 3b 41 da ba … who may spend it", 10, "E6EDF3", font="Courier New", align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    bullets(s, ["The spent coin held 100,000 satoshis: 20,000 go to Bob and 75,000 come back to Alice as change.",
                "The 5,000 left over is the fee. No output claims it, so the miner who mines the block collects it.",
                "An output is eight bytes of amount, a length and a lock, like a till receipt line saying how much and who may collect.", "A bitcoin is 100 million satoshis."], 340, size=13)


def d7(s):
    def row(prefix, y, segs, scale_total=920):
        x = 40
        for nm, w, lab, f, tc in segs:
            R(s, prefix + nm, x, y, w, 44, fill=f, line=WHITE, paras=[P(lab, 10.5, tc, True, align="c")] if lab else None, adj=0.0, shape=MSO_SHAPE.RECTANGLE); x += w
    T(s, "before title", 40, 126, 500, 16, [P("Before segwit", 12, INK, True)])
    row("before ", 144, [("version", 80, "version", "2F6D62", WHITE), ("inputs", 330, "inputs, with the signature inside", INK, WHITE), ("outputs", 330, "outputs", "5F8F86", WHITE), ("lock", 180, "lock time", MUTE, WHITE)])
    R(s, "before txid bar", 40, 192, 920, 7, fill=TEAL, line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "before txid", 40, 201, 920, 16, [P("txid covers everything, signature included: a stranger who re-encodes the signature changes the txid", 10.5, TEAL, True)])
    T(s, "after title", 40, 228, 500, 16, [P("After segwit", 12, INK, True)])
    T(s, "after wtxid", 40, 246, 920, 16, [P("wtxid covers every byte", 10.5, "B5651D", True)])
    R(s, "after wtxid bar", 40, 263, 920, 7, fill="B5651D", line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    segs = [("version", 70, "version", "2F6D62", WHITE), ("mf", 45, "m f", ORANGE, WHITE), ("inputs", 250, "inputs, script empty", INK, WHITE), ("outputs", 250, "outputs", "5F8F86", WHITE), ("witness", 225, "witness: the signature", "B5651D", WHITE), ("lock", 80, "lock", MUTE, WHITE)]
    row("after ", 273, segs)
    xs = {}; x = 40
    for nm, w, *_ in segs: xs[nm] = (x, w); x += w
    for nm in ("version", "inputs", "outputs", "lock"): R(s, "after txid bar " + nm, xs[nm][0], 320, xs[nm][1], 7, fill=TEAL, line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "after txid", 40, 329, 920, 16, [P("txid covers only these four fields; the witness, with marker and flag, stays outside", 10.5, TEAL, True)])
    bullets(s, ["Before segwit the signature sat inside the input script, so the txid covered it and a stranger could re-encode it.",
                "After segwit the signature lives in the witness, outside the txid, so the txid no longer moves.",
                "Think of keeping the passport photo off the ticket number: the photo can change, the ticket number cannot."], 360, size=11.5)


def d8(s):
    T(s, "lock title", 40, 128, 920, 16, [P("Lock time: one field, two readings", 12, INK, True)])
    R(s, "lock zero", 40, 150, 60, 40, fill=CARD, line=LINE, paras=[P("0", 11, INK, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "lock height", 100, 150, 400, 40, fill=TEAL, line=WHITE, paras=[P("1 to 499,999,999: a block height", 11.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    R(s, "lock time", 500, 150, 460, 40, fill=ORANGE, line=WHITE, paras=[P("500,000,000 and up: a time in seconds", 11.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "zero note", 40, 194, 58, 30, [P("any block", 9.5, MUTE, True)])
    T(s, "height note", 100, 194, 400, 30, [P("123,456 means block 123,456 or later", 10, MUTE, True)])
    T(s, "time note", 500, 194, 460, 30, [P("1,675,556,500 means 5 February 2023, tested against the median of eleven block times", 10, MUTE, True)])
    T(s, "maturity title", 40, 236, 920, 16, [P("Coinbase maturity: a coin made in block 9", 12, INK, True)])
    R(s, "mature made", 40, 258, 200, 56, fill=INK, line=None, paras=[P("block 9", 12, WHITE, True, align="c"), P("the coin is created", 10.5, "E6EDF3", align="c")])
    R(s, "mature locked", 260, 258, 440, 56, fill=CARD, line=ORANGE, lw=1.5, paras=[P("blocks 10 to 108", 12, ORANGE, True, align="c"), P("still locked: the coin is less than 100 blocks old", 10.5, INK, align="c")])
    R(s, "mature free", 720, 258, 240, 56, fill=TEAL, line=None, paras=[P("block 109", 12, WHITE, True, align="c"), P("age 100: may be spent", 10.5, WHITE, align="c")])
    A(s, "m arrow 1", 241, 286, 258, 286, MUTE, 1.5); A(s, "m arrow 2", 701, 286, 718, 286, MUTE, 1.5)
    bullets(s, ["Below 500 million the lock time is a block height; from 500 million up it is a time in seconds.",
                "A coinbase coin, such as one made in block 9, may be spent only 100 blocks later, from block 109.",
                "Think of a post-dated cheque, and of wages you cannot spend until the pay has cleared."], 334, size=14)


def d9(prs, s):
    tbl = s.shapes.add_table(9, 4, Emu(40 * U), Emu(135 * U), Emu(440 * U), Emu(9 * 25 * U)); tbl.name = "weight table"
    t = tbl.table
    for c, w in enumerate((170, 90, 60, 120)): t.columns[c].width = Emu(w * U)
    rows = [("Field", "Bytes", "×", "Weight")] + [("input" if nm == "input" else nm, str(n), "1" if nm in ("marker", "flag", "witness") else "4", str(n * (1 if nm in ("marker", "flag", "witness") else 4))) for nm, n in BYTES] + [("Total", "194", "", "569")]
    for r, row_ in enumerate(rows):
        t.rows[r].height = Emu(25 * U)
        for c, v in enumerate(row_):
            cell = t.cell(r, c); cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else (SOFT if r == 8 else (WHITE if r % 2 else CARD)))
            tf = cell.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.RIGHT
            run = tf.paragraphs[0].add_run(); run.text = v; set_run(run, 10.5, WHITE if r == 0 else INK, r in (0, 8)); cell.margin_top = Emu(18000); cell.margin_bottom = Emu(18000)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    sc = 0.78; x0 = 505
    def bar(y, parts, label):
        T(s, "label " + label[:12], x0, y - 20, 455, 18, [P(label, 11, INK, True)])
        x = x0
        for w, f, lab in parts:
            R(s, "bar " + label[:10], x, y, w * sc, 30, fill=f, line=WHITE, paras=[P(lab, 10, WHITE, True, align="c")] if lab and w * sc > 60 else None, adj=0.0, shape=MSO_SHAPE.RECTANGLE); x += w * sc
    bar(160, [(125, TEAL, "125 legacy"), (69, ORANGE, "69")], "194 bytes")
    bar(224, [(500, TEAL, "125 × 4 = 500"), (69, ORANGE, "69")], "569 weight units: 125 × 4 + 69 × 1")
    bar(288, [(143, "5F8F86", "143")], "143 virtual bytes: 569 ÷ 4, rounded up")
    T(s, "scale note", x0, 324, 455, 30, [P("All three bars use the same scale. Orange marks marker, flag and witness: 69 bytes that count once.", 10, MUTE, italic=True)])
    bullets(s, ["Each field's bytes are multiplied by four, except marker, flag and witness, which count once.",
                "Added up, Alice's 194 bytes weigh 569 units; divided by four and rounded up that is 143 virtual bytes.",
                "Think of postage that charges less for the annex pages: that discount is why a segwit transaction is cheaper."], 378, size=12)


PICS = [  # (old slide after which it is inserted, key, title, sub, takeaway, function)
    (5, "D1", "Alice's transaction, drawn to scale", "Each box is a field; its width is its size in bytes", "Seven fields in one fixed order: 194 bytes extended, 125 bytes legacy", d1),
    (11, "D2", "Six bytes that set the rules", "What an old and a new parser do with the same bytes", "A zero where an input count should be tells old and new software apart", d2),
    (15, "D3", "An input is an address, not an amount", "How an input names a coin, and how a count is written in few bytes", "An input names a coin by transaction and output number; it states no amount", d3),
    (20, "D4", "Spending changes the drawer", "A node keeps only unspent outputs", "One coin out, two coins in: the set always holds exactly the unspent coins", d4),
    (24, "D5", "The 32 bits of the sequence field", "Where the flags and the value live", "Bit 31 switches the relative timelock off; bit 22 picks its unit", d5),
    (30, "D6", "Where the 100,000 satoshis went", "An output is an amount and a lock", "An output is an amount plus a lock; what no output claims is the fee", d6),
    (38, "D7", "What each identifier covers", "Why moving the signature out changed everything", "The txid ignores the witness; the wtxid covers every byte", d7),
    (47, "D8", "Two clocks and a waiting room", "How lock time is read, and when a coinbase coin can move", "One field, two readings, and a hundred blocks of waiting for new coins", d8),
    (54, "D9", "From 194 bytes to 569 weight", "Every byte weighs four, except marker, flag and witness", "A block is filled by weight, four million units, and witness bytes cost a quarter", None),
]


def renumber(prs, N):
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): settext(sh, "%d / %d" % (i, N))


def step2(prs, ex):
    stories(prs)
    old = list(prs.slides)                                  # the 62 slides in the old order
    for i, s in enumerate(old, 1): s.notes_slide.notes_text_frame.text = NT.NOTES[i]
    src = old[6]; newslides = {}
    for after, key, title, sub, take, fn in PICS:
        s = new_slide(prs, src, title, sub, take)
        if key == "D9": d9(prs, s)
        else: fn(s)
        s.notes_slide.notes_text_frame.text = NT.NEW_NOTES[key]; newslides[after] = s
    lst = prs.slides._sldIdLst; ids = list(lst)
    by_slide = {sl.slide_id: el for sl, el in zip(list(prs.slides), ids)}
    order = []
    for i, sl in enumerate(old, 1):
        order.append(by_slide[sl.slide_id])
        if i in newslides: order.append(by_slide[newslides[i].slide_id])
    for el in ids: lst.remove(el)
    for el in order: lst.append(el)
    prs.part.rename_slide_parts([el.rId for el in lst])        # part names follow the presentation order (the checks read slideN.xml in file order)
    N = len(order); renumber(prs, N)
    # route slide: the ranges and counters
    newpos = {sl.slide_id: k for k, sl in enumerate(prs.slides, 1)}; oldpos = {i: newpos[sl.slide_id] for i, sl in enumerate(old, 1)}
    parts = [(3, 4), (5, 10), (11, 14), (15, 23), (24, 29), (30, 37), (38, 46), (47, 53), (54, 62)]
    route = prs.slides[1]; k = 0
    for sh in route.shapes:
        if sh.has_text_frame and re.fullmatch(r"\(slides \d+-\d+\)", sh.text_frame.paragraphs[-1].text if len(sh.text_frame.paragraphs) > 1 else ""):
            a, b = parts[k]; k += 1
            a2 = oldpos[a]; b2 = oldpos[b]
            sh.text_frame.paragraphs[1].runs[0].text = "(slides %d-%d)" % (a2, b2)
        elif sh.has_text_frame and sh.text_frame.text.strip() == "62": settext(sh, str(N))
        elif sh.has_text_frame and sh.text_frame.text.strip() == "true stories, each told by 5N1K": settext(sh, "true stories, each with its source link")
        elif sh.has_text_frame and sh.text_frame.text.strip() == "slides, numbered bottom-right": settext(sh, "slides, 9 of them pictures")
    assert k == 9, k
    return N, oldpos
