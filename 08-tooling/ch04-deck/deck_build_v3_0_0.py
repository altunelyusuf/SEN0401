#!/usr/bin/env python3
"""Builds deck_plan_v3_0_0.json - chapter 4 (Keys and Addresses) redesigned for the classroom.

Chapter 4 joins the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0), drawn by
the SHARED renderer 08-tooling/deck_render_v1_0_0.js. Every '>>>' row comes from
examples_out_v2_0_0.json and is re-run off the finished file by deck_check_v2_0_0.py, which
also requires the elliptic-curve source shown on the double-and-add slide to equal, verbatim,
the source that computed every key on these slides. Three 5N1K stories carry fact rows with
live links: the 1976 paper, Satoshi's base-58 memo quoted from the pinned source tree, and the
burn address whose balance this build fetched live.

Usage: python3 deck_build_v3_0_0.py   (writes deck_plan_v3_0_0.json beside itself)
"""
__version__ = "3.0.0"

import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load("corpus4", os.path.join(HERE, "..", "sen0401_ch04_corpus_v1_2_0.py"))
ST = load("stories4", os.path.join(HERE, "..", "sen0401_ch04_stories_v1_0_0.py"))
EXM = load("examples4", os.path.join(HERE, "examples_v2_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch04/assets/"
for _f in ("photo_diffie_hellman.jpg", "mbc3_0402.png", "mbc3_0404.png", "mbc3_0407.png"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v2_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: v for k, v in EX.items() if not k.startswith("_")}

# the EC source the checker requires verbatim on the deck - taken from the SAME module the
# checker imports, so the slide and the gate cannot drift apart
EC_SRC = EXM.EC_SRC
EC_LINES = EC_SRC.split("\n")

BYNAME = {n[0]: n for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in G.values() for _, out in rows)
STORYTEXT = " ".join(s["story"] + " " + s["source"] + " " + s["when"] for s in ST.STORIES)


def _sentences(text, k=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:k])


def paras(*names, ask=None):
    for nm in names:
        if nm not in BYNAME:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
    lead = BYNAME[names[0]][5][0][1]
    say = _sentences(lead, 2)
    if len(say) > 480:
        say = _sentences(lead, 1)
    out = "SAY: " + say
    if ask:
        out += "\nASK: " + ask
    out += "\nFULL TEXT: course page, chapter 4 - " + ", ".join(names) + "."
    return out


def decamel(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", n).replace("P2pkh", "P2PKH").replace("P2pk", "P2PK").replace("P2sh", "P2SH").replace("P2wpkh", "P2WPKH").replace("P2wsh", "P2WSH").replace("P2tr", "P2TR").replace("Wif", "WIF")


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def assert_fact(token, where):
    t = str(token)
    if t in CORPUS_TEXT or t in OUTTEXT or t in STORYTEXT or t.replace(",", "") in OUTTEXT:
        return t
    raise SystemExit("REFUSED: %r (slide %r) is in neither the corpus, the outputs, nor a story" % (t, where))


def bullets_ok(title, items):
    if len(items) > 5:
        raise SystemExit("REFUSED: %r carries %d bullets" % (title, len(items)))
    for b in items:
        if len(b.split()) > 30:
            raise SystemExit("REFUSED: bullet %r on %r reads as a paragraph" % (b, title))
    return items


def code(group, x, y, w, h, fs=11, rows=None):
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    nlines = sum(1 + (1 if out.strip() else 0) for _, out in rr)
    fit = (w - 0.4) / (maxlen * 0.00842)
    fit_h = (h - 0.30) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fx%.1fin" % (group, w, h))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


def srcpanel(lines, x, y, w, h, fs=9, cap=None):
    """A verbatim source panel (no '>>>' rows): used for the EC source the checker demands and
    for Satoshi's base58 memo. Width-gated like everything else - lines never wrap."""
    maxlen = max(len(l) for l in lines)
    fit_w = (w - 0.4) / (maxlen * 0.00842)
    fit_h = (h - (0.52 if cap else 0.30)) * 72.0 / (len(lines) * 1.3)
    fs = min(fs, round(fit_w, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: source panel cannot fit unwrapped in %.1fx%.1fin" % (w, h))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": lines, "fs": fs, "compact": True}
    if cap:
        it["cap"] = cap
    return it


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return "STORY (%s): %s\nSOURCE: %s" % (st["when"], st["story"], st["source"])


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


# figures re-parsed from the executed examples and re-asserted
import ast as _ast
assert _ast.literal_eval(G["Entropy"][-1][1]) == 256
assert _ast.literal_eval(G["Secp256k1"][-1][1]) == (True, True)
assert G["Base58Check"][-1][1] == "'1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy'"
assert _ast.literal_eval(G["AddressReuse"][-1][1]) == (1, 3)
assert _ast.literal_eval(G["VanityAddress"][-1][1]) == 58 ** 11
assert _ast.literal_eval(G["ErrorDetection"][-1][1]) == (0, 0, 0)
E = ST.EATER
assert E["funded_sat"] == 1_341_747_849 and E["spent_sat"] == 0

S = []

TAKES = {
    'The questions this chapter answers': 'If you can answer these, chapter 4 is yours',
    'One chapter, five branches': 'Five branches - every slide today lives on this map',
    'The 1976 paper that split the key in two': 'Public and private halves - one 1976 idea under every address',
    'A private key is just a number': 'Any 256-bit number - the hard part is choosing it unpredictably',
    'The curve everyone agreed on': 'secp256k1: two primes, one base point, shared by all',
    'Double-and-add: the one-way street': '256 doublings forward - and no known road back',
    'Prove the key without showing it': "Chapter 1's house key, kept honest: sign, never reveal",
    'Why 58? Satoshi left the reasons in the file': 'The address alphabet is usability engineering, documented',
    'From key to WIF and back': 'WIF is the same number, dressed for transport',
    'The checksum that catches your typo': 'Four bytes stop a mistyped address from costing coins',
    'From public key to address, exactly': 'Two hashes and an alphabet - the pipeline, executed',
    'The address that eats coins': 'An address commits to a key - it cannot conjure one',
    'SegWit and bech32: the second alphabet': 'New addresses move the witness and drop the look-alikes',
    'Error detection, measured': 'bech32m catches what base58 provably misses',
    'Taproot, and what wallets do today': "A real wallet's defaults, read from the node",
    'Habits the chapter prescribes': 'Fresh address every time; the wallet derives, you back up once',
}


def slide(kind, title, sub, items, notes, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg})


def content(title, sub, items, notes, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "bg": "light"}
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
        sl["lede"] = lede
    if take:
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes, image=None):
    items = [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3 if image else 8.6, "h": 1.9,
              "cols": 2 if image else min(4, len(boxes)), "fs": 14, "subfs": 11, "items": boxes}]
    if image:
        items.append(image)
    slide("section", title, sub, items, notes, bg="light")


# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 4: Keys and Addresses", "From a secret number to the string you can safely read out loud",
      [img("mbc3_0407.png", 6.35, 1.0, 3.1, 3.4, cap="key to address - Mastering Bitcoin 3e, CC BY-SA")],
      "SAY: Chapter 3 gave you the node; chapter 4 gives you ownership: one secret number, the "
      "curve that hides it, and the address formats that carry it in public.\n"
      "FULL TEXT: course page, chapter 4.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.5,
          "items": [re.sub(r",.*", "?", q) if len(q.split()) > 18 else q for q in C.CQS]}],
        paras("Keys"))

content("One chapter, five branches", "The concept map the whole chapter hangs on",
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 12, "root": "Chapter 4",
          "nodes": [{"label": decamel(r), "kids": [decamel(x) for x in children(r, 2)[:7]]}
                    for r in ("Keys", "Format", "Address", "Practice", "Semantics")]}],
        paras("Keys", "Format", "Address"),
        lede="Each branch is a question the chapter answers; the grey lists are the concepts that answer it, every one explained on the course page.")

# ---- Keys -------------------------------------------------------------------------------------
section("Keys", "A number, a curve, and a one-way multiplication",
        [{"label": "Private key"}, {"label": "The curve"}, {"label": "Public key"}, {"label": "Proof by signature"}],
        paras("Keys"),
        image=img("mbc3_0402.png", 6.5, 1.85, 2.9, 2.9, cap="the curve - Mastering Bitcoin 3e, CC BY-SA"))

content("The 1976 paper that split the key in two", STORY["NewDirections1976"]["when"],
        [img("photo_diffie_hellman.jpg", 0.5, 1.5, 3.2, 2.1, cap="Diffie and Hellman - Wikimedia Commons, CC BY-SA 3.0"),
         {"t": "beats", "x": 4.1, "y": 1.5, "w": 5.4, "h": 2.3, "fs": 13, "items": [
             "'We stand today on the brink of a revolution in cryptography'",
             "One key splits in two: publish one half, keep the other",
             "Tied by a computation easy forward, infeasible backward",
             "Turing Award, 2015 - this chapter runs their idea"]},
         factrow("NewDirections1976", x=0.5, y=4.42, w=9.0)],
        story_notes("NewDirections1976"))

