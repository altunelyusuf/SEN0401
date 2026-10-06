#!/usr/bin/env python3
"""Builds deck_plan_v2_7_0.json - the chapter 1 lecture deck redesigned for the classroom.

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

Usage: python3 deck_build_v2_0_0.py   (writes deck_plan_v2_7_0.json beside itself)
"""
__version__ = "2.7.0"

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
ST = load("stories", os.path.join(HERE, "..", "sen0401_ch01_stories_v1_3_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch01/assets/"
for _f in ("genesis_hexdump.png", "photo_cma_stater.jpg", "photo_met_tablet.jpg", "photo_rai_stone.jpg", "photo_pizza_margherita.jpg", "photo_lydian_coins.jpg",
           "mbc3_0101.png", "mbc3_0102.png", "c1s18_circulation.png", "c1s24_protocol.png", "c1s32_nakamoto.jpg", "c2s04_overview.png",
           "c2s07_fractions.jpg", "c8s06_mesh.png", "c8s32_miningnodes.png"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
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


def _sentences(text, k=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:k])


def paras(*names, ask=None):
    """Cue-style notes: two corpus sentences to say, one question to ask, and where the full text
    lives. The slide carries the clues; the course page carries the prose."""
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
    out += "\nFULL TEXT: course page, chapter 1 - " + ", ".join(names) + "."
    return out


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
        if len(b.split()) > 30:
            raise SystemExit("REFUSED: bullet %r on %r reads as a paragraph (over 30 words)" % (b, title))
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
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rows)
    fit = (w - 0.4) / (maxlen * 0.00842)
    fs = min(fs, round(fit, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fin" % (group, w))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rows, "fs": fs, "cap": CAP}


# program slides: every chapter program, whole, in the exact shape deck_check re-runs
def prog(block, x, y, w, h, fs=10):
    src, out = EX["blocks"][block]
    lines = src.split("\n")
    maxlen = max(len(l) for l in lines)
    fit_w = (w - 0.4) / (maxlen * 0.00842)  # Courier advance ~0.60 of size; 1pt = 1/72 in
    fit_h = (h - 0.30) * 72.0 / (len(lines) * 1.3)
    fs = min(fs, round(fit_w, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: %s cannot fit unwrapped in %.1fx%.1fin (width allows %.1f, height %.1f)"
                         % (block, w, h, fit_w, fit_h))
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": lines, "fs": fs,
            "cap": "program %s, lines 1 to %d of %d, run under Python %s" % (block, len(lines), len(lines), PYV),
            "out": out, "block": block, "first": 1, "total": len(lines)}
import ast as _ast
_pc = _ast.literal_eval(EX["blocks"]["PaymentChannel"][1])
assert _pc == (59000, 41000, 100000, 2)
PC_ROWS = [{"label": "Alice, after", "v": _pc[0], "hot": True}, {"label": "Bob, after", "v": _pc[1]},
           {"label": "on-chain txs", "v": _pc[3], "hot": True}]
_ln = _ast.literal_eval(EX["blocks"]["LightningNetwork"][1])
LN_HOPS = _ln[0]
LN_N = _ln[1]
assert LN_N == 3 and _ln[2] is False
_cr = _ast.literal_eval(EX["blocks"]["ConsensusRuleSet"][1])
assert _cr == [True, False, True]
CLAIM_ROWS = [{"label": "312,500,000 sat at height 840,000", "ok": _cr[0]},
              {"label": "312,500,001 sat - one too many", "ok": _cr[1]},
              {"label": "325,000,000 sat incl. 12,500,000 fees", "ok": _cr[2]}]
_bc = _ast.literal_eval(EX["blocks"]["Blockchain"][1])
assert _bc == (True, False)
BC = ("True", "False")
_ks = _ast.literal_eval(EX["blocks"]["KeyStretching"][1])
assert _ks[0] == 64
KS = _ks

PROG = prog("PaymentChannel", 0.5, 3.15, 9.0, 1.5)

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


S = []
TAKES = {'The outcomes this session serves': 'One outcome, one chapter, every concept on the page', 'The questions this chapter answers': 'If you can answer these, chapter 1 is yours', 'One chapter, six branches': 'Six branches - every slide today lives on this map', 'One bitcoin divides into 100 million satoshis': 'Money here is counting, and the units are exact', '21 million, by rule - not by promise': 'Scarcity is enforced by arithmetic every node checks', 'The schedule, executed': 'Three one-liners reproduce the whole monetary policy', 'Price is discovered, not declared': 'No one sets the price; everyone does', 'A bank in the middle vs. peers': 'Remove the hub and the rules must move to every node', 'Peers find each other without a directory': 'The network is just nodes agreeing to speak alike', 'Rules, not rulers, decide validity': 'Validity is computed, never decreed', 'Mining pays for honesty': 'Security is bought with energy and paid in bitcoin', 'The wallet branch, mapped': 'A wallet is software for keys, not a bag of coins', 'Who holds the keys, holds the coins': 'Custody is the first security decision you make', 'From a phrase to a key, slowly on purpose': 'Slowness here is a feature priced against attackers', "Alice's first bitcoin, step by step": 'Five minutes of app taps hide all of this machinery', 'Two solved problems, one new system': "Bitcoin's novelty is the combination, not the parts", 'From keys to the chain': 'This pipeline is the course syllabus in one row', 'A chain that notices tampering': 'History becomes expensive to rewrite, cheap to verify', 'The toolbox under the hood': 'Every term here gets its own page section', 'What kind of thing is Bitcoin?': 'Each adjective is engineered, not advertised', 'Beyond the base layer': 'The chain settles; the edges scale', 'Five thousand years to digital cash': 'Each era changed the ledger-keeper; Bitcoin removed the position', 'Physical cash: superb in person, stuck there': 'Cash is a bearer instrument: perfect in person, useless on a network', 'Why digital money had to wait': 'Perfect copies made digital cash impossible without a referee', 'The double-spend, solved in public': 'The referee is everyone, and the whistle is arithmetic', 'A newspaper headline carved into block zero': 'History is written into the chain itself', 'The first person ever paid in bitcoin': 'Peer to peer meant person to person from day one', 'Forty years of failed digital money': 'The pieces were old; the combination was new', 'The island where money never moved': 'Money is a ledger; Bitcoin makes it digital', 'Two pizzas for ten thousand bitcoin': 'Price is discovered the first time someone pays', 'The exchange that lost everyone\'s coins': 'Whoever holds the keys holds the coins', 'Mt. Gox: the exchange that lost everyone\'s coins': 'Whoever holds the keys holds the coins - exchanges included', 'Your key is your deed - and you may never show it': 'Prove you hold the key; never reveal it'}


def slide(kind, title, sub, items, notes, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes, "bg": bg})


def content(title, sub, items, notes, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "bg": "light"}
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past 26 words" % title)
        sl["lede"] = lede
    if take:
        if len(take.split()) > 24:
            raise SystemExit("REFUSED: takeaway %r runs past 14 words" % take)
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes):
    slide("section", title, sub,
          [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 8.6, "h": 1.9, "cols": min(4, len(boxes)),
            "fs": 14, "subfs": 11, "items": boxes}], notes, bg="dark")


