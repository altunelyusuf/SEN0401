#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - chapter 2 (How Bitcoin Works) redesigned for the classroom.

The chapter-2 deck jumps to the chapter-1 v2.8.0 standard (recorded as the CME materials
look-and-feel standard, v1.0.0): numbered slides on one warm-ivory theme, short sentences under
hard word gates, every code example with plain-language steps and its executed RESULT shown,
native charts with data labels on real axes, 5N1K stories with real pictures and fact rows,
an agenda with exact slide ranges, a summary before the live-linked resources, and the
three-role review recorded beside this builder. Drawn by the SHARED renderer
08-tooling/deck_render_v1_0_0.js so chapters 1-5 carry one look.

Facts: every number shown is asserted against the chapter corpus text, the executed examples
(examples_out_v1_2_0.json - re-run off the finished file by deck_check_v1_2_0.py), or the story
companion's pinned sources. The attacker-success chart draws ONLY what the AttackerSuccess
example computed - the whitepaper's own section-11 procedure.

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


C = load("corpus2", os.path.join(HERE, "..", "sen0401_ch02_corpus_v1_3_0.py"))
ST = load("stories2", os.path.join(HERE, "..", "sen0401_ch02_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch02/assets/"
for _f in ("c2s04_overview.png", "c2s07_fractions.jpg", "mbc3_0202.png", "mbc3_0203.png",
           "mbc3_0207.png", "photo_gavin_andresen.jpg", "shot_bitcoinqt_0_5_2.png",
           "c8s06_mesh.png"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v1_2_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV

# ----------------------------------------------------------------------------------------------
# corpus lookups (chapter 2 has no NUM table; the executed example outputs stand in its place)
# ----------------------------------------------------------------------------------------------
BYNAME = {n[0]: n for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in EX["groups"].values() for _, out in rows)
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
    out += "\nFULL TEXT: course page, chapter 2 - " + ", ".join(names) + "."
    return out


def decamel(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", n).replace("Qr ", "QR ").replace("Uri", "URI")


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def assert_fact(token, where):
    """A number shown on a slide must exist in the corpus text, an executed output, or a pinned
    story source - nowhere else."""
    t = str(token)
    if t in CORPUS_TEXT or t in OUTTEXT or t in STORYTEXT or t.replace(",", "") in OUTTEXT:
        return t
    raise SystemExit("REFUSED: %r (slide %r) is in neither the corpus, the outputs, nor a story" % (t, where))


def bullets_ok(title, items):
    if len(items) > 5:
        raise SystemExit("REFUSED: %r carries %d bullets; the limit is 5" % (title, len(items)))
    for b in items:
        if len(b.split()) > 30:
            raise SystemExit("REFUSED: bullet %r on %r reads as a paragraph (over 30 words)" % (b, title))
    return items


# verified console rows, straight from the executed examples
G = EX["groups"]


def code(group, x, y, w, h, fs=11, rows=None):
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fit = (w - 0.4) / (maxlen * 0.00842)
    fs = min(fs, round(fit, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fin" % (group, w))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


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


# ----------------------------------------------------------------------------------------------
# verified figures pulled from the executed examples (parsed, then re-asserted)
# ----------------------------------------------------------------------------------------------
import ast as _ast
_sp = _ast.literal_eval(G["SimplePayment"][-1][1])
assert _sp == (1, 2, 5000)
_fee = int(G["TransactionFee"][-1][1]); assert _fee == 5000
_fr = float(G["FeeRate"][-1][1]); assert _fr == 34.97
_utxo = _ast.literal_eval(G["UnspentOutput"][-1][1]); assert _utxo == ["Tx2:0", "Tx2:1"]
_pow = int(G["ProofOfWork"][-1][1]); assert _pow == 6630
_mr = _ast.literal_eval(G["MerkleTree"][-1][1]); assert _mr == "59e82c45a3662f55"
_att1 = _ast.literal_eval(G["AttackerSuccess"][1][1])
_att3 = _ast.literal_eval(G["AttackerSuccess"][2][1])
assert _att1[1] == 0.2045873 and _att1[6] == 0.0002428, "the paper's q=0.1 column drifted"
assert len(_att1) == 7 and len(_att3) == 7

S = []

TAKES = {
    'The questions this chapter answers': 'If you can answer these, chapter 2 is yours',
    'One chapter, five branches': 'Five branches - every slide today lives on this map',
    'Nine pages, and a table of odds': 'The paper computes its promises - today we recompute them',
    'Alice pays Bob: one transaction, whole': 'A transaction spends whole outputs and makes new ones',
    'Your balance is outputs, not an account': 'No accounts anywhere - only unspent outputs your keys can unlock',
    'Change comes back to you': 'Inputs are spent whole; the difference returns as change',
    'Fees price bytes, not value': 'You pay for block space - size, not amount',
    'Five free bitcoins for every visitor': 'Before exchanges, distribution itself had to be invented',
    "A transaction's journey to everyone": 'Four seconds of gossip puts Alice\'s payment in every mempool',
    'Who checks? Everyone who wants to': 'Full nodes verify; light clients trust proofs, not people',
    'Watch any transaction live': 'The ledger is public - explorers are just viewers on it',
    'Mining: hard to win, instant to verify': 'Proof-of-work is a lottery whose ticket anyone can check',
    'A block, anatomized': 'A header of 80 bytes summarizes everything beneath it',
    'One root for a thousand leaves': 'Change any leaf and the root betrays it',
    'The coinbase: where new coin enters': 'Every coin in existence began life in a coinbase',
    'The day someone printed 184 billion bitcoin': 'Validation by every node is the immune system - it worked',
    'Confirmations: depth, not time': 'Each block on top multiplies the cost of rewriting yours',
    "The whitepaper's table, recomputed live": 'Six confirmations: the attacker\'s odds drop below 0.03%',
    'Zero-conf espresso, six-block house': 'Match the wait to the stake - that is all 6 blocks means',
    'The chapter as data: triples and provenance': 'The course page you use is built exactly this way',
    'Run the chapter at home': 'Three consoles reproduce the chapter - tonight, on your laptop',
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
# the deck
# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 2: How Bitcoin Works", "Transactions, the network, and the chain - one payment, followed all the way",
      [img("c2s04_overview.png", 5.9, 1.15, 3.7, 2.6, cap="users, wallets, nodes, miners - from the owner's 2025 deck")],
      "SAY: Chapter 1 asked what Bitcoin is; chapter 2 follows one payment - Alice pays Bob - all the "
      "way from her wallet to a buried block, and meets every moving part on the way.\n"
      "FULL TEXT: course page, chapter 2.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.35, "w": 9.0, "h": 3.7, "fs": 12.5,
          "items": [re.sub(r",.*", "?", q) if len(q.split()) > 18 else q for q in C.CQS]}],
        paras("Transaction"))

content("One chapter, five branches", "The concept map the whole chapter hangs on",
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 12, "root": "Chapter 2",
          "nodes": [{"label": r, "kids": [decamel(x) for x in children(r, 2)[:7]]}
                    for r in ("Transaction", "Network", "Blockchain", "Semantics", "Practice")]}],
        paras("Transaction", "Network", "Blockchain"),
        lede="Each branch is a question the chapter answers; the grey lists are the concepts that answer it, every one explained on the course page.")

# ---- Transactions -----------------------------------------------------------------------------
section("Transactions", "Who pays whom, with what, and what it costs",
        [{"label": "Inputs and outputs"}, {"label": "Change"}, {"label": "Fees"}, {"label": "The chain of spends"}],
        paras("Transaction"),
        image=img("mbc3_0203.png", 6.4, 2.2, 3.2, 1.6, cap="outputs become inputs - Mastering Bitcoin 3e, CC BY-SA"))

content("Nine pages, and a table of odds", STORY["WhitepaperMath"]["when"],
        [{"t": "news", "x": 0.5, "y": 1.42, "w": 3.1, "h": 2.5, "paper": "The Cryptography List",
          "date": "Friday October 31 2008", "badge": "nine pages at bitcoin.org",
          "headline": "Bitcoin P2P e-cash paper"},
         {"t": "text", "x": 3.95, "y": 1.55, "w": 5.55, "h": 1.5, "fs": 12, "italic": True, "color": "mute",
          "body": '"A purely peer-to-peer version of electronic cash would allow online payments to be sent '
                  'directly from one party to another without going through a financial institution." - the abstract\'s first sentence'},
         {"t": "beats", "x": 3.95, "y": 3.1, "w": 5.55, "h": 1.15, "fs": 13, "items": [
             "Section 11 computes the attacker's catch-up odds",
             "We rerun that computation live, later in this deck"]},
         factrow("WhitepaperMath", x=3.95, y=4.42, w=5.55)],
        story_notes("WhitepaperMath"))

content("Alice pays Bob: one transaction, whole", "The chapter's running example, shown as the ledger sees it",
        [img("mbc3_0202.png", 0.5, 1.5, 4.3, 2.85, cap="double-entry view - Mastering Bitcoin 3e, CC BY-SA"),
         {"t": "numlist", "x": 5.1, "y": 1.55, "w": 4.4, "h": 1.5, "fs": 10.5, "items": [
             "One 100,000-sat output of Alice's is spent whole",
             "Two new outputs: 75,000 to Bob, 20,000 back to Alice",
             "What the sums leave over - 5,000 sat - is the fee"]},
         dict(code("SimplePayment", 5.1, 3.3, 4.4, 1.05, fs=9.5), label="counted by the run: 1 input, 2 outputs, 5,000 fee")],
        paras("Transaction", "Input", ask="Why must the 100,000 be spent whole rather than split?"))

content("Your balance is outputs, not an account", "The UTXO idea - what a wallet actually sums",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 5.3, "h": 1.75, "fs": 10.5, "items": [
            "Every payment leaves outputs - coins of exact sizes",
            "Spending consumes outputs whole and mints new ones",
            "Your balance = the outputs your keys can unlock",
            "The run keeps only the unspent: Tx2:0 and Tx2:1"]},
         {"t": "chips", "x": 6.2, "y": 1.9, "w": 3.3, "h": 1.2, "fs": 12.5,
          "items": ["Tx2:0 unspent", "Tx2:1 unspent", "Tx1:0 spent"]},
         dict(code("UnspentOutput", 0.5, 3.6, 9.0, 1.1, fs=9.5), label="the ledger's view, filtered to the spendable")],
        paras("UnspentOutput", "Output", ask="Where does the idea of an 'account balance' live, if not on the chain?"))

