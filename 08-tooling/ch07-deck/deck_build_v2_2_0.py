#!/usr/bin/env python3
"""deck_build v2.2.0 - the generator of the chapter 7 deck 2.2.0 (task TK_Deck07_ArcFix_Build, 2026-10-25: a copy of deck_build_v2_1_0.py with ONE content change, the notes of slide 35 (example 9) shortened from five sentences to four so that arc check v1_2_0 accepts them; the examples, concepts and recorded executions are unchanged, so the manifest stays chapter_code_ch07_v1_0_0.json/v1_1_0 and is not written). Earlier text of v2.1.0: the generator of the chapter 7 deck 2.1.0 (task TK_Ch07_Deck_Reissue, 2026-10-24: the re-issue of deck 2.0.0 in new files, same content; the content inputs examples_v2_0_0, deck_concepts_v2_0_0 and examples_out_v2_0_0.json are read unchanged; the manifest is verified on the page path but NOT written, it stays chapter_code_ch07_v1_0_0.json; outputs go to the folder named by the environment variable DECK_OUT, default this folder). Earlier text: the generator of the chapter 7 deck 2.0.0 (task TK_Ch07_Deck_Build, 2026-10-23, owner-directed work ex:CR3_Ch78), a NEW file written on the pattern of
08-tooling/ch06-deck/deck_build_v2_1_0.py. It writes, from the chapter research, the recorded executions and the stories of the chapter, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest
03-materials/ch07/page/chapter_code_ch07_v1_0_0.json and, with --render, (3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).
What it reads: the 87 key concepts of the research with their analogies (deck_concepts_v2_0_0.py), the story module sen0401_ch07_stories_v1_2_0.py (three stories with pictures), the recorded executions
examples_out_v2_0_0.json (made by examples_run_v2_0_0.py under Python 3.14), and the resources slide of the previous plan (deck_plan_v1_3_0.json). Every number on a result picture is parsed from the
recorded output, never typed. The deck standard (D1-D12) is held as refusals BEFORE the file is drawn: no text box over 30 words, notes of at most 60 words, no code line over 60 characters with its
prompt (a listing never wraps), every concept of the research on a slide with its analogy.
Usage: python3.14 deck_build_v2_2_0.py [--render]"""
__version__ = "2.2.0"
import ast, glob, hashlib, importlib, importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_0_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.2.0", "2_2_0"
EXV = "2_0_0"   # the content inputs (examples, concepts, recorded executions) are the unchanged v2_0_0 files
DOUT = os.environ.get("DECK_OUT", HERE)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch07_stories_v*.py")), key=vk)[-1], "stories07")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % EXV)))
PY = OUT["_python"]
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch07/assets/"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v1_3_0.json")))
BRANCHES = K.BRANCHES
LAB = {b: K.L1[b][0] for b in BRANCHES}
CONC = {b: [c for c in K.C if c[1] == b] for b in BRANCHES}
S, ANALOGIES, FIRST_CODE = [], [], []
EST = lambda text, fs, width, k=0.0078: max(1, -(-int(len(text) * fs * k * 100) // int(width * 100)))   # lines a text needs: characters x font size x 0.0078 in, over the width
W = lambda t: len(re.findall(r"\S+", t))
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"


def val(ex, expr):
    for e, o in OUT[ex]:
        if e == expr: return ast.literal_eval(o)
    raise KeyError((ex, expr))


def add(kind, title, sub, items, notes, take=None, bg="light"):
    sl = {"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg}
    if take: sl["take"] = take
    S.append(sl)
    return len(S)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# dividers: the part's concept groups with a line of meaning and an analogy each, and the strip of the nine parts as a native table
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEGS = [(K.L1[b][2], 1.0) for b in BRANCHES]


def strip(branch, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(f for _, f in SEGS)
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": b == branch} for (lab, f), b in zip(SEGS, BRANCHES)]}


DIV_NOTES = {
    "ScriptLanguage": "Every coin is locked by a small program. This part shows the language, its stack and the two scripts that run one after the other. A bug of 2010 shows why they must run apart.",
    "KeyLocking": "The most common lock asks for a signature from one key. We lock a coin to the hash of a public key, check a signature, and see why the strict signature format caused a fork in 2015.",
    "ScriptedMultisig": "A lock can ask for t signatures out of k keys. We run a real two-of-three spend, see why the signatures must follow the order of the keys, and meet the extra element that the opcode pops.",
    "PayToScriptHash": "A long lock is costly for the payer. Pay to script hash puts only a hash in the output and lets the spender reveal the script. We build one and watch a wrong script fail.",
    "DataAndTime": "Two special locks. One records a few bytes of data and can never be spent. The others make a coin wait, until a time or block, or for an age counted from the day it was mined.",
    "FlowControl": "A script can choose between paths, and a check can stop it early. We combine both in a capital account that partners open at once, a lawyer opens after thirty days, and the lawyer alone after ninety.",
    "SegwitScripts": "Segregated witness moves the proof out of the transaction identifier. We spend a witness key hash, look at what real inputs of one block spend, and see why this upgrade was a soft fork.",
    "TreesAndTweaks": "Two ideas that taproot combines. A tree of scripts is committed to by one hash, and a key can be tweaked to commit to hidden data, so many signers look like one.",
    "TaprootBranch": "Taproot gives an output one key that hides a tree. We spend it by key and by script, count signatures with a new opcode, and end with a story of a patented signature.",
}


def divider(branch):
    groups = [g for g, v in K.L2.items() if v[0] == branch]; n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 2 else 11
    its = []
    for g in groups:
        _, pill, mean, ana = K.L2[g]
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12 if n <= 3 else 11, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (branch, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12 if n <= 3 else 11, "items": its}, strip(branch)]
    ANALOGIES.append({"concept": LAB[branch], "analogy": K.L1[branch][1], "slide": len(S) + 1})
    return add("section", LAB[branch], K.L1[branch][1], items, DIV_NOTES[branch])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards: the research label, its meaning, its everyday analogy
# ------------------------------------------------------------------------------------------------------------------------------------------------
def chunks(lst):
    n = len(lst); k = -(-n // 4); size = -(-n // k); return [lst[i:i + size] for i in range(0, n, size)]


def cards(branch, cs, part, parts):
    n = len(cs); cols = 2 if n == 4 else min(3, n); rows = -(-n // cols); bw = (9.0 - (cols - 1) * 0.16) / cols; fw = bw - 0.3
    avail = (3.5 - (rows - 1) * 0.14) / rows
    for fs in (11.5, 11, 10.5, 10):
        items, need = [], 0
        for label, _, meaning, ana_ in cs:
            ana = "Think of " + ana_ + "."
            hA = (EST(label, fs + 1.5, fw, 0.0088) * (fs + 1.5) + EST(meaning, fs, fw) * fs) * 1.22 / 72 + 0.06
            hB = EST(ana, fs, fw) * fs * 1.22 / 72 + 0.04
            items.append({"label": label, "meaning": meaning, "analogy": ana, "hA": round(hA, 3), "hB": round(hB, 3), "hC": 0}); need = max(need, 0.07 + hA + hB + 0.1)
        if need <= avail: break
    else:
        raise SystemExit("REFUSED: cards %s need %.2f in, %.2f available" % ([c[0] for c in cs], need, avail))
    for it in items:
        for k in ("meaning", "analogy"):
            if W(it[k]) > 30: raise SystemExit("REFUSED: card %s has a frame of over 30 words" % it["label"])
        if W(it["label"] + " " + it["meaning"]) > 30: raise SystemExit("REFUSED: card %s head frame over 30 words" % it["label"])
        ANALOGIES.append({"concept": it["label"], "analogy": it["analogy"], "slide": len(S) + 1})
    suffix = " (%d of %d)" % (part, parts) if parts > 1 else ""
    title = "%s: concepts%s" % (LAB[branch], suffix)
    if len(title) > 40: title = "%s%s" % (LAB[branch], suffix)
    if len(title) > 40: title = "%s%s" % (K.L1[branch][2], suffix)
    names = [c[0] for c in cs]
    names_t = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 7." % names_t
    if W(notes) > 60: notes = "These cards cover %d concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 7." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("Script is arithmetic on a stack", "The smallest script of the chapter, run in the chapter's interpreter", "Numbers are pushed; an operation takes its inputs from the top",
             "Script reads its words from left to right. Numbers are pushed on the stack, and OP_ADD replaces the top two by their sum. OP_EQUAL compares the sum with five, so the spend is true with five and false with six."),
    "ex02": ("The OP_RETURN bug of 2010", "Joined scripts against separate scripts", "Run the two scripts apart, and fail closed on anything unknown",
             "In 2010 the software joined the input script and the output script into one program. An input script of 1 then OP_RETURN ended the run with a true value before the lock ran. Today the scripts run apart."),
    "ex03": ("A key-hash lock, tried three ways", "Pay to public key hash with a real signature", "Only the owner of the key, signing this exact transaction, opens the lock",
             "The lock holds the hash of a public key. The spender shows the key and a signature over the transaction. A wrong key fails, and so does a changed amount, because the signature covers the amount."),
    "ex04": ("A DER signature, strict and loose", "Why the encoding of a signature is a consensus rule", "A rule that nodes check for themselves cannot be skipped",
             "A signature is two numbers, r and s, written in DER with a hash type at the end. A padded form was once accepted. Since BIP66 only the strict form is valid, which is the rule behind the fork of 2015."),
    "ex05": ("A 2-of-3 multisignature", "Signatures in key order, and the extra element", "The signatures must follow the order of the keys, after one empty dummy",
             "A two-of-three lock lists three keys and wants two signatures in the same order. A single signature fails. The opcode also pops one item too many, so a dummy sits in front and must be empty."),
    "ex06": ("Pay to script hash", "The payer sees a hash, the spender shows the script", "The long lock moves from the payer to the spender",
             "The output holds only the 20-byte hash of the script, so the payer pays for a short lock. The spender reveals the script, nodes hash it, compare, and then run it. A script that hashes differently fails."),
    "ex07": ("A lock until block 800,000", "OP_CHECKLOCKTIMEVERIFY on a real spend", "The transaction's lock time must reach the number in the script",
             "The script holds a block number. The spending transaction must carry a lock time of at least that number, and its sequence must not be final. One block too early fails, and so does a final sequence."),
    "ex08": ("A wait of 4,320 blocks", "OP_CHECKSEQUENCEVERIFY counts the age of the coin", "The sequence of the input must reach the number in the script",
             "A relative lock counts from the block that confirmed the coin. The input's sequence must reach 4,320 blocks, about thirty days, and the transaction must be version 2. Setting bit 31 turns the lock off."),
    "ex09": ("Three ways out of one output", "Partners at once, a lawyer after 30 days, the lawyer alone after 90", "A conditional script lets one output have several spending paths",
             "Mohammed's capital account uses OP_IF to pick a path. Two of three partners may spend at once. The lawyer with one partner must wait 4,320 blocks, and the lawyer alone 12,960."),
    "ex10": ("Pay to witness public key hash", "A key-hash spend with the proof in the witness", "The signature commits to the amount; the address is bech32",
             "A witness key-hash output is 22 bytes. The signature and the key travel in the witness, not in the input script. They work directly and nested in a script hash, and the signature covers the amount."),
    "ex11": ("A proof grows with the logarithm", "How many hashes a script tree reveals", "A million scripts need only twenty hashes in a proof",
             "A spender reveals one script and the sibling hashes up to the root. Our three scripts need two, two and one. Every doubling of the tree adds one hash, so a tree of a million scripts needs twenty."),
    "ex12": ("Taproot: a key path spend", "One signature, no script revealed", "The output key is the internal key plus a tweak",
             "A taproot output holds one 32-byte key. Spending by key path needs a single 64-byte Schnorr signature, and nothing about the hidden scripts is revealed. A key that was not tweaked correctly is refused."),
    "ex13": ("Taproot: the script path", "Reveal one script of the tree and its proof", "Each path costs about as much as a plain witness script",
             "Spending by script path reveals one leaf script, its data and a control block with the proof. All three paths of the account script verify. Their weights are close to those of the same paths in a witness script hash."),
    "ex14": ("Counting signatures: OP_CHECKSIGADD", "Tapscript's replacement for CHECKMULTISIG", "Each valid signature adds one; an empty slot adds nothing",
             "Tapscript drops the old multisignature opcode. A script checks each key in turn and adds one to a counter per valid signature, then compares the counter with t. The script is a byte shorter than before."),
    "ex15": ("Opcodes kept for upgrades", "OP_SUCCESS in tapscript", "Unknown opcodes succeed, so soft forks can give them a meaning",
             "In tapscript 87 opcode values are OP_SUCCESS: a script that contains one succeeds on sight. This leaves room for future soft forks. The disabled shift of the old language still fails in an old script."),
}

TAIL = " It is example %d in the chapter code tab of the course page."


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    if ex == "ex01":
        ok, bad, code = val(ex, "res")
        return ([tb([["Program", "Result"], ["2 3 OP_ADD 5 OP_EQUAL", ok], ["2 3 OP_ADD 6 OP_EQUAL", bad], ["Assembled bytes", code]], [1.75, 1.5])],
                "the same script with a five and a six", "The sum is five, so the first script ends true and the second false. The five words assemble to five bytes.")
    if ex == "ex02":
        j, n, r = val(ex, "res")
        return ([tb([["Engine", "Result"], ["2010: joined scripts", j], ["Today: scripts apart", n], ["Real secret, today", r]], [1.75, 1.5])],
                "a spend that has no secret, and one that has", "In the old engine OK means that anyone could spend the coin. Today the same input fails with OP_RETURN.")
    if ex == "ex03":
        k = val(ex, "kind"); r = val(ex, "res")
        return ([tb([["Spend", "Result"], ["Lock: bytes, kind", "%d, %s" % k], ["Right key", r[0]], ["Wrong key", r[1]], ["Amount changed", r[2]]], [1.45, 1.8])],
                "four trials of one lock", "Only the right key signing the real amount opens it; the other two fail with EVAL_FALSE.")
    if ex == "ex04":
        f = val(ex, "facts"); r = val(ex, "res")
        return ([tb([["Check", "Result"], ["Length with hash type", str(f[0])], ["First byte (0x30 = 48)", str(f[1])], ["Low s", yn(f[2])], ["Padded, old rules", r[0]], ["Padded, DER rule", r[1]]], [1.85, 1.4])],
                "one signature, two rule sets", "The same padded signature passes without the DER rule and fails with it, with the error SIG_DER.")
    if ex == "ex05":
        r = val(ex, "res"); d = val(ex, "dummy"); sz = val(ex, "len(RED)")
        return ([tb([["Spend", "Result"], ["Keys 0 and 2, in order", r[0]], ["Keys 2 and 0", r[1]], ["Only key 1", r[2]], ["Dummy not empty", d]], [1.4, 1.85], 9)],
                "five trials of a 2-of-3 lock", "The script is %d bytes long. Only signatures in the order of the keys, behind an empty dummy, pass." % sz)
    if ex == "ex06":
        r = val(ex, "res")
        return ([tb([["Quantity", "Result"], ["Address begins", r[0]], ["Lock, bytes", str(r[1])], ["Right script shown", r[2]], ["Other script shown", r[3]]], [1.6, 1.65])],
                "the hash lock and two reveals", "The lock is 23 bytes however long the script is. A script that does not match the hash fails.")
    if ex == "ex07":
        r = val(ex, "res")
        return ([tb([["Lock time of the spend", "Result"], ["800,000, not final", r[0]], ["799,999, not final", r[1]], ["800,000, final", r[2]]], [1.55, 1.7])],
                "three spends of one script", "Only a lock time that reaches 800,000, with a sequence that is not final, satisfies the script.")
    if ex == "ex08":
        ok, e_, v1, off = val(ex, "ok"), val(ex, "early"), val(ex, "v1"), val(ex, "off")
        return ([tb([["Spend", "Result"], ["Version 2, 4,320", ok], ["Version 2, 4,319", e_], ["Version 1, 4,320", v1], ["Bit 31 set", off]], [1.2, 2.05], 9)],
                "four spends of one script", "One block short, the old version, or a disabled lock each fail with UNSATISFIED_LOCKTIME.")
    if ex == "ex09":
        sz, p1, p2, p3 = val(ex, "size"), val(ex, "p1"), val(ex, "p2"), val(ex, "p3")
        return ([tb([["Path and wait", "Result"], ["1: partners, none", p1], ["2: lawyer, 4,320", p2[0]], ["2: lawyer, 4,319", p2[1]], ["3: lawyer, 12,960", p3[0]], ["3: lawyer, 4,320", p3[1]]], [1.35, 1.9], 9)],
                "the script of %d bytes, six spends" % sz, "Each path works only after its wait; asking one block early fails with UNSATISFIED_LOCKTIME.")
    if ex == "ex10":
        ok, wr, ad = val(ex, "ok"), val(ex, "wrong"), val(ex, "addr")
        return ([tb([["Spend", "Result"], ["Direct", ok[0]], ["Nested in P2SH", ok[1]], ["Amount changed", wr], ["Address", ad[:12] + "..."]], [1.4, 1.85])],
                "a witness key-hash spend", "The signature covers the amount, so a changed amount fails. The address starts with bc1q.")
    if ex == "ex11":
        pr, ns, dp = val(ex, "proof"), val(ex, "ns"), val(ex, "depth")
        return ([ch([fmt(n) for n in ns], dp, "hashes in the proof")], "hashes in a proof, by scripts in the tree",
                "Our three scripts need %s hashes each. A tree of 1,048,576 scripts needs only %d." % (", ".join(str(p) for p in pr), dp[-1]))
    if ex == "ex12":
        k = val(ex, "kind"); r = val(ex, "res")
        return ([tb([["Quantity", "Result"], ["Address begins", k[0]], ["Output key, bytes", str(k[1])], ["Key path spend", r[0]], ["Signature, bytes", str(r[1])], ["Weight units", str(r[2])], ["Untweaked key", r[3]]], [1.6, 1.65], 9)],
                "one key path spend", "One 64-byte signature spends it. A key that was not tweaked as the output says fails with SCHNORR_SIG.")
    if ex == "ex13":
        res, tap, wsh = val(ex, "res"), val(ex, "tap"), val(ex, "wsh")
        c = {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": ["path 1", "path 2", "path 3"], "series": [{"name": "taproot script path", "data": [float(v) for v in tap]},
             {"name": "witness script hash", "data": [float(v) for v in wsh]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
        return ([c], "weight units of three spends, two ways", "All three paths verify (%s). Orange bars: taproot script path; green bars: the same path as a witness script hash." % ", ".join(res))
    if ex == "ex14":
        sz = val(ex, "sizes"); r = val(ex, "res")
        return ([tb([["Quantity", "Result"], ["CHECKSIGADD script, bytes", str(sz[0])], ["Old 2-of-3 script, bytes", str(sz[1])], ["Two signatures", r[0]], ["One signature", r[1]]], [1.85, 1.4])],
                "the same rule, two ways of writing it", "The tapscript form is one byte shorter. Two valid signatures reach the count; one does not.")
    if ex == "ex15":
        n, ok, old = val(ex, "res")
        return ([tb([["Quantity", "Result"], ["OP_SUCCESS values", str(n)], ["Opcode 152 in tapscript", ok], ["Same word, old script", old]], [1.7, 1.55])],
                "unknown words in tapscript and in an old script", "Of 256 opcode values, %d are OP_SUCCESS. The disabled shift fails in an old script with DISABLED_OPCODE." % n)
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex11", "ex13") else "table"


def code_slide(e):
    ex = e["id"]; fs = 10; lh = fs * 1.3 / 72
    title, sub_, take, notes = CODE_TEXT[ex]
    fin = e["final"]; groups = [list(g["lines"]) for g in e["groups"]]
    if not groups[-1]: groups[-1] = [fin]
    elif groups[-1][-1] != fin: groups[-1].append(fin)
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
    cap = ("run under Python %s - L, K and the chapter setup as on slide %d" % (PY, FIRST_CODE[0])) if FIRST_CODE else ("run under Python %s - names as in the chapter setup" % PY)
    blocks = {"t": "codeblocks", "x": X_, "w": W_, "fs": fs, "nfs": 10.5, "groups": gl, "cap": cap, "capy": capy}
    res_label = {"t": "text", "x": RX, "y": 1.45, "w": RW, "h": lab_h, "body": lab, "fs": 11, "font": "B", "bold": True, "color": "mute"}
    if items[0]["t"] == "table": ry = round(min(ry, vy + len(items[0]["rows"]) * items[0]["rowH"] + 0.3), 3)       # under the table, not at the foot of the slide
    read = {"t": "text", "x": RX, "y": ry, "w": RW, "h": rh, "body": reading, "fs": 11.5, "font": "B", "italic": True, "color": "ink"}
    if W(notes) > 60: raise SystemExit("REFUSED: notes of %s have %d words" % (ex, W(notes)))
    tail = TAIL % int(ex[2:])
    num = add("content", title, sub_, [blocks, res_label] + items + [read], notes + tail if W(notes + tail) <= 60 else notes, take)
    e["slide"] = num; e["rows"] = [[r[0] for r in g["rows"]] for g in gl]
    if not FIRST_CODE: FIRST_CODE.append(num)
    return num


# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories: 5N1K (who, what, when, where, why, how), a real picture, a live link
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORY_BEATS = {
    "OpReturnBug": ["WHAT: On 28 July 2010 two bugs were shown on the test network; one let a stranger spend coins that were not theirs.",
                    "WHY: The first software joined input and output script into one program, and OP_RETURN jumped to its end with a true result.",
                    "HOW: An input script of 1 then OP_RETURN ended the run true; version 0.3.5 fixed it, and later versions run the scripts apart.",
                    "SO WHAT: Many unused opcodes were disabled; in tapscript such values, like OP_LSHIFT (152), are now OP_SUCCESS."],
    "DerFork": ["WHAT: On 4 July 2015, at block 363,725, strict DER signatures (BIP66) took effect, and a fork of six blocks followed.",
                "WHY: About half of the hash rate mined without fully validating, so it built on an invalid block of a miner that had not upgraded.",
                "HOW: The fork lasted from 02:10 to 03:50 UTC, a second of three blocks followed on 5 July, and the first showed no double spend.",
                "SO WHAT: Bitcoin Core 0.9.5 and later checked the rule and were unaffected: a rule you do not check protects nobody."],
    "SchnorrToTaproot": ["WHAT: At block 709,632, mined on 14 November 2021, the taproot rules and Schnorr signatures (BIPs 340 to 342) took effect.",
                         "WHY: Claus Schnorr had patented his signature, which kept it out of open standards for almost two decades; ECDSA was used instead.",
                         "HOW: BIP340 was assigned in January 2020; a soft fork then added taproot and tapscript to the running chain.",
                         "SO WHAT: A key path spend is one 64-byte signature that looks the same whether one person or a million made it."],
}
STORY_FACT = {  # at most 22 characters each, because the renderer's fact row cuts longer text
    "OpReturnBug": ("Satoshi Nakamoto", "Bitcoin test network", "en.bitcoin.it"),
    "DerFork": ("Pieter Wuille, miners", "Block 363,725", "bitcoin.org"),
    "SchnorrToTaproot": ("Claus-Peter Schnorr", "Block 709,632", "mempool.space"),
}
STORY_SUB = {"OpReturnBug": "A bug of 2010 that let anyone spend any output", "DerFork": "Strict DER signatures, and the fork of 4 July 2015",
             "SchnorrToTaproot": "Taproot took effect at block 709,632 in 2021"}
STORY_TITLE = {"SchnorrToTaproot": "From a patented signature to taproot"}
STORY_BOX = {"photo_bitcoin_mining_farm.jpg": (3.5, 2.55)}        # a wide picture needs a wider frame to meet the 8 percent of the slide that D5 asks for


def story_slide(sid):
    st = STORY[sid]; beats = STORY_BEATS[sid]
    for b in beats:
        if W(b) > 30: raise SystemExit("REFUSED: beat of %s has %d words" % (sid, W(b)))
    who, where, link_text = STORY_FACT[sid]
    iw, ih = STORY_BOX.get(st["photo"], (2.6, 2.55)); bx = 0.5 + iw + 0.3
    items = [{"t": "img", "path": ASSETS + st["photo"], "x": 0.5, "y": 1.4, "w": iw, "h": ih, "cap": st["credit"]},
             {"t": "beats", "x": bx, "y": 1.4, "w": 9.5 - bx, "h": 2.7, "fs": 11.5, "items": beats},
             {"t": "factrow", "x": 0.5, "y": 4.5, "w": 9.0, "who": who, "where": where, "when": st["when"], "link": st["link"], "linkText": link_text}]
    first = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", st["story"].strip())[0]
    notes = "This is a true story, dated %s. %s" % (st["when"], first)
    tail = " The lesson: %s." % (st["lesson"][0].lower() + st["lesson"][1:]).rstrip(".")
    if W(notes + tail) <= 60: notes += tail
    if W(notes) > 60: notes = "This is a true story, dated %s. The lesson: %s." % (st["when"], (st["lesson"][0].lower() + st["lesson"][1:]).rstrip("."))
    return add("content", STORY_TITLE.get(sid, st["title"]), STORY_SUB[sid], items, notes)


def census_slide():
    ct, grp = val("census", "sum(K.census(L).values())"), val("census", "census_groups()")
    items = [{"t": "chart", "ctype": "bar", "x": 0.5, "y": 1.45, "w": 5.8, "h": 3.45, "labels": [g[0] for g in grp], "series": [{"name": "inputs", "data": [float(g[1]) for g in grp]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"},
             {"t": "text", "x": 6.55, "y": 1.45, "w": 2.95, "h": 0.5, "body": "Result: what %s real inputs spend" % fmt(ct), "fs": 11, "font": "B", "bold": True, "color": "mute"},
             {"t": "text", "x": 6.55, "y": 2.05, "w": 2.95, "h": 1.5, "body": "The chapter's interpreter ran every input of the first 599 non-coinbase transactions of block 775,072 and sorted them by the kind of output they spend.", "fs": 11.5, "font": "B", "color": "ink"},
             {"t": "text", "x": 6.55, "y": 3.7, "w": 2.95, "h": 1.2, "body": "Witness key hashes lead; taproot is still rare. Think of a motorway where most cars already use the new lane.", "fs": 11.5, "font": "B", "italic": True, "color": "ink"}]
    ANALOGIES.append({"concept": "P2WPKH", "analogy": "a motorway where most cars already use the new lane.", "slide": len(S) + 1})
    return add("content", "What 1,022 real inputs spend", "Block 775,072, classified by the chapter's own Script interpreter, bytes from mempool.space", items,
               "The first 599 transactions of block 775,072 hold 1,022 inputs. Our interpreter verified each of them and sorted them by spending type. Segwit key hashes dominate, legacy key hashes follow, and taproot is still a handful.",
               "Most real coins already move through witness programs")


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
def build():
    S.clear(); ANALOGIES.clear(); FIRST_CODE.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 7: Scripts and Signatures", "Authorization and authentication: scripts that lock coins, signatures that unlock them",
        [{"t": "img", "path": ASSETS + "mbc3_0701.png", "x": 4.1, "y": 0.45, "w": 5.4, "h": 1.2},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Figure: locking and unlocking scripts, Antonopoulos and Harding, Mastering Bitcoin 3e, CC BY-SA 4.0. Python %s, no Bitcoin Core node." % PY}],
        "This deck explains how Bitcoin decides who may spend an output. The output carries a lock, the spender supplies the key, and every node runs both and accepts only a true result. Every spend shown ran in the chapter's own interpreter; no Bitcoin Core node was available where it was built.")
    add("content", "Today's route", "", [], "", "Nine parts, fifteen runs and three true stories")
    add("content", "The questions this chapter answers", "Its own competency questions; we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "How do an output script and an input script together decide a spend?",
            "Why is Script not Turing complete, and why can every node verify it?",
            "How do key hashes, multisignatures and script hashes move cost to the spender?",
            "How do lock time and sequence make a spend wait?",
            "How does segregated witness fix malleability without splitting the network?",
            "What does taproot hide, and what does a key path or script path reveal?",
            "What does tapscript change in the language?"]}],
        "The seven questions are the chapter's own, shortened so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, nine parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 3, "fs": 12.5, "subfs": 10.5, "accent": [8],
          "items": [{"label": LAB[b], "sub": "%d concepts" % len(CONC[b])} for b in BRANCHES]}],
        "The chapter has nine parts and %d concepts. Each part gets a divider, concept cards with everyday comparisons and code that runs, and some parts a true story. The deck follows the order in which Bitcoin gained its spending conditions." % sum(len(CONC[b]) for b in BRANCHES),
        "Nine parts; every slide today lives on this map")
    plan = {
        "ScriptLanguage": (["ex01", "ex02"], {"ex02": "OpReturnBug"}),
        "KeyLocking": (["ex03", "ex04"], {"ex04": "DerFork"}),
        "ScriptedMultisig": (["ex05"], {}),
        "PayToScriptHash": (["ex06"], {}),
        "DataAndTime": (["ex07", "ex08"], {}),
        "FlowControl": (["ex09"], {}),
        "SegwitScripts": (["ex10"], {}),
        "TreesAndTweaks": (["ex11"], {}),
        "TaprootBranch": (["ex12", "ex13", "ex14", "ex15"], {"ex12": "SchnorrToTaproot"}),
    }
    for b in BRANCHES:
        exs, stories = plan[b]
        divider(b)
        cks = chunks(CONC[b]); order = []
        for i in range(max(len(cks), len(exs))):
            if i < len(cks): order.append(("c", i))
            if i < len(exs): order.append(("x", exs[i]))
        for kind, v in order:
            if kind == "c": cards(b, cks[v], v + 1, len(cks))
            else:
                code_slide(EX[v])
                if v in stories: story_slide(stories[v])
                if v == "ex10": census_slide()
        if b == "SegwitScripts":
            add("content", "Hard fork or soft fork?", "Why segregated witness could be activated without splitting the network",
                [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                  "left": {"head": "A hard fork loosens the rules", "rows": ["Blocks that old nodes reject become valid.", "Every node must upgrade, or the chain splits.", "Like a new road standard that old cars cannot use."]},
                  "right": {"head": "A soft fork tightens the rules", "rows": ["New nodes reject more; they accept nothing new.", "Old nodes still follow the chain and accept its blocks.", "Like a stricter speed limit that old cars can still obey."]}}],
                "Segregated witness was a soft fork. Old nodes saw the new outputs as anyone-can-spend scripts and accepted the blocks, while upgraded nodes enforced the witness rules. That is why it could be activated without a split.",
                "A soft fork can only restrict; old nodes keep accepting the blocks")
    add("content", "The chapter in five lines", "One line per group of parts, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A coin is locked by a script; the spender's script is the key, and the two run apart on a stack.",
            "Key hashes, multisignatures and script hashes lock a coin to what the spender can prove, and move the long lock to the spender.",
            "Lock time and sequence make a spend wait, and flow control gives one output several ways out.",
            "Segregated witness moves the proof out of the identifier, as a soft fork that old nodes accept.",
            "Taproot commits to a tree of scripts with one key, so agreement looks like a single signature."]}],
        "These five lines are the deck in miniature. A line that feels unproven should send you back to its code slide, because every result in it was computed there. The chapter code tab of the course page lets you rerun all fifteen examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", "Resources for further reading and watching; every entry is a live link in this file", [res],
        "Everything here is free to read or watch. A good exercise is to take any spend from the explorer and run it through the chapter's interpreter. The course page for chapter 7 carries the full resource list.",
        "Run a real spend through the interpreter and match the explorer's verdict")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "How a lock and a key decide a spend", "How signatures and script hashes are checked",
            "How timelocks shape who spends, and when", "What segwit and taproot change"]}],
        "Four claims, each carried by runs of the chapter's own interpreter on slides of this deck. The course page for chapter 7 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Nine parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 3, "fs": 11, "subfs": 10, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has nine parts that follow the order in which Bitcoin gained its spending conditions. Three true stories and fifteen code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every slide can be rerun."
    return N


