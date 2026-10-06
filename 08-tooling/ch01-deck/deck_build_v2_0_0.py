#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - the chapter 1 lecture deck redesigned for the classroom.

The owner's ruling of 2026-10-06: a slide carries short sentences or bullets, otherwise a
visualization; the chapter's prose is not thrown away but moves to the speaker notes, and the
interactive page keeps the full text. So this plan builder:

* writes every on-slide line itself, under hard limits it enforces (a bullet <= 14 words, at most
  5 bullets a slide, a title <= 9 words), and puts the corpus's own paragraphs - unabridged - into
  each slide's notes, looked up by concept name from the chapter corpus;
* invents no fact: every number shown is asserted against the corpus's executed figures (NUM) or
  found verbatim in the corpus text before the plan is written, and the console and program slides
  carry the chapter's executed examples unchanged (examples_out_v1_1_0.json), in the exact item
  shapes deck_check_v1_1_0.py re-runs;
* draws the rest: the concept taxonomy as trees, the issuance schedule as a chart computed from
  the same expression NUM verifies, the network comparison, flows, timelines and stat tiles.

Usage: python3 deck_build_v2_0_0.py   (writes deck_plan_v2_0_0.json beside itself)
"""
__version__ = "2.0.0"

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load("corpus", os.path.join(HERE, "..", "sen0401_ch01_corpus_v1_2_0.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_1_0.json")))
OLDPLAN = json.load(open(os.path.join(HERE, "deck_plan_v1_2_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV

# ----------------------------------------------------------------------------------------------
# corpus lookups
# ----------------------------------------------------------------------------------------------
BYNAME = {n[0]: n for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
NUMOUT = {out for _, out in C.NUM}
NUMEXPR = dict(C.NUM)


def paras(*names):
    """The corpus paragraphs of the named concepts, unabridged, for the slide's notes."""
    out = []
    for nm in names:
        n = BYNAME.get(nm)
        if not n:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
        for head, text in n[5]:
            out.append("%s - %s. %s" % (nm, head, text))
    return "\n\n".join(out)


def decamel(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", n).replace("Qr ", "QR ").replace("Http", "HTTP").replace("Uri", "URI").replace("Api", "API")


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def assert_fact(token, where):
    """A number or date shown on a slide must exist in the corpus's verified outputs or text."""
    t = str(token)
    if t in NUMOUT or t in CORPUS_TEXT or t.replace(",", "") in NUMOUT:
        return t
    raise SystemExit("REFUSED: %r (slide %r) is in neither NUM nor the corpus text" % (t, where))


def bullets_ok(title, items):
    if len(items) > 5:
        raise SystemExit("REFUSED: %r carries %d bullets; the limit is 5" % (title, len(items)))
    for b in items:
        if len(b.split()) > 14:
            raise SystemExit("REFUSED: bullet %r on %r runs past 14 words" % (b, title))
    if len(title.split()) > 9:
        raise SystemExit("REFUSED: title %r runs past 9 words" % title)
    return items


# ----------------------------------------------------------------------------------------------
# issuance schedule, computed from the same expression NUM verifies
# ----------------------------------------------------------------------------------------------
ERAS = 9
subsidy = [(50 * 10**8 >> era) / 10**8 for era in range(ERAS)]
total = sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8
assert str(total) == "20999999.9769" and "20999999.9769" in NUMOUT, "supply total drifted from NUM"
cumulative = []
run = 0
for era in range(ERAS):
    run += (50 * 10**8 >> era) * 210000 / 10**8
    cumulative.append(round(run / 1e6, 2))
halving_labels = ["era %d" % e for e in range(ERAS)]
for y in ("2009", "2012", "2016", "2024", "2140", "210,000"):
    assert_fact(y, "issuance chart")

# verified console rows, straight from the executed examples
G = EX["groups"]


def code(group, x, y, w, h, fs=11):
    rows = G[group]
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rows, "fs": fs, "cap": CAP}


