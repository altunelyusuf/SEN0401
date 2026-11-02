#!/usr/bin/env python3
"""No dropped, removed or quarantined template is drawn (X3b). Derives 240 sheets (mocks k = 1..240, seed 1000+37k) with the same derive.js text as the page
(node) and checks every drawn unit id against (a) the bank flag "dropped" and (b) the list of templates removed from the families (--removed ids)
and the quarantined list of the bank. Also checks that the bank itself holds none of the removed ids. Planted defect: a derive that draws a flagged template must be caught.
Usage: mock_test_nodrop_v1_0_0.py BANK.json --removed n3x_4,n4x_5,... [--log F]. Prints ids and counts only."""
import json, subprocess, sys, os, tempfile, collections
H = os.path.dirname(os.path.abspath(__file__)); a = sys.argv
bankf = a[1]; removed = set(a[a.index("--removed") + 1].split(",")) if "--removed" in a else set()
lines = []
def log(x): print(x); lines.append(x)
def node(job):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f: json.dump(job, f); p = f.name
    r = subprocess.run(["nice", "-n", "10", "node", os.path.join(H, "mock_node_driver_v1_0_0.js"), p], capture_output=True, text=True); os.unlink(p)
    if r.returncode: raise SystemExit("node: " + r.stderr[:400])
    return json.loads(r.stdout)
B = json.load(open(bankf)); bank = B["items"]
dropped = {x["id"] for x in bank if x.get("dropped")}; quar = set(B.get("quarantined") or [])
inbank = {x["id"] for x in bank}
log("bank units %d; flagged dropped %d; quarantined list %d; removed ids given %d; removed ids present in the bank: %s" % (len(bank), len(dropped), len(quar), len(removed), sorted(removed & inbank) or "none"))
bad = []
def run(ks, forbidden, tag, planted=None):
    mocks = node({"bank": bankf, "patch": "none", "ops": [{"op": "derive", "k": k, "seed": 1000 + 37 * k} for k in ks]})
    hit = collections.Counter()
    for m in mocks:
        for i in m["itemIds"]:
            if i.split("#")[0] in forbidden: hit[i.split("#")[0]] += 1
    return mocks, hit
forb = dropped | removed | quar
mocks, hit = run(range(1, 241), forb, "main")
used = {i.split("#")[0] for m in mocks for i in m["itemIds"]}
log("sheets derived: %d (k 1..240); distinct units drawn: %d of %d; forbidden units drawn: %d %s" % (len(mocks), len(used), len(bank), sum(hit.values()), dict(hit) or ""))
ok = not hit and not (removed & inbank) and len(mocks) == 240
# planted defect: clear the dropped flag of a template in a temp copy of the bank: the check must see it drawn
plant = json.loads(json.dumps(B)); tid = sorted(dropped)[0] if dropped else None
for x in plant["items"]:
    if x["id"] in dropped: x.pop("dropped")
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f: json.dump(plant, f); pp = f.name
m2 = node({"bank": pp, "patch": "none", "ops": [{"op": "derive", "k": k, "seed": 1000 + 37 * k} for k in range(1, 241)]}); os.unlink(pp)
n2 = sum(1 for m in m2 for i in m["itemIds"] if i.split("#")[0] in dropped)
log("PLANTED DEFECT flag removed from the %d dropped templates in a temp copy: %d draws of them in 240 sheets -> %s" % (len(dropped), n2, "CAUGHT" if n2 else "NOT CAUGHT"))
ok = ok and n2 > 0
log("NODROP TEST " + ("PASS" if ok else "FAIL"))
if "--log" in a: open(a[a.index("--log") + 1], "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