content("Change comes back to you", "Inputs are spent whole, like banknotes",
        [{"t": "bars", "x": 0.5, "y": 1.7, "w": 5.4, "h": 1.5, "rows": [
            {"label": "to Bob", "v": 75000, "hot": True},
            {"label": "change, back to Alice", "v": 20000},
            {"label": "fee, to the miner", "v": 5000}]},
         {"t": "when", "x": 6.3, "y": 1.75, "w": 3.1, "body": "75,000 + 20,000 + 5,000 = 100,000"},
         dict(code("TransactionFee", 0.5, 3.55, 5.4, 0.95, fs=10.5), label="the fee is the remainder - computed, not quoted"),
         img("c2s07_fractions.jpg", 6.3, 3.3, 3.1, 1.55, cap="the fraction table, from the owner's 2025 deck")],
        paras("MakingChange", "TransactionFee", ask="Pay a 20-lira coffee with a 50-lira note: where is the change output?"),
        lede="A 100,000-satoshi output pays a 75,000 bill the way a banknote pays a coffee: spent whole, with change coming back - minus the tip to the miner.")

content("Fees price bytes, not value", "Block space is the scarce good",
        [{"t": "numlist", "x": 0.5, "y": 1.66, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "A block holds bytes, not value - space is what runs out",
            "So fees are bid per virtual byte, not per coin moved",
            "This transaction: 143 vbytes, 5,000 sat - about 35 sat/vB"]},
         dict(code("TransactionSize", 4.3, 1.6, 5.2, 0.95, fs=10), label="1 - weight to virtual bytes"),
         dict(code("FeeRate", 4.3, 2.85, 5.2, 0.95, fs=10), label="2 - the rate a wallet actually bids"),
         {"t": "stat", "x": 4.3, "y": 3.95, "w": 5.2, "h": 1.0, "items": [
             {"n": assert_fact("34.97", "fees"), "label": "sat/vB, from the run"},
             {"n": assert_fact("143", "fees"), "label": "virtual bytes here"}]}],
        paras("FeeRate", "TransactionSize", ask="Why does moving 1 BTC cost the same as moving 100?"))

