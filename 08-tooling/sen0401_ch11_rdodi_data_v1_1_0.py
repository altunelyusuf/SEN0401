"""SEN0401 chapter 11 (The Blockchain) for the RDODI build, version 1.1.0: the research of v1.0.1 plus the relationships between the chapter's sections, stated as links (ruling G134).
Everything the v1.0.1 module holds is taken over unchanged (sources, taxonomy, executed expressions, paragraphs, findings); this module adds PROPS (the relation properties of the domain
TBox, each with an OEE relationship category), DATAPROPS, LINKS (object-property links between the X_ individuals of two different sections) and the date of this version.
Same interface as the data module of chapter 10 version 1.1.0 (SECTION_PROPS, SECTION_LINKS, DECLARE_IO, MODIFIED) and builder 1.3.0 for what chapter 11 adds (LINK_EVIDENCE, LINK_SHAPES, owl:Thing as domain and range).
A section here is a second-level class of the taxonomy (16 of them); the example of a third-level class (its X_ individual) belongs to the section above it."""
__version__ = "1.1.0"
# 1.1.0 (over 1.0.1): section links. Built with sen0401_rdodi_build_v1_2_0.py: python3 -B sen0401_rdodi_build_v1_3_0.py sen0401_ch11_rdodi_data_v1_1_0 2026-10-15T00:00:00Z
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch11_rdodi_data_v1_0_1 import *   # noqa: F401,F403 - the research of v1.0.1, unchanged
from sen0401_ch11_rdodi_data_v1_0_1 import DATE   # the day every source was opened and every claim executed stays 2026-10-15

VERSION = "1_1_0"
MODIFIED = "2026-10-22"   # the day the section links were stated; the sources and claims keep the day of 2026-10-15
DECLARE_IO = True         # chx:input and chx:output, which the ABox uses and no file declared (the one finding of oe_link_discovery on version 1.0.1)
LINK_EVIDENCE = True      # each link is annotated with the sentence of the document that states it
LINK_SHAPES = True        # the domain shapes check the start and the end of every link

_TAXO = "RELATIONSHIP_TAXONOMY_RESEARCH_v1_11_0.md of the OEE (OE v2.32.0), section 3, the category %s; construction method BP-D58."
_ANY = ("The domain and the range are owl:Thing on purpose: the ends are examples of two different sections, and the six top classes of the taxonomy are pairwise disjoint, so no named class covers both "
        "ends (the rule BP-D23 for a property used across branches with no common ancestor). The shape of the domain shapes file checks that both ends are individuals of the chapter.")

SECTION_PROPS = [
    dict(name="hasComponent", label="has component", category="Compositional", domain="owl:Thing", range="owl:Thing", parents=["http://purl.org/dc/terms/hasPart"],
         definition="Links an example to the example of another section that illustrates a part of what it illustrates, the part being one the document itself names for the whole: a block and its header, a header and its merkle root, a merkleblock message and the header it holds.",
         comment="Reused: dcterms:hasPart says that a resource is included in another; this property narrows it to part and whole of the things the examples illustrate. " + _ANY,
         source=_TAXO % "Compositional relationship (part and whole)"),
    dict(name="refersTo", label="refers to", category="ReferenceByName", domain="owl:Thing", range="owl:Thing", parents=["http://purl.org/dc/terms/references"],
         definition="Links an example to the example of another section when the account of the first names the thing that the second illustrates and draws on it: the genesis block, the previous-block field, the hash, a chain by its genesis hash.",
         comment="Reused: dcterms:references says that a resource points to another; the category records that the account names the thing by its name and that the name is carried as a link, never as a string. " + _ANY,
         source=_TAXO % "Reference by name (under the syntactic relationship)"),
    dict(name="hasConsequence", label="has consequence", category="Causal", domain="owl:Thing", range="owl:Thing", parents=[],
         definition="Links an example to the example of another section when the account says that what the first illustrates brings about what the second illustrates: a rule and the flaw it creates, the target and the zeros of the hash, accumulated work and the branch that wins.",
         comment="No standard relation was reused: the Relations Ontology could not be opened in this run, so none was checked against the account. " + _ANY,
         source=_TAXO % "Causal relationship"),
    dict(name="isComparedWith", label="is compared with", category="Comparative", domain="owl:Thing", range="owl:Thing", parents=[], characteristics=["owl:SymmetricProperty"],
         definition="Links two examples of different sections when the account sets what they illustrate side by side, as alike or as different: a hash and a height, a block count and the height of the main chain, the stages of the development pipeline.",
         comment="Symmetric, so the link is stated once and holds both ways. No standard relation says a comparison. " + _ANY,
         source=_TAXO % "Similarity and opposition (Comparative)"),
    dict(name="isFollowedBy", label="is followed by", category="OrderingSequence", domain="owl:Thing", range="owl:Thing", parents=[], characteristics=["owl:AsymmetricProperty"],
         definition="Links an example to the example that comes next in an order the account gives: the stages of the development pipeline, regtest and then signet or testnet.",
         comment="A link from each member to the next, the form the category names; no standard relation was found for a next member of an order of things. " + _ANY,
         source=_TAXO % "Ordering in a list (ordering and sequence)"),
    dict(name="isEarlierThan", label="is earlier than", category="TemporalOrder", domain="owl:Thing", range="owl:Thing", parents=[], characteristics=["owl:AsymmetricProperty"],
         definition="Links an example to the example of another section when the dates the two accounts give put what the first illustrates before what the second illustrates: the hash tree of 1979 before the linked time-stamping of 1991.",
         comment="OWL-Time's before was not reused: it joins temporal entities (instants and intervals) and the ends here are examples that carry dates. " + _ANY,
         source=_TAXO % "Temporal order"),
]

