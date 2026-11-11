#!/usr/bin/env python3
"""Applies the D5 5N1K-hidden-from-audience fix (owner's ruling 2026-11-09, same fix shipped for Ch7-10) to
Chapter 11's four story slides (slide indices 13, 24, 32, 37, 0-based), built by deck_build_v2_0_0.py with the
OLD labelled WHAT:/WHY:/HOW:/SO WHAT: + WHO/WHERE/WHEN/READ-chip pattern. Content is mined, fact for fact, from
sen0401_ch11_stories_v1_2_0.py's own who/where/when fields; two beats (GriefingTheTestnet's WHAT, Signet's WHAT)
are reworded to name the venue/authors/date explicitly where the original wording left where/who implicit or
absent, so the tag union genuinely matches what the three kept beats say - nothing invented beyond the story
module's own fields. Usage: python3 sen0401_ch11_story_fix_v1_0_0.py <in.pptx> <out.pptx>
"""
__version__ = "1.0.0"
import sys
import sen0401_deck_story_fix_v1_0_0 as F

SLIDES = {
    13: (  # HeadlineInTheGenesisBlock
        {
            "WHAT:": ("Satoshi Nakamoto wrote the headline of The Times of 3 January 2009 into the first block: "
                      "Chancellor on brink of second bailout for banks.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("The text proves the block is not older than that day, and the book adds that it recalls "
                     "why an independent monetary system matters.",
                     {"why"}),
            "HOW:": ("The chapter rebuilt the block from the constants in chainparams.cpp and hashed it to "
                     "000000000019d668; its 50 coins can never be spent.",
                     {"how"}),
        },
        "A date quoted inside a block proves the block is not older.",
    ),
    24: (  # TheHashTreeOfRalphMerkle
        {
            "WHAT:": ("Ralph Merkle patented the hash tree in 1979; United States patent 4,309,569 was published "
                      "on 5 January 1982, with Stanford University as assignee.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("A tree of hashes lets one small root vouch for a long list, which is how a block header "
                     "covers every transaction.",
                     {"why"}),
            "HOW:": ("The 40 transaction ids of block 277,315 were hashed in pairs, six levels up, to the root "
                     "in its header.",
                     {"how"}),
        },
        "A small summary can vouch for a large list.",
    ),
    32: (  # GriefingTheTestnet
        {
            "WHAT:": ("On 4 May 2024 Jameson Lopp wrote in a blog post that the minimum-difficulty rule of "
                      "testnet3 let miners create hundreds of blocks in a single day.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("A test network without incentives needs rules against vandals, so testnet4 and BIP 94, "
                     "written by Fabian Jahr, replaced it.",
                     {"why"}),
            "HOW:": ("BIP 94 notes that three years of blocks were mined in a few weeks; on 15 October 2026 "
                     "testnet3 stood at height 5,189,394, testnet4 at 156,618.",
                     {"how"}),
        },
        "Core 31.1 still starts testnet3 but its help says that the support will be removed.",
    ),
    37: (  # SignetBlocksNeedASignature
        {
            "WHAT:": ("Karl-Johan Alm and Anthony Towns wrote BIP 325 on 20 March 2019 in the bitcoin/bips "
                      "repository: a signet block is valid only if it solves a challenge script.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Replace mining by a signature and a test network stays calm.",
                     {"why"}),
            "HOW:": ("The default challenge is a 1-of-2 multisig, and its four magic bytes, 0a03cf40, start the "
                     "double SHA-256 of that script.",
                     {"how"}),
        },
        "Core 0.21.0 added it; on 15 October 2026 the tip was at height 326,440, 2.27 times the book's listing.",
    ),
}

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    F.run(inp, outp, SLIDES)
