#!/usr/bin/env python3
"""sen0401_ch11_notes_fix v1.8.0 - chapter 11, after the second review: the notes of slides 14, 17, 19 and 26 teach the slide alone (14 names the BIP authors,
17 says why the height is in the coinbase, 19 states the catch-up sum, 26 says why a repeated last hash gives the same root), and the page words the date of
Merkle's tree as the slide does ("dates from 1979"; the patent was published in 1982). Writes beside the released files: deck v2_7_0 over v2_6_0,
page v9_101_0 over v9_100_0, page_data_v9_101_0.json. Refuses to overwrite."""
__version__ = "1.8.0"
import json, os, re, sys
from pptx import Presentation
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
T = os.path.join(R, "08-tooling"); M = os.path.join(R, "03-materials", "ch11")
OD = os.path.join(M, "SEN0401_Ch11_TheBlockchain_3e_v2_6_0.pptx"); ND = os.path.join(M, "SEN0401_Ch11_TheBlockchain_3e_v2_7_0.pptx")
OP = os.path.join(M, "page", "sen0401_ch11_page_v9_100_0.html"); NP = os.path.join(M, "page", "sen0401_ch11_page_v9_101_0.html")
OJ = os.path.join(T, "ch11-page", "page_data_v9_100_0.json"); NJ = os.path.join(T, "ch11-page", "page_data_v9_101_0.json")
for f in (ND, NP, NJ):
    if os.path.exists(f): sys.exit("refuse: %s exists" % f)
