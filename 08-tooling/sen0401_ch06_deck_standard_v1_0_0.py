#!/usr/bin/env python3
"""Chapter 6 deck -> next version (deck standard v3.1.0 and CME material check v1.2.0). Reads the committed v2_4_3, never edits it.
Changes: reader-facing notes of 60-140 words; every everyday analogy removed (card lines, bullets, subtitles, footer pills); titles of at least four words;
a visual on every slide (cards and rows become groups); result and byte frames set in Consolas so only code boxes are Courier New code;
5N1K alt text on the story boxes. Usage: python3 sen0401_ch06_deck_standard_v1_0_0.py IN.pptx OUT.pptx VERSION"""
__version__ = "1.0.0"
import copy, re, sys
from pptx import Presentation
from pptx.util import Emu
sys.path.insert(0, __import__("os").path.dirname(__file__))
from sen0401_ch06_notes_v1_0_0 import NOTES
SRC, OUT, VER = sys.argv[1:4]
p = Presentation(SRC)
S = {i: s for i, s in enumerate(p.slides, 1)}

def shp(i, name):
    r = [x for x in S[i].shapes if x.name == name and x.has_text_frame]
    assert len(r) == 1, (i, name, len(r))
    return r[0]
def set_text(sh, text, para=0):
    pa = sh.text_frame.paragraphs[para]
    runs = pa.runs
    runs[0].text = text
    for r in runs[1:]: r._r.getparent().remove(r._r)

