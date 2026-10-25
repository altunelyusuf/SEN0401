#!/usr/bin/env python3
"""deck_build v3.4.0 (chapter 4, Keys and Addresses) - the generator of the chapter 4 deck 3.4.0 (task TK_Ch04_Deck_Build_R24, Iteration 25), a NEW file; the deck 3.3.0 stays as it is.
It writes (1) 03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, (2) the chapter-code manifest 03-materials/ch04/page/chapter_code_ch04_v1_0_0.json (the examples in the
order of the deck's code slides: the manifest IS the deck's code boxes, drawn from the same list), (3) deck_plan_v3_4_0.json.
It reads the chapter research (the 48 key concepts of sen0401_ch04_research_v1_3_0.ttl), the story module sen0401_ch04_stories_v1_2_0.py (three stories with pictures and links), the examples
examples_v3_4_0.py and their recorded executions examples_out_v3_4_0.json (made by examples_run_v3_4_0.py under Python 3.14). Every number on a result picture is parsed from the recorded
output, never typed. The deck standard (D1-D12) is held as refusals in deck_kit_v3_4_0.py BEFORE the file is drawn (and here: every research concept must stand in a table row with its
everyday analogy); the independent checks measure the result afterwards.
Usage: python3 -B deck_build_v3_4_0.py"""
__version__ = "3.4.0"
import ast, glob, hashlib, importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v3_4_0 as X
from deck_kit_v3_4_0 import *

DECK_NAME = "SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx"
WHEEL = "sen0401_ch04_lib-1.0.0-py3-none-any.whl"
OUT = json.load(open(os.path.join(HERE, "examples_out_v3_4_0.json")))
PY = OUT["_python"]
EX = {e["id"]: e for e in X.EXAMPLES}
ASSETS = os.path.join(ROOT, "03-materials", "ch04", "assets")
asset = lambda f: os.path.join(ASSETS, f)
fmt = lambda v: "{:,}".format(v)


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(os.path.join(TOOL, "sen0401_ch04_stories_v1_2_0.py"), "stories04")
STORY = {s["id"]: s for s in ST.STORIES}


def val(ex, i=0):
    return ast.literal_eval(OUT[ex][i][1])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the five parts of the deck, and the key concepts of the research: every one stands in a table row with its meaning and its everyday analogy (D4, D11)
# ------------------------------------------------------------------------------------------------------------------------------------------------
P1, P2, P3, P4, P5 = X.P1, X.P2, X.P3, X.P4, X.P5
PARTS = [(P1, "Keys"), (P2, "Legacy"), (P3, "Bech32"), (P4, "Formats"), (P5, "Advanced")]
CONCEPTS = {  # part -> [(label as the research names it, meaning, analogy)]
 P1: [("Keys and Addresses", "The secret numbers that control coins, and the public names that receive them.", "Think of a house key and the street address on the door."),
      ("Public Key Cryptography", "Two linked keys: one stays secret, the other can be shared with everyone.", "Think of a padlock anyone can snap shut but only you can open."),
      ("Private Keys", "A secret 256-bit number; whoever knows it can spend the coins.", "Think of the one key to your front door."),
      ("Public Keys", "A point on the curve computed from the private key; safe to publish.", "Think of the lock on your door: everyone can see it."),
      ("key pair", "A private key together with the public key computed from it.", "Think of a key and the one lock it fits."),
      ("entropy", "How unpredictable a secret is, counted in bits.", "Think of the dice rolls a thief would have to guess."),
      ("Elliptic Curve Cryptography Explained", "Keys built from points on a curve and a multiplication that cannot be undone.", "Think of stirring milk into coffee: easy to do, hopeless to undo."),
      ("secp256k1", "The curve y squared equals x cubed plus 7 that Bitcoin uses.", "Think of the one game board that every player agrees on."),
      ("generator point", "The fixed point G from which every public key is counted.", "Think of the starting square of a board game."),
      ("point at infinity", "The zero of the curve: adding it to a point changes nothing.", "Think of zero on a number line."),
      ("elliptic curve multiplication", "Adding a point to itself k times, done fast by doubling.", "Think of folding paper: eight folds make 256 layers.")],
 P2: [("Output and Input Scripts", "An output locks coins with a condition; an input supplies what unlocks it.", "Think of a locker and the code that opens it."),
      ("output script", "The locking condition stored in a transaction output.", "Think of the lock fitted to a parcel locker."),
      ("input script", "The data that satisfies the lock when the coins are spent.", "Think of the code you type to open the locker."),
      ("IP Addresses: The Original Address for Bitcoin (P2PK)", "The first Bitcoin paid to an IP address; the output script held the full public key.", "Think of mailing a parcel to a building's blueprint, not its street address."),
      ("P2PK", "Pay to public key: the output script holds the public key itself.", "Think of a sealed box that shows its whole lock to everyone."),
      ("Legacy Addresses for P2PKH", "Short text that names the hash of a public key; it starts with 1.", "Think of a bank account number instead of your ID card."),
      ("P2PKH", "Pay to public key hash: the output script holds only a 20-byte hash.", "Think of a locker that shows a number, never the shape of the key."),
      ("commitment", "A hash that fixes a value now and lets you reveal it later.", "Think of a sealed envelope holding your prediction."),
      ("SHA256", "A hash function: any input becomes a 32-byte fingerprint.", "Think of a fingerprint: small, unique and impossible to reverse."),
      ("RIPEMD-160", "A second hash function that gives a 20-byte fingerprint.", "Think of a photocopier that shrinks a page to a stamp."),
      ("HASH160", "SHA256 followed by RIPEMD-160: the 20-byte hash of a public key.", "Think of two sieves in a row: the finer one decides."),
      ("Base58check Encoding", "Version byte, payload and checksum written in base58.", "Think of a parcel with a label, a content and a seal."),
      ("base58", "An alphabet of 58 letters and digits without look-alike characters.", "Think of a font with no confusable letters."),
      ("checksum", "Four bytes of a double SHA256 that catch typing mistakes.", "Think of the check digit at the end of a barcode."),
      ("version prefix", "The first byte says what follows: 00 for a key hash, 05 for a script hash.", "Think of the country code at the start of a phone number."),
      ("Compressed Public Keys", "33 bytes: the x coordinate and one byte that says whether y is even or odd.", "Think of a map reference that says the column and up or down."),
      ("uncompressed public key", "65 bytes: a 04 byte, then both x and y in full.", "Think of giving both map coordinates in full.")],
 P3: [("Legacy Pay to Script Hash (P2SH)", "An address that commits to the hash of a whole script; it starts with 3.", "Think of a safe-deposit box whose contents you show only when you open it."),
      ("P2SH", "Pay to script hash: spending reveals the script and then satisfies it.", "Think of a locked briefcase opened in front of the cashier."),
      ("redeem script", "The script behind a P2SH hash; it is revealed and run when the coins are spent.", "Think of the instructions sealed inside the envelope."),
      ("collision attack", "Finding any two different inputs that give the same hash.", "Think of finding two strangers with the same fingerprint."),
      ("preimage attack", "Finding an input that gives one particular hash.", "Think of finding the person behind one given fingerprint."),
      ("Bech32 Addresses", "SegWit addresses in lowercase letters and digits with a stronger checksum.", "Think of a postcode that also detects a mistyped letter."),
      ("Problems with Bech32 Addresses", "Letters inserted before a final p slip past the old checksum.", "Think of extra tick marks at the end of a ruler that nobody notices."),
      ("Bech32m", "The same encoding with a new checksum constant, used from witness version 1.", "Think of a corrected second edition of the same form."),
      ("bech32", "The original encoding and checksum, still used for witness version 0.", "Think of the first edition of the form."),
      ("witness version", "The first value in the address: 0 for the first SegWit, 1 for Taproot.", "Think of the version number printed on a form."),
      ("witness program", "The data after the version: a key hash or a script hash.", "Think of the filled-in field of the form."),
      ("human-readable part", "The letters before the 1 that name the network: bc, tb.", "Think of the country code on a number plate.")],
 P4: [("Private Key Formats", "One key, several spellings: raw hex, WIF and WIF-compressed.", "Think of one amount written in figures, in words and as tally marks."),
      ("WIF", "Wallet import format: Base58Check of a version byte 80 and the key.", "Think of a key packed in a labelled travel case."),
      ("WIF-compressed", "WIF with a final 01 byte that marks the key as compressed.", "Think of a luggage tag that says travel light."),
      ("Compressed Private Keys", "Not a smaller key: a flag that tells a wallet to use compressed public keys.", "Think of a note that says use the short form of my name.")],
 P5: [("Advanced Keys and Addresses", "Beyond a plain random key: chosen address prefixes and printed keys.", "Think of a custom number plate and a spare key kept in a drawer."),
      ("Vanity Addresses", "A vanity address starts with chosen letters, found by trying many keys.", "Think of a custom number plate you must keep applying for."),
      ("Paper Wallets", "A key and its address printed on paper and kept offline.", "Think of a banknote locked in a drawer.")],
}
CROWS = {}
for _p, _rows in CONCEPTS.items():
    for _r in _rows:
        if len(_r[1]) > 84 or len(_r[2]) > 84: raise SystemExit("REFUSED: concept row too long for its table cell: %s" % _r[0])
        CROWS[_r[0]] = _r


