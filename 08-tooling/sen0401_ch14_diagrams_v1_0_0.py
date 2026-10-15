#!/usr/bin/env python3
"""SEN0401 chapter 14 - the narrative diagrams of the chapter (version 1.0.0).

Same module shape and contract as chapter 11's sen0401_ch11_diagrams_v1_0_0.py (the owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for, and the mapping from
narrative pattern to diagram type lives in the CME ontology, never in the author's choice); the diagrams are this chapter's, and the grounding threshold is 0.8 as the page brief requires.

Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations the
content draws on), one sentence saying why the pattern fits, and the content in the element names the renderer of that type expects. Every element label is made of words that occur in the
explanations of the accompanying concepts or their section, and run_checks() measures that besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "CheckSecondPayment",
        "pattern": "Workflow",
        "title": "How a node treats a second payment of the same output",
        "concepts": ["DoubleSpendRejected"],
        "also_from": ["ChainGuarantees"],
        "read_from": "chapter 14, A double spend is rejected: a second payment of the same output with a lower fee was refused as an insufficient replacement, one with a higher fee replaced the first in the memory pool",
        "why": "the passage is a procedure with a decision - does the second payment carry a higher fee - and a different outcome on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "fee", "label": "Does the second payment carry a higher fee?", "kind": "decision"},
                {"id": "replace", "label": "It replaces the first in the memory pool"},
                {"id": "refuse", "label": "It is refused as an insufficient replacement"},
            ],
            "flows": [["start", "fee"], ["fee", "replace", "yes"], ["fee", "refuse", "no"], ["replace", "end"], ["refuse", "end"]],
        },
    },
    {
        "id": "SecondLayerInFiveBranches",
        "pattern": "TopicAndParts",
        "title": "Second-layer applications in five branches",
        "concepts": ["PlatformGuarantees", "ColoredCoins", "PaymentChannels", "LightningNetwork", "SinceThePrint"],
        "also_from": ["ChainGuarantees", "ComposedApplications", "SealsAndContracts", "AssetProtocols", "OneWayChannel", "RevocableCommitments", "HashTimeLockContracts", "RoutedPayment", "TransportAndOnion", "ChannelOnChain", "ErrataAndDrift", "NewMachinery", "Limits"],
        "read_from": "chapter 14, the whole chapter: platform guarantees, colored coins, payment channels, the Lightning Network and what changed since the print",
        "why": "the chapter lays out one subject, second-layer applications, by its parts: a topic and its parts",
        "data": {
            "root": "Second-layer applications",
            "branches": [
                {"label": "Platform guarantees", "children": ["Chain guarantees", "Composed applications"]},
                {"label": "Colored coins", "children": ["Seals and contracts", "Asset protocols"]},
                {"label": "Payment channels", "children": ["The one-way channel", "Revocable commitments", "Hash time lock contracts"]},
                {"label": "The Lightning Network", "children": ["The routed payment", "Transport and onion", "The channel on the chain"]},
                {"label": "Since the print", "children": ["Errata and drift", "New machinery", "Limits of the experiments"]},
            ],
        },
    },
    {
        "id": "HtlcExchange",
        "pattern": "Interaction",
        "title": "A payer and a receiver use the secret branch of an HTLC",
        "concepts": ["HtlcSecretBranch", "HtlcTimeoutBranch"],
        "also_from": ["HashTimeLockContracts"],
        "read_from": "chapter 14, The HTLC secret branch: the hash branch pays whoever shows the secret and the receiver's signature; a wrong secret was refused",
        "why": "the passage is an exchange between a payer and a receiver in an order that matters - the lock, then the secret and the signature: an interaction",
        "data": {
            "participants": [{"id": "payer", "label": "The payer"}, {"id": "receiver", "label": "The receiver"}],
            "messages": [
                ["payer", "receiver", "locks coins behind a hash and a time"],
                ["receiver", "payer", "shows the secret and signs", "reply"],
            ],
        },
    },
    {
        "id": "RefundLadderLife",
        "pattern": "LifeCycle",
        "title": "Six commitments with falling lock times, from refused to the sixth accepted",
        "concepts": ["RefundTimelockLadder"],
        "also_from": ["OneWayChannel"],
        "read_from": "chapter 14, The refund timelock ladder: the six commitments had lock times from 488 down to 483, all were refused as non-final at the start, at height 483 only the sixth was accepted, and once it was mined the earlier ones were refused because their input was gone",
        "why": "the passage describes the states the commitments are in and the events that move them - refused, the sixth accepted, the earlier ones refused: a life cycle",
        "data": {
            "states": [
                {"id": "start", "label": "All six commitments are refused as non-final"},
                {"id": "sixth", "label": "Only the sixth is accepted at height 483"},
                {"id": "gone", "label": "The earlier ones are refused because their input is gone"},
            ],
            "initial": "start",
            "final": ["gone"],
            "transitions": [["start", "sixth", "the height reaches 483"], ["sixth", "gone", "the sixth is mined"]],
        },
    },
    {
        "id": "RouteRoles",
        "pattern": "SetOfUses",
        "title": "What the sender and an intermediary each do in a routed payment",
        "concepts": ["FeeArithmetic", "TimelockStaircase"],
        "also_from": ["RoutedPayment", "BalancesAfterPayment"],
        "read_from": "chapter 14, The fee arithmetic: with a fee of 0.001 from each of three intermediaries the sender must offer 1.003, and the payment of 1 bitcoin cost 300,000 satoshis in fees",
        "why": "the passage lists what the different parties of a route do, under different conditions: a set of uses by actors",
        "data": {
            "system": "A ROUTED PAYMENT",
            "actors": [{"id": "sender", "label": "The sender"}, {"id": "hop", "label": "An intermediary"}],
            "usecases": [
                {"id": "offer", "label": "Must offer 1.003"},
                {"id": "fee", "label": "Takes a fee of 0.001"},
                {"id": "time", "label": "Must have more time than the next hop"},
            ],
            "links": [["sender", "offer"], ["hop", "fee"], ["hop", "time"]],
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
        nodes = [{"id": n[0], "label": n[1] or n[0], "parent": n[3], "body": " ".join(t for f, t in n[5]), "definition": n[4][1] if n[4] else ""} for n in corp.NODES]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-20s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
