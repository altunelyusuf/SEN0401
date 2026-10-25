#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 10, The Bitcoin Network) - the generator of the chapter 10 deck 2.0.0 (task TK_Ch10_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch08-deck/deck_build_v2_0_0.py.
It writes, from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch10/page/chapter_code_ch10_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the story module sen0401_ch10_stories_v1_2_0.py (five stories with pictures), the recorded executions examples_out_v2_0_0.json (made by examples_run_v2_0_0.py under Python 3.14 over the
contents of the page's wheel), deck_concepts_v2_0_0.py (the 56 key concepts of the research, each with a meaning and one everyday analogy), the research concept list itself (the deck refuses to build when a
label differs) and the resources slide of the previous plan. Every number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the
file is drawn: no text box over 30 words, notes of at most 60 words, no code line over 60 characters with its prompt (a listing never wraps), every key concept of the research on a slide with its analogy.
The manifest is verified through the page path: a fresh interpreter (-I) in a scratch folder holding ONLY the contents of the wheel, running setup + listing of every example under Python 3.14 and 3.13.
Usage: python3.14 deck_build_v2_0_0.py [--render]"""
__version__ = "2.0.0"
import ast, glob, hashlib, importlib.util, json, os, re, shutil, struct, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_0_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.0.0", "2_0_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(sorted(glob.glob(os.path.join(TOOL, "sen0401_ch10_stories_v*.py")), key=vk)[-1], "stories10")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch10/assets/"
WHEEL = "03-materials/ch10/assets/sen0401_ch10_lib-1.0.0-py3-none-any.whl"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v1_1_0.json")))

S, ANALOGIES, FIRST_CODE = [], [], []
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


def research_labels():
    f = sorted(glob.glob(os.path.join(ROOT, "03-materials", "ch10", "rdodi", "sen0401_ch10_research_v*.ttl")), key=vk)[-1]
    labs = re.findall(r"a sen04(?:01|14):PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", open(f, encoding="utf-8").read())
    norm = lambda t: " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in re.sub(r"[^a-z0-9]+", " ", re.sub(r"\([^)]*\)", " ", t.lower())).split())
    seen, out = set(), []
    for l in labs:
        if norm(l) not in seen: seen.add(norm(l)); out.append(l)
    return out


# ------------------------------------------------------------------------------------------------------------------------------------------------
# dividers
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEGS = [(K.SHORT[p], 1.0) for p in K.PARTS]
DIV_NOTES = {
    "WhoIsOnTheNetwork": "The Bitcoin network is a crowd of ordinary computers that follow the same rules. This part shows who they are, what a node says when it first meets another, and which services it offers.",
    "PeersBlocksTransactions": "Here the node finds its first neighbours, keeps a limited set of links, and learns to pass blocks and payments on. We measure how little a compact block needs and where a payment waits.",
    "LightClientsPrivacyTransport": "A phone cannot hold the chain, so it asks. This part follows the question: Merkle paths, the Bloom filter that told on wallets, block filters that turn the question around, and the new encrypted transport.",
}


def strip(part, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = K.PARTS.index(part)
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": i == hot} for i, (lab, f) in enumerate(SEGS)]}


def divider(part):
    groups = K.L2[part]; n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 3 else 11
    its = []
    for pill, mean, ana in groups:
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12 if n <= 3 else 11, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
        ANALOGIES.append({"concept": pill, "analogy": an, "slide": len(S) + 1})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (part, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12 if n <= 3 else 11, "items": its}, strip(part)]
    ANALOGIES.append({"concept": K.LABEL[part], "analogy": K.L1[part], "slide": len(S) + 1})
    return add("section", K.LABEL[part], K.L1[part], items, DIV_NOTES[part])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards: the key concepts of the research
# ------------------------------------------------------------------------------------------------------------------------------------------------
def layout_cards(names, part_no, parts):
    n = len(names); cols = 2 if n == 4 else min(3, n); rows = -(-n // cols); bw = (9.0 - (cols - 1) * 0.16) / cols; fw = bw - 0.3
    avail = (3.5 - (rows - 1) * 0.14) / rows
    for fs in (11.5, 11, 10.5, 10):
        items, need = [], 0
        for nm in names:
            _, mean, ana0 = K.K3[nm]; ana = "Think of " + ana0 + "."
            hA = (EST(nm, fs + 1.5, fw, 0.0088) * (fs + 1.5) + EST(mean, fs, fw) * fs) * 1.22 / 72 + 0.06
            hB = EST(ana, fs, fw) * fs * 1.22 / 72 + 0.04
            items.append({"label": nm, "meaning": mean, "analogy": ana, "hA": round(hA, 3), "hB": round(hB, 3), "hC": 0}); need = max(need, 0.07 + hA + hB + 0.1)
        if need <= avail: return items, cols, fs, avail, need
    return None


def chunks(lst):
    for size in (6, 5, 4):
        k = -(-len(lst) // size); base, rem = divmod(len(lst), k)
        sizes = [base + 1 if i < rem else base for i in range(k)]
        out, i = [], 0
        for s_ in sizes: out.append(lst[i:i + s_]); i += s_
        return out


def cards(part, names, part_no, parts):
    lay = layout_cards(names, part_no, parts)
    if lay is None: raise SystemExit("REFUSED: cards %s do not fit one slide" % names)
    items, cols, fs, avail, need = lay
    for nm, it in zip(names, items):
        for k in ("meaning", "analogy"):
            if W(it[k]) > 30: raise SystemExit("REFUSED: card %s has a frame of over 30 words" % nm)
        if W(it["label"] + " " + it["meaning"]) > 30: raise SystemExit("REFUSED: card %s head frame over 30 words" % nm)
        ANALOGIES.append({"concept": nm, "analogy": K.K3[nm][2] + ".", "slide": len(S) + 1})
    suffix = " (%d of %d)" % (part_no, parts) if parts > 1 else ""
    short = {"WhoIsOnTheNetwork": "Network", "PeersBlocksTransactions": "Peers and blocks", "LightClientsPrivacyTransport": "Light clients"}[part]
    title = "%s: key concepts%s" % (short, suffix)
    names_t = "%d key concepts of the part %s" % (len(names), K.LABEL[part])
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 10." % names_t
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("The handshake: version, then verack", "Two nodes greet each other before anything else", "A node speaks first with version; verack accepts it",
             "Two nodes cannot trade blocks until they have greeted each other. The first message is version, naming the software, the protocol and the chain height. Verack confirms it. This greeting was recorded from Bitcoin Core 31.1 on a test chain."),
    "ex02": ("A message is a 24-byte frame", "Magic, command, length and checksum come before any payload", "Even an empty message has a frame of 24 bytes",
             "Every message starts with the same 24 bytes. The magic tells which network it belongs to, the command names the message, the length says how much follows, and the checksum guards the payload. Verack has no payload at all."),
    "ex03": ("Services: what a node offers", "A bit field in the greeting names the services of a node", "A pruned node drops the NETWORK flag but keeps relaying what it has",
             "Services travel as bits in the greeting. A full node offers NETWORK, meaning it can serve the whole chain. A pruned node has deleted old blocks and so leaves that bit out. Both are recorded from the same run."),
    "ex04": ("DNS seeds hand out addresses", "The first contact of a node that knows nobody", "Eight seeds gave twenty to thirty IPv4 addresses each, for one default port",
             "A new node has no peers, so it asks the DNS seeds that are written into its code. Each seed answered with a different list of reachable nodes. The node then dials them on the default port, 8333, and learns more from there."),
    "ex05": ("addr against addrv2", "How nodes tell each other about other nodes", "addrv2 can carry Tor and I2P addresses; the old addr could not",
             "Nodes gossip addresses to each other. The old addr message has room for IPv4 and IPv6 only. The newer addrv2 gives each address a network id and a length, so longer onion and I2P addresses fit. A reply is capped at a share of the address book."),
    "ex06": ("Connection types and their limits", "Not every link relays everything", "Block-relay-only links carry no payments and no addresses",
             "A node keeps different kinds of links. Full-relay links carry everything. Block-relay-only links carry blocks but no payments and no addresses, which makes them harder to spy on. The limits are constants in the source, read from the saved file."),
    "ex07": ("Headers first: 80 bytes a block", "How a new node syncs the chain", "Two thousand headers per reply; the whole chain of headers is small",
             "A new node asks for headers before blocks. Each header is 80 bytes, and a reply holds up to 2000. In this run two replies carried the whole chain of 2101 headers. The node checks they link up, then downloads the blocks."),
    "ex08": ("Relay by wtxid and the fee filter", "How a payment is announced to a peer", "A fee filter keeps cheap payments away from a peer that does not want them",
             "A node announces a payment by its witness id, not by the plain id. A peer can also say that it wants only payments above a fee rate. In the run, the peer with a filter heard of the dearer payment only."),
    "ex09": ("An orphan waits for its parent", "A payment that arrives before the one it spends", "The node asks the sender for the parent instead of dropping the child",
             "A child payment can arrive before the payment it spends. The node cannot check it yet, so it keeps it aside and asks the sender for the parent. When the parent arrives, both enter the memory pool."),
    "ex10": ("Every node has its own memory pool", "The waiting list is local; the chain state is shared", "Pools may differ between nodes, yet the unspent outputs agree",
             "A memory pool holds payments that are valid but not yet in a block. Each node has its own. In the run one node held six, the other none. The set of unspent outputs, which only blocks change, was identical on both."),
    "ex11": ("Compact blocks: 332 bytes, not 3,062", "BIP 152 sends only what the peer lacks", "The peer rebuilds the block from its own memory pool",
             "A peer already knows most payments of a new block from its memory pool. So the block travels as a header, a short id of 6 bytes per payment, and the few payments the peer cannot have. The saving here is about nine tenths."),
    "ex12": ("The block-finding race", "Why a slow block risks a rival", "A block that travels for a minute has about a one in ten chance of a rival",
             "Blocks arrive at random, on average every ten minutes. While your block is still travelling, someone else may find one. The longer the delay, the likelier the rival. Fast relay therefore matters most to miners."),
    "ex13": ("A parity part rebuilds a lost part", "The idea behind forward error correction", "One extra part, the XOR of the others, repairs any single loss",
             "Forward error correction sends a little extra so that losses can be repaired without asking again. The simplest form is one parity part: the XOR of all others. XOR the survivors with the parity and the lost part appears."),
    "ex14": ("A light client checks a Merkle path", "Proof of a payment without the block", "Three hashes link the payment to the root in the header",
             "A light client keeps only headers. To check a payment it asks a full node for the Merkle path from that payment to the root stored in the header. Recomputing the path and getting the same root proves the payment is in the block."),
    "ex15": ("Double-spend odds by confirmations", "Nakamoto's calculation for an attacker with a share q", "More confirmations make catching up far less likely",
             "An attacker tries to build a longer secret chain. Nakamoto computed the chance of ever catching up from z blocks behind. With ten percent of the hash rate it falls quickly; with thirty percent it stays large for longer."),
    "ex16": ("A toy Bloom filter", "Sixteen bits, three hash functions, two patterns", "The filter says maybe or definitely not; the maybe can be wrong",
             "A Bloom filter sets a few bits for each item added. A test looks at the same bits: if one is clear, the item was definitely not added. If all are set, it may have been. The measured wrong-maybe rate follows the formula roughly."),
    "ex17": ("Bloom filters are off by default", "What changed after the privacy paper", "A node answers filterload only when the operator turned the service on",
             "Bloom filters told full nodes which addresses a wallet owned. Bitcoin Core now keeps the service off. A node run with defaults does not set the BLOOM bit and disconnects a peer that sends filterload. With the option on, the filter works."),
    "ex18": ("Golomb coding sends differences", "The trick behind compact block filters", "Sorted numbers differ by less than they are, so differences take fewer bits",
             "A block filter is a sorted list of hash values. Instead of sending each value, send the first and then only the gaps between neighbours. The gaps are smaller than the numbers, so each needs fewer bits."),
    "ex19": ("Golomb-Rice coding is lossless", "Unary quotient plus a few remainder bits", "Decoding gives back the exact list, in fewer bits",
             "Golomb-Rice coding writes each gap as a quotient in unary followed by p remainder bits. It is lossless: decoding returns the identical list. Here it needs fewer bits than a fixed width, and for a real filter the saving is larger."),
    "ex20": ("A block filter rebuilt without Core", "BIP 158 checked by independent code", "Our own code produced the same filter, the same header and ten of ten vectors",
             "The chapter library rebuilds the basic filter of a block from the block and the scripts it spends, without using Bitcoin Core code. It matched Core's filter and filter header, and it also reproduced all ten test vectors of BIP 158."),
    "ex21": ("Transport v1 shows its magic, v2 hides it", "What an eavesdropper can see on the wire", "Version 2 traffic looks like random bytes",
             "In the old transport the network magic and the word version are plain to see. In version 2 neither appears, and the stream has almost eight bits of entropy per byte, which is what random data looks like. It is encrypted, not authenticated."),
    "ex22": ("Networks a node can reach", "IPv4, IPv6, Tor, I2P and CJDNS", "A node set to Tor reaches only the onion network",
             "A fresh node reaches the Internet over IPv4 and IPv6. A node configured for Tor reaches the onion network only, so its address is not exposed. The chapter library reads both configurations from the recorded run."),
}


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name, **kw: dict({"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                                 "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": True, "dlFs": 9, "dlPos": "outEnd"}, **kw)
    if ex == "ex01":
        seq, hello, magic = val(ex, "seq"), val(ex, "hello"), val(ex, "e['magic']")
        return ([tb([["Field", "Recorded value"], ["Software", hello[0]], ["Protocol", str(hello[1])], ["Chain height", str(hello[2])], ["Magic (test chain)", magic], ["Messages in all", str(len(seq))]], [1.45, 1.8])],
                "the greeting of two nodes", "The first four messages are %s, %s, %s and %s." % tuple(seq[:4]))
    if ex == "ex02":
        parts, ln, magic = val(ex, "parts"), val(ex, "len(f)"), val(ex, "P.MAGIC['main'].hex()")
        return ([tb([["Field", "Bytes", "Value"], ["Magic (main)", "4", parts[0]], ["Command", "12", parts[1]], ["Length", "4", str(parts[2])], ["Checksum", "4", parts[3]], ["Whole frame", str(ln), ""]], [1.2, 0.65, 1.4])],
                "the 24 bytes of a verack", "The main-network magic is %s. Four fields, 24 bytes, and no payload." % magic)
    if ex == "ex03":
        full, pr, names = val(ex, "full"), val(ex, "pruned"), val(ex, "list(P.SERVICE_BITS.values())")
        return ([tb([["Service", "Full node", "Pruned node"]] + [[n, yn(n in full), yn(n in pr)] for n in names], [1.45, 0.85, 0.95], 9)],
                "services in the greeting", "Only the pruned node leaves out %s: it has deleted old blocks." % ", ".join(val(ex, "gone")))
    if ex == "ex04":
        names, n, summ = val(ex, "list(d['answers'])"), val(ex, "n"), val(ex, "(len(n), min(n), max(n), port)")
        lab = [s.rstrip(".").split(".")[-2] for s in names]
        return ([ch(lab, n, "addresses")], "IPv4 addresses per DNS seed", "%d seeds answered with %d to %d addresses each; the default port is %s." % (summ[0], summ[1], summ[2], summ[3]))
    if ex == "ex05":
        c1, c2, nets, ln, cap = val(ex, "a['without']['addr']['count']"), val(ex, "v2['count']"), val(ex, "v2['networks']"), val(ex, "v2['addr_len']"), val(ex, "cap")
        return ([tb([["Message", "Entries", "Detail"], ["addr (old)", str(c1), "no network id"], ["addrv2", str(c2), "network ids %s" % " and ".join(map(str, nets))], ["addrv2 lengths", "", "%s bytes" % " and ".join(map(str, ln))], ["Reply cap", "%s%%" % cap, "of the address book"]], [1.0, 0.65, 1.6])],
                "two address messages", "Network id 1 is IPv4 and 2 is IPv6; longer ids carry Tor and I2P addresses.")
    if ex == "ex06":
        t, lim = val(ex, "t"), val(ex, "(full, ro, total)")
        return ([tb([["Link type", "Tx", "Addr", "Wire"]] + [[r[0], yn(r[1]), yn(r[2]), r[3]] for r in t], [1.5, 0.55, 0.6, 0.6], 9)],
                "links of one node (Tx: payments, Addr: addresses)", "Limits in the source: %s full-relay, %s block-relay-only, %s links in all." % lim)
    if ex == "ex07":
        got, by, hs, ht = val(ex, "got"), val(ex, "[h['first_bytes'], h['second_bytes']]"), val(ex, "h['header_size']"), val(ex, "h['height']")
        return ([tb([["Reply", "Headers", "Bytes"], ["First reply", fmt(got[0]), fmt(by[0])], ["Second reply", fmt(got[1]), fmt(by[1])], ["One header", "1", str(hs)], ["Chain height", fmt(ht), ""]], [1.2, 0.95, 1.1])],
                "headers fetched by a new node", "Each header is %d bytes; the whole chain of %s headers took two replies." % (hs, fmt(ht)))
    if ex == "ex08":
        ff, rates, heard = val(ex, "ff"), val(ex, "rates"), val(ex, "heard")
        return ([tb([["Peer", "Fee filter", "Heard of"], ["Normal peer", "none", "%d of %d" % (heard[0], len(rates))], ["Filtering peer", "%s sat/kvB" % fmt(ff), "%d of %d" % (heard[1], len(rates))], ["Fee rates sent", "%s and %s" % rates, "sat/vB"]], [1.2, 1.25, 0.8])],
                "who is told of which payment", "A filter of %s sat/kvB is 5 sat/vB: the cheaper payment is not announced." % fmt(ff))
    if ex == "ex09":
        early, ask, late = val(ex, "early"), val(ex, "ask"), val(ex, "late")
        return ([tb([["Step", "Result"], ["Child sent first", "child in pool: " + yn(early)], ["Node asks for", "%s (witness tx)" % ask], ["Parent sent", "parent in pool: " + yn(late[0])], ["Afterwards", "child in pool: " + yn(late[1])]], [1.15, 2.1])],
                "the order of events", "The child is kept aside, not dropped; its parent releases it.")
    if ex == "ex10":
        pools, same, n = val(ex, "pools"), val(ex, "same"), val(ex, "m['utxo_count_F']")
        return ([ch(["Pool of node F", "Pool of node G"], pools, "transactions")], "payments waiting in two nodes",
                "Both nodes hold the same %d unspent outputs: %s." % (n, "the chain state agrees" if same else "they differ"))
    if ex == "ex11":
        sz, ids, ratio = val(ex, "sizes"), val(ex, "ids"), val(ex, "ratio")
        return ([ch(["Full block", "Compact block"], [sz[1], sz[0]], "bytes")], "bytes of one block of 13 payments",
                "The compact block is %.1f percent of the size: %d short ids of %d bytes, the coinbase sent whole." % (ratio * 100, ids[0], ids[1]))
    if ex == "ex12":
        d, p = val(ex, "delays"), val(ex, "p")
        return ([ch(["%d s" % v for v in d], [round(v * 100, 2) for v in p], "percent")], "chance of a rival block, percent, by delay",
                "A block that takes %d seconds to travel has a %.1f percent chance of a rival." % (d[-1], p[-1] * 100))
    if ex == "ex13":
        parts, par, lost, rb, got = val(ex, "parts"), val(ex, "par.hex()"), val(ex, "[i + 1 for i, x in enumerate(lost) if x is None]"), val(ex, "L.rebuild(lost, par)[1]"), val(ex, "got")
        rows = [["Part", "Content", "State"]] + [["Part %d" % (i + 1), p.decode(), "lost" if i + 1 in lost else "received"] for i, p in enumerate(parts)]
        rows += [["Parity", par, "received"], ["Rebuilt part %d" % lost[0], rb.decode(), "from the rest"]]
        return ([tb(rows, [1.1, 1.25, 0.9])], "four parts and one parity part", "The message is whole again: %s." % got.decode())
    if ex == "ex14":
        sz, ok, pl, nt = val(ex, "sizes"), val(ex, "ok"), val(ex, "s['path_len']"), val(ex, "s['block_tx_count']")
        return ([ch(["Merkle proof", "Whole block"], [sz[0], sz[1]], "bytes")], "bytes sent to a light client",
                "A path of %d hashes in a block of %d payments reaches the root: %s." % (pl, nt, "match" if ok else "no match"))
    if ex == "ex15":
        q, zs, od = val(ex, "q"), val(ex, "zs"), val(ex, "odds")
        return ([dict(ch([str(z) for z in zs], od[0], "q = %s" % q[0]), series=[{"name": "q = %s" % q[0], "data": [float(v) for v in od[0]]}, {"name": "q = %s" % q[1], "data": [float(v) for v in od[1]]}], dlFs=8)],
                "chance of catching up, by blocks behind", "Orange: attacker share %s. Slate: share %s. After 6 blocks: %.4f and %.4f." % (q[0], q[1], od[0][-1], od[1][-1]))
    if ex == "ex16":
        ok, bs, fm, ff = val(ex, "r['inserted_ok']"), val(ex, "r['bits_set']"), val(ex, "r['fp_measured']"), val(ex, "r['fp_formula']")
        return ([ch(["Measured", "Formula"], [round(fm * 100, 1), round(ff * 100, 1)], "percent")], "false positives, percent",
                "Both patterns are found (%s); %d of 16 bits are set, so strangers sometimes pass." % (yn(ok), bs))
    if ex == "ex17":
        has, gone, got = val(ex, "has"), val(ex, "gone"), val(ex, "got")
        return ([tb([["Question", "Answer"], ["Offers BLOOM by default", yn(has)], ["Peer sends filterload", "disconnected" if gone else "stays"], ["Option on: filter", "%d bytes" % got[0]], ["Option on: matches", "%d of %d payments" % (got[1], got[2])]], [1.85, 1.4])],
                "default node and enabled node", "The default closed the door that leaked addresses.")
    if ex == "ex18":
        so, de, bits, eq = val(ex, "g['sorted']"), val(ex, "g['deltas']"), val(ex, "bits"), val(ex, "g['equal']")
        return ([dict(ch([str(i + 1) for i in range(len(so))], so, "sorted numbers"), series=[{"name": "sorted numbers", "data": [float(v) for v in so]}, {"name": "differences", "data": [float(v) for v in de]}], dlFs=8)],
                "the five numbers (orange) and their differences (slate)", "The largest number needs %d bits, the largest difference %d. Adding back restores the list: %s." % (bits[0], bits[1], yn(eq)))
    if ex == "ex19":
        same, bits, fixed, by = val(ex, "same"), val(ex, "r['bits']"), val(ex, "r['fixed_bits']"), val(ex, "r['bytes']")
        return ([tb([["Coding", "Result"], ["Fixed width", "%d bits" % fixed], ["Golomb-Rice", "%d bits" % bits], ["Coded set", "%d bytes" % by], ["Decoded equals input", yn(same)]], [1.65, 1.6])], "bits for five numbers",
                "Decoding returns the same five numbers, and the coded set is smaller than the fixed width.")
    if ex == "ex20":
        same, per, vec = val(ex, "same"), val(ex, "per"), val(ex, "L.bip158_vectors()")
        return ([tb([["Check", "Result"], ["Filter equals Core's", yn(same[0])], ["Filter header equals", yn(same[1])], ["Elements, bytes", "%d, %d" % (per[0], per[1])], ["Bits per element", str(per[2])], ["BIP 158 vectors", "%d of %d" % vec]], [1.85, 1.4])],
                "the block filter and its checks", "About %d bits per element, and our code agrees with Core." % round(per[2]))
    if ex == "ex21":
        p1, p2, en = val(ex, "p1"), val(ex, "p2"), val(ex, "v2['entropy_first_4096']")
        return ([tb([["Transport", "Magic seen", "'version' seen"], ["v1 (old)", yn(p1[0]), yn(p1[1])], ["v2 (BIP 324)", yn(p2[0]), yn(p2[1])], ["v2 entropy", str(en), "bits per byte"]], [1.1, 0.95, 1.2])],
                "what an eavesdropper sees", "Random data would give 8 bits per byte; the v2 stream gives %s." % en)
    if ex == "ex22":
        a, b = val(ex, "[(x['name'], x['reachable']) for x in nets]"), val(ex, "[(x[0], x[1]) for x in o]")
        return ([tb([["Network", "Fresh node", "Tor node"]] + [[n[0], yn(n[1]), yn(m[1])] for n, m in zip(a, b)], [1.2, 1.0, 1.05])],
                "reachable networks of two nodes", "The Tor node reaches the onion network only, so peers never see its address.")
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex04", "ex10", "ex11", "ex12", "ex14", "ex15", "ex16", "ex18") else "table"


def code_slide(e):
    ex = e["id"]; fs = 10; lh = fs * 1.3 / 72
    title, sub_, take, notes = CODE_TEXT[ex]
    fin = e["final"]; groups = [list(g["lines"]) for g in e["groups"]]
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
    cap = "run under Python %s - L, P, R and src are the chapter library of the page" % PY
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
    "EclipseAtUsenix": ["WHAT: On 12 August 2015, at USENIX Security in Washington, Ethan Heilman and colleagues presented Eclipse Attacks on Bitcoin's Peer-to-Peer Network.",
                        "WHY: An attacker who controls every connection of a victim can feed it a false world and use it for double spending.",
                        "HOW: The attacker needs enough IP addresses to fill the victim's connection slots; the authors measured the cost by simulation and on live nodes.",
                        "SO WHAT: Bitcoin Core now keeps anchor connections and two block-relay-only links, and picks peers from different autonomous systems."],
    "CompactBlockRelay": ["WHAT: On 27 April 2016 BIP 152, Compact Block Relay, was assigned to Matt Corallo; Suhas Daftuar wrote the Bitcoin Core code.",
                          "WHY: A node already knows most payments of a new block from its memory pool, so sending them again wastes time.",
                          "HOW: The block travels as a header, a 6-byte short id per payment and the few payments the peer cannot have, such as the coinbase.",
                          "SO WHAT: In this chapter's run, a block of 13 payments went out as 332 bytes instead of 3,062."],
    "BloomFiltersLeak": ["WHAT: BIP 37 was assigned to Mike Hearn and Matt Corallo on 24 October 2012: light clients send a Bloom filter of their addresses to a node.",
                         "WHY: In 2014 Arthur Gervais and colleagues at ETH Zurich showed that this leaks considerable information about the addresses of the user.",
                         "HOW: BIP 111 added the service bit NODE_BLOOM in 2015, and Bitcoin Core 0.19.0.1 turned the service off by default.",
                         "SO WHAT: In this chapter's run, a default node closed the connection of a peer that sent filterload."],
    "FilterIdeaPost": ["WHAT: On 9 May 2016 a developer writing as bfd posted Committed Bloom filters to the bitcoin-dev mailing list.",
                       "WHY: A Bloom filter makes the client reveal its addresses; the idea was to turn the question around.",
                       "HOW: The full node builds one small filter per block; the client downloads it and tests its own addresses privately.",
                       "SO WHAT: Olaoluwa Osuntokun and Alex Akselrod wrote BIP 157 and 158 with Golomb-coded sets, and our code reproduced all ten vectors."],
    "EncryptionAtLast": ["WHAT: On 8 March 2019 BIP 324, the v2 encrypted transport, was assigned to Dhruv Mehta, Tim Ruffing, Jonas Schnelli and Pieter Wuille.",
                         "WHY: Version 1 sends everything in the clear, so anyone on the path can read it and tell Bitcoin traffic from other traffic.",
                         "HOW: Bitcoin Core 26.0 added v2 as an option and 27.0 made it the default; it encrypts but does not authenticate.",
                         "SO WHAT: In this chapter's run, the v2 stream showed neither the magic bytes nor the word version."],
}
STORY_SUB = {"EclipseAtUsenix": "A node is only as honest as the peers it happens to meet", "CompactBlockRelay": "Do not resend what the receiver already knows",
             "BloomFiltersLeak": "A privacy tool can leak more than it hides", "FilterIdeaPost": "Reverse the question and the leak disappears",
             "EncryptionAtLast": "Defaults decide how private a network is"}
STANDIN = {"EclipseAtUsenix": "Stand-in picture: an eclipse, not the paper.", "CompactBlockRelay": "Stand-in picture: optical fibre, not the BIP.",
           "FilterIdeaPost": "Stand-in picture: Solomon Golomb, whose coding the filter uses.", "EncryptionAtLast": "Stand-in picture: an Enigma machine, not BIP 324."}


def png_size(path):
    with open(path, "rb") as f: head = f.read(32)
    return struct.unpack(">II", head[16:24])


def story_slide(sid):
    st = STORY[sid]; beats = STORY_BEATS[sid]
    for b in beats:
        if W(b) > 30: raise SystemExit("REFUSED: beat of %s has %d words" % (sid, W(b)))
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    cut = lambda s: s[:150].rsplit(",", 1)[0] if len(s) > 150 else s
    pw, ph = png_size(os.path.join(ROOT, "03-materials", "ch10", "assets", st["photo"])); asp = pw / ph
    if asp < 0.85:   iw, ih, bx, bw, bh = 2.3, 2.55, 3.1, 6.4, 2.7           # portrait picture
    elif asp <= 1.8: iw, ih, bx, bw, bh = 3.4, 2.55, 4.1, 5.4, 2.7           # near-square picture
    else:            iw, ih, bx, bw, bh = 4.4, round(max(4.4 / asp, 4.7 / 4.4), 2), 5.1, 4.4, 2.9   # wide picture: a box of at least 8 percent of the slide
    bfs = 11.5 if bw > 5 else 10.5
    items = [{"t": "img", "path": ASSETS + st["photo"], "x": 0.5, "y": 1.4, "w": iw, "h": ih, "cap": st["credit"]},
             {"t": "beats", "x": bx, "y": 1.4, "w": bw, "h": bh, "fs": bfs, "items": beats}]
    if sid in STANDIN:
        if asp > 1.8: items.append({"t": "text", "x": 0.5, "y": round(1.4 + ih + 0.4, 2), "w": iw, "h": 0.36, "body": STANDIN[sid], "fs": 8.5, "font": "B", "italic": True, "color": "mute"})
        else: items.append({"t": "text", "x": bx, "y": 4.17, "w": bw, "h": 0.22, "body": STANDIN[sid], "fs": 9, "font": "B", "italic": True, "color": "mute"})
    items.append({"t": "factrow", "x": 0.5, "y": 4.5, "w": 9.0, "who": cut(st["who"]), "where": cut(st["where"]), "when": st["when"], "link": st["link"], "linkText": st.get("linkLabel") or host})
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
    "WhoIsOnTheNetwork": ["c", "ex01", "ex02", "c", "ex03", "census"],
    "PeersBlocksTransactions": ["c", "ex04", "ex05", "ex06", ("story", "EclipseAtUsenix"), "ex07", "c", "ex08", "ex09", "ex10", "c", "ex11", ("story", "CompactBlockRelay"), "compare", "ex12", "c", "ex13"],
    "LightClientsPrivacyTransport": ["c", "ex14", "ex15", "c", "ex16", "ex17", ("story", "BloomFiltersLeak"), "c", "ex18", "ex19", "ex20", ("story", "FilterIdeaPost"), "c", "ex21", ("story", "EncryptionAtLast"), "ex22"],
}
BR_KEY = {p: [k for k, v in K.K3.items() if v[0] == p] for p in K.PARTS}


def census_slide():
    import sen0401_ch10_lib_v1_0_0 as L
    b = L.bitnodes(); nets = sorted(b["nets"].items(), key=lambda kv: -kv[1])
    facts = ("%s reachable nodes counted; %s run plain Bitcoin Core and %s run Knots." % (fmt(b["total"]), fmt(b["core_plain"]), fmt(b["knots"])))
    facts2 = "%s advertise the encrypted v2 transport; only %s still offer Bloom filters." % (fmt(b["services"]["P2P_V2"]), fmt(b["services"]["BLOOM"]))
    ts = b["timestamp"]
    return add("content", "Who is on the network today", "Reachable nodes by network, from the saved Bitnodes snapshot of 2026-10-15",
               [{"t": "chart", "ctype": "bar", "x": 0.5, "y": 1.5, "w": 5.6, "h": 3.3, "labels": [k for k, _ in nets], "series": [{"name": "nodes", "data": [float(v) for _, v in nets]}], "dataLabels": True, "dlFs": 10, "dlPos": "outEnd"},
                {"t": "text", "x": 6.4, "y": 1.6, "w": 3.1, "h": 1.5, "body": facts, "fs": 12.5, "font": "B", "color": "ink"},
                {"t": "text", "x": 6.4, "y": 3.2, "w": 3.1, "h": 1.0, "body": facts2, "fs": 12.5, "font": "B", "color": "ink"},
                {"t": "text", "x": 6.4, "y": 4.3, "w": 3.1, "h": 0.6, "body": "Recorded, not run on the course page: the snapshot is saved in the research package.", "fs": 10.5, "font": "B", "italic": True, "color": "mute"}],
               "Onion addresses are the largest group of reachable nodes, ahead of IPv4 and I2P. Almost all nodes run Bitcoin Core or its variant Knots. These counts come from one saved snapshot, so treat them as a picture of one day and not as a constant.",
               "A census is a snapshot of one day, not a constant")


def compare_slide():
    return add("content", "Two ways to announce a compact block", "BIP 152 lets each peer choose its mode",
               [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                 "left": {"head": "Low-bandwidth mode", "rows": ["The peer first announces the block.", "We ask for the compact block if we want it.", "Like a waiter who asks before bringing the dish."]},
                 "right": {"head": "High-bandwidth mode", "rows": ["The peer sends the compact block at once.", "It does so before it has fully checked the block.", "Like a courier who runs over with the parcel unasked."]}}],
               "A peer may announce first and wait to be asked, or push the compact block unasked. Pushing saves one round trip, which matters when blocks race. Announcing first wastes nothing on a peer that already has the block.",
               "Pushing saves a round trip; announcing first saves bandwidth")


def build():
    S.clear(); ANALOGIES.clear(); FIRST_CODE.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 10: The Bitcoin Network", "How nodes find each other, pass blocks and payments, and what moved since print",
        [{"t": "img", "path": ASSETS + "ch10_bitcoinlogo.png", "x": 7.3, "y": 0.35, "w": 1.9, "h": 1.9},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: the Bitcoin logo, public domain (Wikimedia Commons). Python %s; Bitcoin Core 31.1 results are recorded, not run here." % PY}],
        "This deck explains how the Bitcoin network works: who is on it, how nodes find each other, and how blocks and payments travel. Every number on a result picture was read from one recorded run of Bitcoin Core 31.1 on a test chain, or computed with the chapter's own Python library.")
    add("content", "Today's route", "", [], "", "Three parts, twenty-two examples, five true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "Who is on the network, and what does a node say when it first meets another?", "How does a new node find its first peers, and how many links does it keep?",
            "How can a block travel in a few hundred bytes, and why does speed matter?", "Where does a payment wait, and what happens to one that arrives before its parent?",
            "How can a phone check a payment without the chain?", "What did Bloom filters leak, and how do block filters turn the question around?",
            "What does the encrypted transport hide, and what does it leave open?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, three parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 3, "fs": 13, "subfs": 10.5, "accent": [1],
          "items": [{"label": K.LABEL[p], "sub": "%d key concepts, %d examples" % (len(BR_KEY[p]), sum(1 for t in PLAN[p] if isinstance(t, str) and t.startswith("ex")))} for p in K.PARTS]}],
        "The chapter has three parts and %d key concepts. Each part gets a divider, concept cards with everyday comparisons, code that runs, and true stories. The deck follows the order of the chapter." % sum(len(v) for v in BR_KEY.values()),
        "Three parts; every slide today lives on this map")
    for p in K.PARTS:
        divider(p)
        cks = chunks(BR_KEY[p]); ci = 0
        for tok in PLAN[p]:
            if tok == "c": cards(p, cks[ci], ci + 1, len(cks)); ci += 1
            elif tok == "census": census_slide()
            elif tok == "compare": compare_slide()
            elif isinstance(tok, tuple): story_slide(tok[1])
            else: code_slide(EX[tok])
        assert ci == len(cks), (p, ci, len(cks))
    add("content", "The chapter in five lines", "One line per group of slides, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "Nodes greet each other with version and verack, in a 24-byte frame, and announce their services.",
            "A new node finds peers by DNS seeds and addr, and keeps eight full-relay and two block-relay-only links.",
            "Headers come first; compact blocks send about a tenth of a block; each node keeps its own memory pool.",
            "A light client checks a Merkle path; Bloom filters leaked addresses, so block filters turn the question around.",
            "Version 2 encrypts peer traffic but does not authenticate it; Tor and I2P hide who is who."]}],
        "These five lines are the deck in miniature. A line that feels unproven should send you back to its code slide, because every figure in it was read from the recorded run or computed there. The chapter code tab of the course page reruns all twenty-two examples.",
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch, and every link was opened on the date in the subtitle. A good start is the USENIX talk on eclipse attacks, then the Optech topic on compact block relay. The course page for chapter 10 carries the full text.",
        "Watch the eclipse talk, then read the Optech topic beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "Who is on the network and how nodes meet", "How blocks and payments travel and wait",
            "How a light client verifies, and what filters leaked", "What the encrypted transport hides"]}],
        "Four claims, each carried by a computation that ran on a slide of this deck. The course page for chapter 10 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Three parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 2, "fs": 11.0, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has three parts that follow the order of the chapter. Five true stories and twenty-two code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
    return N


RES_SUB = "Opened on 2026-10-25; every entry is a live link in this file"


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
            elif t == "links": pass
            else:
                for v in it.get("items", []):
                    if isinstance(v, str): box(v, "slide %d %s" % (i, t))
                    elif isinstance(v, dict): box(" ".join(str(x) for x in v.values()), "slide %d %s" % (i, t))
            for side in ("left", "right"):
                if side in it: box(" ".join(it[side]["rows"]), "slide %d compare" % i)
    text = " ".join(json.dumps(s["items"], ensure_ascii=False) + s["title"] + s["sub"] for s in S).lower()
    allc = research_labels()
    if sorted(allc) != sorted(K.K3): raise SystemExit("REFUSED: deck_concepts differs from the research concept list: %s | %s" % (sorted(set(allc) - set(K.K3)), sorted(set(K.K3) - set(allc))))
    missing = [c for c in allc if c.lower() not in text]
    cov = 100.0 * (len(allc) - len(missing)) / len(allc)
    print("coverage (D11, by key concept label on a slide): %d of %d = %.1f percent; missing: %s" % (len(allc) - len(missing), len(allc), cov, missing))
    ana = {a["concept"] for a in ANALOGIES}
    nona = [c for c in allc if c not in ana]
    print("analogies (D4): %d of %d key concepts carry one; without: %s" % (len(allc) - len(nona), len(allc), nona))
    if bad: raise SystemExit("REFUSED:\n  " + "\n  ".join(bad))
    if missing or nona: raise SystemExit("REFUSED: key concepts missing or without analogy")
    return cov


LIBMODS = ["sen0401_ch10_lib_v1_0_0", "sen0401_ch10_p2p_v1_0_0"]


def manifest(N):
    setup = "# setup: the chapter library of the page (L = chapter 10 library, P = the wire code written independently of Bitcoin Core, R = the recorded run of Bitcoin Core 31.1); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": K.LABEL[e["branch"]], "library": "sen0401_ch10_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY what the wheel holds, the setup and the listing
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch10_")
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
        print("page path (wheel contents only) under %s: %d examples reproduce the recorded values" % (py, len(exs)))
    shutil.rmtree(tmp, ignore_errors=True)
    return {"manifest": "chapter_code_ch10_v1_0_0", "chapter": 10, "deck": "SEN0401_Ch10_TheBitcoinNetwork_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch10_lib", "file": WHEEL, "sha256": hashlib.sha256(open(os.path.join(ROOT, WHEEL), "rb").read()).hexdigest(), "modules": LIBMODS,
                        "import": "import sen0401_ch10_lib_v1_0_0 as L, sen0401_ch10_p2p_v1_0_0 as P"}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 10: The Bitcoin Network", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch10_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch10", "page", "chapter_code_ch10_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch10_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 10"])
    mat = os.path.join(ROOT, "03-materials", "ch10", "SEN0401_Ch10_TheBitcoinNetwork_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
