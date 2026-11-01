#!/usr/bin/env python3
"""Chapter 4 deck v3.6.0, picture slides part B: SegWit and Bech32, today's practice, assurance and identifiers (a NEW tool file; task TK_Ch04_DeckTeach_Build).
Native shapes and tables only; every number is computed from the chapter library or copied from the page's own definition of the concept. Heights are measured with the real font metrics."""
from deck_teach_kit_v3_6_0 import *
import random


# ---- SW: segregated witness upgrade -----------------------------------------------------------------------------------------------------------------
def SW(s):
    T(s, "before head", X0, 136, 900, 20, [P("Before: the identifier hashes everything, signatures included", 12, TEAL, True)])
    strip(s, "before", X0, 160, 900, [("version", 4, CARD, INK), ("inputs", 8, CARD, INK), ("outputs", 8, CARD, INK), ("signatures", 9, ORANGE, WHITE), ("lock time", 3, CARD, INK)], h=34, size=11)
    T(s, "before id", X0, 198, 900, 20, [P("txid = hash of all of it, so a third party who re-encodes a signature changes the identifier", 11, MUTE, False, True)])
    T(s, "after head", X0, 228, 900, 20, [P("After: the signatures move into a separate witness structure", 12, TEAL, True)])
    strip(s, "after txid", X0, 252, 560, [("version", 4, CARD, INK), ("inputs", 8, CARD, INK), ("outputs", 8, CARD, INK), ("lock time", 3, CARD, INK)], h=34, size=11)
    R(s, "witness part", 630, 252, 320, 34, fill=ORANGE, line=None, adj=0.12, paras=[P("witness: the signatures", 11, WHITE, True, align="c")])
    T(s, "after id", X0, 290, 900, 20, [P("txid hashes only the left part, so it no longer depends on the signatures; the right part is committed to separately", 11, MUTE, False, True)])
    c1 = card(s, "sw card", X0, 322, 440, "Segregated witness upgrade", "Moves the signatures and scripts of a transaction into a separate witness structure, so the transaction identifier no longer depends on them.", size=11.5, fill=SOFT, minh=84)
    c2 = card(s, "sw why", 510, 322, 440, "What it fixes", "A spender, not a third party, controls the identifier. Unconfirmed chains of payments become safe to build.", size=11.5, minh=84)
    bullets(s, ["Think of a parcel label: the address is printed on the box, and the signed receipt travels in a separate envelope that cannot change the label."], max(c1, c2) + 10, size=12)


# ---- NEST: segwit inside P2SH ----------------------------------------------------------------------------------------------------------------------
def NEST(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); h = K.hash160(c); redeem = b"\x00\x14" + h; assert len(redeem) == 22
    a_p2sh = K.p2sh(redeem); a_leg = K.p2pkh(c); a_seg = K.segwit_address("bc", 0, h)
    flow(s, 140, [("1  Redeem script", "OP_0 and the 20-byte key hash: %d bytes, %s..." % (len(redeem), redeem.hex()[:12])),
                  ("2  P2SH address", "The address is the HASH160 of that script with version 05: %s..." % a_p2sh[:8]),
                  ("3  Old payer", "Wallets that only know P2SH pay to it without any change."),
                  ("4  Spend", "The receiver reveals the script and the witness; segwit nodes check it.")], h=124, gap=14, size=11, head=12)
    rows = [("Way to pay the same key", "Address", "Characters"), ("P2PKH", a_leg, str(len(a_leg))), ("Segwit inside P2SH", a_p2sh, str(len(a_p2sh))), ("Native segwit (P2WPKH)", a_seg, str(len(a_seg)))]
    tb = table(s, "nested table", X0, 278, (230, 520, 150), rows, 28, size=11, hh=26)
    c1 = card(s, "nested card", X0, tb.bottom + 14, 440, "Segwit inside P2SH", "A P2SH address can wrap a witness program, so an older payer that only knows P2SH can pay a segwit receiver.", size=11.5, fill=SOFT, minh=60)
    bullets(s, ["A bridge. Think of an adapter plug: the old socket stays as it is and the new device still works."], tb.bottom + 20, size=12, x=510, w=440)


