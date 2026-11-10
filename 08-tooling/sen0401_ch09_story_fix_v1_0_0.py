#!/usr/bin/env python3
"""Applies the D5 5N1K-hidden-from-audience fix (owner's ruling 2026-11-09, same fix already shipped for
Chapters 7-8 in commit 0278076) to Chapter 9's four story slides, which were built by deck_build_v2_0_0.py
with the OLD labelled pattern. Content is mined, fact for fact, from sen0401_ch09_stories_v1_2_0.py's own
'story'/'who'/'where'/'when' fields - nothing invented. Each of the three kept beats stays under 30 words
(the chapter's own deck-build convention); the union of their 5N1K tags covers all six required words.
Usage: python3 sen0401_ch09_story_fix_v1_0_0.py <in.pptx> <out.pptx>
"""
__version__ = "1.0.0"
import sys
import sen0401_deck_story_fix_v1_0_0 as F

# slide index (0-based) -> (beats, so_what)
SLIDES = {
    28: (  # FullRbfPeering, ex14
        {
            "WHAT:": ("On Monday 12 December 2022 Peter Todd posted to the bitcoin-dev list a build of "
                      "Bitcoin Core 24.0.1 carrying Antoine Riard's full-rbf peering code.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Release 24.0.1 had just added mempoolfullrbf, off by default, so only transactions "
                     "that opted in could be replaced by another payer.",
                     {"why"}),
            "HOW:": ("Todd's build advertises a FULL_RBF service bit and peers with others doing the same, "
                     "so replacements travel reliably across roughly thirty nodes.",
                     {"how"}),
        },
        "Bitcoin Core 28.0 made full replacement the default in 2023, and 29.0 removed the option entirely.",
    ),
    44: (  # CarveOutProposal, ex24
        {
            "WHAT:": ("On Thursday 29 November 2018 Matt Corallo wrote to the bitcoin-dev and lightning-dev "
                      "lists that pre-signed Lightning transactions cannot predict next week's fee.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("A counterparty could chain a large, moderate-fee child to a commitment's spare output "
                     "and pin it near the mempool's bottom.",
                     {"why"}),
            "HOW:": ("Corallo's carve-out let one small extra child through; Bitcoin Core 0.19.0.1 shipped "
                     "it in 2019 at 10,000 virtual bytes, not the book's 1,000.",
                     {"how"}),
        },
        "Bitcoin Core 31.0 later removed the carve-out altogether when it adopted the cluster mempool.",
    ),
    48: (  # HalvingBlock, ex25
        {
            "WHAT:": ("Block 840,000 was found on 20 April 2024 at 00:09 UTC by the pool ViaBTC, the first "
                      "block after Bitcoin's fourth halving.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("The halving cut the subsidy from 6.25 to 3.125 bitcoins, so fees made up nearly all "
                     "of that block's reward.",
                     {"why"}),
            "HOW:": ("Fees totalled 3,762,561,499 satoshis of a 4,075,061,499 reward, 92.33 percent, against "
                     "just 0.46 percent in block 971,489.",
                     {"how"}),
        },
        "The chapter's claim that the subsidy dwarfs the fees is true of the later block and false of this one.",
    ),
    50: (  # InstabilityPaper, ex26
        {
            "WHAT:": ("On 21 October 2016 Arvind Narayanan announced on Princeton's CITP blog a paper on "
                      "Bitcoin's instability without the block reward.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Narayanan, Miles Carlsten, Harry Kalodner and Matt Weinberg argued that once fees "
                     "replace rewards a miner can gain by undercutting a rival's block.",
                     {"why", "who"}),
            "HOW:": ("Their model, and this chapter's run, puts a 45-percent miner's odds of re-mining a "
                     "block ahead of a rival at 66.94 percent.",
                     {"how"}),
        },
        "Wallets guard against this by locking a payment's spend to the chain's current height.",
    ),
}

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    F.run(inp, outp, SLIDES)
