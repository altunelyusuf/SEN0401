"""Bitcoin Core's transaction and block-level checks, ported to Python for teaching.

Every function names the Bitcoin Core function it follows and returns the same reject
reason string Core returns (for example "bad-txns-inputs-duplicate"). Source: Bitcoin
Core (MIT licence), src/consensus/tx_check.cpp, src/consensus/tx_verify.cpp,
src/consensus/merkle.cpp, src/consensus/amount.h, src/consensus/consensus.h.
Teaching and testing only: this is not a node and must never guard real funds.
"""
import struct

COIN = 100_000_000                       # src/consensus/amount.h
MAX_MONEY = 21_000_000 * COIN            # src/consensus/amount.h
MAX_BLOCK_WEIGHT = 4_000_000             # src/consensus/consensus.h
WITNESS_SCALE_FACTOR = 4                 # src/consensus/consensus.h
COINBASE_MATURITY = 100                  # src/consensus/consensus.h
NULL_HASH = b"\x00" * 32


def money_range(value):
    """MoneyRange() in src/consensus/amount.h."""
    return 0 <= value <= MAX_MONEY


def is_coinbase(tx):
    """CTransaction::IsCoinBase(): one input whose prevout is null."""
    return len(tx.vin) == 1 and is_null_prevout(tx.vin[0])


def is_null_prevout(txin):
    """COutPoint::IsNull(): hash all zero and index 0xffffffff."""
    return txin[0] == NULL_HASH and (txin[1] & 0xffffffff) == 0xffffffff


def check_transaction(tx):
    """CheckTransaction() in src/consensus/tx_check.cpp. Returns (True, '') or (False, reason)."""
    if not tx.vin:
        return False, "bad-txns-vin-empty"
    if not tx.vout:
        return False, "bad-txns-vout-empty"
    # size limit without the witness (the witness is not yet checked for malleability)
    if len(tx.serialize(witness=False)) * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT:
        return False, "bad-txns-oversize"
    total_out = 0
    for value, _script in tx.vout:       # negative or overflowing outputs, CVE-2010-5139
        if value < 0:
            return False, "bad-txns-vout-negative"
        if value > MAX_MONEY:
            return False, "bad-txns-vout-toolarge"
        total_out += value
        if not money_range(total_out):
            return False, "bad-txns-txouttotal-toolarge"
    seen = set()                         # duplicate inputs, CVE-2018-17144
    for txin in tx.vin:
        outpoint = (txin[0], txin[1] & 0xffffffff)
        if outpoint in seen:
            return False, "bad-txns-inputs-duplicate"
        seen.add(outpoint)
    if is_coinbase(tx):
        if len(tx.vin[0][2]) < 2 or len(tx.vin[0][2]) > 100:
            return False, "bad-cb-length"
    else:
        for txin in tx.vin:
            if is_null_prevout(txin):
                return False, "bad-txns-prevout-null"
    return True, ""


def check_tx_inputs(tx, coins, spend_height):
    """Consensus::CheckTxInputs() in src/consensus/tx_verify.cpp.

    coins maps (txid_internal_bytes, index) to (value, height, is_coinbase), standing in for
    Core's CCoinsViewCache. Returns (True, '', fee) or (False, reason, 0).
    """
    for txin in tx.vin:
        if (txin[0], txin[1]) not in coins:
            return False, "bad-txns-inputs-missingorspent", 0
    value_in = 0
    for txin in tx.vin:
        value, height, coinbase = coins[(txin[0], txin[1])]
        if coinbase and spend_height - height < COINBASE_MATURITY:
            return False, "bad-txns-premature-spend-of-coinbase", 0
        value_in += value
        if not money_range(value) or not money_range(value_in):
            return False, "bad-txns-inputvalues-outofrange", 0
    value_out = sum(v for v, _ in tx.vout)
    if value_in < value_out:
        return False, "bad-txns-in-belowout", 0
    fee = value_in - value_out
    if not money_range(fee):
        return False, "bad-txns-fee-outofrange", 0
    return True, "", fee


def hash256(data):
    import hashlib
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def compute_merkle_root(hashes):
    """ComputeMerkleRoot() in src/consensus/merkle.cpp. Returns (root, mutated).

    mutated is True when two equal hashes are paired, the CVE-2012-2459 signature.
    """
    hashes = list(hashes)
    mutated = False
    while len(hashes) > 1:
        for pos in range(0, len(hashes) - 1, 2):
            if hashes[pos] == hashes[pos + 1]:
                mutated = True
        if len(hashes) & 1:
            hashes.append(hashes[-1])
        hashes = [hash256(hashes[i] + hashes[i + 1]) for i in range(0, len(hashes), 2)]
    return (hashes[0] if hashes else NULL_HASH), mutated


def merkle_path(leaves, position):
    """TransactionMerklePath() / MerkleComputation() in src/consensus/merkle.cpp.

    The sibling hashes from the leaf at `position` up to the root (leaf side first).
    Written level by level; the test compares it with Core's own result.
    """
    path, level = [], list(leaves)
    if not level:
        return path
    index = position
    while len(level) > 1:
        if len(level) & 1:
            level.append(level[-1])
        path.append(level[index ^ 1])
        level = [hash256(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        index >>= 1
    return path


def root_from_branch(leaf, branch, index):
    """ComputeMerkleRootFromBranch() in src/test/merkle_tests.cpp."""
    h = leaf
    for sibling in branch:
        h = hash256(sibling + h) if index & 1 else hash256(h + sibling)
        index >>= 1
    return h
