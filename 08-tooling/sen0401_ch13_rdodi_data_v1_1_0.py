"""SEN0401 chapter 13 (Bitcoin Security) for the RDODI build (generic builder sen0401_rdodi_build_v1_4_0.py), version 1.1.0: the research of v1.0.2 plus the relationships between the chapter's sections, stated as links
(the owner's decision of 2026-10-22: the relationships between the sections of a chapter are discovered with the OEE relationship taxonomy and stated in the chapter research as links, never as text; change request ex:CR3_Ch13Links).
Everything the v1.0.2 module holds is taken over unchanged (sources, taxonomy, executed expressions, paragraphs, findings, claims); this module adds SECTION_PROPS (the relation properties of the domain T-Box, one per meaning,
each with an OEE relationship category, BP-D58 and BP-D61), SECTION_LINKS (object-property links between the X_ individuals of two different sections, each with the words of the chapter's own text that state it), DECLARE_IO and MODIFIED.
A section is a second-level class of the taxonomy (16 of them); the example of a third-level class (its X_ individual) belongs to the section above it. Same interface as the data modules of chapter 10 version 1.2.0 and chapter 11 version 1.1.0.
How the links were found: every pair of sections was asked, category by category (semantic: compositional, causal, comparative, characterization, participation; syntactic: reference by name; temporal: temporal order, succession; requirement; epistemic),
and a link was kept only where the research text of the two examples states it in words that can be quoted; each quoted fragment is checked against the paragraph of its example when this module is imported, so a wrong quotation cannot be built.
Where the text states nothing, no link was made (no section is joined to another only to join it)."""
__version__ = "1.1.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch13_rdodi_data_v1_0_2 import *          # noqa: F401,F403 - the research of v1.0.2, unchanged
from sen0401_ch13_rdodi_data_v1_0_2 import TAX as _TAX, BODY as _BODY, LABELS as _LABELS
# build: python3 -B sen0401_rdodi_build_v1_4_0.py sen0401_ch13_rdodi_data_v1_1_0 2026-10-18T21:48:28Z   (the verification time of v1.0.2, so that every source keeps the time it was opened)

VERSION = "1_1_0"
MODIFIED = "2026-10-27"   # the day the section links were stated; the sources and claims keep the day of version 1.0.2
DECLARE_IO = True         # chx:input and chx:output, which the A-Box uses and no file declared (the one finding of oe_link_discovery on version 1.0.2)
LINK_EVIDENCE = True      # each link is annotated with the words of the chapter's own text that state it
LINK_SHAPES = True        # the domain shapes check the start and the end of every link

REQUIRES = "http://purl.org/dc/terms/requires"
REFERENCES = "http://purl.org/dc/terms/references"

_TAXO = "RELATIONSHIP_TAXONOMY_RESEARCH_v1_11_0.md of the OEE, section 3, the category %s; construction method BP-D58."
_ANY = ("The domain and the range are owl:Thing on purpose: the ends are examples of two different sections, and the six top classes of the taxonomy are pairwise disjoint, so no named class covers both "
        "ends (the rule BP-D23 for a property used across branches with no common ancestor). The class pair belongs to the link and to the words that state it. The shape of the domain shapes file checks that both ends are individuals of the chapter.")

def P(name, label, category, definition, comment, source, parents=(), alt=(), chars=()):
    return dict(name=name, label=label, altlabels=list(alt), category=category, domain="owl:Thing", range="owl:Thing", definition=definition, comment=comment + " " + _ANY, source=source, parents=list(parents), characteristics=list(chars))