content("A private key is just a number", "Any 256-bit number - and the run shows the edges",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Pick a number below the curve order n - that is the whole secret",
            "256 bits of honest randomness; dice work, habits do not",
            "One too large and the arithmetic itself refuses"]},
         dict(code("PrivateKey", 4.3, 1.6, 5.2, 1.5, fs=9.5), label="the edges, probed - the error is real"),
         dict(code("Entropy", 4.3, 3.45, 5.2, 1.1, fs=9.5), label="how big 2^256 - 1 is")],
        paras("PrivateKey", "Entropy", ask="Why is a password a bad private key even if it is long?"))

content("The curve everyone agreed on", "secp256k1 - checked live, not taken on faith",
        [img("mbc3_0404.png", 0.5, 1.5, 2.9, 2.9, cap="point addition - Mastering Bitcoin 3e, CC BY-SA"),
         dict(code("Secp256k1", 3.75, 1.55, 5.75, 1.45, fs=9), label="the two primes, re-tested in the build"),
         dict(code("GeneratorPoint", 3.75, 3.4, 5.75, 1.3, fs=9), label="G generates; after n steps the cycle closes")],
        paras("Secp256k1", "GeneratorPoint", ask="Who chose these constants - and why does 'nothing up my sleeve' matter?"))

content("Double-and-add: the one-way street", "The exact code that computed every key on these slides",
        [srcpanel(EC_LINES, 0.5, 1.5, 6.7, 2.3, fs=8,
                  cap="sen0401_ch04_keys - the deck_check gate requires this source, verbatim"),
         {"t": "stat", "x": 7.45, "y": 1.55, "w": 2.05, "h": 2.45, "vert": True, "items": [
             {"n": "256", "label": "doublings to walk k*G"},
             {"n": "~2^128", "label": "work to walk back (best known)"}]},
         dict(code("PointMultiplication", 0.5, 4.08, 6.7, 0.88, fs=9.5), label="3G = G+G+G - the homework check")],
        paras("PointMultiplication", "DiscreteLogarithm", ask="Where exactly does 'easy forward, hard backward' live in these 13 lines?"))

content("Prove the key without showing it", "Chapter 1's house-key analogy, now executable",
        [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.95, "fs": 9.5, "items": [
            "A signature answers a challenge using k, revealing only K; verify needs the public half alone",
            "The wrong key fails - the run shows both verdicts"]},
         dict(code("KeyControlProof", 0.5, 2.6, 9.0, 1.65, fs=9), label="sign, verify, then try the neighbour's key"),
         {"t": "chips", "x": 0.5, "y": 4.45, "w": 9.0, "h": 0.55, "fs": 12.5,
          "items": ["car key: opens", "house deed: proves", "bitcoin key: both - so never show it"]}],
        paras("DigitalSignature", "KeyControlProof", ask="What would 'showing the key' even mean here - and what breaks the moment you do?"))

# ---- Formats ----------------------------------------------------------------------------------
section("Formats", "The same numbers, dressed to travel",
        [{"label": "Base58Check"}, {"label": "WIF"}, {"label": "Compression"}, {"label": "Checksums"}],
        paras("Format"))

content("Why 58? Satoshi left the reasons in the file", STORY["Base58Design"]["when"],
        [srcpanel(["/**", " * Why base-58 instead of standard base-64 encoding?",
                   " * - Don't want 0OIl characters that look the same in some fonts and",
                   " *      could be used to create visually identical looking data.",
                   " * - A string with non-alphanumeric characters is not as easily accepted as input.",
                   " * - E-mail usually won't line-break if there's no punctuation to break at.",
                   " * - Double-clicking selects the whole string as one word if it's all alphanumeric.",
                   " */"], 0.5, 1.5, 9.0, 1.75, fs=9,
                  cap="src/base58.h at the pinned commit - the file's copyright line names Satoshi Nakamoto, 2009-2010 (MIT)"),
         dict(code("VersionPrefix", 0.5, 3.52, 5.6, 0.85, fs=9.5), label="why keys start with 5 or K: the version byte"),
         factrow("Base58Design", x=0.5, y=4.5, w=9.0)],
        story_notes("Base58Design"))

content("From key to WIF and back", "Wallet Import Format - transport clothing for k",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.15, "fs": 12.5, "steps": [
            {"label": "k, 32 bytes", "sub": "the number itself"},
            {"label": "0x80 prefix", "sub": "+ 0x01 if compressed"},
            {"label": "checksum", "sub": "4 bytes of SHA256^2"},
            {"label": "base58", "sub": "the string you export", "hot": True}]},
         dict(code("WalletImportFormat", 0.5, 3.1, 9.0, 1.1, fs=9.5), label="round trip: encode, decode, same bytes")],
        paras("WalletImportFormat", "CompressedPrivateKey", ask="Decode a WIF by eye: which characters can never appear?"))

