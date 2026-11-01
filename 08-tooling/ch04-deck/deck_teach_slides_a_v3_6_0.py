#!/usr/bin/env python3
"""Chapter 4 deck v3.6.0, picture slides part A: public key cryptography, the curve and legacy addresses (a NEW tool file; task TK_Ch04_DeckTeach_Build).
Each function draws one slide with native shapes and tables; every number is computed from the chapter library (sen0401_ch04_lib_v1_0_0) or copied from the page's own definition of the concept.
Every slide says what the concept is, why it exists, how it works, shows it, and carries an everyday comparison. Heights are measured with the real font metrics, so nothing overlaps."""
from deck_teach_kit_v3_6_0 import *


# ---- SIG: digital signature --------------------------------------------------------------------------------------------------------------------
def SIG(s):
    z = int.from_bytes(hashlib.sha256(b"pay Bob 1 BTC").digest(), "big"); z2 = int.from_bytes(hashlib.sha256(b"pay Bob 2 BTC").digest(), "big")
    d = K.BOOK_K; Q = K.ec_mul(d); nonce = int.from_bytes(hashlib.sha256(b"nonce of this slide").digest(), "big") % K.N
    sig = K.ecdsa_sign(d, z, nonce); r, s_ = sig
    differ = sum(bin(a ^ b).count("1") for a, b in zip(hashlib.sha256(b"pay Bob 1 BTC").digest(), hashlib.sha256(b"pay Bob 2 BTC").digest()))
    checks = [("The message that was signed", K.ecdsa_verify(Q, z, sig)), ("The message changed to pay Bob 2 BTC", K.ecdsa_verify(Q, z2, sig)), ("Checked against another public key", K.ecdsa_verify(K.ec_mul(2), z, sig))]
    assert [c[1] for c in checks] == [True, False, False]
    flow(s, 140, [("1  Sign", "The signer mixes the hash of the message with the private key and a fresh number: out come two numbers, r and s."),
                  ("2  Send", "The message, the signature (r, s) and the public key travel together; none of them is secret."),
                  ("3  Verify", "Anyone recomputes from the public key; only a signature made with the matching private key passes.")], h=118, gap=18, size=11.5, head=12.5)
    T(s, "table head", X0, 276, 520, 22, [P("Three checks of one signature (r %s, s %s)" % (hex(r)[2:10], hex(s_)[2:10]), 12, TEAL, True)])
    rows = [("What is checked", "Result")] + [(a, "valid" if b else "invalid") for a, b in checks]
    table(s, "sig table", X0, 302, (380, 140), rows, 28, size=11.5, hh=26)
    card(s, "why signature", 600, 276, 350, "Why it exists", "Coins must be spendable only by their owner, and nobody should have to hand over the key to prove it. A digital signature is that proof.", size=11.5, fill=SOFT, minh=130)
    bullets(s, ["Changing one letter of the message changes the hash in %d of 256 bits, so the old signature fails. Think of a wax seal that only your ring can press." % differ], None, size=12, w=900)


# ---- L0: lambda ----------------------------------------------------------------------------------------------------------------------------------
def L0(s):
    tiles = [("lambda", 190, ORANGE, WHITE, "makes a function with no name"), ("x", 120, TEAL, WHITE, "the one input it takes"), (":", 90, INK, WHITE, "ends the inputs"), ("0 < x < K.N", 330, SOFT, INK, "the value it hands back")]
    x = X0
    for t, w, f, c, lab in tiles:
        R(s, "tile " + t, x, 138, w, 40, fill=f, line=TEAL if f == SOFT else None, paras=[{"runs": [(t, 14, c, True, False, "Courier New")], "align": "c"}], adj=0.12)
        T(s, "tile label", x, 182, w, 40, [P(lab, 11, MUTE, False, True, align="c")]); x += w + 14
    ok = lambda v: 0 < v < K.N
    xs = [("0", 0), ("1", 1), ("the book's key", K.BOOK_K), ("n - 1", K.N - 1), ("n", K.N)]
    rows = [("x", "ok(x)")] + [(lab, str(ok(v))) for lab, v in xs]
    T(s, "table head", X0, 216, 420, 22, [P("Five inputs run through it", 12, TEAL, True)])
    tb = table(s, "lambda table", X0, 240, (230, 190), rows, 24, size=11.5, hh=24)
    T(s, "def head", 520, 216, 430, 22, [P("The same helper with a name, written with def", 12, TEAL, True)])
    y = codecard(s, "def card", 520, 240, 430, ["def ok(x):", "    return 0 < x < K.N"], size=11.5)
    T(s, "def read", 520, y + 6, 430, 40, [P("Both forms give the same answers; ok is just a name that holds the function.", 11, MUTE, False, True)])
    bullets(s, ["A lambda is a function written on one line, right where it is needed; it may take several inputs, as in lambda a, c. Three code slides use one.",
                "Use a lambda for a tiny job done once and a named def for anything reused. Think of a sticky note with a formula."], None, size=12)