# ---- Network ----------------------------------------------------------------------------------
section("The network", "No postmaster - transactions travel by gossip",
        [{"label": "Propagation"}, {"label": "Mempools"}, {"label": "Full and light nodes"}, {"label": "Explorers"}],
        paras("Network"),
        image=img("c8s06_mesh.png", 6.5, 2.1, 3.1, 2.5))

content("Five free bitcoins for every visitor", STORY["FirstFaucet"]["when"],
        [img("photo_gavin_andresen.jpg", 0.5, 1.45, 2.6, 3.05, cap="Gavin Andresen - photo: Stephen McCarthy / Web Summit, CC BY 2.0"),
         {"t": "beats", "x": 3.5, "y": 1.5, "w": 6.0, "h": 2.3, "fs": 13, "items": [
             "June 2010: almost nowhere to buy bitcoin existed",
             "Andresen stocked a website with 1,100 BTC of his own",
             "Five coins free per visitor; a CAPTCHA was the only price",
             "Thousands got their first coins - then came the exchanges"]},
         factrow("FirstFaucet", x=3.5, y=4.05, w=6.0)],
        story_notes("FirstFaucet"))

content("A transaction's journey to everyone", "Gossip, hop by hop, until every mempool holds it",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Alice signs", "sub": "her wallet builds the tx"},
            {"label": "One peer hears", "sub": "any node will do"},
            {"label": "Gossip", "sub": "each peer tells its peers"},
            {"label": "Every mempool", "sub": "seconds later", "hot": True}]},
         {"t": "numlist", "x": 0.5, "y": 3.1, "w": 3.6, "h": 1.3, "fs": 10.5, "items": [
            "No central dispatcher - the whisper network is the mail",
            "Bob sees it unconfirmed within seconds",
            "It waits in mempools until a miner picks it"]},
         dict(code("TransactionPropagation", 4.3, 3.05, 5.2, 1.0, fs=9.5), label="hops counted by the run"),
         img("shot_bitcoinqt_0_5_2.png", 4.3, 4.2, 2.3, 0.72)],
        paras("TransactionPropagation", "Mempool", ask="What happens if two conflicting spends gossip at once? (next section answers)"))

