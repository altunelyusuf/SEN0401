"""SEN0401 chapter 09 (Transaction Fees) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch09-evidence."""
__version__ = "1.0.0"
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "FullRbfPeering", "title": "A node that only listens to replacements",
     "when": "2022-12-12",
     "who": "Peter Todd, a Bitcoin developer who posted the build, and Antoine Riard, whose peering code it contains",
     "where": "the bitcoin-dev mailing list, and the nodes of the public Bitcoin network that run Bitcoin Core 24.0.1",
     "link": "https://mirror.b10c.me/lists/bitcoindev/Y5eSFbR61HleY6dw@petertodd.org",
     "concepts": ["FullRbfDefault", "OptInSignalRule", "RemovedOption"],
     "story": ("On Monday 12 December 2022 Peter Todd posted to the bitcoin-dev list a build of Bitcoin Core 24.0.1 with Antoine Riard's full-rbf peering code. "
               "Release 24.0.1 had just added the option mempoolfullrbf, which defaults to off and so allows only opt-in replacement. "
               "Todd's build advertises a FULL_RBF service bit when the option is set and connects to four additional nodes that do the same, so that a core group of nodes passes on replacements reliably. "
               "He estimated about 30 reliable nodes running his branch and about 50 Bitcoin Knots nodes that advertised the bit. "
               "Bitcoin Optech's newsletter of 14 December 2022 reported the monitoring of full-rbf replacements, and Bitcoin Core 28.0 later made full replacement the default and 29.0 removed the option. "
               "The test node of this chapter accepts a replacement of a transaction that never signalled."),
     "lesson": "Policy is what most nodes choose to relay, and it changes by their choice",
     "source": "ml_todd_2022-12_fullrbf.txt (P41), core_relnotes_24.0.1.txt (P22), optech_newsletter_2022-12-14.txt (P54), release notes 28.0 and 29.0 (P23, P24); the run's FullRbfDefault leaf",
     "credit": "Bitcoin and Namecoin Accepted Here sign - ninjarobot, CC0, Wikimedia Commons, 2013-06-19",
     "photo": "photo_bitcoin_namecoin_accepted_here_sign.png"},
    {"id": "CarveOutProposal", "title": "A pre-signed transaction cannot guess next week's fee",
     "when": "2018-11-29",
     "who": "Matt Corallo, a Bitcoin Core and Lightning developer, writing to the bitcoin-dev and lightning-dev lists",
     "where": "the bitcoin-dev and lightning-dev mailing lists, cross-posted; the rule shipped in Bitcoin Core 0.19.0.1",
     "link": "https://mirror.b10c.me/lists/bitcoindev/c3f68b73-84c6-7428-4bf6-b47802141392@mattcorallo.com",
     "concepts": ["CarveOut", "CarveOutRule", "AnchorOutputs", "LightningAnchorOutputs"],
     "story": ("On Thursday 29 November 2018 Matt Corallo wrote that Lightning channels exchange pre-signed transactions that are broadcast much later, so their fee has to be predicted or added afterwards by a child. "
               "He described how a counterparty could chain a large child of only moderate fee rate to the anyone-can-spend output of a commitment transaction and keep it at the bottom of the mempool. "
               "His answer, the carve-out, allowed one extra small child beyond the usual limits, and he proposed that it be no greater than 1K in virtual size. "
               "Bitcoin Core 0.19.0.1 shipped the carve-out in November 2019 with an extra child of up to 10,000 virtual bytes, and Bitcoin Core 31.0 removed it with the cluster mempool. "
               "The book states 1,000 and 100,000 where the code says 10,000 and 101,000."),
     "lesson": "A limit built for one attack can outlive the problem it solved",
     "source": "ml_corallo_2018-12_carveout.txt (P40), core_relnotes_0.19.0.1.md (P21), core_relnotes_31.0 (P26), core_src_policy_policy.h (P27); the run's CarveOutRule leaf",
     "credit": "Lightning Network logo - Ole Henrik Skogstrom, CC BY-SA 4.0, Wikimedia Commons, 2020-04-24",
     "photo": "photo_lightning_network_logo.png"},
    {"id": "HalvingBlock", "title": "The block in which fees were nearly the whole reward",
     "when": "2024-04-20",
     "who": "the mining pool ViaBTC, which found block 840,000, and the senders of its 3,050 transactions",
     "where": "the Bitcoin chain at height 840,000, the block of the fourth halving",
     "link": "https://mempool.space/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5",
     "concepts": ["FeesVsSubsidy", "SubsidyHalvings", "BlockRewardMix", "FeeOnlyFuture"],
     "story": ("Block 840,000 was found on 20 April 2024 at 00:09 UTC by the pool ViaBTC and held 3,050 transactions. "
               "It was the first block after the fourth halving, so the subsidy fell from 6.25 to 3.125 bitcoins, 312,500,000 satoshis. "
               "The fees in the same block were 3,762,561,499 satoshis, so the reward of 4,075,061,499 satoshis was 92.33 percent fees. "
               "In block 971,489 the fees were only 0.46 percent of the reward. "
               "The book says that the subsidy is much higher than the fees, which is true of that later block and false of the halving block."),
     "lesson": "Check a book's claim against the block, because the market moves",
     "source": "mempool_block_840000.json (P64), mempool_blocks_fees_1y.json (P66), core_src_validation.cpp (P36); the run's FeesVsSubsidy leaf",
     "credit": "Bitcoin mining farm - Marko Ahtisaari, CC BY 2.0, Wikimedia Commons, 2014-06-14 (an illustration of mining, not of this block)",
     "photo": "photo_bitcoin_mining_farm.jpg"},
    {"id": "InstabilityPaper", "title": "What if nobody got a subsidy?",
     "when": "2016-10-21",
     "who": "Miles Carlsten, Harry Kalodner, S. Matthew Weinberg and Arvind Narayanan, computer scientists at Princeton University",
     "where": "Princeton University, New Jersey; the paper was presented at ACM CCS, the week after the announcement",
     "link": "https://blog.citp.princeton.edu/2016/10/21/bitcoin-is-unstable-without-the-block-reward/",
     "concepts": ["FeeOnlyFuture", "UndercuttingAttack", "SnipingAttack", "SnipingProbability"],
     "story": ("On 21 October 2016 Arvind Narayanan announced on the Princeton CITP blog the paper On the Instability of Bitcoin Without the Block Reward, written with Miles Carlsten, Harry Kalodner and Matt Weinberg and presented at ACM CCS the next week. "
               "They start from the observation that Bitcoin gives miners two incentives, block rewards and transaction fees, and that the first is expected to give way to the second. "
               "Their model shows that when fees are the main income a miner can gain by undercutting a block of a rival, which makes mining less stable. "
               "The chapter's last section describes the same pressure as fee sniping, and the run computes that a miner with 45 percent of the hash rate wins the race to re-mine a block with probability 66.94 percent. "
               "The wallet's countermeasure is the lock time of the current height."),
     "lesson": "Fees must replace the subsidy, so the rules for fees must be stable",
     "source": "carlsten_2016_instability.txt (P60), citp_instability_blog.txt (P72), nakamoto_2008_bitcoin.txt (P59), optech_topic_fee_sniping.txt (P52); the run's SnipingProbability leaf",
     "credit": "Nassau Hall, Princeton University - Smallbones, CC0, Wikimedia Commons, 2012-02-18",
     "photo": "photo_nassau_hall_princeton.jpg"},
]
# the date of the paper is the conference month of the source; the story's "when" is the year the saved paper names
RESOURCES = [   # (kind, title, url): each opened on 2026-10-15
    ("video", "Bitcoin Transaction Fees - Andreas Antonopoulos (Bitcoin TV, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=MPQMCVVhExY"),
    ("podcast", "Chaincode Podcast, Gloria Zhao on package relay (2022-05-23)", "https://podcast.chaincode.com/2022/05/23/gloria-package-relay"),
    ("podcast", "Bitcoin Optech Podcast, 2023-07-06", "https://bitcoinops.org/en/podcast/2023/07/06/"),
    ("topic", "Bitcoin Optech topic: Replace by fee", "https://bitcoinops.org/en/topics/replace-by-fee/"),
    ("mailing list", "bitcoin-dev, Peter Todd, 2022-12-12 (mirror)", "https://mirror.b10c.me/lists/bitcoindev/Y5eSFbR61HleY6dw@petertodd.org"),
    ("explorer", "mempool.space, block 840,000", "https://mempool.space/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5"),
]
FIELDS = ("id", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")
FACTS = {   # story id -> (saved file, fragments that must be found in it)
    "FullRbfPeering": ("ml_todd_2022-12_fullrbf.txt", ["Mon, 12 Dec 2022", "Antoine Riard's full-rbf peering", "FULL_RBF service bit", "four additional FULL_RBF peers", "~30 reliable nodes", "~50 reliable Bitcoin Knots"]),
    "CarveOutProposal": ("ml_corallo_2018-12_carveout.txt", ["Thu, 29 Nov 2018", "Matt Corallo", "no greater than 1K in virtual size"]),
    "HalvingBlock": ("mempool_block_840000.json", ['"height":840000', '"totalFees":3762561499', '"reward":4075061499', '"tx_count":3050', '"name":"ViaBTC"']),
    "InstabilityPaper": ("citp_instability_blog.txt", ["October 21, 2016", "which Harry will present at ACM CCS next week", "Miles Carlsten, Harry Kalodner, and Matt Weinberg"]),
    "InstabilityPaper2": ("carlsten_2016_instability.txt", ["Instability of Bitcoin Without the Block Reward", "Harry Kalodner", "Arvind Narayanan", "block rewards"]),
}


def run_checks():
    bad = []
    ev = os.path.join(HERE, "ch09-evidence")
    for s in STORIES:
        for f in FIELDS:
            v = s.get(f)
            if not v or "TODO" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(HERE, "..", "03-materials", "ch09", "assets", str(s.get("photo", "")))
        if not os.path.exists(p):
            bad.append("%s: picture file %s missing" % (s.get("id"), s.get("photo")))
        for k in (s["id"], s["id"] + "2"):
            if k not in FACTS:
                continue
            fn, frs = FACTS[k]
            t = re.sub(r"\s+", " ", open(os.path.join(ev, fn), encoding="utf-8", errors="replace").read())
            for fr in frs:
                if fr not in t:
                    bad.append("%s: fact %r not in %s" % (s["id"], fr, fn))
    if len(STORIES) < 3:
        bad.append("fewer than three stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
