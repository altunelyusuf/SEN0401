"""Executes every statement of examples_v1_0_0.py (this chapter's) under the interpreter given, one namespace per group after PRELUDE,
and writes examples_out_v1_0_0.json: for every statement its text and what Python answered (empty for a statement that prints
nothing, and 'ErrorClass: message' for a statement that is meant to fail, exactly as deck_check_v1_0_0.py records it).
Usage: examples_run_v1_0_0.py <python> <out.json>
Chapter 7 copy of chapter 6's runner (08-tooling/ch06-deck/examples_run_v1_0_0.py): the code is identical; a copy is needed
because the runner imports the examples module from its own folder."""
__version__ = "1.0.0"
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import EX, PRELUDE

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
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", len(EX), "groups")
