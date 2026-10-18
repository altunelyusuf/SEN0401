#!/usr/bin/env python3
"""sen0401_deck_examples_record v1.0.0 - records the examples of a chapter 1 to 4 deck in the format of sen0401_deck_check_v1_0_0.py (top-level groups of [statement, answer] rows),
under the interpreter given, from the newest chNN-deck/examples_v*.py (EX, PRELUDE, optional BLOCKS and EXPECT of the chapter's own check). One fresh namespace per group after PRELUDE,
as ch0N-deck/examples_run_*.py does. It refuses to write when a group's last answer is not the one the chapter corpus records in EXPECT, so the deck can only show the chapter's own numbers.
The recording is new: examples_out_v<version of the examples file>.json; a committed recording is never overwritten.
Usage: sen0401_deck_examples_record_v1_0_0.py NN [python]      (default python: /home/claude/venv314/bin/python)"""
__version__ = "1.0.0"
import glob, importlib.util, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
n = sys.argv[1]; PY = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/venv314/bin/python"
chd = os.path.join(HERE, "ch%s-deck" % n)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
f = sorted(glob.glob(os.path.join(chd, "examples_v*.py")), key=vk)[-1]
sys.path.insert(0, chd)
spec = importlib.util.spec_from_file_location("ex", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
RUNNER = ("import json, sys\nns = {}\nexec(sys.argv[1], ns)\nout = []\nfor st in json.loads(sys.argv[2]):\n    try:\n        try:\n            out.append(repr(eval(st, ns)))\n"
          "        except SyntaxError:\n            exec(st, ns); out.append('')\n    except Exception as e:\n        out.append('%s: %s' % (type(e).__name__, e))\nprint(json.dumps(out))\n")
ver = subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()
out = {"_version": __version__, "_python": ver, "_source": os.path.basename(f)}
bad = []
for k, rows in m.EX.items():
    for r in rows:
        if "\n" in r: sys.exit("REFUSED: group %s has a multi-line statement" % k)
    r = subprocess.run([PY, "-c", RUNNER, m.PRELUDE, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode: sys.exit("group %s failed: %s" % (k, r.stderr[-400:]))
    vals = json.loads(r.stdout)
    out[k] = [[s, o] for s, o in zip(rows, vals)]
    exp = getattr(m, "EXPECT", {})
    if k in exp and vals[-1] != exp[k]: bad.append((k, exp[k], vals[-1]))
if bad:
    for k, w, g in bad: print("  REFUSED %s: the corpus records %s, this run gives %s" % (k, w, g))
    sys.exit("%d group(s) no longer give the chapter's own answer; nothing written" % len(bad))
dst = os.path.join(chd, "examples_out_v%s.json" % "_".join(str(x) for x in vk(f)))
if os.path.exists(dst): sys.exit("REFUSED: %s exists (a recording is never overwritten)" % dst)
json.dump(out, open(dst, "w"), indent=1)
print("written", os.path.relpath(dst, HERE), "under Python", ver, "-", len(m.EX), "groups")
