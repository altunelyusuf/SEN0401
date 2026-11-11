#!/usr/bin/env python3
"""Applies the D5 5N1K-hidden-from-audience fix (owner's ruling 2026-11-09, same fix already shipped for
Ch7-13) to Chapter 14's four story slides (slide indices 7, 22, 33, 36, 0-based), built by deck_build_v2_0_0.py
with the OLD labelled WHAT:/WHY:/HOW:/SO WHAT: + WHO/WHERE/WHEN/READ-chip pattern. Content is mined, fact for
fact, from sen0401_ch14_stories_v1_2_0.py's own who/where/when fields; every beat's text already named all six
facts somewhere across its own three kept beats, so no beat needed rewording - tags were assigned to the beat
that actually carries each fact (e.g. "where" sits on the WHY or HOW beat in three of the four stories, not WHAT).
Usage: python3 sen0401_ch14_story_fix_v1_0_0.py <in.pptx> <out.pptx>
"""
__version__ = "1.0.0"
import sys
import sen0401_deck_story_fix_v1_0_0 as F

SLIDES = {
    7: (  # PizzaForBitcoins
        {
            "WHAT:": ("On 22 May 2010 Laszlo Hanyecz paid 10,000 bitcoins for two pizzas, the first notable "
                      "retail purchase of physical goods with bitcoin.",
                      {"what", "when", "who"}),
            "WHY:": ("He had offered the coins for a couple of pizzas in a Bitcoin Forum post, and a "
                     "19-year-old, Jeremy Sturdivant, took the offer.",
                     {"why", "where"}),
            "HOW:": ("Sturdivant ordered two Papa John's pizzas to Hanyecz's home in Jacksonville and received "
                     "the coins; the payment settled on the chain.",
                     {"how"}),
        },
        "A payment on the chain waits for confirmations, which payment channels and Lightning avoid for small payments.",
    ),
    22: (  # SpillmanChannels
        {
            "WHAT:": ("Mike Hearn posted Anti DoS for tx replacement on 17 April 2013, and Jeremy Spillman "
                      "answered on 20 April with a one-way channel design.",
                      {"what", "when", "who"}),
            "WHY:": ("The first Bitcoin code already let an unrecorded open transaction be replaced until its "
                     "lock time, and the channel idea grew from that.",
                     {"why"}),
            "HOW:": ("The payer signs larger and larger payments while a refund waits behind a lock time; "
                     "Hearn and Matt Corallo announced bitcoinj code on 27 June 2013.",
                     {"how", "where"}),
        },
        "Such channels were safe only with segwit transactions, so Emma's refund is signed before the funding is sent.",
    ),
    33: (  # LightningTorch
        {
            "WHAT:": ("On 19 January 2019 the Twitter user hodlonaut began a game-like test of Lightning by "
                      "sending 100,000 satoshis to a trusted recipient.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("It was a promotional test, passed from one well-known person to the next, to show that "
                     "the network could carry real payments.",
                     {"why"}),
            "HOW:": ("Each recipient added 10,000 satoshis, 34 cents then, and sent the sum on; Jack Dorsey, "
                     "Charlie Lee, Elizabeth Stark and Changpeng Zhao took part.",
                     {"how"}),
        },
        "Each hand-over was an ordinary Lightning payment, with no transaction on the chain for each step.",
    ),
    36: (  # PoonDryjaWhitepaper
        {
            "WHAT:": ("Joseph Poon and Thaddeus Dryja published a Lightning Network white paper in February "
                      "2015; the draft kept on lightning.network is version 0.5.9.2.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("Their summary calls it a decentralized system for instant, high-volume micropayments "
                     "that removes the risk of trusting third-party custody.",
                     {"why"}),
            "HOW:": ("Lightning Labs launched the network in 2018; the picture shows its cut nodes, from "
                     "under 100 in 2018 to about 1,500 in 2022.",
                     {"how"}),
        },
        "The book says the network was first described in February 2015; the word proposed no longer holds.",
    ),
}

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    F.run(inp, outp, SLIDES)
