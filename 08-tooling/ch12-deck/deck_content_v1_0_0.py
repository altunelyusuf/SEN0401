#!/usr/bin/env python3
"""Chapter 12 (Mining and Consensus) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_0_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the records of Bitcoin Core 31.1 on regtest are on slides that say Recorded;
what the research marks NOT EXECUTED carries that label; the pictures that show a topic and not the event are labelled stand-in. Speaker notes are short reader's prose
(2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, datetime, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E

E.init(12, HERE, assets=("photo_adam_back.png", "photo_fork_in_the_road.png", "photo_asic_miner.png", "photo_taproot_profile.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS)
assert (NPUB, NFIND, NCLAIM) == (91, 27, 69), (NPUB, NFIND, NCLAIM)
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
E.slide("title", "Chapter 12: Mining and Consensus", "How new coins are made, how every node checks a block, why proof of work is a lottery, and how the rules change. Bitcoin Core 31.1 results are Recorded.", [],
        "This deck explains mining and consensus: the reward and its halving, the checklists that every node runs on a block, the nonce lottery of proof of work and its retargeting, the pools and attacks that follow, and the soft forks that change the rules. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1 was run on a test network, so its answers are Recorded and only read back here. The research package for chapter 12 holds the sources and the claims.")

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
E.section("Rewards, rules and the block", "Where new coins come from, who may claim them, and the rules a block must pass.",
          [{"label": "Halving and supply"}, {"label": "Subsidy plus fees"}, {"label": "Node checklists"}, {"label": "Most work wins"}, {"label": "The coinbase"}],
          "This part is about money and rules. It starts with the subsidy that halves every 210,000 blocks and the fees that are added to it, then follows the checklists that every node runs on a transaction and a block, the rule that the chain with the most work wins, and the special first transaction of a block, the coinbase. The story of the part is the block in which fees beat the subsidy twelve times.")
KEEP["secA"] = "Rewards, rules and the block"

WELL = "Like a spring that gives half as much each season, until the last drop around 2140"
page("supply", "Halving and the 21 million limit", WELL,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: blocks 210,000, 420,000, 630,000 and 840,000 (2012 to 2024) pay 25, 12.5, 6.25 and 3.125 coins",
                                   "Row 3: the 33 rewards add up to 2,099,999,997,690,000 satoshis, 2,310,000 short of 21 million; the last satoshi is in block 6,929,999",
                                   "Row 4: the book's max_money.py divides with /=, so Python 3 prints 2100000000000000.0 and not the figure of its text"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Subsidy in coins, by halving block", "dataLabels": True, "dlFmt": "0.###", "dlFs": 9,
       "labels": ["210,000", "420,000", "630,000", "840,000"], "series": [{"name": "coins", "data": [float(r[2]) for r in OUT("Supply", 1)]}]},
      con("Supply", 0.5, 3.42, 9.0, 1.38, "executed on four real blocks saved from mempool.space, and on the book's script as printed", fs=10)],
     "The subsidy is 50 coins shifted right by one bit for every 210,000 blocks, and four real blocks show it: 25, 12.5, 6.25 and 3.125 coins. Summed in whole satoshis the 33 non-zero rewards stop 2,310,000 satoshis short of 21 million coins, and the last reward of one satoshi is in block 6,929,999, about the year 2140. The book's script has an error: its float division makes Python 3 print 2100000000000000.0 and not the figure of the text.",
     "The reward halves every 210,000 blocks, so supply stops just below 21 million")

TIPS = "Like a driver's wage plus tips: in one block the tips were twelve times the wage"
page("reward", "A block's reward is subsidy plus fees", TIPS,
     [chips(0.5, 1.27, 9.0, 0.38, ["subsidy + fees", "tips 12.04x the wage", "may claim less"], fs=9.5),
      con("Reward", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; block 840,000 is saved from mempool.space", fs=9.5),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: the template pays 345,369 satoshis, the subsidy plus 40,194 of fees, as the book says",
                                  "Row 3: block 840,000, by ViaBTC, paid 3,762,561,499 satoshis of fees, 12.04 times the subsidy of 312,500,000",
                                  "Rows 4 and 5: a block that claims 1 satoshi less is accepted; one that claims 1 satoshi more is refused"], fs=10)],
     "A block may claim at most the subsidy plus the fees of its transactions. The test node's template paid 345,369 satoshis, made of the subsidy and 40,194 of fees; a block that claimed one satoshi less was accepted and one that claimed one satoshi more was refused as bad-cb-amount. In block 840,000 the fees were 12.04 times the subsidy, which makes the book's remark that fees are usually a small percentage of income a description of its time and not a law.",
     "Reward is subsidy plus fees, and fees can be 12 times the subsidy")

story("halving", "HalvingBlockWithRecordFees", "photo_asic_miner.png", "Stand-in picture: a miner of the kind, not the one.",
      ["On 20 April 2024 ViaBTC mines block 840,000, the first to pay 3.125 coins, with 3,050 transactions (row 2)",
       "Its fees were 3,762,561,499 satoshis, 12.04 times the subsidy, so the book's small percentage fails here (rows 2, 3)",
       "The reward was 4,075,061,499 satoshis, mostly tips; the pool tag in the coinbase is how statistics are made"],
      "HalvingStory", [0, 1, 2], "executed on block 840,000 saved from mempool.space",
      "Block 840,000 was mined by ViaBTC at 00:09:27 UTC on 20 April 2024 and was the first to pay the new subsidy of 3.125 coins. Its 3,050 transactions paid 3,762,561,499 satoshis in fees, 12.04 times the subsidy, so the reward of 4,075,061,499 satoshis was made mostly of tips. The coinbase carries the tag /ViaBTC/, which is how the statistics of pools are made. The book says that fees are usually a small percentage of income, and this block is an exception.",
      title="The block where tips beat the wage 12 times")

DOOR = "Like a doorman with a checklist: one wrong item and the guest stays outside"
page("checks", "Node checklists for transactions and blocks", DOOR,
     [con("Checks", 0.5, 1.7, 9.0, 1.95, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.95, 9.0, 0.75, ["Row 2: 14 transaction cases and 14 block cases each ended in a named reason; a coinbase at depth 100 is allowed",
                                   "Row 3: a repeated input, a negative output and a coinbase spent at depth 99 are refused, by name",
                                   "Rows 4 and 5: a block is refused for a reward too high, no height, a wrong merkle root, an early time or a version 1"], fs=10)],
     "Consensus is a set of checks, and each one has a name. On a Bitcoin Core 31.1 test node, fourteen transaction cases and fourteen block cases each produced one reason: a repeated input, a negative output, a coinbase spent before 100 blocks, a reward one satoshi too high, no height in the coinbase, a wrong merkle root, a time not above the median or two hours ahead, and a version 1. The one valid block was accepted.",
     "Every rule has a name, and a node reports the first one a block breaks")

COURT = "Like a court that follows the heaviest file of evidence, not the longest"
page("chainsel", "The best chain has the most work", COURT,
     [con("ChainSel", 0.5, 1.7, 9.0, 1.7, "Recorded: Core 31.1 regtest, two nodes", fs=10),
      beats(0.5, 3.75, 9.0, 0.68, ["Row 2: the branch with chainwork 208 beat the one with 206 and became the tip of both nodes",
                                   "Row 3: a payment of 49.999 coins with 1 confirmation fell to -2 confirmations; the receiver then held 0.0",
                                   "Row 4: the payment came back with 2 confirmations, and the losing branch stays as a valid fork"], fs=10),
      foot(0.5, 4.55, 9.0, 0.3, "NOT EXECUTED: block relay over the peer-to-peer network; the test blocks were handed to the nodes by RPC.", fs=10)],
     "A node follows the chain with the most cumulative proof of work, which is not always the longest. On two test nodes a branch with chainwork 208 replaced one with 206, and a payment of 49.999 coins that had one confirmation went to minus two, so the receiver held nothing until the payment was mined again. The losing branch stays on record as a valid fork. The blocks were handed over by RPC and not relayed over the network.",
     "The chain with the most work wins, and a payment can fall back to zero")

CASH = "Like a cashier's first receipt of the day: it creates the money that the rest only move"
page("coinbase", "Coinbase fields and reserved weight", CASH,
     [con("Coinbase", 0.5, 1.7, 9.0, 1.7, "Recorded: Core 31.1 regtest; block 840,000 is saved from mempool.space", fs=10),
      beats(0.5, 3.75, 9.0, 0.68, ["Row 2: Core reserves 8,000 of 4,000,000 weight; block 840,000 weighed 3,993,281, so other software made it",
                                  "Row 3: the script begins with the height as a pushed number: 029c08 for block 2,204, the BIP 34 rule",
                                  "Row 4: Core's coinbase has locktime height - 1, sequence 0xfffffffe and ends in OP_0; the book omits these"], fs=10),
      foot(0.5, 4.55, 9.0, 0.3, "NOT EXECUTED: Bitcoin Core's IPC mining interface; the template came from the getblocktemplate RPC.", fs=10)],
     "The first transaction of a block, the coinbase, has no real input. Since BIP 34 its script begins with the height, so block 2,204 starts with 029c08, and the coinbase of Bitcoin Core 31.1 also sets its locktime to the height minus one, its sequence to 0xfffffffe and ends the script with OP_0, none of which is in the book's table. Core now reserves 8,000 weight units for it, so its blocks stay below 3,992,000, and block 840,000 with 3,993,281 came from other software.",
     "The coinbase begins with the height; Core reserves 8,000 weight units for it")

# ---------------------------------------------------------------------------------------------- part B
E.section("Proof of work", "A lottery whose odds the network sets, and a thermostat that keeps it fair.",
          [{"label": "The nonce lottery"}, {"label": "Difficulty and hash rate"}, {"label": "Retargeting"}, {"label": "Hashcash"}],
          "This part explains proof of work. It starts with a toy lottery in which a counter is hashed until the result is small enough, then asks how small the target must be and how much work that means in days. It ends with the rule that sets the target every 2,016 blocks, and with the story of Adam Back's Hashcash, from which the idea comes.")
KEEP["secB"] = "Proof of work"

DICE = "Like throwing dice until a throw is low enough: hard to find, easy for anyone to check"
page("lottery", "Proof of work is a nonce lottery", DICE,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: the book's phrase with a counter first gives a hash starting with 0 at 32: 09cb91f8, with a lowercase w",
                                   "Row 2: with the capital W the book prints, the hash is 6bbe6a3d, so the printed spelling is wrong",
                                   "Rows 3 and 4: two zero digits take 228 tries, three take 3,460; block 277,316 has 63 leading zero bits",
                                   "NOT EXECUTED: mining on the public network or with ASICs"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Tries to find a hash with leading zero digits", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["1 zero digit", "2 zero digits", "3 zero digits"], "series": [{"name": "tries", "data": [OUT("Lottery", 1)[0]] + list(OUT("Lottery", 2))}]},
      con("Lottery", 0.5, 3.42, 9.0, 1.38, "executed on the saved header of block 277,316; the search runs here on one CPU", fs=10)],
     "Proof of work is a lottery in which anyone can check a winning ticket at once. In the book's toy version the phrase Hello, world with a counter first gives a hash that starts with a zero at 32; two zeros took 228 tries and three took 3,460. The book prints the phrase with a capital W, and that spelling gives a different hash, 6bbe6a3d; only the lowercase one gives 09cb91f8. Nothing was mined on a public network.",
     "A hash below the target is a winning ticket that anyone can check")

LOTTO = "Like a lottery that adds balls until a win still takes ten minutes"
page("difficulty", "Difficulty, hash rate and a 1 TH/s miner", LOTTO,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Difficulty", "sub": "of block 277,316"}, {"label": "x 2^32 hashes", "sub": "per block, on average"}, {"label": "/ 10^12 per second", "sub": "a 1 TH/s miner"}, {"label": "58.7 days", "sub": "8,453 blocks", "hot": True}], fs=10.5),
      con("Difficulty", 0.5, 2.22, 9.0, 1.5, "executed on the saved header, adjustments and hash rate from mempool.space", fs=10),
      beats(0.5, 4.05, 9.0, 0.68, ["Row 2: a 1 TH/s miner needs 58.7 days or 8,453 blocks at that difficulty; the book says 8,496 blocks and 59 days",
                                  "Row 4: the last difficulty implies 9.500e+20 hashes a second; mempool.space reports 1.029e+21",
                                  "Row 4: that is 121,738 times the hash rate of the book's example block"], fs=10)],
     "Difficulty tells how many hashes a block takes on average: difficulty times 2 to the 32. At the difficulty of block 277,316, 1,180,923,195, a miner doing a trillion hashes a second needs 58.7 days, which is 8,453 blocks; the book says 8,496 blocks, an error of about half a percent. Today's hash rate, from the last adjustment and from mempool.space, is about 10 to the 21 per second, 121,738 times that of the book's example.",
     "At 1 TH/s a block takes 8,453 blocks of waiting, not the book's 8,496")

THERMO = "Like a thermostat: blocks too fast and the target tightens, too slow and it loosens"
page("retarget", "Retargeting every 2,016 blocks", THERMO,
     [con("Retarget", 0.5, 1.7, 9.0, 1.7, "executed on three real headers saved from mempool.space", fs=10),
      beats(0.5, 3.75, 9.0, 0.68, ["Row 2: 2,016 blocks took 1,186,047 seconds; the formula turns bits 17034219 into 170331db, as on the real chain",
                                  "Row 3: the real next block has exactly those bits (True); the period ran 1.0199 times faster than two weeks",
                                  "Row 4: counting 2,015 gaps makes the aim 0.05 percent fast; a ten-fold swing is clamped to 4x or a quarter"], fs=10),
      foot(0.5, 4.55, 9.0, 0.3, "NOT EXECUTED: a real Core retarget; regtest never retargets, so the formula met real mainnet headers instead.", fs=10)],
     "Every 2,016 blocks the target is scaled by the time the period took against two weeks, and never by more than a factor of four either way. From the headers of blocks 838,656 and 840,671, which are 1,186,047 seconds apart, the formula computes the bits 170331db, and that is what block 840,672 really carries. Counting 2,015 gaps and not 2,016 makes the aim 0.05 percent faster than ten minutes. Regtest does not retarget, so no real Bitcoin Core retarget was run.",
     "The formula reproduces a real adjustment; a swing is clamped to four times")

REF = "Like timing a race from the first runner, not from whoever starts late"
page("bip94", "The BIP 94 branch and recent adjustments", REF,
     [chips(0.5, 1.27, 9.0, 0.38, ["enforce_BIP94", "absent from the book", "52 adjustments"], fs=9.5),
      con("Bip94", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the source and the adjustments are saved", fs=9.5),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 1: regtest keeps bits 207fffff at height 2,017 because fPowNoRetargeting is true there; on main it is false",
                                  "Rows 2 and 3: Core 31.1 has the branch if (params.enforce_BIP94): true on testnet4, false on main, absent from the book",
                                  "Row 5: 52 adjustments in two years, from 0.888 to 1.147 times; 20 of them eased the difficulty"], fs=10)],
     "The book's listing of the retarget function has no branch for testnet4, but Bitcoin Core 31.1 has one: when enforce_BIP94 is true, the new target is built from the bits of the first block of the period, which may not use the minimum-difficulty exception. It is true on testnet4 and false on the main chain. Regtest sets fPowNoRetargeting and keeps its bits forever. In the last two years there were 52 adjustments, from 0.888 to 1.147 times.",
     "Core has a BIP 94 branch that the book's retarget listing lacks")

story("hashcash", "HashcashBeforeBitcoin", "photo_adam_back.png", None,
      ["On 1 August 2002 Adam Back dates his paper on Hashcash: the sender hashes a string until the hash starts with enough zeros (row 1)",
       "Nakamoto's paper says Bitcoin needs a proof of work similar to Adam Back's Hashcash (row 2)",
       "The book's toy search, Hello, world! with a counter, finds its first zero at 32 (row 3)"],
      "HashStory", [0, 1, 2], "executed on saved sources and the book's toy search",
      "Proof of work did not start with Bitcoin. Cynthia Dwork and Moni Naor proposed in 1992 that a user should compute a moderately hard function to fight junk mail, and Adam Back proposed Hashcash in 1997 and described it in a paper dated 1 August 2002. Satoshi Nakamoto's paper says that Bitcoin needs a proof of work similar to Back's Hashcash, and the book's toy search is the same idea in small.",
      title="The stamp that made email cost something")

# ---------------------------------------------------------------------------------------------- part C
E.section("Competition and rule changes", "What miners do when the lottery gets harder, how attackers fare, and how the rules change.",
          [{"label": "Nonce space"}, {"label": "Pools"}, {"label": "Attacks"}, {"label": "Soft and hard forks"}, {"label": "Two true stories"}],
          "This part is about competition and change. When the 32-bit nonce is used up a miner changes other fields, miners join pools to smooth their luck, and a pool with enough power can attack. Rule changes then come as soft forks, which only tighten, or hard forks, which split. The two stories are the chain split of March 2013 and the activation of taproot.")
KEEP["secC"] = "Competition and rule changes"

LOCK = "Like a combination lock with four billion settings: you must change the lock itself"
page("nonce", "When the 32-bit nonce runs out", LOCK,
     [chips(0.5, 1.27, 9.0, 0.38, ["nonce: 2^32 values", "extra nonce: 2^96 values", "version rolling: 16 bits"], fs=9.5),
      con("NonceSpace", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the hash rate is saved from mempool.space", fs=9.5),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: the nonce holds 4,294,967,296 values, spent 2.40e+11 times a second; an extra nonce makes 7.923e+28",
                                  "Row 3: 16 free version bits give 65,536 times the nonces: 2^48 values, 281.5 trillion, the book's 281 TH/s",
                                  "Rows 4 and 5: a block with version 2000e000 was accepted; a new extra nonce changed the txid and the root"], fs=10)],
     "The nonce has only 4,294,967,296 values, and today's hash rate uses them up 240 billion times a second, so miners change something else. The extra nonce in the coinbase script changes the transaction id and the merkle root, which gives 2 to the 96 values. Version rolling lets miners also change 16 bits of the version, which gives 65,536 times as many nonces; on the test chain a block with a rolled version was accepted.",
     "A miner changes the extra nonce or the version bits when the nonce runs out")

SYND = "Like a lottery syndicate: small steady shares instead of a rare big win"
page("pools", "Mining pools: who finds the blocks", SYND,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: of 52,371 blocks in a year Foundry USA found 28.2 percent, AntPool 18.2, F2Pool 12.6, ViaBTC 9.7",
                                   "Row 3: four pools found 68.6 percent of the blocks, of 32 pools listed",
                                   "Row 4: at 0.01 percent of the hash rate a miner finds a block every 69 days; at 1 percent 1.44 a day",
                                   "NOT EXECUTED: a live pool and Stratum"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Share of one year's blocks, percent", "dataLabels": True, "dlFmt": "0.0", "dlFs": 9,
       "labels": [r[0] for r in OUT("Pools", 1)[1]], "series": [{"name": "percent", "data": [r[1] for r in OUT("Pools", 1)[1]]}]},
      con("Pools", 0.5, 3.42, 9.0, 1.38, "executed on a pool listing saved from mempool.space", fs=10)],
     "Mining by oneself is a lottery with long waits, so most miners join a pool that shares the reward by the shares of work each one sends. In the last year four pools found 68.6 percent of 52,371 blocks, with Foundry USA at 28.2 percent. The book's remark that a miner with 1 percent finds more than a block a day is right at 1.44, while one with 0.01 percent waits 69 days. No live pool or Stratum connection was made.",
     "Four pools found two thirds of the blocks; a small miner waits for months")

RACE = "Like a race: a runner who starts behind rarely catches up, and rarely is not never"
page("attacks", "How much power an attack needs", RACE,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 1: selfish mining pays above 1/3 of the power, or 1/4 if half the honest miners follow its blocks",
                                   "Row 2: from 6 blocks behind a 10 percent attacker catches up with chance 0.0002428, 30 percent 0.1321",
                                   "Row 4: the top pool has 0.2816 of the blocks: below 1/3 and above 1/4",
                                   "NOT EXECUTED: a 51 percent attack on a public chain"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Chance to catch up from 6 blocks behind", "dataLabels": True, "dlFmt": "0.####", "dlFs": 9,
       "labels": ["10 percent", "30 percent", "45 percent"], "series": [{"name": "chance", "data": list(OUT("Attacks", 1))}]},
      con("Attacks", 0.5, 3.42, 9.0, 1.38, "executed on the formula of Nakamoto's paper and a pool listing saved from mempool.space", fs=10)],
     "An attacker does not need 51 percent to do harm. Nakamoto's table gives a 10 percent attacker, six blocks behind, a chance of 0.0002428, and the chance grows fast with power: 0.1321 at 30 percent and 0.766 at 45 percent. The paper on selfish mining shows that a pool profits from hiding blocks above one third of the power, or one quarter if half of the honest miners follow its blocks, and the top pool holds 0.2816. No attack was run on a public chain.",
     "An attacker needs less than a majority; the top pool is below 1/3")

CLUB = "Like a club rule: a stricter rule keeps every member, a looser one splits the club"
page("forks", "Soft forks tighten, hard forks split", CLUB,
     [con("Forks", 0.5, 1.7, 9.0, 1.75, "Recorded: Core 31.1 regtest; the heights are read from the saved chainparams.cpp", fs=9.5),
      beats(0.5, 3.8, 9.0, 0.68, ["Row 2: a lax node accepted a block with no height; a strict node refused it and could not follow the lax chain",
                                   "Rows 3 and 4: BIP 9 on regtest: defined at 143, started at 144, locked in at 288, active at 432; 108 of 144 signal",
                                   "Row 5: in the code BIP 34 is now a height, 227931, and segwit's is 481824; the mainnet threshold is 1,916 of 2,016"], fs=10),
      foot(0.5, 4.6, 9.0, 0.28, "NOT EXECUTED: a real hard-fork client; only soft-fork behaviour ran on test nodes.", fs=10)],
     "A soft fork only tightens the rules, so old nodes still accept the new blocks; a hard fork loosens them and splits the chain. On two test nodes a lax node accepted a block with no height in its coinbase and a strict node refused it, and the strict node could not follow the lax chain. BIP 9 let miners signal in a window: with a period of 144 and a threshold of 108, the deployment went from defined to started, locked in and active. On the main chain the threshold is 1,916 of 2,016.",
     "A soft fork only tightens; BIP 9 lets miners signal, lock in and activate")

story("split", "ChainSplitOfMarch2013", "photo_fork_in_the_road.png", "Stand-in picture: a fork in a road, not the split.",
      ["On 11 March 2013 block 225,430 with 797 transactions was accepted by Bitcoin 0.8 and refused by older nodes (row 2)",
       "A Berkeley DB lock limit of older versions had become a rule by accident; two pools went back to 0.7 (BIP 50)",
       "The split lasted 24 blocks (row 2); a deliberate 80/20 hard fork would take 17.5 or 70 days a period (row 3)"],
      "SplitStory", [0, 1, 2], "executed on blocks saved from mempool.space",
      "On 11 March 2013 a block of 797 transactions, number 225,430, was accepted by nodes of Bitcoin 0.8 and rejected by some older ones. BIP 50, written by Gavin Andresen, explains that versions before 0.8 had too few Berkeley DB locks for a large but valid block, which had become a rule by accident. The pools of Slush and BTCGuild went back to 0.7 so that the old chain had the most work, and the split lasted 24 blocks, about six hours.",
      title="The day Bitcoin had two histories")

story("taproot", "TaprootThroughSpeedyTrial", "photo_taproot_profile.png", "Stand-in picture: a tree's taproot, not the soft fork.",
      ["Speedy Trial opened on 24 April 2021 and timed out on 11 August 2021; it needed 1,815 of 2,016 blocks, 90 percent (row 3)",
       "Block 709,632, mined by F2Pool on 14 November 2021, was the first under the new rules; its version is 0x20200004 (row 2)",
       "Bit 2 of that version signals taproot; Core 31.1 still has the parameters in chainparams.cpp"],
      "TapStory", [0, 1, 2], "executed on block 709,632 saved from mempool.space",
      "Taproot was activated by a variant of BIP 9 called Speedy Trial, which opened on 24 April 2021, timed out on 11 August 2021 and needed 1,815 of 2,016 blocks, 90 percent, instead of 1,916. It also set a minimum activation height of 709,632, so that nodes had time to upgrade. Block 709,632 was mined by F2Pool on 14 November 2021 with the version 0x20200004, in which bit 2 is the signal for taproot.",
      title="Taproot: a 90 percent vote on a clock")

# ---------------------------------------------------------------------------------------------- summary, resources, closing
page("summary", "The chapter in five lines", "One line per part, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "The subsidy halves every 210,000 blocks, fees are added, and a block that claims too much is refused",
         "Every block and transaction passes named checks, and the chain with the most work wins",
         "Proof of work is a nonce lottery; the target is reset every 2,016 blocks from real timestamps",
         "Pools smooth the luck, and an attacker's odds fall fast with each block behind",
         "Soft forks only tighten the rules and need signals; hard forks split the chain"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["Optech topic, soft fork activation", "https://bitcoinops.org/en/topics/soft-fork-activation/"],
             ["Optech topic, selfish mining", "https://bitcoinops.org/en/topics/selfish-mining/"],
             ["mempool.space, the block explorer", "https://mempool.space/"]]},
         {"head": "Standards and papers", "rows": [
             ["BIP 9, version bits with timeout and delay", "https://bips.dev/9/"],
             ["BIP 54, consensus cleanup", "https://bips.dev/54/"],
             ["Eyal and Sirer, Majority is not enough", "https://arxiv.org/abs/1311.0243"]]},
         {"head": "Watch", "rows": [
             ["3Blue1Brown: how does bitcoin actually work (video)", "https://www.youtube.com/embed/bBC-nXj3Ng4"],
             ["Khan Academy: Bitcoin, proof of work (video)", "https://www.youtube.com/embed/9V1bipPkCTU"]]},
         {"head": "Community", "rows": [
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"],
             ["The bitcoin-dev group", "https://groups.google.com/g/bitcoindev"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the 3Blue1Brown video on how bitcoin works, then the Optech topic on soft fork activation next to the chapter. The research package for chapter 12 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the proof-of-work video, then read the Optech topic beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "How the reward is made and why a block cannot claim more",
            "How nodes check a block and choose the chain with most work",
            "Why proof of work is a lottery and how its target is reset",
            "What pools, attacks and soft forks change"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 12 holds the sources and the test records behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
E.agenda(["The chapter's questions", "Rewards, rules and the block", "Proof of work", "Competition and rule changes"],
         "The route has three parts after the questions: rewards, rules and the block, with the subsidy, the checklists, the chain of most work and the coinbase; proof of work, with its lottery, difficulty and retargeting; and competition and rule changes, with pools, attacks and forks. Each part carries a true story or a correction of the book that a reader can check on the slide. The numbers in the list let a reader jump straight to a part.",
         "Three parts, four true stories, and a list of what was not run")
E.finish("Chapter 12: Mining and Consensus", "1.0.0", "2026-10-15, first deck from the committed research package (commit 615aa32, v1_0_1 files), to the CME look and feel; notes are short reader's prose")

planp = os.path.join(HERE, "deck_plan_v1_0_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1", REC],
    "recorded": [1, num["reward"], num["checks"], num["chainsel"], num["coinbase"], num["bip94"], num["nonce"], num["forks"]],
    "notExecuted": [num["chainsel"], num["coinbase"], num["lottery"], num["retarget"], num["pools"], num["attacks"], num["forks"]],
    "standin": {str(num["halving"]): ["Stand-in picture"], str(num["split"]): ["Stand-in picture"], str(num["taproot"]): ["Stand-in picture"]},
    "vectors": [num["supply"], num["reward"], num["halving"], num["coinbase"], num["lottery"], num["difficulty"], num["retarget"], num["bip94"], num["hashcash"],
                num["nonce"], num["pools"], num["attacks"], num["forks"], num["split"], num["taproot"]],
}
plan["meta"]["analogies"] = [
    {"concept": "halving", "analogy": WELL, "slide": num["supply"]},
    {"concept": "block reward", "analogy": TIPS, "slide": num["reward"]},
    {"concept": "consensus checks", "analogy": DOOR, "slide": num["checks"]},
    {"concept": "most work", "analogy": COURT, "slide": num["chainsel"]},
    {"concept": "coinbase", "analogy": CASH, "slide": num["coinbase"]},
    {"concept": "proof of work", "analogy": DICE, "slide": num["lottery"]},
    {"concept": "difficulty", "analogy": LOTTO, "slide": num["difficulty"]},
    {"concept": "retarget", "analogy": THERMO, "slide": num["retarget"]},
    {"concept": "BIP 94", "analogy": REF, "slide": num["bip94"]},
    {"concept": "extra nonce", "analogy": LOCK, "slide": num["nonce"]},
    {"concept": "mining pool", "analogy": SYND, "slide": num["pools"]},
    {"concept": "attack odds", "analogy": RACE, "slide": num["attacks"]},
    {"concept": "soft fork", "analogy": CLUB, "slide": num["forks"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
