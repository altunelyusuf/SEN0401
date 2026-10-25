#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 14, Second-Layer Applications) - the generator of the chapter 14 deck 2.0.0 (task TK_Ch14_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch14-deck/deck_build_v2_0_0.py.
It writes, from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch14/page/chapter_code_ch14_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the story module v1_2_0 (four stories with pictures), the recorded executions examples_out_v2_0_0.json (made by examples_run_v2_0_0.py under Python 3.14),
deck_concepts_v2_0_0.py (the 61 key concepts of the research file, each with a meaning and one everyday analogy) and the resources slide of the previous plan. Every number on a result picture is parsed
from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the file is drawn: no text box over 30 words, notes of at most 60 words, no code line over 60
characters with its prompt (a listing never wraps), every key concept of the research on a slide with its analogy.
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


ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch14_stories_v*.py")), key=vk)[-1], "stories14")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
LAB = K.LAB
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch14/assets/"
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
    "Guarantees": "Bitcoin offers guarantees that any application can reuse: no double spend, immutability, timestamps and more. This part lists them, then shows how a digital notary and a crowdfund mix them. We test four of them on a private chain.",
    "ColoredCoins": "A coin can be marked so that it stands for another asset. Three ideas make that work: a seal that opens once, a key that commits to a contract, and a receiver who checks the history himself. We run two of them.",
    "PaymentChannels": "Two people can trade many times and settle once. This part builds a channel step by step: a funding output, refunds, commitments that punish an old state, and a secret that claims a payment. Each step is run on a private chain.",
    "Lightning": "Lightning links channels into a network. We follow a payment through relays, count the fees and the time locks, read an invoice and a packet, and watch a breach being punished. Every number comes from the recorded run or the specification.",
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
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 14." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 14." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("A double spend and the fee", "Two spends of one coin on a private chain", "Only a spend that pays more can replace the first one",
             "No output can be spent twice in the same chain. Core accepted a first spend and refused a second one that paid less. It replaced the first with a second that paid more, and the first then vanished from the waiting pool."),
    "ex02": ("Nonexpiration and accounting", "A transaction signed long ago, and one that pays too much", "A transaction does not expire, and it can never pay out more than it takes in",
             "A transaction signed 150 blocks earlier was still valid, because its input was unspent. A transaction whose outputs exceed its inputs was refused, whatever the signatures said. These are two of the chain's guarantees."),
    "ex03": ("Proof of existence", "A document's hash in an OP_RETURN output", "A hash in a transaction proves that the document existed at that block's date",
             "A transaction can carry the hash of a document in an output that nobody can spend. The script is OP_RETURN and the hash, and the output holds no value. The block that holds the transaction gives the document its date."),
    "ex04": ("Lighthouse: a crowdfund", "Pledges that move only when the goal is met", "Signatures fix the output, so the money moves only when the goal is reached",
             "Two pledges, less the fee, make the goal. One pledge alone is refused, because it pays out more than it takes in. Changing the output breaks the signatures, and a signature over everything stops a pledge that comes too late."),
    "ex05": ("Client-side validation", "A token history that the chain never shows", "The chain holds a commitment, and the receiver checks the history",
             "The history of ACME tokens passes through two transactions. Each one commits to its contract, and a forged contract does not match. Yet nothing in the chain shows that the tokens exist, so the receiver must check the whole history."),
    "ex06": ("Pay to contract", "A tweaked key that commits to a contract", "Only the holder of the contract can reveal the commitment and spend",
             "A public key is tweaked by a contract and looks like any other key. Revealing the key and the contract proves the commitment; a wrong contract fails. The output can be spent only with the tweaked key, never with the plain one."),
    "ex07": ("Emma and Fabian's channel", "A two-of-two output funded by Emma", "The funding output needs both keys, so neither side can spend alone",
             "Emma funds one hour of video, at 1,000 satoshis a second. The funding output is a two-of-two script. Emma alone cannot spend it, and both together can. The witness script begins with a 2 and ends with a 2 and CHECKMULTISIG."),
    "ex08": ("Refunds with falling lock times", "Six signed refunds; the newest becomes valid first", "The newest refund has the lowest lock time, so it can be used first",
             "Emma signed six refunds before funding, each with a lower lock time than the one before. At the start all are refused as not yet final. Six blocks before the newest lock time it is still refused, and five blocks before it is accepted."),
    "ex09": ("Balances move, capacity stays", "A channel of 100 units after three payments", "The two balances always add up to the capacity of the channel",
             "A channel's capacity is fixed when it is funded. Each payment only shifts value from one side to the other, so the sum of the two balances never changes. A payment larger than the sender's balance cannot be made."),
    "ex10": ("A commitment that can be punished", "The delayed output of a commitment transaction", "A cheater waits a thousand blocks, and the victim can act before that",
             "The delayed output has two paths: a revocation key now, or a wait of 1,000 blocks. At 999 confirmations the delayed spend is refused and at 1,000 it is accepted. The revocation path needs both halves of the key."),
    "ex11": ("An HTLC: a secret or the clock", "Who can claim a hash time lock contract, and when", "A secret claims the payment; after the lock height the payer takes it back",
             "The receiver claims the output with the secret and a signature. A wrong secret fails the hash check, and the payer's key cannot claim it. The payer's refund is final only at the lock height, nineteen blocks after funding."),
    "ex12": ("Five nodes, one payment", "Alice pays one bitcoin to Eric through three relays", "Each relay keeps 100,000 satoshis, and Alice pays 300,000 in all",
             "Each hop forwards what the later hops still need. The surcharge over one bitcoin is 200,000 satoshis at Bob, 100,000 at Carol and nothing at Diana. The library works backwards from the last hop and gets the same numbers."),
    "ex13": ("Each hop has less time", "The expiry of the HTLC on each hop", "A relay that learns the secret still has time to claim upstream",
             "Every hop's HTLC expires at a block height. Neighbouring hops differ by 80 blocks, so a relay that pays downstream and learns the secret still has time to claim from upstream. The library rebuilds the same heights."),
    "ex14": ("A hold invoice keeps a payment waiting", "HTLCs pending on four channels, then cancelled", "A payment can wait in flight, and a cancel returns every balance",
             "Eric held back the secret, so the payment stayed pending on all four channels: one HTLC at each end and two at each relay. When Eric cancelled, every balance returned. A later payment of the same kind settled."),
    "ex15": ("The encrypted link of BOLT 8", "The test vector of the specification, rerun", "The handshake outputs equal the values printed in the specification",
             "Lightning nodes talk over an encrypted link. The specification prints a test vector with fixed keys. We rerun the handshake and compare the three outputs, the two acts and the transport key. The sizes are 50, 66 and 39 bytes."),
    "ex16": ("The onion has a fixed size", "The parts of a BOLT 4 packet", "The packet is 1366 bytes whatever the route, so a relay cannot count the hops",
             "A Lightning onion packet holds a version byte, a key, 1,300 bytes of hop data and a check value. Its size is 1366 bytes for a route of any length, with at most twenty hops. A relay cannot tell how far it is from the end."),
    "ex17": ("An invoice carries the hash", "A parsed invoice, and the one printed in BOLT 11", "The secret, hashed once, is the payment hash in the invoice",
             "A node made an invoice for 100,000,000,000 millisatoshis and the library parsed it. It asks 80 blocks for the last hop. The secret, hashed once, equals the payment hash. The invoice in BOLT 11 is dated 1 June 2017."),
    "ex18": ("A channel on the chain", "Opening and closing a channel in two transactions", "Only two transactions touch the chain, however many updates happen between",
             "A channel is opened by one funding transaction and closed by one more. The funding output is a two-of-two script, and the close pays two taproot outputs. Six updates happened off the chain in between."),
    "ex19": ("A breach and its punishment", "The justice transaction, and a fee paid by a child", "A cheater loses the whole channel, and a child can pay the parent's fee",
             "Irene went back to an old state and published it. Hitesh's node saw the breach and its justice transaction took the whole channel. A separate test showed a parent with no fee lifted into a block by a child that paid for both."),
}


