"""SEN0401 chapter 7 - the story companion to the chapter corpus (version 1.0.0).

Chapter 7 (Authorization and Authentication) under the owner's 5N1K rule: real, dated, sourced stories with one live link each,
enforced by this file's self-check. Chapter 6 already told the first transaction, the pizza, the value overflow and Mt. Gox, so
this chapter tells three others, each tied to a script rule the chapter runs:

* OpReturnBug - 28 July 2010: two bugs found on the test network, one of which let a stranger spend coins that were not theirs
  because OP_RETURN ended the joined script with a true result; fixed in 0.3.5, and the disabled opcodes of that week are
  today's OP_SUCCESS opcodes of tapscript.
* DerFork - 4 July 2015: the activation of strict DER signatures (BIP66); about half the hash rate mined on top of an invalid
  block without checking it, and a six-block fork followed.
* SchnorrToTaproot - from a patented signature to the soft fork of 14 November 2021 (block 709,632), whose key path spends
  look like the signature of one person.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "OpReturnBug",
        "title": "The script that ended with a true result",
        "when": "2010-07-28",
        "who": "Satoshi Nakamoto, the author of the software; the people who found two bugs and showed them on the test network",
        "where": "the Bitcoin test network, in the first release line of the software (0.3.x); the lesson is carved into every later script engine",
        "link": "https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures",
        "concepts": ["OpReturnBug", "SeparateExecution", "OpSuccess"],
        "story": ("On 28 July 2010 two bugs were discovered and demonstrated on the test network. One of them, recorded as "
                  "CVE-2010-5141, let an attacker spend coins that they did not own: the first software joined the input script and "
                  "the output script into one program and treated OP_RETURN as a jump to the end, so an input script of 1 followed "
                  "by OP_RETURN ended the run with a true value and the output script never ran. The bug was never exploited on "
                  "the main network and was fixed in version 0.3.5, and by version 0.3.7 the two scripts run one after the other "
                  "and OP_RETURN fails. After the discovery many unused script words were disabled for safety, and the chapter's "
                  "library shows that today's tapscript turns disabled values such as OP_LSHIFT, number 152, into OP_SUCCESS "
                  "opcodes, which make a script succeed on purpose."),
        "lesson": "Run the two scripts separately, and fail closed on anything unknown",
        "source": ("The Bitcoin Wiki entry on Common Vulnerabilities and Exposures, saved in ch07-evidence: CVE-2010-5141, 2010-07-28, "
                   "wxBitcoin and bitcoind, 'OP_RETURN could be used to spend any output', fixed in 0.3.5, never exploited on the main "
                   "network; the sources of Bitcoin 0.3.0 and 0.3.7 (script.cpp), whose difference the chapter's library reproduces; "
                   "BIP342 on OP_SUCCESS opcodes; the book's chapter 7 section on separate execution. Photo: the bronze bust of "
                   "Satoshi Nakamoto in Graphisoft Park, Budapest, unveiled on 16 September 2021 - Fekist, CC BY-SA 4.0."),
        "photo": "photo_satoshi_bust_budapest.jpg",
        "credit": "Bust of Satoshi Nakamoto, Budapest - Fekist, CC BY-SA 4.0",
    },
    {
        "id": "DerFork",
        "title": "Half the miners did not check the block",
        "when": "2015-07-04",
        "who": "the miners who enforced BIP66 and the roughly half of the hash rate that mined without validating; the Bitcoin Core developers who wrote the alert",
        "where": "the Bitcoin network from block 363,725; the mining pools whose software built on an unchecked block",
        "link": "https://bitcoin.org/en/alert/2015-07-04-spv-mining",
        "concepts": ["SignatureEncoding", "SignatureChecking", "StatelessVerification"],
        "story": ("BIP66 made strict DER the only valid encoding of a signature, and it took effect once 950 of the last 1,000 "
                  "blocks were version 3, which happened early on 4 July 2015, at block 363,725. A small miner that had not upgraded "
                  "then produced an invalid block, as was expected, but roughly half of the network's hash rate was mining without "
                  "fully validating blocks and built on top of it, so a fork of 6 blocks lasted from 02:10 to 03:50 UTC and a second "
                  "of 3 blocks followed on 5 July. No double spend was seen in the first fork; several large miners lost income, and "
                  "the alert advised users of lightweight wallets to wait 30 more confirmations. Bitcoin Core 0.9.5 and later "
                  "were unaffected because they checked the rule."),
        "lesson": "A rule that you do not check for yourself protects nobody",
        "source": ("The Bitcoin.org network alert 'Some Miners Generating Invalid Blocks', 4 July 2015, last updated 15 July 2015, saved "
                   "in ch07-evidence: the 950-of-1,000 threshold, the roughly 50 percent of hash rate that was SPV mining, the "
                   "forks of 6 blocks (4 July, 02:10 to 03:50 UTC) and 3 blocks (5 July), no double spend in the first, the 30 extra "
                   "confirmations; BIP66 and Bitcoin Core's chainparams for the activation height 363,725 (block timestamp 01:54:32 UTC, "
                   "mempool.space). Photo: a bitcoin mining farm, 14 June 2014 - Marko Ahtisaari, CC BY 2.0; it is a general "
                   "view of mining hardware and not of the 2015 pools."),
        "photo": "photo_bitcoin_mining_farm.jpg",
        "credit": "A bitcoin mining farm, 2014 - Marko Ahtisaari, CC BY 2.0",
    },
    {
        "id": "SchnorrToTaproot",
        "title": "From a patented signature to one key for a million people",
        "when": "2021-11-14",
        "who": "Claus-Peter Schnorr, who invented the signature scheme; Pieter Wuille, Jonas Nick, Tim Ruffing and Anthony Towns, the authors of BIPs 340, 341 and 342",
        "where": "block 709,632, mined on 14 November 2021, the block at which the taproot rules took effect",
        "link": "https://mempool.space/block/0000000000000000000687bca986194dc2c1f949318629b44bb54ec0a94d8244",
        "concepts": ["Taproot", "KeyPathSpending", "ScriptlessMultisignature"],
        "story": ("Claus Schnorr patented the signature algorithm he discovered and kept it out of open standards and open-source "
                  "software for almost two decades, so cryptographers of the early 1990s built the DSA family that led to the ECDSA "
                  "signatures Bitcoin used from its first release. BIP340 was assigned in January 2020 to standardise Schnorr "
                  "signatures on Bitcoin's curve, BIP341 and BIP342 added the taproot output and tapscript, and the rules took effect at "
                  "block 709,632 on 14 November 2021, a block of 2,043 transactions. Bitcoin Core's source still notes the height, "
                  "with a warning height one miner confirmation window later at 711,648. A payment such as Alice's in the chapter "
                  "spends such an output with one 64-byte signature, which looks the same whether one person or a million made it."),
        "lesson": "Patents delayed Schnorr for decades; a soft fork brought it to every wallet",
        "source": ("The book's chapter 8, section 'ECDSA Signatures' (the patent, 'almost two decades', ECDSA the only signature "
                   "algorithm until the taproot soft fork in 2021); BIP340 (assigned 2020-01-19, 64-byte Schnorr signatures); BIP341 "
                   "and BIP342; Bitcoin Core src/kernel/chainparams.cpp at commit 05bc2f5, 'taproot activation height + miner "
                   "confirmation window'; the block record from mempool.space: height 709,632, timestamp 2021-11-14 05:15:27 UTC, "
                   "2,043 transactions. Photo: Claus-Peter Schnorr at Oberwolfach, 1986 - Konrad Jacobs (Mathematisches "
                   "Forschungsinstitut Oberwolfach), CC BY-SA 2.0 de."),
        "photo": "photo_claus_schnorr_1986.jpg",
        "credit": "Claus-Peter Schnorr, Oberwolfach, 1986 - Konrad Jacobs, MFO, CC BY-SA 2.0 de",
    },
]


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story", "photo", "credit"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
    if "CVE-2010-5141" not in STORIES[0]["source"]:
        bad.append("OpReturnBug: the bug identifier missing from source")
    if "950-of-1,000" not in STORIES[1]["source"]:
        bad.append("DerFork: the threshold missing from source")
    if "709,632" not in STORIES[2]["source"]:
        bad.append("SchnorrToTaproot: the block missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
