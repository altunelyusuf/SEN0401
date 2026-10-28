"""[v3.1.0, a new file over examples_run_v3_0_0.py: also records the expression of each chart on the slides in _charts, which the deck check v1_1_0 re-runs.]
Runs every listing of examples_v3_1_0.py under the interpreter that runs this file (the deck says which: 'run under Python x.y.z') and writes examples_out_v3_1_0.json: for each example id,
the rows [expression, repr(value)] of its `show` list, exactly as Python printed them, plus "_python". Each listing runs in a fresh namespace after the PRELUDE, so no example depends on
another, with ONLY the chapter library module on the path (as the page has it). Nothing is typed: the deck's result pictures are drawn from this file.
Usage: python3.14 -B examples_run_v3_1_0.py"""
__version__ = "3.1.0"
import json, os, platform, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import examples_v3_1_0 as X
out = {"_version": "3.1.0", "_source": "examples_v3_1_0.py", "_python": platform.python_version(), "_note": "recorded by examples_run_v3_1_0.py; one fresh namespace per example"}
for e in X.EXAMPLES:
    ns = {}; exec(X.PRELUDE, ns); exec("\n".join(l for g in e["groups"] for l in g["lines"]), ns)
    out[e["id"]] = [[x, repr(eval(x, ns))] for x in e["show"]]
    print(e["id"], out[e["id"]])
SETUP = "import sys, os, math; sys.path.insert(0, os.path.dirname(HERE)); import sen0401_ch01_lib_v1_0_0 as K"
CHARTS = {  # key -> expression returning [(label, value), ...]: the first series of the chart on the slide of that example
 "ex03": "[(y, K.subsidy(h)) for y, h in zip(('2009', '2012', '2016', '2020', '2024'), (0, 210000, 420000, 630000, 840000))]",
 "ex04": "[('E%d' % k, math.floor(sum((50 * K.COIN >> j) * K.HALVING for j in range(k)) / K.COIN / 10**6 * 10**6) / 10**6) for k in range(1, 9)]",
 "ex06": "[(d, int(10000 * p)) for d, p in K.PIZZA.items()]",
 "ex07": "[('%d zero%s' % (z, '' if z == 1 else 's'), K.mine(b'alice pays bob 1', z)[0] + 1) for z in (1, 2, 3, 4)]",
 "ex10": "[('Coin in', 100000), ('To Bob', 20000), ('Change', 75000), ('Fee', 100000 - 20000 - 75000)]",
}
out["_charts"] = {}
for k, expr in CHARTS.items():
    ns = {"HERE": HERE}; exec(SETUP, ns); want = eval(expr, ns)
    out["_charts"][k] = {"setup": SETUP, "expr": expr, "labels": [w[0] for w in want], "values": [float(w[1]) for w in want]}
    print(k, out["_charts"][k]["labels"], out["_charts"][k]["values"])
json.dump(out, open(os.path.join(HERE, "examples_out_v3_1_0.json"), "w"), indent=1)
print("recorded %d examples and %d charts under Python %s" % (len(X.EXAMPLES), len(CHARTS), platform.python_version()))
