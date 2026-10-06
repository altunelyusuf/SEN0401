"""SEN0401 chapter 2 - the story companion to the chapter corpus (version 1.0.0).

Chapter 2 (How Bitcoin Works) gets the same treatment the owner ruled for chapter 1: real,
dated, sourced stories carried on the material itself under 5N1K (who/what/when/where/why/how),
each with one live link, enforced by this file's own self-check. Three stories anchor the
chapter's three hard ideas:

* WhitepaperMath - the nine pages of 2008-10-31 and their section 11, whose attacker catch-up
  table the deck RECOMPUTES live (examples group AttackerSuccess; the chapter research record
  already reproduced the paper's q=0.1 column to seven decimal places).
* FirstFaucet - how anyone got bitcoin before exchanges: Gavin Andresen gave it away, five
  coins at a time, which is the Acquisition concept with a date and a face.
* ValueOverflow - the day the rules caught a 184-billion-BTC forgery (block 74,638), which is
  why "every node checks every rule" is taught as the system's immune response, not a slogan.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "WhitepaperMath",
        "title": "Nine pages, one table of probabilities",
        "when": "2008-10-31",
        "who": "Satoshi Nakamoto, announcing on the metzdowd.com cryptography mailing list",
        "where": "bitcoin.org - a nine-page PDF",
        "link": "https://bitcoin.org/bitcoin.pdf",
        "concepts": ["Probability", "Confirmation", "DoubleSpend"],
        "story": ("On 31 October 2008 a pseudonymous author posted nine pages to a cryptography "
                  "mailing list. Section 11 does something unusual for a systems paper: it computes "
                  "the attacker's odds. Modelling the race between an honest chain and a secret one "
                  "as a binomial random walk, it tabulates the probability that an attacker with a "
                  "share q of the hash power ever catches up from z blocks behind. This deck does "
                  "not quote that table - it reruns the paper's own procedure and draws the result."),
        "lesson": "A confirmation is a probability statement, and you can compute it",
        "source": ("Nakamoto, 'Bitcoin: A Peer-to-Peer Electronic Cash System' (2008), section 11; "
                   "announcement of 2008-10-31 on the metzdowd.com cryptography list. The chapter "
                   "research record reproduced the paper's q=0.1 column - 0.2045873 at one "
                   "confirmation, 0.0002428 at six - to seven decimal places (examples group "
                   "AttackerSuccess reruns it for this deck)."),
    },
    {
        "id": "FirstFaucet",
        "title": "Five free bitcoins for every visitor",
        "when": "2010-06-11",
        "who": "Gavin Andresen, the developer Satoshi later handed the project to",
        "where": "freebitcoins.appspot.com, announced on the bitcointalk forum",
        "link": "https://bitcointalk.org/index.php?topic=141.0",
        "concepts": ["Acquisition", "Wallet", "ExchangeRate"],
        "story": ("In June 2010 there was almost nowhere to buy bitcoin, so a developer in "
                  "Massachusetts stocked a website with 1,100 of his own coins and gave five to "
                  "anyone who asked - solving a CAPTCHA was the only price. Thousands of people got "
                  "their first bitcoin from Gavin Andresen's faucet. The giveaway seeded the user "
                  "base the first exchanges and the first payments then grew from, and Andresen "
                  "went on to lead Bitcoin's development when Satoshi withdrew in 2011."),
        "lesson": "Before price discovery, distribution itself had to be invented",
        "source": ("Andresen's own announcement thread, bitcointalk.org topic 141, 2010-06-11: "
                   "'Get 5 free bitcoins from freebitcoins.appspot.com', initially stocked with "
                   "1,100 BTC. Photo: Web Summit 2014, CC BY 2.0."),
    },
    {
        "id": "ValueOverflow",
        "title": "The day someone printed 184 billion bitcoin",
        "when": "2010-08-15",
        "who": "An unknown attacker; spotted by developer Jeff Garzik; patched by Satoshi Nakamoto",
        "where": "block 74,638, discussed live on the bitcointalk forum",
        "link": "https://en.bitcoin.it/wiki/Value_overflow_incident",
        "concepts": ["ConsensusRules", "RuleChange", "BestBlockchain"],
        "story": ("On 15 August 2010 block 74,638 contained a transaction paying out about "
                  "184,467,440,737 BTC - thousands of times the 21 million cap. Two outputs were so "
                  "large that, summed as 64-bit integers, they overflowed to a small number and "
                  "slipped past the checks. Jeff Garzik flagged the 'strange block' on the forum "
                  "within the hour; Satoshi shipped version 0.3.10 with a corrected rule about five "
                  "hours after the block, and the honest chain, rebuilt without the forged coins, "
                  "overtook the bad one. The 184 billion bitcoins ceased to exist."),
        "lesson": "Validation by every node is the immune system - and it worked",
        "source": ("en.bitcoin.it/wiki/Value_overflow_incident: block 74,638 of 2010-08-15 "
                   "(two outputs of 92,233,720,368.54 BTC each), Garzik's 'Strange block 74638' "
                   "thread, Satoshi's 0.3.10 patch ~5 hours later, good chain ahead by block 74,691."),
    },
]


def run_checks():
    bad = []
    ids = [s["id"] for s in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for s in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(s.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (s["id"], f))
        if not s.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % s["id"])
        if len(s["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % s["id"])
        if not (2 <= s["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s["id"])
    # the numeric anchors each story leans on, pinned
    if "0.2045873" not in STORIES[0]["source"] or "0.0002428" not in STORIES[0]["source"]:
        bad.append("WhitepaperMath: the two table anchors missing from source")
    if "1,100 BTC" not in STORIES[1]["source"]:
        bad.append("FirstFaucet: the 1,100 BTC stock missing from source")
    if "74,638" not in STORIES[2]["source"] or "92,233,720,368.54" not in STORIES[2]["source"]:
        bad.append("ValueOverflow: block or overflow amount missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
