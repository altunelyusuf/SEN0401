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
__version__ = "1.0.0"

STORIES = [
    {
        "id": "IronKey",
        "title": "Two guesses from 7,002 bitcoin",
        "when": "2021-01-12",
        "who": "Stefan Thomas, programmer (early bitcoin adopter, later Ripple's CTO)",
        "where": "an IronKey USB drive in a safe - and the front page of the New York Times",
        "link": "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html",
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
        "link": "https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki",
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
        "link": "https://en.wikipedia.org/wiki/Mt._Gox",
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