def refuse(N):
    """the deck standard held at build time: D2 (30 words per text box), D7 (60 words of notes), D1 (numbering is the renderer's), D4 and D11 (every research concept on a slide with an analogy)"""
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
                    box(" ".join(r[0] + " " + r[1] for r in g["rows"]), "slide %d code frame" % i); box(g["note"], "slide %d note" % i)
            elif t == "beats":
                for v in it["items"]: box(v, "slide %d beat" % i)
            elif t == "chart" or t == "links" or t == "table" or t == "striptable":
                pass
            else:
                for v in it.get("items", []):
                    if isinstance(v, str): box(v, "slide %d %s" % (i, t))
                    elif isinstance(v, dict): box(" ".join(str(x) for x in v.values()), "slide %d %s" % (i, t))
            for side in ("left", "right"):
                if side in it: box(" ".join(it[side]["rows"]), "slide %d compare" % i)
    allc = [c[0] for c in K.C]
    text = " ".join(json.dumps(s["items"]) + s["title"] + s["sub"] for s in S).lower()
    missing = [c for c in allc if c.lower() not in text]
    cov = 100.0 * (len(allc) - len(missing)) / len(allc)
    print("coverage (D11, by research label on a slide): %d of %d = %.1f percent; missing: %s" % (len(allc) - len(missing), len(allc), cov, missing))
    ana = {a["concept"] for a in ANALOGIES}
    nona = [c for c in allc if c not in ana]
    print("analogies (D4): %d of %d concepts carry one; without: %s" % (len(allc) - len(nona), len(allc), nona))
    if missing or nona: bad.append("a research concept is missing from the slides or has no analogy")
    if bad: raise SystemExit("REFUSED:\n  " + "\n  ".join(bad))
    return cov


