#!/usr/bin/env python3
"""Applies the D5 5N1K-hidden-from-audience fix (owner's ruling 2026-11-09, same fix already shipped for
Chapters 7-8 in commit 0278076, and for Chapter 9 in sen0401_ch09_story_fix_v1_0_0.py) to Chapter 10's five
story slides, built by ch10-deck's deck_build_v2_0_0.py with the OLD labelled pattern. Content is mined, fact
for fact, from sen0401_ch10_stories_v1_2_0.py's own 'story'/'who'/'where'/'when' fields - nothing invented.
Each of the three kept beats stays under 30 words; the union of their 5N1K tags covers all six required words.
Usage: python3 sen0401_ch10_story_fix_v1_0_0.py <in.pptx> <out.pptx>
"""
__version__ = "1.0.0"
import sys
import sen0401_deck_story_fix_v1_0_0 as F

SLIDES = {
    16: (  # EclipseAtUsenix, slide 17
        {
            "WHAT:": ("On 12 August 2015, at USENIX Security in Washington, D.C., Ethan Heilman and "
                      "colleagues presented Eclipse Attacks on Bitcoin's peer-to-peer network.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("An attacker holding enough IP addresses could monopolize a victim's connections, "
                     "then double-spend against it or mine selfishly.",
                     {"why"}),
            "HOW:": ("Bitcoin Core answered with anchor connections, two block-relay-only links, and peers "
                     "drawn from different autonomous systems.",
                     {"how"}),
        },
        "This chapter's own census still finds 12,488 of 25,361 reachable nodes hiding behind onion addresses.",
    ),
    24: (  # CompactBlockRelay, slide 25
        {
            "WHAT:": ("On 27 April 2016 Matt Corallo was assigned BIP 152, Compact Block Relay, for the "
                      "bitcoin/bips repository on GitHub.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("A node already holds most of a new block's transactions in its own mempool, so "
                     "resending them all wastes bandwidth.",
                     {"why"}),
            "HOW:": ("Suhas Daftuar's Bitcoin Core 0.13.0 code sends a header, a 6-byte short code per "
                     "transaction, and only the few the peer lacks.",
                     {"how", "who"}),
        },
        "In this chapter's run a 13-transaction block went out as 332 bytes instead of 3,062.",
    ),
    36: (  # BloomFiltersLeak, slide 37
        {
            "WHAT:": ("Mike Hearn and Matt Corallo were assigned BIP 37 on 24 October 2012 for the "
                      "bitcoin/bips repository, letting a light client filter by address.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("In 2014 Arthur Gervais and ETH Zurich colleagues showed Bloom filters leak far more "
                     "about a wallet's addresses than intended.",
                     {"why", "who"}),
            "HOW:": ("Bitcoin Core 0.19 turned the filter service off by default, and today only 4,308 of "
                     "25,361 nodes still advertise it.",
                     {"how"}),
        },
        "This chapter's test node simply closes the connection of any peer that still sends a filterload message.",
    ),
    41: (  # FilterIdeaPost, slide 42
        {
            "WHAT:": ("On Monday 9 May 2016 an anonymous developer writing as bfd posted to the bitcoin-dev "
                      "list a committed-filter idea.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Turning the Bloom filter around lets a full node build the filter so the light "
                     "client's own addresses stay hidden.",
                     {"why"}),
            "HOW:": ("Olaoluwa Osuntokun and Alex Akselrod wrote it as BIP 157 and 158, compressing it with "
                     "a Golomb-coded set for Lightning Labs' Neutrino.",
                     {"how", "who"}),
        },
        "This chapter's own code reproduced all ten test vectors published with BIP 158.",
    ),
    44: (  # EncryptionAtLast, slide 45
        {
            "WHAT:": ("On 8 March 2019, in the bitcoin/bips repository, Dhruv Mehta, Tim Ruffing, Jonas "
                      "Schnelli and Pieter Wuille were assigned BIP 324, replacing Schnelli's closed BIP 151.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Unencrypted peer links let anyone watching the wire see which node said what, long "
                     "before BIP 324 closed that gap.",
                     {"why"}),
            "HOW:": ("Bitcoin Core 26.0 added v2 encrypted transport as an option in 2023, and 27.0 made it "
                     "the default in 2024.",
                     {"how"}),
        },
        "This chapter's own capture of a v2 stream showed neither the old magic bytes nor the word version.",
    ),
}

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    F.run(inp, outp, SLIDES)
