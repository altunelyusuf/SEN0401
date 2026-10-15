#!/usr/bin/env python3
"""SEN0401 chapter 9 - the narrative diagrams of the chapter (version 1.0.0).

Same module shape and contract as chapter 8's sen0401_ch08_diagrams_v1_0_0.py (the owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for, and the mapping from
narrative pattern to diagram type lives in the CME ontology, never in the author's choice); the diagrams are this chapter's, and the grounding threshold is 0.8 as the page brief requires.

Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations the
content draws on), one sentence saying why the pattern fits, and the content in the element names the renderer of that type expects. Every element label is made of words that occur in the
explanations of the accompanying concepts or their section, and run_checks() measures that besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "AcceptReplacement",
        "pattern": "Workflow",
        "title": "How a node decides whether a replacement takes the place of a payment",
        "concepts": ["ConflictRule", "AbsoluteFeeRule", "IncrementalFeeRule", "FeerateDiagramRule"],
        "also_from": ["ReplacementRules", "ReplaceByFee"],
        "read_from": "chapter 9, Replacement rules: two transactions conflict when they spend a common output; a replacement must pay at least the absolute fee of what it replaces, also pay the incremental relay fee for its own size, and improve the feerate diagram",
        "why": "the passage is a procedure with decisions - does it conflict, does it pay enough in total, does it pay for its own size, does it improve the diagram - and a different outcome on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "conflict", "label": "Does it spend an output that a transaction in the mempool spends?", "kind": "decision"},
                {"id": "absolute", "label": "Does it pay at least the absolute fee of what it replaces?", "kind": "decision"},
                {"id": "incremental", "label": "Does it also pay the incremental relay fee for its own size?", "kind": "decision"},
                {"id": "diagram", "label": "Does it improve the feerate diagram?", "kind": "decision"},
                {"id": "takes", "label": "The replacement takes the place of the transaction"},
                {"id": "refused", "label": "The node refuses it: less fees than conflicting txs"},
                {"id": "plain", "label": "The transaction does not conflict, so it is not a replacement"},
            ],
            "flows": [["start", "conflict"], ["conflict", "absolute", "yes"], ["conflict", "plain", "no"], ["absolute", "incremental", "yes"], ["absolute", "refused", "no"],
                      ["incremental", "diagram", "yes"], ["incremental", "refused", "no"], ["diagram", "takes", "yes"], ["diagram", "refused", "no"],
                      ["takes", "end"], ["refused", "end"], ["plain", "end"]],
        },
    },
    {
        "id": "FeeBranches",
        "pattern": "TopicAndParts",
        "title": "Transaction fees in seven branches",
        "concepts": ["WhoPaysTheFee", "FeesAndFeeRates", "FeeEstimation", "ReplaceByFee", "ChildPaysForParent", "PinningAndAnchors", "FeeSnipingAndIncentives"],
        "also_from": ["FeeAsDifference", "SizeAndWeight", "EstimatorMechanics", "ReplacementRules", "PackagesAndMining", "TrucPolicy", "SnipingAttack"],
        "read_from": "chapter 9, the whole chapter: who pays the fee, fees and fee rates, fee estimation, replace by fee, child pays for parent, pinning and anchors, and fee sniping and incentives",
        "why": "the chapter lays out one subject, transaction fees, by its parts: a topic and its parts",
        "data": {
            "root": "Transaction fees",
            "branches": [
                {"label": "Who pays the fee", "children": ["Fee as difference", "Spender and signature", "Miner choice"]},
                {"label": "Fees and fee rates", "children": ["Size and weight", "Fee rate arithmetic", "Minimum rates"]},
                {"label": "Fee estimation", "children": ["Estimator mechanics", "Fee market on mainnet"]},
                {"label": "Replace by fee (RBF)", "children": ["Replaceable signal", "Replacement rules", "Replacement hazards"]},
                {"label": "Child pays for parent (CPFP)", "children": ["Packages and mining", "Package relay", "Cluster mempool"]},
                {"label": "Pinning and anchors", "children": ["CPFP carve out", "TRUC policy", "Anchor outputs"]},
                {"label": "Fee sniping and incentives", "children": ["Block reward mix", "Sniping attack", "Lock time defense against fee sniping"]},
            ],
        },
    },
    {
        "id": "ParentLiftedByChild",
        "pattern": "Interaction",
        "title": "A parent that pays too little is accepted together with its child",
        "concepts": ["MinimumRelayProblem", "SubmitPackageRpc", "PackageFeeRate"],
        "also_from": ["PackageRelay", "PackagesAndMining", "ChildPaysForParent"],
        "read_from": "chapter 9, The minimum relay problem and The submitpackage RPC: a parent paying 8 satoshis, below the 15 needed, was refused alone with min relay fee not met, a child alone was refused as spending a missing output, and submitpackage accepted both",
        "why": "the passage is an exchange between a sender and a node in an order that matters - the parent alone, the child alone, then both together: an interaction",
        "data": {
            "participants": [{"id": "sender", "label": "The sender"}, {"id": "node", "label": "The node"}],
            "messages": [
                ["sender", "node", "sends the parent that pays 8 satoshis, below the 15 needed"],
                ["node", "sender", "refuses it with min relay fee not met", "reply"],
                ["sender", "node", "sends the child alone"],
                ["node", "sender", "refuses it as spending a missing output", "reply"],
                ["sender", "node", "hands both to the node with submitpackage"],
                ["node", "sender", "accepts both, because the fee of the child pays for the pair", "reply"],
            ],
        },
    },
    {
        "id": "ThreeVersions",
        "pattern": "LifeCycle",
        "title": "The three versions of one payment, from the first to a payee paid twice",
        "concepts": ["ThreeVersionsPaidTwice", "ConflictRule"],
        "also_from": ["ReplacementHazards", "ReplaceByFee"],
        "read_from": "chapter 9, Three versions paid twice: version 0 spends input A, version 1 spends A and B, version 2 spends B and C; a miner that kept version 0 mined it and then version 2, and the payee received 0.8 bitcoin instead of 0.4",
        "why": "the passage describes the states one payment is in and the events that move it - version 0, version 1, version 2, paid twice: a life cycle",
        "data": {
            "states": [
                {"id": "v0", "label": "Version 0 spends input A"},
                {"id": "v1", "label": "Version 1 spends A and B"},
                {"id": "v2", "label": "Version 2 spends B and C"},
                {"id": "twice", "label": "The payee is paid twice"},
            ],
            "initial": "v0",
            "final": ["twice"],
            "transitions": [["v0", "v1", "version 1 conflicts with version 0 and replaces it in the mempool"],
                            ["v1", "v2", "version 2 conflicts with version 1 and replaces it"],
                            ["v2", "twice", "a miner that kept version 0 mines it and then version 2"]],
        },
    },
    {
        "id": "AnchorUses",
        "pattern": "SetOfUses",
        "title": "What an anyone-can-spend anchor lets others do",
        "concepts": ["AnchorSpend", "PayToAnchor", "EphemeralDust"],
        "also_from": ["AnchorOutputs", "LightningAnchorOutputs"],
        "read_from": "chapter 9, Anchor spend: whoever sees the parent, the counterparty or a third party, can attach a child with two inputs, one for the money that pays the fee and one for the anchor with an empty witness stack",
        "why": "the passage lists what different people can do with one anyone-can-spend output, under different conditions: a set of uses by actors",
        "data": {
            "system": "A PAY-TO-ANCHOR OUTPUT",
            "actors": [{"id": "counterparty", "label": "The counterparty"}, {"id": "third", "label": "A third party"}],
            "usecases": [
                {"id": "attach", "label": "Attach a child to fee bump the parent"},
                {"id": "spend", "label": "Spend the anchor with an empty witness stack"},
                {"id": "pay", "label": "Pay the fee from another input of the child"},
            ],
            "links": [["counterparty", "attach"], ["third", "attach"], ["counterparty", "spend"], ["third", "spend"], ["counterparty", "pay"]],
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
