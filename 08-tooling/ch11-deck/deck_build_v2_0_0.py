#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 11, The Blockchain) - the generator of the chapter 11 deck 2.0.0 (task TK_Ch11_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch08-deck/deck_build_v2_0_0.py.
It writes, from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch11/page/chapter_code_ch11_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the story module v1_2_0 (four stories with pictures), the recorded executions examples_out_v2_0_0.json (made by examples_run_v2_0_0.py under Python 3.14),
deck_concepts_v2_0_0.py (the 41 key concepts of the research, each with a meaning and one everyday analogy) and the resources slide of the previous plan. Every number on a result picture is parsed
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


ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch11_stories_v*.py")), key=vk)[-1], "stories11")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
LAB = K.LAB
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch11/assets/"
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
    "BlockAndChain": "A block is a header of 80 bytes and a list of transactions. This part takes the header apart, shows how a block is named, and why changing one old block breaks every later one.",
    "MerkleTrees": "A merkle tree squeezes thousands of transactions into one hash in the header. We build a small tree, follow a proof of a few hashes, and meet the weakness that comes from repeating the last hash.",
    "TestChains": "Bitcoin has more than one chain. Testnet, signet and regtest follow the same rules with different constants, so developers can experiment without real money. We compare them and read their constants.",
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
def chunks(lst, top=4):
    n = len(lst)
    if n == 0: return []
    k = -(-n // top); base, extra = divmod(n, k)
    out, i = [], 0
    for j in range(k):
        size = base + (1 if j < extra else 0); out.append(lst[i:i + size]); i += size
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
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 11." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 11." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("A block is header, count, transactions", "Sizes of the genesis block, rebuilt from the source code", "Header, count byte and transaction make the whole block",
             "The genesis block is the smallest block there is. Its header takes 80 bytes, a count byte says there is one transaction, and the transaction fills the rest. Bitcoin Core on a private chain reports the same total."),
    "ex02": ("Six fields in 80 bytes", "A header of the private chain, cut at fixed places", "Every header has the same six fields in the same order and widths",
             "Version, previous block, merkle root, time, bits and nonce always sit in the same places. Four plus thirty-two plus thirty-two plus three times four make eighty. That fixed size is what makes headers cheap to store and check."),
    "ex03": ("Time, target and difficulty", "Three numbers that the header carries", "Bits is a compressed target; a smaller target means more difficulty",
             "The time field counts seconds since 1970. Median time past takes the middle of eleven timestamps, so a single lying clock cannot move it. Bits packs the target, and difficulty compares it with the easiest target."),
    "ex04": ("The first block quotes a newspaper", "Message, time and name of block zero", "The ten zeros at the start of the name are the proof of work",
             "The creator wrote a newspaper headline into the first block. The block hash, found by trying nonces, starts with ten zero digits. That is the work that made the block expensive to forge."),
    "ex05": ("Hash twice to get the name", "A block is named by the double SHA-256 of its header", "The name is computed again by every node; it is never stored in the block",
             "One SHA-256 gives a different value from the block's name. Only the second hash, taken over the first, equals the hash in the source code. Every node recomputes it, so no one has to trust a stored name."),
    "ex06": ("Height in the coinbase script", "BIP 34 and the hundred-block wait", "A newly mined reward cannot be spent until 100 blocks are on top of it",
             "Since BIP 34 the first bytes of the coinbase script spell the block height. We decode eight recorded scripts and get the heights back. Core refused to spend a reward after 99 confirmations and accepted it after 100."),
    "ex07": ("Changing one block breaks the chain", "Ten headers, one bit flipped", "Alter block 3 and you must mine seven headers again",
             "Each header holds the hash of its parent. Flip a single bit in header 3 and the link of header 4 no longer fits. To make the chain valid again, seven headers must be mined once more."),
    "ex08": ("A fork, and the odds of catching up", "Two children of one parent, and Nakamoto's formula", "A fork ends when one branch grows longer; an attacker's odds fall fast",
             "Two blocks were mined on the same parent at height 511. One more block on the first child made it the active chain. The formula from the white paper shows how fast an attacker with ten percent falls behind."),
    "ex09": ("Pair, hash, repeat", "A merkle tree of four, and of three, transactions", "An odd level is completed by pairing the last hash with itself",
             "Four transaction ids make two hashes, then one root. The root equals the value in the block header. With three ids the last one is repeated, which gives the same number of levels."),
    "ex10": ("A proof of four hashes", "One transaction of sixteen, proved with its siblings", "The proof grows slowly: 16,000 transactions need 14 hashes",
             "To prove one transaction we hand over the sibling hash at each level. Following them upward rebuilds the root in the header. Doubling the block adds a single hash to the proof."),
    "ex11": ("Two lists, one root", "A weakness of the tree and Core's answer", "Core refuses a block whose transaction list repeats a hash",
             "Repeating the last two ids of six transactions gives the same root as the plain list. A block with such a copy therefore looks valid by its header. Core received one in a test and rejected it as a duplicate."),
    "ex12": ("A light client needs 248 bytes", "A merkleblock proof read apart", "A phone can check one payment without the other fifteen transactions",
             "A light client asks a full node for a proof. It gets the header, the number of transactions, five hashes and some flags. Core confirmed that the proof contains exactly the transaction we asked about."),
    "ex13": ("One code base, five chains", "Ports and expected sizes from the source file", "Each chain has its own port, so nodes of different chains never mix",
             "The constants of every chain live in one source file. Each chain listens on its own port. The size of the data a new node must fetch ranges from hundreds of gigabytes to nothing at all."),
    "ex14": ("Testnet allows easy blocks", "The minimum-difficulty rule, read from the source", "Two of the test chains may drop to the easiest difficulty after twenty minutes",
             "Testnet, testnet4 and regtest allow a block at minimum difficulty. That keeps a small test chain moving, but it also let miners flood testnet3. Core's help text now calls testnet3 deprecated."),
    "ex15": ("Addresses show the chain", "Prefixes of the five chains", "A testnet address can never be mistaken for a real one",
             "Mainnet addresses start with bc and legacy version byte 0. All test chains use tb, except regtest with bcrt, and version byte 111. A wallet can reject an address of the wrong chain at once."),
    "ex16": ("Signet: a challenge script", "The doorman's rule, and the bytes that identify the chain", "The four magic bytes are the start of the hash of the challenge",
             "The default signet asks for a signature from one of two keys. Its network magic comes from hashing that script, so a different challenge gives a different network. Challenge 51 means anyone can sign."),
    "ex17": ("Halving every 150 blocks", "Regtest compresses the reward schedule", "Mine 500 blocks in seconds and see the reward halve three times",
             "On regtest the reward halves every 150 blocks, so the whole schedule can be tested in seconds. The library's rule, fed with this number, matches every height that Core recorded."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                      "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}
    NM = ["Main", "Test", "Testnet4", "Signet", "Regtest"]
    if ex == "ex01":
        size, core, tx = val(ex, "size"), val(ex, "core"), val(ex, "g['tx_bytes']")
        return ([ch(["Header", "Count", "Transaction"], [80, size - 80 - tx, tx], "bytes")], "bytes of each part, %d in all" % size,
                "Core's own genesis block on the private chain is also %d bytes." % core)
    if ex == "ex02":
        wd, ln, bits, ver = val(ex, "widths"), val(ex, "len(b)"), val(ex, "h['bits']"), val(ex, "hex(h['version'])")
        return ([ch(["Version", "Previous", "Merkle root", "Time", "Bits", "Nonce"], wd, "bytes")], "bytes per field, %d in all" % ln,
                "The same bytes give the version %s and the compact target %s." % (ver, bits))
    if ex == "ex03":
        wh, mtp, bl, df = val(ex, "when"), val(ex, "mtp"), val(ex, "tg.bit_length()"), val(ex, "round(diff)")
        return ([tb([["Quantity", "Value"], ["Genesis block time", wh], ["Median time past", str(mtp)], ["Easiest target, bits", str(bl)], ["Difficulty of 1903a30c", fmt(df)]], [1.7, 1.55])],
                "time, target and difficulty", "The easiest target has %d bits; the difficulty is how many times smaller a target is." % bl)
    if ex == "ex04":
        z, hs, tm, msg = val(ex, "zeros"), val(ex, "g['hash'][:16]"), val(ex, "g['time']"), val(ex, "msg")
        return ([tb([["Item", "Value"], ["Block hash starts", hs], ["Zero digits at the start", str(z)], ["Time field", str(tm)], ["Message length", "%d characters" % len(msg)]], [1.75, 1.5])],
                "block zero", "The message reads: %s." % msg)
    if ex == "ex05":
        o, t_, eq = val(ex, "once[:12]"), val(ex, "twice[:12]"), val(ex, "twice == g['hash']")
        return ([tb([["Hash of the header", "Starts with"], ["SHA-256 once", o], ["SHA-256 twice", t_], ["Equals Core's source", yn(eq)]], [1.75, 1.5])],
                "one hash and two", "Only the double hash starts with zeros and matches the name in the source.")
    if ex == "ex06":
        hs, ok = val(ex, "heights"), val(ex, "ok")
        return ([ch(hs, hs, "height")], "heights decoded from eight coinbase scripts",
                "Spending after 99 confirmations: %s. After 100: %s." % ("allowed" if ok[0] else "refused", "allowed" if ok[1] else "refused"))
    if ex == "ex07":
        ok, br, mr, oh = val(ex, "ok"), val(ex, "t['broken_links']"), val(ex, "t['must_remine']"), val(ex, "t['own_hash_changed']")
        return ([tb([["Test", "Result"], ["Links that hold, of 9", str(ok)], ["Link broken at header", ", ".join(str(b) for b in br)], ["Headers to mine again", str(mr)], ["Hash of header 3 changed", yn(oh)]], [2.0, 1.25])],
                "one bit flipped in header 3", "The change cannot stay hidden: header %d no longer names its parent." % br[0])
    if ex == "ex08":
        sm, gr, od = val(ex, "same"), val(ex, "grew"), val(ex, "odds")
        return ([ch(["0 behind", "1 behind", "2 behind", "6 behind"], od, "chance")], "chance of catching up, attacker with 10 percent",
                "Both children had one parent: %s. The longer branch became active: %s." % (yn(sm), yn(gr)))
    if ex == "ex09":
        lv, lo, rt = val(ex, "lv"), val(ex, "lo"), val(ex, "root")
        return ([ch(["4: bottom", "4: middle", "4: top", "3: bottom", "3: middle", "3: top"], lv + lo, "hashes")], "hashes per level, 4 and 3 transactions",
                "The rebuilt root equals the one in the header: %s. Three leaves still make three levels." % yn(rt))
    if ex == "ex10":
        sz, gd, ss = val(ex, "size"), val(ex, "good"), val(ex, "sizes")
        return ([ch(["1,024 tx", "4,096 tx", "16,000 tx"], ss, "bytes")], "proof bytes by number of transactions",
                "A path of %d hashes, %d bytes, proves one of 16 transactions; it rebuilds the root: %s." % (sz[0], sz[1], yn(gd)))
    if ex == "ex11":
        sm, no, nm, sb, tip = val(ex, "same"), val(ex, "m['n_original']"), val(ex, "m['n_mutated']"), val(ex, "m['submit_mutated']"), val(ex, "m['tip_is_original']")
        return ([tb([["Observation", "Result"], ["Twin list, same root", yn(sm)], ["Transactions, original", str(no)], ["Transactions, mutated", str(nm)], ["Core's verdict", sb["ok"]], ["Original stayed the tip", yn(tip)]], [1.75, 1.5])],
                "the duplicate weakness", "Same header, different lists: Core must refuse the copy by its content.")
    if ex == "ex12":
        n, k, tot, vf = val(ex, "n"), val(ex, "k"), val(ex, "mb['total']"), val(ex, "R['b4_proof_for_k_of_16']['verify'] == [R['b4_proof_for_k_of_16']['txid']]")
        return ([tb([["Item", "Value"], ["Transactions in the block", str(n)], ["Hashes in the proof", str(k)], ["Proof size, bytes", str(tot)], ["Core confirms the match", yn(vf)]], [1.9, 1.35])],
                "the merkleblock proof", "Five hashes and a header stand in for sixteen transactions.")
    if ex == "ex13":
        pt, gb = val(ex, "ports"), val(ex, "gb")
        return ([ch(NM, pt, "port")], "default port of each chain",
                "Assumed chain size in gigabytes: %s." % ", ".join("%s %d" % (a.lower(), b) for a, b in zip(NM, gb)))
    if ex == "ex14":
        fl, dp, g4 = val(ex, "flags"), val(ex, "dep"), val(ex, "g4")
        return ([tb([["Chain", "Minimum difficulty"]] + [[a, yn(b)] for a, b in zip(NM, fl)], [1.5, 1.75])],
                "may a block drop to the easiest difficulty?", "Core's help calls testnet3 deprecated: %s. Testnet4's genesis hash starts %s." % (yn(dp), g4[:10]))
    if ex == "ex15":
        hr, pp, ad = val(ex, "hrp"), val(ex, "p2pkh"), val(ex, "a[:6]")
        return ([tb([["Chain", "SegWit prefix", "Legacy byte"]] + [[a, h_, str(p)] for a, h_, p in zip(NM, hr, pp)], [1.2, 1.15, 0.9])],
                "address prefixes", "A regtest address made by Core starts with %s." % ad)
    if ex == "ex16":
        ops, ln, mg, ez = val(ex, "ops"), val(ex, "len(c) // 2"), val(ex, "magic"), val(ex, "easy")
        return ([tb([["Item", "Value"], ["Challenge script", "%d-of-%d multisig" % (int(ops[0][3:]), int(ops[3][3:]))], ["Script size, bytes", str(ln)], ["Magic, default signet", mg], ["Magic, challenge 51", ez]], [1.75, 1.5])],
                "the default signet", "The doorman asks for one of two signatures; change the script and the magic changes.")
    if ex == "ex17":
        hv, bt, sm = val(ex, "half"), val(ex, "btc"), val(ex, "same")
        return ([ch(["1", "149", "150", "299", "300", "450"], bt, "coins")], "reward in coins by block height",
                "The reward halves every %d blocks; the rule matches Core's record: %s." % (hv, yn(sm)))
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex01", "ex02", "ex06", "ex08", "ex09", "ex10", "ex13", "ex17") else "table"


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
    cap = "run under Python %s - L is the chapter library of the page, R its regtest record" % PY
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
    "HeadlineInTheGenesisBlock": [
        "WHAT: Satoshi Nakamoto wrote the headline of The Times of 3 January 2009 into the first block: Chancellor on brink of second bailout for banks.",
        "WHY: The text proves the block is not older than that day, and the book adds that it recalls why an independent monetary system matters.",
        "HOW: The chapter rebuilt the block from the constants in chainparams.cpp and hashed it to 000000000019d668; its 50 coins can never be spent.",
        "SO WHAT: A date quoted inside a block proves the block is not older."],
    "TheHashTreeOfRalphMerkle": [
        "WHAT: Ralph Merkle patented the hash tree in 1979; United States patent 4,309,569 was published on 5 January 1982, with Stanford University as assignee.",
        "WHY: A tree of hashes lets one small root vouch for a long list, which is how a block header covers every transaction.",
        "HOW: The 40 transaction ids of block 277,315 were hashed in pairs, six levels up, to the root in its header.",
        "SO WHAT: A small summary can vouch for a large list."],
    "GriefingTheTestnet": [
        "WHAT: On 4 May 2024 Jameson Lopp described how the minimum-difficulty rule of testnet3 let miners create hundreds of blocks in a single day.",
        "WHY: A test network without incentives needs rules against vandals, so testnet4 and BIP 94, written by Fabian Jahr, replaced it.",
        "HOW: BIP 94 notes that three years of blocks were mined in a few weeks; on 15 October 2026 testnet3 stood at height 5,189,394, testnet4 at 156,618.",
        "SO WHAT: Core 31.1 still starts testnet3 but its help says that the support will be removed."],
    "SignetBlocksNeedASignature": [
        "WHAT: BIP 325 defines signet: a block is valid only if it carries a solution to a challenge script, so its creators decide who may make blocks.",
        "WHY: Replace mining by a signature and a test network stays calm, with no flood of blocks.",
        "HOW: The default challenge is a 1-of-2 multisig, and its four magic bytes, 0a03cf40, start the double SHA-256 of that script.",
        "SO WHAT: Core 0.21.0 added it; on 15 October 2026 the tip was at height 326,440, 2.27 times the book's listing."],
}
STORY_SUB = {"HeadlineInTheGenesisBlock": "A newspaper headline nailed into the first block", "TheHashTreeOfRalphMerkle": "One small hash that vouches for a whole list",
             "GriefingTheTestnet": "A test network without incentives gets flooded", "SignetBlocksNeedASignature": "Replace mining by a signature and the test network stays calm"}
STORY_TITLE = {"HeadlineInTheGenesisBlock": "The Times in the first block", "TheHashTreeOfRalphMerkle": "Ralph Merkle's hash tree", "GriefingTheTestnet": "When the sandbox was flooded",
               "SignetBlocksNeedASignature": "A test network with a doorman"}
STANDIN = {"HeadlineInTheGenesisBlock": "Stand-in picture: a statue, not the creator (unknown)",
           "GriefingTheTestnet": "Stand-in picture: a sandpit stands for the test network",
           "SignetBlocksNeedASignature": "Stand-in picture: a signet ring stands for the signature"}


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
    return add("content", STORY_TITLE[sid], STORY_SUB[sid], items, notes)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
PLAN = {
    "BlockAndChain": (["ex01", "ex02", "ex03", "ex04", "ex05", "ex06", "ex07", "ex08"], {"ex04": "HeadlineInTheGenesisBlock"}),
    "MerkleTrees": (["ex09", "ex10", "ex11", "ex12"], {"ex10": "TheHashTreeOfRalphMerkle"}),
    "TestChains": (["ex13", "ex14", "ex15", "ex16", "ex17"], {"ex14": "GriefingTheTestnet", "ex16": "SignetBlocksNeedASignature"}),
}
BR_KEY = {b: [k for k, v in K.K3.items() if v[0] == b] for b in BRANCHES}
RES_SUB = "Opened on 2026-10-25; every entry is a live link in this file"


def build():
    S.clear(); ANALOGIES.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 11: The Blockchain", "How a block is built, how blocks are linked, how a merkle tree vouches for them, and which chain to test on",
        [{"t": "img", "path": ASSETS + "ch11_bitcoinlogo.png", "x": 7.3, "y": 0.35, "w": 1.9, "h": 1.9},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: the Bitcoin logo, public domain (Wikimedia Commons). Python %s; Bitcoin Core 31.1 results are one recorded run, read back here." % PY}],
        "This deck explains what a block is, how blocks are chained and named, how a merkle tree summarises transactions, and how Bitcoin's test chains differ. Every number on a result picture was computed with the chapter's own Python library or read from one recorded run of Bitcoin Core 31.1.")
    add("content", "Today's route", "", [], "", "Three parts, seventeen examples, four true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "Which six fields make the 80-byte header of a block?", "How is a block named, and where in the chain is it?",
            "Why does changing one old block break every later one?", "How can one root hash stand for thousands of transactions?",
            "How short is the proof that one transaction is in a block?", "How do testnet, signet and regtest differ, and when do I use each?",
            "Why did testnet4 replace testnet3?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, three parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 3, "fs": 14, "subfs": 11.5, "accent": [1],
          "items": [{"label": LAB[b], "sub": "%d key concepts, %d examples" % (len(BR_KEY[b]), len(PLAN[b][0]))} for b in BRANCHES]}],
        "The chapter has three parts and %d key concepts. Each part gets a divider, concept cards with everyday comparisons, code that runs, and true stories. The deck follows the order of the chapter." % sum(len(v) for v in BR_KEY.values()),
        "Three parts; every slide today lives on this map")
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
    add("content", "The chapter in five lines", "One line per idea, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A block is an 80-byte header of six fields plus its transactions; its name is the double hash of the header.",
            "Each header names its parent, so changing one old block breaks every later link; a fork ends when one branch is longer.",
            "A merkle tree puts all transactions under one root, and a path of a few hashes proves one of them.",
            "The tree has a known weakness: repeating the last hash can give two lists one root, and Core refuses the copy.",
            "Testnet, signet and regtest share the rules with other constants; each serves another stage of development."]}],
        "These five lines are the deck in miniature. A line that feels unproven should send you back to its code slide, because every figure in it was computed there. The chapter code tab of the course page reruns all seventeen examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch, and every link was opened on the date in the subtitle. A good start is the visual blockchain demo by Anders Brownworth, then the Optech topic on merkle tree vulnerabilities next to the chapter.",
        "Watch the Brownworth demo, then read the Optech topic beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "How a block is built and named", "Why the chain resists change",
            "How a merkle proof works and where it is weak", "Which test chain to use, and when"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 11 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Three parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 2, "fs": 11.5, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has three parts that follow the order of the chapter. Four true stories and seventeen code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
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


