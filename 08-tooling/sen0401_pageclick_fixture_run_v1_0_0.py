#!/usr/bin/env python3
"""sen0401_pageclick_fixture_run v1_0_0 (the control's copy of sen0401_lineage_page_test_run v1_2_0 with the fixture script injected into the temporary copy of the page, env FIXTURE_JS) - original text: sen0401_lineage_page_test_run v1_2_0 (over 1.1.0: the FULL test output is written to the file named by env FULL_LOG, and the lines about Untangle, SKIP and the counts are printed, so the labels feature can be read as printed) - runs the newest SEN0401 page test (sen0401_page_test_v9_*.py) on a chapter page against a key-substituted copy
(see sen0401_lineage_page_key_substitute). Everything it writes goes to a temporary directory outside the repository. Prints the test's tail and one summary line.
Exit 0 only when the test exits 0, reports every widget passed, and prints no [FAIL] line. The pass proves the page's logic; the release step ran with a TEST key.
Usage: sen0401_lineage_page_test_run_v1_1_0.py NN [PAGEVER]     (PAGEVER default: the newest sen0401_chNN_page_v*.html in 03-materials/chNN/page)
"""
__version__ = "1.2.0"
import glob, os, re, subprocess, sys, tempfile

TOOL = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]


def main():
    n = sys.argv[1]
    if len(sys.argv) > 2:
        pv = sys.argv[2]
    else:
        pv = "_".join(map(str, vkey(sorted(glob.glob(os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0401_ch%s_page_v*.html" % n)), key=vkey)[-1])))
    # v1.1.0: the newest page test in the folder (9.34.0 at the time of writing); override with PAGE_TEST=<file name>
    tests = sorted(glob.glob(os.path.join(TOOL, "sen0401_page_test_v9_*.py")), key=vkey)
    test = os.path.join(TOOL, os.environ.get("PAGE_TEST") or os.path.basename(tests[-1]))
    d = tempfile.mkdtemp(prefix="sen0401_page_test_")
    r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0401_lineage_page_key_substitute_v1_0_0.py"), n, pv, d], capture_output=True, text=True)
    print(r.stdout + r.stderr)
    if r.returncode:
        print("RESULT: FAIL (key substitution)"); sys.exit(1)
    # the test measures the load task against the previously shipped page of the same chapter FOUND NEXT TO THE PAGE UNDER TEST (budget split, 9.29.0): put the
    # key-substituted copy under its real name beside an untouched copy of the newest earlier version, as they sit in the repository
    named = os.path.join(d, "sen0401_ch%s_page_v%s.html" % (n, pv))
    os.replace(os.path.join(d, "page.html"), named)
    # CONTROL FIXTURE (the control's own runner, new file): put the fixture script into a COPY of the page under test, as the criterion (3) describes
    _fj = open(os.environ["FIXTURE_JS"], encoding="utf-8").read(); _h = open(named, encoding="utf-8").read(); assert _h.count("</body>") == 1
    open(named, "w", encoding="utf-8").write(_h.replace("</body>", "<script>" + _fj + "</script></body>")); print("fixture script injected into the temporary copy only; SHA-256 of the script:", __import__("hashlib").sha256(_fj.encode()).hexdigest())
    pk = lambda f: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.html$", f).groups()]
    earlier = [f for f in glob.glob(os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0401_ch%s_page_v*.html" % n)) if pk(f) < pk(named)]
    if earlier:
        import shutil
        pred = sorted(earlier, key=pk)[-1]; shutil.copy(pred, os.path.join(d, os.path.basename(pred))); print("predecessor beside the page under test:", os.path.basename(pred))
    env = dict(os.environ, PAGE=named, RESULTS=os.path.join(d, "results.json"), PAGE_VER=pv, KEY=os.path.join(d, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
    print("page test:", os.path.basename(test), "on page version", pv)
    r = subprocess.run([sys.executable, test, n], capture_output=True, text=True, env=env, cwd=REPO)
    out = r.stdout + r.stderr
    if os.environ.get('FULL_LOG'):
        open(os.environ['FULL_LOG'], 'w', encoding='utf-8').write(out)
    print('\n'.join(l[:400] for l in out.splitlines() if re.search(r'Untangle|SKIP|skip', l)))
    fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
    m = re.search(r"widgets: (\d+) tested, (\d+) passed", out)
    print("\n".join(out.splitlines()[-16:]))
    for l in fails:
        print(l[:300])
    ok = r.returncode == 0 and m is not None and m.group(1) == m.group(2) and not fails
    print("page %s: exit %d, widgets %s, features passed %d, failed %d, release step with a TEST key" % (n, r.returncode, m.groups() if m else None, npass, len(fails)))
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
