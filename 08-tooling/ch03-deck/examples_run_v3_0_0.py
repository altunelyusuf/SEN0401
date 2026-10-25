"""Runs every listing of examples_v3_0_0.py under the interpreter that runs this file (python3.14: the deck prints its version on every code slide) and writes
examples_out_v3_0_0.json: for each example id the rows [expression, repr(value)] of its `show` list exactly as Python printed them, the chart records `_charts` that the deck check
re-runs (setup, expression, labels, values), and "_python". Each listing runs in a fresh namespace after the PRELUDE, so no example depends on another. Nothing is typed:
the result pictures of the deck are drawn from this file.   Usage: python3.14 -B examples_run_v3_0_0.py"""
__version__ = "3.0.0"
import json, os, platform, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import examples_v3_0_0 as X
out = {"_version": "3.0.0", "_python": platform.python_version(), "_source": "examples_v3_0_0.py", "_note": "recorded by examples_run_v3_0_0.py; one fresh namespace per example"}
for e in X.EXAMPLES:
    ns = {}; exec(X.PRELUDE, ns); exec("\n".join(e["lines"]), ns)
    assert e["lines"][-1] == e["show"][0], e["id"]
    out[e["id"]] = [[x, repr(eval(x, ns))] for x in e["show"]]
    print(e["id"], out[e["id"]][0])
SETUP = "import sys, os, json; sys.path.insert(0, os.path.dirname(HERE)); import sen0401_ch03_core_lib_v1_0_0 as T"
CHARTS = {  # key -> expression returning [(label, value), ...]: the first series of the chart on the slide of that example
 "ex06": "list(zip(['Block index', 'Chain state', 'Coins cache'], T.cache_split(1024)))",
 "ex13": "[('Output %d' % o['n'], round(o['value'] * 10**8)) for o in json.loads(T.ALICE_DECODED)['vout']]",
 "ex15": "(lambda b, w: [('Base x 4', 4 * len(b)), ('Witness x 1', len(w)), ('Weight', 4 * len(b) + len(w))])(*T.split_witness(bytes.fromhex(T.ALICE_HEX)))",
 "ex17": "[('Level %d' % i, n) for i, n in enumerate(T.merkle(T.TXIDS_123456)[1])]",
 "ex18": "[(str(h), (T.BLOCK_TIMES[h] - T.BLOCK_TIMES[123446]) // 60) for h in range(123446, 123457)]",
 "ex19": "sorted(T.age_days(T.QUERIED).items(), key=lambda kv: kv[1])",
 "mempool": "[('Default node', T.MAXMEMPOOL_MB), ('Blocks-only mode', T.BLOCKSONLY_MB)]",
}
out["_charts"] = {}
for k, expr in CHARTS.items():
    ns = {"HERE": HERE}; exec(SETUP, ns); want = eval(expr, ns)
    out["_charts"][k] = {"setup": SETUP, "expr": expr, "labels": [w[0] for w in want], "values": [float(w[1]) for w in want]}
json.dump(out, open(os.path.join(HERE, "examples_out_v3_0_0.json"), "w"), indent=1)
print("recorded %d examples and %d charts under Python %s" % (len(X.EXAMPLES), len(CHARTS), platform.python_version()))
