"""SEN0401 chapter 14 (Second-Layer Applications) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch14-evidence."""
__version__ = "1.2.0"  # each story's link goes straight to the resource and carries linkLabel, its title and kind (owner finding of 2026-10-16)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "PizzaForBitcoins", "bio": 'Laszlo Hanyecz, a programmer, offered 10,000 bitcoins for pizza; Jeremy Sturdivant, 19, took the offer on 22 May 2010', "title": "Two pizzas for 10,000 bitcoins",
     "when": "2010-05-22",
     "who": "Laszlo Hanyecz, a programmer who posted the offer and had contributed to Bitcoin's source code, and Jeremy Sturdivant, a 19-year-old in California who accepted it and ordered the pizzas",
     "where": "Jacksonville, Florida, USA, where the pizzas were delivered, and the Bitcoin Forum, where the offer was posted",
     "link": "https://bitcointalk.org/index.php?topic=137.0", "linkLabel": "Bitcointalk thread: Pizza for bitcoins?",
     "concepts": ["DoubleSpendRejected", "BookFeeVersusNetworkFee", "MainnetGraphSize", "LightningNoLongerProposed"],
     "story": ("On 18 May 2010, by the forum's clock, Laszlo Hanyecz opened the thread Pizza for bitcoins? and offered 10,000 bitcoins for a couple of pizzas delivered to Jacksonville, Florida. "
               "The Bitcoin Wiki dates the request to 17 May, which shows how a timestamp depends on the clock that wrote it. "
               "On 22 May 2010 a 19-year-old in California named Jeremy Sturdivant ordered two Papa John's pizzas to Hanyecz's home and received the 10,000 bitcoins, the first notable retail purchase of physical goods with bitcoin. "
               "A payment like that settles on the chain and waits for confirmations, the cost that payment channels and the Lightning Network were designed to avoid for small payments."),
     "lesson": "The first purchase settled on the chain; small ones now travel off it",
     "source": "bitcointalk_pizza_137.html (P63), wikipedia_history_of_bitcoin.html (P68), bitcoinwiki_laszlo_hanyecz.html (P61); the leaves BookFeeVersusNetworkFee and MainnetGraphSize",
     "credit": "Papa Johns Jacksonville - Sanjev Rajaram, CC0 1.0, Wikimedia Commons",
     "photo": "papa_johns_jacksonville.png"},
    {"id": "SpillmanChannels", "bio": 'Mike Hearn, a Bitcoin developer, opened the thread on 17 April 2013; Jeremy Spillman answered on 20 April 2013', "title": "The first payment channels",
     "when": "2013-04-20",
     "who": "Mike Hearn, who posted Anti DoS for tx replacement on 17 April 2013, Jeremy Spillman, who answered on 20 April 2013, and Matt Corallo, who with Hearn announced the bitcoinj implementation on 27 June 2013",
     "where": "the bitcoin-development mailing list, BitcoinTalk.org and the bitcoinj library",
     "link": "https://web.archive.org/web/2023/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2013-April/002433.html", "linkLabel": "Reply: Anti DoS for tx replacement (list post)",
     "concepts": ["EmmaFabianArithmetic", "FundingNeedsBothKeys", "RefundTimelockLadder", "NonExpiration"],
     "story": ("The Bitcoin Wiki traces payment channels to the first Bitcoin code, where an unrecorded open transaction could keep being replaced until its lock time, and to a personal email of Satoshi Nakamoto that described it. "
               "On 17 April 2013 Mike Hearn posted Anti DoS for tx replacement to the bitcoin-development mailing list, and on 20 April Jeremy Spillman replied with the one-way design that the book calls a Spillman-style channel. "
               "Hearn and Matt Corallo announced a micro-payment channels implementation in bitcoinj on 27 June 2013. "
               "The book adds that such channels were only safe with segwit transactions, which became available in 2017, which is why the refund in this chapter's Emma and Fabian test had to be signed before the funding was sent."),
     "lesson": "Channels began as a replaced transaction, waiting for its lock time",
     "source": "bitcoinwiki_payment_channels.html (P56), book_ch14_applications.adoc (P01); the leaves EmmaFabianArithmetic, FundingNeedsBothKeys and RefundTimelockLadder",
     "credit": "Micropayment channel - Burchert, Decker, Wattenhofer, CC BY 4.0, Wikimedia Commons",
     "photo": "micropayment_channel_construction.png"},
    {"id": "PoonDryjaWhitepaper", "bio": 'Joseph Poon and Thaddeus Dryja wrote the Lightning Network paper; Lightning Labs launched the network in 2018', "title": "A paper that became a network",
     "when": "2015-02-28",
     "who": "Joseph Poon and Thaddeus Dryja, the authors of the Lightning Network paper, and Lightning Labs, which launched the network in 2018",
     "where": "the website lightning.network, where the paper is kept, and the open specification repository of the BOLTs",
     "link": "https://lightning.network/lightning-network-paper.pdf", "linkLabel": "Poon and Dryja: Lightning paper (PDF)",
     "concepts": ["WhitepaperDate", "LightningNoLongerProposed", "AsymmetricCommitment", "HtlcSecretBranch"],
     "story": ("Joseph Poon and Thaddeus Dryja published a Lightning Network white paper in February 2015, and Wikipedia cites a copy of version 0.5 archived on 28 February 2015. "
               "The draft that lightning.network keeps today is version 0.5.9.2 of 14 January 2016, and the same site keeps a summary that calls the network a decentralized system for instant, high-volume micropayments that removes the risk of delegating custody of funds to trusted third parties. "
               "Lightning Labs launched the Lightning Network in 2018, and the picture is a chart of the number of cut nodes of the network, from under 100 in 2018 to about 1,500 in 2022, read approximately from the chart. "
               "The book's own sentence, that the network was first described in February 2015, holds, and the word proposed does not hold any more."),
     "lesson": "A design on paper took years, soft forks and four teams",
     "source": "wikipedia_lightning_network.html (P65), poon_dryja_lightning_paper.pdf (P23), poon_dryja_lightning_summary.pdf (P24); the leaf WhitepaperDate",
     "credit": "Lightning cut nodes - FrankAndProust, CC0 1.0, Wikimedia Commons",
     "photo": "lightning_cut_nodes.png"},
    {"id": "LightningTorch", "bio": 'hodlonaut, a pseudonymous Twitter user, began the torch on 19 January 2019 with 100,000 satoshis', "title": "Satoshis passed from hand to hand",
     "when": "2019-01-19",
     "who": "hodlonaut, a pseudonymous Twitter user who began the game, and the recipients who passed it on, among them Jack Dorsey, Charlie Lee, Elizabeth Stark of Lightning Labs and Changpeng Zhao of Binance",
     "where": "Twitter, and the Lightning Network, where each payment was sent",
     "link": "https://en.wikipedia.org/wiki/Lightning_Network", "linkLabel": "Wikipedia: Lightning Network (article)",
     "concepts": ["FeeArithmetic", "BalancesAfterPayment", "InvoiceStructure", "MainnetGraphSize"],
     "story": ("On 19 January 2019 the pseudonymous Twitter user hodlonaut began a game-like promotional test of the Lightning Network by sending 100,000 satoshis, 0.001 bitcoin, to a trusted recipient. "
               "Each recipient added 10,000 satoshis, which was 34 cents at the time, and sent the sum on to the next, so that the lightning torch reached well-known people such as Jack Dorsey, Charlie Lee, Elizabeth Stark and Changpeng Zhao. "
               "Each hand-over was an ordinary Lightning payment between people who had a channel or a route, without a transaction on the chain for each step, and the amount that stays after each hop is what the fee arithmetic of the book's Alice and Eric example predicts. "
               "The picture is a 2009 photograph of Jack Dorsey, one of the recipients, from a technology conference."),
     "lesson": "Lightning payments pass hand to hand without touching the chain",
     "source": "wikipedia_lightning_network.html (P65); the leaves FeeArithmetic and BalancesAfterPayment",
     "credit": "Jack Dorsey 2009 - Brian Solis, CC BY 2.0, Wikimedia Commons",
     "photo": "jack_dorsey_2009.png"},
]
RESOURCES = [   # (kind, title, url): each opened on 2026-10-15
    ("video", "Bitcoin Lightning Network Explained: How it Actually Works (CuriousInventor, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=yKdK-7AtAMQ"),
    ("video", "Bitcoin Lightning Transactions & Protocol Deep Dive (CuriousInventor, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=to8XItlplac"),
    ("video", "Coinbase Speaker Series: Joseph Poon and Thaddeus Dryja of Lightning Network (Coinbase, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=KN7Z5dGWcRY"),
    ("video", "Lightning Network Security and HTLC's on Lightning (Voltage, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=nvy-TCxUHYg"),
    ("video", "The Story of Bitcoin Pizza Day (Bitcoin Magazine, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=Cs6duadLaso"),
    ("video", "Lightning: Payments as Packets and the Future of Blockchain Transactions (HiveMumble, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=Ptdq9SL4684"),
    ("topic", "Bitcoin Optech topic: Hash Time Locked Contract (HTLC)", "https://bitcoinops.org/en/topics/htlc/"),
    ("topic", "Bitcoin Optech topic: Anchor outputs", "https://bitcoinops.org/en/topics/anchor-outputs/"),
    ("topic", "Bitcoin Optech topic: Watchtowers", "https://bitcoinops.org/en/topics/watchtowers/"),
    ("topic", "Bitcoin Optech topic: Client-side validation", "https://bitcoinops.org/en/topics/client-side-validation/"),
    ("explorer", "mempool.space, the Lightning Network explorer that supplied the statistics of this chapter", "https://mempool.space/lightning"),
    ("specification", "The BOLT repository: the Lightning specifications", "https://raw.githubusercontent.com/lightning/bolts/master/README.md"),
    ("documentation", "BOLT 3: Bitcoin transaction and script formats, with the test vectors", "https://raw.githubusercontent.com/lightning/bolts/master/03-transactions.md"),
    ("documentation", "BIP 68: relative lock-time using consensus-enforced sequence numbers", "https://bips.dev/68/"),
    ("documentation", "BIP 112: CHECKSEQUENCEVERIFY", "https://bips.dev/112/"),
    ("documentation", "BIP 431: topology restrictions for pinning (TRUC)", "https://bips.dev/431/"),
    ("documentation", "lnd, the Lightning Network Daemon: the documentation of Lightning Labs", "https://docs.lightning.engineering/"),
    ("book", "Mastering Bitcoin, the book site (Antonopoulos and Harding)", "https://bitcoinbook.info/"),
    ("paper", "Sphinx: a compact and provably secure mix format (Danezis and Goldberg, 2009)", "https://www.cypherpunks.ca/~iang/pubs/Sphinx_Oakland09.pdf"),
    ("paper", "The Bitcoin Lightning Network: scalable off-chain instant payments (Poon and Dryja, draft 0.5.9.2)", "https://lightning.network/lightning-network-paper.pdf"),
]
FIELDS = ("id", "bio", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")
FACTS = {   # story id -> (saved file, fragments that must be found in it)
    "PizzaForBitcoins": ("bitcointalk_pizza_137.txt", ["Pizza for bitcoins? May 18, 2010, 12:35:20 AM", "pay 10,000 bitcoins for a couple of pizzas", "Jacksonville, Florida zip code 32224"]),
    "PizzaForBitcoins2": ("wikipedia_history_of_bitcoin.txt", ["The first notable retail transaction involving physical goods took place on 22 May 2010", "A 19-year-old in California named Jeremy Sturdivant accepted the offer", "ordered two Papa John's pizzas"]),
    "PizzaForBitcoins3": ("bitcoinwiki_laszlo_hanyecz.txt", ["On May 17, 2010, laszlo posted a request to buy pizza with bitcoin", "laszlo had made contributions to Bitcoin's source code in the past"]),
    "SpillmanChannels": ("bitcoinwiki_payment_channels.txt", ["Anti DoS for tx replacement , Mike Hearn, bitcoin-development mailing list, 17 April 2013", "Re: Anti DoS for tx replacement , Jeremy Spillman, bitcoin-development mailing list, 20 April 2013", "Micro-payment channels implementation now in bitcoinj , Mike Hearn & Matt Corallo, BitcoinTalk.org, 27 June 2013", "An unrecorded open transaction can keep being replaced until nLockTime", "Satoshi Nakamoto described the technique to a Bitcoin developer in a personal email"]),
    "SpillmanChannels2": ("book_ch14_applications.adoc", ["Spillman-style payment channel, which was first described and implemented in 2013", "only safe to use with witness (segwit) transactions, which didn't become available until 2017"]),
    "PoonDryjaWhitepaper": ("wikipedia_lightning_network.txt", ["published a Lightning Network white paper in February 2015", "Archived from the original on 2015-02-28", "Lightning Labs launched the Lightning Network in 2018"]),
    "PoonDryjaWhitepaper2": ("poon_dryja_lightning_paper.txt", ["January 14, 2016 DRAFT Version 0.5.9.2"]),
    "PoonDryjaWhitepaper3": ("poon_dryja_lightning_summary.txt", ["The Lightning Network is a decentralized system for instant, high-volume micropayments that removes the risk of delegating custody of funds to trusted third parties"]),
    "LightningTorch": ("wikipedia_lightning_network.txt", ["On January 19, 2019, pseudonymous Twitter user hodlonaut began a game-like promotional test of the Lightning Network", "sending 100,000 satoshis (0.001 bitcoin) to a trusted recipient", "each recipient added 10,000 satoshis ($0.34 at the time)", "Jack Dorsey", "Charlie Lee", "Lightning Labs CEO Elizabeth Stark"]),
}


def run_checks():
    bad = []
    ev = os.path.join(HERE, "ch14-evidence")
    for s in STORIES:
        for f in FIELDS:
            v = s.get(f)
            if not v or "TODO" in str(v) or "CREDIT_" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(HERE, "..", "03-materials", "ch14", "assets", str(s.get("photo", "")))
        if not os.path.exists(p) or os.path.getsize(p) < 10000 or open(p, "rb").read(5) in (b"<!DOC", b"<html"):
            bad.append("%s: picture file %s missing or not a picture" % (s.get("id"), s.get("photo")))
        for k in [s["id"]] + [s["id"] + str(i) for i in range(2, 7)]:
            if k not in FACTS:
                continue
            fn, frs = FACTS[k]
            t = re.sub(r"\s+", " ", open(os.path.join(ev, fn), encoding="utf-8", errors="replace").read())
            for fr in frs:
                if re.sub(r"\s+", " ", fr) not in t:
                    bad.append("%s: fact %r not in %s" % (s["id"], fr, fn))
    if len(STORIES) < 4:
        bad.append("fewer than four stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
