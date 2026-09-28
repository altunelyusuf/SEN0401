"""Executes every row of examples_v1_0_0.py under the interpreter given, each group in one namespace after PRELUDE, and
writes examples_out_v1_0_0.json: for every row its statement and what Python printed (empty for a statement).
Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import EX, PRELUDE, MERKLE_SRC
PY, OUT = sys.argv[1], sys.argv[2]
RUNNER = "import json, sys\nns = {}\nexec(sys.argv[1], ns)\nout = []\nfor st in json.loads(sys.argv[2]):\n    try:\n        out.append(repr(eval(st, ns)))\n    except SyntaxError:\n        exec(st, ns); out.append('')\nprint(json.dumps(out))"
out = {"_version": __version__, "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()}
for k, rows in EX.items():
    r = subprocess.run([PY, "-c", RUNNER, PRELUDE, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode: raise SystemExit("group %s failed: %s" % (k, r.stderr[-300:]))
    out[k] = [[s, o] for s, o in zip(rows, json.loads(r.stdout))]
out["_snippets"] = {"merkle": MERKLE_SRC}
json.dump(out, open(OUT, "w"), indent=1); print("written", OUT, "under Python", out["_python"])