# ---- RAND: secure randomness ----------------------------------------------------------------------------------------------------------------------
def RAND(s):
    rows = [("Module", "Made for", "What an observer can learn", "Use it for a key?"),
            ("secrets", "Secrets: it draws from the secure random source of the operating system.", "Nothing useful: there is no small state to recover.", "Yes, this is its purpose."),
            ("random", "Simulation and games: the Mersenne Twister, a fast generator with a fixed internal state.", "624 outputs of 32 bits seen in a row reveal that state, so every later number can be predicted.", "Never.")]
    tb = table(s, "random table", X0, 140, (110, 330, 330, 130), rows, 50, size=11.5, hh=28)
    y0 = tb.bottom + 14
    T(s, "code head", X0, y0, 420, 22, [P("How a key is drawn, in two lines", 12, TEAL, True)])
    y = codecard(s, "secrets card", X0, y0 + 26, 470, ["import secrets", "k = secrets.randbelow(K.N - 1) + 1"], size=12)
    say(s, X0, y + 6, 470, "randbelow(m) gives 0 to m - 1, so adding 1 gives 1 to n - 1, the range of a private key.", size=11, color=MUTE, italic=True)
    card(s, "secure randomness card", 550, y0, 400, "Secure randomness", "A private key must come from a cryptographically secure generator: one whose next number cannot be guessed from the earlier ones. Whoever guesses the number owns the coins.", size=11.5, fill=SOFT, minh=126)
    bullets(s, ["Think of real dice against last year's lottery list: it looks random, but anyone who has seen it knows the next entry."], None, size=12)


# ---- FF: finite field -----------------------------------------------------------------------------------------------------------------------------
def FF(s):
    cw = 900 / 17
    for v in range(17):
        hi = v in (3, 13, 7)
        R(s, "field cell", X0 + v * cw, 142, cw - 3, 38, fill=ORANGE if v == 3 else (SOFT if hi else CARD), line=LINE, adj=0.12, paras=[P(str(v), 13, WHITE if v == 3 else INK, True, align="c")], inset=1)
    T(s, "field note", X0, 184, 900, 20, [P("The numbers 0 to 16: after 16 the count starts again at 0, like the hours on a clock face", 11, MUTE, False, True)])
    rows = [("Operation modulo 17", "Meaning", "Result")] + [("13 + 7", "20, then wrap around", str((13 + 7) % 17)), ("3 - 5", "below zero, wrap around", str((3 - 5) % 17)), ("5 x 7", "35, then wrap around", str(5 * 7 % 17)), ("1 / 5", "the number that times 5 gives 1", str(pow(5, -1, 17)))]
    assert (13 + 7) % 17 == 3 and pow(5, -1, 17) == 7
    tb = table(s, "field table", X0, 214, (200, 250, 100), rows, 28, size=11.5, hh=26)
    c1 = card(s, "field card", 640, 214, 310, "Finite field", "A finite field of prime order p is the whole numbers from 0 to p - 1 with addition, subtraction, multiplication and division carried out modulo p.", size=11.5, fill=SOFT, minh=120)
    card(s, "bitcoin field", 640, c1 + 10, 310, "Bitcoin's field", "Its prime p has %d digits: 2 to the 256 minus 2 to the 32 minus 977." % len(str(K.P)), size=11.5, minh=60)
    assert K.P == 2**256 - 2**32 - 977
    bullets(s, ["Why it exists: every curve coordinate must stay inside 256 bits, with exact answers and no rounding. Division by 5 is multiplication by 7, as the table shows.", "Think of a clock face: 13 o'clock is 1 o'clock, and the arithmetic never leaves the dial."], tb.bottom + 12, size=12, w=570)