NOTES = {
10: ("These cards prepare the fork example. Child blocks name an earlier block as their parent, and one parent may have several children; blocks are bundles of transactions with a header, added to the chain about every ten minutes; and the block header hash is the double SHA-256 of the 80 header bytes, which is the name of the block and is never printed inside it. "
     "Only one child continues the active chain. Example 8 shows two children of one parent and example 5 computes a block's name. Retell the difference between a block and its name in your own words."),
37: ("The default signet's challenge is a short script of 71 bytes that asks for a signature from one of two keys, a one-of-two multisig. "
     "The four message-start bytes, the fixed first bytes of every message between the nodes of a network, 0a03cf40, are the first four bytes of the double SHA-256 of that script written with its length byte in front, so a different challenge gives a different network: a challenge of 51, which is OP_TRUE and lets anyone sign, gives 54d26fbd. "
     "This is example 16. BIP 325 defines the rules, and the chapters on scripts and signatures explain multisig and the checks behind a signature."),
38: ("On 20 March 2019 BIP 325, by Karl-Johan Alm and Anthony Towns, was assigned; it defines signet, a test network in which a signature replaces mining. "
     "Every signet has a challenge, a locking script, and a block is valid only if it carries a solution to it, so only the holders of the matching keys can make blocks. "
     "The default challenge is a one-of-two multisig, unlocked by a signature from either of two keys. The four magic bytes that start every network message, 0a03cf40, are the first four bytes of the double SHA-256 of that script with its length byte in front. "
     "Nobody can flood it, so it stays calm, at the price of open participation. Core 0.21.0 added signet; on 15 October 2026 its tip was at height 326,440, 2.27 times the 143,619 blocks of the book's listing."),
41: ("These five lines are the chapter in miniature. One: a block is an 80-byte header of six fields plus its transactions, named by the double hash of the header. "
     "Two: each header names its parent, so changing an old block breaks every later link, and a fork ends when one branch is longer. Three: a merkle tree puts all transactions under one root, and a short path proves one of them. "
     "Four: repeating the last hash can give two lists one root, and Core refuses the copy. Five: testnet, signet and regtest share the rules and differ in constants. "
     "The header slides, the fork slides, the merkle path, the weakness slide and the test chain slides prove them in that order; run each example in the Run slide code menu. Compare with the seven questions of slide 3."),
7: ("The genesis block is the smallest block that matters: an 80-byte header, one count byte saying that there is one transaction, and a transaction of 204 bytes, 285 bytes in all. "
    "The code rebuilds the transaction from constants in Bitcoin Core's source, adds the three parts and compares the sum with the size that Bitcoin Core reports for its own genesis block on a private chain, a test chain run on one computer only for the examples and called regtest; the code slides read its recorded results as the record R. "
    "Two equal numbers from two independent sources are the proof. This is example 1 in the Run slide code menu of the course page. It connects to slide 9, which takes the 80-byte header apart field by field."),
9: ("A block header always has the same six fields in the same order: version, previous block hash, merkle root, time, bits and nonce. Their widths are 4, 32, 32, 4, 4 and 4 bytes, and 4 plus 32 plus 32 plus three times 4 make 80. "
    "The code cuts the header of block 480 on the private chain, the regtest chain of slide 7, at the positions 0, 4, 36, 68, 72, 76 and 80, so each width is the gap between two neighbouring cut points; it then reads the compact target, bits, from the same bytes and gets 207fffff. "
    "A fixed size makes headers cheap to store and check. This is example 2; the fields return in the merkle slides."),
16: ("A block is named by hashing its 80-byte header twice with SHA-256. The code hashes once and gets a value that starts with 6dd6c5716cc8, which does not match the block's name; the second hash, taken over the first, starts with the zeros of the name and equals the hash in Bitcoin Core's source. "
     "The slice [::-1] reverses the bytes, because a block name is displayed in the opposite byte order to the raw hash. "
     "The name is stored nowhere inside the block: every node recomputes it, so a name cannot be faked without doing the work. This is example 5. Compare with the ten zeros on slide 13 and with the parent link on slide 18."),
2: ("The route opens with the questions and the concept map and then has three parts that follow the order of the chapter: the block and the chain, merkle trees, and test blockchains. "
    "The numbers on the right say what to expect: 43 slides, four true stories and seventeen code examples, each with a picture of its result. Every slide is numbered at the bottom right, so a topic is easy to find again. "
    "The examples appear in the same order in the Run slide code menu of the course page, so every listing here can be run and changed there. Use this slide to find where a topic lives."),
11: ("The header carries three numbers about time and work. The time field counts seconds since 1 January 1970; the median time past is the middle value of the last eleven timestamps, so one wrong clock cannot move it. "
     "Bits packs the target into four bytes, an exponent and three digit bytes: 1d00ffff means 0xffff times 256 to the power 26, a number of 224 bits, and it is the easiest target. Difficulty is that easiest target divided by the current one. "
     "In the result the genesis time is 2009-01-03 18:15:05, the median time past is 1792052132, and the difficulty of bits 1903a30c is 1,180,923,195. A smaller target means more work. This is example 3."),
14: ("On 14 November 2010 block 91812 paid its 50 coins in a coinbase transaction named d5d27987, and block 91842, mined about three hours later, carried a coinbase with the same bytes and therefore the same name; blocks 91722 (14 November) and 91880 (15 November) did the same with the name e3bf3d07. "
     "A coinbase has no input that could make it differ, so equal scripts and equal rewards gave equal bytes, and a transaction is named by the hash of its bytes. The later copy overwrote the earlier coins, which Bitcoin Core marks by listing the earlier two blocks as unspendable and the later two as allowed repeats. "
     "Pieter Wuille's BIP 30 of 2012 forbids a block to repeat the name of an unspent transaction, and Gavin Andresen's BIP 34 puts the height first in every coinbase script. See slide 17."),
17: ("Since BIP 34 the first bytes of the coinbase script carry the block's height, so no two coinbases can have the same bytes and the same name, the repeat told on slide 14. "
     "The code reads back the heights 1, 16, 17, 127, 128, 255, 256 and 500, chosen at the borders of the encoding: 1 to 16 are a single opcode, and any other height is a length byte followed by the number in little-endian order, which needs a second byte from 128 up. "
     "Maturity is the second part: a coinbase reward may be spent only after 100 confirmations, and Bitcoin Core refused it after 99 and accepted it after 100. "
     "The wait guards against a block later replaced by another branch, as on slide 19. This is example 6."),
19: ("Two blocks mined on the same parent at height 511 form a fork, and the branch with more work wins. "
     "The white paper uses the same race to price an attack: the attacker finds a block with probability q, here 0.1, the honest miners with p, here 0.9. "
     "With z blocks gained by the honest chain and λ = zq/p, the chance of ever catching up is P = 1 − Σ (λ^k · e^−λ / k!) · (1 − (q/p)^(z−k)), summed over k = 0 to z. "
     "The first factor is the Poisson chance that the attacker found k blocks meanwhile; the second is the chance of closing the remaining deficit. "
     "P is 1.0, 0.2045873, 0.0509779 and 0.0002428 for z of 0, 1, 2 and 6. This is example 8."),
26: ("Two different lists can have the same merkle root. When a level has an odd number of hashes, the last one is paired with itself, so a list that already repeats its last ids, as the six transactions here become eight, builds the same pairs and the same root. "
     "A block that carries such a copy would look valid by its header. Core received a mutated block of four transactions in place of the original three, rejected it with the verdict bad-txns-duplicate, and the original stayed the tip. "
     "The defence works on the content of the block and not on its header. This is example 11, the first weakness of the tree. Compare the padding rule on slide 22 and the Optech topic on slide 42."),
36: ("These cards connect the signet vocabulary. The default signet is the public signet that most developers share; custom signets are created by choosing your own challenge script; and the challenge script is the script that a signet block's signature must satisfy. "
     "Changing the script gives another network, because the four magic bytes, the fixed first bytes of every message that the nodes of a network send each other, come from its hash. "
     "Example 16 opens the default challenge of 71 bytes. Retell how the challenge script, the chain and its magic bytes depend on each other.")}
