#!/usr/bin/env python3
"""Chapter 3, version 1.1.0 of the evidence: one more block of public data that the book's examples refer to (block 1000, whose hash the
book prints for the call getblockhash 1000), taken from the Blockstream Esplora API (a third party's index of the chain, not the reader's own
node). Saves next to this script block_1000_header_v1_1_0.json. Usage: sen0401_ch03_blockdata_v1_1_0.py  (needs outbound HTTPS)"""
__version__ = "1.1.0"
import json, os, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); API = "https://blockstream.info/api"
def text(path):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + path, headers={"User-Agent": "sen0401-course-research"}), timeout=30) as r:
                return r.read().decode()
        except Exception:
            time.sleep(2 + attempt * 2)
    raise SystemExit("failed: " + path)
bh = text("/block-height/1000"); b = json.loads(text("/block/" + bh))
json.dump({"source": API, "read": time.strftime("%Y-%m-%d", time.gmtime()), **b}, open(os.path.join(HERE, "block_1000_header_v1_1_0.json"), "w"), indent=1)
print("block 1000:", bh)
