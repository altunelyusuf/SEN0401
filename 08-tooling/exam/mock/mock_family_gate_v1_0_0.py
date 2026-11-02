#!/usr/bin/env python3
"""Family gate v1.0.0 (X3b): runs exclusion gate v1.0.1 on EVERY INSTANCE of the newest part file of each mock family, one instance at a time, and lists the failing instances per template
(template id, instance number, reason codes). Used to decide the exam-wins removals (instance level only when a template keeps its 8 instances, else template level) and to prove the
newest part versions are clean. Prints ids and codes only (no item text). Usage: mock_family_gate_v1_0_0.py [--log F]"""
import sys, json, glob, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mock_exclusion_gate_v1_0_1 as G
P = "/home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/"
lines = []
def L(x): print(x); lines.append(x)
def latest(key):
    fs = glob.glob(P + "mock_bank_ch%s_v*.json" % key)
    return max(fs, key=lambda f: tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.json$", f).groups()))
g = G.Gate(); total = 0; bad = 0
for key in ["1x", "2x", "3x", "4x", "5x", "5y"]:
    f = latest(key); d = json.load(open(f)); fails = []
    for it in d["items"]:
        for k, ins in enumerate(it["instances"]):
            one = {"id": it["id"], "type": "numeric", "unit": it.get("unit", ""), "family": d["family"], "instances": [ins]}
            msgs = []; G.run_items(g, [one], lambda x: msgs.append(x), label=""); total += 1
            b = [m for m in msgs if " FAIL" in m and "units checked" not in m]
            if b:
                bad += 1; fails.append("%s#%d %s" % (it["id"], k, re.sub(r".*FAIL\s*", "", b[0])[:60]))
    L("%s %s: %d templates, %d instances, failing instances %d %s" % (os.path.basename(f), d["family"], len(d["items"]), sum(len(i["instances"]) for i in d["items"]), len(fails), fails))
L("FAMILY GATE: %d instances checked, %d failing -> %s" % (total, bad, "PASS" if bad == 0 else "FAIL"))
if "--log" in sys.argv: open(sys.argv[sys.argv.index("--log") + 1], "w").write("\n".join(lines) + "\n")
sys.exit(1 if bad else 0)
