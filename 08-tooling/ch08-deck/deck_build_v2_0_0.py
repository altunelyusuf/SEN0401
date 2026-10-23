#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 8, Digital Signatures) - the generator of the chapter 8 deck 2.0.0 (task TK_Ch08_Deck_Build, 2026-10-23), a NEW file, built to the pattern of ch06-deck/deck_build_v2_1_0.py. It writes,
from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch08/page/chapter_code_ch08_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the chapter corpus (sen0401_ch08_corpus_v1_2_0.py: branches and groups), the story module v1_2_0 (three stories with pictures), the recorded executions examples_out_v2_0_0.json (made by
examples_run_v2_0_0.py under Python 3.14), deck_concepts_v2_0_0.py (the 45 key concepts of the research, each with a meaning and one everyday analogy) and the resources slide of the previous plan. Every
number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the file is drawn: no text box over 30 words, notes of at most 60 words,
no code line over 60 characters with its prompt (a listing never wraps), every key concept of the research on a slide with its analogy.
Usage: python3.14 deck_build_v2_0_0.py [--render]"""
__version__ = "2.0.0"
import ast, glob, hashlib, importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_0_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.0.0", "2_0_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


C = load(os.path.join(TOOL, "sen0401_ch08_corpus_v1_2_0.py"), "corpus08")
ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch08_stories_v*.py")), key=vk)[-1], "stories08")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
LAB = {n[0]: (n[1] or n[0]) for n in C.NODES}
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch08/assets/"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v1_1_0.json")))

BRANCHES = [n[0] for n in C.NODES if n[2] == 1]
def kids(name): return [n[0] for n in C.NODES if n[3] == name]

S, ANALOGIES, FIRST_CODE = [], [], []
EST = lambda text, fs, width, k=0.0078: max(1, -(-int(len(text) * fs * k * 100) // int(width * 100)))   # lines a text needs: characters x font size x 0.0078 in, over the width
W = lambda t: len(re.findall(r"\S+", t))
BR_SHORT = {"SignatureFoundations": "Basics", "SighashFlags": "SIGHASH", "SchnorrSignatures": "Schnorr", "EcdsaSignatures": "ECDSA", "Randomness": "Nonces", "SegwitSigning": "Segwit", "SinceTheBook": "Since print"}


def val(ex, expr):
    for e, o in OUT[ex]:
        if e == expr: return ast.literal_eval(o)
    raise KeyError((ex, expr))


def add(kind, title, sub, items, notes, take=None, bg="light"):
    sl = {"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg}
    if take: sl["take"] = take
    S.append(sl)
    return len(S)


def sentences(t):
    t = re.sub(r"\b(Mt|Dr|St|Mr|Mrs|vs|No)\.\s", lambda m: m.group(1) + ".\x00", t.strip())
    return [s.replace("\x00", " ") for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9'\"(])", t) if s]


# ------------------------------------------------------------------------------------------------------------------------------------------------
# dividers
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEGS = [(BR_SHORT[b], 1.0) for b in ("SignatureFoundations", "SighashFlags", "SchnorrSignatures", "EcdsaSignatures", "Randomness", "SegwitSigning", "SinceTheBook")]


def strip(branch, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = SEGS.index((BR_SHORT[branch], 1.0))
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": i == hot} for i, (lab, f) in enumerate(SEGS)]}


DIV_NOTES = {
    "SignatureFoundations": "A digital signature is a proof that the holder of a private key approved a message. This part shows what verification needs, why two moduli appear, and what is really signed.",
    "SighashFlags": "A signature need not cover the whole transaction. One byte, the SIGHASH flag, chooses what it covers. We measure what each flag commits to and meet the bug of SINGLE.",
    "SchnorrSignatures": "Schnorr signatures began as a proof of identity. We turn the proof into a signature, meet the BIP340 format, and see why keys that add up bring both multisignatures and a trap.",
    "EcdsaSignatures": "ECDSA signed every Bitcoin payment from 2009 and still signs most. We run its formulas, take apart its byte layout and separate what miners enforce from what nodes prefer.",
    "Randomness": "A signature needs a number used once. If it repeats, the key leaks; if it is derived from key and message, it never repeats. The part ends with how it changes the signature size.",
    "SegwitSigning": "Segregated witness changed what is hashed when a transaction is signed. We count the bytes of the old and the new method and see why the amount is now part of the signature.",
    "SinceTheBook": "The book went to print in 2023 and the standards have moved. This part collects the dates, the status of the proposals and the evidence trail behind every number in the deck.",
}


def divider(branch):
    groups = kids(branch); n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 3 else 11
    its = []
    for g in groups:
        pill, mean, ana = K.L2[g]
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12 if n <= 3 else 11, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
        ANALOGIES.append({"concept": LAB[g], "analogy": an, "slide": len(S) + 1})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (branch, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12 if n <= 3 else 11, "items": its}, strip(branch)]
    ANALOGIES.append({"concept": LAB[branch], "analogy": K.L1[branch], "slide": len(S) + 1})
    return add("section", LAB[branch], K.L1[branch], items, DIV_NOTES[branch])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards: the key concepts of the research
# ------------------------------------------------------------------------------------------------------------------------------------------------
def chunks(lst):
    n = len(lst)
    if n == 0: return []
    k = -(-n // 4); size = -(-n // k); return [lst[i:i + size] for i in range(0, n, size)]


def cards(branch, names, part, parts):
    n = len(names); cols = 2 if n == 4 else min(3, n); rows = -(-n // cols); bw = (9.0 - (cols - 1) * 0.16) / cols; fw = bw - 0.3
    avail = (3.5 - (rows - 1) * 0.14) / rows
    for fs in (11.5, 11, 10.5, 10):
        items, need = [], 0
        for nm in names:
            _, mean, ana0 = K.K3[nm]; mean = mean[0].upper() + mean[1:]; ana = "Think of " + ana0 + "."
            hA = (EST(nm, fs + 1.5, fw, 0.0088) * (fs + 1.5) + EST(mean, fs, fw) * fs) * 1.22 / 72 + 0.06
            hB = EST(ana, fs, fw) * fs * 1.22 / 72 + 0.04
            it = {"label": nm, "meaning": mean, "analogy": ana, "hA": round(hA, 3), "hB": round(hB, 3), "hC": 0}
            items.append(it); need = max(need, 0.07 + hA + hB + 0.1)
        if need <= avail: break
    else:
        raise SystemExit("REFUSED: cards %s need %.2f in, %.2f available" % (names, need, avail))
    for nm, it in zip(names, items):
        for k in ("meaning", "analogy"):
            if W(it[k]) > 30: raise SystemExit("REFUSED: card %s has a frame of over 30 words" % nm)
        if W(it["label"] + " " + it["meaning"]) > 30: raise SystemExit("REFUSED: card %s head frame over 30 words" % nm)
        ANALOGIES.append({"concept": nm, "analogy": K.K3[nm][2] + ".", "slide": len(S) + 1})
    suffix = " (%d of %d)" % (part, parts) if parts > 1 else ""
    title = "%s: key concepts%s" % (LAB[branch], suffix)
    if len(title) > 44: title = "%s: concepts%s" % (LAB[branch], suffix)
    if len(title) > 44: title = "%s%s" % (LAB[branch], suffix)
    names_t = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 8." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 8." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
LH = 10 * 1.3 / 72
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("Three inputs, one answer", "Verifying an ECDSA signature with the chapter's library", "Change the message, the key or the signature and the answer turns to False",
             "Verification takes a message, a public key and a signature, and answers yes or no. We flip one bit of the message, then swap the key, and both attempts fail. Only the true triple passes."),
    "ex02": ("Scalars wrap at n, coordinates at p", "Two moduli, two clocks of different sizes", "The book says everything is modulo p; the response is reduced modulo n",
             "The signature equation lives in the group of curve points, whose order is n. Reducing the response modulo n makes the equation hold, reducing it modulo p does not. The two numbers differ by 129 bits."),
    "ex03": ("What is signed is a digest", "A single satoshi changes the whole digest", "The signature covers a hash of the transaction, not the bytes themselves",
             "A signature is made over a hash of selected transaction fields. The same transaction gives the same digest, and raising one output by a satoshi gives a completely different one, so the signature no longer fits."),
    "ex04": ("A flag is one byte", "Three base values and one modifier bit", "ANYONECANPAY is the top bit, so it combines with every base flag",
             "The flag appended to a signature is a single byte. The three base flags are 1, 2 and 3. The modifier ANYONECANPAY is 128, the top bit, which is why it can be added to any base flag."),
    "ex05": ("What each flag commits to", "Change one field and see whether the hash moves", "Only plain ALL covers every probed field, other inputs' sequences included",
             "We change one field of the transaction at a time and ask if the digest moves. ALL covers all five probed fields. The other flags leave some open, which is what lets others complete a transaction."),
    "ex06": ("SINGLE with no matching output", "The bug the book does not mention", "A digest equal to the number one can be reused on any transaction",
             "SIGHASH_SINGLE signs the output with the same number as the input. For inputs one and two there is none, so the legacy algorithm signs the constant one, which holds for any transaction."),
    "ex07": ("The protocol with whole numbers", "Why the book first explains Schnorr with integers", "With plain integers anyone divides and reads the secret; points forbid that",
             "The book teaches the protocol with whole numbers first. The proof works: s times G equals the commitment plus the challenge times the public key. But dividing the public key by G reveals the secret."),
    "ex08": ("From identity proof to signature", "Replace the verifier's challenge by a hash", "The hash of the message plays the examiner, so no examiner has to be online",
             "An honest prover's response passes and a wrong one fails. Letting a hash of the message choose the challenge turns the proof into a signature, and the signature fits only that message."),
    "ex09": ("A fixed size: 64 bytes", "BIP340 keys are 32 bytes and signatures 64", "Schnorr is smaller and of fixed size; DER signatures vary",
             "A BIP340 public key is the x coordinate only, 32 bytes. The signature is 64 bytes, always. The ECDSA signature of the same key is written in DER, whose length varies by a byte or two."),
    "ex10": ("A key that cancels another key", "Why adding public keys is not enough", "MuSig2 weights each key by a hash of all keys, which stops the trick",
             "If keys are simply added, Bob can wait for Alice's key and publish a key that cancels it. Then Bob alone signs for both. With MuSig2's hashed weights the same attack no longer gives Bob's key."),
    "ex11": ("Any two of three shares", "Shamir's line through points", "Fewer than the threshold reveal nothing; the threshold reveals everything",
             "A secret is the height of a line at zero. Each of three shares is a point on that line. Any two points rebuild the line and give the secret, while one share alone fits every possible secret."),
    "ex12": ("ECDSA with the book's formulas", "Sign with a chosen nonce, verify by rebuilding a point", "If s verifies, so does n minus s: the signature has two forms",
             "We sign with an explicit nonce and verify by rebuilding the point K. The second valid value of s is n minus s. Nodes relay only the smaller one, the low form."),
    "ex13": ("Nine elements in 71 bytes", "A DER signature taken apart", "Seven of the nine elements are one byte; R and s take 32 each",
             "DER writes the signature as nested fields: a type, a length, then R and s, each with its own tag and length, and a final hash-type byte. The byte counts add up to the signature."),
    "ex14": ("Valid for miners, refused by nodes", "Consensus accepts the high-S twin, policy does not", "Policy is a stricter house rule; consensus is the law",
             "Both forms of the signature verify, so a block that contains the high-S twin is valid. A node, however, relays only the low form. Policy is stricter than consensus, and can be changed without a fork."),
    "ex15": ("One nonce, two signatures, no secret", "How a reused nonce leaks the key", "Android's weak generator made this attack possible in 2013",
             "Two signatures with the same nonce give two equations in two unknowns. Subtracting them reveals the nonce and then the private key. A different nonce for the second message leaves nothing to solve."),
    "ex16": ("The nonce derived from the key", "RFC 6979 removes the random number", "Same key and message always give the same nonce, and so the same signature",
             "RFC 6979 derives the nonce by keyed hashing of the secret key and the message. It never repeats for different messages, and a signature can be repeated and compared exactly in a test."),
    "ex17": ("About half are one byte longer", "Signature length and the high R", "Bitcoin Core signs again until R is small, to save a byte",
             "When the top bit of R is set, DER adds a zero byte, so the signature has 71 bytes instead of 70. Over 200 signatures about half are longer. Core grinds the nonce to avoid the extra byte."),
    "ex18": ("Quadratic hashing", "Old signing against BIP143", "Doubling the inputs roughly quadruples the bytes the old method hashes",
             "The old algorithm hashes almost the whole transaction again for every input. BIP143 hashes the shared parts once. The ratio of the two grows with the number of inputs."),
    "ex19": ("BIP143 signs the amount", "A wallet can no longer be lied to about the value", "The new digest changes with the amount; the old one cannot",
             "In the old algorithm the signer never saw the value of the coin it spent. In BIP143 the amount is part of the digest, so a wrong amount gives a different digest and an invalid signature."),
    "ex20": ("Dates behind the patent and taproot", "The term of the Schnorr patent, and 4,698 days", "The patent ended in 2010; taproot came eleven years later",
             "United States law gave the longer of 17 years from grant or 20 years from filing. For Schnorr's patent that ends on 23 February 2010. Taproot activated 4,698 days after the genesis block."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    acc = lambda b: "accepted" if b else "rejected"
    if ex == "ex01":
        c, n = val(ex, "checks"), val(ex, "len(sig)")
        return ([tb([["Check", "Verdict"], ["True message, true key", acc(c[0])], ["One bit of message flipped", acc(c[1])], ["Another public key", acc(c[2])]], [2.0, 1.25])],
                "four inputs, one verdict each", "The signature is %d bytes long. Only the unchanged triple of message, key and signature is accepted." % n)
    if ex == "ex02":
        r, (bn, bp, df), gap = val(ex, "r"), val(ex, "(by_n, by_p, differ)"), val(ex, "gap")
        return ([tb([["Reduce s modulo", "Equation holds"], ["n, the group order", yn(bn)], ["p, the field prime", yn(bp)], ["Remainder of 5 by 3", str(r)]], [1.85, 1.4])],
                "does sG = kG + eX hold?", "The two primes differ by a number of %d bits, so n and p are different clocks%s." % (gap, "" if df else " (they are not)"))
    if ex == "ex03":
        d = val(ex, "digests")
        return ([tb([["Transaction", "Digest (12 hex digits)"], ["Original", d[0]], ["Original again", d[1]], ["One output +1 satoshi", d[2]]], [1.55, 1.7])],
                "the digest that is signed", "The same bytes give the same digest. One satoshi more gives a different one, and the old signature no longer fits.")
    if ex == "ex04":
        v, cb = val(ex, "base + [acp]"), val(ex, "combos")
        return ([ch(["ALL", "NONE", "SINGLE", "ACP", "ALL+ACP", "NONE+ACP", "SINGLE+ACP"], v + cb, "value")], "flag values (ACP = ANYONECANPAY)",
                "ANYONECANPAY is %d, the top bit, so adding it to a base flag gives %s." % (v[3], ", ".join(str(c) for c in cb)))
    if ex == "ex05":
        c = val(ex, "count"); pat = val(ex, "[''.join('Y' if x else '.' for x in cm[f].values()) for f in flags]")
        ks = list(c)
        return ([ch(["ALL", "NONE", "SINGLE", "ALL+ACP", "NONE+ACP", "SINGLE+ACP"], [c[k] for k in ks], "fields")], "fields covered, of the 5 probed",
                "ALL covers %d of 5 fields, NONE with ANYONECANPAY only %d: the field pattern is %s." % (c[ks[0]], c[ks[4]], pat[4]))
    if ex == "ex06":
        d, b = val(ex, "digests"), val(ex, "buggy")
        return ([tb([["Input", "Digest starts", "Equals one?"]] + [[str(i), d[i], yn(b[i])] for i in range(3)], [0.6, 1.4, 1.25])],
                "signature hash of each input", "Inputs 1 and 2 have no output of their own, so the legacy algorithm signs the constant one.")
    if ex == "ex07":
        t = val(ex, "t"); lk = val(ex, "leak")
        return ([tb([["Step", "Value"], ["Public key xG", str(t["xG"])], ["Commitment kG", str(t["kG"])], ["Response s = k + e x", str(t["s"])],
                     ["sG = kG + e xG", "%d = %d + %d" % (t["sG"], t["kG"], t["exG"])], ["Divide xG by G", str(lk)]], [1.75, 1.5])],
                "one round with whole numbers", "The proof holds, but dividing xG by G returns the secret %d: with points that division is impossible." % lk)
    if ex == "ex08":
        p, s_ = val(ex, "proof"), val(ex, "sigs")
        return ([tb([["Test", "Result"], ["Honest response s", acc(p[0])], ["Response s + 1", acc(p[1])], ["Signature on message 'A'", acc(s_[0])], ["Same signature on 'B'", acc(s_[1])]], [2.1, 1.15])],
                "proof and signature checks", "A signature fits only the message whose hash chose the challenge.")
    if ex == "ex09":
        z, ok = val(ex, "sizes"), val(ex, "ok")
        return ([ch(["Full key", "X-only key", "ECDSA sig", "Schnorr sig"], z, "bytes")], "bytes per object",
                "The Schnorr signature verifies (%s) and always takes %d bytes; the x-only key saves one byte over the compressed key." % (yn(ok), z[3]))
    if ex == "ex10":
        nv, mu = val(ex, "naive"), val(ex, "musig")
        return ([tb([["Key aggregation", "Bob signs alone"], ["Plain sum of keys", "yes, valid" if nv[1] else "no"], ["MuSig2 weighted keys", "yes" if mu else "no"]], [1.8, 1.45])],
                "the key cancellation attack", "After Alice's key is public, Bob picks a key that hides it. Only the weighted aggregate resists.")
    if ex == "ex11":
        b, al = val(ex, "back"), val(ex, "alone")
        return ([tb([["Shares used", "Recovered"], ["1 and 2", str(b[0])], ["1 and 3", str(b[1])], ["2 and 3", str(b[2])], ["Share 1 alone", str(al)]], [1.75, 1.5])],
                "the secret from the shares", "Any two shares give %d. A single share gives %d, which is not the secret." % (b[0], al))
    if ex == "ex12":
        bo, lf, a, b = val(ex, "both"), val(ex, "lowform"), val(ex, "hex(s)[:14]"), val(ex, "hex(L.N - s)[:14]")
        return ([tb([["Form", "Starts with", "Verifies"], ["s", a, yn(bo[0])], ["n - s", b, yn(bo[1])]], [0.8, 1.5, 0.95])],
                "the two values of s", "Both verify. The smaller one is the low-S form: here it is %s." % ("s" if lf else "n - s"))
    if ex == "ex13":
        ln, tot, st = val(ex, "[b for n, b in rows]"), val(ex, "total"), val(ex, "C.der_strict_ok(sig)")
        return ([ch(["type", "length", "tag", "R len", "R", "tag", "S len", "S", "hash type"], ln, "bytes")], "bytes per element (all %d)" % tot,
                "R and s take %d bytes each and the other seven elements one byte each. Strict DER accepts it: %s." % (ln[4], yn(st)))
    if ex == "ex14":
        v = val(ex, "verdict")
        return ([tb([["Signature", "Valid", "Relayed"], ["Low-S form", yn(v[0][0]), yn(v[0][1])], ["High-S twin", yn(v[1][0]), yn(v[1][1])]], [1.25, 0.95, 1.05])],
                "consensus against policy", "Miners accept both forms. Nodes relay only the low-S form.")
    if ex == "ex15":
        a, g, k2, f = val(ex, "r == r2"), val(ex, "got == x"), val(ex, "k2 == k"), val(ex, "fresh")
        return ([tb([["Observation", "Result"], ["Same R in both signatures", yn(a)], ["Private key recovered", yn(g)], ["Nonce recovered", yn(k2)], ["Fresh nonce: R differs", yn(f)]], [2.3, 0.95])],
                "what two signatures reveal", "A single reused nonce hands over the private key; a fresh nonce for the second message does not.")
    if ex == "ex16":
        ag, df, sm, a, b = val(ex, "again"), val(ex, "k1 != k2"), val(ex, "same"), val(ex, "hex(k1)[:14]"), val(ex, "hex(k2)[:14]")
        return ([tb([["Observation", "Result"], ["Same message, same nonce", yn(ag)], ["Other message, other nonce", yn(df)], ["Same signature twice", yn(sm)], ["Nonce 1 starts", a], ["Nonce 2 starts", b]], [1.95, 1.3])],
                "the derived nonce", "Nothing random is drawn, so there is nothing to repeat by accident.")
    if ex == "ex17":
        c = val(ex, "cnt"); ks = sorted(c)
        return ([ch(["%d bytes" % k for k in ks], [c[k] for k in ks], "signatures")], "signatures of each length, of %d" % sum(c.values()),
                "Signatures with a 33-byte R are one byte longer. Bitcoin Core signs again until R is small.")
    if ex == "ex18":
        ns, ol, nw, ra = val(ex, "ns"), val(ex, "old"), val(ex, "new"), val(ex, "ratio")
        return ([ch([str(n) for n in ns], ra, "times")], "old bytes hashed divided by BIP143 bytes, by inputs",
                "At %s inputs the old method hashes %s bytes and BIP143 %s: %s times more." % (fmt(ns[-1]), fmt(ol[-1]), fmt(nw[-1]), ra[-1]))
    if ex == "ex19":
        d, lg = val(ex, "ds"), val(ex, "legacy")
        return ([tb([["Case", "Digest (12 hex digits)"], ["BIP143, amount 5000", d[0]], ["BIP143, amount 5000 again", d[1]], ["BIP143, amount 5001", d[2]], ["Legacy, no amount", lg]], [1.75, 1.5])],
                "the signed digest", "The BIP143 digest moves with the amount. The legacy digest has no amount that could move.")
    if ex == "ex20":
        a, b, c, dd = val(ex, "str(t17)"), val(ex, "str(t20)"), val(ex, "str(term_end)"), val(ex, "days")
        return ([tb([["Date or span", "Value"], ["17 years from grant", a], ["20 years from filing", b], ["Patent term ended", c], ["Genesis to taproot, days", fmt(dd)]], [1.9, 1.35])],
                "dates computed from the filing and grant", "The later date ends the term. Taproot activated %s days after the genesis block." % fmt(dd))
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex04", "ex05", "ex09", "ex13", "ex17", "ex18") else "table"


def code_slide(e):
    ex = e["id"]; fs = 10; lh = fs * 1.3 / 72
    title, sub_, take, notes = CODE_TEXT[ex]
    fin = e["final"]; groups = [list(g["lines"]) for g in e["groups"]]
    if groups[-1][-1] != fin:
        if not groups[-1]: groups[-1] = [fin]
        else: groups[-1].append(fin)
    out = dict(OUT[ex])[fin]
    X_, W_ = 0.5, 5.55
    gl, y = [], 1.45
    for k, (g, lines) in enumerate(zip(e["groups"], groups)):
        last = k == len(groups) - 1
        rows = [[ln, ""] for ln in lines]
        if last: rows[-1][1] = out
        words = sum(W(r[0]) + 1 + W(r[1]) for r in rows)
        if words > 30: raise SystemExit("REFUSED: code frame %d of %s has %d words" % (k + 1, ex, words))
        for r in rows:
            if len(">>> " + r[0]) > 60: raise SystemExit("REFUSED: %s has a code line of %d characters (a listing must not wrap): %s" % (ex, len(">>> " + r[0]), r[0]))
            if len(r[1]) > 58: raise SystemExit("REFUSED: %s output line of %d characters" % (ex, len(r[1])))
        if W(g["note"]) < 8 or W(g["note"]) > 20: raise SystemExit("REFUSED: note %d of %s has %d words (8 to 20 wanted)" % (k + 1, ex, W(g["note"])))
        nrows = len(rows) + sum(1 for r in rows if r[1] != "")
        h = round(nrows * lh + 0.16, 3); nh = round(EST(g["note"], 10.5, W_ - 0.3, 0.0072) * 0.18 + 0.05, 3)
        gl.append({"rows": rows, "note": g["note"], "y": round(y, 3), "h": h, "ny": round(y + h + 0.03, 3), "nh": nh}); y += h + 0.03 + nh + 0.09
    capy = round(y - 0.04, 3)
    if capy + 0.2 > 5.0: raise SystemExit("REFUSED: %s needs the left column to end at %.2f in" % (ex, capy + 0.2))
    RX, RW = 6.25, 3.25
    items0, cap_res, reading = visual(ex, RX, RW, 2.0, 2.0)
    if W(reading) > 30: raise SystemExit("REFUSED: reading of %s has %d words" % (ex, W(reading)))
    lab = "Result: " + cap_res; lab_h = round(EST(lab, 11, RW, 0.0085) * 0.2 + 0.04, 3)
    rh = round(EST(reading, 11.5, RW, 0.0082) * 0.2 + 0.06, 3); ry = round(4.97 - rh, 3)
    vy = round(1.45 + lab_h + 0.05, 3); vh = round(ry - 0.1 - vy, 3)
    items, _, _ = visual(ex, RX, RW, vy, vh)
    cap = "run under Python %s - L, C and K are the chapter library of the page" % PY
    blocks = {"t": "codeblocks", "x": X_, "w": W_, "fs": fs, "nfs": 10.5, "groups": gl, "cap": cap, "capy": capy}
    res_label = {"t": "text", "x": RX, "y": 1.45, "w": RW, "h": lab_h, "body": lab, "fs": 11, "font": "B", "bold": True, "color": "mute"}
    if items[0]["t"] == "table": ry = round(min(ry, vy + len(items[0]["rows"]) * items[0]["rowH"] + 0.3), 3)       # under the table, not at the foot of the slide
    read = {"t": "text", "x": RX, "y": ry, "w": RW, "h": rh, "body": reading, "fs": 11.5, "font": "B", "italic": True, "color": "ink"}
    if W(notes) > 60: raise SystemExit("REFUSED: notes of %s have %d words" % (ex, W(notes)))
    tail = " It is example %d in the chapter code tab of the course page." % int(ex[2:])
    num = add("content", title, sub_, [blocks, res_label] + items + [read], notes + tail if W(notes + tail) <= 60 else notes, take)
    e["slide"] = num; e["rows"] = [[r[0] for r in g["rows"]] for g in gl]
    if not FIRST_CODE: FIRST_CODE.append(num)
    return num



# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories (5N1K: who, what, when, where, why, how; a real picture; a live link)
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORY_BEATS = {
    "SchnorrPatent": ["WHAT: Claus-Peter Schnorr's signature scheme was patented in the United States as patent 4,995,082, published on 19 February 1991.",
                      "WHY: The patent kept the scheme out of open standards, so ECDSA was the only signature Bitcoin knew until 2021.",
                      "HOW: The term was the longer of 17 years from grant and 20 from filing, so it ended on 23 February 2010.",
                      "SO WHAT: BIP340 is Schnorr's scheme fitted to secp256k1; it went live with taproot, 30 years after the paper."],
    "BookSignature": ["WHAT: The long hexadecimal signature that the book dissects in its DER section is a real signature from a mined payment.",
                      "WHY: A real example can be checked: the chapter recomputes it, and signature, key and transaction agree.",
                      "HOW: The payment was mined on 27 December 2013 at 23:11:54 UTC; its R has 33 bytes because its top bit is set.",
                      "SO WHAT: Its S is already the low form, so a node would still relay it today."],
    "AndroidRandom": ["WHAT: On 11 August 2013 Bitcoin.org warned that Android's random number generator was weak and that wallets built on it could be robbed.",
                      "WHY: A weak generator can repeat or leak a nonce, and a repeated nonce hands over the private key, as the previous slides computed.",
                      "HOW: Alex Klyubin of Google explained the flaw on 14 August; Bitcoin Wallet and other wallets shipped updates.",
                      "SO WHAT: RFC 6979 derives the nonce from key and message, which is why Bitcoin Core no longer needs a good generator for it."],
}
STORY_SUB = {"SchnorrPatent": "A patent decided which signature Bitcoin started with", "BookSignature": "The signature printed in the book is a real payment",
             "AndroidRandom": "Weak randomness at signing time gives away the key"}


STANDIN = {"BookSignature": "Stand-in picture: no picture of the sender exists", "AndroidRandom": "Stand-in: the platform, not the incident"}


def story_slide(sid):
    st = STORY[sid]; beats = STORY_BEATS[sid]
    for b in beats:
        if W(b) > 30: raise SystemExit("REFUSED: beat of %s has %d words" % (sid, W(b)))
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    cut = lambda s: s[:150].rsplit(",", 1)[0] if len(s) > 150 else s
    items = [{"t": "img", "path": ASSETS + st["photo"], "x": 0.5, "y": 1.4, "w": 3.4, "h": 2.55, "cap": st["credit"]},
             {"t": "beats", "x": 4.1, "y": 1.4, "w": 5.4, "h": 2.7, "fs": 11.5, "items": beats},
             ] + ([{"t": "text", "x": 0.5, "y": 4.3, "w": 3.4, "h": 0.17, "body": STANDIN[sid], "fs": 8.5, "font": "B", "italic": True, "color": "mute"}] if sid in STANDIN else []) + [
             {"t": "factrow", "x": 0.5, "y": 4.5, "w": 9.0, "who": cut(st["who"]), "where": cut(st["where"]), "when": st["when"], "link": st["link"], "linkText": st.get("linkLabel") or host}]
    first = sentences(st["story"])[0]
    notes = "This is a true story, dated %s. %s" % (st["when"], first)
    tail = " The lesson is that %s." % (st["lesson"][0].lower() + st["lesson"][1:]).rstrip(".")
    if W(notes + tail) <= 60: notes += tail
    if W(notes) > 60: notes = "This is a true story, dated %s. The lesson is that %s." % (st["when"], (st["lesson"][0].lower() + st["lesson"][1:]).rstrip("."))
    return add("content", st["title"], STORY_SUB[sid], items, notes)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
PLAN = {
    "SignatureFoundations": (["ex01", "ex02", "ex03"], {}),
    "SighashFlags": (["ex04", "ex05", "ex06"], {}),
    "SchnorrSignatures": (["ex07", "ex08", "ex09", "ex10", "ex11"], {"ex08": "SchnorrPatent"}),
    "EcdsaSignatures": (["ex12", "ex13", "ex14"], {"ex13": "BookSignature"}),
    "Randomness": (["ex15", "ex16", "ex17"], {"ex15": "AndroidRandom"}),
    "SegwitSigning": (["ex18", "ex19"], {}),
    "SinceTheBook": (["ex20"], {}),
}
BR_KEY = {b: [k for k, v in K.K3.items() if v[0] == b] for b in BRANCHES}


def build():
    S.clear(); ANALOGIES.clear(); FIRST_CODE.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 8: Digital Signatures", "What a signature proves and commits to, how Schnorr and ECDSA work, and what moved since print",
        [{"t": "img", "path": ASSETS + "ch08_bitcoinlogo.png", "x": 7.3, "y": 0.35, "w": 1.9, "h": 1.9},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: the Bitcoin logo, public domain (Wikimedia Commons). Python %s; Bitcoin Core 31.1.0 results are recorded, not run here." % PY}],
        "This deck explains how a Bitcoin signature works and what it commits to. Every number on a result picture was computed with the chapter's own Python library. Bitcoin Core 31.1.0 was run once on a test network, and its answers are only read back.")
    add("content", "Today's route", "", [], "", "Seven parts, twenty examples, three true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "What must a verifier have before it can answer yes or no?", "What does each SIGHASH flag commit to, and what does SINGLE do with no matching output?",
            "How does a three-move proof become a 64-byte Schnorr signature?", "Why are keys that simply add up unsafe, and what does MuSig2 change?",
            "Why can an ECDSA signature take two forms, and what do consensus and policy each accept?", "Why does a repeated nonce leak the key, and what does RFC 6979 do about it?",
            "What did segregated witness change in what is signed?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, seven parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 4, "fs": 12.5, "subfs": 10.5, "accent": [2],
          "items": [{"label": LAB[b], "sub": ("%d key concepts, %d examples" % (len(BR_KEY[b]), len(PLAN[b][0]))) if BR_KEY[b] else "%d example and the dates" % len(PLAN[b][0])} for b in BRANCHES]}],
        "The chapter has seven parts and %d key concepts. Each part gets a divider, concept cards with everyday comparisons, code that runs, and some parts a true story. The deck follows the order of the chapter." % sum(len(v) for v in BR_KEY.values()),
        "Seven parts; every slide today lives on this map")
    for b in BRANCHES:
        exs, stories = PLAN[b]
        divider(b)
        cks = chunks(BR_KEY[b]); order = []
        for i in range(max(len(cks), len(exs))):
            if i < len(cks): order.append(("c", i))
            if i < len(exs): order.append(("x", exs[i]))
        for kind, v in order:
            if kind == "c": cards(b, cks[v], v + 1, len(cks))
            else:
                code_slide(EX[v])
                if v in stories: story_slide(stories[v])
                if v == "ex14":
                    add("content", "Policy or consensus?", "Why a transaction can be valid and still not be relayed",
                        [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                          "left": {"head": "Consensus decides what is valid", "rows": ["Every node must agree, or the chain splits.", "A change needs a soft or hard fork.", "Like the law of the land."]},
                          "right": {"head": "Policy decides what is relayed", "rows": ["Each node may choose its own rules.", "A change needs only a new release.", "Like the house rules of a shop."]}}],
                        "High S is policy: miners accept it, nodes do not relay it. Strict DER became consensus in 2015. Keeping the two apart explains why a transaction can be valid and yet never reach a miner through ordinary nodes.",
                        "Policy can change with a release; consensus changes only by a fork")
        if b == "SinceTheBook":
            add("content", "Status of the BIPs the chapter names", "Thirteen proposals; status read from the saved BIP index",
                [{"t": "chart", "ctype": "bar", "x": 0.5, "y": 1.5, "w": 5.6, "h": 3.3, "labels": list(BIPS), "series": [{"name": "proposals", "data": [float(v) for v in BIPS.values()]}], "dataLabels": True, "dlFs": 10, "dlPos": "outEnd"},
                 {"t": "text", "x": 6.4, "y": 1.6, "w": 3.1, "h": 1.7, "body": "Deployed: 66, 143, 327, 340, 341 and 342. Drafts: 118, 361, 390 and 461. Complete: 54 and 373. Closed: 146.", "fs": 12.5, "font": "B", "color": "ink"},
                 {"t": "text", "x": 6.4, "y": 3.4, "w": 3.1, "h": 1.3, "body": "Counted from the saved index in deck 1.1.0, run under Python 3.14.6.", "fs": 10.5, "font": "B", "italic": True, "color": "mute"}],
                "The book states what was a draft in 2023. Counting the saved index of proposals shows six deployed, two complete, four drafts and one closed. A draft can still change, so check the index before you rely on a number.",
                "A proposal's status can change after print; check the index")
    add("content", "The chapter in five lines", "One line per part, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A signature is checked from message, public key and signature; scalars wrap at n and the digest is what is signed.",
            "A SIGHASH flag chooses what is signed, and SINGLE with no matching output signs the number one.",
            "Schnorr turns a three-move proof into 64 bytes; keys add up safely only with MuSig2, and shares give thresholds.",
            "ECDSA has two forms of s and a nested byte layout; a reused nonce leaks the key and RFC 6979 prevents it.",
            "Segwit hashes less and signs the amount; policy is stricter than consensus, and standards moved after print."]}],
        "These five lines are the deck in miniature, one for each group of parts. A line that feels unproven should send you back to its code slide, because every figure in it was computed there. The chapter code tab of the course page reruns all twenty examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch, and every link was opened on the date in the subtitle. A good start is the Optech workshop on Schnorr and taproot, then BIP340 read beside the chapter. The course page for chapter 8 carries the full text.",
        "Watch the Optech workshop, then read BIP340 beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What a verifier needs", "What each SIGHASH flag commits to",
            "How Schnorr, MuSig2 and ECDSA signatures work", "Why the nonce matters; policy against consensus"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 8 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Seven parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 3, "fs": 11.0, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has seven parts that follow the order of the chapter. Three true stories and twenty code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
    return N


BIPS = {"Deployed": 6, "Complete": 2, "Draft": 4, "Closed": 1}
RES_SUB = "Opened on 2026-10-23; every entry is a live link in this file"


def refuse(N):
    """the deck standard held at build time: D2 (30 words per text box), D7 (60 words of notes), D1 (numbering is the renderer's), D4/D11 (the key concepts)"""
    bad = []
    def box(t, where):
        if W(t) > 30: bad.append("%s: a text box of %d words: %r" % (where, W(t), t[:50]))
    for i, s in enumerate(S, 1):
        if W(s["notes"]) > 60: bad.append("slide %d: notes of %d words" % (i, W(s["notes"])))
        box(s["title"], "slide %d title" % i); box(s["sub"], "slide %d subtitle" % i)
        if s.get("take") and W(s["take"]) > 24: bad.append("slide %d: takeaway over 24 words" % i)
        for it in s["items"]:
            t = it.get("t")
            for k in ("body", "q"):
                if k in it: box(it[k], "slide %d %s" % (i, t))
            if t == "bullets": box(" ".join(it["items"]), "slide %d bullets (one frame)" % i)
            elif t == "concepts":
                for v in it["items"]:
                    box(v["label"] + " " + v["meaning"], "slide %d card head" % i); box(v["analogy"], "slide %d card analogy" % i)
            elif t == "groups":
                for v in it["items"]: box(v["pill"], "slide %d pill" % i); box(v["meaning"], "slide %d meaning" % i); box(v["analogy"], "slide %d analogy" % i)
            elif t == "codeblocks":
                for g in it["groups"]:
                    box(" ".join(r[0] + " " + r[1] for r in g["rows"]) + " >>>" * len(g["rows"]), "slide %d code frame" % i); box(g["note"], "slide %d note" % i)
            else:
                for v in it.get("items", []):
                    if isinstance(v, str): box(v, "slide %d %s" % (i, t))
                    elif isinstance(v, dict): box(" ".join(str(x) for x in v.values()), "slide %d %s" % (i, t))
            for side in ("left", "right"):
                if side in it: box(" ".join(it[side]["rows"]), "slide %d compare" % i)
    text = " ".join(json.dumps(s["items"]) + s["title"] + s["sub"] for s in S).lower()
    allc = list(K.K3)
    missing = [c for c in allc if c.lower() not in text]
    cov = 100.0 * (len(allc) - len(missing)) / len(allc)
    print("coverage (D11, by key concept label on a slide): %d of %d = %.1f percent; missing: %s" % (len(allc) - len(missing), len(allc), cov, missing))
    ana = {a["concept"] for a in ANALOGIES}
    nona = [c for c in allc if c not in ana]
    print("analogies (D4): %d of %d key concepts carry one; without: %s" % (len(allc) - len(nona), len(allc), nona))
    if bad: raise SystemExit("REFUSED:\n  " + "\n  ".join(bad))
    if missing or nona: raise SystemExit("REFUSED: key concepts missing or without analogy")
    return cov


LIBMODS = ["sen0401_ch07_script_lib_v1_0_0", "sen0401_ch08_sig_lib_v1_0_0", "sen0401_ch08_claims_v1_0_0"]


def manifest(N):
    setup = "# setup: the chapter library of the page (L = chapter 7 script and curve library, C = chapter 8 signature library, K = chapter 8 claims); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch08_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY the three library modules (no evidence folder, as in the page's wheel), the setup and the listing
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch08_")
    for m in LIBMODS: shutil.copy(os.path.join(TOOL, m + ".py"), tmp)
    prog = os.path.join(tmp, "run_all.py")
    open(prog, "w").write("import json, sys\nsys.path.insert(0, %r)\nex = json.load(open(%r))\nbad = []\nfor e in ex:\n    ns = {}\n    exec(%r, ns); exec(e['code'], ns)\n    for s in e['show']:\n        got = repr(eval(s['expression'], ns))\n        if got != s['expected']: bad.append((e['id'], s['expression'], got, s['expected']))\nprint(json.dumps(bad))\n" % (tmp, os.path.join(tmp, "ex.json"), setup))
    json.dump(exs, open(os.path.join(tmp, "ex.json"), "w"))
    for py in ("python3.14", "python3.13"):
        exe = shutil.which(py)
        if not exe: print("page-path check: %s not installed, skipped" % py); continue
        r = subprocess.run([exe, "-I", prog], capture_output=True, text=True, cwd=tmp)
        if r.returncode: raise SystemExit("REFUSED: page-path run under %s failed:\n%s" % (py, r.stderr[-800:]))
        bad = json.loads(r.stdout.strip().splitlines()[-1])
        if bad: raise SystemExit("REFUSED: page-path run under %s differs from the recording: %s" % (py, bad))
        print("page path (library modules only, no evidence folder) under %s: %d examples reproduce the recorded values" % (py, len(exs)))
    shutil.rmtree(tmp, ignore_errors=True)
    return {"manifest": "chapter_code_ch08_v1_0_0", "chapter": 8, "deck": "SEN0401_Ch08_DigitalSignatures_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch08_lib", "file": "03-materials/ch08/assets/sen0401_ch08_lib-1.0.0-py3-none-any.whl", "sha256": hashlib.sha256(open(os.path.join(ROOT, "03-materials", "ch08", "assets", "sen0401_ch08_lib-1.0.0-py3-none-any.whl"), "rb").read()).hexdigest(), "modules": LIBMODS,
                        "import": "import sen0401_ch07_script_lib_v1_0_0 as L, sen0401_ch08_sig_lib_v1_0_0 as C, sen0401_ch08_claims_v1_0_0 as K"}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 8: Digital Signatures", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-23, task TK_Ch08_Deck_Build: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch08", "page", "chapter_code_ch08_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch08_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 8"])
    mat = os.path.join(ROOT, "03-materials", "ch08", "SEN0401_Ch08_DigitalSignatures_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