SHORT_REASON = {"mempool-script-verify-flag-failed": "script check failed", "bad-txns-in-belowout": "outputs above inputs", "non-final": "not yet final",
                "non-BIP68-final": "wait not over", "missing-inputs": "input spent"}      # the recorded reasons of Core, in words (the raw text is on the slide's last code row)
sr = lambda r: SHORT_REASON.get(r, r)


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    if ex == "ex01":
        fees, low = val(ex, "fees"), val(ex, "low"); gone = not val(ex, "d['first_still_in_mempool']")
        return ([ch(["First spend", "Lower fee", "Higher fee"], fees, "fee in satoshis")], "fee of each spend, in satoshis",
                "The lower fee is refused: %s. The higher fee wins, and the first spend is gone: %s." % (low.split("message: ")[-1], yn(gone)))
    if ex == "ex02":
        wt, al, bad = val(ex, "wait"), val(ex, "n['allowed']"), val(ex, "bad")
        return ([tb([["Guarantee", "Test", "Answer"], ["Nonexpiration", "signed %d blocks ago" % wt, "accepted" if al else "refused"], ["Accounting", "outputs above inputs", sr(bad)]], [1.05, 1.2, 1.0], 9)],
                "two guarantees put to the test", "The old transaction is still valid. The one that pays out more than it takes in is refused with the name %s." % bad)
    if ex == "ex03":
        sz, ok, vl, hg, wn = val(ex, "size"), val(ex, "ok"), val(ex, "p['value']"), val(ex, "p['block_height']"), val(ex, "when")
        return ([tb([["Check", "Result"], ["Hash size, bytes", str(sz)], ["Script is OP_RETURN + hash", yn(ok)], ["Value of the output", str(vl)], ["Block height", str(hg)], ["Block time", wn]], [1.9, 1.35], 9)],
                "the notary output", "The hash is in the chain at block %d, dated %s. The document itself is not in the chain." % (hg, wn[:10]))
    if ex == "ex04":
        gl, al, bo, mv, lt = val(ex, "goal"), val(ex, "alone"), val(ex, "both"), val(ex, "l['output_changed']['reason'].split(' (')[0]"), val(ex, "late")
        return ([tb([["Try", "Result"], ["Pledges less fee = goal", yn(gl)], ["One pledge alone", "refused: " + sr(al)], ["Both pledges", "accepted" if bo else "refused"], ["Output changed", "refused: " + sr(mv)], ["Pledge added late", "accepted" if lt else "refused"]], [1.5, 1.75], 9)],
                "four tries at the fundraiser", "The fundraiser can be spent only with all pledges in and the output unchanged.")
    if ex == "ex05":
        n, o, ok, fk, hd = val(ex, "n"), val(ex, "outs"), val(ex, "ok"), val(ex, "fake"), val(ex, "hidden")
        return ([tb([["Observation", "Result"], ["Transactions in the history", str(n)], ["Outputs it names", str(o)], ["Every commitment matches", yn(ok)], ["Forged contract matches", yn(fk)], ["Tokens visible in the chain", yn(not hd)]], [2.0, 1.25], 9)],
                "the history of the ACME tokens", "The chain shows ordinary outputs only. The receiver must read the history to know what they mean.")
    if ex == "ex06":
        sm, gd, wr, pl, tw, cl = val(ex, "same"), val(ex, "good"), val(ex, "wrong"), val(ex, "plain"), val(ex, "tweaked"), val(ex, "p['contract_len']")
        return ([tb([["Test", "Result"], ["Address equals the plain key's", yn(sm)], ["Reveal with the contract", yn(gd)], ["Reveal with a wrong contract", yn(wr)], ["Spend with the plain key", yn(pl)], ["Spend with the tweaked key", yn(tw)], ["Contract length, bytes", str(cl)]], [2.1, 1.15], 9)],
                "a key tweaked by a contract", "The reveal proves the commitment only for the real contract, and only the tweaked key spends.")
    if ex == "ex07":
        ok, cap, al, bo, fv, sc = val(ex, "ok"), val(ex, "cap"), val(ex, "alone"), val(ex, "both"), val(ex, "c['funding_vsize']"), val(ex, "(s[:2], s[-4:], c['witness_script_len'])")
        return ([tb([["Quantity", "Value"], ["Channel funded, satoshis", fmt(cap)], ["Equals 1,000 x 3,600", yn(ok)], ["Emma alone", "no: " + sr(al)], ["Both sign", yn(bo)], ["Script starts and ends", "%s ... %s" % (sc[0], sc[1])], ["Script size, bytes", str(sc[2])]], [1.5, 1.75], 9)],
                "the funding output of the channel", "Opcode 52 is OP_2 and ae is CHECKMULTISIG: two keys must sign, so Emma cannot run off with the funds.")
    if ex == "ex08":
        lt, st, ea, la = val(ex, "lt"), val(ex, "stuck"), val(ex, "early"), val(ex, "late")
        return ([tb([["Refund", "Lock time", "At the start"]] + [["Refund %d" % (i + 1), str(v), "not yet final" if st == len(lt) else "?"] for i, v in enumerate(lt)], [0.9, 0.95, 1.4], 9)],
                "six refunds signed before funding", "Six blocks early the newest refund is %s; five blocks early it is %s." % (sr(ea), "accepted" if la else "refused"))
    if ex == "ex09":
        lf, tt = val(ex, "left"), val(ex, "tot")
        return ([ch(["Start", "Alice pays 30", "Alice pays 50", "Bob pays 20"], lf, "Alice's balance")], "Alice's balance after each payment",
                "Bob holds the rest each time. The two balances always add up to %d." % list(tt)[0] if isinstance(tt, (set, list)) else "Bob holds the rest each time.")
    if ex == "ex10":
        wt, ea, ok, on, bo = val(ex, "wait"), val(ex, "early"), val(ex, "ok"), val(ex, "one"), val(ex, "both")
        return ([tb([["Test", "Allowed"], ["Delay written in the script", wt[1] + " blocks"], ["Spend at 999 confirmations", "no: " + sr(ea)], ["Spend at 1,000 confirmations", yn(ok)], ["Revoke with one half", yn(on)], ["Revoke with both halves", yn(bo)]], [1.85, 1.4], 9)],
                "the delayed output of a commitment", "The cheater must wait %s blocks, while the victim holding both halves can take the output at once." % wt[1])
    if ex == "ex11":
        ye, ke, wr, rb, la, gp = val(ex, "yes"), val(ex, "key"), val(ex, "h['claim_with_wrong_secret']['reason'].split(' (')[-1].rstrip(')')"), val(ex, "h['refund_before_timeout']['reason']"), val(ex, "late"), val(ex, "gap")
        return ([tb([["Claim", "Allowed"], ["Secret and receiver's key", yn(ye)], ["Secret and payer's key", yn(ke)], ["Wrong secret", "no: hash differs"], ["Refund before the lock", "no: " + sr(rb)], ["Refund at the lock height", yn(la)], ["Blocks from funding to lock", str(gp)]], [1.75, 1.5], 9)],
                "who can claim the HTLC", "The secret opens it for the receiver. The clock opens it for the payer, but only at the lock height.")
    if ex == "ex12":
        a, tf, sm = val(ex, "a"), val(ex, "d[0]"), val(ex, "same")
        return ([ch(["Bob", "Carol", "Diana", "Eric"], a, "satoshis")], "surcharge over one bitcoin that each hop forwards",
                "Alice pays %s satoshis in fees. The surcharge falls to zero at Diana and Eric. The library agrees: %s." % (fmt(tf), yn(sm)))
    if ex == "ex13":
        e, left, gap, same = val(ex, "e"), val(ex, "[x - R['l2']['height_at_payment'] for x in e]"), val(ex, "gap"), val(ex, "calc == e[:3]")
        return ([ch(["Bob", "Carol", "Diana", "Eric"], left, "blocks")], "blocks left until the HTLC of each hop expires",
                "Neighbours differ by %d blocks, and the last two share one expiry. The library agrees: %s." % (gap[0], yn(same)))
    if ex == "ex14":
        cnt, sm, stt = val(ex, "cnt"), val(ex, "same"), val(ex, "h['settled_status']")
        return ([ch(["Alice", "Bob", "Carol", "Diana", "Eric"], cnt, "pending HTLCs")], "payments pending on each node while Eric holds back",
                "The relays carry two HTLCs each, the ends one. After the cancel all balances are back: %s." % yn(sm))
    if ex == "ex15":
        o1, o3, ky, n1, n3, hl = val(ex, "ok1"), val(ex, "ok3"), val(ex, "key"), val(ex, "n1"), val(ex, "n3"), val(ex, "hello")
        return ([tb([["Step", "Matches the specification"], ["Act one (%d bytes)" % n1, yn(o1)], ["Act three (%d bytes)" % n3, yn(o3)], ["Transport key", yn(ky)], ["First message, bytes", str(hl)]], [1.6, 1.65], 9)],
                "the BOLT 8 test vector", "Every output equals the one printed in the specification, so the handshake is implemented as specified.")
    if ex == "ex16":
        pr, sz, fx, tp = val(ex, "parts"), val(ex, "size"), val(ex, "fixed"), val(ex, "top")
        return ([tb([["Part of the packet", "Bytes"], ["Version", str(pr[0])], ["Ephemeral key", str(pr[1])], ["Hop data, 20 hops", fmt(pr[2])], ["Check value", str(pr[3])], ["Total", fmt(sz)], ["Same in the specification", yn(fx and tp)]], [2.05, 1.2], 9)],
                "the BOLT 4 packet", "Hop data takes %s of %s bytes. It is padded, so a short route looks like a long one." % (fmt(pr[2]), fmt(sz)))
    if ex == "ex17":
        pre, cl, ok, md, sp, sa, wn = val(ex, "pre"), val(ex, "cl"), val(ex, "ok"), val(ex, "p['msat']"), val(ex, "L.invoice()['hrp']"), val(ex, "L.invoice()['msat'] // 1000"), val(ex, "when")
        return ([tb([["Field", "Value"], ["Prefix of the test invoice", pre], ["Amount, millisatoshis", fmt(md)], ["Final hop expiry, blocks", str(cl)], ["Secret hashes to the hash", yn(ok)], ["BOLT 11 invoice prefix", sp], ["Its amount, satoshis", fmt(sa)], ["Its date", wn[:10]]], [1.9, 1.35], 9)],
                "two invoices parsed", "The prefix names the chain: lnbcrt is regtest, lnbc is the main chain.")
    if ex == "ex18":
        ty, vl, nc, sc, kd, nn, up, vs = (val(ex, "f['type']"), val(ex, "f['value']"), val(ex, "len(c['outputs'])"), val(ex, "script"), val(ex, "kinds"), val(ex, "n"),
                                          val(ex, "R['l4']['state_before']['num_updates']"), val(ex, "c['vsize']"))
        return ([tb([["Item", "Value"], ["Funding output type", ty.replace("witness_v0_", "")], ["Funding value, BTC", str(vl)], ["Funding script ends with", sc], ["Close outputs", "%d, %s" % (nc, kd[0].replace("witness_v1_", ""))], ["Close size, vbytes", str(vs)], ["Updates in between", str(up)], ["Transactions on the chain", str(nn)]], [1.75, 1.5], 9)],
                "one channel, on the chain", "The chain saw %d transactions. The %d updates in between never touched it." % (nn, up))
    if ex == "ex19":
        cl, ni, ow, gt, pk, pa, bc, pv, cv_ = (val(ex, "close"), val(ex, "len(j['inputs'])"), val(ex, "owed"), val(ex, "got"), val(ex, "pkg"), val(ex, "c6['parent_alone']['reject-reason']"),
                                              val(ex, "c6['both_confirmed']"), val(ex, "c6['parent_vsize']"), val(ex, "c6['child_vsize']"))
        return ([tb([["Item", "Value"], ["Close type", cl], ["Justice inputs", str(ni)], ["Owed, satoshis", fmt(ow)], ["Paid, satoshis", fmt(gt)], ["Parent alone", pa], ["Parent plus child", pk], ["Both confirmed", yn(bc)]], [1.35, 1.9], 9)],
                "the breach and the fee bump", "The cheater lost the whole channel. A child of %d vbytes paid for its parent of %d." % (cv_, pv))
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex01", "ex09", "ex12", "ex13", "ex14") else "table"




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
STORY_BEATS = {
    "PizzaForBitcoins": [
        "WHAT: On 22 May 2010 Laszlo Hanyecz paid 10,000 bitcoins for two pizzas, the first notable retail purchase of physical goods with bitcoin.",
        "WHY: He had offered the coins for a couple of pizzas in a Bitcoin Forum post, and a 19-year-old, Jeremy Sturdivant, took the offer.",
        "HOW: Sturdivant ordered two Papa John's pizzas to Hanyecz's home in Jacksonville and received the coins; the payment settled on the chain.",
        "SO WHAT: A payment on the chain waits for confirmations, which payment channels and Lightning avoid for small payments."],
    "SpillmanChannels": [
        "WHAT: Mike Hearn posted Anti DoS for tx replacement on 17 April 2013, and Jeremy Spillman answered on 20 April with a one-way channel design.",
        "WHY: The first Bitcoin code already let an unrecorded open transaction be replaced until its lock time, and the channel idea grew from that.",
        "HOW: The payer signs larger and larger payments while a refund waits behind a lock time; Hearn and Matt Corallo announced bitcoinj code on 27 June 2013.",
        "SO WHAT: Such channels were safe only with segwit transactions, so Emma's refund is signed before the funding is sent."],
    "PoonDryjaWhitepaper": [
        "WHAT: Joseph Poon and Thaddeus Dryja published a Lightning Network white paper in February 2015; the draft kept on lightning.network is version 0.5.9.2.",
        "WHY: Their summary calls it a decentralized system for instant, high-volume micropayments that removes the risk of trusting third-party custody.",
        "HOW: Lightning Labs launched the network in 2018; the picture shows its cut nodes, from under 100 in 2018 to about 1,500 in 2022.",
        "SO WHAT: The book says the network was first described in February 2015; the word proposed no longer holds."],
    "LightningTorch": [
        "WHAT: On 19 January 2019 the Twitter user hodlonaut began a game-like test of Lightning by sending 100,000 satoshis to a trusted recipient.",
        "WHY: It was a promotional test, passed from one well-known person to the next, to show that the network could carry real payments.",
        "HOW: Each recipient added 10,000 satoshis, 34 cents then, and sent the sum on; Jack Dorsey, Charlie Lee, Elizabeth Stark and Changpeng Zhao took part.",
        "SO WHAT: Each hand-over was an ordinary Lightning payment, with no transaction on the chain for each step."],
}
STORY_SUB = {"PizzaForBitcoins": "The first purchase settled on the chain; small ones now travel off it",
             "SpillmanChannels": "Channels began as a replaced transaction waiting for its lock time",
             "PoonDryjaWhitepaper": "A design on paper took years, soft forks and four teams",
             "LightningTorch": "Satoshis passed hand to hand without touching the chain"}
