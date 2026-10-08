#!/usr/bin/env python3
"""The arithmetic and the encodings of chapter 6 (Transactions) of Mastering Bitcoin, 3rd edition, written out in the
Python standard library (hashlib, struct) so that every number the course prints is computed rather than quoted and
so that the same functions run in the reader's browser (the page's Pyodide interpreter) and in the chapter builder.

What is here, and which standard each part follows:
  * compactSize integers (the book's own table; BIP144 and BIP37 call the type var_int)            - cs_encode, cs_decode
  * the serialized transaction (BIP144's extended format and the legacy format): parse_tx, serialize (legacy or
    extended), txid, wtxid, weight, vbytes - BIP141's definitions, Base * 3 + Total, vbytes = ceil(weight / 4)
  * the byte order of hashes: internal (as serialized) and display (reversed) - the book's sidebar
  * the sequence field: BIP68's relative timelock (disable flag bit 31, type flag bit 22, 16-bit value, 512-second
    units), BIP125's opt-in replace-by-fee signal (any input below 0xfffffffe)
  * the lock time: the 500,000,000 threshold between a block height and an epoch time (Bitcoin Core's
    LOCKTIME_THRESHOLD), and the median time past of eleven block times (Bitcoin Core's GetMedianTimePast)
  * the amount: satoshis, the consensus maximum of 21 million bitcoins, the dust threshold from Bitcoin Core's
    GetDustThreshold at the default 3,000 sat/kvB (546 satoshis for a P2PKH output, 294 for a P2WPKH output)
  * the coinbase transaction: the null outpoint, the 2-to-100-byte coinbase field, the subsidy schedule
    (50 BTC halved every 210,000 blocks, GetBlockSubsidy), the maturity of 100 blocks
  * the witness: the push encodings of one small number that all solve the same script (the third-party
    malleability of the legacy format), and a demonstration that the txid of a segwit transaction ignores the witness
Every function is pure; nothing here reads a file or the network. Checked by sen0401_ch06_verify_v1_0_0.py against the
chapter's own transaction (its weight, txid and fields as the book and an independent explorer report them) and
against the figures of BIP68, BIP141 and Bitcoin Core's sources."""
__version__ = "1.0.0"
import hashlib, struct

# ---------------------------------------------------------------------------------------------------------------------
# hashes and byte order
# ---------------------------------------------------------------------------------------------------------------------
def sha256(b): return hashlib.sha256(b).digest()
def hash256(b): return sha256(sha256(b))                      # Bitcoin's double SHA-256
def internal_to_display(h): return bytes.fromhex(h)[::-1].hex() if isinstance(h, str) else h[::-1].hex()
display_to_internal = internal_to_display                      # the same reversal in the other direction

# ---------------------------------------------------------------------------------------------------------------------
# compactSize unsigned integers (the book's table: 1, 3, 5 or 9 bytes)
# ---------------------------------------------------------------------------------------------------------------------
def cs_encode(n):
    assert 0 <= n <= 0xffffffffffffffff, "compactSize holds 0 to 2**64 - 1"
    if n <= 252: return bytes([n])
    if n <= 0xffff: return b"\xfd" + struct.pack("<H", n)
    if n <= 0xffffffff: return b"\xfe" + struct.pack("<I", n)
    return b"\xff" + struct.pack("<Q", n)

def cs_decode(b, pos=0):
    """(value, bytes consumed) of the compactSize at b[pos]"""
    first = b[pos]
    if first <= 252: return first, 1
    if first == 0xfd: return struct.unpack_from("<H", b, pos + 1)[0], 3
    if first == 0xfe: return struct.unpack_from("<I", b, pos + 1)[0], 5
    return struct.unpack_from("<Q", b, pos + 1)[0], 9

