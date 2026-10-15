#!/usr/bin/env python3
"""SEN0401 chapter 11 (The Blockchain): the library the chapter's executed claims call. Standard library only (plus sen0401_ch10_p2p_v1_0_0 for sha256d and the compact size integer).
* text(), has(), const(): read a saved source (08-tooling/ch11-evidence) and test that a passage or a constant is in it (whitespace collapsed).
* run(): the recorded regtest run (sen0401_ch11_regtest_v1_0_0.py, Bitcoin Core 31.1 nodes on private chains); every value read from it is a SINGLE-RUN value.
* the rules of the chapter written as functions: the header of 80 bytes taken apart, the block hash, the compact target, the merkle root and the merkle path, the genesis block built
  from the constants of chainparams.cpp, the signet message start, the odds of the proof sizes.
* quotes_report(), index_report(): the passages used from every source, and the fetch record of every source."""
__version__ = "1.0.0"
import datetime, hashlib, html, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
EV = os.path.join(HERE, "ch11-evidence")
_T = {}
_J = {}


def text(fname):
    """The saved source as one string, whitespace collapsed; html and pdf copies are read through their .txt conversion."""
    if fname not in _T:
        p = os.path.join(EV, fname)
        if fname.endswith(".html") or fname.endswith(".pdf"):
            p = os.path.splitext(p)[0] + ".txt"
        s = open(p, errors="replace").read()
        if fname.endswith(".html"):
            s = html.unescape(s)
        _T[fname] = re.sub(r"\s+", " ", s)
    return _T[fname]


def has(fname, *frags):
    t = text(fname)
    return all(re.sub(r"\s+", " ", f) in t for f in frags)


def const(fname, name):
    """The value of a C++ constant or a markdown definition: `name = ...;` or `name{...}` in a saved source (first match), as written."""
    t = text(fname)
    m = re.search(re.escape(name) + r"\s*(?:\{|=)\s*([^;}\s,]+)", t)
    return m.group(1) if m else None


def jload(name):
    if name not in _J:
        _J[name] = json.load(open(os.path.join(EV, name)))
    return _J[name]


def run():
    return jload("regtest_run_v1_0_0.json")


def raw(fname):
    return open(os.path.join(EV, fname)).read().strip()


# ------------------------------------------------------------------------------------------------ bytes
sha256d = P.sha256d


def rev(h):
    return bytes.fromhex(h)[::-1].hex()


def header(hex80):
    """The 80 bytes of a block header taken apart; hashes and the block hash in the usual (reversed) display order."""
    b = bytes.fromhex(hex80)
    assert len(b) == 80
    return {"version": int.from_bytes(b[0:4], "little"), "prev": b[4:36][::-1].hex(), "merkle": b[36:68][::-1].hex(), "time": int.from_bytes(b[68:72], "little"),
            "bits": b[72:76][::-1].hex(), "nonce": int.from_bytes(b[76:80], "little"), "hash": sha256d(b)[::-1].hex(), "bytes": len(b)}


def block_hash(hex80):
    return header(hex80)["hash"]


def bits_to_target(bits_hex):
    """The compact encoding: one byte of exponent and three of mantissa; target = mantissa * 256 ** (exponent - 3)."""
    n = int(bits_hex, 16)
    return (n & 0x7fffff) * 256 ** ((n >> 24) - 3)


DIFF1 = 0xffff * 256 ** (0x1d - 3)


def difficulty(bits_hex):
    return DIFF1 / bits_to_target(bits_hex)


def leading_zero_hex(h):
    return len(h) - len(h.lstrip("0"))


# ------------------------------------------------------------------------------------------------ merkle trees
def merkle_root(ids):
    """The merkle root of a list of txids (display order): pairs hashed as double SHA-256 of the two 32-byte hashes in internal byte order; an odd last hash is paired with itself."""
    lvl = [bytes.fromhex(i)[::-1] for i in ids]
    while len(lvl) > 1:
        if len(lvl) % 2:
            lvl.append(lvl[-1])
        lvl = [sha256d(lvl[i] + lvl[i + 1]) for i in range(0, len(lvl), 2)]
    return lvl[0][::-1].hex()


def merkle_levels(ids):
    lvl = [bytes.fromhex(i)[::-1] for i in ids]
    out = [lvl]
    while len(lvl) > 1:
        if len(lvl) % 2:
            lvl = lvl + [lvl[-1]]
        lvl = [sha256d(lvl[i] + lvl[i + 1]) for i in range(0, len(lvl), 2)]
        out.append(lvl)
    return out


def merkle_path(ids, idx):
    """The authentication path of leaf idx: the sibling hash at every level, with a flag that says if the sibling is on the right."""
    lv = merkle_levels(ids)
    path, i = [], idx
    for lvl in lv[:-1]:
        l = lvl + [lvl[-1]] if len(lvl) % 2 else lvl
        sib = i ^ 1
        path.append((l[sib][::-1].hex(), sib > i))
        i //= 2
    return path


