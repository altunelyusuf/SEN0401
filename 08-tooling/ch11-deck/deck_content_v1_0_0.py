#!/usr/bin/env python3
"""Chapter 11 (The Blockchain) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_0_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the records of Bitcoin Core 31.1 on regtest are on slides that say Recorded;
what the research marks NOT EXECUTED carries that label; the pictures that show a topic and not the event are labelled stand-in. Speaker notes are short reader's prose
(2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, datetime, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E

E.init(11, HERE, assets=("photo_satoshi_bust_budapest.png", "photo_ralph_merkle.png", "photo_children_sandpit.png", "photo_signet_ring.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS)
assert (NPUB, NFIND, NCLAIM) == (73, 25, 73), (NPUB, NFIND, NCLAIM)
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
E.slide("title", "Chapter 11: The Blockchain", "What a block holds, how blocks are named and linked, how a merkle tree vouches for them, and the test chains. Bitcoin Core 31.1 results are Recorded.", [],
        "This deck explains the blockchain: the block and its 80-byte header, how a block is named and numbered, how blocks hold one another, how a merkle tree vouches for the transactions, and the test chains that practise all of it. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1 was run on a test network, so its answers are Recorded and only read back here. The research package for chapter 11 holds the sources and the claims.")

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
E.section("The block and the chain", "What a block holds, how it is named and numbered, and how blocks hold one another.",
          [{"label": "Block and header"}, {"label": "The genesis block"}, {"label": "Name, height, links"}, {"label": "Forks"}],
          "This part opens a block and looks at every field of its header. It then asks how a block is named, how it is numbered, and what links it to its parent, and it ends with the case of two children of one parent. The first block, with its newspaper headline, is the story of the part.")
KEEP["secA"] = "The block and the chain"

PARCEL = "Like a parcel: a label on top, a count of the items, then the items themselves"
page("container", "A block is a header and its transactions", PARCEL,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Size field", "sub": "4 bytes, file only"}, {"label": "Header", "sub": "80 bytes"}, {"label": "Counter", "sub": "1 to 9 bytes"}, {"label": "Transactions", "sub": "204 bytes in block 0", "hot": True}], fs=10.5),
      con("Container", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest; the genesis constants are saved from chainparams.cpp", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: the first block is 80 + 1 + 204 = 285 bytes; blocks 1 to 4 then hold 250, 472, 694 and 915 bytes",
                                  "Rows 3 and 4: the book's size field is a prefix Bitcoin Core writes in its block file, which it scrambles with a key",
                                  "Row 5: the counter takes 1, 3 or 5 bytes; at 60 bytes at least per transaction a block holds 16,666 at most"], fs=10)],
     "A block is an 80-byte header, a count of transactions, and the transactions. The first block of the test chain measured 285 bytes: 80 for the header, 1 for the count and 204 for its one transaction. The size field shown in the book's table is not part of the block but a prefix that Bitcoin Core writes in front of each block in its block files, which since release 28.0 are scrambled with a random key.",
     "A block is a header, a count and transactions; the size field is file storage")

page("header", "The 80-byte header and its six fields", "Fields are stored little-endian, and the version is now a set of flags",
     [chips(0.5, 1.27, 9.0, 0.38, ["80 bytes", "50,000 headers in a block", "version = flags"], fs=9.5),
      con("Header", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; blocks 277,315 and 840,000 are saved from mempool.space", fs=9.5),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: block 277,315 has an 80-byte header; its version 2 is stored as 02000000 and its previous hash reversed",
                                  "Row 4: block 840,000 has version 0x2a5fe000: the top three bits are 001 (BIP 9), the other bits are flags",
                                  "Row 5: the first block had version 1 and this one 2, so the book's name version number no longer fits"], fs=10)],
     "The header holds six fields in 80 bytes: version, previous block hash, merkle root, time, bits and nonce, with numbers stored least significant byte first and hashes shown reversed. A block may be 4,000,000 bytes, so it can be 50,000 times its header. The version is no longer a counter: BIP 9 sets the top three bits to 001 for blocks that signal, and the remaining bits are flags.",
     "Six fields fill 80 bytes, and the version is now a set of flags")

CLOCKS = "Like asking eleven clocks and trusting the middle one"
page("timetarget", "Time, target and nonce", CLOCKS,
     [con("TimeTarget", 0.5, 1.7, 9.0, 1.95, "Recorded: Core 31.1 regtest; block 277,315 is saved from mempool.space", fs=10),
      beats(0.5, 3.95, 9.0, 0.75, ["Row 2: time counts seconds from 1970 and runs out in 2106; a block may be at most 7,200 seconds ahead of the clock",
                                   "Row 3: the median of the last 11 times, 1792052132 by our code and the node, is the floor; block 277,315 is 1,651 s above",
                                   "Rows 4 and 5: bits 1d00ffff is difficulty 1; block 277,315 needed 1,180,941,215 full nonce ranges, hence the extra nonce"], fs=10)],
     "The timestamp of a block must be greater than the median of the previous 11 block times and at most two hours ahead of the node's clock. The target is stored compactly in bits: 1d00ffff means a target of 0xffff followed by zeros, which is difficulty 1. Block 277,315 had a difficulty of 1,180,923,195, so its proof of work needed far more than the 4,294,967,296 values of the 32-bit nonce, which is why miners also change an extra nonce.",
     "The median of 11 times is the floor; the nonce alone is too small")

story("genesis", "HeadlineInTheGenesisBlock", "photo_satoshi_bust_budapest.png", "Stand-in picture: a sculpture, not Satoshi's face.",
      ["On 3 January 2009 Satoshi Nakamoto mines the first block and quotes The Times in its coinbase (row 2)",
       "The Chancellor of the day was Alistair Darling; the block hashes to 000000000019d668 from its constants (row 1)",
       "Its 50 coins can never be spent: the node refuses the coinbase with error -5 (row 3)"],
      "Genesis", [0, 1, 2], "executed on the saved constants and the Core 31.1 record (Recorded)",
      "On 3 January 2009 Satoshi Nakamoto mined the first block and wrote into its coinbase a headline of The Times, 69 characters long, which shows that the block cannot be older than that day. The Chancellor of the Exchequer then was Alistair Darling. The chapter rebuilt the block from the constants in chainparams.cpp and hashed it to 000000000019d668, and a test node refused to give out its coinbase, because the first 50 coins can never be spent.",
      title="A headline nailed into the first block")

FING = "Like a fingerprint: taken from the block, never printed inside it"
page("identity", "A block's name is the hash of its header", FING,
     [con("Identity", 0.5, 1.7, 9.0, 2.1, "Recorded: Core 31.1 regtest; the header of block 0 is saved from mempool.space", fs=10),
      beats(0.5, 4.05, 9.0, 0.62, ["Row 2: SHA-256 run twice over the 80 header bytes gives 000000000019d668...; run once it gives 6dd6c571...",
                                   "Rows 3 and 4: the 285 bytes of the first block hold its hash neither way round; the next header holds it",
                                   "Row 6: blocks 0, 277,315 and 840,000 have 10, 15 and 19 leading zeros in hex: the proof of work"], fs=10)],
     "The identifier of a block is the double SHA-256 of its 80-byte header, shown byte-reversed. The hash is not stored in the block itself: the 285 bytes of the first block contain it neither way round, and it is the next block's header that carries it. The leading zeros grow with the difficulty, from 10 hex digits in block 0 to 19 in block 840,000.",
     "The name is computed from the header and carried by the next block")

CHEQUE = "Like a cheque you may not cash until the bank has held it for a hundred days"
page("height", "Height, depth and coinbase maturity", CHEQUE,
     [chips(0.5, 1.27, 9.0, 0.38, ["height 971,537 today", "BIP 34: height in the coinbase", "maturity 100"], fs=9.5),
      con("Height", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the height 971,537 is a public figure saved from mempool.space", fs=9.5),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: the chain stood at height 971,537 on the day of the census, 18.5 years of blocks; a new regtest has 0",
                                  "Row 3: since BIP 34 every coinbase starts with its own height as a script number; all heights decoded back",
                                  "Rows 4 and 5: a coinbase can be spent after 100 blocks; at depth 99 the node refuses it"], fs=10)],
     "Height counts the blocks since the first, which has height 0, and it is not a unique name, because two blocks can share a height during a fork. Since BIP 34 the height is written at the start of the coinbase script. A reward can be spent only 100 blocks later, and the test node refused a spend at depth 99 with premature-spend-of-coinbase.",
     "Height is a count, not a name; a reward matures after 100 blocks")

ICE = "Like layers in a glacier: disturb an old layer and every later one is disturbed"
page("links", "Back-links make the history hard to change", ICE,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Block 3 changed", "sub": "its hash changes", "hot": True}, {"label": "Block 4", "sub": "its link breaks"}, {"label": "Blocks 5 to 9", "sub": "all must be re-mined"}], fs=10.5),
      con("Links", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: in ten consecutive blocks, 9 of 9 previous-hash fields point to the hash of the block before",
                                  "Row 3: changing block 3 changes its own hash, breaks the link in block 4, and 7 blocks would have to be re-mined",
                                  "Row 4: on regtest each block adds work 2, so 501 blocks hold 1002; on the main chain it is far larger"], fs=10)],
     "Each header carries the hash of its parent, so the chain is a list in which every link depends on everything before it. On the test chain, ten consecutive headers linked correctly, and changing the fourth changed its hash, broke the link in the fifth, and meant that seven blocks would have to be mined again. The work of the chain is the sum of the work of its blocks, so the chain with the most work wins.",
     "Changing one old block means mining it and all later blocks again")

BRANCH = "Like two branches on one trunk: the tree grows on along the stronger one"
page("forks", "Forks: two children, one parent", BRANCH,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: two blocks were mined at height 511 on one parent: the same height, different children",
                                   "Row 3: a block built on one child makes it the active chain at 512; the other stays a valid fork",
                                   "Row 4: from 6 blocks behind, an attacker with 10 percent catches up with chance 0.0002428, one with 30 percent 0.1321"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Chance to catch up from 6 blocks behind", "dataLabels": True, "dlFmt": "0.####", "dlFs": 9,
       "labels": ["10 percent of the power", "30 percent"], "series": [{"name": "chance", "data": [OUT("Forks", 4)[0][3], OUT("Forks", 4)[1]]}]},
      con("Forks", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest, and the formula of the paper", fs=10, rows=rows_of("Forks", [0, 1, 3, 4]))],
     "Two miners can find a block at about the same time, and then one parent has two children at the same height. The test node held both and called the one with more work active and the other a valid fork, and a block on top of one child settled it. The chance that an attacker catches up falls quickly with the number of blocks: with 10 percent of the power it is 0.2045873 from one block behind and 0.0002428 from six.",
     "A fork is settled by more work, and an old block is soon safe")

# ---------------------------------------------------------------------------------------------- part B
E.section("Merkle trees", "How one 32-byte root vouches for every transaction in a block, and where the tree is weak.",
          [{"label": "Building the tree"}, {"label": "Proof by a short path"}, {"label": "Two weaknesses"}, {"label": "Ralph Merkle"}],
          "This part is about the hash tree that sits between a block's transactions and its header. It shows how the root is built, how a short path proves that one transaction belongs, and where the tree is weak: a duplicated hash and a 64-byte transaction. The story is that of its inventor, Ralph Merkle.")
KEEP["secB"] = "Merkle trees"

DRAW = "Like a knockout draw: pairs are matched until one name is left at the top"
page("tree", "The merkle tree: many transactions, one root", DRAW,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "4 transactions", "sub": "4 hashes"}, {"label": "2 pairs", "sub": "2 hashes"}, {"label": "1 root", "sub": "32 bytes, in the header", "hot": True}]),
      con("Tree", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: four transactions give levels of 4, 2 and 1 hashes, and hashing the two pairs gives the header's root",
                                  "Rows 3 and 4: three transactions give levels 3, 2 and 1: the last hash is paired with itself; the root is the header's",
                                  "Row 5: adding a copy of the last transaction gives the same root, so the odd one is simply duplicated"], fs=10)],
     "The transaction ids of a block are hashed in pairs, level by level, until one hash is left, and that merkle root goes into the header. For four transactions the levels have 4, 2 and 1 hashes, and the test node's root matched our own. When a level has an odd count, its last hash is paired with itself, which is why a copy of the last transaction gives the same root.",
     "Pairs are hashed upward; an odd hash is paired with itself")

LEDGER = "Like checking a ledger page against a signed total using only the subtotals beside it"
page("proof", "A merkle proof is a short path of hashes", LEDGER,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: to prove transaction 10 of 16 only 4 hashes are needed, 128 bytes, and they lead back to the root",
                                   "Row 3: a path grows with the logarithm: 320, 384 and 448 bytes for 1,024, 4,096 and 16,000 transactions",
                                   "Row 4: with the 80-byte header a proof is 528 bytes, so a full block is 7,576 times larger, not 10,000"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Bytes of proof path by transactions in a block", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["1,024 transactions", "4,096", "16,000"], "series": [{"name": "bytes", "data": [r[2] for r in OUT("Proof", 3)]}]},
      con("Proof", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest; the sizes follow from the depth", fs=10, rows=rows_of("Proof", [0, 1, 3, 4]))],
     "A light client can check that a transaction is in a block with only the hashes along its path to the root, one for each level. For transaction 10 of 16 that is 4 hashes, 128 bytes, and following them reproduced the root of the header. The path grows with the logarithm of the block, 448 bytes for 16,000 transactions, so with the header a proof is 528 bytes; the book's claim of almost 10,000 times smaller is really 7,576 times.",
     "A proof is a few hashes, and the book's ratio of 10,000 is 7,576")

page("flaws", "Two weaknesses of the merkle tree", "Like two different shopping lists that give the same receipt total",
     [chips(0.5, 1.27, 9.0, 0.38, ["CVE-2012-2459", "the last hash is repeated", "64-byte transactions"], fs=9.5),
      con("Flaws", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the BIP 54 passage is saved", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: six transactions and the same six with the last two repeated give one root: two blocks, one header",
                                  "Row 4: given the 4-transaction version of a 3-transaction block, the node refused it and kept the original",
                                  "Row 5: an inner node is the hash of 64 bytes; BIP 54 makes a 64-byte transaction invalid so none can pose as one"], fs=10)],
     "Because an odd hash is paired with itself, a list with the last transactions repeated has the same root as the original, so two different blocks can share one header. Bitcoin Core refuses the mutated block with bad-txns-duplicate, and on the test chain it kept the original. The second weakness is that an inner node is the hash of 64 bytes, so a transaction of exactly 64 bytes could be mistaken for one, which BIP 54 forbids.",
     "The tree has two known weaknesses, and the node defends against both")

story("merkle", "TheHashTreeOfRalphMerkle", "photo_ralph_merkle.png", None,
      ["On 5 January 1982 United States patent 4309569 is published: Ralph Merkle's hash tree, assigned to Stanford University (row 1)",
       "He had described tree authentication in 1980; Nakamoto's paper keeps only the root of such a tree in each header",
       "The 40 transactions of block 277,315 hash up to the root in its header (row 3)"],
      "MerkleStory", [0, 1, 2], "executed on saved sources and a real block saved from mempool.space",
      "Ralph Merkle patented the hash tree in 1979, and the United States patent 4309569 was published on 5 January 1982 with Stanford University as assignee. In 1980 he wrote about tree authentication, and Satoshi Nakamoto's paper hashes the transactions of a block in such a tree and keeps only the root in the header. The 40 transactions of block 277,315 hashed in pairs up six levels to the root in its header.",
      title="One small hash that vouches for a list")

# ---------------------------------------------------------------------------------------------- part C
E.section("Test blockchains", "Practice chains where coins cost nothing: testnet, signet and regtest, and their rules.",
          [{"label": "Several chains"}, {"label": "Testnet"}, {"label": "Signet"}],
          "This part is about the chains on which developers practise. They run the same code as the main chain but with different rules, prefixes and ports, and each solved a problem of the one before it. The stories are the flooding of testnet3 and the signature that a signet block must carry.")
KEEP["secC"] = "Test blockchains"

SIM = "Like a flight simulator, a training pitch and the match: same rules, different stakes"
page("chains", "Several chains, one code base", SIM,
     [chips(0.5, 1.27, 9.0, 0.38, ["5 chains", "ports 8333 to 48333", "regtest halves every 150 blocks"], fs=9.5),
      con("Chains", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the chain parameters are saved from chainparams.cpp", fs=10),
      beats(0.5, 4.3, 9.0, 0.45, ["Row 2: the five chains use ports 8333, 18333, 48333, 38333 and 18444, and assume 856, 245, 31, 24 and 0 GB",
                                  "Row 4: all test chains use the prefix 2 for script addresses, and tb1 or bcrt1 for bech32, not only m, n and tb1 as the book says"], fs=9.5),
      foot(0.5, 4.78, 9.0, 0.24, "NOT EXECUTED: raw TCP to mainnet, testnet and signet peers, and the mainnet download.", fs=10)],
     "The same program runs five chains, chosen by an option, each with its own data directory, port and address prefixes. The book's tip says that test addresses begin with m, n or tb1, but the test chains also use the prefix 2 for script addresses, and regtest uses bcrt1. Regtest halves its reward every 150 blocks, so 500 blocks earned 12,462.5 coins, as the book shows. No connection to a real network was made.",
     "One program runs five chains; the prefixes are more than the book lists")

page("testnet", "Testnet: flooded, then replaced", "Testnet3 is far past one block in ten minutes, and testnet4 follows BIP 94",
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: testnet3 is at height 5,189,394, 6.3 times the 825,696 of one block in ten minutes; Core assumes 245 GB for it, the book says 30",
                                   "Rows 3 and 4: testnet3, testnet4 and regtest allow minimum-difficulty blocks after 20 idle minutes; Core 31.1 warns that testnet3 will go",
                                   "NOT EXECUTED: syncing testnet3 or testnet4; the heights are public figures saved from mempool.space"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Assumed chain size in GB (chainparams.cpp)", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["mainnet", "testnet3", "testnet4", "signet"], "series": [{"name": "GB", "data": OUT("Chains", 1)[1][:4]}]},
      con("Testnet", 0.5, 3.42, 9.0, 1.38, "executed on the saved chain parameters and heights saved from mempool.space", fs=10)],
     "Testnet coins are worth nothing, so nothing stops a miner from flooding the chain. Testnet3 lets a block use minimum difficulty after twenty idle minutes, and its height is 6.3 times what one block in ten minutes would give; the book's size of 30 GB is far out of date too. Testnet4, specified in BIP 94, has its own genesis block and rules against the flooding. The heights are public figures; no test network was synchronised here.",
     "Testnet3 was flooded; testnet4 has rules against it")

story("grief", "GriefingTheTestnet", "photo_children_sandpit.png", "Stand-in picture: a sandpit, not the testnet.",
      ["On 4 May 2024 Jameson Lopp describes how the minimum-difficulty rule lets miners make hundreds of testnet3 blocks a day",
       "BIP 94, by Fabian Jahr, bounds the time of a period's first block; Core 28.0 adds testnet4 (row 4)",
       "BIP 94 says three years of blocks were mined in weeks (row 1); NOT EXECUTED: syncing testnet3"],
      "GriefStory", [0, 1, 2, 3], "executed on saved sources and heights saved from mempool.space",
      "On 4 May 2024 Jameson Lopp published how the minimum-difficulty rule of testnet3 lets miners create hundreds of blocks in a day. Testnet4 had its genesis block on 3 May 2024, and BIP 94, written by Fabian Jahr, bounds the time of the first block of a period; Bitcoin Core 28.0 added the network. BIP 94 notes that three years of blocks were mined on testnet3 in a few weeks, and testnet3 is now 33 times as long as testnet4.",
      title="When the sandbox was flooded")

DOOR = "Like a club with a doorman: only someone he knows may open the door"
page("signet", "Signet: blocks need a signature", DOOR,
     [chips(0.5, 1.27, 9.0, 0.38, ["challenge: 1 of 2 keys", "magic 0a03cf40", "challenge 51: anyone signs"], fs=9.5),
      con("Signet", 0.5, 2.12, 9.0, 1.75, "Recorded: Core 31.1 regtest; the signet height is a public figure saved from mempool.space", fs=10),
      beats(0.5, 4.1, 9.0, 0.62, ["Row 2: the default signet's challenge is 71 bytes, 1 of 2 keys must sign: either of the two operators can sign a block",
                                  "Row 3: the four magic bytes are the start of the hash of the challenge: 0a03cf40; the challenge 51 gives 54d26fbd",
                                  "Rows 4 and 5: both signets share one genesis; the default is at height 326,440, 2.27 times the book's 143,619"], fs=10),
      foot(0.5, 4.76, 9.0, 0.26, "NOT EXECUTED: mining a block on the public signet.", fs=10)],
     "On a signet a block is valid only if it carries a signature that satisfies a challenge script, so the operators decide who may make blocks and the chain stays calm. The default signet's challenge is a one-of-two multisig, which is why the book says two contributors run it; a signet with the challenge 51 can be signed by anyone and ran on the test node. The network magic is derived from the challenge, so every signet has its own.",
     "A signet block needs a signature, so the chain stays calm")

story("signetstory", "SignetBlocksNeedASignature", "photo_signet_ring.png", "Stand-in picture: a signet ring, not the BIP.",
      ["On 20 March 2019 BIP 325 is assigned to Karl-Johan Alm and Anthony Towns: a block needs a signature on a challenge (row 1)",
       "Bitcoin Core 0.21.0 adds signet; the magic is the hash of the challenge (row 2), so every custom signet has its own",
       "The public signet is at 2.27 times the book's 143,619 blocks (row 3); NOT EXECUTED: mining on it"],
      "SignetStory", [0, 1, 2], "executed on saved sources and the Core 31.1 record (Recorded)",
      "BIP 325, Signet, was assigned on 20 March 2019 to Karl-Johan Alm and Anthony Towns: a block is valid only if it carries a solution to a challenge script, so the creators of a signet decide who may make blocks. Bitcoin Core 0.21.0 added the support, and personal signets are possible with the option -signetchallenge. The network magic is the start of the hash of the challenge, so every signet has its own, and the public one is 2.27 times as long as the book's listing.",
      title="A test network with a doorman")

# ---------------------------------------------------------------------------------------------- summary, resources, closing
page("summary", "The chapter in five lines", "One line per part, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "A block is an 80-byte header, a count and transactions; the version field is now a set of flags",
         "A block's name is the double hash of its header, carried by the next block; a reward matures after 100 blocks",
         "Back-links make history costly to change, and the chain with the most work settles a fork",
         "A merkle root vouches for every transaction, a proof is a short path, and the tree has two known weaknesses",
         "Testnet3 was flooded and testnet4 followed; signet needs a signature; regtest is the practice bench"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["Optech topic, merkle tree vulnerabilities", "https://bitcoinops.org/en/topics/merkle-tree-vulnerabilities/"],
             ["Optech topic, signet", "https://bitcoinops.org/en/topics/signet/"],
             ["mempool.space, the block explorer", "https://mempool.space/"]]},
         {"head": "Standards and papers", "rows": [
             ["BIP 94, testnet4", "https://bips.dev/94/"],
             ["BIP 325, signet", "https://bips.dev/325/"],
             ["Nakamoto, the Bitcoin paper", "https://bitcoin.org/bitcoin.pdf"]]},
         {"head": "Watch", "rows": [
             ["Brownworth: Blockchain 101 (video)", "https://www.youtube.com/embed/_160oMzblY8"],
             ["Chainlink: what are Merkle trees (video)", "https://www.youtube.com/embed/na_omeubyYo"]]},
         {"head": "Community", "rows": [
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"],
             ["The bitcoin-dev group", "https://groups.google.com/g/bitcoindev"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the visual blockchain demo by Anders Brownworth, then the Optech topic on merkle tree vulnerabilities next to the chapter. The research package for chapter 11 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the visual demo, then read the Optech topic beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What a block and its header hold, and how a block is named",
            "How blocks are linked, and how a fork is settled",
            "How a merkle root and a short path vouch for a transaction",
            "Which test chain serves which purpose, and why"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 11 holds the sources and the test records behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
E.agenda(["The chapter's questions", "The block and the chain", "Merkle trees", "Test blockchains"],
         "The route has three parts after the questions: the block and the chain, with its header, name, links and forks; the merkle tree that vouches for the transactions; and the test blockchains on which developers practise. Each part carries a true story or a correction of the book that a reader can check on the slide. The numbers in the list let a reader jump straight to a part.",
         "Three parts, four true stories, and a list of what was not run")
E.finish("Chapter 11: The Blockchain", "1.0.0", "2026-10-15, first deck from the committed research package (commit 738662b, v1_0_1 files), to the CME look and feel; notes are short reader's prose")

planp = os.path.join(HERE, "deck_plan_v1_0_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1", REC],
    "recorded": [1, num["container"], num["header"], num["timetarget"], num["genesis"], num["identity"], num["height"], num["links"], num["forks"], num["tree"], num["proof"], num["flaws"], num["chains"], num["signet"], num["signetstory"]],
    "notExecuted": [num["chains"], num["testnet"], num["grief"], num["signet"], num["signetstory"]],
    "standin": {str(num["genesis"]): ["Stand-in picture"], str(num["grief"]): ["Stand-in picture"], str(num["signetstory"]): ["Stand-in picture"]},
    "vectors": [num["container"], num["header"], num["timetarget"], num["genesis"], num["identity"], num["height"], num["merkle"], num["chains"], num["testnet"], num["grief"], num["signet"]],
}
plan["meta"]["analogies"] = [
    {"concept": "block", "analogy": PARCEL, "slide": num["container"]},
    {"concept": "median time past", "analogy": CLOCKS, "slide": num["timetarget"]},
    {"concept": "block hash", "analogy": FING, "slide": num["identity"]},
    {"concept": "coinbase maturity", "analogy": CHEQUE, "slide": num["height"]},
    {"concept": "hash-linked chain", "analogy": ICE, "slide": num["links"]},
    {"concept": "fork", "analogy": BRANCH, "slide": num["forks"]},
    {"concept": "merkle tree", "analogy": DRAW, "slide": num["tree"]},
    {"concept": "merkle proof", "analogy": LEDGER, "slide": num["proof"]},
    {"concept": "test chains", "analogy": SIM, "slide": num["chains"]},
    {"concept": "signet", "analogy": DOOR, "slide": num["signet"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
