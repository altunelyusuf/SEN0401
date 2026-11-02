#!/usr/bin/env python3
# scratch bisect runner (not a gate): runs the UNCHANGED page test 9.38.0 on a scratch variant page, as the committed runner does for a repository page
import json, os, re, subprocess, sys, tempfile, shutil
REPO = "/home/claude/sen0401"; TOOL = REPO + "/08-tooling"
html, label, testname = sys.argv[1:4]; PV = "9_74_0"
sys.path.insert(0, TOOL)
d = tempfile.mkdtemp(prefix="sen0401_page_test_")
r = subprocess.run([sys.executable, TOOL + "/sen0401_lineage_page_key_substitute_v1_0_0.py", "03", PV, d], capture_output=True, text=True)  # makes the test key
s = open(html, encoding="utf-8").read()
PLACE = ("0Sa8MtDE94xNCAAucUwWWoWgdLIgKRY42weFJWUDVrU", "PQfE3vB8fPYCKQ4RPxZZovRuFZ4yQz9u4pmiObDqjus")
jwk = json.load(open(d + "/test_key.json"))["private_jwk"]
named = d + "/sen0401_ch03_page_v%s.html" % PV
open(named, "w", encoding="utf-8").write(s.replace(PLACE[0], jwk["x"]).replace(PLACE[1], jwk["y"]))
os.remove(d + "/page.html")
shutil.copy(REPO + "/03-materials/ch03/page/sen0401_ch03_page_v9_73_0.html", d)
env = dict(os.environ, PAGE=named, RESULTS=d + "/results.json", PAGE_VER=PV, KEY=d + "/test_key.json", PYTHONDONTWRITEBYTECODE="1")
r = subprocess.run([sys.executable, TOOL + "/" + testname, "03"], capture_output=True, text=True, env=env, cwd=REPO)
out = r.stdout + r.stderr
open("/tmp/i60/%s_full.log" % label, "w").write(out)
fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
print("VARIANT", label, "exit", r.returncode, "passed", npass, "failed", len(fails))
for l in out.splitlines():
    if "longest main-thread task" in l or "main-thread budget" in l: print(l[:420])
shutil.rmtree(d, ignore_errors=True)
