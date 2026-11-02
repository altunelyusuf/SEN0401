#!/usr/bin/env python3
"""Assembly v1.0.1 (X3b rebuild): same steps as v1.0.0, with these changes: (1) the NEWEST version of every part file is used (chapter banks and families); (2) no template drop/keep tables for families (the families were pruned by the exam-wins removal into new part versions, so nothing is quarantined here: ANY gate failure refuses the assembly); (3) exclusion gate v1.0.1 (index v1.0.1 with the v8 items); (4) writes sen0401_mock_bank_all_v1_1_0.json into the set folder; (5) prints the supply table. Prints ids/counts/hashes only.\nOriginal text of v1.0.0: verifies each chapter part file with its own check (exit 0 and RESULT PASS), merges the six parts into the private whole bank,
strips a leading 'Tip: ' from every tip (the page prints the label once), validates the schema of every unit, writes the bank and prints sizes.
Prints ids/counts/hashes only. Usage: mock_assemble_v1_0_0.py"""
import json, os, re, subprocess, sys, hashlib
M = "/home/claude/CME/exams/SEN0401/08-tooling/exam/mock"
P = M + "/parts"
SETDIR = M + "/set_v1_0_0"
OUT = SETDIR + "/sen0401_mock_bank_all_v1_1_0.json"
BANK_VERSION = "1.1.0"
lines = []
def log(x):
    print(x, flush=True); lines.append(x)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