SECTION_PROPS = [
    P("refersTo", "refers to", "ReferenceByName",
      "Links an example to the example of another section when the account of the first names the thing that the second illustrates and draws on it: the same rule one level up, the tamper test, the release check, the list of BIP 39, the seed of BIP 32, the descriptor of a backup, the PSBT. It says that the first account points to the second; it states no cause and no need.",
      "Reused: dcterms:references says that a resource points to another; the category records that the account names the thing by its name and that the name is carried as a link, never as a string.",
      _TAXO % "Reference by name (under the syntactic relationship)", parents=[REFERENCES]),
    P("hasConsequence", "has consequence", "Causal",
      "Links an example to the example of another section when the account says that what the first illustrates brings about what the second illustrates: a payment that reveals no secret and the traffic that needs no encryption, the new seed of an encrypted wallet and the backup that is stale at once.",
      "No standard relation was reused: the Relations Ontology could not be opened in this run, so none was checked against the account.",
      _TAXO % "Causal relationship"),
    P("isComparedWith", "is compared with", "Comparative",
      "Links two examples of different sections when the account sets what they illustrate side by side, as alike or as different: the same lesson of a lost key and a lost passphrase, the same error of a wrong order and a missing descriptor, a stretch compared with the rounds of BIP 39, a PIN that makes the guesser wait compared with a file attacked offline, a coin with a hologram compared with a printed paper wallet, secret sharing compared with multisignature.",
      "Symmetric, so the link is stated once and holds both ways. No standard relation says a comparison.",
      _TAXO % "Similarity and opposition (Comparative)", chars=["owl:SymmetricProperty"]),
    P("buildsOn", "builds on", "Requirement",
      "Links an example to the example of another section that illustrates something the first one needs in order to hold: the loss of one key of three is survived only if the descriptor is kept. It differs from refers to (a name is not a need) and from has consequence (the needed thing is not the cause of the first).",
      "Reused: dcterms:requires says that a resource is required by another to support its function or coherence, which is what the sentence of the link says.",
      _TAXO % "Requirement", parents=[REQUIRES]),
    P("isEarlierThan", "is earlier than", "TemporalOrder",
      "Links an example to the example of another section when the dates the two accounts give put what the first illustrates before what the second illustrates: the sale of the physical coins until November 2013 before the closing of the exchange in early 2014.",
      "OWL-Time's before was not reused: it joins temporal entities (instants and intervals) and the ends here are examples that carry dates.",
      _TAXO % "Temporal order", chars=["owl:AsymmetricProperty"]),
    P("qualifies", "qualifies", "Epistemic",
      "Links the example that records what was not run to the example of another section whose claim it limits: the claim of the second is read from a page or a document and not from a run, and the first example says so. It states a limit of knowledge about the second example, not a cause and not a need.",
      "No standard relation was reused: none of the standard properties checked says that an account limits the claim of another; the citation relations of CiTO join publications and were not checked against examples.",
      _TAXO % "Epistemic and argumentative relationship"),
]