# ---- BCHERR: BCH code and error detection ----------------------------------------------------------------------------------------------------------
def BCHERR(s):
    a = K.segwit_address("bc", 0, K.PROG_WPKH); data = range(3, len(a)); rnd = random.Random(2026)
    single = det1 = 0
    for i in data:
        for ch in K.CHARSET:
            if ch != a[i]: single += 1; det1 += K.bech_check(a[:i] + ch + a[i + 1:]) is None
    def multi(k, trials):
        det = 0
        for _ in range(trials):
            b = list(a)
            for p in rnd.sample(list(data), k): b[p] = rnd.choice([c for c in K.CHARSET if c != a[p]])
            det += K.bech_check("".join(b)) is None
        return det, trials
    d2, t2 = multi(2, 20000); d4, t4 = multi(4, 20000)
    assert det1 == single and d2 == t2 and d4 == t4
    T(s, "addr head", X0, 136, 900, 20, [P("A bech32 address of %d characters, split by purpose" % len(a), 12, TEAL, True)])
    strip(s, "bech", X0, 160, 900, [("bc", 2, ORANGE, WHITE), ("1", 1, CARD, INK), ("q", 1, TEAL, WHITE), ("32 letters: the 20-byte program", 32, SOFT, INK), ("6 checksum letters", 6, TEAL, WHITE)], h=34, size=10.5)
    T(s, "bech legend", X0, 198, 900, 18, [P("bc = network   1 = separator   q = witness version 0   then the program letters   then the six checksum letters", 10.5, MUTE, False, True)])
    rows = [("Errors made in the address", "Tests", "Caught"), ("one wrong letter, every case", "{:,}".format(single), "{:,}".format(det1)), ("two wrong letters, at random", "{:,}".format(t2), "{:,}".format(d2)), ("four wrong letters, at random", "{:,}".format(t4), "{:,}".format(d4)),
            ("five or more wrong letters", "chance 1 in 2 to the 30", "1 in {:,} slip through".format(2 ** 30))]
    tb = table(s, "error table", X0, 226, (320, 270, 310), rows, 28, size=11.5, hh=26)
    c1 = card(s, "bch card", X0, tb.bottom + 12, 440, "BCH code", "An error-correcting code. The bech32 checksum is a BCH code of six 5-bit letters, 30 bits.", size=11.5, fill=SOFT, minh=64)
    c2 = card(s, "err card", 510, tb.bottom + 12, 440, "Error detection", "Four wrong letters or fewer are always caught, and Bitcoin Core can point to where.", size=11.5, minh=64)
    bullets(s, ["Think of a postcode that also notices a mistyped letter: the checksum is the spare part of the code."], max(c1, c2) + 8, size=11.5)


# ---- TYPES: P2WPKH, P2WSH, P2TR ----------------------------------------------------------------------------------------------------------------------
def TYPES(s):
    specs = [("Pay to witness public key hash (P2WPKH)", b"\x00\x14" + K.PROG_WPKH, [("OP_0", 1, "0"), ("push 20", 1, "14"), ("HASH160 of a public key, 20 bytes", 20, "")], K.segwit_address("bc", 0, K.PROG_WPKH), "bech32", "one key, as P2PKH commits"),
             ("Pay to witness script hash (P2WSH)", b"\x00\x20" + K.PROG_WSH, [("OP_0", 1, "0"), ("push 32", 1, "20"), ("SHA256 of a script, 32 bytes", 32, "")], K.segwit_address("bc", 0, K.PROG_WSH), "bech32", "any script, as P2SH commits"),
             ("Pay to taproot (P2TR)", b"\x51\x20" + K.PROG_TR, [("OP_1", 1, "1"), ("push 32", 1, "20"), ("a point on the curve, 32 bytes", 32, "")], K.segwit_address("bc", 1, K.PROG_TR), "bech32m", "a key, or more")]
    assert [len(x[1]) for x in specs] == [22, 34, 34]
    for i, (name, script, parts, addr, kind, what) in enumerate(specs):
        x = X0 + i * 306; w = 288
        hdr(s, "type head", x, 138, w, 40, name, size=11)
        R(s, "type body", x, 182, w, 216, fill=WHITE, line=LINE, adj=0.04)
        T(s, "type script", x + 10, 188, w - 20, 20, [P("Output script, %d bytes" % len(script), 11.5, TEAL, True)])
        strip(s, "type strip", x + 10, 212, w - 20, [(l, n, f, c, sh_) for (l, n, sh_), f, c in zip(parts, (ORANGE, CARD, SOFT), (WHITE, INK, INK))], h=32, size=10, minw=28)
        T(s, "type legend", x + 10, 248, w - 20, 40, [P("first byte: witness version; then a push (1-byte parts drawn wider)", 10.5, MUTE, False, True)])
        T(s, "type addr", x + 10, 292, w - 20, 40, [P("Address begins %s, %d characters, %s" % (addr[:4], len(addr), kind), 11.5, INK, True)])
        T(s, "type what", x + 10, 332, w - 20, 40, [P("Commits to: " + what, 11.5, INK)])
        T(s, "type ver", x + 10, 374, w - 20, 20, [P("Witness version %d" % (script[0] if script[0] == 0 else script[0] - 0x50), 11, MUTE, False, True)])
    bullets(s, ["Version 0 uses the older bech32 checksum, version 1 the corrected bech32m. Think of three kinds of locker: one for a single key, one for any rule you write, and one that can look like a single key."], 408, size=12)


