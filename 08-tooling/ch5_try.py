"""scratch: evaluate the CHECKS of a text part and report the ones that do not hold: ch5_try.py MODULE LISTNAME"""
import sys, os, importlib
os.environ["CH5_DEBUG"] = "1"; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
m = importlib.import_module(sys.argv[1]); L = getattr(m, sys.argv[2])
bad = 0
for i, (e, x) in enumerate(L):
    try:
        g = repr(eval(e, {}))
        if g != x: bad += 1; print("CHECK", i, "expected", x[:80], "got", g[:120], "|", e[-160:])
    except Exception as ex: bad += 1; print("CHECK", i, "ERR", repr(ex)[:200], "|", e[-160:])
print(len(L), "checks,", bad, "bad")
