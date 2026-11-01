#!/usr/bin/env python3
"""Chapter 1 deck v3.4.0 (a NEW tool file; task TK_Ch01_DeckTeach_Build). The deck v3.3.0 is read, never written; its SHA-256 is printed before and after.
It applies the chapter 6 Friday method (08-tooling/ch06-deck: deck_lib, deck_enhance helpers) to the chapter 1 deck:
(1) the nine true stories are told as sentences with real names, dates and places (no 'WHAT:' labels); the picture and the live source link stay;
(2) fourteen picture slides are added, drawn with native shapes, tables and one native chart, for the concepts the earlier deck named without showing;
(3) every slide gets short speaker notes that carry clues (deck_teach_content_v3_4_0.py);
(4) the slide numbers 'n / N' and the route slide follow the new order.
The code boxes, their shape names and the result shapes of the 15 code slides are not touched.
Usage: deck_teach_v3_4_0.py OLD NEW [PLAN_OUT_JSON]"""
__version__ = "3.4.0"
import copy, hashlib, hmac, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ch06-deck"))
from deck_lib_v2_3_0 import *
from deck_enhance_v2_3_0 import P, R, T, A, bullets, settext, delete
import deck_teach_content_v3_4_0 as C
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.oxml.ns import qn

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
CHIP = "F2A860"


def hdr(s, name, x, y, w, h, label, fill=TEAL, color=WHITE, size=12.5):
    return R(s, name, x, y, w, h, fill=fill, line=None, paras=[P(label, size, color, True, align="c")], adj=0.15)


def table(s, name, x, y, widths, rows, rh, size=11.5, hh=30):
    tbl = s.shapes.add_table(len(rows), len(widths), Emu(int(x * U)), Emu(int(y * U)), Emu(int(sum(widths) * U)), Emu(int((hh + rh * (len(rows) - 1)) * U))); tbl.name = name
    t = tbl.table
    for c, w in enumerate(widths): t.columns[c].width = Emu(int(w * U))
    for r, row_ in enumerate(rows):
        t.rows[r].height = Emu(int((hh if r == 0 else rh) * U))
        for c, v in enumerate(row_):
            cell = t.cell(r, c); cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else (WHITE if r % 2 else CARD))
            para = cell.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.LEFT
            run = para.add_run(); run.text = v; set_run(run, size, WHITE if r == 0 else INK, r == 0 or c == 0)
            cell.margin_top = Emu(30000); cell.margin_bottom = Emu(30000); cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tbl


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


# ---------------------------------------------------------------------------------------------------------------------------------------------
# stories
# ---------------------------------------------------------------------------------------------------------------------------------------------
def stories(prs):
    for n, (head, paras, lesson) in C.STORY.items():
        s = prs.slides[n - 1]; by = {sh.name: sh for sh in s.shapes}
        left = by["Text 6"].left // U; width = 950 - left
        for nm in ("Shape 5", "Shape 7", "Shape 9", "Text 6", "Text 8", "Text 10", "Shape 11", "Text 12", "Shape 13", "Text 14", "Shape 15", "Text 16"):
            delete(by[nm])
        bgk, rt = by["Shape 17"], by["Text 18"]
        bgk.left = Emu(50 * U); bgk.width = Emu(900 * U); rt.left = Emu(60 * U); rt.width = Emu(880 * U)
        hh0 = est_lines(head, 12, width, 0.5) * 12 * 1.2 / 0.72 + 6
        T(s, "story head", left, 138, width, hh0, [P(head, 12, ORANGE, True)]); y = 138 + hh0 + 4
        for p in paras:
            hh = est_lines(p, 12.5, width, 0.5) * 12.5 * 1.2 / 0.72 + 4
            T(s, "story", left, y, width, hh, [P(p, 12.5, INK)]); y += hh + 4
        ly = y + 4; lh = est_lines(lesson, 12.5, width - 20, 0.5) * 12.5 * 1.2 / 0.72 + 20
        assert ly + lh <= 446, (n, ly, lh)
        R(s, "lesson", left, ly, width, lh, fill=SOFT, line=TEAL, paras=[P(lesson, 12.5, INK, True)], inset=10)