STORY_TITLE = {"PizzaForBitcoins": "Two pizzas for 10,000 bitcoins", "SpillmanChannels": "The first payment channels",
               "PoonDryjaWhitepaper": "A paper that became a network", "LightningTorch": "Satoshis passed from hand to hand"}
STANDIN = {"PizzaForBitcoins": "Picture: the plaque in a Papa John's shop",
           "SpillmanChannels": "Picture: a later authors' channel diagram",
           "PoonDryjaWhitepaper": "Picture: the network's cut nodes, approximate",
           "LightningTorch": "Picture: Jack Dorsey, 2009, a recipient"}

# the web.archive.org copy named in the story record did not answer from this machine on 2026-10-25 (curl: no response); the original list post answers 200 and is the reply of 20 April 2013
LINK_OVERRIDE = {"SpillmanChannels": "https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2013-April/002433.html"}



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
    "Guarantees": (["ex01", "ex02", "ex03", "ex04"], {"ex01": "PizzaForBitcoins"}),
    "ColoredCoins": (["ex05", "ex06"], {}),
    "PaymentChannels": (["ex07", "ex08", "ex09", "ex10", "ex11"], {"ex07": "SpillmanChannels"}),
    "Lightning": (["ex12", "ex13", "ex14", "ex15", "ex16", "ex17", "ex18", "ex19"], {"ex12": "LightningTorch", "ex13": "PoonDryjaWhitepaper"}),
}
BR_KEY = {b: [k for k, v in K.K3.items() if v[0] == b] for b in BRANCHES}
RES_SUB = "Opened on 2026-10-25; every entry is a live link in this file"



