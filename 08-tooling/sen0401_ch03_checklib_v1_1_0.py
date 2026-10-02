#!/usr/bin/env python3
"""Helper functions for the executed claims of sen0401_ch03_corpus_v1_1_0.py (standard library only).
Each function restates an algorithm that was read in Bitcoin Core's source at commit 05bc2f5 (src/primitives/transaction.cpp, src/primitives/block.cpp,
src/consensus/merkle.cpp, src/validation.cpp GetBlockSubsidy, src/rpc/blockchain.cpp GetDifficulty, src/arith_uint256.cpp SetCompact, src/chain.h
GetMedianTimePast, src/policy/policy.cpp GetVirtualTransactionSize) or in the reference code of the Bitcoin Core test framework (test/functional/test_framework/
segwit_addr.py and descriptors.py, MIT licence, copyright Pieter Wuille); none of it is imported from a Bitcoin library."""
__version__ = "1.1.0"
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
EVID = os.path.join(HERE, "ch03-evidence")

def sha256d(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()
def rev_hex(b): return b[::-1].hex()                      # Bitcoin Core prints a 256-bit hash with its bytes reversed (uint256.cpp GetHex)

def read_varint(b, i):
    n = b[i]
    if n < 0xfd: return n, i + 1
    w = {0xfd: 2, 0xfe: 4, 0xff: 8}[n]
    return int.from_bytes(b[i + 1:i + 1 + w], "little"), i + 1 + w

def parse_tx(hexstr):
    """Splits a serialized transaction (BIP144 layout when a marker byte 00 and a flag byte 01 follow the version) into its parts and measures it with and without witness data."""
    b = bytes.fromhex(hexstr); i = 4; version = int.from_bytes(b[:4], "little")
    segwit = b[i] == 0 and b[i + 1] == 1
    if segwit: i += 2
    start_in = i
    n_in, i = read_varint(b, i); ins = []
    for _ in range(n_in):
        txid = b[i:i + 32]; vout = int.from_bytes(b[i + 32:i + 36], "little"); i += 36
        ln, i = read_varint(b, i); script = b[i:i + ln]; i += ln
        seq = int.from_bytes(b[i:i + 4], "little"); i += 4
        ins.append({"txid": rev_hex(txid), "vout": vout, "script_sig": script.hex(), "sequence": seq})
    n_out, i = read_varint(b, i); outs = []
    for _ in range(n_out):
        val = int.from_bytes(b[i:i + 8], "little"); i += 8
        ln, i = read_varint(b, i); outs.append({"value": val, "script_pub_key": b[i:i + ln].hex()}); i += ln
    end_outs = i
    wit = []
    if segwit:
        for _ in range(n_in):
            n_items, i = read_varint(b, i); items = []
            for _ in range(n_items):
                ln, i = read_varint(b, i); items.append(b[i:i + ln].hex()); i += ln
            wit.append(items)
    locktime = int.from_bytes(b[i:i + 4], "little"); assert i + 4 == len(b)
    stripped = b[:4] + b[start_in:end_outs] + b[-4:]
    return {"version": version, "segwit": segwit, "inputs": ins, "outputs": outs, "witness": wit, "locktime": locktime,
            "total_size": len(b), "stripped_size": len(stripped), "stripped": stripped, "raw": b}

def txid(hexstr): return rev_hex(sha256d(parse_tx(hexstr)["stripped"]))
def wtxid(hexstr): return rev_hex(sha256d(bytes.fromhex(hexstr)))
def weight(hexstr):
    t = parse_tx(hexstr); return t["stripped_size"] * 3 + t["total_size"]          # policy.h / validation.h: stripped * (4 - 1) + total
def vsize(hexstr): return (weight(hexstr) + 3) // 4                                 # policy.cpp: (weight + 4 - 1) / 4

def header_bytes(version, prev, merkle, time, bits, nonce):
    return (version.to_bytes(4, "little") + bytes.fromhex(prev)[::-1] + bytes.fromhex(merkle)[::-1] + time.to_bytes(4, "little")
            + bits.to_bytes(4, "little") + nonce.to_bytes(4, "little"))
def block_hash(version, prev, merkle, time, bits, nonce): return rev_hex(sha256d(header_bytes(version, prev, merkle, time, bits, nonce)))

def merkle_root(txids):
    """consensus/merkle.cpp ComputeMerkleRoot: hash the pairs level by level, duplicating the last hash of a level that has an odd count."""
    level = [bytes.fromhex(t)[::-1] for t in txids]
    while len(level) > 1:
        if len(level) & 1: level.append(level[-1])
        level = [sha256d(level[k] + level[k + 1]) for k in range(0, len(level), 2)]
    return rev_hex(level[0])

def bits_to_target(bits):
    """arith_uint256.cpp SetCompact for a positive value."""
    size = bits >> 24; word = bits & 0x007fffff
    return word >> (8 * (3 - size)) if size <= 3 else word << (8 * (size - 3))
def difficulty(bits):
    """rpc/blockchain.cpp GetDifficulty."""
    shift = (bits >> 24) & 0xff; d = float(0x0000ffff) / float(bits & 0x00ffffff)
    while shift < 29: d *= 256.0; shift += 1
    while shift > 29: d /= 256.0; shift -= 1
    return d

def subsidy(height):
    """validation.cpp GetBlockSubsidy with the halving interval 210000 of kernel/chainparams.cpp; amounts in satoshis (COIN = 100000000)."""
    halvings = height // 210000
    return 0 if halvings >= 64 else (50 * 100_000_000) >> halvings

def median(xs):
    xs = sorted(xs); return xs[len(xs) // 2]

# ---- Bech32 / Bech32m (reference code of the Bitcoin Core test framework, segwit_addr.py) ----
_CH = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def _polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]; chk = 1
    for v in values:
        top = chk >> 25; chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5): chk ^= gen[i] if ((top >> i) & 1) else 0
    return chk