# 1. replacement lines for the concept cards: (slide, shape) -> technical detail from the chapter
T = {
5: {"Text 7": "Inputs name coins, outputs create coins, and every full node checks both.", "Text 11": "The extended form carries a witness; the legacy form leaves it out."},
7: {"Text 7": "It asks every full node to update its record of unspent coins.", "Text 11": "That record is the set of unspent outputs, called the UTXO set.", "Text 15": "Version, inputs, outputs and lock time, plus marker, flag and witness.", "Text 19": "Alice's transaction: 194 bytes extended, 125 bytes legacy."},
9: {"Text 7": "It ends with the witness, so it is 69 bytes longer than the legacy form.", "Text 11": "The txid hashes exactly these 125 bytes.", "Text 15": "Defined in BIP174; each signer adds its signatures in turn.", "Text 20": "Alice's map runs from offset 0 to offset 193."},
12: {"Text 7": "In Alice's transaction the version reads 01 00 00 00.", "Text 11": "In Alice's transaction they read 00 01."},
14: {"Text 7": "Alice's transaction is version 1.", "Text 11": "From version 2 on, BIP68 gives sequence a timelock meaning.", "Text 15": "Nodes may relay such transactions under stricter rules."},
16: {"Text 7": "Its signatures exist now; only the broadcast comes later.", "Text 11": "A real input count is never zero, so a zero is a signal.", "Text 16": "Its value is 01 today; other values are reserved."},
17: {"Text 7": "Alice's transaction has one input.", "Text 11": "Alice's outpoint: an earlier txid and output index 1.", "Text 15": "Stored in one order, printed by explorers in the reverse.", "Text 19": "In Alice's segwit input this slot is empty."},
19: {"Text 7": "Alice's transaction has one input, so the count is 01.", "Text 12": "Values 0 to 252 take one byte; larger ones add a prefix.", "Text 16": "Other encodings exist; CompactSize is the one used for counts here.", "Text 20": "Alice's input: 32 bytes of txid plus 4 bytes of index."},
21: {"Text 7": "In display order it equals the earlier transaction's txid.", "Text 11": "Alice's input spends output 1, the coin of 100,000 satoshis.", "Text 15": "Nodes reject a transaction whose outpoint is already spent.", "Text 19": "Only one of two conflicting transactions can be confirmed."},
23: {"Text 7": "Alice's spend removes one coin and adds two.", "Text 12": "The txid is a double SHA-256 digest.", "Text 16": "It is the order in which the hash function produces the bytes.", "Text 20": "It is the reversed order that explorers print for a txid."},
27: {"Text 7": "Alice's segwit input has none: its proof sits in the witness.", "Text 11": "The value 0x6b is 107 in decimal."},
28: {"Text 7": "The oldest use: a higher number replaced an unfinished transaction.", "Text 11": "BIP125 reads the same four bytes as a replacement signal.", "Text 15": "BIP68 reads the same four bytes as a wait after confirmation."},
30: {"Text 7": "The value 0xffffffff means the input is final.", "Text 11": "The refund is signed before the deposit is broadcast.", "Text 16": "The parties exchange newer signed versions off the chain.", "Text 21": "It is the reason the first use of the field was switched off."},
32: {"Text 7": "The replacement must pay a higher fee than the original.", "Text 11": "The value 0xfffffffd is the usual signal.", "Text 16": "A sequence of 30 means the coin must be 30 blocks old.", "Text 21": "Set means units of 512 seconds; clear means blocks."},
34: {"Text 7": "With bit 31 set, the other bits are ignored.", "Text 11": "Sixteen bits hold the values from 0 to 65,535."},
35: {"Text 7": "Alice's transaction has two: Bob's payment and her change.", "Text 11": "Dust is an output that costs more to spend than it holds.", "Text 15": "Bob's script is 34 bytes; Alice's change script is 22 bytes."},
37: {"Text 7": "In Alice's transaction the count byte is 02.", "Text 11": "Bob's amount is written 20 4e 00 00 00 00 00 00.", "Text 15": "So 20,000 satoshis are 0.0002 bitcoin.", "Text 19": "Consensus rejects any amount outside this range."},
39: {"Text 7": "Relay policy refuses to carry such outputs.", "Text 12": "Bob's taproot output must hold at least 330 satoshis.", "Text 16": "An OP_RETURN output cannot be spent, so it is never dust.", "Text 20": "Bob's script starts 51 20: a witness version 1 program."},
42: {"Text 7": "The smallest script is empty, with zero bytes.", "Text 11": "OP_TRUE leaves a one on the stack, so any spender succeeds.", "Text 15": "A node relays only these templates by default."},
44: {"Text 7": "Since segwit it is kept outside the txid.", "Text 11": "The payment stays the same; only the identifier changes.", "Text 15": "Segwit took the signatures out of the txid in 2017.", "Text 19": "It follows the outputs and comes before the lock time."},
46: {"Text 7": "A script with no key can be spent by anyone who knows 2.", "Text 11": "A signature proves that the key holder authorised the spend.", "Text 15": "Parties sign the refund before the deposit is broadcast.", "Text 20": "Before segwit, the deposit's txid depended on signatures not yet made."},
48: {"Text 7": "The payment is the same; only the identifier differs.", "Text 11": "The encodings are 52, 0102, 020200 and 4c0102.", "Text 15": "The counterparty holds a valid key and can sign again.", "Text 19": "The sender signs with a flag that permits later changes."},
51: {"Text 7": "The signatures move to the witness, outside the txid.", "Text 11": "Segwit did not need one.", "Text 15": "Segwit was activated this way in 2017.", "Text 19": "Version 0 programs have 20 or 32 bytes."},
52: {"Text 7": "It follows the outputs and comes before the lock time.", "Text 12": "Alice's transaction has one stack, for its one input.", "Text 16": "Alice's witness holds one item of 65 bytes.", "Text 20": "A legacy input's witness is written as a single 00 byte."},
54: {"Text 7": "It is the last four bytes of a transaction.", "Text 11": "Its one input has a null outpoint."},
56: {"Text 7": "It is the last field of the transaction, four bytes.", "Text 11": "The transaction waits for a block at that height or later.", "Text 15": "The value 1,675,556,500 is 5 February 2023.", "Text 19": "A time lock is compared with it, not with the newest timestamp."},
58: {"Text 7": "It has one input, with no previous output.", "Text 12": "The library tests for it in is_coinbase.", "Text 16": "Miners often write a message or a pool tag there.", "Text 20": "Block 210,000 was the first with 25 BTC."},
60: {"Text 7": "A miner may claim less than this, never more.", "Text 11": "A coin made in block 9 can be spent from block 109."},
62: {"Text 7": "Alice's 194 bytes weigh 569 units.", "Text 11": "Hashes name transactions; rules decide which are valid."},
64: {"Text 7": "Alice's transaction weighs 569 units.", "Text 11": "Alice's 569 weight is 143 vbytes.", "Text 15": "That corresponds to one million vbytes.", "Text 19": "Witness bytes count one unit each."},
66: {"Text 7": "SHA-256 gives 32 bytes whatever the size of the input.", "Text 11": "Bitcoin hashes twice to name a transaction.", "Text 15": "Alice's txid displays as 466200308696 and on.", "Text 19": "Alice's wtxid displays as f7cdbc7cf8b9 and on."},
68: {"Text 7": "A node may relay less than consensus allows.", "Text 11": "A block that breaks one is rejected by every node."},
}
for i, d in T.items():
    for nm, txt in d.items(): set_text(shp(i, nm), txt)

