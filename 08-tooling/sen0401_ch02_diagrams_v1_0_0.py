#!/usr/bin/env python3
"""SEN0401 chapter 2 - the narrative diagrams of the chapter (version 1.0.0).

The owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for - a workflow an activity
diagram, the possible usages of bitcoin a use-case diagram, the life of a transaction a state diagram, an exchange
between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to
diagram type lives in the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl, CME 0.16.0) so that it is reused by every course.

This module is the corpus layer for the chapter's diagrams: each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as (the diagram type follows from the mapping, never from the
author), the passage it was read from (also_from names further concepts whose explanations the content draws on, without the
diagram being shown under them), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects (see the mapping's cme:elements). Nothing here says more than the
chapter's own explanations: every element label is made of words that occur in the explanations of the accompanying
concepts or their section, and run_checks() measures that (the grounding ratio) besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "ConstructAndSend",
        "pattern": "Workflow",
        "title": "From Alice's choice to the network: building and transmitting the transaction",
        "concepts": ["Construction", "TransactionConstruction", "CoinSelection", "MakingChange", "Transmission"],
        "also_from": ["Input", "Output", "TransactionFee", "DigitalSignature", "Linkage", "Propagation"],
        "read_from": "chapter 2: Transaction construction (Alice chooses a destination, an amount and a fee; the wallet finds inputs, creates the outputs, attaches the signature), Coin selection (match the payment plus the fee, or generate change), Making change, Transmitting the transaction",
        "why": "the passages describe a procedure with one decision in it - can the chosen inputs match the payment plus the fee exactly, or is a change output needed - from Alice's three choices to the hand-over to the network: a workflow",
        "data": {
            "nodes": [
                {"id": "choose", "label": "Alice chooses a destination, an amount and a fee"},
                {"id": "select", "label": "The wallet selects unspent outputs as inputs"},
                {"id": "exact", "label": "Do the inputs match the payment plus the fee exactly?", "kind": "decision"},
                {"id": "change", "label": "Add a change output back to Alice"},
                {"id": "outputs", "label": "Create the output to the receiver; the fee is the difference"},
                {"id": "sign", "label": "Attach the signature that proves the inputs may be spent"},
                {"id": "transmit", "label": "Transmit the finished transaction to any node: the route does not matter"},
            ],
            "flows": [["start", "choose"], ["choose", "select"], ["select", "exact"], ["exact", "outputs", "yes"], ["exact", "change", "no"], ["change", "outputs"], ["outputs", "sign"], ["sign", "transmit"], ["transmit", "end"]],
        },
    },
    {
        "id": "NetworkRoles",
        "pattern": "SetOfUses",
        "title": "Who takes part in the network, and what each one does",
        "concepts": ["Network", "Participants", "FullNode", "LightweightClient", "Peer", "Miner", "MiningPool", "BlockExplorer"],
        "read_from": "chapter 2: Who takes part (full verification nodes), Full node (verifies every transaction and block), Lightweight client (block headers only, simplified payment verification), Miner (candidate blocks, proof of work), Mining pool (reward shared in proportion to work), Block explorer (a search engine for the blockchain)",
        "why": "the passages name the kinds of program on the network and say what each can do and cannot - who does what, not in what order: a set of uses",
        "data": {
            "system": "THE BITCOIN NETWORK",
            "actors": [{"id": "fullnode", "label": "Full node"}, {"id": "light", "label": "Lightweight client"}, {"id": "miner", "label": "Miner"}, {"id": "pool", "label": "Mining pool"}, {"id": "explorer", "label": "Block explorer"}],
            "usecases": [
                {"id": "verify", "label": "Verify every transaction and block"},
                {"id": "gossip", "label": "Forward a valid transaction to all peers"},
                {"id": "mempool", "label": "Keep a memory pool of unconfirmed transactions"},
                {"id": "headers", "label": "Download block headers only"},
                {"id": "spv", "label": "Verify a payment by simplified payment verification"},
                {"id": "candidate", "label": "Assemble a candidate block"},
                {"id": "pow", "label": "Search for the proof of work"},
                {"id": "share", "label": "Share the reward in proportion to work"},
                {"id": "search", "label": "Search addresses, transactions and blocks"},
            ],
            "links": [["fullnode", "verify"], ["fullnode", "gossip"], ["fullnode", "mempool"], ["light", "headers"], ["light", "spv"], ["miner", "candidate"], ["miner", "pow"], ["pool", "share"], ["pool", "candidate"], ["explorer", "search"]],
        },
    },
    {
        "id": "TransactionOnTheNetwork",
        "pattern": "LifeCycle",
        "title": "The life of Alice's transaction, from the memory pool to six confirmations",
        "concepts": ["Propagation", "TransactionPropagation", "Mempool", "Security", "UnconfirmedTransaction", "Confirmation", "AlternativeBlock", "BestBlockchain"],
        "also_from": ["CandidateBlock", "Miner", "Gossiping", "Mining", "Block"],
        "read_from": "chapter 2: Transaction propagation, Memory pool (verified but unconfirmed), Unconfirmed transaction, Candidate block, Confirmation (one for the block, one more for each block on top; six is the rule of thumb), Fork and alternative block (two valid blocks at the same height, resolved by the next block), Best blockchain (the most total proof of work)",
        "why": "the passages describe the states a transaction passes through after transmission and the events that move it on - received, verified, pooled, in a candidate block, in a block, confirmed, or in a fork that the next block resolves: a life cycle",
        "data": {
            "states": [
                {"id": "received", "label": "Received by a node"},
                {"id": "pooled", "label": "Verified, in the memory pool: unconfirmed"},
                {"id": "candidate", "label": "In a miner's candidate block"},
                {"id": "inblock", "label": "In a valid block: one confirmation"},
                {"id": "fork", "label": "In one of two blocks at the same height (accidental fork)"},
                {"id": "buried", "label": "Six or more confirmations"},
                {"id": "dropped", "label": "Not valid: not forwarded"},
            ],
            "initial": "received",
            "final": ["buried", "dropped"],
            "transitions": [["received", "pooled", "valid and not seen before"], ["received", "dropped", "the node cannot verify it"], ["pooled", "candidate", "a miner includes it"], ["candidate", "inblock", "valid proof of work"], ["inblock", "fork", "another block at the same height"], ["fork", "inblock", "the next block extends one side"], ["inblock", "buried", "each block on top adds one"]],
        },
    },
    {
        "id": "InvoiceToPayment",
        "pattern": "Interaction",
        "title": "From Bob's invoice to Bob's confirmation",
        "concepts": ["PaymentRequest", "Bip21Uri", "QrCode", "RecipientVerification"],
        "also_from": ["Transmission", "Gossiping", "Mempool", "Confirmation", "BlockExplorer", "Miner"],
        "read_from": "chapter 2: Payment request (Bob's e-commerce system creates a QR code holding an invoice), BIP21 URI (address, amount, label, message), QR code, Transmitting the transaction, Gossiping, Bob's view (the recipient's own check), Confirmation, Block explorer",
        "why": "the passages are an exchange between Bob's store, Alice's wallet, the network's nodes and the miners, in an order that matters - request, scan, transmit, gossip, mine, confirm: an interaction",
        "data": {
            "participants": [{"id": "bob", "label": "Bob's store and wallet"}, {"id": "alice", "label": "Alice's wallet"}, {"id": "nodes", "label": "Network nodes"}, {"id": "miners", "label": "Miners"}],
            "messages": [
                ["bob", "alice", "QR code holding the BIP21 URI: address, amount, label, message"],
                ["alice", "alice", "scan; choose a fee; build and sign the transaction"],
                ["alice", "nodes", "transmit the transaction"],
                ["nodes", "nodes", "verify; keep in the memory pool; gossip to all peers"],
                ["nodes", "bob", "the transaction arrives: an output redeemable by Bob's keys", "reply"],
                ["bob", "bob", "check it is well formed; a full node checks its inputs are unspent"],
                ["nodes", "miners", "unconfirmed transactions for a candidate block"],
                ["miners", "nodes", "a valid block containing it", "reply"],
                ["nodes", "bob", "one confirmation, then one more per block", "reply"],
            ],
        },
    },
    {
        "id": "PartsOfATransaction",
        "pattern": "TopicAndParts",
        "title": "What a transaction is made of",
        "concepts": ["Transaction", "TransactionPart", "Input", "Output", "UnspentOutput", "Outpoint", "Witness"],
        "also_from": ["TransactionFee", "TransactionSize", "FeeRate", "TransactionIdentifier", "Script", "Serialization", "DoubleEntryLedger"],
        "read_from": "chapter 2, the Transaction part section: inputs (an outpoint - transaction identifier and output index - and a witness), outputs (amount and script), the fee as the difference, size and fee rate, the transaction identifier, serialization, the double-entry ledger image",
        "why": "the section lists the pieces a transaction is assembled from and the pieces of those pieces - a topic and its parts, laid out to remember",
        "data": {
            "root": "A transaction",
            "branches": [
                {"label": "Inputs: what is spent", "children": ["Outpoint: transaction identifier + output index", "Witness: the proof the input may be spent", "Each spends one unspent transaction output (UTXO)"]},
                {"label": "Outputs: who receives", "children": ["Amount in satoshis", "Script that locks the amount", "Change output back to the payer"]},
                {"label": "Fee", "children": ["Inputs minus outputs, implied", "Fee rate: fee per unit of size"]},
                {"label": "Identity and form", "children": ["Transaction identifier (txid)", "Serialization: the byte form", "Size in bytes"]},
            ],
        },
    },
    {
        "id": "MiningTheBlock",
        "pattern": "Workflow",
        "title": "How Jing's node turns the memory pool into the next block",
        "concepts": ["Mining", "Miner", "CandidateBlock", "ProofOfWork", "ConsensusRules", "CoinbaseTransaction"],
        "also_from": ["Mempool", "BlockReward", "Difficulty", "BlockHeader", "BestBlockchain"],
        "read_from": "chapter 2, the Mining section: Miner (Jing's rig and full node), Candidate block (transactions from the memory pool, a commitment to the previous block, no valid proof of work yet), Proof of work (repeated hashing until the header meets the target), Consensus rules (every full node validates the block), Coinbase transaction and Block reward",
        "why": "the passages describe a repeated procedure with a test and a loop - assemble, hash, check against the target, try again - and what follows when it succeeds: a workflow",
        "data": {
            "nodes": [
                {"id": "pool", "label": "Collect verified transactions from the memory pool"},
                {"id": "coinbase", "label": "Add the coinbase transaction paying the block reward"},
                {"id": "candidate", "label": "Assemble the candidate block committing to the previous block"},
                {"id": "hash", "label": "Hash the block header with a new nonce"},
                {"id": "target", "label": "Is the hash below the target?", "kind": "decision"},
                {"id": "broadcast", "label": "A valid block: propagate it to all peers"},
                {"id": "validate", "label": "Full nodes validate it by the consensus rules; the best blockchain grows"},
            ],
            "flows": [["start", "pool"], ["pool", "coinbase"], ["coinbase", "candidate"], ["candidate", "hash"], ["hash", "target"], ["target", "hash", "no: another nonce"], ["target", "broadcast", "yes"], ["broadcast", "validate"], ["validate", "end"]],
        },
    },
]

STOP = set("a an the of to in on and or is are be by it its for from with as at that this not yet no yes one every then".split())


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
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
