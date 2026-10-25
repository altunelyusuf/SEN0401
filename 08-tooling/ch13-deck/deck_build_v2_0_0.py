#!/usr/bin/env python3
"""deck_build v2.0.0 (chapter 13, Bitcoin Security) - the generator of the chapter 13 deck 2.0.0 (task TK_Ch13_Deck_Build_R24, 2026-10-25), a NEW file, built to the pattern of ch08-deck/deck_build_v2_0_0.py.
It writes, from the chapter research and the recorded executions, (1) deck_plan_v2_0_0.json, (2) the chapter-code manifest 03-materials/ch13/page/chapter_code_ch13_v1_0_0.json and, with --render,
(3) the .pptx (drawn by sen0401_deck_render_v2_1_0.js, repaired by sen0401_deck_ooxml_fix_v1_0_0.py, stamped by office_stamp_v1_0_0.py).

What it reads: the chapter corpus (sen0401_ch13_corpus_v1_0_2.py: parts and groups), the story module v1_3_0 (four stories with pictures), the recorded executions examples_out_v2_0_0.json (made by
examples_run_v2_0_0.py under Python 3.14 inside the unpacked wheel of the page), deck_concepts_v2_0_0.py (the 25 key concepts of the research, each with a meaning and one everyday analogy) and the
resources slide of the previous plan. Every number on a result picture is parsed from the recorded output, never typed. The deck standard (D1-D12) is held as refusals here BEFORE the file is drawn:
no text box over 30 words, notes of at most 60 words, no code line over 60 characters with its prompt (a listing never wraps), every key concept of the research on a slide with its analogy.
Usage: python3.14 deck_build_v2_0_0.py [--render]"""
__version__ = "2.0.0"
import ast, glob, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v2_0_0 as X
import deck_concepts_v2_0_0 as K
VER, VER_US = "2.0.0", "2_0_0"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


C = load(os.path.join(TOOL, "sen0401_ch13_corpus_v1_0_2.py"), "corpus13")
ST = load(os.path.join(TOOL, "sen0401_ch13_stories_v1_3_0.py"), "stories13")
OUT = json.load(open(os.path.join(HERE, "examples_out_v%s.json" % VER_US)))
PY = OUT["_python"]
LAB = {n[0]: (n[1] or n[0]) for n in C.NODES}
STORY = {s["id"]: s for s in ST.STORIES}
ASSETS = "../../03-materials/ch13/assets/"
OLD = json.load(open(os.path.join(HERE, "deck_plan_v1_2_0.json")))
RECORD = json.load(open(os.path.join(TOOL, "ch13-evidence", "regtest_run_v1_0_0.json")))

BRANCHES = [n[0] for n in C.NODES if n[2] == 1]
def kids(name): return [n[0] for n in C.NODES if n[3] == name]

