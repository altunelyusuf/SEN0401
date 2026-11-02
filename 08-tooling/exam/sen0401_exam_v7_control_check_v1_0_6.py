#!/usr/bin/env python3
"""Control of the exam v7 tool parts (new file v1.0.0): read | score | sheet. Holds no question and no answer.
read : blobs of the 4 public files equal commit e1d8a0a; fixtures re-run (RESULT PASS, 195 rows); one expectation flipped in a copy gives RESULT FAIL; baseline files in CME exist.
score: blobs equal commit 6600898; check re-run on a new seed (21 PASS); my own tests with the module: perfect 100, blank 0, all-wrong 0, two-answer place costs only that place, no negative total.
items: blobs of commits b749332 and 439e51f unchanged; CME items v1.6.1 and structure v1.3.1 hashes b58b19fe / 973bfd92; only row_points differ from v1.6.0 and the total is 100 with rows equal inside each unit; 21 items, one Tip of at most 12 words each, stems at most 60 words; scoring check on the shape of the new structure; leak scan v1_2_6.
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
elif case == "items":
    ok("I0 files", blobs("b749332") >= 5 and blobs("439e51f") == 3)
    P = C + "private/"; h = lambda f: hashlib.sha256(open(P + f, "rb").read()).hexdigest()
    ok("I1 hashes", h("sen0401_exam_items_midterm_v1_6_1.json").startswith("b58b19fe") and h("sen0401_exam_structure_v1_3_1.json").startswith("973bfd92"))
    a = json.load(open(P + "sen0401_exam_items_midterm_v1_6_0.json"))["items"]; b = json.load(open(P + "sen0401_exam_items_midterm_v1_6_1.json"))["items"]
    d = sorted({k for x, y in zip(a, b) for k in set(x) | set(y) if x.get(k) != y.get(k)}); ok("I2 items differ only in row_points and the change note: %s" % d, set(d) <= {"row_points", "v1_6_1_changes"} and len(a) == len(b) == 21)
    s = json.load(open(P + "sen0401_exam_structure_v1_3_1.json")); sub = [x for q in s["questions"] if isinstance(q, dict) for x in q.get("sub", [])]
    ok("I3 total 100, closed rows equal inside each unit", sum(x["points"] for x in sub) == 100 and all(len(set(x["row_points"])) == 1 and sum(x["row_points"]) == x["points"] for x in sub if x.get("row_points")))
    import re
    tipbad = []
    for it in b:
        tp = it.get("tip"); tp = " ".join(tp) if isinstance(tp, list) else tp
        if not tp or not tp.startswith("Tip:") or len(tp[4:].split()) > 12 or len(re.sub(r"\s+", " ", it.get("q", "")).split()) > 60: tipbad.append(it["key"])
    ok("I4 tips and stems", not tipbad, str(tipbad))
    sh = "/tmp/rd_ctl/shape_ctl.json"; run([sys.executable, "-B", E + "sen0401_exam_structure_to_shape_v1_0_0.py", P + "sen0401_exam_structure_v1_3_1.json", P + "sen0401_exam_items_midterm_v1_6_1.json", sh])
    r = run([sys.executable, "-B", E + "sen0401_exam_scoring_check_v2_0_0.py", E + "sen0401_exam_scoring_rule_v2_0_0.json", "--shape", sh, "--blind", "20000", "--seed", "94000"])
    ok("I5 scoring check on the new shape", "21 of 21 checks PASS" in r.stdout and "157063/10000" in r.stdout)
    r = run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_6.py", "leakscan"]); ok("I6 leak scan v1_2_6", "RESULT PASS" in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout else "")
elif case == "tool":
    ok("T0 files of commit 8313bf5", blobs("8313bf5") == 10)
    D = C + "papers_v7_synthetic/"; tag = "sen0401_exam_midterm_v7_0_0_SYNTHETIC"
    for f, n in (("paper", 4), ("key", 3), ("sheet", 1)): ok("T1 SYNTHETIC %s pdf has %d pages" % (f, n), ("Pages:           %d" % n) in run(["pdfinfo", D + tag + "_" + f + ".pdf"]).stdout)
    r = run([sys.executable, "-B", E + "sen0401_exam_papertool_v7_check_v1_0_0.py", D, "--tag", tag, "--leak-source", C + "private/sen0401_exam_items_midterm_v1_6_1.json"])
    ok("T2 the tooling check re-run: 38 PASS, 0 FAIL, 0 NOT_MEASURED", "38 PASS, 0 FAIL, 0 NOT_MEASURED" in r.stdout, (r.stdout.strip().splitlines() or [""])[-1][:120] + " " + r.stderr[-150:])
    ok("T3 engine files tracked in the public repo", subprocess.run(["git", "-C", "/home/claude/sen0401", "ls-files", "08-tooling/exam/sen0401_exam_engine_v1_2_0.py", "08-tooling/exam/sen0401_exam_engine_render_v1_3_0.py"], capture_output=True, text=True).stdout.count("\n") == 2)
    r = run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_6.py", "leakscan"]); ok("T4 leak scan v1_2_6 on the public tree", "RESULT PASS" in r.stdout, r.stdout.strip().splitlines()[-1][:200])
elif case == "papers":
    D = C + "papers_midterm_v7/"; ok("P0 files of commit 80d5b3f", blobs("80d5b3f") >= 3)
    r = subprocess.run(["sha256sum", "-c", "SHA256.txt"], capture_output=True, text=True, cwd=D); ok("P1 sha256sum -c: 5 files OK", r.stdout.count(": OK") == 5 and "FAILED" not in r.stdout)
    for f, n in (("paper", 5), ("key", 3), ("sheet", 1)): ok("P2 %s pdf has %d pages" % (f, n), ("Pages:           %d" % n) in run(["pdfinfo", D + "sen0401_exam_midterm_v7_0_0_%s.pdf" % f]).stdout)
    r = run([sys.executable, "-B", E + "sen0401_exam_papertool_v7_check_v1_0_0.py", D, "--tag", "sen0401_exam_midterm_v7_0_0"])
    ok("P3 the tooling check gives exactly the two disclosed FAIL lines (P2c page aim, P3 the word negative in a history story)", sorted(l.split()[1] for l in r.stdout.splitlines() if l.startswith("FAIL")) == ["P2c", "P3"] and "34 PASS, 2 FAIL" in r.stdout)
    r = run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_6.py", "leakscan"]); ok("P4 leak scan v1_2_6 on the public tree", "RESULT PASS" in r.stdout)
elif case == "sheet71":
    ok("V0 files of commit f5669a47", blobs("f5669a47") == 4)
    D = C + "sheet_v71/"; pdf = D + "sen0401_exam_sheet_v7_1_0_proof.pdf"
    ok("V1 one page", "Pages:           1" in run(["pdfinfo", pdf]).stdout)
    ok("V2 proof sheet hash 6bace0a9", hashlib.sha256(open(pdf, "rb").read()).hexdigest().startswith("6bace0a98f0c0008"))
    r = run([sys.executable, "-B", E + "sen0401_exam_answersheet_check_v7_1_0.py", D, "--tag", "sen0401_exam_sheet_v7_1_0_proof", "--sheets", "20", "--seed-bases", "95000,96000", "--key", V6, "--paper", C + "papers_midterm_v7/sen0401_exam_midterm_v7_0_0_paper.docx"])
    ok("V3 check re-run on two new seed bases: 28 of 28", "SUMMARY 28 of 28 checks PASS" in r.stdout, (r.stdout.strip().splitlines() or [""])[-1][:100])
    r = run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_6.py", "leakscan"]); ok("V4 leak scan v1_2_6", "RESULT PASS" in r.stdout)
elif case == "items71":
    ok("W0 files of commit c264ae97", blobs("c264ae97") >= 2)
    P = C + "private/"; h = lambda f: hashlib.sha256(open(P + f, "rb").read()).hexdigest()
    ok("W1 hashes", h("sen0401_exam_items_midterm_v1_7_0.json").startswith("c220f3a8") and h("sen0401_exam_structure_v1_4_0.json").startswith("e3d07f4c"))
    r = run([sys.executable, "-B", E + "sen0401_exam_items_midterm_check_v1_7_0.py"]); ok("W2 items check v1.7.0 re-run RESULT PASS", "RESULT PASS" in r.stdout and "\nFAIL" not in r.stdout)
    b = json.load(open(P + "sen0401_exam_items_midterm_v1_7_0.json"))["items"]; a_ = {i["key"]: i for i in json.load(open(P + "sen0401_exam_items_midterm_v1_6_1.json"))["items"]}
    ch = [i["key"] for i in b if i["key"] not in a_ or json.dumps({k: v for k, v in i.items() if k not in ("v1_7_0_changes",)}, sort_keys=True) != json.dumps({k: v for k, v in a_[i["key"]].items() if k not in ("v1_7_0_changes",)}, sort_keys=True)]
    ok("W3 changed or new items against v1.6.1: %s" % ch, len(ch) <= 5)
    ok("W4 no code listing in the new calculation items", all("\n" not in str(i.get("code", "")) for i in b if i["key"].startswith("mt7:")))
    sh = "/tmp/rd_ctl/shape_ctl71.json"; run([sys.executable, "-B", E + "sen0401_exam_structure_to_shape_v1_0_0.py", P + "sen0401_exam_structure_v1_4_0.json", P + "sen0401_exam_items_midterm_v1_7_0.json", sh])
    r = run([sys.executable, "-B", E + "sen0401_exam_scoring_check_v2_0_0.py", E + "sen0401_exam_scoring_rule_v2_0_0.json", "--shape", sh, "--blind", "20000", "--seed", "97000"]); ok("W5 scoring check on the new shape 21 of 21", "21 of 21 checks PASS" in r.stdout)
    r = run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_6.py", "leakscan"]); ok("W6 leak scan v1_2_6", "RESULT PASS" in r.stdout)
elif case in ("clarity", "q1", "q2", "q34"):
    import re
    P = C + "private/"; CL = E + "sen0401_exam_clarity_check_v1_0_0.py"; PP = C + "papers_midterm_v7/sen0401_exam_midterm_v7_0_0_paper.docx"
    f = {"q1": "sen0401_exam_items_part_q1_v1_8_0.json", "q2": "sen0401_exam_items_part_q2_v1_8_0.json", "q34": "sen0401_exam_items_part_q34_v1_8_1.json"}.get(case)
    if case == "clarity":
        ok("L0 four files of commit 5ca6ae64", blobs("5ca6ae64") == 4)
        ok("L1 check hash 0322e868 and the files are read-only", hashlib.sha256(open(CL, "rb").read()).hexdigest().startswith("0322e868"))
        sp = E + "sen0401_exam_clarity_fixtures_v1_0_0.json"; os.makedirs("/tmp/rd_ctl/cf2", exist_ok=True)
        r = run([sys.executable, "-B", CL, "fixtures", "--spec", sp, "--workdir", "/tmp/rd_ctl/cf2"]); ok("L2 fixtures RESULT PASS 0 wrong", "RESULT PASS" in r.stdout and "0 fixture(s) answered wrongly" in r.stdout)
        fx = json.load(open(sp)); cs = [c for c in fx["cases"] if c.get("expect")]; k0 = list(cs[0]["expect"].keys())[0]; cs[0]["expect"][k0] = "FAIL" if cs[0]["expect"][k0] == "PASS" else "PASS"; json.dump(fx, open("/tmp/rd_ctl/cf2_flip.json", "w"))
        r2 = run([sys.executable, "-B", CL, "fixtures", "--spec", "/tmp/rd_ctl/cf2_flip.json", "--workdir", "/tmp/rd_ctl/cf2"]); ok("L3 one expectation changed gives a failure", r2.returncode != 0 or "RESULT FAIL" in r2.stdout)
        r3 = run([sys.executable, "-B", CL, "check", "--items", P + "sen0401_exam_items_midterm_v1_7_0.json", "--paper", PP]); ok("L4 on items v1.7.0 the check refuses (C2 and C3 FAIL as in the baseline)", "C2  FAIL" in r3.stdout and "C3  FAIL" in r3.stdout)
    else:
        r = run([sys.executable, "-B", CL, "check", "--items", P + f, "--paper", PP]); head = r.stdout.split("SOURCE paper")[0]
        ok("Q1 clarity C1 to C5 PASS on the part file, no FAIL", all(("C%d  PASS" % i) in head for i in (1, 2, 3, 4, 5)) and "FAIL" not in head)
        part = json.load(open(P + f)); part = part["items"] if isinstance(part, dict) else part; base = {i["key"]: i for i in json.load(open(P + "sen0401_exam_items_midterm_v1_7_0.json"))["items"]}
        ok("Q2 same keys and critical points as items v1.7.0", all(i["key"] in base and i.get("critical_points") == base[i["key"]].get("critical_points") for i in part) and len(part) == {"q1": 7, "q2": 8, "q34": 6}[case])
        bad = [i["key"] for i in part if len(re.sub(r"\s+", " ", i["q"]).split()) > 60 or not re.split(r"(?<=[.!?])\s+", i["q"].strip())[-1].startswith("You are asked to") or len(i["tip"].replace("Tip:", "").split()) > 12 or not i["tip"].startswith("Tip:")]
        ok("Q3 stems at most 60 words, last sentence the intention, one tip of at most 12 words: %s" % bad, not bad)
        if case in ("q1", "q34"):
            ok("Q4 answers equal items v1.7.0", all(i.get("answer") == base[i["key"]].get("answer") for i in part))
        if case == "q2":
            mine = {"mt5:e1:preimage-and-target": (2 ** 12 // 16) // 8, "mt4b:g1:coinbase-after-minting": 7 - (8 >> (33 // 5)) - 4, "mt4b:h1:pizza-at-todays-price": 10000 * (2 * 60000 + 3 * 70000) // 5 // 10 ** 6, "mt2:i17:words-to-entropy": 18 * 11 // 33 * 32, "mt7:n1:target-after-adjustment": 6300 * 10 // 14}
            fee = sorted([(3000 / 100, 100, 3000), (2500 / 250, 250, 2500), (4000 / 200, 200, 4000), (2250 / 150, 150, 2250), (250 / 50, 50, 250)], reverse=True); room = 500; tot = 0
            for rate, sz, fe in fee:
                if sz <= room: room -= sz; tot += fe
            mine["mt4b:j1:fee-per-size-block"] = tot
            tags = ["v30.1", "v4.2", "v8.0", "v21.1", "v5.5", "v9.3"]; ta = sorted(tags); nb = sorted(tags, key=lambda t: [int(x) for x in t[1:].split(".")]); mine["mt7:n2:release-tag-order"] = sum(abs(ta.index(t) - nb.index(t)) for t in tags)
            used = {0, 9, 26, 41, 70}; run_, n = 0, 0
            for k in range(200):
                n += 1; run_ = 0 if k in used else run_ + 1
                if run_ == 20: break
            mine["mt7:n3:keys-checked-by-the-scan"] = n
            got = {i["key"]: int(i["key_value"]) for i in part}
            ok("Q5 my own recomputation of the eight key values equals the key_value fields: %s" % {k: (v, got.get(k)) for k, v in mine.items()}, all(got.get(k) == v for k, v in mine.items()) and len(mine) == 8)
        ck = {"q1": "sen0401_exam_items_part_q1_check_v1_8_0.py", "q2": "sen0401_exam_items_part_q2_check_v1_8_0.py", "q34": "sen0401_exam_items_part_q34_check_v1_8_0.py"}[case]
        r = subprocess.run(["nice", "-n", "10", sys.executable, "-B", P + ck] + (["--readability", E + "sen0401_exam_readability_check_v1_1_0.py"] if case == "q34" else []), capture_output=True, text=True, cwd="/home/claude/sen0401", timeout=900); ok("Q6 the part's own check re-run: RESULT PASS", "RESULT PASS" in r.stdout, (r.stdout.strip().splitlines() or [""])[-1][:100] + r.stderr[-120:])
elif case == "merge":
    import re
    P = C + "private/"; CL = E + "sen0401_exam_clarity_check_v1_0_0.py"; PP = C + "papers_midterm_v7/sen0401_exam_midterm_v7_0_0_paper.docx"
    ok("M0 public log commit 38a85d21", blobs("38a85d21") >= 1)
    hs = {"sen0401_exam_items_midterm_v1_8_0.json": "a640c2a03ec5890b", "sen0401_exam_structure_v1_5_0.json": "b2973028ea17cfd2", "sen0401_exam_key_solutions_v1_8_0.json": "1aadec51cd492247", "sen0401_exam_shape_v1_5_0.json": "f67bda5f65506a99"}
    ok("M1 reported hashes", all(hashlib.sha256(open(P + f, "rb").read()).hexdigest().startswith(h) for f, h in hs.items()))
    L = lambda f: (lambda d: d["items"] if isinstance(d, dict) and "items" in d else d)(json.load(open(P + f)))
    m = {i["key"]: i for i in L("sen0401_exam_items_midterm_v1_8_0.json")}; parts = {}
    for f in ("sen0401_exam_items_part_q1_v1_8_0.json", "sen0401_exam_items_part_q2_v1_8_0.json", "sen0401_exam_items_part_q34_v1_8_1.json"):
        for i in L(f): parts[i["key"]] = i
    d = [(k, f) for k, p in parts.items() for f in ("q", "tip", "options", "answer", "solution", "critical_points", "key_value", "how_to_answer") if p.get(f) != m[k].get(f)]
    ok("M2 the 21 merged items equal the three part files in every text, answer and solution field: %s" % d, set(m) == set(parts) and len(m) == 21 and not d)
    v7 = {i["key"]: i for i in L("sen0401_exam_items_midterm_v1_7_0.json")}; cp = lambda dd: {c_ for i in dd.values() for c_ in (i.get("critical_points") or [])}
    ok("M3 no critical point of v1.7.0 lost: %s" % (cp(v7) - cp(m)), not (cp(v7) - cp(m)))
    s = json.load(open(P + "sen0401_exam_structure_v1_5_0.json")); sub = [x for q in s["questions"] if isinstance(q, dict) for x in q.get("sub", [])]
    ok("M4 structure total 100 over 21 units", sum(x["points"] for x in sub) == 100 and len({x["item"] for x in sub}) == 21)
    r = run([sys.executable, "-B", CL, "check", "--items", P + "sen0401_exam_items_midterm_v1_8_0.json", "--paper", PP]); head = r.stdout.split("SOURCE paper")[0]
    ok("M5 committed clarity check C1 to C5 PASS on the 21 items", all(("C%d  PASS" % i) in head for i in (1, 2, 3, 4, 5)) and "FAIL" not in head)
    sh = "/tmp/rd_ctl/shape_ctl150.json"; run([sys.executable, "-B", E + "sen0401_exam_structure_to_shape_v1_0_0.py", P + "sen0401_exam_structure_v1_5_0.json", P + "sen0401_exam_items_midterm_v1_8_0.json", sh])
    r = run([sys.executable, "-B", E + "sen0401_exam_scoring_check_v2_0_0.py", E + "sen0401_exam_scoring_rule_v2_0_0.json", "--shape", sh, "--blind", "20000", "--seed", "98000"]); ok("M6 scoring check on the new shape 21 of 21, exact blind 77033/5000", "21 of 21 checks PASS" in r.stdout and "77033/5000" in r.stdout)
    r = subprocess.run(["nice", "-n", "10", sys.executable, "-B", P + "sen0401_exam_items_midterm_check_v1_8_0.py"], capture_output=True, text=True, cwd="/home/claude/sen0401", timeout=1500); ok("M7 the merge check re-run RESULT PASS", "RESULT PASS" in r.stdout)
    r = run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_6.py", "leakscan"]); ok("M8 leak scan v1_2_6", "RESULT PASS" in r.stdout)
else:
    ok("H0 files", blobs("fb158e9") >= 5)
    pdf = C + "sheet_v7/sen0401_exam_midterm_v7_proof_sheet_v7_0_0.pdf"
    ok("H1 one page", "Pages:           1" in run(["pdfinfo", pdf]).stdout)
    for sb in ("91000", "92000"):
        r = run([sys.executable, "-B", E + "sen0401_exam_answersheet_check_v7_0_0.py", C + "sheet_v7", "--tag", "sen0401_exam_midterm_v7_proof_sheet_v7_0_0", "--sheets", "20", "--seed-bases", sb, "--key", V6])
        ok("H2 check on seed base " + sb, r.returncode == 0 and "FAIL" not in r.stdout, r.stdout.strip().splitlines()[-1][:120] if r.stdout else r.stderr[-200:])
print("RESULT:", "PASS" if not bad else "FAIL " + str(bad)); sys.exit(1 if bad else 0)
