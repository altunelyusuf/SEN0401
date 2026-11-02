#!/usr/bin/env python3
"""sen0401_exam_move_control_check v1_2_3 - (copy of v1_2_0 whose own search text matched itself, so S2 skips the move-control scripts; copy of v1_1_0; the removal commit and its ancestor are arguments; new mode leakscan) the lineage agent's own control. Usage: copy | items5m | remove COMMIT PARENT_ANCESTOR | leakscan
leakscan: strings of 40 to 200 characters taken from every items and key json in CME (and the item backup) are searched with git grep -F in the tracked files of 08-tooling/exam and 08-tooling/verify; files of course facts (critical points, analysis, fixtures, seed report, structure, owner topics, topic maps, engine logs) are the allow-list; any other match is a FAIL line naming the file and the count
remove: the removal commit cd9706c deletes only (no add, no change), every deleted file has an equal-hash copy in CME, the tracked count fell by exactly the deleted count, the .gitignore is unchanged, the commit sits on the old head (no history rewrite), no key, paper, items or computed-answer file of the removed kinds is tracked in 08-tooling/exam
copy: every file of 08-tooling/exam (incl. private/) of the SEN0401 repository has an equal copy (SHA-256, own walk) in the CME clone under exams/SEN0401/08-tooling/exam, the same count, the item backup folder is fully in CME, the CME repository is private on the remote (REST API), CME has no uncommitted change under exams/.
items5m: the 5M items check re-run (exit 0, RESULT PASS), the private items, structure and topic map in CME equal the ones here, only the check script of 5M is tracked in SEN0401, nothing staged. Names and counts only are printed."""
import hashlib, json, os, subprocess, sys
S = "/home/claude/sen0401"; C = "/home/claude/CME"; X = "08-tooling/exam"; res = []
def ok(n, c, d=""): res.append(bool(c)); print("%s  %s  %s" % ("PASS" if c else "FAIL", n, d))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def walk(r):
    o = {}
    for dp, dn, fs in os.walk(r):
        if "__pycache__" in dp: continue
        for f in fs:
            if f.startswith("sen0401_exam_move_control_check_v1_2_"): continue
            p = os.path.join(dp, f); o[os.path.relpath(p, r)] = p
    return o
src = walk(S + "/" + X); cme = walk(C + "/exams/SEN0401/" + X)
if sys.argv[1] == "remove":
    CM = sys.argv[2]; PAR = sys.argv[3]; g = lambda *a: subprocess.run(["git", "-C", S] + list(a), capture_output=True, text=True).stdout
    st = [l.split("\t") for l in g("diff", "--name-status", CM + "^", CM).splitlines()]; dele = [x[1] for x in st if x[0] == "D"]
    ok("R1 the commit only deletes files", len(st) == len(dele) and len(dele) > 0, "%d deleted of %d changed" % (len(dele), len(st)))
    bad = []
    for f in dele:
        b = subprocess.run(["git", "-C", S, "show", CM + "^:" + f], capture_output=True).stdout; p = C + "/exams/SEN0401/" + f
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != hashlib.sha256(b).hexdigest(): bad.append(f)
    ok("R2 every deleted file has an equal-hash copy in CME (own walk)", not bad, "%d deleted, %d without an equal copy %s" % (len(dele), len(bad), bad[:3]))
    n0 = len(g("ls-tree", "-r", "--name-only", CM + "^").split("\n")) - 1; n1 = len(g("ls-tree", "-r", "--name-only", CM).split("\n")) - 1
    ok("R3 the tracked count fell by exactly the deleted count", n0 - n1 == len(dele), "%d to %d" % (n0, n1))
    ok("R4 the .gitignore is unchanged by the commit", g("diff", "--name-only", CM + "^", CM, "--", ".gitignore").strip() == "")
    par = g("rev-parse", "--short", CM + "^").strip(); inrem = CM in g("log", "origin/main", "--format=%h").split(); anc = subprocess.run(["git", "-C", S, "merge-base", "--is-ancestor", PAR, CM], capture_output=True).returncode == 0
    ok("R5 no rewrite: the commit is in the remote history and the head before it (%s)" % PAR + " is its ancestor", inrem and anc, "parent %s, in origin/main %s, f5b753c ancestor %s" % (par, inrem, anc))
    left = [x for x in g("ls-files", X).split() if "/papers_midterm_v" in x and (x.endswith("_key.json") or x.endswith("_key.pdf") or x.endswith("_key.docx") or x.endswith("_paper.ttl") or x.endswith(".docx")) or "/sen0401_exam_items_midterm_v1_" in x and x.endswith(".json") and "topic" not in x and "map" not in x]
    ok("R6 no key, paper, Word file or items file of the removed kinds is tracked in 08-tooling/exam", not left, str(left[:3]))