SHA = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def manifest(N):
    setup = X.SETUP
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch07_deck_lib_v1_0_0", "needs": ["setup"],
                    "code": "\n".join(l for g in e["rows"] for l in g), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh namespace with ONLY the libraries and the setup, and the listing, as the page will run it
    for e in exs:
        ns = {}; exec(setup, ns); exec(e["code"], ns)
        for s in e["show"]:
            got = repr(eval(s["expression"], ns))
            if got != s["expected"]: raise SystemExit("REFUSED: example %s %s runs to %s on the page path, the recording says %s" % (e["id"], s["expression"], got, s["expected"]))
    lib = "08-tooling/sen0401_ch07_deck_lib_v1_0_0.py"; lib2 = "08-tooling/sen0401_ch07_script_lib_v1_0_0.py"
    return {"manifest": "chapter_code_ch07_v1_0_0", "chapter": 7, "deck": "SEN0401_Ch07_AuthorizationAuthentication_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the two library modules defined in the page",
            "library": {"module": "sen0401_ch07_deck_lib_v1_0_0", "file": lib, "sha256": SHA(os.path.join(ROOT, lib)), "import": "import sen0401_ch07_deck_lib_v1_0_0 as K",
                        "data_files": [{"module": "sen0401_ch07_script_lib_v1_0_0", "file": lib2, "sha256": SHA(os.path.join(ROOT, lib2)), "import": "import sen0401_ch07_script_lib_v1_0_0 as L"}]},
            "setup": {"code": setup}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 7: Authorization and Authentication", "sub": "SEN0401, third-edition deck standard D1-D12", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-23, task TK_Ch07_Deck_Build: the deck rebuilt to the deck standard D1-D12 from the chapter research, with its chapter-code manifest",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "concepts of the research ontology whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(DOUT, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch07", "page", "chapter_code_ch07_v1_0_0.json")
    old = json.load(open(mp))   # the committed manifest is read, never written: the code slides keep their order and names
    same = [(e["order"], e["name"], e["slide"], e["code"]) for e in m["examples"]] == [(e["order"], e["name"], e["slide"], e["code"]) for e in old["examples"]]
    if not same: raise SystemExit("REFUSED: the code slides differ from the committed manifest; a new manifest version would be needed")
    print("manifest not written; examples equal the committed manifest:", len(m["examples"]), "in slide order", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(DOUT, "sen0401_ch07_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 7"])
    mat = os.path.join(DOUT, "SEN0401_Ch07_AuthorizationAuthentication_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
