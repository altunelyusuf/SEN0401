#!/usr/bin/env python3
"""SEN0401 chapter 1 - the narrative diagrams of the chapter (version 1.0.0).

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
        "id": "SpendingWorkflow",
        "pattern": "Workflow",
        "title": "Sending a payment, from Send to confirmed",
        "concepts": ["Transfer", "SendingAndReceiving", "Transaction", "TransactionFee", "Confirmation"],
        "read_from": "chapter 1, the Transfer section: Sending and receiving, Transaction, Transaction fee, Confirmation (explanations in sen0401_ch01_domain_tbox_v1_2_0.ttl, following Antonopoulos and Harding, 2023)",
        "why": "the section follows the payment from the moment Joe presses Send to the moment it is confirmed in a block, step by step with one choice on the way (the fee) - a workflow",
        "data": {
            "nodes": [
                {"id": "receive", "label": "Alice selects Receive; her wallet shows a QR code with her address"},
                {"id": "scan", "label": "Joe selects Send and scans the code"},
                {"id": "amount", "label": "Joe enters the amount, 0.001 BTC"},
                {"id": "feeq", "label": "Does the wallet ask for a fee rate?", "kind": "decision"},
                {"id": "fee", "label": "Joe enters a fee rate or accepts the suggested fee"},
                {"id": "sign", "label": "The wallet signs the transaction and transmits it over the network"},
                {"id": "unconfirmed", "label": "The transaction shows as unconfirmed"},
                {"id": "block", "label": "A miner includes it in a block, every 10 minutes on average"},
                {"id": "confirmed", "label": "The transaction is confirmed: recorded in the blockchain"},
            ],
            "flows": [["start", "receive"], ["receive", "scan"], ["scan", "amount"], ["amount", "feeq"], ["feeq", "fee", "yes"], ["feeq", "sign", "no"], ["fee", "sign"], ["sign", "unconfirmed"], ["unconfirmed", "block"], ["block", "confirmed"], ["confirmed", "end"]],
        },
    },
    {
        "id": "BitcoinUses",
        "pattern": "SetOfUses",
        "title": "Who uses Bitcoin, and for what",
        "concepts": ["Usage", "Acquisition", "EarnBitcoin", "BuyFromFriend", "BitcoinATM", "CurrencyExchange"],
        "also_from": ["Mining", "BitcoinImprovementProposal", "OpenSourceSoftware", "BlockSubsidy", "SendingAndReceiving"],
        "read_from": "chapter 1, the Usage branch and the Acquisition section: four ways to acquire a first bitcoin, sending and receiving, mining as something any participant may do, and the open-source development the Standards section describes",
        "why": "the passage lists what different people do with the system - acquire, pay, receive, mine, develop - which is a set of uses by actors, not a sequence",
        "data": {
            "system": "THE BITCOIN SYSTEM",
            "actors": [{"id": "newcomer", "label": "Newcomer (Alice)"}, {"id": "merchant", "label": "Merchant or friend (Joe)"}, {"id": "miner", "label": "Miner"}, {"id": "developer", "label": "Developer"}],
            "usecases": [
                {"id": "buy", "label": "Buy bitcoin from a friend"},
                {"id": "earn", "label": "Earn bitcoin by selling a product or a service"},
                {"id": "atm", "label": "Use a Bitcoin ATM"},
                {"id": "exchange", "label": "Buy on a currency exchange linked to a bank account"},
                {"id": "receive", "label": "Receive a payment at an address"},
                {"id": "send", "label": "Send a payment"},
                {"id": "mine", "label": "Mine blocks and earn the reward"},
                {"id": "bip", "label": "Propose a change as a BIP"},
            ],
            "links": [["newcomer", "buy"], ["newcomer", "atm"], ["newcomer", "exchange"], ["newcomer", "receive"], ["merchant", "earn"], ["merchant", "send"], ["merchant", "receive"], ["miner", "mine"], ["developer", "bip"]],
        },
    },
    {
        "id": "TransactionLife",
        "pattern": "LifeCycle",
        "title": "The life of a transaction",
        "concepts": ["Transaction", "Confirmation", "Irreversibility", "DoubleSpend"],
        "also_from": ["Node", "SendingAndReceiving", "Mining"],
        "read_from": "chapter 1: Transaction (a signed data structure, transmitted over the network, collected by miners, included in a block, made permanent), Confirmation (unconfirmed, then confirmed by inclusion in a block), Irreversibility, Double-spend",
        "why": "the explanations describe states a transaction is in - signed, transmitted, unconfirmed, in a block, permanent - and what moves it between them: a life cycle",
        "data": {
            "states": [{"id": "signed", "label": "Signed data structure"}, {"id": "transmitted", "label": "Transmitted over the network"}, {"id": "unconfirmed", "label": "Unconfirmed: propagated, not yet in the blockchain"}, {"id": "inblock", "label": "Included in a block: clearing"}, {"id": "permanent", "label": "Permanent: confirmations grow, irreversible"}, {"id": "rejected", "label": "Refused: the same unit spent twice"}],
            "initial": "signed",
            "final": ["permanent", "rejected"],
            "transitions": [["signed", "transmitted", "Send"], ["transmitted", "unconfirmed", "propagated to the network"], ["unconfirmed", "inblock", "a miner includes it"], ["inblock", "permanent", "more blocks follow, every 10 minutes"], ["unconfirmed", "rejected", "double-spend attempt"]],
        },
    },
    {
        "id": "PaymentInteraction",
        "pattern": "Interaction",
        "title": "A payment between two wallets and the network",
        "concepts": ["Address", "BitcoinAddress", "Invoice", "SendingAndReceiving"],
        "also_from": ["Transaction", "Confirmation", "Node", "Mining", "Blockchain"],
        "read_from": "chapter 1: Sending and receiving (Alice selects Receive, Joe selects Send and scans), Bitcoin address, Invoice (an address or invoice shared with another user), Confirmation (propagated, then recorded in a block)",
        "why": "the passage is an exchange of messages between parties - Alice's wallet, Joe's wallet, the network's nodes and the miners - in an order that matters: an interaction",
        "data": {
            "participants": [{"id": "alice", "label": "Alice's wallet"}, {"id": "joe", "label": "Joe's wallet"}, {"id": "nodes", "label": "Network nodes"}, {"id": "miners", "label": "Miners"}],
            "messages": [
                ["alice", "alice", "generate a private key; derive an address"],
                ["alice", "joe", "show the address as a QR code (invoice)"],
                ["joe", "joe", "scan; enter 0.001 BTC; sign the transaction"],
                ["joe", "nodes", "transmit the transaction"],
                ["nodes", "nodes", "propagate it: unconfirmed"],
                ["nodes", "miners", "relay to miners"],
                ["miners", "nodes", "a new block containing it", "reply"],
                ["nodes", "alice", "confirmation: recorded in the blockchain", "reply"],
            ],
        },
    },
    {
        "id": "ChoosingAWallet",
        "pattern": "TopicAndParts",
        "title": "Choosing a wallet: the four questions",
        "concepts": ["Wallet", "WalletPlatform", "NodeType", "KeyControl", "Backup"],
        "read_from": "chapter 1, the Wallet branch: Wallet platform (desktop, mobile, web, hardware signing device), Node type (full node, lightweight client, third-party API client), Key control (noncustodial, custodial), Backup (recovery code, wallet metadata)",
        "why": "the branch classifies one topic, the wallet, by four aspects and lists the choices under each - a topic and its parts, laid out to remember",
        "data": {
            "root": "Choosing a wallet",
            "branches": [
                {"label": "Platform", "children": ["Desktop wallet", "Mobile wallet", "Web wallet", "Hardware signing device"]},
                {"label": "Node type", "children": ["Full node", "Lightweight client", "Third-party API client"]},
                {"label": "Key control", "children": ["Noncustodial: you hold the keys", "Custodial: a third party holds them"]},
                {"label": "Backup", "children": ["Recovery code", "Wallet metadata", "Offchain payments"]},
            ],
        },
    },
    {
        "id": "MiningWorkflow",
        "pattern": "Workflow",
        "title": "How a block is found",
        "concepts": ["Consensus", "Mining", "ProofOfWork", "DifficultyAdjustment"],
        "read_from": "chapter 1, the Consensus section: Mining (a computational task referencing a list of recent transactions), Proof of work (scanning for a value whose hash begins with zero bits; a global lottery every 10 minutes), Difficulty adjustment (adjusted so that someone succeeds every 10 minutes on average)",
        "why": "the explanations describe a repeated procedure with a test and a loop - try a value, hash, check the zero bits, try again - and a rule that retunes it: a workflow",
        "data": {
            "nodes": [
                {"id": "collect", "label": "A miner references a list of recent transactions"},
                {"id": "scan", "label": "Scan for a value: hash it with SHA-256"},
                {"id": "zeros", "label": "Does the hash begin with enough zero bits?", "kind": "decision"},
                {"id": "block", "label": "A valid block: the lottery is won, every 10 minutes on average"},
                {"id": "adjust", "label": "Every 2016 blocks the difficulty is adjusted to keep the 10-minute pace"},
            ],
            "flows": [["start", "collect"], ["collect", "scan"], ["scan", "zeros"], ["zeros", "scan", "no: try again"], ["zeros", "block", "yes"], ["block", "adjust"], ["adjust", "end"]],
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
