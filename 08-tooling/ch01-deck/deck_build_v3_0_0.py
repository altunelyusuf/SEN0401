#!/usr/bin/env python3
"""deck_build v3.0.0 (chapter 1, Introduction) - the generator of the chapter 1 deck 3.0.0 (task TK_Ch01_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch08-deck/deck_build_v2_0_0.py. It writes,
from the chapter research and the recorded executions, (1) deck_plan_v3_0_0.json, (2) the chapter-code manifest 03-materials/ch01/page/chapter_code_ch01_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the story module sen0401_ch01_stories_v1_6_0.py (real names, dates, links, credits), the recorded executions examples_out_v3_0_0.json (made by examples_run_v3_0_0.py under
Python 3.14), deck_concepts_v3_0_0.py (the 33 key concepts of the research, each with a meaning and one everyday analogy), the chapter library sen0401_ch01_lib_v1_0_0.py and the visual
items of the earlier plan deck_plan_v2_11_0.json (reused where they were sound). Every number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is
held as refusals here BEFORE the file is drawn: no text box over 30 words, notes of at most 60 words, no code line over 60 characters with its prompt (a listing never wraps), every key concept of
the research on a slide with its analogy, every story with who, what, when, where, why and how.
Usage: python3.14 deck_build_v3_0_0.py [--render]"""
__version__ = "3.0.0"
import ast, glob, hashlib, importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v3_0_0 as X
import deck_concepts_v3_0_0 as K
VER, VER_US = "3.0.0", "3_0_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(os.path.join(TOOL, "sen0401_ch01_stories_v1_6_0.py"), "stories01")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch01/assets/"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v2_11_0.json")))

