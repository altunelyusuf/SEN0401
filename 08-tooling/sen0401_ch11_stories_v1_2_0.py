"""SEN0401 chapter 11 (The Blockchain) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch11-evidence."""
__version__ = "1.2.0"  # each story's link goes straight to the resource and carries linkLabel, its title and kind (owner finding of 2026-10-16)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "HeadlineInTheGenesisBlock", "bio": 'Satoshi Nakamoto, pseudonymous creator of Bitcoin, mined the first block on 3 January 2009 and quoted The Times; Alistair Darling was then Chancellor of the Exchequer', "title": "A newspaper headline nailed into the first block",
     "when": "2009-01-03",
     "who": "Satoshi Nakamoto, the pseudonymous creator of Bitcoin, and Alistair Darling, then Chancellor of the Exchequer of the United Kingdom, whose office the headline names",
     "where": "the first block of the Bitcoin chain, quoting The Times of London",
     "link": "https://mempool.space/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f", "linkLabel": "Genesis block 0 on mempool.space (block)",
     "concepts": ["GenesisCoinbaseMessage", "ChancellorOfTheHeadline", "GenesisHashRecomputed", "GenesisCoinbaseUnspendable", "TimestampField"],
     "story": ("The genesis block of Bitcoin has the timestamp 1231006505, which is 18:15:05 UTC on 3 January 2009. "
               "Its single coinbase transaction carries 69 characters of free text: The Times 03/Jan/2009 Chancellor on brink of second bailout for banks. "
               "The Chancellor of the Exchequer at that date was Alistair Darling, who served under Gordon Brown from 2007 to 2010, and the newspaper began in 1785 as The Daily Universal Register. "
               "The text shows that the block cannot be older than that day, and the book adds that it was meant as a reminder of the need for an independent monetary system. "
               "In this chapter the block was rebuilt from the constants in chainparams.cpp and hashed to 000000000019d668..., and its 50 coins are the first that can never be spent."),
     "lesson": "A date quoted inside a block proves the block is not older",
     "source": "core_src_kernel_chainparams.cpp (P20), mempool_block_0.json (P59), wikipedia_alistair_darling.html (P55), wikipedia_the_times.html (P56), bitcoinwiki_genesis_block.html (P46), book_ch11_blockchain.adoc (P01); the GenesisHashRecomputed and GenesisCoinbaseUnspendable leaves",
     "credit": "Bust of Satoshi Nakamoto, Budapest - Fekist, CC BY-SA 4.0, Wikimedia Commons",
     "photo": "photo_satoshi_bust_budapest.png"},
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
    "HeadlineInTheGenesisBlock": ("core_src_kernel_chainparams.cpp", ['pszTimestamp = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"']),
    "HeadlineInTheGenesisBlock2": ("mempool_block_0.json", ['"timestamp":1231006505']),
    "HeadlineInTheGenesisBlock3": ("wikipedia_alistair_darling.txt", ["served as Chancellor of the Exchequer under Prime Minister Gordon Brown from 2007 to 2010"]),
    "HeadlineInTheGenesisBlock4": ("wikipedia_the_times.txt", ["It began in 1785 under the title The Daily Universal Register"]),
    "HeadlineInTheGenesisBlock5": ("bitcoinwiki_genesis_block.txt", ["can't be spent due to a quirk"]),
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
    if len(STORIES) < 4:
        bad.append("fewer than four stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
