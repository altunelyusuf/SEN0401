"""Runs every listing of examples_v3_4_0.py under the interpreter that runs this file (python3.14: the deck prints its version on every code slide) and writes
examples_out_v3_4_0.json: for each example id the rows [expression, repr(value)] of its `show` list exactly as Python printed them, the chart records `_charts` that the deck check
re-runs (setup, expression, labels, values), and "_python". Each listing runs in a fresh namespace after the PRELUDE, so no example depends on another. Nothing is typed:
the result pictures of the deck are drawn from this file.   Usage: python3.14 -B examples_run_v3_4_0.py"""
__version__ = "3.4.0"
import json, os, platform, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import examples_v3_4_0 as X
out = {"_version": "3.4.0", "_python": platform.python_version(), "_source": "examples_v3_4_0.py", "_note": "recorded by examples_run_v3_4_0.py; one fresh namespace per example"}
for e in X.EXAMPLES:
    ns = {}; exec(X.PRELUDE, ns); exec("\n".join(e["lines"]), ns)
    assert e["lines"][-1] == e["show"][0], e["id"]
    out[e["id"]] = [[x, repr(eval(x, ns))] for x in e["show"]]
    print(e["id"], out[e["id"]][0])
SETUP = "import sys, os; sys.path.insert(0, os.path.dirname(HERE)); import math; import sen0401_ch04_lib_v1_0_0 as K"
CHARTS = {  # key -> expression returning [(label, value), ...]: the first series of the chart on the slide of that example
 "ex02": "[('4-digit PIN', K.bits_of(10, 4)), ('8 lowercase letters', K.bits_of(26, 8)), ('12 keyboard symbols', K.bits_of(94, 12)), ('256 coin flips', K.bits_of(2, 256))]",
 "ex06": "[('%d-bit key' % n, round(math.log10(2 ** (n - 1)))) for n in (20, 40, 80, 128, 256)]",
 "ex09": "[('Public key', len(K.pub_bytes(K.ec_mul(K.BOOK_K)))), ('After SHA256', 32), ('After RIPEMD-160', len(K.hash160(K.pub_bytes(K.ec_mul(K.BOOK_K)))))]",
 "ex13": "[('HASH160 collision', 80), ('HASH160 preimage', 160), ('SHA256 collision', 128), ('SHA256 preimage', 256)]",
 "ex19": "[('%d letter%s' % (m, '' if m == 1 else 's'), 58 ** m) for m in range(1, 7)]",
}
out["_charts"] = {}
for k, expr in CHARTS.items():
    ns = {"HERE": HERE}; exec(SETUP, ns); want = eval(expr, ns)
    out["_charts"][k] = {"setup": SETUP, "expr": expr, "labels": [w[0] for w in want], "values": [float(w[1]) for w in want]}
json.dump(out, open(os.path.join(HERE, "examples_out_v3_4_0.json"), "w"), indent=1)
print("recorded %d examples and %d charts under Python %s" % (len(X.EXAMPLES), len(CHARTS), platform.python_version()))
