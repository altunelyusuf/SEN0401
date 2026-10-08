"""SEN0401 chapter 6 - the story companion to the chapter corpus (version 1.0.0).

Chapter 6 (Transactions) under the owner's 5N1K rule: real, dated, sourced stories with one live link
each, enforced by this file's self-check. Four stories, four lessons, each tied to a field of the
transaction the chapter reads:

* FirstTransaction - 12 January 2009: Satoshi Nakamoto pays Hal Finney 10 BTC in block 170, the
  first transaction that spends an output - an outpoint to a coinbase, a legacy serialization, two
  pay-to-public-key outputs; the chapter's library parses it and recomputes its txid.
* PizzaDay - 22 May 2010: Laszlo Hanyecz's 10,000 BTC for two pizzas, a transaction with 131 inputs
  and one output - the input count, the outpoint and the fee made visible.
* ValueOverflow - 15 August 2010: block 74,638 carries a transaction whose two outputs sum past the
  64-bit integer; the amount range and Bitcoin Core's check that cites the bug.
* GoxMalleability - 10 February 2014: Mt. Gox halts withdrawals and blames transaction
  malleability - the third-party malleability of the witness branch, measured by researchers.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "FirstTransaction",
        "title": "Ten bitcoins to Hal Finney, block 170",
        "when": "2009-01-12",
        "who": "Satoshi Nakamoto (sender) and Hal Finney, cryptographer and the second person to run the software",
        "where": "block 170 of the blockchain; Finney's computer in California, running bitcoin since the day before",
        "link": "https://mempool.space/tx/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16",
        "concepts": ["Outpoint", "LegacyFormat", "MaturityRule", "Txid"],
        "story": ("On 11 January 2009 Hal Finney posted two words, running bitcoin, and the next day the "
                  "software's author sent him 10 BTC. The transaction, f4184fc5..., sits in block 170 and is "
                  "the first ever to spend an output: its single input points at the coinbase of block 9, "
                  "161 blocks earlier, and its two outputs pay 10 BTC to Finney's public key and 40 BTC back "
                  "to the sender. It is a legacy transaction - no marker, no flag, no witness - and the "
                  "chapter's own library parses it and recomputes its identifier from the bytes. Every field "
                  "this chapter reads was already there, unchanged, in 2009."),
        "lesson": "The format you are reading is the one from block 170",
        "source": ("The transaction f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16 as "
                   "saved in ch06-evidence from mempool.space on 2026-10-08: block 170, 275 bytes, one input "
                   "spending output 0 of 0437cd7f..., outputs of 10 BTC and 40 BTC; Finney's post of "
                   "2009-01-11 is on Wikimedia Commons as 'First tweet about bitcoin'. Photo: Hal Finney in "
                   "1972, Daily News-Post staff photo, public domain."),
    },
    {
        "id": "PizzaDay",
        "title": "10,000 bitcoins for two pizzas",
        "when": "2010-05-22",
        "who": "Laszlo Hanyecz, programmer in Jacksonville, Florida; the pizzas ordered by forum user jercos",
        "where": "a Papa John's on Atlantic Avenue, Jacksonville - the shop now carries a plaque",
        "link": "https://bitcointalk.org/index.php?topic=137.0",
        "concepts": ["InputCount", "Outpoint", "AmountField", "Weight"],
        "story": ("Four days after offering 10,000 BTC on the bitcointalk forum to anyone who would send him "
                  "two pizzas, Laszlo Hanyecz reported that the deal was done. The payment, a1075db5..., "
                  "confirmed in block 57,043 on 22 May 2010: 131 inputs, because his wallet gathered "
                  "mining rewards of 50 BTC each, and a single output of 10,000 BTC, with 0.99 BTC left "
                  "as the fee. The transaction is 23,620 bytes and, as a legacy transaction, weighs exactly "
                  "four times that. The chapter's library parses all 131 inputs and recomputes its "
                  "identifier; the bitcoin community marks 22 May as Pizza Day."),
        "lesson": "An input count of 131 is what one-output payments can look like",
        "source": ("The bitcointalk thread 'Pizza for bitcoins?' opened by laszlo on 2010-05-18 and his "
                   "report of 2010-05-22; the transaction "
                   "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d saved in ch06-evidence "
                   "from mempool.space: block 57,043, 131 inputs, 1 output of 1,000,000,000,000 satoshis, "
                   "fee 99,000,000 satoshis, weight 94,480. Photo: the plaque at Papa John's, Atlantic Ave, "
                   "Jacksonville, by Sanjev Rajaram, CC0."),
    },
    {
        "id": "ValueOverflow",
        "title": "The block that created 184 billion bitcoins",
        "when": "2010-08-15",
        "who": "an unknown attacker; Jeff Garzik, who reported the strange block on the forum; Satoshi Nakamoto, who patched the software the same day",
        "where": "block 74,638 - and the bitcointalk forum thread Strange block 74638, where the fix was coordinated within hours",
        "link": "https://en.bitcoin.it/wiki/Value_overflow_incident",
        "concepts": ["AmountField", "AmountRange", "ConsensusRule", "Coinbase"],
        "story": ("Block 74,638 contained a transaction with two outputs of 92,233,720,368.54277039 BTC each. "
                  "Added as 64-bit integers the two amounts overflowed to a small negative number, so the "
                  "check that outputs do not exceed inputs passed and the chain accepted 184 billion "
                  "bitcoins out of thin air. Jeff Garzik reported the block within two hours, Satoshi Nakamoto pushed a patch "
                  "within about five hours and released version 0.3.10 the next day with a check on the sum "
                  "of the outputs, and the honest chain overtook the bad one at block 74,691, erasing the "
                  "transaction. Bitcoin Core's tx_check.cpp still "
                  "cites the bug, CVE-2010-5139, beside the three refusals this chapter reads: a negative "
                  "value, a value above 21 million, a total that leaves the range."),
        "lesson": "A signed amount needs a range check; the chain learned it the hard way",
        "source": ("The Bitcoin wiki's 'Value overflow incident' page: block 74638 on 2010-08-15, two outputs "
                   "of 92,233,720,368.54277039 BTC, the 0.3.10 fix and the reorganisation at block 74691; "
                   "the forum thread 'Strange block 74638' (bitcointalk topic 822) with its timeline of the patch; "
                   "Bitcoin Core src/consensus/tx_check.cpp at commit 05bc2f5, '(see CVE-2010-5139)', saved "
                   "in ch06-evidence. Photo: Gavin Andresen, the developer to whom Satoshi handed the project "
                   "after this era, at Web Summit 2014 - Stephen McCarthy / Web Summit, CC BY 2.0."),
    },
    {
        "id": "GoxMalleability",
        "title": "Mt. Gox blames malleability",
        "when": "2014-02-10",
        "who": "Mt. Gox, then the largest bitcoin exchange, and its CEO Mark Karpeles; Christian Decker and Roger Wattenhofer of ETH Zurich, who measured the claim",
        "where": "Shibuya, Tokyo - and the whole Bitcoin network, whose relayed transactions the researchers recorded",
        "link": "https://arxiv.org/abs/1403.6676",
        "concepts": ["ThirdPartyMalleability", "PushEncoding", "ConflictingTransactions", "Segwit"],
        "story": ("On 7 February 2014 Mt. Gox halted bitcoin withdrawals, and on 10 February it issued a "
                  "press release blaming a bug in the bitcoin software: someone could alter transaction "
                  "details to make it seem that a sending of bitcoins had not occurred when it had. That is "
                  "third-party malleability - a stranger re-encodes a push in the input script, the txid "
                  "changes, and software that tracks payments by txid believes the payment failed. Decker "
                  "and Wattenhofer, who had recorded the network's transactions for a year, found no "
                  "widespread malleability attacks before the announcement: about 302,000 BTC were ever "
                  "involved in such attacks, and only 1,811 BTC of them before the press release. On 28 February the exchange filed for "
                  "bankruptcy protection, 850,000 BTC short; segregated witness, activated in 2017, took "
                  "the input script out of the txid for good."),
        "lesson": "Track outpoints, not txids - and do not blame the protocol first",
        "source": ("Decker and Wattenhofer, 'Bitcoin Transaction Malleability and MtGox', arXiv:1403.6676 "
                   "(ETH Zurich, March 2014; ESORICS 2014): the figures 302,000 BTC ever involved and 1,811 BTC "
                   "before the press release, and the finding of no widespread attacks before the closure; the Mt. Gox press release of 2014-02-10 and the "
                   "bankruptcy filing of 2014-02-28 as summarised at en.wikipedia.org/wiki/Mt._Gox. No "
                   "free-licence photograph of the exchange or its office could be verified, so the slide "
                   "shows the story's figures instead."),
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
    if "block 170" not in STORIES[0]["source"]:
        bad.append("FirstTransaction: block missing from source")
    if "131 inputs" not in STORIES[1]["source"]:
        bad.append("PizzaDay: input count missing from source")
    if "CVE-2010-5139" not in STORIES[2]["source"]:
        bad.append("ValueOverflow: the bug identifier missing from source")
    if "302,000 BTC" not in STORIES[3]["source"]:
        bad.append("GoxMalleability: the measured figure missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
