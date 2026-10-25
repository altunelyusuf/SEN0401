#!/usr/bin/env python3
"""SEN0401 chapter 12 research v1_1_0 builder (TK_Ch12_Research_Build_R24, criterion AC9_Ch12Research).
Reads the committed 03-materials/ch12/rdodi/sen0401_ch12_research_v1_0_1.ttl (never edited) and writes the NEW file sen0401_ch12_research_v1_1_0.ttl:
the 43 primary-source concepts C_01..C_43 (identical by label to the chapter 11 research) are replaced by the primary-source concepts of chapter 12
(Mining and Consensus), each with a label, a comment in a complete sentence and a citation (dcterms:source); publications, findings, stories-free parts
and the scorecard rows are kept, except the scorecard row of topic coverage, which stated the old count and origin (a wrong statement), and the version header.
Usage: python3 -B sen0401_ch12_research_concepts_v1_1_0.py [OUTFILE]"""
__version__ = "1.1.0"
import os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "03-materials", "ch12", "rdodi", "sen0401_ch12_research_v1_0_1.ttl")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "03-materials", "ch12", "rdodi", "sen0401_ch12_research_v1_1_0.ttl")

# (label, kind, [sources], comment). Labels are those the chapter 12 research taxonomy gives its leaf concepts (sen0401_ch12_rdodi_data_v1_0_1.LABELS);
# P01 is the chapter text, the other P-numbers are the saved sources the research paragraph of the concept cites.
C = [
 # --- money and rewards
 ("Halving every 210,000 blocks", ["P01", "P28", "P75"], "The reward a miner may claim in the first transaction of a block starts at 50 coins and is cut in half every 210,000 blocks, about every four years."),
 ("Total supply below 21 million", ["P01", "P28", "P59"], "Because the subsidy is a whole number of satoshis halved by a shift, the rewards of all blocks add up to 2,099,999,997,690,000 satoshis, just below 21 million coins."),
 ("The float erratum of the book's script", ["P09", "P01"], "The script max_money.py printed in the chapter divides with a slash, which is a float division in Python 3, so run as printed it does not give the total of the text."),
 ("Reward is subsidy plus fees", ["P01", "P28"], "The coinbase transaction of a block may create at most the subsidy plus the fees of all the other transactions of the block."),
 ("The fees of block 840,000", ["P01", "P74"], "Block 840,000 paid fees 12.04 times its subsidy, so the chapter's remark that fees are a small share of a miner's income describes its time of writing and not a law."),
 ("Coinbase fields of Bitcoin Core today", ["P34", "P20", "P01"], "Bitcoin Core 31.1 fills in the locktime, the sequence number and the script ending of the coinbase transaction in ways that the chapter's table does not show."),
 ("Coinbase data and tags", ["P01", "P74"], "The free data in the coinbase script is where pools sign their blocks, within the limit of 2 to 100 bytes."),
 ("BIP 34 height push", ["P12", "P01"], "BIP 34 makes every coinbase transaction unique by requiring the block height as the first item of the coinbase script."),
 # --- verifying and agreeing
 ("Most work, not longest", ["P01", "P28"], "When two valid chains compete, a node follows the one with the most cumulative proof of work, not the one with the most blocks."),
 # --- building the header and the extra nonce
 ("The nonce space is tiny", ["P01", "P72"], "The nonce of the block header is four bytes, so a miner has only 4,294,967,296 values to try before the header is used up."),
 ("The extra nonce space", ["P01"], "The extra nonce in the coinbase script adds eight bytes to the nonce and so gives a miner 2 to the 96 possible headers to try."),
 ("The extra nonce changes the root", ["P01", "P34"], "The coinbase is the first leaf of the merkle tree, so changing its extra nonce changes the merkle root and with it the hash of the whole header."),
 ("Version rolling", ["P19", "P01", "P25"], "Machine makers roll 16 bits of the version field, the mask 0x1fffe000 of BIP 320, to get 65,536 more headers for each coinbase."),
 ("Covert ASICBoost", ["P55", "P16", "P01"], "ASICBoost is a way of constructing the block header so that mining hardware does less work per hash."),
 # --- proof of work
 ("The Hello World nonce", ["P01", "P48", "P49"], "The chapter explains proof of work with a toy in which a counter is added to the phrase Hello, world! and the phrase is hashed until the result starts with a zero."),
 ("The wait of a terahash miner", ["P01", "P72"], "The chapter works out how long a miner doing one trillion hashes per second would wait for a block at the difficulty of block 277,316."),
 ("Hash rate from difficulty", ["P58", "P86", "P88"], "Nobody measures the hash rate of the network directly, so it is estimated from the difficulty, because a block comes every 600 seconds."),
 ("The 2015-gap retarget", ["P26", "P01"], "The retarget measures the time from the first to the last block of a period, which spans 2,015 intervals and not 2,016, so the intended pace is slightly faster than ten minutes."),
 ("The factor-of-four clamp", ["P01", "P26"], "The measured time of a period is limited to between a quarter and four times the aim, so the target can change by at most a factor of four at one retarget."),
 ("The BIP 94 branch", ["P26", "P21", "P01"], "The retarget code of Bitcoin Core has a branch for BIP 94 that the chapter's older listing lacks, which builds the new target from the first block of the period."),
 ("Regtest never retargets", ["P33", "P44"], "The regtest chain switches the difficulty adjustment off with a chain parameter, so its difficulty stays the same."),
 ("Regtest halves every 150 blocks", ["P33", "P01"], "The regtest chain halves the reward every 150 blocks, so a developer can watch a halving without waiting four years."),
 # --- mining competition and pools
 ("Pool shares and fees", ["P01", "P58"], "A pool asks its members for shares, which are hashes below an easier target than the network's, and a member proves effort by showing many of them."),
 ("Stratum protocols", ["P61", "P25", "P24", "P66", "P01"], "Stratum is the protocol that a pool and a mining machine speak, in use since 2012 and succeeded by a second version."),
 ("Block withholding", ["P56"], "In block withholding a pool member is paid for shares but never submits a share that would be a full block, so the pool gets none of the rewards he finds."),
 ("The top pool against the thresholds", ["P85", "P50"], "The largest pool of the last year found about 28 percent of the blocks, which sits between the one quarter and the one third of the selfish-mining thresholds."),
 # --- hash rate attacks
 ("The limits of a majority attack", ["P63", "P01"], "A majority attack lets a group with most of the hash rate build a private chain longer than the public one and so make its own earlier payments disappear."),
 ("Nakamoto's catch-up odds", ["P47", "P51", "P01"], "Nakamoto's paper computes the chance that an attacker with a given share of the hash rate ever catches up from some blocks behind, which falls fast with the number of blocks."),
 ("The selfish-mining threshold", ["P50", "P54"], "Selfish mining keeps found blocks secret to waste the work of others, and Eyal and Sirer show that it can pay with a share of one third of the network or less."),
 # --- changing the rules
 ("The minority chain is slow", ["P01"], "After a hard fork the chain with the smaller share of the hash rate finds blocks slowly until its difficulty falls, which takes weeks at the first retarget."),
 ("The chain split of March 2013", ["P01", "P22", "P89", "P78", "P91"], "In March 2013 an upgrade from Bitcoin Core 0.7 to 0.8 split the chain for 24 blocks because of a limit of the Berkeley DB that stored the blocks."),
 ("The Bitcoin Cash fork of 2017", ["P01", "P71"], "Bitcoin Cash split from Bitcoin on 1 August 2017 at block 478,559, a fork made on purpose."),
 ("A soft fork only tightens", ["P01", "P28"], "A soft fork makes the rules stricter, so blocks valid under the new rules are also valid under the old ones and old nodes keep following the chain."),
 ("BIP 34 activation", ["P12", "P01", "P33"], "BIP 34 was the first soft fork activated by counting the version of recent blocks, with 750 and then 950 of the last 1,000 blocks as thresholds."),
 ("The BIP 9 state machine", ["P10", "P01", "P37"], "BIP 9 gives each deployment a state machine of defined, started, locked-in, active or failed, decided once per period of 2,016 blocks."),
 ("BIP 8 lock-in by height", ["P11", "P01", "P53"], "BIP 8 counts in block heights instead of time and can require miners to signal in the last period, so that the soft fork is locked in by the timeout."),
 ("Segwit activation in 2017", ["P18", "P17", "P01", "P16"], "Segwit was not activated by miners for a long time under BIP 9 and was finally activated on 24 August 2017 after BIP 91 and BIP 148 were proposed."),
 ("Speedy Trial and taproot", ["P23", "P43", "P79", "P57"], "Taproot was activated by Speedy Trial, a quick variant of BIP 9 with a threshold of 90 percent and a minimum activation height of 709,632."),
 ("Buried deployments", ["P33", "P13", "P14"], "When a soft fork is long past, the node writes down only its activation height instead of counting votes, as it does for BIP 34, 65 and 66."),
 ("BIP 54 consensus cleanup", ["P20", "P45", "P52", "P21"], "BIP 54, the consensus cleanup, is a proposed change of the rules that would fix the time warp attack and limit signature operations and the size of transactions."),
]
assert len({l for l, *_ in C}) == len(C)
assert all(c.endswith(".") and c[0].isupper() and len(c.split()) >= 8 for *_, c in C)