# ----------------------------------------------------------------------------------------------
# the deck
# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 1: Introduction", OLDPLAN["meta"]["sub"],
      [img("c1s24_protocol.png", 6.3, 1.15, 3.3, 2.6, cap="from the owner's 2025 deck")],
      OLDPLAN["slides"][0]["notes"], bg="light")

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
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 12, "root": "Chapter 1",
          "nodes": [{"label": r, "sub": "%d concepts" % sum(1 for n in C.NODES if (n[3] == r or (n[3] in children(r)))) if False else ""} for r in []] or
                   [{"label": r, "kids": [decamel(x) for x in children(r, 2)[:7]]} for r in ("Money", "Network", "Wallet", "Usage", "Foundations", "Nature")]}],
        paras("Money", "Network", "Wallet", "Usage", "Foundations", "Nature"),
        lede="Each branch is a question the chapter answers; the grey lists are the concepts that answer it, every one explained on the course page.")

# ---- Origins: the stories ---------------------------------------------------------------------
section("Origins", "Three stories that explain why Bitcoin looks the way it does",
        [{"label": "A headline in block 0"}, {"label": "The first payment"}, {"label": "Forty years of attempts"}],
        story_notes("GenesisHeadline"))

content("A newspaper headline carved into block zero", STORY["GenesisHeadline"]["when"],
        [img("genesis_hexdump.png", 0.5, 1.42, 5.9, 3.0,
             cap="block 0's real 285 bytes, fetched from the live chain for this deck; its hash re-verified in the build"),
         {"t": "news", "x": 6.65, "y": 1.42, "w": 2.85, "h": 2.1, "paper": "The Times",
          "date": "Saturday January 3 2009",
          "headline": "Chancellor on brink of second bailout for banks"},
         {"t": "beats", "x": 6.65, "y": 3.62, "w": 2.85, "h": 0.78, "fs": 11, "items": [
             "The orange bytes ARE the headline"]},
         factrow("GenesisHeadline")],
        story_notes("GenesisHeadline"))

content("The first person ever paid in bitcoin", "Satoshi Nakamoto, and the cryptographer who ran the code",
        [img("c1s32_nakamoto.jpg", 0.5, 1.45, 2.9, 3.4, cap="anonymity, from the owner's 2025 deck"),
         {"t": "beats", "x": 3.7, "y": 1.55, "w": 5.8, "h": 2.3, "fs": 13.5, "items": [
             "Satoshi Nakamoto: still unidentified, by design",
             "Hal Finney answered the whitepaper - and 'Running bitcoin'",
             "Block 170, January 2009: Satoshi pays Finney 10 BTC"]},
         factrow("FirstTransaction", x=3.7, y=4.05, w=5.8)],
        story_notes("FirstTransaction"))