# ---- LEN: bech32 length extension weakness -----------------------------------------------------------------------------------------------------------
def LEN(s):
    rows = [("The book's string", "Length", "Valid as bech32", "Valid as bech32m")]
    for e in K.EXT: rows.append(("", str(len(e)), str(K.bech_check(e) == K.BECH32), str(K.bech_check(e) == K.BECH32M)))
    tbl = table(s, "extension table", X0, 140, (470, 100, 160, 170), rows, 32, size=11, hh=28)
    for r, e in enumerate(K.EXT, 1):
        m = re.match(r"(.*?)(q+)(p)$", e); cell = tbl.table.cell(r, 0); pa = cell.text_frame.paragraphs[0]
        for ptxt, col, bold in ((m.group(1), INK, False), (m.group(2), ORANGE, True), (m.group(3), INK, False)):
            run = pa.add_run(); run.text = ptxt; set_run(run, 12, col, bold, False, "Courier New")
    assert all(K.bech_check(e) == K.BECH32 for e in K.EXT) and not any(K.bech_check(e) == K.BECH32M for e in K.EXT)
    c1 = card(s, "len card", X0, tbl.bottom + 14, 440, "Bech32 length extension weakness", "Adding or removing a q just before a final p keeps the checksum valid. The book's four strings differ only in their q letters (orange).", size=11.5, fill=SOFT, minh=96)
    c2 = card(s, "len why", 510, tbl.bottom + 14, 440, "Why it matters", "A typo that adds a letter would go unnoticed, and the fix is a new checksum constant, not a longer address.", size=11.5, minh=96)
    bullets(s, ["Think of a spell-checker that cannot see a doubled letter before the full stop: the word looks fine, and the page is wrong."], max(c1, c2) + 10, size=12)


# ---- B32M: bech32m address -----------------------------------------------------------------------------------------------------------------------------
def B32M(s):
    samples = [("Version 0, key hash", K.segwit_address("bc", 0, K.PROG_WPKH)), ("Version 0, script hash", K.segwit_address("bc", 0, K.PROG_WSH)), ("Version 1, Taproot key", K.segwit_address("bc", 1, K.PROG_TR))]
    R(s, "v0", X0, 142, 330, 56, fill=CARD, line=LINE, paras=[P("Witness version 0", 12.5, ORANGE, True, align="c"), P("checksum constant 1", 12, INK, True, align="c")])
    A(s, "to bech32", 385, 170, 425, 170, ORANGE, 2.0)
    R(s, "bech32", 430, 142, 190, 56, fill=SOFT, line=TEAL, paras=[P("bech32", 14, TEAL, True, align="c")])
    R(s, "v1", X0, 212, 330, 56, fill=CARD, line=LINE, paras=[P("Witness version 1 to 16", 12.5, ORANGE, True, align="c"), P("checksum constant 0x2bc830a3", 12, INK, True, align="c")])
    A(s, "to bech32m", 385, 240, 425, 240, ORANGE, 2.0)
    R(s, "bech32m", 430, 212, 190, 56, fill=SOFT, line=TEAL, paras=[P("bech32m", 14, TEAL, True, align="c")])
    card(s, "b32m card", 660, 142, 290, "Bech32m address", "Differs from bech32 only in the constant merged into the checksum, 0x2bc830a3 (%d) instead of 1, and is required for witness version 1 and later." % K.BECH32M, size=11, fill=SOFT, minh=126)
    assert [K.bech_check(a) for _, a in samples] == [K.BECH32, K.BECH32, K.BECH32M]
    rows = [("Address", "Constant that makes the checksum valid")] + [(lab + ": " + a, "1 (bech32)" if K.bech_check(a) == K.BECH32 else "0x2bc830a3 (bech32m)") for lab, a in samples]
    tb = table(s, "constant table", X0, 292, (690, 210), rows, 30, size=10.5, hh=26)
    bullets(s, ["Why a new constant: it repairs the length-extension weakness without changing anything else. Think of a corrected second edition of the same form: same layout, one printing error fixed."], tb.bottom + 12, size=12)


