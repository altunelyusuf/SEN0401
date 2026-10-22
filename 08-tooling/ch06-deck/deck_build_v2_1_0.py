#!/usr/bin/env python3
"""deck_build v2.1.0 - the generator of the chapter 6 deck 2.1.0 (over deck_build_v2_1_0.py, kept as the earlier draft: code frames of one-line statements with a note under each, separate frames for card, divider and analogy text, so that the deck standard D1-D12 is met) - deck 2.0.0 (remedy of 2026-10-22, task TK_Remedy_Deck_Ch06_Build), a NEW file. It writes, from the chapter research and the
recorded executions, (1) deck_plan_v2_1_0.json, (2) the chapter-code manifest 03-materials/ch06/page/chapter_code_ch06_v1_1_0.json and, with --render, (3) the .pptx (drawn by
sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the chapter corpus (the 115 concepts of the research ontology and their short captions), the story module v1_2_0 (the four stories with their pictures), the recorded
executions examples_out_v2_1_0.json (made by examples_run_v2_1_0.py under Python 3.14), deck_concepts_v2_0_0.py (one everyday analogy per concept) and the resources slide of the
previous plan. Every number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the file is drawn:
no text box over 30 words, notes of at most 60 words, no code line over 62 characters with its prompt (a listing never wraps), every concept of the research on a slide with its analogy.
Usage: python3.14 deck_build_v2_1_0.py [--render]"""
__version__ = "2.1.0"
import ast, glob, importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_1_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.1.0", "2_1_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


C = load(os.path.join(TOOL, "sen0401_ch06_corpus_v1_0_0.py"), "corpus06")
ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch06_stories_v*.py")), key=vk)[-1], "stories06")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
NODE = {n[0]: n for n in C.NODES}
LAB = {n[0]: (n[1] or n[0]) for n in C.NODES}
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch06/assets/"
OLD = json.load(open(sorted(glob.glob(os.path.join(HERE, "deck_plan_v1_*.json")), key=vk)[-1]))

BRANCHES = [n[0] for n in C.NODES if n[2] == 1]
def kids(name): return [n[0] for n in C.NODES if n[3] == name]
def descendants(name): return [m for k in kids(name) for m in [k] + kids(k)]