# (source example, property, target example, the sentence of the document that states it). Every pair of sections has one link type at most.
SECTION_LINKS = [
    # part and whole
    ("BlockIsHeaderPlusTransactions", "hasComponent", "HeaderIs80Bytes",
     "A block is a container: a small header, then a counter, then the transactions (Block is header plus transactions); the header is exactly 80 bytes (The header is 80 bytes)."),
    ("HeaderIs80Bytes", "hasComponent", "RootIsAlways32Bytes",
     "The 80 bytes of the header are 4 for the version, 32 for the previous block hash, 32 for the merkle root (The header is 80 bytes); the root is the single 32-byte summary of the transactions in the header (Root is always32 bytes)."),
    ("MerkleblockForLightClients", "hasComponent", "HeaderIs80Bytes",
     "A merkleblock message holds the header and a merkle path, 248 bytes of which 80 are the header (Merkleblock for light clients); the fixed size of the header makes light clients possible (The header is 80 bytes)."),
    # cause and consequence
    ("TargetCompactEncoding", "hasConsequence", "HashLeadingZeros",
     "The zeros of a block hash are the visible result of the rule that the hash, read as a number, must not exceed the target (Hash leading zeros); the header stores the target in 4 bytes (Target compact encoding)."),
    ("TargetCompactEncoding", "hasConsequence", "ChainWorkAccumulates",
     "Each header adds the work that its target stands for (Chain work accumulates); the work of one block at difficulty 1 is 0x100010001 (Target compact encoding)."),
    ("BlockHashIsDoubleSha256", "hasConsequence", "TamperingBreaksDescendants",
     "Because the previous-block field is part of the header and so of the hash, changing a block changes its own hash and breaks the link in the next block (Tampering breaks descendants; Block hash is double sha256)."),
    ("CoinbaseMaturity100", "hasConsequence", "RegtestBalanceAfter500",
     "The book's balance is correct only because rewards must be 100 blocks deep to be spent, and 931.25 coins stayed immature (Regtest balance after 500 blocks); the rule applies to every chain, regtest included (Coinbase maturity of 100 blocks)."),
    ("ChainWorkAccumulates", "hasConsequence", "ForkResolvedByMoreWork",
     "A node follows the chain with the most accumulated work (Chain work accumulates); a fork is resolved when one branch becomes heavier (Fork resolved by more work)."),
    ("OddLeafDuplicated", "hasConsequence", "Cve20122459Trees",
     "The rule that an odd last hash is duplicated has a consequence: different lists of transactions can have the same merkle root (CVE-2012-2459 trees); the rule has a price which the section on the design flaw shows (Odd leaf duplicated)."),
    # a thing named in the account of another
    ("HeightIsNotUnique", "refersTo", "TwoChildrenOneParent",
     "Two different children of the same parent were both at height 511 on the test chain (Height is not unique); that fork is the one the section on forks builds (Two children one parent)."),
    ("HeightFromGenesis", "refersTo", "GenesisHardcoded",
     "The genesis block sits at height 0 (Height from genesis); a fresh node reported height 0 and 0 headers because it knows only the genesis block built into its code (Genesis hardcoded)."),
    ("GlacierCoreAnalogy", "refersTo", "CoinbaseMaturity100",
     "The 100 blocks of coinbase maturity are about 16.7 hours of the layers of the picture (Glacier core analogy; Coinbase maturity of 100 blocks)."),
    ("GenesisHashRecomputed", "refersTo", "BlockHashIsDoubleSha256",
     "The 80-byte genesis header is hashed twice to obtain the genesis hash (Genesis hash recomputed), which is the double SHA-256 of the header (Block hash is double sha256)."),
    ("ChancellorOfTheHeadline", "refersTo", "GenesisCoinbaseMessage",
     "The headline in the genesis block, on the Chancellor, is the text of the coinbase message (The Chancellor of the headline; Genesis coinbase message)."),
    ("ChancellorOfTheHeadline", "refersTo", "TimestampField",
     "The timestamp in the genesis header, 2009-01-03 18:15:05 UTC, falls on the same day as the issue (The Chancellor of the headline; Timestamp field)."),
    ("PreviousHashPointsToParent", "refersTo", "GenesisHardcoded",
     "The sequence of hashes is the chain that runs back to the genesis block (Previous hash points to parent); a node follows the parent links back to the genesis block it already knows (Genesis hardcoded)."),
    ("NodeRejectsMutatedBlock", "refersTo", "BlockHashIsDoubleSha256",
     "The mutated block has the same hash as the original, so a careless node could remember that hash as bad (Node rejects mutated block; Block hash is double sha256)."),
    ("SixtyFourByteWeakness", "refersTo", "MerkleblockForLightClients",
     "A light client that checks a merkle path is the one at risk of mistaking a 64-byte transaction for an inner node (The 64-byte weakness; Merkleblock for light clients)."),
    ("TreeDepth", "refersTo", "PathLengthLogarithm",
     "Proving that one transaction is included takes about log2(N) hashes, the depth of the tree (Tree depth); the path grows with the logarithm of the count of transactions (Path length logarithm)."),
    ("BlockIsHeaderPlusTransactions", "refersTo", "GenesisListingMatchesBook",
     "The genesis block is 80 + 1 + 204 = 285 bytes (Block is header plus transactions); the book's listing of the genesis block agrees with the size 285 (Genesis listing matches book)."),
    ("SeveralChainsExist", "refersTo", "Testnet4Replaces",
     "The genesis hash 00000000da84f2ba... that the node of testnet4 reported (Several chains exist) is the hash of the genesis block of testnet4 (Testnet4 replaces testnet3)."),
    ("SeveralChainsExist", "refersTo", "SignetGenesisShared",
     "The genesis hash 00000008819873e9... that the node of the signet reported (Several chains exist) is the hash 000000088198... of the genesis block of every signet (Signet genesis shared)."),
    ("SeveralChainsExist", "refersTo", "RegtestStartState",
     "The genesis hash 0f9188f1... that the node of regtest reported (Several chains exist) is the best block of a fresh regtest node (Regtest start state)."),
    # alike or different
    ("HeightIsNotUnique", "isComparedWith", "BlockHashIsDoubleSha256",
     "A block has two names: its hash identifies it uniquely, its height does not (Height is not unique; Block hash is double sha256)."),
    ("TestnetBlockStorms", "isComparedWith", "HeightFromGenesis",
     "Testnet3 had 5,189,394 blocks, more than 5 times the 971,537 blocks of mainnet (Testnet block storms; Height from genesis)."),
    ("PipelineOrder", "isComparedWith", "RegtestStartState",
     "The stages differ in what the code gives them: regtest has one dummy seed and no peers (Pipeline order; Regtest start state)."),
    ("PipelineOrder", "isComparedWith", "SignetChallengeIsMultisig",
     "The stages differ in what the code gives them: signet has 2 DNS seeds and a block rule that needs a signature (Pipeline order; Signet challenge is a multisig)."),
    ("PipelineOrder", "isComparedWith", "TestnetMinimumDifficulty",
     "The stages differ in what the code gives them: testnet3 has 5 seeds and the minimum-difficulty rule (Pipeline order; Testnet minimum difficulty)."),
    ("SharedGenesisTransaction", "isComparedWith", "Testnet4Replaces",
     "Mainnet, testnet3, signet and regtest start with the same 204-byte coinbase transaction, and testnet4 breaks the pattern with its own of 180 bytes (Shared genesis transaction; Testnet4 replaces testnet3)."),
    # the next in an order
    ("RegtestStartState", "isFollowedBy", "SignetChallengeIsMultisig",
     "The book recommends a development pipeline: test the code on regtest, then on signet or testnet, and finally on mainnet (Pipeline order; Regtest start state; Signet challenge is a multisig)."),
    ("RegtestStartState", "isFollowedBy", "TestnetMinimumDifficulty",
     "The book recommends a development pipeline: test the code on regtest, then on signet or testnet, and finally on mainnet (Pipeline order; Regtest start state; Testnet minimum difficulty)."),
    # earlier in time
    ("HashTreeHistory", "isEarlierThan", "HashChainedTimestamps",
     "Merkle patented the hash tree in 1979 and described it in 1980 (Hash tree history); Haber and Stornetta described linked time-stamping in 1991 (Hash-chained timestamps)."),
]