# 2. divider subtitles, reading bullets, footer pills, card-slide subtitles
SUB = {5: "A transaction asks every full node to update its record of unspent coins.",
12: "Version, marker and flag are the first six bytes; they set how the rest is read.",
17: "Inputs name the coins to spend, each by transaction and output number.",
28: "The sequence field is four bytes whose meaning changed three times.",
35: "Each output is an amount and a lock; the fee is what the outputs leave out.",
44: "A witness is the proof of the right to spend, kept outside the txid.",
54: "A lock time delays a transaction; a coinbase creates new coins.",
62: "Weight measures block space; the foundations are the hashes and the rules."}
for i, t in SUB.items(): set_text(shp(i, "Text 3"), t)
TITLE = {2: "Today's route through the chapter", 17: "Inputs: the coins a transaction spends", 28: "The sequence field: three meanings",
35: "Outputs: new coins and their locks", 44: "Witnesses: the proof kept apart", 62: "Weight and foundations: the base", 24: "Spending changes the set of unspent outputs"}
for i, t in TITLE.items(): set_text(shp(i, "Text 2"), t)
READ = {6: "The txid is computed from the short strip alone, so a change to the signature does not change it.",
13: "The version is a plain number; marker and flag exist only in the extended format.",
18: "The input says where the coin lives; the amount is stored in the coin, not in the input.",
24: "Taking one coin out and putting two back leaves the missing 5,000 satoshis as the fee.",
45: "With the signature outside the txid, the signature can change and the txid stays.",
55: "A lock time delays a transaction; the maturity rule delays a coinbase coin by 100 blocks.",
63: "Witness bytes count once instead of four times; that discount is why a segwit transaction is cheaper."}
for sl in p.slides:
    i = p.slides.index(sl) + 1
    for sh in sl.shapes:
        if not sh.has_text_frame: continue
        tx = sh.text_frame.text
        if sh.name == "reading" and re.search(r"\bThink of\b|, like a till", tx):
            if i == 36: set_text(sh, "▪  An output is eight bytes of amount, a length byte and a lock.")
            else: set_text(sh, "▪  " + READ[i])
        elif tx.startswith("Say each idea twice"): set_text(sh, "Say each idea in your own words before you go on")
        elif tx.startswith("Each card: the meaning in a few words"): set_text(sh, "Each card: the meaning in a few words, then a detail from this chapter")
        elif sh.name.startswith("meaning ") or (i == 53 and sh.name in ("Text 6", "Text 9")):
            for pa in list(sh.text_frame.paragraphs):
                if pa.text.startswith("Like "): pa._p.getparent().remove(pa._p)
# any reading bullet of slide 36 containing 'till receipt'
for sh in S[36].shapes:
    if sh.has_text_frame and "till receipt" in sh.text_frame.text: set_text(sh, "▪  An output is eight bytes of amount, a length byte and a lock.")

# 3. result and byte frames are output, not code: Consolas keeps them monospaced without being counted as code
for sl in p.slides:
    for sh in sl.shapes:
        if sh.has_text_frame and not sh.name.startswith("code"):
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.name == "Courier New": r.font.name = "Consolas"
            for el in sh._element.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}latin"):
                if el.get("typeface") == "Courier New": el.set("typeface", "Consolas")

# 4. 5N1K alt text on the story boxes (invisible), by sentence
FIVE = {11: ["when where", "who what when", "what why where", "how what", "what how"],
26: ["when where", "who what when", "who where what", "how why what", "what why"],
41: ["when where", "what when", "how why", "who when", "what where"],
50: ["when where", "who what where when", "what why how", "how why", "who where how", "what when"]}
for i, tags in FIVE.items():
    boxes = [x for x in S[i].shapes if x.name.startswith("story") and x.has_text_frame]
    assert len(boxes) == len(tags), (i, len(boxes))
    for b, t in zip(boxes, tags):
        b.name = "Story " + ("header" if t == tags[0] else "beat")
        b._element.xpath(".//p:cNvPr")[0].set("descr", t)

# 5. a visual on every slide: cards and rows become groups
E = 914400
def has_visual(sl):
    from pptx.enum.shapes import MSO_SHAPE_TYPE as T_
    for sh in sl.shapes:
        if sh.shape_type in (T_.PICTURE, T_.CHART, T_.TABLE, T_.GROUP): return True
        if sh.has_text_frame and any(r.font.name == "Courier New" for pa in sh.text_frame.paragraphs for r in pa.runs): return True
    return False
def body(sl):
    return [s for s in sl.shapes if 1000000 <= s.top < 4590000]
def centre_in(a, b): return b.left <= a.left + a.width / 2 <= b.left + b.width and b.top <= a.top + a.height / 2 <= b.top + b.height
made = 0
for i, sl in S.items():
    if has_visual(sl) or i in (1, 71): continue
    bs = body(sl)
    cards = [c for c in bs if c.shape_type == 1 and c.width > 1500000 and c.height > 600000]
    used = set()
    for c in sorted(cards, key=lambda c: (c.top, c.left)):
        mem = [m for m in bs if m is not c and id(m) not in used and centre_in(m, c)]
        if not mem: continue
        g = sl.shapes.add_group_shape([c] + mem); g.name = "Card: " + (mem[0].text_frame.text.split("\n")[0][:40] if mem[0].has_text_frame else "card")
        used.update(id(m) for m in mem); used.add(id(c)); made += 1
    if has_visual(sl): continue
    # rows: a badge with its text, grouped by the same band
    rows = sorted([s for s in bs if id(s) not in used], key=lambda s: s.top)
    badges = [s for s in rows if s.shape_type == 1 and s.width < 600000]
    for b in badges:
        mem = [m for m in rows if m is not b and abs((m.top + m.height / 2) - (b.top + b.height / 2)) < 250000]
        g = sl.shapes.add_group_shape([b] + mem); g.name = "Row: " + str(i); used.update(id(m) for m in mem); made += 1
    if not has_visual(sl):
        rest = [s for s in body(sl)]
        if rest: g = sl.shapes.add_group_shape(rest); g.name = "Card group"; made += 1
print("groups made:", made)

# 6. notes
for i, t in NOTES.items():
    S[i].notes_slide.notes_text_frame.text = t
p.core_properties.version = VER
p.save(OUT); print("wrote", OUT)