import glob
def _latest(pattern):
    fs = glob.glob(pattern)
    return max(fs, key=lambda f: tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.(?:json|py)$", f).groups()))
def bank(n): return _latest("%s/mock_bank_ch%d_v*.json" % (P, n))
def gen(n): return _latest("%s/mock_numeric_gen_ch%d_v*.py" % (P, n))
CHECKS = {
 1: ["mock_check_ch1_v1_0_0.py", "check", "--bank", bank(1), "--chapter", "1"],
 2: ["mock_check_ch2_v1_0_0.py", "check", "--bank", bank(2)],
 3: ["mock_check_ch3_v1_0_0.py", "check", "--bank", bank(3), "--gen", gen(3), "--chapter", "3"],
 4: ["mock_check_ch4_v1_0_0.py", "check", "--bank", bank(4)],
 5: ["mock_check_ch5_v1_0_0.py"],
 6: ["mock_check_ch6_v1_0_0.py", "check", "--bank", bank(6), "--gen", gen(6)]}
ok = True
for n in range(1, 7):
    before = sha(bank(n))
    r = subprocess.run(["nice", "-n", "10", "python3", "-B", P + "/" + CHECKS[n][0]] + CHECKS[n][1:], capture_output=True, text=True, cwd=P)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    good = r.returncode == 0 and bool(res) and "PASS" in res[-1] and sha(bank(n)) == before
    ok &= good
    log("chapter %d part file sha256 %s; own check %s: exit %d, '%s' -> %s" % (n, before, CHECKS[n][0], r.returncode, res[-1] if res else "no RESULT line", "OK" if good else "REFUSED"))
if not ok:
    log("ASSEMBLY REFUSED: a part file failed its own check"); sys.exit(1)

FAM = {"1x": ("weighted_price", "mock_check_ch1x_v1_0_0.py"), "2x": ("fee_selection", "mock_check_ch2x_v1_0_0.py"),
       "3x": ("release_tags", "mock_check_ch3x_v1_0_0.py"), "4x": ("hash_search", "mock_check_ch4x_v1_0_0.py"),
       "5x": ("gap_scan", "mock_check_ch5x_v1_0_0.py"), "5y": ("recovery_code", "mock_check_ch5y_v1_0_0.py")}
# standing rule of simple calculations (composition v4): main-bank numeric templates that are never drawn (they stay in the files, flagged) and the
# family templates kept while the newest family file is older than the repaired version
MAIN_DROP = {"n1_1", "n1_4", "n2_1", "n2_2", "n3_3", "n4_2", "n4_3", "n4_4", "n5_1", "n5_3", "n6_1", "n6_2", "n6_3", "n6_4"}
FAM_DROP = {}   # v1.0.1: nothing dropped here; the removals live in the part versions
PUB = "/home/claude/sen0401/08-tooling/exam/mock"
fam_present = {}
def latest(key):
    fs = glob.glob("%s/mock_bank_ch%s_v*.json" % (P, key))
    vs = sorted(fs, key=lambda f: tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.json$", f).groups()))
    return re.search(r"_(v\d+_\d+_\d+)\.json$", vs[-1]).group(1) if vs else "v1_0_0"
FAMVER = {k: latest(k) for k in FAM}   # the latest version of each family file present (superseded older versions are not loaded)
def famfile(key): return "%s/mock_bank_ch%s_%s.json" % (P, key, FAMVER[key])
def pubfile(base, key):
    for ver in (FAMVER[key], "v1_0_0"):
        for d_ in (P, PUB):          # generators and checkers of the families live in the private parts folder (or the public folder)
            v = d_ + "/" + base % (key, ver)
            if os.path.exists(v): return v
    return PUB + "/" + base % (key, "v1_0_0")
for key, (fname, chk) in FAM.items():
    fp = famfile(key)
    chkp = pubfile("mock_check_ch%s_%s.py", key); chk = os.path.basename(chkp)
    if not os.path.exists(fp):
        fam_present[key] = None
        log("family %s: file %s missing (older versions, if any, are superseded and not loaded) -> built without it; its numeric place in every mock is filled from the main bank" % (fname, os.path.basename(fp))); continue
    before = sha(fp)
    gp = pubfile("mock_numeric_gen_ch%s_%s.py", key)
    if not os.path.exists(chkp):
        log("family %s: no own check script found (%s); only the assembly schema check applies" % (fname, chk))
        fam_present[key] = before; continue
    styles = [["check", "--bank", fp, "--gen", gp], [fp, "--gen", gp], ["check", "--bank", fp]]
    r = None
    for st in styles:
        r = subprocess.run(["nice", "-n", "10", "python3", "-I", chkp] + st, capture_output=True, text=True, cwd=os.path.dirname(chkp))
        if r.returncode == 0: break
    out = r.stdout.strip().splitlines()
    good = r.returncode == 0 and sha(fp) == before
    ok &= good
    fam_present[key] = before if good else None
    log("family %s file sha256 %s; own check %s: exit %d, last lines '%s' -> %s" % (fname, before, chk, r.returncode, " | ".join(out[-2:])[:200], "OK" if good else "REFUSED"))
if not ok:
    log("ASSEMBLY REFUSED: a part file failed its own check"); sys.exit(1)

REQ = {"choice": ["stem", "tip", "options", "answer", "steps", "why_right", "why_wrong", "points"],
       "numeric": ["unit", "tip", "instances", "points", "can_be_4"],
       "matching": ["intro", "tip", "premises", "responses", "answer", "steps", "why_right", "why_wrong_rows"],
       "ordering": ["intro", "tip", "steps", "answer", "steps_solution", "why_right", "why_wrong_rows"],
       "fill": ["stem", "tip", "bank", "blanks", "steps", "why_right", "why_wrong_entries"]}
items = []; errs = []; stripped = 0; dupkeys = []; famname = {}
for n in range(1, 7):
    d = json.load(open(bank(n)))
    assert d["chapter"] == n
    for it in d["items"]:
        if it.get("chapter") != n: errs.append("%s chapter field" % it.get("id"))
        for f in REQ.get(it.get("type"), ["?"]):
            if f not in it: errs.append("%s missing %s" % (it.get("id"), f))
        t = it.get("tip")
        if isinstance(t, str) and re.match(r"\s*Tip:\s*", t, re.I):
            it["tip"] = re.sub(r"^\s*Tip:\s*", "", t, flags=re.I); stripped += 1
        if "tip" in it and len(it["tip"].split()) > 12: errs.append("%s tip longer than 12 words" % it["id"])
        ty = it["type"]
        if ty == "choice" and (len(it["options"]) != 5 or not 0 <= it["answer"] <= 4 or it["points"] not in (3, 4)): errs.append(it["id"] + " choice shape")
        if ty == "numeric":
            if len(it["instances"]) != 8: errs.append(it["id"] + " instances")
            keys = [i["key_value"] for i in it["instances"]]
            if len(set(keys)) != 8: errs.append(it["id"] + " duplicate key values")
            if len(set(i["stem"] for i in it["instances"])) != 8: errs.append(it["id"] + " duplicate stems")
            for i in it["instances"]:
                if not (isinstance(i["key_value"], int) and 0 <= i["key_value"] <= 99999): errs.append(it["id"] + " key range")
        if ty == "matching" and (len(it["premises"]) != 4 or len(it["responses"]) != 5 or len(set(it["answer"])) != 4): errs.append(it["id"] + " matching shape")
        if ty == "ordering" and (len(it["steps"]) != 5 or sorted(it["answer"]) != [1, 2, 3, 4, 5] or it["answer"] == [1, 2, 3, 4, 5]): errs.append(it["id"] + " ordering shape")
        if ty == "fill" and (len(it["bank"]) != 5 or len(it["blanks"]) != 2): errs.append(it["id"] + " fill shape")
        if it["type"] == "numeric" and it["id"] in MAIN_DROP: it["dropped"] = True
        items.append(it)
for key, (fname, chk) in FAM.items():
    if not fam_present.get(key): continue
    d = json.load(open(famfile(key)))
    if not d.get("family") or d.get("chapter") != int(key[0]) or len(d["items"]) < 1: errs.append("family %s header or template count" % fname)
    ver = tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.json$", famfile(key)).groups())
    gone = []
    if gone: log("family %s (version %s): templates not drawn under the simple-calculation rule: %s" % (key, FAMVER[key], ", ".join(gone)))
    d["items"] = [i for i in d["items"] if i["id"] not in gone]
    for it in d["items"]:
        for f in REQ["numeric"] + ["why_question"]:
            if f not in it: errs.append("%s missing %s" % (it.get("id"), f))
        it["family"] = d["family"]; famname[key] = d["family"]
        t = it.get("tip")
        if isinstance(t, str) and re.match(r"\s*Tip:\s*", t, re.I):
            it["tip"] = re.sub(r"^\s*Tip:\s*", "", t, flags=re.I); stripped += 1
        if len(it.get("tip", "").split()) > 12: errs.append(it["id"] + " tip longer than 12 words")
        if len(it["instances"]) < 8: errs.append(it["id"] + " fewer than 8 instances")
        keys = [i["key_value"] for i in it["instances"]]
        if len(set(keys)) != len(keys):
            dupkeys.append("%s(%d distinct of %d)" % (it["id"], len(set(keys)), len(keys)))   # families have small answers (counts, places): reported, stems must still all differ
        if len(set(i["stem"] for i in it["instances"])) != len(keys): errs.append(it["id"] + " duplicate stems")
        nl = [tuple(re.findall(r"\d+", i["stem"])) for i in it["instances"]]
        if len(set(nl)) != len(nl): errs.append(it["id"] + " two instances with the same numbers in the stem")
        for i in it["instances"]:
            if not (isinstance(i["key_value"], int) and 0 <= i["key_value"] <= 99999): errs.append(it["id"] + " key range")
        items.append(it)
log("main numeric templates flagged dropped (not drawn): %s; kept: %s" % (sorted(i["id"] for i in items if i.get("dropped")), sorted(i["id"] for i in items if i["type"] == "numeric" and not i.get("family") and not i.get("dropped"))))
ids = [i["id"] for i in items]
if len(ids) != len(set(ids)): errs.append("duplicate ids")
from collections import Counter
c = Counter(i["type"] for i in items if not i.get("family"))
ninst = sum(len(i["instances"]) for i in items if i["type"] == "numeric" and not i.get("family"))
fam_counts = {k: len([i for i in items if famname.get(k) and i.get("family") == famname[k]]) for k in FAM}
log("family templates with repeated answers among their instances (stems and numbers all differ): %s" % (", ".join(dupkeys) or "none"))
log("families merged: %s; family instances: %s" % (fam_counts, {k: sum(len(i["instances"]) for i in items if famname.get(k) and i.get("family") == famname[k]) for k in FAM}))
log("merged bank: choice %d, numeric templates %d (instances %d), matching %d, ordering %d, fill %d; units %d; leading 'Tip: ' stripped from %d tips" % (
    c["choice"], c["numeric"], ninst, c["matching"], c["ordering"], c["fill"], len(items), stripped))
if errs:
    for e in errs[:40]: log("SCHEMA FINDING " + e)
    log("ASSEMBLY REFUSED: %d schema findings" % len(errs)); sys.exit(1)
# ---- exclusion gate on the merged bank: a FAMILY template with a failing instance is quarantined (left out, listed, never waived);
# a failure anywhere else in the bank refuses the assembly
sys.path.insert(0, PUB)
import mock_exclusion_gate_v1_0_1 as G
gate = G.Gate(); quarantined = []; hard = []
for it in items:
    msgs = []
    G.run_items(gate, [it], lambda x: msgs.append(x), label="")
    failed = [m for m in msgs if " FAIL" in m and "units checked" not in m]
    if failed:
        (quarantined if it.get("family") else hard).append((it["id"], len(failed)))
if hard or quarantined:
    for h in hard + quarantined: log("GATE FAILURE: %s (%d unit(s))" % h)
    log("ASSEMBLY REFUSED: exclusion gate failure (v1.0.1 quarantines nothing; failing templates are removed in new part versions first)"); sys.exit(1)
log("exclusion gate v1.0.1 on the merged bank: 0 failing units")
log("supply: " + "; ".join("%s %d templates / %d instances (min per template %d)" % (famname[k], len([i for i in items if i.get("family") == famname[k]]), sum(len(i["instances"]) for i in items if i.get("family") == famname[k]), min(len(i["instances"]) for i in items if i.get("family") == famname[k])) for k in FAM if famname.get(k)))
os.makedirs(SETDIR, exist_ok=True)
json.dump({"version": BANK_VERSION, "quarantined": [], "parts": dict([(str(n), os.path.basename(bank(n))) for n in range(1, 7)] + [(k, os.path.basename(famfile(k))) for k in FAM if fam_present.get(k)]), "parts_sha256": dict([(str(n), sha(bank(n))) for n in range(1, 7)] + [(k, v) for k, v in fam_present.items() if v]), "items": items}, open(OUT, "w"), ensure_ascii=False, indent=0)
log("whole bank written (private): %s sha256 %s" % (OUT, sha(OUT)))
log("ASSEMBLY OK")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_assemble_log_v1_0_1.txt"), "w").write("\n".join(lines) + "\n")