# ---- SECP: the curve and its standard -------------------------------------------------------------------------------------------------------------
def SECP(s):
    x, y = K.G; assert (y * y - x ** 3 - 7) % K.P == 0
    hdr(s, "curve head", X0, 140, 440, 28, "The secp256k1 curve")
    rows = [("Parameter", "Value"), ("Equation", "y squared = x cubed + 7"), ("Field", "prime p, %d digits" % len(str(K.P))), ("Order n", "about 1.1579 x 10 to the 77"), ("Generator G, x", "%s ... %s" % (hex(x)[2:10].upper(), hex(x)[-8:].upper())), ("Generator G, y", "%s ... %s" % (hex(y)[2:10].upper(), hex(y)[-8:].upper()))]
    tb = table(s, "curve parameters", X0, 172, (150, 290), rows, 28, size=11.5, hh=26)
    say(s, X0, tb.bottom + 8, 440, "Every public key is a multiple of the same generator G on this curve; p is 2 to the 256 minus 2 to the 32 minus 977.", size=11.5)
    hdr(s, "std head", 510, 140, 440, 28, "Curve standard (SEC 2 and NIST)")
    rows2 = [("Curve", "Listed in SEC 2", "On the NIST list"), ("secp256k1", "yes", "no"), ("secp256r1", "yes", "yes (NIST P-256)")]
    t2 = table(s, "standard table", 510, 172, (130, 140, 170), rows2, 32, size=11.5, hh=26)
    card(s, "standard card", 510, t2.bottom + 12, 440, "Why a standard", "SEC 2 lists recommended curve parameters. A standard fixes the numbers, so every program computes on the same curve and gets the same key.", size=11.5, fill=SOFT, minh=110)
    bullets(s, ["Bitcoin chose a curve that is not on the NIST list, with a simple equation and a = 0.", "Think of a standard paper size: because everybody agreed, any printer fits any page."], None, size=12, gap=2)


# ---- PA: point addition and the point at infinity --------------------------------------------------------------------------------------------------
def PA(s):
    p = K.SMALL_P; P0 = K.SMALL_PT
    pts = [(x, y) for x in range(p) for y in range(p) if (y * y - x ** 3 - 7) % p == 0]
    cyc = []; q = None
    while True:
        q = K.small_add(q, P0, p)
        if q is None: break
        cyc.append(q)
    cell = 14.5; gx, gy = X0 + 8, 148
    R(s, "grid back", gx - 6, gy - 6, cell * 17 + 12, cell * 17 + 12, fill=WHITE, line=LINE, adj=0.02)
    for (x, y) in pts:
        inc = (x, y) in cyc
        R(s, "curve point", gx + x * cell, gy + (16 - y) * cell, cell - 2, cell - 2, fill=TEAL if inc else GREY, line=None, adj=0.5)
    T(s, "grid note", X0, gy + 17 * cell + 12, 245, 80, [P("The %d points of y squared = x cubed + 7 over 17 numbers (x across, y up). The %d teal points are the multiples of P = (1, 5)." % (len(pts), len(cyc)), 10.5, MUTE, False, True)])
    P2 = K.small_add(P0, P0, p); P3 = K.small_add(P0, P2, p); P4 = K.small_add(P2, P2, p); negP = (P0[0], (-P0[1]) % p)
    rows = [("Sum", "Result", "Rule used"), ("P + P", str(P2), "tangent, third point, mirror"), ("P + 2P", str(P3), "line through two points, mirror"), ("2P + 2P", str(P4), "tangent again"),
            ("P + (-P): (1, 5) + (1, 12)", "infinity (None)", "vertical line meets nowhere else")]
    assert K.small_add(P0, negP, p) is None
    tb = table(s, "addition table", 310, 148, (210, 130, 300), rows, 28, size=11, hh=26)
    c = card(s, "addition card", 310, tb.bottom + 12, 640, "Point addition and the point at infinity", "A line through two points meets the curve in a third; its mirror image is the sum. Infinity acts as zero.", size=11.5, fill=SOFT, minh=90)
    bullets(s, ["Adding P to itself repeatedly gives every multiple kP, which is how a private key k becomes a public key. Think of hopping round a small ring road: after nine hops you are back at the start."], c + 12, size=12, x=310, w=640)


