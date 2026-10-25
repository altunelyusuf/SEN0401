"""Runs every listing of examples_v2_0_0.py under the interpreter that runs this file, INSIDE the unpacked wheel of the page (sen0401_ch13_lib-1.1.0: the library module and the saved files it carries, nothing else on the
path), and writes examples_out_v2_0_0.json: for each example id the rows [expression, repr(value)] of its `show` list, exactly as Python printed them, plus "_python". Each listing runs in a fresh namespace after the
PRELUDE, so no example depends on another. Nothing is typed: the deck's result pictures are drawn from this file.
Usage: python3.14 examples_run_v2_0_0.py"""
__version__ = "2.0.0"
import json, os, platform, sys, tempfile, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import examples_v2_0_0 as X
WHL = os.path.join(ROOT, "03-materials", "ch13", "assets", "sen0401_ch13_lib-1.1.0-py3-none-any.whl")
tmp = tempfile.mkdtemp(prefix="sen0401_fx_ch13_"); zipfile.ZipFile(WHL).extractall(tmp)
sys.path.insert(0, tmp); os.chdir(tmp)
out = {"_python": platform.python_version(), "_note": "recorded by examples_run_v2_0_0.py inside the unpacked wheel sen0401_ch13_lib-1.1.0; one fresh namespace per example"}
for e in X.EXAMPLES:
    ns = {}; exec(X.PRELUDE, ns); exec("\n".join(l for g in e["groups"] for l in g["lines"]), ns)
    out[e["id"]] = [[x, repr(eval(x, ns))] for x in e["show"]]
    print(e["id"], out[e["id"]])
os.chdir(HERE); shutil.rmtree(tmp, ignore_errors=True)
json.dump(out, open(os.path.join(HERE, "examples_out_v2_0_0.json"), "w"), indent=1)
print("recorded %d examples under Python %s" % (len(X.EXAMPLES), platform.python_version()))
