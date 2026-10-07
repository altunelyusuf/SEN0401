#!/usr/bin/env python3
"""SEN0401 chapter 3 - the narrative diagrams of the chapter (version 1.0.0).

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
        "id": "BuildFromSource",
        "pattern": "Workflow",
        "title": "From the Git repository to installed executables",
        "concepts": ["Build", "Source", "ReleaseTag", "GitRepository", "Toolchain", "CMakeBuild", "Compilation", "BuildPrerequisite", "Executable"],
        "also_from": ["ReleaseCandidate", "SourceCode", "PackageManager", "ReleaseVerification"],
        "read_from": "chapter 3, the Build branch: Git repository (clone the project and its history), Release tag (check out a stable version, not a release candidate), Build prerequisite (missing libraries make the build fail), CMake build (cmake -B build, cmake --build build, cmake --install build), Compilation (the CXX lines, resumable), Executable (bitcoind, bitcoin-cli, bitcoin-tx; which confirms the installation)",
        "why": "the branch walks through a procedure the reader performs in order, with one check that can send them back - the prerequisites - and ends with the installed programs: a workflow",
        "data": {
            "nodes": [
                {"id": "clone", "label": "Clone the Git repository with its history"},
                {"id": "tag", "label": "Check out the release tag of a stable version (no rc suffix)"},
                {"id": "prereq", "label": "Are the build prerequisites installed?", "kind": "decision"},
                {"id": "install_prereq", "label": "Install the missing libraries and tools with the package manager"},
                {"id": "configure", "label": "Configure the build: cmake -B build, with options such as no wallet"},
                {"id": "compile", "label": "Compile: cmake --build build; CXX lines, up to an hour, resumable"},
                {"id": "installexe", "label": "Install the executables: bitcoind, bitcoin-cli, bitcoin-tx"},
                {"id": "which", "label": "Confirm with which that the system finds them"},
            ],
            "flows": [["start", "clone"], ["clone", "tag"], ["tag", "prereq"], ["prereq", "install_prereq", "no"], ["install_prereq", "prereq"], ["prereq", "configure", "yes"], ["configure", "compile"], ["compile", "installexe"], ["installexe", "which"], ["which", "end"]],
        },
    },
    {
        "id": "NodeLife",
        "pattern": "LifeCycle",
        "title": "The life of a node, from first start to serving the network",
        "concepts": ["Running", "Daemon", "StartupLog", "InitialDownload", "PrunedNode", "NodeResources"],
        "also_from": ["ConfigurationFile", "DataDirectory", "BlockchainInfo", "FullNode", "Peer"],
        "read_from": "chapter 3: Running (started in the foreground with the log to the console, then as a daemon), Start-up log (version, settings, connection limits, debug.log in the data directory), Initial download (the whole chain fetched and validated before transactions can be processed), Pruned node (old block files deleted after verification), Peer and connection",
        "why": "the passages describe states a node is in and what moves it on - starting, reading its configuration, downloading and validating the chain, synchronised and serving peers, stopped: a life cycle",
        "data": {
            "states": [
                {"id": "starting", "label": "Started: reads bitcoin.conf, writes the start-up log"},
                {"id": "ibd", "label": "Initial download: the whole chain from peers, validated"},
                {"id": "synced", "label": "Running at the tip of the chain, processing transactions"},
                {"id": "pruning", "label": "Pruned: old block files removed after verification"},
                {"id": "behind", "label": "Ten days off: downloading and validating the blocks it missed"},
                {"id": "stopped", "label": "Interrupted or stopped"},
            ],
            "initial": "starting",
            "final": ["stopped"],
            "transitions": [["starting", "ibd", "first start: no blocks in the data directory"], ["ibd", "synced", "the full dataset downloaded and validated"], ["synced", "pruning", "prune option set"], ["pruning", "synced", "disk requirement reduced"], ["synced", "stopped", "the owner interrupts the program"], ["stopped", "behind", "started again after ten days"], ["behind", "synced", "the blocks are validated"]],
        },
    },
    {
        "id": "RpcCall",
        "pattern": "Interaction",
        "title": "One JSON-RPC call, from bitcoin-cli to the node and back",
        "concepts": ["Interface", "RpcInterface", "JsonRpc", "HttpRequest", "CookieAuthentication", "RpcAuth", "Client", "CommandLineClient", "WrapperLibrary"],
        "also_from": ["Api", "JsonFormat", "DataDirectory", "BlockchainInfo"],
        "read_from": "chapter 3: RPC interface (Bitcoin Core's API is JSON-RPC over HTTP, 127.0.0.1 port 8332), JSON-RPC (a request object with method, params and id), HTTP request (an HTTP POST with the call as its body), Cookie authentication (a random credential in .cookie, read from the data directory), rpcauth (user, salt and hash in the configuration), Command-line client (builds the request, finds the credential, sends it), Wrapper library (python-bitcoinlib's RawProxy)",
        "why": "the passages describe messages between a caller, the node and the data directory in a fixed order - find the credential, send the request, check it, answer: an interaction",
        "data": {
            "participants": [{"id": "caller", "label": "bitcoin-cli or a wrapper library"}, {"id": "datadir", "label": "Data directory"}, {"id": "node", "label": "bitcoind (JSON-RPC over HTTP)"}, {"id": "conf", "label": "bitcoin.conf"}],
            "messages": [
                ["caller", "datadir", "read the .cookie credential (or use the rpcauth user and password)"],
                ["datadir", "caller", "the random password of this session", "reply"],
                ["caller", "node", "HTTP POST to 127.0.0.1:8332: the JSON-RPC request (method, params, id)"],
                ["node", "conf", "check the credential: the cookie, or the salt and hash under rpcauth"],
                ["conf", "node", "accepted", "reply"],
                ["node", "node", "run the method, for example getblockchaininfo"],
                ["node", "caller", "HTTP response with the JSON-RPC result and the same id", "reply"],
                ["caller", "caller", "print the JSON, or return it as a Python value"],
            ],
        },
    },
    {
        "id": "ReleaseAssurance",
        "pattern": "Workflow",
        "title": "Verifying a downloaded release before running it",
        "concepts": ["Ecosystem", "Assurance", "ReleaseVerification", "Checksum", "OpenPgpSignature", "ReproducibleBuild"],
        "also_from": ["Executable", "PackageRegistry"],
        "read_from": "chapter 3, the Assurance section: Release verification (SHA256SUMS and the signatures on it; first that the list is genuine, then that the file has the listed checksum), Checksum (SHA-256 over the bytes of the file), OpenPGP signature (a secret key signs, anybody with the public key checks), Reproducible build (several builders get the same bytes from the same source)",
        "why": "the section gives a check in two steps with a decision at each - genuine list, matching checksum - before the program is run: a workflow",
        "data": {
            "nodes": [
                {"id": "download", "label": "Download the release file, SHA256SUMS and the signatures on it"},
                {"id": "keys", "label": "Fetch the builders' public keys"},
                {"id": "sigok", "label": "Do the OpenPGP signatures on SHA256SUMS verify?", "kind": "decision"},
                {"id": "sum", "label": "Compute the SHA-256 checksum of the downloaded file"},
                {"id": "sumok", "label": "Does it equal the checksum listed for the file?", "kind": "decision"},
                {"id": "run", "label": "The file is what the builders built: run it"},
                {"id": "discard", "label": "Do not run it: the list is not genuine or the file changed"},
            ],
            "flows": [["start", "download"], ["download", "keys"], ["keys", "sigok"], ["sigok", "sum", "yes"], ["sigok", "discard", "no"], ["sum", "sumok"], ["sumok", "run", "yes"], ["sumok", "discard", "no"], ["run", "end"], ["discard", "end"]],
        },
    },
    {
        "id": "ConfiguringANode",
        "pattern": "TopicAndParts",
        "title": "What the configuration file can say",
        "concepts": ["Operation", "Configuration", "ConfigurationFile", "ConfigurationOption", "DataDirectory"],
        "also_from": ["DatabaseCache", "TransactionIndex", "BlocksOnlyMode", "MempoolLimit", "AlertNotify", "PrunedNode", "Daemon"],
        "read_from": "chapter 3, the Configuration section: Configuration file (option=value lines in bitcoin.conf, read from the data directory on every start), Data directory (blocks, the unspent-output database, logs and wallets), and the options the chapter explains - prune, dbcache, txindex, blocksonly, maxmempool, alertnotify, daemon",
        "why": "the section describes one thing, the configuration, by the groups of options it holds and what each option governs - a topic and its parts",
        "data": {
            "root": "bitcoin.conf",
            "branches": [
                {"label": "Where it lives", "children": ["The data directory, read on every start", "option=value, one per line, no leading hyphen", "The same options work on the command line"]},
                {"label": "Disk", "children": ["prune: delete old blocks after verification", "txindex: index every transaction", "datadir: another folder"]},
                {"label": "Memory", "children": ["dbcache: the database cache in megabytes", "maxmempool: the mempool limit in megabytes"]},
                {"label": "Network and running", "children": ["blocksonly: no unconfirmed transactions relayed", "daemon: run in the background", "alertnotify: a command run on an alert"]},
            ],
        },
    },
    {
        "id": "ChainReorganisation",
        "pattern": "LifeCycle",
        "title": "What a node does with a new block: extend, fork, or reorganise",
        "concepts": ["Data", "ChainState", "BestChain", "ChainWork", "Reorganization", "Fork", "Confirmation"],
        "also_from": ["Block", "BlockHeight", "FullNode"],
        "read_from": "chapter 3, the Chain state section: Best chain (the greatest-cumulative-work valid chain; its end is the tip), Chain work, Fork (two blocks at the same height), Chain reorganization (a block that does not extend the best chain goes to a secondary chain; if that chain now has more work the node reorganises its view of confirmed transactions), Confirmation (depth of a block)",
        "why": "the passages describe the states the node's view of the chain is in and the events - a new block arrives, work is compared - that move it between them: a life cycle",
        "data": {
            "states": [
                {"id": "tip", "label": "One best chain: the new block extends the tip"},
                {"id": "forked", "label": "Two branches at the same height: a secondary chain"},
                {"id": "compare", "label": "Comparing cumulative work of the branches"},
                {"id": "reorg", "label": "Reorganising: its view of confirmed transactions and UTXOs changes"},
            ],
            "initial": "tip",
            "final": [],
            "transitions": [["tip", "forked", "a valid block that does not extend the tip"], ["forked", "compare", "the next block arrives"], ["compare", "tip", "the best chain still has the most work"], ["compare", "reorg", "the secondary chain has more work"], ["reorg", "tip", "the node's view follows the new best chain"], ["tip", "tip", "each block on top adds a confirmation"]],
        },
    },
    {
        "id": "WhoUsesTheNode",
        "pattern": "SetOfUses",
        "title": "Who works with a Bitcoin Core node, and through what",
        "concepts": ["Node", "Verification", "FullNode", "ReferenceImplementation", "Client", "CommandLineClient", "WrapperLibrary", "Wallet", "DescriptorWallet"],
        "also_from": ["JsonRpc", "Api", "Peer", "BlockchainInfo", "NetworkInfo", "DecodedTransaction", "OutputDescriptor", "ImprovementProposal"],
        "read_from": "chapter 3: Full node (verifies every confirmed transaction against every rule; accepts, validates and relays blocks from other full nodes), Command-line client (bitcoin-cli makes node and wallet RPC calls, for experimenting interactively), Wrapper library (python-bitcoinlib for programs), Wallet (optional, next to the validation engine), Peer and connection, Bitcoin Improvement Proposal",
        "why": "the passages tell what different people and programs do with the node - an operator asking it questions, a program calling its API, peers exchanging blocks, a wallet keeping keys - a set of uses by actors",
        "data": {
            "system": "A BITCOIN CORE NODE",
            "actors": [{"id": "operator", "label": "Node operator"}, {"id": "program", "label": "A program (wrapper library)"}, {"id": "peers", "label": "Other full nodes"}, {"id": "walletuser", "label": "Wallet user"}],
            "usecases": [
                {"id": "chaininfo", "label": "Ask for blockchain information (getblockchaininfo)"},
                {"id": "netinfo", "label": "Ask for network information (getnetworkinfo)"},
                {"id": "decode", "label": "Decode a transaction or read a block"},
                {"id": "api", "label": "Call the JSON-RPC API from code"},
                {"id": "relay", "label": "Exchange and validate blocks and transactions"},
                {"id": "verify", "label": "Verify every transaction against every rule"},
                {"id": "descwallet", "label": "Keep keys in a descriptor wallet"},
                {"id": "bip", "label": "Follow the consensus rules as the BIPs define them"},
            ],
            "links": [["operator", "chaininfo"], ["operator", "netinfo"], ["operator", "decode"], ["program", "api"], ["program", "decode"], ["peers", "relay"], ["peers", "verify"], ["walletuser", "descwallet"], ["peers", "bip"]],
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
