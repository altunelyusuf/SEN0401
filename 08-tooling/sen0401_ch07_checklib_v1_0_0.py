#!/usr/bin/env python3
"""Helpers for the executed claims of the SEN0401 chapter 7 corpus (python standard library only).

Adapted from chapter 6's sen0401_ch06_checklib_v1_0_0.py for this chapter: the evidence folder is 08-tooling/ch07-evidence, and the
readers for what this chapter's evidence holds are added - a raw transaction with the outputs it spends (tx_record, from the two
files of mainnet transactions saved in ch07-evidence), a count of the spending types in the saved block (census) and a reader of
a test-vector file of Bitcoin Core at the pinned commit (core_json). has_book / has_ev / has_core say whether every phrase occurs
(white space collapsed, the book's index markup ((( ... ))) removed) in a chapter of the book (/home/claude/src/bitcoinbook at the
commit the textbook ontology pins, 275c4eb8), in a source saved in ch07-evidence, or in a file of Bitcoin Core at the commit pinned
for this course (05bc2f5). Every saved copy of ch07-evidence was fetched on 2026-10-08 from the URL its evidence script names."""
__version__ = "1.0.0"
import os, re, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = "/home/claude/src/bitcoinbook"
CORE = "/home/claude/src/bitcoin"
COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
EV = os.path.join(HERE, "ch07-evidence")

def _norm(t):
    t = re.sub(r"\(\(\(.*?\)\)\)", "", t, flags=re.S)
    return " ".join(t.split())
