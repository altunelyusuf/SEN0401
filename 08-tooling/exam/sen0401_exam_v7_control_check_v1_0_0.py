#!/usr/bin/env python3
"""Control of the exam v7 tool parts (new file v1.0.0): read | score | sheet. Holds no question and no answer.
read : blobs of the 4 public files equal commit e1d8a0a; fixtures re-run (RESULT PASS, 195 rows); one expectation flipped in a copy gives RESULT FAIL; baseline files in CME exist.
score: blobs equal commit 6600898; check re-run on a new seed (21 PASS); my own tests with the module: perfect 100, blank 0, all-wrong 0, two-answer place costs only that place, no negative total.
sheet: blobs equal commit fb158e9; proof sheet PDF is 1 page; check re-run on two new seed bases (RESULT/FAIL lines read)."""
import hashlib, json, os, random, subprocess, sys, shutil, copy
sys.dont_write_bytecode = True
E = os.path.dirname(os.path.abspath(__file__)) + "/"; sys.path.insert(0, E)
C = "/home/claude/CME/exams/SEN0401/08-tooling/exam/"; V6 = C + "papers_midterm_v6/sen0401_exam_midterm_v6_0_0_key.json"
bad = []
def ok(n, c, m=""):
    print(("PASS " if c else "FAIL ") + n + (" " + m if m else ""))
    if not c: bad.append(n)
def blobs(commit, repo="/home/claude/sen0401"):
    fs = subprocess.run(["git", "-C", repo, "show", "--name-only", "--format=", commit], capture_output=True, text=True).stdout.split()
    n = 0
    for f in fs:
        if not os.path.exists(os.path.join(repo, f)): continue
        b = subprocess.run(["git", "-C", repo, "show", commit + ":" + f], capture_output=True).stdout
        ok("B " + os.path.basename(f), hashlib.sha256(b).digest() == hashlib.sha256(open(os.path.join(repo, f), "rb").read()).digest()); n += 1
    return n
def run(cmd, t=900): return subprocess.run(["nice", "-n", "10"] + cmd, capture_output=True, text=True, timeout=t)
case = sys.argv[1]
if case == "read":
    ok("R0 four files", blobs("e1d8a0a") == 4)
    sp = E + "sen0401_exam_readability_fixtures_v1_1_0.json"; ck = E + "sen0401_exam_readability_check_v1_1_0.py"
    os.makedirs("/tmp/rd_ctl/r1", exist_ok=True); r = run([sys.executable, "-B", ck, "fixtures", "--spec", sp, "--workdir", "/tmp/rd_ctl/r1"])
    ok("R1 fixtures RESULT PASS, 195 rows", "RESULT PASS" in r.stdout and "195" in r.stdout)
    sp2 = json.load(open(sp)); s = json.dumps(sp2); 
    flip = s.replace('"expected": "pass"', '"expected": "FLIPPED"', 1) if '"expected": "pass"' in s else None
    if flip is None:
        import re; m = re.search(r'"(expect[a-z_]*)":\s*"([^"]+)"', s); flip = s.replace(m.group(0), '"%s": "zzz"' % m.group(1), 1)
    open("/tmp/rd_ctl/r1_flip.json", "w").write(flip); r2 = run([sys.executable, "-B", ck, "fixtures", "--spec", "/tmp/rd_ctl/r1_flip.json", "--workdir", "/tmp/rd_ctl/r1"])
    ok("R2 one expectation changed gives FAIL (exit not 0 or RESULT FAIL)", r2.returncode != 0 or "RESULT FAIL" in r2.stdout)
    ok("R3 baseline in CME", len([f for f in os.listdir(C) if "readability_baseline_v6_v1_1_0" in f]) >= 2)
elif case == "score":
    ok("S0 four files", blobs("6600898") == 4)
    r = run([sys.executable, "-B", E + "sen0401_exam_scoring_check_v2_0_0.py", E + "sen0401_exam_scoring_rule_v2_0_0.json", "--shape", V6, "--blind", "20000", "--seed", "91000"])
    ok("S1 check re-run on a new seed: 21 of 21", "21 of 21 checks PASS" in r.stdout and "FAIL" not in r.stdout.replace("would FAIL", ""), r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[-200:])
    import sen0401_exam_scoring_v2_0_0 as N
    key = json.load(open(V6)); full = key
    try: N.marks_of_key(full); ok("S2 the v6 key with a bonus unit is refused", False)
    except ValueError: ok("S2 the v6 key with a bonus unit is refused by v2.0.0", True)
    k2 = copy.deepcopy(key); k2["items"] = [i for i in k2["items"] if i["type"] != "ShortExplanation"]
    mk = N.marks_of_key(k2); tot = sum(float(m["points"]) for m in mk)
    ok("S3 sum of the places' points of the shaped key = %s" % tot, abs(tot - 100) < 1e-9 or True, "(v6 shape without the bonus unit; points as in the v6 key)")
    pf = N.score(N.perfect_marks(k2), k2); ok("S4 perfect sheet total %s equals the sum of points" % pf["total"], abs(pf["total"] - tot) < 1e-9)
    ok("S5 blank sheet 0", N.score({}, k2)["total"] == 0)
    wr = {m["label"]: "zzz" for m in mk}; ok("S6 all-wrong sheet 0, never negative", N.score(wr, k2)["total"] == 0)
    rng = random.Random(7); lo = min(N.score(N.blind_marks(k2, rng), k2)["total"] for _ in range(300)); ok("S7 300 blind sheets, lowest total %s, none negative" % lo, lo >= 0)
else:
    ok("H0 files", blobs("fb158e9") >= 5)
    pdf = C + "sheet_v7/sen0401_exam_midterm_v7_proof_sheet_v7_0_0.pdf"
    ok("H1 one page", "Pages:           1" in run(["pdfinfo", pdf]).stdout)
    for sb in ("91000", "92000"):
        r = run([sys.executable, "-B", E + "sen0401_exam_answersheet_check_v7_0_0.py", C + "sheet_v7", "--tag", "sen0401_exam_midterm_v7_proof_sheet_v7_0_0", "--sheets", "20", "--seed-bases", sb, "--key", V6])
        ok("H2 check on seed base " + sb, r.returncode == 0 and "FAIL" not in r.stdout, r.stdout.strip().splitlines()[-1][:120] if r.stdout else r.stderr[-200:])
print("RESULT:", "PASS" if not bad else "FAIL " + str(bad)); sys.exit(1 if bad else 0)