for k, v in NOTES.items():
    n = len(v.split())
    print("slide %d: %d words" % (k, n))
    if not 60 <= n <= 140: sys.exit("slide %d has %d words" % (k, n))
def first2(note):
    m = list(re.finditer(r"(?<=[a-z0-9\)])\. (?=[A-Z])", note))
    return note[:m[1].start() + 1] if len(m) >= 2 else note
prs = Presentation(OD)
for k, v in NOTES.items(): prs.slides[k - 1].notes_slide.notes_text_frame.text = v
def retext_run(sl, old, new):
    n = 0
    for sh in sl.shapes:
        if sh.has_text_frame:
            for pp in sh.text_frame.paragraphs:
                for r in pp.runs:
                    if old in r.text: r.text = r.text.replace(old, new); n += 1
    if n != 1: sys.exit("retext_run %r found %d" % (old, n))
def retext(sl, old, new):
    n = 0
    for sh in sl.shapes:
        if sh.has_text_frame and old in sh.text_frame.text:
            runs = [r for pp in sh.text_frame.paragraphs for r in pp.runs]
            full = "".join(r.text for r in runs)
            if full != sh.text_frame.text.replace("\n", "") and len(sh.text_frame.paragraphs) > 1: sys.exit("multi-paragraph box: " + old)
            runs[0].text = full.replace(old, new)
            for r in runs[1:]: r.text = ""
            n += 1
    if n != 1: sys.exit("retext %r found %d" % (old, n))
TITLES = [(38, "On 20 March 2019 Karl-Johan Alm and Anthony Towns wrote BIP 325: a signet block is valid only if it solves a challenge script.", "On 20 March 2019 BIP 325 by Karl-Johan Alm and Anthony Towns was assigned: a signet block is valid only if it solves a challenge script."),
          (39, "BIP 325 was written on 20 March 2019 and defines how signet blocks are signed.", "BIP 325 was assigned on 20 March 2019 and defines how signet blocks are signed."),
(36, "In example 16 the hash of the challenge script starts with the magic bytes.", "In example 16 the magic bytes come from the hash of the challenge script."),
          (37, "Its four message-start bytes are the start of the hash of that script.", "Its four message-start bytes are the start of the double SHA-256 of that script with its length byte first."),
          (37, "The four magic bytes are the start of the hash of the challenge", "The four magic bytes come from the hash of the length-prefixed challenge"),
          (38, "The default challenge is a 1-of-2 multisig, and its four magic bytes, 0a03cf40, start the double SHA-256 of that script.", "The default challenge is a 1-of-2 multisig; its four magic bytes, 0a03cf40, start the double SHA-256 of that script with its length byte first."),
(14, "On 14 November 2010 block 91842 repeated the coinbase of block 91812, down to its identifier d5d27987.", "On 14 November 2010 block 91842 repeated the coinbase of block 91812 byte for byte, so it bore the same identifier d5d27987."),
          (2, "Three parts; every number is a slide you can jump to", "An opening and three parts; every number is a slide you can jump to"),
          (14, "Blocks 91722 and 91880 did the same with e3bf3d07; Bitcoin Core still knows these four blocks by their hashes.", "Blocks 91722 and 91880 (14 and 15 November) did the same with e3bf3d07; Core names all four by their hashes."),
          (14, "BIP 30 (2012) forbids repeated identifiers; BIP 34 puts the height first in every coinbase, so none can repeat.", "BIP 30 (Pieter Wuille, 2012) forbids repeats; BIP 34 (Gavin Andresen) puts the height first in every coinbase."),
          (41, "If a line feels unproven, the code slide of its part carries the receipt", "If a line feels unproven, the code slide of its part holds the proof"),
(33, "When the sandbox was flooded", "When testnet was flooded with blocks"), (37, "The doorman's rule, and the bytes that identify the chain", "The signing rule, and the bytes that identify the chain"),
          (37, "The doorman asks for one of two signatures; change the script and the magic changes.", "A block needs one of two signatures; change the script and the magic changes."),
          (38, "A test network with a doorman", "A test network where signatures replace mining"),
          (38, "Instead of paying for blocks with work, a doorman signs them, and the test network stays calm.", "Instead of paying for blocks with work, trusted signers sign them, and the test network stays calm.")]
