#!/usr/bin/env python3
# scratch bisect runner (not a gate): unchanged page test 9.38.0 on a scratch variant, inside a scratch repository tree whose page data is the variant's own
import json, os, subprocess, sys, tempfile, shutil, glob
REAL = "/home/claude/sen0401"
var, testname, man = sys.argv[1:4]; V = "/tmp/i60/" + var; PV = "9_74_0"
root = tempfile.mkdtemp(prefix="sen0401_fx_"); T = root + "/08-tooling"; os.makedirs(T + "/ch03-page"); os.makedirs(root + "/03-materials/ch03/page")
for f in (testname, "sen0401_exam_release_v1_0_0.py", "sen0401_lineage_page_key_substitute_v1_0_0.py"): os.symlink(REAL + "/08-tooling/" + f, T + "/" + f)
for f in glob.glob(REAL + "/08-tooling/ch03-page/test_config_v*.json"): os.symlink(f, T + "/ch03-page/" + os.path.basename(f))
shutil.copy(V + "/d/page_data_v9_74_0.json", T + "/ch03-page/page_data_v9_74_0.json")
P = root + "/03-materials/ch03/page"
os.symlink(REAL + "/03-materials/ch03/page/sen0401_ch03_page_v9_73_0.html", P + "/sen0401_ch03_page_v9_73_0.html")
os.symlink(REAL + "/03-materials/ch03/page/" + man, P + "/" + man)
d = root + "/t"; os.makedirs(d)
subprocess.run([sys.executable, T + "/sen0401_lineage_page_key_substitute_v1_0_0.py", "03", "9_73_0", d], capture_output=True, text=True)
jwk = json.load(open(d + "/test_key.json"))["private_jwk"]
PLACE = ("0Sa8MtDE94xNCAAucUwWWoWgdLIgKRY42weFJWUDVrU", "PQfE3vB8fPYCKQ4RPxZZovRuFZ4yQz9u4pmiObDqjus")
s = open(V + "/sen0401_ch03_page_v%s.html" % PV, encoding="utf-8").read()
named = d + "/sen0401_ch03_page_v%s.html" % PV
open(named, "w", encoding="utf-8").write(s.replace(PLACE[0], jwk["x"]).replace(PLACE[1], jwk["y"]))
env = dict(os.environ, PAGE=named, RESULTS=d + "/results.json", PAGE_VER=PV, KEY=d + "/test_key.json", PYTHONDONTWRITEBYTECODE="1")
r = subprocess.run([sys.executable, T + "/" + testname, "03"], capture_output=True, text=True, env=env, cwd=root)
out = r.stdout + r.stderr
open("/tmp/i60/%s_full.log" % var, "w").write(out)
fails = sorted(set(l.strip()[:150] for l in out.splitlines() if l.strip().startswith("[FAIL]")))
print("VARIANT", var, "exit", r.returncode, "features passed", sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]")), "distinct FAIL lines", len(fails))
for l in out.splitlines():
    if "longest main-thread task" in l or "main-thread budget" in l: print(l[:420])
for f in fails: print("FAILED:", f)
shutil.rmtree(root, ignore_errors=True)
