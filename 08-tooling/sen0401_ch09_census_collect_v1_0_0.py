#!/usr/bin/env python3
"""sen0401_ch09_census_collect v1_0_0 - the course's own census of mainnet blocks for chapter 9 (transaction fees).
What it does, in order:
 1. SAMPLING (fixed, written here, not chosen after looking at the data): the heights in HEIGHTS - ten blocks spread over the chain's history (100,000 to 800,000 in steps of 100,000, the 2024 halving block 840,000 and
    900,000) and a recent window of ten consecutive blocks 971,480-971,489 (the window ends at the block the chapter's examples already used).
 2. For every sampled block, the block facts (hash, height, timestamp, transaction count, size, weight) and the coinbase transaction (the sum of its outputs) are fetched from mempool.space (https://mempool.space/api) AND
    from blockstream.info (https://blockstream.info/api) and compared.
 3. For the two blocks the chapter's examples read (840,000 and 971,489) every transaction is fetched from mempool.space (25 per request); the first 600 are stored in the file as they were fetched (txid, version, lock time,
    size, weight, fee, input sequence numbers, coinbase flag, number of outputs), and the first 600 plus a last page are fetched from blockstream.info too and compared field by field.
 4. The statistics are computed HERE, from the raw facts: total fees = coinbase outputs - subsidy; reward = coinbase outputs; median fee rate of the whole block = the median of fee / (weight / 4) over all transactions except
    the coinbase, rounded to a whole satoshi per vbyte (medianFee_own); the share of the reward that fees make; the field medianFee, which the chapter's examples read, is the figure the mempool.space block
    page prints for the block (it differs from ours: that service uses package-adjusted fee rates), stored beside ours and named as the service's.
 5. Writes ch09-evidence/mainnet_fee_census_v2_0_0.json: the raw facts, the statistics, the retrieval date, both sources named, the method and the licence statement (CC BY 4.0). Requests are spaced (SPACING seconds) and
    retried with exponential backoff (Retry-After honoured). A cache folder keeps every answer so a re-run does not ask again: CACHE (default /tmp/ch09_census_cache, not part of the repository).
Usage: sen0401_ch09_census_collect_v1_0_0.py [CACHE_DIR]"""
__version__ = "1.0.0"
import hashlib, json, os, statistics, subprocess, sys, time
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "ch09-evidence", "mainnet_fee_census_v2_0_0.json")
CACHE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ch09_census_cache"; os.makedirs(CACHE, exist_ok=True)
SPACING = 1.2; UA = "sen0401-course-research/1.0 (course materials; contact altunel.yusuf@gmail.com)"
SRC = {"mempool.space": "https://mempool.space/api", "blockstream.info": "https://blockstream.info/api"}
HISTORY = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 840000, 900000]; WINDOW = list(range(971480, 971490))
HEIGHTS = HISTORY + WINDOW; FULL = (840000, 971489); STORE = 600
_last = [0.0]
def get(src, path):
    f = os.path.join(CACHE, hashlib.sha256((src + path).encode()).hexdigest()[:24] + ".json")
    if os.path.exists(f): return open(f).read()
    for k in range(7):
        w = SPACING - (time.time() - _last[0])
        if w > 0: time.sleep(w)
        _last[0] = time.time()
        r = subprocess.run(["curl", "-sS", "-L", "-m", "90", "-A", UA, "-D", "-", "-o", f + ".body", "-w", "%{http_code}", SRC[src] + path], capture_output=True, text=True)
        code = r.stdout.strip()[-3:]
        if r.returncode == 0 and code == "200":
            os.replace(f + ".body", f); return open(f).read()
        ra = [l.split(":", 1)[1].strip() for l in r.stdout.splitlines() if l.lower().startswith("retry-after")]
        time.sleep(float(ra[0]) if ra and ra[0].replace(".", "").isdigit() else 2 ** (k + 1))
    raise SystemExit("giving up on %s%s (last code %s)" % (src, path, code))
def jget(src, path): return json.loads(get(src, path))
def subsidy(h): return 0 if h // 210000 >= 64 else (50 * 100_000_000) >> (h // 210000)
def tx_row(t): return {"txid": t["txid"], "version": t["version"], "locktime": t["locktime"], "size": t["size"], "weight": t["weight"], "fee": t["fee"],
                       "vin": [{"sequence": v["sequence"], "coinbase": bool(v.get("is_coinbase", False))} for v in t["vin"]], "n_out": len(t["vout"])}
facts = {s: {} for s in SRC}
for s in SRC:
    for h in HEIGHTS:
        bh = get(s, "/block-height/%d" % h).strip(); b = jget(s, "/block/" + bh); cb = jget(s, "/block/%s/txs/0" % bh)[0]
        assert cb["vin"][0].get("is_coinbase"), (s, h)
        facts[s][h] = {"hash": bh, "height": b["height"], "timestamp": b["timestamp"], "tx_count": b["tx_count"], "size": b["size"], "weight": b["weight"], "coinbase_out": sum(o["value"] for o in cb["vout"])}
        assert b["id"] == bh
    print("headers", s, len(facts[s]), flush=True)
cross = {"blocks_compared": 0, "blocks_equal": 0, "differences": []}
for h in HEIGHTS:
    cross["blocks_compared"] += 1
    a, b = facts["mempool.space"][h], facts["blockstream.info"][h]
    if a == b: cross["blocks_equal"] += 1
    else: cross["differences"].append({"height": h, "mempool.space": a, "blockstream.info": b})