S, ANALOGIES, FIRST_CODE = [], [], []
EST = lambda text, fs, width, k=0.0078: max(1, -(-int(len(text) * fs * k * 100) // int(width * 100)))   # lines a text needs: characters x font size x 0.0078 in, over the width


SHORT = {"TransactionIdea": "Idea of a transaction", "MarkerAndFlag": "Marker and flag", "ByteOrder": "Byte order", "RelativeTimelock": "Relative timelock", "SequenceReplacement": "Sequence replacement", "DustPolicy": "Dust policy", "MalleabilityProblems": "Malleability", "WitnessSerialization": "Witness layout", "SegregatedWitness": "Segwit", "WitnessIdea": "Idea of a witness"}
ALIAS = {"SerializedTransaction": "A Serialized Bitcoin Transaction", "MarkerByte": "Extended Marker and Flag", "InputCount": "Length of Transaction Input List",
         "ReplacementAttack": "Original sequence-based transaction replacement", "Bip125Signal": "Opt-in transaction replacement signaling",
         "Bip68Timelock": "Sequence as a consensus-enforced relative timelock", "UneconomicalOutput": "Uneconomical outputs and disallowed dust",
         "CircularDependency": "Circular Dependencies", "PsbtFormat": "PSBT", "SetupTransaction": "setup transaction", "PaymentChannel": "high-frequency transactions",
         "UtxoDatabase": "Utreexo", "WitnessStructure": "Witness Structure Serialization", "ContractProtocol": "trustless protocol", "Coinbase": "generation transaction"}

W = lambda t: len(re.findall(r"\S+", t))


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
SEGS = [("Version", 1.0), ("Marker Flag", 0.9), ("Inputs", 1.9), ("Outputs", 1.9), ("Witnesses", 1.9), ("Lock time", 1.0)]
HOT = {"TransactionAnatomy": "all", "VersionMarkerFlag": [0, 1], "Inputs": [2], "SequenceField": [2], "Outputs": [3], "Witnesses": [4], "LockTimeAndCoinbase": [5], "WeightAndFoundations": "all"}
SEGLABEL = {"SequenceField": {2: "Inputs: sequence"}, "WeightAndFoundations": {}}


def strip(branch, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = HOT[branch]
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": SEGLABEL.get(branch, {}).get(i, lab), "hot": hot == "all" or i in hot} for i, (lab, f) in enumerate(SEGS)]}


DIV_NOTES = {
    "TransactionAnatomy": "This part opens one real transaction. We read Alice's payment byte by byte and compare its two serializations. A story about the first transaction ever closes the part.",
    "VersionMarkerFlag": "The first six bytes of a transaction are not data about money. They tell a node which rules apply and whether a witness follows, so every later field is read correctly.",
    "Inputs": "Inputs name the coins a transaction spends, and they state no amount. We meet the compact count, the outpoint and its two byte orders, and the database of unspent coins.",
    "SequenceField": "One four-byte field has carried three meanings in fifteen years. We decode it against two proposals, BIP125 and BIP68, and see why bit 31 matters.",
    "Outputs": "Outputs hold the amounts and the locks. The part ends with a block that created 184 billion bitcoins and with the policy that keeps tiny outputs out of everyone's database.",
    "Witnesses": "A witness is the proof that a spender may spend. We see how proofs inside the input script made identifiers malleable, and how segregated witness repaired that as a soft fork.",
    "LockTimeAndCoinbase": "Two special cases of a transaction: one that may not be mined before a time, and one that creates new coins. The clock and the money supply both follow from simple rules.",
    "WeightAndFoundations": "The part closes with what a block is filled by, and with the hashes and rule sets that every figure of the chapter rests on. We recompute the weight 569 from the bytes.",
}


def divider(branch):
    groups = kids(branch); n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 3 else 11
    its = []
    for g in groups:
        mean, ana = K.L2[g]; pill = SHORT.get(g, LAB[g])
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12 if n <= 3 else 11, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
        ANALOGIES.append({"concept": LAB[g], "analogy": ana, "slide": len(S) + 1})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (branch, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12 if n <= 3 else 11, "items": its}, strip(branch)]
    ANALOGIES.append({"concept": LAB[branch], "analogy": K.L1[branch], "slide": len(S) + 1})
    return add("section", LAB[branch], K.L1[branch], items, DIV_NOTES[branch])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards
# ------------------------------------------------------------------------------------------------------------------------------------------------
def chunks(lst):
    n = len(lst); k = -(-n // 4); size = -(-n // k); return [lst[i:i + size] for i in range(0, n, size)]


def cards(branch, names, part, parts):
    n = len(names); cols = 2 if n == 4 else min(3, n); rows = -(-n // cols); bw = (9.0 - (cols - 1) * 0.16) / cols; fw = bw - 0.3
    avail = (3.5 - (rows - 1) * 0.14) / rows
    for fs in (11.5, 11, 10.5, 10):
        items, need = [], 0
        for nm in names:
            mean = NODE[nm][4][0]; mean = mean[0].upper() + mean[1:] + "."; ana = "Think of " + K.L3[nm] + "."; al = ("Also called: " + ALIAS[nm]) if nm in ALIAS else None
            hA = (EST(LAB[nm], fs + 1.5, fw, 0.0088) * (fs + 1.5) + EST(mean, fs, fw) * fs) * 1.22 / 72 + 0.06
            hB = EST(ana, fs, fw) * fs * 1.22 / 72 + 0.04
            hC = (EST(al, fs - 1.5, fw) * (fs - 1.5) * 1.22 / 72 + 0.04) if al else 0
            it = {"label": LAB[nm], "meaning": mean, "analogy": ana, "hA": round(hA, 3), "hB": round(hB, 3), "hC": round(hC, 3)}
            if al: it["alias"] = al
            items.append(it); need = max(need, 0.07 + hA + hB + hC + 0.1)
        if need <= avail: break
    else:
        raise SystemExit("REFUSED: cards %s need %.2f in, %.2f available" % (names, need, avail))
    for nm, it in zip(names, items):
        for k in ("meaning", "analogy"):
            if W(it[k]) > 30: raise SystemExit("REFUSED: card %s has a frame of over 30 words" % nm)
        if W(it["label"] + " " + it["meaning"]) > 30: raise SystemExit("REFUSED: card %s head frame over 30 words" % nm)
        ANALOGIES.append({"concept": LAB[nm], "analogy": K.L3[nm] + ".", "slide": len(S) + 1})
        if nm in ALIAS: ANALOGIES.append({"concept": ALIAS[nm], "analogy": K.L3[nm] + ".", "slide": len(S) + 1})
    suffix = " (%d of %d)" % (part, parts) if parts > 1 else ""
    title = "%s: concepts%s" % (LAB[branch], suffix)
    if len(title) > 40: title = "%s%s" % (LAB[branch], suffix)
    names_t = ", ".join(LAB[x] for x in names[:-1]) + " and " + LAB[names[-1]] if len(names) > 1 else LAB[names[0]]
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 6." % names_t
    if W(notes) > 60: notes = "These cards cover %d concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 6." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart, table or drawn diagram)
# ------------------------------------------------------------------------------------------------------------------------------------------------
LH = 10 * 1.3 / 72
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("194 bytes, every one named", "Alice's transaction, parsed from its hexadecimal text", "Every byte belongs to a named field, and the fields come in a fixed order",
             "The library parses Alice's transaction from the book into named fields and adds up their lengths. The seven groups add back to the 194 bytes of the serialized transaction, so no byte is unexplained."),
    "ex02": ("Two serializations, two identifiers", "Extended with the witness, legacy without it", "The txid hashes the legacy bytes only; the wtxid hashes everything",
             "The same payment is written twice. The legacy form leaves out marker, flag and witness, and its hash is the txid that explorers show. The extended form has its own hash, the wtxid."),
    "ex03": ("The first six bytes", "Version, marker and flag in Alice's transaction", "A zero marker where an input count would be tells old and new nodes apart",
             "Six bytes decide how everything after them is read. The version says which rules apply, and the zero marker with the one flag announces a witness. A legacy parser would read the zero as an empty input list."),
    "ex04": ("CompactSize: counting in few bytes", "The bytes a count takes grow with the count", "Small counts cost one byte; the first byte warns when a longer number follows",
             "Counts in a transaction use a variable-length integer. Up to 252 it is one byte; beyond that a first byte of fd, fe or ff says that two, four or eight more bytes follow."),
    "ex05": ("The outpoint, read both ways round", "Which coin an input spends", "An input states no amount; it names a coin by transaction and output number",
             "An input points at a coin by the txid of an earlier transaction and an output number. The bytes are stored in one order and printed in the reverse order, which is a classic source of mistakes."),
    "ex06": ("A spend updates the UTXO set", "Remove what is spent, add what is created", "Nodes keep only unspent outputs; the fee is whatever is left over",
             "A full node keeps a database of unspent outputs. Applying a transaction removes the coins its inputs name and adds the coins its outputs create. The difference in value is the fee."),
    "ex07": ("Four sequence values, three meanings", "Final, replaceable, and a relative timelock", "Bit 31 of the sequence field is the security bit of this chapter",
             "The same four bytes signal finality, opt-in replacement under BIP125 and a relative timelock under BIP68. Setting bit 31 switches the timelock off, which is why the third value shows none."),
    "ex08": ("BIP68: an hour as a sequence number", "How the 32 bits of the field are divided", "Disable flag, type flag and a 16-bit value share one field",
             "To demand an hour, the type flag is set and the value counts units of 512 seconds, so an hour rounds up to 4,096 seconds. Counted in blocks, thirty blocks after a coin confirms is the earliest spend."),
    "ex09": ("Amounts, change and the fee", "An output is an amount and a condition", "No field holds a balance or a fee; both are differences",
             "Outputs state amounts in satoshis. The input states none, so the spent coin's value comes from the record of that coin. What the outputs do not take is the fee that the miner collects."),
    "ex10": ("The 2010 overflow, in five lines", "How two huge outputs added up to a negative number", "Check each amount and the total: one check on the total was not enough",
             "In August 2010 a block carried two outputs of about 92 billion bitcoins each. Their sum wrapped around to a negative number, which passed the check on the total. Checking every output closes the hole."),
    "ex11": ("Dust limits by output type", "The smallest output a node will relay", "Dust is a policy about who pays for the UTXO set: everyone, for ever",
             "An output is dust when it costs more to spend than it is worth, at the relay fee. Segwit outputs are cheaper to spend, so their limit is lower. A data-carrier output can never be spent and is exempt."),
    "ex12": ("One spend, four identifiers", "Push encodings and third-party malleability", "A stranger could change the txid without changing the payment",
             "A small number can be pushed on the script stack in four ways. Each way is a different byte string, so the same payment gets four different legacy identifiers. This was the malleability that software could not ignore."),
    "ex13": ("Segwit: change the witness, keep the txid", "What the two identifiers cover", "What a hash covers decides what can safely be built on it",
             "After segregated witness the signature lives outside the txid. Replacing it leaves the txid unchanged, so chains of unconfirmed payments stay valid. The wtxid still covers the witness and changes."),
    "ex14": ("Lock time and the median time past", "Which clock a lock time is read against", "Lock time says not before; nothing in a transaction says not after",
             "Block timestamps are not monotonic, so a time lock is compared with the median of the last eleven. Values below 500 million are heights; larger ones are times. The median lags the highest timestamp."),
    "ex15": ("The subsidy, halving by halving", "New bitcoin created by each block", "The coinbase is the only transaction that creates bitcoin",
             "The subsidy starts at 50 bitcoin and is halved every 210,000 blocks by a right shift. It reaches zero after block 6,929,999, and the total ever issued stays just below 21 million."),
    "ex16": ("The coinbase and its maturity", "A null input, and 100 blocks of waiting", "Newly created coins cannot be spent until 100 blocks have passed",
             "A coinbase has one input that points at nothing. Its coins are locked for 100 blocks, so that a reorganisation cannot invalidate coins that were already spent. Block 9's coins were spendable by block 170."),
    "ex17": ("569: weight by field", "Where the weight of Alice's transaction comes from", "Weight is what a block is filled by, and witness bytes cost a quarter",
             "Each field weighs its bytes times four, except the marker, the flag and the witness, which weigh one. The sum is the 569 the book quotes, and dividing by four gives 143 virtual bytes."),
    "ex18": ("How a txid is made", "Double SHA-256 of the legacy bytes, reversed", "Identifiers are computed, never stored: anyone can recompute them",
             "A txid is not a field. It is the double SHA-256 of the legacy serialization, shown in reverse byte order. We recompute it from the bytes and it matches the library and the explorer."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    if ex == "ex01":
        g = val(ex, "dict(g)"); tot = val(ex, "sum(g.values())")
        return ([ch(list(g), list(g.values()), "bytes")], "bytes per field group (all %d)" % tot,
                "Outputs and the witness take the most bytes; version and lock time take four each.")
    if ex == "ex02":
        sz = val(ex, "sizes"); ids = val(ex, "ids")
        return ([tb([["Form", "Bytes", "Hash (16 hex digits)"], ["Extended", str(sz[0]), ids[0]], ["Legacy", str(sz[1]), ids[1]]], [0.85, 0.55, 1.85])],
                "the two forms of one payment", "The %d extra bytes are marker, flag and witness. The txid hashes the legacy form; the wtxid hashes the extended one." % (sz[0] - sz[1]))
    if ex == "ex03":
        hd = val(ex, "head"); v = val(ex, "version"); mf = val(ex, "(marker, flag)")
        return ([tb([["Bytes", "Field", "Value"], [hd[:8], "version", str(v)], [hd[8:10], "marker", str(mf[0])], [hd[10:12], "flag", str(mf[1])]], [1.1, 1.0, 1.15])],
                "the first six bytes, read", "A zero where a count is expected tells a node that the extended format, with a witness, follows.")
    if ex == "ex04":
        sz = val(ex, "sizes"); pf = val(ex, "prefix")
        return ([ch(["1", "252", "253", "65535", "65536", "2**32"], sz, "bytes")], "bytes taken by each count",
                "First bytes written: " + " ".join(pf) + ". The values fd, fe and ff announce longer numbers.")
    if ex == "ex05":
        a, b, ok, vo = val(ex, "stored[:16]"), val(ex, "shown[:16]"), val(ex, "check"), val(ex, "i0['vout']")
        return ([tb([["Form", "First 16 hex digits"], ["Stored in the input", a], ["Printed by explorers", b], ["Reversing back restores it", yn(ok)]], [1.65, 1.6])],
                "one outpoint, read both ways", "Input 0 spends output %d of the earlier transaction. The stored and printed forms are mirror images." % vo)
    if ex == "ex06":
        b, a, fee = val(ex, "before"), val(ex, "sorted(utxo.values())"), val(ex, "fee")
        return ([tb([["Step", "Coins", "Satoshis"], ["Before", str(len(b)), " + ".join(fmt(v) for v in b)], ["After", str(len(a)), " + ".join(fmt(v) for v in a)], ["Left over: fee", "-", fmt(fee)]], [1.0, 0.6, 1.65])],
                "the set of unspent outputs", "The fee of %s satoshis is no field; it is %s minus %s." % (fmt(fee), fmt(sum(b)), fmt(sum(a))))
    if ex == "ex07":
        rows = val(ex, "rows")
        t = [["Sequence", "Replaceable", "Timelock"]] + [[r[0], yn(r[1]), "none" if r[2] is None else "%d %s" % (r[2][1], r[2][0])] for r in rows]
        return ([tb(t, [1.2, 1.0, 1.05])], "four values decoded", "The first two are final or almost final; the third signals replacement; only the last carries a timelock.")
    if ex == "ex08":
        hx, rt, first, fl = val(ex, "hex(s)"), val(ex, "rt"), val(ex, "first"), val(ex, "[dis, typ, msk]")
        t = [["Quantity", "Result"], ["One hour", "%s = %s s" % (hx, fmt(rt[1]))], ["Earliest block", fmt(first)], ["Masks", ", ".join(fl)]]
        return ([tb(t, [0.95, 2.3])], "sequence values and BIP68 masks", "An hour rounds up to eight units of 512 seconds, which is 4,096 seconds.")
    if ex == "ex09":
        parts = val(ex, "parts"); funds = val(ex, "funds")
        return ([ch(["output 0", "output 1", "fee"], parts, "satoshis")], "satoshis in each output, and the fee",
                "The spent coin held %s satoshis; the outputs take %s and the remaining %s is the fee." % (fmt(funds), fmt(sum(parts[:2])), fmt(parts[2])))
    if ex == "ex10":
        tot, nv, fx = val(ex, "total"), val(ex, "naive_ok"), val(ex, "fixed_ok")
        t = [["Check", "Result"], ["Two outputs added", fmt(tot)], ["Old test: total in range", "%s: accepted" % nv if nv else "%s: refused" % nv], ["New test: each in range", "%s: accepted" % fx if fx else "%s: refused" % fx]]
        return ([tb(t, [1.75, 1.5])], "the arithmetic of block 74,638", "A negative total is below the limit, so only the per-output check catches it.")
    if ex == "ex11":
        lim = val(ex, "limits")
        return ([ch(["P2PKH", "P2WPKH", "P2TR", "RET"], lim, "satoshis")], "dust limit in satoshis, at 3,000 sat/kvB",
                "An output below its limit is not relayed. OP_RETURN outputs cannot be spent, so their limit is zero.")
    if ex == "ex12":
        sc, ids, d = val(ex, "list(enc.values())"), val(ex, "ids"), val(ex, "distinct")
        t = [["Encoding", "Script", "New txid"]] + [[k, s_, v] for (k, v), s_ in zip(ids.items(), sc)]
        return ([tb(t, [1.15, 0.9, 1.2], 9)], "four pushes of the number 2", "%d encodings give %d different identifiers for one payment." % (len(sc), d))
    if ex == "ex13":
        st, sw, ids = val(ex, "same_txid"), val(ex, "same_wtxid"), val(ex, "[a, b, c]")
        t = [["Identifier", "Before", "After"], ["txid", ids[0], ids[0]], ["wtxid", ids[1], ids[2]]]
        return ([tb(t, [0.85, 1.2, 1.2], 9)], "12 hex digits of each identifier", "Only the wtxid notices the new witness; the txid, and everything built on it, stays valid.")
    if ex == "ex14":
        of, mo, kinds = val(ex, "offsets"), val(ex, "mtp_offset"), val(ex, "kinds")
        return ([ch(["b%d" % (i + 1) for i in range(len(of))], of, "seconds after the first")], "block times, seconds after 1675556500",
                "The median of the eleven is %s s, %s s below the highest. Lock time kinds: %s." % (fmt(mo), fmt(max(of) - mo), ", ".join(kinds)))
    if ex == "ex15":
        sb, last, tot = val(ex, "subs"), val(ex, "last"), val(ex, "total")
        return ([ch(["%d" % i for i in range(len(sb))], sb, "bitcoin per block")], "subsidy in bitcoin, by halving number",
                "The last subsidy is paid at block %s; the total ever issued is %s bitcoin." % (fmt(last), "{:,.4f}".format(tot)))
    if ex == "ex16":
        fl, ag = val(ex, "flags"), val(ex, "ages")
        t = [["Spend at block", "Age", "Spendable?"]] + [[str(a), str(b), yn(c)] for a, b, c in ag]
        return ([tb(t, [1.3, 0.8, 1.15])], "a coin created at block 9", "is_coinbase is %s for the null input and %s for Alice's transaction." % (fl[0], fl[1]))
    if ex == "ex17":
        Wd, tot, vb = val(ex, "dict(W)"), val(ex, "total"), val(ex, "vb")
        return ([ch(list(Wd), list(Wd.values()), "weight units")], "weight units per field group (total %d)" % tot, "Total weight %d; divided by four and rounded up that is %d virtual bytes." % (tot, vb))
    if ex == "ex18":
        ln, sh, same = val(ex, "len(leg)"), val(ex, "shown[:16]"), val(ex, "same")
        return ([tb([["Step", "Result"], ["Legacy bytes", str(ln)], ["Double SHA-256, reversed", sh], ["Equals the library's txid", yn(same)]], [1.65, 1.6])],
                "from the legacy bytes to the txid", "The reversed digest %s the library's txid." % ("equals" if same else "differs from"))
    raise KeyError(ex)


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
            if len(">>> " + r[0]) > 60: raise SystemExit("REFUSED: %s has a code line of %d characters (a listing must not wrap)" % (ex, len(">>> " + r[0])))
            if len(r[1]) > 58: raise SystemExit("REFUSED: %s output line of %d characters" % (ex, len(r[1])))
        if W(g["note"]) < 8 or W(g["note"]) > 20: raise SystemExit("REFUSED: note %d of %s has %d words (8 to 20 wanted)" % (k + 1, ex, W(g["note"])))
        nrows = len(rows) + sum(1 for r in rows if r[1] != "")
        h = round(nrows * lh + 0.16, 3); nh = round(EST(g["note"], 10.5, W_ - 0.3, 0.0072) * 0.18 + 0.05, 3)
        gl.append({"rows": rows, "note": g["note"], "y": round(y, 3), "h": h, "ny": round(y + h + 0.03, 3), "nh": nh}); y += h + 0.03 + nh + 0.09
    capy = round(y - 0.04, 3)
    if capy + 0.2 > 5.0: raise SystemExit("REFUSED: %s needs the left column to end at %.2f in" % (ex, capy + 0.2))
    # right column: the result picture and its reading
    RX, RW = 6.25, 3.25
    items0, cap_res, reading = visual(ex, RX, RW, 2.0, 2.0)
    if W(reading) > 30: raise SystemExit("REFUSED: reading of %s has %d words" % (ex, W(reading)))
    lab = "Result: " + cap_res; lab_h = round(EST(lab, 11, RW, 0.0085) * 0.2 + 0.04, 3)
    rh = round(EST(reading, 11.5, RW, 0.0082) * 0.2 + 0.06, 3); ry = round(4.97 - rh, 3)
    vy = round(1.45 + lab_h + 0.05, 3); vh = round(ry - 0.1 - vy, 3)
    items, _, _ = visual(ex, RX, RW, vy, vh)
    cap = ("run under Python %s - ALICE, PREV, FIRST and tx as set up on slide %d" % (PY, FIRST_CODE[0])) if FIRST_CODE else ("run under Python %s - ALICE, PREV, FIRST and tx come from the chapter setup" % PY)
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
# stories
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORY_BEATS = {
    "FirstTransaction": ["WHAT: Satoshi Nakamoto sent Hal Finney 10 bitcoins, the first transaction ever to spend an output.",
                         "WHY: Finney had started the software the day before and wanted to test the network with a real payment.",
                         "HOW: One input points at the coinbase of block 9; two outputs pay 10 BTC to Finney and 40 BTC back.",
                         "SO WHAT: Legacy format, no marker, no flag, no witness: every field this chapter reads was already there."],
    "PizzaDay": ["WHAT: Laszlo Hanyecz paid 10,000 bitcoins for two pizzas that a forum user ordered for him.",
                 "WHY: He wanted to show that bitcoin could buy something real; his forum offer began four days earlier.",
                 "HOW: The payment confirmed in block 57,043: 131 inputs, one output of 10,000 BTC, a fee of 0.99 BTC.",
                 "SO WHAT: A wallet that gathered many 50 BTC rewards must list every one of them as an input."],
    "ValueOverflow": ["WHAT: Block 74,638 held a transaction with two outputs of 92 billion bitcoins each, 184 billion in all.",
                      "WHY: Added as 64-bit integers the amounts wrapped to a small negative number, which passed the check.",
                      "HOW: Jeff Garzik reported it within two hours; Satoshi patched it in about five; the chain recovered at block 74,691.",
                      "SO WHAT: Bitcoin Core still cites the bug, CVE-2010-5139, in tx_check.cpp."],
    "GoxMalleability": ["WHAT: Mt. Gox halted withdrawals and blamed transaction malleability for missing bitcoins.",
                        "WHY: A stranger can re-encode an input script, change the txid and make a payment look as if it failed.",
                        "HOW: Decker and Wattenhofer of ETH Zurich recorded a year of traffic: only 1,811 BTC were hit before the press release.",
                        "SO WHAT: Segregated witness took the input script out of the txid in 2017."],
}


STORY_SUB = {"FirstTransaction": "The first transaction ever to spend an output", "PizzaDay": "The most famous purchase ever made with bitcoin",
             "ValueOverflow": "A bug that created money out of thin air", "GoxMalleability": "An exchange blames the protocol, and researchers check"}


def story_slide(sid):
    st = STORY[sid]; beats = STORY_BEATS[sid]
    for b in beats:
        if W(b) > 30: raise SystemExit("REFUSED: beat of %s has %d words" % (sid, W(b)))
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    cut = lambda s: s[:150].rsplit(",", 1)[0] if len(s) > 150 else s
    items = [{"t": "img", "path": ASSETS + st["photo"], "x": 0.5, "y": 1.4, "w": 2.6, "h": 2.55, "cap": st["credit"]},
             {"t": "beats", "x": 3.4, "y": 1.4, "w": 6.1, "h": 2.7, "fs": 11.5, "items": beats},
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
def build():
    S.clear(); ANALOGIES.clear(); FIRST_CODE.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    # 1 title
    add("title", "Chapter 6: Transactions", "One real transaction, 194 bytes, read field by field, with every number recomputed",
        [{"t": "img", "path": ASSETS + "mbc3_0601.png", "x": 6.9, "y": 0.35, "w": 2.6, "h": 1.75},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Figure: a byte map of a transaction, Antonopoulos and Harding, Mastering Bitcoin 3e, CC BY-SA 4.0. Python %s, no Bitcoin Core node." % PY}],
        "This deck reads one real Bitcoin transaction, Alice's payment to Bob from the book, byte by byte. Every number was computed from those bytes with the chapter's own Python library, and no Bitcoin Core node was available where it was built.")
    # 2 agenda placeholder, 3 questions, 4 map
    add("content", "Today's route", "", [], "", "Eight parts, one real transaction, and a summary you can check")
    add("content", "The questions this chapter answers", "Its own competency questions; we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "What does a Bitcoin transaction ask full nodes to do?", "How is a transaction serialized in the extended and the legacy format?",
            "What do the version, marker and flag tell a node?", "Which three meanings has the sequence field carried?",
            "Why did witnesses in the input script make the identifier malleable?", "How are weight and vbytes computed, and does 569 reproduce from the bytes?",
            "Who creates new bitcoins, and when can they be spent?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, eight branches", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 4, "fs": 12.5, "subfs": 10.5, "accent": [2],
          "items": [{"label": LAB[b], "sub": "%d concepts" % len(descendants(b))} for b in BRANCHES]}],
        "The chapter has eight branches and %d concepts. Each branch gets a divider, concept cards with everyday comparisons, code that runs, and some branches a true story. The deck follows the order in which the bytes of a transaction are written." % sum(len(descendants(b)) for b in BRANCHES),
        "Eight branches; every slide today lives on this map")
    # branches
    plan = {
        "TransactionAnatomy": (["ex01", "ex02"], {"ex02": "FirstTransaction"}),
        "VersionMarkerFlag": (["ex03"], {}),
        "Inputs": (["ex04", "ex05", "ex06"], {"ex06": "PizzaDay"}),
        "SequenceField": (["ex07", "ex08"], {}),
        "Outputs": (["ex09", "ex10", "ex11"], {"ex10": "ValueOverflow"}),
        "Witnesses": (["ex12", "ex13"], {"ex13": "GoxMalleability"}),
        "LockTimeAndCoinbase": (["ex14", "ex15", "ex16"], {}),
        "WeightAndFoundations": (["ex17", "ex18"], {}),
    }
    for b in BRANCHES:
        exs, stories = plan[b]
        divider(b)
        l3 = [m for k in kids(b) for m in kids(k)]
        cks = chunks(l3); order = []
        for i in range(max(len(cks), len(exs))):
            if i < len(cks): order.append(("c", i))
            if i < len(exs): order.append(("x", exs[i]))
        for kind, v in order:
            if kind == "c": cards(b, cks[v], v + 1, len(cks))
            else:
                code_slide(EX[v])
                if v in stories: story_slide(stories[v])
        if b == "Witnesses":
            add("content", "Hard fork or soft fork?", "Why segregated witness could be activated without splitting the network",
                [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                  "left": {"head": "A hard fork loosens the rules", "rows": ["Blocks that old nodes reject become valid.", "Every node must upgrade, or the chain splits.", "Like a new road standard that old cars cannot use."]},
                  "right": {"head": "A soft fork tightens the rules", "rows": ["New nodes reject more; they accept nothing new.", "Old nodes still follow the chain and accept its blocks.", "Like a stricter speed limit that old cars can still obey."]}}],
                "Segregated witness was a soft fork. Old nodes saw the new outputs as anyone-can-spend scripts and accepted the blocks, while upgraded nodes enforced the witness rules. That is why it could be activated without a split.",
                "A soft fork can only restrict; old nodes keep accepting the blocks")
    # summary, resources, closing
    add("content", "The chapter in five lines", "One line per part, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A transaction asks strangers to update their ledgers: inputs point, witnesses prove, outputs assign.",
            "The sequence field has meant three things, and the lock time is read against the median of eleven blocks.",
            "An output is an amount and a condition; the fee is a difference, and dust is a policy about everyone's database.",
            "Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork.",
            "The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by."]}],
        "These five lines are the deck in miniature, one for each group of parts. A line that feels unproven should send you back to its code slide, because every figure in it was computed there. The chapter code tab of the course page lets you rerun all eighteen examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", "Checked 2026-10-22; every entry is a live link in this file", [res],
        "Everything here is free to read, and every link was opened on the date in the subtitle. A good exercise is to take any confirmed transaction from the explorer and run the chapter code on its hexadecimal. The course page for chapter 6 carries the full resource list.",
        "Parse any transaction yourself and match the explorer's identifier and weight")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What a transaction asks of full nodes", "What sequence and lock time permit",
            "Why identifiers were malleable, and the fix", "How 569 is computed; who creates bitcoin"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 6 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    # the agenda (slide 2): contiguous ranges from slide 3, every part starting at its divider
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Eight parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 3, "fs": 11.5, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has eight parts that follow the order of the bytes of a transaction. Four true stories and eighteen code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every slide can be rerun."
    return N