# ---------------------------------------------------------------------------------------------------------------------
# the serialized transaction
# ---------------------------------------------------------------------------------------------------------------------
def parse_tx(h):
    """A serialized transaction (hex, legacy or extended) as a dictionary of its fields, with the byte position and
    length of every field in `spans`, so that a byte map can be drawn from it."""
    b = bytes.fromhex(h) if isinstance(h, str) else bytes(h)
    p = 0; spans = []
    def take(n, name):
        nonlocal p
        spans.append((name, p, n)); v = b[p:p + n]; p += n; return v
    def take_cs(name):
        nonlocal p
        v, n = cs_decode(b, p); spans.append((name, p, n)); p += n; return v
    tx = {"version": struct.unpack("<i", take(4, "version"))[0], "segwit": False}
    if b[p] == 0x00 and b[p + 1] != 0x00:
        tx["marker"] = take(1, "marker")[0]; tx["flag"] = take(1, "flag")[0]; tx["segwit"] = True
    n_in = take_cs("input count")
    assert n_in >= 1, "a transaction has at least one input"
    tx["inputs"] = []
    for i in range(n_in):
        txid_internal = take(32, "input %d txid" % i)
        vout = struct.unpack("<I", take(4, "input %d output index" % i))[0]
        slen = take_cs("input %d script length" % i)
        script = take(slen, "input %d script" % i)
        seq = struct.unpack("<I", take(4, "input %d sequence" % i))[0]
        tx["inputs"].append({"txid": txid_internal[::-1].hex(), "txid_internal": txid_internal.hex(), "vout": vout, "script": script.hex(), "sequence": seq})
    n_out = take_cs("output count")
    assert n_out >= 1, "a transaction has at least one output"
    tx["outputs"] = []
    for i in range(n_out):
        value = struct.unpack("<q", take(8, "output %d amount" % i))[0]
        slen = take_cs("output %d script length" % i)
        script = take(slen, "output %d script" % i)
        tx["outputs"].append({"value": value, "script": script.hex()})
    tx["witness"] = []
    if tx["segwit"]:
        for i in range(n_in):
            k = take_cs("witness %d count" % i); items = []
            for j in range(k):
                ln = take_cs("witness %d item %d length" % (i, j)); items.append(take(ln, "witness %d item %d" % (i, j)).hex())
            tx["witness"].append(items)
    tx["locktime"] = struct.unpack("<I", take(4, "lock time"))[0]
    assert p == len(b), "%d trailing bytes" % (len(b) - p)
    tx["spans"] = spans; tx["size"] = len(b)
    return tx

def serialize(tx, witness=None):
    """The bytes of a parsed transaction: with the witness structure (extended format, BIP144) when `witness` is True,
    without it (legacy format) when False; the default keeps whatever the transaction has."""
    if witness is None: witness = tx["segwit"] and any(tx["witness"])
    out = struct.pack("<i", tx["version"])
    if witness: out += b"\x00\x01"
    out += cs_encode(len(tx["inputs"]))
    for i in tx["inputs"]:
        s = bytes.fromhex(i["script"])
        out += bytes.fromhex(i["txid"])[::-1] + struct.pack("<I", i["vout"]) + cs_encode(len(s)) + s + struct.pack("<I", i["sequence"])
    out += cs_encode(len(tx["outputs"]))
    for o in tx["outputs"]:
        s = bytes.fromhex(o["script"])
        out += struct.pack("<q", o["value"]) + cs_encode(len(s)) + s
    if witness:
        for items in (tx["witness"] or [[] for _ in tx["inputs"]]):
            out += cs_encode(len(items))
            for it in items:
                d = bytes.fromhex(it); out += cs_encode(len(d)) + d
    out += struct.pack("<I", tx["locktime"])
    return out

def txid(h):
    """The transaction identifier: double SHA-256 of the LEGACY serialization (no marker, flag or witness), shown in
    display order. BIP141: the txid of a segwit transaction is computed without the witness data."""
    return hash256(serialize(parse_tx(h), witness=False))[::-1].hex()

def wtxid(h):
    """The witness transaction identifier: double SHA-256 of the whole extended serialization, display order."""
    tx = parse_tx(h)
    return hash256(serialize(tx, witness=tx["segwit"]))[::-1].hex()

WITNESS_SCALE_FACTOR = 4
def weight(h):
    """BIP141: Base transaction size * 3 + Total transaction size (Bitcoin Core's GetTransactionWeight)."""
    tx = parse_tx(h)
    base = len(serialize(tx, witness=False)); total = len(serialize(tx, witness=tx["segwit"]))
    return base * (WITNESS_SCALE_FACTOR - 1) + total

