#!/usr/bin/env python3
"""sen0401_exam_analysis_build v1_1_0 - (second edition: adds the owner points G to P of 21:49) writes the owner's analysis of the midterm items v1.3.0 (plain words) from the items file, the structure, the critical points and the owner topics. It decides nothing. Usage: no arguments; writes analysis_v1_3_0/sen0401_exam_analysis_v1_3_0.md"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); ld = lambda f: json.load(open(os.path.join(H, f), encoding="utf-8"))
N = {x["key"]: x for x in ld("sen0401_exam_items_midterm_v1_3_0.json")["items"]}; S = ld("sen0401_exam_structure_v1_0_0.json")
CPJ = ld("sen0401_exam_critical_points_v1_0_0.json"); CP = {p["id"]: p for p in CPJ["list_A_points_carried_by_a_source"]}
short = lambda k: k[4:7]
SUBS = {}; BON = {}
for q in S["questions"]:
    for s in q["sub"]:
        (BON if q.get("bonus") else SUBS).setdefault(s["item"], []).append((s["key"], s["points"]))
DESC = {
 "i01": "Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it.",
 "i02": "Your case 3: a payment with several inputs and outputs; find the change and see that, with no change output, the miner collects the whole left-over as the fee.",
 "i03": "Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much.",
 "i04": "How a day's volume-weighted price is built from trades, with one trade left out to find.",
 "i05": "Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table.",
 "i06": "Your case 1: put five transactions in order by the spending references, back to the coinbase transaction.",
 "i07": "Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be.",
 "i09": "Which setting a Bitcoin node really uses when the command line and the configuration file disagree.",
 "i10": "Match each node setting (pruning, index, connections and similar) to the need it serves.",
 "i11": "Why release tags must be sorted by version number, not as text, shown by a small program.",
 "i12": "Why both the node password setting and the older address keep a hash instead of the secret.",
 "i13": "Why every extra letter of a vanity address makes the search 58 times harder.",
 "i14": "Why a backup key in the wrong form shows a zero balance and what the paper wallet must give back.",
 "i15": "Why the older address hides the key behind a hash (a commitment) and why newer scripts use a longer hash.",
 "i17": "How long a recovery code is, from the bits each word carries and the checksum.",
 "i18": "Match each short real story (a lost password, a block that created coins from nothing, and so on) to the lesson it teaches.",
 "i19": "How far a recovery scan looks before it stops (the gap limit), shown by a small program.",
 "i20": "Why a phone restored from the words alone shows other addresses and no labels: the passphrase and labels matter.",
 "i21": "How a count is written in few bytes (CompactSize), shown by a small program at the edges.",
 "i22": "Which inputs allow replacement and carry a relative timelock, read from the sequence field by a small program.",
 "i23": "Why a payment tracker can rely on the transaction identifier after the witness change, and why witness bytes make a payment cheaper.",
}
BDESC = {"b1:no-bank": "Bonus, written by hand: who refuses a double spend when no bank stands in the middle, and why that makes history costly to change.",
         "b2:mining-check": "Bonus, written by hand: why mining is a search nobody can shortcut, yet every node can check a block easily."}
TOP = {"T4": ["i05"], "T6": ["i18"], "T7": ["i06", "i07", "i22"], "T8": ["i20", "i17", "i19"], "A": ["i02"], "B": ["i03"], "C": ["i06", "i07"]}
BTOP = {"b1:no-bank": ["T1 (half)", "T2 (half)", "T3"], "b2:mining-check": ["E (half)"]}
touch = {}
for t, its in TOP.items():
    for i in its: touch.setdefault(i, []).append(t)
holders = {}
for k, x in N.items():
    for c in x.get("critical_points", []): holders.setdefault(c, set()).add(short(k))
bonus_cps = {"b1:no-bank": ["CP1.03", "CP1.07"], "b2:mining-check": ["CP2.12"]}
for b, cs in bonus_cps.items():
    for c in cs: holders.setdefault(c, set()).add("bonus " + b[:2])
sole = lambda i: [c for c in N[[k for k in N if short(k) == i][0]].get("critical_points", []) if holders[c] == {i}]
def cpt(c, n=400): return CP[c]["point"][:n].rstrip() if c in CP else ""
GP = [  # id+name, today verdict text, items text, plain point, related CPs, chapter slot, candidate items
 ("G", "Coinbase amount, reward by block number, minting end, first blocks, totals", "PARTIAL: i03 asks the reward by height with the halving interval and the fees, and a claim that is too large; NOT asked: the first blocks' amounts, the total over a halving era, the coinbase after minting ends (fees only)", "i03 (and i02 for the fee)", ["CP6.18", "CP6.05", "CP1.02", "CP6.17"], "chapter 6 (the schedule, CP6.18 and CP6.05) with chapter 1 (the cap, CP1.02); i03 could carry the other parts by rework with varied numbers", ["i03", "i04", "i13", "i17"]),
 ("H", "First spend and the pizza", "GAP: no item asks it", "none", ["CP1.01", "CP6.22", "CP1.02"], "chapter 1 (the first payment, CP1.01, and the first spend, CP6.22 in chapter 6); a numeric slot with easy arithmetic", ["i04", "i03", "i17", "i13"]),
 ("I", "Hash capacity, the 10-minute rule and price; pools", "GAP for the machine-read items; only the half 'nobody can shortcut the search' sits in the hand-marked bonus b2", "bonus b2 (half)", ["CP2.12", "CP2.04", "CP1.11"], "chapter 2 (mining, CP2.12) with chapter 1 (price, CP1.11); the same family as your points D, E and F", ["i05", "i06", "i07", "i04"]),
 ("J", "Choice of transactions by fee per size", "PARTIAL: i02 asks the fee as the difference of inputs and outputs, i23 asks the weight that makes witness bytes cheaper; NOT asked: that miners choose by fee per size (CP2.08)", "i02, i23", ["CP2.08", "CP2.10", "CP6.19", "CP3.10"], "chapter 2 (CP2.08, best fee rates first) or chapter 6 (weight, CP6.19)", ["i05", "i06", "i07", "i22"]),
 ("K", "Why digital money failed before Bitcoin", "GAP for the machine-read items; the double-spend half sits in the hand-marked bonus b1", "bonus b1 (half)", ["CP1.07", "CP1.03", "CP1.02"], "chapter 1 (CP1.07 and CP1.03)", ["i01", "i02", "i03", "i04"]),
 ("L", "Why old currencies are no longer used (Ottoman, TL and YTL)", "GAP: no critical point or deck slide carries it; it is your own material and the items would be new text with synthetic data", "none", ["CP1.02"], "chapter 1 (money as a ledger, CP1.02)", ["i04", "i01", "i03"]),
 ("M", "Losing access to private keys; best practices", "PARTIAL: i18 (a lost password story), i01 (an untested backup), i20 (what a full backup holds) touch it; NOT asked as the list of best practices", "i01, i18, i20", ["CP5.15", "CP5.18", "CP5.19", "CP5.07", "CP5.17"], "chapter 5 (backups, CP5.15); i20, i17 or i19 slots", ["i17", "i19", "i20", "i14"]),
 ("N", "Why an input cannot carry its own confirmation; locking and unlocking scripts", "GAP: the decks name the lock of an output but no item asks why both scripts must run together; the nearest points are CP6.01 (no holder) and CP4.05 (i12, i15)", "none (i12 and i15 touch hashes in locks)", ["CP6.01", "CP4.05", "CP4.06"], "chapter 6 (CP6.01) or chapter 4 (scripts that hash, CP4.05 and CP4.06)", ["i21", "i22", "i23", "i12", "i15"]),
 ("O", "Who confirms; fake transactions and blocks", "PARTIAL: i18 (a range check refuses an invalid amount), i05 (confirmations) and bonus b1 (every node checks) touch it; NOT asked: how a fake source is met", "i05, i18, bonus b1", ["CP2.06", "CP2.13", "CP6.13", "CP3.11", "CP1.03"], "chapter 2 (consensus rules checked by every node, CP2.06) or chapter 3 (checking a block, CP3.11)", ["i05", "i06", "i07", "i09", "i10", "i11", "i12"]),
 ("P", "The 51 percent rule and the attack", "PARTIAL: i05 asks the chance that an attacker with a share of the hash power catches up and how many confirmations protect; NOT asked: the 51 percent rule itself", "i05", ["CP2.05", "CP1.03"], "chapter 2 (CP2.05); i05 could carry it by rework", ["i05", "i06", "i07"]),
]
L = []; w = L.append
w("# SEN0401 midterm: analysis of the items v1.3.0 for the owner (second edition, with points G to P)\n")
w("Written for you to read, not to decide. Nothing here drops or changes an item. Each row says what an item tests, which important points of the chapters (critical points, CP) it holds and which of your topics it touches. Your topics: T1 to T9 are the first list (T1 serverless peer-to-peer, T2 distributed trust, T3 double-spending prevention, T4 independent confirmations, T5 approval without private keys, T6 genuine against fake transaction, T7 timing differences in spending, T8 why seed words replaced random keys, T9 borderless nature). A to F are the six added points of 21:23, and G to P are the ten added points of 21:49 (G coinbase amounts, H the first spend and the pizza, I hash capacity, ten-minute rule, price and pools, J choice by fee per size, K why digital money failed, L old currencies, M lost keys, N input and output scripts, O who confirms and fake transactions, P the 51 percent attack). A to F are the six added points (A inputs against outputs and fee, B block reward by height, C coins minted by miners, D blocks link to the previous block, E hash search and difficulty target, F the 10-minute rule and soft forks).\n")
w("How to read the numbers: the paper has 4 questions of 25 points and a hand-marked bonus of 10. There are 21 items; they give 24 machine-read units (sub-questions) because items i07, i15 and i23 fill two sub-questions each, and 2 bonus prompts that you mark by hand.\n")
w("## 1. All items of the exam\n")
w("| Item | Chapter | Sub-question (points) | What it tests, in plain words | Critical points it holds | Your topics it touches |"); w("|---|---|---|---|---|---|")
for k, x in N.items():
    i = short(k); sq = ", ".join("%s (%s)" % s for s in SUBS.get(k, [])); chs = ", ".join(str(c) for c in x["chapters"])
    w("| %s | %s | %s | %s | %s | %s |" % (i, chs, sq, DESC[i], ", ".join(x.get("critical_points", [])), ", ".join(touch.get(i, [])) or "none"))
for q in S["questions"]:
    if q.get("bonus"):
        for s in q["sub"]:
            b = s["item"][4:]; w("| %s | %s | %s (%s) | %s | %s | %s |" % (b[:2], ", ".join(str(c) for c in s["chapters"]), s["key"], s["points"], BDESC[b], ", ".join(s.get("critical_points", [])), ", ".join(BTOP[b])))
w("")
w("Count by chapter (an item with two chapters counts under its first): chapter 1: i01, i02, i03, i04 (4); chapter 2: i05, i06, i07 (3); chapter 3: i09, i10, i11, i12 (4); chapter 4: i13, i14, i15 (3); chapter 5: i17, i18, i19, i20 (4); chapter 6: i21, i22, i23 (3).\n")
w("## 2. What your topics have today\n")
w("| Topic | Today | Items |"); w("|---|---|---|")
for t, v, its in [("T1 serverless peer-to-peer", "not asked by the machine-read items", "only half of bonus b1"), ("T2 distributed trust", "not asked", "only half of bonus b1"), ("T3 double-spending prevention", "not asked by the machine-read items", "bonus b1 by hand"), ("T4 independent confirmations", "asked", "i05"), ("T5 approval without private keys", "not asked", "none"), ("T6 genuine against fake transaction", "partly", "i18 (one story: a range check refuses a bad amount)"), ("T7 timing differences in spending", "partly (my reading: order and moment of spending)", "i06, i07, i22"), ("T8 why seed words replaced random keys", "partly: the words are used, the reason is not asked", "i20, i17, i19"), ("T9 borderless", "not asked", "none"), ("A inputs against outputs and fee", "asked", "i02"), ("B block reward by height", "asked, but not the end of halving at one satoshi and not that the names satoshi and bitcoin are not on the chain", "i03"), ("C coins minted by miners, inputs back to a coinbase", "asked", "i06 (and i07)"), ("D block links to the previous block", "not asked", "none"), ("E hash trials, difficulty target, adjustment", "not asked; only the 'nobody can shortcut' half in bonus b2", "bonus b2"), ("F ten-minute rule and soft forks", "not asked; soft fork appears only inside i23", "i23 (a side mention)")] + [(p[0] + " " + p[1], p[2], p[3]) for p in GP]:
    w("| %s | %s | %s |" % (t, v, its))
w("")
w("## 3. The critical points that each item alone holds\n")
w("If you drop an item, these important points would have no other item that asks about them (bonus prompts count as holders; they are marked by hand).\n")
w("| Item | Critical points held by this item alone | Critical points it shares with other items |"); w("|---|---|---|")
for k, x in N.items():
    i = short(k); so = sole(i); sh = [c for c in x.get("critical_points", []) if c not in so]
    w("| %s | %s | %s |" % (i, "; ".join("%s (%s)" % (c, cpt(c)) for c in so) or "none", ", ".join(sh) or "none"))
w("")
# emphasised concepts
EMPH = [
 ("D", "Each block links to the previous block, so miners restart on a new block", "chapter 2 (mining, CP2.04 and CP2.12) or chapter 3 (checking a block header, CP3.11)", "No critical point of the chapters states this exactly; CP2.04 (how a payment reaches a block) and CP3.11 (hash the 80-byte header) are the nearest: CP2.04 is held by i07 alone, CP3.11 by no item.", ["i05", "i06", "i07", "i09", "i10", "i11", "i12"]),
 ("E", "Hash trials are unpredictable; the requirement is a value below a difficulty target, adjusted after a fixed number of blocks", "chapter 2 (CP2.12, mining is a search nobody can shortcut), or chapter 4 where i13 (vanity search) already asks a related unshortcut-able search", "CP2.12 is held only by the hand-marked bonus b2. i13 could be reworked in place instead of dropped.", ["i05", "i06", "i07", "i13", "i14", "i15"]),
 ("F", "The 10-minute rule and soft forks: the steady block interval protects against forking risk", "chapter 6 (CP6.15 soft fork, held by no item) with i23, which already mentions the soft fork as a side point", "CP6.15 and the interval rule have no holder today.", ["i21", "i22", "i23", "i03"]),
 ("T1", "Serverless peer-to-peer", "chapter 1 (CP1.12 and CP1.03)", "Only the hand-marked bonus b1 touches half of it.", ["i01", "i02", "i03", "i04"]),
 ("T2", "Distributed trust", "chapter 1 (CP1.10 and CP1.03)", "Only half of bonus b1.", ["i01", "i02", "i03", "i04"]),
 ("T3", "Double-spending prevention", "chapter 1 (CP1.07) or chapter 2 next to i05", "Only bonus b1, by hand.", ["i01", "i04", "i05", "i06", "i07"]),
 ("T5", "Approval without private keys: what a signature proves", "chapter 6 (CP6.01) or chapter 1 (CP1.08, the key is the proof of ownership)", "CP6.01 is held by no item.", ["i21", "i22", "i23", "i01", "i04"]),
 ("T9", "The borderless nature of Bitcoin", "chapter 1 (CP1.12)", "CP1.12 is held by no item.", ["i01", "i02", "i03", "i04"]),
]
w("## 4. Your emphasised concepts: where each could go and what it would cost\n")
w("For each concept: the chapter whose slot could host it, the items that sit in that area, and, for each, the important points that would lose their only holder if that item were dropped. A new item would take the dropped item's place and answer type, so the paper keeps 25/25/25/25 + 10. Each table drops one item at a time; dropping two items together can lose more. Reworking an item in place is also possible and loses nothing; it is not shown as a row because it keeps the old item's topic.\n")
for cid, name, slot, note, cands in EMPH:
    w("### %s: %s\n" % (cid, name)); w("- Slot: %s." % slot); w("- Today: %s" % note)
    w("| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |"); w("|---|---|---|---|")
    for i in cands:
        k = [x for x in N if short(x) == i][0]; typ = N[k]["type"]; pts = sum(p for _, p in SUBS[k]); so = sole(i)
        w("| %s | %s, %d points | %s | %s |" % (i, typ, pts, DESC[i], "; ".join("%s (%s)" % (c, cpt(c)) for c in so) or "none"))
    w("")
w("The unit count stays 24 as long as an item is replaced by one of the same unit count; dropping i07, i15 or i23 frees two sub-questions at once.\n")
w("## 4b. Your added points G to P: where each could go and what it would cost\n")
w("Same reading as section 4: one item dropped at a time, nothing decided. Critical points marked 'no item' today are held by no item, so a new item could add a first holder. Many of G to P are economic and trust topics of chapters 1 and 2; the mechanics are chapters 3 and 6, as the slot lines say.\n")
for cid, name, verdict, holders_txt, rel, slot, cands in GP:
    w("### %s: %s\n" % (cid, name)); w("- Today: %s." % verdict); w("- Related critical points: %s." % "; ".join("%s (%s, %s)" % (c, cpt(c), "held by " + ", ".join(sorted(holders[c])) if c in holders else "no item") for c in rel if c in CP))
    w("- Slot: %s.\n" % slot)
    w("| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |"); w("|---|---|---|---|")
    for i in cands:
        k = [x for x in N if short(x) == i][0]; so = sole(i); w("| %s | %s, %d points | %s | %s |" % (i, N[k]["type"], sum(p for _, p in SUBS[k]), DESC[i], "; ".join("%s (%s)" % (c, cpt(c)) for c in so) or "none"))
    w("")
w("## 5. The C2 question: mined or not, under your simpler rule\n")
w("Your rule: a spending reference means the referenced transaction was already mined. The current C2 (item i07) is more careful: it says a transaction that only names an output of another, unmined transaction does not prove that one mined. So today A, B and C are mined (C is stated to be in a block, and A and B are named by the chain above it), and D and E are left undecided.\n")
w("The facts of the current item: C spends an output of B; B spends an output of A; E spends an output of D; C is stated to be inside a block; nothing is said of E.\n")
w("Under your simpler rule C2 becomes:\n")
w("- A, B and D are mined, because each of them is named by a spending reference (B by C, A by B, D by E).")
w("- C and E are not shown to be mined: nobody spends them yet, so they may be in a block or still waiting.")
w("- The sentence 'C is inside a block' is no longer needed as a fact; the rule itself gives A and B.")
w("- The two blanks become: 'A, B and D are ____' (mined) and 'C and E are ____' (not shown to be mined, may still wait). The wrong entries stay: 'not mined (still waiting)' and 'mined later than C'.")
w("- The tip must then state your rule in words: a spending reference can only point at an output that already exists in a block.")
w("- The answer sheet is unchanged (same fill-in block type); only the key changes (D moves from undecided to mined, C and E become the undecided pair).")
w("- If you want a strict 'mined / not mined' two-way answer, the item must also say which transactions are known to be waiting (for example, 'F and G are in a node's waiting list'); without that the student cannot know, and the honest third answer 'not shown to be mined' stays.")
w("- Note for you: a node can hold chains of unmined transactions that spend each other, so your rule is exactly right for references written in blocks. The item can say that the references shown are the ones written in blocks, which makes your rule true as stated.\n")
w("Nothing in this file has been applied to the items. Items v1.3.0 stay as committed.")
out = os.path.join(H, "analysis_v1_3_0", "sen0401_exam_analysis_v1_3_0_b.md"); open(out, "w", encoding="utf-8").write("\n".join(L) + "\n"); print(out, len(L), "lines")
