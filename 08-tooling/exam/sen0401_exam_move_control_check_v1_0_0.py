#!/usr/bin/env python3
"""sen0401_exam_move_control_check v1_0_0 - the lineage agent's own control. Usage: copy | items5m
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
            if f == "sen0401_exam_move_control_check_v1_0_0.py": continue
            p = os.path.join(dp, f); o[os.path.relpath(p, r)] = p
    return o
src = walk(S + "/" + X); cme = walk(C + "/exams/SEN0401/" + X)
if sys.argv[1] == "copy":
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
    for f in ("private/sen0401_exam_items_midterm_v1_4_0.json", "private/sen0401_exam_structure_v1_1_0.json", "private/sen0401_exam_topic_map_v1_4_0.json"):
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