# ---------------------------------------------------------------------------------------------------------------------------------------------
# the fourteen picture slides
# ---------------------------------------------------------------------------------------------------------------------------------------------
def m1(s):
    rows = [("Job", "A central bank and a clearing house", "Bitcoin", "What changes"),
            ("Create the money", "A board decides how much is issued", "The block subsidy halves every 210,000 blocks; the cap is just under 21 million", "A rule anyone can read replaces a decision"),
            ("Settle payments", "A clearing house confirms and records each payment", "Every node checks every payment; miners settle them in blocks", "Many keepers replace one"),
            ("Hold value steady", "Supply is adjusted to the economy", "Supply is fixed by rule; the book calls the currency deflationary over the long term", "Predictable supply, no discretion")]
    table(s, "central bank table", 40, 135, (150, 260, 290, 220), rows, 52)
    bullets(s, ["Mining takes over the issuing and clearing work of a central bank, so no central bank is needed for the currency to work.",
                "Deflationary means issuance shrinks and ends: it describes the supply, and it does not promise that the price rises.",
                "Think of a recipe printed on the packet instead of a chef who changes it every day."], 363, size=12.5)


def d1(s):
    rows = [("62,400", "sell", 0.7), ("62,300", "sell", 1.6), ("62,200", "sell", 2.3), ("62,100", "sell", 1.1),
            ("62,000", "buy", 1.8), ("61,900", "buy", 0.9), ("61,800", "buy", 2.1), ("61,700", "buy", 1.4)]
    T(s, "ladder head buy", 40, 130, 230, 20, [P("Buyers: bitcoin wanted", 11.5, TEAL, True, align="r")])
    T(s, "ladder head sell", 370, 130, 230, 20, [P("Sellers: bitcoin offered", 11.5, ORANGE, True)])
    T(s, "ladder head price", 272, 126, 96, 22, [P("dollars", 10.5, MUTE, True, align="c")])
    sc = 92.0
    for i, (price, side, q) in enumerate(rows):
        y = 156 + 37 * i + (14 if i >= 4 else 0)
        R(s, "price " + price, 272, y, 96, 32, fill=WHITE, line=LINE, paras=[P(price, 12.5, INK, True, align="c")], adj=0.15)
        if side == "buy":
            R(s, "bid " + price, 268 - q * sc, y, q * sc, 32, fill=TEAL, line=None, paras=[P("%.1f" % q, 11.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
        else:
            R(s, "ask " + price, 372, y, q * sc, 32, fill=ORANGE, line=None, paras=[P("%.1f" % q, 11.5, WHITE, True, align="c")], adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    gy = 156 + 37 * 4 + 3
    A(s, "gap line", 60, gy + 1, 590, gy + 1, MUTE, 1.0, head=False, dash=True)
    T(s, "gap label", 480, gy - 4, 118, 20, [P("no trade yet", 10.5, MUTE, False, True, align="r")])
    T(s, "toy note", 40, 474, 560, 20, [P("Toy numbers for illustration, in bitcoin per price level.", 10.5, MUTE, False, True)])
    x, y = 625, 140
    for t in ["Buyers queue below the market and sellers above it; a trade happens only where a bid reaches an ask.",
              "Here the best bid is 62,000 and the best ask 62,100, so nothing trades until one side moves.",
              "The last trade becomes the quoted price, which is why the price floats with the crowd.",
              "An exchange quotes such a price; a Bitcoin ATM adds a margin. Think of a money-changer's board."]:
        hh = est_lines(t, 12.5, 335, 0.5) * 12.5 * 1.2 / 0.72 + 12
        T(s, "reading", x, y, 335, hh, [{"runs": [("▪  ", 12.5, ORANGE, True), (t, 12.5, INK)]}]); y += hh + 4


def m2(s):
    steps = ["2016 blocks have been found", "Compare the time they took with two weeks", "Set the next target to hold ten minutes"]
    for i, t in enumerate(steps):
        R(s, "step %d" % (i + 1), 40 + 325 * i, 140, 270, 62, fill=CARD if i < 2 else SOFT, line=LINE if i < 2 else TEAL, paras=[P(t, 12.5, INK, True, align="c")], inset=8)
        if i < 2: A(s, "arrow %d" % (i + 1), 312 + 325 * i, 171, 363 + 325 * i, 171, ORANGE, 2.0)
    R(s, "fast card", 40, 218, 440, 100, fill=WHITE, line=ORANGE, lw=1.5, paras=[P("Blocks came faster than ten minutes", 13, ORANGE, True), P("More computing power joined. The next target is harder: more leading zeros are needed, so each search takes longer.", 12, INK)], inset=12)
    R(s, "slow card", 520, 218, 440, 100, fill=WHITE, line=TEAL, lw=1.5, paras=[P("Blocks came slower than ten minutes", 13, TEAL, True), P("Computing power left. The next target is easier, so blocks come faster again.", 12, INK)], inset=12)
    R(s, "limit", 40, 330, 920, 32, fill=CARD, line=LINE, paras=[P("One step changes the difficulty by at most a factor of four, up or down.", 12, INK, True, align="c")], inset=6)
    bullets(s, ["The difficulty is adjusted every 2016 blocks so that, on average, one block is found every ten minutes whatever the total computing power.",
                "In the toy proof of work each extra zero costs about sixteen times more guesses; the real network turns the same dial.",
                "Think of a thermostat: it holds the room at the set temperature whoever lights the fire."], 374, size=12)


def b1(s):
    names = ["Block n − 1", "Block n", "Block n + 1"]
    for i, nm in enumerate(names):
        x = 40 + 330 * i
        R(s, "block card %d" % i, x, 134, 270, 164, fill=CARD, line=LINE, paras=None)
        hdr(s, "block name %d" % i, x + 12, 140, 246, 28, nm)
        R(s, "block time %d" % i, x + 12, 174, 246, 32, fill=WHITE, line=LINE, paras=[P("timestamp: when it was found", 11.5, INK)], inset=3)
        R(s, "block tx %d" % i, x + 12, 211, 246, 32, fill=WHITE, line=LINE, paras=[P("a list of transactions", 11.5, INK)], inset=3)
        R(s, "block link %d" % i, x + 12, 248, 246, 40, fill=SOFT if i else WHITE, line=ORANGE, lw=1.5, paras=[P("fingerprint of the block before", 11.5, INK, True)], inset=3)
        if i: A(s, "back arrow %d" % i, x - 2, 268, x - 58, 268, ORANGE, 2.0)
    R(s, "tamper", 40, 310, 920, 36, fill=WHITE, line=ORANGE, lw=1.5, paras=[P("Edit block n: its fingerprint changes and every later link breaks.", 12.5, INK, True, align="c")], inset=8)
    bullets(s, ["The blockchain is the list of validated blocks, each linking to the one before it back to block 0; the timestamps place the transactions in an agreed order.",
                "A timestamp orders blocks but does not make their content true; the checks of every node do that.",
                "Think of a book whose every page ends with a seal of the page before: tearing one page out shows at the next seal."], 358, size=12)


def e1(s):
    hts = [58, 84, 110, 136, 162, 188]; base = 314
    caps = ["block found", "+1 block", "+2 blocks", "+3 blocks", "+4 blocks", "+5 blocks"]
    for i, h in enumerate(hts):
        x = 40 + 118 * i
        R(s, "layer %d" % (i + 1), x, base - h, 110, h, fill=TEAL if i < 5 else ORANGE, line=WHITE, paras=[P("%d" % (i + 1), 20, WHITE, True, align="c"), P("confirm.", 10.5, WHITE, align="c")], adj=0.05, shape=MSO_SHAPE.RECTANGLE)
        T(s, "layer caption %d" % (i + 1), x, base + 4, 110, 20, [P(caps[i], 10.5, MUTE, True, align="c")])
    R(s, "rule of thumb", 760, 134, 200, 130, fill=SOFT, line=TEAL, paras=[P("About an hour", 14, TEAL, True), P("Six confirmations at ten minutes a block is the usual wait for a larger amount.", 11.5, INK)], inset=10)
    bullets(s, ["A payment is confirmed once when its block is found; every block built on top adds one more confirmation.",
                "To reverse it, someone must redo that block and every block after it faster than the honest network adds new ones.",
                "Card payments, bank transfers and other electronic payments can be reversed; a Bitcoin transaction practically cannot.",
                "Think of cement poured in layers over a footprint: after enough layers the print is there for good."], 346, size=12)


def w1(s):
    rows = [("Kind", "Where the keys live", "Main risk", "Think of"),
            ("Desktop wallet", "On your computer's disk", "Malware on that computer", "The cash register on the shop counter"),
            ("Mobile wallet", "On your phone", "A lost or stolen phone with no backup", "The purse in your pocket"),
            ("Web wallet", "On someone else's server", "The host is hacked, fails or freezes you out", "Your coat at the cloakroom"),
            ("Hardware signing device", "Inside a small dedicated device", "Losing the device with no recovery code", "A stamp kept in a locked drawer"),
            ("Third-party API client", "In your client; the facts come from a remote service", "The service sees your questions and may be wrong", "A travel agent instead of the timetable")]
    table(s, "wallet table", 40, 135, (160, 250, 290, 220), rows, 50, size=12)
    bullets(s, ["Choose by who holds the keys and where the device runs."], 428, size=12.5)


def w2(s):
    for x, title, fill, lines in ((40, "Full node", TEAL, ["Downloads every block and checks every rule itself.", "Needs the most storage and time.", "Trusts nobody for the facts."]),
                                  (520, "Lightweight client", ORANGE, ["Keeps your keys but asks other nodes for most of the data.", "Needs little storage and starts fast.", "Trusts the nodes it asks, and may reveal which addresses it watches."])):
        R(s, "node card " + title[:4], x, 138, 440, 196, fill=CARD, line=LINE, paras=None)
        hdr(s, "node title " + title[:4], x + 12, 146, 416, 30, title, fill=fill)
        yy = 186
        for t in lines:
            hh = est_lines(t, 12.5, 410, 0.5) * 12.5 * 1.2 / 0.72 + 6
            T(s, "node line", x + 16, yy, 410, hh, [{"runs": [("▪  ", 12.5, ORANGE, True), (t, 12.5, INK)]}]); yy += hh + 8
    R(s, "peer strip", 40, 346, 920, 34, fill=SOFT, line=TEAL, paras=[P("Every node is a peer of the others; a lightweight wallet is a client of one or a few of them.", 12.5, INK, True, align="c")], inset=6)
    bullets(s, ["The choice trades independence and storage on one side for convenience and trust on the other.",
                "Think of cooking from raw ingredients against buying a ready meal: you can check the first, and you must trust the second."], 396, size=12.5)


def t1(s):
    cols = [("Phishing", INK, "A fake site, message or app pretends to be your wallet and asks you for the recovery code."),
            ("Malware", INK, "A harmful program on your device reads the wallet data or swaps the address you paste."),
            ("Three habits that help", TEAL, "Never type the recovery code into a website. Install wallets from the official page. Check the address on a screen you trust.")]
    for i, (h, f, body) in enumerate(cols):
        x = 40 + 318 * i
        hdr(s, "threat title %d" % i, x, 138, 290, 30, h, fill=f)
        R(s, "threat body %d" % i, x, 172, 290, 134, fill=WHITE if i < 2 else SOFT, line=LINE if i < 2 else TEAL, paras=[P(body, 12.5, INK)], inset=12)
    R(s, "warning", 40, 318, 920, 34, fill=WHITE, line=ORANGE, lw=1.5, paras=[P("A wallet that asks for the recovery code at an unexpected time is a warning sign.", 12.5, INK, True, align="c")], inset=6)
    bullets(s, ["Phishing attacks the person, malware attacks the device; the defence for the first is a habit and for the second a trusted source.",
                "The fake wallet application is the chapter's own example of malware.",
                "Think of a forged letter from your bank for phishing, and of a pickpocket already inside your coat for malware."], 362, size=12.5)


def a2(s):
    names = ["Bob", "Carol", "Dan"]
    T(s, "reuse title", 40, 130, 440, 26, [P("One address for every payer", 13, ORANGE, True)])
    T(s, "fresh title", 520, 130, 440, 26, [P("A fresh address for each payer", 13, TEAL, True)])
    for i, nm in enumerate(names):
        y = 166 + 44 * i
        R(s, "payer old " + nm, 40, y, 110, 32, fill=CARD, line=LINE, paras=[P(nm, 12, INK, True, align="c")])
        A(s, "arrow old " + nm, 152, y + 16, 268, 214, MUTE, 1.5)
        R(s, "payer new " + nm, 520, y, 110, 32, fill=CARD, line=LINE, paras=[P(nm, 12, INK, True, align="c")])
        A(s, "arrow new " + nm, 632, y + 16, 748, y + 16, TEAL, 1.5)
        R(s, "address new " + nm, 750, y, 210, 32, fill=SOFT, line=TEAL, paras=[P("address %d" % (i + 1), 12, INK, True, align="c")])
    R(s, "address one", 270, 170, 210, 90, fill=WHITE, line=ORANGE, lw=2.0, paras=[P("address A", 13, INK, True, align="c"), P("all three payments land here", 11.5, MUTE, align="c")])
    T(s, "reuse result", 40, 310, 440, 40, [P("Anyone can link the three payments and add them up.", 12.5, INK, True)])
    T(s, "fresh result", 520, 310, 440, 40, [P("Each payment stands apart from the others.", 12.5, INK, True)])
    bullets(s, ["Using the same address for several payments lets others link and total them; a new address for each payment protects privacy.",
                "Think of a new locker number for every delivery: the courier never learns what else you receive."], 366, size=12.5)


def a1(s):
    rows = [("Way", "Whom you deal with", "What they need from you", "Think of"),
            ("Buy from a friend", "A person who already has bitcoin", "An address to send to, and an agreed price", "Swapping banknotes with a travelling friend"),
            ("Earn it", "A customer who pays you in bitcoin", "An address, for a product or service you sell", "Being paid in foreign money for your work"),
            ("Bitcoin ATM", "A machine and its operator", "Cash, often a phone number or an identity check, and a fee", "A vending machine that sells coins"),
            ("Currency exchange", "A company", "Identity verification and a way to pay; the coins stay in its account until you withdraw", "The airport money-changer's booth")]
    table(s, "first bitcoin table", 40, 135, (150, 210, 340, 220), rows, 58, size=12)
    bullets(s, ["Buying from a friend is the least complicated way; every other way adds a company, a fee or an identity check.",
                "A balance at an exchange is not your keys: the Mt. Gox story shows what that can cost."], 412, size=12.5)


def k1(s):
    h1 = hashlib.sha256(b"alice pays bob 1").hexdigest()[:12]; h2 = hashlib.sha256(b"alice pays bob 2").hexdigest()[:12]
    k1_ = hmac.new(b"key-one", b"alice pays bob 1", "sha256").hexdigest()[:12]; k2_ = hmac.new(b"key-two", b"alice pays bob 1", "sha256").hexdigest()[:12]
    tiles = [("Hash function", "Maps data of any length to a fixed-length fingerprint; any change gives a different result.", "'… bob 1' → %s\n'… bob 2' → %s" % (h1, h2), "a fingerprint."),
             ("Digital signature", "A value computed from data and a private key that anyone with the public key can check.", "message + private key\n→ signature", "a wax seal only you press."),
             ("Public-key cryptography", "A pair of related keys: what one does, only the other can undo.", "private key → public key\n→ address (one way)", "a padlock you hand out."),
             ("Entropy", "Unpredictability, counted in bits; a wallet needs enough that nobody can guess a key.", "12 words = 128 bits\n2^128 possible phrases", "rolling dice many times."),
             ("Keyed hash", "A hash with a secret key mixed in, so only the key holder can produce or confirm it.", "key-one → %s\nkey-two → %s" % (k1_, k2_), "a secret ingredient.")]
    pos = [(40, 130), (352, 130), (664, 130), (40, 304), (352, 304)]
    for (x, y), (ttl, mean, ex, an) in zip(pos, tiles):
        R(s, "tile " + ttl[:8], x, y, 296, 168, fill=CARD, line=LINE, paras=None)
        T(s, "tile title", x + 10, y + 5, 276, 24, [P(ttl, 13, TEAL, True)])
        T(s, "tile meaning", x + 10, y + 29, 276, 62, [P(mean, 11.5, INK)])
        R(s, "tile example", x + 10, y + 92, 276, 44, fill=WHITE, line=ORANGE, paras=[P(l, 10.5, INK, False, False, "Courier New") for l in ex.split("\n")], inset=6)
        T(s, "tile analogy", x + 10, y + 141, 276, 24, [P("Think of: " + an, 11, MUTE, False, True)])
    R(s, "how they fit", 664, 304, 296, 168, fill=SOFT, line=TEAL, paras=[P("How they fit", 13, TEAL, True), P("A wallet draws entropy, stretches it with a keyed hash into a seed, derives key pairs, signs with the private key, and shows hashes as addresses.", 11.5, INK)], anchor="t", inset=10)


def c1(s):
    rows = [("Term", "What it is", "Where it shows up here", "Think of"),
            ("HTTP", "The protocol browsers and servers use to exchange web pages", "Block explorers and price sites answer your browser with it", "Ordering at a counter with fixed phrases"),
            ("Web browser", "A program that fetches and shows web pages", "You look up block 0 on mempool.space with one", "A window onto a library"),
            ("Database", "Organised storage that is easy to search", "A node keeps blocks and coins in one; a wallet keeps labels and history", "A filing cabinet with labelled folders"),
            ("Operating system", "System software that runs the hardware and the programs", "Desktop and mobile wallets run on top of one", "The manager of an office building"),
            ("Distributed system", "Computers that work together over a network without a centre", "Bitcoin itself has no central server", "A choir without a conductor"),
            ("Bits and bytes", "A byte is eight bits; a hexadecimal digit stands for four bits", "A 256-bit hash is 32 bytes or 64 hexadecimal digits", "Letters and words")]
    table(s, "computing table", 40, 134, (140, 290, 310, 180), rows, 42, size=11.5, hh=28)


def s1(s):
    steps = ["An idea for a change", "A Bitcoin Improvement Proposal: a numbered design document, discussed in public", "The reference implementation, open source software, receives the code", "Each node operator decides whether to run it"]
    for i, t in enumerate(steps):
        R(s, "flow %d" % (i + 1), 40 + 240 * i, 138, 200, 96, fill=SOFT if i == 3 else CARD, line=TEAL if i == 3 else LINE, paras=[P(t, 12, INK, True, align="c")], inset=8)
        if i < 3: A(s, "flow arrow %d" % (i + 1), 242 + 240 * i, 186, 278 + 240 * i, 186, ORANGE, 2.0)
    for i, (h, t) in enumerate((("W3C standards", "The World Wide Web Consortium publishes open Recommendations."),
                                ("Decentralized identifier", "An identifier you prove control of by key, with no central registry."),
                                ("Verifiable credential", "An issuer's signed claim that a holder can show to a verifier."))):
        R(s, "w3c %d" % (i + 1), 40 + 318 * i, 250, 290, 100, fill=WHITE, line=TEAL, paras=[P(h, 12.5, TEAL, True), P(t, 12, INK)], inset=10)
    bullets(s, ["Bitcoin has no owner who can order a change: a proposal becomes real only when enough nodes choose to run it.",
                "Bitcoin Core, the descendant of Satoshi Nakamoto's 2009 software, is the reference implementation that proposals first reach.",
                "Think of a town's rules: anyone may propose a bylaw, but it applies only where residents agree to follow it."], 364, size=12.5)


def o1(s):
    R(s, "open", 40, 140, 240, 74, fill=CARD, line=LINE, paras=[P("Open", 13, TEAL, True, align="c"), P("one transaction on the chain", 12, INK, align="c")], inset=8)
    R(s, "inside", 330, 140, 340, 74, fill=WHITE, line=ORANGE, lw=2.0, paras=[P("Pay many times inside the channel", 13, ORANGE, True, align="c"), P("none of these payments reaches the chain", 12, INK, align="c")], inset=8)
    R(s, "close", 720, 140, 240, 74, fill=CARD, line=LINE, paras=[P("Close", 13, TEAL, True, align="c"), P("one transaction on the chain", 12, INK, align="c")], inset=8)
    A(s, "arrow open", 282, 177, 328, 177, ORANGE, 2.0); A(s, "arrow close", 672, 177, 718, 177, ORANGE, 2.0)
    T(s, "ln title", 40, 230, 920, 26, [P("The Lightning Network links channels so that a payment can be routed through several of them", 12.5, INK, True)])
    for i, nm in enumerate(["Alice", "Bob", "Carol", "Dave"]):
        R(s, "peer " + nm, 60 + 230 * i, 262, 130, 40, fill=SOFT, line=TEAL, paras=[P(nm, 13, INK, True, align="c")])
        if i < 3: A(s, "channel %d" % (i + 1), 192 + 230 * i, 282, 288 + 230 * i, 282, TEAL, 2.0)
    T(s, "ln note", 40, 308, 920, 20, [P("Alice reaches Dave through three channels; the chain sees nothing of it.", 12, MUTE, False, True)])
    bullets(s, ["An offchain payment moves value without recording every payment in the public blockchain, which lowers cost and improves privacy.",
                "It also changes what a backup must cover: the state of the channel as well as the keys.",
                "Think of a bar tab that is settled once at closing time."], 346, size=12.5)


PICS = [  # (old slide after which it is inserted, key, title, sub, takeaway, function)
    (22, "M1", "A central bank's jobs, done by rules", "Who issues the money, who settles payments, what keeps its value steady", "Rules every node checks replace three institutions' jobs", m1),
    (22, "D1", "Where a price comes from", "Buyers below, sellers above: a trade happens where they meet", "A price is the last place a buyer and a seller agreed", d1),
    (30, "M2", "Keeping blocks ten minutes apart", "Difficulty adjustment, every 2016 blocks", "The network turns its own difficulty dial to hold the pace", m2),
    (34, "B1", "A chain of dated blocks", "Each block carries a time and the fingerprint of the block before", "Edit one old block and every later link breaks", b1),
    (35, "E1", "Confirmations pile up like layers", "Why a payment gets safer with every block built on top", "Irreversible means ever costlier to reverse", e1),
    (40, "W1", "Five kinds of wallet compared", "Where the keys live and what can go wrong", "The kind of wallet decides who can lose or lock the keys", w1),
    (41, "W2", "Full node or lightweight client?", "Independence on one side, convenience on the other", "Checking for yourself costs storage; asking others costs trust", w2),
    (44, "T1", "Where a wallet gets attacked", "Two threats the chapter names, and three habits that blunt them", "No honest wallet asks for the recovery code in a web form", t1),
    (51, "A2", "Why one address per payer", "Address reuse lets others link and total your payments", "A fresh address for each payment keeps payments apart", a2),
    (52, "A1", "Four ways to a first bitcoin", "Whom you deal with and what they need from you", "Buying from a friend is simplest; an exchange adds identity checks", a1),
    (56, "K1", "Five cryptographic tools in a wallet", "Hash, signature, key pair, entropy and keyed hash, each with an example", "Every wallet builds on these five small ideas", k1),
    (56, "C1", "Computing words under the chapter", "Six everyday terms and where each one appears", "Plain computing ideas carry Bitcoin", c1),
    (56, "S1", "How Bitcoin changes without a boss", "Open proposals, a reference implementation and open web standards", "Anyone may propose; only the nodes that choose to run a change make it real", s1),
    (58, "O1", "A channel in three steps", "Open once, pay many times offchain, close once", "Two transactions on the chain can carry any number of payments", o1),
]


def widen_results(prs):
    """a result that would wrap in its column gets the full content width (x 50 to 950), one line, directly below the chart column; no expression is shortened"""
    for s in prs.slides:
        for sh in list(s.shapes):
            if not sh.name.startswith("result ") or not sh.has_text_frame: continue
            txt = sh.text_frame.text; room = (sh.width - sh.text_frame.margin_left - sh.text_frame.margin_right) / 12700
            if len(txt) <= int(room / 6.0): continue
            assert len(txt) <= int((900 * U - sh.text_frame.margin_left - sh.text_frame.margin_right) / 12700 / 6.0), txt
            for o in s.shapes:                                           # the right column (chart and its reading) makes room above the result
                if o.left // U >= 600 and o.top // U >= 190:
                    if o.has_chart: o.height = Emu(200 * U)
                    elif o.has_text_frame and 400 < o.top // U < 500: o.top = Emu(398 * U)
            sh.left = Emu(50 * U); sh.width = Emu(900 * U); sh.top = Emu(450 * U); sh.height = Emu(30 * U)


def renumber(prs, N):
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): settext(sh, "%d / %d" % (i, N))


def build(old_path, new_path):
    prs = Presentation(old_path)
    stories(prs); widen_results(prs)
    old = list(prs.slides); assert len(old) == 62
    src = old[5]; newslides = {}; order_new = []
    for after, key, title, sub, take, fn in PICS:
        s = new_slide(prs, src, title, sub, take); fn(s)
        s.notes_slide.notes_text_frame.text = C.NEW_NOTES[key]
        newslides.setdefault(after, []).append((key, s))
    for i, s in enumerate(old, 1): s.notes_slide.notes_text_frame.text = C.NOTES[i]
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
    parts = [(3, 4), (5, 11), (12, 25), (26, 36), (37, 46), (47, 53), (54, 59), (60, 62)]
    route = prs.slides[1]; k = 0
    for sh in route.shapes:
        if not sh.has_text_frame: continue
        tx = sh.text_frame.text.strip()
        if len(sh.text_frame.paragraphs) > 1 and re.fullmatch(r"\(slides \d+-\d+\)", sh.text_frame.paragraphs[-1].text):
            a, b = parts[k]; k += 1
            sh.text_frame.paragraphs[1].runs[0].text = "(slides %d-%d)" % (oldpos[a], oldpos[b])
        elif tx == "62": settext(sh, str(N))
        elif tx == "slides, numbered bottom-right": settext(sh, "slides, 14 of them concept pictures")
        elif tx == "true stories, each told by 5N1K": settext(sh, "true stories, each with its source link")
    assert k == 8, k
    prs.core_properties.version = "3.4.0"
    prs.save(new_path)
    return N, oldpos, {key: newpos[s.slide_id] for lst_ in newslides.values() for key, s in lst_}


def main(old, new):
    before = sha(old); print("SHA-256 old deck before:", before)
    N, oldpos, newpos = build(old, new)
    after = sha(old); print("SHA-256 old deck after: ", after, "UNCHANGED" if before == after else "CHANGED")
    assert before == after
    print("wrote", new, sha(new), "slides", N)
    print("new slides:", json.dumps(newpos)); print("old->new:", json.dumps(oldpos))
    json.dump({"slides": N, "new": newpos, "old_to_new": oldpos, "old_sha256": before, "new_sha256": sha(new)}, open(new + ".map.json", "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