def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

t = open(SRC, encoding="utf-8").read()
lines = t.split("\n")
pids = set(re.findall(r"^chx:(P\d+) a res:Publication", t, re.M))
for l, srcs, c in C:
    assert set(srcs) <= pids, (l, set(srcs) - pids)
first = next(i for i, x in enumerate(lines) if x.startswith("chx:C_"))
last = max(i for i, x in enumerate(lines) if x.startswith("chx:C_"))
assert all(x.startswith("chx:C_") for x in lines[first:last + 1])
new = []
for i, (l, srcs, c) in enumerate(C, 1):
    new.append('chx:C_%02d a sen0414:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0414:conceptKind "Concept" ; rdfs:comment "%s"@en ; dcterms:source %s .' % (i, q(l), q(c), ", ".join("chx:" + s for s in srcs)))
lines[first:last + 1] = new
t = "\n".join(lines)
NOTE = ("Version 1.1.0 (2026-10-25, task TK_Ch12_Research_Build_R24, criterion AC9_Ch12Research), a new file over the unchanged 1.0.1. "
        "Changed: (1) the 43 primary-source concepts C_01 to C_43 of 1.0.1, which were the headings and index terms of chapter 11 (41 of 41 labels identical to the chapter 11 research), are replaced by the %d primary-source concepts C_01 to C_%02d of chapter 12, "
        "each with a label, a comment in a complete sentence and one or more citations to publications of this file; (2) the scorecard row of topic coverage, which stated 43 concepts from the textbook ontology, now states the new count and origin; "
        "(3) the ontology header: version, modified date, identifier and this note. Kept without change: the research question and scope, the 91 publications P01 to P91, the 27 findings F1 to F27, the scorecard rows of citation strength, methodology and reproducibility." % (len(C), len(C)))
t = t.replace('owl:versionInfo "1.0.1" ; owl:versionIRI <http://example.org/sen0401/ch12/research/1.0.1>', 'owl:versionInfo "1.1.0" ; owl:versionIRI <http://example.org/sen0401/ch12/research/1.1.0>\n    ; skos:changeNote "%s"@en' % q(NOTE), 1)
t = t.replace('dcterms:modified "2026-10-15"^^xsd:date', 'dcterms:modified "2026-10-25"^^xsd:date', 1)
t = t.replace('dcterms:identifier "sen0401_ch12_research_v1_0_1"', 'dcterms:identifier "sen0401_ch12_research_v1_1_0"', 1)
old = 'sen0414:topicCoverage "43 primary-source concepts inventoried from the textbook ontology."'
assert old in t
t = t.replace(old, 'sen0414:topicCoverage "%d primary-source concepts of chapter 12, each with a comment and a citation, taken from the chapter text and the saved sources."' % len(C))
assert 'owl:versionInfo "1.0.1"' not in t and "ch12/research/1.0.1" not in t
open(OUT, "w", encoding="utf-8").write(t)
print("wrote", OUT, "concepts", len(C))
