#!/usr/bin/env python3
"""SEN0401 chapter 10 - the narrative diagrams of the chapter (version 1.0.0).

Same module shape and contract as chapter 9's sen0401_ch09_diagrams_v1_0_0.py (the owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for, and the mapping from
narrative pattern to diagram type lives in the CME ontology, never in the author's choice); the diagrams are this chapter's, and the grounding threshold is 0.8 as the page brief requires.

Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations the
content draws on), one sentence saying why the pattern fits, and the content in the element names the renderer of that type expects. Every element label is made of words that occur in the
explanations of the accompanying concepts or their section, and run_checks() measures that besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "AnswerBlockRequest",
        "pattern": "Workflow",
        "title": "How a node answers a request for a block with a compact block",
        "concepts": ["CompactBlockDepthLimit", "MissingTransactionsRequest", "CoinbaseIsPrefilled", "ShortIdsAreSixBytes"],
        "also_from": ["CompactBlocks", "RaceAndAnnouncement"],
        "read_from": "chapter 10, Compact blocks: a compact block is answered only for a block at most 5 blocks deep, otherwise the full block is sent; the receiver completes the block from its mempool and asks with getblocktxn for the transactions it lacks",
        "why": "the passage is a procedure with decisions - is the block deep, does the receiver lack transactions - and a different outcome on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "deep", "label": "Is the block at most 5 blocks deep?", "kind": "decision"},
                {"id": "lack", "label": "Does the receiver lack transactions of the block?", "kind": "decision"},
                {"id": "full", "label": "The node answers with the full block"},
                {"id": "complete", "label": "The receiver completes the block from its mempool"},
                {"id": "ask", "label": "The receiver asks with getblocktxn and the node answers with blocktxn"},
            ],
            "flows": [["start", "deep"], ["deep", "lack", "yes"], ["deep", "full", "no"], ["lack", "complete", "no"], ["lack", "ask", "yes"],
                      ["full", "end"], ["complete", "end"], ["ask", "end"]],
        },
    },
    {
        "id": "NetworkBranches",
        "pattern": "TopicAndParts",
        "title": "The Bitcoin network in seven branches",
        "concepts": ["NetworkAndNodes", "PeersAndDiscovery", "BlockRelay", "Syncing", "LightClients", "PrivacyAndTransport", "MempoolAndOrphans"],
        "also_from": ["FlatNetwork", "Handshake", "CompactBlocks", "HeadersFirst", "BloomFilters", "EncryptedTransport", "OrphanPool"],
        "read_from": "chapter 10, the whole chapter: the network and its nodes, peers and discovery, block relay, syncing, light clients, privacy and transport, and the mempool with orphans",
        "why": "the chapter lays out one subject, the Bitcoin network, by its parts: a topic and its parts",
        "data": {
            "root": "The Bitcoin network",
            "branches": [
                {"label": "Network and nodes", "children": ["Flat network", "Node kinds"]},
                {"label": "Peers and discovery", "children": ["Handshake", "Discovery", "Connections"]},
                {"label": "Block relay", "children": ["Race and announcement", "Compact blocks", "Private relay"]},
                {"label": "Syncing", "children": ["Headers first"]},
                {"label": "Light clients", "children": ["Simplified payment verification (SPV)", "Bloom filters", "Block filters"]},
                {"label": "Privacy and transport", "children": ["Encrypted transport", "Anonymity networks", "Network attacks"]},
                {"label": "Mempool and orphans", "children": ["Mempool relay", "Orphan pool"]},
            ],
        },
    },
    {
        "id": "HandshakeOrder",
        "pattern": "Interaction",
        "title": "The messages a node sends when it accepts a connection",
        "concepts": ["HandshakeMessageOrder", "VersionMessageFields"],
        "also_from": ["Handshake", "MessageFraming"],
        "read_from": "chapter 10, Handshake message order: a node that accepts a connection says version first, then the feature messages wtxidrelay and sendaddrv2, then verack, and after verack it sends sendcmpct, ping, getheaders, inv and feefilter",
        "why": "the passage is an exchange between a peer and a node in an order that matters - version first, then features, then verack: an interaction",
        "data": {
            "participants": [{"id": "peer", "label": "The connecting peer"}, {"id": "node", "label": "The node"}],
            "messages": [
                ["peer", "node", "connects to the node"],
                ["node", "peer", "says version first", "reply"],
                ["node", "peer", "then the feature messages wtxidrelay and sendaddrv2"],
                ["node", "peer", "then verack"],
                ["node", "peer", "after verack: sendcmpct, ping, getheaders, inv and feefilter"],
            ],
        },
    },
    {
        "id": "OrphanLife",
        "pattern": "LifeCycle",
        "title": "The life of a child transaction that arrives before its parent",
        "concepts": ["OrphanWaitsForParent", "NodeRequestsMissingParent", "ParentReleasesOrphan"],
        "also_from": ["OrphanPool", "MempoolAndOrphans"],
        "read_from": "chapter 10, Orphan pool: a child whose parent was not known did not enter the mempool and was kept in the orphanage; the node asked the peer for the parent with getdata, and when the parent arrived both were in the mempool",
        "why": "the passage describes the states a child transaction is in and the events that move it - unknown parent, kept in the orphanage, parent requested, both in the mempool: a life cycle",
        "data": {
            "states": [
                {"id": "child", "label": "A child arrives whose parent was not known"},
                {"id": "orphan", "label": "The child is kept in the orphanage"},
                {"id": "asked", "label": "The node asks the peer for the parent"},
                {"id": "both", "label": "Both are in the mempool"},
            ],
            "initial": "child",
            "final": ["both"],
            "transitions": [["child", "orphan", "the child does not enter the mempool"],
                            ["orphan", "asked", "the node asks with getdata"],
                            ["asked", "both", "the parent arrives and releases the child"]],
        },
    },
    {
        "id": "RelayFlagUses",
        "pattern": "SetOfUses",
        "title": "What three kinds of peer receive of the announced transactions",
        "concepts": ["RelayFlagSilencesTransactions"],
        "also_from": ["Handshake", "MempoolRelay", "Connections"],
        "read_from": "chapter 10, Relay flag silences transactions: of two transactions the node announced two to the normal peer, none to the peer that connected with the relay flag false, and one to the peer whose feefilter was 5 satoshis per virtual byte",
        "why": "the passage lists what different peers get under different conditions - the relay flag and the feefilter: a set of uses by actors",
        "data": {
            "system": "TRANSACTION ANNOUNCEMENTS",
            "actors": [{"id": "normal", "label": "A normal peer"}, {"id": "silent", "label": "A peer with the relay flag false"}, {"id": "filter", "label": "A peer with a feefilter"}],
            "usecases": [
                {"id": "all", "label": "Receive both of the announced transactions"},
                {"id": "none", "label": "Receive no announcement at all"},
                {"id": "one", "label": "Receive only the transactions that pay enough"},
            ],
            "links": [["normal", "all"], ["silent", "none"], ["filter", "one"]],
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
