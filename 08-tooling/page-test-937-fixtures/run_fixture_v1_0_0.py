#!/usr/bin/env python3
"""run_fixture v1_0_0 - runs a page test on a fixture page exactly as sen0401_lineage_page_test_run_v1_2_0.py runs one on a chapter page (key substitution,
predecessor page beside it, same environment). Usage: FULL_LOG=<log> run_fixture_v1_0_0.py TESTFILE FIXTURE   (the fixture stands in for page 9.85.0 of chapter 8)"""
import glob, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); REPO = os.path.dirname(TOOL)
test, fx = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); n, pv = "08", "9_85_0"
d = tempfile.mkdtemp(prefix="sen0401_page_test_fx_")
sys.path.insert(0, TOOL); import importlib; ks = importlib.import_module("sen0401_lineage_page_key_substitute_v1_0_0")
jwk = __import__("json").load(open(ks.TEST_KEY))["private_jwk"]; shutil.copy(ks.TEST_KEY, os.path.join(d, "test_key.json"))
t = open(fx, encoding="utf-8").read(); a, b = ks.PLACEHOLDER; assert a in t and b in t
named = os.path.join(d, "sen0401_ch%s_page_v%s.html" % (n, pv)); open(named, "w", encoding="utf-8").write(t.replace(a, jwk["x"]).replace(b, jwk["y"]))
pk = lambda f: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.html$", f).groups()]
earlier = [f for f in glob.glob(os.path.join(REPO, "03-materials", "ch08", "page", "sen0401_ch08_page_v*.html")) if pk(f) < pk(named)]
shutil.copy(sorted(earlier, key=pk)[-1], d)
env = dict(os.environ, PAGE=named, RESULTS=os.path.join(d, "results.json"), PAGE_VER=pv, KEY=os.path.join(d, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
print("page test:", os.path.basename(test), "on fixture", os.path.basename(fx))
r = subprocess.run([sys.executable, test, n], capture_output=True, text=True, env=env, cwd=REPO); out = r.stdout + r.stderr
open(os.environ["FULL_LOG"], "w", encoding="utf-8").write(out)
for l in out.splitlines():
    if re.search(r"P2|widgets:", l): print(l[:500])
print("exit", r.returncode, "fails:", sum(1 for l in out.splitlines() if l.strip().startswith("[FAIL]")), "passes:", sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]")))
shutil.rmtree(d, ignore_errors=True)