# ---- QR: QR code -------------------------------------------------------------------------------------------------------------------------------------------
def QR(s):
    a = K.segwit_address("bc", 0, K.PROG_WPKH).upper(); alnum = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"); assert all(ch in alnum for ch in a)
    n = len(a); bits_byte = 8 * n; bits_alnum = 11 * (n // 2) + 6 * (n % 2)
    T(s, "bars head", X0, 138, 500, 22, [P("Bits needed for the same %d-character address" % n, 12, TEAL, True)])
    yb = hbar(s, "qr", X0, 166, 540, [("byte mode (lowercase)", bits_byte, "%d bits" % bits_byte), ("alphanumeric mode (uppercase)", bits_alnum, "%d bits" % bits_alnum)], labw=260, valw=90, size=11, hi=1)
    card(s, "qr card", 610, 138, 340, "QR code", "A two-dimensional barcode that a camera can read. Its alphanumeric mode makes uppercase text about 45 percent more compact than the normal byte mode.", size=11.5, fill=SOFT, minh=116)
    rows = [("Largest QR code (version 40, low correction)", "Characters"), ("alphanumeric mode", "4,296"), ("byte mode", "2,953")]
    tb = table(s, "qr table", X0, yb + 6, (400, 150), rows, 30, size=11.5, hh=26)
    y = say(s, X0, tb.bottom + 12, 900, "Alphanumeric mode has 45 characters and no lowercase letters, so a bech32 address goes into a QR code in capitals; base58 needs both cases and falls back to byte mode. Capitals use 11 bits per two characters against 16, which is %d percent fewer bits here." % round(100 * (1 - bits_alnum / bits_byte)), size=11.5)
    bullets(s, ["Think of a suitcase packed with a vacuum bag: the same clothes take less room when they are in the right shape, and the smaller code scans faster."], y + 8, size=12)


# ---- DEFAULT: default address type ---------------------------------------------------------------------------------------------------------------
def DEFAULT(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); h = K.hash160(c)
    types = [("legacy", "P2PKH", K.p2pkh(c)), ("p2sh-segwit", "P2SH around P2WPKH", K.p2sh(b"\x00\x14" + h)), ("bech32", "P2WPKH", K.segwit_address("bc", 0, h)), ("bech32m", "P2TR (Taproot)", K.segwit_address("bc", 1, K.PROG_TR))]
    rows = [("addresstype value", "Output type", "Address begins", "Characters")] + [(a, b, c_[:4], str(len(c_))) for a, b, c_ in types]
    tbl = table(s, "default table", X0, 140, (200, 270, 230, 200), rows, 30, size=12, hh=28)
    for cell in tbl.table.rows[3].cells: cell.fill.solid(); cell.fill.fore_color.rgb = rgb(SOFT)
    y0 = tbl.bottom + 14
    T(s, "bars head", X0, y0, 450, 20, [P("Address length in characters", 12, TEAL, True)])
    yb = hbar(s, "length", X0, y0 + 24, 480, [(a, len(c_), str(len(c_))) for a, _, c_ in types], labw=130, valw=50, size=10.5, bh=18, gap=7, hi=2)
    c1 = card(s, "default card", 560, y0, 390, "Default address type", "Bitcoin Core's addresstype option defaults to bech32, a P2WPKH address (highlighted). The four values are legacy, p2sh-segwit, bech32 and bech32m, the last a Taproot address.", size=11.5, fill=SOFT, minh=110)
    bullets(s, ["A default shows what the reference software regards as current. Think of the factory setting on a phone: most users never change it."], max(yb, c1) + 8, size=12)


# ---- EXPORT: exporting a single key -------------------------------------------------------------------------------------------------------------------
def EXPORT(s):
    w = K.wif(K.BOOK_K)
    rows = [("Command", "Bitcoin Core 30.0 and later"), ("getnewaddress", "still there"), ("importdescriptors", "still there"), ("dumpprivkey", "removed"), ("importprivkey", "removed")]
    tb = table(s, "export table", X0, 140, (230, 220), rows, 28, size=11.5, hh=26)
    c1 = card(s, "export card", 540, 140, 410, "Exporting a single key", "Taking one private key out of a wallet as a WIF string. Deterministic descriptor wallets no longer export single keys.", size=11.5, fill=SOFT, minh=60)
    c2 = card(s, "export why", 540, c1 + 8, 410, "Why it is gone", "A leaked key plus some public data about a deterministic wallet can reveal every other key in it.", size=11.5, minh=60)
    y0 = max(tb.bottom, c2) + 14
    T(s, "descriptor head", X0, y0, 900, 22, [P("A single WIF key can still sit inside a descriptor", 12, TEAL, True)])
    y = codecard(s, "descriptor card", X0, y0 + 26, 900, ["wpkh(" + w + ")"], size=11)
    y = say(s, X0, y + 6, 900, "wpkh(...) asks for a P2WPKH output script for that key; importdescriptors takes the whole line, so the wallet knows exactly what it may watch.", size=11, color=MUTE, italic=True)
    bullets(s, ["Think of tearing one page out of a numbered ledger: the page can give away how the others are numbered."], y + 6, size=12)


# ---- BIP38: passphrase-protected key -------------------------------------------------------------------------------------------------------------------
def BIP38(s):
    ex = "6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi"
    flow(s, 140, [("Private key", "The 32-byte key to protect."), ("+ Passphrase", "A secret phrase chosen by the owner."), ("Encrypt", "BIP38 stretches the passphrase and encrypts the key."), ("58 characters", "A base58check string; this one begins %s." % ex[:2])], h=100, gap=14, size=11.5, head=12.5)
    T(s, "ex head", X0, 256, 600, 20, [P("An example record, %d characters" % len(ex), 12, TEAL, True)])
    y = codecard(s, "bip38 card", X0, 280, 600, [ex], size=11.5)
    rows = [("Part", "Holds"), ("the paper record", "something you have"), ("the passphrase", "something you know")]
    tb = table(s, "bip38 table", X0, y + 12, (300, 300), rows, 28, size=11.5, hh=26)
    c1 = card(s, "bip38 card2", 680, 256, 270, "Passphrase-protected key", "BIP38 encrypts a private key under a passphrase so it can be printed or stored without being usable by whoever finds it.", size=11, fill=SOFT, minh=130)
    bullets(s, ["Its status in the BIPs repository is Deployed, yet the comment summary reads Unanimously Discourage; the book does not cover it, and you meet it on old paper wallets.", "Think of a padlocked case whose combination you tell by phone."], max(tb.bottom, c1) + 8, size=11.5, gap=2)


# ---- SEED: deterministic wallet and seed -----------------------------------------------------------------------------------------------------------------
def SEED(s):
    seed = "f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73"
    keys = [hashlib.sha256(("%s + %d\n" % (seed, i)).encode()).hexdigest() for i in range(3)]
    assert keys[0][:8] == "50b18e0b" and all(0 < int(k, 16) < K.N for k in keys)
    addrs = [K.key_to_address(int(k, 16)) for k in keys]
    R(s, "seed box", X0, 196, 200, 60, fill=ORANGE, line=None, paras=[P("seed", 14, WHITE, True, align="c"), P(seed[:8] + "...", 11, WHITE, False, align="c")])
    for i, (k, a) in enumerate(zip(keys, addrs)):
        y = 140 + i * 74
        A(s, "seed arrow", 252, 226, 318, y + 28, ORANGE, 2.0)
        R(s, "derived key", 322, y, 300, 56, fill=CARD, line=LINE, paras=[P("key %d = hash of the seed and %d: %s..." % (i, i, k[:8]), 11, INK, True, align="c")], inset=4)
        A(s, "key to address", 626, y + 28, 664, y + 28, ORANGE, 2.0)
        R(s, "derived address", 668, y, 282, 56, fill=SOFT, line=TEAL, paras=[P(a, 10.5, INK, True, align="c")], inset=2)
    c1 = card(s, "seed card", X0, 372, 560, "Deterministic wallet and seed", "One random value, the seed, derives every private key by a repeatable procedure, so one backup covers every key.", size=11.5, fill=SOFT, minh=76)
    bullets(s, ["Think of a recipe book: write down one master recipe and you can cook every dish again."], 372, size=12, x=630, w=320)


# ---- REUSE: address reuse and privacy ---------------------------------------------------------------------------------------------------------------
def REUSE(s):
    T(s, "reuse head", X0, 138, 430, 22, [P("Reuse: one address receives three payments", 12, TEAL, True)])
    for i, lab in enumerate(("payment from Alice", "payment from Carol", "payment from Dan")):
        R(s, "payer", X0, 168 + i * 52, 170, 38, fill=CARD, line=LINE, paras=[P(lab, 11, INK, True, align="c")]); A(s, "payer arrow", 222, 187 + i * 52, 262, 242, ORANGE, 2.0)
    R(s, "one address", 266, 218, 214, 48, fill=ORANGE, line=None, paras=[P("one address", 12.5, WHITE, True, align="c")])
    T(s, "reuse read", X0, 330, 430, 40, [P("An onlooker sees all three payments together and can link every payer.", 11.5, INK, True)])
    T(s, "fresh head", 520, 138, 430, 22, [P("Fresh address for each payment", 12, TEAL, True)])
    for i, lab in enumerate(("payment from Alice", "payment from Carol", "payment from Dan")):
        R(s, "payer2", 520, 168 + i * 52, 170, 38, fill=CARD, line=LINE, paras=[P(lab, 11, INK, True, align="c")]); A(s, "payer2 arrow", 692, 187 + i * 52, 730, 187 + i * 52, ORANGE, 2.0)
        R(s, "addr2", 734, 168 + i * 52, 216, 38, fill=SOFT, line=TEAL, paras=[P("address %d" % (i + 1), 11.5, TEAL, True, align="c")])
    T(s, "fresh read", 520, 330, 430, 40, [P("Three unrelated addresses: nothing on the chain joins the payments.", 11.5, INK, True)])
    c1 = card(s, "reuse card", X0, 384, 560, "Address reuse and privacy", "Several payments to one address link them for anyone watching the blockchain. The eater address of the story shows 5,832 such deposits.", size=11.5, fill=SOFT, minh=86)
    bullets(s, ["Wallets give a new address on every call to getnewaddress. Think of a fresh envelope for every letter."], 384, size=12, x=630, w=320)


# ---- HW: hardware signing device -----------------------------------------------------------------------------------------------------------------------
def HW(s):
    R(s, "device zone", 440, 136, 510, 150, fill=SOFT, line=TEAL, lw=2.0, adj=0.04)
    T(s, "device label", 452, 140, 480, 20, [P("Hardware signing device: the key never leaves this box", 11.5, TEAL, True)])
    R(s, "prepare", X0, 168, 330, 88, fill=CARD, line=LINE, paras=[P("1  Computer or phone", 12, ORANGE, True, align="c"), P("prepares the unsigned transaction", 11, INK, align="c")], inset=6)
    A(s, "to device", 384, 212, 460, 212, ORANGE, 2.0)
    R(s, "shows", 464, 168, 220, 88, fill=WHITE, line=LINE, paras=[P("2  Device shows", 12, ORANGE, True, align="c"), P("amount and address, you confirm", 11, INK, align="c")], inset=6)
    R(s, "signs", 722, 168, 210, 88, fill=WHITE, line=LINE, paras=[P("3  Device signs", 12, ORANGE, True, align="c"), P("with the key inside", 11, INK, align="c")], inset=6)
    A(s, "inside", 686, 212, 720, 212, ORANGE, 2.0)
    R(s, "broadcast", X0, 306, 330, 60, fill=CARD, line=LINE, paras=[P("4  Computer broadcasts", 12, ORANGE, True, align="c"), P("the signed transaction", 11, INK, align="c")], inset=6)
    A(s, "back", 470, 288, 384, 326, ORANGE, 2.0)
    c1 = card(s, "hw card", 440, 306, 510, "Hardware signing device", "A small device whose only job is to hold private keys and sign with them; the less secure program that prepares and broadcasts never sees a key.", size=11.5, fill=SOFT, minh=76)
    bullets(s, ["Think of a notary with a stamp that is never lent out: you bring the paper, the notary stamps it, and the stamp stays in the office."], max(c1, 366) + 14, size=12)


# ---- TVXC: BIP350 test vectors and cross-checking -------------------------------------------------------------------------------------------------------
def TVXC(s):
    valid = ["BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4", "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7", "bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7kt5nd6y", "BC1SW50QGDZ25J",
             "bc1zw508d6qejxtdg4y5r3zarvaryvaxxpcs", "tb1qqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesrxh6hy", "tb1pqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesf3hn0c", "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqzk5jj0"]
    acc = sum(1 for v in valid if K.segwit_decode(v[:v.rfind("1")].lower(), v) is not None); assert acc == 8
    ours = K.key_to_address(K.BOOK_K)
    hdr(s, "tv head", X0, 138, 440, 28, "BIP350 test vectors")
    rows = [("Group of the BIP350 list", "Count"), ("valid bech32m strings", "7"), ("valid segwit addresses", "8"), ("invalid segwit addresses, each with its reason", "15"), ("valid ones this toolkit accepts, run for this slide", "%d of %d" % (acc, len(valid)))]
    tb = table(s, "tv table", X0, 170, (340, 100), rows, 28, size=11, hh=26)
    hdr(s, "xc head", 510, 138, 440, 28, "Cross-checking with independent software")
    for i, (lab, sub) in enumerate((("This chapter's toolkit", "computed just now"), ("Bitcoin Core 31.1", "run as an offline node"), ("The book's reference code", "bech32 reference implementation"))):
        R(s, "source", 510, 172 + i * 52, 250, 44, fill=CARD, line=LINE, paras=[P(lab, 11.5, ORANGE, True, align="c"), P(sub, 10.5, INK, align="c")], inset=3); A(s, "to same", 764, 194 + i * 52, 794, 242, ORANGE, 2.0)
    R(s, "same answer", 798, 212, 152, 60, fill=SOFT, line=TEAL, lw=2.0, paras=[P("same address", 11.5, TEAL, True, align="c"), P(ours[:10] + "...", 10.5, INK, align="c")], inset=3)
    y0 = max(tb.bottom, 334) + 12
    c1 = card(s, "tv card", X0, y0, 440, "A test vector", "An input with the output a correct implementation must give, published so implementers can check their work, including addresses of future witness versions.", size=11, fill=SOFT, minh=84)
    c2 = card(s, "xc card", 510, y0, 440, "Cross-checking", "Compare independent implementations on the same input. Two programs written apart rarely make the same mistake.", size=11, minh=84)
    bullets(s, ["Think of two accountants adding the same column: when both reach the same total, the total can be trusted."], max(c1, c2) + 10, size=12)


# ---- CTL: proof of control by a key ---------------------------------------------------------------------------------------------------------------------------
def CTL(s):
    msg = b"login 2026-11-01 challenge 4821"; z = int.from_bytes(hashlib.sha256(msg).digest(), "big"); d = K.BOOK_K; Q = K.ec_mul(d)
    sig = K.ecdsa_sign(d, z, int.from_bytes(hashlib.sha256(b"nonce of the proof slide").digest(), "big") % K.N)
    ok, bad = K.ecdsa_verify(Q, z, sig), K.ecdsa_verify(K.ec_mul(7), z, sig); assert ok and not bad
    R(s, "verifier", X0, 142, 200, 38, fill=TEAL, line=None, paras=[P("Verifier", 13, WHITE, True, align="c")]); R(s, "holder", 750, 142, 200, 38, fill=TEAL, line=None, paras=[P("Key holder", 13, WHITE, True, align="c")])
    steps = [("1  Challenge: " + msg.decode(), "to holder"), ("2  Signature (r, s) made with the private key", "to verifier"), ("3  Checked with the public key: %s" % ("valid" if ok else "invalid"), "none")]
    for i, (t, dr) in enumerate(steps):
        y = 194 + i * 48
        R(s, "step", 330, y, 340, 38, fill=CARD, line=LINE, paras=[P(t, 10.5, INK, True, align="c")], inset=3)
        if dr == "to holder": A(s, "arrow", 254, y + 19, 328, y + 19, ORANGE, 2.0); A(s, "arrow2", 672, y + 19, 748, y + 19, ORANGE, 2.0)
        elif dr == "to verifier": A(s, "arrow", 748, y + 19, 672, y + 19, ORANGE, 2.0); A(s, "arrow2", 328, y + 19, 254, y + 19, ORANGE, 2.0)
    c1 = card(s, "ctl card", X0, 350, 440, "Proof of control by a key", "Whoever holds a private key can prove control of the matching public key by signing, without a central registry or anyone's permission.", size=11.5, fill=SOFT, minh=84)
    c2 = card(s, "ctl why", 510, 350, 440, "Why it matters", "The same step runs in every Bitcoin payment: a node accepts a spend because the signature verifies, not because anyone vouches. Another key gives: %s." % ("valid" if bad else "invalid"), size=11.5, minh=84)
    bullets(s, ["Think of a stamp that only you own: anyone can look at the print and recognise it, nobody can make it without the stamp."], max(c1, c2) + 10, size=12)


# ---- URIDID: URI and DID --------------------------------------------------------------------------------------------------------------------------------------
def URIDID(s):
    hdr(s, "uri head", X0, 138, 440, 28, "Uniform resource identifier (URI)")
    strip(s, "uri", X0, 176, 440, [("https", 5, ORANGE, WHITE), ("example.org", 11, SOFT, INK), ("/keys/1", 7, CARD, INK)], h=34, size=10.5)
    T(s, "uri tags", X0, 214, 440, 18, [P("scheme            authority                path", 10.5, MUTE, False, True)])
    y1 = say(s, X0, 236, 440, "A web address is a URI. A URI is a compact sequence of characters that identifies a resource, so the same string names the same thing everywhere.", size=11.5)
    hdr(s, "did head", 510, 138, 440, 28, "Decentralized identifier (DID)")
    parts = "did:example:123456789abcdefghi".split(":"); assert parts == ["did", "example", "123456789abcdefghi"]
    strip(s, "did", 510, 176, 440, [(parts[0], 3, ORANGE, WHITE), (parts[1], 7, TEAL, WHITE), (parts[2], 18, SOFT, INK)], h=34, size=10.5)
    T(s, "did tags", 510, 214, 440, 18, [P("scheme    DID method    identifier specific to the method", 10.5, MUTE, False, True)])
    y2 = say(s, 510, 236, 440, "A DID is a URI that associates a subject with a DID document.", size=11.5)
    y0 = max(y1, y2) + 12
    c = card(s, "uri why", X0, y0, 440, "Why both appear here", "A DID is built to be decoupled from registries and certificate authorities: its controller proves control with a key, as a Bitcoin key pair does.", size=11.5, fill=SOFT, minh=96)
    R(s, "doc card", 510, y0, 440, 96, fill=CODEBG, line=None, adj=0.05)
    T(s, "doc text", 524, y0 + 6, 412, 86, [{"runs": [("DID document of did:example:123...", 11, "F2A860", True, False, "Courier New")]}, {"runs": [("  verification method: a public key", 11, "E6EDF3", False, False, "Courier New")]},
                                         {"runs": [("  proof of control: a signature made", 11, "E6EDF3", False, False, "Courier New")]}, {"runs": [("  with the matching private key", 11, "E6EDF3", False, False, "Courier New")]}])
    bullets(s, ["Think of an address on an envelope against a signature on a letter: the first says where to find you, the second proves it was you."], max(c, y0 + 96) + 10, size=12)