content("Who checks? Everyone who wants to", "Full nodes verify history; light clients verify proofs",
        [{"t": "compare", "x": 0.5, "y": 1.6, "w": 9.0, "h": 2.3, "fs": 12.5,
          "left": {"head": "Full node", "rows": [
              "Downloads and checks every block since 2009",
              "Trusts nobody - recomputes all the rules",
              "Serves the network; needs disk and patience"]},
          "right": {"head": "Lightweight client", "rows": [
              "Keeps headers only - megabytes, not gigabytes",
              "Verifies proofs that a tx sits in a block",
              "Perfect for phones; trusts the strongest chain"]}},
         dict(code("FullNode", 0.5, 4.1, 9.0, 0.8, fs=10.5), label="the checklist a full node runs on every block")],
        paras("FullNode", "LightweightClient", ask="Which one is Alice's phone wallet, and what exactly does it trust?"))

content("Watch any transaction live", "The ledger is public - explorers are windows on it",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.75, "fs": 10.5, "items": [
            "Paste any txid into an explorer and watch it confirm",
            "Chapter 1's genesis bytes came from such an API",
            "Same data, three windows: your node, a site, an API"]},
         dict(code("BlockExplorer", 4.3, 1.66, 5.2, 1.3, fs=9), label="what an explorer answers, computed by the run"),
         {"t": "chips", "x": 0.5, "y": 3.9, "w": 9.0, "h": 0.6, "fs": 13,
          "items": ["mempool.space", "blockstream.info", "your own node"]}],
        paras("BlockExplorer", "RecipientVerification", ask="Why does Bob check his OWN copy rather than trust Alice's screenshot?"))

# ---- Blockchain and mining --------------------------------------------------------------------
section("Blockchain and mining", "How the next page of history gets written",
        [{"label": "Proof-of-work"}, {"label": "Blocks and Merkle trees"}, {"label": "The coinbase"}, {"label": "Confirmations"}],
        paras("Blockchain"))