def vbytes(h): return -(-weight(h) // WITNESS_SCALE_FACTOR)   # rounded up, BIP141

def field_weights(h):
    """The weight of every top-level field of a transaction, from its byte spans: a factor of 4 for the fields that
    legacy nodes see, 1 for the marker, the flag and the witness structure (BIP141's table as the book prints it)."""
    tx = parse_tx(h); rows = []
    for name, pos, n in tx["spans"]:
        factor = 1 if name in ("marker", "flag") or name.startswith("witness") else 4
        rows.append((name, n, factor, n * factor))
    return rows

# ---------------------------------------------------------------------------------------------------------------------
# the sequence field: BIP68 and BIP125
# ---------------------------------------------------------------------------------------------------------------------
SEQUENCE_FINAL = 0xffffffff
SEQUENCE_LOCKTIME_DISABLE_FLAG = 1 << 31
SEQUENCE_LOCKTIME_TYPE_FLAG = 1 << 22
SEQUENCE_LOCKTIME_MASK = 0x0000ffff
SEQUENCE_LOCKTIME_GRANULARITY = 9              # 2 ** 9 = 512 seconds
MAX_BIP125_RBF_SEQUENCE = 0xfffffffd           # BIP125: a sequence below 0xfffffffe signals replaceability

def sequence_decode(seq, version=2):
    """What a sequence value means, by BIP68 (for version 2 or higher) and BIP125."""
    out = {"value": seq, "hex": "0x%08x" % seq, "rbf_signal": seq <= MAX_BIP125_RBF_SEQUENCE, "final": seq == SEQUENCE_FINAL}
    if version < 2 or seq & SEQUENCE_LOCKTIME_DISABLE_FLAG:
        out["relative_timelock"] = None
    elif seq & SEQUENCE_LOCKTIME_TYPE_FLAG:
        out["relative_timelock"] = ("seconds", (seq & SEQUENCE_LOCKTIME_MASK) << SEQUENCE_LOCKTIME_GRANULARITY)
    else:
        out["relative_timelock"] = ("blocks", seq & SEQUENCE_LOCKTIME_MASK)
    return out

def sequence_for(blocks=None, seconds=None):
    """The sequence value that encodes a relative timelock of so many blocks, or of so many seconds (rounded up to
    the next multiple of 512)."""
    if blocks is not None:
        assert 0 <= blocks <= SEQUENCE_LOCKTIME_MASK, "at most 65535 blocks"; return blocks
    units = -(-seconds // 512)
    assert 0 <= units <= SEQUENCE_LOCKTIME_MASK, "at most 65535 units of 512 seconds"
    return SEQUENCE_LOCKTIME_TYPE_FLAG | units

def earliest_block(spent_height, seq):
    """The lowest height at which an input with this sequence may be confirmed, when the output it spends was
    confirmed at spent_height (Bitcoin Core's CalculateSequenceLocks: nCoinHeight + value - 1 is the last forbidden)."""
    d = sequence_decode(seq)
    if not d["relative_timelock"] or d["relative_timelock"][0] != "blocks": return spent_height + 1
    return spent_height + d["relative_timelock"][1]

# ---------------------------------------------------------------------------------------------------------------------
# the lock time field and the median time past
# ---------------------------------------------------------------------------------------------------------------------
LOCKTIME_THRESHOLD = 500_000_000

def locktime_decode(lt):
    if lt == 0: return ("any block", 0)
    if lt < LOCKTIME_THRESHOLD: return ("block height", lt)
    return ("epoch time", lt)

def locktime_satisfied(lt, height, mtp, sequences):
    """Bitcoin Core's IsFinalTx: a lock time of 0 is final; otherwise it is compared with the block height or with the
    median time past, and it is ignored when every input's sequence is SEQUENCE_FINAL."""
    if lt == 0: return True
    if lt < (height if lt < LOCKTIME_THRESHOLD else mtp): return True
    return all(s == SEQUENCE_FINAL for s in sequences)

def median_time_past(times):
    """The median of the last eleven block times (Bitcoin Core's GetMedianTimePast, nMedianTimeSpan = 11)."""
    last = sorted(times[-11:]); return last[len(last) // 2]

# ---------------------------------------------------------------------------------------------------------------------
# amounts, dust, the coinbase and the subsidy
# ---------------------------------------------------------------------------------------------------------------------
COIN = 100_000_000
MAX_MONEY = 21_000_000 * COIN
DUST_RELAY_TX_FEE = 3000                        # satoshis per kvB, Bitcoin Core's default
SUBSIDY_HALVING_INTERVAL = 210_000
COINBASE_MATURITY = 100

def money_range(v): return 0 <= v <= MAX_MONEY

def dust_threshold(output_script_hex, dust_rate=DUST_RELAY_TX_FEE):
    """Bitcoin Core's GetDustThreshold: the size of the output plus the smallest input that could spend it, at the
    dust relay rate. 148 bytes of input for a legacy output, 67 for a segwit output (32 + 4 + 1 + 4 + 107 / 4)."""
    s = bytes.fromhex(output_script_hex)
    if s[:1] == b"\x6a": return 0                                             # OP_RETURN: unspendable, never dust
    size = 8 + len(cs_encode(len(s))) + len(s)
    is_witness = 2 <= len(s) <= 42 and (s[0] == 0 or 0x51 <= s[0] <= 0x60) and len(s) == s[1] + 2
    size += (32 + 4 + 1 + 4 + (107 // WITNESS_SCALE_FACTOR)) if is_witness else (32 + 4 + 1 + 107 + 4)
    return size * dust_rate // 1000

def block_subsidy(height):
    """Bitcoin Core's GetBlockSubsidy: 50 BTC shifted right once per 210,000 blocks; zero after 64 halvings."""
    halvings = height // SUBSIDY_HALVING_INTERVAL
    if halvings >= 64: return 0
    return (50 * COIN) >> halvings

def total_subsidy():
    """Every satoshi the schedule will ever issue."""
    return sum(block_subsidy(h * SUBSIDY_HALVING_INTERVAL) * SUBSIDY_HALVING_INTERVAL for h in range(64))

def last_subsidy_height():
    """The last height whose subsidy is not zero."""
    h = 0
    while block_subsidy(h) > 0: h += SUBSIDY_HALVING_INTERVAL
    return h - 1

def is_coinbase(tx):
    """One input, with a null txid and the maximal output index (Bitcoin Core's CTransaction::IsCoinBase)."""
    return len(tx["inputs"]) == 1 and tx["inputs"][0]["txid"] == "00" * 32 and tx["inputs"][0]["vout"] == 0xffffffff

def coinbase_field_ok(script_hex): return 2 <= len(bytes.fromhex(script_hex)) <= 100   # bad-cb-length otherwise

def coinbase_mature(coinbase_height, spend_height): return spend_height - coinbase_height >= COINBASE_MATURITY

# ---------------------------------------------------------------------------------------------------------------------
# the witness and the malleability of the legacy format
# ---------------------------------------------------------------------------------------------------------------------
def push_encodings(n):
    """Several input scripts that each put the small number n on the stack: OP_n, a one-byte push, a two-byte push,
    OP_PUSHDATA1 - the book's list. Every one is a different byte string, hence a different legacy txid."""
    assert 1 <= n <= 16
    return {"OP_%d" % n: bytes([0x50 + n]).hex(),
            "OP_PUSH1 0x%02x" % n: bytes([0x01, n]).hex(),
            "OP_PUSH2 0x%04x" % n: bytes([0x02, n, 0x00]).hex(),
            "OP_PUSHDATA1 0x01%02x" % n: bytes([0x4c, 0x01, n]).hex()}

def with_input_script(h, script_hex, index=0):
    """The same transaction with the input script of one input replaced (legacy serialization)."""
    tx = parse_tx(h); tx["inputs"][index]["script"] = script_hex
    return serialize(tx, witness=False).hex()

def with_witness_item(h, item_hex, index=0, item=0):
    """The same segwit transaction with one witness item replaced."""
    tx = parse_tx(h); tx["witness"][index][item] = item_hex
    return serialize(tx, witness=True).hex()

def segwit_output_version(output_script_hex):
    """BIP141: an output script of one number 0 to 16 followed by a push of 2 to 40 bytes is a witness program;
    returns (version, program) or None."""
    s = bytes.fromhex(output_script_hex)
    if not (4 <= len(s) <= 42): return None
    v = 0 if s[0] == 0 else (s[0] - 0x50 if 0x51 <= s[0] <= 0x60 else None)
    if v is None or s[1] != len(s) - 2 or not (2 <= s[1] <= 40): return None
    return v, s[2:].hex()