full = {}
for h in FULL:
    bh = facts["mempool.space"][h]["hash"]; n = facts["mempool.space"][h]["tx_count"]; txs = []
    for off in range(0, n, 25): txs += [tx_row(t) for t in jget("mempool.space", "/block/%s/txs/%d" % (bh, off))]
    assert len(txs) == n, (h, len(txs), n)
    full[h] = txs; print("full block", h, n, flush=True)
txcmp = {"transactions_compared": 0, "transactions_equal": 0, "pages": [], "differences": []}
for h in FULL:
    bh = facts["mempool.space"][h]["hash"]; n = facts["mempool.space"][h]["tx_count"]
    offs = list(range(0, STORE, 25)) + [(n - 1) // 25 * 25]
    for off in offs:
        page = [tx_row(t) for t in jget("blockstream.info", "/block/%s/txs/%d" % (bh, off))]; mine = full[h][off:off + 25]
        txcmp["pages"].append("%d@%d" % (h, off))
        for x, y in zip(mine, page):
            txcmp["transactions_compared"] += 1
            if x == y: txcmp["transactions_equal"] += 1
            else: txcmp["differences"].append({"height": h, "txid": x["txid"], "mempool.space": x, "blockstream.info": y})
        if len(mine) != len(page): txcmp["differences"].append({"height": h, "offset": off, "lengths": [len(mine), len(page)]})
    print("cross-checked transactions", h, flush=True)
blocks = {}; stats = {}
for h in HEIGHTS:
    f = facts["mempool.space"][h]; reward = f["coinbase_out"]; fees = reward - subsidy(h)
    e = {"totalFees": fees, "reward": reward}
    row = {"hash": f["hash"], "height": h, "timestamp": f["timestamp"], "tx_count": f["tx_count"], "size": f["size"], "weight": f["weight"], "extras": e, "txs": []}
    stats[str(h)] = {"subsidy": subsidy(h), "fees_sat": fees, "reward_sat": reward, "fee_share_of_reward_percent": round(fees / reward * 100, 2)}
    if h in full:
        allx = full[h]; rates = sorted(t["fee"] / (t["weight"] / 4) for t in allx if not t["vin"][0]["coinbase"])
        med = statistics.median(rates)
        shown = jget("mempool.space", "/v1/block/" + f["hash"])["extras"]["medianFee"]
        e["medianFee"] = shown; e["medianFee_own"] = round(med)   # medianFee is the figure the mempool.space block page prints (the chapter's research and examples quote it); medianFee_own is ours (plain fee / (weight / 4)); they differ because mempool.space uses package-adjusted (CPFP) fee rates
        assert sum(t["fee"] for t in allx) == fees, ("sum of fees differs from coinbase - subsidy", h)
        stats[str(h)].update({"median_fee_rate_sat_per_vb": round(med, 4), "sum_of_transaction_fees_sat": sum(t["fee"] for t in allx), "stored_transactions": STORE})
        row["txs"] = allx[:STORE]
        stats[str(h)]["mempool_space_block_page_medianFee"] = shown
    blocks[str(h)] = row
doc = {"_version": "2.0.0", "fetched": time.strftime("%Y-%m-%d", time.gmtime()),
       "licence": "This dataset is the SEN0401 course's own work (the selection, the method and the computed statistics). The facts in it are facts of the Bitcoin block chain. Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); attribution: 'SEN0401 course, mainnet fee census v2.0.0'.",
       "sources": {"mempool.space": "https://mempool.space/api (primary: every request below the heading 'primary')", "blockstream.info": "https://blockstream.info/api (second source, used to cross-check)"},
       "terms_read": "mempool.space Terms of Service (updated 2024-07-10; the text of frontend/.../terms-of-service.component.html of github.com/mempool/mempool): no clause forbids the use of the API; no licence for the data is stated; 'no warranty ... verify all data'. blockstream.info: the explorer is Blockstream's; its terms of use (blockstream.com/terms, version 1.0) contain no clause on automated requests or on the data. Neither service states a licence for chain data; the facts are re-derived and cross-checked here.",
       "method": "Fixed sampling HEIGHTS (history: every 100,000 blocks from 100,000 to 900,000 with 840,000 added; window: 971,480-971,489). Block facts and the coinbase from both services and compared; all transactions of 840,000 and 971,489 from mempool.space, the first %d stored, the first %d and the last page of each fetched from blockstream.info and compared field by field. Statistics computed by sen0401_ch09_census_collect_v1_0_0.py: total fees = coinbase outputs - subsidy (and, for the two full blocks, equal to the sum of the transaction fees: asserted); medianFee_own = round(median of fee / (weight / 4) over all transactions but the coinbase); medianFee = the figure the mempool.space block page prints for the same block (kept because the chapter's research quotes it; it differs from ours because that service uses package-adjusted fee rates)." % (STORE, STORE),
       "requests": {"spacing_seconds": SPACING, "retry": "up to 7 tries, exponential backoff, Retry-After honoured", "user_agent": UA},
       "crosscheck": {"blocks": cross, "transactions": txcmp},
       "statistics": stats, "blocks": blocks}
json.dump(doc, open(OUT, "w"), indent=None, separators=(",", ":"))
print("written", OUT, os.path.getsize(OUT), "bytes | blocks equal %d of %d | transactions equal %d of %d" % (cross["blocks_equal"], cross["blocks_compared"], txcmp["transactions_equal"], txcmp["transactions_compared"]))
for h in FULL: print(h, "medianFee (mempool.space page)", blocks[str(h)]["extras"]["medianFee"], "own", blocks[str(h)]["extras"]["medianFee_own"])
