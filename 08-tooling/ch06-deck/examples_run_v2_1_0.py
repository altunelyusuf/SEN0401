"""Runs every listing of examples_v2_1_0.py under the interpreter that runs this file (the deck says which: 'run under Python x.y.z') and writes
examples_out_v2_1_0.json: for each example id, the rows [expression, repr(value)] of its `show` list, exactly as Python printed them, plus "_python".
Each listing runs in a fresh namespace after the PRELUDE, so no example depends on another. Nothing is typed: the deck's result pictures are drawn from this file.
Usage: python3.14 examples_run_v2_1_0.py"""
__version__ = "2.1.0"
import json, os, platform, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import examples_v2_1_0 as X
out = {"_python": platform.python_version(), "_note": "recorded by examples_run_v2_1_0.py; one fresh namespace per example"}
for e in X.EXAMPLES:
    ns = {}; exec(X.PRELUDE, ns); exec("\n".join(e["code"]), ns)
    out[e["id"]] = [[x, repr(eval(x, ns))] for x in e["show"]]
json.dump(out, open(os.path.join(HERE, "examples_out_v2_1_0.json"), "w"), indent=1)
print("recorded %d examples under Python %s" % (len(X.EXAMPLES), platform.python_version()))
