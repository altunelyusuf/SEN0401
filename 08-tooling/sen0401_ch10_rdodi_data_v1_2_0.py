"""SEN0401 chapter 10 (The Bitcoin Network) for the RDODI build (generic builder sen0401_rdodi_build_v1_4_0.py), version 1.2.0: the section links of version 1.1.0 stated once per meaning (BP-D61 one meaning, one term; the owner's standing rule of 2026-10-21).
Everything of version 1.0.1 is taken over unchanged (sources, taxonomy, executed expressions, paragraphs, findings, claims). Version 1.1.0 stated 28 links with 26 properties, one per class pair; this version states the same 28 links, between the same two individuals,
with 9 general properties, one per meaning, the way chapter 11 version 1.1.0 does (6 properties for 32 links): the class pair belongs to the link and to the sentence that states it (an owl:Axiom rdfs:comment of the link), not to a new property.
 SECTION_PROPS   the 9 properties, each with domain and range owl:Thing (the ends are examples of two different sections, and the six top classes of the taxonomy are pairwise disjoint), one label, the earlier wordings as skos:altLabel,
                 kb:hasRelationshipCategory from the OEE relationship taxonomy, a standard relation reused (rdfs:subPropertyOf) only where it is true of every link the property states, and a definition that says what it means that no other property of the chapter means
 SECTION_LINKS   the 28 links of 1.1.0, unchanged but for the property, each with the sentence of the chapter's own text that states it (EVIDENCE, written as the annotation of the link)
 CLASS_KINDS     kb:hasClassKind as in 1.1.0 (Process for the five classes of the messages of a connection, Specification for the two classes of a supersession)
 DECLARE_IO      chx:input and chx:output, as in 1.1.0
Which of the 26 properties of 1.1.0 became which of the 9 (the groups were made by reading the definitions and the sentences, not by the class pairs):
 isCharacterizedBy   signalledByServiceBit, ranOverTransport            (a thing is characterized by a feature it carries: the service bit of a kind of node, the transport of a connection type)
 isCountedIn         countedInCensus
 comesBefore         precedesFeefilter, precedesWtxidAnnouncement, precedesCompactBlockMode, precedesHeadersRequest, relayNetworkPrecedesCompactBlocks
 buildsOn            requiresProtocolVersion, buildsOnCompactBlocks, buildsOnMerklePath, buildsOnHeaderChain, requiresAddressExchange, plaintextFramedBy
 takesPartIn         usesWtxidAnnouncement                              (a different category, Participation, so not a requirement)
 isMeansAgainst      mitigatesRoutingAttack, mitigatesEclipseAttack, shortensBlockRace   (the two 'defend against an attack' variants, and the compact blocks as a means against the loss in the block race)
 replaces            replacesBloomFilter
 isComparedWith      contrastsWithBloomPrivacy, sharesSipHashWith, guardsMemoryLike, withholdsTransactionsLike, isLocalViewLike
 isReasonFor         motivatesAddrv2, isBaseOfConnectionType            (what is the reason for, or the base of, something that exists because of it)
Not merged, and why: Characterization, Participation, Requirement, Intentional and Causal are different categories of the taxonomy; Succession and Versioning likewise; the two properties that keep a standard super-property (buildsOn: dcterms:requires, replaces: dcterms:replaces, isCountedIn: dcterms:isPartOf)
differ from each other in category and meaning. The standard relation BFO precedes, which 1.1.0 reused for the five 'comes before' variants, is NOT reused any more: it joins occurrents, and the ends of the fifth link are examples that carry dates (the use of the relay network in 2015, the
year of the assignment of BIP 152), as in chapter 11 where OWL-Time's before is not reused for the same reason; the statement of 1.1.0 that BFO precedes holds for the five links is therefore withdrawn."""
__version__ = "1.2.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch10_rdodi_data_v1_0_1 import *          # noqa: F401,F403
from sen0401_ch10_rdodi_data_v1_0_1 import TAX as _TAX
# build: python3 -B sen0401_rdodi_build_v1_4_0.py sen0401_ch10_rdodi_data_v1_2_0 2026-10-15T00:00:00Z

