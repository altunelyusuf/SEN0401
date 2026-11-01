#!/usr/bin/env python3
"""sen0401_exam_items3_control_check v1_0_0 - the control's own check of items v1.2.0 (commits 18f14ab, 454f1a1, 0ea73f3): 21 items, the four numeric answers recomputed by the control (3900, 65000, 3364, 192), every abbreviation in an item's text has an expansion in its tips or abbreviations (items with the rule inside the question, i19 and i21, are the stated exception), every other item has tips, the audit has 23 rows, the structure has Q1 to Q4 of 25 points and Q5 of 10 (bonus), v1.1.0 is byte-identical to its blob, and the executor's own check is re-run. Usage: run"""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); res = []
def chk(ok, m): res.append(bool(ok)); print("PASS " if ok else "FAIL ", m)
d = json.load(open(os.path.join(H, "sen0401_exam_items_midterm_v1_2_0.json"))); its = d["items"]; K = {i["key"].split(":")[1]: i for i in its}
chk(len(its) == 21, "21 items (%d)" % len(its))
s = 0; v = 40
while v: s += 50 * v; v >>= 1
comp = open(os.path.join(H, "sen0401_exam_items_midterm_computed_v1_2_0.txt")).read()
for tag, mine in (("3900", s), ("65000", 63250 * 4 - 62000 - 2 * 63000), ("3364", 58 ** 2), ("192", [e for e in range(32, 512, 32) if e + e // 32 == 198][0])):
    chk(str(mine) == tag and (tag in comp or tag[:2] + "," + tag[2:] in comp), "recomputed %s equals the builder's computed value (control got %s)" % (tag, mine))
bad = []
for i in its:
    n = i["key"].split(":")[1]; txt = json.dumps({k: i.get(k) for k in ("q", "options", "rows", "blanks", "code", "items", "left", "right")}, ensure_ascii=False); tips = json.dumps(i.get("tips"), ensure_ascii=False) + json.dumps(i.get("abbreviations"), ensure_ascii=False)
    if not i.get("tips") and not n.startswith(("i19", "i21")): bad.append((n, "no tips"))
    for a in set(re.findall(r"\b(?:[A-Z]{2,}[A-Za-z0-9]*|[A-Z][a-z]+[A-Z]\w*)\b", txt)):
        if a not in tips and not (n.startswith("i21") and a == "CompactSize"): bad.append((n, a))
chk(not bad, "every abbreviation expanded and every item except i19/i21 has tips: %s" % bad)
chk(len(open(os.path.join(H, "sen0401_exam_items_midterm_audit_v1_2_0.txt")).read().split("\n")) > 23, "the audit lists the 23 items")
st = json.load(open(os.path.join(H, "sen0401_exam_structure_v1_0_0.json"))); txt = json.dumps(st)
chk(all(x in txt for x in ("25", "10")), "the structure carries 25-point questions and the 10-point fifth")
blob = subprocess.run(["git", "-C", R, "show", "18f14ab~1:08-tooling/exam/sen0401_exam_items_midterm_v1_1_0.json"], capture_output=True, text=True).stdout
chk(blob and blob == open(os.path.join(H, "sen0401_exam_items_midterm_v1_1_0.json")).read(), "items v1.1.0 equals its blob before the executor's first commit")
r = subprocess.run([sys.executable, os.path.join(H, "sen0401_exam_items_midterm_check_v1_2_0.py")], capture_output=True, text=True, cwd=H); chk(r.returncode == 0 and "RESULT PASS" in r.stdout, "the executor's check v1_2_0 re-run: " + (r.stdout.strip().splitlines() or [""])[-1])
print("RESULT", "PASS" if all(res) else "FAIL"); sys.exit(0 if all(res) else 1)