# ---- DL: discrete logarithm and brute force --------------------------------------------------------------------------------------------------------
def DL(s):
    vals = [(k, pow(2, k, 101)) for k in range(1, 10)]; assert vals[-1] == (9, 7)
    T(s, "chart head", X0, 138, 430, 22, [P("2 to the k = 7 modulo 101: nine tries", 12, TEAL, True)])
    col_chart(s, "toy tries", X0, 162, 430, 168, ["k=%d" % k for k, _ in vals], [v for _, v in vals], size=10, hi=8)
    work = K.N // 2; years = work / 10 ** 12 / (365.25 * 24 * 3600)
    c = card(s, "dl card", 510, 142, 440, "Discrete logarithm and brute-force search", "Finding k from K = kG is the discrete logarithm problem. With no known shortcut, it means trying every k: a brute-force search.", size=11.5, fill=SOFT, minh=110)
    rows = [("Group", "Tries on average", "Time at a trillion tries a second"), ("modulus 101 (toy)", "9", "instant"), ("secp256k1", "%.1e" % work, "%.1e years" % years)]
    t2 = table(s, "dl table", 510, c + 12, (150, 120, 170), rows, 30, size=11.5, hh=30)
    bullets(s, ["The forward direction is quick: doubling and adding needs a few hundred steps. Going back needs half of all keys, about %.1e tries; the universe is about 1.4 x 10 to the 10 years old." % work,
                "Think of mixing paint: stirring two colours together takes a moment, separating them again is hopeless."], 346, size=12, w=430)


# ---- LIB: cryptographic library -------------------------------------------------------------------------------------------------------------------
def LIB(s):
    ones = lambda k: bin(k).count("1") - 1
    keys = [("key 2 to the 252 (one 1-bit)", 2 ** 252), ("the book's key (%d 1-bits)" % bin(K.BOOK_K).count("1"), K.BOOK_K), ("key 2 to the 253 minus 1 (all 1-bits)", 2 ** 253 - 1)]
    T(s, "bars head", X0, 138, 450, 22, [P("Point additions the sketch performs for three keys", 12, TEAL, True)])
    yb = hbar(s, "additions", X0, 166, 470, [(a, ones(k), str(ones(k))) for a, k in keys], labw=290, valw=50, size=11, hi=1)
    assert ones(K.BOOK_K) == 123
    say(s, X0, yb + 2, 470, "Each 1-bit costs one addition, so the running time of the sketch tells an onlooker how many 1-bits the key has. A tested library does the same work in the same time for every key.", size=11.5, color=MUTE, italic=True)
    hdr(s, "lib head", 560, 138, 390, 28, "Cryptographic library (libsecp256k1)")
    rows = [("", "This chapter's sketch", "libsecp256k1"), ("Written to", "be read and taught", "protect real funds"), ("Timing", "depends on the key", "the same for every key"), ("Checked against", "Bitcoin Core 31.1, BIP 350 vectors", "years of public review"), ("Real funds", "never", "yes")]
    tb = table(s, "lib table", 560, 170, (110, 140, 140), rows, 30, size=11, hh=26)
    c = card(s, "lib card", X0, max(tb.bottom, below(s, X0, 470)) + 8, 900, "What a cryptographic library is", "Tested, reusable code for the elliptic curve math. Many Bitcoin implementations use libsecp256k1; do not write your own for real money.", size=11.5, fill=SOFT, minh=40)
    bullets(s, ["Think of a pharmacy: a recipe may be fine for the kitchen table, but medicine comes from a tested, inspected factory."], c + 10, size=12)