S, ANALOGIES = [], []
EST = lambda text, fs, width, k=0.0078: max(1, -(-int(len(text) * fs * k * 100) // int(width * 100)))   # lines a text needs: characters x font size x 0.0078 in, over the width
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


def old_item(n, t, k=0):
    """the k-th item of type t on slide n of the earlier plan (deck 2.11.0), copied"""
    return json.loads(json.dumps([i for i in OLD["slides"][n - 1]["items"] if i.get("t") == t][k]))


# ------------------------------------------------------------------------------------------------------------------------------------------------
# dividers
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEGS = [(K.PART_SHORT[p], 1.0) for p in K.PARTS]


def strip(part, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = K.PARTS.index(part)
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": i == hot} for i, (lab, f) in enumerate(SEGS)]}


DIV_NOTES = {
    "Origins": "Bitcoin did not appear from nothing. This part reads the first block, follows the first payment and meets the cryptographers whose parts Nakamoto combined.",
    "Money": "Money is a ledger. We see old forms of money, count in satoshis, run the supply schedule and watch a price being discovered by trades, never declared.",
    "Network": "No bank stands in the middle. Every node checks the same rules, proof of work makes history costly to forge, and fees and confirmations settle payments.",
    "Wallets": "A wallet holds keys, not coins. This part sorts wallets by platform, by how much of the network they check, and by who holds the keys and the backup.",
    "FirstUse": "We follow a first payment from an empty wallet. First how to get bitcoin, then what an address and an invoice are, and finally how a wallet sends with change.",
    "Foundations": "Two old ideas, proof of work and agreement without trust, meet in Bitcoin. Payment channels keep many payments off the chain, and four adjectives name its nature.",
}


def divider(part):
    groups = K.L2[part]; n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 3 else 11
    its = []
    for pill, mean, ana in groups:
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (part, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12, "items": its}, strip(part)]
    return add("section", K.PART_LABEL[part], K.L1[part], items, DIV_NOTES[part])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards: the key concepts of the research
# ------------------------------------------------------------------------------------------------------------------------------------------------
def chunks(lst):
    n = len(lst)
    if n == 0: return []
    k = -(-n // 4); size = -(-n // k); return [lst[i:i + size] for i in range(0, n, size)]


def cards(part, names, num, parts, extra=None):
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
    suffix = " (%d of %d)" % (num, parts) if parts > 1 else ""
    title = "%s: key concepts%s" % (K.PART_LABEL[part], suffix)
    if len(title) > 44: title = "%s: concepts%s" % (K.PART_LABEL[part], suffix)
    names_t = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 1." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 1." % (len(names), K.PART_LABEL[part])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}] + (extra or []), notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("The headline inside block zero", "Reading the first block's script as bytes", "The first block carries its own date: a newspaper headline",
             "The first block keeps a short script. Eight bytes of pushes come first, then 69 bytes of text. Decode them and you read The Times of 3 January 2009 inside the chain itself."),
    "ex02": ("A bitcoin counted in satoshis", "The unit and its smallest piece", "Money here is counting, and the units are exact",
             "A bitcoin divides into 100 million satoshis. We multiply 0.001 by that number and get exactly 100,000. Amounts in the protocol are whole satoshis, never fractions."),
    "ex03": ("The subsidy at five block heights", "New bitcoin per block, halved every 210,000 blocks", "Every halving cuts new issuance in half",
             "The block subsidy starts at fifty bitcoin. The code shifts it right once per era. Five heights give the staircase from 2009 to 2024, each step exactly half of the one before."),
    "ex04": ("The 21 million cap is a sum", "Issuance by era, added up by the code", "Scarcity is arithmetic that every node can re-run",
             "Each era issues its subsidy over 210,000 blocks. Adding 33 eras gives 20,999,999.9769 bitcoin. The chart shows the running total approaching 21 million without reaching it."),
    "ex05": ("No one sets the price: trades do", "A price is a ratio; a day's figure is a weighted average", "Everyone who trades sets the price a little",
             "Each trade has its own price, found by dividing dollars by bitcoin. A volume-weighted average gives one fair figure for the day. The three trades are illustrative, not market data."),
    "ex06": ("The Pizza Day coins, repriced", "10,000 bitcoin at six documented moments", "From 41 dollars to 854 million: price discovery never stopped",
             "The pizzas cost 41 dollars of bitcoin in May 2010. The same coins at five later milestones draw the chart; the last point is the price fetched on 6 October 2026. Each gridline is ten times more."),
    "ex07": ("Hard to find, easy to check", "A toy proof of work with hexadecimal zeros", "Finding takes thousands of guesses; checking takes one hash",
             "The search tries numbers until the hash starts with zeros. Each extra zero makes it about sixteen times longer on average. Anyone checks the winner with a single hash."),
    "ex08": ("A double spend is refused", "One shared ledger, one rule, no referee", "The second spend of a coin is refused everywhere",
             "A ledger remembers which coins are spent. Alice pays Bob with coin c1 and it is accepted. When she offers the same coin to Carol, the rule refuses it. No bank decides."),
    "ex09": ("A chain that notices tampering", "Each block hashes its text with the block before", "Change one old block and every later link fails",
             "Each block's hash covers its own text and the hash of the block before. Changing one word in block two makes the check stop there, so nothing after it can be trusted."),
    "ex10": ("What the outputs leave over is the fee", "A transaction has no fee field; the difference is the fee", "The fee is the part of the coin nobody was given",
             "A coin of 100,000 satoshis pays 20,000 to Bob and returns 75,000 as change. The 5,000 left over goes to the miner who includes the payment. Fees are implied, never written."),
    "ex11": ("A recovery phrase becomes a seed", "Key stretching repeats a hash, 2048 times in BIP 39", "Slow on purpose: every guess costs the full 2048 rounds",
             "A recovery phrase of twelve words is stretched by repeating a keyed hash. With 1, 10 or 2048 rounds the seeds look unrelated. A thief guessing phrases pays all 2048 rounds per guess."),
    "ex12": ("An address is a hash with a checksum", "How the address of the first block is built", "A mistyped address is caught by its checksum",
             "Block 0 pays to a 20-byte key hash behind a version byte. The checksum is the first four bytes of a double hash. Together they make 25 bytes, written in Base58 as a 34-character address."),
    "ex13": ("An invoice is a link with an amount", "A payment request in the form of BIP 21", "A QR code is only this text, drawn as dots",
             "A payment request packs an address, an amount, a label and a message into one text. The wallet splits it into named fields and turns the amount into whole satoshis."),
    "ex14": ("Sending: coins in, payment and change out", "A wallet spends whole coins and sends the rest back", "You never cut a coin: you spend it and get change",
             "The wallet owes 60,000 satoshis plus a 1,500 fee. It picks the smallest coin that covers both, 80,000, and sends 18,500 back to itself as change."),
    "ex15": ("Two transactions, any number of payments", "A payment channel opens and closes on the chain", "A channel pays off from the third payment on",
             "On the chain every payment is a transaction. A channel needs one to open and one to close, whatever happens between. One payment alone costs more; a thousand save 998 transactions."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name, **kw: dict({"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                               "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}, **kw)
    if ex == "ex01":
        sz, hx, text, n = val(ex, "sizes"), val(ex, "head.hex()"), val(ex, "text"), val(ex, "len(raw)")
        return ([tb([["Part of the script", "Bytes"], ["Pushes (hex %s)" % hx[:8] + "...", str(sz[0])], ["The headline text", str(sz[1])], ["Whole script", str(n)]], [2.25, 1.0])],
                "the %d bytes of block 0's script" % n, "It reads: %s." % text)
    if ex == "ex02":
        sats, units = val(ex, "sats"), val(ex, "units")
        return ([tb([["Unit", "In satoshis"], ["1 bitcoin", fmt(units[0])], ["1 millibitcoin (0.001)", fmt(units[1])], ["1 satoshi", fmt(units[2])]], [1.85, 1.4])],
                "the same value in three units", "0.001 bitcoin is exactly %s satoshis, so every amount is a whole number." % fmt(sats))
    if ex == "ex03":
        subs = val(ex, "subs"); yrs = [h[1] for h in ST.HALVINGS[:5]]
        return ([ch(yrs, subs, "subsidy", dlFmt="General")], "subsidy in bitcoin, by halving year", "Each era pays half of the one before: %s, and since April 2024 %s." % (", ".join("%g" % s for s in subs[:4]), "%g" % subs[4]))
    if ex == "ex04":
        cap, cum = val(ex, "cap"), val(ex, "[sum(eras[:k + 1]) // COIN for k in range(8)]")
        return ([{"t": "chart", "ctype": "line", "x": x, "y": y, "w": w, "h": h, "labels": ["E%d" % (k + 1) for k in range(8)], "series": [{"name": "issued", "data": [c / 1e6 for c in cum]}],
                  "dataLabels": True, "dlFs": 8, "dlFmt": "0.0", "min": 0, "max": 22}], "bitcoin issued after each era, in millions", "The total creeps toward 21 million; the cap is %s bitcoin." % cap)
    if ex == "ex05":
        tr, pr, avg = val(ex, "trades"), val(ex, "prices"), val(ex, "avg")
        return ([tb([["Trade", "Dollars per bitcoin"]] + [["Trade %d (%s BTC)" % (i + 1, t[0]), fmt(int(p))] for i, (t, p) in enumerate(zip(tr, pr))] + [["Day average, by volume", "{:,.2f}".format(avg)]], [1.85, 1.4])],
                "dollars paid per bitcoin", "Each trade sets its own price; the volume-weighted day average is %s dollars." % "{:,.2f}".format(avg))
    if ex == "ex06":
        d, v, f = val(ex, "list(val.keys())"), val(ex, "list(val.values())"), val(ex, "round(val['2026-10'] / val['2010-05'])")
        return ([{"t": "chart", "ctype": "line", "x": x, "y": y, "w": w, "h": h, "log": True, "min": 10, "max": 10000000000, "fmt": "$#,##0", "title": "Value of 10,000 BTC in dollars (log axis)", "labels": d, "series": [{"name": "USD value", "data": [float(a) for a in v]}],
                  "dataLabels": True, "dlFs": 7.5, "dlFmt": "[>=1000000]$#,##0,,\"M\";[>=1000]$#,##0,\"K\";$#,##0"}], "value of the 10,000 BTC, in dollars (log axis)",
                "The same coins grew by a factor of %s, from $%d to $%sM." % (fmt(f), v[0], fmt(v[-1] // 10 ** 6)))
    if ex == "ex07":
        t = val(ex, "tries")
        return ([ch(["1 zero", "2 zeros", "3 zeros", "4 zeros"], t, "guesses", log=True, min=1, max=100000, fmt="#,##0", dlFmt="#,##0", title="Guesses needed (log axis)")], "guesses needed (log axis)", "Each extra zero makes the search about sixteen times longer on average; checking stays one hash.")
    if ex == "ex08":
        a, b, o = val(ex, "first"), val(ex, "second"), val(ex, "book.owner")
        return ([tb([["Step", "Ledger answer"], ["1. Alice pays Bob", a.split(":")[0]], ["2. Alice pays Carol", b.split(":")[0]], ["Owner of coin c1", o["c1"]]], [1.9, 1.35])],
                "two payments of the same coin", "The first spend is recorded; the same coin offered again is refused by the rule alone.")
    if ex == "ex09":
        be, af, ok = val(ex, "before"), val(ex, "after"), val(ex, "[verify(blocks[:k]) == k for k in (1, 2, 3)]")
        aft = ["holds" if ok[0] else "broken"] + ["broken" if (ok[k - 1] is False and ok[k - 2] is True) else ("holds" if ok[k - 1] else "not trusted") for k in (2, 3)]
        return ([tb([["Block", "Before", "After the change"]] + [["Block %d" % (k + 1), "holds", aft[k]] for k in range(3)], [0.95, 1.0, 1.3])],
                "does each block's link still hold?", "Changing block two breaks its link, so block two and everything after it are no longer trusted.")
    if ex == "ex10":
        fee, sh, ins, outs = val(ex, "fee"), val(ex, "share"), val(ex, "sum(inputs)"), val(ex, "outputs")
        return ([ch(["Coin in", "To Bob", "Change", "Fee"], [ins, outs[0], outs[1], fee], "satoshis", dlFmt="#,##0")], "where the 100,000 satoshis go", "The fee is %s satoshis, %.1f percent of the coin; no output carries it." % (fmt(fee), sh))
    if ex == "ex11":
        r, sd = val(ex, "rounds"), val(ex, "seeds")
        return ([tb([["Rounds", "Seed starts with"]] + [[str(a), b] for a, b in zip(r, sd)], [1.0, 2.25])], "the same twelve words, three round counts", "More rounds give an unrelated seed; wallets use %d, so every guess costs %d rounds." % (r[-1], r[-1]))
    if ex == "ex12":
        ad, ck, n, kh = val(ex, "address"), val(ex, "check.hex()"), val(ex, "len(payload + check)"), val(ex, "payload[1:].hex()")
        return ([tb([["Part", "Bytes", "Hex"], ["Version", "1", "00"], ["Key hash", "20", kh[:8] + "..."], ["Checksum", "4", ck], ["Together", str(n), "base58: %s..." % ad[:6]]], [0.95, 0.6, 1.7])],
                "the address of block 0, in parts", "The %d bytes are written in Base58 as the %d-character address %s." % (n, len(ad), ad))
    if ex == "ex13":
        rq, sats = val(ex, "req"), val(ex, "sats")
        a = rq["address"]
        return ([tb([["Field", "Value"], ["address", a[:8] + "..." + a[-4:]], ["amount", rq["amount"]], ["label", rq["label"]], ["message", rq["message"]]], [0.95, 2.3])],
                "the fields of one payment link", "%s bitcoin is %s satoshis, the amount the wallet shows the payer." % (rq["amount"], fmt(sats)))
    if ex == "ex14":
        pk, pay, fee, chg = val(ex, "pick"), val(ex, "pay"), val(ex, "fee"), val(ex, "change")
        return ([tb([["Item", "Satoshis"], ["Coin picked", fmt(pk)], ["Payment", fmt(pay)], ["Fee", fmt(fee)], ["Change back", fmt(chg)]], [1.75, 1.5])],
                "one coin in, three amounts out", "A coin is spent whole, like a banknote, and the change returns as a new output.")
    if ex == "ex15":
        on, sv = val(ex, "onchain"), val(ex, "saved")
        return ([tb([["Payments", "On chain", "Channel", "Saved"]] + [[fmt(a), fmt(a), "2", ("%d" % b)] for a, b in zip(on, sv)], [0.8, 0.8, 0.85, 0.8])],
                "transactions on the chain, per payment count", "Opening and closing cost two transactions however many payments follow; a single payment alone does not pay off.")
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex03", "ex04", "ex06", "ex07", "ex10") else "table"


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
    cap = "run under Python %s - the chapter library of the page supplies the helper functions" % PY
    blocks = {"t": "codeblocks", "x": X_, "w": W_, "fs": fs, "nfs": 10.5, "groups": gl, "cap": cap, "capy": capy}
    res_label = {"t": "text", "x": RX, "y": 1.45, "w": RW, "h": lab_h, "body": lab, "fs": 11, "font": "B", "bold": True, "color": "mute"}
    if items[0]["t"] == "table": ry = round(min(ry, vy + len(items[0]["rows"]) * items[0]["rowH"] + 0.3), 3)       # under the table, not at the foot of the slide
    read = {"t": "text", "x": RX, "y": ry, "w": RW, "h": rh, "body": reading, "fs": 11.5, "font": "B", "italic": True, "color": "ink"}
    tail = " It is example %d in the chapter code tab of the course page." % int(ex[2:])
    if W(notes) > 60: raise SystemExit("REFUSED: notes of %s have %d words" % (ex, W(notes)))
    num = add("content", title, sub_, [blocks, res_label] + items + [read], notes + tail if W(notes + tail) <= 60 else notes, take)
    e["slide"] = num; e["rows"] = [[r[0] for r in g["rows"]] for g in gl]
    return num


# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories (5N1K: who, what, when, where, why, how; a real picture; a live link)
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORIES = {
    "GenesisHeadline": {"sub": "Recorded: 3 January 2009", "img": "genesis_hexdump.png", "box": (3.4, 2.55), "who": "Satoshi Nakamoto", "where": "block 0 of the chain", "when": "2009-01-03",
                        "linkText": "Genesis block coinbase (tx)",
                        "beats": ["WHAT: The first Bitcoin block carries a newspaper headline: The Times, 3 January 2009, Chancellor on brink of second bailout for banks.",
                                  "WHY: The headline proves the block was not made earlier, and it records the banking crisis that Bitcoin answers.",
                                  "HOW: Satoshi typed the text into the coinbase script of block 0, the 69 bytes the next code slide reads."],
                        "notes": "A true story, dated 3 January 2009. Satoshi Nakamoto, the pseudonymous creator of Bitcoin, mined block 0 and wrote the headline of that morning's Times into it. The block is a timestamp and a manifesto."},
    "FirstTransaction": {"sub": "Satoshi Nakamoto, and the cryptographer who ran the code", "img": "photo_hal_finney_1972.jpg", "box": (3.4, 2.55), "who": "Satoshi to Hal Finney", "where": "block 170 of the chain", "when": "2009-01-12",
                         "linkText": "Satoshi to Finney, block 170 (tx)",
                         "beats": ["WHAT: Nine days after block 0, Satoshi Nakamoto sent 10 bitcoin to Hal Finney in block 170, the first payment between two people.",
                                   "WHY: Finney had answered the white paper with curiosity and had built the first reusable proof-of-work system years before.",
                                   "HOW: Finney ran the software and wrote 'Running bitcoin'; the coins reached him directly, with no bank in between."],
                         "notes": "A true story, dated 12 January 2009. Hal Finney, who had worked on PGP, was the first person besides Satoshi to run Bitcoin and the first to be paid. One peer paid another, directly."},
    "CypherpunkLineage": {"sub": "Every part existed before Bitcoin combined them", "img": "photo_david_chaum_2018.jpg", "box": (3.4, 2.6), "who": "Chaum, Back, Dai, Szabo", "where": "papers, mailing lists", "when": "2008-10-31",
                          "linkText": "Bitcoin white paper (PDF)",
                          "beats": ["WHAT: David Chaum, Adam Back, Wei Dai and Nick Szabo each built a part of digital money between 1982 and 1998.",
                                    "WHY: Their systems failed or stayed unbuilt, because none could agree on one history without a trusted leader.",
                                    "HOW: Nakamoto's white paper of 31 October 2008 cites them and adds proof of work as the voting weight of an open network."],
                          "notes": "A true story, dated 31 October 2008. Chaum's company DigiCash went bankrupt; Back's Hashcash priced email with work; b-money and bit gold were never built. Nakamoto added the missing piece and combined them."},
    "StoneMoney": {"sub": "Documented in 1903; the free ebook edition came in 2024", "img": "photo_rai_stone.jpg", "box": (3.4, 2.55), "who": "W. H. Furness III", "where": "Yap, Micronesia", "when": "1903",
                   "linkText": "Furness: The Island of Stone Money (book)",
                   "beats": ["WHAT: On Yap, wealth was held in limestone discs called rai, up to four metres wide, that never moved when they changed owner.",
                             "WHY: What changed was the shared memory of who owned each stone, so the stone worked as a public ledger.",
                             "HOW: Anthropologist William Henry Furness III described it after visiting in 1903; a stone that sank at sea was still traded."],
                   "notes": "A true story, documented in 1903. On the island of Yap the stones stayed where they lay and the community remembered who owned them. Money is a ledger, and Bitcoin makes the shared memory digital."},
    "MoneyEvolution": {"sub": "From grain ledgers to pure fiat money, 3000 BCE to 1971", "img": "photo_cma_stater.jpg", "box": (3.9, 2.3), "who": "Nixon and ledger-keepers", "where": "Mesopotamia to the U.S.", "when": "1971-08-15",
                       "linkText": "The History of Money (museum exhibit)",
                       "beats": ["WHAT: On 15 August 1971 President Richard Nixon cut the dollar's last tie to gold, leaving pure fiat money.",
                                 "WHY: Grain ledgers, Lydian coins, paper notes and bank balances are all ledgers; they differ in who keeps them.",
                                 "HOW: Cards and online banking made money digital as entries in private ledgers; Bitcoin makes the ledger public."],
                       "notes": "A true story, dated 15 August 1971. Money kept changing form, from Mesopotamian grain entries to Lydian coins to bank balances. Cryptocurrency is the next step: a ledger that no single institution keeps."},
    "OnlinePayments": {"sub": "The dot-com boom digitised paying, not cash", "img": "photo_paypal_logo.png", "box": (3.0, 2.55), "who": "Levchin, Thiel and Musk", "where": "Palo Alto and San Jose", "when": "2002-07-08",
                       "linkText": "PayPal (encyclopedia article)",
                       "beats": ["WHAT: On 8 July 2002 eBay agreed to buy PayPal for 1.5 billion dollars, ending the dot-com race to pay online.",
                                 "WHY: Online payment was solved only as accounts on one company's private ledger; the internet still had no cash.",
                                 "HOW: Confinity (Levchin, Thiel, 1998) and X.com (Musk, 1999) merged in 2000; Beenz and Flooz died in the 2001 crash."],
                       "notes": "A true story, dated 8 July 2002. The web could sell before it could pay. PayPal solved it by adding a middleman, and the pure digital currencies of the boom failed."},
    "WhenMoneyStops": {"sub": "Ukraine, February 2022: a state turns to an open payment network", "img": "photo_fedorov_portrait.jpg", "box": (3.4, 2.6), "who": "Mykhailo Fedorov", "where": "Kyiv, Ukraine", "when": "2022-02-26",
                       "linkText": "CNBC: Ukraine's crypto donations (news)",
                       "beats": ["WHAT: On 26 February 2022 Ukraine's government posted crypto donation addresses and, with an aid group, raised 54.7 million dollars in about a week.",
                                 "WHY: With war at the capital, ordinary rails were too slow; open digital money kept working where banks, cards or cash stopped.",
                                 "HOW: Fedorov's ministry of digital transformation published the addresses, and CNBC reported the total on 3 March 2022."],
                       "notes": "A true story, dated 26 February 2022. Mykhailo Fedorov, Ukraine's minister of digital transformation, published donation addresses. The next slide lists four more documented cases from 2007 to 2018."},
    "PizzaDay": {"sub": "22 May 2010: the day a price began to exist", "img": "photo_papa_johns_jacksonville.jpg", "box": (3.4, 2.6), "who": "Laszlo Hanyecz", "where": "Jacksonville, Florida", "when": "2010-05-22",
                 "linkText": "Guinness: first Bitcoin purchase (record)",
                 "beats": ["WHAT: On 22 May 2010 Laszlo Hanyecz paid 10,000 bitcoin for two Papa John's pizzas, the first known commercial purchase in bitcoin.",
                           "WHY: Until then nobody knew what a bitcoin was worth; this purchase is the day a floating price began to exist.",
                           "HOW: He offered the coins on the bitcointalk forum, and student Jeremy Sturdivant ordered the pizzas for delivery to Jacksonville."],
                 "notes": "A true story, dated 22 May 2010. Laszlo Hanyecz offered 10,000 bitcoin for two pizzas on a forum and Jeremy Sturdivant ordered them. Price is discovered the first time someone actually pays."},
    "MtGox": {"sub": "Tokyo, February 2014: balances on a website, keys elsewhere", "img": "photo_mtgox_logo.png", "box": (3.4, 2.55), "who": "Mark Karpeles, Mt. Gox", "where": "Tokyo District Court", "when": "2014-02-28",
              "linkText": "Mt.Gox filing statement, TechCrunch (news)",
              "beats": ["WHAT: On 28 February 2014 Mt. Gox of Tokyo filed for bankruptcy and admitted that about 850,000 bitcoin were gone.",
                        "WHY: Customers had balances on a website, but the keys, and so the coins, were in someone else's hands all along.",
                        "HOW: The exchange of chief executive Mark Karpeles filed at the Tokyo District Court; creditors were still being repaid a decade later."],
              "notes": "A true story, dated 28 February 2014. Mt. Gox was once the largest bitcoin exchange. Whoever holds the keys holds the coins, exchanges included. This is the cost of a custodial wallet."},
}


def story_slide(sid):
    sc = STORIES[sid]; st = STORY[sid]
    for b in sc["beats"]:
        if W(b) > 30: raise SystemExit("REFUSED: beat of %s has %d words" % (sid, W(b)))
    if len(sc["who"]) > 25 or len(sc["where"]) > 23 or len(sc["when"]) > 17 or len(sc["linkText"]) > 43: raise SystemExit("REFUSED: fact row of %s would be cut" % sid)
    if W(sc["notes"]) > 60: raise SystemExit("REFUSED: notes of %s over 60 words" % sid)
    bw, bh = sc["box"]; cr = st["credit"]
    items = [{"t": "img", "path": ASSETS + sc["img"], "x": 0.5, "y": 1.4, "w": bw, "h": bh, "cap": cr},
             {"t": "beats", "x": 4.1 if bw <= 3.5 else 0.5 + bw + 0.3, "y": 1.4, "w": 5.4 if bw <= 3.5 else 9.5 - (0.5 + bw + 0.3), "h": 2.7, "fs": 11.5, "items": sc["beats"]},
             {"t": "factrow", "x": 0.5, "y": 4.5, "w": 9.0, "who": sc["who"], "where": sc["where"], "when": sc["when"], "link": st["link"], "linkText": sc["linkText"]}]
    return add("content", st["title"], sc["sub"], items, sc["notes"])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
PLAN = {   # per part: the order of the slides after the divider
    "Origins": ["cards:0", "story:GenesisHeadline", "ex01", "story:FirstTransaction", "story:CypherpunkLineage", "timeline"],
    "Money": ["cards:0", "story:StoneMoney", "story:MoneyEvolution", "kinds", "story:OnlinePayments", "story:WhenMoneyStops", "cases", "ex02", "ex03", "ex04", "ex05", "story:PizzaDay", "ex06"],
    "Network": ["net", "cards:0", "ex07", "mining", "copyviz", "dsolve", "ex08", "ex09", "cards:1", "ex10"],
    "Wallets": ["tree", "cards:0", "cards:1", "cards:2", "keyhouse", "keys", "story:MtGox", "cards:3", "ex11"],
    "FirstUse": ["cards:0", "alice", "ex12", "ex13", "cards:1", "ex14"],
    "Foundations": ["twoproblems", "pipeline", "cards:0", "ex15", "kind"],
}
PART_KEYS = {p: [k for k, v in K.K3.items() if v[0] == p] for p in K.PARTS}
PART_CHUNKS = {p: chunks(PART_KEYS[p]) if p != "Network" else [PART_KEYS[p][:3], PART_KEYS[p][3:]] for p in K.PARTS}
EXN = {e["id"]: e for e in X.EXAMPLES}


def misc(kind, part):
    if kind == "timeline":
        return add("content", "Four near misses, one combination", "Each part existed before Bitcoin joined them",
                   [old_item(9, "timeline"), {"t": "bullets", "x": 0.5, "y": 3.85, "w": 9.0, "h": 0.95, "fs": 13, "items": ["DigiCash went bankrupt; b-money and bit gold were never built.", "Agreement without a leader was the missing piece."]}],
                   "Chaum's ecash of 1982, Back's Hashcash of 1997, and the b-money and bit gold of 1998 each solved a piece. Nakamoto's paper of 2008 combined them with proof of work as the vote. The genesis block ran in 2009.",
                   "The pieces were old; the combination was new")
    if kind == "kinds":
        return add("content", "Traditional, digital, crypto: side by side", "The chapter's one table: same uses, different ledgers", [dict(old_item(13, "table"), y=1.5, rowH=0.55)],
                   "Read down a column to see one kind of money, and across a row to see which property changes. Who keeps the ledger is the row that matters most in this course.", "Same uses, different ledgers: that difference is this course")
    if kind == "cases":
        CASES = [("Kenya", "2007", "photo_mpesa_agent.jpg", "Fiona Graham / WorldRemit, CC BY-SA 2.0"), ("Cyprus", "2013", "photo_laiki_bank.jpg", "Martin Addison, CC BY-SA 2.0"),
                 ("Greece", "2015", "photo_greece_atm.jpg", "Norbert Nagel, CC BY-SA 3.0"), ("Venezuela", "2018", "photo_bolivar_note.jpg", "Rjcastillo, CC BY-SA 4.0"),
                 ("Ukraine", "2022", "photo_fedorov.jpg", "U.S. Embassy Kyiv, public domain")]
        old = {c["place"]: c for c in old_item(16, "cases")["items"]}
        imgs = [{"t": "img", "path": ASSETS + f, "x": round(0.5 + i * 1.825, 3), "y": 1.4, "w": 1.7, "h": 1.05, "cap": "%s: %s" % (pl, cr)} for i, (pl, yr, f, cr) in enumerate(CASES)]
        row = lambda pl: ["%s %s" % (pl, old[pl]["year"]), old[pl]["link"], old[pl]["text"]]
        links = {"t": "links", "x": 0.5, "y": 3.0, "w": 9.0, "h": 1.95, "fs": 10, "groups": [{"head": "Banks, cards or cash stopped serving people", "rows": [row("Kenya"), row("Cyprus"), row("Greece")]},
                                                                                                {"head": "A currency or a state failed", "rows": [row("Venezuela"), row("Ukraine")]}]}
        return add("content", "When the money in your hand stops working", "Five documented cases, five links; no hypotheticals", imgs + [links],
                   "Kenya 2007, Cyprus 2013, Greece 2015, Venezuela 2018 and Ukraine 2022. In each case banks, cards or cash stopped serving people. Each line links to its source.",
                   "Crisis or war, banked or not: the need is documented")
    if kind == "net":
        return add("content", "A bank in the middle against peers", "Decentralisation is an architecture, not a slogan", [old_item(26, "net")],
                   "On the left one ledger-keeper sees everything and everyone depends on it. On the right every node checks every rule. Remove one node and the network goes on.", "Remove any one node and the network still agrees")
    if kind == "mining":
        fl = old_item(29, "flow"); fl["y"] = 1.5; fl["h"] = 1.15
        bl = {"t": "bullets", "x": 0.5, "y": 3.05, "w": 5.6, "h": 1.7, "fs": 14, "items": ["The subsidy follows the halving chart", "Cheating costs more than it could win", "Chapter 12 opens the mechanism"]}
        im = old_item(29, "img"); im["y"] = 3.0; im["h"] = 1.45; im["cap"] = "from the owner's 2025 deck"
        return add("content", "Mining pays for honesty", "New coin and fees reward the work that secures the chain", [fl, bl, im],
                   "Transactions wait, miners spend energy on proof of work, a block is found about every ten minutes, and the finder earns subsidy plus fees. Cheating costs more than it could win.", "Security is bought with energy and paid in bitcoin")
    if kind == "copyviz":
        return add("content", "Why digital money had to wait", "The copy problem: a digital coin is a file",
                   [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.6, "h": 2.9, "fs": 11.5, "items": ["Make money digital and it becomes a file", "Files copy perfectly, so coins would too", "Both copies get spent: the double-spend", "Only a trusted central ledger could stop it"]}, old_item(17, "copyviz")],
                   "A digital coin is only a file, and files copy perfectly. Both copies could be spent. For decades only a trusted central ledger could stop that, so digital money meant bank money.", "A file can be copied; a coin must not be")
    if kind == "dsolve":
        return add("content", "The double-spend, solved in public", "One shared ledger, one agreed order, no referee",
                   [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.1, "h": 2.9, "fs": 11.5, "items": ["Every payment is broadcast to every node", "Nodes agree on one order for all payments", "The first spend of a coin enters the block", "The second is refused by every node"]}, old_item(18, "dsolve")],
                   "Every payment is broadcast and the nodes agree on one order. The first spend of a coin enters the block, and every node refuses the second. The next code slide runs that rule.", "Agreement on order is what removes the referee")
    if kind == "tree":
        it = old_item(31, "tree")
        return add("content", "The wallet branch, mapped", "Four questions about any wallet: platform, node, keys, backup", [it],
                   "A wallet is classified by its platform, by how much of the network it checks, by who holds the keys, and by how it is backed up. Every leaf has a card in this part.", "Four questions place any wallet on this map")
    if kind == "keyhouse":
        return add("content", "Your key is your deed", "With a house the key opens and the registry proves; in Bitcoin the key does both",
                   [old_item(32, "keyhouse"), {"t": "bullets", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12.5, "items": ["Bitcoin's trick: a signature proves you hold the key while the key stays secret"]}],
                   "Access to bitcoin is controlled by private keys, like very long PINs. With a house, the key opens the door and a registry proves the owner. In Bitcoin the key is both, so it must prove without being shown.",
                   "Prove you hold the key; never reveal it")
    if kind == "keys":
        cm = old_item(33, "compare"); ch_ = old_item(33, "chips"); cm["h"] = 2.0; ch_["items"] = ["desktop", "mobile", "web", "hardware"]
        return add("content", "Whoever holds the keys holds the coins", "The one wallet decision that matters most", [cm, ch_],
                   "With full control you keep the keys, sign yourself and carry the backup. With third-party control a service keeps the keys, which is convenient, and you trust its honesty and uptime. Every wallet type can be either.",
                   "Custody is the first security decision you make")
    if kind == "alice":
        return add("content", "Alice's first bitcoin, step by step", "The chapter's running story begins",
                   [{"t": "flow", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.15, "fs": 12.5, "steps": [{"label": "Install a wallet", "sub": "keys made on her phone"}, {"label": "First address", "sub": "shared as text or QR"}, {"label": "Acquire bitcoin", "sub": "buy, earn, or exchange"}, {"label": "Confirmations", "sub": "the network accepts it"}]},
                    {"t": "bullets", "x": 0.5, "y": 3.0, "w": 9.0, "h": 1.7, "fs": 14, "items": ["The wallet writes down a recovery code first", "An address is shared; no account is opened anywhere", "Each confirmation makes the payment harder to reverse"]}],
                   "Alice installs a wallet, which makes her keys and a recovery code. She shares an address, acquires her first bitcoin, and waits for confirmations. The next slides build each step.", "Four steps from an empty phone to a first payment")
    if kind == "twoproblems":
        a = old_item(38, "card", 0); b = old_item(38, "card", 1)
        return add("content", "Two solved problems, one new system", "1997 and 1982 meet in 2008", [a, b],
                   "Hashcash of 1997 makes sending cost computation. The Byzantine Generals' problem of 1982 asks how parties that cannot trust each other agree. Proof of work with the longest valid chain is Bitcoin's practical answer.", "Neither idea was new; their combination was")
    if kind == "pipeline":
        fl = old_item(39, "flow"); bl = old_item(39, "bullets")
        return add("content", "From keys to the chain", "The pipeline the rest of the course walks", [fl, bl],
                   "Keys make addresses, addresses receive transactions, transactions are gathered into blocks, and blocks are added by mining. Each stage trusts only what it can verify. Later chapters open each box.", "This pipeline is the course syllabus in one row")
    if kind == "kind":
        it = [old_item(42, "text", 0), old_item(42, "chips", 0), old_item(42, "text", 1), old_item(42, "chips", 1)]
        return add("content", "What kind of thing is Bitcoin?", "Its stated characteristics, and the architecture behind them", it,
                   "The chapter gives two answers. Bitcoin is virtual, borderless, decentralized and robust, and it is built from a peer-to-peer protocol, a public journal and a consensus rule set. Each adjective is engineered.", "Each adjective is engineered, not advertised")
    raise KeyError(kind)


def build():
    S.clear(); ANALOGIES.clear()
    add("title", "Chapter 1: Introduction", "What Bitcoin is, what it is made of, and why every part of it exists",
        [{"t": "img", "path": ASSETS + "c1s24_protocol.png", "x": 6.2, "y": 0.3, "w": 3.4, "h": 1.95},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: gold coin on circuit traces, from the owner's 2025 Chapter 1 deck. Python %s; every result on a slide was computed, not typed." % PY}],
        "This deck introduces Bitcoin through true stories, the chapter's key concepts with everyday comparisons, and fifteen short programs. Every number on a result picture was computed with the chapter's own Python library.")
    add("content", "Today's route", "", [], "", "Six parts, fifteen examples, nine true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "Where did Bitcoin come from, and what did it combine?", "What is the unit of its money, and who decides how much exists?",
            "Who sets the price, and how does a double-spend get refused?", "What do the kinds of wallet differ in, and who controls the keys?",
            "What are an address and an invoice, and how does a wallet send with change?", "What can payment channels do that the chain alone cannot?"]}],
        "These six questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all six has understood the chapter.")
    tr = old_item(5, "tree"); tr["y"] = 1.5; tr["h"] = 3.4
    add("content", "One chapter, six branches", "The concept map the whole deck hangs on", [tr],
        "Chapter 1 says that Bitcoin is a collection of concepts and technologies that form the basis of a digital money ecosystem. The six branches are money, network, wallet, usage, foundations and nature. This deck regroups them into six parts.",
        "Six branches; every slide today lives on this map")
    for part in K.PARTS:
        divider(part)
        cks = PART_CHUNKS[part]
        for step in PLAN[part]:
            if step.startswith("cards:"):
                i = int(step.split(":")[1])
                ex_ = [{"t": "route", "x": 0.5, "y": 2.8, "w": 9.0, "h": 1.7, "hops": ["Alice", "Bob", "Carol", "Dave"], "cap": "Alice pays Dave through three channels; the chain is untouched"}] if part == "Foundations" else None
                cards(part, cks[i], i + 1, len(cks), ex_)
            elif step.startswith("story:"): story_slide(step.split(":")[1])
            elif step.startswith("ex"): code_slide(EXN[step])
            else: misc(step, part)
    add("content", "The chapter in six lines", "One line per part, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.45, "fs": 12.5, "items": [
            "Origins: a dated headline sits in block 0, and the first payment went from person to person.",
            "Money is a ledger; the cap of 21 million is arithmetic, and the price is discovered by trades.",
            "The network has no bank: every node checks every rule, and proof of work makes history costly.",
            "A wallet holds keys, not coins; whoever holds the keys holds the coins, and the code restores them.",
            "A first payment needs an address or invoice, whole coins, change, and a fee for the miner.",
            "Foundations: two old ideas joined, and payment channels that keep many payments off the chain."]}],
        "Six lines, one per part. If any line still feels like a claim rather than a fact, go back to the slide that carries its receipt. The course page for chapter 1 has the full text and the question bank.",
        "If a line feels unproven, its code slide carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch. A good start is the white paper, nine pages, and then the 3Blue1Brown video. The block explorers let you look up the first block and the pizza payment yourself.",
        "Read the white paper, then look up block 0 yourself")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "Where Bitcoin came from", "Why supply is capped and price discovered",
            "How a double spend is refused", "Who controls the keys; how a payment works"]}],
        "Four claims, each carried by a program that ran on a slide of this deck. The course page for chapter 1 has every word behind them, the stories with their sources, and the question bank.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N - 3)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Six parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 3, "fs": 11.0, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has six parts that follow the order of the chapter. Nine true stories and fifteen code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
    return N