def follow_path(txid, path, swap=False):
    h = bytes.fromhex(txid)[::-1]
    for sib, right in path:
        s = bytes.fromhex(sib)[::-1]
        r = (not right) if swap else right
        h = sha256d(h + s) if r else sha256d(s + h)
    return h[::-1].hex()


def depth(n):
    return max(0, math.ceil(math.log2(n))) if n > 1 else 0


def compact_size(n):
    return P.cs_enc(n)


# ------------------------------------------------------------------------------------------------ the genesis block, built from the constants of chainparams.cpp
def _push(b):
    n = len(b)
    if n < 0x4c:
        return bytes([n]) + b
    return b"\x4c" + bytes([n]) + b


def genesis(msg, pubkey_hex, t, nonce, bits, version=1, reward=50 * 10 ** 8):
    """CreateGenesisBlock of chainparams.cpp: a coinbase whose scriptSig is the push of 486604799 (0x1d00ffff), the push of the number 4 and the push of the message."""
    ss = _push((486604799).to_bytes(4, "little")) + _push(b"\x04") + _push(msg.encode())
    spk = _push(bytes.fromhex(pubkey_hex)) + b"\xac"
    tx = (1).to_bytes(4, "little") + b"\x01" + bytes(32) + b"\xff\xff\xff\xff" + compact_size(len(ss)) + ss + b"\xff\xff\xff\xff" + b"\x01" + reward.to_bytes(8, "little") + compact_size(len(spk)) + spk + bytes(4)
    txid = sha256d(tx)
    hdr = version.to_bytes(4, "little", signed=True) + bytes(32) + txid + t.to_bytes(4, "little") + bytes.fromhex(bits)[::-1] + nonce.to_bytes(4, "little")
    return {"tx_hex": tx.hex(), "txid": txid[::-1].hex(), "header": hdr.hex(), "hash": sha256d(hdr)[::-1].hex(), "scriptsig": ss.hex(), "tx_bytes": len(tx)}


def chainparams_genesis(chain):
    """Reads the arguments of the CreateGenesisBlock call of one chain from the saved chainparams.cpp and builds the block."""
    t = text("core_src_kernel_chainparams.cpp")
    if chain == "testnet4":
        m = re.search(r'testnet4_genesis_msg = "([^"]+)".*?testnet4_genesis_script = CScript\(\) << "([0-9a-f]+)"_hex.*?CreateGenesisBlock\(testnet4_genesis_msg, testnet4_genesis_script, (\d+), (\d+), (0x[0-9a-f]+), 1', t)
        msg, pk, tm, nonce, bits = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5)
    else:
        msg = re.search(r'pszTimestamp = "([^"]+)"', t).group(1)
        pk = re.search(r'genesisOutputScript = CScript\(\) << "([0-9a-f]+)"_hex', t).group(1)
        key = {"main": "1231006505", "test": "1296688602, 414098458", "signet": "1598918400", "regtest": "1296688602, 2,"}[chain]
        m = re.search(r"genesis = CreateGenesisBlock\(" + re.escape(key) + r"[, ]*(\d*)[, ]*(0x[0-9a-f]+), 1, 50 \* COIN\)", t)
        # the arguments in full
        m2 = re.search(r"genesis = CreateGenesisBlock\((" + re.escape(key) + r"[^)]*)\)", t)
        a = [x.strip() for x in m2.group(1).split(",")]
        tm, nonce, bits = int(a[0]), int(a[1]), a[2]
    g = genesis(msg, pk, tm, nonce, bits[2:] if bits.startswith("0x") else bits)
    g.update({"message": msg, "time": tm, "nonce": nonce, "bits": bits})
    return g


def signet_magic(challenge_hex):
    """Message start of a signet: the first four bytes of the double SHA-256 of the challenge script as a single push (length first)."""
    c = bytes.fromhex(challenge_hex)
    return sha256d(compact_size(len(c)) + c)[:4].hex()


# ------------------------------------------------------------------------------------------------ small rules
def subsidy(height, interval=210000):
    h = height // interval
    return 0 if h >= 64 else (50 * 10 ** 8) >> h