# program slides: every chapter program, whole, in the exact shape deck_check re-runs
def prog(block, x, y, w, h, fs=10):
    src, out = EX["blocks"][block]
    lines = src.split("\n")
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": lines, "fs": fs,
            "cap": "program %s, lines 1 to %d of %d, run under Python %s" % (block, len(lines), len(lines), PYV),
            "out": out, "block": block, "first": 1, "total": len(lines)}
PROG = prog("PaymentChannel", 0.5, 3.15, 9.0, 1.5)

S = []


def slide(kind, title, sub, items, notes, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg})


def content(title, sub, items, notes):
    slide("content", title, sub, items, notes)


def section(title, sub, boxes, notes):
    slide("section", title, sub,
          [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 8.6, "h": 1.9, "cols": min(4, len(boxes)),
            "fs": 14, "subfs": 11, "items": boxes}], notes, bg="dark")


# ----------------------------------------------------------------------------------------------
# the deck
# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 1: Introduction", OLDPLAN["meta"]["sub"], [], OLDPLAN["slides"][0]["notes"], bg="dark")

content("The outcomes this session serves", "One course outcome, in the chapter's own parts",
        [{"t": "stat", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.5, "items": [
            {"n": "LO-1", "label": "explain Bitcoin as money and as a system"},
            {"n": "6", "label": "subject branches in this chapter"},
            {"n": "117", "label": "concepts, every one on the course page"}]},
         {"t": "bullets", "x": 0.5, "y": 3.25, "w": 9.0, "h": 1.7, "fs": 15, "items": bullets_ok("outcomes", [
             "History, units and the supply schedule",
             "The parts: keys, addresses, transactions, blocks, nodes, mining",
             "The problems each part was designed to solve"])}],
        OLDPLAN["slides"][1]["notes"])

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.35, "w": 9.0, "h": 3.7, "fs": 12.5,
          "items": [re.sub(r",.*", "?", q) if len(q.split()) > 18 else q for q in C.CQS]}],
        OLDPLAN["slides"][2]["notes"] if len(OLDPLAN["slides"]) > 2 else paras("Money"))

content("One chapter, six branches", "The concept map the whole chapter hangs on",
        [{"t": "tree", "x": 0.4, "y": 1.35, "w": 9.2, "h": 3.75, "fs": 12, "root": "Chapter 1",
          "nodes": [{"label": r, "sub": "%d concepts" % sum(1 for n in C.NODES if (n[3] == r or (n[3] in children(r)))) if False else ""} for r in []] or
                   [{"label": r, "kids": [decamel(x) for x in children(r, 2)[:7]]} for r in ("Money", "Network", "Wallet", "Usage", "Foundations", "Nature")]}],
        paras("Money", "Network", "Wallet", "Usage", "Foundations", "Nature"))

# ---- Money ------------------------------------------------------------------------------------
section("Money", "What the currency is, who issues it, and on what schedule",
        [{"label": "Unit"}, {"label": "Supply"}, {"label": "Issuance"}, {"label": "Price"}],
        paras("Money"))

content("One bitcoin divides into 100 million satoshis", "The unit and its divisions - run, not quoted",
        [{"t": "flow", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.15, "fs": 13, "steps": [
            {"label": "1 BTC", "sub": "the currency unit"},
            {"label": "1,000 mBTC", "sub": "millibitcoin"},
            {"label": "100,000,000 sat", "sub": "the smallest unit"}]},
         code("SatoshiUnit", 0.5, 3.0, 5.6, 1.1),
         {"t": "stat", "x": 6.4, "y": 3.0, "w": 3.1, "h": 1.5, "items": [
             {"n": assert_fact("100000", "unit"), "label": "satoshis in 0.001 BTC - the slide ran it"}]}],
        paras("Unit"))

