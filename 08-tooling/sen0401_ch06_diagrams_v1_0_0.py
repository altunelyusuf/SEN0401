#!/usr/bin/env python3
"""SEN0401 chapter 6 - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages a use-case diagram, the life of a transaction a state diagram, an exchange between
parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to diagram
type lives in the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl, CME 0.16.0) so
that it is reused by every course. Same module shape as chapter 5's sen0401_ch05_diagrams_v1_0_0.py; the diagrams
are this chapter's.

This module is the corpus layer for the chapter's diagrams: each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as (the diagram type follows from the mapping, never from the
author), the passage it was read from (also_from names further concepts whose explanations the content draws on,
without the diagram being shown under them), one sentence saying why the pattern fits, and the diagram's content in
the element names the renderer of that type expects (see the mapping's cme:elements). Nothing here says more than
the chapter's own explanations: every element label is made of words that occur in the explanations of the
accompanying concepts or their section, and run_checks() measures that (the grounding ratio) besides the structural
rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ParseTransaction",
        "pattern": "Workflow",
        "title": "Reading a serialized transaction, field by field",
        "concepts": ["TransactionAnatomy", "SerializationFormats", "SerializedTransaction", "ExtendedFormat", "LegacyFormat", "ByteMap", "TransactionParts", "MarkerByte", "FlagByte", "InputCount", "OutputCount", "WitnessStack"],
        "also_from": ["Transaction", "VersionOne", "Outpoint", "InputScript", "SequenceNumber", "AmountField", "OutputScript", "WitnessItem", "LockTimeField", "CompactSize"],
        "read_from": "chapter 6, A serialized Bitcoin transaction and its parts: the version (4 bytes), the marker 0x00 and the flag 0x01 of the extended format, the input count as a compactSize integer, each input's outpoint, input script and sequence, the output count, each output's amount and output script, one witness stack per input, and the lock time; the legacy format has no marker, flag or witness",
        "why": "the chapter walks the bytes in order, with one decision - is the byte after the version a zero marker? - and a loop over the counted inputs and outputs: a workflow",
        "data": {
            "nodes": [
                {"id": "version", "label": "Read the version: 4 bytes, little-endian"},
                {"id": "marker", "label": "Is the next byte a zero marker followed by a nonzero flag?", "kind": "decision"},
                {"id": "ext", "label": "Extended format: read the marker and the flag"},
                {"id": "legacy", "label": "Legacy format: no marker, flag or witness"},
                {"id": "incount", "label": "Read the input count, a compactSize integer"},
                {"id": "input", "label": "Read an input: outpoint, length-prefixed input script, sequence"},
                {"id": "morein", "label": "More inputs?", "kind": "decision"},
                {"id": "outcount", "label": "Read the output count, a compactSize integer"},
                {"id": "output", "label": "Read an output: 8-byte amount, length-prefixed output script"},
                {"id": "moreout", "label": "More outputs?", "kind": "decision"},
                {"id": "witness", "label": "Extended format: one witness stack per input, items length-prefixed"},
                {"id": "locktime", "label": "Read the lock time: the final 4 bytes"},
            ],
            "flows": [["start", "version"], ["version", "marker"], ["marker", "ext", "yes"], ["marker", "legacy", "no"], ["ext", "incount"], ["legacy", "incount"],
                      ["incount", "input"], ["input", "morein"], ["morein", "input", "yes"], ["morein", "outcount", "no"],
                      ["outcount", "output"], ["output", "moreout"], ["moreout", "output", "yes"], ["moreout", "witness", "no"],
                      ["witness", "locktime"], ["locktime", "end"]],
        },
    },
    {
        "id": "TransactionFields",
        "pattern": "TopicAndParts",
        "title": "A transaction and its fields",
        "concepts": ["TransactionIdea", "Transaction", "TransactionParts", "OwnershipRecord", "VersionField", "InputList", "OutputList", "WitnessSerialization", "LockTime"],
        "also_from": ["VersionOne", "MarkerByte", "FlagByte", "Outpoint", "InputScript", "SequenceNumber", "AmountField", "OutputScript", "WitnessStack", "WitnessItem", "LockTimeField", "CompactSize"],
        "read_from": "chapter 6, the parts of a transaction: the version, in the extended format a marker and a flag, the inputs field (a count, then for each input an outpoint, a length-prefixed input script and a sequence), the outputs field (a count, then for each output an amount and a length-prefixed output script), the witness structure (one stack per input, counted items) and the lock time",
        "why": "the chapter lays out one subject, the serialized transaction, by its fields and the fields inside them - a topic and its parts",
        "data": {
            "root": "A serialized transaction",
            "branches": [
                {"label": "Version", "children": ["4 bytes, little-endian: 1 or 2", "Version 2: BIP68 reads the sequence as a timelock"]},
                {"label": "Marker and flag", "children": ["Marker 0x00, flag 0x01: the extended format", "Absent in the legacy format"]},
                {"label": "Inputs", "children": ["A compactSize count, at least one", "Outpoint: 32-byte txid and 4-byte output index", "Length-prefixed input script, empty for a segwit spend", "Sequence: 4 bytes"]},
                {"label": "Outputs", "children": ["A compactSize count, greater than zero", "Amount: 8 bytes of satoshis", "Length-prefixed output script"]},
                {"label": "Witness structure", "children": ["One witness stack per input", "A count of items, each length-prefixed"]},
                {"label": "Lock time", "children": ["The final 4 bytes: zero, a block height or an epoch time"]},
            ],
        },
    },
    {
        "id": "CardGameChannel",
        "pattern": "Interaction",
        "title": "Alice and Bob's card game: the original payment channel",
        "concepts": ["SequenceReplacement", "SequenceNumber", "SetupTransaction", "PaymentChannel", "ReplacementAttack"],
        "also_from": ["SequenceField", "ConflictingTransactions", "DoubleSpendRule", "OptInRbf"],
        "read_from": "chapter 6, Original sequence-based transaction replacement: the setup transaction into a multisignature output, the refund with sequence 0 that neither broadcasts, the rounds of the card game in which the sequence is incremented and the balances move, the final version with sequence 0xffffffff that is broadcast, relayed and confirmed, and the alternative scenario in which Bob broadcasts an earlier version",
        "why": "the passage is an exchange between Alice, Bob and the network in an order that matters - deposit, refund, rounds, final version, and an old version that nodes refuse: an interaction",
        "data": {
            "participants": [{"id": "alice", "label": "Alice"}, {"id": "bob", "label": "Bob"}, {"id": "nodes", "label": "Full nodes and miners"}],
            "messages": [
                ["alice", "bob", "the setup transaction: both deposit into a multisignature output"],
                ["bob", "alice", "the refund transaction, sequence 0, signed by both and not broadcast", "reply"],
                ["alice", "nodes", "the setup transaction is broadcast and confirmed"],
                ["alice", "bob", "round 1: Alice wins, a new version with sequence 1, both sign"],
                ["bob", "alice", "round 2: Bob wins, sequence 2, both sign, not broadcast", "reply"],
                ["alice", "nodes", "the final version, sequence 0xffffffff, is broadcast"],
                ["bob", "nodes", "an earlier version with a lower sequence number"],
                ["nodes", "bob", "not relayed: a higher-sequence version replaces it", "reply"],
                ["nodes", "alice", "the final version is relayed and confirmed by miners", "reply"],
            ],
        },
    },
    {
        "id": "TransactionLife",
        "pattern": "LifeCycle",
        "title": "The life of a transaction, from signing to confirmation",
        "concepts": ["PresignedTransaction", "ReplaceByFee", "OptInRbf", "Bip125Signal", "ConflictingTransactions", "LockTimeField", "RelativeTimelock", "Bip68Timelock", "RelayPolicy", "ConsensusRule"],
        "also_from": ["Transaction", "DoubleSpendRule", "UtxoDatabase", "HeightLock", "MaturityRule", "Coinbase"],
        "read_from": "chapter 6: Protecting presigned transactions (signed but not broadcast, for months or years), Opt-in transaction replacement signaling (an unconfirmed transaction with the BIP125 signal may be replaced by a conflicting one paying a higher fee rate), Lock time (eligible for any block, or only from a height or a time), Sequence as a relative timelock (confirmed only once the spent output has aged), the rule against double spending (only one of two conflicting transactions can be in a valid blockchain)",
        "why": "the passages describe the states a transaction is in over time and the events that move it - signed, held, broadcast, replaced, confirmed, or refused as a conflict: a life cycle",
        "data": {
            "states": [
                {"id": "signed", "label": "Signed: a valid transaction, not yet broadcast"},
                {"id": "held", "label": "Presigned and held, perhaps for years"},
                {"id": "mempool", "label": "Unconfirmed: relayed and kept by full nodes under their policy"},
                {"id": "locked", "label": "Waiting: lock time or relative timelock not yet satisfied"},
                {"id": "replaced", "label": "Replaced: a conflicting transaction paying a higher fee rate"},
                {"id": "confirmed", "label": "Confirmed: included in a block, its outputs in the UTXO database"},
                {"id": "rejected", "label": "Refused: it conflicts with a confirmed transaction"},
            ],
            "initial": "signed",
            "final": ["confirmed", "rejected", "replaced"],
            "transitions": [["signed", "held", "the holder keeps it unbroadcast"], ["held", "mempool", "the holder broadcasts it"], ["signed", "mempool", "the wallet broadcasts it"],
                            ["mempool", "locked", "its lock time or a sequence timelock is not yet satisfied"], ["locked", "mempool", "the height or the median time past reaches the lock"],
                            ["mempool", "replaced", "it signalled replaceability and a conflicting transaction pays more"], ["mempool", "confirmed", "a miner includes it in a block"],
                            ["mempool", "rejected", "a conflicting transaction spending the same output was confirmed first"], ["held", "rejected", "the output it spends was spent by another transaction"]],
        },
    },
    {
        "id": "MalleabilityAttack",
        "pattern": "Interaction",
        "title": "Third-party malleability: a stranger changes the txid, Bob's payment to Carol fails",
        "concepts": ["MalleabilityProblems", "ThirdPartyMalleability", "PushEncoding", "CircularDependency", "SecondPartyMalleability", "Segwit"],
        "also_from": ["Witness", "InputScript", "Txid", "ConflictingTransactions", "DoubleSpendRule", "Transaction", "WitnessStructure"],
        "read_from": "chapter 6, Third-party transaction malleability: Alice creates a transaction with OP_2 in the input script paying Bob, Bob immediately spends that output to Carol, anyone on the network replaces OP_2 with OP_PUSH1 0x02 creating a conflict with a different txid; if the conflicting version is confirmed, Alice's original cannot be, and Bob's transaction cannot spend its output - and Segregated witness: an empty input script keeps witnesses from affecting the txid",
        "why": "the passage is an exchange between Alice, Bob, Carol, a third party and the network, in an order that decides who loses: an interaction",
        "data": {
            "participants": [{"id": "alice", "label": "Alice"}, {"id": "bob", "label": "Bob"}, {"id": "carol", "label": "Carol"}, {"id": "third", "label": "A third party"}, {"id": "net", "label": "The network"}],
            "messages": [
                ["alice", "net", "a transaction that pays Bob, OP_2 in its input script"],
                ["bob", "net", "a transaction that spends that output to Carol, by Alice's txid"],
                ["third", "net", "the same transaction with OP_PUSH1 0x02: a different txid, a conflict"],
                ["net", "alice", "the conflicting version is in the valid blockchain, the original is not", "reply"],
                ["net", "bob", "the output Bob spends does not exist: his transaction is invalid", "reply"],
                ["net", "carol", "no output for Carol to spend", "reply"],
                ["alice", "net", "segregated witness: the witness is separated from the txid, no conflict"],
            ],
        },
    },
    {
        "id": "WhoUsesTransactions",
        "pattern": "SetOfUses",
        "title": "Who works with a transaction, and for what",
        "concepts": ["OwnershipRecord", "OutpointField", "UtxoDatabase", "DoubleSpendRule", "CoinbaseTransaction", "Coinbase", "BlockReward", "WeightUnits", "Weight", "Foundations", "RelayPolicy"],
        "also_from": ["Transaction", "PresignedTransaction", "ContractProtocol", "OptInRbf", "Bip68Timelock", "LockTimeField", "AmountField", "ConsensusRule"],
        "read_from": "chapter 6: a transaction as the data Alice uses to convince full nodes to update their database; the full node that looks up the outpoint, obtains the amount and the conditions, checks for double spending and updates its UTXO database; the miner who creates the coinbase and claims the fees and the subsidy; the software that measures a transaction's weight; the relay policy a node applies to unconfirmed transactions; and the contract protocols that presign transactions",
        "why": "the chapter tells what the different people and programs do with a transaction - build, sign, relay, validate, mine, measure - a set of uses by actors",
        "data": {
            "system": "A BITCOIN TRANSACTION",
            "actors": [{"id": "user", "label": "Wallet user (Alice)"}, {"id": "node", "label": "Full node"}, {"id": "miner", "label": "Miner"}, {"id": "dev", "label": "Contract protocol"}],
            "usecases": [
                {"id": "build", "label": "Build and sign a transaction that spends her outputs"},
                {"id": "broadcast", "label": "Broadcast it to the network"},
                {"id": "lookup", "label": "Look up each outpoint and obtain the amount and the conditions"},
                {"id": "dbl", "label": "Refuse a double spend and update the UTXO database"},
                {"id": "policy", "label": "Apply relay policy to an unconfirmed transaction"},
                {"id": "coinbase", "label": "Create the coinbase and claim the fees and the subsidy"},
                {"id": "weigh", "label": "Measure the weight and the fee rate"},
                {"id": "presign", "label": "Presign transactions with lock times and sequence timelocks"},
            ],
            "links": [["user", "build"], ["user", "broadcast"], ["node", "lookup"], ["node", "dbl"], ["node", "policy"], ["miner", "coinbase"], ["miner", "weigh"], ["user", "weigh"], ["dev", "presign"], ["dev", "build"]],
        },
    },
    {
        "id": "SoftForkSegwit",
        "pattern": "Workflow",
        "title": "Deploying segregated witness as a soft fork",
        "concepts": ["SegregatedWitness", "HardFork", "SoftFork", "WitnessProgram", "WitnessStructure", "AnyoneCanSpend"],
        "also_from": ["Segwit", "InputScript", "OutputScript", "ConsensusRule", "StandardOutput"],
        "read_from": "chapter 6, Segregated witness: the obvious method requires a hard fork, not compatible with older full nodes; the alternative of late 2015 uses a soft fork, a backward-compatible change under which newer nodes may reject blocks older nodes accept but not the reverse; the approach is based on anyone-can-spend output scripts - a number 0 to 16 followed by 2 to 40 bytes is the segwit template; old nodes allow an empty input script, new nodes require one, and the witness goes in the new witness structure",
        "why": "the passage is a procedure with one decision - change the rules in a way old nodes reject, or in a way they accept - and the steps that follow the second branch: a workflow",
        "data": {
            "nodes": [
                {"id": "goal", "label": "The idea: the witness is not part of the data generating the txid"},
                {"id": "choice", "label": "Would older full nodes reject the new blocks?", "kind": "decision"},
                {"id": "hard", "label": "A hard fork: a change older full nodes reject; every node must upgrade"},
                {"id": "soft", "label": "A soft fork: new nodes reject blocks old nodes accept, not the reverse"},
                {"id": "template", "label": "The template: a number 0 to 16 and 2 to 40 bytes, anyone-can-spend"},
                {"id": "old", "label": "Old nodes allow an empty input script and accept the block"},
                {"id": "new", "label": "New nodes require an empty input script and a valid witness"},
                {"id": "field", "label": "The witness structure holds the witness, which is not part of the txid"},
            ],
            "flows": [["start", "goal"], ["goal", "choice"], ["choice", "hard", "yes"], ["choice", "soft", "no"], ["hard", "end"], ["soft", "template"], ["template", "old"], ["template", "new"], ["old", "field"], ["new", "field"], ["field", "end"]],
        },
    },
]

STOP = set("a an the of to in on and or is are be by it its for from with as at that this not yet no yes one every then her his".split())


def _labels(d):
    """every element label of a diagram, whatever its type"""
    x = d["data"]; out = []
    for n in x.get("nodes", []) + x.get("states", []) + x.get("actors", []) + x.get("usecases", []) + x.get("participants", []):
        out.append(n["label"] if isinstance(n, dict) else n)
    out += [f[2] for f in x.get("flows", []) + x.get("transitions", []) if len(f) > 2 and f[2]]
    out += [m[2] for m in x.get("messages", [])]
    for b in x.get("branches", []):
        out.append(b["label"]); out += b.get("children", [])
    if x.get("root"): out.append(x["root"])
    if x.get("system"): out.append(x["system"])
    return out


def grounding(d, nodes):
    """share of a diagram's content words that occur in the explanations of its concepts (and their section and subject)"""
    import re
    by = {n["id"]: n for n in nodes}
    ids = set(d["concepts"]) | set(d.get("also_from", []))
    for c in list(ids):
        n = by.get(c)
        while n and n.get("parent"):
            ids.add(n["parent"]); n = by.get(n["parent"])
    text = " ".join((by[c].get("body") or "") + " " + (by[c].get("definition") or "") + " " + by[c]["label"] for c in ids if c in by).lower()
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9'-]*", " ".join(_labels(d)).lower()) if w not in STOP and len(w) > 1]
    hit = [w for w in words if w in text or w.rstrip("s") in text or (w + "s") in text]
    return len(hit), len(words), sorted(set(w for w in words if w not in hit))


