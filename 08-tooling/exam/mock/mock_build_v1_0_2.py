#!/usr/bin/env python3
"""Build v1.0.2 (X3b): the delivered mock set. Code only; output goes to the private CME set folder.
Usage: mock_build_v1_0_2.py BANK.json OUTDIR --set v1_0_0
Writes sen0401_mock_exam_master_<set>.html and sen0401_mock_exam_m1_<set>.html .. m8 from shell v1.0.1 (page footer shows the set version and the bank version).
The master is the same page as m1 (same bytes). Refuses a synthetic bank."""
import json, os, sys, hashlib
H = os.path.dirname(os.path.abspath(__file__))
def read(n): return open(os.path.join(H, n), encoding="utf-8").read()
def build(bank, preset, footer):
    t = read("mock_shell_v1_0_1.html")
    bj = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = "window.MOCK_PRESET=%s;" % json.dumps(preset)
    for ph, val in (("/*@@BANK@@*/", bj), ("/*@@PRESET@@*/", pre), ("/*@@SCORING@@*/", read("mock_scoring_v1_0_0.js")),
                    ("/*@@DERIVE@@*/", read("mock_derive_v1_0_0.js")), ("/*@@UI@@*/", read("mock_ui_v1_0_0.js")), ("/*@@SETFOOTER@@*/", footer)):
        assert t.count(ph) == 1, ph
        t = t.replace(ph, val)
    return t
def main():
    a = sys.argv; bankf, out = a[1], a[2]; setv = a[a.index("--set") + 1]
    bank = json.load(open(bankf))
    if bank.get("synthetic"): raise SystemExit("refusing: synthetic bank")
    os.makedirs(out, exist_ok=True)
    footer = "SEN0401 mock exam set %s (bank %s). Practice papers only; they are not the real exam." % (setv, "v" + bank["version"].replace(".", "_"))
    files = [("sen0401_mock_exam_master_%s.html" % setv, {"k": 1})] + [("sen0401_mock_exam_m%d_%s.html" % (k, setv), {"k": k}) for k in range(1, 9)]
    for name, preset in files:
        p = os.path.join(out, name)
        open(p, "w", encoding="utf-8").write(build(bank, preset, footer))
        print(name, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest())
main()
