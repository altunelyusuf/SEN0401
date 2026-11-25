"""sen0401_ch01_lib v1.1.0 - the chapter library of chapter 1 (Introduction), written for the deck 3.6.0 and the chapter-code tab of the course page ("Run slide code").
Plain Python 3, standard library only (hashlib, decimal, urllib.parse), so that the same lines run in the page and in the deck builder. No lambda, no prompt line. Nothing here is random and nothing reads the network,
so every result is the same on every run. The code of the library is the code of the slides: the same file stands in the page's wheel, in the lab folder and beside the deck builder.
Bitcoin Core counterparts (read in Bitcoin Core at commit 079437cca7a8, 19 November 2026; the library is a teaching model and does not run Core):
  COIN, HALVING, subsidy  - src/consensus/amount.h (COIN = 100'000'000), src/kernel/chainparams.cpp (nSubsidyHalvingInterval = 210000), GetBlockSubsidy in src/validation.cpp (50 * COIN, shifted right once per halving);
  COINBASE_HEX, GENESIS_HASH160 - CreateGenesisBlock in src/kernel/chainparams.cpp (the script 486604799, CScriptNum(4), then the text of pszTimestamp; the output script is the public key of the genesis block and OP_CHECKSIG);
  dsha            - CHash256 and Hash() in src/hash.h (SHA-256 applied twice);
  base58          - EncodeBase58 and EncodeBase58Check in src/base58.cpp (the check is the first four bytes of the double SHA-256);
  mine            - a toy: Core's CheckProofOfWork in src/pow.cpp compares the block hash with the target that nBits encodes, not with a count of leading hexadecimal zeros;
  fee (slide 41)  - CheckTxInputs in src/consensus/tx_verify.cpp: the fee is the value in minus the value out, and the rule 'bad-txns-in-belowout' refuses an output sum above the input sum;
  Ledger, chain, verify - teaching models; Core refuses a spent coin with 'bad-txns-inputs-missingorspent' (src/validation.cpp, src/consensus/tx_verify.cpp) and links blocks with hashPrevBlock (src/primitives/block.h);
  parse_uri       - BIP 21 (bitcoin/bips, bip-0021.mediawiki); Core's reader of such links is parseBitcoinURI in src/qt/guiutil.cpp;
  stretch         - BIP 39 (bitcoin/bips, bip-0039.mediawiki): PBKDF2-HMAC-SHA512 with 2048 rounds and the salt 'mnemonic'; Bitcoin Core has no BIP 39 code;
  vwap, PIZZA     - price data is not part of consensus, so Core has no counterpart."""
__version__ = "1.1.0"
import hashlib
from decimal import Decimal
from urllib.parse import urlparse, parse_qs

COIN = 10 ** 8                       # satoshis in one bitcoin
HALVING = 210000                     # blocks between two halvings

# the coinbase script of block 0 (the genesis block): a difficulty push, a number push and a push of the headline text
COINBASE_HEX = ("04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73")
# the 20-byte hash of the public key that block 0 pays to, and the address it gives
GENESIS_HASH160 = "62e907b15cbf27d5425399ebf6f0fb50ebb88f18"
# a payment link in the form of BIP 21 (the address is the one of the proposal text; the amount, label and message are made up for the coffee example)
BIP21_URI = "bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W?amount=0.00015&label=Bob%27s%20Cafe&message=One%20coffee"
# the standard test phrase of BIP 39 (eleven times 'abandon', then 'about')
TEST_PHRASE = " ".join(["abandon"] * 11 + ["about"])
# what 10,000 BTC (the Pizza Day coins) cost per coin at the documented milestones, in US dollars (the last entry fetched on 2026-10-06)
PIZZA = {"2010-05": Decimal("0.0041"), "2011-02": Decimal("1"), "2013-11": Decimal("1000"),
                "2017-12": Decimal("19600"), "2021-11": Decimal("69000"), "2026-10": Decimal("85409")}

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def dsha(b):
    """double SHA-256, the hash Bitcoin uses for blocks and checksums"""
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def subsidy(height):
    """the block subsidy in bitcoin at a block height: 50, halved once per 210,000 blocks"""
    return (50 * COIN >> (height // HALVING)) / COIN


def base58(b):
    """Base58 text of a byte string; leading zero bytes become '1'"""
    n = int.from_bytes(b, "big"); s = ""
    while n:
        n, r = divmod(n, 58); s = B58[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + s


def mine(data, zeros):
    """the smallest nonce whose SHA-256 of data + nonce starts with `zeros` hexadecimal zeros; returns (nonce, digest)"""
    n = 0
    while True:
        d = hashlib.sha256(data + str(n).encode()).hexdigest()
        if d.startswith("0" * zeros):
            return n, d
        n += 1


def vwap(trades):
    """volume-weighted average price of (volume, price) trades"""
    return sum(v * p for v, p in trades) / sum(v for v, p in trades)


def stretch(phrase, rounds):
    """PBKDF2-HMAC-SHA512 of a recovery phrase, as BIP 39 stretches it (salt 'mnemonic'), as hexadecimal"""
    return hashlib.pbkdf2_hmac("sha512", phrase.encode(), b"mnemonic", rounds).hex()


def parse_uri(uri):
    """split a bitcoin: payment link into its address and its named fields"""
    u = urlparse(uri)
    f = {k: v[0] for k, v in parse_qs(u.query).items()}
    return {"address": u.path, **f}


class Ledger:
    """a toy shared ledger that remembers which coins are spent; it has no referee, only a rule"""

    def __init__(self, coins):
        self.owner = dict(coins)
        self.spent = set()

    def pay(self, coin, to):
        if coin in self.spent:
            return "refused: coin %s is already spent" % coin
        self.spent.add(coin)
        self.owner[coin] = to
        return "accepted: coin %s now belongs to %s" % (coin, to)


def chain(items):
    """link items into blocks: each block's hash covers its own text and the hash of the block before"""
    out, prev = [], "0" * 64
    for t in items:
        h = hashlib.sha256((prev + t).encode()).hexdigest()
        out.append({"text": t, "prev": prev, "hash": h}); prev = h
    return out


def verify(blocks):
    """recompute every link from the first block on; return how many blocks in a row still check out"""
    prev = "0" * 64
    for i, b in enumerate(blocks):
        if b["prev"] != prev or hashlib.sha256((b["prev"] + b["text"]).encode()).hexdigest() != b["hash"]:
            return i
        prev = b["hash"]
    return len(blocks)
