#!/usr/bin/env python3
"""sen0401_urgent_control_check v1_0_0 - the lineage agent's own small checks for the control of the urgent chapter 6 deck and page tasks (control97). Not the executor's tools.
  nochange C1,C2,...   the commits (oldest first) leave every file that existed before the first of them with the same content at the last of them (a file may be changed and restored; the net is what counts); files they add are listed
  logcheck KEY MINFEAT  KEY = a page test version such as 38_0 (log ctl_sen0401_page_test_v9_38_0.log) or 'panels'; reads a full page-test log of the lineage agent's own run: exit 0 only when it has no traceback, no [FAIL] line, a widgets line 'N tested, N passed; failing: []', and at least MINFEAT [PASS] lines
  samelines            the control's re-run log of the executor's engine check v1.1.1 has the same PASS/FAIL lines as the executor's log and no FAIL
Prints what it found; exit 0 = every element holds."""
import re, subprocess, sys
REPO = "/home/claude/sen0401"
def git(*a): return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout
def nochange(cs):
    cs = cs.split(","); first, last = cs[0], cs[-1]; files = sorted({f for c in cs for f in git("show", "--name-only", "--format=", c).splitlines() if f}); added = []; changed = []
    for f in files:
        before = subprocess.run(["git", "-C", REPO, "cat-file", "-e", first + "^:" + f], capture_output=True).returncode == 0
        if not before: added.append(f); continue
        a = subprocess.run(["git", "-C", REPO, "show", first + "^:" + f], capture_output=True).stdout; b = subprocess.run(["git", "-C", REPO, "show", last + ":" + f], capture_output=True).stdout
        if a != b: changed.append(f)
    print("commits %s: %d files touched, %d added, %d existed before and differ at the last commit" % (",".join(cs), len(files), len(added), len(changed)))
    for f in changed: print("CHANGED", f)
    ok = not changed; print("RESULT:", "no committed file changed (net)" if ok else "a committed file differs"); return 0 if ok else 1
def logcheck(p, minfeat):
    p = REPO + "/08-tooling/verify/iter53/ctl/" + ("ctl_panels_test.log" if p == "panels" else "ctl_sen0401_page_test_v9_%s.log" % p)
    t = open(p, errors="replace").read(); tb = "Traceback" in t; fail = len(re.findall(r"\[FAIL\]", t)); ps = len(re.findall(r"\[PASS\]", t)); w = re.findall(r"widgets: (\d+) tested, (\d+) passed; failing: (\[[^\]]*\])", t)
    print("%s: traceback %s, [PASS] %d, [FAIL] %d, widgets %s" % (p.split("/")[-1], tb, ps, fail, w[-1] if w else None))
    pan = "panels" in p; ok = (not tb) and fail == 0 and (pan or (bool(w) and w[-1][0] == w[-1][1] and w[-1][2] == "[]")) and ps >= int(minfeat); print("RESULT:", "PASS" if ok else "FAIL"); return 0 if ok else 1
def samelines(which="nocopy"):
    d = REPO + "/08-tooling/"; a = d + "verify/iter54/ctl/ctl_%s_rerun.log" % ("nocopy_engine_check_v1_1_1" if which == "nocopy" else "items_midterm_check_v1_0_0"); b = d + ("exam/sen0401_exam_engine_check_log_v1_1_1.txt" if which == "nocopy" else "exam/sen0401_exam_items_midterm_check_log_v1_0_0.txt")
    f = lambda p: [re.sub(r"\s+", " ", l)[:60] for l in open(p, errors="replace").read().splitlines() if re.match(r"\s*(PASS|FAIL|NOT_MEASURED)|SUMMARY|RESULT", l)]
    x, y = f(a), f(b); print("control's re-run of the executor's check v1.1.1: %d result lines, %d PASS, %d FAIL; committed log: %d lines; equal (first 60 characters of each): %s" % (len(x), sum(l.startswith("PASS") for l in x), sum(l.startswith("FAIL") for l in x), len(y), x == y))
    ok = x == y and x and not any(l.startswith("FAIL") for l in x) and (x[-1].startswith("SUMMARY 16 of 16") if which == "nocopy" else x[-1].startswith("RESULT PASS")); print("RESULT:", "PASS" if ok else "FAIL"); return 0 if ok else 1
if __name__ == "__main__":
    sys.exit({"nochange": nochange, "logcheck": logcheck, "samelines": samelines}[sys.argv[1]](*sys.argv[2:]))
