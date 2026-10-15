"""SEN0401 chapter 10 (The Bitcoin Network) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch10-evidence."""
__version__ = "1.1.0"  # the FilterIdeaPost read link is the BIP 157 page (the list archive answered 418 on the day of the deck); 1.1.0: PNG copies of the four JPEG pictures, bio fields, credits without dates and without the stand-in remark (the deck labels stand-ins)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "CompactBlockRelay", "bio": 'Matt Corallo, Bitcoin Core developer who built the relay network for miners, was assigned BIP 152 on 27 April 2016; Suhas Daftuar wrote the Bitcoin Core code', "title": "Sending a block as a list of short codes",
     "when": "2016-04-27",
     "who": "Matt Corallo, a Bitcoin Core and relay-network developer, and Suhas Daftuar, who wrote the Bitcoin Core implementation",
     "where": "the bitcoin/bips repository on GitHub, and Bitcoin Core 0.13.0, released in August 2016",
     "link": "https://bips.dev/152/",
     "concepts": ["CompactBlocks", "ShortIdsAreSixBytes", "CoinbaseIsPrefilled", "CompactBlocksYear", "RelayNetworkHistory"],
     "story": ("On 27 April 2016 the number 152 was assigned to the BIP Compact Block Relay by Matt Corallo. "
               "His idea was that a node already knows most of the transactions of a new block from its mempool, so the block can be sent as a header, a short code of 6 bytes for each transaction and the few transactions the receiver cannot have, such as the coinbase. "
               "Bitcoin Core 0.13.0 lists compact blocks as a pull request of Suhas Daftuar, and the BIP is marked Deployed. "
               "Corallo had earlier built a relay network for miners, and the book dates the compact blocks to a release of 2015, which is a year too early. "
               "In the run of this chapter a block of 13 transactions was sent as 332 bytes instead of 3,062."),
     "lesson": "Do not resend what the receiver already knows",
     "source": "bip-0152.mediawiki (P14), core_relnotes_0.13.0.md (P22), book_ch10_network.adoc (P01); the run's ShortIdsAreSixBytes and CompactBlocksYear leaves",
     "credit": "Optical fibre strands - BigRiz, CC BY-SA 3.0, Wikimedia Commons",
     "photo": "photo_optical_fibre.png"},
    {"id": "BloomFiltersLeak", "bio": 'Mike Hearn and Matt Corallo wrote BIP 37 (assigned 24 October 2012); Arthur Gervais, ETH Zurich, showed the leak in 2014', "title": "The filter that told on the wallet",
     "when": "2012-10-24",
     "who": "Mike Hearn and Matt Corallo, who wrote BIP 37, and Arthur Gervais, Srdjan Capkun, Ghassan Karame and Damian Gruber of ETH Zurich, who tested it",
     "where": "the bitcoin/bips repository, the ETH Zurich security group, and Bitcoin Core 0.19, which turned the service off by default in 2019",
     "link": "https://eprint.iacr.org/2014/763",
     "concepts": ["BloomFilters", "ToyBloomFilter", "BloomDisabledByDefault", "BloomFilterWireFormat"],
     "story": ("BIP 37 was assigned to Mike Hearn and Matt Corallo on 24 October 2012: a light client would send a Bloom filter of its addresses to a full node and receive only matching transactions. "
               "In 2014 Arthur Gervais and colleagues at ETH Zurich showed, analytically and empirically, that the reliance on Bloom filters in existing clients leaks considerable information about the addresses of the user. "
               "In 2015 BIP 111 added the service bit NODE_BLOOM so that a node could say whether it offered the service. "
               "Bitcoin Core 0.19.0.1 changed the option peerbloomfilters to false, and in the census of 2026-10-15 only 4,308 of 25,361 nodes still set the bit. "
               "The test node of this chapter closed the connection of a peer that sent filterload."),
     "lesson": "A privacy tool can leak more than it hides",
     "source": "bip-0037.mediawiki (P08), gervais_2014_bloom_privacy.html (P57), bip-0111.mediawiki (P09), core_relnotes_0.19.0.1.md (P23), bitnodes_snapshot_latest.json (P73); the run's BloomDisabledByDefault leaf",
     "credit": "Bloom filter diagram - David Eppstein, public domain, Wikimedia Commons",
     "photo": "photo_bloom_filter_diagram.png"},
    {"id": "FilterIdeaPost", "bio": 'A developer writing as bfd posted the idea on 9 May 2016; Olaoluwa Osuntokun, Lightning Labs, and Alex Akselrod wrote BIP 157 and 158', "title": "An anonymous post turned the filter around",
     "when": "2016-05-09",
     "who": "an anonymous developer who wrote as bfd, and Olaoluwa Osuntokun and Alex Akselrod, who wrote BIP 157 and 158",
     "where": "the bitcoin-dev mailing list, and the Lightning Labs project Neutrino",
     "link": "https://bips.dev/157/",
     "concepts": ["BlockFilters", "FilterIdeaPost2016", "GolombWorkedExample", "BasicFilterParameters", "FiltersOverP2P"],
     "story": ("On Monday 9 May 2016 a developer writing as bfd posted to the bitcoin-dev list the message Committed Bloom filters for improved wallet performance and SPV security. "
               "The idea was to turn the Bloom filter around: the full node makes one small filter for each block, and the light client downloads it and tests its own addresses, so that the client never reveals them. "
               "Olaoluwa Osuntokun and Alex Akselrod wrote it as BIP 157 and BIP 158, and replaced the Bloom filter by a Golomb-coded set, a form of compression named after the mathematician Solomon Golomb. "
               "Lightning Labs built the light client Neutrino on it. "
               "The independent code of this chapter reproduced all ten test vectors of BIP 158."),
     "lesson": "Reverse the question and the leak disappears",
     "source": "ml_bfd_2016-05_committed_bloom.html (P66), bip-0157.mediawiki (P16), bip-0158.mediawiki (P17), neutrino_README.md (P67), bip-0158_testnet-19.json (P68); the run's BasicFilterParameters leaf",
     "credit": "Solomon W. Golomb - National Science Foundation, public domain, Commons",
     "photo": "photo_solomon_golomb.png"},
    {"id": "EclipseAtUsenix", "bio": 'Ethan Heilman, Boston University, presented the paper with Alison Kendler, Aviv Zohar and Sharon Goldberg at USENIX Security on 12 August 2015', "title": "Eight connections, one liar",
     "when": "2015-08-12",
     "who": "Ethan Heilman and Alison Kendler of Boston University, Aviv Zohar of the Hebrew University of Jerusalem and Sharon Goldberg of Boston University",
     "where": "the 24th USENIX Security Symposium in Washington, D.C., 12 to 14 August 2015",
     "link": "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman",
     "concepts": ["EclipseAttack", "ConnectionTypes", "DnsSeedList", "AddrGossipFormat"],
     "story": ("At the USENIX Security Symposium in Washington, D.C., which began on 12 August 2015, Ethan Heilman, Alison Kendler, Aviv Zohar and Sharon Goldberg presented Eclipse Attacks on Bitcoin's Peer-to-Peer Network. "
               "They showed that an adversary controlling enough IP addresses could monopolize all connections to and from a victim node, and then use the victim for double spending, selfish mining or adversarial forks. "
               "They measured the resources needed with Monte Carlo simulations and experiments on live nodes, and proposed countermeasures. "
               "Bitcoin Core now keeps anchor connections and two block-relay-only connections, and chooses peers from different autonomous systems. "
               "The chapter's census shows the other side of the problem: 12,488 of 25,361 reachable nodes are onion addresses."),
     "lesson": "A node is only as honest as the peers it happens to meet",
     "source": "heilman_2015_eclipse.txt (P52), optech_topic_eclipse_attacks.html (P61), core_src_net.h (P33); the run's ConnectionTypes leaf",
     "credit": "Total solar eclipse - NASA / Aubrey Gemignani, public domain, Commons",
     "photo": "photo_total_solar_eclipse_2017.png"},
    {"id": "EncryptionAtLast", "bio": 'Jonas Schnelli proposed BIP 151 in 2016; Dhruv Mehta, Tim Ruffing, Jonas Schnelli and Pieter Wuille were assigned BIP 324 on 8 March 2019', "title": "From a closed proposal to the default",
     "when": "2019-03-08",
     "who": "Dhruv Mehta, Tim Ruffing, Jonas Schnelli and Pieter Wuille, the authors of BIP 324; Jonas Schnelli had written the earlier BIP 151",
     "where": "the bitcoin/bips repository, and the releases Bitcoin Core 26.0 (December 2023) and 27.0 (April 2024)",
     "link": "https://bips.dev/324/",
     "concepts": ["EncryptedV2", "V2DefaultHistory", "UnauthenticatedTransport", "PlaintextV1"],
     "story": ("Jonas Schnelli proposed encrypting peer connections in BIP 151 on 23 March 2016, a proposal that drew mixed comments and was closed with a replacement named. "
               "On 8 March 2019 BIP 324, Version 2 P2P Encrypted Transport Protocol, was assigned to Dhruv Mehta, Tim Ruffing, Jonas Schnelli and Pieter Wuille, and it replaces BIP 151. "
               "Bitcoin Core 26.0 added it as an option that is off by default, and 27.0 made it the default. "
               "The BIP is explicit that the transport is encrypted but not authenticated. "
               "In the run of this chapter the v2 stream showed neither the magic bytes nor the word version, and 21,768 of the 25,361 nodes of the census advertise the P2P_V2 bit."),
     "lesson": "Defaults decide how private a network is",
     "source": "bip-0324.mediawiki (P19), bip-0151.mediawiki (P13), core_relnotes_26.0.md (P27), core_relnotes_27.0.md (P28), bitnodes_snapshot_latest.json (P73); the run's EncryptedV2 leaf",
     "credit": "Enigma machine - Rama, CC BY-SA 2.0 FR, Wikimedia Commons",
     "photo": "photo_enigma_machine.png"},
]
RESOURCES = [   # (kind, title, url): each opened on 2026-10-15
    ("video", "USENIX Security '15 - Eclipse Attacks on Bitcoin's Peer-to-Peer Network (USENIX, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=b-qGTj2Vvns"),
    ("video", "Neutrino: The Privacy Preserving Bitcoin Light Client (SF Bitcoin Developers, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=7FWKc8lM4Ek"),
    ("video", "Bloom Filters, Visualized (Generalist Programmer, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=HxAnFcEn0K4"),
    ("topic", "Bitcoin Optech topic: Compact block relay", "https://bitcoinops.org/en/topics/compact-block-relay/"),
    ("topic", "Bitcoin Optech topic: Version 2 P2P transport", "https://bitcoinops.org/en/topics/v2-p2p-transport/"),
    ("topic", "Bitcoin Optech topic: Compact block filters", "https://bitcoinops.org/en/topics/compact-block-filters/"),
    ("census", "Bitnodes, live map of reachable Bitcoin nodes", "https://bitnodes.io/"),
    ("book", "Mastering Bitcoin, the book site (Antonopoulos and Harding)", "https://bitcoinbook.info/"),
    ("documentation", "Bitcoin Core 31.0 release notes (cluster mempool, orphanage, startingheight)", "https://bitcoincore.org/en/releases/31.0/"),
    ("paper", "Eclipse Attacks on Bitcoin's Peer-to-Peer Network (USENIX Security 2015)", "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman"),
]
FIELDS = ("id", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")
FACTS = {   # story id -> (saved file, fragments that must be found in it)
    "CompactBlockRelay": ("bip-0152.mediawiki", ["Assigned: 2016-04-27", "Matt Corallo", "Status: Deployed"]),
    "CompactBlockRelay2": ("core_relnotes_0.13.0.md", ["compact blocks (sdaftuar)"]),
    "CompactBlockRelay3": ("book_ch10_network.adoc", ["In 2015, a new version of Bitcoin Core added a feature called"]),
    "BloomFiltersLeak": ("bip-0037.mediawiki", ["Assigned: 2012-10-24", "Mike Hearn", "Matt Corallo"]),
    "BloomFiltersLeak2": ("gervais_2014_bloom_privacy.txt", ["We show analytically and empirically that the reliance on Bloom filters within existing SPV clients leaks considerable information ab", "Damian Gruber", "Srdjan Capkun"]),
    "BloomFiltersLeak3": ("bip-0111.mediawiki", ["Assigned: 2015-08-20", "NODE_BLOOM"]),
    "FilterIdeaPost": ("ml_bfd_2016-05_committed_bloom.txt", ["Date: Mon, 09 May 2016", "Committed bloom filters for improved wallet performance and SPV security"]),
    "FilterIdeaPost2": ("bip-0158.mediawiki", ["Olaoluwa Osuntokun", "Alex Akselrod", "Golomb-Rice coding"]),
    "EclipseAtUsenix": ("heilman_2015_eclipse.txt", ["24th USENIX Security Symposium", "August 12–14, 2015", "Ethan Heilman", "Alison Kendler", "Aviv Zohar", "Sharon Goldberg", "Monte Carlo simu-"]),
    "EncryptionAtLast": ("bip-0324.mediawiki", ["Assigned: 2019-03-08", "Dhruv Mehta", "Tim Ruffing", "Jonas Schnelli", "Pieter Wuille", "Replaces: 151"]),
    "EncryptionAtLast2": ("bip-0151.mediawiki", ["Assigned: 2016-03-23", "Status: Closed", "Controversial"]),
    "EncryptionAtLast3": ("core_relnotes_26.0.md", ["It is off by default"]),
    "EncryptionAtLast4": ("core_relnotes_27.0.md", ["BIP324 v2 transport is now enabled by default"]),
}


def run_checks():
    bad = []
    ev = os.path.join(HERE, "ch10-evidence")
    for s in STORIES:
        for f in FIELDS:
            v = s.get(f)
            if not v or "TODO" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(HERE, "..", "03-materials", "ch10", "assets", str(s.get("photo", "")))
        if not os.path.exists(p):
            bad.append("%s: picture file %s missing" % (s.get("id"), s.get("photo")))
        for k in [s["id"]] + [s["id"] + str(i) for i in range(2, 6)]:
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