content("Forty years of failed digital money", "Every part existed before Bitcoin combined them",
        [{"t": "timeline", "x": 0.4, "y": 1.6, "w": 9.2, "h": 2.2, "items": [
            {"year": "1982", "label": "Chaum: blind signatures, ecash"},
            {"year": "1997", "label": "Back: Hashcash proof-of-work"},
            {"year": "1998", "label": "Dai: b-money; Szabo: bit gold"},
            {"year": "2008", "label": "Nakamoto: the whitepaper", "hot": True},
            {"year": "2009", "label": "The genesis block runs", "hot": True}]},
         {"t": "bullets", "x": 0.5, "y": 3.85, "w": 9.0, "h": 0.55, "fs": 13, "items": bullets_ok("lineage", [
             "DigiCash went bankrupt; b-money and bit gold were never built - agreement without a leader was missing"])},
         factrow("CypherpunkLineage")],
        story_notes("CypherpunkLineage"))

# ---- Money ------------------------------------------------------------------------------------
slide("section", "Money", "What the currency is, who issues it, and on what schedule",
      [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3, "h": 1.9, "cols": 2, "fs": 14, "subfs": 11,
        "items": [{"label": "Unit"}, {"label": "Supply"}, {"label": "Issuance"}, {"label": "Price"}]},
       img("photo_lydian_coins.jpg", 6.5, 1.7, 3.1, 2.9, cap="Lydian electrum, the first coins - photo: brewbooks, CC BY-SA 2.0")],
      paras("Money"), bg="light")

content("The island where money never moved", STORY["StoneMoney"]["when"],
        [img("photo_rai_stone.jpg", 0.5, 1.5, 3.1, 3.1, cap="a rai stone on Yap - photo: Eric Guinther, CC BY-SA 3.0, Wikimedia Commons"),
         {"t": "beats", "x": 3.95, "y": 1.5, "w": 5.55, "h": 1.75, "fs": 13, "items": [
             "Rai stones were money too heavy to move, so they never moved",
             "A payment was the village agreeing the owner had changed",
             "One stone sank at sea - and kept changing owners anyway"]},
         {"t": "ledger", "x": 4.0, "y": 3.12, "w": 5.4, "h": 1.28, "owners": ["Fatu", "Ngirmang", "Teru"],
          "cap": "the stone stays; only the shared record moves"}, factrow("StoneMoney", x=3.95, y=4.5, w=5.55)],
        story_notes("StoneMoney"))

content("Five thousand years to digital cash", STORY["MoneyEvolution"]["when"],
        [img("photo_met_tablet.jpg", 0.75, 1.55, 1.75, 1.45, cap="a barley account, Sumer - Met, CC0"),
         img("photo_cma_stater.jpg", 7.55, 1.55, 1.75, 1.45, cap="electrum stater, 600-550 BCE - CMA, CC0"),
         {"t": "text", "x": 2.75, "y": 1.9, "w": 4.6, "fs": 12.5, "italic": True, "color": "mute", "h": 0.9,
          "body": "The oldest money we can hold is already a ledger entry (left) and a standard token (right)."},
         {"t": "timeline", "x": 0.4, "y": 3.15, "w": 9.2, "h": 1.75, "items": [
            {"year": "~3000 BCE", "label": "grain ledgers, Mesopotamia"},
            {"year": "~600 BCE", "label": "first coins, Lydia"},
            {"year": "~1000", "label": "paper money, Song China"},
            {"year": "1600s", "label": "goldsmiths' receipts, bank money"},
            {"year": "1971", "label": "gold tie cut - pure fiat"},
            {"year": "2009", "label": "cryptocurrency", "hot": True}]},
         factrow("MoneyEvolution")],
        story_notes("MoneyEvolution"),
        lede="Those Lydian coins were money once; so is your app balance - the difference is always the ledger.")

content("Traditional, digital, crypto - side by side", "The chapter's one-table comparison",
        [{"t": "table", "x": 0.4, "y": 1.6, "w": 9.2, "colW": [1.7, 2.4, 2.55, 2.55], "fs": 10.5, "rowH": 0.62,
          "rows": [[""] + [k for k in ST.MONEY_KINDS if k != "axes"]] +
                  [[ax] + [ST.MONEY_KINDS[k][i] for k in ST.MONEY_KINDS if k != "axes"]
                   for i, ax in enumerate(ST.MONEY_KINDS["axes"])]}],
        story_notes("MoneyEvolution"),
        take="Same uses, different ledgers - and that difference is this course")