# (source example, property, target example, [(example, fragment of its paragraph), (example, fragment of its paragraph)]); the two fragments are the words of the chapter's own text that state the link
_L = "WhatWasNotExecuted"
SECTION_LINKS_RAW = [
    # the same thing named in the account of another section
    ("TamperBreaksSignature", "refersTo", "GenerateblockRefusesBadSignature",
     [("TamperBreaksSignature", "A block with the swapped version was refused too, which is the same rule one level up"),
      ("GenerateblockRefusesBadSignature", "The call generateblock with the address-swapped transaction answered error code -25")]),
    ("HardwareDoesNotCheckTheAddress", "refersTo", "TamperBreaksSignature",
     [("HardwareDoesNotCheckTheAddress", "In our tamper test the swapped transaction was refused because the old signature no longer matched"),
      ("TamperBreaksSignature", "swapped the recipient's output script for an attacker's script")]),
    ("AssumeValidShortcut", "refersTo", "TarballHashMatches",
     [("AssumeValidShortcut", "the hash is part of the software that people download, which is why the release check of the next paragraphs matters"),
      ("TarballHashMatches", "equals its line among the 28 lines of SHA256SUMS")]),
    ("BrainwalletGuessTime", "refersTo", "Bip39MnemonicChecksum",
     [("BrainwalletGuessTime", "a phrase of 4 words from a list of 2,048 words, the list of BIP 39"),
      ("Bip39MnemonicChecksum", "the list has 2,048 words")]),
    ("PaperWalletsAreObsolete", "refersTo", "Bip32MasterVector",
     [("PaperWalletsAreObsolete", "a written seed that feeds a hierarchical deterministic wallet"),
      ("Bip32MasterVector", "A hierarchical deterministic wallet needs one secret to make all keys")]),
    ("Codex32AndSlip39", "refersTo", "Bip32MasterVector",
     [("Codex32AndSlip39", "splits a BIP 32 seed into up to 31 shares"),
      ("Bip32MasterVector", "BIP 32 fixes how: the master key is the HMAC-SHA512 of the seed under the text Bitcoin seed")]),
    ("ExternalSignerSupport", "refersTo", "DescriptorIsPartOfBackup",
     [("ExternalSignerSupport", "BIP 388 explains why descriptors alone are not enough for such devices"),
      ("DescriptorIsPartOfBackup", "the wallet policies that hardware devices register")]),
    ("CoreHasNoMnemonics", "refersTo", "DescriptorIsPartOfBackup",
     [("CoreHasNoMnemonics", "Recovery in Core is by wallet file and descriptors"),
      ("DescriptorIsPartOfBackup", "a backup of keys without the descriptor is incomplete")]),
    ("TwoOfThreeSigning", "refersTo", "PsbtThroughColdNode",
     [("TwoOfThreeSigning", "the first key alone left the PSBT incomplete with one signature"),
      ("PsbtThroughColdNode", "A partially signed bitcoin transaction is a container that travels between a machine that knows the coins and a machine that holds the keys")]),
    # what one illustrates brings about the other
    ("SignedTransactionHidesKey", "hasConsequence", "BookSaysNoEncryption",
     [("SignedTransactionHidesKey", "a Bitcoin payment can travel over an open channel because it authorizes one value to one recipient and reveals no secret"),
      ("BookSaysNoEncryption", "no encryption is required for Bitcoin traffic")]),
    ("EncryptionMakesNewSeed", "hasConsequence", "StaleBackupMissesFunds",
     [("EncryptionMakesNewSeed", "Any coins received by the new seed cannot be recovered from the older backups"),
      ("StaleBackupMissesFunds", "after an encryption the backup is stale at once, as the earlier paragraph showed")]),
    # something the first needs
    ("KeyLossTolerance", "buildsOn", "DescriptorIsPartOfBackup",
     [("KeyLossTolerance", "a lost descriptor makes even three keys useless"),
      ("DescriptorIsPartOfBackup", "a wallet given the full descriptor again found the 2.0 coins")]),
    # alike or different
    ("WrongPassphraseError", "isComparedWith", "LostSevenThousand",
     [("WrongPassphraseError", "This is the same lesson as the book's story of backups lost with their own keys"),
      ("LostSevenThousand", "securing coins too well may make them unfindable")]),
    ("SortedmultiOrder", "isComparedWith", "DescriptorIsPartOfBackup",
     [("SortedmultiOrder", "which is the same error as the missing descriptor of the previous subject"),
      ("DescriptorIsPartOfBackup", "the same three keys in a different order under multi gave another address and balance 0.0")]),
    ("CrypterParameters", "isComparedWith", "Bip39SeedFromWords",
     [("CrypterParameters", "12.2 times the 2048 rounds of PBKDF2 in BIP 39"),
      ("Bip39SeedFromWords", "The seed is HMAC-SHA512 with 2048 rounds over the words")]),
    ("TrezorPinWait", "isComparedWith", "StretchingBuysDays",
     [("TrezorPinWait", "which is the opposite of the file on a disk that can be copied and attacked offline"),
      ("StretchingBuysDays", "costs a single machine about 1,242.8 days to exhaust")]),
    ("CasasciusHologram", "isComparedWith", "PaperWalletsAreObsolete",
     [("CasasciusHologram", "a coin with a hologram is a nicer package of the same idea"),
      ("PaperWalletsAreObsolete", "the paper wallet, a single private key and its address printed together")]),
    ("ShamirTwoOfThree", "isComparedWith", "TwoOfThreeSigning",
     [("ShamirTwoOfThree", "Multisignature splits control among keys, and secret sharing splits a single secret into pieces"),
      ("TwoOfThreeSigning", "a 2-of-3 wallet needed two signers")]),
    # earlier in time
    ("CasasciusHologram", "isEarlierThan", "MtGoxLoss",
     [("CasasciusHologram", "sold them until 26 November 2013"),
      ("MtGoxLoss", "handled over 70% of all bitcoin transactions by early 2014 and then closed")]),
    # what was not run
    (_L, "qualifies", "V2SessionOnBothSides", [(_L, "BIP 324 on the wire"), ("V2SessionOnBothSides", "Nothing was captured on the wire here")]),
    (_L, "qualifies", "SignatureNeedsKeys", [(_L, "a good gpg verification"), ("SignatureNeedsKeys", "could call none good, exit code 2")]),
    (_L, "qualifies", "PsbtThroughColdNode", [(_L, "a true air gap"), ("PsbtThroughColdNode", "so no true air gap or removable medium was involved")]),
    (_L, "qualifies", "ExternalSignerSupport", [(_L, "the hardware device"), ("ExternalSignerSupport", "No device was available here, so the signer is read from documents and not run")]),
    (_L, "qualifies", "PaperWalletsAreObsolete", [(_L, "paper and metal backups"), ("PaperWalletsAreObsolete", "No paper, printer or steel plate was used in this chapter; the claim is from the pages only")]),
    (_L, "qualifies", "CoreHasNoMnemonics", [(_L, "BIP 39 recovery in Core"), ("CoreHasNoMnemonics", "This is a statement about the saved files only, not about every wallet program")]),
    (_L, "qualifies", "Codex32AndSlip39", [(_L, "Shamir in a wallet"), ("Codex32AndSlip39", "None of these was run on a device in this chapter")]),
    (_L, "qualifies", "MtGoxLoss", [(_L, "an exchange breach"), ("MtGoxLoss", "No server was attacked in this chapter, so the case is read from the pages and not run")]),
    (_L, "qualifies", "BitfinexSegregatedWallets", [(_L, "The stories of Mt. Gox, Bitfinex and Casascius are read from the saved pages"), ("BitfinexSegregatedWallets", "The page does not say how the keys were arranged, so we do not claim a technical cause")]),
    (_L, "qualifies", "CasasciusHologram", [(_L, "The stories of Mt. Gox, Bitfinex and Casascius are read from the saved pages"), ("CasasciusHologram", "Casascius coins were metal coins with a private key on paper hidden under a tamper-evident hologram")]),
    (_L, "qualifies", "HeirWaitsTenBlocks", [(_L, "estate planning with a lawyer"), ("HeirWaitsTenBlocks", "the lawyer, the court and the family were not part of this run")]),
]