content("Mining: hard to win, instant to verify", "A sudoku in reverse - and the run finds a real nonce",
        [{"t": "numlist", "x": 0.5, "y": 1.66, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Guess a nonce, hash the block, hope the digest is small",
            "Like sudoku: hours to solve, seconds to check",
            "The run really searches - and finds 6,630"]},
         {"t": "funnel", "x": 4.35, "y": 1.6, "w": 5.1, "h": 1.7, "cap": "nonce found: %s - anyone re-checks it in one hash" % assert_fact("6630", "pow"),
          "steps": ["try nonce 0, 1, 2, ...", "hash each candidate", "most fail the target", "6,630 clears it"]},
         dict(code("ProofOfWork", 0.5, 3.75, 9.0, 1.1, fs=9.5), label="the search, exactly as the slide claims it")],
        paras("ProofOfWork", "SudokuAnalogy", ask="Who pays for all the losing tickets - and why is that the point?"))

content("A block, anatomized", "80 bytes of header summarize everything beneath",
        [img("mbc3_0207.png", 0.5, 1.45, 3.1, 3.45, cap="Alice's tx inside a block - Mastering Bitcoin 3e, CC BY-SA"),
         {"t": "numlist", "x": 3.95, "y": 1.55, "w": 5.55, "h": 1.9, "fs": 10.5, "items": [
            "Header: previous-block hash, Merkle root, time, target, nonce",
            "Body: the transactions - Alice's among them",
            "Chain the headers and you chain all history"]},
         {"t": "chips", "x": 3.95, "y": 3.5, "w": 5.55, "h": 0.55, "fs": 11,
          "items": ["prev hash", "Merkle root", "time", "target", "nonce"]},
         dict(code("Block", 3.95, 4.14, 5.55, 0.8, fs=9.5), label="80 header bytes carry a 4,000,000-byte body: 1 to 50,000")],
        paras("Block", "BlockHeader", ask="Why hash the header only, not the whole megabyte?"))

content("One root for a thousand leaves", "The Merkle tree pins every transaction at once",
        [{"t": "numlist", "x": 0.5, "y": 1.66, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Hash the transactions in pairs, then pairs of pairs",
            "One root remains - 32 bytes for any number of leaves",
            "Change any leaf and the root betrays it instantly"]},
         {"t": "funnel", "x": 4.35, "y": 1.6, "w": 5.1, "h": 1.7, "cap": "root of A,B,C,D: %s..." % assert_fact("59e82c45a3662f55", "merkle"),
          "steps": ["4 leaves: A B C D", "2 pair-hashes", "1 root seals them all"]},
         dict(code("MerkleTree", 0.5, 3.75, 9.0, 1.1, fs=9.5), label="four leaves to one root, computed")],
        paras("MerkleTree", ask="A light client holds only the root - what must a proof hand it?"))

content("The coinbase: where new coin enters", "The one transaction with no inputs",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Coinbase tx", "sub": "first in every block"},
            {"label": "No inputs", "sub": "value from the protocol"},
            {"label": "Subsidy + fees", "sub": "chapter 1's chart", "hot": True},
            {"label": "100 blocks", "sub": "before it can be spent"}]},
         dict(code("CoinbaseTransaction", 0.5, 3.1, 5.6, 1.0, fs=10), label="the reward at this block, computed"),
         {"t": "stat", "x": 6.4, "y": 3.05, "w": 3.1, "h": 1.35, "items": [
             {"n": "0", "label": "inputs in a coinbase - the only transaction so allowed"}]}],
        paras("CoinbaseTransaction", "BlockReward", ask="Trace any coin backwards: where must the trail always end?"))

content("The day someone printed 184 billion bitcoin", STORY["ValueOverflow"]["when"],
        [{"t": "stat", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "items": [
            {"n": assert_fact("184,467,440,737", "overflow"), "label": "BTC conjured by one transaction in block 74,638"},
            {"n": assert_fact("74,638", "overflow"), "label": "the block that carried it, 2010-08-15"},
            {"n": "~5 hours", "label": "from forum report to Satoshi's 0.3.10 fix"}]},
         {"t": "claims", "x": 0.5, "y": 3.0, "w": 9.0, "h": 1.3, "rows": [
             {"label": "output of 92,233,720,368.54 BTC - overflow, summed as a small number", "ok": False},
             {"label": "its twin output, same trick", "ok": False},
             {"label": "0.3.10's corrected rule: outputs must sum in range - chain rebuilt without them", "ok": True}]},
         factrow("ValueOverflow")],
        story_notes("ValueOverflow"))

