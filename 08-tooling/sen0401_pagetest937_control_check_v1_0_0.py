#!/usr/bin/env python3
"""sen0401_pagetest937_control_check v1_0_0 - exit-code checks for the control of TK_PageTest937_Build (criterion AC7R_PageTest937). Each kind reads files; the page runs themselves were made by the builder under flock /tmp/page_test.lock, one at a time, into 08-tooling/verify/iter22/pagetest937/.
Usage: kind  (sha | diff | fa937 | fa936 | fb937 | fc937 | ch05 | ch06 | ch08 | nochange)"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
REPO = os.environ.get("SEN0401_ROOT", "/home/claude/sen0401"); D = os.path.join(REPO, "08-tooling/verify/iter22/pagetest937"); T = "08-tooling/"
def git(*a): return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout
def run(n): return open(os.path.join(D, n + ".run.txt"), encoding="utf-8", errors="replace").read()
def p2(txt): return [l for l in txt.splitlines() if "P2 every chapter-code example" in l]
def sha(): 
    h = hashlib.sha256(open(REPO + "/" + T + "sen0401_page_test_v9_36_0.py", "rb").read()).hexdigest(); log = git("log", "--format=%h", "--", T + "sen0401_page_test_v9_36_0.py").split()
    ok = h.startswith("85afebf64de155d2f9beffcadd9aecad708d4c46c7ae6604d80d051e6df1a0cf") and log == ["d4880a3"]; print("9.36.0 sha256", h, "commits touching it", log); return ok
def diff():
    import difflib; a = open(REPO + "/" + T + "sen0401_page_test_v9_36_0.py", encoding="utf-8").read().splitlines(); b = open(REPO + "/" + T + "sen0401_page_test_v9_37_0.py", encoding="utf-8").read().splitlines()
    rem = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l.startswith("-") and not l.startswith("---")]; add = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l.startswith("+") and not l.startswith("+++")]
    print("removed", len(rem), "added", len(add)); [print(" -", l[:140]) for l in rem]; [print(" +", l[:140]) for l in add]
    kinds = [("version" if "__version__" in l else "wait" if "wait_for_function" in l else "other") for l in rem]; addk = [("comment" if l.startswith("+#") else "version" if "__version__" in l else "wait" if "wait_for_function" in l else "other") for l in add]
    return sorted(kinds) == ["version", "wait"] and sorted(addk) == ["comment", "version", "wait"]
def fixture(name, want):
    l = p2(run(name)); print("\n".join(x[:230] for x in l)); return want(l)
def pagechk(n, ver, feat, w):
    r = run(n); m = re.search(r"page 0?%s: exit 0, widgets \('%d', '%d'\), features passed (\d+), failed (\d+)" % (ver, w, w), r); print(m.group(0) if m else "(no result line)")
    return bool(m) and int(m.group(1)) == feat and int(m.group(2)) == 0 and "RESULT: PASS" in r
def nochange():
    st = git("show", "--name-status", "--format=", "1f9550b", "af48938", "d7f49b8").splitlines(); bad = [l for l in st if l and l[0] != "A"]; print(len(st), "files, not added:", bad); return len(st) > 0 and not bad
K = {"sha": sha, "diff": diff,
     "fa937": lambda: fixture("fixture_a_slow_visual_937", lambda l: len(l) >= 1 and all("[PASS]" in x for x in l)),
     "fa936": lambda: fixture("fixture_a_slow_visual_936", lambda l: len(l) >= 1 and all("[FAIL]" in x and "result is text, not a visualisation" in x for x in l)),
     "fb937": lambda: fixture("fixture_b_text_only_937", lambda l: len(l) >= 1 and all("[FAIL]" in x and "result is text, not a visualisation" in x for x in l)),
     "fc937": lambda: fixture("fixture_c_never_ends_937", lambda l: len(l) >= 1 and all("[FAIL]" in x and "Timeout 90000ms" in x for x in l)),
     "ch05": lambda: pagechk("ch05_9_83_0_937", 5, 398, 113), "ch06": lambda: pagechk("ch06_9_83_0_937", 6, 398, 121), "ch08": lambda: pagechk("ch08_9_85_0_937", 8, 394, 127), "nochange": nochange}
if __name__ == "__main__":
    ok = K[sys.argv[1]](); print("RESULT:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