VERSION = "1_2_0"
MODIFIED = "2026-10-22"
DECLARE_IO = True
LINK_EVIDENCE = True      # each link is annotated with the sentence of the chapter's own text that states it
LINK_SHAPES = True        # the domain shapes check the start and the end of every link

REQUIRES = "http://purl.org/dc/terms/requires"
REPLACES = "http://purl.org/dc/terms/replaces"
IS_PART_OF = "http://purl.org/dc/terms/isPartOf"

CLASS_KINDS = {
    "HandshakeMessageOrder": "Process", "FeefilterHonoured": "Process", "TxAnnouncementByWtxid": "Process", "HighAndLowBandwidthModes": "Process", "HeadersBatchOf2000": "Process",
    "BasicFilterParameters": "Specification", "BloomFilterWireFormat": "Specification",
}

_TAXO = "RELATIONSHIP_TAXONOMY_RESEARCH_v1_11_0.md of the OEE (OE v2.33.0), section 3, the category %s; construction method BP-D58."
_ANY = ("The domain and the range are owl:Thing on purpose: the ends are examples of two different sections, and the six top classes of the taxonomy are pairwise disjoint, so no named class covers both "
        "ends (the rule BP-D23 for a property used across branches with no common ancestor). The class pair belongs to the link and to the sentence that states it. The shape of the domain shapes file checks that both ends are individuals of the chapter.")

def P(name, label, category, definition, comment, source, parents=(), alt=(), chars=()):
    return dict(name=name, label=label, altlabels=list(alt), category=category, domain="owl:Thing", range="owl:Thing", definition=definition, comment=comment + " " + _ANY, source=source, parents=list(parents), characteristics=list(chars))