content("Confirmations: depth, not time", "Each block on top multiplies the attacker's bill",
        [{"t": "chainviz", "x": 0.5, "y": 1.66, "w": 5.3, "h": 1.5, "tampered": False,
          "cap": "Alice's block + 2 on top = 3 confirmations"},
         dict(code("Confirmation", 6.2, 1.7, 3.3, 1.2, fs=9.5), label="depth, counted"),
         {"t": "numlist", "x": 0.5, "y": 3.5, "w": 9.0, "h": 1.3, "fs": 10.5, "items": [
            "A confirmation is a block on top of yours - depth, not minutes",
            "To rewrite yours an attacker must redo every block above it, faster than everyone",
            "How unlikely that is, the whitepaper computes - next slide"]}],
        paras("Confirmation", "BestBlockchain", ask="Why does a reorg of depth 1 happen weekly, depth 6 almost never?"))

content("The whitepaper's table, recomputed live", "Section 11's procedure, rerun for this deck - not quoted",
        [{"t": "chart", "x": 0.45, "y": 1.5, "w": 6.5, "h": 3.4, "ctype": "line", "log": True,
          "min": 0.0001, "max": 1, "fmt": "0.####",
          "title": "P(attacker ever catches up) vs confirmations (log axis)",
          "dataLabels": True, "dlFmt": "0.0###", "dlFs": 7.5,
          "labels": [str(z) for z in range(1, 7)],
          "series": [{"name": "attacker holds 10% of hash power", "data": _att1[1:]},
                     {"name": "attacker holds 30%", "data": _att3[1:]}]},
         {"t": "stat", "x": 7.15, "y": 1.55, "w": 2.35, "h": 2.5, "vert": True, "items": [
             {"n": assert_fact("0.2045873", "attacker"), "label": "catch-up odds after 1 block (q=0.1)"},
             {"n": assert_fact("0.0002428", "attacker"), "label": "after 6 - the '6 confirmations' rule"}]},
         {"t": "when", "x": 7.15, "y": 4.3, "w": 2.3, "body": "the paper's own table"}],
        "SAY: This chart is not an illustration: the build ran the whitepaper's section-11 procedure "
        "(examples group AttackerSuccess) and drew what it returned; the chapter research record matched "
        "the q=0.1 column against the paper to seven decimals.\n"
        "ASK: Read the 30% line at six blocks - why do exchanges wait longer for huge deposits?\n"
        "FULL TEXT: course page, chapter 2 - Probability, Confirmation.",
        take=TAKES["The whitepaper's table, recomputed live"])

content("Zero-conf espresso, six-block house", "Match the wait to the stake",
        [{"t": "compare", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.4, "fs": 12.5,
          "left": {"head": "Espresso: accept at zero", "rows": [
              "Small sum, repeat customer, in person",
              "Risk: someone races a double-spend for a coffee",
              "Seconds matter more than certainty"]},
          "right": {"head": "House: wait for six", "rows": [
              "Large, irreversible, worth attacking",
              "Six blocks: odds near one in four thousand (q=0.1)",
              "An hour of patience prices out the attack"]}},
         {"t": "when", "x": 3.35, "y": 4.35, "w": 3.3, "body": "same rule, different stakes"}],
        paras("SmallPaymentAcceptance", "UnconfirmedTransaction", ask="Where would you put a used-car sale on this line?"))

# ---- Semantics and practice -------------------------------------------------------------------
section("Semantics and practice", "The chapter as data, and the chapter on your laptop",
        [{"label": "Triples"}, {"label": "Provenance"}, {"label": "Run it at home"}],
        paras("Semantics"))

content("The chapter as data: triples and provenance", "How the course page itself stores what you just learned",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.0, "fs": 9.5, "items": [
            "Every fact on the course page is a triple: subject, predicate, object",
            "Provenance says who asserted it and from where - the run builds one of each and reads it back"]},
         dict(code("Triple", 0.5, 2.75, 9.0, 0.9, fs=10), label="1 - one fact, as the page stores it"),
         dict(code("ProvenanceGraph", 0.5, 3.95, 9.0, 0.9, fs=10), label="2 - and who says so")],
        paras("Triple", "ProvenanceGraph", ask="What triple would record Alice's payment to Bob?"))

