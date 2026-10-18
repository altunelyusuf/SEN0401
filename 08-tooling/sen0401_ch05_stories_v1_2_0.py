"""SEN0401 chapter 5 - the story companion to the chapter corpus (version 1.0.0).

Chapter 5 (Wallet Recovery) under the owner's 5N1K rule: real, dated, sourced stories with one
live link each, enforced by this file's self-check. Three stories, three lessons:

* IronKey - Stefan Thomas, two guesses from 7,002 BTC: what this chapter's recovery codes
  exist to prevent.
* Bip39Birth - the 2013 proposal from SatoshiLabs that put twelve ordinary words between
  humans and 128 bits - the standard every slide of the middle sections executes.
* GoxColdFind - March 2014: a forgotten old-format wallet file surfaces with 200,000 BTC.
  Backups outlive the people who made them - test them, label them, keep them.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.2.0"  # each story link goes straight to the resource and carries linkLabel (owner finding of 2026-10-16)

STORIES = [
    {
        "id": "IronKey",
        "title": "Two guesses from 7,002 bitcoin",
        "when": "2021-01-12",
        "who": "Stefan Thomas, programmer (early bitcoin adopter, later Ripple's CTO)",
        "where": "an IronKey USB drive in a safe - and the front page of the New York Times",
        "link": "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html", "linkLabel": "Lost passwords lock millionaires out (NYT)",
        "concepts": ["RecoveryCodes", "DataLoss", "Memorization"],
        "story": ("In 2011 Stefan Thomas was paid 7,002 BTC for making an animated explainer about "
                  "bitcoin. He put the keys on an encrypted IronKey drive, wrote the password on a "
                  "paper he later lost, and the drive allows ten guesses before locking forever. By "
                  "January 2021, when the New York Times told the story, he had used eight. The "
                  "chapter you are in - recovery codes, written backups, backup TESTING - is the "
                  "discipline that makes this story impossible to repeat."),
        "lesson": "Memory is not a backup; a recovery code you never test is barely one",
        "source": ("The New York Times, 2021-01-12, 'Lost Passwords Lock Millionaires Out of Their "
                   "Bitcoin Fortunes': 7,002 BTC, ten guesses, eight used. Photo: Lift Conference "
                   "2015, CC BY 2.0 (the file page names Stefan Thomas)."),
    },
    {
        "id": "Bip39Birth",
        "title": "Twelve words between you and 128 bits",
        "when": "2013-09-10",
        "who": "Marek Palatinus and Pavol Rusnak (SatoshiLabs/Trezor), with Aaron Voisine and Sean Bowe",
        "where": "BIP 39, in the public bips repository",
        "link": "https://bips.dev/39/", "linkLabel": "BIP 39: Mnemonic code (spec)",
        "concepts": ["Bip39Code", "WordList", "RecoveryPassphrase"],
        "story": ("The team building the first hardware signing device faced a human problem: "
                  "nobody transcribes 128 raw bits correctly. Their 2013 proposal, BIP 39, encodes "
                  "entropy as ordinary words from a curated list of 2,048 - eleven bits a word, a "
                  "checksum folded in, a key-stretching function from words to seed. The slides "
                  "around this one do not describe that pipeline; they run it, word by word, "
                  "against the standard's own test vectors."),
        "lesson": "The recovery code is an interface standard between humans and entropy",
        "source": ("BIP 39, 'Mnemonic code for generating deterministic keys', authors Palatinus, "
                   "Rusnak, Voisine, Bowe, dated 2013-09-10, in bitcoin/bips. Photo: two Trezor "
                   "One devices by Gage Skidmore, CC BY-SA 3.0."),
    },
    {
        "id": "GoxColdFind",
        "title": "The 200,000 BTC in a forgotten wallet file",
        "when": "2014-03-21",
        "who": "Mt. Gox, weeks into its bankruptcy proceedings",
        "where": "an old-format wallet file, unused since June 2011",
        "link": "https://www.theregister.com/2014/03/21/mtgox_finds_200000_bitcoin_in_old_wallets/", "linkLabel": "MtGox finds 200,000 Bitcoin (The Register)",
        "concepts": ["WalletDatabase", "DataLoss", "BackupTesting"],
        "story": ("Chapter 1 told how Mt. Gox collapsed owing 850,000 BTC. Three weeks after the "
                  "bankruptcy filing came a twist: the company reported finding about 200,000 BTC "
                  "in an old-format wallet file that had sat unused since 2011. A file made by "
                  "software two generations older still held spendable keys - backups do not "
                  "expire. Those coins became the pool from which creditors, a decade later, began "
                  "to be repaid."),
        "lesson": "Wallet files hold keys forever - label, test, and never discard them blindly",
        "source": ("Mt. Gox announcement of 2014-03-20/21 reporting approximately 200,000 BTC "
                   "found in an old-format wallet; summarized with the bankruptcy chronology at "
                   "en.wikipedia.org/wiki/Mt._Gox."),
    },
]


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
    if "7,002 BTC" not in STORIES[0]["source"]:
        bad.append("IronKey: amount missing from source")
    if "2013-09-10" not in STORIES[1]["source"]:
        bad.append("Bip39Birth: date missing from source")
    if "200,000 BTC" not in STORIES[2]["source"]:
        bad.append("GoxColdFind: amount missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)


# ---------------------------------------------------------------------------------------------- 1.2.0: the story contract of the deck checks (owner's coordinator, 2026-10-19)
# Every story gets an ISO date (the day of the event the story is anchored to), a who that names real people or bodies, a where of three words or more, a licence-clear picture of
# the chapter's assets with its credit, and a further-reading link that answers from the build machine; the old fields not named here are unchanged.
_OVERRIDES = {'IronKey': {'when': '2021-01-12',
             'who': 'Stefan Thomas, the programmer who holds the locked IronKey drive, and Nathaniel Popper, the New York Times reporter who told the story',
             'where': 'an IronKey USB drive in a safe, and the front page of the New York Times',
             'bio': 'Stefan Thomas, German-born programmer in San Francisco and former chief technology officer of Ripple; Nathaniel Popper, technology reporter of the '
                    'New York Times',
             'story': 'In 2011 Stefan Thomas was paid 7,002 BTC for making a video that explained how bitcoin works. He put the keys on an encrypted IronKey drive, '
                      'wrote the password on a paper he later lost, and the drive allows ten guesses before it locks forever. By January 2021, when the New York Times '
                      'told the story, he had used eight of them. The chapter you are in - recovery codes, written backups, backup TESTING - is the discipline that '
                      'makes this story impossible to repeat.',
             'link': 'https://www.business-standard.com/article/international/a-german-programmer-has-two-guesses-to-unlock-bitcoin-worth-240-million-121011400070_1.html',
             'linkLabel': 'NYT via Business Standard (news)',
             'source': "Nathaniel Popper, The New York Times, 2021-01-12, 'Lost Passwords Lock Millionaires Out of Their Bitcoin Fortunes' (nytimes.com answers 403 from "
                       "the build machine; the article's opening is republished at business-standard.com on 2021-01-14, which the link uses): Stefan Thomas, 7,002 BTC, "
                       'an IronKey with ten guesses, eight used; the 2011 video reward is in Finance Magnates, 2021-01-13. Picture: Stefan Thomas at the Lift Conference '
                       '2015 (Wikimedia Commons, file page names him), Lift Conference, CC BY 2.0.',
             'photo': 'photo_stefan_thomas.jpg',
             'credit': 'Stefan Thomas, 2015 - Lift Conference, CC BY 2.0'},
 'Bip39Birth': {'when': '2013-09-10',
                'bio': 'Marek Palatinus (slush) and Pavol Rusnak (stick), Czech developers and founders of SatoshiLabs, the makers of the Trezor hardware wallet; Aaron '
                       'Voisine, developer of breadwallet; Sean Bowe, developer',
                'source': "BIP 39, 'Mnemonic code for generating deterministic keys', authors Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe, created "
                          '2013-09-10, in bitcoin/bips (bips.dev/39). Picture: two Trezor One hardware wallets - Gage Skidmore, CC BY-SA 3.0, Wikimedia Commons.',
                'photo': 'photo_trezor_pair.jpg',
                'credit': 'Trezor One devices - Gage Skidmore, CC BY-SA 3.0'},
 'GoxColdFind': {'when': '2014-03-21',
                 'who': 'Mark Karpeles, the chief executive of Mt. Gox, whose company made the statement, and Simon Sharwood, the reporter who covered it',
                 'where': "an old-format wallet file that held no bitcoins on the exchange's books",
                 'bio': 'Mark Karpeles, born 1985, French programmer and chief executive of Mt. Gox from 2011 until its collapse in 2014; Simon Sharwood, technology '
                        'journalist at The Register',
                 'story': 'Chapter 1 told how Mt. Gox collapsed owing 850,000 BTC. Three weeks after the bankruptcy filing came a twist: in a statement the company said '
                          'it had old-format wallets that it thought no longer held any bitcoins, opened one, and found about 200,000 BTC in it. A file made by software '
                          'two generations older still held spendable keys - backups do not expire. Those coins became part of the pool from which creditors, a decade '
                          'later, began to be repaid.',
                 'source': "Simon Sharwood, The Register, 2014-03-21, 'MtGox finds 200,000 Bitcoin in old wallets': the statement says the exchange 'had certain old "
                           "format wallets which were used in the past and which, MtGox thought, no longer held any bitcoins'; one held 200,000 BTC, a couple of "
                           'thousand more turned up elsewhere, leaving about 650,000 BTC missing; summarized with the bankruptcy chronology at '
                           'en.wikipedia.org/wiki/Mt._Gox. Picture: the Mt. Gox logo, Wikimedia Commons File:Logo of Mt. Gox.svg, author not recorded, public domain '
                           'text logo.',
                 'photo': 'photo_mtgox_logo.png',
                 'credit': 'Mt. Gox logo - author unknown, public domain'}}
for _s in STORIES:
    _s.update(_OVERRIDES[_s["id"]])
