#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - chapter 6 (Transactions) for the classroom, at the chapter-1 standard as chapter 5
carries it (CME materials look-and-feel v1.0.0), drawn by the SHARED renderer 08-tooling/deck_render_v1_0_0.js.

Every '>>>' row comes from examples_out_v1_0_0.json and is re-run off the finished file by deck_check_v1_0_0.py.
Alice's transaction is parsed field by field with the chapter's own library, its identifier and its weight (569,
the figure the book took from bitcoin-cli) are recomputed from the bytes and compared with an independent
explorer's saved record - no node is available here, and the slide says so - and the three native charts (dust
thresholds, the subsidy schedule, the weight of every field) are drawn ONLY from executed examples.

What differs from chapter 5's deck_build_v2_0_0.py, and why: the speaker notes follow the owner's ruling of
2026-10-08 - the decks are published and students read the notes - so every note is reader's prose in full
sentences (what the slide shows, why it matters, what to look at, one question to think about, where the full text
is), with no SAY/ASK/STORY/FULL TEXT labels; 08-tooling/deck_notes_check_v1_0_0.py refuses the old form and is run
on the finished file. Four stories instead of three, one without a photograph (no free-licence photograph of
Mt. Gox could be verified), shown through its figures as chapter 5 did for its third story.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json beside itself)
"""
__version__ = "1.0.0"

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


import sys
sys.path.insert(0, os.path.join(HERE, ".."))
C = load("corpus6", os.path.join(HERE, "..", "sen0401_ch06_corpus_v1_0_0.py"))
ST = load("stories6", os.path.join(HERE, "..", "sen0401_ch06_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch06/assets/"
for _f in ("photo_hal_finney_1972.jpg", "photo_papa_johns_jacksonville.jpg", "photo_gavin_andresen_2014.jpg",
           "mbc3_0601.png", "mbc3_0602.png", "mbc3_0603.png", "mbc3_0604.png", "mbc3_0605.png", "mbc3_0606.png"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: v for k, v in EX.items() if not k.startswith("_")}

BYNAME = {n[0]: n for n in C.NODES}
LABEL = {n[0]: (n[1] or n[0]) for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in G.values() for _, out in rows)
STORYTEXT = " ".join(s["story"] + " " + s["source"] + " " + s["when"] for s in ST.STORIES)


def _sentences(text, k=2):
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:k])


def _section_of(name):
    n = BYNAME[name]
    while n[2] > 2:
        n = BYNAME[n[3]]
    return LABEL[n[0]]


def notes(*names, look=None, think=None):
    """Reader's prose for the published deck: what the slide shows (the opening sentences of the first concept's own
    explanation), what to look at, one question to think about, and where the full text is - all as sentences."""
    for nm in names:
        if nm not in BYNAME:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
    lead = BYNAME[names[0]][5][0][1]
    shows = _sentences(lead, 2)
    if len(shows) > 520:
        shows = _sentences(lead, 1)
    out = shows
    if look:
        out += " " + look.rstrip(".") + "."
    if think:
        out += " A question to think about is this: " + think.rstrip(".?") + "?"
    secs = sorted({_section_of(nm) for nm in names})
    out += " The full explanation is on the course page, chapter 6, under " + " and ".join(secs) + \
           (", in the concept" if len(names) == 1 else ", in the concepts") + " " + ", ".join(LABEL[nm] for nm in names) + "."
    return out


def story_notes(sid, look=None):
    st = STORY[sid]
    out = "This is a true story, dated %s. %s" % (st["when"], st["story"])
    if look:
        out += " " + look.rstrip(".") + "."
    out += " The lesson the slide carries is that %s. The sources are these. %s" % (st["lesson"][0].lower() + st["lesson"][1:], st["source"])
    return out


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


def code(group, x, y, w, h, fs=11, rows=None):
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    nlines = sum(1 + (1 if out.strip() else 0) for _, out in rr)
    fit = (w - 0.4) / (maxlen * 0.00842)
    fit_h = (h - 0.30) * 72.0 / (nlines * 1.3)
    fs = min(fs, round(fit, 1), round(fit_h, 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fx%.1fin (needs %.1f pt)" % (group, w, h, fs))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


BOOKCAP = "Antonopoulos & Harding, Mastering Bitcoin 3e, CC BY-SA"

# verified figures parsed back out of the executed examples
import ast as _ast
_wt = _ast.literal_eval(G["WeightUnits"][-1][1])
assert sum(_wt) == 569 and len(_wt) == 12, _wt
_sub = _ast.literal_eval(G["BlockSubsidy"][0][1])
assert _sub[0] == 50.0 and _sub[4] == 3.125 and len(_sub) == 9
_dust = _ast.literal_eval(G["DustLimit"][3][1])
assert _dust == [546, 294, 330, 0]
assert _ast.literal_eval(G["Weight"][0][1]) == (569, 569) and _ast.literal_eval(G["Weight"][1][1])[0] == 569, "the weight no longer matches the explorer's record"
assert G["Segwit"][-1][1] == "(True, False)", "the witness no longer stays out of the txid"

S = []


def slide(kind, title, sub, items, notes_text, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes_text, "bg": bg})


def content(title, sub, items, notes_text, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes_text, "bg": "light"}
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
        for it in items:
            top = it["y"] - (0.3 if it.get("t") == "code" and it.get("label") else 0)
            if top < 1.68:
                raise SystemExit("REFUSED: %r starts at %.2f in under the lede of %r" % (it.get("label") or it.get("t"), top, title))
        sl["lede"] = lede
    if take:
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes_text, image=None):
    items = [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3 if image else 8.6, "h": 1.9,
              "cols": 2 if image else min(4, len(boxes)), "fs": 14, "subfs": 11, "items": boxes}]
    if image:
        items.append(image)
    slide("section", title, sub, items, notes_text, bg="light")


# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 6: Transactions", "One real transaction, 194 bytes, read field by field - and every number recomputed",
      [img("mbc3_0601.png", 5.7, 1.1, 3.9, 2.6, cap="a byte map of Alice's transaction - " + BOOKCAP)],
      "This deck reads one real Bitcoin transaction, Alice's payment to Bob from the book's own example, byte by byte. "
      "Every number on the slides was computed from those bytes with the Python standard library and the chapter's own "
      "library, and the identifier and the weight were compared with an independent explorer's record of the same "
      "transaction, because no Bitcoin Core node was available where this deck was built. The full text of every slide is "
      "on the course page for chapter 6.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0,
          "items": [re.sub(r",.*", "?", q) if len(q.split()) > 20 else q for q in C.CQS]}],
        notes("TransactionAnatomy", look="The seven questions are the chapter's own competency questions, and each one is answered by a slide range of this deck and in full on the course page",
              think="which of the seven you could already answer from chapters 2 and 3"))

content("One chapter, eight branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 4, "fs": 12.5, "subfs": 10, "accent": [2],
          "items": [{"label": LABEL[r], "sub": "%d concepts" % len([n for n in C.NODES if n[3] == r or (n[3] in children(r))])}
                    for r in ("TransactionAnatomy", "VersionMarkerFlag", "Inputs", "SequenceField", "Outputs", "Witnesses", "LockTimeAndCoinbase", "WeightAndFoundations")]}],
        notes("TransactionAnatomy", "Inputs", look="The count under each branch is how many concepts the course page explains for it; the deck walks the spine of the eight in the order the bytes are serialized",
              think="why the sequence field, four bytes inside each input, earns a branch of its own"),
        lede="Eight branches, one per field group; the deck follows the bytes in order and stops at four true stories.",
        take="Eight branches - every slide today lives on this map")

# ---- Part 1: a transaction, byte by byte ------------------------------------------------------
section("A transaction, byte by byte", "What a transaction asks of strangers, and how it is written as bytes",
        [{"label": "The request"}, {"label": "194 bytes"}, {"label": "Inputs and outpoints"}, {"label": "Byte order"}],
        notes("TransactionAnatomy", "SerializationFormats", look="The picture is the book's map of the inputs field of Alice's transaction, which the slides of this part recompute from the hexadecimal",
              think="what a transaction would have to contain if it were a message to Bob rather than a request to full nodes"),
        image=img("mbc3_0602.png", 6.1, 2.2, 3.5, 1.05, cap="the inputs field of Alice's transaction - " + BOOKCAP))

content("Ten bitcoins to Hal Finney, block 170", STORY["FirstTransaction"]["when"],
        [img("photo_hal_finney_1972.jpg", 0.5, 1.45, 2.6, 2.95, cap="Hal Finney, 1972 - Daily News-Post, public domain"),
         {"t": "beats", "x": 3.4, "y": 1.45, "w": 6.1, "h": 1.45, "fs": 12.5, "items": [
             "11 January 2009: Finney posts two words, running bitcoin",
             "The next day the author of the software sends him 10 BTC",
             "One input spends the coinbase of block 9; two outputs, 10 and 40 BTC",
             "Legacy format: no marker, no flag, no witness - parsed below"]},
         dict(code("LegacyFormat", 3.4, 3.28, 6.1, 0.8, fs=9, rows=G["LegacyFormat"][1:]), label="the first transaction, from its saved bytes"),
         factrow("FirstTransaction", x=3.4, y=4.42, w=6.1)],
        story_notes("FirstTransaction", look="The console parses the saved bytes of that transaction and finds no segwit marker and the block height 170, which is what the explorer records too"))

content("194 bytes, seven fields", "Alice's transaction parsed by the chapter's own library",
        [dict(code("SerializedTransaction", 0.5, 1.98, 9.0, 1.2, fs=9.5), label="size, version, marker and flag, counts, lock time: version 1, extended format, one input, two outputs"),
         dict(code("ByteMap", 0.5, 3.42, 9.0, 0.85, fs=9), label="the fixed fields at their offsets; all the spans sum to 194 bytes"),
         {"t": "chips", "x": 0.5, "y": 4.58, "w": 9.0, "h": 0.4, "fs": 10, "items": ["extended format, version 1", "1 in, 2 out, 1 witness", "lock time 0"]}],
        notes("SerializedTransaction", "ByteMap", look="Read the first console from the top: the two lengths agree, the marker is zero and the flag one, and the counts are what the byte map shows",
              think="why a parser must read the input count before it can find the lock time"),
        lede="The legacy form is 125 bytes; the marker, the flag and the 67-byte witness structure are the other 69.",
        take="Every byte belongs to a named field, and the fields are found in order")

content("Inputs: an outpoint, read both ways round", "32 bytes of identifier, 4 of index - and the byte order that trips everyone",
        [dict(code("Outpoint", 0.5, 1.5, 9.0, 1.45, fs=9), label="the outpoint: the identifier in internal order, index 1, and the 100,000-satoshi output in block 774,958"),
         dict(code("DisplayByteOrder", 0.5, 3.25, 9.0, 1.2, fs=9), label="the fold-tac pipeline in Python: the reversed bytes equal the identifier the library computes"),
         {"t": "chips", "x": 0.5, "y": 4.6, "w": 9.0, "h": 0.4, "fs": 11, "items": ["eb3a... hashed", "4ac5... shown", "two spellings"]}],
        notes("Outpoint", "DisplayByteOrder", look="The reversed identifier in the right console equals the identifier the library computes for the previous transaction, which is the check that the reversal is the right one",
              think="which of the two spellings an explorer shows, and which one a node hashes"),
        take="An input states no amount; the node reads it from the output the outpoint names")

content("10,000 bitcoins for two pizzas", STORY["PizzaDay"]["when"],
        [img("photo_papa_johns_jacksonville.jpg", 0.5, 1.45, 2.4, 2.95, cap="the plaque at Papa John's, Jacksonville - photo: Sanjev Rajaram, CC0"),
         {"t": "beats", "x": 3.2, "y": 1.45, "w": 6.3, "h": 1.2, "fs": 12.5, "items": [
             "22 May 2010: Laszlo Hanyecz pays 10,000 BTC for two pizzas",
             "131 inputs, one output, and 0.99 BTC left to the miner as fee",
             "Block 57,043 - and the whole 23,620-byte transaction parses below"]},
         dict(code("InputCount", 3.2, 3.0, 6.3, 1.2, fs=8.5), label="the pizza transaction: inputs, output, fee, identifier"),
         factrow("PizzaDay", x=3.2, y=4.5, w=6.3)],
        story_notes("PizzaDay", look="The console counts the 131 inputs twice, once from the parsed list and once from the single count byte 0x83, and recomputes the identifier that the explorer and the forum thread name"))

# ---- Part 2: sequence and lock time -----------------------------------------------------------
section("Sequence and lock time", "Four bytes with three meanings, and four bytes with three readings",
        [{"label": "The card game"}, {"label": "Replace by fee"}, {"label": "BIP68 timelocks"}, {"label": "Lock time and MTP"}],
        notes("SequenceField", "LockTime", look="The figure is BIP68's own layout of the sequence field as the book reproduces it: the disable flag, the type flag and the sixteen bits of value",
              think="how one field can carry three meanings without the three ever colliding"),
        image=img("mbc3_0603.png", 6.1, 2.3, 3.5, 0.5, cap="BIP68's layout of the sequence field - " + BOOKCAP))

content("One field, three meanings", "Final, replaceable, or a relative timelock - decided bit by bit",
        [{"t": "flow", "x": 0.5, "y": 1.5, "w": 9.0, "h": 0.95, "fs": 11.5, "steps": [
            {"label": "0xffffffff", "sub": "final: no replacement, no lock"},
            {"label": "below 0xfffffffe", "sub": "BIP125: replaceable"},
            {"label": "below 2^31, v2", "sub": "BIP68: a relative timelock", "hot": True}]},
         dict(code("Bip125Signal", 0.5, 2.75, 9.0, 0.75, fs=8.5), label="the BIP125 threshold, tested on three values"),
         dict(code("Bip68Timelock", 0.5, 3.75, 9.0, 1.2, fs=8.5), label="30 blocks from 774,958; an hour in 512-second units; the constants")],
        notes("SequenceNumber", "Bip68Timelock", look="The first console shows that 0xfffffffe does not signal while 0xfffffffd does; the second shows the lock of 30 blocks landing at 774,988 and an hour rounding up to eight units of 512 seconds",
              think="why a transaction that sets a relative timelock also, unavoidably, signals replaceability"),
        take="Bit 31 of the sequence is this chapter's security bit")

content("Lock time, and the clock it is checked against", "A height below 500,000,000, a time above it, and the median of eleven blocks",
        [{"t": "flow", "x": 0.5, "y": 1.5, "w": 9.0, "h": 0.95, "fs": 11.5, "steps": [
            {"label": "0", "sub": "eligible for any block"},
            {"label": "below 500,000,000", "sub": "a block height: that block or later"},
            {"label": "500,000,000 or more", "sub": "an epoch time, against the median time past", "hot": True}]},
         dict(code("LockTimeField", 0.5, 2.85, 9.0, 0.95, fs=9), label="Alice's lock time is 0; the transaction that funded her used 774,957 and confirmed in 774,958"),
         dict(code("MedianTimePast", 0.5, 4.1, 9.0, 0.8, fs=9), label="eleven block times, their median, and how far it trails the newest: 600 seconds here")],
        notes("LockTimeField", "MedianTimePast", look="The first console decodes Alice's zero, the funding transaction's 774,957 and a block's time; the second sorts eleven timestamps and takes the sixth, which trails the newest by 600 seconds in this sample",
              think="why a time lock set for noon is usually only satisfiable in the early afternoon"),
        take="Lock time says not before; nothing in a transaction can say not after")

# ---- Part 3: outputs --------------------------------------------------------------------------
section("Outputs", "Satoshis, the consensus range, dust, and the script that says who may spend",
        [{"label": "Amounts"}, {"label": "The 2010 overflow"}, {"label": "Dust"}, {"label": "Output scripts"}],
        notes("Outputs", "OutputList", look="The figure is the book's map of the outputs field: a count, then for each output eight bytes of amount, a length and a script",
              think="why the fee is written nowhere in these bytes"),
        image=img("mbc3_0604.png", 6.1, 2.0, 3.5, 1.35, cap="the outputs field - " + BOOKCAP))

content("Amounts: 20,000, 75,000, and a 5,000 fee", "8-byte signed integers of satoshis, and the fee nobody writes down",
        [dict(code("AmountField", 0.5, 1.5, 9.0, 1.3, fs=9), label="the two amounts, the fee as a difference, and the consensus maximum"),
         dict(code("OutputScript", 0.5, 3.1, 9.0, 0.75, fs=8.5), label="each output's script: 34 bytes of taproot for Bob, 22 bytes of version 0 for the change"),
         {"t": "chips", "x": 0.5, "y": 4.15, "w": 9.0, "h": 0.6, "fs": 12, "items": ["100,000 in", "20,000 + 75,000 out", "5,000 fee", "max 2,100,000,000,000,000"]}],
        notes("AmountField", "OutputScript", look="The fee in the first console is computed as the previous output's amount minus the two new amounts, and it equals the fee the explorer reports",
              think="what a wallet shows as a balance when the chain holds only whole outputs"),
        take="An output is an amount and a condition; no field holds a balance or a fee")

content("The block that created 184 billion bitcoins", STORY["ValueOverflow"]["when"],
        [img("photo_gavin_andresen_2014.jpg", 0.5, 1.45, 2.2, 2.95, cap="Gavin Andresen, 2014 - photo: Stephen McCarthy / Web Summit, CC BY 2.0"),
         {"t": "beats", "x": 3.0, "y": 1.45, "w": 6.5, "h": 1.2, "fs": 12, "items": [
             "15 August 2010: block 74,638 holds two outputs of 92,233,720,368.54 BTC",
             "Summed as 64-bit integers they wrap to a small negative number: the check passes",
             "A patch within five hours, 0.3.10 the next day, the chain reorganised at 74,691"]},
         dict(code("AmountRange", 3.0, 3.0, 6.5, 1.2, fs=7.5), label="the overflow reproduced, and refused by the range check Core still cites"),
         factrow("ValueOverflow", x=3.0, y=4.5, w=6.5)],
        story_notes("ValueOverflow", look="The console doubles the overflowing amount as a 64-bit signed integer, obtains the negative sum of 997,538 satoshis that the 2010 check accepted, and shows that the money-range check refuses both the sum and each output"))

content("Dust, measured", "Bitcoin Core's threshold is a size times a rate - and it depends on the output type",
        [{"t": "chart", "x": 0.45, "y": 1.72, "w": 4.5, "h": 3.15, "ctype": "bar",
          "title": "Dust threshold by output type (satoshis, 3,000 sat/kvB)",
          "dataLabels": True, "dlFmt": "0", "dlFs": 9,
          "labels": ["P2PKH (legacy)", "P2WPKH (segwit v0)", "P2TR (taproot)", "OP_RETURN"],
          "series": [{"name": "dust threshold", "data": _dust}]},
         dict(code("DustLimit", 5.1, 2.0, 4.4, 1.6, fs=7.5), label="the four thresholds, and the sizes behind two of them"),
         {"t": "numlist", "x": 5.1, "y": 3.75, "w": 4.4, "h": 1.15, "fs": 10, "items": [
             "Output size plus the smallest input that could spend it, times 3 satoshis a byte",
             "An OP_RETURN output can never be spent, so it is never dust"]}],
        notes("DustLimit", "DataCarrierOutput", look="The bars are computed, never quoted: the console's fourth line produced them, and the last line shows the rate and the sizes that give 546 and 294",
              think="why a 600-satoshi output passes the dust policy and may still not be worth spending on a busy day"),
        lede="The bars are the console's own output; the checker re-runs it off this file.",
        take="Dust is a policy about who pays for the UTXO set: everyone, for ever")

# ---- Part 4: witnesses ------------------------------------------------------------------------
section("Witnesses", "Where the proof of authorisation lives, and why it moved",
        [{"label": "Malleability"}, {"label": "Mt. Gox, 2014"}, {"label": "Segregated witness"}, {"label": "The soft fork"}],
        notes("Witnesses", "WitnessIdea", look="The figure is the book's map of the witness structure: one stack for Alice's one input, holding one 65-byte item, her signature",
              think="what a court would ask of a witness that it cannot ask of a number"),
        image=img("mbc3_0605.png", 6.1, 2.0, 3.5, 1.35, cap="the witness structure - " + BOOKCAP))

content("Malleability: the same spend, four identifiers", "Re-encode a push in a legacy input script and the txid changes; outside the txid it cannot",
        [dict(code("PushEncoding", 0.5, 1.5, 9.0, 1.05, fs=7.5), label="four ways to push the number 2: four identifiers for the first bitcoin transaction"),
         dict(code("Segwit", 0.5, 2.85, 9.0, 1.25, fs=8), label="Alice's txid is the hash of the 125 legacy bytes; a new witness changes the wtxid, not the txid"),
         {"t": "when", "x": 2.3, "y": 4.4, "w": 5.4, "body": "the witness is outside the txid - by design"}],
        notes("ThirdPartyMalleability", "Segwit", look="The first console's set has four members, one per encoding; the second console's last line is the whole of segregated witness in two booleans",
              think="what Bob loses when a stranger's re-encoded copy of Alice's transaction confirms instead of hers"),
        take="What a hash covers decides what can be built on it")

content("Mt. Gox blames malleability", STORY["GoxMalleability"]["when"],
        [{"t": "stat", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.2, "items": [
            {"n": assert_fact("302,000 BTC", "gox"), "label": "ever involved in malleability attacks (Decker and Wattenhofer)"},
            {"n": assert_fact("1,811 BTC", "gox"), "label": "of those before the press release of 10 February"},
            {"n": assert_fact("850,000 BTC", "gox"), "label": "the shortfall declared in the filing of 28 February"}]},
         {"t": "beats", "x": 0.5, "y": 2.95, "w": 9.0, "h": 1.3, "fs": 12, "items": [
             "Withdrawals halted on 7 February; the press release blamed a bug in the bitcoin software",
             "Researchers who had recorded the network for a year found no widespread attacks before the announcement",
             "Software that tracked payments by txid saw mutated copies as failed payments"]},
         factrow("GoxMalleability")],
        story_notes("GoxMalleability", look="The three figures are the paper's and the bankruptcy filing's, as the fact row's link gives them; no free-licence photograph of the exchange could be verified, so the slide shows the numbers"))

content("Segregated witness as a soft fork", "Old nodes allow an empty input script; new nodes require one",
        [{"t": "compare", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.75, "fs": 11.5,
          "left": {"head": "What an old node sees", "rows": ["A script of a number 0-16 and 2-40 bytes: anyone can spend it", "An empty input script is allowed", "Every segwit block is valid to it"]},
          "right": {"head": "What a new node requires", "rows": ["The same template is a witness program with a version", "The input script must be empty", "A valid witness in the witness structure"]}},
         dict(code("WitnessProgram", 0.5, 3.55, 9.0, 0.95, fs=8.5), label="Alice's outputs are witness programs of versions 1 and 0; her input script is empty, her witness 65 bytes"),
         {"t": "chips", "x": 0.5, "y": 4.65, "w": 9.0, "h": 0.4, "fs": 11, "items": ["reject more", "accept no more", "block 481,824 - August 2017"]}],
        notes("SoftFork", "WitnessProgram", look="The two columns are the book's own sentence turned into a table, and the console checks it on Alice's bytes: two witness programs, an empty input script, a witness item",
              think="why a change that only tightens the rules can be enforced by a minority of nodes while a change that loosens them cannot"),
        take="A soft fork can only restrict; upgrades are built on anyone-can-spend")

# ---- Part 5: coinbase and weight --------------------------------------------------------------
section("The coinbase and the weight", "Where bitcoins come from, and how a block is filled",
        [{"label": "Null outpoint"}, {"label": "The subsidy"}, {"label": "Maturity"}, {"label": "Weight and vbytes"}],
        notes("CoinbaseTransaction", "WeightUnits", look="The figure is the book's map of Alice's transaction drawn in weight units rather than bytes: the witness shrinks to a quarter and everything else stays",
              think="why the two maps of the same transaction have different shapes"),
        image=img("mbc3_0606.png", 6.1, 1.8, 3.5, 2.0, cap="the same transaction in weight units - " + BOOKCAP))

content("The subsidy, halving by halving", "50 BTC shifted right once per 210,000 blocks - down to one satoshi, then zero",
        [{"t": "chart", "x": 0.45, "y": 1.72, "w": 4.4, "h": 3.15, "ctype": "bar",
          "title": "Block subsidy at each halving (BTC)",
          "dataLabels": True, "dlFmt": "0.####", "dlFs": 8,
          "labels": ["%d" % (h * 210000) for h in range(9)],
          "series": [{"name": "subsidy", "data": _sub}]},
         dict(code("BlockSubsidy", 5.0, 2.0, 4.5, 1.2, fs=8, rows=G["BlockSubsidy"][1:]), label="one satoshi from 6,720,000, zero from 6,930,000"),
         dict(code("MaturityRule", 5.0, 3.55, 4.5, 1.3, fs=8), label="block 170 spends block 9's coinbase: mature")],
        notes("BlockSubsidy", "MaturityRule", look="The bars are the first executed line of the subsidy example; the console beside them shows where the schedule ends, which is 209,999 blocks later than the figure the book names",
              think="why the schedule sums to a little under 21 million and never exactly to it"),
        lede="Nine halvings drawn from one executed line; the library and Core's GetBlockSubsidy agree on every bar.",
        take="The coinbase is the only transaction that creates bitcoins")

content("569: the weight, field by field", "The book's table recomputed from the bytes - and Bitcoin Core's figure matched without a node",
        [{"t": "chart", "x": 0.45, "y": 1.72, "w": 4.4, "h": 3.15, "ctype": "bar",
          "title": "Weight of each field of Alice's transaction",
          "dataLabels": True, "dlFmt": "0", "dlFs": 8,
          "labels": ["version", "marker+flag", "in count", "outpoint", "in script", "sequence", "out count", "amounts", "out scripts", "wit count", "wit items", "lock time"],
          "series": [{"name": "weight", "data": _wt}]},
         dict(code("Weight", 5.0, 2.0, 4.5, 1.3, fs=8), label="569 from the bytes and from the explorer; 143 vbytes"),
         dict(code("WeightFactor", 5.0, 3.65, 4.5, 1.2, fs=8), label="the spans that weigh one per byte; the header")],
        notes("Weight", "WeightFactor", look="The twelve bars are the book's twelve rows, each computed from the byte spans the parser recorded, and they sum to 569; the console shows the same 569 three ways, the third being the explorer's saved record",
              think="why the witness item of 65 bytes weighs less than the 34-byte script that pays Bob"),
        lede="No node ran here: 569 is recomputed from the bytes and compared with the explorer's saved record.",
        take="Weight is what a transaction pays for, and witness bytes cost a quarter")

# ---- summary, resources, closing --------------------------------------------------------------
content("The chapter in five lines", "One line per part - each one provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A transaction is a request to strangers: inputs point, witnesses prove, outputs assign - 194 bytes, every one named",
            "The sequence field has meant three things; the lock time is read against the median of eleven blocks",
            "An output is an amount and a condition; the fee is a difference, and dust is a policy about everyone's database",
            "Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork",
            "The coinbase creates under a schedule that ends at block 6,929,999, and weight is what a block is filled by"]}],
        "These five lines are the deck in miniature, one per part, and each of them is carried by a slide range that the agenda "
        "names. A line that feels unproven should send the reader back to its consoles, because every figure in it was computed "
        "on a slide. The full text behind all five lines is on the course page for chapter 6.",
        take="If a line feels unproven, its part's slides carry the receipt")

content("Where to go from here", "Checked 2026-10-08; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["This chapter, free (CC BY-SA)", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/ch06_transactions.adoc"],
                ["The malleability paper behind the Mt. Gox story", "https://arxiv.org/abs/1403.6676"]]},
            {"head": "Standards", "rows": [
                ["BIP 141 - segregated witness, weight", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0141.mediawiki"],
                ["BIP 68 - the relative timelock", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0068.mediawiki"],
                ["BIP 125 - opt-in replace-by-fee", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0125.mediawiki"]]},
            {"head": "Tools", "rows": [
                ["Alice's transaction on mempool.space", "https://mempool.space/tx/466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177"],
                ["learnmeabitcoin - a raw transaction, drawn", "https://learnmeabitcoin.com/technical/transaction/"]]},
            {"head": "Community", "rows": [
                ["Pizza for bitcoins? - the 2010 thread", "https://bitcointalk.org/index.php?topic=137.0"],
                ["Strange block 74638 - the overflow, live", "https://bitcointalk.org/index.php?topic=822.0"]]}]}],
        "Everything here is free to read, and every link was fetched on the date in the subtitle. A good exercise is to take "
        "any confirmed transaction from the explorer, paste its hexadecimal into the chapter's library on the course page, and "
        "check that the identifier and the weight you compute are the ones the explorer shows. The course page for chapter 6 "
        "carries the full resource list with a sentence on why each entry is there.",
        take="Parse any transaction yourself and match the explorer's identifier and weight")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "What a transaction asks full nodes to do, field by field",
          "What the sequence and lock time permit, and when",
          "Why identifiers were malleable, and how segwit fixed it",
          "How 569 is computed, and who creates bitcoins under which schedule"])}],
      "Four claims, each carried by a computation that ran on a slide of this deck against the chapter's own transaction, "
      "the standards and Bitcoin Core's sources. The course page for chapter 6 carries every word behind them, the stories "
      "with their sources, and the question bank to test the four claims on yourself.", bg="dark")

# ---- agenda -----------------------------------------------------------------------------------
S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and at the end, a transaction you have parsed yourself",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d, _e = (_sec[t] for t in ("A transaction, byte by byte", "Sequence and lock time", "Outputs", "Witnesses", "The coinbase and the weight"))
_rows = [("Questions and the chapter map", 3, _a),
         ("A transaction, byte by byte - block 170 and the pizza", _a + 1, _b),
         ("Sequence and lock time - three meanings, three readings", _b + 1, _c),
         ("Outputs - amounts, the 2010 overflow, dust", _c + 1, _d),
         ("Witnesses, the coinbase, the weight, and resources", _d + 1, len(S))]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.5,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") == "code")),
                      "label": "live-run consoles, each shown with its result"}]}]
S[1]["notes"] = ("The route has five parts and ends with a transaction the reader can parse alone. One story is the first "
                 "transaction ever to spend an output, one is the most expensive pizza in history, one is a block that briefly "
                 "created 184 billion bitcoins, and one is an exchange that blamed the protocol. The part a reader expects to be "
                 "hardest is worth marking now and checking at the summary slide.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for line in str(s["notes"]).splitlines():
        if re.match(r"^\s*(?:[A-Z][A-Z \-/&()0-9]{1,24}|say|ask|tell|show|story|cue|demo|note|full text|read|point|click|pause|transition|timing)\s*(?:\([^)]*\))?\s*:", line):
            raise SystemExit("REFUSED: slide %r carries a directive label in its notes: %r" % (s["title"], line[:60]))
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
_story_titles = {STORY[k]["title"] for k in STORY}
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl and sl["title"] not in _story_titles and sl["title"] != "The questions this chapter answers"]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 6: Transactions", "sub": "SEN0401, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-08, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0), notes as reader's prose"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