content("Run the chapter at home", "Three consoles reproduce today's claims",
        [dict(code("HashDemo", 0.5, 1.55, 9.0, 0.85, fs=10.5), label="1 - the fingerprint that seals everything"),
         dict(code("BlockDemo", 0.5, 2.68, 9.0, 0.85, fs=10.5), label="2 - a toy block, mined like the real ones"),
         dict(code("BlockchainDemo", 0.5, 3.81, 9.0, 0.95, fs=10.5), label="3 - chain two and break one")],
        paras("Practice"))

content("Where to go from here", "Checked 2026-10-06; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The whitepaper - section 11 is today's chart", "https://bitcoin.org/bitcoin.pdf"],
                ["This chapter, free (CC BY-SA)", "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch02_overview.adoc"],
                ["The value-overflow incident, documented", "https://en.bitcoin.it/wiki/Value_overflow_incident"]]},
            {"head": "Explore & verify", "rows": [
                ["mempool.space - watch a tx confirm tonight", "https://mempool.space"],
                ["blockstream.info - the API chapter 1 used", "https://blockstream.info"],
                ["learnmeabitcoin - every structure, drawn", "https://learnmeabitcoin.com"]]},
            {"head": "Community & history", "rows": [
                ["Bitcoin Stack Exchange Q&A", "https://bitcoin.stackexchange.com"],
                ["The faucet announcement, as posted (2010)", "https://bitcointalk.org/index.php?topic=141.0"]]},
            {"head": "Watch", "rows": [
                ["But how does bitcoin work? (3Blue1Brown)", "https://www.youtube.com/watch?v=bBC-nXj3Ng4"]]}]}],
        "SAY: Everything here is free. Watch one transaction confirm on mempool.space tonight - pick any "
        "txid from the latest block - and you will have SEEN this whole chapter happen once.\n"
        "ASK: Who can find Alice-sized fees (about 35 sat/vB) in the current mempool?\n"
        "FULL TEXT: course page, chapter 2 - Practice.",
        take="One evening on an explorer replays this whole chapter for free")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a transaction spends, creates, and pays",
          "How a payment reaches every mempool with no postmaster",
          "Why rewriting a buried block costs more than it wins",
          "What six confirmations actually promises - a number"])}],
      "SAY: Four claims, each one carried by a computation you watched run. Next week: the wallet that "
      "holds Alice's keys.\nFULL TEXT: course page, chapter 2.", bg="dark")

# ---- the agenda (after the title) and the summary (before the resources) ----------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "A transaction spends outputs whole and mints new ones - balance is a sum, not an account",
              "Fees buy bytes of block space; change is just an output back to yourself",
              "Transactions travel by gossip; within seconds every mempool holds Alice's payment",
              "Miners race a lottery that is instant to verify - and rules caught the 184-billion forgery",
              "A confirmation is depth; the whitepaper computes what each block of depth buys you"]}],
          "notes": "SAY: Five lines, one per part. If any feels like a claim rather than a fact, the agenda "
                   "names the slides that prove it; the course page carries the full text.\n"
                   "ASK: Which line would you defend to a sceptic first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 2 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts, one payment followed all the way through",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_t, _n, _b, _p = (_sec[t] for t in ("Transactions", "The network", "Blockchain and mining", "Semantics and practice"))
_rows = [("Questions and the chapter map", 3, _t),
         ("Transactions - inputs, outputs, change, fees", _t + 1, _n),
         ("The network - gossip, nodes, explorers", _n + 1, _b),
         ("Blockchain and mining - blocks, proof, confirmations", _b + 1, _p),
         ("Semantics, practice, summary, and resources", _p + 1, len(S))]
for _ti, _a, _bb in _rows:
    if not 2 < _a <= _bb <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) is out of order" % (_ti, _a, _bb))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") == "code")),
                      "label": "code examples, run live - each shown with its result"}]}]
S[1]["notes"] = ("SAY: Five parts, one payment followed all the way. The stories carry the why, the "
                 "consoles carry the proof, and every slide number here is printed bottom-right as we pass it.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 2 - every section.")

# every slide must carry notes; every content slide a takeaway
for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES:
        sl["take"] = TAKES[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 2: How Bitcoin Works", "sub": "SEN0401, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0)"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
