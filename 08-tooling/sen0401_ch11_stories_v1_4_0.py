"""SEN0401 chapter 11 (The Blockchain) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch11-evidence."""
__version__ = "1.4.0"  # TK_Ch11_StoryReplace_R1: the genesis-headline story is told in chapter 1 (slide 7) and must not be told again here (owner ruling 2026-11-26); replaced by the repeated coinbases of blocks 91722, 91812, 91842 and 91880 (14-15 November 2010), the reason of BIP 30 and BIP 34 and of slide 17; the overflow block 74638 was weighed and dropped because chapters 2 and 6 already tell it; sources P74-P84 saved in ch11-evidence (sources_index_v1_1_0.json). Before that, v1.3.0 - TK_Ch11_StoryNameFoldIn_R1: HeadlineInTheGenesisBlock's own story text named the Chancellor but never Satoshi Nakamoto, who the who-field also names; folded in on the coinbase-transaction sentence, no fact changed
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "TwoCoinbasesThatRepeated", "bio": 'Pieter Wuille wrote BIP 30 (assigned 22 February 2012) and Gavin Andresen BIP 34 (assigned 6 July 2012) after blocks 91842 and 91880 repeated the coinbase transactions of blocks 91812 and 91722 on 14 and 15 November 2010', "title": "The reward that was mined twice",
     "when": "2010-11-14",
     "who": "Pieter Wuille, who wrote BIP 30, Gavin Andresen, who wrote BIP 34, and the miners of blocks 91722, 91812, 91842 and 91880, whose names the chain does not record",
     "where": "the Bitcoin chain (blocks 91722, 91812, 91842 and 91880), the Bitcoin Core source file validation.cpp and the bitcoin/bips repository",
     "link": "https://bips.dev/30/", "linkLabel": "BIP 30: Duplicate transactions (spec)",
     "concepts": ["Bip34HeightInCoinbase", "HeightFromGenesis", "HeightAndMaturity", "CoinbaseMaturity100"],
     "story": ("On 14 November 2010 block 91812, mined at 17:59 UTC, paid its 50 coins in a coinbase transaction with the identifier d5d27987, and block 91842, mined three hours later, carried a coinbase with the same identifier. "
               "Blocks 91722 and 91880, mined about sixteen hours apart, repeated the identifier e3bf3d07 in the same way, because the two coinbases of each pair were the same bytes. "
               "Bitcoin Core marks the 50 coins of the earlier blocks 91722 and 91812 as unspendable, and its function IsBIP30Repeat lets the later blocks 91842 and 91880 through by their heights and hashes. "
               "In 2012 Pieter Wuille wrote BIP 30, which forbids a block to contain a transaction whose identifier matches an earlier transaction that is not fully spent, and Gavin Andresen wrote BIP 34, which puts the height of the block first in every coinbase script. "
               "Block 227,835 was the last version 1 block, the last that did not have to carry that height. "
               "In this chapter the height is read back from the coinbase scripts of eight blocks, and blocks 91842 and 91880 remain the only two that the rule against repeated identifiers lets through by exception."),
     "lesson": "Put the height in the coinbase and no two coinbases can be equal",
     "source": "mempool_block_91722.json, mempool_block_91812.json, mempool_block_91842.json, mempool_block_91880.json (P74-P77), mempool_txids_91722.json, mempool_txids_91812.json, mempool_txids_91842.json, mempool_txids_91880.json (P78-P81), mempool_coinbase_tx_d5d27987.json and mempool_coinbase_tx_e3bf3d07.json (P82, P83), core_src_validation.cpp (P24), bip-0030.mediawiki (P08), bip-0034.mediawiki (P09), photo_bitcoinqt_0_5_2_screenshot.png (P84); the Bip34HeightInCoinbase leaf",
     "credit": "Screenshot of Bitcoin-qt 0.5.2 on Windows 7 - the Bitcoin developers (Satoshi Nakamoto, Gavin Andresen, Jeff Garzik and others), MIT licence, Wikimedia Commons, 2012-02-21 (stand-in picture: the client of February 2012, the month BIP 30 was written)",
     "photo": "photo_bitcoinqt_0_5_2_screenshot.png"},
    {"id": "TheHashTreeOfRalphMerkle", "bio": 'Ralph Merkle, cryptographer, patented the hash tree in 1979 (United States patent 4309569, published 5 January 1982) at Stanford University', "title": "One small hash that vouches for a whole list",
     "when": "1982-01-05",
     "who": "Ralph Merkle, the cryptographer who patented the hash tree, and Stanford University, the assignee of the patent",
     "where": "Stanford University in California; United States patent 4309569, published on 5 January 1982",
     "link": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4309569", "linkLabel": "Merkle's patent US 4,309,569 (PDF)",
     "concepts": ["HashTreeHistory", "FourLeafTree", "TreeDepth", "RealBlockRoot", "MerklePathOf16"],
     "story": ("Ralph Merkle patented the hash tree in 1979, and the United States patent 4309569, Method of providing digital signatures, was published on 5 January 1982 with the Board of Trustees of Stanford University as assignee. "
               "The patent explains both the tree and how it handles many one-time signatures, and in 1980 Merkle wrote about tree authentication in his paper Protocols for Public Key Cryptosystems. "
               "Satoshi Nakamoto's paper hashes the transactions of a block in a Merkle tree and keeps only the root in the block header. "
               "In this chapter the 40 transaction ids of block 277,315 were hashed in pairs up six levels and gave the root 5e049f40..., the value in its header, and a path of 4 hashes proved one transaction among 16."),
     "lesson": "A small summary can vouch for a large list",
     "source": "wikipedia_merkle_tree.html (P52), merkle_1980_protocols.pdf (P41), nakamoto_2008_bitcoin.pdf (P39), mempool_txids_277315.json (P65); the RealBlockRoot and MerklePathOf16 leaves",
     "credit": "Ralph Merkle - david.orban (Flickr), CC BY 2.0, Wikimedia Commons",
     "photo": "photo_ralph_merkle.png"},
    {"id": "GriefingTheTestnet", "bio": 'Jameson Lopp, Bitcoin developer, described the testnet3 block storms on 4 May 2024; Fabian Jahr, Bitcoin Core contributor, wrote BIP 94 for testnet4', "title": "When the sandbox was flooded",
     "when": "2024-05-04",
     "who": "Jameson Lopp, who wrote the blog post, and Fabian Jahr, who wrote BIP 94 for testnet4",
     "where": "the blog of Jameson Lopp, the bitcoin/bips repository, and Bitcoin Core 28.0",
     "link": "https://bips.dev/94/", "linkLabel": "BIP 94: Testnet 4 (spec)",
     "concepts": ["TestnetBlockStorms", "Testnet4Replaces", "Bip94Rules", "Testnet3StillThere", "TestnetMinimumDifficulty"],
     "story": ("On 4 May 2024 Jameson Lopp published Griefing Bitcoin's Testnet, which describes how the testnet3 rule of minimum difficulty after 20 minutes lets miners create hundreds of blocks in a single day. "
               "Testnet4 had its genesis block on 3 May 2024 and BIP 94 was assigned to Fabian Jahr on 27 May 2024; it starts the retarget from the first block of the previous period and bounds the time of the first block of a period. "
               "Bitcoin Core 28.0 added the network with the option -testnet4. "
               "BIP 94 notes that three years' worth of blocks had been mined on testnet3 in a few weeks, and on 15 October 2026 testnet3 stood at height 5,189,394, against 156,618 on testnet4. "
               "Bitcoin Core 31.1 still starts testnet3 but says in its help that the support will be removed."),
     "lesson": "A test network without incentives needs rules against vandals",
     "source": "bitcoinwiki_testnet.html (P48), bip-0094.mediawiki (P12), core_relnotes_28.0.md (P33), bitcoind_help_31.1.txt (P38), mempool_testnet3_tip_height.txt (P70), mempool_testnet4_tip_height.txt (P69); the TestnetBlockStorms leaf",
     "credit": "Children in a sandpit - Shixart1985, CC BY 2.0, Wikimedia Commons",
     "photo": "photo_children_sandpit.png"},
    {"id": "SignetBlocksNeedASignature", "bio": 'Karl-Johan Alm, Bitcoin Core developer, and Anthony Towns, Bitcoin Core contributor, were assigned BIP 325 on 20 March 2019', "title": "A test network with a doorman",
     "when": "2019-03-20",
     "who": "Karl-Johan Alm and Anthony Towns, the authors of BIP 325",
     "where": "the bitcoin/bips repository, and Bitcoin Core 0.21.0",
     "link": "https://bips.dev/325/", "linkLabel": "BIP 325: Signet (spec)",
     "concepts": ["SignetChallengeIsMultisig", "SignetMagicFromChallenge", "SignetGenesisShared", "SignetSizeToday"],
     "story": ("BIP 325, Signet, was assigned on 20 March 2019 to Karl-Johan Alm and Anthony Towns: a test network in which a block is valid only if it carries a solution to a challenge script, so that its creators decide who may make blocks. "
               "Bitcoin Core 0.21.0 added the support, with one public signet maintained and personal signets possible with -signetchallenge. "
               "The challenge of the default signet is a 1-of-2 multisig of two keys, and its four message-start bytes, 0a03cf40, are the start of the double SHA-256 of that script. "
               "Its genesis block has the time 2020-09-01 00:00:00 UTC, and on 15 October 2026 its tip was at height 326,440, 2.27 times the 143,619 blocks of the book's listing. "
               "A signet that anyone could sign, with the challenge 51, ran on the test node of this chapter."),
     "lesson": "Replace mining by a signature and a test network stays calm",
     "source": "bip-0325.mediawiki (P11), core_relnotes_0.21.0.md (P32), optech_topic_signet.html (P44), mempool_signet_tip_height.txt (P68), book_ch11_blockchain.adoc (P01); the SignetChallengeIsMultisig and SignetMagicFromChallenge leaves",
     "credit": "Signet ring of Ramesses II - akhenatenator, CC0 1.0, Flickr",
     "photo": "photo_signet_ring.png"},
]
RESOURCES = [   # (kind, title, url): each opened on 2026-10-15
    ("video", "Blockchain 101 - A Visual Demo (Anders Brownworth, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=_160oMzblY8"),
    ("video", "What Actually Are Merkle Trees? (Chainlink, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=na_omeubyYo"),
    ("video", "Creating a Local Bitcoin Testnet / Regtest - Programming Bitcoin (YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=LLZNvl90PC0"),
    ("video", "Hashing Algorithms and Security - Computerphile (YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=b4b8ktEV4Bg"),
    ("topic", "Bitcoin Optech topic: Merkle tree vulnerabilities", "https://bitcoinops.org/en/topics/merkle-tree-vulnerabilities/"),
    ("topic", "Bitcoin Optech topic: Testnet", "https://bitcoinops.org/en/topics/testnet/"),
    ("topic", "Bitcoin Optech topic: Signet", "https://bitcoinops.org/en/topics/signet/"),
    ("topic", "Bitcoin Optech topic: Time warp attack", "https://bitcoinops.org/en/topics/time-warp/"),
    ("explorer", "mempool.space, the block explorer that supplied the real blocks of this chapter", "https://mempool.space/"),
    ("book", "Mastering Bitcoin, the book site (Antonopoulos and Harding)", "https://bitcoinbook.info/"),
    ("documentation", "Bitcoin.org Developer Guide: the block chain", "https://developer.bitcoin.org/devguide/block_chain.html"),
    ("documentation", "Bitcoin Core 31.0 release notes (the coinbase_tx object of getblock)", "https://bitcoincore.org/en/releases/31.0/"),
    ("transcript", "Karl-Johan Alm, Signet integration (Advancing Bitcoin 2020, transcript)", "https://diyhpl.us/wiki/transcripts/advancing-bitcoin/2020/2020-02-06-kalle-alm-signet-integration"),
    ("blog", "Jameson Lopp, The block storms of Bitcoin's testnet", "https://blog.lopp.net/the-block-storms-of-bitcoins-testnet/"),
]
FIELDS = ("id", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")
FACTS = {   # story id -> (saved file, fragments that must be found in it)
    "TwoCoinbasesThatRepeated": ("mempool_txids_91812.json", ["d5d27987d2a3dfc724e359870c6644b40e497bdc0589a033220fe15429d88599"]),
    "TwoCoinbasesThatRepeated2": ("mempool_txids_91842.json", ["d5d27987d2a3dfc724e359870c6644b40e497bdc0589a033220fe15429d88599"]),
    "TwoCoinbasesThatRepeated3": ("mempool_txids_91722.json", ["e3bf3d07d4b0375638d5f1db5255fe07ba2c4cb067cd81b84ee974b6585fb468"]),
    "TwoCoinbasesThatRepeated4": ("mempool_txids_91880.json", ["e3bf3d07d4b0375638d5f1db5255fe07ba2c4cb067cd81b84ee974b6585fb468"]),
    "TwoCoinbasesThatRepeated5": ("mempool_coinbase_tx_d5d27987.json", ['"value":5000000000', '"scriptsig":"0456720e1b00"']),
    "TwoCoinbasesThatRepeated6": ("core_src_validation.cpp", ["bool IsBIP30Repeat", "block_index.nHeight==91842", "block_index.nHeight==91880", "bool IsBIP30Unspendable", "block_height==91722", "block_height==91812"]),
    "TwoCoinbasesThatRepeated7": ("bip-0030.mediawiki", ["Authors: Pieter Wuille", "Assigned: 2012-02-22", "identifier matches that of an earlier, not-fully-spent transaction", "heights 91842 and 91880"]),
    "TwoCoinbasesThatRepeated8": ("bip-0034.mediawiki", ["Authors: Gavin Andresen", "Add height as the first item in the coinbase transaction's scriptSig", "227,835"]),
    "TheHashTreeOfRalphMerkle": ("wikipedia_merkle_tree.txt", ["who patented it in 1979", "patent 4309569", "Method of providing digital signatures", "published Jan 5, 1982", "Stanford"]),
    "TheHashTreeOfRalphMerkle2": ("merkle_1980_protocols.txt", ["Ralph C. Merkle"]),
    "TheHashTreeOfRalphMerkle3": ("nakamoto_2008_bitcoin.txt", ["hashed in a Merkle Tree"]),
    "GriefingTheTestnet": ("bitcoinwiki_testnet.txt", ["Jameson Lopp", "Griefing Bitcoin's Testnet", "May 4, 2024"]),
    "GriefingTheTestnet2": ("bip-0094.mediawiki", ["Assigned: 2024-05-27", "Fabian Jahr", "three years' worth of blocks were mined in a few weeks"]),
    "GriefingTheTestnet3": ("core_relnotes_28.0.md", ["Support for Testnet4 as specified in"]),
    "SignetBlocksNeedASignature": ("bip-0325.mediawiki", ["Assigned: 2019-03-20", "Karl-Johan Alm", "Anthony Towns"]),
    "SignetBlocksNeedASignature2": ("core_relnotes_0.21.0.md", ["This release adds support for signets", "One public signet is maintained"]),
}


def run_checks():
    bad = []
    ev = os.path.join(HERE, "ch11-evidence")
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
        p = os.path.join(HERE, "..", "03-materials", "ch11", "assets", str(s.get("photo", "")))
        if not os.path.exists(p) or os.path.getsize(p) < 10000 and not str(s.get("photo")).endswith(".jpg") or open(p, "rb").read(5) in (b"<!DOC", b"<html"):
            bad.append("%s: picture file %s missing or not a picture" % (s.get("id"), s.get("photo")))
        for k in [s["id"]] + [s["id"] + str(i) for i in range(2, 7)]:
            if k not in FACTS:
                continue
            fn, frs = FACTS[k]
            t = re.sub(r"\s+", " ", open(os.path.join(ev, fn), encoding="utf-8", errors="replace").read())
            for fr in frs:
                if re.sub(r"\s+", " ", fr) not in t:
                    bad.append("%s: fact %r not in %s" % (s["id"], fr, fn))
    # the times of the story: block times of the four blocks
    import datetime, json as _j
    def _t(h):
        return _j.load(open(os.path.join(ev, "mempool_block_%d.json" % h)))["timestamp"]
    t812, t842, t722, t880 = _t(91812), _t(91842), _t(91722), _t(91880)
    if datetime.datetime.fromtimestamp(t812, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M") != "2010-11-14 17:59":
        bad.append("TwoCoinbasesThatRepeated: block 91812 was not mined at 17:59 UTC on 14 November 2010")
    if not 2.9 * 3600 <= t842 - t812 <= 3.2 * 3600:
        bad.append("TwoCoinbasesThatRepeated: blocks 91812 and 91842 are not about three hours apart")
    if not 15.5 * 3600 <= t880 - t722 <= 16.5 * 3600:
        bad.append("TwoCoinbasesThatRepeated: blocks 91722 and 91880 are not about sixteen hours apart")
    if len(STORIES) < 4:
        bad.append("fewer than four stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