# ---- BB: bits, bytes and number bases ---------------------------------------------------------------------------------------------------------------
def BB(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); n = int.from_bytes(c, "big"); import base64
    rows = [("Binary (base 2)", len(c) * 8, "%d characters" % (len(c) * 8)), ("Hexadecimal (base 16)", len(c.hex()), "%d characters" % len(c.hex())), ("Base64", len(base64.b64encode(c)), "%d characters" % len(base64.b64encode(c))), ("Base58", len(b58plain(n)), "%d characters" % len(b58plain(n)))]
    T(s, "bars head", X0, 136, 480, 22, [P("The same 33-byte public key written in four bases", 12, TEAL, True)])
    yb = hbar(s, "bases", X0, 162, 490, rows, labw=170, valw=120, size=11, bh=22, gap=9, hi=3)
    rows2 = [("Number base", "Symbols", "Bits per symbol"), ("2", "0 and 1", "1"), ("16, hexadecimal", "0-9, a-f", "4"), ("64, base64", "A-Z, a-z, 0-9, + /", "6"), ("58, base58", "no 0 O I l", "5.86")]
    tb = table(s, "base table", 560, 138, (150, 150, 90), rows2, 28, size=11, hh=40)
    y0 = max(yb, tb.bottom) + 12
    c1 = card(s, "bits card", X0, y0, 440, "Bits and bytes", "A bit is 0 or 1; a byte is 8 bits. A 65-byte public key has 520 bits; one hexadecimal digit stands for 4 bits.", size=11.5, minh=96)
    c2 = card(s, "base card", 510, y0, 440, "Number base (hexadecimal, base58, base64)", "A number base, or radix, is the count of different symbols used to write numbers. The same number is shorter in a larger base.", size=11.5, fill=SOFT, minh=96)
    bullets(s, ["Think of a distance in centimetres, metres or kilometres: the length is the same, but the bigger the unit the fewer digits you write."], max(c1, c2) + 10, size=12)


# ---- IP: payment to an IP address -----------------------------------------------------------------------------------------------------------------
def IP(s):
    R(s, "payer lane", X0, 140, 250, 34, fill=TEAL, line=None, paras=[P("Payer", 13, WHITE, True, align="c")]); R(s, "receiver lane", 500, 140, 250, 34, fill=TEAL, line=None, paras=[P("Receiver (online, reachable)", 13, WHITE, True, align="c")])
    steps = [("1  Payer types the receiver's IP address", 1), ("2  The payer's node connects to the receiver's node", 1), ("3  The receiver replies with a new public key", -1), ("4  The payer sends coins to that key", 1)]
    for i, (t, d) in enumerate(steps):
        y = 188 + i * 44
        R(s, "ip step", 300, y, 410, 34, fill=CARD, line=LINE, paras=[P(t, 11.5, INK, True, align="c")], inset=4)
        if d == -1: A(s, "ip arrow", 298, y + 17, 262, y + 17, ORANGE, 2.0)
        else: A(s, "ip arrow", 262, y + 17, 298, y + 17, ORANGE, 2.0)
    card(s, "ip card", 740, 188, 210, "Payment to an IP address", "The earliest Bitcoin software let a spender type the receiver's IP address.", size=11, fill=SOFT, minh=150)
    c1 = card(s, "ip why", X0, 374, 440, "Why it faded", "The receiver had to be online and reachable, and nothing proved who answered.", size=11.5, minh=70)
    c2 = card(s, "ip next", 510, 374, 440, "What replaced it", "A short address that anyone can write down and pay at any time, which is where the rest of this part leads.", size=11.5, minh=70)
    bullets(s, ["Think of paying a shop by phoning it and asking it to read out a fresh bank number: it works only if somebody picks up."], max(c1, c2) + 10, size=12)


