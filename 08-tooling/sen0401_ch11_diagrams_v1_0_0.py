#!/usr/bin/env python3
"""SEN0401 chapter 11 - the narrative diagrams of the chapter (version 1.0.0).

Same module shape and contract as chapter 10's sen0401_ch10_diagrams_v1_0_0.py (the owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for, and the mapping from
narrative pattern to diagram type lives in the CME ontology, never in the author's choice); the diagrams are this chapter's, and the grounding threshold is 0.8 as the page brief requires.

Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations the
content draws on), one sentence saying why the pattern fits, and the content in the element names the renderer of that type expects. Every element label is made of words that occur in the
explanations of the accompanying concepts or their section, and run_checks() measures that besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "CheckMutatedBlock",
        "pattern": "Workflow",
        "title": "How a node treats a block whose merkle tree was forged",
        "concepts": ["NodeRejectsMutatedBlock", "MutationDefenseInSource", "Cve20122459Trees"],
        "also_from": ["TreeFlaws", "OddLeafDuplicated"],
        "read_from": "chapter 11, Node rejects mutated block: a block of 3 transactions was changed into one of 4 by repeating the last transaction, with the same header and the same hash; submitblock answered bad-txns-duplicate, and the original block was then accepted and became the tip",
        "why": "the passage is a procedure with decisions - does the root match the header, does the block repeat its last transaction - and a different outcome on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "root", "label": "Does the merkle root match the header?", "kind": "decision"},
                {"id": "dup", "label": "Does the block repeat its last transaction?", "kind": "decision"},
                {"id": "refused", "label": "The block is refused"},
                {"id": "mutated", "label": "The node answers bad-txns-duplicate"},
                {"id": "tip", "label": "The block is accepted and becomes the tip"},
            ],
            "flows": [["start", "root"], ["root", "dup", "yes"], ["root", "refused", "no"], ["dup", "mutated", "yes"], ["dup", "tip", "no"],
                      ["refused", "end"], ["mutated", "end"], ["tip", "end"]],
        },
    },
    {
        "id": "BlockchainBranches",
        "pattern": "TopicAndParts",
        "title": "The blockchain in six branches",
        "concepts": ["BlockStructure", "BlockIdentifiers", "GenesisBlock", "LinkingBlocks", "MerkleTrees", "TestBlockchains"],
        "also_from": ["BlockContainer", "HeaderFields", "HashIdentity", "BackLinks", "TreeConstruction", "Regtest"],
        "read_from": "chapter 11, the whole chapter: block structure, block identifiers, the genesis block, linking blocks, merkle trees and test blockchains",
        "why": "the chapter lays out one subject, the blockchain, by its parts: a topic and its parts",
        "data": {
            "root": "The blockchain",
            "branches": [
                {"label": "Block structure", "children": ["Block container", "Header fields"]},
                {"label": "Block identifiers", "children": ["Hash identity", "Height and maturity"]},
                {"label": "Genesis block", "children": ["Genesis constants", "Genesis quirks"]},
                {"label": "Linking blocks", "children": ["Back links", "Forks and reorganizations"]},
                {"label": "Merkle trees", "children": ["Tree construction", "Tree flaws", "Merkle proofs"]},
                {"label": "Test blockchains", "children": ["Chains and addresses", "Testnet", "Signet", "Regtest", "Development pipeline"]},
            ],
        },
    },
    {
        "id": "ProofForLightClient",
        "pattern": "Interaction",
        "title": "A light client asks for a proof that one transaction is in a block",
        "concepts": ["MerkleblockForLightClients", "MerklePathOf16"],
        "also_from": ["MerkleProofs", "ProofSizeVsBlock"],
        "read_from": "chapter 11, Merkleblock for light clients: the merkleblock that Bitcoin Core made for one transaction was 248 bytes against the block's 3,580 bytes, and verifytxoutproof returned the transaction",
        "why": "the passage is an exchange between a client and a node in an order that matters - the request, the merkleblock, the check: an interaction",
        "data": {
            "participants": [{"id": "client", "label": "The light client"}, {"id": "node", "label": "The full node"}],
            "messages": [
                ["client", "node", "asks for the proof of one transaction"],
                ["node", "client", "answers with a merkleblock of 248 bytes", "reply"],
                ["client", "node", "calls verifytxoutproof on it"],
                ["node", "client", "returns the transaction", "reply"],
            ],
        },
    },
    {
        "id": "ForkLife",
        "pattern": "LifeCycle",
        "title": "A fork on the test chain, from two children to one active branch",
        "concepts": ["TwoChildrenOneParent", "ForkResolvedByMoreWork"],
        "also_from": ["ForksAndReorgs", "HeightIsNotUnique"],
        "read_from": "chapter 11, Forks: two different blocks with the same parent hash and the same height 511, one active and one a valid-fork branch; a third block on top of the first child made height 512 the tip, so the fork was resolved without anyone deleting a block",
        "why": "the passage describes the states a chain is in and the events that move it - two children, a third block, one branch active: a life cycle",
        "data": {
            "states": [
                {"id": "two", "label": "Two children of one parent at height 511"},
                {"id": "third", "label": "A third block is mined on the first child"},
                {"id": "active", "label": "The first branch is active and the second is a valid fork"},
            ],
            "initial": "two",
            "final": ["active"],
            "transitions": [["two", "third", "a third block makes height 512 the tip"],
                            ["third", "active", "the fork is resolved without anyone deleting a block"]],
        },
    },
    {
        "id": "ChainUses",
        "pattern": "SetOfUses",
        "title": "What each of the chains gives a developer to try",
        "concepts": ["PipelineOrder", "RegtestStartState"],
        "also_from": ["DevelopmentPipeline", "Regtest", "Signet", "Testnet"],
        "read_from": "chapter 11, Development pipeline: regtest has one dummy seed and no public peers, signet 2 seeds and a signed block rule, testnet3 5 seeds and the minimum-difficulty rule, mainnet 8 seeds",
        "why": "the passage lists what different chains offer, under different conditions: a set of uses by actors",
        "data": {
            "system": "A DEVELOPMENT PIPELINE",
            "actors": [{"id": "regtest", "label": "A developer on regtest"}, {"id": "signet", "label": "A developer on signet"}, {"id": "testnet", "label": "A developer on testnet3"}],
            "usecases": [
                {"id": "private", "label": "Work with one dummy seed and no public peers"},
                {"id": "signed", "label": "Test with a signed block rule"},
                {"id": "mindiff", "label": "Test with the minimum-difficulty rule"},
            ],
            "links": [["regtest", "private"], ["signet", "signed"], ["testnet", "mindiff"]],
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
