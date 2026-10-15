#!/usr/bin/env python3
"""sen0401_ch08_freeze v1.0.0 - evaluates every K-expression that the chapter's data module uses (leaf examples and extra claims) once, in one Python 3.14 process, and writes the values
as sen0401_ch08_expect_v1_0_0.py. The values are then reviewed by a person against the text before they are accepted; the checks (sen0401_rdodi_checks) re-run each expression in a fresh interpreter and compare."""
__version__ = "1.0.0"
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_ch08_rdodi_data_v1_0_0 as D
import sen0401_ch08_claims_v1_0_0 as K
keys = [l[5] for l in D.LEAVES] + list(D.EXTRA)
out = {}
for k in dict.fromkeys(keys):
    t = time.time(); out[k] = repr(eval(k, {"K": K})); print("%-52s %5.1fs %s" % (k, time.time() - t, out[k][:110]))
with open(os.path.join(HERE, "sen0401_ch08_expect_v1_0_0.py"), "w") as f:
    f.write('"""Frozen expected values of the chapter 8 K-expressions (written by sen0401_ch08_freeze_v1_0_0.py, reviewed against the text)."""\n__version__ = "1.0.0"\nEXPECT = {\n')
    for k, v in out.items():
        f.write("    %r: %r,\n" % (k, v))
    f.write("}\n")
print(len(out), "expressions frozen")