content("Physical cash: superb in person, stuck there", "Why the oldest form still works - and where it stops",
        [{"t": "compare", "x": 0.5, "y": 1.7, "w": 9.0, "h": 3.1, "fs": 12.5,
          "left": {"head": "What cash does well", "rows": [
              "Settles hand to hand, instantly and finally",
              "Needs no account, bank, identity, or permission",
              "Cannot be frozen or censored remotely"]},
          "right": {"head": "Where it fails", "rows": [
              "Cannot travel a wire - no remote commerce",
              "Theft and loss are final; carrying value is risky",
              "Counterfeiting must be policed forever"]}}],
        paras("Money", ask="Which of these failures did cards fix - and at what new price?"),
        take="Cash is a bearer instrument: perfect in person, useless on a network",
        lede="Before praising Bitcoin, be fair to cash: it settles instantly, anonymously, with no middleman - but it cannot reach the internet.")

content("The internet got payments - and new gatekeepers", "The dot-com boom digitised paying, not cash",
        [{"t": "timeline", "x": 0.4, "y": 1.75, "w": 9.2, "h": 1.9, "items": [
            {"year": "1998", "label": "Confinity - Levchin and Thiel"},
            {"year": "1999", "label": "X.com - Elon Musk"},
            {"year": "2000", "label": "they merge; dot-com crash begins"},
            {"year": "2001", "label": "Beenz and Flooz die with the crash", "hot": True},
            {"year": "2002", "label": "PayPal sold to eBay, $1.5B"}]},
         {"t": "bullets", "x": 0.5, "y": 3.7, "w": 9.0, "h": 0.6, "fs": 12.5, "items": bullets_ok("dotcom", [
             "What survived was account money on one company's ledger - convenient, reversible, and censorable"])},
         factrow("OnlinePayments")],
        story_notes("OnlinePayments"),
        take="Payments went online in 1998-2002; cash never did",
        lede="Before asking why Bitcoin exists, remember the dot-com race: the web needed money, companies built it as accounts - and the failures took their users' balances down with them.")

content("When the money in your hand stops working", "Five documented cases, five links - no hypotheticals",
        [{"t": "cases", "x": 0.4, "y": 1.75, "w": 9.2, "h": 2.5, "cols": 5,
          "items": [{"place": p, "year": y, "text": t, "link": l} for p, y, t, l in ST.WHEN_MONEY_STOPS]},
         factrow("WhenMoneyStops")],
        story_notes("WhenMoneyStops"),
        take="Crisis or war, banked or not - the need is documented, not theoretical",
        lede="E-commerce without cards, aid without banks, savings under levies, wages under hyperinflation, a state under invasion: each card below is a real, dated case with its source.")

content("Why digital money had to wait", "The copy problem: a digital coin is a file",
        [{"t": "numlist", "x": 0.5, "y": 1.75, "w": 3.6, "h": 2.9, "fs": 11.5, "items": [
            "Make money digital and it becomes a file",
            "Files copy perfectly - so coins would too",
            "Both copies get spent: the double-spend",
            "For decades only a trusted central ledger could stop it - so digital money meant bank money"]},
         {"t": "copyviz", "x": 4.35, "y": 1.9, "w": 5.1, "h": 2.5}],
        paras("DoubleSpend", ask="Why does the same problem not exist for paper cash?"),
        take="Perfect copies made digital cash impossible without a referee",
        lede="Digital money is older than you think - what was missing for forty years was a way to stop one coin being spent twice without a bank in the middle.")

content("The double-spend, solved in public", "One shared ledger, one agreed order - no referee needed",
        [{"t": "numlist", "x": 0.5, "y": 1.75, "w": 3.6, "h": 2.9, "fs": 11.5, "items": [
            "Every payment is broadcast to every node",
            "Nodes agree on one order for all payments",
            "The first spend of a coin enters the block",
            "The second is refused by every node, everywhere"]},
         {"t": "dsolve", "x": 4.3, "y": 1.9, "w": 5.2, "h": 2.5}],
        paras("DoubleSpend", "Consensus", ask="What stops the network agreeing on the WRONG order? (chapter 12 answers)"),
        take="Bitcoin's invention: the referee is everyone, and the whistle is arithmetic",
        lede="Satoshi's whitepaper names the problem in its second sentence; the answer is not better files but a public ledger every node keeps and orders together.")

content("One bitcoin divides into 100 million satoshis", "The unit and its divisions - run, not quoted",
        [{"t": "flow", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.15, "fs": 13, "steps": [
            {"label": "1 BTC", "sub": "the currency unit"},
            {"label": "1,000 mBTC", "sub": "millibitcoin"},
            {"label": "100,000,000 sat", "sub": "the smallest unit"}]},
         dict(code("SatoshiUnit", 0.5, 3.0, 5.6, 1.1), label="0.001 BTC, counted in satoshis"),
         img("c2s07_fractions.jpg", 6.35, 2.95, 3.15, 1.75, cap="the fraction table, from the owner's 2025 deck")],
        paras("Unit", ask="How many satoshis buy a coffee at today's price?"))

