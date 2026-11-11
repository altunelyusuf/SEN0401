#!/usr/bin/env python3
"""Applies the D5 5N1K-hidden-from-audience fix (owner's ruling 2026-11-09, same fix shipped for Ch7-11) to
Chapter 12's four story slides (slide indices 9, 24, 44, 46, 0-based), built by deck_build_v3_0_1.py with the
OLD labelled WHAT:/WHY:/HOW:/SO WHAT: + WHO/WHERE/WHEN/READ-chip pattern. Content is mined, fact for fact, from
sen0401_ch12_stories_v1_2_0.py's own who/where/when fields. For ChainSplitOfMarch2013 and TaprootThroughSpeedyTrial,
who/where land on the HOW beat (where the original text already names the people/place) rather than the WHAT
beat, since that is where the facts actually sit; nothing invented beyond the story module's own fields.
Usage: python3 sen0401_ch12_story_fix_v1_0_0.py <in.pptx> <out.pptx>
"""
__version__ = "1.0.0"
import sys
import sen0401_deck_story_fix_v1_0_0 as F

SLIDES = {
    9: (  # HalvingBlockWithRecordFees
        {
            "WHAT:": ("Block 840,000, mined by ViaBTC at 00:09:27 UTC on 20 April 2024, was the first to pay "
                      "the new subsidy of 3.125 coins.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Its 3,050 transactions paid 3,762,561,499 satoshis in fees, 12.04 times the subsidy, so "
                     "the reward was mostly tips.",
                     {"why"}),
            "HOW:": ("The sum was recomputed from the saved block; its coinbase carries the tag ViaBTC, by "
                     "which pool statistics are made.",
                     {"how"}),
        },
        "The book says that fees are a small part of income; this block is an exception.",
    ),
    24: (  # HashcashBeforeBitcoin
        {
            "WHAT:": ("Adam Back proposed Hashcash in 1997 and wrote it up in his paper Hashcash: A Denial of "
                      "Service Counter-Measure, dated 1 August 2002.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Cynthia Dwork and Moni Naor had proposed in 1992 to price junk mail with a moderately "
                     "hard function; Hashcash made the idea practical.",
                     {"why", "who"}),
            "HOW:": ("The sender hashes a string with a growing counter until the hash starts with zeros, as "
                     "in our lottery; the receiver checks it with one hash.",
                     {"how"}),
        },
        "Satoshi Nakamoto's paper of 2008 calls Bitcoin's proof of work similar to Adam Back's Hashcash.",
    ),
    44: (  # ChainSplitOfMarch2013
        {
            "WHAT:": ("On 11 March 2013 block 225,430 was valid for Bitcoin 0.8 and refused by older nodes, "
                      "so the chain split for 24 blocks, about six hours.",
                      {"what", "when", "where"}),
            "WHY:": ("Older versions had too few Berkeley DB locks for a large block, and this accident had "
                     "become a rule of consensus.",
                     {"why"}),
            "HOW:": ("Marek Palatinus and Michael Marsee moved their pools back to 0.7, so the old chain "
                     "carried the most work; Gavin Andresen wrote BIP 50.",
                     {"how", "who"}),
        },
        "Most large businesses paused deposits: they knew that the chain with the most work wins.",
    ),
    46: (  # TaprootThroughSpeedyTrial
        {
            "WHAT:": ("Taproot was activated by Speedy Trial: it opened on 24 April 2021, timed out on 11 "
                      "August 2021 and needed 1,815 of 2,016 blocks.",
                      {"what", "when"}),
            "WHY:": ("A short vote at 90 percent makes a soft fork succeed or fail quickly, and a minimum "
                     "activation height gave nodes time to upgrade.",
                     {"why"}),
            "HOW:": ("F2Pool mined block 709,632 on 14 November 2021 with version 0x20200004, in which bit 2 "
                     "is the taproot signal.",
                     {"how", "who", "where"}),
        },
        "Bitcoin Core 31.1 still holds these parameters in chainparams.cpp, which is how the dates were recomputed.",
    ),
}

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    F.run(inp, outp, SLIDES)