def refuse(N):
    """the deck standard held at build time: D2 (30 words per text box), D7 (60 words of notes), D1 (numbering is the renderer's), D11 (coverage)"""
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
                    box(v["label"] + " " + v["meaning"], "slide %d card head" % i); box(v["analogy"], "slide %d card analogy" % i); box(v.get("alias", ""), "slide %d card alias" % i)
            elif t == "groups":
                for v in it["items"]: box(v["pill"], "slide %d pill" % i); box(v["meaning"], "slide %d meaning" % i); box(v["analogy"], "slide %d analogy" % i)
            elif t == "codeblocks":
                for g in it["groups"]:
                    box(" ".join(r[0] + " " + r[1] for r in g["rows"]), "slide %d code frame" % i); box(g["note"], "slide %d note" % i)
            else:
                for v in it.get("items", []):
                    if isinstance(v, str): box(v, "slide %d %s" % (i, t))
                    elif isinstance(v, dict): box(" ".join(str(x) for x in v.values()), "slide %d %s" % (i, t))
            for side in ("left", "right"):
                if side in it: box(" ".join(it[side]["rows"]), "slide %d compare" % i)
    text = " ".join(json.dumps(s["items"]) + s["title"] + s["sub"] for s in S).lower()
    allc = [LAB[n[0]] for n in C.NODES]
    missing = [c for c in allc if c.lower() not in text]
    cov = 100.0 * (len(allc) - len(missing)) / len(allc)
    print("coverage (D11, by concept label on a slide): %d of %d = %.1f percent; missing: %s" % (len(allc) - len(missing), len(allc), cov, missing))
    ana = {a["concept"] for a in ANALOGIES}
    nona = [c for c in allc if c not in ana]
    print("analogies (D4): %d of %d concepts carry one; without: %s" % (len(allc) - len(nona), len(allc), nona))
    if bad: raise SystemExit("REFUSED:\n  " + "\n  ".join(bad))
    return cov