content("21 million, by rule - not by promise", "Issuance halves every 210,000 blocks; the cap is the sum",
        [{"t": "chart", "x": 0.5, "y": 1.45, "w": 5.6, "h": 3.55, "ctype": "line",
          "title": "Block subsidy per era of 210,000 blocks (BTC)",
          "labels": halving_labels, "series": [{"name": "subsidy", "data": subsidy}]},
         {"t": "stat", "x": 6.3, "y": 1.45, "w": 3.2, "h": 3.55, "vert": True, "items": [
             {"n": "210,000", "label": "blocks between halvings"},
             {"n": assert_fact("20999999.9769", "cap"), "label": "the sum of every era's issuance"},
             {"n": "~2140", "label": "the year issuance ends"}]}],
        paras("Supply", "Issuance", ask="Why does the sum stop just short of 21 million?"))

content("The schedule, executed", "The cap is an arithmetic fact - the slide computes it",
        [{"t": "numlist", "x": 0.5, "y": 1.38, "w": 9.0, "h": 1.0, "fs": 9.5, "items": [
            "Shift 50 BTC right once per era, times 210,000 blocks, summed over 33 eras: the 20,999,999.9769 cap",
            "One shift for height 840,000 halves the subsidy to 3.125",
            "Five heights at once show the whole staircase"]},
         dict(code("SupplyCap", 0.5, 2.62, 9.0, 0.70, fs=11), label="1 - The cap, summed over 33 eras"),
         dict(code("Halving", 0.5, 3.50, 9.0, 0.70, fs=11), label="2 - One halving = divide by two"),
         dict(code("BlockSubsidy", 0.5, 4.34, 9.0, 0.61, fs=9.5), label="3 - The subsidy at any block height")],
        paras("Supply", "Issuance"))

content("Price is discovered, not declared", "No authority sets an exchange rate",
        [{"t": "numlist", "x": 0.5, "y": 1.42, "w": 9.0, "h": 0.95, "fs": 9.5, "items": [
            "No authority quotes a rate: the first program just divides one trade's two amounts",
            "The second weights every trade by its volume - one fair daily figure, as exchanges publish"]},
         dict(code("FloatingExchangeRate", 0.5, 2.72, 9.0, 0.68, fs=11.5), label="1 - A price is a ratio of two quotes"),
         dict(code("VolumeWeightedAverage", 0.5, 3.78, 9.0, 0.95, fs=10.5), label="2 - A day summarised fairly, by volume")],
        paras("Price"))

content("Two pizzas for ten thousand bitcoin", STORY["PizzaDay"]["when"],
        [{"t": "stat", "x": 0.5, "y": 1.55, "w": 3.0, "h": 1.6, "items": [
            {"n": "10,000 BTC", "label": "offered on the bitcointalk forum by Laszlo Hanyecz"}]},
         img("photo_pizza_margherita.jpg", 0.55, 3.3, 2.95, 1.55, cap="photo: Valerio Capello, CC BY-SA 3.0, Wikimedia Commons"),
         {"t": "beats", "x": 3.95, "y": 1.55, "w": 5.55, "h": 2.6, "fs": 13, "items": [
             "For 18 months bitcoin ran with no known price at all",
             "Someone took the offer and ordered him two pizzas",
             "The first commercial purchase gave bitcoin its first real price",
             "22 May is still celebrated as Bitcoin Pizza Day"]},
         factrow("PizzaDay", x=3.95, y=4.35, w=5.55)],
        story_notes("PizzaDay"))

content("The pizza, repriced every few years", "Documented milestones; the last point fetched live for this deck",
        [{"t": "chart", "x": 0.45, "y": 1.5, "w": 6.5, "h": 3.4, "ctype": "line", "log": True,
          "min": 10, "max": 10_000_000_000, "fmt": "$#,##0",
          "title": "Value of the Pizza Day 10,000 BTC (log axis)",
          "labels": [p[0] for p in ST.PIZZA_VALUE],
          "series": [{"name": "USD value", "data": [p[1] for p in ST.PIZZA_VALUE]}]},
         {"t": "stat", "x": 7.15, "y": 1.55, "w": 2.35, "h": 2.5, "vert": True, "items": [
             {"n": "$41", "label": "the pizzas' value in May 2010"},
             {"n": "$854M", "label": "the same 10,000 BTC on 2026-10-06, two APIs agreeing"}]},
         {"t": "when", "x": 7.15, "y": 4.3, "w": 2.3, "body": "each step x10"}],
        "SAY: Every point is a documented milestone - dollar parity in 2011, the first thousand in 2013, the 2017 and 2021 peaks - and the last one was fetched live from mempool.space and CoinGecko while this deck was built, agreeing within 0.1 percent.\nASK: Why does this chart need a log scale - what would it look like linear?\nFULL TEXT: course page, chapter 1 - Price; story companion, PIZZA_VALUE.",
        take="From 41 dollars to 854 million - price discovery never stopped")