WHEEL = "03-materials/ch11/assets/sen0401_ch11_lib-1.0.0-py3-none-any.whl"
LIBMODS = ["sen0401_ch11_lib_v1_0_0", "sen0401_ch10_p2p_v1_0_0"]


def manifest(N):
    setup = "# setup: the chapter library of the page (L = chapter 11 library, R = the single regtest record of Bitcoin Core 31.1 inside the same wheel); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch11_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY what the wheel holds (unpacked as the page does), the setup and the listing
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch11_")
    zipfile.ZipFile(os.path.join(ROOT, WHEEL)).extractall(tmp)
    prog = os.path.join(tempfile.mkdtemp(prefix="sen0401_fx_ch11_run_"), "run_all.py")
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
    return {"manifest": "chapter_code_ch11_v1_0_0", "chapter": 11, "deck": "SEN0401_Ch11_TheBlockchain_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch11_lib", "file": WHEEL, "sha256": hashlib.sha256(open(os.path.join(ROOT, WHEEL), "rb").read()).hexdigest(), "modules": LIBMODS,
                        "import": "import sen0401_ch11_lib_v1_0_0 as L, hashlib"}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 11: The Blockchain", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch11_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch11", "page", "chapter_code_ch11_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch11_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 11"])
    mat = os.path.join(ROOT, "03-materials", "ch11", "SEN0401_Ch11_TheBlockchain_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
