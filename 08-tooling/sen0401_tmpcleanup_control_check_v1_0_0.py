#!/usr/bin/env python3
"""sen0401_tmpcleanup_control_check v1_0_0 - the lineage agent's OWN check of the temporary-folder repair (criterion AC9_TmpCleanup).
Usage: sen0401_tmpcleanup_control_check_v1_0_0.py sha | noleak | equal | refuse | nochange:COMMIT
sha: fixtures v1_2_0 and chapter check v1_3_0 are byte-identical to their content before the executor's commit (git blob compare) and the new files exist.
noleak: one run each of Deck/Ch09 and Research/Ch09 (new chapter check v1_4_0) leaves no new /tmp/sen0401_fx_* or /tmp/hermit_* folder (counted by name before and after), exit 0.
equal: old v1_3_0 and new v1_4_0 print the same lines on Deck/Ch09, Deck/Ch12, Research/Ch09 (temp names, timings and version numbers masked) with the same exit code; the folders the OLD runs leave are removed by this check.
refuse: the stale fixtures are refused ('every stale fixture refused, the control accepted'), a nonexistent deck exits 1 and leaves no folder, --keep keeps exactly one.
nochange:COMMIT: the commit only ADDS files (no modified or deleted file)."""
import glob, os, re, shutil, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
def py(*a): return subprocess.run([sys.executable, "-B"] + list(a), capture_output=True, text=True, cwd=T)
def folders(): return set(glob.glob("/tmp/sen0401_fx_*")) | set(glob.glob("/tmp/hermit_*"))
def mask(s): return re.sub(r"\d+\.\d+ ?s", "", re.sub(r"1\.[34]\.0", "N", re.sub(r"v1_[34]_0", "vN", re.sub(r"/tmp/\w+", "/tmp/X", s))))
def git(*a): return subprocess.run(["git"] + list(a), cwd=R, capture_output=True, text=True).stdout.strip()
def sha():
    ok = True
    for f in ("sen0401_deck_fixtures_v1_2_0.py", "sen0401_lineage_chapter_check_v1_3_0.py"):
        p = "08-tooling/" + f; first = git("log", "--diff-filter=A", "--format=%H", "--", p).splitlines()[-1]; mods = git("log", "--format=%h", "--diff-filter=M", "--", p)
        same = git("rev-parse", first + ":" + p) == git("rev-parse", "HEAD:" + p) and not mods; print(f, "identical to its first commit:", same); ok &= same
    for f in ("sen0401_deck_fixtures_v1_3_0.py", "sen0401_lineage_chapter_check_v1_4_0.py"): e = os.path.exists(os.path.join(T, f)); print(f, "exists:", e); ok &= e
    return ok
def noleak():
    b = folders(); ok = True
    for c in ("Deck/Ch09", "Research/Ch09"):
        r = py("sen0401_lineage_chapter_check_v1_4_0.py", c); new = folders() - b; print(c, "exit", r.returncode, "new folders:", len(new)); ok &= r.returncode == 0 and not new
    return ok
def equal():
    ok = True
    for c in ("Deck/Ch09", "Deck/Ch12", "Research/Ch09"):
        b = folders(); o = py("sen0401_lineage_chapter_check_v1_3_0.py", c); left = folders() - b; [shutil.rmtree(x, ignore_errors=True) for x in left]
        n = py("sen0401_lineage_chapter_check_v1_4_0.py", c); same = mask(o.stdout) == mask(n.stdout) and o.returncode == n.returncode; print(c, "old exit", o.returncode, "new exit", n.returncode, "lines equal:", same, "(old run left %d folders, removed)" % len(left)); ok &= same
    return ok
def refuse():
    b = folders(); r = py("sen0401_deck_fixtures_v1_3_0.py", "09", "--run"); a1 = folders() - b
    ok = r.returncode == 0 and "every stale fixture refused, the control accepted" in r.stdout and not a1; print("fixtures run: exit", r.returncode, "refused-and-accepted line:", "every stale fixture refused" in r.stdout, "new folders:", len(a1))
    r = py("sen0401_deck_fixtures_v1_3_0.py", "09", "--run", "--deck", "/nonexistent.pptx"); a2 = folders() - b; print("nonexistent deck: exit", r.returncode, "new folders:", len(a2)); ok &= r.returncode == 1 and not a2
    r = py("sen0401_deck_fixtures_v1_3_0.py", "09", "--run", "--keep"); a3 = folders() - b; print("--keep: exit", r.returncode, "new folders:", len(a3)); ok &= r.returncode == 0 and len(a3) == 1; [shutil.rmtree(x, ignore_errors=True) for x in a3]
    return ok
def nochange(c):
    st = git("show", "--name-status", "--format=", c).splitlines(); bad = [l for l in st if not l.startswith("A")]; print(len(st), "files, not added:", bad); return not bad
a = sys.argv[1]; ok = nochange(a.split(":", 1)[1]) if a.startswith("nochange:") else {"sha": sha, "noleak": noleak, "equal": equal, "refuse": refuse}[a]()
print("RESULT %s: %s" % (a.split(":")[0], "PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
