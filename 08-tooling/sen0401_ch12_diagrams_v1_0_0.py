#!/usr/bin/env python3
"""SEN0401 chapter 12 - the narrative diagrams of the chapter (version 1.0.0).

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
        "id": "CheckGreedyCoinbase",
        "pattern": "Workflow",
        "title": "How a node treats a block whose coinbase claims too much",
        "concepts": ["GreedyCoinbaseRejected", "MinerMayClaimLess", "RewardIsSubsidyPlusFees"],
        "also_from": ["RewardComposition", "BlockChecklist"],
        "read_from": "chapter 12, Greedy coinbase rejected: a coinbase that claims one satoshi more than subsidy plus fees makes the block invalid and the node answers bad-cb-amount; one that claims less is accepted",
        "why": "the passage is a procedure with a decision - does the coinbase claim more than the reward allows - and a different outcome on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "more", "label": "Does the coinbase claim more than subsidy plus fees?", "kind": "decision"},
                {"id": "refused", "label": "The node answers bad-cb-amount"},
                {"id": "invalid", "label": "The block is invalid"},
                {"id": "ok", "label": "The block is accepted"},
            ],
            "flows": [["start", "more"], ["more", "refused", "yes"], ["more", "ok", "no"], ["refused", "invalid"], ["invalid", "end"], ["ok", "end"]],
        },
    },
    {
        "id": "MiningInSixBranches",
        "pattern": "TopicAndParts",
        "title": "Mining and consensus in six branches",
        "concepts": ["MoneyCreation", "DecentralizedConsensus", "BuildingTheCandidateBlock", "ProofOfWork", "MiningCompetition", "ChangingConsensusRules"],
        "also_from": ["SubsidySchedule", "RewardComposition", "IndependentVerification", "ChainSelection", "BlockTemplate", "CoinbaseTransaction", "HeaderConstruction", "TheLottery", "TargetAndDifficulty", "Retargeting", "NonceSpace", "MiningPools", "HashrateAttacks", "HardForks", "SoftForks"],
        "read_from": "chapter 12, the whole chapter: money creation, decentralized consensus, building the candidate block, proof of work, mining competition and changing consensus rules",
        "why": "the chapter lays out one subject, mining and consensus, by its parts: a topic and its parts",
        "data": {
            "root": "Mining and consensus",
            "branches": [
                {"label": "Money creation", "children": ["Subsidy schedule", "Reward composition"]},
                {"label": "Decentralized consensus", "children": ["Independent verification", "Chain selection"]},
                {"label": "Building the candidate block", "children": ["Block template", "Coinbase transaction", "Header construction"]},
                {"label": "Proof of work", "children": ["The lottery", "Target and difficulty", "Retargeting"]},
                {"label": "Mining competition", "children": ["Nonce space", "Mining pools", "Hashrate attacks"]},
                {"label": "Changing consensus rules", "children": ["Hard forks", "Soft forks"]},
            ],
        },
    },
    {
        "id": "PoolSharesExchange",
        "pattern": "Interaction",
        "title": "A pool member proves work to the pool with shares",
        "concepts": ["PoolSharesAndFees", "BlockWithholding"],
        "also_from": ["MiningPools", "StratumProtocols"],
        "read_from": "chapter 12, Pool shares and fees: a pool sets an easier target so that members prove their work with shares; the pool pays by the share and takes a fee",
        "why": "the passage is an exchange between a member and a pool in an order that matters - the shares, then the payment: an interaction",
        "data": {
            "participants": [{"id": "member", "label": "A pool member"}, {"id": "pool", "label": "The pool"}],
            "messages": [
                ["pool", "member", "sets an easier target"],
                ["member", "pool", "proves work with shares"],
                ["pool", "member", "pays by the share and takes a fee", "reply"],
            ],
        },
    },
    {
        "id": "Bip9Deployment",
        "pattern": "LifeCycle",
        "title": "A deployment under BIP 9 on regtest, from defined to active",
        "concepts": ["Bip9StateMachine"],
        "also_from": ["SoftForks", "SoftForkOnlyTightens"],
        "read_from": "chapter 12, The BIP 9 state machine: on regtest, periods of 144 and a threshold of 108 gave defined at 143, started at 144, locked_in at 288 and active at 432",
        "why": "the passage describes the states a deployment is in and the events that move it - defined, started, locked_in, active: a life cycle",
        "data": {
            "states": [
                {"id": "defined", "label": "defined at 143"},
                {"id": "started", "label": "started at 144"},
                {"id": "locked", "label": "locked_in at 288"},
                {"id": "active", "label": "active at 432"},
            ],
            "initial": "defined",
            "final": ["active"],
            "transitions": [["defined", "started", "decided once per period of 144"],
                            ["started", "locked", "with a threshold of 108"],
                            ["locked", "active", "decided once per period of 144"]],
        },
    },
    {
        "id": "MinerKinds",
        "pattern": "SetOfUses",
        "title": "What a solo miner and a pool member each get from mining",
        "concepts": ["SoloMinerVariance", "PoolSharesAndFees"],
        "also_from": ["MiningPools", "PoolConcentration"],
        "read_from": "chapter 12, Solo miner variance and Pool shares and fees: a miner with 0.01% waits 69 days on average for a block, which is why small miners join pools, where one expects a thousand shares for each block",
        "why": "the passage lists what two kinds of miner experience, under different conditions: a set of uses by actors",
        "data": {
            "system": "MINING A BLOCK",
            "actors": [{"id": "solo", "label": "A solo miner"}, {"id": "member", "label": "A pool member"}],
            "usecases": [
                {"id": "wait", "label": "Waits 69 days on average for a block"},
                {"id": "shares", "label": "Expects a thousand shares for each block"},
                {"id": "fee", "label": "Is paid by the share and pays a fee"},
            ],
            "links": [["solo", "wait"], ["member", "shares"], ["member", "fee"]],
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
