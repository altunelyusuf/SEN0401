#!/usr/bin/env python3
"""SEN0401 chapter 7 - the narrative diagrams of the chapter (version 1.0.0).

Same module shape and contract as chapter 6's sen0401_ch06_diagrams_v1_0_0.py (the owner's ruling of 2026-10-07: a paragraph gets the
diagram its narrative calls for, and the mapping from narrative pattern to diagram type lives in the CME ontology, never in the
author's choice); the diagrams are this chapter's, and the grounding threshold is 0.85 as the chapter brief requires (chapter 6 used 0.8).

Each entry names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read
from (also_from names further concepts whose explanations the content draws on), one sentence saying why the pattern fits, and the
content in the element names the renderer of that type expects. Every element label is made of words that occur in the explanations
of the accompanying concepts or their section, and run_checks() measures that besides the structural rules.

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "VerifySpend",
        "pattern": "Workflow",
        "title": "How a full node decides whether a spend is authorized",
        "concepts": ["SeparateExecution", "InputScript", "OutputScript", "ScriptTruth", "StackExecution"],
        "also_from": ["Script", "PayToScriptHashOutput", "WitnessProgram", "RedeemScript"],
        "read_from": "chapter 7, Separate execution of output and input scripts: the input script runs first and leaves a stack, the output script runs on a copy of that stack, and the spend is valid when the top item is true; with pay to script hash the redeem script is run as well, and with a witness program the witness is checked",
        "why": "the passage is a procedure with decisions - is the output a script hash, is it a witness program - and a result that depends on the top of the stack: a workflow",
        "data": {
            "nodes": [
                {"id": "input", "label": "Run the input script and keep the stack it leaves"},
                {"id": "output", "label": "Run the output script on that stack"},
                {"id": "top", "label": "Is the top item true?", "kind": "decision"},
                {"id": "p2sh", "label": "Is the output a script hash?", "kind": "decision"},
                {"id": "redeem", "label": "Run the redeem script on the stack"},
                {"id": "wit", "label": "Is the output a witness program?", "kind": "decision"},
                {"id": "witcheck", "label": "Check the witness against the program"},
                {"id": "valid", "label": "The spend is valid"},
                {"id": "rejected", "label": "The spend is rejected"},
            ],
            "flows": [["start", "input"], ["input", "output"], ["output", "top"], ["top", "rejected", "no"], ["top", "p2sh", "yes"],
                      ["p2sh", "redeem", "yes"], ["p2sh", "wit", "no"], ["redeem", "wit"], ["wit", "witcheck", "yes"], ["wit", "valid", "no"],
                      ["witcheck", "valid"], ["valid", "end"], ["rejected", "end"]],
        },
    },
    {
        "id": "ScriptFamilies",
        "pattern": "TopicAndParts",
        "title": "Authorization and authentication in nine branches",
        "concepts": ["ScriptLanguage", "KeyLocking", "ScriptedMultisig", "PayToScriptHash", "DataAndTime", "FlowControl", "SegwitScripts", "TreesAndTweaks", "TaprootBranch"],
        "also_from": ["Script", "PayToPublicKeyHash", "ScriptedMultisignature", "RedeemScript", "CheckLockTimeVerify", "ConditionalClauses", "P2wpkh", "Mast", "Taproot"],
        "read_from": "chapter 7, the whole chapter: the script language, locking to a key, scripted multisignatures, pay to script hash, data and time, flow control, segregated witness, trees and tweaks, and taproot",
        "why": "the chapter lays out one subject, the ways an output can ask for authorization, by its parts: a topic and its parts",
        "data": {
            "root": "Authorization and authentication",
            "branches": [
                {"label": "The script language", "children": ["A stack of operations, not Turing complete", "Stateless: the same result on every node"]},
                {"label": "Locking to a key", "children": ["Pay to public key hash", "A signature check with OP_CHECKSIG"]},
                {"label": "Scripted multisignatures", "children": ["OP_CHECKMULTISIG with m of n keys", "The extra dummy element"]},
                {"label": "Pay to script hash", "children": ["The redeem script moves to the spender", "Addresses that start with 3"]},
                {"label": "Data and time", "children": ["OP_RETURN data outputs", "Lock time and OP_CHECKLOCKTIMEVERIFY", "Relative timelocks and OP_CHECKSEQUENCEVERIFY"]},
                {"label": "Flow control", "children": ["OP_IF, OP_ELSE and OP_ENDIF", "Mohammed's script with three paths"]},
                {"label": "Segregated witness", "children": ["Pay to witness public key hash", "Pay to witness script hash"]},
                {"label": "Trees and tweaks", "children": ["A tree of alternative scripts", "Pay to contract", "Scriptless multisignatures"]},
                {"label": "Taproot", "children": ["Key path spending", "Script path spending", "Tapscript"]},
            ],
        },
    },
    {
        "id": "RedeemScriptExchange",
        "pattern": "Interaction",
        "title": "Pay to script hash: who sends what, and what the node checks",
        "concepts": ["PayToScriptHashOutput", "RedeemScript", "P2shAddress", "P2shBenefits", "P2shRules"],
        "also_from": ["ScriptedMultisignature", "OutputScript", "InputScript", "PublicKeyHash"],
        "read_from": "chapter 7, Pay to Script Hash: the payer pays to the hash of a script, the spender later shows the redeem script together with the data that satisfies it, and the node checks the hash and then runs the redeem script",
        "why": "the passage is an exchange between the payer, the spender and the full node in an order that matters - hash first, script later: an interaction",
        "data": {
            "participants": [{"id": "payer", "label": "Payer"}, {"id": "spender", "label": "Spender"}, {"id": "node", "label": "Full node"}],
            "messages": [
                ["spender", "payer", "an address that encodes the hash of the redeem script"],
                ["payer", "node", "a transaction that pays to the script hash"],
                ["spender", "node", "an input script with the signatures and the redeem script"],
                ["node", "node", "hash the redeem script and compare it with the script hash", "reply"],
                ["node", "node", "run the redeem script on the signatures", "reply"],
                ["node", "spender", "the spend is valid if the redeem script gives true", "reply"],
            ],
        },
    },
    {
        "id": "TimelockLife",
        "pattern": "LifeCycle",
        "title": "The life of a timelocked output",
        "concepts": ["LockTimeLimits", "CheckLockTimeVerify", "RelativeTimelock", "CheckSequenceVerify"],
        "also_from": ["MohammedScript", "OpReturnOutput"],
        "read_from": "chapter 7, Transaction lock time limitations, Check lock time verify and Relative timelocks: an output that cannot be spent before an absolute time or before a relative age, and that becomes spendable when the chain reaches it",
        "why": "the passages describe the states an output is in over time and the events that move it - created, waiting, mature, spent: a life cycle",
        "data": {
            "states": [
                {"id": "confirmed", "label": "Confirmed: the output is in a block"},
                {"id": "waiting", "label": "Waiting: the lock time has not passed"},
                {"id": "spendable", "label": "Spendable: the lock time has passed"},
                {"id": "spent", "label": "Spent: a valid transaction uses it"},
            ],
            "initial": "confirmed",
            "final": ["spent"],
            "transitions": [["confirmed", "waiting", "the script has a lock time or a relative lock"],
                            ["waiting", "spendable", "the block height or the age passes the lock"],
                            ["spendable", "spent", "a transaction with the signatures spends it"]],
        },
    },
    {
        "id": "MohammedUses",
        "pattern": "SetOfUses",
        "title": "Who can spend Mohammed's output, and when",
        "concepts": ["MohammedScript", "MultiPathScript", "ConditionalClauses", "CheckSequenceVerify"],
        "also_from": ["ScriptedMultisignature", "RelativeTimelock", "Miniscript"],
        "read_from": "chapter 7, Complex script example: the company's script has three paths - two of the three partners at any time, the lawyer with one partner after 30 days, and the lawyer alone after 90 days",
        "why": "the passage lists what different actors can do with the same output under different conditions: a set of uses by actors",
        "data": {
            "system": "MOHAMMED'S TIMELOCKED OUTPUT",
            "actors": [{"id": "partners", "label": "Two of the three partners"}, {"id": "lawyer", "label": "The lawyer"}, {"id": "partner", "label": "One partner"}],
            "usecases": [
                {"id": "any", "label": "Spend the output at any time with two signatures"},
                {"id": "thirty", "label": "Spend the output after 30 days with the lawyer's signature"},
                {"id": "ninety", "label": "Spend the output after 90 days alone"},
            ],
            "links": [["partners", "any"], ["lawyer", "thirty"], ["partner", "thirty"], ["lawyer", "ninety"]],
        },
    },
    {
        "id": "TaprootVerify",
        "pattern": "Workflow",
        "title": "How a node checks a taproot spend",
        "concepts": ["Taproot", "KeyPathSpending", "ScriptPathSpending", "ControlBlock"],
        "also_from": ["Mast", "PayToContract", "TapscriptChanges", "ChecksigAdd"],
        "read_from": "chapter 7, Taproot and BIP341: with one witness element left the key path is used and the element is a signature for the output key; with two or more the last is the control block and the one before is the script, the script's hash is folded with the hashes of the control block and the tweaked internal key must equal the output key, and then the script runs",
        "why": "the passage is a procedure with one decision - one element or more - and a different sequence of steps on each branch: a workflow",
        "data": {
            "nodes": [
                {"id": "annex", "label": "Remove the annex if the witness has one"},
                {"id": "count", "label": "Is there only one witness element?", "kind": "decision"},
                {"id": "sig", "label": "Check the signature for the output key"},
                {"id": "control", "label": "Take the control block and the script from the end of the witness"},
                {"id": "fold", "label": "Hash the script with the hashes of the control block"},
                {"id": "match", "label": "Is the tweaked internal key the output key?", "kind": "decision"},
                {"id": "run", "label": "Execute the script with the witness items"},
                {"id": "valid", "label": "The spend is valid"},
                {"id": "rejected", "label": "The spend is rejected"},
            ],
            "flows": [["start", "annex"], ["annex", "count"], ["count", "sig", "yes"], ["count", "control", "no"], ["sig", "valid"], ["control", "fold"], ["fold", "match"],
                      ["match", "run", "yes"], ["match", "rejected", "no"], ["run", "valid"], ["valid", "end"], ["rejected", "end"]],
        },
    },
    {
        "id": "CooperateOrReveal",
        "pattern": "Interaction",
        "title": "Taproot: the parties agree, or one of them reveals a script",
        "concepts": ["KeyPathSpending", "ScriptPathSpending", "ScriptlessMultisignature", "Taproot"],
        "also_from": ["Mast", "ControlBlock", "ThresholdSignature"],
        "read_from": "chapter 7, Taproot: when all participants agree they sign with the combined key and the chain shows one signature; when they do not, one participant reveals one script of the tree, a control block and the data that satisfies it",
        "why": "the passage is an exchange between the participants, a wallet and the full node, with an order and two possible outcomes: an interaction",
        "data": {
            "participants": [{"id": "parties", "label": "The participants"}, {"id": "wallet", "label": "One participant's wallet"}, {"id": "node", "label": "Full node"}],
            "messages": [
                ["parties", "node", "a transaction that pays to the taproot output key"],
                ["parties", "wallet", "all agree: the partial signatures are combined"],
                ["wallet", "node", "key path: one signature for the output key"],
                ["node", "wallet", "valid: the chain shows only a signature", "reply"],
                ["parties", "wallet", "they do not agree: one script of the tree is chosen"],
                ["wallet", "node", "script path: the script, the control block and the data"],
                ["node", "wallet", "valid: only the script that was used is public", "reply"],
            ],
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
            if n and h / n < 0.85: bad.append("%s: grounding %d/%d below 0.85; words not in the concepts' explanations: %s" % (d["id"], h, n, ", ".join(miss)))
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
