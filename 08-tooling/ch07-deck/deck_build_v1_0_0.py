#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - chapter 7 (Authorization and Authentication) for the classroom, at the chapter-1 standard as
chapter 6 carries it (CME materials look-and-feel v1.0.0), drawn by the SHARED renderer 08-tooling/deck_render_v1_0_0.js.

Every '>>>' row comes from examples_out_v1_0_0.json and is re-run off the finished file by deck_check_v1_0_0.py. The rows run the
chapter's own stdlib-only Script interpreter (sen0401_ch07_script_lib_v1_0_0.py) on real, signed spends; no Bitcoin Core node was
available where this deck was built, and the interpreter is checked against Core's published test vectors instead (the slides say
so). The two native charts (what the 1,022 inputs of block 775,072 spend; the weight of the three paths of one contract) and the
tree chart are drawn ONLY from executed examples.

Differences from chapter 6's deck_build_v1_0_0.py: this chapter's corpus, stories (three, each with a licensed photograph) and
examples; speaker notes are the owner's ruling of 2026-10-08 (reader's prose in full sentences, no label-colon cues).
Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json beside itself)
"""
__version__ = "1.0.0"

import ast as _ast
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


sys.path.insert(0, os.path.join(HERE, ".."))
C = load("corpus7", os.path.join(HERE, "..", "sen0401_ch07_corpus_v1_0_0.py"))
ST = load("stories7", os.path.join(HERE, "..", "sen0401_ch07_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch07/assets/"
for _f in ("photo_satoshi_bust_budapest.jpg", "photo_bitcoin_mining_farm.jpg", "photo_claus_schnorr_1986.jpg",
           "mbc3_0702.png", "mbc3_0703.png", "mbc3_0705.png", "mbc3_0710.png"):
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
    """Reader's prose for the published deck: what the slide shows (the opening sentences of the first concept's own explanation),
    what to look at, one question to think about, and where the full text is - all as sentences."""
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
    out += " The full explanation is on the course page, chapter 7, under " + " and ".join(secs) + \
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
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"][:150].rsplit(",", 1)[0] if len(st["who"]) > 150 else st["who"],
            "where": st["where"][:150].rsplit(",", 1)[0] if len(st["where"]) > 150 else st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


BOOKCAP = "Mastering Bitcoin 3e, CC BY-SA"

# verified figures parsed back out of the executed examples
_cen = _ast.literal_eval(G["BlockCensus"][-1][1])
assert sum(v for _, v in _cen) == 1022 and _cen[0] == ("P2WPKH", 626), _cen
assert _ast.literal_eval(G["BlockCensus"][0][1]) == 1022
_tw = _ast.literal_eval(G["ScriptPathSpending"][1][1])
_ww = _ast.literal_eval(G["ScriptPathSpending"][2][1])
assert _tw == [577, 617, 414] and _ww == [585, 584, 509], (_tw, _ww)
_kp = _ast.literal_eval(G["Taproot"][3][1])
assert _kp == ("OK", 64, 308), _kp
_mast = _ast.literal_eval(G["Mast"][1][1])
assert [d for _, d in _mast] == [2, 3, 10, 20]
assert G["ChecksigAdd"][0][1] == "(104, 105)" and G["OpSuccess"][0][1] == "87"
assert G["OpReturnBug"][0][1] == "'OK'" and G["OpReturnBug"][1][1] == "'OP_RETURN'"

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


def story_slide(sid, photo, photo_box, beats, grp, rows, label, lookstr, code_box, beats_box, title=None):
    st = STORY[sid]
    items = [img(photo, *photo_box, cap=st["credit"]),
             {"t": "beats", "x": beats_box[0], "y": beats_box[1], "w": beats_box[2], "h": beats_box[3], "fs": 12, "items": beats},
             dict(code(grp, *code_box, fs=9, rows=rows), label=label),
             factrow(sid, x=beats_box[0] if code_box[0] > 1 else 0.5, y=4.62, w=9.5 - (beats_box[0] if code_box[0] > 1 else 0.5))]
    content(title or st["title"], st["when"], items, story_notes(sid, look=lookstr))


# ----------------------------------------------------------------------------------------------
slide("title", "Chapter 7: Scripts and Signatures", "Authorization and Authentication: scripts that lock coins, signatures that unlock them, every spend run in a real interpreter",
      [img("mbc3_0701.png", 4.1, 0.8, 5.3, 1.1, cap="locking and unlocking scripts - " + BOOKCAP)],
      "This deck explains how Bitcoin decides who may spend an output: the output carries a locking script, the spender supplies "
      "an unlocking script, and a node runs the two and accepts the spend only if the result is true. Every example on the slides "
      "was executed by this course's own Python port of Bitcoin's script interpreter on real, signed spends, because no Bitcoin "
      "Core node was available where the deck was built; the port is checked against Core's published test vectors and against "
      "every input of a real block. The full text of every slide is on the course page for chapter 7.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.6, "fs": 10.5, "items": list(C.CQS)}],
        notes("Script", look="The seven questions are the chapter's own competency questions, and each one is answered by a part of this deck and in full on the course page",
              think="which of the seven you could already answer from chapters 5 and 6"),
        take=None)

_BR = ("ScriptLanguage", "KeyLocking", "ScriptedMultisig", "PayToScriptHash", "DataAndTime", "FlowControl", "SegwitScripts", "TreesAndTweaks", "TaprootBranch")
content("One chapter, nine branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 5, "fs": 11.5, "subfs": 10, "accent": [8],
          "items": [{"label": LABEL[r], "sub": "%d concepts" % len([n for n in C.NODES if n[2] == 3 and (n[3] == r or n[3] in children(r))])} for r in _BR]}],
        notes("Script", "PayToPublicKeyHash", look="The count under each branch is how many concepts the course page explains for it; the deck follows the spine of the nine, from the stack machine to taproot",
              think="why a language with no loops still needs nine branches to describe"),
        lede="Nine branches, one per family of spending conditions; the deck walks them in the order Bitcoin gained them.",
        take="Nine branches - every slide today lives on this map")

# ---- Part 1: scripts and the stack -------------------------------------------------------------
section("Scripts and the stack", "The language, its two scripts and a bug of 2010",
        [{"label": "A stack machine"}, {"label": "Lock and unlock"}, {"label": "A key hash"}, {"label": "OP_RETURN, 2010"}],
        notes("Script", "StackExecution", look="The figure is the book's picture of a simple stack calculation, the same two numbers added and compared that the next slide runs",
              think="what a language without loops can still express"),
        image=img("mbc3_0702.png", 6.75, 1.85, 2.0, 2.67, cap="a simple stack calculation - " + BOOKCAP))

content("A script is a short program for a stack", "Push data, or pop inputs and push a result; the top of the stack is the verdict",
        [{"t": "flow", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.85, "fs": 11.5, "steps": [
            {"label": "Unlocking script", "sub": "pushes the proof, usually a signature and a key"},
            {"label": "Locking script", "sub": "runs on the same stack and checks the proof"},
            {"label": "Top of the stack", "sub": "non-zero: the spend is valid", "hot": True}]},
         dict(code("StackExecution", 0.5, 2.7, 4.4, 1.5, fs=9), label="2 3 ADD 5 EQUAL, run; then its bytes"),
         dict(code("PayToPublicKeyHash", 5.1, 2.7, 4.4, 1.5, fs=9), label="a real key-hash spend, then two broken ones"),
         {"t": "chips", "x": 0.5, "y": 4.55, "w": 9.0, "h": 0.4, "fs": 11, "items": ["no loops", "no state", "a Python port of Core's engine"]}],
        notes("StackExecution", "PayToPublicKeyHash", look="The left console runs the arithmetic script of the book's figure and shows its five bytes; the right console builds a real pay to public key hash output, signs a spend, and then breaks it twice, by signing with another key and by changing the amount after signing",
              think="why changing the amount after signing makes the signature check fail"),
        take="A spend is a proof run against a condition, and the verdict is one value")

story_slide("OpReturnBug", "photo_satoshi_bust_budapest.jpg", (0.5, 1.45, 2.3, 3.0),
            ["28 July 2010: two bugs are found and shown on the test network",
             "Version 0.3.0 joined the two scripts, and OP_RETURN jumped to the end",
             "So 1 OP_RETURN ended the run true; fixed in 0.3.5"],
            "OpReturnBug", G["OpReturnBug"],
            "2010 model accepts 1 OP_RETURN; today's engine refuses; the owner still spends",
            "The first console line is a model of the 2010 design in which the input script 1 OP_RETURN ends the joined script with a true value; the second line gives the verdict of today's engine, which fails the script at OP_RETURN; the third line shows that the genuine owner, who pushes the secret, is still accepted",
            (3.1, 3.15, 6.4, 1.2), (3.1, 1.45, 6.4, 1.5))

# ---- Part 2: signatures, multisig, script hash ---------------------------------------------------
section("Signatures, multisig and script hash", "Signatures, t of k keys and script hashes",
        [{"label": "DER and the hash type"}, {"label": "Strict DER, 2015"}, {"label": "2-of-3 multisig"}, {"label": "Pay to script hash"}],
        notes("SignatureEncoding", "ScriptedMultisignature", look="The figure is the book's picture of validating a pay to public key hash script step by step, the pattern that every lock of this part repeats",
              think="which step of the figure fails first when the key does not match the hash"),
        image=img("mbc3_0703.png", 6.5, 1.85, 2.9, 2.42, cap="validating a P2PKH script - " + BOOKCAP))

content("A signature is two numbers, written in strict DER", "Strict encoding is a consensus rule since BIP66; the low form of s is only a relay policy",
        [dict(code("SignatureEncoding", 0.5, 2.0, 9.0, 1.4, fs=9.5), label="a signature of 72 bytes, strictly encoded and low-s; a padded copy is refused only when DERSIG applies"),
         {"t": "beats", "x": 0.5, "y": 3.65, "w": 9.0, "h": 0.9, "fs": 12, "items": [
             "A signature is the pair r and s in DER, followed by one hash-type byte",
             "The hash type says which parts of the transaction the signature commits to"]},
         {"t": "chips", "x": 0.5, "y": 4.6, "w": 9.0, "h": 0.4, "fs": 11, "items": ["ALL", "NONE", "SINGLE", "plus ANYONECANPAY"]}],
        notes("SignatureEncoding", "SignatureHash", look="The first console signs a message with a demonstration key and checks the encoding; the second builds the same signature with an extra zero byte in r, which the engine accepts without the DERSIG flag and refuses with it, as the nodes of 2015 began to do",
              think="why two encodings of the same signature are a problem for a rule that every node must apply identically"),
        take="Two valid-looking encodings of one signature must not both be valid",
        lede="The same signature, padded with a zero byte, passes without the DERSIG rule and fails with it.")

story_slide("DerFork", "photo_bitcoin_mining_farm.jpg", (0.5, 1.45, 3.0, 1.69),
            ["BIP66 made strict DER the only valid signature encoding, from block 363,725 on 4 July 2015",
             "About half of the hash rate mined without fully validating and built on an invalid block",
             "A fork of 6 blocks lasted from 02:10 to 03:50 UTC; a second, of 3 blocks, followed on 5 July"],
            "SignatureEncoding", G["SignatureEncoding"],
            "the same padded signature: accepted before the rule, SIG_DER under it",
            "The console takes a signature that is valid except for a padded integer and shows that the engine accepts it only when the strict-DER flag is not set, which is exactly the difference between a node that enforced BIP66 and one that did not",
            (3.75, 3.35, 5.75, 0.95), (3.75, 1.45, 5.75, 1.7))

content("Multisignature: t of k keys, in order", "A 105-byte script for 2 of 3; the signatures must follow the order of the keys",
        [dict(code("ScriptedMultisignature", 0.5, 1.85, 9.0, 1.6, fs=9.5), label="2 of 3 with real signatures: the right order, the wrong order, one signature short, and the extra element"),
         {"t": "chips", "x": 0.5, "y": 3.75, "w": 9.0, "h": 0.4, "fs": 11.5, "items": ["bare: 3 keys by policy", "script hash: 15 keys", "consensus: 20 keys"]},
         {"t": "beats", "x": 0.5, "y": 4.25, "w": 9.0, "h": 0.7, "fs": 11.5, "items": [
             "The opcode pops one extra stack element, which must be empty since BIP147"]}],
        notes("ScriptedMultisignature", "MultisigLimits", look="The first line measures the script, 105 bytes with three compressed keys; the second shows that the signatures of keys 0 and 2 pass while the same signatures in the opposite order fail and one signature alone runs out of stack; the third shows that a non-empty dummy element is refused under the NULLDUMMY rule",
              think="why the opcode needs the signatures in the same order as the keys"),
        take="Signatures follow the order of the keys, and the odd extra element must be empty")

content("Pay to script hash: the payer sees only a hash", "A 23-byte output, a 3-address, and a redeem script that the spender reveals",
        [{"t": "flow", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.85, "fs": 11.5, "steps": [
            {"label": "Payer", "sub": "pays to a 23-byte hash: any script looks alike"},
            {"label": "Spender", "sub": "reveals the redeem script as the last item"},
            {"label": "Node", "sub": "hashes it, compares, then runs it", "hot": True}]},
         dict(code("RedeemScript", 0.5, 2.85, 9.0, 1.45, fs=9.5), label="the 2-of-3 script as an output: its address, a real spend, and a spend whose script hashes to something else"),
         {"t": "chips", "x": 0.5, "y": 4.55, "w": 9.0, "h": 0.4, "fs": 11, "items": ["payer: short output", "spender: the script and fee"]}],
        notes("RedeemScript", "PayToScriptHashOutput", look="The console hashes the 105-byte script into a 23-byte output and a 34-character address starting with 3, spends it with two real signatures, and then shows that presenting a script that hashes to a different value fails",
              think="who pays for the storage of a long script under pay to script hash, and why that is fairer"),
        take="Pay to script hash moves the size and the fee of the script to its spender")

# ---- Part 3: time and flow control -----------------------------------------------------------------
section("Time and flow control", "Making a spend wait, and letting one output have several ways out",
        [{"label": "Absolute lock"}, {"label": "Relative lock"}, {"label": "IF and VERIFY"}, {"label": "Three paths"}],
        notes("CheckLockTimeVerify", "CheckSequenceVerify", look="The boxes name the four slides of this part: the two kinds of timelock, the conditional opcodes, and the book's company contract that uses them all",
              think="the difference between a time that is fixed on the calendar and one that starts when the output is confirmed"))

content("Two timelocks, both enforced by the script", "Absolute: the lock time field. Relative: the age in the sequence field",
        [dict(code("CheckLockTimeVerify", 0.5, 1.8, 9.0, 1.4, fs=9.5), label="wait until height 800,000: the lock time must be at least that, and the input must not be final"),
         dict(code("CheckSequenceVerify", 0.5, 3.55, 9.0, 1.3, fs=9.5), label="wait 4,320 blocks (30 days): version 2, the same kind, an age at least as large")],
        notes("CheckLockTimeVerify", "CheckSequenceVerify", look="The first console spends real outputs and shows when the absolute lock holds: a lock time of 800,000 passes, 799,999 fails, and a final input fails; its last line shows that a lock time of 800,000 is first final in a block of height 800,001, which differs by one block from the book's wording; the second console shows the relative lock failing for an age of 4,319 blocks, for version 1, and for a sequence with the disable flag",
              think="why OP_CHECKLOCKTIMEVERIFY fails when the input's sequence is final"),
        take="Scripts check the transaction's own fields, so consensus enforces the wait")

content("One output, three ways out", "Partners at any time, the lawyer with one after 30 days, alone after 90",
        [{"t": "flow", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.85, "fs": 11, "steps": [
            {"label": "Path 1", "sub": "two of three partners, any time"},
            {"label": "Path 2", "sub": "the lawyer and one partner, after 30 days"},
            {"label": "Path 3", "sub": "the lawyer alone, after 90 days", "hot": True}]},
         dict(code("MohammedScript", 0.5, 2.75, 9.0, 1.5, fs=9.5), label="the 192-byte script spent through each path with real signatures; too young an age fails"),
         {"t": "chips", "x": 0.5, "y": 4.55, "w": 9.0, "h": 0.4, "fs": 11, "items": ["30 days = 4,320 blocks", "90 days = 12,960 blocks"]}],
        notes("MohammedScript", "MultiPathScript", look="The console measures the script, 192 bytes, and spends it through the three paths with real signatures; path 2 passes at an age of 4,320 blocks and fails at 4,319, and path 3 passes at 12,960 blocks and fails at 4,320",
              think="why the lawyer needs a partner for the first 90 days but not afterwards"),
        take="One output, several redemption paths, each with its own terms")

# ---- Part 4: segregated witness and script trees -----------------------------------------------------
section("Witness programs and script trees", "Where the proof moved to, what a real block spends, and how alternatives hide in a hash",
        [{"label": "Witness programs"}, {"label": "Segwit addresses"}, {"label": "A real block"}, {"label": "Merkle tree of scripts"}],
        notes("WitnessProgram", "Mast", look="The four boxes are the two slides of this part and the two ideas they carry, the version byte of a witness program and the tree of alternative scripts",
              think="how a version byte lets later upgrades reuse the same output format"))

content("Witness programs, and what 1,022 real inputs spend", "The first 599 transactions of block 775,072, classified by the chapter's own library",
        [{"t": "chart", "x": 0.45, "y": 1.95, "w": 4.6, "h": 3.0, "ctype": "bar",
          "title": "Inputs of block 775,072 by the script they spend",
          "dataLabels": True, "dlFmt": "0", "dlFs": 9,
          "labels": [n for n, _ in _cen], "series": [{"name": "inputs", "data": [v for _, v in _cen]}]},
         dict(code("P2wpkh", 5.2, 2.0, 4.3, 1.6, fs=8.5), label="native and nested spends; a wrong amount fails"),
         {"t": "numlist", "x": 5.2, "y": 3.75, "w": 4.3, "h": 1.2, "fs": 10, "items": [
             "A witness program is a version byte and a push of 2 to 40 bytes",
             "Version 0 is P2WPKH and P2WSH, version 1 is taproot"]}],
        notes("WitnessProgram", "P2wpkh", look="The bars are the second line of the block census: 626 of the 1,022 inputs spend a native P2WPKH output and 194 a legacy key hash output, and six spend taproot; the console on the right signs a native and a nested P2WPKH spend, and shows that a signature made over a different amount is refused because the version 0 signature hash commits to the amount",
              think="why a signature that commits to the amount lets a hardware wallet know the fee"),
        lede="The bars come from executed code over a saved block; the checker re-runs the console off this file.",
        take="Most inputs spend witness programs, and the signature commits to the amount")

content("A tree of scripts hides every script you do not use", "A Merkle tree commits to all scripts; the spender shows one and its proof",
        [img("mbc3_0705.png", 0.45, 1.75, 4.4, 1.6, cap="a MAST with three sub-scripts - " + BOOKCAP),
         dict(code("Mast", 0.45, 4.1, 4.4, 0.85, fs=8), label="the contract as a tree: proofs, then larger trees"),
         {"t": "chart", "x": 5.0, "y": 1.75, "w": 4.55, "h": 3.2, "ctype": "bar",
          "title": "Sibling hashes needed to prove one script",
          "dataLabels": True, "dlFmt": "0", "dlFs": 9,
          "labels": ["%s scripts" % format(n, ",") for n, _ in _mast], "series": [{"name": "hashes", "data": [d for _, d in _mast]}]}],
        notes("Mast", "MastVersusAst", look="The picture is the book's Merklized alternative script tree with three scripts; the first console line builds that tree for the three-path contract and finds proofs of two, two and one hashes; the bars show the length of a proof for 3, 8, 1,024 and 1,048,576 scripts, one hash per level of depth",
              think="why a million alternative scripts cost only twenty hashes to prove one of them"),
        lede="Only the depth of the tree matters: 20 hashes of 32 bytes prove one script out of a million.",
        take="The cost grows with the depth of the tree, not with the number of scripts")

# ---- Part 5: taproot and tapscript ---------------------------------------------------------------------
section("Taproot and tapscript", "One key for agreement, one script for the rest",
        [{"label": "Output key"}, {"label": "Key path"}, {"label": "Script path"}, {"label": "Tapscript"}],
        notes("Taproot", "KeyPathSpending", look="The figure is the book's picture of a taproot output in which the public key commits to the Merkle root of a script tree",
              think="what an observer of the chain can learn from a spend by the key path"),
        image=img("mbc3_0710.png", 6.55, 1.85, 2.9, 2.56, cap="a taproot output - " + BOOKCAP))

content("Taproot: one 32-byte key that commits to a tree", "Output key = internal key + tweak; the key path shows one 64-byte signature",
        [{"t": "flow", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.85, "fs": 11.5, "steps": [
            {"label": "Internal key P", "sub": "possibly the sum of many keys"},
            {"label": "Tweak by the tree root", "sub": "Q = P + hash(P, root) x G"},
            {"label": "Output key Q", "sub": "32 bytes, in a bc1p address", "hot": True}]},
         dict(code("Taproot", 0.5, 2.7, 9.0, 1.65, fs=9.5), label="output key and address; a 64-byte key path spend of 308 units; an untweaked key fails"),
         {"t": "chips", "x": 0.5, "y": 4.6, "w": 9.0, "h": 0.4, "fs": 11, "items": ["key path: one signature", "witness version 1", "BIP340, BIP341"]}],
        notes("Taproot", "KeyPathSpending", look="The console derives the output key of an output without scripts and its address, then spends a second output that does commit to a tree by the key path with one 64-byte signature that weighs 308 units; signing with the untweaked key instead fails the Schnorr check",
              think="why the signer must use the key tweaked by the tree's root"),
        take="When everyone agrees, the chain shows one signature and no script")

content("The script path: reveal one script, hide the rest", "Witness = inputs, script, and a control block linking it to the output key",
        [{"t": "chart", "x": 0.45, "y": 1.72, "w": 4.6, "h": 3.2, "ctype": "bar",
          "title": "Weight of the three paths of one contract (weight units)",
          "dataLabels": True, "dlFmt": "0", "dlFs": 8,
          "labels": ["2 of 3 partners", "lawyer and partner", "lawyer alone"],
          "series": [{"name": "tapscript leaf", "data": _tw}, {"name": "P2WSH script", "data": _ww}]},
         dict(code("ScriptPathSpending", 5.2, 2.0, 4.3, 1.85, fs=8.5), label="per-leaf results, weights and control blocks"),
         {"t": "beats", "x": 5.2, "y": 4.2, "w": 4.3, "h": 0.75, "fs": 10.5, "items": ["The key path of the same output weighs 308 units", "A control block is 33 + 32 x depth bytes"]}],
        notes("ScriptPathSpending", "ControlBlock", look="The bars compare the same three-path contract as three tapscript leaves and as one P2WSH script; the leaf of the second path weighs 617 units against 584, so the script path costs about the same as the old way, but the key path of the same output would weigh only 308; the last line shows control blocks of 97, 97 and 65 bytes for a tree of three leaves",
              think="why a contract that is almost always settled by agreement is cheaper in taproot"),
        lede="Revealing a script costs about what P2WSH costs; the cooperative key path costs half.",
        take="A script path spend shows one script and nothing about the others")

story_slide("SchnorrToTaproot", "photo_claus_schnorr_1986.jpg", (0.5, 1.45, 2.4, 2.2),
            ["Claus Schnorr patented his signature scheme and kept it out of open standards for almost two decades",
             "BIP340, BIP341 and BIP342 specified Schnorr signatures, taproot and tapscript",
             "The rules took effect at block 709,632 on 14 November 2021"],
            "Taproot", G["Taproot"][2:4],
            "a taproot key path spend: one 64-byte Schnorr signature, 308 weight units",
            "The console builds a taproot output, spends it by the key path and shows that the witness is a single 64-byte Schnorr signature, whatever number of people produced the key",
            (3.2, 3.35, 6.3, 0.85), (3.2, 1.45, 6.3, 1.65), title="From a patented signature to taproot")

content("Tapscript: three small changes to the language", "OP_CHECKSIGADD counts signatures; unknown opcodes succeed for upgrades",
        [dict(code("ChecksigAdd", 0.5, 1.85, 9.0, 1.45, fs=9.5), label="2 of 3 with OP_CHECKSIGADD: 104 bytes, spent with one empty signature; with only one signature it fails"),
         dict(code("OpSuccess", 0.5, 3.55, 9.0, 1.4, fs=9.5), label="87 opcode values are OP_SUCCESS; a script that contains OP_LSHIFT succeeds, and the legacy engine refuses it")],
        notes("ChecksigAdd", "OpSuccess", look="The first console measures the tapscript form of 2 of 3 at 104 bytes against 105 in legacy script and spends it in a real taproot transaction with one empty signature, which counts nothing, and fails when only one signature counts; the second console counts the 87 OP_SUCCESS values and shows that a leaf holding the disabled opcode OP_LSHIFT, number 152, is accepted, while the legacy engine rejects the same opcode as disabled",
              think="why making unknown opcodes succeed lets a later soft fork give them a meaning"),
        take="Tapscript counts signatures one at a time and leaves room for upgrades")

# ---- summary, resources, closing ------------------------------------------------------------------------
content("The chapter in five lines", "One line per part - each one provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A script is a stack program with no loops and no state: the unlocking script proves, the locking script checks, and the top value is the verdict",
            "A signature is two numbers in strict DER; multisignatures count them in key order, and pay to script hash moves a long script to its spender",
            "Lock time and sequence let a spend wait, and conditionals give one output several ways out",
            "Segregated witness moved the proof into a witness program with a version, and a tree of scripts hides every alternative that is not used",
            "Taproot commits a key to a tree: the key path shows one signature, the script path one script, and tapscript counts signatures one by one"]}],
        "These five lines are the deck in miniature, one per part, and each of them is carried by a slide range that the agenda "
        "names. A line that feels unproven should send the reader back to its consoles, because every figure in it was computed "
        "on a slide with the chapter's own interpreter. The full text behind all five lines is on the course page for chapter 7.",
        take="If a line feels unproven, its part's slides carry the receipt")

content("Where to go from here", "Checked 2026-10-08; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["The whitepaper, nine pages", "https://bitcoin.org/bitcoin.pdf"],
                ["The Bitcoin Wiki's Script page", "https://en.bitcoin.it/wiki/Script"]]},
            {"head": "Standards", "rows": [
                ["BIP 66 - strict DER signatures", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0066.mediawiki"],
                ["BIP 141 - segregated witness", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0141.mediawiki"],
                ["BIP 341 - taproot", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0341.mediawiki"],
                ["BIP 342 - tapscript", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0342.mediawiki"]]},
            {"head": "The stories", "rows": [
                ["Bitcoin 0.3.0, the first script engine", "https://raw.githubusercontent.com/bitcoin/bitcoin/v0.3.0/script.cpp"],
                ["The early bugs, CVE-2010-5141", "https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures"],
                ["The July 2015 network alert", "https://bitcoin.org/en/alert/2015-07-04-spv-mining"]]},
            {"head": "Tools", "rows": [
                ["Bitcoin Optech - taproot", "https://bitcoinops.org/en/topics/taproot/"],
                ["The Bitcoin Wiki on taproot", "https://en.bitcoin.it/wiki/Taproot"]]}]}],
        "Everything here is free to read, and every link was fetched on the date in the subtitle. A good exercise is to read the "
        "source of the first script engine next to today's rules and find the line where OP_RETURN changed meaning, then run the "
        "same script in the chapter's library on the course page. The course page for chapter 7 carries the full resource list, "
        "including the chapter itself and Bitcoin Core's interpreter, with a sentence on why each entry is there.",
        take="Read the first engine beside today's rules and find where OP_RETURN changed")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
          "How a locking and an unlocking script decide a spend",
          "How a signature, a multisignature and a script hash are checked",
          "How timelocks and conditionals shape who can spend, and when",
          "What segwit and taproot change, and what a key path or script path reveals"]}],
      "Four claims, each carried by computations that ran on slides of this deck with the chapter's own interpreter, which is "
      "checked against Bitcoin Core's published script tests and against every input of a real block. The course page for chapter 7 "
      "carries every word behind them, the stories with their sources, and the question bank to test the four claims on yourself.", bg="dark")

# ---- agenda -----------------------------------------------------------------------------------------------
S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "The questions, then five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and at the end, a taproot spend you have read yourself",
             "bg": "light"})
_sec = [i for i, s in enumerate(S) if s["kind"] == "section"]
_rows = [("Questions and the chapter map", 3, _sec[0]),
         ("Scripts and the stack - the OP_RETURN bug of 2010", _sec[0] + 1, _sec[1]),
         ("Signatures, multisig and script hash - the 2015 DER fork", _sec[1] + 1, _sec[2]),
         ("Time and flow control - timelocks and the three paths", _sec[2] + 1, _sec[3]),
         ("Witness programs and script trees", _sec[3] + 1, _sec[4]),
         ("Taproot and tapscript - the 2021 soft fork, summary and resources", _sec[4] + 1, len(S))]
for _ti, _x, _y in _rows:
    if not 2 < _x <= _y <= len(S):
        raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (_ti, _x, _y))
S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.0,
                  "items": ["%s  (slides %d-%d)" % r for r in _rows]},
                 {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                     {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                     {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                     {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") == "code")),
                      "label": "live-run consoles, each shown with its result"}]}]
S[1]["notes"] = ("The route has five parts and ends with a taproot spend the reader has examined alone. One story is the bug of 2010 "
                 "in which an input script of one number and OP_RETURN could spend any output, one is the fork of July 2015 that "
                 "followed a rule about the encoding of signatures, and one is the path of a signature scheme from a patent to the "
                 "soft fork of November 2021. The part a reader expects to be hardest is worth marking now and checking at the "
                 "summary slide.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for line in str(s["notes"]).splitlines():
        if re.match(r"^\s*(?:[A-Z][A-Z \-/&()0-9]{1,24}|say|ask|tell|show|story|cue|demo|note|full text|read|point|click|pause|transition|timing)\s*(?:\([^)]*\))?\s*:", line):
            raise SystemExit("REFUSED: slide %r carries a directive label in its notes: %r" % (s["title"], line[:60]))
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
_story_titles = {STORY[k]["title"] for k in STORY} | {"From a patented signature to taproot"}
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl and sl["title"] not in _story_titles and sl["title"] != "The questions this chapter answers"]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))

plan = {"meta": {"title": "Chapter 7: Authorization and Authentication", "sub": "SEN0401, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-08, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0), notes as reader's prose"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