SECTION_PROPS = [
    P("isCharacterizedBy", "is characterized by", "Characterization",
      "Links an example to the example of another section that illustrates a feature the first one carries and by which it is told from others: the service bit that marks a kind of node, the transport that a connection type spoke. It is not a requirement (the feature is not needed in order to work) and not a part (the feature is not a component).",
      "No standard relation was reused: none of the standard properties checked says that a thing is told by a feature it carries without saying that it is part of it or needs it.",
      _TAXO % "Characterization (a thing and its characteristic)", alt=["is signalled by", "ran over"]),
    P("isCountedIn", "is counted in", "ContainmentMembership",
      "Links an example to the example of another section that illustrates a count or a whole in which the first one is included: the nodes reached through an overlay network are among the nodes of the census. It joins a member and the collection it is counted in; no other property of the chapter says membership.",
      "Reused: dcterms:isPartOf says that a resource is included in another, which is what the sentences of both links say of the nodes of an overlay network and the census.",
      _TAXO % "Containment and membership", parents=[IS_PART_OF]),
    P("comesBefore", "comes before", "SuccessionTransformation",
      "Links an example to the example of another section that illustrates what comes after it in time: in the order of messages of a new connection the verack before the feefilter, the wtxidrelay before the announcement by wtxid, the sendcmpct before the choice of mode, the getheaders before the batch of headers, and the relay network of 2015 before the BIP of compact blocks of 2016. It says only that the first is earlier; it states no cause and no requirement.",
      "No standard relation was reused. BFO precedes (BFO_0000063) was reused in version 1.1.0 for these links; it joins occurrents, and the ends of the link of the relay network are examples that carry dates, so the statement was not true of every link and is withdrawn here, as in chapter 11 for OWL-Time's before.",
      _TAXO % "Succession and transformation (direct sequence)",
      alt=["came before", "is earlier than"]),
    P("buildsOn", "builds on", "Requirement",
      "Links an example to the example of another section that illustrates something the first one needs in order to work or to be defined: addrv2 needs the protocol version 70016, FIBRE needs compact blocks, a merkleblock needs the Merkle path, a light client needs the header chain checks, an addr-fetch connection needs the address exchange, the plain transport needs the frame of the old transport. It differs from takes part in (a participation is not a need) and from is a reason for (the needed thing is not the cause of the first).",
      "Reused: dcterms:requires says that a resource is required by another to support its function or coherence, which is what the sentence of each of the six links says.",
      _TAXO % "Requirement", parents=[REQUIRES],
      alt=["needs", "requires", "is framed as described in"]),
    P("takesPartIn", "takes part in", "Participation",
      "Links an example to the example of another section that illustrates a process or an exchange in which the first one takes part: the handling of an orphan transaction takes part in the announcement by wtxid. It differs from builds on in the category: the orphan is not shown to need the announcement in order to be defined, it is shown to be asked for through it.",
      "No standard relation was reused: dcterms:requires would say a need, which the sentence of the link does not state.",
      _TAXO % "Participation"),
    P("isMeansAgainst", "is a means against", "Intentional",
      "Links an example to the example of another section that illustrates a harm or a loss which the first one is a means to lessen: the peers of other networks and the block-relay-only connections against the routing and the eclipse attack, the compact blocks against the chance that a rival block is found while a block travels. It states a purpose of the first, not a cause: it differs from is a reason for, which says why something exists.",
      "No standard relation was reused: none of the standard properties checked says that a thing is a means to lessen a harm.",
      _TAXO % "Intentional relationship (means and end)",
      alt=["helps to defend against", "is a means to shorten"]),
    P("replaces", "replaces", "Versioning",
      "Links an example to the example of another section that illustrates what it took the place of: the basic block filter of BIP 158 replaced the Bloom filter of BIP 37. It states a supersession, not an order in time only (it differs from comes before) and not a need (it differs from builds on).",
      "Reused: dcterms:replaces says that a resource supplants, displaces or supersedes another, which is what the sentence of the link says.",
      _TAXO % "Versioning", parents=[REPLACES]),
    P("isComparedWith", "is compared with", "Comparative",
      "Links two examples of different sections when the account sets what they illustrate side by side, as alike or as different: the privacy of a block filter and of a Bloom filter, the SipHash of the filter and of the short ids, the guard of the memory by presync and by the orphanage, the withholding of transactions by the feefilter and by the relay flag, the mempool and the orphan pool as local views.",
      "Symmetric, so the link is stated once and holds both ways. No standard relation says a comparison.",
      _TAXO % "Similarity and opposition (Comparative)", chars=["owl:SymmetricProperty"],
      alt=["differs from", "is like", "shares with"]),
    P("isReasonFor", "is a reason for", "Causal",
      "Links an example to the example of another section that illustrates what exists because of it: the five address formats of the five networks are the reason for addrv2, and the relay flag set to false is the base of the block-relay-only connections. It says why the second exists; it differs from is a means against, which states what the first is for.",
      "No standard relation was reused: the Relations Ontology could not be opened in this run, so none was checked against the account.",
      _TAXO % "Causal relationship", alt=["motivates", "is the base of"]),
]

