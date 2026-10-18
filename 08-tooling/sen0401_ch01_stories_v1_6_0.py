#!/usr/bin/env python3
"""SEN0401 chapter 1 - the story companion to the chapter corpus (version 1.4.0).

The owner's ruling of 2026-10-06: the teaching materials need stories - the histories and
biographical notes of money, cryptography, digital currencies and Bitcoin - because stories make
concepts memorable. This module is the corpus layer for them: each story is short, dated, tied to
the chapter concepts it serves, and carries its sources. The deck and the interactive page read
stories from here and never invent their own.

Every story states facts checkable against its sources; the self-check at the bottom enforces the
structural rules (a lesson of at most 14 words, a non-empty source, a date or era on every story)
and re-checks the numeric claims the stories make. Nothing here contradicts the chapter corpus;
where a story touches a corpus concept, the concept list names it.

1.1.0 adds, on the owner's direction of 2026-10-06: the MoneyEvolution story; PIZZA_VALUE, the
documented milestones of what the Pizza Day coins were worth (the current point fetched live on
2026-10-06 from two independent price APIs agreeing within 0.1 percent); and MONEY_KINDS, the
three-column comparison of traditional money, digital money and cryptocurrency the chapter
teaches from.

1.2.0, on the owner's 5N1K ruling of 2026-10-06: every story now answers who/where as its own
fields and carries one live link for further reading or watching, and the self-check refuses a
story missing any of them. The deck and page print these on the story itself.

1.3.0, on the owner's direction of 2026-10-06: the online-payments story (Confinity, X.com,
PayPal, and the dot-com digital-cash failures) and WHEN_MONEY_STOPS - dated, named, linked cases
from Kenya, Cyprus, Greece, Venezuela and Ukraine where cards, banks or cash stopped serving
people, and where even a government under attack turned to an open payment network. Every case
carries its own link and passes the 5N1K self-check.

1.4.0, on the owner's ruling of 2026-10-06 that "era 0..8" chart labels are not how the field
speaks: HALVINGS - the real halving dates, one row per 210,000-block era, the first five dated
from the chain itself (any explorer shows the block timestamps at heights 0, 210,000, 420,000,
630,000, 840,000), the rest marked as projections at the 10-minute target. The issuance chart
labels its axis from this table and from nowhere else.

Usage: import STORIES, PIZZA_VALUE, MONEY_KINDS, WHEN_MONEY_STOPS, HALVINGS; run for self-checks.
"""
__version__ = "1.6.0"  # each story link goes straight to the resource and carries linkLabel (owner finding of 2026-10-16)

