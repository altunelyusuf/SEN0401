"""Runs every listing of examples_v2_0_0.py under the interpreter that runs this file (the deck says which: 'run under Python x.y.z') and writes examples_out_v2_0_0.json: for each example id,
the rows [expression, repr(value)] of its `show` list (and of its `final` expression, which the slide prints), exactly as Python printed them, plus "_python". Each listing runs in a fresh namespace after the PRELUDE, so no example depends on
another. The library modules are taken from SEN_LIBDIR when set (a scratch folder holding only what the page's wheel holds: the two library modules and ch10-evidence), else from 08-tooling.
Nothing is typed: the deck's result pictures are drawn from this file.   Usage: [SEN_LIBDIR=dir] python3.14 examples_run_v2_0_0.py"""
__version__ = "2.0.0"
import json, os, platform, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
LIB = os.environ.get("SEN_LIBDIR") or os.path.dirname(HERE)
sys.path.insert(0, LIB)
import examples_v2_0_0 as X
out = {"_python": platform.python_version(), "_note": "recorded by examples_run_v2_0_0.py; one fresh namespace per example; library from the wheel contents"}
for e in X.EXAMPLES:
    ns = {}; exec(X.PRELUDE, ns); exec("\n".join(l for g in e["groups"] for l in g["lines"]), ns)
    out[e["id"]] = [[x, repr(eval(x, ns))] for x in e["show"] + ([e["final"]] if e["final"] not in e["show"] else [])]
    print(e["id"], out[e["id"]])
json.dump(out, open(os.path.join(HERE, "examples_out_v2_0_0.json"), "w"), indent=1)
print("recorded %d examples under Python %s" % (len(X.EXAMPLES), platform.python_version()))