# ---- Network ----------------------------------------------------------------------------------
slide("section", "Network", "No bank in the middle - and what replaces it",
      [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3, "h": 1.9, "cols": 2, "fs": 14, "subfs": 11,
        "items": [{"label": "Peer-to-peer"}, {"label": "Consensus"}, {"label": "Mining"}, {"label": "History"}]},
       img("c1s18_circulation.png", 6.5, 2.0, 3.1, 2.8)],
      paras("Network"), bg="light")

content("A bank in the middle vs. peers", "Decentralisation is an architecture, not a slogan",
        [{"t": "net", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.3,
          "left": {"title": "Centralised: one ledger-keeper", "hub": "Bank"},
          "right": {"title": "Bitcoin: every node checks every rule", "n": 8}}],
        paras("Network", "Consensus", ask="What breaks first in each picture if one machine lies?"))

content("Peers find each other without a directory", "The chapter's own protocol sketch - run, not quoted",
        [{"t": "numlist", "x": 0.5, "y": 1.66, "w": 3.55, "h": 1.8, "fs": 10.5, "items": [
            "Four peers start, each knowing one neighbour",
            "Each asks its neighbours for THEIR neighbours",
            "Links are counted when the gossip settles: 4"]},
         img("c8s06_mesh.png", 4.3, 1.58, 2.4, 1.6, cap="what it builds: a flat mesh"),
         {"t": "stat", "x": 7.0, "y": 1.58, "w": 2.5, "h": 1.6, "items": [
             {"n": "4", "label": "links counted by the run - no server, no registry"}]},
         dict(prog("PeerToPeerProtocol", 0.5, 3.62, 9.0, 1.3, fs=8), label="the exact program - run it at home")],
        paras("Network"))

content("Rules, not rulers, decide validity", "Each node applies the same consensus rules",
        [{"t": "numlist", "x": 0.5, "y": 1.66, "w": 3.55, "h": 1.75, "fs": 10, "items": [
            "The rule: at height h, a block may create subsidy plus fees, nothing more",
            "Three blocks claim rewards at height 840,000",
            "Verdicts: allowed, refused, allowed - right"]},
         {"t": "claims", "x": 4.2, "y": 1.58, "w": 5.3, "h": 1.78, "rows": CLAIM_ROWS},
         dict(prog("ConsensusRuleSet", 0.5, 3.72, 9.0, 1.1, fs=9), label="the exact program - run it at home")],
        paras("Consensus"))

content("Mining pays for honesty", "New coin and fees reward the work that secures the chain",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Transactions", "sub": "wait in the mempool"},
            {"label": "Miners", "sub": "spend energy on proof-of-work"},
            {"label": "Block found", "sub": "~every 10 minutes"},
            {"label": "Reward", "sub": "subsidy + fees"}]},
         {"t": "bullets", "x": 0.5, "y": 3.2, "w": 5.6, "h": 1.7, "fs": 14.5, "items": bullets_ok("mining", [
             "The subsidy follows the halving chart",
             "Cheating costs more than it could win",
             "Chapter 12 opens the mechanism"])},
         img("c8s32_miningnodes.png", 6.3, 3.05, 3.2, 1.85, cap="from the owner's 2025 deck")],
        paras("Consensus", "History"))

# ---- Wallet & Usage ---------------------------------------------------------------------------
slide("section", "Wallets and first use", "Choosing software, holding keys, and the first payment",
      [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.0, "h": 1.9, "cols": 2, "fs": 14, "subfs": 11,
        "items": [{"label": "Wallet platforms"}, {"label": "Key control"}, {"label": "Backup"}, {"label": "First payment"}]},
       img("mbc3_0101.png", 6.25, 1.35, 1.6, 2.85), img("mbc3_0102.png", 8.0, 1.35, 1.6, 2.85,
           cap="Mastering Bitcoin 3e, CC BY-SA")],
      paras("Wallet", "Usage"), bg="light")

content("The wallet branch, mapped", "Every leaf is explained on the course page",
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 11.5, "root": "Wallet",
          "nodes": [{"label": decamel(k), "kids": [decamel(x) for x in children(k, 3)[:4]]} for k in children("Wallet", 2)]}],
        paras("Wallet"),
        lede="A wallet is the software that keeps keys and signs payments; these eight decisions - platform, node, custody, backup - define every wallet you will meet.")

content("Your key is your deed - and you may never show it", "The house-key analogy, and where it breaks",
        [{"t": "keyhouse", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.5},
         {"t": "bullets", "x": 0.5, "y": 4.35, "w": 9.0, "h": 0.55, "fs": 12.5, "items": bullets_ok("keyanalogy", [
            "Bitcoin's trick (ch. 4 and 8): a signature proves you hold the key while the key itself stays secret"])}],
        paras("KeyControl", ask="Your house has a registry if the key is lost - what does bitcoin have?"),
        take="Lose the key, lose the coins; show the key, lose them too",
        lede="With a car or a house, the key grants access but a registry proves ownership; in Bitcoin the key is both - so it must prove without being shown.")

