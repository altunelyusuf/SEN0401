#!/usr/bin/env python3
"""SEN0401 chapter 13 - the narrative diagrams of the chapter (version 1.0.0).

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
        "id": "CheckSoftwareDownload",
        "pattern": "Workflow",
        "title": "How a user checks the downloaded software against the published list",
        "concepts": ["TarballHashMatches", "SignatureNeedsKeys"],
        "also_from": ["VerifyingTheSoftware"],
        "read_from": "chapter 13, The tarball hash matches: the SHA-256 of the tarball equals its line among the lines of SHA256SUMS and that line is in the saved copy of the list; a signature needs keys",
        "why": "the passage is a procedure with a decision - does the hash of the tarball equal its line in the list - and a different outcome on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "hash", "label": "Does the SHA-256 of the tarball equal its line in the list?", "kind": "decision"},
                {"id": "use", "label": "The tarball is the published one"},
                {"id": "stop", "label": "The tarball is not used"},
            ],
            "flows": [["start", "hash"], ["hash", "use", "yes"], ["hash", "stop", "no"], ["use", "end"], ["stop", "end"]],
        },
    },
    {
        "id": "SecurityInSixBranches",
        "pattern": "TopicAndParts",
        "title": "Bitcoin security in six branches",
        "concepts": ["SecurityModel", "ProtectingKeys", "KeepingAccess", "SharingControl", "CustodyHistory", "Survivability"],
        "also_from": ["TransactionsPublishable", "TransportEncryption", "RootOfTrust", "VerifyingTheSoftware", "ColdStorage", "WalletEncryption", "SigningDevices", "PaperAndMemory", "SeedWords", "WalletBackups", "Multisig", "SharingASecret", "ExchangeFailures", "PhysicalCoins", "Heirs", "Limits"],
        "read_from": "chapter 13, the whole chapter: the security model, protecting keys, keeping access, sharing control, custody history and survivability",
        "why": "the chapter lays out one subject, Bitcoin security, by its parts: a topic and its parts",
        "data": {
            "root": "Bitcoin security",
            "branches": [
                {"label": "The security model", "children": ["Transactions that can be published", "Transport encryption", "The root of trust", "Verifying the software"]},
                {"label": "Protecting keys", "children": ["Cold storage", "Wallet encryption", "Signing devices", "Paper and memory"]},
                {"label": "Keeping access", "children": ["Seed words", "Wallet backups"]},
                {"label": "Sharing control", "children": ["Multisignature", "Sharing a secret"]},
                {"label": "Custody history", "children": ["Exchange failures", "Physical coins"]},
                {"label": "Survivability", "children": ["Heirs", "Limits of the experiments"]},
            ],
        },
    },
    {
        "id": "ColdSigningExchange",
        "pattern": "Interaction",
        "title": "A hot node and a cold node sign a PSBT without a blockchain on the cold side",
        "concepts": ["PsbtThroughColdNode", "WatchOnlyCannotSign"],
        "also_from": ["ColdStorage"],
        "read_from": "chapter 13, A PSBT through a cold node: the cold node took the unsigned PSBT and returned a signed PSBT with the final witness, and the hot node finalized and broadcast it",
        "why": "the passage is an exchange between two nodes in an order that matters - the unsigned PSBT, the signed PSBT, the broadcast: an interaction",
        "data": {
            "participants": [{"id": "hot", "label": "The hot node"}, {"id": "cold", "label": "The cold node"}],
            "messages": [
                ["hot", "cold", "hands over the unsigned PSBT"],
                ["cold", "hot", "returns a signed PSBT with the final witness", "reply"],
            ],
        },
    },
    {
        "id": "HeirScriptLife",
        "pattern": "LifeCycle",
        "title": "The heir's coin, from locked to spendable after ten confirmations",
        "concepts": ["HeirWaitsTenBlocks"],
        "also_from": ["Heirs", "OlderSixtyFiveThousand"],
        "read_from": "chapter 13, The heir waits ten blocks: the heir's spend with sequence 10 was refused as non-BIP68-final at 1 and at 9 confirmations and accepted at 10, while the owner's spend was accepted at once",
        "why": "the passage describes the states a coin is in and the events that move it - refused at 1 and 9 confirmations, accepted at 10: a life cycle",
        "data": {
            "states": [
                {"id": "fresh", "label": "The coin has 1 confirmation"},
                {"id": "nine", "label": "The coin has 9 confirmations"},
                {"id": "ten", "label": "The coin has 10 confirmations"},
            ],
            "initial": "fresh",
            "final": ["ten"],
            "transitions": [["fresh", "nine", "the heir's spend is refused as non-BIP68-final"],
                            ["nine", "ten", "the heir's spend is accepted at 10"]],
        },
    },
    {
        "id": "KeyChoices",
        "pattern": "SetOfUses",
        "title": "What a single key and a 2-of-3 wallet each give an owner",
        "concepts": ["OddsOfLossAndTheft", "TwoOfThreeSigning"],
        "also_from": ["Multisig", "KeyLossTolerance"],
        "read_from": "chapter 13, The odds of loss and theft: one key alone is lost with 0.1 and stolen with 0.05; 2-of-3 is stuck with 0.028 and robbed with 0.00725",
        "why": "the passage lists what different setups offer an owner, under different conditions: a set of uses by actors",
        "data": {
            "system": "KEEPING COINS SAFE",
            "actors": [{"id": "single", "label": "An owner with one key"}, {"id": "multi", "label": "An owner with a 2-of-3 wallet"}],
            "usecases": [
                {"id": "lost", "label": "Is lost with 0.1 and stolen with 0.05"},
                {"id": "stuck", "label": "Is stuck with 0.028 and robbed with 0.00725"},
                {"id": "two", "label": "Needs two signers"},
            ],
            "links": [["single", "lost"], ["multi", "stuck"], ["multi", "two"]],
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
