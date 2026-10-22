#!/usr/bin/env python3
"""sen0401_lineage_verify_page v1_2_0 - the control run of a Verify task of Iter_14 (over v1_0_0: the logs go to verify/iter14, the default page is 9_78_0, and a page test that FAILS an assertion is not repeated: only a run that crashed or hit the budget without a [FAIL] line is run again, up to 3 times) for ONE chapter page, serial, every output kept verbatim as a log file:
  1 template markers, 2 deck match, link check, 3/4 page tests 9.34.1 and 9.35.1 (key-substituted TEST copy; a crashed run is repeated up to 3 times, every run kept), 5 Stage 4 runner, Research/Deck/Page chapter checks, SHA-256 of the page and its Stage 4 page ABox.
Nothing is changed or waived. Usage: sen0401_lineage_verify_page_v1_2_0.py NN [PAGEVER=9_79_0]   Logs: 08-tooling/verify/iter16/chNN/*.log and summary.json"""
__version__ = "1.2.0"
import hashlib, json, os, re, subprocess, sys, time
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
NN = sys.argv[1]; PV = sys.argv[2] if len(sys.argv) > 2 else "9_79_0"
D = os.path.join(H, "verify", "iter16", "ch" + NN); os.makedirs(D, exist_ok=True)
res = {"chapter": NN, "page": PV, "started": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())}
def run(name, cmd, env=None, timeout=3000):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); e.update(env or {})
    t0 = time.time(); r = subprocess.run(cmd, cwd=R, capture_output=True, text=True, env=e, timeout=timeout)
    out = "$ " + " ".join(cmd) + (" [env %s]" % env if env else "") + "\n" + r.stdout + r.stderr + "\n[exit %d, %.0fs]\n" % (r.returncode, time.time() - t0)
    open(os.path.join(D, name + ".log"), "w", encoding="utf-8").write(out); return r.returncode, r.stdout + r.stderr
page = os.path.join(R, "03-materials", "ch" + NN, "page", "sen0401_ch%s_page_v%s.html" % (NN, PV)); html = open(page, encoding="utf-8").read()
res["markers"] = {"const LBLRE=LBL.map": "const LBLRE=LBL.map" in html, "function edVars()": "function edVars()" in html}
c, o = run("deck_match", ["python3", "-B", "08-tooling/pages_deck_match_verify_v1_0_0.py", NN, PV]); res["deck_match"] = o.strip().splitlines()[-1]
c, o = run("link_check", ["python3", "-B", "08-tooling/pages_link_verify_v1_0_0.py", NN, PV]); res["link_check"] = o.strip().splitlines()[-1]
for ver in ("9_34_1", "9_35_1"):
    runs = []
    for k in range(1, 4):
        log = os.path.join(D, "page_test_%s_run%d.full.log" % (ver, k))
        c, o = run("page_test_%s_run%d" % (ver, k), ["python3", "-B", "08-tooling/sen0401_lineage_page_test_run_v1_2_0.py", NN, PV], {"PAGE_TEST": "sen0401_page_test_v%s.py" % ver, "FULL_LOG": log})
        last = [l for l in o.splitlines() if l.startswith("page %s:" % NN) or l.startswith("RESULT")]
        fails = [l.strip()[:200] for l in o.splitlines() if l.strip().startswith("[FAIL]")]
        runs.append({"run": k, "exit": c, "summary": last, "fails": fails, "skips": [l.strip()[:250] for l in o.splitlines() if re.search(r"SKIP|skip", l)][:6], "untangle": [l.strip()[:300] for l in o.splitlines() if "Untangle" in l][:4]})
        if c == 0 or fails: break
    res["page_test_" + ver] = runs
c, o = run("stage4_runner", ["python3", "-B", "08-tooling/sen0401_stage4_gates_v1_2_0.py", NN]); res["stage4"] = {"exit": c, "lines": [l for l in o.splitlines() if re.search(r"PASS|FAIL|NOT_MEASURED|CANNOT_RUN", l)][:30]}
for k in ("Research", "Deck", "Page"):
    c, o = run("chapter_check_" + k, ["python3", "-B", "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py", "%s/Ch%s" % (k, NN)]); res["check_" + k] = {"exit": c, "tail": o.strip().splitlines()[-2:]}
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
res["sha256"] = {os.path.relpath(page, R): sha(page)}
import glob
for p in glob.glob(os.path.join(R, "**", "*%s*" % PV), recursive=True):
    if os.path.isfile(p) and ".git" not in p and "verify" not in p and "ch%s" % NN in p and p.endswith((".ttl", ".json", ".html")): res["sha256"][os.path.relpath(p, R)] = sha(p)
res["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
json.dump(res, open(os.path.join(D, "summary.json"), "w"), indent=1); print(json.dumps(res, indent=1)[:6000])