STORIES = [
    {
        "id": "StoneMoney",
        "who": "the Yapese; documented by anthropologist W. H. Furness III",
        "where": "Yap, Micronesia",
        "link": "https://www.gutenberg.org/ebooks/72830", "linkLabel": "Furness: The Island of Stone Money (book)",
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
        "who": "Satoshi Nakamoto",
        "where": "block 0 of the chain itself",
        "link": "https://mempool.space/tx/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b", "linkLabel": "Genesis block coinbase, with the headline (tx)",
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
        "who": "Satoshi Nakamoto to Hal Finney",
        "where": "block 170",
        "link": "https://mempool.space/tx/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16", "linkLabel": "Satoshi to Finney, block 170 (tx)",
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
        "who": "Laszlo Hanyecz",
        "where": "the bitcointalk forum (Jacksonville, Florida)",
        "link": "https://www.guinnessworldrecords.com/world-records/696240-first-commercial-bitcoin-transaction", "linkLabel": "First commercial Bitcoin transaction (record)",
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
        "who": "Chaum, Back, Dai, Szabo - then Nakamoto",
        "where": "academic papers and mailing lists",
        "link": "https://bitcoin.org/bitcoin.pdf", "linkLabel": "Bitcoin white paper (PDF)",
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
        "who": "Mt. Gox, led by CEO Mark Karpeles",
        "where": "Tokyo; bankruptcy filed at the Tokyo District Court",
        "link": "https://techcrunch.com/2014/03/03/mt-gox-posts-new-statement-on-alleged-theft-bankruptcy-filing/", "linkLabel": "Mt.Gox filing statement, TechCrunch (news)",
        "title": "The exchange that lost everyone's coins",
        "when": "February 2014",
        "concepts": ["KeyControl", "Backup"],
        "story": ("Mt. Gox of Tokyo, led by Mark Karpeles, was once the world's largest bitcoin exchange, handling the large "
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
    {
        "id": "MoneyEvolution",
        "who": "ledger-keepers, from temple scribes to central banks",
        "where": "Mesopotamia, Lydia, China, and onward",
        "link": "https://www.money.org/money-museum/virtual-exhibits/hom", "linkLabel": "The History of Money (museum exhibit)",
        "title": "Five thousand years to digital cash",
        "when": "c. 3000 BCE - 2009",
        "concepts": ["Money", "History"],
        "story": ("Money keeps changing form: grain-ledger entries in Mesopotamia, the first struck coins in "
                  "Lydia around 600 BCE, paper notes in Song-dynasty China, goldsmiths' receipts becoming "
                  "bank money, and in 1971 the dollar's last tie to gold cut, leaving pure fiat. Cards and "
                  "online banking then made most money digital - but always as entries in some "
                  "institution's private ledger. Cryptocurrency is the next step on the same road: money "
                  "that is only a ledger, but a public one no single institution keeps."),
        "lesson": "Every form of money is a ledger; they differ in who keeps it",
        "source": ("Standard monetary history: Lydian electrum coinage (c. 7th-6th century BCE); "
                   "Song-dynasty jiaozi paper money; the 1971 Nixon gold-convertibility suspension; "
                   "Mastering Bitcoin 3e, ch. 1, on bitcoin as digital money."),
    },
    {
        "id": "OnlinePayments",
        "title": "The internet got payments - and new gatekeepers",
        "when": "1998 - 2002",
        "who": "Max Levchin and Peter Thiel (Confinity), Elon Musk (X.com)",
        "where": "Palo Alto, in the dot-com boom",
        "link": "https://www.sec.gov/Archives/edgar/data/1103415/000091205701533855/a2059025zs-1.htm", "linkLabel": "PayPal Form S-1, 2001 (SEC filing)",
        "concepts": ["History", "Transfer"],
        "story": ("The web could sell before it could pay: cards were unsafe to type and banks had no "
                  "internet rails. Confinity, founded 1998 by Max Levchin and Peter Thiel, and X.com, "
                  "founded 1999 by Elon Musk, raced to fix it, merged in 2000, and became PayPal - sold "
                  "to eBay for 1.5 billion dollars in 2002. The same boom's pure digital currencies, "
                  "Beenz and Flooz, died in the 2001 crash, taking their customers' balances with them. "
                  "Online payment was solved, but only as accounts on one company's private ledger - "
                  "the internet still had no cash."),
        "lesson": "The dot-com era digitised payments by adding middlemen, not by removing them",
        "source": ("en.wikipedia.org/wiki/PayPal (Confinity 1998, X.com 1999, merger 2000, eBay "
                   "acquisition 2002); en.wikipedia.org/wiki/Flooz.com and /wiki/Beenz.com "
                   "(both closed 2001 in the dot-com crash)."),
    },
    {
        "id": "WhenMoneyStops",
        "title": "When the money in your hand stops working",
        "when": "2007 - 2022",
        "who": "savers, the unbanked, and one government under invasion",
        "where": "Kenya, Cyprus, Greece, Venezuela, Ukraine",
        "link": "https://www.cnbc.com/2022/03/02/ukraine-dogecoin-other-cryptocurrencies-accepted-for-donations.html", "linkLabel": "CNBC: Ukraine accepts crypto donations (news)",
        "concepts": ["Money", "Characteristic", "Borderless"],
        "story": ("Money fails people in documented ways. Kenya, 2007: most adults had no bank, so "
                  "Safaricom's M-Pesa turned phone credit into the country's money rail. Cyprus, March "
                  "2013: banks closed for days and a levy took part of large deposits overnight. Greece, "
                  "summer 2015: capital controls capped ATM withdrawals at 60 euros a day. Venezuela, "
                  "2018: hyperinflation passed one million percent and wages evaporated between morning "
                  "and evening. Ukraine, February 2022: with war at the capital, the government itself "
                  "posted donation addresses and raised tens of millions of dollars in crypto within "
                  "days, run by Deputy Minister Alex Bornyakov, when ordinary rails were too slow."),
        "lesson": "Open digital money matters most exactly where banks, cards or cash stop",
        "source": ("en.wikipedia.org/wiki/M-Pesa (Safaricom, 2007); en.wikipedia.org/wiki/2012-2013_Cypriot_financial_crisis "
                   "(deposit levy, March 2013); en.wikipedia.org/wiki/Greek_government-debt_crisis (2015 capital controls, 60-euro limit); "
                   "en.wikipedia.org/wiki/Hyperinflation_in_Venezuela (over 1,000,000% in 2018); "
                   "CNBC 2022-03-02 and Fortune 2022-03-26 on Ukraine's official crypto donations (Alex Bornyakov, 35 million dollars within the first week)."),
    },
]

# The five cases, one per card on the slide and the page, each with its own link (5N1K).
WHEN_MONEY_STOPS = [
    ("Kenya", "2007", "No banks for most adults - M-Pesa made phones the payment rail",
     "https://en.wikipedia.org/wiki/M-Pesa"),
    ("Cyprus", "2013", "Banks shut for days; a levy took part of deposits overnight",
     "https://en.wikipedia.org/wiki/2012%E2%80%932013_Cypriot_financial_crisis"),
    ("Greece", "2015", "Capital controls: ATM withdrawals capped at 60 euros a day",
     "https://en.wikipedia.org/wiki/Greek_government-debt_crisis"),
    ("Venezuela", "2018", "Hyperinflation beyond 1,000,000% - wages melted in hours",
     "https://en.wikipedia.org/wiki/Hyperinflation_in_Venezuela"),
    ("Ukraine", "2022", "Under invasion, the state itself raised ~$35M in crypto in a week",
     "https://www.cnbc.com/2022/03/02/ukraine-dogecoin-other-cryptocurrencies-accepted-for-donations.html"),
]

# What the Pizza Day coins were worth - teaching milestones, each widely documented at its date;
# the final point was fetched live on 2026-10-06 from mempool.space and CoinGecko (85,409 and
# 85,387 USD/BTC, agreeing within 0.1 percent), 10,000 BTC = 854 million dollars.
PIZZA_VALUE = [
    ("2010-05", 41, "the two pizzas, as valued at the time of the purchase"),
    ("2011-02", 10_000, "bitcoin reaches dollar parity (1 BTC = 1 USD)"),
    ("2013-11", 10_000_000, "bitcoin first crosses 1,000 USD"),
    ("2017-12", 196_000_000, "the ~19,600 USD December 2017 peak"),
    ("2021-11", 690_000_000, "the 69,000 USD November 2021 high"),
    ("2026-10", 854_090_000, "live price fetched 2026-10-06, two independent APIs"),
]

# The halving schedule with its REAL dates. The first five rows are chain facts: the block at
# each height carries its timestamp, and any explorer shows it (the link below tabulates them
# all). Rows with est=True have not happened yet - they are projections at the protocol's
# 10-minute block target and are displayed with a leading "~" wherever they appear.
#   (era, axis_label, date, block_height, subsidy_btc, est)
HALVINGS = [
    (0, "2009",  "2009-01-03", 0,         50.0,       False),  # the genesis block itself
    (1, "2012",  "2012-11-28", 210_000,   25.0,       False),
    (2, "2016",  "2016-07-09", 420_000,   12.5,       False),
    (3, "2020",  "2020-05-11", 630_000,   6.25,       False),
    (4, "2024",  "2024-04-20", 840_000,   3.125,      False),
    (5, "~2028", None,         1_050_000, 1.5625,     True),
    (6, "~2032", None,         1_260_000, 0.78125,    True),
    (7, "~2036", None,         1_470_000, 0.390625,   True),
    (8, "~2040", None,         1_680_000, 0.1953125,  True),
]
HALVINGS_LINK = "https://en.bitcoin.it/wiki/Controlled_supply"

# Traditional money vs digital money vs cryptocurrency - the chapter's comparison.
MONEY_KINDS = {
    "axes": ["Issued by", "Exists as", "Who keeps the ledger", "Supply is set by", "Settles"],
    "Traditional (cash)": ["A central bank", "Paper and coin in hand", "No ledger - possession is the record",
                           "Monetary policy", "Hand to hand, instantly"],
    "Digital money (bank, card, e-money)": ["Commercial banks on a central bank base", "Entries in banks' private ledgers",
                                            "Banks and processors", "Monetary policy and credit", "Through intermediaries, in days"],
    "Cryptocurrency (bitcoin)": ["No one - issuance is in the protocol", "Entries in one public ledger",
                                 "Every node, together", "Fixed rules anyone can verify", "Peer to peer, in about an hour"],
}


def run_checks():
    bad = []
    ids = [s["id"] for s in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for s in STORIES:
        for f in ("who", "where", "link"):
            if not s.get(f, "").strip():
                bad.append("%s: missing %s (5N1K)" % (s["id"], f))
        if not s.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % s["id"])
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
    for c in WHEN_MONEY_STOPS:
        if len(c) != 4 or not c[3].startswith("http"):
            bad.append("WHEN_MONEY_STOPS: malformed case %r" % (c[0],))
    if [p[0] for p in PIZZA_VALUE] != sorted(p[0] for p in PIZZA_VALUE):
        bad.append("PIZZA_VALUE: milestones out of order")
    if PIZZA_VALUE[0][1] != 41 or PIZZA_VALUE[-1][1] != 854_090_000:
        bad.append("PIZZA_VALUE: endpoint values drifted")
    n = len(MONEY_KINDS["axes"])
    for k, v in MONEY_KINDS.items():
        if k != "axes" and len(v) != n:
            bad.append("MONEY_KINDS: %s has %d rows, axes %d" % (k, len(v), n))
    # the halving table: heights and subsidies re-derived from the protocol arithmetic, the
    # documented dates pinned, and every projection visibly marked
    for era, lab, d, h, sub, est in HALVINGS:
        if h != era * 210_000:
            bad.append("HALVINGS: era %d height %d is not era*210000" % (era, h))
        if sub != (50 * 10**8 >> era) / 10**8:
            bad.append("HALVINGS: era %d subsidy %r disagrees with the shift" % (era, sub))
        if est and (not lab.startswith("~") or d is not None):
            bad.append("HALVINGS: era %d is a projection but not marked '~'/dateless" % era)
        if not est and (d is None or lab != d[:4]):
            bad.append("HALVINGS: era %d label %r does not match its date %r" % (era, lab, d))
    if [x[2] for x in HALVINGS if not x[5]] != ["2009-01-03", "2012-11-28", "2016-07-09",
                                                "2020-05-11", "2024-04-20"]:
        bad.append("HALVINGS: the documented dates drifted")
    if not HALVINGS_LINK.startswith("http"):
        bad.append("HALVINGS_LINK is not a URL")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
    raise SystemExit(1 if b else 0)


# ---------------------------------------------------------------------------------------------- 1.6.0: the story contract of the deck checks (owner's coordinator, 2026-10-19)
# Every story gets an ISO date (the day of the event the story is anchored to), a who that names real people or bodies, a where of three words or more, a licence-clear picture of
# the chapter's assets with its credit, and a further-reading link that answers from the build machine; the old fields not named here are unchanged.
_OVERRIDES = {'StoneMoney': {'when': '2024-01-30',
                'who': 'William Henry Furness III, the American anthropologist who visited Yap in 1903, and the Yapese owners of the stones',
                'where': 'the island of Yap in the Caroline Islands, Micronesia',
                'bio': 'William Henry Furness III (1866-1920), American anthropologist and physician, visited Yap in 1903 and published his account in September 1910',
                'story': 'On the island of Yap, wealth was held in rai - limestone discs up to four metres wide, far too heavy to move. When a stone changed owners, the '
                         "stone stayed where it lay; what changed was the community's shared memory of who owned it. The anthropologist William Henry Furness III "
                         'visited the island in 1903 and described the stones in his book of 1910, which Project Gutenberg released as a free ebook on 30 January 2024. '
                         'One famous stone sank to the sea floor in transit, and the islanders kept trading it anyway, because everyone agreed it existed and whose it '
                         'was.',
                'link': 'https://www.gutenberg.org/ebooks/72830',
                'linkLabel': 'Furness: The Island of Stone Money (book)',
                'source': 'W. H. Furness III, The Island of Stone Money (Philadelphia: J. B. Lippincott, published September 1910; free ebook 72830 released '
                          "2024-01-30); Milton Friedman, 'The Island of Stone Money', Hoover Institution Working Paper E-91-3 (1991). Picture: Yap Stone Money.jpg, Eric "
                          'Guinther, CC BY-SA 3.0, Wikimedia Commons.',
                'photo': 'photo_rai_stone.jpg',
                'credit': 'Yap stone money - Eric Guinther, CC BY-SA 3.0'},
 'GenesisHeadline': {'when': '2009-01-03',
                     'who': 'Satoshi Nakamoto, the pseudonymous creator of Bitcoin, who mined block 0',
                     'where': 'block 0 of the Bitcoin chain, the genesis block',
                     'bio': 'Satoshi Nakamoto, pseudonym of the author of the Bitcoin white paper (2008) and of the first software (2009); identity unknown',
                     'story': "The first Bitcoin block ever mined carries a piece of that morning's newspaper: 'The Times 03/Jan/2009 Chancellor on brink of second "
                              "bailout for banks'. It proves the block could not have been made earlier than that headline. It also records why the system was built - "
                              'in the middle of a banking crisis, by someone who wanted money that needs no bailout and no bank.',
                     'link': 'https://mempool.space/tx/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
                     'linkLabel': 'Genesis block coinbase, the headline (tx)',
                     'source': 'Bitcoin genesis block coinbase text, block 0, 2009-01-03; The Times front page of 3 January 2009; en.wikipedia.org/wiki/Bitcoin (genesis '
                               "block). Picture: the block's 285 bytes fetched from blockstream.info/api and rendered for this course by Yusuf Altunel, CC BY 4.0.",
                     'photo': 'genesis_hexdump.png',
                     'credit': 'Block 0 hex dump - Yusuf Altunel, CC BY 4.0'},
 'FirstTransaction': {'when': '2009-01-12',
                      'who': 'Satoshi Nakamoto, who sent the coins, and Hal Finney, the cryptographer who received them',
                      'where': 'block 170 of the Bitcoin chain',
                      'bio': 'Hal Finney (1956-2014), American cryptographer, PGP developer and creator of the first reusable proof-of-work system (RPOW), first to run '
                             'Bitcoin besides its author',
                      'story': 'Nine days after the genesis block, Satoshi Nakamoto sent 10 bitcoin to Hal Finney, a veteran cryptographer who had answered the '
                               "whitepaper with curiosity instead of dismissal and famously tweeted 'Running bitcoin'. Finney had worked on PGP and had built the first "
                               'reusable proof-of-work system years before Bitcoin existed. The first payment went to someone who had spent a career preparing for it.',
                      'source': "Bitcoin block 170, 2009-01-12, the first bitcoin transaction (Satoshi Nakamoto to Hal Finney, 10 BTC); Hal Finney, 'Running bitcoin', "
                                'twitter.com/halfin, 2009-01-10. Picture: Hal Finney, 1972, Daily News-Post, public domain, Wikimedia Commons.',
                      'photo': 'photo_hal_finney_1972.jpg',
                      'credit': 'Hal Finney, 1972 - Daily News-Post, public domain'},
 'PizzaDay': {'when': '2010-05-22',
              'link': 'https://www.guinnessworldrecords.com/world-records/696240-first-commercial-bitcoin-transaction',
              'linkLabel': 'Guinness: first Bitcoin purchase (record)',
              'who': 'Laszlo Hanyecz, the programmer who offered the coins, and Jeremy Sturdivant, the student who ordered the pizzas for him',
              'where': "the bitcointalk forum, and a Papa John's in Jacksonville, Florida",
              'bio': 'Laszlo Hanyecz, Hungarian-American programmer in Jacksonville, Florida, who mined bitcoin on graphics cards in 2010',
              'story': "For Bitcoin's first year and a half, nobody knew what a bitcoin was worth, because nobody had ever bought anything with one. Then Laszlo "
                       'Hanyecz, a Florida programmer, offered 10,000 BTC on a forum to anyone who would bring him two pizzas - and Jeremy Sturdivant, a student in '
                       "California, did, ordering two Papa John's pizzas for delivery to Jacksonville. That order, the first known commercial purchase paid in bitcoin, "
                       'is why 22 May is still celebrated as Bitcoin Pizza Day: it is the day a floating price began to exist.',
              'source': "Guinness World Records, 'First commercial Bitcoin transaction' (Laszlo Hanyecz, 2010-05-22, 10,000 BTC for two pizzas); bitcointalk.org thread "
                        "'Pizza for bitcoins?', May 2010. Picture: the plaque at Papa John's, Atlantic Ave, Jacksonville, photo Sanjev Rajaram, CC0, Wikimedia Commons.",
              'photo': 'photo_papa_johns_jacksonville.jpg',
              'credit': "Papa John's plaque - Sanjev Rajaram, CC0"},
 'CypherpunkLineage': {'when': '2008-10-31',
                       'who': 'David Chaum, Adam Back, Wei Dai and Nick Szabo, the cryptographers whose ideas Satoshi Nakamoto cited and combined',
                       'where': 'academic papers and cryptography mailing lists, 1982 to 2008',
                       'bio': 'David Chaum, born 1955, American cryptographer, founder of DigiCash; Adam Back, British cryptographer, inventor of Hashcash (1997); Wei '
                              'Dai, b-money (1998); Nick Szabo, bit gold (1998)',
                       'story': 'Bitcoin was not a first attempt. David Chaum designed blind-signature ecash in the 1980s and his company DigiCash went bankrupt; Adam '
                                "Back built Hashcash's proof-of-work in 1997 to price email spam; Wei Dai sketched b-money and Nick Szabo bit gold in 1998, both unbuilt "
                                'for want of a way to agree without a leader. On 31 October 2008 Satoshi Nakamoto announced the white paper on a cryptography mailing '
                                'list; it cites them and adds the missing piece, proof-of-work as the voting weight of an open network. That turned four decades of '
                                'near-misses into a running system.',
                       'source': "S. Nakamoto, 'Bitcoin: A Peer-to-Peer Electronic Cash System' (2008, announced 2008-10-31), references; A. Back, Hashcash (1997); W. "
                                 "Dai, b-money (1998); N. Szabo, bit gold; D. Chaum, 'Blind signatures for untraceable payments' (1982).",
                       'photo': 'photo_david_chaum_2018.jpg',
                       'credit': 'David Chaum, 2018 - Harry Murphy, CC BY 2.0'},
 'MtGox': {'when': '2014-02-28',
           'who': 'Mark Karpeles, the chief executive of Mt. Gox, and the Tokyo District Court that received its bankruptcy filing',
           'where': 'Tokyo, where the exchange was based and where its bankruptcy was filed',
           'bio': 'Mark Karpeles, born 1985, French programmer and chief executive of Mt. Gox from 2011 until its collapse in 2014',
           'story': "Mt. Gox of Tokyo, led by Mark Karpeles, was once the world's largest bitcoin exchange, handling the large majority of all trades. On 28 February "
                    "2014 it filed for bankruptcy at the Tokyo District Court and admitted that around 850,000 bitcoins held on customers' behalf were gone. The "
                    "customers had balances on a website, but the keys, and therefore the coins, had been in someone else's hands all along; creditors were still being "
                    'repaid more than a decade later.',
           'photo': 'photo_mtgox_logo.png',
           'credit': 'Mt. Gox logo - author unknown, public domain'},
 'MoneyEvolution': {'when': '1971-08-15',
                    'who': "Richard Nixon, the American president who suspended the dollar's convertibility into gold, after temple scribes, Lydian kings and goldsmiths "
                           'had each reshaped money',
                    'where': 'Mesopotamia, Lydia, Song China and the United States, from 3000 BCE to 1971',
                    'bio': 'Richard Nixon (1913-1994), thirty-seventh president of the United States, announced on 15 August 1971 that the dollar would no longer be '
                           'exchanged for gold',
                    'story': 'Money keeps changing form: grain-ledger entries in Mesopotamia, the first struck coins in Lydia around 600 BCE, paper notes in '
                             "Song-dynasty China, goldsmiths' receipts becoming bank money. On 15 August 1971 President Richard Nixon cut the dollar's last tie to gold, "
                             "leaving pure fiat money. Cards and online banking then made most money digital - but always as entries in some institution's private "
                             'ledger, and cryptocurrency is the next step on the same road: money that is only a ledger, but a public one no single institution keeps.',
                    'source': 'Standard monetary history: Lydian electrum coinage (c. 7th-6th century BCE); Song-dynasty jiaozi paper money; the Nixon announcement of '
                              '1971-08-15 suspending gold convertibility; Mastering Bitcoin 3e, ch. 1, on bitcoin as digital money. Picture: Stater with a lion, 600-550 '
                              'BCE, Cleveland Museum of Art open access, CC0.',
                    'photo': 'photo_cma_stater.jpg',
                    'credit': 'Electrum stater, 600-550 BCE - Cleveland Museum of Art, CC0',
                    'money_picture': True},
 'OnlinePayments': {'when': '2002-07-08',
                    'who': 'Max Levchin and Peter Thiel, who founded Confinity, and Elon Musk, who founded X.com; eBay, which bought the merged PayPal',
                    'where': 'Palo Alto and San Jose, California, in the dot-com boom',
                    'bio': 'Max Levchin, Peter Thiel and Elon Musk, founders of Confinity (1998) and X.com (1999), which merged in 2000 to form PayPal',
                    'story': 'The web could sell before it could pay: cards were unsafe to type and banks had no internet rails. Confinity, founded 1998 by Max Levchin '
                             'and Peter Thiel, and X.com, founded 1999 by Elon Musk, raced to fix it, merged in 2000, and became PayPal - which eBay agreed to buy on 8 '
                             "July 2002 for 1.5 billion dollars. The same boom's pure digital currencies, Beenz and Flooz, died in the 2001 crash, taking their "
                             "customers' balances with them. Online payment was solved, but only as accounts on one company's private ledger - the internet still had no "
                             'cash.',
                    'link': 'https://en.wikipedia.org/wiki/PayPal',
                    'linkLabel': 'PayPal (encyclopedia article)',
                    'source': 'PayPal history as summarised at en.wikipedia.org/wiki/PayPal: Confinity (December 1998), X.com (1999), the merger of 2000 and the eBay '
                              'purchase announced on 8 July 2002 for 1.5 billion dollars (CNET News.com, 2002-07-08). The PayPal Form S-1 of 2001 answers 403 from the '
                              'build machine and is not linked.',
                    'photo': 'photo_paypal_logo.png',
                    'credit': 'PayPal logo - PayPal, public domain'},
 'WhenMoneyStops': {'when': '2022-02-26',
                    'who': "Mykhailo Fedorov, Ukraine's minister of digital transformation, whose ministry published the donation addresses",
                    'where': 'Kenya, Cyprus, Greece, Venezuela and Ukraine, from 2007 to 2022',
                    'bio': 'Mykhailo Fedorov, born 1991, Ukrainian minister of digital transformation and vice prime minister, whose ministry ran the official crypto '
                           'donation drive of 2022',
                    'story': "Money fails people in documented ways. Kenya, 2007: most adults had no bank, so Safaricom's M-Pesa turned phone credit into the country's "
                             'money rail. Cyprus, March 2013: banks closed for days and a levy took part of large deposits overnight. Greece, summer 2015: capital '
                             'controls capped ATM withdrawals at 60 euros a day. Venezuela, 2018: hyperinflation passed one million percent and wages evaporated between '
                             'morning and evening. Ukraine, 26 February 2022: with war at the capital, the government itself posted crypto donation addresses and '
                             'raised, with an aid group, 54.7 million dollars in about a week, when ordinary rails were too slow.',
                    'link': 'https://nbclosangeles.com/news/business/money-report/ukraine-has-raised-more-than-54-million-as-bitcoin-donations-pour-in-to-support-the-war-against-russia/2840244',
                    'linkLabel': "CNBC: Ukraine's crypto donations (news)",
                    'source': "MacKenzie Sigalos, CNBC, 2022-03-03, 'Ukraine Has Raised More Than $54 Million as Bitcoin Donations Pour in to Support the War Against "
                              "Russia' (read on nbclosangeles.com, which republishes CNBC's Money Report; cnbc.com itself answers 403 from the build machine): the "
                              'government began soliciting crypto on 26 February 2022, and by 3 March 102,000 donations worth 54.7 million dollars had gone to it and to '
                              'Come Back Alive, per Elliptic; M-Pesa (2007), Cyprus (2013), Greece (2015), Venezuela (2018) as linked on the slide. Picture: Mykhailo '
                              'Fedorov at Diia Center, Bucha, 19 July 2023, U.S. Embassy Kyiv, public domain.',
                    'photo': 'photo_fedorov_portrait.jpg',
                    'credit': 'Fedorov - U.S. Embassy Kyiv, PD'}}
for _s in STORIES:
    _s.update(_OVERRIDES[_s["id"]])
