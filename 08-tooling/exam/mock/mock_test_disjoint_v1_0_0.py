#!/usr/bin/env python3
"""Disjointness test (brief point 7): derive mocks 1..8 from a bank (the same derive.js as the page, run by node), prove by code that no item
id appears in two mocks, mock 9.. reuse only ids of mocks 1..8, plus structure checks (100 points, 21 places, chapters, letters).
Planted defect: a derive that gives two mocks the same slice must be caught.
Usage: mock_test_disjoint_v1_0_0.py BANK.json [--log FILE]"""
import json, subprocess, sys, os, tempfile, collections
H = os.path.dirname(os.path.abspath(__file__))
bankf = sys.argv[1]
lines = []
def log(x):
    print(x); lines.append(x)

def node(job):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(job, f); p = f.name
    r = subprocess.run(["nice", "-n", "10", "node", os.path.join(H, "mock_node_driver_v1_0_0.js"), p], capture_output=True, text=True)
    os.unlink(p)
    if r.returncode:
        raise SystemExit("node error: " + r.stderr[:500])
    return json.loads(r.stdout)

bank = json.load(open(bankf))["items"]
FAMOF = {x["id"]: x.get("family") for x in bank}
cnt = collections.Counter(x["type"] for x in bank if not x.get("family"))
inst = sum(len(x["instances"]) for x in bank if x["type"] == "numeric" and not x.get("family"))
fams = collections.Counter(x["family"] for x in bank if x.get("family"))
faminst = {f: sum(len(x["instances"]) for x in bank if x.get("family") == f) for f in fams}
log("families in the bank: %s templates, instances %s" % (dict(fams) or "none", faminst or "none"))
nfam = len(fams)
log("bank size: choice %d, numeric templates %d (instances %d), matching %d, ordering %d, fill %d; units %d" % (
    cnt["choice"], cnt["numeric"], inst, cnt["matching"], cnt["ordering"], cnt["fill"], len(bank)))
ids = [x["id"] for x in bank]
assert len(ids) == len(set(ids)), "duplicate bank ids"

def check(patch, ks):
    mocks = node({"bank": bankf, "patch": patch, "ops": [{"op": "derive", "k": k, "seed": 1000 + k} for k in ks]})
    return mocks

def disjoint(mocks):
    seen = {}; shared = []
    for m in mocks:
        for i in m["itemIds"]:
            if i in seen:
                shared.append((i, seen[i], m["k"]))
            seen[i] = m["k"]
    return shared

mocks = check("none", range(1, 9))
sh = disjoint(mocks)
log("mocks 1..8: items per mock %s; shared ids between mocks: %d" % (sorted(set(len(m["itemIds"]) for m in mocks)), len(sh)))
ok = (len(sh) == 0)
# structure per mock
bad = 0
for m in mocks:
    pf = lambda it: it["points"] if it["type"] in ("choice", "numeric") else (sum(it["rowPoints"]) if it["type"] == "matching" else (5 if it["type"] == "ordering" else sum(it["blankPoints"])))
    pts = sum(pf(it) for Q in m["questions"] for it in Q["items"])
    places = sum(len(it.get("correct", [0])) if it["type"] in ("matching", "ordering", "fill") else 1 for Q in m["questions"] for it in Q["items"])
    chs = collections.Counter(it["chapter"] for Q in m["questions"] if Q["q"] == 1 for it in Q["items"])
    allch = set(it["chapter"] for Q in m["questions"] for it in Q["items"])
    q1 = m["questions"][0]["items"]
    letters = set(it["correct"] for it in q1)
    shape = [len(Q["items"]) for Q in m["questions"]]
    pq1 = sorted(it["points"] for it in q1)
    pq2 = sorted(it["points"] for it in m["questions"][1]["items"])
    good = (pts == 100 and shape == [7, 8, 3, 3] and max(chs.values()) <= 2 and len(chs) == 6 and allch == set(range(1, 7)) and letters == {0, 1, 2, 3, 4}
            and pq1 == [3, 3, 3, 4, 4, 4, 4] and pq2 == [3] * 7 + [4] and places == 7 + 8 + 4 + 4 + 5 + 6)
    fc = collections.Counter(FAMOF.get(it["uid"].split("#")[0]) for it in m["questions"][1]["items"])
    comp = all(fc.get(f_, 0) == 1 for f_ in fams) and sum(v_ for k_, v_ in fc.items() if k_) == len(fams)
    good = good and comp
    bad += (not good)
    log("  mock %d: points %d, shape %s, q1 chapters %s, q1 right letters %s, q1 points %s, q2 points %s, places %d, Q2 families %s -> %s" % (
        m["k"], pts, shape, dict(sorted(chs.items())), "".join("ABCDE"[i] for i in sorted(letters)), pq1, pq2, places, dict((str(k_), v_) for k_, v_ in fc.items() if k_) or "none", "OK" if good else "BAD"))
ok = ok and bad == 0
# mock 9..16
m2 = check("none", range(9, 17))
ids18 = set(i for m in mocks for i in m["itemIds"])
new = [i for m in m2 for i in m["itemIds"] if i not in ids18]
log("mocks 9..16: ids not seen in mocks 1..8: %d (expected 0); mock 9 shares %d of %d ids with mocks 1..8" % (len(new), len(set(m2[0]["itemIds"]) & ids18), len(m2[0]["itemIds"])))
ok = ok and not new
# used units
used = set(i.split("#")[0] for i in ids18)
famused = sum(1 for i in ids18 if FAMOF.get(i.split("#")[0]))
log("family instances used by mocks 1..8: %d (all distinct: %s)" % (famused, len(set(i for i in ids18 if FAMOF.get(i.split("#")[0]))) == famused))
log("distinct bank units used by mocks 1..8: %d of %d; numeric instances used: %d of %d" % (len(used), len(bank), sum(1 for i in ids18 if "#" in i), inst))
# every unit of the bank used by exactly one mock? report unused
unused = [x["id"] for x in bank if x["id"] not in used]
log("bank units not used by mocks 1..8: %d" % len(unused))
disjoint_count = 8 if ok else 0
log("number of disjoint mocks (computed): %d" % disjoint_count)
# same seed same mock; different seed same items
a = check("none", [3]); b = check("none", [3])
c = node({"bank": bankf, "ops": [{"op": "derive", "k": 3, "seed": 99}]})
log("same k and seed twice identical: %s; other seed same item ids: %s; other seed different layout: %s" % (
    a == b, set(c[0]["itemIds"]) == set(a[0]["itemIds"]), c[0]["questions"] != a[0]["questions"]))
ok = ok and a == b and set(c[0]["itemIds"]) == set(a[0]["itemIds"]) and c[0]["questions"] != a[0]["questions"]
# planted defect
d = check("slice", range(1, 9))
sh2 = disjoint(d)
caught = len(sh2) > 0
log("PLANTED DEFECT two mocks of the same k share an item: shared ids found %d -> %s" % (len(sh2), "CAUGHT" if caught else "NOT CAUGHT"))
ok = ok and caught
log("DISJOINT TEST " + ("PASS" if ok else "FAIL"))
if "--log" in sys.argv:
    open(sys.argv[sys.argv.index("--log") + 1], "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
