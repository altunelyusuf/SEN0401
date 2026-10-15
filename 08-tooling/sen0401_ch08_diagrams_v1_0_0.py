#!/usr/bin/env python3
"""SEN0401 chapter 8 - the narrative diagrams of the chapter (version 1.0.0).

Same module shape and contract as chapter 7's sen0401_ch07_diagrams_v1_0_0.py (the owner's ruling of 2026-10-07: a paragraph gets the diagram its narrative calls for, and the mapping from
narrative pattern to diagram type lives in the CME ontology, never in the author's choice); the diagrams are this chapter's, and the grounding threshold is 0.8 as the page brief requires.

Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations the
content draws on), one sentence saying why the pattern fits, and the content in the element names the renderer of that type expects. Every element label is made of words that occur in the
explanations of the accompanying concepts or their section, and run_checks() measures that besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "AcceptSignature",
        "pattern": "Workflow",
        "title": "How a node judges a signature: consensus first, then relay policy",
        "concepts": ["StrictDerConsensus", "PolicyVerdicts", "LowSRule", "PolicyFlags"],
        "also_from": ["ConsensusAndPolicy", "DerEncoding", "SignatureMalleability"],
        "read_from": "chapter 8, Consensus rules and relay policy: a node applies stricter rules to the transactions it relays than the consensus rules that decide whether a block is valid; a non-DER signature is refused everywhere since BIP66, a high S value is refused in relay but accepted in a block",
        "why": "the passage is a procedure with decisions - is the signature strict DER, does it verify, is S high - and a different outcome on each branch, consensus against relay policy: a workflow",
        "data": {
            "nodes": [
                {"id": "der", "label": "Is the signature strict DER?", "kind": "decision"},
                {"id": "verify", "label": "Does the signature verify?", "kind": "decision"},
                {"id": "high", "label": "Is the S value high?", "kind": "decision"},
                {"id": "relay", "label": "The transaction is relayed and valid"},
                {"id": "refuse", "label": "The node refuses to relay it, but a block may hold it"},
                {"id": "invalid", "label": "The transaction is invalid"},
            ],
            "flows": [["start", "der"], ["der", "verify", "yes"], ["der", "invalid", "no"], ["verify", "high", "yes"], ["verify", "invalid", "no"],
                      ["high", "refuse", "yes"], ["high", "relay", "no"], ["relay", "end"], ["refuse", "end"], ["invalid", "end"]],
        },
    },
    {
        "id": "SignatureBranches",
        "pattern": "TopicAndParts",
        "title": "Digital signatures in seven branches",
        "concepts": ["SignatureFoundations", "SighashFlags", "SchnorrSignatures", "EcdsaSignatures", "Randomness", "SegwitSigning", "SinceTheBook"],
        "also_from": ["SignatureRoles", "Commitments", "Bip340Format", "Aggregation", "DerEncoding", "NonceSafety", "TaprootSigning", "StandardsStatus"],
        "read_from": "chapter 8, the whole chapter: what a signature is, the signature hash flags, schnorr signatures, ECDSA signatures, randomness and signature size, segwit signing, and what moved since print",
        "why": "the chapter lays out one subject, signatures, by its parts: a topic and its parts",
        "data": {
            "root": "Digital signatures",
            "branches": [
                {"label": "Foundations of digital signatures", "children": ["What a signature does", "Arithmetic of the curve", "Signing a transaction"]},
                {"label": "Signature hash flags (SIGHASH)", "children": ["How flags are coded", "What each flag commits to", "Known pitfalls of the flags"]},
                {"label": "Schnorr signatures", "children": ["From identity proof to signature", "The BIP340 format", "Aggregating keys and signatures", "Threshold signatures from secret sharing"]},
                {"label": "ECDSA signatures", "children": ["The ECDSA equations", "DER serialization", "Consensus rules and relay policy"]},
                {"label": "Randomness and signature size", "children": ["Safety of the nonce", "Deterministic nonces", "Signature size and nonce grinding"]},
                {"label": "Segwit signing", "children": ["Cost of hashing", "Commitment to amounts", "Taproot signing"]},
                {"label": "Since the book went to print", "children": ["Status of the standards", "Library and release support", "History and dates"]},
            ],
        },
    },
    {
        "id": "KeyCancellationExchange",
        "pattern": "Interaction",
        "title": "The key cancellation attack on naive key aggregation",
        "concepts": ["KeyCancellation", "NaiveMultisig", "MuSigBlocksCancellation"],
        "also_from": ["Aggregation", "MuSigKeyAgg", "Linearity"],
        "read_from": "chapter 8, Naive scriptless multisignature, Key cancellation attack and MuSig2 against key cancellation: Bob waits to see Alice's public key, publishes his key minus hers, and can sign alone for both; with the coefficients of BIP327 the aggregate is not his key",
        "why": "the passage is an exchange between two signers and a verifier in an order that matters - Alice first, Bob after seeing her key: an interaction",
        "data": {
            "participants": [{"id": "alice", "label": "Alice"}, {"id": "bob", "label": "Bob"}, {"id": "verifier", "label": "The verifier"}],
            "messages": [
                ["alice", "bob", "publishes her public key yG"],
                ["bob", "alice", "publishes the key zG minus yG after seeing hers"],
                ["bob", "verifier", "signs alone with z for the aggregate key zG"],
                ["verifier", "bob", "the signature verifies against the aggregate", "reply"],
                ["bob", "verifier", "with the coefficients of BIP327 the aggregate is not his key"],
                ["verifier", "bob", "Bob cannot sign alone", "reply"],
            ],
        },
    },
    {
        "id": "NonceLife",
        "pattern": "LifeCycle",
        "title": "The life of a signing nonce, from one-time secret to lost key",
        "concepts": ["NonceReuse", "DistinctNonces", "DeterministicSigning"],
        "also_from": ["NonceSafety", "Rfc6979Vector", "Randomness"],
        "read_from": "chapter 8, Nonce reuse: the nonce k is a one-time secret; two signatures with the same k have the same R, anyone can compute k and then the private key",
        "why": "the passage describes the states a nonce is in and the events that move it - chosen, used, reused, the key recovered: a life cycle",
        "data": {
            "states": [
                {"id": "chosen", "label": "Chosen: the nonce k is a one-time secret"},
                {"id": "used", "label": "Used: one signature is made with k"},
                {"id": "reused", "label": "Reused: two signatures have the same R"},
                {"id": "lost", "label": "The private key is recovered"},
            ],
            "initial": "chosen",
            "final": ["lost"],
            "transitions": [["chosen", "used", "the signer signs a hash"],
                            ["used", "reused", "the signer uses k a second time"],
                            ["reused", "lost", "anyone computes k from the two signatures and then the private key"]],
        },
    },
    {
        "id": "FlagUses",
        "pattern": "SetOfUses",
        "title": "What the signature hash flags let a signer do",
        "concepts": ["AnyoneCanPayEffect", "SingleBug", "CommitmentMatrix"],
        "also_from": ["Commitments", "FlagValues", "SighashFlags"],
        "read_from": "chapter 8, Effect of ANYONECANPAY, The SIGHASH_SINGLE bug and Matrix of commitments: ANYONECANPAY lets anybody add inputs after one input has been signed; SIGHASH_SINGLE signs the output that has the same position as the input",
        "why": "the passage lists what a signer can do with different flags, under different conditions: a set of uses by actors",
        "data": {
            "system": "A SIGNATURE HASH FLAG",
            "actors": [{"id": "all", "label": "A signer with ALL"}, {"id": "single", "label": "A signer with SINGLE"}, {"id": "acp", "label": "A signer with ANYONECANPAY"}],
            "usecases": [
                {"id": "outputs", "label": "Commit to the outputs of the transaction"},
                {"id": "same", "label": "Sign the output that has the same position as the input"},
                {"id": "open", "label": "Let anybody add inputs after one input has been signed"},
            ],
            "links": [["all", "outputs"], ["single", "same"], ["acp", "open"], ["acp", "outputs"]],
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