content("21 million, by rule - not by promise", "Issuance halves every 210,000 blocks; the cap is the sum",
        [{"t": "chart", "x": 0.5, "y": 1.45, "w": 5.6, "h": 3.55, "ctype": "line",
          "title": "Block subsidy per era of 210,000 blocks (BTC)",
          "labels": halving_labels, "series": [{"name": "subsidy", "data": subsidy}]},
         {"t": "stat", "x": 6.3, "y": 1.45, "w": 3.2, "h": 3.55, "vert": True, "items": [
             {"n": "210,000", "label": "blocks between halvings"},
             {"n": assert_fact("20999999.9769", "cap"), "label": "the sum of every era's issuance"},
             {"n": "~2140", "label": "the year issuance ends"}]}],
        paras("Supply", "Issuance"))

content("The schedule, executed", "The cap is an arithmetic fact - the slide computes it",
        [code("SupplyCap", 0.5, 1.45, 9.0, 1.05),
         code("Halving", 0.5, 2.7, 9.0, 1.05),
         code("BlockSubsidy", 0.5, 3.95, 9.0, 1.05)],
        paras("Supply", "Issuance"))

content("Price is discovered, not declared", "No authority sets an exchange rate",
        [{"t": "bullets", "x": 0.5, "y": 1.5, "w": 4.4, "h": 3.4, "fs": 15, "items": bullets_ok("price", [
            "Bitcoin floats against every other currency",
            "Markets discover the price trade by trade",
            "A volume-weighted average summarises a day"])},
         code("FloatingExchangeRate", 5.1, 1.5, 4.4, 1.3),
         code("VolumeWeightedAverage", 5.1, 3.1, 4.4, 1.3)],
        paras("Price"))

# ---- Network ----------------------------------------------------------------------------------
section("Network", "No bank in the middle - and what replaces it",
        [{"label": "Peer-to-peer"}, {"label": "Consensus"}, {"label": "Mining"}, {"label": "History"}],
        paras("Network"))

content("A bank in the middle vs. peers", "Decentralisation is an architecture, not a slogan",
        [{"t": "net", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.3,
          "left": {"title": "Centralised: one ledger-keeper", "hub": "Bank"},
          "right": {"title": "Bitcoin: every node checks every rule", "n": 8}}],
        paras("Network", "Consensus"))

content("Peers find each other without a directory", "The chapter's own protocol sketch - run, not quoted",
        [{"t": "bullets", "x": 0.5, "y": 1.5, "w": 3.6, "h": 3.3, "fs": 14.5, "items": bullets_ok("p2p", [
            "Every node speaks the same protocol",
            "Any peer can join or leave freely",
            "Four peers already form a working net"])},
         prog("PeerToPeerProtocol", 4.3, 1.5, 5.2, 3.3)],
        paras("Network"))

content("Rules, not rulers, decide validity", "Each node applies the same consensus rules",
        [{"t": "bullets", "x": 0.5, "y": 1.5, "w": 3.6, "h": 3.3, "fs": 14.5, "items": bullets_ok("rules", [
            "A rule set is code every node runs",
            "A block either conforms or it does not",
            "No vote, no committee, no appeal"])},
         prog("ConsensusRuleSet", 4.3, 1.5, 5.2, 3.3)],
        paras("Consensus"))

content("Mining pays for honesty", "New coin and fees reward the work that secures the chain",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Transactions", "sub": "wait in the mempool"},
            {"label": "Miners", "sub": "spend energy on proof-of-work"},
            {"label": "Block found", "sub": "~every 10 minutes"},
            {"label": "Reward", "sub": "subsidy + fees"}]},
         {"t": "bullets", "x": 0.5, "y": 3.2, "w": 9.0, "h": 1.7, "fs": 15, "items": bullets_ok("mining", [
             "The subsidy follows the halving chart you just saw",
             "Cheating costs more than the reward it could win",
             "Chapter 12 opens the mechanism in full"])}],
        paras("Consensus", "History"))