def _lab(x): return _LABELS.get(x) or x
SECTION_LINKS = []
for _a, _p, _b, _ev in SECTION_LINKS_RAW:
    SECTION_LINKS.append((_a, _p, _b, "; ".join("%s: '%s'" % (_lab(e), f) for e, f in _ev) + "."))
EVIDENCE = {(a, p, b): e for a, p, b, e in SECTION_LINKS}

# ---- checks of this module's own claims (run at import, so a wrong end or a wrong quotation cannot be built) ----------------------------------------------------------------------------------------
_parent = {}
for _t, _m, _l, *_ in _TAX:
    _parent[_l] = _m; _parent[_m] = _t; _parent.setdefault(_t, None)
def _section(leaf): return _parent[leaf]
_pn = {p["name"]: p for p in SECTION_PROPS}
assert len(_pn) == len(SECTION_PROPS) == 6, "duplicate property name"
assert len({p["label"].lower() for p in SECTION_PROPS}) == len(SECTION_PROPS)
assert len({(p["category"], tuple(p["parents"])) for p in SECTION_PROPS}) == len(SECTION_PROPS), "two properties of one category and super-property (BP-D61)"
assert len({p["definition"] for p in SECTION_PROPS}) == len(SECTION_PROPS)
_leaves = {l for _t, _m, l, *_ in _TAX}
for _a, _p, _b, _ev in SECTION_LINKS_RAW:
    assert _a in _leaves and _b in _leaves, (_a, _b)
    assert _p in _pn, _p
    assert _section(_a) != _section(_b), "%s and %s are in one section" % (_a, _b)
    assert len(_ev) == 2 and {e for e, f in _ev} == {_a, _b}, (_a, _b)
    for _e, _f in _ev:
        assert '"' not in _f and _f in _BODY[_e], "the words are not in the paragraph of %s: %s" % (_e, _f)
assert len({(a, p, b) for a, p, b, _ in SECTION_LINKS_RAW}) == len(SECTION_LINKS_RAW), "a link stated twice"
assert all(any(l[1] == n for l in SECTION_LINKS_RAW) for n in _pn), "a declared property no link uses"
_secs = {m for _t, m, *_ in _TAX if _t is not None}
_rel = {s: 0 for s in _secs}
for _a, _p, _b, _e in SECTION_LINKS:
    _rel[_section(_a)] += 1; _rel[_section(_b)] += 1
assert all(_rel.values()), "a section with no link: %s" % [s for s, n in _rel.items() if not n]
assert len(_secs) == 16, len(_secs)