def build():
    S.clear(); ANALOGIES.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 14: Second-Layer Apps", "What the chain guarantees, how a payment channel is built, and how Lightning routes payments",
        [{"t": "img", "path": ASSETS + "ch14_bitcoinlogo.png", "x": 7.3, "y": 0.35, "w": 1.9, "h": 1.9},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: the Bitcoin logo, public domain (Wikimedia Commons). Python %s; Bitcoin Core 31.1 and lnd 0.21.3-beta results are one recorded run, read back here." % PY}],
        "This deck explains what is built on top of Bitcoin: the guarantees of the chain, colored coins, payment channels and the Lightning Network. Every number on a result picture was computed with the chapter's own Python library or read from one recorded run on private test chains.")
    add("content", "Today's route", "", [], "", "Four parts, nineteen examples, four true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "Which guarantees of the chain can an application rely on, and how do two applications mix them?", "How can a coin carry a second meaning, and who checks it?",
            "What does a payment channel put on the chain, and what stays off it?", "How does a revocation key stop a party from cheating with an old state?",
            "How does an HTLC let a secret open a payment and time return it?", "How does Lightning route a payment through strangers and keep the route private?",
            "What does a channel cost, and what does a relay earn?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, four parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 4, "fs": 12.5, "subfs": 10.5, "accent": [],
          "items": [{"label": LAB[b], "sub": "%d key concepts, %d examples" % (len(BR_KEY[b]), len(PLAN[b][0])) if PLAN[b][0] else "%d key concepts" % len(BR_KEY[b])} for b in BRANCHES]}],
        "The chapter has four parts. Together they hold %d key concepts. Each part gets a divider, concept cards with everyday comparisons, code that runs, and some parts a true story. The deck follows the order of the chapter." % sum(len(v) for v in BR_KEY.values()),
        "Four parts; every slide today lives on this map")
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
                if v == "ex09":
                    add("content", "On the chain, or off it?", "Why a channel is cheap and fast, and what it still needs from the chain",
                        [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                          "left": {"head": "On the chain", "rows": ["The funding transaction opens the channel.", "The settlement closes it for good.", "Like the deposit and the final bill."]},
                          "right": {"head": "Off the chain", "rows": ["Signed commitments change the balances.", "No one else sees them, and fees are small.", "Like the running tab in between."]}}],
                        "A channel puts two transactions on the chain, the funding and the settlement. Everything between them stays off the chain as signed commitments. The chain is the court of last resort, which is why each side keeps its latest commitment.",
                        "Two transactions on the chain, and any number of updates between them")
    add("content", "The chapter in five lines", "One line per idea, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "The chain guarantees no double spend, immutability and more, and applications are recipes that mix these guarantees.",
            "Colored coins use a seal, a contract-committing key and client-side checks, so the chain never sees the asset.",
            "A payment channel needs two transactions on the chain, and signed commitments in between.",
            "A revocation key punishes an old state, and an HTLC lets a secret claim a payment before a deadline.",
            "Lightning routes a payment through relays that each keep a fee and have less time than the one before."]}],
        "These five lines are the deck in miniature. A line that feels unproven should send you back to its code slide, because every figure in it was computed there. The chapter code tab of the course page reruns all nineteen examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch, and every link was opened on the date in the subtitle. A good start is the video of CuriousInventor on how Lightning works, then the Optech topic on hash time locked contracts next to the chapter.",
        "Watch CuriousInventor, then read the Optech topic on HTLCs beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What the chain guarantees", "How a channel moves value off the chain",
            "How a secret and a clock settle a payment", "How Lightning routes and punishes cheats"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 14 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Four parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 2, "fs": 11.0, "subfs": 10.0, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has four parts that follow the order of the chapter. Four true stories and nineteen code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
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


