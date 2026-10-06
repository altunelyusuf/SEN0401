#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - chapter 3 (Bitcoin Core) redesigned for the classroom.

Chapter 3 jumps to the chapter-1 v2.8.0 standard (the CME materials look-and-feel standard
v1.0.0), drawn by the SHARED renderer 08-tooling/deck_render_v1_0_0.js. Everything real:
console rows and program excerpts come from examples_out_v1_1_0.json (deck_check_v1_1_0.py
re-runs whatever the finished file shows), the startup log line and the systemd options come
from the chapter's own evidence capture of a real Bitcoin Core 31.1 node, and the three 5N1K
stories carry fact rows with live links. Long programs appear as honest excerpts - the caption
says 'lines a to b of n' and the checker verifies the excerpt against the full program.

Usage: python3 deck_build_v2_0_0.py   (writes deck_plan_v2_0_0.json beside itself)
"""
__version__ = "2.0.0"

import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load("corpus3", os.path.join(HERE, "..", "sen0401_ch03_corpus_v1_2_0.py"))
ST = load("stories3", os.path.join(HERE, "..", "sen0401_ch03_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch03/assets/"
for _f in ("c3_cointocode.png", "core_logo_128.png", "mbc3_0301.png", "shot_bitcoinqt_0_5_2.png"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v1_1_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV

BYNAME = {n[0]: n for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in EX["groups"].values() for _, out in rows) + " " + \
          " ".join(out for _, out in EX["blocks"].values())
STORYTEXT = " ".join(s["story"] + " " + s["source"] + " " + s["when"] for s in ST.STORIES)


def _sentences(text, k=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:k])


def paras(*names, ask=None):
    for nm in names:
        if nm not in BYNAME:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
    lead = BYNAME[names[0]][5][0][1]
    say = _sentences(lead, 2)
    if len(say) > 480:
        say = _sentences(lead, 1)
    out = "SAY: " + say
    if ask:
        out += "\nASK: " + ask
    out += "\nFULL TEXT: course page, chapter 3 - " + ", ".join(names) + "."
    return out


def decamel(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", n).replace("Json", "JSON").replace("Rpc", "RPC").replace("Api", "API").replace("Cmake", "CMake").replace("Utxo", "UTXO")


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def assert_fact(token, where):
    t = str(token)
    if t in CORPUS_TEXT or t in OUTTEXT or t in STORYTEXT or t.replace(",", "") in OUTTEXT:
        return t
    raise SystemExit("REFUSED: %r (slide %r) is in neither the corpus, the outputs, nor a story" % (t, where))


def bullets_ok(title, items):
    if len(items) > 5:
        raise SystemExit("REFUSED: %r carries %d bullets" % (title, len(items)))
    for b in items:
        if len(b.split()) > 30:
            raise SystemExit("REFUSED: bullet %r on %r reads as a paragraph" % (b, title))
    return items


G = EX["groups"]


def code(group, x, y, w, h, fs=11):
    rr = G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fit = (w - 0.4) / (maxlen * 0.00842)
    fs = min(fs, round(fit, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fin" % (group, w))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


def prog(block, x, y, w, h, fs=10, lines=None, compact=False):
    """A chapter program, whole or as an honest excerpt (lines a to b of n, checker-verified)."""
    src, out = EX["blocks"][block]
    all_lines = src.split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    maxlen = max(max(len(l) for l in shown), (len("result ") + len(out)) if compact else 0)
    nlines = len(shown) + (1 if compact else 0)
    budget = 0.56 if compact else 0.30   # compact keeps result and caption inside the panel
    fit_w = (w - 0.4) / (maxlen * 0.00842)
    fit_h = (h - budget) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit_w, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: %s lines %d-%d cannot fit unwrapped in %.1fx%.1fin" % (block, a, b, w, h))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs,
          "cap": "program %s, lines %d to %d of %d, run under Python %s" % (block, a, b, len(all_lines), PYV),
          "out": out, "block": block, "first": a, "total": len(all_lines)}
    if compact:
        it["compact"] = True
    return it


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return "STORY (%s): %s\nSOURCE: %s" % (st["when"], st["story"], st["source"])


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


# verified figures parsed back out of the executed examples
import ast as _ast
_tags = _ast.literal_eval(G["ReleaseTag"][-1][1]); assert _tags == ["24", "0", "1"]
_hexlen = int(G["GitRepository"][-1][1]); assert _hexlen == 40
_thr = _ast.literal_eval(G["StartupLog"][-1][1]); assert _thr == "16"
_bci = _ast.literal_eval(G["BlockchainInfo"][-1][1]); assert _bci == ("main", 0, True)
_hdr = int(G["BlockHeader"][-1][1]); assert _hdr == 80
_mr = _ast.literal_eval(EX["blocks"]["MerkleRoot"][1]); assert _mr.startswith("0e60651a")
_sub = _ast.literal_eval(EX["blocks"]["SoftwareTesting"][1]); assert _sub[0] == 5000000000
_ids = _ast.literal_eval(EX["blocks"]["TransactionIdentifier"][1]); assert _ids[0] == "466200308696215b"
_desc = _ast.literal_eval(EX["blocks"]["OutputDescriptor"][1]); assert _desc == "#8zl0zxma"

S = []

TAKES = {
    'The questions this chapter answers': 'If you can answer these, chapter 3 is yours',
    'One chapter, eight branches': 'Eight branches - every slide today lives on this map',
    'Version 0.1, set in stone': 'The software came first - the program IS the specification',
    'One program, many postures': 'Same rules, different storage - pruning keeps the checks, drops the history',
    'Clone it, then pick your version by tag': 'A release is a tag; a tag names one exact snapshot',
    'Dozens of builders, one identical binary': "Verify, don't trust - applied to the software itself",
    'From source to bitcoind': 'The build system turns audited text into your node',
    'The log narrates everything the node decides': 'When a node misbehaves, the log already wrote the diagnosis',
    'The project that outlives its keyholders': 'Maintainers change; the repository and its rules remain',
    'Talking to the node: bitcoin-cli and JSON-RPC': 'Every GUI and every explorer speaks this same protocol',
    'Wallets are descriptors now': 'A descriptor states, in one line, what the wallet watches',
    'Decode a real transaction': "The node explains any transaction - Alice's included",
    'The header is 80 bytes of commitment': 'Eighty bytes pin megabytes - that is the whole trick',
    'The chapter as data, and in one library call': 'The course page and your scripts read the same node',
}

def slide(kind, title, sub, items, notes, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg})


def content(title, sub, items, notes, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "bg": "light"}
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
        sl["lede"] = lede
    if take:
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes, image=None):
    items = [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3 if image else 8.6, "h": 1.9,
              "cols": 2 if image else min(4, len(boxes)), "fs": 14, "subfs": 11, "items": boxes}]
    if image:
        items.append(image)
    slide("section", title, sub, items, notes, bg="light")


# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 3: Bitcoin Core", "The reference implementation - download it, verify it, run it, question it",
      [img("c3_cointocode.png", 6.1, 1.15, 3.5, 2.5, cap="from the owner's 2025 deck")],
      "SAY: Chapters 1 and 2 described the system; this chapter hands it to you. By tonight you can "
      "be running the same program that wrote the genesis block's successors.\n"
      "FULL TEXT: course page, chapter 3.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.5,
          "items": [re.sub(r",.*", "?", q) if len(q.split()) > 18 else q for q in C.CQS]}],
        paras("Node"))

content("One chapter, eight branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 4, "fs": 13, "subfs": 10, "accent": [0],
          "items": [{"label": decamel(r), "sub": "%d concepts" % len([n for n in C.NODES if n[3] == r or (n[3] in children(r))])}
                    for r in ("Node", "Build", "Operation", "Interface", "Data", "Ecosystem", "Semantics", "Computing")]}],
        paras("Node", "Build", "Operation", "Interface"),
        lede="Eight branches; the count under each is how many concepts the course page explains for it - today walks the spine.")

# ---- The node ---------------------------------------------------------------------------------
section("The node", "What the reference implementation is, and what it keeps",
        [{"label": "Full node"}, {"label": "Pruned node"}, {"label": "Initial download"}, {"label": "The UTXO set"}],
        paras("Node"),
        image=img("mbc3_0301.png", 6.3, 1.9, 3.3, 2.9, cap="Bitcoin Core architecture - Mastering Bitcoin 3e, CC BY-SA"))

content("Version 0.1, set in stone", STORY["FirstRelease"]["when"],
        [{"t": "news", "x": 0.5, "y": 1.42, "w": 3.1, "h": 2.5, "paper": "The Cryptography List",
          "date": "Friday January 9 2009", "badge": "a download on SourceForge",
          "headline": "Bitcoin v0.1 released"},
         {"t": "beats", "x": 3.95, "y": 1.5, "w": 5.55, "h": 2.0, "fs": 13, "items": [
             "Six days after the genesis block: a runnable Windows program",
             "'The core design was set in stone' - Satoshi, a year later",
             "Everything this chapter runs descends from that program"]},
         img("shot_bitcoinqt_0_5_2.png", 3.95, 3.52, 2.2, 0.8),
         factrow("FirstRelease", x=3.95, y=4.42, w=5.55)],
        story_notes("FirstRelease") + "\nIMAGE: the 0.5.2 GUI (MIT licence) - the same program two years on.")

content("One program, many postures", "Full, pruned, and the set every posture must keep",
        [{"t": "compare", "x": 0.5, "y": 1.6, "w": 9.0, "h": 2.0, "fs": 12,
          "left": {"head": "Full archive", "rows": [
              "Keeps every block since 2009",
              "Serves history to anyone who asks"]},
          "right": {"head": "Pruned", "rows": [
              "Verifies everything, then discards old blocks",
              "550 MB floor - the run checks 5000 >= 550"]}},
         dict(code("PrunedNode", 0.5, 3.85, 4.3, 0.95, fs=9.5), label="pruning's floor, checked"),
         dict(code("InitialDownload", 5.1, 3.85, 4.4, 0.95, fs=9.5), label="IBD: 400 GB at 10 MB/s, in hours")],
        paras("PrunedNode", "InitialDownload", ask="Which posture still enforces every consensus rule? (both - that is the point)"))

# ---- From source to binary --------------------------------------------------------------------
section("From source to binary", "Trust arithmetic, not downloads",
        [{"label": "Clone and tags"}, {"label": "Reproducible builds"}, {"label": "CMake"}, {"label": "Tests"}],
        paras("Build"))

content("Clone it, then pick your version by tag", "The repository is the publication of record",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.15, "fs": 12.5, "steps": [
            {"label": "git clone", "sub": "the whole history"},
            {"label": "git tag", "sub": "list the releases"},
            {"label": "git checkout v...", "sub": "one exact snapshot", "hot": True}]},
         dict(code("GitRepository", 0.5, 3.0, 4.3, 0.95, fs=10), label="a commit name is 40 hex digits"),
         dict(code("ReleaseTag", 5.1, 3.0, 4.4, 0.95, fs=10), label="a tag is just a version, readable"),
         {"t": "chips", "x": 0.5, "y": 4.2, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["stable today: v31.1", "next candidate: v32.0rc3", "book's example: v24.0.1"]}],
        paras("GitRepository", "ReleaseTag", ask="Why does the course pin a commit instead of saying 'latest'?"),
        lede="The chapter corpus itself reads a pinned checkout - commit 05bc2f53 - and the tag list was read live from the public repository on 2026-10-02.")

content("Dozens of builders, one identical binary", STORY["ReproducibleBuilds"]["when"],
        [img("core_logo_128.png", 0.6, 1.6, 1.5, 1.5, cap="the project's own icon (MIT)"),
         {"t": "funnel", "x": 2.5, "y": 1.55, "w": 4.6, "h": 1.8, "cap": "one hash, many signers - a mismatch would betray itself",
          "steps": ["source at the tag", "Guix builds it, bit for bit", "builders compare hashes", "signed attestations, public"]},
         {"t": "stat", "x": 7.3, "y": 1.6, "w": 2.2, "h": 1.7, "vert": True, "items": [
             {"n": "22.0", "label": "first Guix-built release line"}]},
         {"t": "bullets", "x": 0.5, "y": 3.7, "w": 9.0, "h": 0.55, "fs": 12.5, "items": bullets_ok("repro", [
             "The chapter's research re-verified a real release: checksum equal, signatures good, node run"])},
         factrow("ReproducibleBuilds")],
        story_notes("ReproducibleBuilds"))

content("From source to bitcoind", "The build branch, compressed to one slide",
        [{"t": "flow", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.15, "fs": 12.5, "steps": [
            {"label": "cmake -B build", "sub": "configure"},
            {"label": "compile + link", "sub": "the toolchain"},
            {"label": "ctest", "sub": "the suite must pass"},
            {"label": "bitcoind", "sub": "your node", "hot": True}]},
         dict(code("CMakeBuild", 0.5, 2.9, 9.0, 0.8, fs=9.5), label="old autotools flag, new CMake flag - one mapping"),
         dict(prog("SoftwareTesting", 0.5, 3.8, 9.0, 1.12, fs=9, compact=True), label="the test the chapter runs: chapter 1's subsidy staircase, as a unit test")],
        paras("CMakeBuild", "SoftwareTesting", ask="Why does the project treat review and tests as the bottleneck?"))

# ---- Running and talking to it ----------------------------------------------------------------
section("Running and talking to it", "A daemon, a log that explains itself, and one protocol",
        [{"label": "First run"}, {"label": "The daemon"}, {"label": "bitcoin-cli"}, {"label": "JSON-RPC"}],
        paras("Operation"))

content("The log narrates everything the node decides", "A real 31.1 startup, captured for this chapter",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "First run creates the data directory and a config",
            "The log names every subsystem as it wakes",
            "The run reads the real log: 16 worker threads"]},
         dict(code("StartupLog", 4.3, 1.6, 5.2, 1.3, fs=8.5), label="one line of the captured log, parsed"),
         dict(code("Daemon", 0.5, 3.6, 9.0, 1.25, fs=9), label="the systemd unit's own flags, extracted from the pinned source tree")],
        paras("StartupLog", "Daemon", ask="Where would you look first when a node misbehaves? (the answer is this slide's title)"))

content("The project that outlives its keyholders", STORY["MaintainerHandoffs"]["when"],
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Satoshi", "sub": "2009: v0.1"},
            {"label": "Gavin Andresen", "sub": "2011: the handoff"},
            {"label": "W. van der Laan", "sub": "2014: lead maintainer"},
            {"label": "many maintainers", "sub": "today", "hot": True}]},
         {"t": "beats", "x": 0.5, "y": 3.1, "w": 9.0, "h": 1.1, "fs": 13, "items": [
             "The faucet builder of chapter 2 is the 2011 keyholder here",
             "Hundreds of contributors; no one has been indispensable since"]},
         factrow("MaintainerHandoffs")],
        story_notes("MaintainerHandoffs"))

content("Talking to the node: bitcoin-cli and JSON-RPC", "One protocol under every interface",
        [{"t": "flow", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.1, "fs": 12.5, "steps": [
            {"label": "bitcoin-cli", "sub": "or any HTTP client"},
            {"label": "JSON request", "sub": "method + params"},
            {"label": "bitcoind", "sub": "cookie-authenticated"},
            {"label": "JSON answer", "sub": "machine-readable", "hot": True}]},
         dict(code("JsonRpc", 0.5, 2.88, 9.0, 1.05, fs=9.5), label="a real request body, built and read back"),
         {"t": "stat", "x": 0.5, "y": 4.02, "w": 9.0, "h": 0.98, "items": [
             {"n": "'main'", "label": "chain, from the captured getblockchaininfo"},
             {"n": "0", "label": "blocks still to verify"},
             {"n": "True", "label": "initial download complete"}]}],
        paras("JsonRpc", "BitcoinCommand", ask="Your phone wallet never shows this - what is it speaking underneath?"))

content("Wallets are descriptors now", "One line states what the wallet watches",
        [{"t": "compare", "x": 0.5, "y": 1.52, "w": 9.0, "h": 1.7, "fs": 11.5,
          "left": {"head": "Descriptor wallet (today)", "rows": [
              "A readable expression names keys and script type",
              "Ends in a checksum, like an address does"]},
          "right": {"head": "Legacy wallet (retired)", "rows": [
              "A bag of loose keys in a binary file",
              "Removed from current Bitcoin Core"]}},
         dict(prog("OutputDescriptor", 0.5, 3.4, 9.0, 1.58, fs=8, lines=(34, 40), compact=True),
              label="the tail of the chapter's descriptor program - the checksum the node itself confirms")],
        paras("DescriptorWallet", "LegacyWallet", ask="What does the # suffix buy you when you mistype one character?"))

content("Decode a real transaction", "The node explains Alice's payment back to us",
        [{"t": "numlist", "x": 0.5, "y": 1.46, "w": 9.0, "h": 1.18, "fs": 9.5, "items": [
            "Chapter 2 built Alice's payment; here the real node decodes the real thing",
            "Two outputs come back typed: a taproot payment and taproot change",
            "Full parse (version, marker, flag, ins, outs, locktime) = (1, 0, 1, 1, 2, 0); flip one witness byte and (wtxid equal, txid equal) = (False, True)"]},
         dict(code("DecodedTransaction", 0.5, 2.78, 9.0, 0.78, fs=8.5), label="the outputs, as the node reports them"),
         dict(prog("TransactionIdentifier", 0.5, 3.68, 9.0, 1.32, fs=8.5, lines=(44, 48), compact=True),
              label="txid and wtxid, computed from her raw bytes"),
         ],
        paras("DecodedTransaction", "TransactionIdentifier", ask="Which of the two identifiers survives a witness change, and why does that matter?"))

# ---- The chain as data ------------------------------------------------------------------------
section("The chain as data", "Headers, roots, and the same node from your own code",
        [{"label": "The 80-byte header"}, {"label": "Merkle root, recomputed"}, {"label": "Libraries"}, {"label": "Semantics"}],
        paras("Data"))

content("The header is 80 bytes of commitment", "Block 123,456's root, recomputed from its transactions",
        [dict(code("BlockHeader", 0.5, 1.6, 3.4, 0.95, fs=10), label="the six fields, summed"),
         {"t": "stat", "x": 4.2, "y": 1.55, "w": 5.3, "h": 1.1, "items": [
             {"n": "80", "label": "bytes that pin the whole block"},
             {"n": "0e60651a...", "label": "block 123,456's Merkle root, recomputed"}]},
         dict(prog("MerkleRoot", 0.5, 3.0, 9.0, 1.9, fs=9, compact=True), label="the whole program: pair, hash, repeat - against a real block")],
        paras("BlockHeader", "MerkleRoot", ask="Chapter 2 drew this tree with toy leaves - what changed here? (nothing but the data)"))

content("The chapter as data, and in one library call", "Your scripts and the course page read the same node",
        [{"t": "numlist", "x": 0.5, "y": 1.55, "w": 9.0, "h": 0.95, "fs": 9.5, "items": [
            "A wrapper library turns the RPC protocol into one function call",
            "And the course page stores what you just learned as triples with provenance - same discipline"]},
         dict(prog("WrapperLibrary", 0.5, 2.7, 9.0, 1.32, fs=9, compact=True), label="the whole program: the request a library builds for you"),
         {"t": "chips", "x": 0.5, "y": 4.2, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["python-bitcoinlib", "JSON-RPC", "triples", "provenance"]}],
        paras("Semantics") if "Semantics" in BYNAME else paras("Data"))

content("Where to go from here", "Checked 2026-10-06; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["This chapter, free (CC BY-SA)", "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch03_bitcoin-core.adoc"],
                ["Bitcoin Core's own site and releases", "https://bitcoincore.org"],
                ["The source, at any tag", "https://github.com/bitcoin/bitcoin"]]},
            {"head": "Verify & build", "rows": [
                ["Builder attestations (guix.sigs)", "https://github.com/bitcoin-core/guix.sigs"],
                ["Build documentation in-tree", "https://github.com/bitcoin/bitcoin/tree/master/doc"]]},
            {"head": "Talk to a node", "rows": [
                ["RPC reference, every method", "https://developer.bitcoin.org/reference/rpc/"],
                ["Bitcoin Stack Exchange Q&A", "https://bitcoin.stackexchange.com"]]},
            {"head": "History", "rows": [
                ["Bitcoin Core, the project's story", "https://en.wikipedia.org/wiki/Bitcoin_Core"],
                ["Pro Git, free - the tool under it all", "https://git-scm.com/book"]]}]}],
        "SAY: Everything here is free. The homework writes itself: clone, checkout the newest tag, "
        "build, and bring your log's worker-thread line to class.\n"
        "ASK: Who will have a pruned node syncing before Friday?\n"
        "FULL TEXT: course page, chapter 3 - Ecosystem.",
        take="Clone, verify, build, run - the whole chapter is one evening of commands")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "Where the program comes from, and how to pick a version",
          "Why a verified build beats a trusted download",
          "What the daemon writes, and how to ask it anything",
          "How 80 bytes commit to everything beneath them"])}],
      "SAY: Four claims, each carried by something you watched run - a log, a request, a recomputed "
      "root. Next: the keys and addresses that make ownership work.\nFULL TEXT: course page, chapter 3.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "Bitcoin Core descends from v0.1 of 2009 - the program IS the specification",
              "A release is a tag on a public repository; reproducible builds make the binary provable",
              "The node narrates itself: a data directory, a config, and a log that explains decisions",
              "Everything speaks JSON-RPC underneath - your scripts can too, today",
              "80 header bytes commit to the whole chain - the Merkle root we recomputed is the hinge"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 3 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and by tonight, your own node",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d = (_sec[t] for t in ("The node", "From source to binary", "Running and talking to it", "The chain as data"))
_rows = [("Questions and the chapter map", 3, _a),
         ("The node - full, pruned, and the UTXO set", _a + 1, _b),
         ("From source to binary - tags, builds, proofs", _b + 1, _c),
         ("Running and talking to it - logs, RPC, wallets", _c + 1, _d),
         ("The chain as data, summary, and resources", _d + 1, len(S))]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))),
                      "label": "live-run examples, shown with their results"}]}]
S[1]["notes"] = ("SAY: Five parts: by the end you can fetch, verify, build, run and query the reference "
                 "implementation - and every claim on the way arrives with its receipt.\n"
                 "ASK: Who already runs a node? You are today's teaching assistants.\n"
                 "FULL TEXT: course page, chapter 3 - every section.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES and TAKES[sl["title"]]:
        sl["take"] = TAKES[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 3: Bitcoin Core", "sub": "SEN0401, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0)"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
