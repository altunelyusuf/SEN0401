"""SEN0401 chapter 10 (The Bitcoin Network) for the RDODI build (generic builder sen0401_rdodi_build_v1_2_0.py), version 1.1.0: the relationships between the chapter's sections stated as links.
Everything of version 1.0.1 is taken over unchanged (sources, taxonomy, executed expressions, paragraphs, findings, claims); this module adds what the owner asked on 2026-10-22 (ruling G134, links not text):
 SECTION_PROPS   the object properties, each declared in the domain TBox with domain, range, label and kb:hasRelationshipCategory taken from the OEE relationship taxonomy
                 (oe-method/04-documentation/RELATIONSHIP_TAXONOMY_RESEARCH_v1_11_0.md), a standard relation reused (rdfs:subPropertyOf) where one says it
 SECTION_LINKS   the links, stated in the domain ABox between the X_ individuals of two different sections (sections are the second-level subjects; a leaf belongs to the section above it)
 CLASS_KINDS     kb:hasClassKind where the kind rule of a category needs the kind of an end (Process for the ends of a direct sequence, Specification for the ends of a supersession)
 DECLARE_IO      chx:input and chx:output, which the ABox of every version used and no file declared (the one finding of oe_link_discovery on this chapter)
Each link was kept only because the text of the chapter's own sections states it; the sentence that states it is given with the link (EVIDENCE below), after asking the categories of the taxonomy one by one
(syntactic, semantic with its sub-categories, temporal with its sub-categories, structural). No syntactic relation between two sections is stated by the text (the discovery tool finds no text that names a modelled
thing of another section without a link), and no temporal-order relation between instants or intervals of two sections is stated; both categories are therefore not used."""
__version__ = "1.1.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch10_rdodi_data_v1_0_1 import *          # noqa: F401,F403  (everything of 1.0.1: TITLE, QUESTION, CQS, LABELS, PUBS, CONCEPTS, FINDINGS, TAX, BODY, CLAIMS, BEH, ...)
from sen0401_ch10_rdodi_data_v1_0_1 import TAX as _TAX

VERSION = "1_1_0"
MODIFIED = "2026-10-22"       # the day the section links were stated; the sources and claims keep the day of 2026-10-15
DECLARE_IO = True

PRECEDES = "http://purl.obolibrary.org/obo/BFO_0000063"      # Relations Ontology / BFO: precedes
REQUIRES = "http://purl.org/dc/terms/requires"
REPLACES = "http://purl.org/dc/terms/replaces"
IS_PART_OF = "http://purl.org/dc/terms/isPartOf"

CLASS_KINDS = {
    "HandshakeMessageOrder": "Process", "FeefilterHonoured": "Process", "TxAnnouncementByWtxid": "Process", "HighAndLowBandwidthModes": "Process", "HeadersBatchOf2000": "Process",
    "BasicFilterParameters": "Specification", "BloomFilterWireFormat": "Specification",
}

def P(name, label, category, domain, range_, definition, parents=()):
    return dict(name=name, label=label, category=category, domain=domain, range=range_, definition=definition, parents=list(parents))

