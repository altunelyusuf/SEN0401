"""SEN0401 chapter 4 - the story companion to the chapter corpus (version 1.0.0).

Chapter 4 (Keys and Addresses) under the owner's 5N1K rule: real, dated, sourced stories with
one live link each, enforced by this file's self-check. Three stories carry the chapter's
three hard ideas:

* NewDirections1976 - public-key cryptography has a birthday and two named parents; everything
  the chapter derives (k -> K -> address) stands on that 1976 paper.
* Base58Design - the address alphabet is not arbitrary: Satoshi's own four reasons sit as a
  comment in src/base58.h of the pinned source tree, quoted verbatim on the slide.
* BitcoinEater - a valid address no key has ever matched: 13.4+ BTC provably burned, fetched
  live from an explorer at build time. Addresses commit to keys; they do not conjure them.

Usage: import STORIES, EATER; run the file for self-checks.
"""
__version__ = "1.2.0"  # each story link goes straight to the resource and carries linkLabel (owner finding of 2026-10-16)

STORIES = [
    {
        "id": "NewDirections1976",
        "title": "The 1976 paper that split the key in two",
        "when": "1976-11",
        "who": "Whitfield Diffie and Martin Hellman (Turing Award 2015)",
        "where": "IEEE Transactions on Information Theory",
        "link": "https://www-ee.stanford.edu/~hellman/publications/24.pdf", "linkLabel": "Diffie, Hellman: New Directions (PDF)",
        "concepts": ["PublicKeyCryptography", "DiscreteLogarithm", "DigitalSignature"],
        "story": ("In November 1976 two Stanford researchers published 'New Directions in "
                  "Cryptography', opening with a sentence that aged well: 'We stand today on the "
                  "brink of a revolution in cryptography.' Their idea - a key split into a public "
                  "half and a private half, tied by a one-way computation - is the exact machinery "
                  "this chapter runs: multiply a point, publish the result, keep the multiplier. "
                  "Forty years later the ACM gave them the Turing Award for it."),
        "lesson": "Every address in this chapter stands on one 1976 idea",
        "source": ("Diffie and Hellman, 'New Directions in Cryptography', IEEE Transactions on "
                   "Information Theory 22(6), November 1976; ACM A.M. Turing Award 2015. Photo: "
                   "Wikimedia Commons 'Diffie and Hellman', CC BY-SA 3.0."),
    },
    {
        "id": "Base58Design",
        "title": "Why 58? Satoshi left the reasons in the file",
        "when": "2009-2010",
        "who": "Satoshi Nakamoto - named by the file's own copyright line",
        "where": "src/base58.h in the bitcoin/bitcoin tree",
        "link": "https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/base58.h", "linkLabel": "base58.h in bitcoin/bitcoin (source)",
        "concepts": ["Base58Check", "NumberBase", "Checksum"],
        "story": ("Open src/base58.h in the source tree this course pins and the first thing after "
                  "the copyright lines - 'Copyright (c) 2009-2010 Satoshi Nakamoto' - is a design "
                  "memo. Why base-58 and not base-64? Because 0, O, I and l look alike in some "
                  "fonts; because punctuation breaks selection and line-wrapping; because an "
                  "all-alphanumeric string survives e-mail and double-clicks whole. Four human "
                  "reasons, zero mathematics - the alphabet of every legacy address is a usability "
                  "decision, documented by its author in the code itself."),
        "lesson": "Address formats are human-factors engineering, documented in the source",
        "source": ("src/base58.h at the corpus-pinned commit 05bc2f53 of bitcoin/bitcoin: the "
                   "copyright line naming Satoshi Nakamoto (2009-2010) and the 'Why base-58 "
                   "instead of standard base-64' comment, quoted verbatim on the slide (MIT)."),
    },
    {
        "id": "BitcoinEater",
        "title": "The address that eats coins",
        "when": "since 2011; balance fetched 2026-10-06",
        "who": "thousands of senders; no key holder - by construction",
        "where": "address 1BitcoinEaterAddressDontSendf59kuE",
        "link": "https://blockstream.info/address/1BitcoinEaterAddressDontSendf59kuE", "linkLabel": "The eater address on blockstream.info",
        "concepts": ["P2pkhAddress", "Commitment", "VanityAddress"],
        "story": ("Spell a message inside an address, append a valid checksum, and you get "
                  "1BitcoinEaterAddressDontSendf59kuE - a perfectly valid address whose matching "
                  "key nobody has, because it was chosen as text, not derived from a key. People "
                  "send coins to it anyway: at this build it held 13.41747849 BTC across 5,832 "
                  "deposits, and not one satoshi has ever left. The checksum protects you from "
                  "mistyping an address; nothing protects coins sent to an address that commits "
                  "to no key."),
        "lesson": "An address is a commitment to a key - not proof one exists",
        "source": ("blockstream.info API, address 1BitcoinEaterAddressDontSendf59kuE, fetched "
                   "2026-10-06 during this build: funded 1,341,747,849 sat over 5,832 outputs, "
                   "spent 0 - the figures pinned in EATER below."),
    },
]

# The burn-address figures the deck shows, pinned at build time (sat, outputs, spent).
EATER = {"addr": "1BitcoinEaterAddressDontSendf59kuE",
         "funded_sat": 1_341_747_849, "outputs": 5_832, "spent_sat": 0,
         "fetched": "2026-10-06"}


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
    if "November 1976" not in STORIES[0]["source"]:
        bad.append("NewDirections1976: date missing from source")
    if "05bc2f53" not in STORIES[1]["source"]:
        bad.append("Base58Design: pinned commit missing from source")
    if "1,341,747,849" not in STORIES[2]["source"]:
        bad.append("BitcoinEater: funded figure missing from source")
    if EATER["funded_sat"] != 1_341_747_849 or EATER["spent_sat"] != 0 or EATER["outputs"] != 5_832:
        bad.append("EATER: pinned figures drifted from the recorded fetch")
    if abs(EATER["funded_sat"] / 1e8 - 13.41747849) > 1e-9:
        bad.append("EATER: BTC restatement wrong")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)


