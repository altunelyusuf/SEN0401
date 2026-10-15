#!/usr/bin/env python3
"""Fetches every source of sen0401_ch09_sources_v1_0_0.py into ch09-evidence (curl through the sandbox proxy), converts PDFs to text (pdftotext) and
HTML to text, fetches the block census (the first 600 non-coinbase-inclusive transactions of block 840,000 and of the current tip block, from mempool.space)
and writes ch09-evidence/sources_index_v1_0_0.json: per source the URL, HTTP status, bytes, sha256 and the day fetched. Run with python 3.14 or any python 3.
Usage: sen0401_ch09_fetch_v1_0_0.py [--only P01,P02]"""
__version__ = "1.0.0"
import hashlib, html, json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch09_sources_v1_0_0 as SR
EV = os.path.join(HERE, "ch09-evidence"); os.makedirs(EV, exist_ok=True)
IDX = os.path.join(EV, "sources_index_v1_0_0.json")
idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None


def get(url, path, retries=3):
    for k in range(retries):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "120", "-A", "sen0401-research/1.0", "-o", path, "-w", "%{http_code}", url], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip() == "200":
            return 200
        time.sleep(2 * (k + 1))
    return int(r.stdout.strip() or 0) if r.stdout.strip().isdigit() else 0


def totext(path):
    if path.endswith(".pdf"):
        subprocess.run(["pdftotext", "-layout", path, path[:-4] + ".txt"], check=True)
    elif path.endswith(".html"):
        t = open(path, errors="replace").read()
        t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", t)
        t = re.sub(r"(?s)<[^>]+>", " ", t)
        open(path[:-5] + ".txt", "w").write(html.unescape(t))


for sid, ay, label, url, fn, role in SR.S:
    if only and sid not in only:
        continue
    p = os.path.join(EV, fn)
    code = get(url, p)
    if code != 200:
        print("FAILED", sid, url, code); idx[sid] = {"url": url, "http": code}; continue
    totext(p)
    b = open(p, "rb").read()
    idx[sid] = {"url": url, "file": fn, "http": 200, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "fetched": time.strftime("%Y-%m-%d", time.gmtime())}
    print("ok", sid, fn, len(b))
json.dump(idx, open(IDX, "w"), indent=1, sort_keys=True)

# block census: transactions of two mainnet blocks with the fields the chapter's claims need
if not only or "census" in only:
    def api(path):
        out = subprocess.run(["curl", "-sS", "-L", "-m", "60", "https://mempool.space/api" + path], capture_output=True, text=True).stdout
        return json.loads(out)
    tip_h = int(subprocess.run(["curl", "-sS", "-m", "30", "https://mempool.space/api/blocks/tip/height"], capture_output=True, text=True).stdout)
    out = {"fetched": time.strftime("%Y-%m-%d", time.gmtime()), "blocks": {}}
    for h in (840000, tip_h - 3):
        bh = subprocess.run(["curl", "-sS", "-m", "30", "https://mempool.space/api/block-height/%d" % h], capture_output=True, text=True).stdout.strip()
        blk = api("/v1/block/" + bh)
        txs = []
        for off in range(0, 600, 25):
            for attempt in range(4):
                try:
                    page = api("/block/%s/txs/%d" % (bh, off)); break
                except Exception:
                    time.sleep(3)
            txs += [{"txid": t["txid"], "version": t["version"], "locktime": t["locktime"], "size": t["size"], "weight": t["weight"], "fee": t["fee"],
                     "vin": [{"sequence": v["sequence"], "coinbase": v.get("is_coinbase", False)} for v in t["vin"]], "n_out": len(t["vout"])} for t in page]
            time.sleep(0.4)
        out["blocks"][str(h)] = {"hash": bh, "height": h, "timestamp": blk["timestamp"], "tx_count": blk["tx_count"], "weight": blk["weight"], "extras": {k: blk["extras"][k] for k in ("totalFees", "reward", "medianFee", "feeRange", "avgFee", "avgFeeRate", "pool") if k in blk["extras"]}, "txs": txs}
        print("census", h, len(txs))
    json.dump(out, open(os.path.join(EV, "mainnet_fee_census_v1_0_0.json"), "w"))