content("The checksum that catches your typo", "Four bytes between you and a lost payment",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Hash the payload twice, keep four bytes, append",
            "Any single typo breaks the match",
            "The run flips one character - and is refused"]},
         dict(code("Checksum", 4.3, 1.6, 5.2, 1.75, fs=8.5), label="a real address, a real typo, a real refusal"),
         dict(code("Base58Check", 0.5, 3.8, 9.0, 0.95, fs=9.5), label="the whole encoder, applied to the book's hash160")],
        paras("Checksum", "Base58Check", ask="What does the checksum NOT protect you from? (the next story answers)"))

# ---- Addresses --------------------------------------------------------------------------------
section("Addresses", "Commitments you can read out loud",
        [{"label": "P2PKH"}, {"label": "SegWit / bech32"}, {"label": "Taproot"}, {"label": "What wallets pick"}],
        paras("Address"))

content("From public key to address, exactly", "Two hashes and an alphabet - executed, then validated by the node",
        [{"t": "flow", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.1, "fs": 12, "steps": [
            {"label": "K, 33 bytes", "sub": "compressed point"},
            {"label": "SHA256", "sub": "then RIPEMD160"},
            {"label": "hash160", "sub": "20 bytes"},
            {"label": "Base58Check", "sub": "1... address", "hot": True}]},
         dict(code("Hash160", 0.5, 2.9, 4.3, 1.3, fs=8.5), label="both hashes, and why compression matters"),
         dict(code("P2pkhAddress", 5.1, 2.9, 4.4, 1.3, fs=8.5), label="the node validates the result"),
         {"t": "when", "x": 2.8, "y": 4.4, "w": 4.4, "body": "address: 1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy"}],
        paras("P2pkhAddress", "Hash160", ask="Why hash the key at all - why not publish K as the address?"))

content("The address that eats coins", STORY["BitcoinEater"]["when"],
        [{"t": "stat", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "items": [
            {"n": assert_fact("13.41747849", "eater"), "label": "BTC sent to it, as of this build's live fetch"},
            {"n": assert_fact("5,832", "eater"), "label": "separate deposits over the years"},
            {"n": "0", "label": "satoshis ever spent from it - no key exists"}]},
         {"t": "beats", "x": 0.5, "y": 3.0, "w": 9.0, "h": 1.25, "fs": 12.5, "items": [
             "The address spells a sentence - chosen as text, so no private key was ever behind it",
             "Checksum valid, coins accepted, coins gone: commitment is not existence",
             "Vanity addresses differ only in effort: 58^11 tries for eleven chosen characters"]},
         factrow("BitcoinEater")],
        story_notes("BitcoinEater"))

content("SegWit and bech32: the second alphabet", "Move the witness; drop the look-alikes",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10, "items": [
            "SegWit moves signatures out of the txid's reach",
            "bech32: one case, no 1/b/i/o - QR-friendly",
            "A witness program is version + bytes, re-encoded"]},
         dict(code("SegwitUpgrade", 4.3, 1.55, 5.2, 1.85, fs=8.5), label="txid steady while the witness moves"),
         dict(code("Bech32Address", 0.5, 3.62, 9.0, 1.3, fs=9), label="encode, decode, same program - version 0")],
        paras("SegwitUpgrade", "Bech32Address", ask="Read bc1q... aloud to a friend: which old-alphabet mistakes are now impossible?"))

content("Error detection, measured", "Not claimed - counted, against the standards' own vectors",
        [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.95, "fs": 9.5, "items": [
            "Base58's checksum is strong but unstructured; bech32's BCH code GUARANTEES small errors are caught",
            "The run mutates addresses and counts the escapes: zero"]},
         dict(code("ErrorDetection", 0.5, 2.55, 9.0, 1.45, fs=8.5), label="one, two, three flips - none slip through"),
         dict(code("TestVectors", 0.5, 4.15, 9.0, 0.8, fs=9, rows=[G["TestVectors"][0], G["TestVectors"][2]]), label="all BIP-350 vectors pass, valid and invalid")],
        paras("ErrorDetection", "BchCode", ask="Why does 'provably catches' beat 'has never missed so far'?"))

