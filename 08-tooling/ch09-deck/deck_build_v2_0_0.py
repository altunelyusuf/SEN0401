#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 9, Transaction Fees) - the generator of the chapter 9 deck 2.0.0 (task TK_Ch09_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch08-deck/deck_build_v2_0_0.py.
It writes, from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch09/page/chapter_code_ch09_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the chapter corpus (sen0401_ch09_corpus_v1_0_1.py: parts and groups), the story module v1_2_0 (four stories with pictures), the recorded executions examples_out_v2_0_0.json (made by
examples_run_v2_0_0.py under Python 3.14), deck_concepts_v2_0_0.py (the key concepts of the research, each with a meaning and one everyday analogy) and the resources slide of the previous plan.
Every number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the file is drawn: no text box over 30 words, notes of at most
60 words, no code line over 60 characters with its prompt (a listing never wraps), every key concept of the research on a slide with its analogy.
Usage: python3.14 deck_build_v2_0_0.py [--render]"""
__version__ = "2.0.0"
import ast, glob, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_0_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.0.0", "2_0_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
WHEEL = "03-materials/ch09/assets/sen0401_ch09_lib-1.0.2-py3-none-any.whl"
LIBMOD = "sen0401_ch09_lib_v1_0_1"


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


C = load(os.path.join(TOOL, "sen0401_ch09_corpus_v1_0_1.py"), "corpus09")
ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch09_stories_v*.py")), key=vk)[-1], "stories09")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
LAB = {n[0]: (n[1] or n[0]) for n in C.NODES}
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch09/assets/"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v1_1_0.json")))

BRANCHES = [n[0] for n in C.NODES if n[2] == 1]
def kids(name): return [n[0] for n in C.NODES if n[3] == name]

S, ANALOGIES, FIRST_CODE = [], [], []
EST = lambda text, fs, width, k=0.0078: max(1, -(-int(len(text) * fs * k * 100) // int(width * 100)))   # lines a text needs: characters x font size x 0.0078 in, over the width
W = lambda t: len(re.findall(r"\S+", t))
BR_SHORT = {"WhoPaysTheFee": "Who pays", "FeesAndFeeRates": "Rates", "FeeEstimation": "Estimates", "ReplaceByFee": "RBF", "ChildPaysForParent": "CPFP", "PinningAndAnchors": "Pinning",
            "FeeSnipingAndIncentives": "Sniping"}


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
SEGS = [(BR_SHORT[b], 1.0) for b in BRANCHES]


def strip(branch, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = SEGS.index((BR_SHORT[branch], 1.0))
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": i == hot} for i, (lab, f) in enumerate(SEGS)]}


DIV_NOTES = {
    "WhoPaysTheFee": "A transaction has no fee field. The fee is what the inputs hold and the outputs do not claim, so the spender pays it and only the spender can change it. This part shows how to see that, and what goes wrong when change is forgotten.",
    "FeesAndFeeRates": "Miners are paid by the space a payment takes, not by its value. This part measures size, weight and virtual size, turns a fee into a rate, and meets the floors that nodes, wallets and dust rules set.",
    "FeeEstimation": "A wallet must guess a rate that will confirm in time. We see how the estimator learns from blocks, where its answers stop, and how two real blocks show a market that moves by a factor of five hundred.",
    "ReplaceByFee": "A payment that waits too long can be replaced by a copy that pays more. We run the signal, the rules a replacement must meet, the default that changed, and the hazards of replacing.",
    "ChildPaysForParent": "When the parent cannot be changed, a child can pay for it. We measure the package rate, see why nodes now relay packages, and meet the cluster mempool that replaced the old chain limits.",
    "PinningAndAnchors": "A large child can make a parent costly to replace, and a pre-signed payment cannot guess a future fee. This part runs the carve-out, the TRUC limits and the pay-to-anchor output that answer both.",
    "FeeSnipingAndIncentives": "A block pays a subsidy and fees, and the mix changes. When fees dominate, a miner may gain by re-mining a block. We compute the odds and see how wallets defend with the lock time.",
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
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 9." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 9." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("A fee is a difference, not a field", "Parsing a real transaction from its raw bytes", "Nothing in the transaction states the fee: it is inputs minus outputs",
             "A transaction lists its inputs and its outputs, and nothing else. The miner's fee is whatever the inputs hold and the outputs do not claim. We parse the raw bytes ourselves and find 1,900,000,000 satoshis left over, with no field to name them."),
    "ex02": ("Forgetting the change", "A 20 coin input, a 1 coin output and no change output", "A safety limit protects the spender from paying nearly everything as fee",
             "If a wallet forgets the change output, the difference becomes a gigantic fee. The node refuses the payment with max-fee-exceeded. Mined with the limit lifted, the miner's reward equals the subsidy plus that fee, which shows where the money went."),
    "ex03": ("Only the spender can raise the fee", "Editing an amount after signing", "The signature covers the amounts, so nobody else can add to the fee",
             "We cut the first output of a signed payment by 5,000 satoshis. The node rejects the copy because the signature no longer fits. So the fee belongs to the spender; anyone else must pay in a second transaction, which is the idea of child pays for parent."),
    "ex04": ("Size, weight and virtual size", "Three measures of one payment", "Fees are charged per virtual byte, which is the weight over four",
             "One payment has 113 bytes without witness data and 222 bytes in all. Its weight is 561 units, because witness bytes count one each and the other bytes four. Its virtual size is 141, the weight over four rounded up. Fees and block space use this unit."),
    "ex05": ("A fee rate and its units", "Satoshis per virtual byte, or coins per thousand bytes", "Mixing the units changes the fee by a factor of a hundred thousand",
             "The rate is the fee over the virtual size: 282 over 141 gives 2 satoshis per byte. Some tools speak in coins per thousand bytes, so 0.0000657 means 6.57 satoshis per byte. Two spellings of ten satoshis per byte give the same fee, and a wrong factor gives an absurd one."),
    "ex06": ("Space in a block is limited", "The block weight limit and a real block", "A full block makes fee rates compete",
             "The consensus limit is four million units of weight per block. Block 840,000 weighs 3,993,281, which is 99.83 percent of it. When blocks are full, payments must bid for room, and the fee rate is the bid."),
    "ex07": ("The minimum relay fee", "Why 14 satoshis were not enough for 141 bytes", "A fee below the floor is not relayed, however valid the payment",
             "A node relays only payments above its floor, here a tenth of a satoshi per byte. For 141 bytes that is 14.1 satoshis, so 8 and 14 are refused and 15 is accepted. The floor protects nodes from spam, and it is policy, not consensus."),
    "ex08": ("Dust and the wallet's floor", "Outputs too small to be worth spending", "Wallets keep stricter floors than nodes; dust is a floor on outputs",
             "An output is dust when spending it would cost more than it holds. The limit is three satoshis for each byte of the output plus its spending input, 294 for the common segwit key. The wallet in this run also refuses rates below one satoshi per byte."),
    "ex09": ("An estimate needs history", "A new node cannot yet say what a fee should be", "The estimator answers only from blocks it has seen",
             "A node without history answers with an error: insufficient data. After 120 rounds of test traffic it can estimate, here about 1.2 satoshis per byte at every target. The estimate is a summary of what past blocks confirmed."),
    "ex10": ("How far the estimator can see", "A target of 144 blocks answered with 60", "The estimator cannot see further than its data; the modes differ in caution",
             "Asked for a target of 144 blocks, the node answers with the 60 blocks it can see. The default mode equals the economical mode at every target tried. The conservative mode is more cautious and answers differently at 144, so choose the mode that fits your risk."),
    "ex11": ("Two blocks, two fee markets", "The median fee rate of the highest-paying payments", "The market moved from over a thousand satoshis per byte to three",
             "The census holds the 599 highest-paying payments of the halving block 840,000 and of block 971,489. The median rate in the first was 1,436.45 satoshis per byte and in the second 3.02. A fee estimate is only as good as the market it was learned in."),
    "ex12": ("The opt-in replacement signal", "BIP 125: a sequence number that invites replacement", "Any input with a sequence below 0xfffffffe signals replaceability",
             "A payment signals that it may be replaced when one of its inputs has a sequence number below 0xfffffffe. In the halving block 485 of 599 payments signalled; in block 971,489 only 273. The signal matters less now that replacement needs no signal."),
    "ex13": ("A replacement must pay enough", "Four conflicting copies of one 564-satoshi payment", "Pay the old fee plus the new size at the incremental rate",
             "A replacement must pay more than the payment it replaces, and also pay for its own size at the incremental rate. For a payment of 564 satoshis and 141 bytes that is 579. The copies at 514, 564 and 578 are refused, and the one at 579 is accepted."),
    "ex14": ("Full replacement is the default", "A payment that never signalled is replaced", "Bitcoin Core 31.1 replaces without a signal and has no switch to stop it",
             "The first payment used the final sequence number, so it never asked to be replaceable. A conflicting payment replaced it anyway. Release 28.0 made full replacement the default and 29.0 removed the option, so starting the node with it off now fails."),
    "ex15": ("Paying the payee twice", "Three versions of one payment", "Replacing is not undoing: an old version may still be mined",
             "Three versions of a payment replace each other in turn. Versions 0 and 2 do not conflict, so once version 0 is mined, version 2 can be mined too. The payee asked for 40,000,000 satoshis and received 80,000,000. The sender pays twice."),
    "ex16": ("A child lifts its parent", "Child pays for parent, measured in a block", "Miners price a parent and its child as one package",
             "A parent pays 1 satoshi per byte and would wait a long time. Its child pays 100. Miners treat the pair as one package of 50.77 satoshis per byte, which beats a waiting payment at 20, so the pair is mined first."),
    "ex17": ("A weak child does not help", "A child at 5 satoshis per byte", "A package is only as good as its combined rate",
             "This time the child pays only 5 satoshis per byte. The pair together pays 3.02, less than the waiting payment A at 20. Miners took A and left the pair out. A child must pay enough to lift the pair above the competition."),
    "ex18": ("Package relay", "A parent below the floor, sent with its child", "Nodes can judge a pair that a single payment would fail",
             "A parent with 8 satoshis fails the relay floor of 15 on its own, and its child cannot be sent first because the parent is unknown. As a package the pair is judged by its combined rate and accepted. Limited package relay of one parent and one child exists since release 28.0."),
    "ex19": ("Cluster limits", "The cluster mempool of Bitcoin Core 31", "Limits are set on clusters of connected payments, not on single chains",
             "Release 31.0 groups connected payments into clusters, limited to 64 payments and 101,000 virtual bytes. Of a chain of 65, 64 are accepted and the next is refused as a too-large cluster. The old limit of 25 ancestors is gone, so a chain of 26 is accepted."),
    "ex20": ("Mempool size and expiry", "Two defaults of the waiting room", "A payment may wait fourteen days, not one",
             "The mempool holds 300 megabytes by default. A payment that waits too long is dropped after 336 hours, which is 14 days. The book speaks of about a day's worth, which describes neither default."),
    "ex21": ("A big child pins its parent", "Replacing a parent costs more when its child is large", "Cap the size of the child and pinning becomes cheap to undo",
             "A parent that pays 705 satoshis gets a child of 90,012 bytes. To replace the parent, the replacer must pay for the whole family: 450,780 satoshis. With a version 3 child, capped at 1,000 bytes, the same replacement costs 5,145, about 88 times less."),
    "ex22": ("TRUC limits on a family", "Version 3: one small child, and a better sibling replaces it", "Strict limits make the worst case of pinning small and known",
             "A version 3 parent may have one child of at most 1,000 virtual bytes. A child of 1,350 is refused and one of 141 is accepted. A second child at the same rate is refused, and one at a higher rate evicts its sibling, so a pin cannot last."),
    "ex23": ("Pay to anchor", "A zero-fee parent with an output anyone can spend", "The parent pays nothing; the child brings the fee when it is needed",
             "The parent has a zero-value output with the script 51024e73, which anyone can spend, and it pays no fee. Alone the node refuses it. The child spends the anchor with an empty witness and pays 10,000 satoshis, so the package is accepted."),
    "ex24": ("The carve-out limit", "What the book says and what the code says", "Check the numbers of a book against the source code",
             "The carve-out allowed one extra child beyond the usual limits. The book gives its size as 1,000 virtual bytes, while the source code says 10,000. Release 31.0 removed the rule, because the cluster limits replaced the descendant limits it worked around."),
    "ex25": ("Fees against the subsidy", "The reward of the halving block and of a later block", "The claim that the subsidy dwarfs fees fails in the halving block",
             "In block 840,000 the fees were 3,762,561,499 satoshis of a 4,075,061,499 reward, so the subsidy of 312,500,000 was only the rest. That is 92.33 percent fees. In block 971,489 fees were 0.46 percent of the reward."),
    "ex26": ("Odds of winning a sniping race", "How hash rate turns into the chance to re-mine a block", "With 45 percent of the hash rate a miner wins two races in three",
             "A miner with a share x of the hash rate wins the race to re-mine a block with probability x over one minus x, squared. That is 1.23 percent at 10 percent of the hash rate and 66.94 percent at 45. At half the hash rate the chance is certain."),
    "ex27": ("Wallets lock to the chain tip", "The lock time against fee sniping", "A lock time equal to the tip makes a re-mined block useless to the sniper",
             "A wallet sets the lock time of a payment to the current height, so that a miner who rewrites the block cannot take it. Of 60 payments in the test, 56 sit at the tip and four are set back. Such a payment is not final in the block of that height."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    acc = lambda b: "accepted" if b else "refused"
    v = lambda e: val(ex, e)
    if ex == "ex01":
        hf, fee = v("(has_fee, fee)"); ni, no = v("(n_in, n_out)"); ins, outs = v("ins"), v("outs")
        return ([tb([["Quantity", "Value"], ["Fee field in the parsed payment", yn(hf)], ["Inputs and outputs", "%d and %d" % (ni, no)], ["Value of the inputs, sat", fmt(ins)], ["Value of the outputs, sat", fmt(outs)], ["Inputs minus outputs, sat", fmt(fee)]], [2.0, 1.25])],
                "what the parser finds", "No field states the fee. It is the difference: %s satoshis, left unclaimed by the outputs." % fmt(fee))
    if ex == "ex02":
        why, guard, paid = v("(why, guard, paid)"); sub, fee, rew = v("bs['subsidy']"), v("bs['totalfee']"), v("a['coinbase_out_sat']")
        return ([ch(["Subsidy", "Fee", "Reward"], [sub, fee, rew], "satoshis")], "the miner's reward, satoshis",
                "The node said %s. With the limit lifted, the reward %s equals subsidy plus fee: %s." % (why, fmt(rew), yn(paid)))
    if ex == "ex03":
        ok, cut = v("(ok, cut)"); why, d, t = v("why"), v("d"), v("w['output0_tampered_sat']")
        return ([tb([["Version", "Output 0, sat", "Node"], ["As signed", fmt(d), acc(ok[0])], ["Output cut", fmt(t), acc(ok[1])]], [0.95, 1.3, 1.0])],
                "the same payment, signed and edited", "The cut of %s satoshis breaks the signature: %s." % (fmt(cut), why))
    if ex == "ex04":
        z, ra = v("sizes + wv"), v("ratio")
        return ([ch(["No witness", "All bytes", "Weight", "Virtual size"], z, "units")], "four measures of one payment",
                "Virtual size %d is the weight %d over four, rounded up: the ratio is %s." % (z[3], z[2], ra))
    if ex == "ex05":
        rate, a, b, same = v("(rate, a, b, same)"); f, vs = v("x['fee_sat']"), v("x['vsize']")
        return ([tb([["Quantity", "Value"], ["Fee over virtual size", "%d / %d = %s" % (f, vs, rate)], ["0.00006570 BTC per kvB", "%s sat/vB" % a], ["0.00001225 BTC per kvB", "%s sat/vB" % b],
                     ["10 sat/vB or 0.0001 BTC/kvB", "same fee: %s" % yn(same)]], [1.9, 1.35])],
                "rates and their units", "A coin-per-kilobyte rate is a hundred thousand times smaller as a number than the same rate in satoshis per byte.")
    if ex == "ex06":
        wt, lim, sh = v("(w, limit, share)")
        return ([tb([["Quantity", "Weight units"], ["Limit of a block", fmt(lim)], ["Block 840,000", fmt(wt)], ["Room left", fmt(lim - wt)], ["Share of the limit", "%s percent" % sh]], [1.75, 1.5])],
                "weight units of a block", "The block fills %s percent of the %s units, so payments compete for room." % (sh, fmt(lim)))
    if ex == "ex07":
        fees, taken, need = v("(fees, taken, need)"); fl = v("floor")
        return ([tb([["Fee, sat", "Node says"]] + [[str(f), acc(t)] for f, t in zip(fees, taken)] + [["Floor, sat per byte", str(fl)]], [1.5, 1.75])],
                "three fees for 141 virtual bytes", "At %s satoshi per byte, 141 bytes cost 14.1 satoshis: %d is the smallest whole fee." % (fl, need))
    if ex == "ex08":
        dust, wal = v("dust"), v("wal")
        return ([ch(["P2WPKH", "P2TR", "P2A anchor"], list(dust.values()), "satoshis")], "dust limit of three output types, satoshis",
                "The wallet refused 0.5 and 0.1 satoshis per byte and took 1: %s." % ", ".join(acc(b) for b in wal))
    if ex == "ex09":
        rates, f, n = v("rates"), v("f"), v("n")
        return ([ch(["2 blocks", "6 blocks", "25 blocks"], rates, "sat/vB")], "estimated fee rate by target, sat per byte",
                "Before: '%s'. After %d rounds the estimate is about 1.2 satoshis per byte at every target." % (f, n))
    if ex == "ex10":
        seen, same, cons = v("(seen, same, cons)"); tip = v("R['estimate']['tip']")
        return ([tb([["Question", "Answer"], ["Chain height of the test node", str(tip)], ["Blocks seen for target 144", str(seen)], ["Default equals economical", yn(same)], ["Conservative equals default", yn(cons)]], [2.2, 1.05])],
                "what the estimator answers", "The estimator cannot see beyond its own data: a target of 144 blocks is answered for %d." % seen)
    if ex == "ex11":
        med, n = v("med"), v("n")
        return ([ch(["Block 840,000", "Block 971,489"], med, "sat/vB")], "median fee rate, sat per byte",
                "Among the %d highest-paying payments of each block, the median rate fell from %s to %s." % (n, fmt(med[0]), med[1]))
    if ex == "ex12":
        fl, mixed, share = v("(flags, mixed, share)"); n = v("a['n']")
        return ([tb([["Input sequence", "Replaceable"], ["0xfffffffd", yn(fl[0])], ["0xfffffffe", yn(fl[1])], ["0xffffffff with 0xfffffffd", yn(mixed)], ["Signalling, block 840,000", "%d of %d" % (share[0], n)], ["Signalling, block 971,489", "%d of %d" % (share[1], n)]], [2.0, 1.25])],
                "the signal and its use", "One low sequence number is enough to signal, and fewer payments signal in the later block.")
    if ex == "ex13":
        fees, taken = v("(fees, taken)"); need = v("need")
        return ([tb([["Fee, sat", "Node says"]] + [[str(f), acc(t)] for f, t in zip(fees, taken)] + [["Needed, sat", str(need)]], [1.5, 1.75])],
                "four copies of a 564-satoshi payment", "The old fee plus the new size at the incremental rate: %d pass, %d do not." % (need, fees[2]))
    if ex == "ex14":
        full, seq, sw, gone = v("(full, seq, swapped, gone)")
        return ([tb([["Observation", "Result"], ["Sequence of the first payment", hex(seq)], ["Node runs full replacement", yn(full)], ["Conflicting payment replaced it", yn(sw)], ["Option switched off", "exit code %d" % gone[0]]], [2.1, 1.15])],
                "a payment that never signalled", "A payment without a signal was replaced, and the switch that turned this off is gone.")
    if ex == "ex15":
        asked, got, cf = v("(asked, got, [c01, c12, c02])")
        return ([ch(["Payee asked", "Payee received"], [asked, got], "satoshis")], "payee's amount, satoshis",
                "Versions 0 and 2 do not conflict (%s): both were mined and the payee got double." % yn(cf[2]))
    if ex == "ex16":
        al, pr = v("(alone, pair)")[0], v("(alone, pair)")[1]; fee = v("fee")
        return ([ch(["Parent alone", "Child alone", "Pair"], [al[0], al[1], pr], "sat/vB")], "fee rate, satoshis per byte",
                "The pair's %s beats the waiting payment A at %d, so parent and child are mined together." % (pr, round(fee["A"] / 141)))
    if ex == "ex17":
        pr, first = v("(pair, first)"); fee = v("fee")
        return ([tb([["Observation", "Result"], ["Child pays, sat per byte", str(round(fee["C"] / 141))], ["Pair pays, sat per byte", str(pr)], ["Waiting payment A pays", str(round(fee["A"] / 141))], ["A was mined", yn(first[0])], ["The parent was mined", yn(first[1])]], [2.0, 1.25])],
                "a child that pays too little", "The pair's combined rate stays below A, so miners take A and leave the pair out.")
    if ex == "ex18":
        msg, solo, alone, fee = v("msg"), v("solo"), v("alone"), v("p['v2_parent']['fee_sat']")
        return ([tb([["Sent as", "Node says"], ["Parent alone (%d sat)" % fee, solo], ["Child first", alone], ["Parent and child", msg]], [1.15, 2.1], 9)],
                "three ways to send the same pair", "Alone, each fails; as a package the pair is judged by its combined rate.")
    if ex == "ex19":
        lim, tried, why, ok26 = v("(lim, tried, why, ok26)")
        return ([tb([["Quantity", "Value"], ["Cluster limit: payments", str(lim[0])], ["Cluster limit: bytes", fmt(lim[1])], ["Chain tried and accepted", "%d and %d" % tried], ["The refusal", why], ["26th of a chain accepted", yn(ok26)]], [1.75, 1.5], 9)],
                "limits on one cluster", "Size is limited per cluster; the old limit of 25 ancestors no longer applies.")
    if ex == "ex20":
        size, hours, days = v("(size, hours, days)")
        return ([tb([["Setting", "Default"], ["Mempool size", "%d MB" % size], ["Expiry", "%d hours" % hours], ["Expiry in days", str(days)]], [1.75, 1.5])],
                "two defaults of the mempool", "A payment may wait %d days before the node forgets it." % days)
    if ex == "ex21":
        c2, c3, ra = v("(cost2, cost3, ratio)"); k2, k3, pf = v("v2['child']['vsize']"), v("v3['child']['vsize']"), v("v2['parent']['fee_sat']")
        return ([ch(["Child of %s B" % fmt(k2), "Child of %s B" % fmt(k3)], [c2, c3], "satoshis")], "cost to replace the parent, satoshis",
                "The parent pays %d. A pinned family of %s bytes costs %s to replace; a capped one only %s." % (pf, fmt(k2), fmt(c2), fmt(c3)))
    if ex == "ex22":
        bad, ok, ev = v("(bad, ok, ev)"); big, small = v("t['big_child']['vsize']"), v("t['child1']['vsize']")
        return ([tb([["Test", "Result"], ["Child of %s bytes" % fmt(big), "refused: TRUC rule" if bad else "accepted"], ["Child of %d bytes" % small, acc(ok)], ["Sibling at the same rate", "refused" if ev[0] else "accepted"], ["Sibling at a higher rate", "replaces the first" if ev[1] else "refused"]], [1.75, 1.5])],
                "limits of a version 3 family", "The family stays small, and a better sibling can always replace a pinning one.")
    if ex == "ex23":
        anc, alone, msg, emp, fee = v("anchor"), v("alone"), v("msg"), v("empty"), v("p['anchor_child']['fee_sat']")
        return ([tb([["Part", "Value"], ["Anchor script", anc[0]], ["Anchor value, sat", str(anc[1])], ["Parent alone", alone], ["Parent with child", msg], ["Child fee, sat", fmt(fee)]], [1.2, 2.05], 9)],
                "the anchor and the package", "The anchor carries no value and needs no key: the child that spends it brings the fee.")
    if ex == "ex24":
        lim, book, gone = v("(lim, book, gone)")
        return ([tb([["Source", "Says"], ["Bitcoin Core policy.h", "%s bytes" % fmt(lim)], ["The book, saved text", "1,000 bytes: %s" % yn(book)], ["Release notes 31.0", "removed: %s" % yn(gone)]], [1.5, 1.75])],
                "three sources compared", "The book and the code disagree by a factor of ten.")
    if ex == "ex25":
        sh = v("share"); sub, fees, rew = v("subsidy"), v("fees"), v("reward")
        return ([ch(["Block 840,000", "Block 971,489"], sh, "percent")], "fees as a percent of the block reward",
                "In the halving block the subsidy was %s of %s satoshis, the rest was fees." % (fmt(sub), fmt(rew)))
    if ex == "ex26":
        p = v("pct")
        return ([ch(["10%", "30%", "45%", "50%"], p, "percent")], "chance to win the re-mining race, percent",
                "At 45 percent of the hash rate the chance is %s percent; at half it is certain." % p[2])
    if ex == "ex27":
        at, back, late = v("(at_tip, back, late)"); n = v("len(s)"); rej = v("R2['locktime_block']['mempool_next']['reject-reason']")
        mn = v("[L.census_stats(h)['locktime_prev_height'] for h in (840000, 971489)]"); tot = v("L.census_stats(840000)['n']")
        return ([tb([["Observation", "Result"], ["Lock time at the tip", "%d of %d" % (at, n)], ["Set back by, blocks", ", ".join(str(b) for b in back)], ["Final in its own block", "%s (%s)" % (yn(late), rej)], ["Mainnet, tip as lock time", "%d and %d of %d" % (mn[0], mn[1], tot)]], [1.75, 1.5], 9)],
                "lock times of 60 payments", "A lock time at the tip keeps a payment out of any block that a sniper re-mines.")
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex02", "ex04", "ex08", "ex09", "ex11", "ex15", "ex16", "ex21", "ex25", "ex26") else "table"


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
    cap = "run under Python %s - L is the chapter library; R, R2 its runs" % PY
    blocks = {"t": "codeblocks", "x": X_, "w": W_, "fs": fs, "nfs": 10.5, "groups": gl, "cap": cap, "capy": capy}
    res_label = {"t": "text", "x": RX, "y": 1.45, "w": RW, "h": lab_h, "body": lab, "fs": 11, "font": "B", "bold": True, "color": "mute"}
    if items[0]["t"] == "table": ry = round(min(ry, vy + len(items[0]["rows"]) * items[0]["rowH"] + 0.3), 3)       # under the table, not at the foot of the slide
    read = {"t": "text", "x": RX, "y": ry, "w": RW, "h": rh, "body": reading, "fs": 11.5, "font": "B", "italic": True, "color": "ink"}
    if W(notes) > 60: raise SystemExit("REFUSED: notes of %s have %d words" % (ex, W(notes)))
    tail = " It is example %d in the chapter code tab of the course page." % int(ex[2:])
    num = add("content", title, sub_, [blocks, res_label] + items + [read], notes + tail if W(notes + tail) <= 60 and len(sentences(notes)) < 4 else notes, take)
    e["slide"] = num; e["rows"] = [[r[0] for r in g["rows"]] for g in gl]
    if not FIRST_CODE: FIRST_CODE.append(num)
    return num


# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories (5N1K: who, what, when, where, why, how; a real picture; a live link)
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORY_BEATS = {
    "FullRbfPeering": ["WHAT: On 12 December 2022 Peter Todd posted a build of Bitcoin Core 24.0.1 that carries Antoine Riard's full-rbf peering code.",
                       "WHY: Release 24.0.1 had added the option mempoolfullrbf, off by default, so only payments that signalled could be replaced.",
                       "HOW: The build advertises a FULL_RBF service bit and connects to four more nodes that do the same, so replacements travel reliably.",
                       "SO WHAT: Bitcoin Core 28.0 made full replacement the default and 29.0 removed the option, as the previous slide ran."],
    "CarveOutProposal": ["WHAT: On 29 November 2018 Matt Corallo proposed that a Lightning commitment transaction may carry one extra small child.",
                         "WHY: Pre-signed transactions are broadcast much later, so their fee cannot be guessed and a child has to add it.",
                         "HOW: A counterparty could chain a large child of moderate rate to the output and pin the transaction; the carve-out allows one more small child.",
                         "SO WHAT: Release 0.19.0.1 shipped it with 10,000 bytes, not the 1,000 the book states, and 31.0 removed it."],
    "HalvingBlock": ["WHAT: Block 840,000 was found on 20 April 2024 at 00:09 UTC by the pool ViaBTC and held 3,050 transactions.",
                     "WHY: It was the first block after the fourth halving, so the subsidy fell from 6.25 to 3.125 bitcoins.",
                     "HOW: Fees were 3,762,561,499 satoshis of a 4,075,061,499 reward, which is 92.33 percent; in block 971,489 they were 0.46 percent.",
                     "SO WHAT: The book says the subsidy is much higher than fees, which is true of the later block and false of this one."],
    "InstabilityPaper": ["WHAT: On 21 October 2016 Arvind Narayanan announced the paper On the Instability of Bitcoin Without the Block Reward on the Princeton CITP blog.",
                         "WHY: Rewards are expected to give way to fees, and when fees are the main income a miner can gain by undercutting a rival's block.",
                         "HOW: The chapter computes that a miner with 45 percent of the hash rate wins the race to re-mine a block with probability 66.94 percent.",
                         "SO WHAT: Fees must replace the subsidy, so the rules for fees must be stable; wallets defend with the lock time."],
}
STORY_SUB = {"FullRbfPeering": "Peter Todd's build, 12 December 2022", "CarveOutProposal": "Matt Corallo's proposal, 29 November 2018",
             "HalvingBlock": "ViaBTC and block 840,000, 20 April 2024", "InstabilityPaper": "A Princeton paper, 21 October 2016"}
STORY_LINK = {"FullRbfPeering": "Peter Todd: Full-RBF Peering (post)", "CarveOutProposal": "Matt Corallo: CPFP carve-out (post)", "InstabilityPaper": "CITP blog: no block reward (post)"}   # at most 40 characters, so the chip shows the host under it
STORY_TITLE = {"CarveOutProposal": "A pre-signed payment cannot guess its fee", "HalvingBlock": "Block 840,000: fees were nearly the reward"}   # shorter than the story module's title: the title box holds one line
STORY_FACT = {"FullRbfPeering": ("Peter Todd, A. Riard", "bitcoin-dev list"), "CarveOutProposal": ("Matt Corallo", "bitcoin-dev list"),
              "HalvingBlock": ("ViaBTC pool", "block 840,000"), "InstabilityPaper": ("Narayanan et al.", "Princeton, ACM CCS")}
STANDIN = {"FullRbfPeering": "Stand-in picture: an accepted-here sign, not the post", "CarveOutProposal": "Stand-in picture: the Lightning logo, not the proposal",
           "HalvingBlock": "Stand-in picture: a mining farm, not the pool ViaBTC"}


def story_slide(sid):
    st = STORY[sid]; beats = STORY_BEATS[sid]
    for b in beats:
        if W(b) > 30: raise SystemExit("REFUSED: beat of %s has %d words" % (sid, W(b)))
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    cut = lambda s: s[:150].rsplit(",", 1)[0] if len(s) > 150 else s
    items = [{"t": "img", "path": ASSETS + st["photo"], "x": 0.5, "y": 1.4, "w": 3.4, "h": 2.55, "cap": st["credit"]},
             {"t": "beats", "x": 4.1, "y": 1.4, "w": 5.4, "h": 2.7, "fs": 11.5, "items": beats},
             ] + ([{"t": "text", "x": 0.5, "y": 4.3, "w": 3.4, "h": 0.17, "body": STANDIN[sid], "fs": 8.5, "font": "B", "italic": True, "color": "mute"}] if sid in STANDIN else []) + [
             {"t": "factrow", "x": 0.5, "y": 4.5, "w": 9.0, "who": STORY_FACT[sid][0], "where": STORY_FACT[sid][1], "when": st["when"], "link": st["link"], "linkText": STORY_LINK.get(sid) or st.get("linkLabel") or host}]
    first = sentences(st["story"])[0]
    notes = "This is a true story, dated %s. %s" % (st["when"], first)
    tail = " The lesson is that %s." % (st["lesson"][0].lower() + st["lesson"][1:]).rstrip(".")
    if W(notes + tail) <= 60: notes += tail
    if W(notes) > 60: notes = "This is a true story, dated %s. The lesson is that %s." % (st["when"], (st["lesson"][0].lower() + st["lesson"][1:]).rstrip("."))
    return add("content", STORY_TITLE.get(sid, st["title"]), STORY_SUB[sid], items, notes)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
PLAN = {
    "WhoPaysTheFee": (["ex01", "ex02", "ex03"], {}),
    "FeesAndFeeRates": (["ex04", "ex05", "ex06", "ex07", "ex08"], {}),
    "FeeEstimation": (["ex09", "ex10", "ex11"], {}),
    "ReplaceByFee": (["ex12", "ex13", "ex14", "ex15"], {"ex14": "FullRbfPeering"}),
    "ChildPaysForParent": (["ex16", "ex17", "ex18", "ex19", "ex20"], {}),
    "PinningAndAnchors": (["ex21", "ex22", "ex23", "ex24"], {"ex24": "CarveOutProposal"}),
    "FeeSnipingAndIncentives": (["ex25", "ex26", "ex27"], {"ex25": "HalvingBlock", "ex26": "InstabilityPaper"}),
}
BR_KEY = {b: [k for k, v in K.K3.items() if v[0] == b] for b in BRANCHES}
RES_SUB = "Opened on 2026-10-25; every entry is a live link in this file"


def build():
    S.clear(); ANALOGIES.clear(); FIRST_CODE.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    assert list(PLAN) == BRANCHES, (list(PLAN), BRANCHES)
    add("title", "Chapter 9: Transaction Fees", "Who pays a fee, how it is priced, replaced and bumped, and what moved since print",
        [{"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Python %s on the chapter's own library; Bitcoin Core 31.1 results are recorded from one test run, not run here." % PY}],
        "This deck explains transaction fees: who pays them, how they are priced, how a payment is replaced or bumped, and what changed since the book went to print. Every number on a result picture was computed with the chapter's own Python library. Bitcoin Core 31.1 was run once on a test network, and its answers are only read back.")
    add("content", "Today's route", "", [], "", "Seven parts, twenty-seven examples, four true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "Who pays a transaction fee, and why is it not a field of the transaction?", "How is a fee rate computed, and which minimum rates apply?",
            "How does a node estimate a fee, and what do two real blocks show?", "What must a replacement pay, and why is full replacement now the default?",
            "How does a child pay for its parent, and what does package relay add?", "How can a family pin a payment, and what do TRUC and anchors change?",
            "What is fee sniping, and why do wallets lock a payment to the tip?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, seven parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 4, "fs": 12.5, "subfs": 10.5, "accent": [],
          "items": [{"label": LAB[b], "sub": "%d key concepts, %d examples" % (len(BR_KEY[b]), len(PLAN[b][0]))} for b in BRANCHES]}],
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
                if v == "ex15":
                    add("content", "Policy or consensus?", "Why a payment can be valid and still not be relayed",
                        [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                          "left": {"head": "Consensus decides what is valid", "rows": ["Every node must agree, or the chain splits.", "The block weight limit is one such rule.", "A change needs a soft or hard fork."]},
                          "right": {"head": "Policy decides what is relayed", "rows": ["Each node may choose its own rules.", "Relay floor, replacement rules, TRUC and cluster limits are policy.", "A change needs only a new release."]}}],
                        "Most rules of this chapter are policy: the relay floor, the replacement rules, the version 3 limits and the cluster limits. A payment that breaks them can still be valid in a block that a miner builds. Policy changes with a release; consensus changes only by a fork.",
                        "Policy can change with a release; consensus changes only by a fork")
    add("content", "The chapter in five lines", "One line per group of parts, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "The fee is inputs minus outputs: no field holds it, and only the spender can change it.",
            "Miners sort by fee rate in satoshis per virtual byte; the relay floor and dust set minimums.",
            "A payment is replaced by a copy that pays the old fee plus its own size; full replacement is the default.",
            "A child pays for its parent as one package; clusters, TRUC and anchors bound pinning.",
            "When fees replace the subsidy, a miner may snipe a block, and wallets defend with the lock time."]}],
        "These five lines are the deck in miniature. A line that feels unproven should send you back to its code slide, because every figure in it was computed there. The chapter code tab of the course page reruns all twenty-seven examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch. A good start is the Antonopoulos talk on fees, then the Optech topic on replace by fee next to the chapter. The course page for chapter 9 carries the full text and the sources behind every figure.",
        "Watch the fees talk, then read the Optech topic beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "Who pays a fee, and how rates work", "How payments are replaced or bumped",
            "How packages, clusters and anchors work", "Why sniping matters; the lock time defence"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 9 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Seven parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 3, "fs": 11.0, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has seven parts that follow the order of the chapter. Four true stories and twenty-seven code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
    return N


def research_labels():
    f = sorted(glob.glob(os.path.join(ROOT, "03-materials", "ch09", "rdodi", "sen0401_ch09_research_v*.ttl")), key=vk)[-1]
    labs = re.findall(r"a sen04(?:01|14):PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", open(f, encoding="utf-8").read())
    norm = lambda t: " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in re.sub(r"[^a-z0-9]+", " ", re.sub(r"\([^)]*\)", " ", t.lower())).split())
    seen, out = set(), []
    for l in labs:
        k = norm(l)
        if k and k not in seen: seen.add(k); out.append((l, k))
    return out, norm


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
    labs, norm = research_labels()
    text = norm(" ".join(json.dumps(s["items"]) + " " + s["title"] + " " + s["sub"] for s in S))
    missing = [l for l, k in labs if k not in text]
    cov = 100.0 * (len(labs) - len(missing)) / len(labs)
    print("coverage (D11, by research concept label on a slide): %d of %d = %.1f percent; missing: %s" % (len(labs) - len(missing), len(labs), cov, missing))
    ana = {a["concept"] for a in ANALOGIES}
    nona = [c for c in K.K3 if c not in ana]
    print("analogies (D4): %d of %d key-concept cards carry one; without: %s" % (len(K.K3) - len(nona), len(K.K3), nona))
    if bad: raise SystemExit("REFUSED:\n  " + "\n  ".join(bad))
    if missing or nona: raise SystemExit("REFUSED: key concepts missing or without analogy")
    return cov


def manifest(N):
    setup = "# setup: the chapter library of the page (L = the chapter 9 library, with the recorded runs of Bitcoin Core 31.1 and the census of two blocks, R, R2 and C); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch09_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: the wheel of the page is unpacked into a scratch folder (the module and the saved records it carries, nothing else), and each example runs in a fresh
    # interpreter as setup + listing; every recorded value must reproduce
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch09_")
    zipfile.ZipFile(os.path.join(ROOT, WHEEL)).extractall(tmp)
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
        print("page path (the wheel's files only) under %s: %d examples reproduce the recorded values" % (py, len(exs)))
    shutil.rmtree(tmp, ignore_errors=True)
    return {"manifest": "chapter_code_ch09_v1_0_0", "chapter": 9, "deck": "SEN0401_Ch09_TransactionFees_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch09_lib", "file": WHEEL, "sha256": hashlib.sha256(open(os.path.join(ROOT, WHEEL), "rb").read()).hexdigest(), "modules": [LIBMOD],
                        "import": "import %s as L" % LIBMOD}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 9: Transaction Fees", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch09_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch09", "page", "chapter_code_ch09_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch09_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 9"])
    mat = os.path.join(ROOT, "03-materials", "ch09", "SEN0401_Ch09_TransactionFees_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