WHEEL = "03-materials/ch14/assets/sen0401_ch14_lib-1.0.0-py3-none-any.whl"
LIBMODS = ["sen0401_ch14_lib_v1_0_0", "sen0401_ch10_p2p_v1_0_0", "sen0401_ch14_crypto_v1_0_0"]


def manifest(N):
    setup = "# setup: the chapter library of the page (L = chapter 14 library, R = the single recorded run of Bitcoin Core 31.1 and five lnd 0.21.3-beta nodes on private regtest chains, inside the same wheel; seen finds a passage in a saved source); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch14_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY what the wheel holds (unpacked as the page does), the setup and the listing
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch14_")
    zipfile.ZipFile(os.path.join(ROOT, WHEEL)).extractall(tmp)
    prog = os.path.join(tempfile.mkdtemp(prefix="sen0401_fx_ch14_run_"), "run_all.py")
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
    return {"manifest": "chapter_code_ch14_v1_0_0", "chapter": 14, "deck": "SEN0401_Ch14_SecondLayerApplications_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch14_lib", "file": WHEEL, "sha256": hashlib.sha256(open(os.path.join(ROOT, WHEEL), "rb").read()).hexdigest(), "modules": LIBMODS,
                        "import": "import sys, math, hashlib, datetime\nimport sen0401_ch14_lib_v1_0_0 as L"}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 14: Second-Layer Applications", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch14_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch14", "page", "chapter_code_ch14_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch14_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 14"])
    mat = os.path.join(ROOT, "03-materials", "ch14", "SEN0401_Ch14_SecondLayerApplications_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