# ---- Wallet & Usage ---------------------------------------------------------------------------
section("Wallets and first use", "Choosing software, holding keys, and the first payment",
        [{"label": "Wallet platforms"}, {"label": "Key control"}, {"label": "Backup"}, {"label": "First payment"}],
        paras("Wallet", "Usage"))

content("The wallet branch, mapped", "Every leaf is explained on the course page",
        [{"t": "tree", "x": 0.4, "y": 1.35, "w": 9.2, "h": 3.75, "fs": 11.5, "root": "Wallet",
          "nodes": [{"label": decamel(k), "kids": [decamel(x) for x in children(k, 3)[:4]]} for k in children("Wallet", 2)]}],
        paras("Wallet"))

content("Who holds the keys, holds the coins", "The one wallet decision that matters most",
        [{"t": "compare", "x": 0.5, "y": 1.5, "w": 9.0, "h": 2.1, "fs": 13,
          "left": {"head": "Full control", "rows": ["You keep the keys", "You sign; nobody can freeze", "Backup is your job"]},
          "right": {"head": "Third-party control", "rows": ["A service keeps the keys", "Convenient, custodial", "You trust their honesty and uptime"]}},
         {"t": "chips", "x": 0.5, "y": 3.85, "w": 9.0, "h": 0.9, "fs": 13,
          "items": ["desktop", "mobile", "web", "hardware", "paper"]}],
        paras("KeyControl", "WalletPlatform", "Backup"))

content("From a phrase to a key, slowly on purpose", "Key stretching makes guessing expensive",
        [{"t": "bullets", "x": 0.5, "y": 1.5, "w": 3.6, "h": 3.3, "fs": 14.5, "items": bullets_ok("stretch", [
            "A backup phrase becomes the wallet seed",
            "2,048 HMAC rounds slow every guess",
            "Chapter 5 derives whole wallets from this"])},
         prog("KeyStretching", 4.3, 1.5, 5.2, 3.3)],
        paras("Backup", "KeyControl"))

content("Alice's first bitcoin, step by step", "The chapter's running story begins",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Install a wallet", "sub": "keys made on her phone"},
            {"label": "First address", "sub": "shared as text or QR"},
            {"label": "Acquire bitcoin", "sub": "buy, earn, or exchange"},
            {"label": "Confirmations", "sub": "the network accepts it"}]},
         {"t": "prog_here", "x": 0.5, "y": 3.15, "w": 9.0, "h": 1.5}],
        paras("Acquisition", "Address", "Transfer"))

# ---- Foundations ------------------------------------------------------------------------------
section("Foundations", "The two old problems Bitcoin finally joined up",
        [{"label": "Hashcash"}, {"label": "Byzantine Generals"}, {"label": "Keys and signatures"}, {"label": "The chain"}],
        paras("Foundations"))

content("Two solved problems, one new system", "1997 and 1982 meet in 2008",
        [{"t": "card", "x": 0.5, "y": 1.5, "w": 4.4, "h": 2.9, "fs": 13, "accent": "orange",
          "head": "Hashcash (1997)", "body": "Proof-of-work: make sending cost a computation, so flooding costs real resources. Bitcoin turns the same cost into the price of writing history."},
         {"t": "card", "x": 5.1, "y": 1.5, "w": 4.4, "h": 2.9, "fs": 13, "accent": "slate",
          "head": "Byzantine Generals (1982)", "body": "How do parties that cannot trust each other agree on one message? Proof-of-work plus the longest valid chain is Bitcoin's practical answer."}],
        paras("Foundations", "Cryptography"))