SECTION_PROPS = [
    P("signalledByServiceBit", "signalled by service bit", "Characterization", "NodeKinds", "ServiceBitsOfNetwork",
      "A kind of node tells which history it keeps by a bit of the services field that every node sends in its version message."),
    P("countedInCensus", "counted in the census", "ContainmentMembership", "AnonymityNetworks", "ReachableNodesToday",
      "The nodes that are reached through an overlay network are among the nodes counted by the Bitnodes census.", [IS_PART_OF]),
    P("precedesFeefilter", "comes before the feefilter of", "SuccessionTransformation", "HandshakeMessageOrder", "FeefilterHonoured",
      "In the order of messages of a new connection the feefilter message comes after the verack that ends the handshake.", [PRECEDES]),
    P("precedesWtxidAnnouncement", "comes before the announcement by wtxid of", "SuccessionTransformation", "HandshakeMessageOrder", "TxAnnouncementByWtxid",
      "The wtxidrelay message must be sent before verack, and only after both sides sent it are transactions announced by their wtxid.", [PRECEDES]),
    P("precedesCompactBlockMode", "comes before the choice of compact block mode of", "SuccessionTransformation", "HandshakeMessageOrder", "HighAndLowBandwidthModes",
      "The sendcmpct message, with which a peer picks high or low bandwidth mode, follows the verack of the handshake.", [PRECEDES]),
    P("precedesHeadersRequest", "comes before the request for headers of", "SuccessionTransformation", "HandshakeMessageOrder", "HeadersBatchOf2000",
      "The getheaders message, with which a new node asks for the chain, follows the verack of the handshake.", [PRECEDES]),
    P("relayNetworkPrecedesCompactBlocks", "came before the compact blocks of", "SuccessionTransformation", "RelayNetworkHistory", "CompactBlocksYear",
      "The private relay network of miners was in use in 2015, before compact blocks were assigned their BIP in 2016.", [PRECEDES]),
    P("requiresProtocolVersion", "needs the protocol version of", "Requirement", "Addrv2Networks", "ProtocolVersionNumber",
      "The addrv2 message of BIP 155 builds on the protocol version 70016 that the version message carries.", [REQUIRES]),
    P("buildsOnCompactBlocks", "builds on the compact blocks of", "Requirement", "ForwardErrorCorrectionDemo", "ShortIdsAreSixBytes",
      "The relay system FIBRE sends compact blocks over UDP with forward error correction, so it needs compact blocks.", [REQUIRES]),
    P("buildsOnMerklePath", "builds on the Merkle path of", "Requirement", "MerkleblockForOneMatch", "MerklePathProof",
      "The merkleblock message that answers a loaded filter carries the partial Merkle tree whose path the light client checks against the root in the header.", [REQUIRES]),
    P("buildsOnHeaderChain", "builds on the header chain checks of", "Requirement", "HeaderChainSize", "HeaderChainLinks",
      "A light client that keeps only the headers relies on the checks that a chain of headers can be verified without any block.", [REQUIRES]),
    P("usesWtxidAnnouncement", "takes part in the announcement by wtxid of", "Participation", "OrphanWaitsForParent", "TxAnnouncementByWtxid",
      "A node that meets an orphan asks for it by the wtxid in an inv entry of type 5, which is the announcement that BIP 339 introduced.", []),
    P("requiresAddressExchange", "needs the address exchange of", "Requirement", "ConnectionTypes", "AddrGossipFormat",
      "An addr-fetch connection exists only to ask for addresses with getaddr and to leave, so it needs the address exchange.", [REQUIRES]),
    P("plaintextFramedBy", "is framed as described in", "Requirement", "PlaintextV1", "MessageFraming",
      "The plain transport sends every message with the frame of magic bytes, command, length and checksum that the old transport defines.", [REQUIRES]),
    P("shortensBlockRace", "is a means to shorten the race of", "Intentional", "CompactBlocks", "BlockFindingRaceProbability",
      "Faster relay of blocks, which compact blocks achieve, lowers the chance that a rival block is found while a block travels.", []),
    P("replacesBloomFilter", "replaces the Bloom filter of", "Versioning", "BasicFilterParameters", "BloomFilterWireFormat",
      "The basic block filter of BIP 158 replaced the Bloom filter of BIP 37 as the way for a light client to find its transactions.", [REPLACES]),
    P("contrastsWithBloomPrivacy", "differs in privacy from", "Comparative", "FilterFalsePositiveRate", "BloomDisabledByDefault",
      "A false positive of a block filter costs only the download of a block and reveals no address, whereas a Bloom filter gave the node a view of the addresses of the wallet.", []),
    P("sharesSipHashWith", "shares its hash function with", "Comparative", "BasicFilterParameters", "ShortIdsAreSixBytes",
      "The basic filter and the short ids of a compact block are both computed with SipHash-2-4, and one reference value of its paper checks both.", []),
    P("guardsMemoryLike", "guards the memory in the way of", "Comparative", "HeadersPresync", "OrphanageLimits",
      "Both protect the memory of a node against an attacker who floods it with data that never becomes valid.", []),
    P("withholdsTransactionsLike", "withholds transactions in the way of", "Comparative", "FeefilterHonoured", "RelayFlagSilencesTransactions",
      "Both are ways in which a peer limits which transactions it is told about, and one run tested them together on three peers.", []),
    P("isLocalViewLike", "is a local view in the way of", "Comparative", "MempoolIsLocalUtxoIsShared", "OrphanWaitsForParent",
      "The mempool and the orphan pool are both a local view of one node and may differ from node to node.", []),
    P("motivatesAddrv2", "is the reason for", "Causal", "FiveNetworks", "Addrv2Networks",
      "Each of the five networks has its own address format, which is why addrv2 was invented.", []),
    P("mitigatesRoutingAttack", "helps to defend against the routing attack", "Causal", "FiveNetworks", "RoutingAttack",
      "Encryption does not help against a route that is dropped, whereas peers from different networks, such as Tor, do.", []),
    P("mitigatesEclipseAttack", "helps to defend against the eclipse attack", "Causal", "ConnectionTypes", "EclipseAttack",
      "The two block-relay-only connections are part of the answer to the eclipse attack, since transaction gossip does not show them.", []),
    P("isBaseOfConnectionType", "is the base of the connection types of", "Causal", "RelayFlagSilencesTransactions", "ConnectionTypes",
      "The relay flag set to false is the base of the block-relay-only connections of Bitcoin Core.", []),
    P("ranOverTransport", "ran over the transport of", "Characterization", "ConnectionTypes", "PlaintextV1",
      "In the run the block-relay-only connection spoke the old plaintext transport.", []),
]

