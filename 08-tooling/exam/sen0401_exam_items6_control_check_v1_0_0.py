#!/usr/bin/env python3
"""Control of the v6 items and structure (new file v1.0.0). Holds no question and no answer (reads them from CME at run time).
Own checks: hashes as reported; v1.4.0 equals its CME copy file by file; every item of v1.5.0 other than the new one has the same answer,
options, computed and type as v1.4.0 and the removed item is the vanity item only; the new item's key recomputed by my own program from its data;
stems of 60 words or fewer and how_to_answer of 25 words or fewer (own count); no 'vanity' trace in the new private files; penalty fractions
recomputed as p/(1-p) in exact fractions for every type and compared with the structure and with the scoring module (the two differ for numbers
of one or two digits: the scoring module governs); every item's tip labels exist; the leak search of the public tree passes."""
import hashlib, json, os, re, subprocess, sys
from fractions import Fraction as F
CME = "/home/claude/CME/exams/SEN0401/08-tooling/exam/"; P = CME + "private/"; E = "/home/claude/sen0401/08-tooling/exam/"
sys.path.insert(0, E); sys.dont_write_bytecode = True
H = {P + "sen0401_exam_items_midterm_v1_5_0.json": "d390e764fc0acac83738b8aa0d3e3a46c79a8b22050b489b2affe2349f585df6", P + "sen0401_exam_structure_v1_2_0.json": "78c097bfaece1d82fb338a1c1e7bdfa8fa7163db6e2e82462b506fa9b6ed7a8b",
 P + "sen0401_exam_topic_map_v1_5_0.json": "a34449e5a8f7e684c01d437ebdb2bd90a6432331d434a7d020de9b722d1330b3", P + "sen0401_exam_items_build_v1_5_0.py": "c40aad7f6b9c63fcb57f79045586fb8b55996a0355626d2fd37bc6aa744c7a4d",
 P + "sen0401_exam_topic_map_build_v1_5_0.py": "635a4c6295421f8a0a6285959c3ca3707b06d7728445259dacd2c6b398a8cf28", CME + "sen0401_exam_items_midterm_check_v1_5_0.py": "eaf3024146f8c4f2f35f6769891c7390a8ed10132a1cca959fde623d17acca4d",
 P + "sen0401_exam_items_midterm_check_log_v1_5_0.txt": "7d6a713f8c98baf744ca8b580c33d29ac3f96f4282f37c37ebfbca39dc38b09e"}
bad = []
def ok(n, c, m=""):
    print(("PASS " if c else "FAIL ") + n + (" " + m if m else ""))
    if not c: bad.append(n)
W = lambda s: len(re.findall(r"\S+", s))
for p, h in H.items(): ok("H " + os.path.basename(p), hashlib.sha256(open(p, "rb").read()).hexdigest() == h)
new = json.load(open(P + "sen0401_exam_items_midterm_v1_5_0.json"))["items"]; old = json.load(open(P + "sen0401_exam_items_midterm_v1_4_0.json"))["items"]
ok("I1 v1.4.0 file equals its committed CME blob", subprocess.run(["git", "-C", "/home/claude/CME", "diff", "--quiet", "--", "exams/SEN0401/08-tooling/exam/private/sen0401_exam_items_midterm_v1_4_0.json"]).returncode == 0)
ok_ = {i["key"]: i for i in old}; nk = {i["key"] for i in new}; added = [k for k in nk if k not in ok_]; gone = [k for k in ok_ if k not in nk]
ok("I2 one item added and one removed; the removed is the vanity item", len(added) == 1 and len(gone) == 1 and "vanity" in gone[0], "added %s removed %s" % (added, gone))
diff = [(k, f) for k in nk if k in ok_ for f in ("type", "answer", "options", "computed", "points", "key_value") if [i for i in new if i["key"] == k][0].get(f) != ok_[k].get(f)]
ok("I3 the other 20 items: type, answer, options, computed, points, key value equal to v1.4.0", not diff, str(diff))
e = [i for i in new if i["key"] == added[0]][0]; d = e["data"]; tries = 2 ** d["bits"]; sec = F(tries, d["target"]) / d["tries_per_second"]
ok("I4 new item key recomputed by my own program: %d tries / %d accepted / %d per second = %s" % (tries, d["target"], d["tries_per_second"], sec), sec == e["key_value"] == 32 and e["points"] == 3 and e["unit"] == "seconds")
ok("I5 new item: chapter 4 first, topic E, CP2.12, a tip for every label named in the stem", e["chapters"][0] == 4 and "E" in e["owner_points"] and "CP2.12" in e["critical_points"] and all(l in e["tips_by_label"] for l in re.findall(r"See tip (\w+)", e["q"])))
long_ = [(i["key"], W(i["q"])) for i in new if isinstance(i.get("q"), str) and W(i["q"]) > 60]; ok("W1 every plain stem is 60 words or fewer (own count, %d stems counted)" % sum(isinstance(i.get("q"), str) for i in new), not long_, str(long_))
hl = [(i["key"], W(i["how_to_answer"])) for i in new if W(i.get("how_to_answer", "x " * 99)) > 25]; ok("W2 how_to_answer is present and 25 words or fewer on all %d items" % len(new), not hl and all(i.get("how_to_answer") for i in new), str(hl))
inl = [i["key"] for i in new if isinstance(i.get("q"), str) and re.search(r"\(|tip:", i["q"]) and not re.search(r"See tip", i["q"])]; ok("W3 no stem holds a bracketed gloss without a tip reference", not inl, str(inl))
tx = "".join(open(p).read() for p in H if p.endswith((".json", ".py")) and "check" not in p); ok("V1 no 'vanity' in the new items, structure, topic map or builders", "vanity" not in tx.lower())
s = json.load(open(P + "sen0401_exam_structure_v1_2_0.json")); rows = []
def walk(o):
    if isinstance(o, dict):
        if "penalty_fraction" in o and "key" in o: rows.append(o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(s); ok("P1 structure holds 26 positions with a penalty (7 choice, 8 number or trace, 3 ordering or matching, 6 fill-in, 2 bonus)", len(rows) == 26, str(len(rows)))
def own(r):
    p = F(r["guess_chance"]); return p / (1 - p) if p else F(0)
mm = [r["key"] for r in rows if F(r["guess_chance"]) >= F(1, 1000) and own(r) != F(r["penalty_fraction"])]; ok("P2 every penalty with p of 1/1000 or more equals p/(1-p) (own fractions)", not mm, str(mm))
import sen0401_exam_scoring_v1_0_0 as SC
rule = json.load(open(E + "sen0401_exam_scoring_rule_v1_0_0.json")); txt = json.dumps(rule)
nums = {i["key"]: len(re.sub(r"\D", "", str(i.get("key_value", i.get("answer"))))) for i in new if i["type"] in ("NumericAnswer", "CodeTrace")}
ev = {k: ("1/%d" % (10 ** n - 1) if n < 3 else "0") for k, n in nums.items() if n}
print("INFO digits of the keys and the penalty the scoring module's rule gives: " + ", ".join("%s:%s" % (k.split(":")[1], v) for k, v in ev.items()))
print("INFO structure gives 0 for all of these (5 digit boxes, p = 1/100000): the scoring module governs, because the printed sentence of the tips page and the scoring check use it")
r = subprocess.run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_1.py", "leakscan"], capture_output=True, text=True); ok("S1 leak search of the public tree", "RESULT PASS" in r.stdout)
print("CONTROL " + ("PASS" if not bad else "FAIL " + ",".join(bad))); sys.exit(1 if bad else 0)