# (source leaf, property, target leaf, the sentence of the chapter's own text that states it); the 28 links of version 1.1.0, between the same two individuals
SECTION_LINKS = [
    ("ArchivalNodeServices", "isCharacterizedBy", "ServiceBitsOfNetwork", "Archival: 'it says so with the service bit NETWORK'; Service bits: 'NETWORK (the full block history)' and 'counts 22,402 nodes with NETWORK'."),
    ("PrunedNodeServices", "isCharacterizedBy", "ServiceBitsOfNetwork", "Pruned: 'it must not set the NETWORK bit and uses NETWORK_LIMITED instead'; Service bits: 'NETWORK_LIMITED (only the last 288 blocks)'."),
    ("TorHiddenService", "isCountedIn", "ReachableNodesToday", "Tor: 'The census of 2026-10-15 lists 12,488 onion nodes, half of all reachable nodes'; Reachable nodes: '12,488 onion services'."),
    ("I2pAndCjdns", "isCountedIn", "ReachableNodesToday", "I2P: 'The census of 2026-10-15 holds 4,208 I2P nodes, one in six of all'; Reachable nodes: '4,208 on I2P'."),
    ("HandshakeMessageOrder", "comesBefore", "FeefilterHonoured", "Handshake order: 'the node followed verack with sendcmpct' and 'and feefilter'; Feefilter: 'The handshake order of the run shows that the feefilter message follows verack'."),
    ("HandshakeMessageOrder", "comesBefore", "TxAnnouncementByWtxid", "Handshake order: 'the feature messages that must come before verack, wtxidrelay (BIP 339)'; Announcement: 'after both sides sent wtxidrelay'."),
    ("HandshakeMessageOrder", "comesBefore", "HighAndLowBandwidthModes", "Handshake order: 'the node followed verack with sendcmpct (compact blocks)'; Modes: 'A peer picks the mode with the message sendcmpct'."),
    ("HandshakeMessageOrder", "comesBefore", "HeadersBatchOf2000", "Handshake order: 'getheaders (what chain does the peer have)' after verack; Headers: 'the node asks with getheaders and the peer answers with at most 2,000 headers'."),
    ("RelayNetworkHistory", "comesBefore", "CompactBlocksYear", "Relay history: 'Before compact blocks, miners built private networks'; Year: 'the relay network, which was in use in 2015'; 'BIP 152 was assigned its number on 2016-04-27'."),
    ("Addrv2Networks", "buildsOn", "ProtocolVersionNumber", "Protocol version: 'The number 70016 is also the one that BIP 339 and BIP 155 build on'."),
    ("ForwardErrorCorrectionDemo", "buildsOn", "ShortIdsAreSixBytes", "FEC: 'FIBRE ... uses it on UDP together with compact blocks'; 'the compact block idea on which FIBRE builds'."),
    ("MerkleblockForOneMatch", "buildsOn", "MerklePathProof", "Merkleblock: 'a partial Merkle tree holding only the paths ... the partial tree led to the root in the header'; Merkle path: 'a client with the header can recompute the root and compare'."),
    ("HeaderChainSize", "buildsOn", "HeaderChainLinks", "Header chain links: 'a node can check the whole chain of headers by itself, without any block' and 'lightweight clients that synchronize the headers alone'; Header chain size: 'downloads only the block headers'."),
    ("OrphanWaitsForParent", "takesPartIn", "TxAnnouncementByWtxid", "Orphan: 'the node asked for the child by its wtxid (an inv entry of type 5)'; Announcement: 'the identifier is the wtxid ... announced with the type MSG_WTX (0x00000005)'."),
    ("ConnectionTypes", "buildsOn", "AddrGossipFormat", "Connection types: 'addr-fetch connections that only ask for addresses and leave'; Addr gossip: 'it learns more addresses by asking, with the message getaddr'."),
    ("PlaintextV1", "buildsOn", "MessageFraming", "Plaintext: 'the first bytes that the script sent over a v1 connection were fabfb5da, the magic of the test chain'; Framing: 'every message ... on the old transport is a block of bytes with a header of 24 bytes: 4 bytes of magic'."),
    ("ShortIdsAreSixBytes", "isMeansAgainst", "BlockFindingRaceProbability", "Race: 'faster block relay is a security matter ' and 'topic page on compact block relay presents it as a way to cut the delay'."),
    ("BasicFilterParameters", "replaces", "BloomFilterWireFormat", "Filter idea: 'Osuntokun and Alex Akselrod, who replaced the Bloom filter by the Golomb-coded set'; Bloom disabled: 'presents the block filters as the safer replacement of BIP 37'."),
    ("FilterFalsePositiveRate", "isComparedWith", "BloomDisabledByDefault", "False positive: 'the false positives do not harm privacy as the Bloom filters did'; Bloom disabled: 'give the node a view of the client's addresses with weak privacy'."),
    ("BasicFilterParameters", "isComparedWith", "ShortIdsAreSixBytes", "Basic filter: 'SipHash-2-4 keyed by the block hash ... its SipHash returned the reference value a129ca6149be45e5'; Short ids: 'SipHash-2-4 ... the reference test value a129ca6149be45e5 of the SipHash paper'."),
    ("HeadersPresync", "isComparedWith", "OrphanageLimits", "Presync: 'an attacker could send millions of low-work headers to fill its memory'; Orphanage: 'a place where an attacker could try to fill the memory with transactions that never become valid'."),
    ("FeefilterHonoured", "isComparedWith", "RelayFlagSilencesTransactions", "Relay flag: 'three peers were connected to the same node: one normal peer, one with relay false and one that had set a minimum fee with feefilter'."),
    ("MempoolIsLocalUtxoIsShared", "isComparedWith", "OrphanWaitsForParent", "Mempool: 'the mempool and the orphan pool are a node's local view and may differ from node to node'; Orphan: 'it keeps it in a small separate pool, the orphanage'."),
    ("FiveNetworks", "isReasonFor", "Addrv2Networks", "Five networks: 'each has its own address format, which is why addrv2 was invented'."),
    ("FiveNetworks", "isMeansAgainst", "RoutingAttack", "Routing: 'encryption does not help against a route that is simply dropped, whereas peers from different networks, such as Tor, do'."),
    ("ConnectionTypes", "isMeansAgainst", "EclipseAttack", "Eclipse: 'The two block-relay-only connections of Bitcoin Core are part of the answer, since they are not seen by transaction gossip'."),
    ("RelayFlagSilencesTransactions", "isReasonFor", "ConnectionTypes", "Relay flag: 'a node that sets it to false asks to receive blocks only ... and is the base of the block-relay-only connections of Bitcoin Core'."),
    ("ConnectionTypes", "isCharacterizedBy", "PlaintextV1", "Connection types: 'block-relay-only did not [relay transactions] and spoke the v1 transport, the old plaintext one'."),
]
EVIDENCE = {(a, p, b): e for a, p, b, e in SECTION_LINKS}

