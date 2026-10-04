"""Executes every statement of examples_v2_0_0.py under the interpreter given, one namespace per group after PRELUDE,
and writes examples_out_v2_0_0.json: for every statement its text and what Python answered (empty for a statement that
prints nothing, and 'ErrorClass: message' for a statement that is meant to fail, exactly as deck_check_v2_0_0.py
records it, so that the error messages on the slides are executed too).
Usage: examples_run_v2_0_0.py <python> <out.json>"""
__version__ = "2.0.0"
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v2_0_0 import EX, PRELUDE, EC_SRC

PY, OUT = sys.argv[1], sys.argv[2]
RUNNER = (
    "import json, sys\n"
    "ns = {}\n"
    "exec(sys.argv[1], ns)\n"
    "out = []\n"
    "for st in json.loads(sys.argv[2]):\n"
    "    try:\n"
    "        try:\n"
    "            out.append(repr(eval(st, ns)))\n"
    "        except SyntaxError:\n"
    "            exec(st, ns); out.append('')\n"
    "    except Exception as e:\n"
    "        out.append('%s: %s' % (type(e).__name__, e))\n"
    "print(json.dumps(out))\n"
)
ver = subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True)
out = {"_version": __version__, "_python": ver.stdout.strip()}
for k, rows in EX.items():
    r = subprocess.run([PY, "-c", RUNNER, PRELUDE, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("group %s failed: %s" % (k, r.stderr[-400:]))
    out[k] = [[s, o] for s, o in zip(rows, json.loads(r.stdout))]
out["_snippets"] = {"ec": EC_SRC}
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", len(EX), "groups")