elif sys.argv[1] == "leakscan":
    import glob, tempfile
    pats = set()
    def walk(o):
        if isinstance(o, str):
            for part in o.split("\n"):
                p = part.strip()
                if 40 <= len(p) <= 200 and not p.startswith(("03-materials", "08-tooling")): pats.add(p)
        elif isinstance(o, list):
            for x in o: walk(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("key", "source", "sources", "file", "seeds", "note", "derived_from", "critical_points", "enhancements", "no_seed_reason", "understanding", "owner_points", "papers"): continue
                walk(v)
    nf = 0
    for f in glob.glob(C + "/exams/SEN0401/08-tooling/exam/**/*.json", recursive=True) + glob.glob(C + "/exams/SEN0401/08-tooling/verify/**/*.json", recursive=True) + glob.glob("/home/claude/exam_private_backup/*.json"):
        if not any(w in f for w in ("items", "key")): continue
        try: walk(json.load(open(f))); nf += 1
        except Exception: pass
    pats.discard('DECIDED by the owner on 2026-11-02 16:52 Istanbul: the total of the whole paper is not below 0 (floor at 0 on the paper total, none inside a question)')  # v1_2_2: the owner's ruling sentence is public decision text (register, rule file), read by the lineage agent; no other string is exempt
    for s in ("One rule for every question: a right answer scores its points; a wrong answer, a blank and two answers in one place score 0.", "none (removed); the total of a perfect sheet is 100", "none (the total is a plain sum and cannot be below 0)"): pats.discard(s)  # v1_2_3: the three scoring-rule sentences of the owner's v7 rulings are public rule text (scoring rule file, register), found again in a private structure copy; they hold no question and no answer
    pf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False); pf.write("\n".join(sorted(pats)) + "\n"); pf.close()
    allow = ("critical_points", "exam_analysis", "analysis_v1_3_0", "engine_fixtures", "seedreport", "exam_structure_v1_0_0", "owner_topics", "topic_map_v1_3_0", "engine_check_log", "exam_items_midterm_report_v1_0_0", "exam_paperrules_fixtures", "BRIEF_TK_Exam_Items5A_Build", "exam_paper_lib_v2", "midterm_v2_0_0_formA_measure", "midterm_v2_0_0_formB_measure", "owner_input_check", "_bank_", "bank_gen", "bank_apply", "bank_text")
    out = subprocess.run(["git", "-C", S, "grep", "-F", "-c", "-f", pf.name, "--", "08-tooling/exam", "08-tooling/verify", "08-tooling/briefs"], capture_output=True, text=True).stdout.split("\n")
    hits = [(l.rsplit(":", 1)[0], l.rsplit(":", 1)[1]) for l in out if ":" in l and not any(a in l for a in allow)]
    ok("S1 %d strings from %d private items and key files: no tracked file of 08-tooling/exam, verify or briefs outside the allow-list holds one" % (len(pats), nf), not hits, str(hits[:6]))
    nums = subprocess.run(["git", "-C", S, "grep", "-l", "-E", "660_000_000|660 million|fee == 9500|3 \\* 58 \\*\\* 2|37,000 in"], capture_output=True, text=True).stdout.split()
    ok("S2 no tracked file outside the register holds the computed answers of the new form by value", not [x for x in nums if not x.startswith("07-lineage") and "exam_move_control_check" not in x], str([x for x in nums if not x.startswith("07-lineage") and "exam_move_control_check" not in x][:6]))
    os.unlink(pf.name)
