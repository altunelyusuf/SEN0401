"""SEN0401 chapter 10 (The Bitcoin Network) for the RDODI build (generic builder sen0401_rdodi_build_v1_1_0.py).
The data module assembles: the source table (sen0401_ch10_sources_v1_0_0), the taxonomy and executed expressions (sen0401_ch10_leaves_v1_0_0),
and the teaching paragraphs (sen0401_ch10_text_a..d_v1_0_0). Every expression is executed by the checks against the saved sources, the recorded Bitcoin Core 31.1 regtest run and the Bitnodes snapshot."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch10_sources_v1_0_0 as SRC
import sen0401_ch10_leaves_v1_0_0 as LV
import sen0401_ch10_text_a_v1_0_0 as TA
import sen0401_ch10_text_b_v1_0_0 as TB
import sen0401_ch10_text_c_v1_0_0 as TC
import sen0401_ch10_text_d_v1_0_0 as TD

CH = 10
DATE = "2026-10-15"          # the day every source was opened and every claim executed
PYVER = "3.14.6"
VERSION = "1_0_0"
TITLE = "The Bitcoin Network"
QUESTION = ("What does Chapter 10 of Mastering Bitcoin (3rd edition) say about the Bitcoin network, which of its statements can be recomputed or run on Bitcoin Core 31.1 "
            "and on the census of the real network, and what has changed in Bitcoin Core, the BIPs and the network since the book went to print?")
CQS = ("Which claims of the chapter can be checked by computation, and what does the computation give?",
       "What in the chapter has changed since the book went to print, and on what source?")
LABELS = {
    "DnsSeedList": "DNS seed list", "Addrv2Networks": "Addrv2 networks (BIP 155)", "Spv": "Simplified payment verification (SPV)", "FiltersOverP2P": "Block filters over the peer-to-peer network",
    "V2DefaultHistory": "Default history of the v2 transport", "EncryptedV2": "Encrypted v2 transport (BIP 324)", "PlaintextV1": "Plaintext v1 transport", "I2pAndCjdns": "I2P and CJDNS",
    "TxAnnouncementByWtxid": "Transaction announcement by wtxid", "FilterIdeaPost2016": "Filter idea post of 2016", "ForwardErrorCorrectionDemo": "Forward error correction demonstration",
    "HeadersBatchOf2000": "Headers in batches of 2,000", "BloomFilterWireFormat": "Bloom filter wire format (BIP 37)", "MerkleblockForOneMatch": "Merkleblock for one match",
    "BasicFilterParameters": "Basic filter parameters (BIP 158)", "CompactBlocksYear": "The year of compact blocks", "ShortIdsAreSixBytes": "Short ids are six bytes",
    "SixConfirmationsOdds": "Odds after six confirmations", "TorHiddenService": "Tor hidden service", "MempoolIsLocalUtxoIsShared": "The mempool is local, the UTXO set is shared",
    "NetworkAndNodes": "Network and nodes", "PeersAndDiscovery": "Peers and discovery", "BlockRelay": "Block relay", "LightClients": "Light clients", "PrivacyAndTransport": "Privacy and transport",
    "MempoolAndOrphans": "Mempool and orphans", "ArchivalNodeServices": "Archival node services", "PrunedNodeServices": "Pruned node services", "GolombRiceRoundTrip": "Golomb-Rice round trip",
    "FilterEqualsNodeFilter": "Filter equals the node's filter", "FilterSkipsOpReturn": "The filter skips OP_RETURN", "ProtocolVersionNumber": "Protocol version number", "UnauthenticatedTransport": "Unauthenticated transport",
}
S = "Antonopoulos and Harding, 2023"
PUBS = [(r[0], r[2], r[3], r[5] == "primary") for r in SRC.S]
CONCEPTS = [("Section", x) for x in (
    "Node Types and Roles", "The Network", "Compact Block Relay", "Private Block Relay Networks", "Network Discovery", "Full Nodes", "Lightweight Clients", "Bloom Filters",
    "How Bloom Filters Work", "How Lightweight Clients Use Bloom Filters", "Compact Block Filters", "Golomb-Rice Coded Sets (GCS)", "What Data to Include in a Block Filter",
    "Downloading Block Filters from Multiple Peers", "Reducing Bandwidth with Lossy Encoding", "Using Compact Block Filters", "Lightweight Clients and Privacy",
    "Encrypted and Authenticated Connections", "Mempools and Orphan Pools")] + [("Concept", x) for x in (
    "Bitcoin", "peer-to-peer networks, Bitcoin as", "Bitcoin network", "nodes", "full nodes", "peers", "archival full nodes", "SPV (simplified-payment-verification) clients", "lightweight clients",
    "blocks", "compact block relay", "mining", "block-finding races", "low-bandwidth mode (compact block relay)", "high-bandwidth mode (compact block relay)", "private block relay",
    "FEC (Forward Error Correction)", "Bitcoin Relay Network", "FIBRE (Fast Internet Bitcoin Relay Engine)", "network discovery", "DNS seeds", "UTXOs (unspent transaction outputs)",
    "blockchain", "syncing blockchain", "bloom filters", "compact block filters", "GCS (Golomb-Rice coded sets)", "lossless encoding", "downloading multiple block filters", "lossy encoding",
    "false positives", "privacy", "encryption", "Tor transport", "Bitcoin Core", "memory pool", "orphan pools", "unconfirmed transactions", "transactions")] + [("Concept", x) for x in (
    "BIP 37", "BIP 152", "BIP 157", "BIP 158")]
FINDINGS = [   # (id, section, text, cites)
 ("F1", "Background", "The chapter states that the Bitcoin network is a flat peer-to-peer network with about 10,000 listening nodes (Antonopoulos and Harding, 2023). The Bitnodes snapshot of 2026-10-15 lists 25,361 reachable nodes: 12,488 onion services, 7,473 on IPv4, 4,208 on I2P, 1,191 on IPv6 and one on CJDNS, so only 8,664 are on the plain internet, and the growth lies almost wholly in the hidden networks (Bitnodes, 2026).", ["P01", "P73"]),
 ("F2", "Background", "The software share is as the book says, more than 95 percent of full nodes on Bitcoin Core code: 25,278 of 25,361 nodes (99.67 percent) report a /Satoshi: user agent, of which 4,083 are Bitcoin Knots and 21,195 (83.57 percent of all) plain Bitcoin Core, and the most common agent is /Satoshi:31.1.0/ with 7,442 nodes. The user agent is only a text that a node chooses (Bitnodes, 2026); (Taaki and Strateman, 2011); (Antonopoulos and Harding, 2023).", ["P73", "P07", "P01"]),
 ("F3", "Contemporary developments", "Erratum: the book dates compact block relay to a release of 2015, whereas BIP 152 was assigned on 2016-04-27 and Bitcoin Core lists it as implemented as of version 0.13.0, whose release notes name the pull request of Suhas Daftuar (Antonopoulos and Harding, 2023); (Corallo, 2016); (Bitcoin Core, 2026); (Bitcoin Core developers, 2016).", ["P01", "P14", "P47", "P22"]),
 ("F4", "Contemporary developments", "Changed default: BIP 37 Bloom filters are off in Bitcoin Core, the option -peerbloomfilters having been changed to false in release 0.19.0.1; a default node in the run did not set the BLOOM bit and disconnected a peer that sent filterload, and 4,308 of the 25,361 nodes of the census still set it. The book explains the filters at length without saying this (Bitcoin Core developers, 2019); (Bitcoin Core, 2026); (Corallo and Todd, 2015); (Bitnodes, 2026); (Antonopoulos and Harding, 2023).", ["P23", "P47", "P09", "P73", "P01"]),
 ("F5", "Contemporary developments", "Changed default: the book says that Bitcoin Core communicates entirely in the clear, but the v2 encrypted transport of BIP 324 was added as an option in 26.0 and is on by default since 27.0, DEFAULT_V2_TRANSPORT being true, and 21,768 of the 25,361 nodes of the census (85.8 percent) advertise it. In the run a v2 stream carried neither the magic nor the word version (Antonopoulos and Harding, 2023); (Bitcoin Core developers, 2023); (Bitcoin Core developers, 2024); (Mehta et al., 2019); (Bitcoin Core, 2026).", ["P01", "P27", "P28", "P19", "P33"]),
 ("F6", "Contemporary developments", "The v2 transport encrypts but does not authenticate: BIP 324 says that it defends against passive observers and leaves the man-in-the-middle possible, and its predecessor BIP 151 of Jonas Schnelli was closed after mixed comments (Mehta et al., 2019); (Schnelli, 2016).", ["P19", "P13"]),
 ("F7", "Contemporary developments", "The book knows only Tor as an overlay network. Bitcoin Core 0.21.0 added Tor version 3 and addrv2, release 22.0 removed Tor version 2 and added I2P, release 23.0 added CJDNS, and the census holds 12,488 onion nodes, 4,208 I2P nodes and one CJDNS node (Bitcoin Core developers, 2021); (Bitcoin Core developers, 2022); (Van der Laan, 2019); (Bitnodes, 2026); (Antonopoulos and Harding, 2023).", ["P24", "P25", "P84", "P15", "P73", "P01"]),
 ("F8", "Contemporary developments", "Changed value: the book shows the protocol version 70002 in its description of the handshake, while PROTOCOL_VERSION of Bitcoin Core 31.1 is 70016 and the node sent it in the run; the same number is the first version for wtxid relay (Antonopoulos and Harding, 2023); (Bitcoin Core, 2026); (Daftuar, 2020).", ["P01", "P36", "P21"]),
 ("F9", "Contemporary developments", "Erratum: the book says that each output script is reduced to just 64 bits in the lossy encoding of a block filter. BIP 158 hashes into the range N x M with M = 784931 and codes the differences with P = 19, so the stored element takes about 21 bits, and the filter of the run held 104 elements in 275 bytes, 21.15 bits per element (Antonopoulos and Harding, 2023); (Osuntokun and Akselrod, 2017).", ["P01", "P17"]),
 ("F10", "Contemporary developments", "BIP 158 and the code of Bitcoin Core leave all OP_RETURN output scripts out of the basic filter, a detail that matters to a client that looks for data outputs; in the run 2 OP_RETURN outputs were absent from the filter, and the independent code reproduced the node's filter and filter header byte for byte, and all 10 test vectors of the BIP (Osuntokun and Akselrod, 2017); (Bitcoin Core, 2026); (Osuntokun et al., 2018).", ["P17", "P38", "P68"]),
 ("F11", "Contemporary developments", "The history of the block filters is as the book says: an anonymous developer wrote to the bitcoin-dev list on 2016-05-09, the idea became BIP 157 and 158, Bitcoin Core indexed the filters in 0.19.0 and served them in 0.21.0, and the service bit COMPACT_FILTERS is set by 7,905 nodes of the census, because -peerblockfilters is off by default (Bfd, 2016); (Osuntokun et al., 2017); (Bitcoin Core, 2026); (Bitnodes, 2026); (Antonopoulos and Harding, 2023).", ["P66", "P16", "P47", "P73", "P01"]),
 ("F12", "Comparative analysis", "The book's remark that the headers are about 10,000 times smaller than the chain holds almost exactly: at height 971,499 the headers are 77.7 megabytes against 775,272 megabytes, a ratio of 9,975. The simplified payment verification of the paper needs only these (Antonopoulos and Harding, 2023); (Blockchain Charts, 2026); (Mempool Space, 2026); (Nakamoto, 2008).", ["P01", "P74", "P75", "P51"]),
 ("F13", "Comparative analysis", "The numbers of block download in the book are right in kind and incomplete in detail: Bitcoin Core answers a getheaders with at most 2,000 headers (MAX_HEADERS_RESULTS), requests blocks inside a window of 1,024 (BLOCK_DOWNLOAD_WINDOW) with at most 16 in transit from one peer, and protects itself by a presync phase for low-work headers (Bitcoin Core, 2026); (Antonopoulos and Harding, 2023).", ["P81", "P34", "P82", "P01"]),
 ("F14", "Comparative analysis", "The orphan pool changed three times after the book: 29.0 asks all peers that announced an orphan for its missing parents, 30.0 replaced the limit of 100 orphans by 404,000 weight units for each peer and 3,000 entries, and 31.0 removed the option -maxorphantx. The book has no limit to compare (Bitcoin Core developers, 2025); (Bitcoin Core developers, 2026); (Bitcoin Core, 2026); (Antonopoulos and Harding, 2023).", ["P30", "P31", "P32", "P41", "P01"]),
 ("F15", "Comparative analysis", "Compact blocks have limits that the book does not state: a short id is 6 bytes, a node sends compact blocks unasked to at most 3 high-bandwidth peers, and it answers a request for a compact block only for blocks at most 5 deep (MAX_CMPCTBLOCK_DEPTH); in the run a block of 13 transactions took 332 bytes instead of 3,062 (Corallo, 2016); (Bitcoin Core, 2026); (Antonopoulos and Harding, 2023).", ["P14", "P37", "P34", "P01"]),
 ("F16", "Comparative analysis", "The statement that the mempool is local and the UTXO set shared is confirmed by the run, in which one node held 6 transactions and its blocks-only neighbour 0 while both held the same UTXO set of 107 outputs after a block; the defaults of the mempool, 300 MB and 336 hours, are not given by the book (Antonopoulos and Harding, 2023); (Bitcoin Core developers, 2026).", ["P01", "P50"]),
 ("F17", "Comparative analysis", "Transactions are announced by wtxid since BIP 339 (inv type MSG_WTX, 5), the book describes the txid form, and a peer's feefilter (BIP 133) held back the cheaper of two transactions in the run, which announced 20.0 satoshis per virtual byte and not 2.0 to a peer that asked for 5 (Daftuar, 2020); (Morcos, 2016); (Antonopoulos and Harding, 2023).", ["P21", "P11", "P01"]),
 ("F18", "Comparative analysis", "Pruned nodes do not set NETWORK but NETWORK_LIMITED (BIP 159), which promises the last 288 blocks, and the census shows 25,322 nodes with that bit against 22,402 with NETWORK; the book's listing shows the bit without explaining it (Schnelli, 2017); (Bitcoin Core, 2026); (Bitnodes, 2026); (Antonopoulos and Harding, 2023).", ["P18", "P35", "P73", "P01"]),
 ("F19", "Comparative analysis", "The connection types are in the code and in the peer listing: 8 outbound full-relay connections, 2 block-relay-only connections, feelers, addr-fetch and manual connections, up to 125 in all (Bitcoin Core, 2026); the book's listing shows the field connection_type but does not explain it (Antonopoulos and Harding, 2023).", ["P33", "P44", "P01"]),
 ("F20", "Comparative analysis", "Erratum: the listing of getpeerinfo in the book is outdated for Bitcoin Core 31: the node of the run returned the new fields inv_to_send, last_inv_sequence, session_id and transport_protocol_type, and no startingheight, which release 31.0 hides unless -deprecatedrpc=startingheight is given (Bitcoin Core developers, 2026); (Bitcoin Core, 2026); (Antonopoulos and Harding, 2023).", ["P32", "P44", "P01"]),
 ("F21", "Conclusion", "Attacks on the network are real but could not be run in the sandbox: eclipse attacks need many addresses and routing attacks need control of internet routes; the papers report that an adversary with enough addresses can monopolize a node's connections, and that fewer than 100 BGP prefixes can isolate about 50 percent of the mining power; anchor connections are a defence (Heilman et al., 2015); (Apostolaki et al., 2017); (Bitcoin Optech, 2026).", ["P52", "P55", "P61"]),
 ("F22", "Conclusion", "Erlay, the reconciliation of transaction announcements of BIP 330, is a Draft and is off by default in Bitcoin Core 31.1 (-txreconciliation default 0), so the book's picture of flooding by inv messages is still the practice; it was not run for that reason (Naumenko and Wuille, 2019); (Naumenko et al., 2019); (Bitcoin Core developers, 2026).", ["P20", "P53", "P50"]),
 ("F23", "Conclusion", "Nakamoto's calculation of an attacker's chance of catching up, which the book uses to justify light clients, gives 0.0002428 for a share of 10 percent and 6 blocks, and 0.1321 for a share of 30 percent, computed in the chapter and equal to the table of the paper; the light client's privacy was shown to be weak by the Bloom filter study of Gervais and colleagues (Nakamoto, 2008); (Gervais et al., 2014).", ["P51", "P57"]),
 ("F24", "Conclusion", "Taken together, the chapter's picture of a flat network of equal nodes remains right in principle, but its numbers (nodes, protocol version), its date of compact blocks and its 64 bits are wrong or out of date, and five defaults have moved since the book: Bloom filters off, v2 transport on, new overlay networks, new orphan limits and no startingheight (Antonopoulos and Harding, 2023); (Bitcoin Core developers, 2026).", ["P01", "P32"]),
]
TAX = [(t, m, l, ex, d, ((e.replace("\n", "; "), r) if e and r is not None else None)) for t, m, l, ex, d, e, r in LV.LEAVES]   # one line each: the ABox holds it as a string literal
_ALL = {}
for _x in (TA.A, TB.B, TC.C, TD.D):
    _ALL.update(_x)
_LAB = lambda c: LABELS.get(c) or (lambda t: t[0].upper() + t[1:])("".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip())
BODY = dict(_ALL)
_mem = {}
for _t, _m, _l, *_ in TAX:
    _mem.setdefault(_t, [])
    if _m not in _mem[_t]:
        _mem[_t].append(_m)
    _mem.setdefault(_m, []).append(_l)
for _c in _mem:
    _intro = TD.TOP[_c] if _c in TD.TOP else TD.MID[_c]
    BODY[_c] = _intro + " This subject covers " + "; ".join(_LAB(x) for x in _mem[_c]) + "."
BODY = {k: v.replace('"', "'").replace("\n", " ") for k, v in BODY.items()}
_P = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch10_lib_v1_0_0 as L; "
CLAIMS = [
 (_P + "r = L.quotes_report(); (r[0], r[2], r[3])", "(85, [], [])"),
 (_P + "L.index_report()", "(85, 85, [])"),
 (_P + "L.getpeerinfo_new_and_gone()", "(['inv_to_send', 'last_inv_sequence', 'session_id', 'transport_protocol_type'], ['addrlocal', 'startingheight'])"),
 (_P + "(L.has('core_src_rpc_net.cpp', 'DEPRECATED, returned only if config option -deprecatedrpc=startingheight is passed'), L.has('core_relnotes_31.0.html', 'startingheight'), L.book_keys_in_text())", "(True, True, ['addrlocal', 'connection_type', 'bip152_hb_to', 'minfeefilter'])"),
 (_P + "(L.has('bitcoind_help_31.1.txt', 'Enable transaction reconciliations per BIP 330 (default: 0)'), L.has('bip-0330.mediawiki', 'Status: Draft'))", "(True, True)"),
]
BEH = [
 ("The checksum of the empty payload of a verack message", "import hashlib; print(hashlib.sha256(hashlib.sha256(b'').digest()).digest()[:4].hex())", "5df6e0e2"),
 ("The services value 3081 decoded", "print([n for b, n in ((1, 'NETWORK'), (8, 'WITNESS'), (1024, 'NETWORK_LIMITED'), (2048, 'P2P_V2')) if 3081 & b])", "['NETWORK', 'WITNESS', 'NETWORK_LIMITED', 'P2P_V2']"),
 ("The chance of a rival block within 10 seconds", "import math; print(round(1 - math.exp(-10 / 600), 4))", "0.0165"),
 ("The size of the header chain at 971,500 headers, in megabytes", "print(80 * 971500 / 1e6)", "77.72"),
 ("The bits per element of a 275-byte filter with 104 elements", "print(round(275 * 8 / 104, 2))", "21.15"),
]