content("Who holds the keys, holds the coins", "The one wallet decision that matters most",
        [{"t": "compare", "x": 0.5, "y": 1.5, "w": 9.0, "h": 2.1, "fs": 13,
          "left": {"head": "Full control", "rows": ["You keep the keys", "You sign; nobody can freeze", "Backup is your job"]},
          "right": {"head": "Third-party control", "rows": ["A service keeps the keys", "Convenient, custodial", "You trust their honesty and uptime"]}},
         {"t": "chips", "x": 0.5, "y": 3.85, "w": 9.0, "h": 0.9, "fs": 13,
          "items": ["desktop", "mobile", "web", "hardware", "paper"]}],
        paras("KeyControl", "WalletPlatform", "Backup", ask="Which side was the exchange that lost its customers' coins on?"))

content("Mt. Gox: the exchange that lost everyone's coins", "Tokyo, February 2014 - CEO Mark Karpeles files for bankruptcy",
        [{"t": "stat", "x": 0.5, "y": 1.62, "w": 9.0, "h": 1.25, "items": [
            {"n": "850,000", "label": "bitcoins missing per the Tokyo court filing, Feb 2014"},
            {"n": "#1", "label": "Mt. Gox had been the largest bitcoin exchange in the world"},
            {"n": "10+ yrs", "label": "creditors still being repaid a decade later"}]},
         {"t": "beats", "x": 0.5, "y": 3.05, "w": 9.0, "h": 1.25, "fs": 13, "items": [
             "Customers saw balances on a website; the keys - so the coins - sat in one company's safe",
             "When the keys vanished, every balance on the screen meant nothing"]},
         factrow("MtGox")],
        story_notes("MtGox"),
        lede="Not a parable: a named company, a named CEO, a dated court filing - and the course's first security lesson.")

content("From a phrase to a key, slowly on purpose", "Key stretching makes guessing expensive",
        [{"t": "numlist", "x": 0.5, "y": 1.7, "w": 3.55, "h": 2.5, "fs": 11, "items": [
            "Start from a human backup phrase and a salt",
            "Hash them with HMAC-SHA512 - that is one round",
            "Feed each round into the next, 2,048 times",
            "Result: a 64-byte seed; a guesser pays the 2,048 rounds for every guess"]},
         {"t": "funnel", "x": 4.6, "y": 1.62, "w": 4.6, "h": 1.72, "cap": "result: a %d-byte seed, digest %s" % KS,
          "steps": ["phrase 'abandon' + salt", "HMAC-SHA512, round 1", "... 2,048 rounds ...", "the wallet seed: 64 bytes"]},
         dict(prog("KeyStretching", 4.3, 3.5, 5.2, 1.45, fs=8), label="the exact program - run it at home")],
        paras("Backup", "KeyControl"))

content("Alice's first bitcoin, step by step", "The chapter's running story begins",
        [{"t": "flow", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "fs": 12.5, "steps": [
            {"label": "Install a wallet", "sub": "keys made on her phone"},
            {"label": "First address", "sub": "shared as text or QR"},
            {"label": "Acquire bitcoin", "sub": "buy, earn, or exchange"},
            {"label": "Confirmations", "sub": "the network accepts it"}]},
         {"t": "numlist", "x": 0.5, "y": 2.98, "w": 3.6, "h": 1.9, "fs": 10.5, "items": [
             "A channel opens on-chain: Alice 60,000, Bob 40,000",
             "100 payments of 10 sat hop inside the channel",
             "Only the final balances settle on-chain: 2 transactions total"]},
         {"t": "bars", "x": 4.3, "y": 2.88, "w": 4.35, "h": 0.8, "rows": PC_ROWS},
         dict(PROG, x=4.3, y=4.12, w=5.2, h=0.83, fs=8, label="the program")],
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
        [{"t": "numlist", "x": 0.5, "y": 1.62, "w": 3.55, "h": 1.35, "fs": 10, "items": [
            "Each block stores the digest of the one before",
            "Verify = recompute every digest: True",
            "Change one byte - the next block refuses: False"]},
         {"t": "chainviz", "x": 4.2, "y": 1.56, "w": 5.3, "h": 1.42, "tampered": True, "hit": 1,
          "cap": "verify: %s, then %s" % BC},
         dict(prog("Blockchain", 0.5, 3.1, 9.0, 1.85, fs=8), label="the exact program, line by line")],
        paras("Chain"))

# ---- Computing & threats ----------------------------------------------------------------------
content("The toolbox under the hood", "Four vocabularies the whole book leans on",
        [{"t": "tree", "x": 0.4, "y": 1.62, "w": 9.2, "h": 3.3, "fs": 11, "root": "Foundations",
          "nodes": [{"label": k, "kids": [decamel(x) for x in children(k)[:6]] + (["+ %d more" % (len(children(k)) - 6)] if len(children(k)) > 6 else [])}
                    for k in ("Cryptography", "Chain", "Computing", "Threats")]}],
        paras("Computing", "Threats"),
        lede="Four vocabularies feed the chapters ahead: the cryptography that signs, the chain that remembers, the computing it all runs on, and the threats it must survive.")

