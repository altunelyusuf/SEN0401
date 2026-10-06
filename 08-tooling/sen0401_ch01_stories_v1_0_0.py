#!/usr/bin/env python3
"""SEN0401 chapter 1 - the story companion to the chapter corpus (version 1.0.0).

The owner's ruling of 2026-10-06: the teaching materials need stories - the histories and
biographical notes of money, cryptography, digital currencies and Bitcoin - because stories make
concepts memorable. This module is the corpus layer for them: each story is short, dated, tied to
the chapter concepts it serves, and carries its sources. The deck and the interactive page read
stories from here and never invent their own.

Every story states facts checkable against its sources; the self-check at the bottom enforces the
structural rules (a lesson of at most 14 words, a non-empty source, a date or era on every story)
and re-checks the numeric claims the stories make. Nothing here contradicts the chapter corpus;
where a story touches a corpus concept, the concept list names it.

Usage: import STORIES; or run this file to execute the self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "StoneMoney",
        "title": "The island where money never moved",
        "when": "Yap, documented 1903",
        "concepts": ["Money", "PublicJournal"],
        "story": ("On the island of Yap, wealth was held in rai - limestone discs up to four metres wide, "
                  "far too heavy to move. When a stone changed owners, the stone stayed where it lay; what "
                  "changed was the community's shared memory of who owned it. One famous stone sank to the "
                  "sea floor in transit, and the islanders kept trading it anyway, because everyone agreed "
                  "it existed and whose it was."),
        "lesson": "Money is a ledger; Bitcoin makes the shared memory digital",
        "source": ("W. H. Furness III, The Island of Stone Money (1910); Milton Friedman, 'The Island of "
                   "Stone Money', Hoover Institution Working Paper E-91-3 (1991)."),
    },
    {
        "id": "GenesisHeadline",
        "title": "A newspaper headline carved into block zero",
        "when": "3 January 2009",
        "concepts": ["History", "PublicJournal"],
        "story": ("The first Bitcoin block ever mined carries a piece of that morning's newspaper: "
                  "'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'. It proves the "
                  "block could not have been made earlier than that headline, and at the same time records "
                  "why the system was built - in the middle of a banking crisis, by someone who wanted "
                  "money that needs no bailout and no bank."),
        "lesson": "The genesis block is both a timestamp and a manifesto",
        "source": ("Bitcoin genesis block coinbase text, block 0, 2009-01-03; The Times front page of "
                   "3 January 2009; https://en.wikipedia.org/wiki/Bitcoin (genesis block)."),
    },
    {
        "id": "FirstTransaction",
        "title": "The first person ever paid in bitcoin",
        "when": "January 2009",
        "concepts": ["Transfer", "History"],
        "story": ("Nine days after the genesis block, Satoshi Nakamoto sent 10 bitcoin to Hal Finney, a "
                  "veteran cryptographer who had answered the whitepaper with curiosity instead of "
                  "dismissal and famously tweeted 'Running bitcoin'. Finney had worked on PGP and had "
                  "built the first reusable proof-of-work system years before Bitcoin existed - the first "
                  "payment went to someone who had spent a career preparing for it."),
        "lesson": "A transfer needs no bank: one peer paid another, directly",
        "source": ("Bitcoin block 170, 2009-01-12, the first bitcoin transaction (Satoshi Nakamoto to "
                   "Hal Finney, 10 BTC); Hal Finney, 'Running bitcoin', twitter.com/halfin, 2009-01-10."),
    },
    {
        "id": "PizzaDay",
        "title": "Two pizzas for ten thousand bitcoin",
        "when": "22 May 2010",
        "concepts": ["Price", "Unit"],
        "story": ("For Bitcoin's first year and a half, nobody knew what a bitcoin was worth, because "
                  "nobody had ever bought anything with one. Then Laszlo Hanyecz, a Florida programmer, "
                  "offered 10,000 BTC on a forum to anyone who would bring him two pizzas - and someone "
                  "did. That order, the first known commercial purchase paid in bitcoin, is why 22 May is "
                  "still celebrated as Bitcoin Pizza Day: it is the day a floating price began to exist."),
        "lesson": "Price is discovered the first time someone actually pays",
        "source": ("Guinness World Records, 'First commercial Bitcoin transaction' (Laszlo Hanyecz, "
                   "2010-05-22, 10,000 BTC for two pizzas); bitcointalk.org thread 'Pizza for bitcoins?', "
                   "May 2010."),
    },
    {
        "id": "CypherpunkLineage",
        "title": "Forty years of failed digital money",
        "when": "1982 - 2008",
        "concepts": ["Foundations", "History"],
        "story": ("Bitcoin was not a first attempt. David Chaum designed blind-signature ecash in the "
                  "1980s and his company DigiCash went bankrupt; Adam Back built Hashcash's proof-of-work "
                  "in 1997 to price email spam; Wei Dai sketched b-money and Nick Szabo bit gold in 1998, "
                  "both unbuilt for want of a way to agree without a leader. Satoshi's 2008 whitepaper "
                  "cites them and adds the missing piece - proof-of-work as the voting weight of an "
                  "open network - turning four decades of near-misses into a running system."),
        "lesson": "Bitcoin's novelty is the combination; every part existed first",
        "source": ("S. Nakamoto, 'Bitcoin: A Peer-to-Peer Electronic Cash System' (2008), references; "
                   "A. Back, Hashcash (1997); W. Dai, b-money (1998); N. Szabo, bit gold; D. Chaum, "
                   "'Blind signatures for untraceable payments' (1982)."),
    },
    {
        "id": "MtGox",
        "title": "The exchange that lost everyone's coins",
        "when": "February 2014",
        "concepts": ["KeyControl", "Backup"],
        "story": ("Mt. Gox of Tokyo was once the world's largest bitcoin exchange, handling the large "
                  "majority of all trades. In February 2014 it halted withdrawals, filed for bankruptcy "
                  "and admitted that around 850,000 bitcoins held on customers' behalf were gone - the "
                  "customers had balances on a website, but the keys, and therefore the coins, had been "
                  "in someone else's hands all along. Creditors were still being repaid more than a "
                  "decade later."),
        "lesson": "Whoever holds the keys holds the coins - exchanges included",
        "source": ("Mt. Gox bankruptcy filing, Tokyo District Court, 2014-02-28, reporting approximately "
                   "850,000 BTC missing (about 750,000 of them customers'); widely reported, e.g. "
                   "en.wikipedia.org/wiki/Mt._Gox."),
    },
]


def run_checks():
    bad = []
    ids = [s["id"] for s in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for s in STORIES:
        if len(s["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % s["id"])
        if not s["source"].strip():
            bad.append("%s: no source" % s["id"])
        if not s["when"].strip():
            bad.append("%s: no date or era" % s["id"])
        if not (2 <= s["story"].count(". ") + 1 <= 6):
            bad.append("%s: story not 2-6 sentences" % s["id"])
    # numeric claims the stories make, re-checked
    if "10,000 BTC" not in STORIES[3]["source"]:
        bad.append("PizzaDay: amount missing from source line")
    if "850,000" not in STORIES[5]["source"]:
        bad.append("MtGox: amount missing from source line")
    if "2009-01-12" not in STORIES[2]["source"]:
        bad.append("FirstTransaction: block-170 date missing")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
    raise SystemExit(1 if b else 0)
