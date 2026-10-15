"""SEN0401 chapter 12 (Mining and Consensus) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch12-evidence."""
__version__ = "1.1.0"  # PNG copies of the four JPEG pictures, bio fields, credits without dates and without the stand-in remark (the deck labels stand-ins)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "HashcashBeforeBitcoin", "bio": 'Adam Back, cryptographer, proposed Hashcash in 1997 and described it in a paper dated 1 August 2002; Satoshi Nakamoto cites it in the Bitcoin paper', "title": "The stamp that made email cost something",
     "when": "2002-08-01",
     "who": "Adam Back, the cryptographer who proposed Hashcash, Cynthia Dwork and Moni Naor, who proposed pricing functions against junk mail, and Satoshi Nakamoto, who cites Back's idea",
     "where": "the paper Hashcash - A Denial of Service Counter-Measure, dated 1 August 2002, and the Bitcoin paper of 2008",
     "link": "https://en.bitcoin.it/wiki/Hashcash",
     "concepts": ["HelloWorldNonce", "DiceAnalogy", "ProofIsCheapToCheck", "HashBelowTarget"],
     "story": ("Proof of work did not start with Bitcoin: Cynthia Dwork and Moni Naor proposed in 1992 that a user should compute a moderately hard function before using a shared resource, to fight junk mail. "
               "Adam Back proposed Hashcash in 1997 and described it more formally in a paper dated 1 August 2002, in which the sender hashes a string with a growing counter until the hash begins with enough zeros. "
               "Nakamoto's paper says that Bitcoin needs a proof-of-work system similar to Adam Back's Hashcash. "
               "In this chapter the book's toy version, the phrase Hello, world! with a counter, found its first zero at 32, as the book prints, and a block of Bitcoin does the same with 62 or more zero bits."),
     "lesson": "A cheap check of an expensive search can price any request",
     "source": "dwork_naor_1992_pricing.pdf (P49), wikipedia_hashcash.html (P68), back_2002_hashcash.pdf (P48), nakamoto_2008_bitcoin.pdf (P47), wikipedia_adam_back.html (P67), bitcoinwiki_hashcash.html (P62); the HelloWorldNonce leaf",
     "credit": "Adam Back - Joi Ito, CC BY 2.0, Wikimedia Commons",
     "photo": "photo_adam_back.png"},
    {"id": "ChainSplitOfMarch2013", "bio": 'Gavin Andresen, Bitcoin developer, wrote BIP 50 about the split of 11 March 2013; Marek Palatinus and Michael Marsee ran the pools that went back to 0.7', "title": "The day Bitcoin had two histories",
     "when": "2013-03-11",
     "who": "Gavin Andresen, who wrote the post-mortem BIP 50, Marek Palatinus (Slush) and Michael Marsee (Eleuthria of BTCGuild), whose pools downgraded their nodes, and Vitalik Buterin, who reported it for Bitcoin Magazine",
     "where": "the Bitcoin network, from block 225,430, and BIP 50 in the bitcoin/bips repository",
     "link": "https://bips.dev/50/",
     "concepts": ["ChainSplitMarch2013", "MostWorkNotLongest", "MinorityChainSlow", "SoftForkOnlyTightens"],
     "story": ("On 11 March 2013 at 23:24:19 UTC block 225,430, with 797 transactions, was mined and accepted by nodes of Bitcoin 0.8 but rejected by some older nodes. "
               "BIP 50, written by Gavin Andresen, explains that versions before 0.8 had too few Berkeley DB locks for a large but valid block, which had accidentally become a rule of consensus, while 0.8 used LevelDB. "
               "Marek Palatinus and Michael Marsee downgraded their pools to 0.7 so that the old chain would carry the most work, and the split lasted 24 blocks, about six hours, until block 225,454. "
               "Most large businesses shut their deposits to protect themselves from double spends, which shows what the choice of the chain with most work means for a shop."),
     "lesson": "An accident in software can become a rule of the network",
     "source": "bip-0050.mediawiki (P22), bitcoinmagazine_2013_chain_fork.html (P89), mempool_block_225430.json (P78), mempool_block_225454.json (P91); the ChainSplitMarch2013 leaf",
     "credit": "Fork in the road - Ian Sane, CC BY 2.0, Flickr",
     "photo": "photo_fork_in_the_road.png"},
    {"id": "HalvingBlockWithRecordFees", "bio": 'ViaBTC, a mining pool, mined block 840,000 on 20 April 2024, the first to pay 3.125 coins of subsidy', "title": "The block where the tips beat the wage twelve times",
     "when": "2024-04-20",
     "who": "Satoshi Nakamoto, who wrote the halving schedule, and ViaBTC, the pool that mined block 840,000",
     "where": "the main chain of Bitcoin, block 840,000, as listed by mempool.space",
     "link": "https://mempool.space/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5",
     "concepts": ["HalvingEvery210000", "FeesOfBlock840000", "CoinbaseDataAndTags", "RewardIsSubsidyPlusFees"],
     "story": ("Block 840,000 was mined at 00:09:27 UTC on 20 April 2024 and was the first to pay the new subsidy of 3.125 coins, half of 6.25. "
               "Its 3,050 transactions paid 3,762,561,499 satoshis in fees, 12.04 times the subsidy, so the reward of 4,075,061,499 satoshis was made mostly of tips. "
               "The coinbase carries the tag /ViaBTC/ and the words Mined by buzz120, the sign by which the statistics of pools are made. "
               "The book says that fees are usually a small percentage of income, and this block shows an exception; in this chapter the sum was recomputed from the saved block."),
     "lesson": "The subsidy halves on schedule, but fees can swing wildly",
     "source": "mempool_block_840000.json (P74), mempool_block_630000.json (P77), book_ch12_mining.adoc (P01); the HalvingEvery210000 and FeesOfBlock840000 leaves",
     "credit": "Antminer ASIC Miner - Steve Rainwater, CC BY-SA 2.0, Wikimedia Commons",
     "photo": "photo_asic_miner.png"},
    {"id": "TaprootThroughSpeedyTrial", "bio": 'Pieter Wuille, Jonas Nick and Anthony Towns wrote BIP 341; F2Pool mined block 709,632 on 14 November 2021, the first under taproot rules', "title": "A ninety percent vote with a three-month clock",
     "when": "2021-11-14",
     "who": "Pieter Wuille, Jonas Nick and Anthony Towns, the authors of BIP 341, and F2Pool, which mined the first block under the new rules",
     "where": "the main chain of Bitcoin at block 709,632, and BIP 341 in the bitcoin/bips repository",
     "link": "https://bips.dev/341/",
     "concepts": ["SpeedyTrialTaproot", "Bip9StateMachine", "Bip8LockInByHeight", "VersionHistory"],
     "story": ("Taproot was activated by a variant of BIP 9 called Speedy Trial, which opened on 24 April 2021, timed out on 11 August 2021 and needed 1,815 of 2,016 blocks, 90 percent, instead of 1,916. "
               "It also set a minimum activation height of 709,632, so that nodes had time to upgrade after the lock-in. "
               "Block 709,632 was mined by F2Pool on 14 November 2021 at 05:15:27 UTC with the version 0x20200004, in which bit 2 is the signal for taproot. "
               "Bitcoin Core 0.21.1 carried the parameters, and release 31.1 still has them in chainparams.cpp, which is how this chapter recomputed the dates."),
     "lesson": "Fail fast or succeed: a short vote keeps a soft fork calm",
     "source": "bip-0341.mediawiki (P23), core_relnotes_0.21.1.md (P43), core_src_kernel_chainparams.cpp (P33), mempool_block_709632.json (P79), optech_topic_taproot.html (P57); the SpeedyTrialTaproot leaf",
     "credit": "Taproot profile - Forest and Kim Starr, CC BY 3.0, Wikimedia Commons",
     "photo": "photo_taproot_profile.png"},
]
RESOURCES = [   # (kind, title, url): each opened on 2026-10-15
    ("video", "But how does bitcoin actually work? (3Blue1Brown, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=bBC-nXj3Ng4"),
    ("video", "Mining Difficulty - Simply Explained (YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=o1gOyhU6XEw"),
    ("video", "Bitcoin - Proof of work (Khan Academy, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=9V1bipPkCTU"),
    ("video", "Bitcoin - The money supply (Khan Academy, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=JuWYLAtz3Y4"),
    ("topic", "Bitcoin Optech topic: Time warp attack", "https://bitcoinops.org/en/topics/time-warp/"),
    ("topic", "Bitcoin Optech topic: Soft fork activation", "https://bitcoinops.org/en/topics/soft-fork-activation/"),
    ("topic", "Bitcoin Optech topic: Selfish mining", "https://bitcoinops.org/en/topics/selfish-mining/"),
    ("topic", "Bitcoin Optech topic: Block withholding attacks", "https://bitcoinops.org/en/topics/block-withholding/"),
    ("topic", "Bitcoin Optech topic: ASICBoost", "https://bitcoinops.org/en/topics/asicboost/"),
    ("explorer", "mempool.space, the block explorer that supplied the real blocks and the statistics of this chapter", "https://mempool.space/"),
    ("book", "Mastering Bitcoin, the book site (Antonopoulos and Harding)", "https://bitcoinbook.info/"),
    ("documentation", "BIP 9: version bits with timeout and delay", "https://bips.dev/9/"),
    ("documentation", "BIP 54: consensus cleanup", "https://bips.dev/54/"),
    ("documentation", "Bitcoin Core 29.0 release notes (timewarp rule in block templates)", "https://bitcoincore.org/en/releases/29.0/"),
    ("paper", "Majority is not Enough: Bitcoin Mining is Vulnerable (Eyal and Sirer)", "https://arxiv.org/abs/1311.0243"),
    ("paper", "Analysis of Hashrate-Based Double Spending (Rosenfeld)", "https://arxiv.org/abs/1402.2009"),
]
FIELDS = ("id", "bio", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")
FACTS = {   # story id -> (saved file, fragments that must be found in it)
    "HashcashBeforeBitcoin": ("dwork_naor_1992_pricing.txt", ["We present a computational technique for combatting junk mail", "moderately hard, but not intractable, function"]),
    "HashcashBeforeBitcoin2": ("wikipedia_hashcash.txt", ["Hashcash was proposed in 1997 by Adam Back"]),
    "HashcashBeforeBitcoin3": ("back_2002_hashcash.txt", ["1st August 2002"]),
    "HashcashBeforeBitcoin4": ("nakamoto_2008_bitcoin.txt", ["similar to Adam Back's Hashcash"]),
    "HashcashBeforeBitcoin5": ("wikipedia_adam_back.txt", ["He invented Hashcash"]),
    "ChainSplitOfMarch2013": ("bip-0050.mediawiki", ["Authors: Gavin Andresen", "Bitcoin 0.8 nodes were able to handle this, but some pre-0.8 Bitcoin nodes rejected it", "Marek Palatinus (Slush) and Michael Marsee (Eleuthria of BTCGuild)", "Bitcoin 0.8 did not use Berkeley DB. It switched to LevelDB instead"]),
    "ChainSplitOfMarch20132": ("bitcoinmagazine_2013_chain_fork.txt", ["Starting from block 225430", "The split lasted for 24 blocks or 6 hours", "most large businesses, including BitcoinStore, BitPay, SatoshiDice and MtGox, shut down deposits to protect themselves from double spend attacks"]),
    "ChainSplitOfMarch20133": ("mempool_block_225430.json", ['"height":225430', '"tx_count":797']),
    "HalvingBlockWithRecordFees": ("mempool_block_840000.json", ['"height":840000', '"tx_count":3050', '"totalFees":3762561499', '"reward":4075061499', '"name":"ViaBTC"', '"timestamp":1713571767']),
    "HalvingBlockWithRecordFees2": ("book_ch12_mining.adoc", ["Today, the fees usually represent only a small percentage of a miner's income"]),
    "TaprootThroughSpeedyTrial": ("bip-0341.mediawiki", ["Authors: Pieter Wuille", "Jonas Nick", "Anthony Towns", "the threshold is 1815 blocks (90%) instead of 1916 blocks (95%), and the min_activation_height is block 709632", "The deployment did activate at height 709632 on Bitcoin mainnet"]),
    "TaprootThroughSpeedyTrial2": ("mempool_block_709632.json", ['"height":709632', '"name":"F2Pool"', '"timestamp":1636866927', '"version":538968068']),
    "TaprootThroughSpeedyTrial3": ("core_relnotes_0.21.1.md", ["Speedy Trial"]),
    "TaprootThroughSpeedyTrial4": ("core_src_kernel_chainparams.cpp", ["consensus.vDeployments[Consensus::DEPLOYMENT_TAPROOT].min_activation_height = 709632"]),
}


def run_checks():
    bad = []
    ev = os.path.join(HERE, "ch12-evidence")
    for s in STORIES:
        for f in FIELDS:
            v = s.get(f)
            if not v or "TODO" in str(v) or "CREDIT_" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(HERE, "..", "03-materials", "ch12", "assets", str(s.get("photo", "")))
        if not os.path.exists(p) or os.path.getsize(p) < 10000 and not str(s.get("photo")).endswith((".jpg", ".png")) or open(p, "rb").read(5) in (b"<!DOC", b"<html"):
            bad.append("%s: picture file %s missing or not a picture" % (s.get("id"), s.get("photo")))
        for k in [s["id"]] + [s["id"] + str(i) for i in range(2, 7)]:
            if k not in FACTS:
                continue
            fn, frs = FACTS[k]
            t = re.sub(r"\s+", " ", open(os.path.join(ev, fn), encoding="utf-8", errors="replace").read())
            for fr in frs:
                if re.sub(r"\s+", " ", fr) not in t:
                    bad.append("%s: fact %r not in %s" % (s["id"], fr, fn))
    if len(STORIES) < 4:
        bad.append("fewer than four stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