S, ANALOGIES, FIRST_CODE = [], [], []
EST = lambda text, fs, width, k=0.0078: max(1, -(-int(len(text) * fs * k * 100) // int(width * 100)))   # lines a text needs: characters x font size x 0.0078 in, over the width
W = lambda t: len(re.findall(r"\S+", t))
BR_SHORT = {"SecurityModel": "Model", "ProtectingKeys": "Keys", "KeepingAccess": "Access", "SharingControl": "Sharing", "CustodyHistory": "Custody", "Survivability": "Survival"}


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
SEGS = [(BR_SHORT[b], 1.0) for b in BRANCHES]


def strip(branch, x=0.85, y=4.32, w=8.6, h=0.4):
    tot = sum(s_[1] for s_ in SEGS); hot = SEGS.index((BR_SHORT[branch], 1.0))
    return {"t": "striptable", "x": x, "y": y, "w": w, "h": h, "fs": 10, "colW": [round(w * f / tot, 3) for _, f in SEGS],
            "cells": [{"t": lab, "hot": i == hot} for i, (lab, f) in enumerate(SEGS)]}


DIV_NOTES = {
    "SecurityModel": "A node trusts only what it can check. This part shows why a signed payment can be published, how peers talk, where checking starts, and what a download proves.",
    "ProtectingKeys": "Coins are as safe as their keys. We compare a watching wallet with a signing one, see a device that makes a thief wait, and count what a guess costs.",
    "KeepingAccess": "Safe keys are no use if you lose them. We see what a backup restores, how twelve words stand for every key, and where a master key comes from.",
    "SharingControl": "One key is one point of failure. Several keys and shared secrets spread loss and theft, and we measure what that costs in bytes and in chances.",
    "CustodyHistory": "Giving your coins to someone else is trust, not safety. Two true stories show what happens when a shop or a seal replaces your own key.",
    "Survivability": "Funds should outlive their owner. A timelock lets an heir spend after a wait, and the last slide lists what these experiments did not run.",
}


def divider(branch):
    groups = kids(branch); n = len(groups); cw = (8.6 - (n - 1) * 0.2) / n; fs = 11.5 if n <= 3 else 11
    its = []
    for g in groups:
        pill, mean, ana = K.L2[g]
        if W(pill) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words" % pill)
        if EST(pill, 12 if n <= 3 else 11, cw - 0.16, 0.0092) > 1: raise SystemExit("REFUSED: divider pill %r does not fit one line of %.2f in" % (pill, cw - 0.16))
        an = "Think of %s." % ana
        its.append({"pill": pill, "meaning": mean, "analogy": an, "hM": round(EST(mean, fs, cw) * fs * 1.22 / 72 + 0.04, 3), "hA": round(EST(an, fs, cw) * fs * 1.22 / 72 + 0.04, 3)})
        ANALOGIES.append({"concept": LAB[g], "analogy": an, "slide": len(S) + 1})
    need = max(0.45 + i["hM"] + i["hA"] for i in its)
    if 2.3 + need > 4.25: raise SystemExit("REFUSED: divider %s columns need %.2f in" % (branch, need))
    items = [{"t": "groups", "x": 0.85, "y": 2.3, "w": 8.6, "fs": fs, "pfs": 12 if n <= 3 else 11, "items": its}, strip(branch)]
    ANALOGIES.append({"concept": LAB[branch], "analogy": K.L1[branch], "slide": len(S) + 1})
    return add("section", LAB[branch], K.L1[branch], items, DIV_NOTES[branch])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# concept cards: the key concepts of the research
# ------------------------------------------------------------------------------------------------------------------------------------------------
def chunks(lst):
    n = len(lst)
    if n == 0: return []
    k = -(-n // 4); size = -(-n // k); return [lst[i:i + size] for i in range(0, n, size)]


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
    notes = "These cards cover %s. Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. The full explanation is on the course page, chapter 13." % names_t
    if W(notes) > 60: notes = "These cards cover %d key concepts of the part %s. Each pairs a short meaning with something from everyday life. The full explanation is on the course page, chapter 13." % (len(names), LAB[branch])
    take = "Say each idea twice: once as the meaning, once as the everyday comparison"
    return add("content", title, "Each card: the meaning in a few words, then something you already know",
               [{"t": "concepts", "x": 0.5, "y": 1.4, "w": 9.0, "ch": round(min(avail, max(need, 1.2)), 3), "cols": cols, "fs": fs, "items": items}], notes, take)


# ------------------------------------------------------------------------------------------------------------------------------------------------
# code slides: listing, explanation beside it, and the executed result as a picture (chart or table)
# ------------------------------------------------------------------------------------------------------------------------------------------------
fmt = lambda n: "{:,}".format(n)
yn = lambda b: "yes" if b else "no"

CODE_TEXT = {  # title, sub, take, notes
    "ex01": ("A signed payment hides the key", "What the recorded bytes of a payment contain", "The payment carries a signature and a public key, never the private key",
             "A payment can be published because it contains a signature and a public key, not the private key. The recorded bytes of one signed payment show the witness items and their sizes, and no key of the owner."),
    "ex02": ("Edit the payee or the amount: rejected", "The node tested the payment as signed and two edited copies", "A signature covers payee and amount, so any edit fails the check",
             "The signature covers the amounts and the receiving scripts. A copy with another payee, or another amount, is no longer what was signed, so the node refuses it. Only the original is allowed."),
    "ex03": ("A replayed payment pays nothing", "Offering a mined payment to the same node again", "A node that knows a payment refuses it, so nothing is paid twice",
             "Sending the same signed payment again gains nothing. The node already knows it and says so, and the receiver's balance does not change. A signature is not a bearer cheque that can be cashed twice."),
    "ex04": ("Encrypted by default since release 27.0", "Two recorded nodes, and one without the service", "Peers with the service speak version two; others stay on version one",
             "Since release 27.0 nodes talk over the encrypted transport of BIP 324. Two recorded peers both report version two and the same session identifier. A node without the service falls back to the plain version one."),
    "ex05": ("The first block's hash, rebuilt", "Eighty bytes, hashed twice, found in the source", "The first block is not fetched; its hash is typed into the software",
             "The header of the first block has 80 bytes. Hashing it twice gives the hash that Bitcoin Core carries in its source. Software checks every later block against this typed-in starting point."),
    "ex06": ("Assumed valid: a typed-in shortcut", "Where Core describes it and where it keeps the block", "Old blocks are trusted by a block hash typed into the release",
             "To start faster, a node may skip checking old signatures for blocks that lead up to a block hash typed into the release. The help text describes it, the source holds the hash, and an option controls it."),
    "ex07": ("Does the download match the list?", "The recorded check of the release 31.1 tarball", "A matching hash proves the file; a checked signature proves who listed it",
             "The hash of the downloaded file equals its line in the signed list. That proves the file is the listed one. Eleven builders signed the list, but their keys were not imported, so no signature was checked."),
    "ex08": ("A watch-only wallet cannot sign", "The online half of cold storage", "A wallet without keys can build payments but never finish them",
             "The online wallet holds only public information. It sees the balance and builds a payment, but it cannot sign, and it refuses to list private descriptors. That is why a thief of this machine gets no coins."),
    "ex09": ("The payment file travels offline and back", "A partially signed payment goes to the cold node", "Only the file travels; the keys never touch the online machine",
             "The online wallet writes an unsigned payment file. The cold node, with no blocks and no connection, signs it and returns a longer file. The online node finishes it and the payment confirms."),
    "ex10": ("A PIN that makes the thief wait", "The waits of a hardware wallet double after each wrong try", "Waiting costs the thief hours long before the device wipes itself",
             "A hardware wallet answers wrong PINs with waits that double: 1, 2, 4 seconds and so on. Fifteen waits add up to hours, and after sixteen failed tries the device wipes itself, so guessing is hopeless."),
    "ex11": ("Four words fall in seconds", "How long a phrase of words lasts against a fast rig", "A few random words are not a safe secret on their own",
             "A phrase made of words from a list of 2048 has 2048 to the power of its length in possibilities. At a trillion guesses a second four words last seconds, six words about two years. Choose long, random secrets."),
    "ex12": ("A locked wallet still shows the balance", "A passphrase locks the keys, not the view", "The balance stays visible; spending needs the passphrase",
             "After encryption the wallet still shows the balance and creates addresses, because those need no private key. Sending is refused until the passphrase is entered, and a wrong passphrase is refused too."),
    "ex13": ("Stretching the passphrase buys days", "Core repeats a hash thousands of times per guess", "More rounds per guess mean more days for an attacker",
             "Bitcoin Core stretches the passphrase by repeating a hash many times, so each guess costs time. We assume a rig and a passphrase of thirty bits of strength, and count the days an attacker needs."),
    "ex14": ("A stale backup misses the newest coins", "Two restores of the same recorded wallet", "A backup restores only what it knew when it was made",
             "A wallet pre-computes a pool of addresses. A backup taken early knows few of them. Restoring from it finds fewer coins than the wallet holds, while a late backup finds them all."),
    "ex15": ("A backup range covers only the pool", "The same idea with whole numbers you can change", "Coins sent beyond the known addresses are not found",
             "Change the pool size or the payments and rerun. Only payments sent to addresses inside the backup's pool are found after a restore. The rest are on the chain but invisible to the restored wallet."),
    "ex16": ("Twelve words, 128 bits and a checksum", "The arithmetic of BIP 39", "A wrong word set passes the checksum only one time in sixteen",
             "Sixteen bytes of entropy are 128 bits. One bit in 32 is added as a checksum and everything is cut into groups of eleven bits, each choosing one of 2048 words. That gives twelve words."),
    "ex17": ("Seed words are stretched into a seed", "The first test vector of BIP 39", "The same words with another passphrase give another wallet",
             "The words are hashed many times, with the passphrase as salt, into a 64-byte seed. We compare it with the official test vector. With no passphrase the same words give a different seed, hence another wallet."),
    "ex18": ("A master key grows from the seed", "The first test vector of BIP 32", "Every key of the wallet descends from these two values",
             "A keyed hash of the seed splits into a master private key and a chain code. All the wallet's keys are derived from this pair. We compare with the published test vector of BIP 32."),
    "ex19": ("Two of three keys sign", "Recorded signing with one, two and three keys", "One key alone cannot sign; any two of the three can",
             "A two-of-three wallet needs two signatures. One key alone leaves the payment unfinished. If one key is lost the other two still sign, but with two keys lost the wallet cannot be spent."),
    "ex20": ("More keys: fewer losses, more thefts", "Chances of being stuck or robbed", "Two of three cuts both risks; one of three trades loss for theft",
             "A scheme that needs fewer keys is easier to use but easier to rob. With a loss chance of 0.1 and a theft chance of 0.05 per key, two of three is the balance; one of three is often robbed."),
    "ex21": ("A two-of-three payment is larger", "Virtual bytes of one spend", "More signatures mean more bytes, and so a higher fee",
             "A multisignature spend carries several signatures and the script that lists the keys. The recorded sizes in virtual bytes show the cost. Counting the script parts by hand gives the same number."),
    "ex22": ("Shamir by hand: shares on a line", "A line, three points, a secret at zero", "Two points fix the line; its height at zero is the secret",
             "The secret is the height of a line at zero. Each share is the line's height at another point. Two points fix the line, so two shares rebuild the secret. Try other numbers and rerun."),
    "ex23": ("Shamir with the chapter library", "Three shares, any two rebuild the secret", "One share alone gives no information about the secret",
             "The library cuts a secret into three shares with a fixed slope so that the run repeats. Any two shares rebuild the secret. A single share rebuilds some number, but not the secret."),
    "ex24": ("One share fits every secret", "A small field where every case can be listed", "A single share is consistent with every possible secret",
             "In a small field we can list every possibility. For each possible secret exactly one slope fits the single share we hold. So the share alone tells nothing about which secret is the true one."),
    "ex25": ("The Mt. Gox figures, recomputed", "Arithmetic on figures quoted in the research", "Counts differ by source; the arithmetic shows by how much",
             "Four figures from the story, recomputed. If 850,000 coins were 7 percent of all coins, the supply was about 12.1 million. A 36 percent cut turns 40 coins into 25.6. The sources disagree on the rest."),
    "ex26": ("The Casascius coin in the saved page", "Three passages searched in the saved wiki page", "Each claim of the story can be found in the saved source",
             "The story's facts are read from the saved wiki page, not from memory. The search finds the date sales stopped, the coin sizes and the regulator's view. A claim you cannot find in a source is only a claim."),
    "ex27": ("The heir must wait ten blocks", "A recorded timelock: owner at once, heir after a wait", "Before the wait, the node refuses the heir's payment",
             "The policy lets the owner spend at any time and the heir only after ten confirmations. The recorded tests show the heir refused after one and nine confirmations and accepted at ten."),
    "ex28": ("The wait field has sixteen bits", "A trap in the heir's timelock", "A wait of 65536 wraps to zero, so the heir can spend at once",
             "The relative wait is stored in sixteen bits, so it cannot exceed 65535 blocks, about 455 days. A value of 65536 is cut to zero in those bits, which lets the heir spend at once. Check your own numbers."),
}


def human_time(s):
    if s < 1e-3: return "under a millisecond"
    if s < 1: return "%d milliseconds" % round(s * 1000)
    if s < 60: return "%.1f seconds" % s
    if s < 3600: return "%.1f minutes" % (s / 60)
    if s < 86400: return "%.1f hours" % (s / 3600)
    if s < 365 * 86400: return "%.1f days" % (s / 86400)
    return "%.1f years" % (s / (365 * 86400))


def visual(ex, x, w, y, h):
    """(items, caption of the result, reading) for the executed result of one example, drawn from the recorded values; the picture stands in the right column, x to x+w"""
    def tb(rows, colW, fs=9.5):
        assert abs(sum(colW) - w) < 0.011, (ex, sum(colW), w)
        return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": [[str(c) for c in r] for r in rows], "fs": fs, "rowH": round(min(0.3, h / len(rows)), 3)}
    ch = lambda labels, data, name, labels_on=True: {"t": "chart", "ctype": "bar", "x": x, "y": y, "w": w, "h": h, "labels": [str(l) for l in labels],
                                                  "series": [{"name": name, "data": [float(d) for d in data]}], "dataLabels": labels_on, "dlFs": 9, "dlPos": "outEnd"}
    acc = lambda b: "allowed" if b else "refused"
    if ex == "ex01":
        k, wf, ln = val(ex, "(key_in, wif_in, lens)")[0], val(ex, "(key_in, wif_in, lens)")[1], val(ex, "(key_in, wif_in, lens)")[2]
        size, sh = val(ex, "size"), val(ex, "s['sighash_byte']")
        return ([tb([["Observation", "Result"], ["Bytes in the payment", fmt(size)], ["Witness item sizes", " and ".join(str(i) for i in ln)], ["Private key inside", yn(k)], ["Wallet-format key inside", yn(wf)], ["Hash type byte", sh + " (ALL)" if sh == "01" else sh]], [1.95, 1.3])],
                "what the signed bytes contain", "The witness holds a signature of %d bytes and a public key of %d bytes. No key of the owner is in the payment." % (ln[0], ln[1]))
    if ex == "ex02":
        ok = val(ex, "ok"); d1, d2 = val(ex, "t['address_replaced_differs']"), val(ex, "t['amount_changed_differs']")
        return ([tb([["Copy offered", "Mempool test"], ["As signed", acc(ok[0])], ["Payee replaced", acc(ok[1])], ["Amount changed", acc(ok[2])]], [2.0, 1.25])],
                "three copies offered to the node", "Both edited copies really differ from the original (%s), and both are refused: the signature covered what was changed." % yn(d1 and d2))
    if ex == "ex03":
        why, gain = val(ex, "(why, gain)"); bal = val(ex, "r['balance_r']")
        return ([tb([["Check", "Result"], ["Second offer to the node", "refused"], ["Reject reason", why], ["Receiver's balance before", str(bal)], ["Change after the replay", str(gain)]], [1.75, 1.5])],
                "the replay and its effect", "A node that already knows a payment will not take it again: nothing is paid twice.")
    if ex == "ex04":
        v2, v1 = val(ex, "(v2, v1)"); same = val(ex, "same"); a, b = val(ex, "'P2P_V2' in n['P_localservices']"), val(ex, "'P2P_V2' in n['X_localservices']")
        return ([tb([["Peer", "Transport"], ["Q, talking to P", v2[0]], ["P, talking to Q", v2[1]], ["Old-style node X", v1], ["Same session id", yn(same)], ["P offers the service", yn(a)], ["X offers the service", yn(b)]], [1.85, 1.4])],
                "who speaks which version", "Both ends of an encrypted link derive the same session identifier. The node without the service stays on version one.")
    if ex == "ex05":
        n_, h20, found = val(ex, "(len(hdr), h[:20], found)"); z = val(ex, "len(h) - len(h.lstrip('0'))")
        return ([tb([["Step", "Value"], ["Header bytes", str(n_)], ["Hash starts", h20], ["Leading zero digits", str(z)], ["Found in Core's source", yn(found)]], [1.55, 1.7])],
                "the double hash of the header", "The hash begins with %d zero digits and appears in the source of Core: the starting point is typed in." % z)
    if ex == "ex06":
        a, b, c = val(ex, "(says, typed, opt)")
        return ([tb([["Search", "Found"], ["Help text names the shortcut", yn(a)], ["Source types the trusted block", yn(b)], ["Option -assumevalid exists", yn(c)]], [2.4, 0.85])],
                "three searches in saved sources", "The shortcut is documented, typed into the release and switchable. Trust in it is trust in the release.")
    if ex == "ex07":
        m, made, un = val(ex, "(match, made, unchecked)"); mb, ln, gs = val(ex, "size_mb"), val(ex, "lines"), val(ex, "r['gpg_has_signature_line']")
        return ([tb([["Check", "Result"], ["Hash equals the listed one", yn(m)], ["Lines in the list", str(ln)], ["Signatures made", str(made)], ["Signatures checked", "none (%d keys missing)" % un]], [1.75, 1.5])],
                "the recorded download check", "The hash proves the file is the listed one. Without the builders' keys, nothing says who made the list.")
    if ex == "ex08":
        cs, dn = val(ex, "(can_sign, done)"); why = val(ex, "why"); bal = val(ex, "h['balance']")
        return ([tb([["Question", "Answer"], ["Holds private keys?", yn(cs)], ["Signature complete?", yn(dn)], ["Coins it watches", str(bal)]], [2.0, 1.25])],
                "the online wallet of cold storage", "Asked for private descriptors it answers: %s. It can watch and build, never sign." % why.strip())
    if ex == "ex09":
        sg, off, fin = val(ex, "(signed, off, fin)"); gr = val(ex, "grown"); got = val(ex, "b['dest_received']")
        return ([ch(["Unsigned file", "Signed file"], gr, "characters")], "characters of the payment file, before and after signing",
                "The cold node, with %d blocks and %d connections, signed it. The online node finished it: %s confirmation, %s coin received." % (off[0], off[1], fin[1], got))
    if ex == "ex10":
        tot, hrs = val(ex, "(total, hours)"); wt = val(ex, "wait"); wp = val(ex, "wipes")
        return ([ch([str(i + 1) for i in range(len(wt))], wt, "seconds", False)], "seconds waited after each wrong PIN, tries 1 to %d" % len(wt),
                "The waits add up to %s seconds, %s hours. The saved wiki page says the device wipes itself after 16 tries: %s." % (fmt(tot), hrs, yn(wp)))
    if ex == "ex11":
        ch_, secs = val(ex, "(choices, secs)"); ts = val(ex, "[2048 ** w / rate for w in range(1, 7)]")
        return ([tb([["Words from 2048", "Time to try all"]] + [[str(i + 1), human_time(t)] for i, t in enumerate(ts)], [1.35, 1.9])],
                "time to try every phrase at 10^12 guesses a second", "Four words give %s phrases and last %s seconds. Six words last %s." % (fmt(ch_), secs, human_time(ts[5])))
    if ex == "ex12":
        sh_, sp = val(ex, "(shown, spend)"); wr = val(ex, "wrong"); lf = val(ex, "left"); af = val(ex, "R['b4_after_timeout']['unlocked_until']")
        return ([tb([["Action", "Answer"], ["Balance shown", str(sh_)], ["Send while locked", "refused"], ["Send, wrong passphrase", "refused"], ["Open for (seconds)", str(lf)], ["Locked again after", yn(af == 0)]], [1.95, 1.3])],
                "the encrypted wallet", "Sending is refused with: \"%s\". The wrong passphrase gives: \"%s\"" % (sp.strip(), wr.replace("Error: ", "")[:32].strip()))
    if ex == "ex13":
        rd, dy = val(ex, "(rounds, round(days, 1))"); pg = val(ex, "per_guess")
        return ([tb([["Quantity", "Value"], ["Rounds per guess (source)", fmt(rd)], ["Seconds per guess (assumed rig)", str(pg)], ["Days for 2^30 guesses", str(dy)]], [2.1, 1.15])],
                "the cost of guessing a passphrase", "Each guess costs %s seconds on the assumed rig, so thirty bits of passphrase hold out for %s days." % (pg, dy))
    if ex == "ex14":
        fr, st_ = val(ex, "(fresh, stale)"); far = val(ex, "far"); kn = val(ex, "known")
        return ([ch(["Original wallet", "Late backup", "Early backup"], [fr[0], fr[1], st_[0]], "coins")], "coins found by the wallet and by two restores",
                "The early copy finds %s of %s coins. Address %d, far ahead in the pool, is known to the late copy (%s) and not to the early one." % (st_[0], fr[0], far, yn(kn)))
    if ex == "ex15":
        f, t = val(ex, "(found, total)")
        return ([ch(["Found after restore", "Paid in all"], [f, t], "coins")], "coins found against coins paid",
                "Only %d of %d coins sit at addresses the backup knows. The other coins are on the chain but invisible to the restored wallet." % (f, t))
    if ex == "ex16":
        b, c, wd, lk = val(ex, "(bits, cs, words, luck)")
        return ([tb([["Part", "Value"], ["Entropy, bits", str(b)], ["Checksum, bits", str(c)], ["Bits in all", str(b + c)], ["Words of 11 bits", str(wd)], ["Chance a wrong set passes", "1 in %d" % round(1 / lk)]], [2.0, 1.25])],
                "how the words are made", "%d words carry %d bits and a %d-bit check; one wrong word set in %d would pass by luck." % (wd, b, c, round(1 / lk)))
    if ex == "ex17":
        ok, ln, oth = val(ex, "(ok, len(seed), other)"); s16 = val(ex, "seed.hex()[:16]")
        return ([tb([["Test", "Result"], ["Seed length, bytes", str(ln)], ["Starts with", s16], ["Matches official vector", yn(ok)], ["No passphrase starts with", oth]], [1.75, 1.5])],
                "the seed from the words", "Same words, other passphrase, other seed: the passphrase is part of the secret.")
    if ex == "ex18":
        ok, k8, cl = val(ex, "(ok, k[:8], len(c) // 2)"); x12 = val(ex, "x[:12]")
        return ([tb([["Part", "Value"], ["Master key starts", k8], ["Chain code, bytes", str(cl)], ["Extended key starts", x12], ["Matches test vector", yn(ok)]], [1.85, 1.4])],
                "the master key of the seed", "Key and chain code together are the root from which every key of the wallet is derived.")
    if ex == "ex19":
        al, pr, ls = val(ex, "(alone, pair, lost)"); acc2 = val(ex, "s['accept']")
        return ([tb([["Signers", "Payment complete?"], ["One key alone", yn(al)], ["Two keys", yn(pr)], ["Lose one: other two sign", yn(ls[0])], ["Lose two: third signs", yn(ls[1])]], [2.0, 1.25])],
                "who can finish the payment", "Two of three keys are enough, and one lost key is no disaster. The node accepted the signed payment: %s." % yn(acc2))
    if ex == "ex20":
        st_, rb = val(ex, "(stuck, robbed)"); nm = ["One key", "Two of three", "One of three"]; pc = lambda v: ("%.2f" % (v * 100)).rstrip("0").rstrip(".") + " %"
        return ([tb([["Scheme", "Stuck", "Robbed"]] + [[nm[i], pc(st_[i]), pc(rb[i])] for i in range(3)], [1.35, 0.95, 0.95])],
                "chance of loss and of theft, per scheme", "Two of three cuts both risks against one key. One of three is stuck rarely but robbed %s of the time." % pc(rb[2]))
    if ex == "ex21":
        vs, sg, cl = val(ex, "(vsize, single, calc)")
        return ([ch(["One key", "Two of three"], [sg, vs], "virtual bytes")], "virtual bytes of one spend",
                "Counting the script parts by hand gives %d, the same as the node recorded. More signatures mean a higher fee." % cl)
    if ex == "ex22":
        y_, bk = val(ex, "(y, back)")
        return ([tb([["Share at x", "Height y = 12 + 30x mod 47"]] + [["x = %d" % (i + 1), str(v)] for i, v in enumerate(y_)] + [["Secret from two shares", str(bk)]], [1.35, 1.9])],
                "three shares and the secret", "Two shares fix the line and give %d, its height at zero. One share alone does not." % bk)
    if ex == "ex23":
        bk, al = val(ex, "(back, alone)"); sh = val(ex, "sh")
        return ([tb([["Share", "Height y"]] + [["x = %d" % i, str(y_)] for i, y_ in sh] + [["Any two shares give", str(bk[0])], ["One share gives the secret", yn(al)]], [1.75, 1.5])],
                "shares and what they rebuild", "The shares are ordinary numbers. Pairs of them agree on %d; a single share does not give it." % bk[0])
    if ex == "ex24":
        n_, m_, p_ = val(ex, "(len(fits), len({s for s, a in fits}), p)"); fs_ = val(ex, "sorted(fits)")
        return ([ch([str(s) for s, a in fs_], [a for s, a in fs_], "slope")], "the slope that fits the share, for each possible secret s",
                "All %d possible secrets have a slope that fits the one share we hold: it reveals nothing." % m_)
    if ex == "ex25":
        sh_, kp, lf = val(ex, "(share, kept, left)"); cut = val(ex, "round(40 * 36 / 100, 2)")
        return ([tb([["Quantity", "Value"], ["Supply implied, millions", str(sh_)], ["40 coins after a 36 % cut", str(kp)], ["Part of the 40 cut away", str(cut)], ["850,000 less 199,999.99", fmt(lf)]], [2.0, 1.25])],
                "arithmetic on quoted figures", "Counts differ by source. These sums show what each figure implies, not which source is right.")
    if ex == "ex26":
        a, b, c = val(ex, "(sold, sizes, msb)")
        return ([tb([["Passage in the saved page", "Found"], ["Sales stopped 26 Nov 2013", yn(a)], ["Sold in set coin sizes", yn(b)], ["Maker called a money transmitter", yn(c)]], [2.3, 0.95])],
                "three claims searched in the saved source", "All three claims of the story are in the saved page. A claim you cannot find in a source is only a claim.")
    if ex == "ex27":
        ow, hr, why = val(ex, "(owner, heir, why)"); pol = val(ex, "p")
        return ([tb([["Who and when", "Allowed?"], ["Owner, at any time", yn(ow)], ["Heir after 1 confirmation", yn(hr[0])], ["Heir after 9", yn(hr[1])], ["Heir after 10", yn(hr[2])]], [2.0, 1.25])],
                "the recorded timelock tests", "The policy is %s. Before the wait the node says: %s." % (pol, why))
    if ex == "ex28":
        top, wr, tr, dy = val(ex, "(top, wrapped, trap, days)")
        return ([tb([["Quantity", "Value"], ["Largest wait, blocks", fmt(top)], ["65536 cut to 16 bits", str(wr)], ["Heir spends at once", yn(tr)], ["Longest wait, days", str(dy)]], [2.0, 1.25])],
                "the sixteen-bit wait field", "A wait of 65536 wraps to %d, so the recorded heir could spend at once: %s." % (wr, yn(tr)))
    raise KeyError(ex)


def visual_kind(ex):
    return "native chart" if ex in ("ex09", "ex10", "ex14", "ex15", "ex21", "ex24") else "table"


CAPTION = {"R": "run under Python %s - L is the chapter library; R is the recorded run of Core 31.1", "seen": "run under Python %s - L is the chapter library; seen() searches a saved source",
           "const": "run under Python %s - L.const reads a constant from a saved source", "none": "run under Python %s - L is the chapter library of the page"}


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
    cap = CAPTION[e["reads"]] % PY
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
    "MtGoxHotWallet": ["WHAT: Mt. Gox of Shibuya, Tokyo, halted withdrawals on 7 February 2014 and suspended all trading on 24 February.",
                       "WHY: It kept customers' coins in its own wallets, so customers held a claim on the exchange and not the keys.",
                       "HOW: A leaked document said 744,408 coins were stolen unnoticed for years; the Tokyo court found Karpeles guilty of falsifying data.",
                       "SO WHAT: Not your keys, not your coins: custody is trust."],
    "CasasciusCoins": ["WHAT: Mike Caldwell sold physical bitcoins: a coin with the private key under a hologram that shows a honeycomb pattern when peeled.",
                       "WHY: A peeled seal shows that someone looked, which a bare slip of paper cannot do.",
                       "HOW: Coins came in 1, 10, 25, 100 and 1000 BTC; FinCEN said minting them made him a money transmitter, so sales stopped on 26 November 2013.",
                       "SO WHAT: A tamper seal tells you someone looked, not who."],
    "ShamirSharesTheSecret": ["WHAT: In November 1979 Adi Shamir published How to Share a Secret, two pages in the Communications of the ACM.",
                              "WHY: A secret kept in one place is lost or stolen with it; shares make both loss and theft need several failures.",
                              "HOW: Any k of n shares rebuild the secret by polynomial interpolation, and k minus 1 shares leave it completely undetermined.",
                              "SO WHAT: Codex32 and SLIP39 apply the same idea to seed words."],
    "TrezorSecureElement": ["WHAT: SatoshiLabs announced the Trezor Safe 5 on 14 June 2024 at BTC Prague, with a colour touchscreen and an EAL 6+ secure element.",
                            "WHY: A thief with the device must guess the PIN, and every wrong try costs more waiting.",
                            "HOW: The waits double, 1, 2, 4 seconds and so on, and after 16 failed tries the device wipes itself.",
                            "SO WHAT: A signing box protects the key; you protect the intent by reading the address on its own screen."],
}
STORY_SUB = {"MtGoxHotWallet": "The coins of everyone sat in one wallet of the exchange", "CasasciusCoins": "A private key hidden under a hologram",
             "ShamirSharesTheSecret": "Shares of a secret: loss and theft both need several failures", "TrezorSecureElement": "A device that makes a thief wait"}
STANDIN = {"MtGoxHotWallet": "Stand-in: a bankruptcy letter, not the theft.", "CasasciusCoins": "Stand-in: a hologram close-up, not the coin.",
           "TrezorSecureElement": "Stand-in: a Trezor Model T, not the Safe 5."}


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
    return add("content", st["title"], STORY_SUB[sid], items, notes)


NE_LABEL = {"bip324_on_the_wire": "BIP 324 on the wire", "bip39_recovery_in_core": "BIP 39 recovery in Core", "estate_planning_with_a_lawyer": "Estate planning with a lawyer",
            "exchange_hack_or_hot_wallet_breach": "An exchange hack or hot-wallet breach", "gpg_signature_check": "A good gpg signature check", "hardware_signing_device": "A hardware signing device",
            "mainnet_funds": "Mainnet funds", "paper_and_metal_backups": "Paper and metal backups", "shamir_slip39_in_a_wallet": "Shamir or SLIP 39 in a wallet", "true_air_gap": "A true air gap"}


def not_run_slide():
    ne = RECORD["not_executed"]; rows = [["Not run here", "Why"]]
    for k, v in ne.items():
        why = re.split(r";| \(|, so ", v)[0].strip()
        why = why[0].upper() + why[1:]
        if len(why) > 62: why = why[:62].rsplit(" ", 1)[0]
        rows.append([NE_LABEL.get(k) or k.replace("_", " ").capitalize(), why])
    n = len(rows)
    tbl = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [3.5, 5.5], "rows": rows, "fs": 10, "rowH": round(min(0.3, 3.4 / n), 3)}
    return add("content", "What these runs did not cover", "Read from the record of the one run; nothing here is claimed as executed", [tbl],
               "Bitcoin Core 31.1 ran once on a private test chain. The table lists, from that record, what was not run: real funds, a physical device, a true air gap, an exchange breach and more. Treat those parts of the chapter as read, not tested.",
               "A safeguard that was not run here is explained, not proven")


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
PLAN = {
    "SecurityModel": (["ex01", "ex02", "ex03", "ex04", "ex05", "ex06", "ex07"], {}),
    "ProtectingKeys": (["ex08", "ex09", "ex10", "ex11", "ex12", "ex13"], {"ex10": "TrezorSecureElement"}),
    "KeepingAccess": (["ex14", "ex15", "ex16", "ex17", "ex18"], {}),
    "SharingControl": (["ex19", "ex20", "ex21", "ex22", "ex23", "ex24"], {"ex24": "ShamirSharesTheSecret"}),
    "CustodyHistory": (["ex25", "ex26"], {"ex25": "MtGoxHotWallet", "ex26": "CasasciusCoins"}),
    "Survivability": (["ex27", "ex28"], {}),
}
BR_KEY = {b: [k for k, v in K.K3.items() if v[0] == b] for b in BRANCHES}


def build():
    S.clear(); ANALOGIES.clear(); FIRST_CODE.clear()
    EX = {e["id"]: e for e in X.EXAMPLES}
    add("title", "Chapter 13: Bitcoin Security", "How keys are protected, backed up, shared and handed on, and what each safeguard costs",
        [{"t": "img", "path": ASSETS + "ch13_bitcoinlogo.png", "x": 7.3, "y": 0.35, "w": 1.9, "h": 1.9},
         {"t": "foot", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.4, "fs": 10, "body": "Picture: the Bitcoin logo, public domain (Wikimedia Commons). Python %s; Bitcoin Core 31.1 results are recorded from one run, not run here." % PY}],
        "This deck explains how Bitcoin coins are kept safe: what a signature protects, where keys are stored, how they are backed up and shared, and what an heir needs. Every number on a result picture was computed, or read from one recorded run of Bitcoin Core 31.1 on a test network.")
    add("content", "Today's route", "", [], "", "Six parts, twenty-eight examples, four true stories")
    add("content", "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 12.0, "items": [
            "Why can a signed payment be published without showing the key, and what breaks it?", "What does a node trust, and how can it check the first block and a download?",
            "How do cold storage, a locked wallet and a signing device each protect keys?", "What does a backup or a set of seed words restore, and what does it miss?",
            "What do several keys and shared secrets buy, and what do they cost?", "What does it mean to leave your coins with an exchange?",
            "How can an heir be allowed to spend after a wait, and what was not run here?"]}],
        "The seven questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all seven has understood the chapter.")
    add("content", "One chapter, six parts", "The concept map the whole deck hangs on",
        [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.4, "cols": 3, "fs": 12.5, "subfs": 10.5, "accent": [],
          "items": [{"label": LAB[b], "sub": "%d key concepts, %d examples" % (len(BR_KEY[b]), len(PLAN[b][0]))} for b in BRANCHES]}],
        "The chapter has six parts and %d key concepts. Each part gets a divider, concept cards with everyday comparisons, code that runs, and some parts a true story. The deck follows the order of the chapter." % sum(len(v) for v in BR_KEY.values()),
        "Six parts; every slide today lives on this map")
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
                if v == "ex09":
                    add("content", "Hot or cold?", "Why the keys live on a machine that is never online",
                        [{"t": "compare", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5,
                          "left": {"head": "A hot wallet is online", "rows": ["Handy for daily payments.", "A thief of the machine can reach the keys.", "Like the cash in your pocket."]},
                          "right": {"head": "Cold storage is offline", "rows": ["Only a signed file travels in.", "The keys never touch a connected machine.", "Like a safe kept at home."]}}],
                        "A hot wallet keeps its keys on a machine that is online, so malware or a thief of the machine can reach them. Cold storage keeps them on a machine that is never connected, and only signed files travel.",
                        "Hot is handy, cold is safe; many people keep both")
        if b == "Survivability":
            not_run_slide()
    add("content", "The chapter in five lines", "One line per idea, each provable from its slides",
        [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.3, "fs": 12.5, "items": [
            "A signed payment shows no key, and editing its payee or amount breaks the signature; peers talk encrypted and trust one typed-in block.",
            "Keys stay offline in cold storage, behind a passphrase, or in a device that waits longer after each wrong PIN.",
            "A backup restores only what it knew; twelve words and a checksum rebuild every key of a wallet.",
            "Two of three keys cut the chance of being stuck but raise the chance of theft; one share of a secret reveals nothing.",
            "An exchange holds claims, not keys; an heir can be made to wait ten blocks; some safeguards were not run here."]}],
        "These five lines are the deck in miniature, one for each group of parts. A line that feels unproven should send you back to its code slide, because every figure in it was computed or read from the recorded run. The chapter code tab of the course page reruns all %d examples." % len(X.EXAMPLES),
        "If a line feels unproven, the code slide of its part carries the receipt")
    old_res = [s for s in OLD["slides"] if any(i.get("t") == "links" for i in s["items"])][0]
    res = json.loads(json.dumps(old_res["items"][0]))
    add("content", "Where to go from here", RES_SUB, [res],
        "Everything here is free to read or watch. A good start is the Stand-up Maths video on secret sharing, then the Optech topic on partially signed transactions beside the chapter. The course page for chapter 13 carries the full text and every source.",
        "Watch the secret-sharing video, then read the Optech topic beside the chapter")
    add("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What a signature protects", "How keys are stored and backed up", "How control is shared among holders", "Why custody is trust"]}],
        "Four claims, each carried by computations that ran on slides of this deck. The course page for chapter 13 has every word behind them, the stories with their sources, and the question bank to test yourself.", None, "dark")
    N = len(S)
    sec = [i + 1 for i, s in enumerate(S) if s["kind"] == "section"]
    rows = [("Questions and the chapter map", 3, sec[0] - 1)] + [(S[a - 1]["title"], a, (sec[i + 1] - 1 if i + 1 < len(sec) else N)) for i, a in enumerate(sec)]
    S[1]["sub"] = "Six parts; every number is a slide you can jump to"
    S[1]["items"] = [{"t": "boxes", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.5, "cols": 2, "fs": 11.0, "subfs": 10.5, "accent": [],
                      "items": [{"label": "%d. %s" % (i + 1, r[0]), "sub": "(slides %d-%d)" % (r[1], r[2])} for i, r in enumerate(rows)]},
                     {"t": "stat", "x": 7.05, "y": 1.4, "w": 2.45, "h": 3.5, "vert": True, "items": [
                         {"n": str(N), "label": "slides, numbered bottom-right"}, {"n": str(len(ST.STORIES)), "label": "true stories, each told by 5N1K"},
                         {"n": str(len(X.EXAMPLES)), "label": "code examples with a picture of each result"}]}]
    S[1]["notes"] = "The route has six parts that follow the order of the chapter. Four true stories and twenty-eight code examples are spread across them. The examples are listed in the same order in the chapter code tab of the course page, so every listing here can be run and edited there."
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


