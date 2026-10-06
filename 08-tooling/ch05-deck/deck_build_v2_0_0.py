#!/usr/bin/env python3
"""Builds deck_plan_v2_0_0.json - chapter 5 (Wallet Recovery) redesigned for the classroom.

Chapter 5 completes the first five chapters on the chapter-1 v2.8.0 standard (CME materials
look-and-feel v1.0.0), drawn by the SHARED renderer 08-tooling/deck_render_v1_0_0.js. Every
'>>>' row comes from examples_out_v1_0_0.json and is re-run off the finished file by
deck_check_v1_0_0.py. The BIP-39 pipeline is executed against the standard's own vectors, the
BIP-84 address is matched against Bitcoin Core's, and the words-to-entropy chart is a native
chart object with data labels drawn ONLY from the executed CodeLength example.

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


C = load("corpus5", os.path.join(HERE, "..", "sen0401_ch05_corpus_v1_1_0.py"))
ST = load("stories5", os.path.join(HERE, "..", "sen0401_ch05_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
ASSETS = "../../03-materials/ch05/assets/"
for _f in ("photo_stefan_thomas.jpg", "photo_trezor_pair.jpg", "mbc3_0502.png", "mbc3_0503.png", "mbc3_0504.png"):
    if not os.path.exists(os.path.join(HERE, ASSETS, _f)):
        raise SystemExit("REFUSED: missing asset %s" % _f)
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: v for k, v in EX.items() if not k.startswith("_")}

BYNAME = {n[0]: n for n in C.NODES}
CORPUS_TEXT = " ".join(t for n in C.NODES for _, t in n[5])
OUTTEXT = " ".join(out for rows in G.values() for _, out in rows)
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
    out += "\nFULL TEXT: course page, chapter 5 - " + ", ".join(names) + "."
    return out


def decamel(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", n).replace("Bip", "BIP").replace("Hd", "HD").replace("Xpub", "xpub").replace("Hmac", "HMAC").replace("Sha", "SHA").replace("Pbkdf", "PBKDF")


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
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fx%.1fin" % (group, w, h))
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


# verified figures parsed back out of the executed examples
import ast as _ast
_cl = _ast.literal_eval(G["CodeLength"][-1][1])
assert _cl == [(128, 4, 12), (160, 5, 15), (192, 6, 18), (224, 7, 21), (256, 8, 24)]
assert _ast.literal_eval(G["Seed"][-1][1]) == 512
assert G["StandardPath84"][-1][1] == "True", "the BIP-84 address no longer matches Core's"
assert _ast.literal_eval(G["GapLimit"][0][1]) == [0, 3]
assert _ast.literal_eval(G["Bip44Structure"][1][1]) == 5

S = []

TAKES = {
    'The questions this chapter answers': 'If you can answer these, chapter 5 is yours',
    'One chapter, eight branches': 'Eight branches - every slide today lives on this map',
    'Two guesses from 7,002 bitcoin': 'Memory is not a backup - this chapter is the alternative',
    'From loose keys to one seed': 'Back up one secret once, instead of every key forever',
    'Twelve words between you and 128 bits': 'The recovery code is an interface between humans and entropy',
    'Words to bits, measured': 'Eleven bits a word; the checksum rides along',
    'From words to seed, slowly on purpose': 'The passphrase changes everything - by design',
    'The paths everyone agreed on': "m/84h/0h/0h/0/0 - and Core derives the same address",
    'Split the secret, not the risk': 'Three of five recovers; two of five learns nothing',
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
slide("title", "Chapter 5: Wallet Recovery", "One seed, twelve words, and every key you will ever need back",
      [img("mbc3_0503.png", 5.9, 1.2, 3.7, 2.5, cap="the HD tree - Mastering Bitcoin 3e, CC BY-SA")],
      "SAY: Chapter 4 made one key; chapter 5 makes ALL of them recoverable from twelve words "
      "you can write on paper - and shows what happens to people who skip the writing.\n"
      "FULL TEXT: course page, chapter 5.")

content("The questions this chapter answers", "Its own competency questions - we return to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.5,
          "items": [re.sub(r",.*", "?", q) if len(q.split()) > 18 else q for q in C.CQS]}],
        paras("WalletKeys"))

content("One chapter, eight branches", "The concept map the whole chapter hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 4, "fs": 12.5, "subfs": 10, "accent": [2],
          "items": [{"label": decamel(r), "sub": "%d concepts" % len([n for n in C.NODES if n[3] == r or (n[3] in children(r))])}
                    for r in ("WalletKeys", "RecoveryCodes", "Bip39Stack", "HdWallet", "PathBackup", "NonkeyBackup", "WalletDeployment", "Foundations")]}],
        paras("WalletKeys", "RecoveryCodes"),
        lede="Eight branches; the count under each is how many concepts the course page explains for it - today walks the spine.")

# ---- Keys in wallets --------------------------------------------------------------------------
section("Keys in wallets", "From a bag of keys to one recoverable seed",
        [{"label": "Wallet databases"}, {"label": "Loose keys"}, {"label": "Deterministic"}, {"label": "Hierarchical"}],
        paras("WalletKeys"),
        image=img("mbc3_0502.png", 6.3, 2.0, 3.3, 2.4, cap="one seed, many keys - Mastering Bitcoin 3e, CC BY-SA"))

content("Two guesses from 7,002 bitcoin", STORY["IronKey"]["when"],
        [img("photo_stefan_thomas.jpg", 0.5, 1.45, 2.4, 3.1, cap="Stefan Thomas - Lift 2015, CC BY 2.0"),
         {"t": "beats", "x": 3.3, "y": 1.5, "w": 6.2, "h": 2.3, "fs": 13, "items": [
             "2011: paid 7,002 BTC for an animated bitcoin explainer",
             "Keys on an encrypted drive; password on a paper, lost",
             "The drive allows ten guesses - by 2021, eight were gone",
             "Front page of the New York Times, and of this chapter"]},
         factrow("IronKey", x=3.3, y=4.05, w=6.2)],
        story_notes("IronKey"))

content("From loose keys to one seed", "Three generations of wallet, one slide",
        [{"t": "flow", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.15, "fs": 12, "steps": [
            {"label": "Loose keys", "sub": "back up every key, forever"},
            {"label": "Deterministic", "sub": "one seed makes them all"},
            {"label": "Hierarchical", "sub": "a tree with branches", "hot": True}]},
         dict(code("IndependentKeyGeneration", 0.5, 3.0, 4.3, 0.85, fs=9.5), label="loose keys: unrelated by design"),
         dict(code("DeterministicKeyGeneration", 5.1, 2.96, 4.4, 1.02, fs=8.5), label="same seed in, same keys out - always"),
         {"t": "when", "x": 2.8, "y": 4.3, "w": 4.4, "body": "back up ONE secret, ONCE"}],
        paras("IndependentKeyGeneration", "DeterministicKeyGeneration", ask="What breaks if a deterministic wallet's RNG is biased? (chapter 4 answered)"))

# ---- Recovery codes ---------------------------------------------------------------------------
section("Recovery codes", "Entropy, dressed for handwriting",
        [{"label": "BIP-39 words"}, {"label": "Checksum"}, {"label": "Passphrase"}, {"label": "The rivals"}],
        paras("RecoveryCodes"),
        image=img("mbc3_0504.png", 6.4, 1.8, 3.1, 2.9, cap="entropy to code - Mastering Bitcoin 3e, CC BY-SA"))

content("Twelve words between you and 128 bits", STORY["Bip39Birth"]["when"],
        [img("photo_trezor_pair.jpg", 0.5, 1.5, 3.3, 2.1, cap="Trezor One devices - photo: Gage Skidmore, CC BY-SA 3.0"),
         {"t": "beats", "x": 4.2, "y": 1.5, "w": 5.3, "h": 2.3, "fs": 13, "items": [
             "2013: the first hardware-wallet team hits a human problem",
             "Nobody transcribes 128 raw bits correctly",
             "BIP 39: 2,048 words, 11 bits each, checksum folded in",
             "These slides run that standard against its own vectors"]},
         factrow("Bip39Birth", x=0.5, y=4.42, w=9.0)],
        story_notes("Bip39Birth"))

content("Words to bits, measured", "The whole size table, computed - then checked word by word",
        [{"t": "chart", "x": 0.45, "y": 1.5, "w": 5.3, "h": 3.3, "ctype": "bar",
          "title": "Entropy carried by a recovery code (bits)",
          "dataLabels": True, "dlFmt": "0", "dlFs": 9,
          "labels": ["%d words" % w for _, _, w in _cl],
          "series": [{"name": "entropy bits", "data": [e for e, _, _ in _cl]}]},
         dict(code("WordList", 6.0, 1.55, 3.5, 1.5, fs=8.5), label="the list: 2,048 words, sorted"),
         dict(code("Bip39Code", 6.0, 3.4, 3.5, 1.4, fs=7.5, rows=G["Bip39Code"][1:]), label="the vector decodes and verifies")],
        paras("CodeLength", "WordList", ask="Why eleven bits a word - what is 2 to the 11?"),
        lede="The bars are computed, never quoted: CodeLength derived every pair, and the checker re-runs it off this file.")

content("From words to seed, slowly on purpose", "PBKDF2, salt, and the passphrase that changes everything",
        [{"t": "flow", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.0, "fs": 12, "steps": [
            {"label": "words", "sub": "the code you wrote"},
            {"label": "+ 'mnemonic' + passphrase", "sub": "the salt"},
            {"label": "PBKDF2, 2048 rounds", "sub": "HMAC-SHA512"},
            {"label": "512-bit seed", "sub": "the tree's root", "hot": True}]},
         dict(code("Seed", 0.5, 2.68, 4.3, 0.85, fs=9.5), label="the seed is 512 bits, counted"),
         dict(code("RecoveryPassphrase", 5.1, 2.68, 4.4, 0.85, fs=8.5), label="same words, new passphrase - different wallet"),
         dict(code("Pbkdf2", 0.5, 3.72, 9.0, 1.1, fs=9), label="the stretcher itself - and it refuses sloppy input")],
        paras("Pbkdf2", "RecoveryPassphrase", ask="Where must the passphrase NOT be stored - and why is 'nowhere' a defensible answer?"))

# ---- The tree and its paths -------------------------------------------------------------------
section("The tree and its paths", "One seed, a numbered key for every purpose",
        [{"label": "Master key"}, {"label": "Child derivation"}, {"label": "Hardened"}, {"label": "Standard paths"}],
        paras("HdWallet"))

content("One seed, a tree of keys", "HMAC-SHA512 splits every node in two",
        [{"t": "numlist", "x": 0.5, "y": 1.6, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "The seed makes a master key and a chain code",
            "Each child: HMAC of parent and an index",
            "32 bytes of key, 32 of chain code - every node"]},
         dict(code("MasterPrivateKey", 4.3, 1.6, 5.2, 1.3, fs=9), label="the master pair, derived and range-checked"),
         dict(code("ChildKeyDerivation", 4.3, 3.25, 5.2, 1.3, fs=9.5), label="child zero, with its own chain code"),
         {"t": "when", "x": 0.5, "y": 3.95, "w": 3.55, "body": "the tree never runs dry"}],
        paras("HdKeyGeneration", "ChildKeyDerivation", ask="Why carry a chain code at all - what would leak without it?"))

content("Hardened or not: one question, two columns", "Can a thief with the xpub climb down?",
        [{"t": "compare", "x": 0.5, "y": 1.55, "w": 9.0, "h": 1.95, "fs": 12,
          "left": {"head": "Normal derivation (index < 2^31)", "rows": [
              "Public keys derivable WITHOUT private keys",
              "Perfect for watch-only shops",
              "But: child private + xpub leaks the parent"]},
          "right": {"head": "Hardened (index >= 2^31, the h)", "rows": [
              "Needs the private parent - no public shortcut",
              "Standard for account levels",
              "The run proves the two differ"]}},
         dict(code("HardenedDerivation", 0.5, 3.75, 9.0, 1.2, fs=9), label="same index, hardened and not - different keys, provably")],
        paras("HardenedDerivation", "PrivateChildDerivation", ask="Read m/84h/0h/0h/0/2: which hops could a watch-only server have taken itself?"))

content("The paths everyone agreed on", "Five levels, and Core derives the same address we do",
        [dict(code("Bip44Structure", 0.5, 1.55, 9.0, 0.95, fs=9.5), label="purpose / coin / account / change / index - hardened where it matters"),
         dict(code("StandardPath84", 0.5, 2.75, 9.0, 1.3, fs=9), label="BIP-84's own test vector: our math, then Core's answer - equal"),
         {"t": "chips", "x": 0.5, "y": 4.3, "w": 9.0, "h": 0.55, "fs": 12,
          "items": ["44h legacy", "49h nested", "84h segwit", "86h taproot"]}],
        paras("Bip44Structure", "StandardPath84", ask="Your phone wallet says 'account 0' - write its path from memory."))

# ---- Beyond keys ------------------------------------------------------------------------------
section("Beyond keys", "What else must survive, and how wallets ship",
        [{"label": "Watch-only xpubs"}, {"label": "Labels and channels"}, {"label": "Split secrets"}, {"label": "Test the backup"}],
        paras("NonkeyBackup"))

content("Watch-only: the shop holds no keys", "An xpub derives addresses; it cannot spend",
        [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 0.9, "fs": 9.5, "items": [
            "Deploy the xpub to the web shop, keep keys cold - it mints a fresh address per customer",
            "The gap limit decides how far a recovery scan looks for used addresses"]},
         dict(code("XpubDeployment", 0.5, 2.55, 9.0, 1.3, fs=8.5), label="three addresses from the public key alone - cold keys, warm addresses"),
         dict(code("GapLimit", 0.5, 4.1, 9.0, 0.82, fs=9.5), label="scan 20: index 25 is missed; scan 30 finds it")],
        paras("XpubDeployment", "GapLimit", ask="A donation page went viral and used 400 addresses - what must recovery change?"))

content("The 200,000 BTC in a forgotten wallet file", STORY["GoxColdFind"]["when"],
        [{"t": "stat", "x": 0.5, "y": 1.6, "w": 9.0, "h": 1.2, "items": [
            {"n": assert_fact("200,000 BTC", "goxfind"), "label": "reported found, three weeks into bankruptcy"},
            {"n": "2011", "label": "when the old-format wallet file was last used"},
            {"n": "10+ yrs", "label": "later, those coins began repaying creditors"}]},
         {"t": "beats", "x": 0.5, "y": 3.0, "w": 9.0, "h": 1.25, "fs": 12.5, "items": [
             "A file written by software two generations older still held spendable keys",
             "Backups do not expire - label them, test them, never discard them blindly"]},
         factrow("GoxColdFind")],
        story_notes("GoxColdFind"))

content("Split the secret, not the risk", "Shamir: three of five recovers; two learn nothing",
        [{"t": "numlist", "x": 0.5, "y": 1.55, "w": 3.55, "h": 1.9, "fs": 10.5, "items": [
            "Split the seed into five shares, threshold three",
            "Any three reconstruct it exactly",
            "Any two: provably nothing - the run shows both"]},
         dict(code("SecretSharing", 4.3, 1.55, 5.2, 1.75, fs=8.5), label="split, recover, and fail honestly"),
         dict(code("Slip39Code", 0.5, 3.65, 9.0, 1.25, fs=9), label="SLIP-39 does this in words; Codex32 by hand on paper")],
        paras("SecretSharing", "Slip39Code", ask="Where do five shares live so no burglary, flood, or sibling feud collects three?"))

content("Test the backup, not your luck", "The chapter's closing discipline, executable",
        [dict(code("BackupTesting", 0.5, 1.55, 9.0, 1.25, fs=9.5), label="restore-drill: right words verify; one wrong word is caught"),
         dict(code("DataLoss", 0.5, 3.1, 9.0, 0.9, fs=9.5), label="Core's own tooling: backupwallet, and the keypool that guards gaps"),
         {"t": "chips", "x": 0.5, "y": 4.25, "w": 9.0, "h": 0.6, "fs": 12.5,
          "items": ["write it", "split it if large", "store it apart", "TEST the restore"]}],
        paras("BackupTesting", "DataLoss", ask="When did you last restore a backup of anything - and how do you know it works?"))

content("Where to go from here", "Checked 2026-10-06; every entry is a live link in this file",
        [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
            {"head": "Read", "rows": [
                ["This chapter, free (CC BY-SA)", "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch05_wallets.adoc"],
                ["The IronKey story, as reported", "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html"]]},
            {"head": "Standards", "rows": [
                ["BIP 39 - the recovery code", "https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki"],
                ["BIP 32 - the HD tree", "https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki"],
                ["BIP 84 - the path these slides derived", "https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki"]]},
            {"head": "Tools", "rows": [
                ["Ian Coleman's BIP-39 tool (offline use!)", "https://iancoleman.io/bip39/"],
                ["learnmeabitcoin - HD wallets, drawn", "https://learnmeabitcoin.com"]]},
            {"head": "Community", "rows": [
                ["Bitcoin Stack Exchange Q&A", "https://bitcoin.stackexchange.com"]]}]}],
        "SAY: Everything here is free. Homework: generate a THROWAWAY twelve-word code, restore "
        "it in a second wallet, and bring the one surprise you hit to class. Never type a real "
        "code into any website.\n"
        "ASK: Which of the four closing chips does your current phone wallet fail?\n"
        "FULL TEXT: course page, chapter 5 - WalletDeployment.",
        take="Twelve words on paper beat every password you have ever memorized")

slide("closing", "What you should now be able to say", "And where each claim gets its proof",
      [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": bullets_ok("closing", [
          "Why one seed replaced bags of keys",
          "What twelve words carry, and how they become a tree",
          "Which path your wallet walks, and who else can walk it",
          "What a tested backup is - and what Stefan Thomas teaches"])}],
      "SAY: Four claims, each carried by a computation you watched run against the standards' "
      "own vectors. First five chapters complete - the course page carries every word.\n"
      "FULL TEXT: course page, chapter 5.", bg="dark")

# ---- agenda and summary -----------------------------------------------------------------------
S.insert(next(i for i, s in enumerate(S) if s["title"] == "Where to go from here"),
         {"kind": "content", "title": "The chapter in five lines",
          "sub": "One line per part - each one provable from its slides",
          "items": [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
              "Wallets stopped storing keys and started deriving them - one seed, backed up once",
              "A recovery code is entropy in human clothing: 11 bits a word, checksum included",
              "Words become a 512-bit seed through deliberate slowness - and a passphrase forks the wallet",
              "The HD tree hands every purpose a numbered key; hardened hops keep the xpub harmless",
              "Beyond keys: labels, channels, split secrets - and a backup only counts once restored"]}],
          "notes": "SAY: Five lines, one per part; the agenda names the slides that prove each.\n"
                   "ASK: Which line would you defend first, and with which slide?\n"
                   "FULL TEXT: course page, chapter 5 - every section.",
          "take": "If a line feels unproven, its part's slides carry the receipt", "bg": "light"})

S.insert(1, {"kind": "content", "title": "Today's route",
             "sub": "Five parts; every number is a slide you can jump to",
             "items": [], "notes": "", "take": "Five parts - and at the end, a backup you have actually tested",
             "bg": "light"})
_sec = {s["title"]: i for i, s in enumerate(S) if s["kind"] == "section"}
_a, _b, _c, _d = (_sec[t] for t in ("Keys in wallets", "Recovery codes", "The tree and its paths", "Beyond keys"))
_rows = [("Questions and the chapter map", 3, _a),
         ("Keys in wallets - loose, deterministic, hierarchical", _a + 1, _b),
         ("Recovery codes - BIP-39, measured and stretched", _b + 1, _c),
         ("The tree and its paths - to Core's own address", _c + 1, _d),
         ("Beyond keys, summary, and resources", _d + 1, len(S))]
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
S[1]["notes"] = ("SAY: Five parts, ending at a tested backup. One story costs 7,002 BTC, one finds "
                 "200,000, and one explains the twelve words in your pocket.\n"
                 "ASK: Which part do you expect to be hardest - mark it now, check at the summary.\n"
                 "FULL TEXT: course page, chapter 5 - every section.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for sl in S:
    if sl["kind"] == "content" and sl["title"] in TAKES and TAKES[sl["title"]]:
        sl["take"] = TAKES[sl["title"]]
EXTRA_TAKES = {
    'One seed, a tree of keys': 'Two 32-byte halves at every node keep the tree alive',
    'Hardened or not: one question, two columns': 'The h in a path is a security decision, not decoration',
    'Watch-only: the shop holds no keys': 'Publish the xpub; the keys never feel the internet',
    'The 200,000 BTC in a forgotten wallet file': 'Backups do not expire - treat old wallet files as live keys',
    'Beyond keys: what else must survive': None,
    'Test the backup, not your luck': 'A backup counts only after a successful restore drill',
}
for sl in S:
    if sl["kind"] == "content" and "take" not in sl and EXTRA_TAKES.get(sl["title"]):
        sl["take"] = EXTRA_TAKES[sl["title"]]
for sl in S:
    if sl["kind"] == "content" and sl.get("take") and len(sl["take"].split()) > 24:
        raise SystemExit("REFUSED: takeaway %r runs past the gate" % sl["take"])
missing = [sl["title"] for sl in S if sl["kind"] == "content" and "take" not in sl]
if missing:
    raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)

plan = {"meta": {"title": "Chapter 5: Wallet Recovery", "sub": "SEN0401, third-edition redesign",
                 "version": __version__, "python": PYV, "total": 0,
                 "redesign": "2026-10-06, to the chapter-1 v2.8.0 standard (CME materials look-and-feel v1.0.0)"},
        "slides": S}
out = os.path.join(HERE, "deck_plan_v2_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