def run_checks(nodes=None, mapping=None):
    """structural rules and, with the chapter's nodes, the grounding ratio; with the CME mapping, the pattern is known and its type is assigned"""
    bad = []
    ids = [d["id"] for d in DIAGRAMS]
    if len(ids) != len(set(ids)): bad.append("duplicate diagram ids")
    by = {n["id"]: n for n in nodes} if nodes else None
    for d in DIAGRAMS:
        for f in ("pattern", "title", "concepts", "read_from", "why", "data"):
            if not d.get(f): bad.append("%s: missing %s" % (d["id"], f))
        if by:
            for c in d["concepts"] + d.get("also_from", []):
                if c not in by: bad.append("%s: unknown concept %s" % (d["id"], c))
        if mapping:
            m = mapping.get(d["pattern"])
            if not m: bad.append("%s: pattern %s is not in the CME mapping" % (d["id"], d["pattern"]))
            else:
                d["type"] = m["types"][0]
        x = d["data"]
        if "flows" in x:
            nid = set(n["id"] for n in x["nodes"]) | {"start", "end"}
            for f in x["flows"]:
                if f[0] not in nid or f[1] not in nid: bad.append("%s: flow names an unknown node %r" % (d["id"], f))
            if not any(f[0] == "start" for f in x["flows"]) or not any(f[1] == "end" for f in x["flows"]): bad.append("%s: no start or no end" % d["id"])
            for n in x["nodes"]:
                if n.get("kind") == "decision" and len([f for f in x["flows"] if f[0] == n["id"]]) < 2: bad.append("%s: decision %s has fewer than two outgoing flows" % (d["id"], n["id"]))
        if "transitions" in x:
            sid = set(s["id"] if isinstance(s, dict) else s for s in x["states"])
            if x["initial"] not in sid: bad.append("%s: initial state unknown" % d["id"])
            for f in x.get("final", []):
                if f not in sid: bad.append("%s: final state unknown" % d["id"])
            for tr in x["transitions"]:
                if tr[0] not in sid or tr[1] not in sid or not tr[2]: bad.append("%s: transition %r unknown state or unlabelled" % (d["id"], tr))
        if "usecases" in x:
            aid = set(a["id"] for a in x["actors"]); uid = set(u["id"] for u in x["usecases"])
            for a, u in x["links"]:
                if a not in aid or u not in uid: bad.append("%s: link %r names an unknown actor or use case" % (d["id"], (a, u)))
            if uid - set(u for _, u in x["links"]): bad.append("%s: a use case has no actor" % d["id"])
        if "messages" in x:
            pid = set(p["id"] for p in x["participants"])
            for m in x["messages"]:
                if m[0] not in pid or m[1] not in pid or not m[2]: bad.append("%s: message %r unknown participant or empty" % (d["id"], m))
        if "branches" in x:
            if len(x["branches"]) < 2: bad.append("%s: a mind map needs at least two branches" % d["id"])
        for lab in _labels(d):
            if len(lab) > 72: bad.append("%s: label over 72 characters: %r" % (d["id"], lab))
        if nodes:
            h, n, miss = grounding(d, nodes)
            d["grounding"] = [h, n]
            if n and h / n < 0.8: bad.append("%s: grounding %d/%d below 0.8; words not in the concepts' explanations: %s" % (d["id"], h, n, ", ".join(miss)))
    return bad


if __name__ == "__main__":
    import sys, json, glob, os, re
    here = os.path.dirname(os.path.abspath(__file__))
    nodes = None
    ch = re.search(r"sen0401_(ch\d+)_diagrams", os.path.basename(__file__)).group(1)
    f = sorted(glob.glob(os.path.join(here, ch + "-page", "page_data_v*.json")), key=lambda p: [int(x) for x in p.rsplit("_v", 1)[1][:-5].split("_")])
    if f: nodes = json.load(open(f[-1]))["nodes"]
    else:
        # before the page data exists: the corpus module in the same shape the page data gives (first paragraph as body)
        sys.path.insert(0, here)
        import importlib
        corp = importlib.import_module(sorted(glob.glob(os.path.join(here, "sen0401_%s_corpus_v*.py" % ch)))[-1][len(here) + 1:-3])
        nodes = [{"id": n[0], "label": n[1] or n[0], "parent": n[3], "body": n[5][0][1], "definition": n[4][1] if n[4] else ""} for n in corp.NODES]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