# ---------------------------------------------------------------------------------------------- 1.2.0: the story contract of the deck checks (owner's coordinator, 2026-10-19)
# Every story gets an ISO date (the day of the event the story is anchored to), a who that names real people or bodies, a where of three words or more, a licence-clear picture of
# the chapter's assets with its credit, and a further-reading link that answers from the build machine; the old fields not named here are unchanged.
_OVERRIDES = {'NewDirections1976': {'when': '1976-06-03',
                       'who': 'Whitfield Diffie and Martin Hellman, the Stanford researchers who wrote the paper and received the Turing Award for it',
                       'where': 'IEEE Transactions on Information Theory, volume IT-22, number 6',
                       'bio': 'Whitfield Diffie, born 1944, American cryptographer; Martin Hellman, born 1945, American cryptographer and professor at Stanford; ACM '
                              'A.M. Turing Award 2015',
                       'story': "Two Stanford researchers, Whitfield Diffie and Martin Hellman, sent a paper called 'New Directions in Cryptography' to the IEEE "
                                'Transactions on Information Theory, which stamped the manuscript received on 3 June 1976 and printed it in its November issue. It opens '
                                'with a sentence that aged well: we stand today on the brink of a revolution in cryptography. Their idea, a key split into a public half '
                                'and a private half tied by a one-way computation, is the exact machinery this chapter runs: multiply a point, publish the result, keep '
                                'the multiplier. Forty years after the paper the ACM gave them its Turing Award for it.',
                       'source': "Diffie and Hellman, 'New Directions in Cryptography', IEEE Transactions on Information Theory 22(6), November 1976, pp. 644-654; the "
                                 "first page's footnote reads 'Manuscript received June 3, 1976' (read in the PDF at www-ee.stanford.edu/~hellman); ACM A.M. Turing "
                                 'Award for 2015. Picture: Whitfield Diffie at the Royal Society, 2017 - Duncan Hull, CC BY-SA 4.0, Wikimedia Commons.',
                       'photo': 'photo_whitfield_diffie_2017.jpg',
                       'credit': 'Whitfield Diffie, 2017 - Duncan Hull, CC BY-SA 4.0'},
 'Base58Design': {'when': '2009-01-08',
                  'who': "Satoshi Nakamoto, named by the file's own copyright line",
                  'where': 'src/base58.h in the bitcoin/bitcoin source tree',
                  'bio': 'Satoshi Nakamoto, pseudonym of the unknown author of the first Bitcoin software, announced as version 0.1 on 8 January 2009',
                  'story': "Open src/base58.h in the source tree this course pins and the first thing after the copyright lines - 'Copyright (c) 2009-2010 Satoshi "
                           "Nakamoto' - is a design memo. Why base-58 and not base-64? Because 0, O, I and l look alike in some fonts; because punctuation breaks "
                           'selection and line-wrapping; because an all-alphanumeric string survives e-mail and double-clicks whole. The same four reasons stand in the '
                           'original source of 2009, which Satoshi announced as version 0.1 on 8 January 2009. Four human reasons, zero mathematics - the alphabet of '
                           'every legacy address is a usability decision, documented by its author in the code itself.',
                  'source': "src/base58.h at the corpus-pinned commit 05bc2f53 of bitcoin/bitcoin: the copyright line naming Satoshi Nakamoto (2009-2010) and the 'Why "
                            "base-58 instead of standard base-64' comment, quoted verbatim on the slide (MIT); the same comment, with 'account number' for 'data', in "
                            'src/base58.h of the 0.1.x source of 2009 (github.com/trottier/original-bitcoin, readme.txt: BitCoin v0.1.3 ALPHA). The anchor date is the '
                            'announcement of version 0.1 (metzdowd.com, 2009-01-08); the day the memo was written is not recorded. Picture: the bronze bust of Satoshi '
                            'Nakamoto in Graphisoft Park, Budapest, unveiled on 16 September 2021 - Fekist, CC BY-SA 4.0, Wikimedia Commons.',
                  'photo': 'photo_satoshi_bust_budapest.jpg',
                  'credit': 'Satoshi bust, Budapest - Fekist, CC BY-SA 4.0'},
 'BitcoinEater': {'when': '2026-10-06',
                  'who': 'Blockstream Explorer, whose address page and API recorded the deposits of thousands of anonymous senders',
                  'where': 'the Bitcoin main chain, at address 1BitcoinEaterAddressDontSendf59kuE',
                  'bio': 'Blockstream Explorer, the public block explorer of the company Blockstream, queried through its API on 2026-10-06',
                  'source': 'blockstream.info API, address 1BitcoinEaterAddressDontSendf59kuE, fetched 2026-10-06 during this build: funded 1,341,747,849 sat over 5,832 '
                            'outputs, spent 0 - the figures pinned in EATER below. Picture: the Bitcoin logo, Wikimedia Commons File:Bitcoin.svg, public domain - a '
                            'stand-in, since there is no picture of an address.',
                  'photo': 'photo_bitcoin_logo.png',
                  'credit': 'Bitcoin logo - Grayliptrot, public domain'}}
for _s in STORIES:
    _s.update(_OVERRIDES[_s["id"]])