def manifest(N):
    ev = os.path.join(TOOL, "ch06-evidence"); rd = lambda n: open(os.path.join(ev, n), encoding="utf-8", errors="replace").read().strip()
    prev_rec = json.load(open(os.path.join(ev, "mempool_tx_4ac5418026798669_v1_0_0.json"), encoding="utf-8"))
    data = {"ALICE": rd("tx_alice_46620030_v1_0_0.hex"), "PREV": rd("tx_alice_prev_4ac54180_v1_0_0.hex"), "FIRST": rd("tx_first_f4184fc5_v1_0_0.hex"),
            "PREV_REC": {"vout": [{"value": o["value"]} for o in prev_rec["vout"]]}}
    setup = "\n".join(["# setup: the saved transactions of the chapter (hexadecimal) and one saved explorer record; the page runs this before every example",
                       "ALICE = %r" % data["ALICE"], "PREV = %r" % data["PREV"], "FIRST = %r" % data["FIRST"], "PREV_REC = %r" % data["PREV_REC"], "tx = parse_tx(ALICE)"])
    lib = "sen0401_ch06_tx_lib_v1_0_0"
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": lib, "needs": ["setup"],
                    "code": "\n".join(l for g in e["rows"] for l in g), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh namespace with ONLY the library, the setup and the listing, as the page will run it
    sys.path.insert(0, TOOL); L = importlib.import_module(lib)
    for e in exs:
        ns = {k: getattr(L, k) for k in dir(L) if not k.startswith("__")}; exec(setup, ns); exec(e["code"], ns)
        for s in e["show"]:
            got = repr(eval(s["expression"], ns))
            if got != s["expected"]: raise SystemExit("REFUSED: example %s %s runs to %s on the page path, the recording says %s" % (e["id"], s["expression"], got, s["expected"]))
    return {"manifest": "chapter_code_ch06_v1_1_0", "chapter": 6, "deck": "SEN0401_Ch06_Transactions_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": lib, "file": "08-tooling/%s.py" % lib, "import": "from %s import *" % lib}, "setup": {"code": setup, "data": data}, "examples": exs}


def visual_kind(ex):
    return {"ex01": "native chart", "ex02": "table", "ex03": "table", "ex04": "native chart", "ex05": "table", "ex06": "table", "ex07": "table", "ex08": "table", "ex09": "native chart",
            "ex10": "table", "ex11": "native chart", "ex12": "table", "ex13": "table", "ex14": "native chart", "ex15": "native chart", "ex16": "table", "ex17": "native chart", "ex18": "table"}[ex]


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 6: Transactions", "sub": "SEN0401, third-edition remedy deck", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-22, remedy of the owner's 17:27 message: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "concepts of the research ontology whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch06", "page", "chapter_code_ch06_v1_1_0.json")
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch06_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 6"])
    mat = os.path.join(ROOT, "03-materials", "ch06", "SEN0401_Ch06_Transactions_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