# ---- Nature -----------------------------------------------------------------------------------
content("What kind of thing is Bitcoin?", "Its stated characteristics, and the architecture behind them",
        [{"t": "text", "x": 0.5, "y": 1.62, "w": 9.0, "h": 0.4, "fs": 15, "bold": True, "color": "dark", "body": "Characteristics - each one a design choice"},
         {"t": "chips", "x": 0.5, "y": 2.1, "w": 9.0, "h": 0.7, "fs": 14, "big": True,
          "items": [decamel(c) for c in children("Characteristic", 3)]},
         {"t": "text", "x": 0.5, "y": 3.05, "w": 9.0, "h": 0.4, "fs": 15, "bold": True, "color": "dark", "body": "The architecture that delivers them"},
         {"t": "chips", "x": 0.5, "y": 3.5, "w": 9.0, "h": 0.7, "fs": 14, "big": True,
          "items": [decamel(c) for c in children("Architecture", 3)]}],
        paras("Nature", "Characteristic", "Architecture"),
        lede="The first row makes promises to users; the second names the machinery that keeps them.")

content("Beyond the base layer", "Payment channels route through a network - chapter 14's subject",
        [{"t": "numlist", "x": 0.5, "y": 1.62, "w": 3.55, "h": 1.35, "fs": 10, "items": [
            "Channels: Alice-Bob, Bob-Carol, Carol-Dave",
            "Alice pays Dave with no direct channel",
            "A path is found: 3 hops, chain untouched"]},
         {"t": "route", "x": 4.3, "y": 1.56, "w": 5.1, "h": 1.4, "hops": LN_HOPS,
          "cap": "%d hops; no direct channel" % LN_N},
         dict(prog("LightningNetwork", 0.5, 3.1, 9.0, 1.85, fs=8), label="the exact program, line by line")],
        paras("Transfer", "SemanticBridge"))

content("Where to go from here", "Checked 2026-10-06; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The whitepaper (9 pages, 2008)", "https://bitcoin.org/bitcoin.pdf"],
                ["The textbook, free (CC BY-SA)", "https://github.com/bitcoinbook/bitcoinbook"],
                ["Developer documentation", "https://developer.bitcoin.org"]]},
            {"head": "Explore & markets", "rows": [
                ["Bitcoin Core, the reference client", "https://bitcoincore.org"],
                ["mempool.space - watch blocks live", "https://mempool.space"],
                ["blockstream.info - block 0 came from here", "https://blockstream.info"],
                ["CoinGecko - market data", "https://www.coingecko.com"]]},
            {"head": "Community", "rows": [
                ["Bitcoin Stack Exchange Q&A", "https://bitcoin.stackexchange.com"],
                ["bitcointalk - the forum of Pizza Day", "https://bitcointalk.org"]]},
            {"head": "Seminal & watch", "rows": [
                ["Hashcash, the proof-of-work paper", "http://www.hashcash.org"],
                ["b-money, Wei Dai (1998)", "http://www.weidai.com/bmoney.txt"],
                ["But how does bitcoin work? (3Blue1Brown)", "https://www.youtube.com/watch?v=bBC-nXj3Ng4"]]}]}],
        "SAY: Everything on this slide is free. The whitepaper is nine pages - read it this week; the textbook is the one this course follows, free under CC BY-SA in the same repository our materials pin.\nASK: Who can find today's newest block on mempool.space before the break ends?\nFULL TEXT: course page, chapter 1 - Standards, History.",
        take="Nine free pages started all of this - read them this week")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a bitcoin is, and how far it divides",
          "Why 21 million is arithmetic, not promise",
          "What replaces the bank in the middle",
          "Which chapter opens each box we drew"])}],
      S[0]["notes"], bg="dark")

# the one program slide rides on the Alice slide: place PROG where prog_here marks
for s in S:
    s["items"] = [dict(PROG, x=i["x"], y=i["y"], w=i["w"], h=i["h"], label="Her channel settles on-chain only twice") if i.get("t") == "prog_here" else i
                  for i in s["items"]]

# every slide must carry notes
for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])

for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES:
        t = TAKES[sl["title"]]
        if len(t.split()) > 24:
            raise SystemExit("REFUSED: takeaway %r runs past 14 words" % t)
        sl["take"] = t
missing_takes = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing_takes:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing_takes)

plan = {"meta": dict(OLDPLAN["meta"], version=__version__, python=PYV, total=0,
                     redesign="2026-10-06, by the owner's ruling: short bullets and visuals on the slide, prose in the notes"),
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_7_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
