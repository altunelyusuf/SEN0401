#!/usr/bin/env python3
"""sen0401_exam_reader_v12_control_check v1_0_0 - the lineage agent's own control of the answer sheet reader v1.2.0 on seed blocks the executor did not name. Usage: run. (a) the files of the readers v1.0.0 and v1.1.0, their measurements and the gap control v1.0.0 equal their committed blobs before the executor's commit 3af6697; (b) the gap control v1.1.0 on seeds 95000..95059 and 96000..96059 reads all three layouts with 0 BAD rows, 0 registration failures and a held share of at most 25 percent; (c) the reader's own measurement on the default layout (100 sheets, seeds 17000..): v1.2.0 has no silent wrong, no missed and no unflagged empty and its ok rows are at least 99 percent of v1.1.0's. Exit 1 on a FAIL."""
import hashlib, json, os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(D + "/../.."); fails = 0
def out(ok, m):
    global fails; fails += (not ok); print(("PASS  " if ok else "FAIL  ") + m)
def sh(*a): return subprocess.run(a, capture_output=True, text=True, cwd=D)
bad = []
for f in ("sen0401_exam_answersheet_v1_0_0.py", "sen0401_exam_answersheet_v1_1_0.py", "sen0401_exam_answersheet_measure_v1_0_0.py", "sen0401_exam_answersheet_measure_v1_1_0.py", "sen0401_exam_reader_gap_control_v1_0_0.py"):
    b = subprocess.run(["git", "-C", R, "show", "3af6697~1:08-tooling/exam/" + f], capture_output=True).stdout
    if hashlib.sha256(b).hexdigest() != hashlib.sha256(open(D + "/" + f, "rb").read()).hexdigest(): bad.append(f)
out(not bad, "the earlier reader, measurement and gap-control files equal their committed blobs before 3af6697 (differing: %s)" % bad)
for sb in ("95000", "96000"):
    r = sh(sys.executable, "sen0401_exam_reader_gap_control_v1_1_0.py", sb, "60", "--reader", "1.2.0"); print(r.stdout.strip())
    lines = [l for l in r.stdout.splitlines() if l.startswith("reader")]
    out(len(lines) == 3 and all("registration failures 0" in l and "BAD rows 0 on 0 sheets" in l for l in lines) and all(float(re.search(r"held [\d]+ = ([\d.]+) percent", l).group(1)) <= 25 for l in lines), "gap control v1.1.0 (reader 1.2.0), seeds %s..%d, 3 layouts: 0 BAD, 0 registration failures, held share <= 25 percent" % (sb, int(sb) + 59))
res = {}
for v in ("1_1_0", "1_2_0"):
    p = "/tmp/sen0401_rmeas_%s.json" % v; sh(sys.executable, "sen0401_exam_answersheet_measure_%s.py" % ("v" + v), "--sheets", "100", "--seed-base", "17000", "--json", p); res[v] = json.load(open(p))
a, b = res["1_1_0"], res["1_2_0"]; w = b["with_methods"]
out(w.get("silent_wrong", 0) == 0 and w.get("missed", 0) == 0 and w.get("empty_not_flagged", 0) == 0 and b["registration_failures"] == 0, "reader 1.2.0 on the default layout, 100 sheets: with methods %s, registration failures %d" % (w, b["registration_failures"]))
out(w["ok"] >= 0.99 * a["with_methods"]["ok"], "ok rows 1.2.0 %d against 1.1.0 %d (at least 99 percent)" % (w["ok"], a["with_methods"]["ok"]))
print("RESULT", "FAIL" if fails else "PASS"); sys.exit(1 if fails else 0)
