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
SETUP = "import sys, os; sys.path.insert(0, os.path.dirname(HERE)); import sen0401_ch02_tx_lib_v1_0_0 as T"
CHARTS = {  # key -> expression returning [(label, value), ...]: the first series of the chart on the slide of that example
 "ex03": "[('Input', sum(T.ALICE_IN)), ('To Bob', T.ALICE_OUT[0]), ('Change', T.ALICE_OUT[1]), ('Fee', sum(T.ALICE_IN) - sum(T.ALICE_OUT))]",
 "ex07": "[('Payment', 80000), ('Coins picked', sum(T.select([60000, 30000, 25000], 80000)[0])), ('Change back', T.select([60000, 30000, 25000], 80000)[1])]",
 "ex09": "[('%d sat/vB' % r, 100000 - 75000 - r * 143) for r in (10, 20, 35, 100)]",
 "ex10": "[('%d zero%s' % (z, '' if z == 1 else 's'), next(n for n in range(10**7) if T.sha('Hello, world! ' + str(n)).startswith('0' * z))) for z in (1, 2, 3, 4)]",
 "ex12": "[('%d' % z, round(T.catch_up(0.1, z), 7)) for z in range(7)]",
 "ex13": "[(y, (50 * T.COIN >> i) / T.COIN) for i, y in enumerate(('2009', '2012', '2016', '2020', '2024', '2028'))]",
}
out["_charts"] = {}
for k, expr in CHARTS.items():
    ns = {"HERE": HERE}; exec(SETUP, ns); want = eval(expr, ns)
    out["_charts"][k] = {"setup": SETUP, "expr": expr, "labels": [w[0] for w in want], "values": [float(w[1]) for w in want]}
json.dump(out, open(os.path.join(HERE, "examples_out_v3_0_0.json"), "w"), indent=1)
print("recorded %d examples and %d charts under Python %s" % (len(X.EXAMPLES), len(CHARTS), platform.python_version()))