# ---- STACK: stack, opcodes and script evaluation --------------------------------------------------------------------------------------------------
def STACK(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); h = K.hash160(c); sig = b"sig"
    assert K.run_p2pkh(sig, c, h) == [sig, c]
    H = h.hex()[:8]
    steps = [("start: the unlocking data", [("signature", "data"), ("public key", "data")]),
             ("OP_DUP copies the top item", [("signature", "data"), ("public key", "data"), ("public key", "data")]),
             ("OP_HASH160 hashes the top item", [("signature", "data"), ("public key", "data"), ("hash " + H, "hash")]),
             ("push the hash from the locking script", [("signature", "data"), ("public key", "data"), ("hash " + H, "hash"), ("hash " + H, "hash")]),
             ("OP_EQUALVERIFY: equal, both removed", [("signature", "data"), ("public key", "data")]),
             ("OP_CHECKSIG checks the signature", [("true", "ok")])]
    T(s, "stack head", X0, 134, 900, 20, [P("A P2PKH script on a stack, step by step (the top of the stack is the right-hand chip, outlined)", 12, TEAL, True)])
    for i, (lab, st) in enumerate(steps):
        y = 160 + i * 40
        R(s, "opcode", X0, y, 280, 33, fill=CARD, line=LINE, paras=[P(lab, 11, INK, True)], inset=6)
        chips(s, "stack %d" % i, 338, y + 2, st, h=28, w=96, gap=4, size=10)
    card(s, "stack card", 750, 160, 200, "Stack, opcodes and script evaluation", "Data is pushed on top of a list; each opcode takes the top items and pushes its result.", size=11, fill=SOFT, minh=150)
    bullets(s, ["The script passes when a nonzero item is on top at the end. Think of a stack of plates: you can only touch the top one, and each opcode is a small chore done on it."], None, size=12)


# ---- COMMIT: hash commitment ----------------------------------------------------------------------------------------------------------------------
def COMMIT(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); h = K.hash160(c); flipped = bytes([c[0]]) + bytes([c[1] ^ 1]) + c[2:]
    diff = sum(bin(a ^ b).count("1") for a, b in zip(h, K.hash160(flipped)))
    flow(s, 140, [("1  Commit", "The address holds only the 20-byte hash of the public key (%s...)." % h.hex()[:8]),
                  ("2  Reveal", "To spend, the owner shows the public key itself, %d bytes, with a signature." % len(c)),
                  ("3  Check", "Anyone hashes the shown key and compares it with the hash in the address.")], h=98, gap=18, size=11.5, head=12.5)
    rows = [("Key shown at spending", "HASH160 equals the address hash?"), ("the real public key", str(K.hash160(c) == h)), ("the same key with one bit flipped", str(K.hash160(flipped) == h) + " (%d of 160 hash bits changed)" % diff)]
    tb = table(s, "commit table", X0, 250, (320, 400), rows, 28, size=11.5, hh=26)
    c1 = card(s, "commit card", X0, tb.bottom + 14, 440, "Hash commitment (HASH160)", "A hash output commits to its input. Bitcoin commits to a public key with HASH160, SHA-256 then RIPEMD-160: 20 bytes instead of 65.", size=11.5, fill=SOFT, minh=90)
    c2 = card(s, "commit why", 510, tb.bottom + 14, 440, "Why commit first", "A short hash is easy to print and hides the key until the moment of spending.", size=11.5, minh=90)
    bullets(s, ["Think of a sealed envelope holding your prediction: opening it later proves you did not change your mind."], max(c1, c2) + 8, size=12)