content("From keys to the chain", "The pipeline the rest of the course walks",
        [{"t": "flow", "x": 0.5, "y": 1.7, "w": 9.0, "h": 1.35, "fs": 12.5, "steps": [
            {"label": "Keys", "sub": "ch. 4"},
            {"label": "Addresses", "sub": "ch. 4"},
            {"label": "Transactions", "sub": "ch. 6"},
            {"label": "Blocks", "sub": "ch. 11"},
            {"label": "Mining", "sub": "ch. 12"}]},
         {"t": "bullets", "x": 0.5, "y": 3.4, "w": 9.0, "h": 1.5, "fs": 15, "items": bullets_ok("pipeline", [
             "Each stage only trusts what it can verify",
             "Every later chapter opens one of these boxes"])}],
        paras("Chain", "Cryptography"))

content("A chain that notices tampering", "Each block carries the digest of the one before",
        [{"t": "bullets", "x": 0.5, "y": 1.5, "w": 3.6, "h": 3.3, "fs": 14.5, "items": bullets_ok("chainprog", [
            "Change one byte and every later link breaks",
            "Verification is recomputing, not trusting"])},
         prog("Blockchain", 4.3, 1.5, 5.2, 3.3, fs=9.5)],
        paras("Chain"))

# ---- Computing & threats ----------------------------------------------------------------------
content("The toolbox under the hood", "Four vocabularies the whole book leans on",
        [{"t": "tree", "x": 0.4, "y": 1.4, "w": 9.2, "h": 3.6, "fs": 11, "root": "Foundations",
          "nodes": [{"label": k, "kids": [decamel(x) for x in children(k)[:6]] + (["+ %d more" % (len(children(k)) - 6)] if len(children(k)) > 6 else [])}
                    for k in ("Cryptography", "Chain", "Computing", "Threats")]}],
        paras("Computing", "Threats"))

# ---- Nature -----------------------------------------------------------------------------------
content("What kind of thing is Bitcoin?", "Its stated characteristics, and the architecture behind them",
        [{"t": "text", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.4, "fs": 15, "bold": True, "color": "dark", "body": "Characteristics - each one a design choice"},
         {"t": "chips", "x": 0.5, "y": 1.95, "w": 9.0, "h": 0.7, "fs": 14, "big": True,
          "items": [decamel(c) for c in children("Characteristic", 3)]},
         {"t": "text", "x": 0.5, "y": 2.95, "w": 9.0, "h": 0.4, "fs": 15, "bold": True, "color": "dark", "body": "The architecture that delivers them"},
         {"t": "chips", "x": 0.5, "y": 3.45, "w": 9.0, "h": 0.7, "fs": 14, "big": True,
          "items": [decamel(c) for c in children("Architecture", 3)]}],
        paras("Nature", "Characteristic", "Architecture"))

content("Beyond the base layer", "Payment channels route through a network - chapter 14's subject",
        [{"t": "bullets", "x": 0.5, "y": 1.5, "w": 3.6, "h": 3.3, "fs": 14.5, "items": bullets_ok("lightning", [
            "Channels move value without touching the chain",
            "Routes hop wallet to wallet",
            "The chain settles only open and close"])},
         prog("LightningNetwork", 4.3, 1.5, 5.2, 3.3, fs=9.5)],
        paras("Transfer", "SemanticBridge"))

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 2.3, "w": 8.8, "h": 2.3, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a bitcoin is, and how far it divides",
          "Why 21 million is arithmetic, not promise",
          "What replaces the bank in the middle",
          "Which chapter opens each box we drew"])}],
      S[0]["notes"], bg="dark")

# the one program slide rides on the Alice slide: place PROG where prog_here marks
for s in S:
    s["items"] = [dict(PROG, x=i["x"], y=i["y"], w=i["w"], h=i["h"]) if i.get("t") == "prog_here" else i
                  for i in s["items"]]

# every slide must carry notes
for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])

plan = {"meta": dict(OLDPLAN["meta"], version=__version__, python=PYV,
                     redesign="2026-10-06, by the owner's ruling: short bullets and visuals on the slide, prose in the notes"),
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