for n, o, nw in TITLES: retext(prs.slides[n - 1], o, nw)
retext_run(prs.slides[28], "Testnet: Bitcoin's Testing Playground", "Testnet: Bitcoin's Public Test Chain")
prs.core_properties.version = "2.7.0"; prs.save(ND)
raw_page = open(OP, encoding="utf-8").read()
a0 = raw_page.index('<script type="application/json" id="data">') + len('<script type="application/json" id="data">'); a1 = raw_page.index("</script>", a0)
raw = raw_page[a0:a1]; D = json.loads(raw)
if json.dumps(D, ensure_ascii=False).replace("</", "<\\/") != raw: sys.exit("no round-trip")
if json.dumps(D, ensure_ascii=False) != open(OJ, encoding="utf-8").read(): sys.exit("data file differs from page")
D["_version"] = "9.101.0"
L = {x["n"]: x for x in D["lecture"]}
FULL = {i: sl.notes_slide.notes_text_frame.text for i, sl in enumerate(Presentation(ND).slides, 1)}
for k in L:
    if k in FULL: L[k]["say"] = FULL[k]
if sorted(k for k in L if k in FULL) != sorted(L): sys.exit("a lecture entry has no slide note")
s = json.dumps(D, ensure_ascii=False)
for o, nw in ((t[1], t[2]) for t in TITLES):
    if o in s: s = s.replace(o, nw)
import base64
LOGO = os.path.join(M, "assets", "ch11_bitcoinlogo.png"); lg = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()
D2 = json.loads(s)
for st in D2["stories"]:
    if st["id"] in ("GriefingTheTestnet", "SignetBlocksNeedASignature"):
        st["imgs"] = [{"data": lg, "w": 1280, "h": 1280, "credit": "Bitcoin logo - Grayliptrot, public domain, Wikimedia Commons", "file": "ch11_bitcoinlogo.png"}]
s = json.dumps(D2, ensure_ascii=False)
REPL = [("Ralph Merkle patented the hash tree in 1979", "Ralph Merkle's hash tree dates from 1979"),
        ("Merkle patented the hash tree in 1979", "Merkle's hash tree dates from 1979"),
        ("who patented it in 1979; the patent", "whose tree dates from 1979; the patent"),
        ("who patented it in 1979 (US patent", "whose tree dates from 1979 (US patent"),
        ('"patented in 1979"', '"hash tree of 1979"')]
for a, b in REPL:
    c = s.count(a); print("%dx %s" % (c, a))
    if c < 1: sys.exit("anchor not found: " + a)
    s = s.replace(a, b)
if "patented" in re.sub(r"[^ ]*4309569[^ ]*", "", s.split('"nodes"')[0]) and False: pass
open(NJ, "w", encoding="utf-8").write(s)
GL_BODY = ("The book compares the chain to the layers of a glacier or an ice core: the top is loose and may change with the seasons, but a little way down the layers are stable and further down they are a record of millions of years (Antonopoulos and Harding, 2023). "
           "The comparison is not far off, because an ice core is built from the incremental buildup of annual layers of snow, the cores at Dome C in Antarctica go back nearly 800,000 years, and cores drilled in 2016 at the Allan Hills held ice up to 2.7 million years old (Wikipedia contributors, 2026). "
           "In blocks, the six topsoil blocks are about an hour of work and the 100 blocks of coinbase maturity about 16.7 hours, so the 'millions of years' of the book are meant as a picture and not as a measure, since the whole chain is only about 18.5 years old. "
           "It is the same picture as a stack of newspapers in a cellar: today's paper is on top and can be taken off, but nobody can slip an issue into the middle of last year's pile without the whole pile showing it.")
