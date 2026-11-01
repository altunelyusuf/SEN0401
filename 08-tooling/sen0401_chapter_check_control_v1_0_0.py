#!/usr/bin/env python3
"""sen0401_chapter_check_control v1_0_0 - the control's own check of the chapter check v1_6_0 (commit cc31307): v1_5_0 is byte-identical to its blob before the commit; the only code line that differs from v1_5_0 (besides docstring, usage and version) is the fixtures call; Deck/Ch01 PASS with v1_6_0 and FAIL with v1_5_0; Deck/Ch04 (prompts) gives the same lines with both. Usage: run"""
import difflib, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); res = []
def chk(ok, m): res.append(bool(ok)); print("PASS " if ok else "FAIL ", m)
def run(v, k): r = subprocess.run([sys.executable, os.path.join(H, "sen0401_lineage_chapter_check_v%s.py" % v), k], capture_output=True, text=True); return r.returncode, re.sub(r"1_[56]_0|1\.[56]\.0", "V", r.stdout)
old = open(os.path.join(H, "sen0401_lineage_chapter_check_v1_5_0.py")).read().splitlines(); new = open(os.path.join(H, "sen0401_lineage_chapter_check_v1_6_0.py")).read().splitlines()
blob = subprocess.run(["git", "-C", R, "show", "cc31307~1:08-tooling/sen0401_lineage_chapter_check_v1_5_0.py"], capture_output=True, text=True).stdout.splitlines()
chk(old == blob, "v1_5_0 equals its blob before the commit")
d = [l for l in difflib.unified_diff(old, new, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
code = [l for l in d if not re.search(r"Usage|__version__|sen0401_lineage_chapter_check v1_[56]_0", l)]
chk(len(code) == 2 and "fixtures_v1_3_0" in code[0] and "fixtures_v1_4_0" in code[1], "the only code change is the fixtures call (%d changed lines besides docstring, usage, version)" % len(code))
a, b = run("1_5_0", "Deck/Ch01"), run("1_6_0", "Deck/Ch01"); chk(a[0] != 0 and b[0] == 0, "Deck/Ch01 v3_3_0: v1_5_0 exit %d, v1_6_0 exit %d" % (a[0], b[0]))
a, b = run("1_5_0", "Deck/Ch04"), run("1_6_0", "Deck/Ch04"); chk(a == b, "Deck/Ch04 (prompts): same exit code and lines with both")
print("RESULT", "PASS" if all(res) else "FAIL"); sys.exit(0 if all(res) else 1)
