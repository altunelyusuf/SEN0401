#!/usr/bin/env python3
"""SEN0401 chapter 5 - the narrative diagrams of the chapter (version 1.0.0).

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
        "id": "Bip39NineSteps",
        "pattern": "Workflow",
        "title": "The nine steps of BIP39: from entropy to the root seed",
        "concepts": ["Bip39Stack", "CodeGeneration", "Entropy", "Bip39Checksum", "WordList", "BitSegment", "SeedDerivation", "Pbkdf2", "RootSeed", "Bip39Passphrase"],
        "also_from": ["Bip39Code", "CodeLength", "KeyStretchingFunction", "Salt", "TextNormalization"],
        "read_from": "chapter 5, the BIP39 stack: Generating a recovery code (steps one to six: 128 to 256 bits of entropy, the SHA-256 checksum of entropy-length over 32 bits appended, split into 11-bit segments, each mapped to one of 2,048 words) and From the code to the seed (steps seven to nine: PBKDF2 with the words as the password, the salt mnemonic plus the optional passphrase, 2,048 rounds of HMAC-SHA512, a 512-bit root seed)",
        "why": "the chapter states the standard as a numbered list of steps with one choice in it, the optional passphrase - a workflow",
        "data": {
            "nodes": [
                {"id": "entropy", "label": "Create a random sequence of 128 to 256 bits: the entropy"},
                {"id": "checksum", "label": "Checksum: the first entropy-length / 32 bits of its SHA-256 hash"},
                {"id": "append", "label": "Add the checksum to the end of the random sequence"},
                {"id": "split", "label": "Split the result into segments 11 bits long"},
                {"id": "words", "label": "Map each 11-bit value to a word from the list of 2,048 words"},
                {"id": "code", "label": "The recovery code: 12 to 24 words"},
                {"id": "pass", "label": "Is an optional passphrase used?", "kind": "decision"},
                {"id": "salt1", "label": "Salt = the constant mnemonic + the passphrase"},
                {"id": "salt0", "label": "Salt = the constant mnemonic"},
                {"id": "pbkdf2", "label": "PBKDF2: 2,048 rounds of HMAC-SHA512 over the words and the salt"},
                {"id": "seed", "label": "The 512-bit root seed of the wallet"},
            ],
            "flows": [["start", "entropy"], ["entropy", "checksum"], ["checksum", "append"], ["append", "split"], ["split", "words"], ["words", "code"], ["code", "pass"], ["pass", "salt1", "yes"], ["pass", "salt0", "no"], ["salt1", "pbkdf2"], ["salt0", "pbkdf2"], ["pbkdf2", "seed"], ["seed", "end"]],
        },
    },
    {
        "id": "RecoveryCodeChoices",
        "pattern": "TopicAndParts",
        "title": "Choosing a recovery code: the schemes and the choices behind them",
        "concepts": ["RecoveryCodes", "CodeSchemes", "CodeTradeoffs", "Bip39Code", "ElectrumV2Code", "AezeedCode", "MuunCode", "Slip39Code", "Codex32Code", "RecoveryPassphrase", "WalletBirthday"],
        "also_from": ["PlausibleDeniability", "Brainwallet", "Memorization", "PhysicalCoercion", "WrittenBackup"],
        "read_from": "chapter 5, the Recovery codes branch: the five schemes in wide use (BIP39, Electrum version 2, Aezeed, Muun, SLIP39) and the codex32 proposal, and the choices a scheme does not settle - passphrase, plausible deniability, brainwallet, memorising, coercion, wallet birthday",
        "why": "the branch lays out one subject, the recovery code, by its schemes and by the decisions behind any of them - a topic and its parts",
        "data": {
            "root": "A recovery code",
            "branches": [
                {"label": "Word schemes", "children": ["BIP39: 12 to 24 words, 2,048-word list, SHA-256 checksum", "Electrum version 2: a version number inside the words", "Aezeed: a wallet birthday and a version inside the code", "SLIP39: shares of a secret, any threshold of them recovers"]},
                {"label": "Other schemes", "children": ["Muun: a string of letters and digits, with an emergency kit", "codex32: letters and digits, checkable by hand"]},
                {"label": "Choices a scheme leaves open", "children": ["An optional passphrase: an extra secret, another seed", "Plausible deniability: a feature or a trap", "A brainwallet is not a recovery code", "Memorising a code, or writing it down", "Coercion and physical risk", "A wallet birthday to shorten a rescan"]},
            ],
        },
    },
    {
        "id": "HdTreeDerivation",
        "pattern": "Workflow",
        "title": "From the root seed to one address: deriving down the BIP44 tree",
        "concepts": ["HdWallet", "MasterKeys", "HmacSha512", "MasterPrivateKey", "MasterChainCode", "ChildDerivation", "ChildKeyDerivation", "HardenedDerivation", "PublicChildDerivation", "TreeNavigation", "KeyPath", "Bip44Structure", "AccountBranch", "ChangeBranch", "AddressIndex"],
        "also_from": ["RootSeed", "ChainCode", "IndexNumber", "ExtendedPublicKey", "Bip43Purpose", "PrivateChildDerivation"],
        "read_from": "chapter 5: Master keys from the seed (HMAC-SHA512 over the root seed gives the master private key and the master chain code; the master public key by elliptic curve multiplication), Child key derivation (parent key, chain code and index hashed with HMAC-SHA512 and split in two halves), Hardened derivation (the parent private key enters the hash), Public child derivation (from the parent public key alone), BIP44 structure (purpose 44', coin type, account, change, address index)",
        "why": "the passages describe one procedure applied level by level, with a choice at each level - hardened or normal derivation - from the seed to the key an address is made from: a workflow",
        "data": {
            "nodes": [
                {"id": "seed", "label": "The root seed"},
                {"id": "hmac", "label": "HMAC-SHA512 over the seed: master private key m and master chain code"},
                {"id": "level", "label": "Next level of the path m / 44' / 0' / account' / change / index"},
                {"id": "hard", "label": "Hardened level (with a prime)?", "kind": "decision"},
                {"id": "dhard", "label": "Hash the parent private key, chain code and index"},
                {"id": "dnorm", "label": "Hash the parent public key, chain code and index"},
                {"id": "split", "label": "Split the 512-bit hash: the child key and the child chain code"},
                {"id": "more", "label": "More levels in the path?", "kind": "decision"},
                {"id": "key", "label": "The child key at the address index: its public key makes the address"},
            ],
            "flows": [["start", "seed"], ["seed", "hmac"], ["hmac", "level"], ["level", "hard"], ["hard", "dhard", "yes"], ["hard", "dnorm", "no"], ["dhard", "split"], ["dnorm", "split"], ["split", "more"], ["more", "level", "yes"], ["more", "key", "no"], ["key", "end"]],
        },
    },
    {
        "id": "WebStoreDeployment",
        "pattern": "Interaction",
        "title": "Gabriel's web store: an extended public key receives, the private key stays offline",
        "concepts": ["WebStore", "XpubDeployment", "GapLimit", "PaymentProcessor", "ExtendedKeys", "ExtendedPublicKey"],
        "also_from": ["PublicChildDerivation", "OfflineKeys", "ColdStorage", "HardwareSigningDevice", "ExtendedPrivateKey"],
        "read_from": "chapter 5: An extended key on a web store (Gabriel's story), Extended public key deployment (the public half on the web server creates a new address per order and cannot spend), Payment processor (BTCPay Server watches for payments and matches them to orders), Gap limit (how far the wallet keeps looking), Keys kept offline (the extended private key on a hardware device or in cold storage)",
        "why": "the passage is an exchange between the shop's server, its customers, the offline wallet and the network, in an order that matters - deploy, derive, pay, watch, spend: an interaction",
        "data": {
            "participants": [{"id": "offline", "label": "Gabriel's offline wallet (xprv)"}, {"id": "server", "label": "Web store and payment processor (xpub)"}, {"id": "customer", "label": "Customer"}, {"id": "chain", "label": "The blockchain"}],
            "messages": [
                ["offline", "server", "the extended public key of the receiving branch, once"],
                ["customer", "server", "an order"],
                ["server", "server", "public child derivation: a new address for this order"],
                ["server", "customer", "the invoice with the fresh address", "reply"],
                ["customer", "chain", "the payment"],
                ["server", "chain", "watch the addresses up to the gap limit"],
                ["chain", "server", "the payment to the order's address", "reply"],
                ["server", "offline", "nothing: the server holds no private key"],
                ["offline", "chain", "spend the received funds, signed with the private branch"],
            ],
        },
    },
    {
        "id": "BackupLife",
        "pattern": "LifeCycle",
        "title": "The life of a backup, from the wallet's first start to a recovery",
        "concepts": ["PathBackup", "Descriptors", "OutputScriptDescriptor", "WalletNotes", "OtherProtocolData", "OfflineKeys", "WrittenBackup", "RecoveryPractice", "DataLoss", "BackupTesting"],
        "also_from": ["RecoveryCodes", "Bip39Code", "ImplicitPath", "ExplicitPath", "StaticChannelBackup", "EncryptedWalletBackup", "AddressLabel"],
        "read_from": "chapter 5: Backing up derivation paths (a recovery code does not contain the path; implicit and explicit paths, descriptors), Labels and notes, Other data a wallet keeps (static channel backups), Written backup (write the code down), Data loss (perhaps the leading cause of lost bitcoins), Testing a backup (recover before it is needed)",
        "why": "the passages describe the states a backup is in over time and the events that move it - written, completed with paths and labels, tested, used for a recovery, or lost: a life cycle",
        "data": {
            "states": [
                {"id": "code", "label": "Recovery code shown at first start"},
                {"id": "written", "label": "Written down on a physical medium"},
                {"id": "complete", "label": "Complete: with the derivation paths (descriptors), labels and other data"},
                {"id": "tested", "label": "Tested: a recovery performed while optional"},
                {"id": "recovered", "label": "Recovered after data loss: the funds are spendable again"},
                {"id": "lost", "label": "Lost: keys gone, bitcoins unspendable"},
            ],
            "initial": "code",
            "final": ["recovered", "lost"],
            "transitions": [["code", "written", "the user writes it down"], ["code", "lost", "device fails before any backup"], ["written", "complete", "paths, labels and channel backups added"], ["complete", "tested", "a recovery is tried"], ["tested", "recovered", "the device is lost; the backup restores the wallet"], ["written", "lost", "an explicit path was needed and not kept"], ["tested", "complete", "new data added, test again"]],
        },
    },
    {
        "id": "WhoUsesTheWallet",
        "pattern": "SetOfUses",
        "title": "Who works with wallet keys, and for what",
        "concepts": ["WalletKeys", "WalletContents", "WalletDatabase", "PublicKeyOnlyWallet", "ExternalSigning", "KeyGenerationMethods", "IndependentKeyGeneration", "Seed", "DeterministicKeyGeneration", "HdKeyGeneration"],
        "also_from": ["XpubDeployment", "HardwareSigningDevice", "KeyTweak", "ColdStorage"],
        "read_from": "chapter 5, the Wallet keys branch: Wallet contents (a wallet database holds keys, not bitcoins), Wallet with public keys only, External signing, Key generation methods (independent, deterministic from a seed, hierarchical deterministic), Seed, Key tweak",
        "why": "the branch tells what the different programs and people do with a wallet's keys - generate, hold, derive, sign, watch - a set of uses by actors",
        "data": {
            "system": "A WALLET DATABASE",
            "actors": [{"id": "user", "label": "Wallet user"}, {"id": "app", "label": "Wallet application"}, {"id": "signer", "label": "External signer"}, {"id": "watcher", "label": "Public-key-only wallet"}],
            "usecases": [
                {"id": "backup", "label": "Write down the seed as a recovery code"},
                {"id": "restore", "label": "Restore every key from the seed"},
                {"id": "independent", "label": "Generate keys independently from random data"},
                {"id": "derive", "label": "Derive a tree of keys from one seed (BIP32)"},
                {"id": "distribute", "label": "Give out a fresh address per payment"},
                {"id": "sign", "label": "Sign with keys kept outside the application"},
                {"id": "watch", "label": "Receive and watch without any private key"},
            ],
            "links": [["user", "backup"], ["user", "restore"], ["app", "independent"], ["app", "derive"], ["app", "distribute"], ["signer", "sign"], ["watcher", "watch"], ["watcher", "distribute"]],
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