# ---- P2PKH: the address and its script ---------------------------------------------------------------------------------------------------------------
def P2PKH(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); cu = K.pub_bytes(K.ec_mul(K.BOOK_K), False)
    script = K.p2pkh_script(c); assert len(script) == 25 and script[:3] == b"\x76\xa9\x14"
    a1, a2 = K.p2pkh(c), K.p2pkh(cu)
    T(s, "script head", X0, 136, 900, 20, [P("The locking script of a P2PKH output, 25 bytes", 12, TEAL, True)])
    strip(s, "script", X0, 160, 900, [("76 OP_DUP", 1, ORANGE, WHITE, "76"), ("a9 OP_HASH160", 1, TEAL, WHITE, "a9"), ("14", 1, CARD, INK, "14"), ("the 20-byte key hash", 20, SOFT, INK), ("88 OP_EQUALVERIFY", 1, TEAL, WHITE, "88"), ("ac OP_CHECKSIG", 1, ORANGE, WHITE, "ac")], h=34, size=10.5)
    T(s, "script legend", X0, 198, 900, 18, [P("76 = OP_DUP   a9 = OP_HASH160   14 = push the next 20 bytes   88 = OP_EQUALVERIFY   ac = OP_CHECKSIG", 10.5, MUTE, False, True)])
    T(s, "addr head", X0, 228, 900, 20, [P("The address of the same output, 25 bytes written as %d characters" % len(a1), 12, TEAL, True)])
    strip(s, "address", X0, 252, 900, [("version 00", 1, ORANGE, WHITE, "00"), ("the same 20-byte key hash", 20, SOFT, INK), ("checksum, 4 bytes", 4, TEAL, WHITE)], h=34, size=10.5)
    rows = [("Public key", "Bytes", "Address"), ("compressed", str(len(c)), a1), ("uncompressed", str(len(cu)), a2)]
    tb = table(s, "p2pkh table", X0, 306, (170, 70, 350), rows, 30, size=11.5, hh=26)
    c1 = card(s, "p2pkh card", 700, 306, 250, "P2PKH address", "Base58check of version 00 and the HASH160 of the public key: two key forms, two addresses.", size=11, fill=SOFT, minh=90)
    bullets(s, ["The script is the lock and the address is its label. Think of a locker that shows only its number: the number is printed everywhere, the key stays with you."], max(tb.bottom, c1) + 12, size=12)


# ---- NET: mainnet and testnet ------------------------------------------------------------------------------------------------------------------------
def NET(s):
    c = K.pub_bytes(K.ec_mul(K.BOOK_K)); h = K.hash160(c)
    m, t = K.b58check(b"\x00" + h), K.b58check(b"\x6f" + h); bm, bt = K.segwit_address("bc", 0, K.PROG_WPKH), K.segwit_address("tb", 0, K.PROG_WPKH)
    assert K.segwit_decode("bc", bt) is None
    R(s, "main lane", X0, 140, 440, 36, fill=TEAL, line=None, paras=[P("Main network: coins with real value", 12.5, WHITE, True, align="c")])
    R(s, "test lane", 510, 140, 440, 36, fill=ORANGE, line=None, paras=[P("Test network: coins with no value, for trying things", 12.5, WHITE, True, align="c")])
    rows = [("What shows the network", "Main", "Test"), ("P2PKH version byte", "00 (starts with %s)" % m[0], "6F (starts with %s)" % t[0]), ("P2SH version byte", "05 (starts with 3)", "C4 (starts with 2)"), ("Bech32 human-readable part", "bc", "tb"),
            ("The same key hash as P2PKH", m, t), ("The same program as bech32", bm, bt)]
    tb = table(s, "network table", X0, 186, (230, 340, 330), rows, 26, size=10.5, hh=26)
    c1 = card(s, "network card", X0, tb.bottom + 14, 560, "Mainnet and testnet", "Two separate chains. The version byte (base58check) or human-readable part (bech32) names the chain, so a test payment cannot reach the main chain.", size=11.5, fill=SOFT, minh=76)
    c2 = card(s, "network check", 630, tb.bottom + 14, 320, "A wallet checks", "Reading the test address tb1q... as a main address returns nothing: refused.", size=11.5, minh=76)
    bullets(s, ["Think of play money in a board game: it looks like the real thing, so the box is marked, and the shop will not take it."], max(c1, c2) + 8, size=12)


