#!/usr/bin/env python3
"""Chapter 3: public block data the book's examples refer to, taken from the Blockstream Esplora API (a secondary source:
a third party's index of the chain, not the reader's own node). Saves, next to this script:
  block_123456_header_v1_0_0.json  - the block's header fields and counts as the explorer gives them
  block_775072_outputs_v1_0_0.json - for every transaction of block 775072: txid, output values in satoshis, fee (coinbase has none)
Usage: sen0401_ch03_blockdata_v1_0_0.py   (needs outbound HTTPS; about 80 requests)"""
__version__ = "1.0.0"
import json, os, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); API = "https://blockstream.info/api"
def get(path):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + path, headers={"User-Agent": "sen0401-course-research"}), timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 + attempt * 2)
    raise SystemExit("failed: " + path)
def text(path):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + path, headers={"User-Agent": "sen0401-course-research"}), timeout=30) as r:
                return r.read().decode()
        except Exception:
            time.sleep(2 + attempt * 2)
    raise SystemExit("failed: " + path)
for height, name in ((123456, "block_123456_header"),):
    bh = text("/block-height/%d" % height); b = get("/block/" + bh)
    json.dump({"source": API, "read": time.strftime("%Y-%m-%d", time.gmtime()), **b}, open(os.path.join(HERE, name + "_v1_0_0.json"), "w"), indent=1)
bh = text("/block-height/775072"); b = get("/block/" + bh); txs = []
for start in range(0, b["tx_count"], 25): txs += get("/block/%s/txs/%d" % (bh, start))
out = {"source": API, "read": time.strftime("%Y-%m-%d", time.gmtime()), "height": 775072, "id": bh, "tx_count": b["tx_count"],
       "txs": [{"txid": t["txid"], "out_sat": [o["value"] for o in t["vout"]], "fee_sat": t.get("fee")} for t in txs]}
assert len(out["txs"]) == b["tx_count"]
json.dump(out, open(os.path.join(HERE, "block_775072_outputs_v1_0_0.json"), "w"))
print("block 123456 header and", len(txs), "transactions of block 775072 saved")
