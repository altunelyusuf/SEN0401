#!/usr/bin/env python3
"""Applies the D5 5N1K-hidden-from-audience fix (owner's ruling 2026-11-09, same fix already shipped for
Ch7-12) to Chapter 13's four story slides (slide indices 21, 40, 44, 46, 0-based), built by deck_build_v2_0_0.py
with the OLD labelled WHAT:/WHY:/HOW:/SO WHAT: + WHO/WHERE/WHEN/READ-chip pattern. Content is mined, fact for
fact, from sen0401_ch13_stories_v1_3_0.py's own who/where/when fields. CasasciusCoins' WHAT beat is reworded to
add "of Sandy, Utah" because none of its three kept beats otherwise names a where-fact at all (its who-field's
Sandy, Utah was never on the slide); nothing else invented beyond the story module's own fields.
Usage: python3 sen0401_ch13_story_fix_v1_0_0.py <in.pptx> <out.pptx>
"""
__version__ = "1.0.0"
import sys
import sen0401_deck_story_fix_v1_0_0 as F

SLIDES = {
    21: (  # TrezorSecureElement
        {
            "WHAT:": ("SatoshiLabs announced the Trezor Safe 5 on 14 June 2024 at BTC Prague, with a colour "
                      "touchscreen and an EAL 6+ secure element.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("A thief with the device must guess the PIN, and every wrong try costs more waiting.",
                     {"why"}),
            "HOW:": ("The waits double, 1, 2, 4 seconds and so on, and after 16 failed tries the device wipes "
                     "itself.",
                     {"how"}),
        },
        "A signing box protects the key; you protect the intent by reading the address on its own screen.",
    ),
    40: (  # ShamirSharesTheSecret
        {
            "WHAT:": ("In November 1979 Adi Shamir published How to Share a Secret, two pages in the "
                      "Communications of the ACM.",
                      {"what", "when", "where", "who"}),
            "WHY:": ("A secret kept in one place is lost or stolen with it; shares make both loss and theft "
                     "need several failures.",
                     {"why"}),
            "HOW:": ("Any k of n shares rebuild the secret by polynomial interpolation, and k minus 1 shares "
                     "leave it completely undetermined.",
                     {"how"}),
        },
        "Codex32 and SLIP39 apply the same idea to seed words.",
    ),
    44: (  # MtGoxHotWallet
        {
            "WHAT:": ("Mt. Gox of Shibuya, Tokyo, halted withdrawals on 7 February 2014 and suspended all "
                      "trading on 24 February.",
                      {"what", "when", "where"}),
            "WHY:": ("It kept customers' coins in its own wallets, so customers held a claim on the exchange "
                     "and not the keys.",
                     {"why"}),
            "HOW:": ("A leaked document said 744,408 coins were stolen unnoticed for years; the Tokyo court "
                     "found Karpeles guilty of falsifying data.",
                     {"how", "who"}),
        },
        "Not your keys, not your coins: custody is trust.",
    ),
    46: (  # CasasciusCoins
        {
            "WHAT:": ("Mike Caldwell of Sandy, Utah, sold physical bitcoins: a coin with the private key under "
                      "a hologram that shows a honeycomb pattern when peeled.",
                      {"what", "who", "where"}),
            "WHY:": ("A peeled seal shows that someone looked, which a bare slip of paper cannot do.",
                     {"why"}),
            "HOW:": ("Coins came in 1, 10, 25, 100 and 1000 BTC; FinCEN said minting them made him a money "
                     "transmitter, so sales stopped on 26 November 2013.",
                     {"when", "how"}),
        },
        "A tamper seal tells you someone looked, not who.",
    ),
}

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    F.run(inp, outp, SLIDES)
