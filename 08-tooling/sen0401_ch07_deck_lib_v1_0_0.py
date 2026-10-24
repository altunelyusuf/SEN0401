#!/usr/bin/env python3
"""sen0401_ch07_deck_lib v1.0.0 - the worked-example helpers of the chapter 7 lecture deck 2.0.0 and of the chapter-code tab of the course page.

A NEW file. It is the part of sen0401_ch07_checklib_v1_0_0.py (which stays unchanged) that builds real, signed spends with the chapter's own script library
(sen0401_ch07_script_lib_v1_0_0.py), copied without the readers of saved evidence files, so that it needs nothing but the Python standard library and runs in the
reader's browser (the page's Pyodide) as it runs in the builder. The demonstration private keys 12, 13, 14, ... are the chapter's (never use such keys).
Use:   import sen0401_ch07_script_lib_v1_0_0 as L ; import sen0401_ch07_deck_lib_v1_0_0 as K
"""
__version__ = "1.0.0"


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




# ---- the names that the deck's code slides use without defining them (the same as the PRELUDE of ch07-deck/examples_v1_0_0.py, written here without the checklib readers) ----
import hashlib
import sen0401_ch07_script_lib_v1_0_0 as L


def p2pkh(signer=1, flags=None, loose=False, amount_after=None):
    """one pay-to-public-key-hash spend of the chapter's coin, verified: 'OK' or the engine's error name. signer=2 signs with the wrong key; loose=True pads the DER signature; amount_after changes the output amount after signing"""
    pk = L.pubkey_create(secret(1)); spk = L.p2pkh_script(L.hash160(pk))
    tx, spent = L.credit_and_spend(b'', spk, amount=100000)
    sig = L.sign_ecdsa_input(tx, 0, spk, secret(signer))
    if loose:
        r, s = L.der_parse_lax(sig[:-1])[:2]
        rb = r.to_bytes(32, 'big'); sb = s.to_bytes(32, 'big')
        rb = (b'\x00' + rb) if rb[0] < 0x80 else rb
        rb = b'\x00' + rb
        sb = (b'\x00' + sb) if sb[0] >= 0x80 else sb
        body = b'\x02' + bytes([len(rb)]) + rb + b'\x02' + bytes([len(sb)]) + sb
        sig = b'\x30' + bytes([len(body)]) + body + sig[-1:]
    tx.vin[0] = (tx.vin[0][0], tx.vin[0][1], L.push_data(sig) + L.push_data(pk), tx.vin[0][3])
    if amount_after is not None:
        tx.vout[0] = (amount_after, b'')
    return L.verify_input(tx, 0, spent, L.MAINNET_FLAGS if flags is None else flags)


def old_joined(sig_asm, lock_asm):
    """the first software's way: both scripts joined into one program, which ends at the first OP_RETURN"""
    words = (sig_asm + ' ' + lock_asm).split()
    if 'OP_RETURN' in words:
        words = words[:words.index('OP_RETURN')]
    return L.run(' '.join(words), '', flags=())


LOCK = 'OP_SHA256 0x20' + hashlib.sha256(b'secret').hexdigest() + ' OP_EQUAL'
CLTV = L.push_int(800000) + b'\xb1\x75' + L.push_data(pub(1)) + b'\xac'
CSV = L.push_int(4320) + b'\xb2\x75' + L.push_data(pub(1)) + b'\xac'
RED = L.multisig_script(2, [pub(i) for i in range(3)])
MOH_LEAVES = [csa_script([0, 1, 2], 2),
              L.push_int(4320) + b'\xb2\x75' + L.push_data(xpub(3)) + b'\xad' + L.push_data(xpub(0)) + b'\xac' + L.push_data(xpub(1)) + b'\xba' + L.push_data(xpub(2)) + b'\xba' + L.push_int(1) + b'\x9c',
              L.push_int(12960) + b'\xb2\x75' + L.push_data(xpub(3)) + b'\xac']
MOH_ITEMS = [([b'', ('sig', 1), ('sig', 0)], 0xffffffff), ([('sig0',), ('sig', 1), ('sig0',), ('sig', 3)], 4320), ([('sig', 3)], 12960)]


def moh_tap(i):
    return tr_spend(MOH_LEAVES, i, MOH_ITEMS[i][0], sequence=MOH_ITEMS[i][1])


def moh_wsh(path):
    out = []
    moh_spend(path, sequence=[0xffffffff, 4320, 12960][path - 1], tx_out=out)
    return out[0].weight()