elif sys.argv[1] == "copy":
    diff = [k for k in src if k not in cme or h(src[k]) != h(cme[k])]
    ok("M1 every exam file has an equal-hash copy in CME (own walk)", not diff and len(src) == len(cme), "%d source files, %d copies, %d missing or different %s" % (len(src), len(cme), len(diff), diff[:3]))
    bs = walk("/home/claude/exam_private_backup"); bc = walk(C + "/exams/exam_private_backup")
    bd = [k for k in bs if k not in bc or h(bs[k]) != h(bc[k])]; ok("M2 the item backup folder is complete in CME with equal hashes", not bd, "%d files, %d missing or different" % (len(bs), len(bd)))
    r = subprocess.run(["gh", "api", "repos/altunelyusuf/cme", "--jq", ".private"], capture_output=True, text=True); ok("M3 the CME repository is private on the remote", r.stdout.strip() == "true", r.stdout.strip())
    st = subprocess.run(["git", "-C", C, "status", "--short", "exams"], capture_output=True, text=True).stdout.strip(); ok("M4 nothing under exams/ in CME is uncommitted", st == "", st[:80])
    ok("M5 nothing deleted at the source (the source walk equals the manifest count of 307 plus the later files)", len(src) >= 230)
else:
    r = subprocess.run([sys.executable, "-B", S + "/" + X + "/sen0401_exam_items_midterm_check_v1_4_0.py"], capture_output=True, text=True, cwd=S)
    ok("I1 the 5M items check re-run: exit 0, RESULT PASS, no FAIL line", r.returncode == 0 and "RESULT PASS" in r.stdout and not [l for l in r.stdout.splitlines() if l.startswith("FAIL")], "%d PASS lines" % sum(1 for l in r.stdout.splitlines() if l.startswith("PASS")))
    for f in ("private/sen0401_exam_items_midterm_v1_4_0.json", "private/sen0401_exam_structure_v1_2_2.json", "private/sen0401_exam_topic_map_v1_4_0.json"):
        ok("I2 %s equals its copy in CME" % f.split("/")[-1], f in src and f in cme and h(src[f]) == h(cme[f]) if f in src else (f.replace("private/", "") in src and h(src[f.replace("private/", "")]) == h(cme[f.replace("private/", "")])))
    tr = [x for x in subprocess.run(["git", "-C", S, "ls-files", X], capture_output=True, text=True).stdout.split() if "v1_4_0" in x or "structure_v1_1" in x]
    ok("I3 only the 5M check script is tracked among the v1_4_0 files", tr == [X + "/sen0401_exam_items_midterm_check_v1_4_0.py"], str(tr))
    ok("I4 nothing staged", subprocess.run(["git", "-C", S, "diff", "--cached", "--name-only"], capture_output=True, text=True).stdout.strip() == "")
    d = json.load(open(S + "/" + X + "/private/sen0401_exam_items_midterm_v1_4_0.json")); its = d["items"]
    out = {}
    import io, contextlib
    for i in its:
        if i["type"] == "CodeTrace":
            b = io.StringIO()
            with contextlib.redirect_stdout(b): exec(i["code"], {})
            ok("I5 code trace %s executed here equals its stored output" % i["key"], b.getvalue().strip() == str(i["output"]).strip(), b.getvalue().strip())
    ok("I6 21 items, positions Q1.a to Q5 present once", len(its) == 21 and len({i.get("position") or i.get("sub_question") for i in its}) == 21, str(len(its)))
print("RESULT " + ("PASS" if all(res) else "FAIL")); sys.exit(0 if all(res) else 1)
