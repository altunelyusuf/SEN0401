#!/usr/bin/env python3
"""Fetch the first transactions of Bitcoin block 775,072 from mempool.space and save them in the compact form the chapter 7
verifier needs (python standard library only; run with network access, the result is already saved beside this file).

Block 775,072 is the block the textbook's chapter 6 follows Alice's transaction into, so it is also the block chapter 7 draws
its real spending examples from. For every transaction the saved record holds the raw serialisation (rebuilt from the explorer's
fields and checked against the explorer's transaction id before it is saved) and, for every input, the output it spends
(amount in satoshis and the locking script), because a Bitcoin script check needs both. Nothing else of the explorer's reply is kept.

    python3 sen0401_ch07_chain_evidence_v1_0_0.py [number of pages of 25 transactions, default 24]
Fetched on 2026-10-08 from https://mempool.space/api/block/<hash>/txs/<start>."""
__version__ = "1.0.0"
import json, os, struct, sys, urllib.request, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
HASH = "000000000000000000027d39da52dd790d98f85895b02e764611cb7acf552e90"
OUT = os.path.join(HERE, "mainnet_block775072_census_v1_0_0.json")

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sen0401-evidence/1.0"}), timeout=60) as r:
        return json.load(r)
def cs(n):
    return bytes([n]) if n < 253 else b"\xfd" + struct.pack("<H", n) if n < 65536 else b"\xfe" + struct.pack("<I", n)
def raw(t):
    segwit = any(v.get("witness") for v in t["vin"])
    b = struct.pack("<i", t["version"]) + (b"\x00\x01" if segwit else b"") + cs(len(t["vin"]))
    for v in t["vin"]:
        b += bytes.fromhex(v["txid"])[::-1] + struct.pack("<I", v["vout"]) + cs(len(v["scriptsig"]) // 2) + bytes.fromhex(v["scriptsig"]) + struct.pack("<I", v["sequence"])
    b += cs(len(t["vout"]))
    for o in t["vout"]:
        s = bytes.fromhex(o["scriptpubkey"]); b += struct.pack("<q", o["value"]) + cs(len(s)) + s
    if segwit:
        for v in t["vin"]:
            w = v.get("witness") or []; b += cs(len(w))
            for x in w: b += cs(len(x) // 2) + bytes.fromhex(x)
    return b + struct.pack("<I", t["locktime"])
def txid(b_hex_noWitness): return hashlib.sha256(hashlib.sha256(b_hex_noWitness).digest()).digest()[::-1].hex()
def strip(t):
    t2 = dict(t); t2["vin"] = [dict(v, witness=[]) for v in t["vin"]]
    return raw(t2)

LANDMARKS = [("f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16", "the first bitcoin payment between people, Satoshi Nakamoto to Hal Finney, block 170, 12 Jan 2009 (a pay-to-public-key spend)"),
             ("a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d", "the 'pizza' payment of 22 May 2010, 10,000 bitcoin for two pizzas (a pay-to-public-key-hash spend)"),
             ("466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177", "Alice's payment to Bob's Cafe from chapter 6, spending a taproot output by the key path")]
OUT2 = os.path.join(HERE, "mainnet_landmarks_v1_0_0.json")

def landmarks():
    rec = []
    for tid, note in LANDMARKS:
        t = get("https://mempool.space/api/tx/" + tid)
        assert txid(strip(t)) == tid, tid
        rec.append({"txid": tid, "note": note, "block_height": t["status"]["block_height"], "block_time": t["status"]["block_time"],
                    "fee": t.get("fee"), "weight": t.get("weight"), "hex": raw(t).hex(),
                    "spent": [[v["prevout"]["value"], v["prevout"]["scriptpubkey"]] for v in t["vin"]]})
    json.dump({"fetched": "2026-10-08", "source": "https://mempool.space/api/tx/<txid>", "transactions": rec}, open(OUT2, "w"), separators=(",", ":"))
    print(len(rec), "landmark transactions saved,", os.path.getsize(OUT2), "bytes")

def main():
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    txs = []
    for p in range(pages):
        txs += get("https://mempool.space/api/block/%s/txs/%d" % (HASH, p * 25))
    rec = []
    for t in txs:
        if t["vin"][0].get("is_coinbase"): continue
        assert txid(strip(t)) == t["txid"], t["txid"]
        rec.append({"txid": t["txid"], "hex": raw(t).hex(),
                    "spent": [[v["prevout"]["value"], v["prevout"]["scriptpubkey"]] for v in t["vin"]]})
    json.dump({"block": HASH, "height": 775072, "fetched": "2026-10-08", "source": "https://mempool.space/api/block/%s/txs/<start>" % HASH,
               "transactions": rec}, open(OUT, "w"), separators=(",", ":"))
    print(len(txs), "transactions read,", len(rec), "saved,", os.path.getsize(OUT), "bytes")
main()
landmarks()