RES_SUB = "Opened on 2026-10-25; every entry is a live link in this file"


def norm(t):
    t = re.sub(r"\([^)]*\)", " ", t.lower()); t = re.sub(r"[^a-z0-9]+", " ", t).split()
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in t)


def refuse(N):
    """the deck standard held at build time: D2 (30 words per text box), D7 (60 words of notes), D4/D11 (the key concepts)"""
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
                if side in it and "rows" in it[side]: box(" ".join(it[side]["rows"]), "slide %d compare" % i)
            if t == "card": box(it["body"], "slide %d card body" % i)
    text = norm(" ".join(json.dumps(s["items"], ensure_ascii=False) + " " + s["title"] + " " + s["sub"] for s in S))
    allc = list(K.K3)
    missing = [c for c in allc if norm(c) not in text]
    cov = 100.0 * (len(allc) - len(missing)) / len(allc)
    print("coverage (D11, by key concept label on a slide): %d of %d = %.1f percent; missing: %s" % (len(allc) - len(missing), len(allc), cov, missing))
    ana = {a["concept"] for a in ANALOGIES}
    nona = [c for c in allc if c not in ana]
    print("analogies (D4): %d of %d key concepts carry one; without: %s" % (len(allc) - len(nona), len(allc), nona))
    if bad: raise SystemExit("REFUSED:\n  " + "\n  ".join(bad))
    if missing or nona: raise SystemExit("REFUSED: key concepts missing or without analogy")
    return cov