# (source leaf, property, target leaf, the sentence of the chapter's own text that states it)
SECTION_LINKS = [
    ("ArchivalNodeServices", "signalledByServiceBit", "ServiceBitsOfNetwork", "Archival: 'it says so with the service bit NETWORK'; Service bits: 'NETWORK (the full block history)' and 'counts 22,402 nodes with NETWORK'."),
    ("PrunedNodeServices", "signalledByServiceBit", "ServiceBitsOfNetwork", "Pruned: 'it must not set the NETWORK bit and uses NETWORK_LIMITED instead'; Service bits: 'NETWORK_LIMITED (only the last 288 blocks)'."),
    ("TorHiddenService", "countedInCensus", "ReachableNodesToday", "Tor: 'The census of 2026-10-15 lists 12,488 onion nodes, half of all reachable nodes'; Reachable nodes: '12,488 onion services'."),
    ("I2pAndCjdns", "countedInCensus", "ReachableNodesToday", "I2P: 'The census of 2026-10-15 holds 4,208 I2P nodes, one in six of all'; Reachable nodes: '4,208 on I2P'."),
    ("HandshakeMessageOrder", "precedesFeefilter", "FeefilterHonoured", "Handshake order: 'the node followed verack with sendcmpct' and 'and feefilter'; Feefilter: 'The handshake order of the run shows that the feefilter message follows verack'."),
    ("HandshakeMessageOrder", "precedesWtxidAnnouncement", "TxAnnouncementByWtxid", "Handshake order: 'the feature messages that must come before verack, wtxidrelay (BIP 339)'; Announcement: 'after both sides sent wtxidrelay'."),
    ("HandshakeMessageOrder", "precedesCompactBlockMode", "HighAndLowBandwidthModes", "Handshake order: 'the node followed verack with sendcmpct (compact blocks)'; Modes: 'A peer picks the mode with the message sendcmpct'."),
    ("HandshakeMessageOrder", "precedesHeadersRequest", "HeadersBatchOf2000", "Handshake order: 'getheaders (what chain does the peer have)' after verack; Headers: 'the node asks with getheaders and the peer answers with at most 2,000 headers'."),
    ("RelayNetworkHistory", "relayNetworkPrecedesCompactBlocks", "CompactBlocksYear", "Relay history: 'Before compact blocks, miners built private networks'; Year: 'the relay network, which was in use in 2015'; 'BIP 152 was assigned its number on 2016-04-27'."),
    ("Addrv2Networks", "requiresProtocolVersion", "ProtocolVersionNumber", "Protocol version: 'The number 70016 is also the one that BIP 339 and BIP 155 build on'."),
    ("ForwardErrorCorrectionDemo", "buildsOnCompactBlocks", "ShortIdsAreSixBytes", "FEC: 'FIBRE ... uses it on UDP together with compact blocks'; 'the compact block idea on which FIBRE builds'."),
    ("MerkleblockForOneMatch", "buildsOnMerklePath", "MerklePathProof", "Merkleblock: 'a partial Merkle tree holding only the paths ... the partial tree led to the root in the header'; Merkle path: 'a client with the header can recompute the root and compare'."),
    ("HeaderChainSize", "buildsOnHeaderChain", "HeaderChainLinks", "Header chain links: 'a node can check the whole chain of headers by itself, without any block' and 'lightweight clients that synchronize the headers alone'; Header chain size: 'downloads only the block headers'."),
    ("OrphanWaitsForParent", "usesWtxidAnnouncement", "TxAnnouncementByWtxid", "Orphan: 'the node asked for the child by its wtxid (an inv entry of type 5)'; Announcement: 'the identifier is the wtxid ... announced with the type MSG_WTX (0x00000005)'."),
    ("ConnectionTypes", "requiresAddressExchange", "AddrGossipFormat", "Connection types: 'addr-fetch connections that only ask for addresses and leave'; Addr gossip: 'it learns more addresses by asking, with the message getaddr'."),
    ("PlaintextV1", "plaintextFramedBy", "MessageFraming", "Plaintext: 'the first bytes that the script sent over a v1 connection were fabfb5da, the magic of the test chain'; Framing: 'every message ... on the old transport is a block of bytes with a header of 24 bytes: 4 bytes of magic'."),
    ("ShortIdsAreSixBytes", "shortensBlockRace", "BlockFindingRaceProbability", "Race: 'faster block relay is a security matter ' and 'topic page on compact block relay presents it as a way to cut the delay'."),
    ("BasicFilterParameters", "replacesBloomFilter", "BloomFilterWireFormat", "Filter idea: 'Osuntokun and Alex Akselrod, who replaced the Bloom filter by the Golomb-coded set'; Bloom disabled: 'presents the block filters as the safer replacement of BIP 37'."),
    ("FilterFalsePositiveRate", "contrastsWithBloomPrivacy", "BloomDisabledByDefault", "False positive: 'the false positives do not harm privacy as the Bloom filters did'; Bloom disabled: 'give the node a view of the client's addresses with weak privacy'."),
    ("BasicFilterParameters", "sharesSipHashWith", "ShortIdsAreSixBytes", "Basic filter: 'SipHash-2-4 keyed by the block hash ... its SipHash returned the reference value a129ca6149be45e5'; Short ids: 'SipHash-2-4 ... the reference test value a129ca6149be45e5 of the SipHash paper'."),
    ("HeadersPresync", "guardsMemoryLike", "OrphanageLimits", "Presync: 'an attacker could send millions of low-work headers to fill its memory'; Orphanage: 'a place where an attacker could try to fill the memory with transactions that never become valid'."),
    ("FeefilterHonoured", "withholdsTransactionsLike", "RelayFlagSilencesTransactions", "Relay flag: 'three peers were connected to the same node: one normal peer, one with relay false and one that had set a minimum fee with feefilter'."),
    ("MempoolIsLocalUtxoIsShared", "isLocalViewLike", "OrphanWaitsForParent", "Mempool: 'the mempool and the orphan pool are a node's local view and may differ from node to node'; Orphan: 'it keeps it in a small separate pool, the orphanage'."),
    ("FiveNetworks", "motivatesAddrv2", "Addrv2Networks", "Five networks: 'each has its own address format, which is why addrv2 was invented'."),
    ("FiveNetworks", "mitigatesRoutingAttack", "RoutingAttack", "Routing: 'encryption does not help against a route that is simply dropped, whereas peers from different networks, such as Tor, do'."),
    ("ConnectionTypes", "mitigatesEclipseAttack", "EclipseAttack", "Eclipse: 'The two block-relay-only connections of Bitcoin Core are part of the answer, since they are not seen by transaction gossip'."),
    ("RelayFlagSilencesTransactions", "isBaseOfConnectionType", "ConnectionTypes", "Relay flag: 'a node that sets it to false asks to receive blocks only ... and is the base of the block-relay-only connections of Bitcoin Core'."),
    ("ConnectionTypes", "ranOverTransport", "PlaintextV1", "Connection types: 'block-relay-only did not [relay transactions] and spoke the v1 transport, the old plaintext one'."),
]
EVIDENCE = {(a, p, b): e for a, p, b, e in SECTION_LINKS}