def median_time_past(times):
    t = sorted(times[-11:])
    return t[len(t) // 2]


def tamper_chain(headers_hex, k):
    """Change one bit of the merkle root of header k in a chain of consecutive headers: which previous-hash links now fail, and how many headers would have to be mined again."""
    hs = [bytes.fromhex(h) for h in headers_hex]
    h2 = bytearray(hs[k]); h2[36] ^= 1
    hs2 = list(hs); hs2[k] = bytes(h2)
    broken = [i for i in range(1, len(hs2)) if hs2[i][4:36] != sha256d(hs2[i - 1])]
    return {"broken_links": broken, "must_remine": len(hs) - k, "own_hash_changed": sha256d(hs[k]) != sha256d(hs2[k])}


def work(bits_hex):
    return 2 ** 256 // (bits_to_target(bits_hex) + 1)


# ------------------------------------------------------------------------------------------------ the quotes of the sources
def quotes_report():
    """Every source's used passages re-read from the saved copy: returns (n_sources, n_fragments, failures[(id, fragment)], sources without a quote)."""
    import sen0401_ch11_quotes_v1_0_0 as Q
    import sen0401_ch11_sources_v1_0_0 as S
    files = {r[0]: r[4] for r in S.S}
    bad, n = [], 0
    for sid, frags in Q.QUOTES.items():
        for f in frags:
            n += 1
            if not has(files[sid], f):
                bad.append((sid, f[:70]))
    missing = [sid for sid in files if sid not in Q.QUOTES]
    return len(Q.QUOTES), n, bad, missing


def index_report():
    idx = json.load(open(os.path.join(EV, "sources_index_v1_0_0.json")))
    import sen0401_ch11_sources_v1_0_0 as S
    ok = []
    for sid, r in idx.items():
        if r.get("http") == 200 and r.get("sha256"):
            b = open(os.path.join(EV, r["file"]), "rb").read()
            if hashlib.sha256(b).hexdigest() == r["sha256"]:
                ok.append(sid)
    return len(S.S), len(ok), sorted(set(r[0] for r in S.S) - set(ok))


# ------------------------------------------------------------------------------------------------ chain parameters, scripts, proofs, odds
_CLS = {"main": "CMainParams", "test": "CTestNetParams", "testnet4": "CTestNet4Params", "signet": "SigNetParams", "regtest": "CRegTestParams"}


def chain_section(chain):
    """The text of one chain's class in the saved chainparams.cpp."""
    t = text("core_src_kernel_chainparams.cpp")
    starts = sorted((t.find("class " + c + " "), k) for k, c in _CLS.items())
    for i, (pos, k) in enumerate(starts):
        if k == chain:
            return t[pos:starts[i + 1][0] if i + 1 < len(starts) else len(t)]


def chain_facts(chain):
    s = chain_section(chain)
    g = lambda pat: (re.search(pat, s) or [None, None])[1]
    magic = re.findall(r"pchMessageStart\[\d\] = 0x([0-9a-f]{2});", s)
    return {"port": int(g(r"nDefaultPort = (\d+);")), "seeds": len(re.findall(r"vSeeds\.emplace_back", s)), "p2pkh": int(g(r"base58Prefixes\[PUBKEY_ADDRESS\] = std::vector<unsigned char>\(1,(\d+)\)")),
            "p2sh": int(g(r"base58Prefixes\[SCRIPT_ADDRESS\] = std::vector<unsigned char>\(1,(\d+)\)")), "hrp": g(r'bech32_hrp = "([a-z]+)"'), "magic": "".join(magic) or None,
            "powlimit": g(r'consensus\.powLimit = uint256\{"([0-9a-f]+)"\}'), "min_diff": g(r"fPowAllowMinDifficultyBlocks = (true|false);") == "true", "bip94": g(r"enforce_BIP94 = (true|false|opts\.enforce_bip94);"),
            "halving": int(g(r"nSubsidyHalvingInterval = (\d+);")), "assumed_gb": int(g(r"m_assumed_blockchain_size = (\d+);"))}


def script_ops(hex_script):
    """A short disassembly of a challenge script: pushes as data, OP_n, OP_CHECKMULTISIG."""
    b, i, out = bytes.fromhex(hex_script), 0, []
    names = {0xae: "OP_CHECKMULTISIG", 0xac: "OP_CHECKSIG", 0x00: "OP_0"}
    while i < len(b):
        o = b[i]; i += 1
        if 1 <= o <= 0x4b:
            out.append("PUSH%d" % o); i += o
        elif 0x51 <= o <= 0x60:
            out.append("OP_%d" % (o - 0x50))
        else:
            out.append(names.get(o, hex(o)))
    return out


def bip34_height(script_hex):
    """The height at the start of a coinbase scriptSig: OP_1..OP_16 for 1..16, otherwise a push of the little-endian number."""
    b = bytes.fromhex(script_hex)
    if 0x51 <= b[0] <= 0x60:
        return b[0] - 0x50
    n = b[0]
    return int.from_bytes(b[1:1 + n], "little")


def catchup(q, z):
    """Nakamoto's section 11: the chance that an attacker with the share q of the hash rate ever catches up from z blocks behind (Poisson sum of the paper)."""
    p = 1.0 - q
    lam = z * q / p
    s = 1.0
    for k in range(z + 1):
        poisson = math.exp(-lam) * lam ** k / math.factorial(k)
        s -= poisson * (1 - (q / p) ** (z - k))
    return s


def parse_merkleblock(hex_proof):
    """The pieces of a merkleblock (as gettxoutproof returns it): header, number of transactions, the hashes, the flag bytes."""
    b = bytes.fromhex(hex_proof)
    n = int.from_bytes(b[80:84], "little")
    c, off = b[84], 85
    assert c < 253
    hashes = [b[off + 32 * i:off + 32 * i + 32][::-1].hex() for i in range(c)]
    off += 32 * c
    fl = b[off]
    return {"header": b[:80].hex(), "ntx": n, "hashes": hashes, "flag_bytes": fl, "total": len(b), "flags": b[off + 1:off + 1 + fl].hex()}


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