WHEEL = "03-materials/ch13/assets/sen0401_ch13_lib-1.1.0-py3-none-any.whl"
LIBMODS = ["sen0401_ch13_lib_v1_0_0", "sen0401_ch10_p2p_v1_0_0"]


def manifest(N):
    setup = "# setup: the chapter library of the page (L = chapter 13 library, R = the recorded run of Bitcoin Core 31.1, seen = search a saved source); the page boots these names\n" + X.PRELUDE.strip()
    exs = []
    for i, e in enumerate(sorted(X.EXAMPLES, key=lambda e: e["slide"]), 1):
        exs.append({"order": i, "id": e["id"], "name": e["name"], "slide": e["slide"], "branch": LAB[e["branch"]], "library": "sen0401_ch13_lib", "needs": ["setup"],
                    "code": "\n".join(l for g in e["groups"] for l in g["lines"]), "show": [{"expression": x, "expected": o} for x, o in OUT[e["id"]]], "result_picture": visual_kind(e["id"])})
    # the page path is verified here: a fresh interpreter in a scratch folder holding ONLY the unpacked wheel of the page, the setup and the listing
    tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch13_")
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
        print("page path (the unpacked wheel only) under %s: %d examples reproduce the recorded values" % (py, len(exs)))
    shutil.rmtree(tmp, ignore_errors=True)
    return {"manifest": "chapter_code_ch13_v1_0_0", "chapter": 13, "deck": "SEN0401_Ch13_BitcoinSecurity_3e_v%s.pptx" % VER_US, "deck_version": VER, "python_of_expected_values": PY,
            "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the library defined in the page",
            "library": {"module": "sen0401_ch13_lib", "file": WHEEL, "sha256": hashlib.sha256(open(os.path.join(ROOT, WHEEL), "rb").read()).hexdigest(), "modules": LIBMODS,
                        "import": "import sen0401_ch13_lib_v1_0_0 as L; R = L.run(); seen = L.has"}, "setup": {"code": setup, "data": {}}, "examples": exs}


def main(render):
    N = build(); cov = refuse(N)
    plan = {"meta": {"title": "Chapter 13: Bitcoin Security", "sub": "SEN0401, third-edition deck 2.0.0", "version": VER, "python": PY, "total": N,
                     "redesign": "2026-10-25, task TK_Ch13_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
                     "notes": "short reader's prose: 2-4 sentences, at most 60 words",
                     "analogies": ANALOGIES, "coverage": {"measure": "key concepts of the research whose label is on a slide", "percent": round(cov, 1)}}, "slides": S}
    p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p, "-", N, "slides")
    m = manifest(N); mp = os.path.join(ROOT, "03-materials", "ch13", "page", "chapter_code_ch13_v1_0_0.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False); print("written", mp, "-", len(m["examples"]), "examples in slide order:", [e["slide"] for e in m["examples"]])
    if not render: return
    out = os.path.join(HERE, "sen0401_ch13_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    def run(cmd, env=None, cwd=None):
        r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
        if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
    run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"}, cwd=HERE)
    run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
    run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 13"])
    mat = os.path.join(ROOT, "03-materials", "ch13", "SEN0401_Ch13_BitcoinSecurity_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)


if __name__ == "__main__":
    main("--render" in sys.argv)