# ---- checks of this module's own claims (run at import, so a wrong end cannot be built) ------------------------------------------------------------------------------------------------------
_parent = {}
for _t, _m, _l, *_ in _TAX:
    _parent[_l] = _m; _parent[_m] = _t; _parent.setdefault(_t, None)
def _under(c, anc):
    while c is not None:
        if c == anc: return True
        c = _parent.get(c)
    return False
def _section(leaf): return _parent[leaf]                         # the second-level subject that holds a leaf
_pn = {p["name"]: p for p in SECTION_PROPS}
assert len(_pn) == len(SECTION_PROPS), "duplicate property name"
assert len({p["label"] + "|" + p["domain"] + "|" + p["range"] for p in SECTION_PROPS}) == len(SECTION_PROPS)
assert len({p["definition"] for p in SECTION_PROPS}) == len(SECTION_PROPS), "two properties with one definition (BP-D61)"
_leaves = {l for _t, _m, l, *_ in _TAX}
for _a, _p, _b, _e in SECTION_LINKS:
    assert _a in _leaves and _b in _leaves, (_a, _b)
    assert _under(_a, _pn[_p]["domain"]) and _under(_b, _pn[_p]["range"]), "an end of %s is not under the declared domain/range of %s" % ((_a, _b), _p)
    assert _section(_a) != _section(_b), "%s and %s are in one section" % (_a, _b)
assert all(any(l[1] == n for l in SECTION_LINKS) for n in _pn), "a declared property no link uses"
_secs = {m for _t, m, *_ in _TAX}
_rel = {s: 0 for s in _secs}
for _a, _p, _b, _e in SECTION_LINKS:
    _rel[_section(_a)] += 1; _rel[_section(_b)] += 1
assert all(_rel.values()), "a section with no link: %s" % [s for s, n in _rel.items() if not n]
assert len(_secs) == 17