def _read(path): return open(path, encoding="utf-8", errors="replace").read()
def book_text(name): return _norm(_read(os.path.join(BOOK, name)))
def ev_text(name): return _norm(_read(os.path.join(EV, name)))
def core_raw(path):
    r = subprocess.run(["git", "-c", "gc.auto=0", "-C", CORE, "show", "%s:%s" % (COMMIT, path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    return r.stdout
def core_text(path): return _norm(core_raw(path))
def _all(t, phrases, where):
    ok = True
    for p in phrases:
        if _norm(p) not in t:
            ok = False
            if os.environ.get("CH7_DEBUG"): print("MISSING in %s: %r" % (where, p))
    return ok
def has_book(name, *phrases): return _all(book_text(name), phrases, name)
def has_ev(name, *phrases): return _all(ev_text(name), phrases, name)
def has_core(path, *phrases): return _all(core_text(path), phrases, path)
def core_json(path): return json.loads(core_raw(path))
def ev_json(name): return json.load(open(os.path.join(EV, name), encoding="utf-8"))
def ev_hex(name): return _read(os.path.join(EV, name)).strip()
def ev_raw(name): return _read(os.path.join(EV, name))
def ev_lines(name): return len(_read(os.path.join(EV, name)).splitlines())
def book_raw(name): return _read(os.path.join(BOOK, name))

def pptx_text(rel):
    """all text of the slides of a .pptx (a zip of XML files), white space collapsed"""
    import zipfile
    z = zipfile.ZipFile(os.path.join(HERE, rel)); parts = []
    for n in sorted(z.namelist()):
        if re.match(r"ppt/slides/slide\d+\.xml$", n): parts += re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8"))
    return _norm(" ".join(parts))
def has_pptx(rel, *phrases): return _all(pptx_text(rel), phrases, rel)

# ---- the real transactions saved in ch07-evidence ----
_CACHE = {}
def _records(name):
    if name not in _CACHE: _CACHE[name] = ev_json(name)["transactions"]
    return _CACHE[name]
def tx_record(txid):
    """(raw transaction as hex, [(amount, scriptPubKey hex) of each spent output]) for a landmark transaction or a transaction of the saved block"""
    for f in ("mainnet_landmarks_v1_0_0.json", "mainnet_block775072_census_v1_0_0.json"):
        for r in _records(f):
            if r["txid"].startswith(txid): return r["hex"], [tuple(s) for s in r["spent"]]
    raise KeyError(txid)
def block_records(): return _records("mainnet_block775072_census_v1_0_0.json")
def census(L):
    """what the inputs of the saved block's transactions spend, counted with the chapter's library L: a dict kind -> count, where kind is the
    template of the spent output, and for P2SH and P2WSH outputs the kind of the script revealed (multisig t-of-k, a nested witness program)"""
    key = ("census", id(L))
    if key in _CACHE: return _CACHE[key]
    out = {}
    for r in block_records():
        tx = L.parse_tx(r["hex"])
        for i in range(len(tx.vin)):
            spk = bytes.fromhex(r["spent"][i][1]); k = L.classify(spk)[0]; w = tx.witness[i]
            if k == "scripthash":
                red = [o[2] for o in L.get_ops(tx.vin[i][2]) if o[2] is not None][-1]
                k = ("p2sh-p2wpkh" if len(red) == 22 and red[0] == 0 else "p2sh-p2wsh" if len(red) == 34 and red[0] == 0 else
                     "p2sh-multisig %d-of-%d" % (red[0] - 80, red[-2] - 80) if red[-1] == 0xae else "p2sh-other")
            elif k == "witness_v0_scripthash":
                k = "p2wsh-multisig %d-of-%d" % (w[-1][0] - 80, w[-1][-2] - 80) if w[-1][-1] == 0xae else "p2wsh-other"
            elif k == "witness_v1_taproot":
                k = "p2tr-keypath" if len(w) == 1 or (len(w) == 2 and w[-1][:1] == b"\x50") else "p2tr-scriptpath"
            out[k] = out.get(k, 0) + 1
    _CACHE[key] = out
    return out

# ---- worked examples that need several library calls: built here so that a check in the corpus stays one readable call ----
def _L():
    import sen0401_ch07_script_lib_v1_0_0 as L
    return L
def secret(i): return 11 + i                         # the demonstration private keys of the chapter: 11, 12, 13, ... (never use such keys)
def pub(i): return _L().pubkey_create(secret(i))
def _put(tx, script_sig, witness=None):
    tx.vin = [(tx.vin[0][0], tx.vin[0][1], script_sig, tx.vin[0][3])] + list(tx.vin[1:])
    if witness is not None: tx.witness = [list(witness)] + list(tx.witness[1:])
    return tx
def counted(fn):
    """run fn() and count the ECDSA verifications the engine performs meanwhile: (result of fn, count)"""
    L = _L(); real = L.ecdsa_verify; n = [0]
    def wrap(*a, **k): n[0] += 1; return real(*a, **k)
    L.ecdsa_verify = wrap
    try: r = fn()
    finally: L.ecdsa_verify = real
    return r, n[0]
def ms_spend(m, n, signers, dummy=b"", flags=None, count=False, wrap=None, locktime=0):
    """a real t-of-k spend: build the output script, sign with the keys numbered in `signers` (in that order), put `dummy` first, and verify.
    wrap=None: bare output; 'p2sh', 'p2wsh' or 'p2sh-p2wsh': the script is the redeem script, the witness script, or the witness script nested in a script hash. Returns 'OK' or the engine's error name"""
    L = _L(); keys = [pub(i) for i in range(n)]; script = L.multisig_script(m, keys)
    flags = L.MAINNET_FLAGS if flags is None else flags
    amount = 100000
    wprog = L.p2wsh_script(L.sha256(script))
    if wrap is None: spk = script
    elif wrap == "p2sh": spk = L.p2sh_script(L.hash160(script))
    elif wrap == "p2sh-p2wsh": spk = L.p2sh_script(L.hash160(wprog))
    else: spk = wprog
    tx, spent = L.credit_and_spend(b"", spk, amount=amount, locktime=locktime)
    ver = "WITNESS_V0" if wrap in ("p2wsh", "p2sh-p2wsh") else "BASE"
    sigs = [L.sign_ecdsa_input(tx, 0, script, secret(i), amount=amount, sigversion=ver) for i in signers]
    if wrap == "p2wsh": _put(tx, b"", [dummy] + sigs + [script])
    elif wrap == "p2sh-p2wsh": _put(tx, L.push_data(wprog), [dummy] + sigs + [script])
    else:
        _put(tx, L.push_data(dummy) + b"".join(L.push_data(s) for s in sigs) + (L.push_data(script) if wrap == "p2sh" else b""))
    go = lambda: L.verify_input(tx, 0, spent, flags)
    return counted(go) if count else go()

def sigops(script, accurate=True):
    """the signature operations of a script as Bitcoin Core's CScript::GetSigOpCount counts them (BIP16 rules 1-3)"""
    L = _L(); n = 0; last = None
    for _, op, data in L.get_ops(script):
        if op in (0xac, 0xad): n += 1
        elif op in (0xae, 0xaf): n += (last - 80) if accurate and last is not None and 81 <= last <= 96 else 20
        last = op
    return n
def p2sh_spend(redeem, pushes=(), script_sig=None, hashed=None, flags=None):
    """spend a P2SH output: its output script commits to `hashed` (default: the redeem script); the input script pushes `pushes` and the
    redeem script, unless script_sig is given. Returns 'OK' or the engine's error name"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    spk = L.p2sh_script(L.hash160(redeem if hashed is None else hashed))
    ss = script_sig if script_sig is not None else b"".join(L.push_data(p) for p in pushes) + L.push_data(redeem)
    tx, spent = L.credit_and_spend(ss, spk)
    return L.verify_input(tx, 0, spent, flags)
def ms_scriptsig(m, n, signers, wrap="p2sh"):
    """the input script (hex) of a real p2sh multisignature spend made by ms_spend's recipe"""
    L = _L(); keys = [pub(i) for i in range(n)]; script = L.multisig_script(m, keys)
    tx, spent = L.credit_and_spend(b"", L.p2sh_script(L.hash160(script)), amount=100000)
    sigs = [L.sign_ecdsa_input(tx, 0, script, secret(i)) for i in signers]
    return (L.push_data(b"") + b"".join(L.push_data(s) for s in sigs) + L.push_data(script)).hex()

def key_spend(script, signer=1, locktime=0, sequence=0xffffffff, version=1, wrap="p2sh", flags=None, tail=(), amount=100000, count=False):
    """spend an output whose script is `script` (wrapped as a script hash, a witness script hash or not at all) with one signature of the demonstration key
    `signer`, then the pushes in `tail` (after the signature), on a transaction with the given lock time, input sequence and version.
    Returns 'OK' or the engine's error name"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    spk = script if wrap is None else L.p2sh_script(L.hash160(script)) if wrap == "p2sh" else L.p2wsh_script(L.sha256(script))
    tx, spent = L.credit_and_spend(b"", spk, amount=amount, locktime=locktime, sequence=sequence, version=version)
    ver = "WITNESS_V0" if wrap == "p2wsh" else "BASE"
    sig = L.sign_ecdsa_input(tx, 0, script, secret(signer), amount=amount, sigversion=ver) if signer is not None else b""
    items = ([sig] if signer is not None else []) + list(tail)
    if wrap == "p2wsh": _put(tx, b"", items + [script])
    else: _put(tx, b"".join(L.push_data(i) for i in items) + (L.push_data(script) if wrap == "p2sh" else b""))
    go = lambda: L.verify_input(tx, 0, spent, flags)
    return counted(go) if count else go()
def is_final(locktime, height, mtp, sequences):
    """Bitcoin Core's IsFinalTx (src/consensus/tx_verify.cpp): may a transaction with this lock time and these input sequences be in a block of this height whose
    predecessor has this median time past?"""
    if locktime == 0: return True
    if locktime < (height if locktime < 500000000 else mtp): return True
    return all(s == 0xffffffff for s in sequences)

def witness_scripts(L):
    """the witness scripts revealed by the inputs of the saved block that spend a witness script hash output, directly or nested in a script hash"""
    out = []
    for r in block_records():
        tx = L.parse_tx(r["hex"])
        for i in range(len(tx.vin)):
            spk = bytes.fromhex(r["spent"][i][1]); k = L.classify(spk)[0]; w = tx.witness[i]
            if k == "witness_v0_scripthash": out.append(w[-1])
            elif k == "scripthash":
                red = [o[2] for o in L.get_ops(tx.vin[i][2]) if o[2] is not None][-1]
                if len(red) == 34 and red[0] == 0: out.append(w[-1])
    return out

# ---- the complex script of the book (Mohammed, three partners and a lawyer) ----
KEYS_MOH = {"M": 0, "S": 1, "Z": 2, "L": 3}                  # demonstration key numbers of Mohammed, Saeed, Zaira and the lawyer
def moh_script(csv30=4320, csv90=12960):
    """the redeem script of the book's listing 'Variable multi-signature with timelock' with 30 and 90 days written as numbers of blocks (4,320 and 12,960)"""
    L = _L(); P_ = L.push_data; N = L.push_int; k = lambda c: P_(pub(KEYS_MOH[c]))
    return (b"\x63" + b"\x63" + N(2) + b"\x67" + N(csv30) + b"\xb2\x75" + k("L") + b"\xad" + N(1) + b"\x68" + k("M") + k("S") + k("Z") + N(3) + b"\xae"
            + b"\x67" + N(csv90) + b"\xb2\x75" + k("L") + b"\xac" + b"\x68")
def moh_spend(path, sequence=0xffffffff, version=2, wrap="p2wsh", signers=None, flags=None, count=False, tx_out=None):
    """spend with path 1 (2-of-3 partners), 2 (lawyer and one partner, after 30 days) or 3 (lawyer alone, after 90 days); signers overrides the default signers"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    script = moh_script(); amount = 100000
    spk = L.p2wsh_script(L.sha256(script)) if wrap == "p2wsh" else L.p2sh_script(L.hash160(script))
    tx, spent = L.credit_and_spend(b"", spk, amount=amount, sequence=sequence, version=version)
    ver = "WITNESS_V0" if wrap == "p2wsh" else "BASE"
    sg = lambda c: L.sign_ecdsa_input(tx, 0, script, secret(KEYS_MOH[c]), amount=amount, sigversion=ver)
    signers = signers or {1: ["M", "Z"], 2: ["S", "L"], 3: ["L"]}[path]
    sel = {1: [b"\x01", b"\x01"], 2: [b"", b"\x01"], 3: [b""]}[path]            # the choices at the IF opcodes, as the book writes them: OP_TRUE OP_TRUE, OP_FALSE OP_TRUE, OP_FALSE
    items = ([b""] if path != 3 else []) + [sg(c) for c in signers] + sel
    if wrap == "p2wsh": _put(tx, b"", items + [script])
    else: _put(tx, b"".join(L.push_data(i) if len(i) != 1 or i[0] > 16 else bytes([81 + i[0] - 1]) if i else b"\x00" for i in items) + L.push_data(script))
    if tx_out is not None: tx_out.append(tx)
    go = lambda: L.verify_input(tx, 0, spent, flags)
    return counted(go) if count else go()

# ---- Miniscript: the translation table of BIP379 for a few fragments, as nested tuples ----
def ms_compile(m):
    """the Bitcoin Script (bytes) of a miniscript given as nested tuples, by the rules of the translation table of BIP379: ('pk', 'A'), ('older', n), ('after', n),
    ('v', X), ('and_v', X, Y), ('or_i', X, Z), ('multi', k, 'A', 'B', ...); a key letter is a key of moh_script's KEYS_MOH"""
    L = _L(); P_ = L.push_data; N = L.push_int; k = m[0]
    if k == "pk": return P_(pub(KEYS_MOH[m[1]])) + b"\xac"
    if k == "older": return N(m[1]) + b"\xb2"
    if k == "after": return N(m[1]) + b"\xb1"
    if k == "v":
        s = ms_compile(m[1]); ver = {0xac: 0xad, 0x87: 0x88, 0xae: 0xaf, 0x9c: 0x9d}.get(s[-1])
        return s[:-1] + bytes([ver]) if ver else s + b"\x69"
    if k == "and_v": return ms_compile(m[1]) + ms_compile(m[2])
    if k == "or_i": return b"\x63" + ms_compile(m[1]) + b"\x67" + ms_compile(m[2]) + b"\x68"
    if k == "multi": return N(m[1]) + b"".join(P_(pub(KEYS_MOH[c])) for c in m[2:]) + N(len(m) - 2) + b"\xae"
    raise ValueError(k)

def wsh_run(script, items, flags=None, **kw):
    """run a witness script hash output: the witness holds `items` and then the script; returns 'OK' or the engine's error name"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    tx, spent = L.credit_and_spend(b"", L.p2wsh_script(L.sha256(script)), witness=list(items) + [script], **kw)
    return L.verify_input(tx, 0, spent, flags)

def wpkh_spend(signer=1, nested=False, amount=100000, signed_amount=None, compressed=True, flags=None, witness=None, script_sig=None, program=None, prefix=None):
    """spend a P2WPKH output (native, or nested in a script hash when nested=True) of the demonstration key `signer`; signed_amount is the value the signature
    commits to (default: the real amount); witness / script_sig / program / prefix override the honest values. Returns 'OK' or the engine's error name"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    pk = L.pubkey_create(secret(signer), compressed); h = L.hash160(pk) if program is None else program
    wp = (b"\x00" if prefix is None else prefix) + L.push_data(h)
    spk = L.p2sh_script(L.hash160(wp)) if nested else wp
    tx, spent = L.credit_and_spend(b"", spk, amount=amount)
    sig = L.sign_ecdsa_input(tx, 0, L.p2pkh_script(L.hash160(pk)), secret(signer), amount=amount if signed_amount is None else signed_amount, sigversion="WITNESS_V0")
    _put(tx, (L.push_data(wp) if nested else b"") if script_sig is None else script_sig, [sig, pk] if witness is None else witness)
    return L.verify_input(tx, 0, spent, flags)

def addr_ok(addr, hrp="bc"):
    """does the segregated witness address decode (right checksum constant for its version, right program length)? True or False"""
    L = _L()
    try: L.segwit_decode(hrp, addr); return True
    except Exception: return False

def naive_agg_sign(secrets, msg32, nonces=None):
    """a teaching sketch of a scriptless n-of-n signature: the aggregate key is the plain sum of the public keys, each signer adds a partial signature, and the sum is
    an ordinary BIP340 signature under the aggregate key. Returns (x-only aggregate key, 64-byte signature). NOT secure (a rogue signer can choose a key that cancels
    the others; BIP327 adds a coefficient per key and a two-point nonce) and used only to show that the result has the form of a one-signer signature."""
    L = _L(); n = L.N
    ds = list(secrets); P = None
    for d in ds: P = L.point_add(P, L.point_mul(d)) if P else L.point_mul(d)
    if P[1] & 1: ds = [n - d for d in ds]; P = (P[0], L.P - P[1])
    nonces = nonces or [int.from_bytes(L.sha256(b"nonce" + bytes([i]) + msg32), "big") % n for i in range(len(ds))]
    R = None
    for k in nonces: R = L.point_add(R, L.point_mul(k)) if R else L.point_mul(k)
    if R[1] & 1: nonces = [n - k for k in nonces]
    e = int.from_bytes(L.tagged_hash("BIP0340/challenge", R[0].to_bytes(32, "big") + P[0].to_bytes(32, "big") + msg32), "big") % n
    s = sum(k + e * d for k, d in zip(nonces, ds)) % n
    return P[0].to_bytes(32, "big"), R[0].to_bytes(32, "big") + s.to_bytes(32, "big")


# ---- taproot and tapscript helpers (text part I) ----
def xpub(i): return _L().schnorr_pubkey(secret(i))
def tap_tree(scripts, ver=0xc0):
    """a Merkle tree over the leaf scripts built by pairing neighbours level by level: (root, [control-path hashes for each leaf], [leaf hashes])"""
    L = _L(); lh = [L.tap_leaf_hash(ver, s) for s in scripts]
    level = [(h, [i]) for i, h in enumerate(lh)]; proofs = [[] for _ in scripts]
    while len(level) > 1:
        nxt = []
        for k in range(0, len(level) - 1, 2):
            (a, ia), (b, ib) = level[k], level[k + 1]
            for i in ia: proofs[i].append(b)
            for i in ib: proofs[i].append(a)
            nxt.append((L.tap_branch_hash(a, b), ia + ib))
        if len(level) % 2: nxt.append(level[-1])
        level = nxt
    return level[0][0], proofs, lh
def tr_spend(scripts, idx, items, internal=1, flags=None, ver=0xc0, annex=None, sequence=0xffffffff, version=2, locktime=0, amount=100000, tamper=None):
    """a real taproot script path spend of leaf idx; items are the witness items for the leaf script, bottom first: bytes, ('sig', i) for a Schnorr
    signature of key i over the leaf, or ('sig0',) for the empty signature. Returns (result, witness list, weight of the spending transaction)"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    root, proofs, lh = tap_tree(scripts, ver) if scripts else (b"", [[]], [None])
    ip = xpub(internal); par, q = L.taproot_tweak_pubkey(ip, root); spk = L.p2tr_script(q)
    tx, spent = L.credit_and_spend(b"", spk, amount=amount, sequence=sequence, version=version, locktime=locktime)
    ctrl = bytes([ver | par]) + ip + b"".join(proofs[idx])
    if tamper == "ctrl": ctrl = bytes([ver | (par ^ 1)]) + ip + b"".join(proofs[idx])
    def sg(it):
        if isinstance(it, tuple): return b"" if it[0] == "sig0" else L.sign_taproot_input(tx, 0, spent, secret(it[1]), tapleaf_hash=lh[idx])
        return it
    wit = [sg(i) for i in items] + [scripts[idx], ctrl]
    if annex is not None: wit.append(b"\x50" + annex)
    tx.witness = [wit]
    return L.verify_input(tx, 0, spent, flags), wit, tx.weight()
def tr_keypath(secret_i=1, scripts=None, flags=None, amount=100000, hashtype=0, tamper=None, wrap=None):
    """a real taproot key path spend: the signature is made with the internal key tweaked by the tree root. Returns (result, witness, weight)"""
    L = _L(); flags = L.MAINNET_FLAGS if flags is None else flags
    root = tap_tree(scripts)[0] if scripts else b""
    ip = xpub(secret_i - 11) if False else L.schnorr_pubkey(secret_i); par, q = L.taproot_tweak_pubkey(ip, root); spk = L.p2tr_script(q)
    tx, spent = L.credit_and_spend(b"", spk, amount=amount)
    sig = L.sign_taproot_input(tx, 0, spent, secret_i, hashtype=hashtype, merkle_root=root)
    if tamper == "untweaked": sig = L.sign_taproot_input(tx, 0, spent, secret_i, hashtype=hashtype, merkle_root=b"")
    tx.witness = [[sig]]
    return L.verify_input(tx, 0, spent, flags), [sig], tx.weight()
def csa_script(keys, m, ver_push=None):
    """<k1> CHECKSIG <k2> CHECKSIGADD ... <kn> CHECKSIGADD <m> NUMEQUAL, the tapscript form of an m-of-n multisignature (BIP342); keys are demonstration key indexes"""
    L = _L(); s = L.push_data(xpub(keys[0])) + b"\xac"
    for k in keys[1:]: s += L.push_data(xpub(k)) + b"\xba"
    return s + L.push_int(m) + b"\x9c"


def html_text(name):
    """the visible text of a saved web page, tags removed and white space normalised (used for the network alert of July 2015)"""
    import re as _re, html as _html
    t = ev_raw(name); t = _re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=_re.S)
    return _re.sub(r"\s+", " ", _html.unescape(_re.sub(r"<[^>]+>", " ", t)))