def _hrp_expand(hrp): return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
def _convertbits(data, frombits, tobits):
    acc = 0; bits = 0; ret = []; maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value; bits += frombits
        while bits >= tobits: bits -= tobits; ret.append((acc >> bits) & maxv)
    assert bits < frombits and not ((acc << (tobits - bits)) & maxv)
    return ret
def decode_segwit_address(hrp, addr):
    """Returns (witness version, witness program as hex, 'bech32' or 'bech32m')."""
    pos = addr.rfind("1"); data = [_CH.find(x) for x in addr.lower()[pos + 1:]]
    chk = _polymod(_hrp_expand(addr[:pos].lower()) + data)
    kind = {1: "bech32", 0x2bc830a3: "bech32m"}[chk]
    assert addr[:pos].lower() == hrp
    return data[0], bytes(_convertbits(data[1:-6], 5, 8)).hex(), kind

# ---- output descriptor checksum (descriptors.py of the Bitcoin Core test framework, after BIP 380) ----
_IN = "0123456789()[],'/*abcdefgh@:$%{}IJKLMNOPQRSTUVWXYZ&+-.;<=>?!^_|~ijklmnopqrstuvwxyzABCDEFGH`#\"\\ "
_GEN = [0xf5dee51989, 0xa9fdca3312, 0x1bab10e32d, 0x3706b1677a, 0x644d626ffd]
def _dpoly(symbols):
    chk = 1
    for v in symbols:
        top = chk >> 35; chk = (chk & 0x7ffffffff) << 5 ^ v
        for i in range(5): chk ^= _GEN[i] if ((top >> i) & 1) else 0
    return chk
def descriptor_checksum(s):
    groups = []; symbols = []
    for c in s:
        v = _IN.find(c); symbols.append(v & 31); groups.append(v >> 5)
        if len(groups) == 3: symbols.append(groups[0] * 9 + groups[1] * 3 + groups[2]); groups = []
    if len(groups) == 1: symbols.append(groups[0])
    elif len(groups) == 2: symbols.append(groups[0] * 3 + groups[1])
    chk = _dpoly(symbols + [0] * 8) ^ 1
    return "".join(_CH[(chk >> (5 * (7 - i))) & 31] for i in range(8))

def evidence(name): return open(os.path.join(EVID, name)).read()
def evidence_json(name): return json.loads(evidence(name))