# ---- MSIG: multisignature script -----------------------------------------------------------------------------------------------------------------------
def MSIG(s):
    keys = [K.pub_bytes(K.ec_mul(n)) for n in (1, 2, 3)]; script = K.multisig_script(2, keys); assert len(script) == 105
    T(s, "script head", X0, 136, 900, 20, [P("The 2-of-3 script, 105 bytes", 12, TEAL, True)])
    strip(s, "msig", X0, 160, 900, [("OP_2", 1, ORANGE, WHITE, "2"), ("key A  34 bytes", 34, SOFT, INK), ("key B  34 bytes", 34, SOFT, INK), ("key C  34 bytes", 34, SOFT, INK), ("OP_3", 1, ORANGE, WHITE, "3"), ("CHECK", 1, TEAL, WHITE, "ae")], h=34, size=10.5, minw=26)
    T(s, "msig legend", X0, 198, 900, 32, [P("2 = OP_2, signatures needed   each key = a 1-byte push and 33 bytes   3 = OP_3, keys listed   ae = OP_CHECKMULTISIG", 10.5, MUTE, False, True), P("The 1-byte parts are drawn wider than to scale.", 10.5, MUTE, False, True)])
    subsets = [(), ("A",), ("B",), ("C",), ("A", "B"), ("A", "C"), ("B", "C"), ("A", "B", "C")]
    T(s, "grid head", X0, 240, 600, 20, [P("Every set of signers, and whether the script passes (needs at least 2)", 12, TEAL, True)])
    for i, sg in enumerate(subsets):
        x = X0 + (i % 4) * 150; y = 266 + (i // 4) * 66; ok = len(sg) >= 2
        R(s, "signers", x, y, 140, 56, fill=SOFT if ok else CARD, line=TEAL if ok else LINE, paras=[P(" + ".join(sg) if sg else "nobody", 12.5, INK, True, align="c"), P("passes" if ok else "fails", 11.5, TEAL if ok else MUTE, True, align="c")], inset=3)
    c = card(s, "msig card", 670, 240, 280, "Multisignature script", "A script that requires signatures from several keys: OP_CHECKMULTISIG checks m signatures against n public keys, as in BIP16's example of 2 of 3.", size=11, fill=SOFT, minh=124)
    bullets(s, ["Why: no single stolen or lost key can spend, or block, the coins. Three of the eight combinations above pass. Think of a safe-deposit box where any two of three keyholders must be present."], 404, size=12, w=900)


# ---- SECOND: second preimage attack --------------------------------------------------------------------------------------------------------------
def SECOND(s):
    rows = [("Attack", "The attacker has", "The goal", "Tries for a 160-bit hash"), ("Preimage", "only the hash", "any input with that hash", "2 to the 160 = %.2e" % 2.0 ** 160),
            ("Second preimage attack", "the hash and one input", "a different input with the same hash", "2 to the 160 = %.2e" % 2.0 ** 160), ("Collision", "nothing", "any two inputs with one hash", "2 to the 80 = %.2e" % 2.0 ** 80)]
    tb = table(s, "attack table", X0, 140, (190, 200, 270, 240), rows, 30, size=11, hh=26)
    y0 = tb.bottom + 14
    T(s, "bars head", X0, y0, 560, 20, [P("Work as a power of two (the longer the bar, the harder)", 12, TEAL, True)])
    yb = hbar(s, "work", X0, y0 + 26, 580, [("collision", 80, "2 to the 80"), ("preimage", 160, "2 to the 160"), ("second preimage", 160, "2 to the 160")], labw=130, valw=110, size=11, hi=2)
    c = card(s, "second card", 650, y0, 300, "Second preimage attack", "Finding a different input with the same hash as a given one. For an address one party made alone: about 1 in 2 to the 160.", size=11, fill=SOFT, minh=110)
    bullets(s, ["So nobody can substitute another key for the one behind your address. Think of a fingerprint taken from a particular person: matching it is far harder than finding any two people who share one."], max(yb, c) + 8, size=12)
