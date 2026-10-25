"""sen0401_ch02_tx_lib v1.0.0 - the chapter library of the chapter 2 deck (How Bitcoin Works) and of its page tab 'chapter code'.
Standard library only (hashlib, math, struct), so it runs unchanged in the page's Python. Every constant below is read from the chapter research
(sen0401_ch02_research_v1_4_0.ttl and the corpus): Alice's transaction of the book's figures, the chain Tx1 - Tx2 - Tx3 of figure 2-3, the invoice URI,
the genesis block header and the numbers of block 74,638. The deck shows short listings; the helper functions here keep every listing within one line."""
__version__ = "1.0.0"
import hashlib, math, struct

COIN = 100_000_000                       # satoshis in one bitcoin (Bitcoin Core, src/consensus/amount.h)
INVOICE = "bitcoin:bc1qk2g6u8p4qm2s2lh3gts5cpt2mrv5skcuu7u3e4?amount=0.01577764&label=Bob%27s%20Store"
ALICE_IN = [100000]                      # Alice spends Tx1:0 (100,000 satoshis)
ALICE_OUT = [75000, 20000]               # 75,000 to Bob's Store, 20,000 back to herself
PREV_RAW = "eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a"   # the txid as an input stores it (internal byte order)
CHAIN = {                                # the chain of figure 2-3: transaction -> (spent outputs, new outputs with their values in satoshis)
    "Tx1": (["Tx0:0"], {"Tx1:0": 100000, "Tx1:1": 500000}),
    "Tx2": (["Tx1:0"], {"Tx2:0": 20000, "Tx2:1": 75000}),
    "Tx3": (["Tx2:1"], {"Tx3:0": 67000}),
}
FORMS = {                                # three common shapes: name -> (input values, output values), satoshis
    "payment": ([100000], [75000, 20000]),
    "consolidation": ([30000, 25000, 20000], [73500]),
    "batching": ([200000], [60000, 55000, 50000, 32000]),
}
GENESIS = {"version": 1, "merkle": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b", "time": 1231006505, "bits": 0x1d00ffff, "nonce": 2083236893}
HALVING_INTERVAL = 210000                # blocks between two halvings (Bitcoin Core, src/kernel/chainparams.cpp)


def to_sats(btc):
    """'0.01577764' -> 1577764; whole numbers only, no floating point"""
    whole, _, frac = btc.partition(".")
    return int(whole) * COIN + int((frac + "0" * 8)[:8])


def to_btc(sats):
    """1577764 -> '0.01577764'"""
    return "%d.%08d" % divmod(sats, COIN)


def sha(text):
    """sha256 of a text, as 64 hexadecimal characters"""
    return hashlib.sha256(text.encode()).hexdigest()


def select(values, need):
    """the simplest coin selection: take the coins in the order given until they cover the payment; returns (coins taken, change)"""
    taken, total = [], 0
    for v in values:
        taken.append(v); total += v
        if total >= need:
            return taken, total - need
    return None, 0


def genesis_header():
    """the 80 bytes that Bitcoin's first block hashes: version, previous block, merkle root, time, bits, nonce"""
    g = GENESIS
    return (struct.pack("<I", g["version"]) + bytes(32) + bytes.fromhex(g["merkle"])[::-1]
            + struct.pack("<III", g["time"], g["bits"], g["nonce"]))


def block_hash(header):
    """double sha256 of a header, shown the way block explorers show it (bytes reversed)"""
    return hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1].hex()


def catch_up(q, z):
    """Nakamoto's white paper, section 11: the chance that an attacker with the share q of the hash power ever catches up from z blocks behind"""
    p = 1.0 - q
    lam = z * q / p
    s = sum(math.exp(-lam) * lam ** k / math.factorial(k) * (1 - (q / p) ** (z - k)) for k in range(z + 1))
    return 1.0 - s


def wrap64(x):
    """what a signed 64-bit integer holds after x is stored in it (two's complement wrap-around)"""
    return (x + 2 ** 63) % 2 ** 64 - 2 ** 63