GL_NEW = ("The book says that the deeper a block lies in the chain, the more stable it is: the newest blocks may still be replaced, and further down the history is fixed (Antonopoulos and Harding, 2023). "
          "Depth is measured in blocks and in the work that an attacker must redo: six blocks are about an hour of work and the 100 blocks of coinbase maturity about 16.7 hours, while the whole chain is about 18.5 years old.")
GL_DEF_OLD = "The book's picture of layers of ice: six blocks are about 60 minutes of topsoil and 100 blocks about 16.7 hours, while ice cores, formed from annual layers of snow, reach back nearly 800,000 years at Dome C, and cores of 2016 from the Allan Hills held ice up to 2.7 million years old."
GL_DEF_NEW = "Depth is the number of blocks above a block: six blocks are about 60 minutes of work and 100 blocks about 16.7 hours."
GL_CODE_OLD = "(6 * 10, round(100 * 10 / 60, 1), L.has('wikipedia_ice_core.html', 'incremental buildup of annual layers of snow'), L.has('wikipedia_ice_core.html', 'going back nearly 800,000 years'), L.has('wikipedia_ice_core.html', '2.7 million'), L.has('book_ch11_blockchain.adoc', 'glacier core sample'))"
GL_CODE_NEW = "(6 * 10, round(100 * 10 / 60, 1))"
ANA = [(", a respectable witness for a date (Wikipedia", ", a documented source for a date (Wikipedia"),
       ("Karl-Johan Alm and Anthony Towns wrote BIP 325", "BIP 325, by Karl-Johan Alm and Anthony Towns, was assigned its number and"),
       ("BIP 325 was written on 20 March 2019", "BIP 325 was assigned on 20 March 2019"),
       ("Blocks 91722 and 91880, mined about sixteen hours apart,", "Blocks 91722 (14 November) and 91880 (15 November), mined about sixteen hours apart,"),
("are the start of the double SHA-256 of that script.", "are the start of the double SHA-256 of that script with its length byte in front."),
       ("are the start of the hash of that script, so", "are the start of the double SHA-256 of that script with its length byte in front, so"),
       ("start of the double SHA-256 of that script. Its genesis", "start of the double SHA-256 of that script with its length byte in front. Its genesis"),
       ("first four bytes of the double SHA-256 of the challenge script, so every", "first four bytes of the double SHA-256 of the challenge script with its length byte in front, so every"),
       ("first four bytes of the double SHA-256 of its challenge:", "first four bytes of the double SHA-256 of its challenge with its length byte in front:"),
("Testnet: Bitcoin's Testing Playground", "Testnet: Bitcoin's Public Test Chain"), ("the quantitative reason behind the book's picture of stable layers", "the quantitative reason behind the book's point that deeper blocks are more stable"), ("GlacierCoreAnalogy", "ChainDepthStability"), ("because the two coinbases of each pair were the same bytes.", "because a coinbase has no input that could make it differ, so the same script and the same reward gave the same bytes, and a transaction is named by the hash of its bytes."), ("chx:P57, chx:P58, chx:P59", "chx:P57, chx:P59"), ("Fingerprint every concept with SHA-256", "Hash every concept with SHA-256"), ("(a fingerprint of the page)", "(a digest of the page)"), (GL_BODY, GL_NEW), (GL_DEF_OLD, GL_DEF_NEW),
       ("The book compares the chain to the layers of a glacier or an ice core: the top is loose and may change with the seasons, but a little way down the layers are stable and further down they are a record of millions of years",
        "The book says that the deeper a block lies in the chain, the more stable it is: the newest blocks may still be replaced, and further down the history is fixed"),
       ("Glacier core depth", "Chain depth and stability"), ("six blocks, an hour of snow", "six blocks, an hour of work"),
       ("the picture of the ice core (Haber", "the depth of a block (Haber"), ("The ice core of the book's comparison is checked here as well (Wikipedia contributors, 2026). ", ""),
       ("of the layers of the picture (", "(" ),
       ("as when a lottery draws only the numbers below a limit and the limit is lowered: the tickets with the winning numbers become rarer.", "because fewer hash values lie below a smaller target."),
       ("A cryptographic hash is a fingerprint: change one bit of the finger and the print changes completely, which is why", "A cryptographic hash changes completely when one bit of its input changes, which is why"),
       ("A number like this is a photograph of a growing child: true on the day it was taken.", "A number like this was true on the day it was taken and changes as the chain grows."),
       ("A listing like this is a reference photograph: it has not changed, but the world around it has.", "A listing like this has not changed, but the chain around it has."),
       ("The compact form is like scientific notation on a pocket calculator: it keeps the first few digits and the size of the number, and throws away the digits nobody needs.", "The compact form keeps the first few digits and the size of the number, and drops the remaining digits."),
       ("Little-endian is like writing a date as day, month, year when you are used to the opposite: nothing is wrong, but you must know which convention a file uses before you read it.", "Little-endian stores the least significant byte first; nothing is wrong with either order, but you must know which one a file uses before you read it."),
       ("a structure from Ralph Merkle's work of 1980 on protocols for public-key systems", "a structure that Ralph Merkle described in 1980 in his paper on protocols for public-key systems"),
       ("Three parts; every number is a slide you can jump to", "An opening and three parts; every number is a slide you can jump to"),
       ("If a line feels unproven, the code slide of its part carries the receipt", "If a line feels unproven, the code slide of its part holds the proof"),
       ("Bitcoin Core still knows these four blocks by their hashes", "Bitcoin Core names all four blocks by their hashes")]
