#!/usr/bin/env python3
"""Fetches (from mempool.space, an open-source block explorer) the block at each height where a rule of this chapter first applied on
Bitcoin mainnet - the heights are those of Bitcoin Core's chainparams at commit 05bc2f5 - and saves hash, time and size in
mainnet_activation_blocks_v1_0_0.json. Python standard library only. Version 1.0.0."""
import json, urllib.request, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
HEIGHTS = {"BIP34 (block height in the coinbase)": 227931, "BIP66 (strict DER)": 363725, "BIP65 (CHECKLOCKTIMEVERIFY)": 388381, "CSV (BIP68, BIP112, BIP113)": 419328,
           "Segwit (BIP141, BIP143, BIP147)": 481824, "Taproot (BIP341, BIP342)": 709632}
def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "SEN0401-course/1.0"})
    return urllib.request.urlopen(req, timeout=40).read().decode()
out = {"source": "https://mempool.space/api/", "fetched": "2026-10-08", "blocks": []}
for name, h in HEIGHTS.items():
    bh = get("https://mempool.space/api/block-height/%d" % h).strip()
    b = json.loads(get("https://mempool.space/api/block/" + bh))
    out["blocks"].append({"rule": name, "height": h, "hash": bh, "timestamp": b["timestamp"], "tx_count": b["tx_count"], "size": b["size"], "weight": b["weight"]})
    print(name, h, bh, b["timestamp"])
json.dump(out, open(os.path.join(HERE, "mainnet_activation_blocks_v1_0_0.json"), "w"), indent=1)
