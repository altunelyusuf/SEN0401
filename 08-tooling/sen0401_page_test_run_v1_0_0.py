#!/usr/bin/env python3
"""sen0401_page_test_run v1.0.0 - runs a SEN0401 page test on a chapter page against a key-substituted copy (see sen0401_page_key_substitute_v1_0_0.py),
for a machine without the instructor's private key. Everything it writes goes to a temporary directory outside the repository. Exit 0 only when the test
exits 0, reports every widget passed and prints no [FAIL] line. The pass proves the page's logic; the release step ran with a TEST key.
Usage: sen0401_page_test_run_v1_0_0.py NN [PAGEVER] [TESTFILE]
  PAGEVER default: the newest sen0401_chNN_page_v*.html of the chapter;  TESTFILE default: the newest sen0401_page_test_v*.py beside this file
  (9.33.0 when sen0401_page_test_v9_33_0.py exists, else 9.32.0). Pass sen0401_page_test_v9_32_0.py to run SEN0401's own earlier test through the same wrapper.
Environment: SEN0401_ROOT = repository root (default the parent of this file's folder; a scratch copy works), TESTPY = interpreter with playwright (default /home/claude/venv314/bin/python)."""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys, tempfile

TOOL = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
PY = os.environ.get("TESTPY") or ("/home/claude/venv314/bin/python" if os.path.exists("/home/claude/venv314/bin/python") else sys.executable)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def main():
    n = sys.argv[1]
    pages = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0401_ch%s_page_v*.html" % n)), key=vkey)
    pv = sys.argv[2] if len(sys.argv) > 2 else "_".join(map(str, vkey(pages[-1])))
    tests = sorted(glob.glob(os.path.join(TOOL, "sen0401_page_test_v9_*.py")), key=vkey)
    test = os.path.join(TOOL, sys.argv[3]) if len(sys.argv) > 3 else tests[-1]
    d = tempfile.mkdtemp(prefix="sen0401_page_test_")
    r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0401_page_key_substitute_v1_0_0.py"), n, pv, d], capture_output=True, text=True, env=dict(os.environ, SEN0401_ROOT=REPO))
    print(r.stdout + r.stderr)
    if r.returncode:
        print("RESULT: FAIL (key substitution)"); sys.exit(1)
    env = dict(os.environ, PAGE=os.path.join(d, "page.html"), RESULTS=os.path.join(d, "results.json"), PAGE_VER=pv, KEY=os.path.join(d, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
    print("test file:", os.path.basename(test), " page version:", pv, " repo:", REPO, flush=True)
    r = subprocess.run([PY, test, n], capture_output=True, text=True, env=env, cwd=REPO)
    out = r.stdout + r.stderr
    fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
    nskip = sum(1 for l in out.splitlines() if l.strip().startswith("[SKIP]"))
    m = re.search(r"widgets: (\d+) tested, (\d+) passed", out)
    open(os.path.join(d, "full_output.txt"), "w").write(out)
    print("\n".join(out.splitlines()[-12:]))
    ok = r.returncode == 0 and m is not None and m.group(1) == m.group(2) and not fails
    print("page %s: exit %d, widgets %s, features passed %d, skipped %d, failed %d, release step with a TEST key; full output in %s" % (n, r.returncode, m.groups() if m else None, npass, nskip, len(fails), d))
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