def research_concepts():
    f = sorted(glob.glob(os.path.join(ROOT, "03-materials", "ch04", "rdodi", "sen0401_ch04_research_v*.ttl")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    txt = open(f, encoding="utf-8").read()
    return f, re.findall(r"a sen04(?:01|14):PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", txt)


def norm(t):
    t = re.sub(r"\([^)]*\)", " ", t.lower()); t = re.sub(r"[^a-z0-9]+", " ", t).split()
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in t)


_f, _labels = research_concepts()
_rowtext = norm(" ".join(r[0] + " " + r[1] + " " + r[2] for r in CROWS.values()))
_missing = [l for l in _labels if norm(l) not in _rowtext]
if _missing: raise SystemExit("REFUSED: research concepts without a row of meaning and everyday analogy: %s" % _missing)

DIV = {  # part -> (subtitle, notes, [labels of the three concepts named on the divider])
 P1: ("From one secret number to a point that nobody can run backwards",
      "Part 1 starts with the secret itself. A private key is only a number, a public key is a point computed from it, and the curve makes that computation a one-way street.",
      ["Private Keys", "Public Keys", "secp256k1"]),
 P2: ("From a public key to the address that people read aloud",
      "Part 2 turns a public key into the first kind of Bitcoin address. Two hashes shorten the key to twenty bytes, and Base58Check adds a version and a checksum that catches typing mistakes.",
      ["P2PKH", "HASH160", "Base58check Encoding"]),
 P3: ("Addresses that commit to a script, and the second alphabet",
      "Part 3 covers the addresses that came after the first kind. P2SH commits to a whole script, and SegWit's Bech32 and Bech32m add a version, a program and a stronger checksum.",
      ["P2SH", "Bech32 Addresses", "Bech32m"]),
 P4: ("The same private key, written in the forms a wallet can import",
      "Part 4 is about writing a private key down. The same number can appear as hex or as WIF, and one extra byte tells the wallet whether to use compressed public keys.",
      ["WIF", "WIF-compressed", "Compressed Private Keys"]),
 P5: ("Chosen prefixes, printed keys and an address with no key",
      "Part 5 goes beyond a plain random key. A vanity address costs work in proportion to its letters, a paper wallet must be tested, and a valid address can still have no key.",
      ["Vanity Addresses", "Paper Wallets", "commitment"]),
}
for _p, (_s, _n, _l) in DIV.items():
    for _x in _l:
        if _x not in CROWS: raise SystemExit("REFUSED: divider concept %s has no row" % _x)
        if len(_x.split()) > 4: raise SystemExit("REFUSED: divider pill over 4 words (D10): %s" % _x)
ANALOGIES = []
relp = lambda f: os.path.relpath(asset(f), HERE)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# the code slides: title, subtitle, takeaway, notes; and the executed result as a picture
# ------------------------------------------------------------------------------------------------------------------------------------------------
TEXT = {
 "ex01": ("A private key is a number below n", "The book's example key, and the edges of the range", "Any whole number from 1 to n minus 1 is a key",
          "A private key is a very large number between 1 and n minus 1. Zero and n itself are not allowed. Every number inside the range is a valid key, which is why choosing one at random is safe."),
 "ex02": ("Entropy: bits an attacker must guess", "Why a Bitcoin key needs 256 fair coin flips", "Only truly random choices reach the 256 bits of a key",
          "Entropy counts how many bits of guessing a secret withstands. A PIN has 13 bits and a long password 79. Only 256 fair coin flips match a Bitcoin key, so a key must come from a proper random source."),
 "ex03": ("The curve secp256k1 and its generator", "Checking that G really lies on the curve", "The curve is one short formula: y squared = x cubed + 7",
          "Bitcoin's curve is y squared equals x cubed plus 7, counted modulo a 256-bit prime. We test that the generator point G satisfies the formula. Every public key starts from this one fixed point."),
 "ex04": ("Doubling and adding: k times G", "How one multiplication reaches a huge number", "Doubling reaches a 256-bit key in a few hundred steps",
          "Multiplying G by k means adding G to itself k times. Doubling makes this fast: a key of 253 bits needs a few hundred doublings and additions, not 10 to the 76 steps."),
 "ex05": ("The point at infinity on a toy curve", "A curve over 17 numbers, small enough to list", "Multiples of a point repeat; the cycle closes at infinity",
          "On a toy curve we can list every multiple of a point. The ninth multiple is the point at infinity, the zero of the curve, and then the list starts over. Bitcoin's curve works the same way with a vastly larger cycle."),
 "ex06": ("One-way: the work to find a key", "Why the public key cannot be run backwards", "Each extra bit doubles the attacker's work",
          "Finding k from k times G means trying keys one by one, about half of them on average. A 20-bit key falls after half a million tries. A 256-bit key needs about 10 to the 77, which is out of reach."),
 "ex07": ("A public key has two encodings", "Compressed keys keep x and the parity of y", "A compressed key is 33 bytes; the full one is 65",
          "A public key is a point with two coordinates. The uncompressed form writes both after a 04 byte. The compressed form writes x and one byte for the parity of y, and y is recovered from x."),
 "ex08": ("P2PK holds the key, P2PKH only its hash", "Two output scripts for the same public key", "P2PKH shows a commitment to the key, not the key",
          "The original output script, P2PK, contains the public key itself. P2PKH contains only a 20-byte hash of it. The hash is a commitment: the key is revealed only when the coins are spent."),
 "ex09": ("HASH160 is SHA256 then RIPEMD-160", "Two hashes turn a 33-byte key into 20 bytes", "Two hashes in a row: 33 bytes in, 20 bytes out",
          "HASH160 first applies SHA256 and then RIPEMD-160. The 33-byte key becomes 32 bytes and then 20 bytes. The result is the number that a legacy address stands for."),
 "ex10": ("Base58Check, step by step", "Version, hash and checksum become an address", "An address is 25 bytes written in 34 characters",
          "A legacy address has three parts: a version byte, the 20-byte key hash and a four-byte checksum. Written in base58 they give a 34-character string. The leading 00 version byte becomes the first character, 1."),
 "ex11": ("The checksum catches every single typo", "Every one-character mistake, tried one by one", "A single typo is caught almost every time",
          "We change one character of the address in every possible way: 1,938 variants. A wallet that checks the four-byte checksum rejects every one of them. A random typo passes only about once in 4.3 billion."),
 "ex12": ("P2SH commits to a whole script", "A two-of-three multisignature behind one address", "A P2SH address hides the script until spending",
          "P2SH lets an address stand for any script. We build a two-of-three multisignature script of 105 bytes and hash it with HASH160. The address starts with 3 and reveals the script only when the coins are spent."),
 "ex13": ("Collision and preimage: bits of work", "Why a 160-bit hash is weaker for scripts", "A collision costs only half the bits of a hash",
          "Finding any two inputs with one hash takes about 2 to the n over 2 tries; finding an input for a given hash takes 2 to the n. A 160-bit hash gives only 80 bits against collisions, which is why SegWit scripts use SHA256."),
 "ex14": ("A Bech32 address, taken apart", "Network, version, program and checksum", "Split at the last 1: name, version, program, checksum",
          "A Bech32 address has four parts. The network name bc, a separator 1, the data and a six-letter checksum. The first data letter is the witness version, and the rest is the witness program."),
 "ex15": ("Witness version and witness program", "Three addresses from the book, decoded", "Version 0 for older SegWit; version 1 for Taproot",
          "The decoder returns the witness version and the program. Version 0 holds a 20-byte key hash or a 32-byte script hash. Version 1 holds a 32-byte Taproot key and makes the address start with bc1p."),
 "ex16": ("Bech32 accepts the extra q, Bech32m does not", "The weakness that Bech32m repaired", "Bech32m changed one constant and closed the gap",
          "In Bech32 a q inserted before a final p leaves the checksum valid, so a typo can go unnoticed. The strings from the book all pass the old check and fail the new one. Bech32m changes the constant to close the gap."),
 "ex17": ("WIF: a private key dressed for travel", "Base58Check of version 80, the key and a flag", "The final 01 byte says: use compressed public keys",
          "Wallet import format wraps the private key in Base58Check. The version byte is 80. A trailing 01 byte, added only for compressed keys, makes the string one byte longer and changes its first letter to K or L."),
 "ex18": ("One private key, two addresses", "Compressed and uncompressed keys hash differently", "The flag in WIF decides which address a wallet watches",
          "One private key gives two public key encodings, and each hashes to a different address. Coins sent to one address are not seen at the other. The compressed flag in the WIF tells a wallet which one to use."),
 "ex19": ("Vanity search: 58 times harder per letter", "Trying keys until the address starts as chosen", "Every extra letter costs about 58 times more work",
          "A vanity address is found by trying keys until the text fits. One chosen letter is quick. Each further letter divides the chance by 58, so six letters need about 38 billion tries, and the work cannot be shortcut."),
 "ex20": ("A paper wallet must give back its address", "Print, scan and check before funding", "Test the paper before you put coins on it",
          "A paper wallet prints a WIF key and its address. Before any coins are sent, decode the WIF and confirm that the key reproduces the printed address. A smudged character is found while the paper is still empty."),
 "ex21": ("The eater address is valid but keyless", "A message spelled in base58, with a good checksum", "A valid checksum is not proof that a key exists",
          "The address spells a message in base58 letters and then closes with letters that make the checksum right. Wallets accept it without a warning. Nobody holds a key for it, so coins sent there are gone for good."),
}
RESULT_CAP = {"ex01": "Result: five numbers, valid or not", "ex02": "Result: bits of entropy of five secrets", "ex03": "Result: the generator point and the curve", "ex04": "Result: multiples of G and the work",
              "ex05": "Result: the cycle of one point", "ex06": "Result: tries as a power of ten", "ex07": "Result: the two encodings", "ex08": "Result: the two output scripts",
              "ex09": "Result: bytes after each hash", "ex10": "Result: the three parts of an address", "ex11": "Result: every typo, tested", "ex12": "Result: script, hash and address",
              "ex13": "Result: bits of work, by attack", "ex14": "Result: the parts of the address", "ex15": "Result: three decoded addresses", "ex16": "Result: the same strings, two checksums",
              "ex17": "Result: the two WIF forms", "ex18": "Result: two addresses, one key", "ex19": "Result: expected tries per letter", "ex20": "Result: the paper wallet round trip",
              "ex21": "Result: the parts of the eater address"}


TEXT["ex11"] = TEXT["ex11"][:3] + (TEXT["ex11"][3].replace("1,938", fmt(val("ex11", 0)[0])),)
TEXT["ex12"] = TEXT["ex12"][:3] + (TEXT["ex12"][3].replace("105 bytes", "%d bytes" % val("ex12", 0)[0]),)


def visual(s, ex, x, y, w):
    """draws the executed result of one example from its recorded values; returns (height used, reading line)"""
    if ex == "ex01":
        okv, bits = val(ex, 0), val(ex, 1)
        names = ["0", "1", "the book's key", "n - 1", "n"]
        rows = [["Key", "Bits", "Valid?"]] + [[names[i], bits[i], "yes" if okv[i] else "no"] for i in range(5)]
        table(s, x, y, w, [1.4, 0.7, 1.0], rows, rowh=0.32, hot={i for i in range(5) if not okv[i]}, align=["l", "c", "c"])
        return 6 * 0.32, "Valid keys fill the range from 1 to n - 1, about 2 to the power %d of them." % val(ex, 1)[4]
    if ex == "ex02":
        vals = val(ex, 0)
        chart(s, x, y, w, 2.3, "bar", ["4-digit PIN", "8 lowercase letters", "12 keyboard symbols", "256 coin flips"], [("bits", vals)], fmt="0.0", pointcolors=[ORANGE, ORANGE, ORANGE, TEAL], size=8)
        return 2.3, "A 12-symbol password has %s bits; a key needs %d." % (vals[2], val(ex, 1))
    if ex == "ex03":
        on, pbits, xs, form = val(ex, 0), val(ex, 1), val(ex, 2), val(ex, 3)
        rows = [["Question", "Answer"], ["G on the curve?", "yes" if on else "no"], ["p has bits", pbits], ["x of G begins", xs], ["p = 2^256 - 2^32 - 977?", "yes" if form else "no"]]
        table(s, x, y, w, [1.75, 1.35], rows, rowh=0.34, align=["l", "l"])
        return 5 * 0.34, "One formula and one fixed point: nothing else is needed to start."
    if ex == "ex04":
        xs, cnt = val(ex, 1), val(ex, 2)
        rows = [["n", "x of n times G (8 hex)"]] + [[str(i + 1) + "G", xs[i]] for i in range(4)]
        table(s, x, y, w, [0.8, 2.3], rows, rowh=0.34, align=["l", "l"])
        return 5 * 0.34, "The book's key needs %d doublings and %d additions." % (cnt[0], cnt[1])
    if ex == "ex05":
        pts = val(ex, 1); order = val(ex, 0)
        rows = [["n", "n times P"]] + [[str(i + 1), "infinity" if p is None else "(%d, %d)" % p] for i, p in enumerate(pts)]
        table(s, x, y, w, [0.8, 2.3], rows, rowh=0.25, size=9, hot={len(pts) - 1}, align=["l", "l"])
        return len(rows) * 0.25, "After %d steps the walk reaches infinity and repeats." % order
    if ex == "ex06":
        pw = val(ex, 0)
        chart(s, x, y, w, 2.3, "bar", ["20-bit key", "40-bit key", "80-bit key", "128-bit key", "256-bit key"], [("power of ten", pw)], fmt="0", pointcolors=[ORANGE] * 4 + [TEAL], size=8)
        return 2.3, "A 20-bit key falls after about %s tries; a 256-bit key needs 10 to the %d." % (fmt(val(ex, 1)), pw[4])
    if ex == "ex07":
        a, same, saving = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Form", "Prefix", "Bytes", "Holds"], ["Compressed", "02 or 03" if a[2] in (2, 3) else "?", a[0], "x and parity"], ["Uncompressed", "%02d" % a[3], a[1], "x and y"]]
        table(s, x, y, w, [1.0, 0.75, 0.5, 0.85], rows, rowh=0.4, size=9.5, align=["l", "l", "c", "l"])
        return 3 * 0.4, "Compressed is %.0f percent shorter, and decompressing returns the same point: %s." % (100 * saving, same)
    if ex == "ex08":
        n, ok, last = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Output script", "Bytes", "Holds"], ["P2PK", n[0], "the public key"], ["P2PKH", n[1], "a 20-byte hash"]]
        table(s, x, y, w, [1.2, 0.6, 1.3], rows, rowh=0.4, align=["l", "c", "l"])
        return 3 * 0.4, "The hash inside P2PKH equals HASH160 of the key: %s. Both end in opcode %s (CHECKSIG)." % (ok, hex(last[0]))
    if ex == "ex09":
        n = val(ex, 0)
        chart(s, x, y, w, 2.25, "bar", ["Public key", "After SHA256", "After RIPEMD-160"], [("bytes", [n[0], n[1], n[2]])], fmt="0", pointcolors=[TEAL, ORANGE, ORANGE], size=8.5)
        return 2.25, "The 20 bytes are %s... and match HASH160: %s." % (val(ex, 1)[:8], n[3])
    if ex == "ex10":
        n, chk, addr, same, h8 = val(ex, 0), val(ex, 1), val(ex, 2), val(ex, 3), val(ex, 4)
        rows = [["Part", "Bytes", "Value"], ["Version", 1, "00"], ["Key hash", 20, h8 + "..."], ["Checksum", 4, chk], ["Together", n[0], "%d characters" % n[1]]]
        table(s, x, y, w, [1.0, 0.6, 1.5], rows, rowh=0.34, align=["l", "c", "l"], hot={3})
        return 5 * 0.34, "The address %s starts with %s; the one-step library function gives the same text: %s." % (addr, n[2], same)
    if ex == "ex11":
        tried, acc = val(ex, 0); good = val(ex, 1); big = val(ex, 2)
        rows = [["Test", "Count"], ["Typos tried", fmt(tried)], ["Typos accepted", acc], ["Original valid?", "yes" if good else "no"]]
        table(s, x, y, w, [1.9, 1.2], rows, rowh=0.36, align=["l", "r"], hot={1})
        return 4 * 0.36, "A random typo passes the check about once in %s tries." % fmt(big)
    if ex == "ex12":
        n, h12, addr = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Item", "Value"], ["Redeem script", "%d bytes" % n[0]], ["Its HASH160", h12 + "..."], ["Address starts", "%s, %d characters" % (n[1], n[2])]]
        table(s, x, y, w, [1.2, 1.9], rows, rowh=0.36, align=["l", "l"])
        return 4 * 0.36, "Address %s... commits to the script; spending reveals all %d bytes." % (addr[:12], n[0])
    if ex == "ex13":
        v = val(ex, 0)
        chart(s, x, y, w, 2.3, "bar", ["HASH160 collision", "HASH160 preimage", "SHA256 collision", "SHA256 preimage"], [("bits of work", v)], fmt="0", pointcolors=[ORANGE, TEAL, ORANGE, TEAL], size=8)
        return 2.3, "A 160-bit hash gives %d bits against collisions; SHA256 gives %d." % (v[0], v[2])
    if ex == "ex14":
        p, addr, ln = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Part", "Value"], ["Network (HRP)", p[0]], ["Separator", "1"], ["Version letter", "%s = 0" % p[1]], ["Program letters", "%d = 20 bytes" % p[2]], ["Checksum", p[3]]]
        table(s, x, y, w, [1.4, 1.7], rows, rowh=0.3, align=["l", "l"])
        return 6 * 0.3, "The whole address, %d characters: %s" % (ln, addr)
    if ex == "ex15":
        d, st, ln = val(ex, 0), val(ex, 1), val(ex, 2)
        names = ["P2WPKH", "P2WSH", "P2TR"]
        rows = [["Kind", "Starts", "Version", "Bytes", "Chars"]] + [[names[i], st[i], d[i][0], d[i][1], ln[i]] for i in range(3)]
        table(s, x, y, w, [0.8, 0.6, 0.65, 0.5, 0.55], rows, rowh=0.36, size=9.5, align=["l", "l", "c", "c", "c"])
        return 4 * 0.36, "Version 1 changes the letter after 1 from q to p."
    if ex == "ex16":
        both, lens = val(ex, 0), val(ex, 1)
        rows = [["Length", "Bech32", "Bech32m"]] + [[lens[i], "accepted" if both[0][i] else "rejected", "accepted" if both[1][i] else "rejected"] for i in range(4)]
        table(s, x, y, w, [0.9, 1.1, 1.1], rows, rowh=0.34, align=["c", "l", "l"], hot={0, 1, 2, 3} if not any(both[1]) else None)
        return 5 * 0.34, "Each string has more q letters before the last p."
    if ex == "ex17":
        a, dec, flag = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Form", "Starts", "Chars", "Bytes"], ["WIF", a[0], a[1], dec[0]], ["WIF-compressed", a[2], a[3], dec[1]]]
        table(s, x, y, w, [1.3, 0.6, 0.6, 0.6], rows, rowh=0.4, align=["l", "c", "c", "c"])
        return 3 * 0.4, "The decoded bytes are 80, the 32-byte key and, when compressed, a final %02d." % flag
    if ex == "ex18":
        t, pair = val(ex, 0), val(ex, 1)
        rows = [["Public key", "Bytes", "Address"], ["Uncompressed", 65, pair[0]], ["Compressed", 33, pair[1]]]
        table(s, x, y, w, [1.05, 0.5, 1.55], rows, rowh=0.5, size=9, align=["l", "c", "l"])
        return 3 * 0.5, "Two different addresses from one key: %s." % ("yes" if t[2] else "no")
    if ex == "ex19":
        n_, tries = val(ex, 0), val(ex, 1)
        chart(s, x, y, w, 2.3, "bar", ["%d letter%s" % (m, "" if m == 1 else "s") for m in range(1, 7)], [("tries", tries)], fmt="#,##0", log=True, pointcolors=[ORANGE] * 5 + [TEAL], size=8)
        return 2.3, "Our one letter took %d tries (address %s...); six letters take %s on average." % (n_[0], n_[1], fmt(tries[5]))
    if ex == "ex20":
        ok, lens, fl = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Step", "Result"], ["Print", "WIF %d characters, address %d" % lens], ["Scan", "version 0x%02x, flag 0x%02x" % fl], ["Restore the key", "from the WIF text"], ["Same address?", "yes" if ok else "no"]]
        table(s, x, y, w, [1.15, 1.95], rows, rowh=0.36, align=["l", "l"], hot={3})
        return 5 * 0.36, "Only when this reads yes should coins go to the address."
    if ex == "ex21":
        t, n21, h = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Part", "Value"], ["Message", t[0]], ["Closing letters", t[1]], ["Checksum valid?", "yes" if t[2] else "no"], ["Decoded bytes", "%d = 1 + 20" % n21]]
        table(s, x, y, w, [1.2, 1.9], rows, rowh=0.36, size=9.5, align=["l", "l"], hot={3})
        return 5 * 0.36, "The 20-byte hash %s... was never computed from a key." % h[:8]
    raise SystemExit("no picture for " + ex)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# slide builders: each draws one slide and returns its entry of the plan (kind, title, items, take, bg) for the owner checks that read deck_plan_v3_4_0.json
# ------------------------------------------------------------------------------------------------------------------------------------------------
def s_title(d, k, n):
    s = d.new("Chapter 3 showed the software that checks the rules. Chapter 4 opens the smallest secret it protects, a private key, and follows it to the address that people read aloud. Every number in this deck was computed with the chapter's own Python library.")
    labels = [("k", "private key"), ("K", "public key"), ("1J7m...", "address")]
    for i, (a, b) in enumerate(labels):
        x = 0.6 + i * 1.75
        text(s, x, 0.8, 1.35, 0.8, [a], size=22 if i < 2 else 15, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.OVAL, fill=[TEAL, TEAL, ORANGE][i])
        text(s, x - 0.1, 1.68, 1.55, 0.3, [b], size=11, color=MUTED, align="c")
        if i < 2: arrow(s, x + 1.4, 1.2, x + 1.7, 1.2, color=ORANGE)
    text(s, 0.6, 2.2, 5.5, 1.1, ["Chapter 4: Keys and Addresses"], size=30, font=SERIF, anchor="m")
    text(s, 0.6, 3.35, 5.5, 0.7, ["From a secret number to the string you can safely read out loud"], size=16, italic=True, color=MUTED)
    picture(s, asset("mbc3_0402.png"), 6.4, 0.7, 3.1, 3.1, "Figure 4-2: the curve y squared = x cubed + 7 drawn over the real numbers", mode="fit")
    text(s, 6.4, 3.85, 3.1, 0.4, ["Figure 4-2, Mastering Bitcoin 3rd edition, Antonopoulos and Harding, CC BY-SA 4.0"], size=8.5, color=MUTED)
    text(s, 0.6, 4.3, 8.8, 0.3, ["Python %s; every result is computed by the chapter library; no Bitcoin Core node was run." % PY], size=11, color=MUTED)
    text(s, 0.6, 4.68, 7.9, 0.35, ["SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University"], size=10.5, color=MUTED)
    number(s, k, n)
    return dict(kind="title", title="Chapter 4: Keys and Addresses", items=[{"t": "img", "path": relp("mbc3_0402.png"), "cap": "Figure 4-2, Mastering Bitcoin 3rd edition, CC BY-SA 4.0"}, {"t": "flow", "steps": [a for a, _ in labels]}, {"t": "foot"}], bg="light")


def s_route(d, k, n, ranges, ncode):
    s = d.new("The route has five parts that follow one secret from a number to an address. Three true stories and twenty-one code examples are spread across them, and every example has a picture of its result.")
    frame(d, s, k, n, "Today's route", "Five parts around one key; every range is a slide you can jump to", "Five parts, three true stories, twenty-one examples")
    names = ["1. Questions and the chapter map"] + ["%d. %s" % (i + 2, PARTS[i][0]) for i in range(5)] + ["7. Summary, resources, closing"]
    for i, a in enumerate(names):
        cx, cy = 0.5 + (i % 3) * 2.15, 1.4 + (i // 3) * 1.12
        text(s, cx, cy, 2.0, 1.0, [[(a, {"bold": True, "font": SERIF, "size": 11.5})], [("(slides %d-%d)" % ranges[i], {"size": 10.5, "color": MUTED})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD,
             line=LINE, pad=0.1, anchor="m", radius=0.1)
    stats = [(str(n), "slides, numbered bottom-right"), ("3", "true stories, each told by 5N1K"), (str(ncode), "code examples, each with a picture of its result")]
    for i, (a, b) in enumerate(stats):
        y = 1.4 + i * 1.12
        rect(s, 6.95, y, 2.55, 1.0, CARD, line=LINE)
        text(s, 7.1, y + 0.05, 2.25, 0.42, [a], size=22, font=SERIF, color=ORANGE, anchor="m")
        text(s, 7.1, y + 0.5, 2.25, 0.45, [b], size=10.5, color=MUTED)
    return dict(kind="content", title="Today's route", items=[{"t": "boxes"}, {"t": "stat"}], take="Five parts, three true stories, twenty-one examples")


def s_questions(d, k, n):
    s = d.new("The six questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all six has understood the chapter.")
    frame(d, s, k, n, "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary")
    qs = ["What is a private key, and what makes one safe to use?", "How does a private key become a public key, and why can it not be reversed?",
          "How does a public key become a legacy address, and why does it carry a checksum?", "What do P2SH, Bech32 and Bech32m change about addresses?",
          "How is a private key written down so that a wallet can import it?", "Why can an address be valid and still have no key behind it?"]
    for i, q in enumerate(qs):
        y = 1.4 + i * 0.58
        text(s, 0.5, y, 0.44, 0.44, [str(i + 1)], size=14, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.OVAL, fill=TEAL)
        text(s, 1.12, y, 8.38, 0.44, [q], size=13, anchor="m")
    return dict(kind="content", title="The questions this chapter answers", items=[{"t": "numlist", "items": qs}])


def s_map(d, k, n):
    s = d.new("One secret travels five steps. Random bits become a private key, the curve turns it into a public key, two hashes shorten it, and an encoding with a checksum makes the address. The parts of this deck follow the same path.")
    frame(d, s, k, n, "The chapter in one picture", "One secret, five steps; the parts of the deck follow them", "Random bits, a key, a point, a hash, an address")
    steps = [("1 Entropy", "256 random bits, kept secret."), ("2 Private key k", "A number between 1 and n - 1."), ("3 Public key K", "The point k times G."),
             ("4 HASH160", "SHA256, then RIPEMD-160: 20 bytes."), ("5 Address", "Version, hash and checksum in text.")]
    w, gap = 1.62, 0.225
    for i, (a, b) in enumerate(steps):
        x = 0.5 + i * (w + gap)
        text(s, x, 1.7, w, 0.5, [a], size=12, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL if i < 4 else ORANGE, radius=0.2)
        text(s, x, 2.4, w, 0.9, [b], size=11.5)
        if i < 4: arrow(s, x + w + 0.01, 1.95, x + w + gap - 0.01, 1.95, color=ORANGE)
    text(s, 0.5, 3.6, 9.0, 0.9, ["Every step runs forward easily and backwards never: you can always compute the next stage, but you cannot recover the one before it."], size=14, color=MUTED, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         fill=CARD, line=LINE, pad=0.15, anchor="m", radius=0.1)
    return dict(kind="content", title="The chapter in one picture", items=[{"t": "flow", "steps": [a for a, _ in steps]}, {"t": "text"}], take="Random bits, a key, a point, a hash, an address")


def s_divider(d, k, n, part, idx):
    sub, notes, labels = DIV[part]
    s = d.new(notes)
    text(s, 0.6, 0.45, 8.8, 0.8, [part], size=28 if len(part) <= 34 else 26, font=SERIF, anchor="m")
    text(s, 0.6, 1.28, 8.8, 0.4, [sub], size=15, italic=True, color=MUTED, anchor="m")
    m = len(labels); cw = (8.8 - (m - 1) * 0.2) / m
    for i, lab in enumerate(labels):
        _, mean, ana = CROWS[lab]; x = 0.6 + i * (cw + 0.2)
        text(s, x, 1.95, cw, 0.42, [lab], size=12, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL, pad=0.06, radius=0.3)
        text(s, x, 2.48, cw, 0.8, [mean], size=11.5)
        text(s, x, 3.34, cw, 0.62, [ana], size=11.5, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": lab, "analogy": ana, "slide": k})
    gf = table(s, 0.6, 4.3, 8.8, [8.8 / 5.0] * 5, [[p[1] for p in PARTS]], size=10, rowh=0.4, head=False, align=["c"] * 5)
    for j in range(5):
        c = gf.table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = rgb(ORANGE if j == idx else CARD)
        for r in c.text_frame.paragraphs[0].runs: r.font.color.rgb = rgb(WHITE if j == idx else MUTED); r.font.bold = (j == idx)
    number(s, k, n)
    return dict(kind="section", title=part, sub=sub, items=[{"t": "groups", "items": [{"pill": a, "meaning": CROWS[a][1], "analogy": CROWS[a][2]} for a in labels]}, {"t": "striptable"}], bg="light")


def s_concepts(d, k, n, part, rows, idx, parts):
    short = dict(PARTS)[part]
    suffix = " (%d of %d)" % (idx, parts) if parts > 1 else ""
    names = ", ".join(r[0] for r in rows[:3])
    s = d.new("These rows pair each concept of the part %s with something you already know. Say the meaning first, then the comparison, in your own words. The code slides that follow run the same ideas." % part)
    frame(d, s, k, n, "%s: concepts, with everyday pictures%s" % (short, suffix), "Each row: the idea in one line, then something you already know", "Think of each row as a flashcard: the concept, then a picture you know")
    tb = [["Concept", "In short", "Think of"]] + [[r[0], r[1], r[2].replace("Think of ", "", 1)[:1].upper() + r[2].replace("Think of ", "", 1)[1:]] for r in rows]
    rh = 0.46 if len(rows) >= 6 else 0.5
    table(s, 0.5, 1.4, 9.0, [2.3, 3.4, 3.3], tb, size=11, rowh=rh)
    for r in rows: ANALOGIES.append({"concept": r[0], "analogy": r[2].replace("Think of ", "", 1)[:1].upper() + r[2].replace("Think of ", "", 1)[1:], "slide": k})
    return dict(kind="content", title="%s: concepts%s" % (short, suffix), items=[{"t": "table"}], take="Think of each row as a flashcard: the concept, then a picture you know")


def when_runs(iso, long):
    return [(iso, {}), (" (%s)" % long, {})]


STORIES = {
 "NewDirections1976": dict(title="The 1976 paper that split the key in two", sub="3 June 1976 · public-key cryptography is born", take="Every address in this chapter stands on one 1976 idea", pic_w=3.0, focus=0.15,
    alt="Whitfield Diffie at the Royal Society in 2017", credit_tail=", Wikimedia Commons",
    n5=[("WHO", "Whitfield Diffie and Martin Hellman, cryptographers at Stanford; both received the 2015 Turing Award."),
        ("WHAT", "The paper 'New Directions in Cryptography': a key split into a public half and a private half."),
        ("WHEN", when_runs("1976-06-03", "manuscript received; printed in November 1976")),
        ("WHERE", "Stanford University, California; IEEE Transactions on Information Theory, volume IT-22."),
        ("WHY", "Secret keys had to be carried to every partner; the authors wanted to remove that need."),
        ("HOW", "Each user publishes one half and keeps the other; a one-way computation links them, as in this chapter.")],
    notes="In 1976 Whitfield Diffie and Martin Hellman asked whether two people could talk privately without first sharing a secret. Their answer was a key split in two. Bitcoin's elliptic-curve multiplication is a later form of the same idea."),
 "Base58Design": dict(title="Why 58? Satoshi left the reasons in the file", sub="8 January 2009 · a design memo inside base58.h", take="Address formats are human-factors engineering, written into the source", pic_w=3.0, focus=0.3,
    alt="Bronze bust of Satoshi Nakamoto in Budapest", credit_tail=", Wikimedia Commons - a stand-in, since the author's face is unknown",
    n5=[("WHO", "Satoshi Nakamoto, the pseudonymous author of Bitcoin's first software; the file's copyright line names him."),
        ("WHAT", "A comment in base58.h that lists four reasons for dropping 0, O, I and l and all punctuation."),
        ("WHEN", when_runs("2009-01-08", "version 0.1 announced; the memo's own date is not recorded")),
        ("WHERE", "The file src/base58.h in the bitcoin/bitcoin source tree on GitHub."),
        ("WHY", "People copy addresses by hand, in e-mail and by double-click, so the text must survive all three."),
        ("HOW", "Of 62 letters and digits the four look-alikes go, so 58 remain: the alphabet of every legacy address.")],
    notes="The first lines of base58.h are a design memo. It gives four human reasons: look-alike characters, punctuation that breaks selection, line breaks in e-mail, and double-clicking. The alphabet of every legacy address is a usability decision."),
 "BitcoinEater": dict(title="The address that eats coins", sub="6 October 2026 · figures fetched from a block explorer", take="An address commits to a key; it does not prove that a key exists", pic_w=2.45,
    alt="The Bitcoin logo, a stand-in picture", credit_tail=", Wikimedia Commons - a stand-in, since an address has no picture",
    n5=[("WHO", "Thousands of anonymous senders; Blockstream Explorer recorded their deposits. Nobody holds the key."),
        ("WHAT", "The valid address 1BitcoinEaterAddressDontSendf59kuE holds 13.41747849 bitcoin in 5,832 outputs, none ever spent."),
        ("WHEN", when_runs("2026-10-06", "the day this balance was fetched")),
        ("WHERE", "The Bitcoin main chain; the address page of blockstream.info shows every deposit."),
        ("WHY", "A checksum catches typing mistakes, not a missing key, so wallets accept the address and the coins stay."),
        ("HOW", "A message was written in base58 letters, and the last letters were chosen so that the checksum fits.")],
    notes="This address was made by spelling a message and then closing it with letters that satisfy the checksum. No private key exists for it. Thousands of senders still paid into it, and not one coin has ever left."),
}


def s_story(d, k, n, sid, a):
    st = STORY[sid]; s = d.new(a["notes"])
    frame(d, s, k, n, a["title"], a["sub"])
    if a["pic_w"] == 3.0: picture(s, asset(st["photo"]), 0.5, 1.35, 3.0, 2.45, a["alt"], focus=a.get("focus", 0.3))
    else: picture(s, asset(st["photo"]), 0.5 + (3.0 - a["pic_w"]) / 2, 1.35, a["pic_w"], 2.45, a["alt"], mode="fit")
    credit = "Picture: " + st["credit"] + a["credit_tail"]
    text(s, 0.5, 3.88, 3.0, 0.62, [credit], size=8.5, color=MUTED)
    for i, (lab, body) in enumerate(a["n5"]):
        parts = [(lab + " ", {"bold": True, "color": ORANGE, "size": 10.5})] + ([(body, {"size": 10.5})] if isinstance(body, str) else [(b, dict(o, size=10.5)) for b, o in body])
        text(s, 3.75, 1.33 + i * 0.52, 5.75, 0.48, [parts], size=10.5)
    host = re.sub(r"^https?://(www\.)?", "", st["link"]).split("/")[0]
    text(s, 3.75, 4.5, 5.75, 0.3, [[("READ ", {"bold": True, "color": ORANGE, "size": 10.5}), (st["linkLabel"], {"size": 10.5, "color": TEAL, "link": st["link"]}), (" - " + host, {"size": 10.5, "color": MUTED})]], size=10.5)
    return dict(kind="content", title=a["title"], sub=a["sub"], items=[{"t": "img", "path": relp(st["photo"]), "cap": credit}, {"t": "beats", "items": ["%s %s" % (l, b if isinstance(b, str) else "".join(x for x, _ in b)) for l, b in a["n5"]]},
                {"t": "factrow", "who": st["who"], "where": st["where"], "when": st["when"], "link": st["link"], "linkText": st["linkLabel"]}], take=a["take"])


def s_code(d, k, n, ex):
    e = EX[ex]; title, sub, take, notes = TEXT[ex]
    s = d.new(notes); frame(d, s, k, n, title, sub, take)
    out = OUT[ex][0][1]
    if len(out) > 62: raise SystemExit("REFUSED %s: output line over 62 characters (D12)" % ex)
    y = 1.4; lay = []
    for gi, g in enumerate(e["groups"]):
        for l in g["lines"]:
            if len(l) + 4 > 62: raise SystemExit("REFUSED %s: code line over 62 characters with its prompt (D12): %s" % (ex, l))
        rows = [code_runs(l) for l in g["lines"]]
        if gi == len(e["groups"]) - 1: rows.append([(out, {"color": CODE_OUT})])
        th = est(rows, 5.4, 10, mono=True) + 0.02; nh = est([g["note"]], 5.7, 11) + 0.04
        lay.append((y, rows, th, g["note"], nh)); y += th + 0.2 + 0.06 + nh + 0.12
    for (y0, rows, th, note, nh) in lay:      # all listings first, so that the executed rows of the slide follow one another (the deck check reads them in shape order)
        rect(s, 0.5, y0, 5.7, th + 0.2, CODE, radius=0.06)
    for (y0, rows, th, note, nh) in lay:
        text(s, 0.66, y0 + 0.1, 5.4, th, rows, size=10, font=MONO)
    for (y0, rows, th, note, nh) in lay:      # then the plain-language note beside each listing
        text(s, 0.5, y0 + th + 0.2 + 0.06, 5.7, nh, [note], size=11)
    if y > 4.95: raise SystemExit("REFUSED %s: the listings need %.2f in (limit 4.95)" % (ex, y))
    text(s, 0.5, y - 0.04, 5.7, 0.2, ["run under Python %s - K is the chapter library of the page (%s)" % (PY, X.LIB)], size=9, color=MUTED)
    items = [{"t": "codeblocks", "ex": ex}]
    text(s, 6.4, 1.4, 3.1, 0.4, [RESULT_CAP[ex]], size=11, bold=True, color=TEAL)
    used, reading = visual(s, ex, 6.4, 1.85, 3.1)
    text(s, 6.4, 1.85 + used + 0.12, 3.1, 0.7, [reading], size=11)
    items.append({"t": EX[ex]["picture"] == "native chart" and "chart" or "table", "ex": ex})
    return dict(kind="content", title=title, sub=sub, items=items, take=take)


def s_curve_fig(d, k, n):
    s = d.new("Figure 4-4 shows one doubling on the curve of figure 4-2. Draw the tangent at G, find where it meets the curve again, and mirror that point across the x-axis. The result is 2G, and repeating the step gives 4G and 8G.")
    frame(d, s, k, n, "Points on a curve: doubling G", "How the curve turns one point into many", "Tangent, meeting point, mirror image: that is one doubling")
    picture(s, asset("mbc3_0404.png"), 0.9, 1.35, 3.25, 3.25, "Figure 4-4: doubling the point G with a tangent and a reflection on the x-axis", mode="fit")
    text(s, 4.4, 1.5, 2.1, 1.3, ["The red line is the curve; the blue and green arrows are the steps of one doubling."], size=11, color=MUTED)
    text(s, 4.4, 3.0, 2.1, 0.9, ["G, 2G, 4G and 8G are labelled on the picture."], size=11, color=MUTED)
    text(s, 0.5, 4.62, 6.0, 0.36, ["Figure 4-4, Mastering Bitcoin 3rd edition, Antonopoulos and Harding, CC BY-SA 4.0"], size=8.5, color=MUTED)
    steps = [("1 Tangent", "Draw the tangent to the curve at G."), ("2 Meeting point", "It meets the curve once more."), ("3 Mirror", "Reflect that point on the x-axis: this is 2G.")]
    for i, (a, b) in enumerate(steps):
        text(s, 6.75, 1.4 + i * 1.0, 2.75, 0.88, [[(a, {"bold": True, "font": SERIF, "size": 12.5})], [(b, {"size": 11})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.12, anchor="m", radius=0.1)
    return dict(kind="content", title="Points on a curve: doubling G", items=[{"t": "img", "path": relp("mbc3_0404.png")}, {"t": "cards"}], take="Tangent, meeting point, mirror image: that is one doubling")


def s_pipe_fig(d, k, n):
    s = d.new("Figure 4-7 is the whole road from public key to address. SHA256 and RIPEMD-160 shrink the key to 20 bytes, a version byte and a checksum make 25, and base58 writes them as 34 characters. Each step is a function you have just run.")
    frame(d, s, k, n, "From public key to address", "The pipeline of figure 4-7, with the sizes that we measured", "Each arrow is a function that you have just run")
    picture(s, asset("mbc3_0407.png"), 0.5, 1.35, 2.9, 3.2, "Figure 4-7: public key, SHA256, RIPEMD-160, Base58Check with version 00, Bitcoin address", mode="fit")
    text(s, 0.5, 4.6, 2.9, 0.4, ["Figure 4-7, Mastering Bitcoin 3rd edition, Antonopoulos and Harding, CC BY-SA 4.0"], size=8.5, color=MUTED)
    n9, n10 = val("ex09", 0), val("ex10", 0)
    steps = [("Public key", "%d bytes" % n9[0]), ("SHA256", "%d bytes" % n9[1]), ("RIPEMD-160", "%d bytes: the key hash" % n9[2]), ("Version and checksum added", "%d bytes" % n10[0]), ("Base58 text", "%d characters" % n10[1])]
    for i, (a, b) in enumerate(steps):
        y = 1.4 + i * 0.66
        text(s, 3.9, y, 5.6, 0.46, [[(a + "  ", {"bold": True, "font": SERIF, "size": 12}), (b, {"size": 12, "color": TEAL})]], size=12, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD if i < 4 else SOFT, line=LINE, pad=0.12, anchor="m", radius=0.12)
        if i < 4: arrow(s, 6.7, y + 0.46, 6.7, y + 0.66, color=ORANGE)
    return dict(kind="content", title="From public key to address", items=[{"t": "img", "path": relp("mbc3_0407.png")}, {"t": "flow", "steps": [a for a, _ in steps]}], take="Each arrow is a function that you have just run")


def s_summary(d, k, n):
    s = d.new("Each row answers one of the six opening questions in a line. If you can say each answer in your own words, using the everyday pictures of this chapter, you have the chapter.")
    frame(d, s, k, n, "Summary: the six answers", "The questions of slide 3, answered", "Entropy, a point, a hash, a checksum, a flag, no key")
    rows = [["Question", "Answer in one line"],
            ["1 What is a private key?", "A random number between 1 and n - 1 with 256 bits of entropy."],
            ["2 How does it give a public key?", "Multiply G by k with doubling and adding; nobody can run it backwards."],
            ["3 How does that give an address?", "HASH160, a version byte and four checksum bytes, written in base58."],
            ["4 What do P2SH and Bech32 change?", "P2SH hashes a script; Bech32 and Bech32m add a version, a program, a stronger checksum."],
            ["5 How is a key written down?", "WIF: Base58Check of version 80, the key and a final 01 when compressed."],
            ["6 Valid address, no key?", "A checksum catches typos, not a missing key: the eater address holds coins nobody can spend."]]
    table(s, 0.5, 1.4, 9.0, [2.9, 6.1], rows, size=11, rowh=0.46)
    return dict(kind="content", title="Summary: the six answers", items=[{"t": "table"}], take="Entropy, a point, a hash, a checksum, a flag, no key")


RES = [("Read", "Mastering Bitcoin, chapter 4 (source text)", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/ch04_keys.adoc", "The chapter this deck follows."),
       ("Read", "Elliptic curve cryptography: a gentle introduction", "https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/", "Pictures of the curve, step by step."),
       ("Read", "Bitcoin Wiki: technical background of addresses", "https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses", "From key to address, in steps."),
       ("Standards and papers", "Diffie and Hellman: New Directions (PDF)", "https://www-ee.stanford.edu/~hellman/publications/24.pdf", "The 1976 paper behind the key pair."),
       ("Standards and papers", "BIP 173: Bech32 addresses", "https://bips.dev/173/", "The format of native SegWit addresses."),
       ("Standards and papers", "BIP 350: Bech32m addresses", "https://bips.dev/350/", "The fix used from witness version 1."),
       ("Try", "The eater address on blockstream.info", "https://blockstream.info/address/1BitcoinEaterAddressDontSendf59kuE", "Open it and watch nothing move."),
       ("Try", "base58.h in bitcoin/bitcoin (source)", "https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/base58.h", "Satoshi's four reasons, in the code."),
       ("Watch", "Elliptic Curves - Computerphile (video)", "https://www.youtube.com/watch?v=NF1pwjL9-DE", "The curve behind every public key."),
       ("Community", "Bitcoin Stack Exchange", "https://bitcoin.stackexchange.com/", "Ask a question, read the answers.")]


def s_resources(d, k, n):
    s = d.new("These links are all open and free. Start with the chapter source, read the three standards or papers, open the eater address on an explorer, and watch the video for the curve behind every public key.")
    frame(d, s, k, n, "Resources: read, try, watch, ask", "Every link was opened on 25 October 2026; free to use", "Open the eater address tonight and watch nothing move")
    for i, (kind, lab, url, why) in enumerate(RES):
        col, row = i // 5, i % 5
        x, y = 0.5 + col * 4.6, 1.4 + row * 0.72
        text(s, x, y, 4.4, 0.64, [[(kind + "  ", {"bold": True, "color": ORANGE, "size": 9}), (lab, {"size": 11.5, "bold": True, "color": TEAL, "link": url})], [(why, {"size": 10, "color": MUTED})]], size=11)
    groups = []
    for head in ("Read", "Standards and papers", "Try", "Watch", "Community"):
        groups.append({"head": head, "rows": [[lab, url, why] for kd, lab, url, why in RES if kd == head]})
    return dict(kind="content", title="Resources: read, try, watch, ask", items=[{"t": "links", "groups": groups}], take="Open the eater address tonight and watch nothing move")


def s_closing(d, k, n):
    s = d.new("That is the whole path from a secret number to an address. Chapter 5 asks what happens when the secret is lost, and how a word list can bring every key back. Bring your questions.")
    rect(s, 0.5, 0.9, 9.0, 3.7, CODE, radius=0.04)
    text(s, 0.9, 1.3, 8.2, 1.1, ["Questions?"], size=44, font=SERIF, color=WHITE, anchor="m")
    text(s, 0.9, 2.5, 8.2, 0.5, ["From a secret number to an address you can read aloud"], size=18, italic=True, color=C_NUM)
    text(s, 0.9, 3.3, 8.2, 0.45, ["Next: chapter 5, Wallet Recovery: from a word list back to every key"], size=15, font=SERIF, color=CODE_OR)
    text(s, 0.9, 4.0, 8.2, 0.4, ["Python %s; every result in this deck was computed by the chapter library, not typed" % PY], size=11, color=CODE_TXT)
    number(s, k, n)
    return dict(kind="closing", title="Questions?", items=[{"t": "bullets", "items": ["Next: chapter 5, Wallet Recovery: from a word list back to every key"]}], bg="dark")


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the order of the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
def split(rows, size):
    n = len(rows); parts = -(-n // size); per = -(-n // parts)
    return [rows[i:i + per] for i in range(0, n, per)]


SEQ = [("title",), ("route",), ("questions",), ("map",)]
for _i, (_part, _short) in enumerate(PARTS):
    SEQ.append(("div", _part, _i))
    _chunks = split(CONCEPTS[_part], 6)
    for _j, _c in enumerate(_chunks, 1): SEQ.append(("concepts", _part, _c, _j, len(_chunks), _i))
    SEQ += {0: [("story", "NewDirections1976"), ("code", "ex01"), ("code", "ex02"), ("code", "ex03"), ("curvefig",), ("code", "ex04"), ("code", "ex05"), ("code", "ex06")],
            1: [("code", "ex07"), ("code", "ex08"), ("code", "ex09"), ("story", "Base58Design"), ("code", "ex10"), ("pipefig",), ("code", "ex11")],
            2: [("code", "ex12"), ("code", "ex13"), ("code", "ex14"), ("code", "ex15"), ("code", "ex16")],
            3: [("code", "ex17"), ("code", "ex18")],
            4: [("code", "ex19"), ("code", "ex20"), ("story", "BitcoinEater"), ("code", "ex21")]}[_i]
SEQ += [("summary",), ("resources",), ("closing",)]


def main():
    n = len(SEQ); ncode = sum(1 for q in SEQ if q[0] == "code")
    pos = [i + 1 for i, q in enumerate(SEQ) if q[0] == "div"]; summ = [j + 1 for j, q in enumerate(SEQ) if q[0] == "summary"][0]
    ranges = [(3, pos[0] - 1)] + [(pos[i], (pos[i + 1] - 1) if i + 1 < len(pos) else summ - 1) for i in range(5)] + [(summ, n)]
    d = Deck(); code_slides = {}; plan = []
    for k, q in enumerate(SEQ, 1):
        kind = q[0]
        if kind == "title": e = s_title(d, k, n)
        elif kind == "route": e = s_route(d, k, n, ranges, ncode)
        elif kind == "questions": e = s_questions(d, k, n)
        elif kind == "map": e = s_map(d, k, n)
        elif kind == "div": e = s_divider(d, k, n, q[1], q[2])
        elif kind == "concepts": e = s_concepts(d, k, n, q[1], q[2], q[3], q[4])
        elif kind == "story": e = s_story(d, k, n, q[1], STORIES[q[1]])
        elif kind == "code": e = s_code(d, k, n, q[1]); code_slides[q[1]] = k
        elif kind == "curvefig": e = s_curve_fig(d, k, n)
        elif kind == "pipefig": e = s_pipe_fig(d, k, n)
        elif kind == "summary": e = s_summary(d, k, n)
        elif kind == "resources": e = s_resources(d, k, n)
        elif kind == "closing": e = s_closing(d, k, n)
        e["n"] = k; e["notes"] = d.last_notes; e.setdefault("bg", "light"); e.setdefault("sub", ""); plan.append(e)
    deck_path = os.path.join(ROOT, "03-materials", "ch04", DECK_NAME)
    d.prs.save(deck_path)
    import shutil
    shutil.copyfile(deck_path, os.path.join(HERE, "sen0401_ch04_deck_v3_4_0.pptx"))     # the copy the owner checks of the chapter's deck folder read by default (as for every earlier version)
    # the chapter-code manifest: the examples in the order of the deck's code slides, drawn from the same list
    wheel_path = os.path.join(ROOT, "03-materials", "ch04", "assets", WHEEL)
    lib_py = "sen0401_ch04_lib_v1_0_0.py"
    setup = "# setup: the chapter library of the page (K = the chapter 4 library); the page runs this before every example\n" + X.PRELUDE.rstrip("\n")
    exs = []
    for o, q in enumerate([q for q in SEQ if q[0] == "code"], 1):
        e = EX[q[1]]
        exs.append({"order": o, "id": e["id"], "name": e["name"], "slide": code_slides[e["id"]], "branch": e["branch"], "library": "sen0401_ch04_lib", "needs": ["setup"],
                    "code": "\n".join(e["lines"]), "show": [{"expression": x, "expected": r} for x, r in OUT[e["id"]]], "result_picture": e["picture"]})
    man = {"manifest": "chapter_code_ch04_v1_0_0", "chapter": 4, "deck": DECK_NAME, "deck_version": "3.4.0", "python_of_expected_values": PY,
           "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the chapter library defined in the page; the manifest equals the deck's code boxes",
           "library": {"module": "sen0401_ch04_lib", "file": "03-materials/ch04/assets/" + WHEEL, "sha256": hashlib.sha256(open(wheel_path, "rb").read()).hexdigest(), "modules": [os.path.splitext(lib_py)[0]],
                       "source": "08-tooling/" + lib_py, "source_sha256": hashlib.sha256(open(os.path.join(TOOL, lib_py), "rb").read()).hexdigest(),
                       "import": "import sen0401_ch04_lib_v1_0_0 as K", "requires": "Python standard library only (hashlib, math, struct); a pure-Python RIPEMD-160 is carried for runtimes without one"},
           "setup": {"code": setup, "data": {}}, "examples": exs}
    json.dump(man, open(os.path.join(ROOT, "03-materials", "ch04", "page", "chapter_code_ch04_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
    standin = {str(e["n"]): ["stand-in"] for e in plan if any("stand-in" in (it.get("cap") or "") for it in e["items"])}
    meta = {"title": "Chapter 4: Keys and Addresses", "sub": "SEN0401, third-edition deck 3.4.0", "version": "3.4.0", "python": PY, "total": n,
            "redesign": "2026-10-25, task TK_Ch04_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
            "notes": "short reader's prose: 2-4 sentences, at most 60 words", "analogies": ANALOGIES,
            "honesty": {"title": ["no Bitcoin Core node"], "no_node": True, "notExecuted": [], "recorded": [], "standin": standin, "vectors": []}}
    json.dump({"meta": meta, "slides": plan}, open(os.path.join(HERE, "deck_plan_v3_4_0.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote %s (%d slides, %d code slides) and chapter_code_ch04_v1_0_0.json (%d examples)" % (DECK_NAME, n, len(code_slides), len(exs)))


if __name__ == "__main__":
    main()