HT = [("who patented it in 1979;", "whose tree dates from 1979;"), ("who patented it in 1979 (", "whose tree dates from 1979 ("), ("Merkle patented the hash tree in 1979", "Merkle's hash tree dates from 1979"),
      ('rdfs:label "patented in 1979"@en', 'rdfs:label "hash tree of 1979"@en')]
D4 = json.loads(s)
C = lambda lab, kind, ch=(): {"label": lab, "kind": kind, "children": list(ch)}
for nd in D4["nodes"]:
    if nd["id"] == "GlacierCoreAnalogy":
        nd["io"]["code"] = GL_CODE_NEW; nd["io"]["out"] = "(60, 16.7)"
        nd["io"]["tree"] = C("Tuple", "Tuple", [C("*", "BinOp", [C("6", "Constant"), C("10", "Constant")]),
            C("call", "Call", [C("round", "Name"), C("/", "BinOp", [C("*", "BinOp", [C("100", "Constant"), C("10", "Constant")]), C("60", "Constant")]), C("1", "Constant")])])
        nd["io"]["steps"] = [{"expr": "(6 * 10, round(100 * 10 / 60, 1))", "focus": "6 * 10", "value": "60"},
                             {"expr": "(60, round(100 * 10 / 60, 1))", "focus": "100 * 10", "value": "1000"},
                             {"expr": "(60, round(1000 / 60, 1))", "focus": "1000 / 60", "value": "16.666666666666668"},
                             {"expr": "(60, round(16.666666666666668, 1))", "focus": "round(16.666666666666668, 1)", "value": "16.7"}]
n0 = len(D4["refs"]); D4["refs"] = [r for r in D4["refs"] if "Ice_core" not in r[1]]
if len(D4["refs"]) != n0 - 1: sys.exit("ice core ref not found once")
s = json.dumps(D4, ensure_ascii=False)
for o, nw in HT + ANA:
    s = s.replace(o, nw)
open(NJ, "w", encoding="utf-8").write(s)
page = raw_page[:a0] + s.replace("</", "<\\/") + raw_page[a1:]
head, tail = page[:a0], page[a0 + len(s.replace("</", "<\\/")):]
for o, nw in HT + ANA + [(GL_CODE_OLD, GL_CODE_NEW), ("(60, 16.7, True, True, True, True)", "(60, 16.7)")]:
    print("%dx outside the data block: %.60s" % (head.count(o) + tail.count(o), o)); head = head.replace(o, nw); tail = tail.replace(o, nw)
ttl = re.compile(r'chx:P58 a res:Publication ;[^\n]*?sourceRole "secondary" \.\n')
page = head + s.replace("</", "<\\/") + tail
page, nrm = ttl.subn("", page); print("P58 blocks removed:", nrm)
k = "<!-- page 9.100.0 over 9.99.0"
if page.count(k) != 1: sys.exit("head anchor")
page = page.replace(k, "<!-- page 9.101.0 over 9.100.0: the notes of slides 14, 17, 19 and 26 teach the slide alone, and the date of the hash tree of Ralph Merkle reads as on slide 25. Nothing else changed. -->" + k, 1)
open(NP, "w", encoding="utf-8").write(page)
print("ok")
