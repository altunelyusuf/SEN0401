"""Executes every row and every program of examples_v1_1_0.py under the interpreter given, each example in
one namespace after PRELUDE, and writes examples_out_v1_1_0.json: for every row its statement and what
Python answered (empty for a statement that has no value).

It refuses to write anything if a recast example stops producing the output the chapter corpus records in
EXPECT, so the deck can only ever show numbers the chapter itself has.

Usage: examples_run_v1_1_0.py <python> <out.json>
"""
__version__ = "1.1.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_1_0 import EX, BLOCKS, EXPECT, PRELUDE

PY, OUT = sys.argv[1], sys.argv[2]
ROWS = ("import json, sys\nns = {}\nexec(sys.argv[1], ns)\nout = []\n"
        "for st in json.loads(sys.argv[2]):\n"
        "    try:\n        out.append(repr(eval(st, ns)))\n"
        "    except SyntaxError:\n        exec(st, ns); out.append('')\n"
        "print(json.dumps(out))")
BLOCK = ("import json, sys\nns = {}\nexec(sys.argv[1], ns)\nexec(sys.argv[2], ns)\n"
         "print(json.dumps(repr(ns['result'])))")

out = {"_version": __version__,
       "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"],
                                 capture_output=True, text=True).stdout.strip(),
       "groups": {}, "blocks": {}}
bad = []
for key, rows in EX.items():
    r = subprocess.run([PY, "-c", ROWS, PRELUDE, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("example %s failed: %s" % (key, r.stderr[-400:]))
    vals = json.loads(r.stdout)
    out["groups"][key] = [[s, v] for s, v in zip(rows, vals)]
    if key in EXPECT and vals[-1] != EXPECT[key]:
        bad.append((key, EXPECT[key], vals[-1]))
for key, body in BLOCKS.items():
    r = subprocess.run([PY, "-c", BLOCK, PRELUDE, body], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("program %s failed: %s" % (key, r.stderr[-400:]))
    val = json.loads(r.stdout)
    out["blocks"][key] = [body, val]
    if key in EXPECT and val != EXPECT[key]:
        bad.append((key, EXPECT[key], val))
if bad:
    for key, want, got in bad:
        print("  REFUSED %s: the corpus records %s, this run gives %s" % (key, want, got))
    raise SystemExit("%d example(s) no longer give the chapter's own answer; nothing written" % len(bad))
json.dump(out, open(OUT, "w"), indent=1)
print("written %s: %d row examples, %d programs, all matching the corpus, under Python %s"
      % (os.path.basename(OUT), len(out["groups"]), len(out["blocks"]), out["_python"]))