LIBMOD = "sen0401_ch01_lib_v1_0_0"


def manifest(N):
    setup = "# setup: the chapter library of the page (helper functions, the saved block-0 script and the documented prices); the page runs this before every example\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": e["branch"], "library": LIBMOD, "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    bad_first = [e["id"] for e in exs if re.match(r"^(\w*Error|Traceback|Stopped after)", e["show"][0]["expected"])]
    if bad_first: raise SystemExit("REFUSED: first output line starts with an error name: %s" % bad_first)
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY the library module (as in the page), the setup and the listing
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch01_")
    shutil.copy(os.path.join(TOOL, LIBMOD + ".py"), tmp)
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
        print("page path (library module only) under %s: %d examples reproduce the recorded values" % (py, len(exs)))
    shutil.rmtree(tmp, ignore_errors=True)
    lp = os.path.join(TOOL, LIBMOD + ".py")
    return {"manifest": "chapter_code_ch01_v1_0_0", "chapter": 1, "deck": "SEN0401_Ch01_Introduction_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": LIBMOD, "file": "08-tooling/%s.py" % LIBMOD, "sha256": hashlib.sha256(open(lp, "rb").read()).hexdigest(), "import": "from %s import *" % LIBMOD},
            "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 1: Introduction", "sub": "SEN0401, third-edition deck 3.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch01_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, stories by 5N1K, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch01", "page", "chapter_code_ch01_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch01_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "deck_chart_logaxis_v1_0_0.py"), out])
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 1"])
    mat = os.path.join(ROOT, "03-materials", "ch01", "SEN0401_Ch01_Introduction_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
