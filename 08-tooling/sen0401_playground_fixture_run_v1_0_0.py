#!/usr/bin/env python3
"""sen0401_playground_fixture_run v1_0_0 (new file; task TK_Test_Playground_Fixtures_Build) - runs a page test (PAGE_TEST=<file>) on a FIXTURE of known answer
for the Playground step 'choosing an example in the Playground fills the code at once'. It does what sen0401_lineage_page_test_run_v1_2_0.py does (key-substituted
copy under its real name, predecessor beside it, same environment, same output lines) and, before the test runs, applies ONE mutation to the scratch copy:
  true        no change (the true page; must PASS)
  altered     the code of the 2nd slide example (value cc:1) in the page's embedded chapter code gets a marker line (must FAIL, naming the option)
  outofrange  the 2nd slide example option is given the value cc:99 (must FAIL, not crash)
The repository page and the page data are never changed; the page data (the expected manifest) is read by the test from the repository as for the true page.
Every mutation is asserted to have changed the copy exactly once. Usage: PAGE_TEST=<file> sen0401_playground_fixture_run_v1_0_0.py NN PAGEVER MUTATION   (env FULL_LOG=<path>)"""
__version__ = "1.0.0"
import glob, os, re, shutil, subprocess, sys, tempfile
TOOL = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(TOOL)

def mutate(s, kind):
    if kind == "true": return s
    if kind == "outofrange":
        a = "'<option value=\"cc:'+i+'\""; assert s.count(a) == 1, "option template found %d times" % s.count(a)
        return s.replace(a, "'<option value=\"cc:'+(i===1?99:i)+'\"")
    if kind == "altered":
        m = re.search(r'("chaptercode": \{.*?"examples": \[\{.*?\}, \{"order": 2, "name": "[^"]*", "code": ")', s, re.S)
        assert m, "second chapter-code example not found"
        return s[:m.end()] + "# ALTERED BY FIXTURE\\n" + s[m.end():]
    raise SystemExit("unknown mutation " + kind)

def main():
    n, pv, kind = sys.argv[1:4]
    test = os.path.join(TOOL, os.environ["PAGE_TEST"])
    d = tempfile.mkdtemp(prefix="sen0401_fx_")
    r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0401_lineage_page_key_substitute_v1_0_0.py"), n, pv, d], capture_output=True, text=True); print(r.stdout + r.stderr)
    if r.returncode: print("RESULT: FAIL (key substitution)"); sys.exit(1)
    named = os.path.join(d, "sen0401_ch%s_page_v%s.html" % (n, pv)); os.replace(os.path.join(d, "page.html"), named)
    s = open(named, encoding="utf-8").read(); t = mutate(s, kind)
    print("fixture:", kind, "| page bytes changed:", len(t.encode()) - len(s.encode()), "| differs:", t != s); assert (t != s) == (kind != "true")
    open(named, "w", encoding="utf-8").write(t)
    pk = lambda f: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.html$", f).groups()]
    earlier = [f for f in glob.glob(os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0401_ch%s_page_v*.html" % n)) if pk(f) < pk(named)]
    if earlier:
        pred = sorted(earlier, key=pk)[-1]; shutil.copy(pred, os.path.join(d, os.path.basename(pred))); print("predecessor beside the page under test:", os.path.basename(pred))
    env = dict(os.environ, PAGE=named, RESULTS=os.path.join(d, "results.json"), PAGE_VER=pv, KEY=os.path.join(d, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
    print("page test:", os.path.basename(test), "on page version", pv, "fixture", kind)
    r = subprocess.run([sys.executable, test, n], capture_output=True, text=True, env=env, cwd=REPO); out = r.stdout + r.stderr
    if os.environ.get("FULL_LOG"): open(os.environ["FULL_LOG"], "w", encoding="utf-8").write(out)
    fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]; npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
    m = re.search(r"widgets: (\d+) tested, (\d+) passed", out)
    print("\n".join(l[:400] for l in out.splitlines()[-16:]))
    for l in fails: print(l[:300])
    ok = r.returncode == 0 and m is not None and m.group(1) == m.group(2) and not fails
    print("page %s: exit %d, widgets %s, features passed %d, failed %d, fixture %s" % (n, r.returncode, m.groups() if m else None, npass, len(fails), kind))
    print("RESULT:", "PASS" if ok else "FAIL")
    shutil.rmtree(d, ignore_errors=True); sys.exit(0 if ok else 1)

if __name__ == "__main__": main()
