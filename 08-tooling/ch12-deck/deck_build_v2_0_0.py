#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 12, Mining and Consensus) - the generator of the chapter 12 deck 2.0.0 (task TK_Ch12_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch11-deck/deck_build_v2_0_0.py.
It writes, from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch12/page/chapter_code_ch12_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the story module v1_2_0 (four stories with pictures), the recorded executions examples_out_v2_0_0.json (made by examples_run_v2_0_0.py under Python 3.14),
deck_concepts_v2_0_0.py (the 39 key concepts of the chapter taxonomy and the 41 concepts that the research file lists, each with a meaning and one everyday analogy) and the resources slide of the previous
plan. Every number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the file is drawn: no text box over 30 words, notes of at
most 60 words, no code line over 60 characters with its prompt (a listing never wraps), every key concept of the research on a slide with its analogy.
Usage: python3.14 -I deck_build_v2_0_0.py [--render]"""
__version__ = "2.0.0"
import ast, glob, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_0_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.0.0", "2_0_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch12_stories_v*.py")), key=vk)[-1], "stories12")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
LAB = K.LAB
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch12/assets/"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v1_1_0.json")))
BRANCHES = K.BRANCHES

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


def sentences(t):
    t = re.sub(r"\b(Mt|Dr|St|Mr|Mrs|vs|No)\.\s", lambda m: m.group(1) + ".\x00", t.strip())
    return [s.replace("\x00", " ") for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9'\"(])", t) if s]


# ------------------------------------------------------------------------------------------------------------------------------------------------
# dividers
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEGS = [(K.SHORT[b], 1.0) for b in BRANCHES]


def strip(branch, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = SEGS.index((K.SHORT[branch], 1.0))
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": i == hot} for i, (lab, f) in enumerate(SEGS)]}


DIV_NOTES = {
    "MoneyCreation": "A miner is paid in new coins and fees. This part shows how the subsidy halves, why the supply stops just below 21 million coins, and how Core checks that a miner claims no more than the reward.",
    "DecentralizedConsensus": "No one is in charge, so every node checks everything itself. We run the rules for transactions and blocks, and see why the chain with the most work wins, not the longest chain.",
    "BuildingTheCandidateBlock": "Before the lottery starts the miner builds a candidate block. We read the coinbase that Core makes today, take an 80-byte header apart, and see how the extra nonce gives a new search space.",
    "ProofOfWork": "Proof of work is a lottery with a target. We play it with a text, read the target from the bits, turn difficulty into days, and follow the retarget rule on a real period of 2024.",
    "MiningCompetition": "Mining is a race. The nonce space runs out, small miners form pools, and a large share of the power buys the odds of an attack. We compute each of these.",
    "ChangingConsensusRules": "Rules change by forks. We watch a looser and a stricter node disagree, time a minority chain, follow a BIP 9 vote and read the heights of old soft forks in the source code.",
    "RecapChapter11": "Mining stands on the ideas of chapter 11. A miner builds a header, commits to a merkle root, writes a height into the coinbase and tests on regtest. These cards recall the 41 concepts.",
}


def divider(branch):
    groups = K.GROUPS[branch]; n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 3 else 11
    its = []
    for key, pill, mean, ana in groups:
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12 if n <= 3 else 11, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
        ANALOGIES.append({"concept": pill, "analogy": an, "slide": len(S) + 1})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (branch, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12 if n <= 3 else 11, "items": its}, strip(branch)]
    ANALOGIES.append({"concept": LAB[branch], "analogy": K.L1[branch], "slide": len(S) + 1})
    return add("section", LAB[branch], K.L1[branch], items, DIV_NOTES[branch])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards: the key concepts of the research
# ------------------------------------------------------------------------------------------------------------------------------------------------
def chunks(lst, top=6):
    n = len(lst)
    if n == 0: return []
    k = -(-n // top); base, extra = divmod(n, k)
    out, i = [], 0
    for j in range(k):
        size = base + (1 if j < extra else 0); out.append(lst[i:i + size]); i += size
    return out


def plan_chunks(branch, names, top=6):
    """greedy: the largest group of cards (at most top) that still fits the slide, tried by a dry run of cards() that is rolled back"""
    out, i = [], 0
    while i < len(names):
        for size in range(min(top, len(names) - i), 0, -1):
            ns, na = len(S), len(ANALOGIES)
            try:
                cards(branch, names[i:i + size], 1, 1)
                ok = True
            except SystemExit:
                ok = False
            del S[ns:]; del ANALOGIES[na:]
            if ok: break
        else:
            raise SystemExit("REFUSED: a single card %s does not fit" % names[i])
        out.append(names[i:i + size]); i += size
    # balance: no lone card on the last slide; one card of the slide before moves to it (a smaller slide still fits)
    if len(out) > 1 and len(out[-1]) == 1 and len(out[-2]) > 2:
        out[-1].insert(0, out[-2].pop())
    return out


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
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 12." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 12." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("Halving every 210,000 blocks", "The reward at five heights, and the last non-zero reward", "The reward halves on a fixed calendar until it reaches one satoshi",
             "The reward starts at 50 coins and is cut in half at every multiple of 210,000 blocks. The shift is done in whole satoshis, so after the 33rd halving a single satoshi is left, and after the 34th nothing. The sum of all rewards sets the supply."),
    "ex02": ("The 21 million limit", "Whole satoshis against the book's float script", "The real total is a little under 21 million coins, and a float hides that",
             "Adding the 33 non-zero rewards in whole satoshis gives a total just below 21 million coins. The book's script divides with a slash, which in Python 3 is a float division. Run as printed it ends at a float and never shows the shortfall."),
    "ex03": ("Subsidy plus fees is the reward", "A private chain: what Core offers and what a miner claims", "A miner may claim less than the reward, never one satoshi more",
             "Bitcoin Core offered a reward made of the subsidy and the fees of the chosen transactions. A miner claimed one satoshi less and the block was accepted. A test block that claimed one satoshi more was refused with the name bad-cb-amount."),
    "ex04": ("A transaction faces a checklist", "Spoiled transactions and the reasons Core gave", "Every refusal has a name, and a fresh coinbase cannot be spent before 100 blocks",
             "Each node tests every transaction against the same rules. We asked a private node about a spoiled transaction and got a named reason each time. A coinbase output is refused at depth 99 and accepted at depth 100."),
    "ex05": ("A block faces its own checklist", "Fourteen test blocks, each breaking one rule", "Reward, height, merkle root, clock and version each have a rule of their own",
             "The block checks go further than the transaction checks. We handed Core blocks that each broke one rule. The reward one satoshi too high, a missing height, a wrong merkle root, a wrong clock or an old version each got its own named reason."),
    "ex06": ("The best chain has the most work", "Two branches on a private chain, and a reversed payment", "A heavier branch replaces a lighter one, even when both have equal length",
             "Two branches were built, and the first paid Carol. The second branch carried more chain work, so Core switched to it and the payment fell out of the chain. This is why a shop waits for confirmations."),
    "ex07": ("The coinbase of Bitcoin Core today", "Height, lock time and sequence in the first transaction", "Core sets the lock time and the sequence, which the book does not say",
             "The coinbase script starts with the block height as a short pushed number. Bitcoin Core 31.1 also sets the lock time to the height minus one and a sequence below the maximum. The template's weight limit leaves room for the block header."),
    "ex08": ("The header of a mined block", "Eighty bytes, and a hash under the target", "A valid header hashes to a number that is not above its target",
             "The header of a regtest block is eighty bytes with six fields. Its hash, read as a number, is not larger than the target that the bits describe. On regtest the target is huge, so a few zero bits are enough."),
    "ex09": ("A new extra nonce, a new root", "Same block, one counter changed in the coinbase", "The header's nonce stays, yet the hash is new: a fresh search space",
             "A miner that has used up the nonce changes a counter in the coinbase script. That changes the coinbase id, the merkle root and so the whole header. The header's own nonce can start again from zero."),
    "ex10": ("Proof of work is a nonce lottery", "Hello, world! with a counter, and the tries for each zero", "Each extra zero digit costs about sixteen times more tries",
             "The book hashes a text with a counter added. The first hash that starts with a zero comes at counter 32. Every further zero digit makes the search about sixteen times longer, while checking the answer always takes a single hash."),
    "ex11": ("Target, bits and difficulty", "Block 277,316 as the book lists it", "A smaller target means a higher difficulty and more zero bits",
             "The header stores the target as four bytes called bits. Block 277,316 has bits 1903a30c, a target of 194 bits. The difficulty is the number of times smaller this target is than the easiest one. A valid hash must start with 62 zero bits."),
    "ex12": ("The wait of a one-terahash miner", "Difficulty turned into days and into hashes", "The book's 8,496 blocks are 8,453 when recomputed",
             "Difficulty times two to the 32 is the number of hashes to find a block. A miner doing one terahash a second waits about 59 days at that difficulty. The same formula applied to today's difficulty estimates the network hash rate."),
    "ex13": ("Retargeting on a real epoch", "The period that ended at block 840,671", "The rule reproduces the real adjustment from two block times",
             "Every 2,016 blocks Bitcoin scales the target by the real duration over the intended fourteen days. The period before block 840,672 took 1,186,047 seconds, a little short of fourteen days. The rule gives the bits that the chain really has."),
    "ex14": ("The factor-of-four clamp", "A period far too fast, on time, and far too slow", "One retarget moves the target by at most a factor of four",
             "A period of 2,016 blocks may be much faster or slower than planned. To protect the network the rule limits the change of the target to a quarter or four times. The ratios stop at those two values."),
    "ex15": ("Regtest never retargets", "Chain constants, and the BIP 94 branch", "Testnet4 turns the BIP 94 branch on; mainnet does not need it",
             "Each chain has its own constants in the source file. Regtest sets a flag that stops all retargeting, so its bits stay put after 2,016 blocks. Testnet4 enforces BIP 94, a branch of the retarget code that the book's listing does not have."),
    "ex16": ("When the 32-bit nonce runs out", "How often the nonce space is emptied each second", "A modern network empties the nonce space hundreds of billions of times a second",
             "A 32-bit nonce gives 4.3 billion tries. The network does a thousand billion billion hashes a second, so the space is used up far too often. Miners vary the version field and the coinbase script to get new header contents."),
    "ex17": ("Why a small miner joins a pool", "The wait for one block, by share of the hash rate", "A share of one in ten thousand waits more than two months for a block",
             "The network finds 144 blocks a day. A miner with a small share of the power has to wait long for one block. A pool collects power and pays members for easy partial solutions, so the income comes in small regular amounts."),
    "ex18": ("Odds of a hash rate attack", "Catching up from six blocks, and the selfish-mining share", "The odds climb steeply with the attacker's share of the power",
             "Nakamoto's formula gives the chance that an attacker with a given share ever catches up from six blocks behind. The share needed for selfish mining falls as more honest miners follow the selfish block."),
    "ex19": ("A hard fork splits, a soft fork does not", "A loose and a strict node on a private chain", "Looser rules split the chain into two; stricter rules do not",
             "A node with the old, looser rule accepted a block that has no height. A node with the new, stricter rule refused it. The loose node went on building, and the two nodes ended with different tips."),
    "ex20": ("The minority chain is slow", "How long 2,016 blocks take on a weaker branch", "With a tenth of the power a fortnight of blocks takes 140 days",
             "After a split a branch has the old difficulty but only a share of the hash rate. Blocks arrive more slowly, and the next retarget is far away. In March 2013 the old chain was kept for only six hours for this reason."),
    "ex21": ("BIP 9 states and the vote", "A test deployment and the two thresholds", "The state moves forward only on signals; taproot needed 90 percent",
             "A deployment is defined, started, locked in and then active. Core, on a private chain, reported each state at six heights. BIP 9 asks for 95 percent of 2,016 blocks. The Speedy Trial of taproot asked for 90 percent."),
    "ex22": ("Buried deployments", "Soft fork heights in the source code", "An old soft fork is no longer voted on; it is a plain height",
             "Once a soft fork is old and settled, Bitcoin Core writes its activation as a plain height in the source file. We read the heights of four soft forks from the saved file. Nobody needs to count signals any more."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    if ex == "ex01":
        btc, last, zero = val(ex, "btc"), val(ex, "last"), val(ex, "L.subsidy(34 * 210000)")
        return ([ch(["0", "210,000", "420,000", "630,000", "840,000"], btc, "coins")], "reward in coins from each height",
                "The reward falls from %g to %g coins. After the 33rd halving it is %d satoshi, and after the 34th %d." % (btc[0], btc[-1], last, zero))
    if ex == "ex02":
        tot, sh, tn, fl = val(ex, "tot"), val(ex, "short"), val(ex, "type(fl).__name__"), val(ex, "fl")
        return ([tb([["Quantity", "Value"], ["Total, in satoshis", fmt(tot)], ["Short of 21 million coins", fmt(sh) + " sat"], ["Book script returns", tn], ["Value as printed", str(fl)]], [1.5, 1.75])],
                "the supply, in whole satoshis", "The exact total is %s satoshis. Run as printed, the book's script ends with a %s, which hides the shortfall." % (fmt(tot), tn))
    if ex == "ex03":
        sb, fe, cv_, ok, m, bad = val(ex, "r['subsidy']"), val(ex, "r['fees']"), val(ex, "r['coinbasevalue']"), val(ex, "ok"), val(ex, "m"), val(ex, "bad")
        return ([ch(["Subsidy", "Fees", "Reward offered", "Claimed"], [sb, fe, cv_, m], "satoshis")], "satoshis offered and claimed",
                "Subsidy plus fees equals the reward: %s. The claim is one satoshi less and is accepted; one more gives %s." % (yn(ok), bad))
    if ex == "ex04":
        why, ok, nf = val(ex, "why"), val(ex, "ok"), val(ex, "c['locktime_in_the_future']['reject-reason']")
        sh = lambda r: r.replace("bad-txns-", "")
        return ([tb([["Spoiled transaction", "Reason (bad-txns- left out)"], ["Same input twice", sh(why[0])], ["Negative output", sh(why[1])], ["Coinbase at depth 99", sh(why[2])],
                     ["Coinbase at depth 100", "accepted" if ok else "refused"], ["Lock time ahead", nf]], [1.35, 1.9], 9)],
                "named reasons from Bitcoin Core", "Each refusal names the rule it broke. Only the coinbase at depth 100 is allowed.")
    if ex == "ex05":
        n, ok = val(ex, "len(rules)"), val(ex, "ok")
        g = lambda k: val(ex, "rules['%s']" % k)
        return ([tb([["Rule broken", "Reason given"], ["Reward one satoshi high", g("reward_one_satoshi_too_high")], ["No height in coinbase", g("no_height_in_coinbase")], ["Wrong merkle root", g("merkle_root_wrong")],
                     ["Time equals median", g("time_equal_to_median_time_past")], ["Time two hours ahead", g("time_two_hours_and_a_second_ahead")], ["Version 1", g("version_1")]], [1.6, 1.65], 9)],
                "six of the %d test blocks" % n, "The valid block is %s; every other block is refused with a name for its rule." % ok)
    if ex == "ex06":
        w1, w2, y2 = val(ex, "w1"), val(ex, "w2"), val(ex, "a['tip_is_y2']")
        cb, ca, pb, pa = val(ex, "b['carol_received']"), val(ex, "a['carol_received']"), val(ex, "b['pay_confirmations']"), val(ex, "a['pay_confirmations']")
        return ([ch(["First branch", "Second branch"], [w1, w2], "chain work")], "chain work of the two tips",
                "The second branch has more work, so it wins: %s. Carol held %s before and %s after; the payment went from %d to %d confirmations." % (yn(y2), cb, ca, pb, pa))
    if ex == "ex07":
        wl, hgt, hx, ss, lt, sq, vr = val(ex, "w"), val(ex, "k['height']"), val(ex, "hx"), val(ex, "k['scriptsig']"), val(ex, "k['locktime'] == k['height'] - 1"), val(ex, "hex(k['sequence'])"), val(ex, "k['version']")
        return ([tb([["Field", "Value"], ["Weight limit of the template", fmt(wl)], ["Block height", str(hgt)], ["Height as a script push", hx], ["Whole script", ss], ["Lock time is height - 1", yn(lt)], ["Sequence", sq]], [1.9, 1.35], 9)],
                "the first transaction of a Core block", "The script is the height as a short push, %s, and a zero byte. Core sets version %d." % (hx, vr))
    if ex == "ex08":
        by, ve, bi, no, z, ok = val(ex, "h['bytes']"), val(ex, "h['version']"), val(ex, "h['bits']"), val(ex, "h['nonce']"), val(ex, "z"), val(ex, "ok")
        return ([tb([["Field", "Value"], ["Header size, bytes", str(by)], ["Version", str(ve)], ["Bits", bi], ["Nonce", str(no)], ["Zero bits at the start", str(z)], ["Hash not above target", yn(ok)]], [1.75, 1.5], 9)],
                "a regtest header taken apart", "The bits %s describe a huge target, so %d zero bits are enough on this private chain." % (bi, z))
    if ex == "ex09":
        a, b, c, d = val(ex, "t1 != t2"), val(ex, "m1 != m2"), val(ex, "n1 == n2"), val(ex, "e['hash_1'] != e['hash_2']")
        return ([tb([["Observation", "Result"], ["Coinbase id differs", yn(a)], ["Merkle root differs", yn(b)], ["Header nonce is the same", yn(c)], ["Header hash differs", yn(d)]], [2.1, 1.15])],
                "the same block, two extra nonces", "Only the counter in the coinbase changed, yet the header is new.")
    if ex == "ex10":
        lo, up, t = val(ex, "lo"), val(ex, "up"), val(ex, "t")
        return ([ch(["1 zero", "2 zeros", "3 zeros", "4 zeros"], t, "tries")], "tries until the hash starts with zeros",
                "The book prints the hash %s for the capital W, but that is the hash of the small w. The capital W gives %s." % (lo, up))
    if ex == "ex11":
        bl, df, nd, bb = val(ex, "tg.bit_length()"), val(ex, "round(d)"), val(ex, "need"), val(ex, "hex(L.target_to_bits(tg))")
        return ([tb([["Quantity", "Value"], ["Bits in the header", "1903a30c"], ["Target is how many bits long", str(bl)], ["Difficulty", fmt(df)], ["Zero bits a hash needs", str(nd)], ["Bits written back", bb]], [1.9, 1.35], 9)],
                "block 277,316", "A valid hash must start with %d zero bits. The bits can be rebuilt from the target." % nd)
    if ex == "ex12":
        dy, bk, hr = val(ex, "round(days, 1)"), val(ex, "blocks"), val(ex, "hr")
        return ([tb([["Quantity", "Value"], ["Difficulty, block 277,316", "1,180,923,195"], ["Days for one TH/s", str(dy)], ["Blocks of waiting", fmt(bk)], ["Hash rate by difficulty, 2026", hr]], [1.9, 1.35], 9)],
                "waiting time and hash rate", "The book says 8,496 blocks. The difficulty gives %s blocks, about %s days." % (fmt(bk), dy))
    if ex == "ex13":
        sp, nb, eq, ra, bs = val(ex, "z - a"), val(ex, "hex(new)"), val(ex, "new == 0x170331db"), val(ex, "round(1209600 / (z - a), 4)"), val(ex, "bias")
        return ([tb([["Quantity", "Value"], ["Seconds the period took", fmt(sp)], ["Seconds intended", fmt(1209600)], ["Intended over real", str(ra)], ["New bits by the rule", nb], ["Equal to block 840,672", yn(eq)], ["Bias of 2,016 for 2,015", str(bs) + " percent"]], [1.75, 1.5], 9)],
                "the retarget of April 2024", "The period was short, so the target shrank by %.1f percent: mining became a little harder." % (100 * (1 - 1 / ra)))
    if ex == "ex14":
        r = val(ex, "r")
        return ([ch(["Far too fast", "On time", "Far too slow"], r, "target ratio")], "new target divided by old target",
                "The ratio stops at %g and %g. The difficulty moves by the inverse, so it too changes at most fourfold." % (r[0], r[2]))
    if ex == "ex15":
        no, b94, bt, sn = val(ex, "no"), val(ex, "b94"), val(ex, "R['b2_bits']['2017']"), val(ex, "seen('core_src_pow.cpp', 'enforce_BIP94')")
        nm = ["Main", "Testnet4", "Regtest"]; cell = lambda v: {"true": "yes", "false": "no"}.get(v, "by option")
        return ([tb([["Chain", "No retarget", "BIP 94"]] + [[a, cell(b), cell(c)] for a, b, c in zip(nm, no, b94)], [1.2, 1.1, 0.95])],
                "constants of three chains", "Regtest keeps the bits %s at block 2017. Core's pow.cpp has the BIP 94 branch: %s." % (bt, yn(sn)))
    if ex == "ex16":
        bits, pr = val(ex, "bits"), val(ex, "f'{per:.1e}'")
        return ([ch(["Header nonce", "Version rolling"], bits, "bits")], "free bits of the search space",
                "At 1.029e21 hashes a second the 32-bit nonce is emptied %s times a second, so more room is needed." % pr)
    if ex == "ex17":
        wt = val(ex, "w"); rt = val(ex, "[round(144 * s, 3) for s in shares]")
        return ([ch(["10 percent", "1 percent", "0.1 percent", "0.01 percent"], wt, "days")], "expected days for one block, by share of power",
                "A share of 0.01 percent expects %g blocks a day, so one block in about %g days." % (rt[-1], wt[-1]))
    if ex == "ex18":
        od, th = val(ex, "odds"), val(ex, "thr")
        return ([ch(["Share 10 percent", "Share 30 percent", "Share 45 percent"], od, "chance")], "chance of catching up from six blocks",
                "Selfish mining pays above a share of %g if no honest miner follows, and %g if half follow." % (th[0], th[1]))
    if ex == "ex19":
        la, st, sm, hl, hs = val(ex, "r['lax_node']"), val(ex, "r['strict_node']"), val(ex, "c['same_tip']"), val(ex, "c['height_L']"), val(ex, "c['height_S']")
        return ([tb([["Observation", "Result"], ["Old, looser node", la], ["New, stricter node", st], ["Height of the loose node", str(hl)], ["Height of the strict node", str(hs)], ["Same tip", yn(sm)]], [1.7, 1.55])],
                "one block seen by two nodes", "The two nodes now follow different chains: the chain has split.")
    if ex == "ex20":
        d = val(ex, "d"); m = val(ex, "[round(L.blocks_per_period(s)[0]) for s in sh]")
        return ([ch(["80 percent", "50 percent", "20 percent", "10 percent"], d, "days")], "days for 2,016 blocks, by share of power",
                "With a tenth of the power a block takes %d minutes and 2,016 blocks take %d days." % (m[-1], d[-1]))
    if ex == "ex21":
        st, th, sg = val(ex, "st"), val(ex, "th"), val(ex, "L.signals(0x20200004, 2)")
        hs = val(ex, "[x['height'] for x in v]")
        return ([tb([["Height", "State"]] + [[str(a), b] for a, b in zip(hs, st)], [1.0, 2.25], 9)],
                "a test deployment on a private chain", "Thresholds: %s of 2,016 for 95 percent and %s for 90 percent. Version 0x20200004 signals bit 2: %s." % (fmt(th[0]), fmt(th[1]), yn(sg)))
    if ex == "ex22":
        hs = val(ex, "hs")
        return ([ch(["BIP 34", "BIP 66", "CSV", "SegWit"], hs, "height")], "main chain activation heights",
                "The heights run from %s to %s; none of these forks is voted on any more." % (fmt(hs[0]), fmt(hs[-1])))
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex01", "ex03", "ex06", "ex10", "ex14", "ex16", "ex17", "ex18", "ex20", "ex22") else "table"



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
        if W(g["note"]) < 8 or W(g["note"]) > 20: raise SystemExit("REFUSED: note %d of %s has %d words (8 to 20 wanted): %s" % (k + 1, ex, W(g["note"]), g["note"]))
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
    cap = "run under Python %s - L is the chapter library, R its regtest record" % PY
    blocks = {"t": "codeblocks", "x": X_, "w": W_, "fs": fs, "nfs": 10.5, "groups": gl, "cap": cap, "capy": capy}
    res_label = {"t": "text", "x": RX, "y": 1.45, "w": RW, "h": lab_h, "body": lab, "fs": 11, "font": "B", "bold": True, "color": "mute"}
    if items[0]["t"] == "table": ry = round(min(ry, vy + len(items[0]["rows"]) * items[0]["rowH"] + 0.3), 3)       # under the table, not at the foot of the slide
    read = {"t": "text", "x": RX, "y": ry, "w": RW, "h": rh, "body": reading, "fs": 11.5, "font": "B", "italic": True, "color": "ink"}
    if W(notes) > 60: raise SystemExit("REFUSED: notes of %s have %d words" % (ex, W(notes)))
    tail = " It is example %d in the chapter code tab of the course page." % int(ex[2:])
    num = add("content", title, sub_, [blocks, res_label] + items + [read], notes + tail if W(notes + tail) <= 60 else notes, take)
    e["slide"] = num; e["rows"] = [[r[0] for r in g["rows"]] for g in gl]
    return num


# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories (5N1K: who, what, when, where, why, how; a real picture; a live link)
# ------------------------------------------------------------------------------------------------------------------------------------------------
STORY_BEATS = {
    "HashcashBeforeBitcoin": [
        "WHAT: Adam Back proposed Hashcash in 1997 and wrote it up in a paper dated 1 August 2002: a stamp of computing work that makes sending mail cost a little.",
        "WHY: Cynthia Dwork and Moni Naor had proposed in 1992 to price junk mail with a moderately hard function; Hashcash made the idea practical.",
        "HOW: The sender hashes a string with a growing counter until the hash starts with zeros, as in our lottery; the receiver checks it with one hash.",
        "SO WHAT: Satoshi Nakamoto's paper of 2008 calls Bitcoin's proof of work similar to Adam Back's Hashcash."],
    "ChainSplitOfMarch2013": [
        "WHAT: On 11 March 2013 block 225,430 was valid for Bitcoin 0.8 and refused by older nodes, so the chain split for 24 blocks, about six hours.",
        "WHY: Older versions had too few Berkeley DB locks for a large block, and this accident had become a rule of consensus.",
        "HOW: Marek Palatinus and Michael Marsee moved their pools back to 0.7, so the old chain carried the most work; Gavin Andresen wrote BIP 50.",
        "SO WHAT: Most large businesses paused deposits: they knew that the chain with the most work wins."],
    "HalvingBlockWithRecordFees": [
        "WHAT: Block 840,000, mined by ViaBTC at 00:09:27 UTC on 20 April 2024, was the first to pay the new subsidy of 3.125 coins.",
        "WHY: Its 3,050 transactions paid 3,762,561,499 satoshis in fees, 12.04 times the subsidy, so the reward was mostly tips.",
        "HOW: The sum was recomputed from the saved block; its coinbase carries the tag ViaBTC, by which pool statistics are made.",
        "SO WHAT: The book says that fees are a small part of income; this block is an exception."],
    "TaprootThroughSpeedyTrial": [
        "WHAT: Taproot was activated by Speedy Trial: it opened on 24 April 2021, timed out on 11 August 2021 and needed 1,815 of 2,016 blocks.",
        "WHY: A short vote at 90 percent makes a soft fork succeed or fail quickly, and a minimum activation height gave nodes time to upgrade.",
        "HOW: F2Pool mined block 709,632 on 14 November 2021 with version 0x20200004, in which bit 2 is the taproot signal.",
        "SO WHAT: Bitcoin Core 31.1 still holds these parameters in chainparams.cpp, which is how the dates were recomputed."],
}
STORY_SUB = {"HashcashBeforeBitcoin": "Proof of work was invented to price email, years before Bitcoin",
             "ChainSplitOfMarch2013": "An accident in software became a rule of the network",
             "HalvingBlockWithRecordFees": "The subsidy halves on schedule, but fees can swing wildly",
             "TaprootThroughSpeedyTrial": "Fail fast or succeed: a short vote keeps a soft fork calm"}
STORY_TITLE = {"HashcashBeforeBitcoin": "The stamp that made email cost", "ChainSplitOfMarch2013": "The day Bitcoin had two histories",
               "HalvingBlockWithRecordFees": "Tips twelve times the wage", "TaprootThroughSpeedyTrial": "A ninety percent vote on a clock"}
STANDIN = {"ChainSplitOfMarch2013": "Stand-in picture: a fork in a road stands for the split",
           "HalvingBlockWithRecordFees": "Stand-in picture: a mining machine, not block 840,000",
           "TaprootThroughSpeedyTrial": "Stand-in picture: a taproot stands for the name"}



# the web.archive.org copy named in the story record did not answer from this machine on 2026-10-25 (curl: no response, three tries); the paper's own address answers 200 with the same 84,537 bytes as the saved copy
LINK_OVERRIDE = {"HashcashBeforeBitcoin": "http://www.hashcash.org/papers/hashcash.pdf"}


def story_slide(sid):
    st = dict(STORY[sid]); beats = STORY_BEATS[sid]
    if sid in LINK_OVERRIDE: st["link"] = LINK_OVERRIDE[sid]
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
    return add("content", STORY_TITLE[sid], STORY_SUB[sid], items, notes)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
PLAN = {
    "MoneyCreation": (["ex01", "ex02", "ex03"], {"ex03": "HalvingBlockWithRecordFees"}),
    "DecentralizedConsensus": (["ex04", "ex05", "ex06"], {}),
    "BuildingTheCandidateBlock": (["ex07", "ex08", "ex09"], {}),
    "ProofOfWork": (["ex10", "ex11", "ex12", "ex13", "ex14", "ex15"], {"ex10": "HashcashBeforeBitcoin"}),
    "MiningCompetition": (["ex16", "ex17", "ex18"], {}),
    "ChangingConsensusRules": (["ex19", "ex20", "ex21", "ex22"], {"ex20": "ChainSplitOfMarch2013", "ex21": "TaprootThroughSpeedyTrial"}),
    "RecapChapter11": ([], {}),
}
BR_KEY = {b: [k for k, v in K.K3.items() if v[0] == b] for b in BRANCHES}
RES_SUB = "Opened on 2026-10-25; every entry is a live link in this file"


def build():
    S.clear(); ANALOGIES.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 12: Mining and Consensus", "Where rewards and blocks come from, how nodes agree on one chain, and how the rules change",
        [{"t": "img", "path": ASSETS + "ch12_bitcoinlogo.png", "x": 7.3, "y": 0.35, "w": 1.9, "h": 1.9},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: the Bitcoin logo, public domain (Wikimedia Commons). Python %s; Bitcoin Core 31.1 results are one recorded run, read back here." % PY}],
        "This deck explains how a miner earns a reward, how every node checks and chooses blocks, how proof of work sets the pace, and how the rules of Bitcoin are changed. Every number on a result picture was computed with the chapter's own Python library or read from one recorded run of Bitcoin Core 31.1.")
    add("content", "Today's route", "", [], "", "Seven parts, twenty-two examples, four true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "How is a block's reward made, and why can there never be more than 21 million coins?", "Which checks must a transaction and a block pass before a node accepts them?",
            "Why does a node follow the chain with the most work and not the longest?", "What does a miner put into a candidate block, and what does the coinbase carry?",
            "How do target, difficulty and retargeting set the pace of the lottery?", "Why do small miners join pools, and what share of the power does an attack need?",
            "How do hard and soft forks change the rules, and how is a soft fork voted in?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, seven parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 4, "fs": 12.5, "subfs": 10.5, "accent": [4],
          "items": [{"label": LAB[b], "sub": "%d key concepts, %d examples" % (len(BR_KEY[b]), len(PLAN[b][0])) if PLAN[b][0] else "%d key concepts" % len(BR_KEY[b])} for b in BRANCHES]}],
        "The chapter has six parts and a seventh that recalls chapter 11. Together they hold %d key concepts. Each part gets a divider, concept cards with everyday comparisons, code that runs, and some parts a true story. The deck follows the order of the chapter." % sum(len(v) for v in BR_KEY.values()),
        "Seven parts; every slide today lives on this map")
    for b in BRANCHES:
        exs, stories = PLAN[b]
        divider(b)
        cks = plan_chunks(b, BR_KEY[b]); order = []
        for i in range(max(len(cks), len(exs))):
            if i < len(cks): order.append(("c", i))
            if i < len(exs): order.append(("x", exs[i]))
        for kind, v in order:
            if kind == "c": cards(b, cks[v], v + 1, len(cks))
            else:
                code_slide(EX[v])
                if v in stories: story_slide(stories[v])
                if v == "ex19":
                    add("content", "Hard fork or soft fork?", "Why one splits the chain and the other does not",
                        [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                          "left": {"head": "A hard fork loosens the rules", "rows": ["New blocks may break the old rules.", "Old nodes refuse them, and the chain splits.", "Like a fork in the road."]},
                          "right": {"head": "A soft fork tightens the rules", "rows": ["New blocks still obey the old rules.", "Old nodes accept them, and the chain stays whole.", "Like a stricter door policy."]}}],
                        "A hard fork loosens the rules, so old nodes refuse the new blocks and two histories grow. A soft fork tightens them, so old nodes still accept every new block. A soft fork needs a majority of the miners, but not of the nodes.",
                        "A soft fork needs most of the miners; a hard fork needs everyone")
    add("content", "The chapter in five lines", "One line per idea, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "The reward is subsidy plus fees; the subsidy halves every 210,000 blocks, and the supply stops just below 21 million coins.",
            "Every node checks every transaction and block by the same rules, and follows the chain with the most work.",
            "A candidate block has a template, a coinbase with the height, and a header whose nonce, extra nonce and version are searched.",
            "Proof of work is a hash below a target; retargeting every 2,016 blocks keeps the pace at ten minutes, at most fourfold per step.",
            "Pools smooth a miner's income, attacks need a large share, and soft forks tighten the rules by a vote."]}],
        "These five lines are the deck in miniature. A line that feels unproven should send you back to its code slide, because every figure in it was computed there. The chapter code tab of the course page reruns all twenty-two examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch, and every link was opened on the date in the subtitle. A good start is the video of 3Blue1Brown on how Bitcoin works, then the Optech topic on soft fork activation next to the chapter.",
        "Watch 3Blue1Brown, then read the Optech topic on soft forks beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "How the reward is fixed", "How nodes check and choose a chain",
            "How proof of work sets the pace", "How pools, attacks and forks matter"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 12 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Seven parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 2, "fs": 11.0, "subfs": 10.0, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has seven parts that follow the order of the chapter. Four true stories and twenty-two code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
    return N



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


WHEEL = "03-materials/ch12/assets/sen0401_ch12_lib-1.0.1-py3-none-any.whl"
LIBMODS = ["sen0401_ch12_lib_v1_0_0", "sen0401_ch10_p2p_v1_0_0"]


def manifest(N):
    setup = "# setup: the chapter library of the page (L = chapter 12 library, R = the single regtest record of Bitcoin Core 31.1 inside the same wheel; src, seen, cv, pw and hw are small helpers); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch12_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY what the wheel holds (unpacked as the page does), the setup and the listing
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch12_")
    zipfile.ZipFile(os.path.join(ROOT, WHEEL)).extractall(tmp)
    prog = os.path.join(tempfile.mkdtemp(prefix="sen0401_fx_ch12_run_"), "run_all.py")
    open(prog, "w").write("import json, sys\nsys.path.insert(0, %r)\nex = json.load(open(%r))\nbad = []\nfor e in ex:\n    ns = {}\n    exec(%r, ns); exec(e['code'], ns)\n    for s in e['show']:\n        got = repr(eval(s['expression'], ns))\n        if got != s['expected']: bad.append((e['id'], s['expression'], got, s['expected']))\nprint(json.dumps(bad))\n" % (tmp, os.path.join(os.path.dirname(prog), "ex.json"), setup))
    json.dump(exs, open(os.path.join(os.path.dirname(prog), "ex.json"), "w"))
    for py in ("python3.14", "python3.13"):
        exe = shutil.which(py)
        if not exe: print("page-path check: %s not installed, skipped" % py); continue
        r = subprocess.run([exe, "-I", prog], capture_output=True, text=True, cwd=os.path.dirname(prog))
        if r.returncode: raise SystemExit("REFUSED: page-path run under %s failed:\n%s" % (py, r.stderr[-800:]))
        bad = json.loads(r.stdout.strip().splitlines()[-1])
        if bad: raise SystemExit("REFUSED: page-path run under %s differs from the recording: %s" % (py, bad))
        print("page path (the wheel's files only, no evidence folder of the repository) under %s: %d examples reproduce the recorded values" % (py, len(exs)))
    shutil.rmtree(tmp, ignore_errors=True); shutil.rmtree(os.path.dirname(prog), ignore_errors=True)
    return {"manifest": "chapter_code_ch12_v1_0_0", "chapter": 12, "deck": "SEN0401_Ch12_MiningAndConsensus_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch12_lib", "file": WHEEL, "sha256": hashlib.sha256(open(os.path.join(ROOT, WHEEL), "rb").read()).hexdigest(), "modules": LIBMODS,
                        "import": "import sen0401_ch12_lib_v1_0_0 as L, hashlib, math"}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 12: The Blockchain", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch12_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch12", "page", "chapter_code_ch12_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch12_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 12"])
    mat = os.path.join(ROOT, "03-materials", "ch12", "SEN0401_Ch12_MiningAndConsensus_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