content("Taproot, and what wallets do today", "Version 1, and a real wallet's own defaults",
        [dict(code("P2tr", 0.5, 1.6, 9.0, 0.95, fs=9.5), label="a version-1 address from the book's witness program"),
         dict(code("DefaultAddressType", 0.5, 2.8, 9.0, 1.28, fs=9), label="a real Core wallet, asked what it uses: wpkh by default"),
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.6, "fs": 12.5,
          "items": ["1... legacy", "3... script / nested", "bc1q... segwit v0", "bc1p... taproot"]}],
        paras("P2tr", "DefaultAddressType", ask="Which prefix will your first wallet hand you - and can you say why now?"))

# ---- Practice ---------------------------------------------------------------------------------
section("Practice", "Habits that keep keys safe",
        [{"label": "Fresh addresses"}, {"label": "One seed"}, {"label": "Export with care"}],
        paras("Practice"))

content("Habits the chapter prescribes", "Two runnable reasons",
        [{"t": "compare", "x": 0.5, "y": 1.52, "w": 9.0, "h": 1.68, "fs": 12,
          "left": {"head": "Reuse an address", "rows": [
              "One cluster: every payment publicly linked",
              "The run counts identities: 1"]},
          "right": {"head": "Fresh address each time", "rows": [
              "Payments unlinked on the chain",
              "The run counts: 3 - and one seed derives them all"]}},
         dict(code("AddressReuse", 0.5, 3.32, 9.0, 0.95, fs=9), label="linkability, counted"),
         dict(code("DeterministicWallet", 0.5, 4.4, 9.0, 0.62, fs=9, rows=[G["DeterministicWallet"][1]]), label="one seed, address #0 - chapter 5 opens this door")],
        paras("AddressReuse", "DeterministicWallet", ask="If one seed makes every address, what single thing must you back up?"))

content("Where to go from here", "Checked 2026-10-06; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["This chapter, free (CC BY-SA)", "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch04_keys.adoc"],
                ["Diffie-Hellman, the 1976 turn", "https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange"],
                ["Satoshi's base58 memo, in place", "https://github.com/bitcoin/bitcoin/blob/master/src/base58.h"]]},
            {"head": "Standards", "rows": [
                ["BIP 173 - bech32 addresses", "https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki"],
                ["BIP 350 - bech32m for v1+", "https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki"]]},
            {"head": "Explore", "rows": [
                ["The eater address, live", "https://blockstream.info/address/1BitcoinEaterAddressDontSendf59kuE"],
                ["learnmeabitcoin - formats, drawn", "https://learnmeabitcoin.com"]]},
            {"head": "Community", "rows": [
                ["Bitcoin Stack Exchange Q&A", "https://bitcoin.stackexchange.com"]]}]}],
        "SAY: Everything here is free. Open the eater address tonight and watch nothing move - "
        "that standstill is this chapter's whole lesson about commitments.\n"
        "ASK: Who can explain to a parent why bc1p beats 1... for reading aloud?\n"
        "FULL TEXT: course page, chapter 4 - Practice.",
        take="One secret number; everything else on these slides is derivation")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a private key is, and what makes one safe",
          "How k becomes K becomes an address - and never back",
          "What a checksum catches, and what it cannot",
          "Which address format to use today, and why"])}],
      "SAY: Four claims, each carried by a computation you watched run. Next: the wallets that "
      "manage these keys for Alice.\nFULL TEXT: course page, chapter 4.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "A private key is a 256-bit number; the curve turns it into a public point, one way only",
              "The 13 lines of double-and-add on these slides computed every key we showed",
              "Formats are the same numbers dressed to travel - version byte, checksum, alphabet",
              "An address is a commitment: the eater address holds 13.4 BTC no key can ever spend",
              "bech32m's error detection is proven, not anecdotal - and wallets default to segwit today"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 4 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - from one secret number to safe habits",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_k, _f, _a, _p = (_sec[t] for t in ("Keys", "Formats", "Addresses", "Practice"))
_rows = [("Questions and the chapter map", 3, _k),
         ("Keys - the number, the curve, the proof", _k + 1, _f),
         ("Formats - base58, WIF, checksums", _f + 1, _a),
         ("Addresses - P2PKH to taproot, measured", _a + 1, _p),
         ("Practice, summary, and resources", _p + 1, len(S))]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") == "code")),
                      "label": "live-run consoles, each shown with its result"}]}]
S[1]["notes"] = ("SAY: Five parts: the key, its public face, its travel clothes, its addresses, and the "
                 "habits - every claim arrives with its receipt, and one slide is signed by Satoshi's "
                 "own source comment.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 4 - every section.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES:
        sl["take"] = TAKES[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 4: Keys and Addresses", "sub": "SEN0401, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0)"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v3_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
