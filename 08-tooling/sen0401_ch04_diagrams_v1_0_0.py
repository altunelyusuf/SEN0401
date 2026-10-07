#!/usr/bin/env python3
"""SEN0401 chapter 4 - the narrative diagrams of the chapter (version 1.0.0).

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
        "id": "KeyToAddress",
        "pattern": "Workflow",
        "title": "From 256 random bits to a P2PKH address",
        "concepts": ["Keys", "KeyPair", "PrivateKey", "PublicKey", "Entropy", "SecureRandomness", "PointMultiplication", "Hash160", "Base58Check", "P2pkhAddress"],
        "also_from": ["Hashing", "Sha256", "Ripemd160", "VersionPrefix", "Checksum", "CompressedPublicKey", "GeneratorPoint"],
        "read_from": "chapter 4: Private key (a number picked at random between 1 and n-1), Entropy and Secure randomness (256 bits from a CSPRNG, never a simple generator), Public key (K = k x G by elliptic curve multiplication), Compressed public key (x and one parity byte, 33 bytes), HASH160 (RIPEMD160 of SHA256), Base58check (version byte, data, four checksum bytes), P2PKH address (version 0x00, begins with 1)",
        "why": "the branch is a procedure every wallet performs in order, with one choice - the compressed or the uncompressed encoding of the public key - and one output, the address: a workflow",
        "data": {
            "nodes": [
                {"id": "random", "label": "Draw 256 bits from a cryptographically secure random generator"},
                {"id": "privkey", "label": "The private key k: a number between 1 and n - 1"},
                {"id": "mult", "label": "Elliptic curve multiplication: K = k x G"},
                {"id": "compressed", "label": "Compressed encoding?", "kind": "decision"},
                {"id": "enc33", "label": "33 bytes: x and one byte for the parity of y"},
                {"id": "enc65", "label": "65 bytes: both coordinates"},
                {"id": "hash160", "label": "HASH160: RIPEMD160(SHA256(K)), a 20-byte commitment"},
                {"id": "b58", "label": "Base58check: version byte 0x00, the commitment, four checksum bytes"},
                {"id": "address", "label": "A P2PKH address beginning with 1"},
            ],
            "flows": [["start", "random"], ["random", "privkey"], ["privkey", "mult"], ["mult", "compressed"], ["compressed", "enc33", "yes"], ["compressed", "enc65", "no"], ["enc33", "hash160"], ["enc65", "hash160"], ["hash160", "b58"], ["b58", "address"], ["address", "end"]],
        },
    },
    {
        "id": "AddressKinds",
        "pattern": "TopicAndParts",
        "title": "The kinds of address, legacy and segwit",
        "concepts": ["Address", "Legacy", "Segwit", "P2shAddress", "Bech32Address", "Bech32mAddress", "P2wpkh", "P2wsh", "P2tr"],
        "also_from": ["P2pkhAddress", "VersionPrefix", "WitnessVersion", "WitnessProgram", "HumanReadablePart", "RedeemScript", "NestedSegwit", "DefaultAddressType"],
        "read_from": "chapter 4, the Address branch: Legacy addresses (P2PKH with version 0x00 beginning with 1, P2SH with version 5 beginning with 3, both base58check), Segwit addresses (bech32 for witness version 0: P2WPKH with a 20-byte program, P2WSH with 32 bytes; bech32m for version 1: P2TR), Segwit inside P2SH, the human-readable part, Default address type (bech32)",
        "why": "the branch classifies one thing, the address, by its encoding and the kind of output it commits to, and lists the members of each class - a topic and its parts",
        "data": {
            "root": "Bitcoin address",
            "branches": [
                {"label": "Legacy: base58check", "children": ["P2PKH: version 0x00, begins with 1, HASH160 of a public key", "P2SH: version 5, begins with 3, HASH160 of a redeem script", "Segwit inside P2SH: a P2SH address wrapping a witness program"]},
                {"label": "Segwit version 0: bech32", "children": ["P2WPKH: witness program of 20 bytes, the HASH160 of a public key", "P2WSH: witness program of 32 bytes, the SHA256 of a script", "Human-readable part bc, separator 1, six-character checksum"]},
                {"label": "Segwit version 1: bech32m", "children": ["P2TR: a 32-byte witness program that is a point on the curve", "The length extension weakness of bech32 fixed"]},
                {"label": "Which one a wallet gives out", "children": ["Bitcoin Core's addresstype defaults to bech32", "legacy, p2sh-segwit, bech32, bech32m"]},
            ],
        },
    },
    {
        "id": "ScriptEvaluation",
        "pattern": "Workflow",
        "title": "How a full node runs the input script and the output script",
        "concepts": ["Scripts", "OutputScript", "InputScript", "StackExecution"],
        "also_from": ["P2pkhAddress", "DigitalSignature", "Hash160", "PublicKey"],
        "read_from": "chapter 4, Locking and unlocking scripts: Output script (the lock: OP_DUP OP_HASH160 <commitment> OP_EQUALVERIFY OP_CHECKSIG for P2PKH), Input script (the signature followed by the public key), Stack, opcodes and script evaluation (data pushed on top, each opcode consumes the topmost items and pushes its result; valid when the stack ends with true)",
        "why": "the passages describe the steps of the script machine in order with a test at the end - push, duplicate, hash, compare, check the signature: a workflow",
        "data": {
            "nodes": [
                {"id": "push", "label": "Push the input script: the signature, then the public key"},
                {"id": "dup", "label": "OP_DUP: duplicate the public key on top of the stack"},
                {"id": "hash", "label": "OP_HASH160: replace the copy by its HASH160"},
                {"id": "pushc", "label": "Push the commitment from the output script"},
                {"id": "eqv", "label": "OP_EQUALVERIFY: are the two commitments equal?", "kind": "decision"},
                {"id": "sig", "label": "OP_CHECKSIG: does the signature verify with the public key?", "kind": "decision"},
                {"id": "valid", "label": "The stack ends with true: the spend is allowed"},
                {"id": "invalid", "label": "Evaluation fails: the transaction is not valid"},
            ],
            "flows": [["start", "push"], ["push", "dup"], ["dup", "hash"], ["hash", "pushc"], ["pushc", "eqv"], ["eqv", "sig", "yes"], ["eqv", "invalid", "no"], ["sig", "valid", "yes"], ["sig", "invalid", "no"], ["valid", "end"], ["invalid", "end"]],
        },
    },
    {
        "id": "KeyEncodings",
        "pattern": "LifeCycle",
        "title": "One private key, its encodings",
        "concepts": ["Format", "KeyEncoding", "WalletImportFormat", "CompressedPrivateKey", "Checksummed", "VersionPrefix", "KeyExport"],
        "also_from": ["Base58Check", "NumberBase", "CompressedPublicKey", "PrivateKey", "Checksum"],
        "read_from": "chapter 4: Key encoding (hexadecimal, wallet import format, WIF with a compression flag - all the same number, any one convertible to any other), Wallet import format (base58check of version 0x80 and the 32-byte key, a 01 suffix for compressed public keys), Version prefix (0x80 for a private key: 5, K or L as the first character), Exporting a single key",
        "why": "the passages describe the forms one key passes through and the operations that move it between them - encode, add the flag, decode back: a life cycle of a value through its representations",
        "data": {
            "states": [
                {"id": "number", "label": "A number of 32 bytes"},
                {"id": "hex", "label": "Hexadecimal: 64 characters"},
                {"id": "wif", "label": "WIF: base58check of 0x80 + key, first character 5"},
                {"id": "wifc", "label": "WIF with the compression flag 01: first character K or L"},
                {"id": "exported", "label": "Exported into another wallet (dumpprivkey, importprivkey)"},
            ],
            "initial": "number",
            "final": ["exported"],
            "transitions": [["number", "hex", "write in base 16"], ["hex", "number", "read as a number"], ["number", "wif", "version 0x80, checksum, base58"], ["number", "wifc", "the same with the compression flag"], ["wif", "number", "base58check back to bytes, checksum verified"], ["wifc", "number", "base58check back to bytes, without the flag"], ["wif", "exported", "imported into another wallet"], ["wifc", "exported", "imported into another wallet"]],
        },
    },
    {
        "id": "SigningAndChecking",
        "pattern": "Interaction",
        "title": "Proof of control by a key: who signs, who checks",
        "concepts": ["Semantics", "Identifiers", "KeyControlProof", "DigitalSignature", "HardwareSigningDevice"],
        "also_from": ["PrivateKey", "PublicKey", "InputScript", "OutputScript", "StackExecution", "DecentralizedIdentifier"],
        "read_from": "chapter 4: Proof of control by a key (a signature only the holder of the private key can produce, which anyone with the public key and the transaction can verify, with no registry), Digital signature, Hardware signing device (holds the keys and only signs; a less secure program prepares the transaction and broadcasts it), Input script and Output script (the full nodes run them)",
        "why": "the passages describe an exchange between the wallet software, the device that holds the key, and the full nodes that check the result, in a fixed order - prepare, sign, return, verify: an interaction",
        "data": {
            "participants": [{"id": "wallet", "label": "Wallet software (less secure)"}, {"id": "device", "label": "Hardware signing device"}, {"id": "nodes", "label": "Full nodes"}],
            "messages": [
                ["wallet", "wallet", "prepare the transaction that spends Bob's output"],
                ["wallet", "device", "the transaction and the key tweaks to use"],
                ["device", "device", "derive the child private key; sign with it; the key never leaves"],
                ["device", "wallet", "the signed transaction", "reply"],
                ["wallet", "nodes", "broadcast the transaction: input script = signature + public key"],
                ["nodes", "nodes", "run the input script and the output script on the stack"],
                ["nodes", "nodes", "OP_CHECKSIG verifies the signature with the public key"],
                ["nodes", "wallet", "valid: relayed and eligible for a block", "reply"],
            ],
        },
    },
    {
        "id": "WhoUsesAddresses",
        "pattern": "SetOfUses",
        "title": "Who handles keys and addresses, and for what",
        "concepts": ["Practice", "Modern", "DefaultAddressType", "PassphraseProtection", "DeterministicWallet", "AddressReuse", "VanityAddress", "PaperWallet", "Assurance", "TestVectors", "IndependentCheck"],
        "also_from": ["HardwareSigningDevice", "KeyExport", "Bech32Address", "KeyControlProof"],
        "read_from": "chapter 4, the Practice branch: Default address type (what a wallet gives out), Exporting a single key, Passphrase-protected key, Deterministic wallet and seed, Address reuse and privacy (a new address per payment), Vanity address, Paper wallet (obsolete and dangerous), BIP350 test vectors and Cross-checking with independent software",
        "why": "the branch tells what different people do with keys and addresses today - a user receiving, a developer checking an implementation, a device signing - a set of uses by actors",
        "data": {
            "system": "KEYS AND ADDRESSES IN PRACTICE",
            "actors": [{"id": "user", "label": "Wallet user (Bob)"}, {"id": "developer", "label": "Developer"}, {"id": "device", "label": "Hardware signing device"}, {"id": "payer", "label": "Payer (Alice)"}],
            "usecases": [
                {"id": "newaddr", "label": "Get a new address for each payment: bech32 by default"},
                {"id": "export", "label": "Export a single key in wallet import format"},
                {"id": "passphrase", "label": "Protect a key with a passphrase"},
                {"id": "seed", "label": "Restore every key from one seed"},
                {"id": "vanity", "label": "Search for a vanity address"},
                {"id": "vectors", "label": "Check an implementation against the BIP350 test vectors"},
                {"id": "crosscheck", "label": "Cross-check results with independent software"},
                {"id": "sign", "label": "Sign a transaction without exposing the key"},
                {"id": "pay", "label": "Pay to the address given, whatever its kind"},
            ],
            "links": [["user", "newaddr"], ["user", "export"], ["user", "passphrase"], ["user", "seed"], ["user", "vanity"], ["developer", "vectors"], ["developer", "crosscheck"], ["device", "sign"], ["payer", "pay"]],
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
