#!/usr/bin/env python3
"""Chapter 9 (Transaction Fees) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_1_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the records of Bitcoin Core 31.1 on regtest are on slides that say Recorded;
what the research marks NOT EXECUTED carries that label; the three pictures that show a topic and not the event are labelled stand-in. Speaker notes are short reader's prose
(2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, datetime, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_1_0 as E
import sen0401_links_v1_0_0 as LK

E.init(9, HERE, assets=("photo_bitcoin_mining_farm.png", "photo_bitcoin_namecoin_accepted_here_sign.png", "photo_lightning_network_logo.png", "photo_nassau_hall_princeton.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS)
assert (NPUB, NFIND, NCLAIM) == (72, 20, 71), (NPUB, NFIND, NCLAIM)
OUT = lambda grp, i: ast.literal_eval(G[grp][i][1])
REC = "Recorded"
KEEP = {}          # key -> title, to find the slide numbers once the agenda has been inserted


def con(grp, x, y, w, h, label, fs=10, rows=None):
    return dict(E.code(grp, x, y, w, h, fs=fs, rows=rows), label=label)


def beats(x, y, w, h, items, fs=10.5):
    return {"t": "beats", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def foot(x, y, w, h, body, fs=11.5):
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def chips(x, y, w, h, items, fs=10):
    return {"t": "chips", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def flow(x, y, w, h, steps, fs=11):
    return {"t": "flow", "x": x, "y": y, "w": w, "h": h, "fs": fs, "steps": steps}


def page(key, title, sub, items, notes, take, lede=None):
    KEEP[key] = title
    E.content(title, sub, items, notes, take=take, lede=lede)


def rows_of(grp, idx):
    return [G[grp][i] for i in idx]


def story(key, sid, photo, standin, beats_, grp, idx, label, notes, title=None):
    st = STORY[sid]
    rr = rows_of(grp, idx)
    E.story_slide(sid, photo, (0.5, 1.4, 2.9, 2.45), beats_, grp, rr, label, "", (3.6, 3.0, 5.9, 1.38), (3.6, 1.4, 5.9, 1.2), title=title)
    s = E.S[-1]
    s["notes"] = notes
    dt = datetime.date.fromisoformat(st["when"])
    s["sub"] = "The story of %d %s %d: who, where, when and what to read next" % (dt.day, dt.strftime("%B"), dt.year)
    for it in s["items"]:
        if it.get("t") == "factrow":
            it["x"], it["w"], it["y"] = 0.5, 9.0, 4.62
        if it.get("t") == "beats":
            it["fs"] = 10.5
    if standin:
        s["items"].append(foot(0.5, 4.22, 2.9, 0.36, standin, fs=9))
    KEEP[key] = s["title"]


# ---------------------------------------------------------------------------------------------- 1-3 opening
E.slide("title", "Chapter 9: Transaction Fees", "Who pays a fee, how it is priced, replaced and bumped, and what moved since print. Bitcoin Core 31.1 results are Recorded.", [],
        "This deck explains transaction fees: who pays them, how they are priced, how a payment is replaced or bumped, and what has changed since the book went to print. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1 was run on a test network, so its answers are Recorded and only read back here. The research package for chapter 9 holds the sources and the claims.")

page("questions", "The questions this chapter answers", "Its own competency questions, and the numbers behind the answers",
     [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 1.7, "fs": 13, "items": list(C.CQS)},
      {"t": "stat", "x": 0.5, "y": 3.3, "w": 9.0, "h": 1.6, "items": [
          {"n": str(NPUB), "label": "sources, opened and read on %s" % D.DATE},
          {"n": str(NCLAIM), "label": "claims, each recomputed by running code"},
          {"n": str(NFIND), "label": "findings, several of them corrections of the book"}]}],
     "The chapter asks two questions that this deck answers by computation: which of its statements can be checked, and what has changed since print. The three numbers are counted from the research package, which holds %d sources, %d findings and %d executed claims. Each slide that follows shows the computation behind one claim." % (NPUB, NFIND, NCLAIM),
     "")
E.S[-1].pop("take", None)

# ---------------------------------------------------------------------------------------------- part A
E.section("Who pays, and how a fee is priced", "A fee is what is left over; size is counted in virtual bytes, and nodes and wallets set a floor.",
          [{"label": "The fee is a difference"}, {"label": "Size and fee rate"}, {"label": "Minimums and dust"}],
          "This part starts from the simplest fact, that a fee is the difference between inputs and outputs, and prices it in virtual bytes. It ends with the floors that nodes and wallets apply, and with the dust rule that bars tiny outputs. Each slide has a console that ran on the test node of Bitcoin Core 31.1.")
KEEP["secA"] = "Who pays, and how a fee is priced"

CHANGE = "Like the change at a shop: the fee is what is left over, and nobody writes it on the note"
page("diff", "A fee is a difference, not a field", CHANGE,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Inputs", "sub": "20 BTC spent"}, {"label": "Outputs", "sub": "1 BTC sent"}, {"label": "Fee", "sub": "19 BTC left over", "hot": True}]),
      con("FeeDiff", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest, parsed here by an independent parser", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 1 and 2: the parser finds version, inputs, outputs and lock time, and no field called fee",
                                  "Rows 3 and 4: inputs minus outputs is 1,900,000,000 satoshis; Core refuses it as max-fee-exceeded",
                                  "Row 5: lowering an output after signing makes a bigger fee, and the signature no longer matches"], fs=10)],
     "A Bitcoin transaction has no fee field: the fee is what the inputs hold minus what the outputs take, and the miner of the block collects it. The console parses the raw bytes of a test transaction and finds only version, inputs, outputs and lock time. Core refused a transaction that forgot its change, because 19 bitcoins would have gone to the miner. Lowering an output after signing breaks the signature, so only the spender can set the fee.",
     "The fee exists only as inputs minus outputs, so only the signer can set it")

POST = "Like postage by volume: a bulky parcel pays for the space it takes, not its weight"
page("size", "Virtual size and the fee rate", POST,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "No witness", "sub": "113 bytes"}, {"label": "With witness", "sub": "222 bytes"}, {"label": "Weight", "sub": "561 units"}, {"label": "Virtual size", "sub": "141 vB", "hot": True}]),
      con("SizeRate", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest; block 840,000 is a saved block", fs=10, rows=rows_of("SizeRate", [0, 1, 2, 3, 5])),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: 113 bytes without witness, 222 with it; weight is 3 x 113 + 222 = 561, and the virtual size is 141",
                                  "Row 3: 282 satoshis over 141 vB is 2.0 sat/vB; the book's size over weight, 0.2513, is no price at all",
                                  "Rows 4 and 5: 0.00006570 BTC per kvB is 6.57 sat/vB; a block may weigh 4,000,000 and block 840,000 weighed 3,993,281"], fs=10)],
     "Weight counts witness bytes once and other bytes four times, and the virtual size is the weight divided by four, rounded up. The console parses a test transaction and finds 113 bytes without witness, 222 with it, weight 561 and 141 virtual bytes. The fee rate is the fee divided by the virtual size, 2.0 satoshis per virtual byte here, whereas the book's size divided by weight is a pure number. The unit of estimatesmartfee is bitcoin per kilovirtual byte.",
     "The fee rate is the fee over virtual size; size over weight is no price")

page("floor", "Minimum fees and dust", "Core 30.0 lowered the relay floor to 0.1 sat/vB; the wallet keeps its own floor of 1",
     [chips(0.5, 1.27, 9.0, 0.38, ["relay floor 0.1 sat/vB", "wallet floor 1 sat/vB", "dust 294 / 330 / 240"], fs=9.5),
      con("MinFees", 0.5, 2.15, 9.0, 1.98, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 4.38, 9.0, 0.6, ["Rows 2 to 4: for 141 vB, 8 and 14 satoshis are refused and 15 accepted; the wallet refuses 0.5 and 0.1 and takes 1",
                                  "Rows 5 and 6: dust is 3 sat/B times (size + 67): 294, 330 and 240; one satoshi less is refused each time"], fs=10)],
     "A node refuses a transaction below its minimum relay fee: since Bitcoin Core 30.0 that is 0.1 satoshi per virtual byte, so a 141-byte transaction needs 15 satoshis and the node refused 8 and 14. Bitcoin Core's wallet keeps its own minimum of 1 satoshi per virtual byte, ten times higher. An output is dust when it costs more to spend than it is worth: 294 satoshis for P2WPKH, 330 for P2WSH and 240 for pay to anchor.",
     "The node floor is 0.1 sat/vB; the wallet floor is ten times higher")

# ---------------------------------------------------------------------------------------------- part B
BUS = "Like seats on a bus that leaves every ten minutes: the highest bids board first."
E.section("Estimating fees, and the market", BUS,
          [{"label": "The estimator"}, {"label": "Two blocks compared"}, {"label": "The halving block"}],
          "This part asks how a wallet guesses a good fee and what the market for block space looked like in two real blocks. The bus on the slide is the picture to keep: a block is a bus with a fixed number of seats, and a fee is a bid for one. The part ends with the story of the halving block, in which fees were almost the whole reward.")
KEEP["secB"] = "Estimating fees, and the market"

page("estimator", "The estimator learns from blocks", "A fresh node has no history, so the book's call needs time and traffic before it answers",
     [chips(0.5, 1.27, 9.0, 0.38, ["120 blocks, 2,640 payments", "1.225 sat/vB", "144 blocks: 60 answered"], fs=9.5),
      con("Estimator", 0.5, 2.15, 9.0, 1.98, "Recorded: Core 31.1 regtest, estimatesmartfee on a chain of 231 blocks", fs=10),
      beats(0.5, 4.38, 9.0, 0.6, ["Rows 2 and 3: no estimate at first; after 2,640 payments 1.225 sat/vB for 2 blocks and 1.173 for 6 and 25",
                                  "Rows 4 to 6: a target of 144 was answered for 60 blocks; the default mode equals economical, and differs from conservative at 144"], fs=10)],
     "The call estimatesmartfee looks for the lowest fee rate at which most recent transactions confirmed within the target, so it needs history. A fresh test node answered Insufficient data; after 120 blocks and 2,640 payments of mixed fee rates it answered 1.225 satoshis per virtual byte. The target of 144 blocks was answered for only 60, because the node's history was that long. Since Bitcoin Core 28.0 the default mode is economical, not conservative.",
     "The estimator needs history; a fresh node answers with no estimate")

page("census", "Two blocks, two fee markets", "Median fee rate, fee share and replacement signals in two saved mainnet blocks",
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: the median fee rate of the first 599 transactions was 1,436.45 sat/vB in block 840,000 and 3.02 in block 971,489",
                                   "Row 3: fees were 92.33 percent of the reward in the halving block and 0.46 percent in the later one",
                                   "Row 4: 81 and 46 percent of those transactions signal replaceability"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Fee share of reward, and signals of 599, in %", "dataLabels": True, "dlFmt": "0.##", "dlFs": 9,
       "labels": ["fees 2024", "fees 2026", "signals 2024", "signals 2026"], "series": [{"name": "percent", "data": OUT("Census", 2) + OUT("Census", 3)}]},
      con("Census", 0.5, 3.42, 9.0, 1.38, "executed on saved blocks: the census of 2026-10-15", fs=10, rows=rows_of("Census", [0, 1, 2, 3]))],
     "A census of the first 599 transactions after the coinbase of two real blocks shows how much the market moves. In the halving block of April 2024 the median fee rate was 1,436 satoshis per virtual byte and fees were 92.33 percent of the reward; in block 971,489, mined on 15 October 2026, the median was 3.02 and fees were 0.46 percent. The share of transactions that signal replaceability fell from 81 to 46 percent.",
     "Fees were 92.33 percent of the reward in 2024 and 0.46 percent in 2026")

story("halving", "HalvingBlock", "photo_bitcoin_mining_farm.png", "Stand-in picture: a mining farm, not this block.",
      ["On 20 April 2024 the pool ViaBTC mines block 840,000, the first after the fourth halving",
       "The subsidy fell to 312,500,000 satoshis (row 2); the fees were 3,762,561,499, so 92.33 percent of the reward (row 3)",
       "The book says the subsidy is much higher than the fees: true of block 971,489 at 0.46 percent, false here"],
      "Halving", [0, 1, 2], "executed on a saved block: fees and reward in satoshis",
      "On 20 April 2024 the pool ViaBTC found block 840,000, the first block after the fourth halving, which cut the subsidy to 312,500,000 satoshis. The fees in the same block were 3,762,561,499 satoshis, so the reward of 4,075,061,499 was 92.33 percent fees. In block 971,489 the fees were only 0.46 percent. The book's remark that the subsidy is much higher than fees is true of some blocks and not of others.",
      title="The block where fees were nearly the reward")

# ---------------------------------------------------------------------------------------------- part C
E.section("Replace, bump and relay", "From replacing a payment to paying for a parent: what a wallet can do when the fee was set too low.",
          [{"label": "Replace by fee"}, {"label": "Full RBF, a story"}, {"label": "When it goes wrong"}, {"label": "Child pays for parent"}],
          "This part covers what a sender or a receiver can do when a transaction pays too little and waits. The sender can replace it with a better-paying version, and the receiver can add a child that pays for both. The story shows how the default changed from opt-in to full replacement, and the hazards slide shows what that costs.")
KEEP["secC"] = "Replace, bump and relay"

BID = "Like raising your bid at an auction: it must beat the last bid by at least one step"
page("rbf", "A replacement must pay more than it replaces", BID,
     [chips(0.5, 1.27, 9.0, 0.4, ["514 refused", "564 refused", "578 refused", "579 accepted"], fs=10.5),
      con("RbfRules", 0.5, 2.05, 9.0, 1.95, "Recorded: Core 31.1 regtest, replacing a payment of 564 satoshis (141 vB)", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 1: a transaction signals replaceability when an input sequence is below 0xfffffffe",
                                  "Rows 2 and 3: 514 pays less than the 564 it replaces, and 564 pays nothing extra for the relay; both are refused",
                                  "Rows 4 and 5: the extra is 0.1 sat/vB x 141, 15 satoshis, so 579 passes and 578 fails"], fs=10)],
     "Replace by fee lets a sender swap a waiting transaction for another that spends the same output. The replacement must pay at least the absolute fee of what it replaces, plus the incremental relay fee for its own size. On the test node a replacement of 514 satoshis was refused for paying less, 564 for paying nothing extra, 578 by one satoshi, and 579 was accepted. A transaction signals replaceability when an input has a sequence below 0xfffffffe.",
     "A replacement pays more in total and pays for its own relay too")

story("fullrbf", "FullRbfPeering", "photo_bitcoin_namecoin_accepted_here_sign.png", "Stand-in picture: a shop sign, not a node.",
      ["On 12 December 2022 Peter Todd posts a build of Bitcoin Core 24.0.1 with Antoine Riard's full-rbf peering code",
       "Core 24.0.1 had added the option mempoolfullrbf, off by default; Core 28.0 made it the default and 29.0 removed it",
       "On the 31.1 test node a transaction with a final sequence was replaced (row 2), and the old option stops the node (row 3)"],
      "FullRbf", [0, 1, 2], "Recorded: Core 31.1 regtest",
      "On 12 December 2022 Peter Todd posted to the bitcoin-dev list a build of Bitcoin Core 24.0.1 with Antoine Riard's full-rbf peering code, while the new option mempoolfullrbf was still off by default. Bitcoin Core 28.0 later made full replacement the default, and 29.0 removed the option. The test node of this chapter replaced a transaction that never signalled, and refused to start with the old option. Policy is what most nodes choose to relay.")

page("hazard", "When replacement goes wrong", "Three versions paid twice; a large child made a replacement 639 times dearer",
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Version 0", "sub": "spends A"}, {"label": "Version 1", "sub": "spends A and B"}, {"label": "Version 2", "sub": "spends B and C"},
                                  {"label": "Payee receives", "sub": "0.8 BTC for 0.4 BTC", "hot": True}], fs=10.5),
      con("Hazards", 0.5, 2.2, 9.0, 1.88, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 4.33, 9.0, 0.4, ["Rows 2 and 3: a miner kept version 0, then mined version 2, so the payee was paid twice",
                                  "Rows 4 and 5: a 90,012-byte child pins a 705-satoshi parent; replacing it costs 639 times its fee"], fs=9.5),
      foot(0.5, 4.77, 9.0, 0.24, "NOT EXECUTED: replacement cycling needs several peers; row 6 found its text in the saved Optech page.", fs=10)],
     "Three versions of one payment of 0.4 bitcoin conflict in a chain: version 1 replaces version 0, and version 2 conflicts with version 1 but not with version 0. A miner that kept version 0 mined it and then version 2, so the payee received 0.8 bitcoin. A large child also pins a parent: replacing a 705-satoshi parent cost 450,780 satoshis. The replacement cycling attack of 2023 is described in the sources but was not run.",
     "Replacement is a hazard as well as a tool, and here it was measured")

FRIEND = "Like a friend who pays your fare with his own: the driver takes the pair that pays enough"
page("cpfp", "Child pays for parent, and packages", FRIEND,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Parent", "sub": "pays 141 satoshis"}, {"label": "Child", "sub": "pays 14,100"}, {"label": "Package", "sub": "50.77 sat/vB", "hot": True}]),
      con("Cpfp", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest, a block with room for two of three transactions", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: parent and child were mined together; the pair pays 50.77 sat/vB, ahead of an unrelated transaction at 20",
                                  "Row 4: a child at 5 sat/vB makes the pair 3.02, so the unrelated transaction was mined alone",
                                  "Row 5: a parent of 8 satoshis is refused alone, its child too, and together they succeed"], fs=10)],
     "A receiver can pay for a stuck parent by spending its output in a child with a high fee, because miners rank a transaction together with its unconfirmed ancestors. In the run a parent paying 141 satoshis and a child paying 14,100 formed a package at 50.77 satoshis per virtual byte, and the node mined the pair before an unrelated transaction at 20. A child at 5 satoshis per virtual byte did not help. The submitpackage call took a parent of 8 satoshis with its child.",
     "A child can pay for its parent when the pair's fee rate is high enough")

# ---------------------------------------------------------------------------------------------- part D
E.section("Pinning, anchors, clusters, sniping", "How a child can pin a parent, and what version 3, anchors and clusters changed.",
          [{"label": "Pinning and version 3"}, {"label": "Anchors"}, {"label": "Cluster mempool"}, {"label": "Sniping and incentives"}],
          "This part is about the attacks and fixes that came after the book's model of fees. A large child can pin a parent, and version 3 transactions, anchor outputs and the cluster mempool of Core 31.0 are the answers. The last slides turn to fee sniping and to the question of what happens when the subsidy is gone.")
KEEP["secD"] = "Pinning, anchors, clusters, sniping"

LORRY = "Like a lorry parked behind your car: moving it costs more the bigger it is"
page("pin", "A large child can pin a parent", LORRY,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: an unrestricted child of 90,012 bytes made the replacement of its parent cost 450,780 satoshis",
                                   "Row 3: with version 3 the child is at most 1,000 vB (885 here), and the same replacement cost 5,145: 88 times less",
                                   "Row 4: a version-3 child of 1,350 vB is refused as a TRUC violation"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Recorded: satoshis to replace a pinned parent", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["child of 90,012 vB", "child of 885 vB, version 3"], "series": [{"name": "satoshis", "data": [OUT("Truc", 1)[1], OUT("Truc", 2)[1]]}]},
      con("Truc", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest", fs=10, rows=rows_of("Truc", [0, 1, 2, 4]))],
     "A counterparty can attach a very large child of modest fee rate to a payment, and then a replacement has to pay for the child too. In the run a child of 90,012 virtual bytes raised the price of replacing the parent to 450,780 satoshis. Version 3, the TRUC policy of Bitcoin Core 28.0, caps the child at 1,000 virtual bytes, and the same replacement cost 5,145 satoshis, 88 times less. A version-3 child of 1,350 bytes was refused.",
     "Version 3 caps the child, so replacing a pinned parent cost 88 times less")

SPARE = "Like a spare handle on a door: anyone can grab it, so whoever needs it can add the fee"
page("anchor", "Anchors: a fee added afterwards", SPARE,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Parent", "sub": "version 3, fee 0, anchor output"}, {"label": "Child", "sub": "spends the anchor, pays 10,000"}, {"label": "Package", "sub": "36.5 sat/vB", "hot": True}], fs=10.5),
      con("Anchors", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest, submitpackage", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: the anchor output is the script 51024e73 with value 0; the zero-fee parent is refused alone, 0 < 13",
                                  "Rows 4 and 5: the child spends the anchor with an empty witness, so anyone could, and pays 10,000 satoshis",
                                  "Row 6: submitted together, the package paid 36.5 sat/vB and was accepted"], fs=10)],
     "A pay-to-anchor output is a tiny output that anyone can spend, so whoever needs a transaction confirmed can attach a child and pay the fee then. In the run a version-3 parent paying nothing was refused alone with min relay fee not met, and accepted with its child through submitpackage at 36.5 satoshis per virtual byte. The child spent the anchor with an empty witness stack. Lightning commitment transactions use such anchors.",
     "An anchor lets whoever needs it add the fee after the transaction is signed")

story("carve", "CarveOutProposal", "photo_lightning_network_logo.png", "Stand-in picture: the Lightning logo, not the proposal.",
      ["On 29 November 2018 Matt Corallo writes that pre-signed Lightning transactions cannot guess next week's fee",
       "His carve-out lets one extra small child past the limits: he proposed 1K, Core 0.19.0.1 shipped 10,000 vB (row 1)",
       "The book says 1,000 (row 2); Core 31.0 removed the carve-out (slide 21); NOT EXECUTED on an older node"],
      "CarveOut", [0, 1, 2], "executed on the saved sources; NOT EXECUTED: an older node",
      "On 29 November 2018 Matt Corallo wrote that Lightning channels exchange pre-signed transactions that are broadcast much later, so their fee must be predicted or added afterwards by a child. His answer, the carve-out, allowed one extra small child beyond the usual limits: he proposed 1K, and Bitcoin Core 0.19.0.1 shipped 10,000 virtual bytes where the book says 1,000. The removal in Core 31.0 was found in the saved notes and not run on an older node.",
      title="Pre-signed transactions cannot guess fees")

page("cluster", "Cluster mempool replaces the old limits", "Release 31.0 groups connected transactions in clusters and drops the limits of 25",
     [chips(0.5, 1.27, 9.0, 0.38, ["64 per cluster", "101,000 vB per cluster", "625 updates at 25"], fs=9.5),
      con("Cluster", 0.5, 2.15, 9.0, 1.98, "Recorded: Core 31.1 regtest, and the saved release notes", fs=10),
      beats(0.5, 4.38, 9.0, 0.6, ["Rows 2 and 3: a cluster holds at most 64 transactions; a chain of 65 was accepted to 64, then refused",
                                  "Rows 4 to 6: the 26th is accepted; 25 x 25 is 625 updates, 50 x 50 is 2,500; 300 MB for 336 hours; carve-out gone"], fs=10)],
     "The old limits of 25 ancestors or descendants existed because updating them was quadratic: 25 children of 25 ancestors need 625 package updates, and doubling the limit makes 2,500. Release 31.0 replaces them with clusters of at most 64 transactions and 101,000 virtual bytes, and the carve-out is removed. The test node accepted a chain of 64 and refused the 65th. The mempool keeps 300 megabytes and forgets a transaction after 336 hours, 14 days, not one day.",
     "Cluster limits replaced the 25-transaction limits and removed the carve-out")

LEDGER = "Like a thief who rewrites the last page of a ledger to keep the best-paying lines"
page("sniping", "Fee sniping and the lock time", LEDGER,
     [beats(0.5, 1.38, 4.6, 1.75, ["Rows 1 and 2: the wallet put the tip's height in 56 of 60 lock times; four were back-dated by 6, 28, 35 and 54 blocks",
                                   "Row 3: a lock time equal to the next block's height is not final; the node says non-final",
                                   "Row 4: a miner with share x wins with probability (x / (1 - x)) squared",
                                   "NOT EXECUTED: BIP 326 would use the sequence, not the lock time"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Chance to win the re-mining race, in percent", "dataLabels": True, "dlFmt": "0.##", "dlFs": 9,
       "labels": ["10 % of hash rate", "30 %", "45 %"], "series": [{"name": "percent", "data": OUT("Sniping", 3)}]},
      con("Sniping", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest, and a formula", fs=10, rows=rows_of("Sniping", [0, 1, 2, 3]))],
     "A miner who could re-mine the last block and take its fees might tempt others to build on the older block. A wallet defends by setting the lock time to the current height, so that such a transaction cannot be placed in an older block; in the run 56 of 60 transactions had the tip and four were back-dated. A transaction is final in a block when its lock time is below the height, which the book's chapter 6 gets off by one. BIP 326 for taproot was not executed.",
     "A lock time at the tip makes re-mining the last block pay less")

story("instab", "InstabilityPaper", "photo_nassau_hall_princeton.png", None,
      ["On 21 October 2016 Arvind Narayanan announces the Princeton paper written with Carlsten, Kalodner and Weinberg",
       "Their model: when fees are the main income a miner gains by undercutting a rival's block, so mining is less stable",
       "NOT EXECUTED: the model; the passages are found in the saved copies (rows 1 and 2); a 45 percent miner wins 66.94 percent (row 3)"],
      "Instability", [0, 1, 2], "executed on the saved papers and a formula; NOT EXECUTED: the model",
      "On 21 October 2016 Arvind Narayanan announced a Princeton paper, written with Miles Carlsten, Harry Kalodner and Matt Weinberg, on the instability of Bitcoin without the block reward. Satoshi Nakamoto's paper had already said that fees can replace the subsidy. The authors show that when fees are the main income a miner can gain by undercutting a rival's block. The model was not recomputed here; the passages were found in the saved copies.")

# ---------------------------------------------------------------------------------------------- summary, resources, closing
page("summary", "The chapter in five lines", "One line per part, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "A fee is the difference between inputs and outputs, signed by the spender and priced in virtual bytes",
         "Nodes relay from 0.1 sat/vB and wallets from 1; the estimator needs history, and the market moves from block to block",
         "A replacement must pay more in total and for its own relay, and since Core 28.0 it need not signal",
         "A child can pay for a parent; version 3, anchors and package submission make that safe, and clusters replace the old limits",
         "A fee-only future needs stable fee rules, and the wallet's lock time answers fee sniping"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["Optech topic, replace by fee", "https://bitcoinops.org/en/topics/replace-by-fee/"],
             ["Mastering Bitcoin, the book", "https://aantonop.com/books/mastering-bitcoin/"],
             ["mempool.space, the explorer", "https://mempool.space/"]]},
         {"head": "Standards and papers", "rows": [
             ["BIP 125, opt-in replace by fee", "https://bips.dev/125/"],
             ["BIP 431, version 3 (TRUC)", "https://bips.dev/431/"],
             ["Nakamoto, the Bitcoin paper", "https://bitcoin.org/bitcoin.pdf"]]},
         {"head": "Watch", "rows": [
             ["Antonopoulos on fees (video)", "https://www.youtube.com/embed/MPQMCVVhExY"],
             ["MIT OCW 15.S12 course", "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/"]]},
         {"head": "Community", "rows": [
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"],
             ["The bitcoin-dev group", "https://groups.google.com/g/bitcoindev"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the Antonopoulos video on fees, then the Optech topic on replace by fee next to the chapter. The research package for chapter 9 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the fees video, then read the Optech topic beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "Why a fee is a difference, and how it is priced in virtual bytes",
            "What a replacement must pay, and what a child can pay for",
            "What version 3, anchors and clusters changed for pinning",
            "How the wallet answers fee sniping, and why fees must replace the subsidy"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 9 holds the sources and the test records behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
LK.patch(E.S, 9)   # v1.1.0: every resources row names its resource, goes straight to it and says what the reader finds there
E.agenda(["The chapter's questions", "Fee, size and fee rate: the price of space", "Estimating fees and the market today", "Replace, bump and relay: RBF and CPFP", "Pinning, anchors, clusters and sniping"],
         "The route has four parts after the questions: what a fee is and how it is priced, estimating fees and reading the market, replacing and bumping a transaction, and finally pinning, anchors, clusters and sniping. Each part carries a true story or a correction of the book that a reader can check on the slide. The numbers in the list let a reader jump straight to a part.",
         "Four parts, four true stories, and a list of what was not run")
E.finish("Chapter 9: Transaction Fees", "1.1.0", "2026-10-15, first deck from the committed research package (commit 2521ab3), to the CME look and feel; notes are short reader's prose; v1.1.0: every READ card and resources link names its resource and goes straight to it (link_register_v1_0_0.json)")

planp = os.path.join(HERE, "deck_plan_v1_1_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1", REC],
    "recorded": [1, num["diff"], num["size"], num["floor"], num["estimator"], num["rbf"], num["fullrbf"], num["hazard"], num["cpfp"], num["pin"], num["anchor"], num["cluster"], num["sniping"]],
    "notExecuted": [num["hazard"], num["carve"], num["sniping"], num["instab"]],
    "standin": {str(num["halving"]): ["Stand-in picture"], str(num["fullrbf"]): ["Stand-in picture"], str(num["carve"]): ["Stand-in picture"]},
    "vectors": [num["size"], num["census"], num["halving"], num["carve"], num["hazard"], num["cluster"], num["instab"]],
}
plan["meta"]["analogies"] = [
    {"concept": "transaction fee", "analogy": CHANGE, "slide": num["diff"]},
    {"concept": "virtual size", "analogy": POST, "slide": num["size"]},
    {"concept": "fee market", "analogy": BUS, "slide": num["secB"]},
    {"concept": "replace by fee", "analogy": BID, "slide": num["rbf"]},
    {"concept": "child pays for parent", "analogy": FRIEND, "slide": num["cpfp"]},
    {"concept": "transaction pinning", "analogy": LORRY, "slide": num["pin"]},
    {"concept": "anchor output", "analogy": SPARE, "slide": num["anchor"]},
    {"concept": "fee sniping", "analogy": LEDGER, "slide": num["sniping"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
