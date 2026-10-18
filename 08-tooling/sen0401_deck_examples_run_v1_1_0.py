#!/usr/bin/env python3
"""sen0401_deck_examples_run v1.1.0 (over 1.0.0: reads the NEWEST chNN-deck/examples_v*.py) - executes every statement of it (one namespace per group after PRELUDE) and writes
examples_out_v1_0_0.json, as ch07-deck/examples_run_v1_0_0.py does. Usage: sen0401_deck_examples_run_v1_1_0.py NN <python> <out.json>"""
import glob, importlib.util, json, os, re, subprocess, sys
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, PY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("ex", sorted(glob.glob(os.path.join(ROOT, "08-tooling", "ch%s-deck" % n, "examples_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
RUNNER = ("import json, sys\nns = {}\nexec(sys.argv[1], ns)\nout = []\nfor st in json.loads(sys.argv[2]):\n    try:\n        try:\n            out.append(repr(eval(st, ns)))\n"
          "        except SyntaxError:\n            exec(st, ns); out.append('')\n    except Exception as e:\n        out.append('%s: %s' % (type(e).__name__, e))\nprint(json.dumps(out))\n")
ver = subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True)
out = {"_version": "1.1.0", "_python": ver.stdout.strip()}
for k, rows in m.EX.items():
    if any("\n" in r for r in rows): sys.exit("REFUSED: group %s has a multi-line statement" % k)
    r = subprocess.run([PY, "-c", RUNNER, m.PRELUDE, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode: sys.exit("group %s failed: %s" % (k, r.stderr[-400:]))
    out[k] = [[s, o] for s, o in zip(rows, json.loads(r.stdout))]
json.dump(out, open(OUT, "w"), indent=1); print("written", OUT, "under Python", out["_python"], "-", len(m.EX), "groups")