# ---- checks of this module's own claims (run at import, so a wrong end cannot be built) ----------------------------------------------------------------------------------------------------
_parent = {}
for _t, _m, _l, *_ in _TAX:
    _parent[_l] = _m; _parent[_m] = _t; _parent.setdefault(_t, None)
def _section(leaf): return _parent[leaf]
_pn = {p["name"]: p for p in SECTION_PROPS}
assert len(_pn) == len(SECTION_PROPS) == 9, "duplicate property name"
assert len({p["label"].lower() for p in SECTION_PROPS}) == len(SECTION_PROPS)
assert len({(p["category"], tuple(p["parents"])) for p in SECTION_PROPS}) == len(SECTION_PROPS), "two properties of one category and super-property (BP-D61)"
assert len({p["definition"] for p in SECTION_PROPS}) == len(SECTION_PROPS)
_leaves = {l for _t, _m, l, *_ in _TAX}
assert len(SECTION_LINKS) == 28
for _a, _p, _b, _e in SECTION_LINKS:
    assert _a in _leaves and _b in _leaves, (_a, _b)
    assert _p in _pn, _p
    assert _section(_a) != _section(_b), "%s and %s are in one section" % (_a, _b)
assert all(any(l[1] == n for l in SECTION_LINKS) for n in _pn), "a declared property no link uses"
_secs = {m for _t, m, *_ in _TAX}
_rel = {s: 0 for s in _secs}
for _a, _p, _b, _e in SECTION_LINKS:
    _rel[_section(_a)] += 1; _rel[_section(_b)] += 1
assert all(_rel.values()), "a section with no link: %s" % [s for s, n in _rel.items() if not n]
assert len(_secs) == 17
